# PDG21+
<p align="justify">
PDG21+ is a hadron list that contains all hadrons (no charmness) listed on the 
Review of Particle Physics, along with their quantum numbers and properties.

A collection of Python scripts are provided to help formatting the list for use
with ThermalFIST, SMASH, and other post-processing tools.
</p>

## Contents
### Generating scripts
<p align="justify">
The list is stored in `xlsx` format for easy access but a set but a set of
scripts are provided in order to cross-check that the listed properties of
particles respect physical laws and formats it to be used in Thermal-FIST and
other models.

After updating the master list, execute the following lines:

    cd generating_scripts
    python3 PDG21Plus_generator.py
</p>
	
### Hadron lists
<p align="justify">
Contains the PDG21+ and other commonly used lists.
</p>

### SMASH
<p align="justify">
`hadron_lists/SMASH_particles.txt` lists most of the particles of the full
PDG21+ list in the format that SMASH takes as input. Notice that some hadrons
have been omitted due to their lack of information.

`hadron_lists/SMASH_decaymodes.txt` includes a list all the decaying particles
in the PDG21+ list and their branching ratios. All 3- and 4-daughter decays are
modeled via some intermediate state, with the exeption of $\eta$, which has
been explicitly treated as a 3-body decay. All the decay channels that have
been parametrized by an intermediate state and violate mass conservation have
been omitted.
</p>