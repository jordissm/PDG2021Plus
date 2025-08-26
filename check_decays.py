#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
check_decays.py — Validate decay tables for Thermal-FIST or SMASH formats, with a compact summary.

Usage
-----
  ./check_decays.py --particle-list /path/to/particle/list --decays /path/to/decays/file --format {Thermal-FIST|SMASH}

Options
-------
  --err-br-tol FLOAT   : error tolerance for |sum(BR)-1| (default: 1e-2)
  --warn-br-tol FLOAT  : warning tolerance for |sum(BR)-1| (default: 1e-6)
  --strict-stable      : Thermal-FIST only; stable=1 with decays -> error (default warn)
  --no-B-conservation   : disable baryon number conservation checks
  --no-Q-conservation   : disable electric charge conservation checks
  --no-S-conservation   : disable strangeness conservation checks
  --no-C-conservation   : disable charm number conservation checks
  --summary-only       : suppress detailed messages, show only the summary
  --no-rich            : disable rich output even if available

Exit codes
----------
  0 = all checks passed
  1 = any error
"""

from __future__ import annotations
import sys
import argparse
import numpy as np
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# --- Ensure UTF-8 console output on all platforms ---
def _ensure_utf8_stdio() -> None:
    # Python 3.7+: reconfigure; fallback: wrap with TextIOWrapper
    import io
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name)
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            try:
                wrapper = io.TextIOWrapper(stream.buffer, encoding="utf-8", errors="replace")
                setattr(sys, name, wrapper)
            except Exception:
                pass


# -------- Optional rich pretty output --------
_RICH_AVAILABLE = False
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.rule import Rule
    from rich.text import Text
    _RICH_AVAILABLE = True
except Exception:
    Console = None

# ------------------------------ Data types ------------------------------ #

@dataclass(frozen=True)
class QN:
    B: int
    Q: int
    S: int
    C: int

@dataclass(frozen=True)
class Particle:
    pdg: int
    name: Optional[str]        # None when not relevant
    stable: Optional[int]      # None for SMASH
    mass: Optional[float]
    qn: Optional[QN]           # None for SMASH

@dataclass
class ChannelPDG:
    br: float
    daughters: List[int]

@dataclass
class ChannelName:
    br: float
    L: Optional[int]
    daughters: List[str]

@dataclass
class DecayBlockPDG:
    parent: int
    channels: List[ChannelPDG]

@dataclass
class DecayBlockName:
    parent_name: str
    channels: List[ChannelName]

@dataclass
class ValidationReport:
    ok: bool
    # messages
    warnings: List[str]
    errors: List[str]
    # metrics
    parents_checked: int
    channels_checked: int
    br_sum_violations: int
    br_sum_error_count: int
    br_sum_warning_count: int
    unknown_parent_count: int
    unknown_daughter_count: int
    br_out_of_range_count: int
    empty_daughters_count: int
    baryon_number_violations: int
    electric_charge_violations: int
    strangeness_violations: int
    charm_number_violations: int
    stable_mismatch_count: int

# ------------------------------ Utilities ------------------------------ #

def strip_comment(line: str) -> str:
    return line.split("#", 1)[0].strip()

def normspace(s: str) -> str:
    return " ".join(s.split())

def _inc(d: dict, k: str, v: int = 1) -> None:
    d[k] = d.get(k, 0) + v


import unicodedata
from typing import Dict, List, Set, Tuple, Optional

# --- Normalization primitives (keep your existing alias and digit helpers alongside) ---

# Aliases (e.g., νe in decays ↔ ve in table)
_ALIAS_NAME: Dict[str, str] = {"νe": "ve", "ν_e": "ve", "nu_e": "ve", "nu e": "ve"}

# Overbar/macron code points
_ANTI_COMBINING = {0x0304, 0x0305, 0x033F}  # MACRON, OVERLINE, DOUBLE OVERLINE
_ANTI_SPACING   = {0x00AF}                  # MACRON (spacing)

# Charge symbols
_PLUS_ASCII = "+"
_MINUS_ASCII = "-"
_MINUS_UNICODE = "−"  # U+2212
_PLUS_SUPER = "⁺"
_MINUS_SUPER = "⁻"
_ZERO_ASCII = "0"
_ZERO_SUPER = "⁰"

# Subscript digit maps (keep if you already have these)
_SUB_TO_ASCII = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
_ASCII_TO_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

def canon_name(s: str) -> str:
    """Collapse whitespace and normalize Unicode lookalikes."""
    return unicodedata.normalize("NFKC", " ".join(s.split()))

def _remove_overbar(name: str) -> str:
    """Strip overbar/macron (combining or spacing) anywhere in the string."""
    if not name:
        return name
    decomp = unicodedata.normalize("NFKD", name)
    cleaned = "".join(
        ch for ch in decomp
        if (ord(ch) not in _ANTI_COMBINING) and (ord(ch) not in _ANTI_SPACING)
    )
    return unicodedata.normalize("NFKC", cleaned)

def _ascii_digits_to_subscripts_after_letter(s: str) -> str:
    """convert ASCII digits to subscripts only when immediately after a letter (K1→K₁; (1270) unchanged)."""
    out: List[str] = []
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        out.append(ch); i += 1
        if ch.isalpha() and i < n and s[i].isdigit():
            j = i
            while j < n and s[j].isdigit():
                out.append(s[j].translate(_ASCII_TO_SUB))
                j += 1
            i = j
    return "".join(out)

def _generate_digit_variants(key: str) -> List[str]:
    """Return variants with subscript↔ASCII digits (K₁↔K1), preserving non-digit parts like (1270)."""
    variants = [key]
    sub_to_ascii = key.translate(_SUB_TO_ASCII)
    if sub_to_ascii != key:
        variants.append(sub_to_ascii)
    ascii_to_sub = _ascii_digits_to_subscripts_after_letter(key)
    if ascii_to_sub != key:
        variants.append(ascii_to_sub)
    if sub_to_ascii != key:
        ascii_to_sub2 = _ascii_digits_to_subscripts_after_letter(sub_to_ascii)
        if ascii_to_sub2 not in variants:
            variants.append(ascii_to_sub2)
    return variants

# --- NEW: trailing-charge cluster parsing & variant generation ---

def _parse_trailing_charge_cluster(name: str) -> Tuple[str, Optional[Tuple[str, int]]]:
    """
    Parse trailing charge cluster at end of the string.
    Returns (base_name, (sign, magnitude)) where sign in {'+','-','0'} and magnitude in {1,2} (0→1).
    Recognizes: '+', '++', '⁺', '⁺⁺', '-', '--', '−', '−−', '⁻', '⁻⁻', '0', '⁰'.
    """
    if not name:
        return name, None
    # Normalize lookalikes first (NFKC already applied via canon_name before this typically)
    last = name[-1]
    # zero
    if last in (_ZERO_ASCII, _ZERO_SUPER):
        return name[:-1], ("0", 1)

    # collect trailing plus/minus marks (ASCII '+', '-', Unicode '−', superscript '⁺','⁻')
    marks: List[str] = []
    i = len(name) - 1
    while i >= 0:
        ch = name[i]
        if ch in (_PLUS_ASCII, _PLUS_SUPER, _MINUS_ASCII, _MINUS_UNICODE, _MINUS_SUPER):
            marks.append(ch)
            i -= 1
        else:
            break

    if not marks:
        return name, None

    # Limit magnitude to 1 or 2 (Δ family uses up to ±2)
    cluster = "".join(reversed(marks))[:2]
    # deduce sign if all marks are + or all are - (accept ASCII '-', Unicode '−', superscript '⁻' as minus)
    if all(c in (_PLUS_ASCII, _PLUS_SUPER) for c in cluster):
        mag = min(2, len(cluster))
        return name[:-mag], ("+", mag)
    if all(c in (_MINUS_ASCII, _MINUS_UNICODE, _MINUS_SUPER) for c in cluster):
        mag = min(2, len(cluster))
        return name[:-mag], ("-", mag)

    # Mixed or unexpected pattern → treat as no charge cluster
    return name, None

def _charge_cluster_variants(base: str, sign: str, mag: int) -> List[str]:
    """
    For base name and sign ('+','-','0') with magnitude (1 or 2),
    return variants using ASCII, Unicode minus, and superscripts.
    """
    out: List[str] = []
    if sign == "0":
        out.extend([base + _ZERO_ASCII, base + _ZERO_SUPER])
    elif sign == "+":
        plus_ascii = _PLUS_ASCII * mag
        plus_super = _PLUS_SUPER * mag
        out.extend([base + plus_ascii, base + plus_super])
    elif sign == "-":
        minus_ascii = _MINUS_ASCII * mag
        minus_uni   = _MINUS_UNICODE * mag
        minus_super = _MINUS_SUPER * mag
        out.extend([base + minus_ascii, base + minus_uni, base + minus_super])
    # dedup
    seen: Set[str] = set()
    return [k for k in out if (k not in seen and not seen.add(k))]

def _default_charge_cluster_variants(base: str) -> List[str]:
    """
    Heuristic: if a bare name appears with no explicit charge, try the physically
    standard charge for certain families. For Ω baryons, that is −1.
    This also covers excited states like 'Ω(2012)'.
    """
    out: List[str] = []
    if base and base[0] == "Ω":
        # Try minus in ASCII, Unicode minus, and superscript forms
        out.extend([base + "-", base + "−", base + "⁻"])
    # de-dup preserving order
    seen: Set[str] = set()
    dedup: List[str] = []
    for k in out:
        if k not in seen:
            seen.add(k)
            dedup.append(k)
    return dedup

def _flip_charge(sign: str) -> Optional[str]:
    if sign == "+": return "-"
    if sign == "-": return "+"
    if sign == "0": return "0"
    return None

def _candidate_lookup_keys(raw_name: str) -> List[str]:
    """
    (Updated) Robust candidate generator:
      - exact + alias
      - unbarred + alias
      - digit-notation variants for all above
      - if trailing charge cluster present → try base, same-charge, flipped-charge variants
      - if NO trailing charge cluster present → try a default charge heuristic (e.g. Ω→Ω⁻)
    """
    n = canon_name(raw_name)
    seeds: List[str] = [n]

    alias = _ALIAS_NAME.get(n)
    if alias:
        seeds.append(alias)

    unbar = _remove_overbar(n)
    if unbar != n:
        seeds.append(unbar)
        alias_unbar = _ALIAS_NAME.get(unbar)
        if alias_unbar:
            seeds.append(alias_unbar)

    keys: List[str] = []
    # Base seeds and digit-notation variants
    for seed in seeds:
        keys.extend(_generate_digit_variants(seed))

    # Handle trailing charge clusters on both original and unbarred forms
    applied_default_for_uncharged = False
    for seed in (n, unbar):
        base, charge = _parse_trailing_charge_cluster(seed)
        if charge is not None and base:
            sign, mag = charge
            # 1) multiplet base
            keys.extend(_generate_digit_variants(base))
            # 2) same-charge variants
            for k in _charge_cluster_variants(base, sign, mag):
                keys.extend(_generate_digit_variants(k))
            # 3) flipped-charge variants
            flip = _flip_charge(sign)
            if flip is not None:
                for k in _charge_cluster_variants(base, flip, mag):
                    keys.extend(_generate_digit_variants(k))
        elif base:
            # No explicit charge: try default charge heuristic once.
            if not applied_default_for_uncharged:
                keys.extend(_generate_digit_variants(base))
                for k in _default_charge_cluster_variants(base):
                    keys.extend(_generate_digit_variants(k))
                applied_default_for_uncharged = True

    # de-dup preserving order
    seen: Set[str] = set()
    out: List[str] = []
    for k in keys:
        if k and k not in seen:
            seen.add(k)
            out.append(k)
    return out

def _is_known_name(name: str, known_names: Set[str]) -> bool:
    return any(k in known_names for k in _candidate_lookup_keys(name))


def _to_superscript_charge(name: str) -> str:
    base, charge = _parse_trailing_charge_cluster(name)
    if not charge or not base:
        return name
    sign, mag = charge
    if sign == "+":
        return base + ("⁺" * mag)
    if sign == "-":
        return base + ("⁻" * mag)
    # sign == "0"
    return base + "⁰"

def pretty_particle(name: str) -> str:
    # Start from your canonical token, then "beautify" for display.
    n = _ascii_digits_to_subscripts_after_letter(name)  # K1 -> K₁ (but leaves (1270) intact)
    n = _to_superscript_charge(n)                       # K- -> K⁻, Δ++ -> Δ⁺⁺
    return n


# ------------------------------ Parsing: PARTICLE LISTS ------------------------------ #

def parse_particle_list_thermal(particle_list_path: Path) -> Dict[int, Particle]:
    """
    Thermal-FIST list.dat style:
    pdgid name stable mass[GeV] degeneracy statistics B Q S C |S| |C| width[GeV] threshold[GeV]
    """
    particles: Dict[int, Particle] = {}
    for raw in particle_list_path.read_text(encoding="utf-8").splitlines():
        line = strip_comment(raw)
        if not line:
            continue
        parts = line.split()
        # Expect at least through C (index 9)
        try:
            pdg = int(parts[0])
            name = parts[1]
            stable = int(parts[2])
            mass = float(parts[3])
            B = int(parts[6]); Q = int(parts[7]); S = int(parts[8]); C = int(parts[9])
        except Exception:
            continue  # header/malformed
        particles[pdg] = Particle(pdg=pdg, name=name, stable=stable, mass=mass, qn=QN(B=B, Q=Q, S=S, C=C))
    if not particles:
        raise ValueError(f"No particles parsed from '{particle_list_path}'.")
    return particles

def parse_particle_list_smash(particle_list_path: Path) -> Tuple[Dict[int, Particle], Dict[str, List[int]]]:
    """
    SMASH Particles style:
    NAME MASS WIDTH PARITY PDG [PDG...]
    """
    pdg_map: Dict[int, Particle] = {}
    name_to_pdgs: Dict[str, List[int]] = {}
    for raw in particle_list_path.read_text(encoding="utf-8").splitlines():
        line = strip_comment(raw)
        if not line:
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        name = canon_name(parts[0])
        try:
            mass = float(parts[1])
        except Exception:
            continue
        pdgs: List[int] = []
        ok_tail = True
        for tok in parts[4:]:
            try:
                pdgs.append(int(tok))
            except Exception:
                ok_tail = False
                break
        if not ok_tail or not pdgs:
            continue
        name_to_pdgs.setdefault(name, [])
        for pdg in pdgs:
            name_to_pdgs[name].append(pdg)
            if pdg not in pdg_map:
                pdg_map[pdg] = Particle(pdg=pdg, name=name, stable=None, mass=mass, qn=None)
    if not pdg_map:
        raise ValueError(f"No particles parsed from '{particle_list_path}'.")
    return pdg_map, name_to_pdgs

# ------------------------------ Parsing: DECAY LISTS ------------------------------ #

def parse_decays_thermal(decays_path: Path) -> List[DecayBlockPDG]:
    """
    PDG-based format:
      parent
      n_channels
      BR  d1 d2 ...
      ...
    """
    tokens: List[str] = []
    for raw in decays_path.read_text(encoding="utf-8").splitlines():
        s = strip_comment(raw)
        if s:
            tokens.append(s)

    i = 0
    n = len(tokens)
    blocks: List[DecayBlockPDG] = []

    def need(cond: bool, msg: str):
        if not cond:
            raise ValueError(msg)

    while i < n:
        parent_str = tokens[i]; i += 1
        need(parent_str.lstrip("-").isdigit(), f"Expected PDG ID, got '{parent_str}'")
        parent = int(parent_str)

        need(i < n, f"Missing number of channels after parent {parent}")
        nch_str = tokens[i]; i += 1
        need(nch_str.isdigit(), f"Expected integer number of channels after parent {parent}")
        nch = int(nch_str)

        channels: List[ChannelPDG] = []
        for k in range(nch):
            need(i < n, f"Missing channel {k+1}/{nch} for parent {parent}")
            parts = tokens[i].split(); i += 1
            need(len(parts) >= 2, f"[PDG {parent}] Channel {k+1}: need BR and ≥1 daughter")
            try:
                br = float(parts[0])
            except Exception:
                raise ValueError(f"[PDG {parent}] Channel {k+1}: invalid BR '{parts[0]}'")
            try:
                daughters = [int(x) for x in parts[1:]]
            except Exception:
                raise ValueError(f"[PDG {parent}] Channel {k+1}: invalid daughters '{' '.join(parts[1:])}'")
            channels.append(ChannelPDG(br=br, daughters=daughters))
        blocks.append(DecayBlockPDG(parent=parent, channels=channels))
    return blocks

def parse_decays_smash(decays_path: Path) -> List[DecayBlockName]:
    """
    SMASH 'Decays' style:
      <ParentName>
      <BR> <L> <d1> <d2> ...
      (blank/comment lines ignored; new parent starts with a non-number token)
    """
    blocks: List[DecayBlockName] = []
    lines = decays_path.read_text(encoding="utf-8").splitlines()

    parent: Optional[str] = None
    current: List[ChannelName] = []

    def flush():
        nonlocal parent, current, blocks
        if parent is not None:
            blocks.append(DecayBlockName(parent_name=parent, channels=current))
        parent = None
        current = []

    for raw in lines:
        line = strip_comment(raw)
        if not line:
            continue
        head = line.split()[0]
        # Channel line starts with float
        is_channel = False
        try:
            float(head); is_channel = True
        except Exception:
            is_channel = False

        if not is_channel:
            flush()
            parent = canon_name(line)
            continue

        parts = line.split()
        if len(parts) < 3:
            raise ValueError(f"[{parent}] Invalid channel line: '{line}'")
        br = float(parts[0])
        try:
            L = int(parts[1])
        except Exception:
            L = None
        daughters = [canon_name(x) for x in parts[2:]]
        current.append(ChannelName(br=br, L=L, daughters=daughters))

    flush()
    return blocks

# ------------------------------ Validation helpers ------------------------------ #

def _classify_and_add_msg(errors: List[str], msg: str) -> None:
    """
    Adds the message to errors. We keep plain strings but later indent specific categories.
    """
    errors.append(msg)

# ------------------------------ Validation: Thermal-FIST ------------------------------ #

def get_qn_thermal(particles: Dict[int, Particle], pdg: int) -> QN:
    # Exact PDG match
    p = particles.get(pdg)
    if p is not None and p.qn is not None:
        return p.qn

    # Fallback: use |pdg| and flip quantum numbers for antiparticles
    apdg = abs(pdg)
    p_abs = particles.get(apdg)
    if p_abs is not None and p_abs.qn is not None:
        base = p_abs.qn
        sgn = 1 if pdg > 0 else -1
        return QN(B=sgn * base.B, Q=sgn * base.Q, S=sgn * base.S, C=sgn * base.C)

    raise KeyError(f"Unknown PDG {pdg}")

def get_stable_thermal(particles: Dict[int, Particle], pdg: int) -> int:
    # Exact PDG match
    p = particles.get(pdg)
    if p is not None and p.stable is not None:
        return int(p.stable)

    # Fallback: use |pdg|
    apdg = abs(pdg)
    p_abs = particles.get(apdg)
    if p_abs is not None and p_abs.stable is not None:
        return int(p_abs.stable)

    raise KeyError(f"Unknown PDG {pdg}")


def validate_thermal(
    particles: Dict[int, Particle],
    blocks: List[DecayBlockPDG],
    err_br_tol: float,
    warn_br_tol: float,
    strict_stable: bool,
    check_B: bool,
    check_Q: bool,
    check_S: bool,
    check_C: bool,
) -> ValidationReport:
    errors: List[str] = []
    warnings: List[str] = []
    metrics = {
        "parents_checked": len(blocks),
        "channels_checked": 0,
        "br_sum_violations": 0,
        "br_sum_error_count": 0,
        "br_sum_warning_count": 0,
        "unknown_parent_count": 0,
        "unknown_daughter_count": 0,
        "br_out_of_range_count": 0,
        "empty_daughters_count": 0,
        "baryon_number_violations": 0,
        "electric_charge_violations": 0,
        "strangeness_violations": 0,
        "charm_number_violations": 0,
        "stable_mismatch_count": 0,
    }

    parents_in_list = set(particles.keys()) | {-k for k in particles.keys()}

    # Loop over decay blocks
    for blk in blocks:
        if blk.parent not in parents_in_list and abs(blk.parent) not in particles:
            _classify_and_add_msg(errors, f"[PDG {blk.parent}] Parent not found in particle list.")
            _inc(metrics, "unknown_parent_count")

        # Stable vs decays
        try:
            stable = get_stable_thermal(particles, blk.parent)
            if stable == 1 and len(blk.channels) > 0:
                _inc(metrics, "stable_mismatch_count")
                msg = f"[PDG {blk.parent}] has decays listed but is marked stable in particle list."
                (errors if strict_stable else warnings).append(msg)
        except KeyError as e:
            _classify_and_add_msg(errors, f"[PDG {blk.parent}] {e}")
            _inc(metrics, "unknown_parent_count")

        # BR checks
        total = 0.0
        # Loop over decay channels
        for idx, ch in enumerate(blk.channels, start=1):
            _inc(metrics, "channels_checked")
            # Check if BR is valid
            if not (0.0 <= ch.br <= 1.0):
                _classify_and_add_msg(errors, f"[PDG {blk.parent}] Channel {idx}: BR out of range {ch.br}")
                _inc(metrics, "br_out_of_range_count")
            # Check if number of daughters is valid
            if len(ch.daughters) == 0:
                _classify_and_add_msg(errors, f"[PDG {blk.parent}] Channel {idx}: no daughters")
                _inc(metrics, "empty_daughters_count")
            total += ch.br

        # Check if BR sum is valid
        delta = abs(total - 1.0)
        if delta > err_br_tol:
            _classify_and_add_msg(errors, f"[PDG {blk.parent}] BR sum = {total:.6f} (Δ={delta:.2e}) > error tol {err_br_tol}")
            _inc(metrics, "br_sum_violations"); _inc(metrics, "br_sum_error_count")
        elif delta > warn_br_tol:
            warnings.append(f"[PDG {blk.parent}] BR sum = {total:.6f} (Δ={delta:.2e}) > warning tol {warn_br_tol}")
            _inc(metrics, "br_sum_violations"); _inc(metrics, "br_sum_warning_count")

        # Conservation laws
        try:
            qnp = get_qn_thermal(particles, blk.parent)
        except KeyError as e:
            _classify_and_add_msg(errors, f"[PDG {blk.parent}] {e}")
            continue

        for idx, ch in enumerate(blk.channels, start=1):
            B = Q = S = C = 0
            unknowns: List[int] = []
            for d in ch.daughters:
                try:
                    q = get_qn_thermal(particles, d)
                except KeyError:
                    unknowns.append(d)
                    continue
                B += q.B; Q += q.Q; S += q.S; C += q.C
            if unknowns:
                _classify_and_add_msg(errors, f"[PDG {blk.parent}] Channel {idx}: Unknown daughter PDG IDs {unknowns}")
                _inc(metrics, "unknown_daughter_count", len(unknowns))
                continue
            if qnp.B != B:
                _classify_and_add_msg(errors, f"[PDG {blk.parent}] Channel {idx}: baryon number not conserved (B_parent={qnp.B}, B_daughters={B})")
                _inc(metrics, "baryon_number_violations")
            if qnp.Q != Q:
                _classify_and_add_msg(errors, f"[PDG {blk.parent}] Channel {idx}: electric charge not conserved (Q_parent={qnp.Q}, Q_daughters={Q})")
                _inc(metrics, "electric_charge_violations")
            if qnp.S != S:
                _classify_and_add_msg(errors, f"[PDG {blk.parent}] Channel {idx}: strangeness not conserved (S_parent={qnp.S}, S_daughters={S})")
                _inc(metrics, "strangeness_violations")
            if qnp.C != C:
                _classify_and_add_msg(errors, f"[PDG {blk.parent}] Channel {idx}: charm number not conserved (C_parent={qnp.C}, C_daughters={C})")
                _inc(metrics, "charm_number_violations")


    ok = len(errors) == 0
    return ValidationReport(
        ok=ok,
        errors=errors,
        warnings=warnings,
        **metrics,
    )

# ------------------------------ Validation: SMASH ------------------------------ #

def validate_smash(
    pdg_map: Dict[int, Particle],
    name_to_pdgs: Dict[str, List[int]],
    blocks: List[DecayBlockName],
    err_br_tol: float,
    warn_br_tol: float,
) -> ValidationReport:
    errors: List[str] = []
    warnings: List[str] = []
    metrics = {
        "parents_checked": len(blocks),
        "channels_checked": 0,
        "br_sum_violations": 0,
        "br_sum_error_count": 0,
        "br_sum_warning_count": 0,
        "unknown_parent_count": 0,
        "unknown_daughter_count": 0,
        "br_out_of_range_count": 0,
        "empty_daughters_count": 0,
        "electric_charge_violations": np.nan,
        "baryon_number_violations": np.nan,
        "strangeness_violations": np.nan,
        "charm_number_violations": np.nan,
        "stable_mismatch_count": np.nan,
    }

    known_names: Set[str] = set(name_to_pdgs.keys())

    for blk in blocks:
        parent = blk.parent_name
        parent_disp = pretty_particle(parent)

        if not _is_known_name(parent, known_names):
            _classify_and_add_msg(errors, f"[{parent_disp}] Parent name not found in particle list.")
            _inc(metrics, "unknown_parent_count")
        total = 0.0

        for idx, ch in enumerate(blk.channels, start=1):
            _inc(metrics, "channels_checked")
            if not (0.0 <= ch.br <= 1.0):
                _classify_and_add_msg(errors, f"[{parent_disp}] Channel {idx}: BR out of range {ch.br}")
                _inc(metrics, "br_out_of_range_count")
            if len(ch.daughters) == 0:
                _classify_and_add_msg(errors, f"[{parent_disp}] Channel {idx}: no daughters")
                _inc(metrics, "empty_daughters_count")

            missing = [d for d in ch.daughters if not _is_known_name(d, known_names)]
            if missing:
                missing_disp = [pretty_particle(d) for d in missing]
                _classify_and_add_msg(errors, f"[{parent_disp}] Channel {idx}: unknown daughter names {missing_disp}")
                _inc(metrics, "unknown_daughter_count", len(missing))

            total += ch.br

        delta = abs(total - 1.0)
        if delta > err_br_tol:
            _classify_and_add_msg(
                errors,
                f"[{parent_disp}] BR sum = {total:.6f} (Δ={delta:.2e}) > error tol {err_br_tol}",
            )
            _inc(metrics, "br_sum_violations"); _inc(metrics, "br_sum_error_count")
        elif delta > warn_br_tol:
            warnings.append(
                f"[{parent_disp}] BR sum = {total:.6f} (Δ={delta:.2e}) > warning tol {warn_br_tol}"
            )
            _inc(metrics, "br_sum_violations"); _inc(metrics, "br_sum_warning_count")


    ok = len(errors) == 0
    return ValidationReport(
        ok=ok,
        errors=errors,
        warnings=warnings,
        **metrics,  # all ints; matches ValidationReport fields
    )

# ------------------------------ Pretty printing ------------------------------ #

_ERR_TAGS = (
    "Parent not found", 
    "Unknown daughter", 
    "No daughters",
    "Charge not conserved", 
    "Baryon number not conserved",
    "Strangeness not conserved", 
    "Charm number not conserved",
    "BR out of range", "BR sum ="
)

def _indent_lines(lines: List[str], prefix: str = "  • ") -> List[str]:
    return [f"{prefix}{ln}" for ln in lines]

def print_detailed(report: ValidationReport, use_rich: bool) -> None:
    # Partition errors/warnings to indent everything inside their sections
    err_lines = report.errors
    warn_lines = report.warnings

    if use_rich:
        console = Console()                                                             # type: ignore
        if warn_lines:
            console.print(Rule("[bold yellow]Warnings[/bold yellow]"))                  # type: ignore
            for ln in _indent_lines(warn_lines):
                console.print(ln, style="yellow", markup=False)
        if err_lines:
            console.print(Rule("[bold red]Errors[/bold red]"))                          # type: ignore
            for ln in _indent_lines(err_lines):
                console.print(ln, style="red", markup=False)
        if not err_lines and not warn_lines:
            console.print("[bold green]No errors or warnings.[/bold green]")
    else:
        if warn_lines:
            print("Warnings:", file=sys.stderr)
            for ln in _indent_lines(warn_lines, prefix="  - "):
                print(ln)
        if err_lines:
            print("Errors:", file=sys.stderr)
            for ln in _indent_lines(err_lines, prefix="  - "):
                print(ln, file=sys.stderr)
        if not err_lines and not warn_lines:
            print("No errors or warnings.")

def print_summary(report: ValidationReport, format_name: str, use_rich: bool) -> None:
    if use_rich:
        console = Console()                                                             # type: ignore
        status_style = "bold green" if report.ok else "bold red"
        panel_title = f"[{status_style}]STATUS: {'OK' if report.ok else 'FAIL'}[/]"
        table = Table(show_header=True, header_style="bold")                            # type: ignore
        table.add_column("Metric", justify="left")
        table.add_column("Value", justify="right")

        rows = [
            ("Parents checked", report.parents_checked),
            ("Channels checked", report.channels_checked),
            ("Warnings", len(report.warnings)),
            ("Total BR sum violations", report.br_sum_violations),
            ("  ↳ BR sum warnings", report.br_sum_warning_count),
            ("Errors", len(report.errors)),
            ("  ↳ BR sum errors", report.br_sum_error_count),
            ("  ↳ Unknown parents", report.unknown_parent_count),
            ("  ↳ Unknown daughters", report.unknown_daughter_count),
            ("  ↳ BR out of range", report.br_out_of_range_count),
            ("  ↳ Empty daughter lists", report.empty_daughters_count),
            ("  ↳ Baryon number violations", report.baryon_number_violations),
            ("  ↳ Electric charge violations", report.electric_charge_violations),
            ("  ↳ Strangeness violations", report.strangeness_violations),
            ("  ↳ Charm number violations", report.charm_number_violations),
            ("  ↳ Stable/unstable mismatches", report.stable_mismatch_count),
        ]
        for k, v in rows:
            table.add_row(k, str(v))

        console.print(Panel(table, title=panel_title, border_style="cyan"))             # type: ignore
    else:
        print(f"=== Summary ({format_name.upper()}) ===")
        print(f"STATUS: {'OK' if report.ok else 'FAIL'}")
        print(f"- Parents checked:            {report.parents_checked}")
        print(f"- Channels checked:           {report.channels_checked}")
        print(f"- Warnings:                   {len(report.warnings)}")
        print(f"- Total BR sum violations:    {report.br_sum_violations}")
        print(f"    ↳ BR sum warnings:        {report.br_sum_warning_count}")
        print(f"- Errors:                     {len(report.errors)}")
        print(f"    ↳ BR sum errors:          {report.br_sum_error_count}")
        print(f"    ↳ Unknown parents:            {report.unknown_parent_count}")
        print(f"    ↳ Unknown daughters:          {report.unknown_daughter_count}")
        print(f"    ↳ BR out of range:            {report.br_out_of_range_count}")
        print(f"    ↳ Empty daughter lists:       {report.empty_daughters_count}")
        print(f"    ↳ Baryon number violations:          {report.baryon_number_violations}")
        print(f"    ↳ Electric charge violations:          {report.electric_charge_violations}")
        print(f"    ↳ Strangeness violations:     {report.strangeness_violations}")
        print(f"    ↳ Charm number violations:           {report.charm_number_violations}")
        print(f"    ↳ Stable/unstable mismatches:          {report.stable_mismatch_count}")

# ------------------------------ CLI ------------------------------ #

def main(argv=None) -> int:

    ap = argparse.ArgumentParser(description="Validate particle decay tables (Thermal-FIST or SMASH).")

    # Required arguments
    ap.add_argument("-p", "--particle-list", type=Path, required=True, help="Path to particle list file")
    # ap.add_argument("--particle-list-format", choices=["Thermal-FIST", "SMASH"], required=True, help="Format of particle list")
    ap.add_argument("-d", "--decays", type=Path, required=True, help="Path to decay list file")
    # ap.add_argument("--decays-format", choices=["Thermal-FIST", "SMASH"], required=True, help="Format of decay list")
    ap.add_argument("-f", "--format", choices=["Thermal-FIST", "SMASH"], required=True, help="Format of the input files")

    # Optional arguments
    # Tolerance for BRs sum check
    ap.add_argument("--err-br-tol", type=float, default=1e-2,
                    help="ABS error tolerance for |sum(BR)-1| to count as ERROR (default: 1e-2 = 1%)")
    ap.add_argument("--warn-br-tol", type=float, default=1e-6,
                    help="ABS tolerance for |sum(BR)-1| to count as WARNING (default: 1e-6)")

    # Stable conditions
    ap.add_argument("--strict-stable", action="store_true", help="Flag particles marked as stable but with decays listed")

    # Charge conservation
    ap.add_argument("--no-B-conservation", action="store_true", help="Disable B conservation checks")
    ap.add_argument("--no-Q-conservation", action="store_true", help="Disable Q conservation checks")
    ap.add_argument("--no-S-conservation", action="store_true", help="Disable S conservation checks")
    ap.add_argument("--no-C-conservation", action="store_true", help="Disable C conservation checks")

    # Logging options    
    ap.add_argument("--summary-only", action="store_true", help="Suppress detailed messages; show compact summary")
    ap.add_argument("--no-rich", action="store_true", help="Disable rich output even if available")

    # Parse arguments
    args = ap.parse_args(argv)

    _ensure_utf8_stdio()

    # Fix tolerances if needed
    if args.warn_br_tol > args.err_br_tol:
        print("[config] --warn-br-tol is greater than --err-br-tol; adjusting warn to equal err.",
              file=sys.stderr)
        args.warn_br_tol = args.err_br_tol

    # Determine rich output usage
    use_rich = (_RICH_AVAILABLE and (not args.no_rich))

    # Parse particle list
    try:
        if args.format == "Thermal-FIST":
            particles = parse_particle_list_thermal(args.particle_list)
            pdg_map = particles
            name_to_pdgs = None
        elif args.format == "SMASH":
            pdg_map, name_to_pdgs = parse_particle_list_smash(args.particle_list)
            particles = None
        else:
            print("[error] Unsupported format.", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"[particle list parse error] {e}", file=sys.stderr)
        return 1

    # Parse decay list
    try:
        if args.format == "Thermal-FIST":
            dec_blocks_pdg = parse_decays_thermal(args.decays)
            dec_blocks_name = None
        elif args.format == "SMASH":
            dec_blocks_name = parse_decays_smash(args.decays)
            dec_blocks_pdg = None
        else:
            print("[error] Unsupported format.", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"[decay list parse error] {e}", file=sys.stderr)
        return 1

    # Validate
    if args.format == "Thermal-FIST":
        report = validate_thermal(
            particles=particles,                                                        # type: ignore
            blocks=dec_blocks_pdg,                                                      # type: ignore
            err_br_tol=args.err_br_tol,
            warn_br_tol=args.warn_br_tol,
            strict_stable=args.strict_stable,
            check_B=not args.no_B_conservation,
            check_Q=not args.no_Q_conservation,
            check_S=not args.no_S_conservation,
            check_C=not args.no_C_conservation,
        )
    elif args.format == "SMASH":
        report = validate_smash(
            pdg_map=pdg_map,
            name_to_pdgs=name_to_pdgs,                                                  # type: ignore
            blocks=dec_blocks_name,                                                     # type: ignore
            err_br_tol=args.err_br_tol,
            warn_br_tol=args.warn_br_tol,
        )
    else:
        report = None
        print("[error] Unsupported format.", file=sys.stderr)

    # Detailed output (unless summary-only)
    if not args.summary_only:
        print_detailed(report, use_rich=use_rich)                                       # type: ignore

    # Compact summary (always)
    print_summary(report, args.format, use_rich=use_rich)                               # type: ignore

    return 0 if report.ok else 1

if __name__ == "__main__":
    sys.exit(main())