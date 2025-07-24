#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: PDG21Plus_generator.py

Description: Generates machine-readable files for SMASH and Thermal-FIST from
PDG21Plus_master.xlsx
"""

#.........................
# Import  standard modules
import os
import sys
import pandas as pd
import numpy as np

#.........................
# Import custom modules
import utils.PDG21Plus_tests as pdg_tests
import utils.PDG21Plus_process as pdg_process
import utils.PDG21Plus_format as pdg_format
import utils.PDG21Plus_plot as pdg_plot

#------------------------------------------------------------------------------

def main():
    os.system('clear')

#-----START MESSAGE-----
    sys.stdout.write('>Preparing lists... \n')
    sys.stdout.flush()

#-----READ/PARSE-----
    # Reads Excel source file.
    names = ['index','ID','Name','Mass(GeV)','Width(GeV)','Degeneracy',\
        'Baryon no.','Strangeness no.','Charm no.','Bottom no.','Isospin',\
        'I_3','Electric charge','No. of decay channels','Mass upper limit',\
        'Mass lower limit', 'Width upper limit', 'Width lower limit', 'Stars']
    df = pd.read_excel('PDG21Plus_master.xlsx', names=names, usecols=names[1:])

#-----PROCESSING-----
    # Calculates # of decay channels.
    df = pdg_process.build_decay_channel_number(df)

#-----TESTS-----
    # Run all tests. Program continues only if all are passed succesfully.
    tests_outcome = pdg_tests.all_tests(df)
    if tests_outcome[1] == True:
        pass
    else:
        sys.stdout.write('>One or more tests show inconsistency: \n')
        print(tests_outcome[0])
        sys.stdout.flush()
        sys.exit('>Lists were not created')

#-----PLOTTING-----
    if '--plot' in sys.argv[:]:
        particle_lists = [df]
        script_path = os.path.dirname(__file__)
        parent_path = os.path.dirname(script_path)

        # Reads PDG16+ list
        PDG16Plus_cols = ['ID','Name','Mass(GeV)','Width(GeV)','Degeneracy',\
                          'Baryon no.','Strangeness no.','Charm no.',\
                          'Bottom no.','Isospin','Electric charge',\
                          'No. of decay channels']

        PDG16Plus_path = os.path.join(parent_path, 'hadron_lists/PDG16Plus/PDG2016Plus_massorder.dat')
        if os.path.isfile(PDG16Plus_path):
            PDG16Plus_df = pd.read_table(PDG16Plus_path, sep='\t', header=None, \
                                         names=PDG16Plus_cols, na_filter=True)
            particle_lists.append(PDG16Plus_df)

        # Reads SMASH list
        SMASH_cols = ['Name','Mass(GeV)','Width(GeV)','Parity',\
                      'PID1','PID2','PID3','PID4']
        SMASH_path = os.path.join(parent_path, 'hadron_lists/SMASH/particles.txt')
        if os.path.isfile(SMASH_path):
            SMASH_df = pd.read_table(SMASH_path, delim_whitespace=True, header=None,\
                                     names=SMASH_cols, na_filter=True, comment='#')
            particle_lists.append(SMASH_df)
            # Drop leptons and heavy flavor baryons
            indexElectron = SMASH_df[SMASH_df['Name']=='e⁻'].index.item()
            indexFinal = SMASH_df.last_valid_index()
            indicesToDrop = np.arange(indexElectron, indexFinal+1)
            SMASH_df.drop(indicesToDrop, inplace=True)

        pdg_plot.plot_mass_spectrum(df)
        pdg_plot.plot_mass_spectra_comparison(particle_lists)

#-----FILTERING-----
    df = pdg_format.floats_to_ints(df)
    df = df.drop(columns=['Mass upper limit','Mass lower limit'])
    df = df.drop(columns=['Width upper limit','Width lower limit'])
    df = df.drop(columns=['Stars'])

#-----FORMATTING-----
    #--PARTICLES--
    df_PDG21Plus_massorder_particles = pdg_format.massorder_particles_format(df)
    df_PDG21Plus_ThFIST_particles = pdg_format.ThFIST_particles_format(df)
    #--DECAYS--
    #--massorder--
    df_PDG21Plus_massorder_full_decays = pdg_format.massorder_full_decays_format(df)
    #df_PDG21Plus_massorder_intermediate_decays = pdg_format.massorder_intermediate_decays_format(df)
    #--ThFIST--
    df_PDG21Plus_ThFIST_full_decays = pdg_format.ThFIST_full_decays_format(df)
    #df_PDG21Plus_ThFIST_intermediate_decays = pdg_format.ThFIST_intermediate_decays_format(df)

#-----WRITE OUTPUT FILE(S)-----
    header = False      # True or False.
    script_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(script_path)
    output_path = os.path.join(parent_path, 'hadron_lists/PDG21Plus/')
    decays_full_path = os.path.join(output_path, 'full_decays/')
    decays_intermediate_path = os.path.join(output_path, 'intermediate_decays/')
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(decays_full_path, exist_ok=True)
    os.makedirs(decays_intermediate_path, exist_ok=True)
    #--PARTICLES--
    pdg_format.save_PDG21Plus_massorder_particles_df(df_PDG21Plus_massorder_particles, output_path, header)
    pdg_format.save_PDG21Plus_ThFIST_particles_df(df_PDG21Plus_ThFIST_particles, output_path, header)
    #--DECAYS--
    #--massorder--
    pdg_format.save_PDG21Plus_massorder_decays_df(df_PDG21Plus_massorder_full_decays, decays_full_path, header)
    #pdg_format.save_PDG21Plus_massorder_decays_df(df_PDG21Plus_massorder_intermediate_decays, decays_intermediate_path, header)
    #--ThFIST--
    pdg_format.save_PDG21Plus_ThFIST_decays_df(df_PDG21Plus_ThFIST_full_decays, decays_full_path, header)
    #pdg_format.save_PDG21Plus_ThFIST_decays_df(df_PDG21Plus_ThFIST_intermediate_decays, decays_intermediate_path, header)

#-----END MESSAGE-----
    sys.stdout.write('>PDG lists created succesfully :) \n')
    sys.stdout.flush()

if __name__ == '__main__':
    main()
