#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Validate a decay table against a SMASH-like particle list.

Inputs
------
1) Particle list file (e.g., list.dat as shown)
2) Decay table in your custom format (blocks with PDG, #channels, then BR + daughters)

Checks
------
- Branching ratios in each block are within [0, 1] and sum to ~1
- Conservation of Q, B, S, C for every decay channel
- All PDG IDs are known (anti-particles auto-supported via sign flip)
- Count of channels matches declared number
- Optional: warn/error if a 'stable' particle has decays

Usage
-----
  ./check_decays.py --plist list.dat --decays decays.txt
Options
-------
  --abs-tol-br  5e-4   | absolute tolerance for sum(BR)≈1
  --rel-tol-br  1e-6   | relative tolerance for sum(BR)≈1
  --strict-stable       | treat decays of stable=1 parents as an error (default: warn)
  --no-BSCC             | only check charge conservation (skip B,S,C)
  --show-ok             | print a success line on pass
Exit codes
----------
  0 = all checks passed
  1 = any error
"""

from __future__ import annotations
import sys
import math
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

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
    name: str
    stable: int
    mass: float
    qn: QN

@dataclass
class Channel:
    br: float
    daughters: List[int]

@dataclass
class DecayBlock:
    parent: int
    channels: List[Channel]

# ------------------------------ Parsing ------------------------------ #

def parse_particle_list(plist_path: Path) -> Dict[int, Particle]:
    """
    Parse SMASH-style list.dat.
    Expected columns (whitespace separated):
    pdgid, name, stable, mass[GeV], degeneracy, statistics, B, Q, S, C, |S|, |C|, width[GeV], threshold[GeV]
    Lines starting with '#' or blank are ignored.
    """
    particles: Dict[int, Particle] = {}
    for raw in plist_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        # handle malformed or header-like lines gracefully
        try:
            pdg = int(parts[0])
        except Exception:
            continue
        # name is the 2nd token (no spaces in provided sample)
        try:
            name = parts[1]
            stable = int(parts[2])
            mass = float(parts[3])
            # parts[4], parts[5] = degeneracy, statistics (unused here)
            B = int(parts[6])
            Q = int(parts[7])
            S = int(parts[8])
            C = int(parts[9])
        except Exception as e:
            raise ValueError(f"Malformed particle list line:\n{raw}") from e

        particles[pdg] = Particle(
            pdg=pdg,
            name=name,
            stable=stable,
            mass=mass,
            qn=QN(B=B, Q=Q, S=S, C=C),
        )
    if not particles:
        raise ValueError(f"No particles parsed from {plist_path}")
    return particles

def parse_decay_table(decays_path: Path) -> List[DecayBlock]:
    """
    Parse the custom decay table format:
      parent
      n_channels
      br  d1 d2 ...
      ...
    """
    txt = decays_path.read_text(encoding="utf-8")

    def strip_comment(s: str) -> str:
        return s.split("#", 1)[0].strip()

    tokens: List[str] = []
    for raw in txt.splitlines():
        s = strip_comment(raw)
        if s:
            tokens.append(s)

    i = 0
    n = len(tokens)
    blocks: List[DecayBlock] = []

    def need(cond: bool, msg: str):
        if not cond:
            raise ValueError(msg)

    while i < n:
        need(i < n, "Unexpected EOF while reading parent PDG")
        parent_str = tokens[i]; i += 1
        need(parent_str.lstrip("-").isdigit(), f"Expected PDG ID, got '{parent_str}'")
        parent = int(parent_str)

        need(i < n, f"Missing number of channels after parent {parent}")
        nch_str = tokens[i]; i += 1
        need(nch_str.isdigit(), f"Expected integer number of channels after parent {parent}, got '{nch_str}'")
        nch = int(nch_str)

        channels: List[Channel] = []
        for k in range(nch):
            need(i < n, f"Missing line for channel {k+1}/{nch} of parent {parent}")
            parts = tokens[i].split()
            i += 1
            need(len(parts) >= 2, f"[PDG {parent}] Channel {k+1}: must have BR and >=1 daughter")
            try:
                br = float(parts[0])
            except Exception:
                raise ValueError(f"[PDG {parent}] Channel {k+1}: invalid BR '{parts[0]}'")
            try:
                daughters = [int(x) for x in parts[1:]]
            except Exception:
                raise ValueError(f"[PDG {parent}] Channel {k+1}: invalid daughter list '{' '.join(parts[1:])}'")
            channels.append(Channel(br=br, daughters=daughters))

        blocks.append(DecayBlock(parent=parent, channels=channels))

    return blocks

# ------------------------------ Utilities ------------------------------ #

def almost_equal(a: float, b: float, tol_abs: float, tol_rel: float) -> bool:
    return abs(a - b) <= max(tol_abs, tol_rel * max(1.0, abs(a), abs(b)))

def get_qn(particles: Dict[int, Particle], pdg: int) -> QN:
    """
    Fetch quantum numbers for PDG, inferring anti-particles by sign flip
    on (B, Q, S, C) if only |pdg| is present.
    """
    if pdg in particles:
        return particles[pdg].qn
    apdg = abs(pdg)
    if apdg in particles:
        base = particles[apdg].qn
        sgn = 1 if pdg > 0 else -1
        return QN(B=sgn * base.B, Q=sgn * base.Q, S=sgn * base.S, C=sgn * base.C)
    raise KeyError(f"Unknown PDG ID {pdg}")

def get_stable_flag(particles: Dict[int, Particle], pdg: int) -> int:
    if pdg in particles:
        return particles[pdg].stable
    apdg = abs(pdg)
    if apdg in particles:
        return particles[apdg].stable  # stable flag is same for anti
    raise KeyError(f"Unknown PDG ID {pdg}")

# ------------------------------ Validation ------------------------------ #

def validate(
    particles: Dict[int, Particle],
    blocks: List[DecayBlock],
    abs_tol_br: float = 5e-4,
    rel_tol_br: float = 1e-6,
    check_BSCC: bool = True,
    strict_stable: bool = False,
) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    # Index for quick lookup of parents defined in decays
    parents_in_list = set(particles.keys()) | {-k for k in particles.keys()}

    for blk in blocks:
        # Parent existence
        if blk.parent not in parents_in_list and abs(blk.parent) not in particles:
            errors.append(f"[PDG {blk.parent}] Parent not found in particle list.")
            # We still try other checks to report more issues.

        # Stable flag vs decays
        try:
            stable = get_stable_flag(particles, blk.parent)
            if stable == 1 and len(blk.channels) > 0:
                msg = f"[PDG {blk.parent}] has decays listed but is marked stable in particle list."
                (errors if strict_stable else warnings).append(msg)
        except KeyError as e:
            errors.append(f"[PDG {blk.parent}] {e}")

        # BR sanity + sum
        total_br = 0.0
        for idx, ch in enumerate(blk.channels, start=1):
            if not (0.0 <= ch.br <= 1.0):
                errors.append(f"[PDG {blk.parent}] Channel {idx}: BR out of range: {ch.br}")
            if len(ch.daughters) == 0:
                errors.append(f"[PDG {blk.parent}] Channel {idx}: no daughters listed")
            total_br += ch.br
        if not almost_equal(total_br, 1.0, abs_tol_br, rel_tol_br):
            errors.append(f"[PDG {blk.parent}] Sum of BRs = {total_br:.6f} (≠ 1.0)")

        # Conservation laws per channel
        try:
            qn_parent = get_qn(particles, blk.parent)
        except KeyError as e:
            errors.append(f"[PDG {blk.parent}] {e}")
            # Can't check conservation without parent QNs
            continue

        for idx, ch in enumerate(blk.channels, start=1):
            unknowns: List[int] = []
            B = Q = S = C = 0
            for d in ch.daughters:
                try:
                    q = get_qn(particles, d)
                except KeyError:
                    unknowns.append(d)
                    continue
                B += q.B
                Q += q.Q
                S += q.S
                C += q.C

            if unknowns:
                errors.append(f"[PDG {blk.parent}] Channel {idx}: Unknown daughter PDG IDs {unknowns}")
                continue

            # Always check charge; optionally others
            if qn_parent.Q != Q:
                errors.append(
                    f"[PDG {blk.parent}] Channel {idx}: charge not conserved "
                    f"(parent Q={qn_parent.Q}, daughters Q={Q}) daughters={ch.daughters}"
                )
            if check_BSCC:
                if qn_parent.B != B:
                    errors.append(
                        f"[PDG {blk.parent}] Channel {idx}: baryon number not conserved "
                        f"(parent B={qn_parent.B}, daughters B={B})"
                    )
                if qn_parent.S != S:
                    errors.append(
                        f"[PDG {blk.parent}] Channel {idx}: strangeness not conserved "
                        f"(parent S={qn_parent.S}, daughters S={S})"
                    )
                if qn_parent.C != C:
                    errors.append(
                        f"[PDG {blk.parent}] Channel {idx}: charm not conserved "
                        f"(parent C={qn_parent.C}, daughters C={C})"
                    )

    ok = len(errors) == 0
    messages = (["All checks passed."] if ok else errors) + (warnings if ok else warnings)
    return ok, messages

# ------------------------------ CLI ------------------------------ #

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Check decay table consistency against a particle list.")
    ap.add_argument("--plist", type=Path, required=True, help="Path to particle list file (e.g., list.dat)")
    ap.add_argument("--decays", type=Path, required=True, help="Path to decay table")
    ap.add_argument("--abs-tol-br", type=float, default=5e-4, help="Absolute tolerance for sum(BR)=1")
    ap.add_argument("--rel-tol-br", type=float, default=1e-6, help="Relative tolerance for sum(BR)=1")
    ap.add_argument("--strict-stable", action="store_true", help="Error (not warn) if stable=1 has decays")
    ap.add_argument("--no-BSCC", action="store_true", help="Only check charge; skip B,S,C conservation")
    ap.add_argument("--show-ok", action="store_true", help="Print a success message when valid")
    args = ap.parse_args(argv)

    try:
        particles = parse_particle_list(args.plist)
    except Exception as e:
        print(f"[particle list parse error] {e}", file=sys.stderr)
        return 1
    try:
        blocks = parse_decay_table(args.decays)
    except Exception as e:
        print(f"[decay table parse error] {e}", file=sys.stderr)
        return 1

    ok, messages = validate(
        particles=particles,
        blocks=blocks,
        abs_tol_br=args.abs_tol_br,
        rel_tol_br=args.rel_tol_br,
        check_BSCC=not args.no_BSCC,
        strict_stable=args.strict_stable,
    )
    stream = sys.stdout if ok else sys.stderr
    for m in messages:
        print(m, file=stream)
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
