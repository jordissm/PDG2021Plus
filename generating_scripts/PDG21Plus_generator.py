import os
import sys
import pandas as pd
from PDG21Plus_crosschecking_tool import *
from PDG21Plus_formatting_tool import *
from PDG21Plus_plotting_tool import *

os.system('clear')

def main():
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
    df = build_decay_channel_number(df)

#-----TESTS-----
    # Run all tests. Program continues only if all are passed succesfully.
    tests_outcome = all_tests(df)
    if tests_outcome[1] == True:
        pass
    else:
        sys.stdout.write('>One or more tests show inconsistency: \n')
        print(tests_outcome[0])
        sys.stdout.flush()
        sys.exit('>Lists were not created')

#-----PLOTTING-----
    names = ['ID','Name','Mass(GeV)','Width(GeV)','Degeneracy','Baryon no.',\
            'Strangeness no.','Charm no.','Bottom no.','Isospin',\
            'Electric charge','No. of decay channels']
    paths = '../../PDG16Plus/PDG2016Plus_massorder.dat'
    old_df = pd.read_table(path, sep='\t', header=None, \
                           names=names, na_filter=True)
    #print(old_df)
    plot_mass_spectra_new(df)
    plot_mass_spectra_old_vs_new(df,old_df,old_df)

#-----FILTERING-----
    df = floats_to_ints(df)
    df = df.drop(columns=['Mass upper limit','Mass lower limit'])
    df = df.drop(columns=['Width upper limit','Width lower limit'])
    df = df.drop(columns=['Stars'])

#-----FORMATTING-----
    #--massorder--
    df_PDG21Plus_massorder_parents = massorder_parents_format(df)
    df_PDG21Plus_massorder_decays = massorder_decays_format(df)
    #--ThFIST--
    df_PDG21Plus_ThFIST_parents = ThFIST_parents_format(df)
    df_PDG21Plus_ThFIST_decays = ThFIST_decays_format(df)

#-----WRITE OUTPUT FILE(S)-----
    header = None      # True or None.
    os.system(' '.join(['mkdir -p',save_path]))
    os.system(''.join(['rm ',save_path,'*.dat']))
    #--massorder--
    save_PDG21Plus_massorder_parents_df(df_PDG21Plus_massorder_parents, header)
    save_PDG21Plus_massorder_decays_df(df_PDG21Plus_massorder_decays, header)
    #--ThFIST--
    save_PDG21Plus_ThFIST_parents_df(df_PDG21Plus_ThFIST_parents, header)
    save_PDG21Plus_ThFIST_decays_df(df_PDG21Plus_ThFIST_decays, header)

#-----END MESSAGE-----
    sys.stdout.write('>PDG lists created succesfully :) \n')
    sys.stdout.flush()

if __name__ == '__main__':
    main()
