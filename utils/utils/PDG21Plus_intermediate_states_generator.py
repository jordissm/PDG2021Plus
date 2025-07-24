import os
import sys
import pandas as pd
import numpy as np
from PDG21Plus_intermediate_states_formatting_tool import *

os.system('clear')
sys.stdout.write('>Preparing lists... \n')
sys.stdout.flush()

#-----READ/PARSE-----
names = ['ID','Name','Mass(GeV)','Width(GeV)','Degeneracy','Baryon no.',\
        'Strangeness no.','Charm no.','Bottom no.','Isospin','I_3',\
        'Electric charge','No. of decay channels']
df = pd.read_table('../hadron_lists/full_decays/decays_PDG21Plus_massorder.dat', sep='\t', header=None,\
        names=names, na_filter=True)

#-----PARENTS-----
parents = df.dropna()
parents_ordered_by_ID = parents.sort_values(by=['ID'])
particles_dictionary = parents.iloc[:,:-10]
particles_dictionary = particles_dictionary.set_index(['ID'])
particles_dictionary = particles_dictionary.to_dict()['Name']

#-----DECAYS-----
decays = df[df['No. of decay channels'].isnull()]
decays = decays.iloc[:,:-5]
decays.columns = ['ID(mother)', 'No. of daughter particles',\
                  'Branching ratio', 'ID#1', 'ID#2', 'ID#3', 'ID#4', 'ID#5']
decays = decays.apply(pd.to_numeric)
decays['ID#1'] = pd.to_numeric(decays['ID#1'], downcast='integer')
####-----2 DAUGHTERS-----
decays2daughters = decays[decays['No. of daughter particles']==2]
decays2daughters = decays2daughters.drop(columns='No. of daughter particles')
decays2daughters = decays2daughters.drop(columns='Branching ratio')
decays2daughters = decays2daughters.iloc[:,:-3]
decays2daughters_matrix = decays2daughters.pivot_table(index='ID#1',\
                columns='ID#2', values='ID(mother)', aggfunc=lambda x:list(x))
decays2daughters_matrix = decays2daughters_matrix.apply(lambda s: s.fillna({i: [] for\
                i in decays2daughters_matrix.index}))

####-----3 DAUGHTERS-----
decays3daughters = decays[decays['No. of daughter particles']==3]
decays3daughters = decays3daughters.drop(columns='No. of daughter particles')
decays3daughters = decays3daughters.drop(columns='Branching ratio')
decays3daughters = decays3daughters.iloc[:,:-2]
decays3daughters = decays3daughters.sort_values(by=['ID#1','ID(mother)'])

####-----4 DAUGHTERS-----
decays4daughters = decays[decays['No. of daughter particles']==4]
decays4daughters = decays4daughters.drop(columns='No. of daughter particles')
decays4daughters = decays4daughters.drop(columns='Branching ratio')
decays4daughters = decays4daughters.iloc[:,:-1]
decays4daughters = decays4daughters.sort_values(by=['ID#1','ID(mother)'])

#-----FUNCTIONS-----
def header():
    print('*'*65)
    print('*'+'\t'*8+'*')
    print('*'+' '*5+'Python3: daughter1_ID daughter2_ID'+'\t'*3+'*')
    print('*'+' '*5+'iPython3: find_reactions(daughter1_ID, daughter2_ID)'+'\t'+'*')
    print('*'+'\t'*8+'*')
    print('*'*65)

def mother_of(daughter1_ID, daughter2_ID, source_df=decays2daughters_matrix):
    columns = source_df.columns
    indices = source_df.index
    if (daughter1_ID in columns and daughter1_ID in indices) and\
       (daughter2_ID in columns and daughter2_ID in indices):
        possible_mothers = source_df[daughter1_ID][daughter2_ID]+\
                               source_df[daughter2_ID][daughter1_ID]
    elif daughter1_ID in columns and daughter2_ID in indices:
        possible_mothers = source_df[daughter1_ID][daughter2_ID]
    elif daughter2_ID in columns and daughter1_ID in indices:
        possible_mothers = source_df[daughter2_ID][daughter1_ID]
    else:
        return []
    return list(set(possible_mothers))

def prettyfy_reaction(possible_mothers, daughter1_ID, daughter2_ID):
    daughters = ' -> {} {}'.format(daughter1_ID, daughter2_ID)
    if len(possible_mothers)>0:
        for ii in range(len(possible_mothers)):
            print(' '+str(particles_dictionary[possible_mothers[ii]])+daughters)
        print('\n{} decays found'.format(ii+1))
    else:
        print(' No possible decays')

def find_reactions(daughter1_ID, daughter2_ID, source_df=decays2daughters_matrix):
    print('')
    print(' Mother -> daughter_1 daughter_2')
    print('-'*33)
    prettyfy_reaction(mother_of(daughter1_ID, daughter2_ID, source_df),\
                                daughter1_ID, daughter2_ID)
    print('')

def find_2decays(mother_ID, source_df=decays2daughters):
    sub_df = decays2daughters[decays2daughters['ID(mother)'] == mother_ID]
    print(sub_df)

def lowest_mass(particle_list, source_df=parents):
    min_mass = 4
    min_id = 0
    if len(particle_list) > 0:
        for ii in range(len(particle_list)):
            if particle_list[ii] == 0:
                pass
            else:
                current_mass = parents.at[parents.index[parents['ID']==particle_list[ii]][0].tolist(),'Mass(GeV)']
                if current_mass <= min_mass:
                    min_mass = current_mass
                    min_id = ii
        return particle_list[min_id]
    else:
        return 0

def get_mass(particle_ID, source_df=parents):
    if particle_ID == 0:
        return 4
    else:
        mass = parents.at[parents.index[parents['ID']==particle_ID][0].tolist(),'Mass(GeV)']
    return mass

#-----PROCESSES------
decays3daughters['1-2'] = decays3daughters.apply(lambda df: lowest_mass(mother_of(df['ID#1'],df['ID#2'])), axis=1)
decays3daughters['1-3'] = decays3daughters.apply(lambda df: lowest_mass(mother_of(df['ID#1'],df['ID#3'])), axis=1)
decays3daughters['2-3'] = decays3daughters.apply(lambda df: lowest_mass(mother_of(df['ID#2'],df['ID#3'])), axis=1)
decays3daughters['intermediate_particle'] = decays3daughters.apply(lambda df: df['1-2'] if get_mass(df['1-2'])+get_mass(df['ID#3']) <= get_mass(df['1-3'])+get_mass(df['ID#2']) and get_mass(df['1-2'])+get_mass(df['ID#3']) <= get_mass(df['2-3'])+get_mass(df['ID#1']) else df['1-3'] if get_mass(df['1-3'])+get_mass(df['ID#2']) <= get_mass(df['1-2'])+get_mass(df['ID#3']) and get_mass(df['1-3'])+get_mass(df['ID#2']) <= get_mass(df['2-3'])+get_mass(df['ID#1']) else df['2-3'], axis=1)
decays3daughters['final_particle'] = decays3daughters.apply(lambda df: df['ID#1'] if df['intermediate_particle']==df['2-3'] else df['ID#2'] if df['intermediate_particle']==df['1-3'] else df['ID#3'], axis=1)
decays3daughters['DeltaM(GeV)'] = decays3daughters.apply(lambda df: get_mass(df['intermediate_particle']) + get_mass(df['final_particle']) - get_mass(df['ID(mother)']), axis=1)
decays3daughters['conserves_mass'] = decays3daughters.apply(lambda df: 'yes' if df['DeltaM(GeV)']<0 else 'no', axis=1)
decays3daughters_conserving = decays3daughters.copy()
decays3daughters_conserving = decays3daughters_conserving[decays3daughters_conserving['conserves_mass']=='yes']
decays3daughters_conserving.sort_index(inplace=True)
decays3daughters_nonconserving = decays3daughters.copy()
decays3daughters_nonconserving = decays3daughters_nonconserving[decays3daughters_nonconserving['conserves_mass']=='no']
decays3daughters_nonconserving.sort_index(inplace=True)

decays4daughters['1-2'] = decays4daughters.apply(lambda df: lowest_mass(mother_of(df['ID#1'],df['ID#2'])), axis=1)
decays4daughters['1-3'] = decays4daughters.apply(lambda df: lowest_mass(mother_of(df['ID#1'],df['ID#3'])), axis=1)
decays4daughters['1-4'] = decays4daughters.apply(lambda df: lowest_mass(mother_of(df['ID#1'],df['ID#4'])), axis=1)
decays4daughters['2-3'] = decays4daughters.apply(lambda df: lowest_mass(mother_of(df['ID#2'],df['ID#3'])), axis=1)
decays4daughters['2-4'] = decays4daughters.apply(lambda df: lowest_mass(mother_of(df['ID#2'],df['ID#4'])), axis=1)
decays4daughters['3-4'] = decays4daughters.apply(lambda df: lowest_mass(mother_of(df['ID#3'],df['ID#4'])), axis=1)
decays4daughters['intermediate_particle_1'] = decays4daughters.apply(lambda df: df['1-2'] if get_mass(df['1-2'])+get_mass(df['3-4']) <= get_mass(df['1-3'])+get_mass(df['2-4']) and get_mass(df['1-2'])+get_mass(df['3-4']) <= get_mass(df['1-4'])+get_mass(df['2-3']) else df['1-3'] if get_mass(df['1-3'])+get_mass(df['2-4']) <= get_mass(df['1-2'])+get_mass(df['3-4']) and get_mass(df['1-3'])+get_mass(df['2-4']) <= get_mass(df['1-4'])+get_mass(df['2-3']) else df['1-4'], axis=1)
decays4daughters['intermediate_particle_2'] = decays4daughters.apply(lambda df: lowest_mass(mother_of(df['ID#1'],df['ID#2'])) if df['intermediate_particle_1']==df['3-4'] else lowest_mass(mother_of(df['ID#1'],df['ID#3'])) if df['intermediate_particle_1']==df['2-4'] else lowest_mass(mother_of(df['ID#1'],df['ID#4'])) if df['intermediate_particle_1']==df['2-3'] else lowest_mass(mother_of(df['ID#2'],df['ID#3'])) if df['intermediate_particle_1']==df['1-4'] else lowest_mass(mother_of(df['ID#2'],df['ID#4'])) if df['intermediate_particle_1']==df['1-3'] else lowest_mass(mother_of(df['ID#3'],df['ID#4'])), axis=1)
decays4daughters['DeltaM(GeV)'] = decays4daughters.apply(lambda df: get_mass(df['intermediate_particle_1']) + get_mass(df['intermediate_particle_2']) - get_mass(df['ID(mother)']), axis=1)
decays4daughters['conserves_mass'] = decays4daughters.apply(lambda df: 'yes' if df['DeltaM(GeV)']<0 else 'no', axis=1)
decays4daughters_conserving = decays4daughters.copy()
decays4daughters_conserving = decays4daughters_conserving[decays4daughters_conserving['conserves_mass']=='yes']
decays4daughters_conserving.sort_index(inplace=True)
decays4daughters_nonconserving = decays4daughters.copy()
decays4daughters_nonconserving = decays4daughters_nonconserving[decays4daughters_nonconserving['conserves_mass']=='no']
decays4daughters_nonconserving.sort_index(inplace=True)

intermediates = df.copy()
for i in decays3daughters_conserving.index.values:
    intermediates.loc[i,'Name'] = 2
    intermediates.loc[i,'Width(GeV)'] = decays3daughters_conserving.loc[i,'intermediate_particle']
    intermediates.loc[i,'Degeneracy'] = decays3daughters_conserving.loc[i,'final_particle']
    intermediates.loc[i,'Baryon no.'] = 0
    intermediates.loc[i,'Strangeness no.'] = 0
for i in decays4daughters_conserving.index.values:
    intermediates.loc[i,'Name'] = 2
    intermediates.loc[i,'Width(GeV)'] = decays4daughters_conserving.loc[i,'intermediate_particle_1']
    intermediates.loc[i,'Degeneracy'] = decays4daughters_conserving.loc[i,'intermediate_particle_2']
    intermediates.loc[i,'Baryon no.'] = 0
    intermediates.loc[i,'Strangeness no.'] = 0
for i in decays3daughters_nonconserving.index.values:
    intermediates.drop(labels=i, axis=0,inplace=True)
for i in decays4daughters_nonconserving.index.values:
    intermediates.drop(labels=i, axis=0,inplace=True)

os.system(''.join(['rm ',save_path,'*.dat']))
df_PDG21Plus_massorder_intermediates_decays = massorder_decays_format(intermediates)
save_PDG21Plus_massorder_decays_df(df_PDG21Plus_massorder_intermediates_decays, header=None)
df_PDG21Plus_ThFIST_intermediates_decays = ThFIST_decays_format(intermediates)
save_PDG21Plus_ThFIST_decays_df(df_PDG21Plus_ThFIST_intermediates_decays, header=None)

#-----END MESSAGE-----
sys.stdout.write('>PDG lists created succesfully :) \n')
sys.stdout.flush()

#-----DEBUGGING FILES-----
#df.to_csv('../hadron_lists/intermediate_decays/out_main.csv')
#decays3daughters_conserving.to_csv('../hadron_lists/intermediate_decays/out_3daughtersdecays_intermediate_conserving.csv')
#decays3daughters_nonconserving.to_csv('../hadron_lists/intermediate_decays/out_3daughtersdecays_intermediate_nonconserving.csv')
#decays4daughters_conserving.to_csv('../hadron_lists/intermediate_decays/out_4daughtersdecays_intermediate_conserving.csv')
#decays4daughters_nonconserving.to_csv('../hadron_lists/intermediate_decays/out_4daughtersdecays_intermediate_nonconserving.csv')
#intermediates.to_csv('../hadron_lists/intermediate_decays/intermediates.csv')
