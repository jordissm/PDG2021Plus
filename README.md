# PDG21+
## Description
PDG21+ is a hadron list that contains all hadrons (no charmness) listed on the 
Review of Particle Physics, along with their quantum numbers and decays. A
collection of Python scripts is provided to help formatting the list for use
with [Thermal-FIST](https://github.com/vlvovch/Thermal-FIST),
[SMASH](https://github.com/smash-transport/smash), and other post-processing tools.

Please see [Supl. Rev. Mex. Fis. 3, 040921 (2022)](https://doi.org/10.31349/SuplRevMexFis.3.040921) for details and cite when using the list.

<br>
<br>

## Contents
### Generating scripts
The list is stored in `xlsx` format for easy access but a set but a set of
scripts are provided in order to cross-check that the listed properties of
particles respect physical laws and formats it to be used in Thermal-FIST and
other models.

After updating the master list, execute the following lines:

    cd generating_scripts
    python3 PDG21Plus_generator.py

<br>

### Hadron lists / PDG21+
`PDG21Plus_massorder.dat`\
Complete list of particles (including anti-particles) sorted by mass.
<font size="1">
<p align="center">

| PID | Name | Mass (GeV) | Width (GeV) | Spin deg. | B | S | Charmness | Bottom no. | Isospin | Q | No. of decay channels |
| - | - | - | - | - | - | - | - | - | - | - | - |

</p>
</font>

<br>

`PDG21Plus_ThFIST.dat`\
Complete list of particles (without anti-particles) sorted by mass.
<font size="1">
<p align="center">

| PID | Name | Stable flag | Mass (GeV) | Spin deg. | Statistics | B | Q | S | Charmness | Absolute S | Absolute Charmness | Width (GeV) | Threshold (GeV) |
| - | - | - | - | - | - | - | - | - | - | - | - | - | - |

</p>
</font>

<br>

`SMASH_particles.txt`\
Lists most of the particles of the full PDG21+ list in the format that SMASH
takes as input. Notice that some hadrons have been omitted due to their lack of
information.
<font size="1">
<p align="center">

| PID | Name | Mass (GeV) | Width (GeV) | Spin deg. | B | S | Charm no. | Bottom no. | Isospin | Q | No. of decay channels |
| - | - | - | - | - | - | - | - | - | - | - | - |

</p>
</font>

<br>

`SMASH_decaymodes.txt`\
Includes a list all the decaying particles in the PDG21+ list and their
branching ratios. All 3- and 4-daughter decays are modeled via some
intermediate state, with the exeption of $\eta$, which has been explicitly
treated as a 3-body decay. All the decay channels that have been parametrized
by an intermediate state and violate mass conservation have been omitted.
<font size="1">
<p align="center">

| PID | Name | Mass (GeV) | Width (GeV) | Spin deg. | B | S | Charm no. | Bottom no. | Isospin | Q | No. of decay channels |
| - | - | - | - | - | - | - | - | - | - | - | - |

</p>
</font>

<br>
<br>

### Hadron lists / PDG16+
`PDG16Plus_massorder.dat`\
Complete list of particles sorted by mass.
<font size="1">
<p align="center">

| PID | Name | Mass (GeV) | Width (GeV) | Spin deg. | B | S | Charm no. | Bottom no. | Isospin | Q | No. of decay channels |
| - | - | - | - | - | - | - | - | - | - | - | - |

</p>
</font>
<br>

`PDG16Plus_ThFIST.dat`\
Complete list of particles sorted by mass.
<font size="1">
<p align="center">

| PID | Name | Mass (GeV) | Width (GeV) | Spin deg. | B | S | Charm no. | Bottom no. | Isospin | Q | No. of decay channels |
| - | - | - | - | - | - | - | - | - | - | - | - |

</p>
</font>
<br>
<br>

### Hadron lists / SMASH
`particles.txt`\
Complete list of particles sorted by mass.
<font size="1">
<p align="center">

| PID | Name | Mass (GeV) | Width (GeV) | Spin deg. | B | S | Charm no. | Bottom no. | Isospin | Q | No. of decay channels |
| - | - | - | - | - | - | - | - | - | - | - | - |

</p>
</font>
<br>

`decaymodes.txt`\
Complete list of particles sorted by mass.
<font size="1">
<p align="center">

| PID | Name | Mass (GeV) | Width (GeV) | Spin deg. | B | S | Charm no. | Bottom no. | Isospin | Q | No. of decay channels |
| - | - | - | - | - | - | - | - | - | - | - | - |

</p>
</font>
<br>