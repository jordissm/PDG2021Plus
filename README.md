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
```shell
cd generating_scripts
python3 PDG21Plus_generator.py
```
This will generate all versions of the PDG21+ hadron list on the `hadron_lists`
folder. Optionally, the script can be executed with the `--plot` option to
produce Figs. 1 and 2 of the [paper](https://doi.org/10.31349/SuplRevMexFis.3.040921).

<br>

### Hadron lists –– Particles
`PDG21Plus_massorder.dat`\
Complete list of particles (including anti-particles) sorted by mass.
<font size="1">
<p align="center">

|  PID  |          Name          | Mass (GeV) | Width (GeV) | Spin deg. |  $B$  | $S$ | Charmness | Bottom no. | Isospin | $I_z$ | $Q$ | No. of decay channels |
|  :-:  | :--------------------: | :--------: | :---------: | :-------: |  :-:  |  -  | :-------: | :--------: | :-----: |  :-:  | :-: | :-------------------: |
|  2124 |      $N^+(1520)$       |   1.515    |    0.11     |     4     |   1   |  0  |     0     |     0      |   0.5   |  0.5  |  1  |           8           |
|  1214 |      $N^0(1520)$       |   1.515    |    0.11     |     4     |   1   |  0  |     0     |     0      |   0.5   | -0.5  |  0  |           8           |
| -1214 | $\overline{N}^0(1520)$ |   1.515    |    0.11     |     4     |  -1   |  0  |     0     |     0      |   0.5   |  0.5  |  0  |           8           |
| -2124 | $\overline{N}^-(1520)$ |   1.515    |    0.11     |     4     |  -1   |  0  |     0     |     0      |   0.5   | -0.5  | -1  |           8           |

</p>
</font>

<br>

`PDG21Plus_ThFIST.dat`\
Complete list of particles (without anti-particles) sorted by mass.
<font size="1">
<p align="center">

| PID  |    Name     | Stable flag | Mass (GeV) | Spin deg. | Statistics | $B$ | $Q$ | $S$ | Charmness | Absolute Strangeness | Absolute Charmness | Width (GeV) | Threshold (GeV) |
| :--: | :---------: | :---------: | :--------: | :-------: | :--------: |  -  |  -  |  -  | :-------: | :------------------: | :----------------: | :---------: | :-------------: |
| 2124 | $N^+(1520)$ |      0      |   1.515    |     4     |     1      |  1  |  1  |  0  |     0     |          0           |         0          |    0.11     |        0        |
| 1214 | $N^0(1520)$ |      0      |   1.515    |     4     |     1      |  1  |  0  |  0  |     0     |          0           |         0          |    0.11     |        0        |

</p>
</font>

<br>

`SMASH_particles.txt`\
Lists most of the particles of the full PDG21+ list in the format that SMASH
takes as input. Notice that some hadrons have been omitted due to their lack of
information.
<font size="1">
<p align="center">

|    Name   | Mass (GeV) | Width (GeV) | Parity | PIDs |      |
| :-------: | :--------: | :---------: | :----: | :--: | :--: |
| $N(1520)$ |   1.515    |    0.110    |   –    | 1214 | 2124 |

</p>
</font>

<br>

### Hadron lists –– Decays
`decays_PDG21Plus_massorder.dat`\
Decays
<font size="1">
<p align="center">

|  PID  |             Name            |      Mass (GeV)   |      Width (GeV)     |       Spin deg.      |          $B$         |          $S$         |       Charmness      | Bottom no. | Isospin | $I_z$ | $Q$ | # decay channels |
| :---: | :-------------------------: | :---------------: | :------------------: | :------------------: | :------------------: | :------------------: | :------------------: | :--------: | :-----: |  :-:  | :-: | :--------------: |
| 1214  |         $N^0(1520)$         |       1.515       |         0.11         |          4           |           1          |           0          |           0          |      0     |   0.5   | -0.5  |  0  |        8         |
|__PID__|__No. of daughter particles__|__Branching ratio__|__PID of daughter #1__|__PID of daughter #2__|__PID of daughter #3__|__PID of daughter #4__|__PID of daughter #5__|            |         |       |     |                  |
| 1214  |             3               |    0.016796189    |         2112         |        -211          |          211         |           0          |           0          |            |         |       |     |                  |
| 1214  |             3               |    0.016796189    |         2112         |         111          |          111         |           0          |           0          |            |         |       |     |                  |
| 1214  |             3               |    0.016796189    |         2212         |        -211          |          111         |           0          |           0          |            |         |       |     |                  |
| 1214  |             2               |    0.464276761    |         2212         |        -211          |           0          |           0          |           0          |            |         |       |     |                  |
| 1214  |             2               |    0.232138381    |         2112         |         111          |           0          |           0          |           0          |            |         |       |     |                  |
| 1214  |             2               |    0.126598145    |         1114         |         211          |           0          |           0          |           0          |            |         |       |     |                  |
| 1214  |             2               |    0.084482327    |         2114         |         111          |           0          |           0          |           0          |            |         |       |     |                  |
| 1214  |             2               |    0.042115818    |         2214         |        -211          |           0          |           0          |           0          |            |         |       |     |                  |

</p>
</font>

<br>

`decays_PDG21Plus_ThFIST.dat`\
Decays
<font size="1">
<p align="center">

|           PID           |                      |                      |                      |                      |                      |
| :---------------------: | :------------------: | :------------------: | :------------------: | :------------------: |:-------------------: |
|          1214           |                      |                      |                      |                      |                      |
|__No. of decay channels__|                      |                      |                      |                      |                      |
|            8            |                      |                      |                      |                      |                      |
|   __Branching ratio__   |__PID of daughter #1__|__PID of daughter #2__|__PID of daughter #3__|__PID of daughter #4__|__PID of daughter #5__|
|       0.464276761       |         2212         |         -211         |                      |                      |                      |
|       0.232138381       |         2112         |          111         |                      |                      |                      |
|       0.126598145       |         1114         |          211         |                      |                      |                      |
|       0.084482327       |         2114         |          111         |                      |                      |                      |
|       0.042115818       |         2214         |         -211         |                      |                      |                      |
|       0.016796189       |         2112         |         -211         |          211         |                      |                      |
|       0.016796189       |         2112         |          111         |          111         |                      |                      |
|       0.016796189       |         2212         |         -211         |          111         |                      |                      |

</p>
</font>

<br>

`SMASH_decaymodes.txt`\
Decays
<font size="1">
<p align="center">

a
</p>
</font>