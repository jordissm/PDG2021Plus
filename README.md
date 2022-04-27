# PDG21+

PDG21+ is a hadron list that contains all (u->s quark-containing) hadrons
listed on the Particle Data Booklet, along with their quantum numbers and
properties. 

A collection of Python scripts are provided to help formatting the list
for use with ThermalFIST, SMASH, and other post-processing tools. 

## Contents
### SMASH
The particles.txt lists most of the particles of the full PDG21+ list in
the format that SMASH takes as input. Notice that some hadrons have been
omitted due to their large lack of information.

decaymodes.txt includes a list all the decaying particles in the PDG21+
list and their branching ratios. All 3- and 4-daughter decays are 
modeled via some intermediate state, with the exeption of $\eta$, which
has been explicitly treated as a 3-body decay. All the decay channels
that have been parametrized by an intermediate state and violate mass 
conservation have been omitted.

### Generating scripts
The list is stored in xlsx format for easiness of modification but a set
of scripts are provided in order to cross-check that the listed
properties of particles respect physical laws and formats it to be used
in ThermalFIST and other post-processing tools.

After updating the xlsx, one needs to execute the following lines:

    python3 PDG21Plus_generator.py
	python3 PDG21Plus_intermediate_states_generator.py
	
### Hadron lists
The output of the Python scripts is written in the full_decays and
intermediate_decays directories.