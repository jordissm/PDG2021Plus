import pandas as pd
import numpy as np

save_path = '../hadron_lists/full_decays/'

SMASH_particles = 'particles.txt'
SMASH_decaymodes = 'decaymodes.txt'
PDG21Plus_massorder_parents_filename = 'PDG21Plus_massorder.dat'
PDG21Plus_massorder_decays_filename = 'decays_PDG21Plus_massorder.dat'
PDG21Plus_ThFIST_parents_filename = 'PDG21Plus_ThFIST.dat'
PDG21Plus_ThFIST_decays_filename = 'decays_PDG21Plus_ThFIST.dat'
PDG21Plus_ThFIST_decays_header = '''# the list of decays
# each entry consists of the following:
# a line with the pdgid of decaying particle
# a line with the number of decay channels
# for each channel a line containing whitespace-separated values of the channel branching ratio and pdg ids of the daughter products
# everything after the # symbol is treated as a comment and ignored
# decays of antiparticles are not listed but generated from the listed decays of particles\n\n'''

def floats_to_ints(input_df):
    """Turns floats to integers when possible"""
    df = input_df.copy()
    mask = df['No. of decay channels'].isnull()
    df['No. of decay channels'] = df['No. of decay channels'].astype('Int64')
    df['Width(GeV)']=df['Width(GeV)'].apply(lambda r: int(r)\
                                            if (r % 1 == 0) else str(r))
    df['Bottom no.'] = df['Bottom no.'].astype('Int64')
    df['Strangeness no.'] = df['Strangeness no.'].astype('Int64')
    df['Charm no.'] = df['Charm no.'].astype('Int64')
    df['Bottom no.'] = df['Bottom no.'].astype('Int64')
    df['Electric charge'] = df['Electric charge'].astype('Int64')
    df['Stars'] = df['Stars'].astype('Int64')
    return df

def SMASH_particles_format(input_df):
    """Returns a list ordered in ascending mass order to use in SMASH"""
    pass

def SMASH_decaymodes_format(input_df):
    """Returns a decay list in ascending mass order to use in SMASH"""
    pass

def massorder_parents_format(input_df):
    """Returns list ordered in descending mass order"""
    df = input_df.copy()
    df = df[df['Name'].str.isalpha().notnull()]
    df.sort_values(by=['Mass(GeV)','ID'],\
                   ascending=[False,False],inplace=True)
    return df

def massorder_decays_format(input_df):
    """Returns list ordered in descending mass order"""
    df = input_df.copy()
    mask = df['Name'].str.isalpha().notnull()
    df.loc[mask,'Mass_parent'] = df['Mass(GeV)']
    df['Mass_parent'] = df['Mass_parent'].ffill(axis=0)
    df.sort_values(by=['Mass_parent','ID','Name','Mass(GeV)'],\
                   ascending=[False,False,False,False],inplace=True)
    df = df.drop(columns=['Mass_parent'])
    return df

def ThFIST_parents_format(input_df):
    """Returns list formatted intended to be used in Thermal FIST"""
    df = input_df.copy()
    df = df[df['Name'].str.isalpha().notnull()]
    df = df[df['ID']>=0]
    df.sort_values(by=['Mass(GeV)','ID'],\
                   ascending=[True,False],inplace=True)
    df['Stable?'] = df['Width(GeV)'].apply(lambda width: 1 if width==0 else 0)
    mask = (df['ID'] != 22)
    df.loc[~mask,'Statistics'] = -1
    df.loc[mask,'Statistics'] = df['Degeneracy'].apply(lambda s: 1 if (s%2)==0 else -1)
    df['Statistics'] = df['Statistics'].astype(int)
    df['Absolute strangeness'] = df['Strangeness no.'].apply(abs)
    df["Absolute 'charmness'"] = df['Charm no.'].apply(abs)
    df['Threshold(GeV)'] = 0
    df = df[['ID','Name','Stable?','Mass(GeV)','Degeneracy','Statistics',\
             'Baryon no.','Electric charge','Strangeness no.','Charm no.',\
             'Absolute strangeness',"Absolute 'charmness'",'Width(GeV)',\
             'Threshold(GeV)']]
    return df

def ThFIST_decays_format(input_df):
    """Returns list formatted intended to be used in Thermal FIST"""
    df = input_df.copy()
    df = df[df['ID']>=0]
    mask = df['Name'].str.isalpha().notnull()
    df.loc[mask,'Width_parent'] = df['Width(GeV)']
    df['Width_parent'] = df['Width_parent'].ffill(axis=0)
    df['Stable?'] = df['Width_parent'].apply(lambda width: 1 if width==0 else 0)
    df = df[df['Stable?']!=1].reset_index(drop=True)
    mask = df['Name'].str.isalpha().notnull()
    df.loc[:,'ID_copy'] = df['ID'].apply(lambda r: str(int(r))\
                                            if (r % 1 == 0) else str(r))
    blank_df = df[mask][['ID']]
    ID_df = df[mask][['ID','ID_copy']].rename(columns={'ID_copy':'col0'})
    decays_df = df[mask][['ID','No. of decay channels']].rename(columns={'No. of decay channels':'col0'})
    branching_ratios_df = df[~mask][['ID','Mass(GeV)','Width(GeV)','Degeneracy','Baryon no.','Strangeness no.','Charm no.']]
    branching_ratios_df = branching_ratios_df.rename(columns={'Mass(GeV)':'col0','Width(GeV)':'col1','Degeneracy':'col2','Baryon no.':'col3','Strangeness no.':'col4','Charm no.':'col5'})
    cols = ['col1','col2','col3','col4','col5']
    branching_ratios_df[cols] = branching_ratios_df[cols].replace({'0':np.nan,0:np.nan})
    branching_ratios_df[cols] = branching_ratios_df[cols].astype('Int64')
    df = pd.concat([blank_df,ID_df,decays_df,branching_ratios_df], ignore_index=True).reset_index(drop=True)
    df.sort_values(by=['ID','col0'],ascending=[False,False],inplace=True)
    df = df.drop(columns=['ID'])
    return df

def save_PDG21Plus_massorder_parents_df(df,header=None):
    path = ''.join([save_path,PDG21Plus_massorder_parents_filename])
    df.to_csv(path, sep='\t', index=False, header=header)

def save_PDG21Plus_massorder_decays_df(df,header=None):
    path = ''.join([save_path,PDG21Plus_massorder_decays_filename])
    df.to_csv(path, sep='\t', index=False, header=header)

def save_PDG21Plus_ThFIST_parents_df(df,header=None):
    path = ''.join([save_path,PDG21Plus_ThFIST_parents_filename])
    df.to_csv(path, sep='\t', index=False, header=header)

def save_PDG21Plus_ThFIST_decays_df(df,header=None):
    path = ''.join([save_path,PDG21Plus_ThFIST_decays_filename])
    f = open(path,'a')
    f.write(PDG21Plus_ThFIST_decays_header)
    df.to_csv(f, sep='\t', index=False, header=header)
    f.close()
