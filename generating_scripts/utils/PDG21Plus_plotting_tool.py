import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = 'Computer Modern Roman'

def plot_mass_spectra_old_vs_new(df1, df2, df3):
    PDG21Plus_df = df1.copy()
    PDG16Plus_df = df2.copy()
    SMASH_df     = df3.copy()

    # Nucleons
    PDG21Plus_masses_nucleons = PDG21Plus_df[(PDG21Plus_df['Baryon no.']!=0) &\
                                 (PDG21Plus_df['Electric charge']==0) &\
                                 (PDG21Plus_df['ID']>0) &\
                                 (PDG21Plus_df['Isospin']==0.5) &\
                                 (PDG21Plus_df['Strangeness no.']==0)]['Mass(GeV)']
    PDG16Plus_masses_nucleons = PDG16Plus_df[(PDG16Plus_df['Baryon no.']!=0) &\
                                 (PDG16Plus_df['Electric charge']==0) &\
                                 (PDG16Plus_df['ID']>0) &\
                                 (PDG16Plus_df['Isospin']==0.5) &\
                                 (PDG16Plus_df['Strangeness no.']==0)]['Mass(GeV)']
    SMASH_masses_nucleons = SMASH_df[(SMASH_df['Baryon no.']!=0) &\
                                 (SMASH_df['Electric charge']==0) &\
                                 (SMASH_df['ID']>0) &\
                                 (SMASH_df['Isospin']==0.5) &\
                                 (SMASH_df['Strangeness no.']==0)]['Mass(GeV)']
    # Deltas
    PDG21Plus_masses_deltas = PDG21Plus_df[(PDG21Plus_df['Baryon no.']!=0) &\
                                 (PDG21Plus_df['Electric charge']==0) &\
                                 (PDG21Plus_df['ID']>0) &\
                                 (PDG21Plus_df['Isospin']==1.5) &\
                                 (PDG21Plus_df['Strangeness no.']==0)]['Mass(GeV)']
    PDG16Plus_masses_deltas = PDG16Plus_df[(PDG16Plus_df['Baryon no.']!=0) &\
                                 (PDG16Plus_df['Electric charge']==0) &\
                                 (PDG16Plus_df['ID']>0) &\
                                 (PDG16Plus_df['Isospin']==1.5) &\
                                 (PDG16Plus_df['Strangeness no.']==0)]['Mass(GeV)']
    SMASH_masses_deltas = SMASH_df[(SMASH_df['Baryon no.']!=0) &\
                                 (SMASH_df['Electric charge']==0) &\
                                 (SMASH_df['ID']>0) &\
                                 (SMASH_df['Isospin']==1.5) &\
                                 (SMASH_df['Strangeness no.']==0)]['Mass(GeV)']
    # Kaons
    PDG21Plus_masses_kaons = PDG21Plus_df[(PDG21Plus_df['Baryon no.']==0) &\
                              (abs(PDG21Plus_df['Strangeness no.'])==1) &\
                              (PDG21Plus_df['Electric charge']==0) &\
                              (PDG21Plus_df['ID']>0)]['Mass(GeV)']
    PDG16Plus_masses_kaons = PDG16Plus_df[(PDG16Plus_df['Baryon no.']==0) &\
                              (abs(PDG16Plus_df['Strangeness no.'])==1) &\
                              (PDG16Plus_df['Electric charge']==0) &\
                              (PDG16Plus_df['ID']>0)]['Mass(GeV)']
    SMASH_masses_kaons = SMASH_df[(SMASH_df['Baryon no.']==0) &\
                          (abs(SMASH_df['Strangeness no.'])==1) &\
                          (SMASH_df['Electric charge']==0) &\
                          (SMASH_df['ID']>0)]['Mass(GeV)']
    # Lambdas
    PDG21Plus_masses_lambdas = PDG21Plus_df[(PDG21Plus_df['Baryon no.']!=0) &\
                                 (PDG21Plus_df['Electric charge']==0) &\
                                 (PDG21Plus_df['ID']>0) &\
                                 (PDG21Plus_df['Isospin']==0) &\
                                 (PDG21Plus_df['Strangeness no.']==-1)]['Mass(GeV)']
    PDG16Plus_masses_lambdas = PDG16Plus_df[(PDG16Plus_df['Baryon no.']!=0) &\
                                 (PDG16Plus_df['Electric charge']==0) &\
                                 (PDG16Plus_df['ID']>0) &\
                                 (PDG16Plus_df['Isospin']==0) &\
                                 (PDG16Plus_df['Strangeness no.']==-1)]['Mass(GeV)']
    SMASH_masses_lambdas = SMASH_df[(SMASH_df['Baryon no.']!=0) &\
                                 (SMASH_df['Electric charge']==0) &\
                                 (SMASH_df['ID']>0) &\
                                 (SMASH_df['Isospin']==0) &\
                                 (SMASH_df['Strangeness no.']==-1)]['Mass(GeV)']
    # Xis
    PDG21Plus_masses_xis = PDG21Plus_df[(PDG21Plus_df['Baryon no.']!=0) &\
                            (PDG21Plus_df['Isospin']==0.5) &\
                            (PDG21Plus_df['Electric charge']==-1) &\
                            (PDG21Plus_df['ID']>0) &\
                            (abs(PDG21Plus_df['Strangeness no.'])==2)]['Mass(GeV)']
    PDG16Plus_masses_xis = PDG16Plus_df[(PDG16Plus_df['Baryon no.']!=0) &\
                            (PDG16Plus_df['Isospin']==0.5) &\
                            (PDG16Plus_df['Electric charge']==-1) &\
                            (PDG16Plus_df['ID']>0) &\
                            (abs(PDG16Plus_df['Strangeness no.'])==2)]['Mass(GeV)']
    SMASH_masses_xis = SMASH_df[(SMASH_df['Baryon no.']!=0) &\
                            (SMASH_df['Isospin']==0.5) &\
                            (abs(SMASH_df['Strangeness no.'])==2) &\
                            (SMASH_df['Electric charge']==-1) &\
                            (SMASH_df['ID']>0)]['Mass(GeV)']
    # Sigmas
    PDG21Plus_masses_sigmas = PDG21Plus_df[(PDG21Plus_df['Baryon no.']!=0) &\
                                 (PDG21Plus_df['Electric charge']==0) &\
                                 (PDG21Plus_df['ID']>0) &\
                                 (PDG21Plus_df['Isospin']==1) &\
                                 (PDG21Plus_df['Strangeness no.']==-1)]['Mass(GeV)']
    PDG16Plus_masses_sigmas = PDG16Plus_df[(PDG16Plus_df['Baryon no.']!=0) &\
                                 (PDG16Plus_df['Electric charge']==0) &\
                                 (PDG16Plus_df['ID']>0) &\
                                 (PDG16Plus_df['Isospin']==1) &\
                                 (PDG16Plus_df['Strangeness no.']==-1)]['Mass(GeV)']
    SMASH_masses_sigmas = SMASH_df[(SMASH_df['Baryon no.']!=0) &\
                                 (SMASH_df['Electric charge']==0) &\
                                 (SMASH_df['ID']>0) &\
                                 (SMASH_df['Isospin']==1) &\
                                 (SMASH_df['Strangeness no.']==-1)]['Mass(GeV)']
    # Omegas
    PDG21Plus_masses_omegas = PDG21Plus_df[(PDG21Plus_df['Baryon no.']!=0) &\
                                 (PDG21Plus_df['Electric charge']==-1) &\
                                 (PDG21Plus_df['ID']>0) &\
                                 (PDG21Plus_df['Isospin']==0) &\
                                 (PDG21Plus_df['Strangeness no.']==-3)]['Mass(GeV)']
    PDG16Plus_masses_omegas = PDG16Plus_df[(PDG16Plus_df['Baryon no.']!=0) &\
                                 (PDG16Plus_df['Electric charge']==-1) &\
                                 (PDG16Plus_df['ID']>0) &\
                                 (PDG16Plus_df['Isospin']==0) &\
                                 (PDG16Plus_df['Strangeness no.']==-3)]['Mass(GeV)']
    SMASH_masses_omegas = SMASH_df[(SMASH_df['Baryon no.']!=0) &\
                                 (SMASH_df['Electric charge']==-1) &\
                                 (SMASH_df['ID']>0) &\
                                 (SMASH_df['Isospin']==0) &\
                                 (SMASH_df['Strangeness no.']==-3)]['Mass(GeV)']

    fig = plt.figure(figsize=(5.5,7.5))
    #First row
    ax1 = fig.add_subplot(3,7,1)
    ax2 = fig.add_subplot(3,7,2)
    ax3 = fig.add_subplot(3,7,3)
        #
    ax4 = fig.add_subplot(3,7,4)
        #
    ax5 = fig.add_subplot(3,7,5)
    ax6 = fig.add_subplot(3,7,6)
    ax7 = fig.add_subplot(3,7,7)
    #Second row
    ax8 = fig.add_subplot(3,7,8)
    ax9 = fig.add_subplot(3,7,9)
    ax10 = fig.add_subplot(3,7,10)
        #
    ax11 = fig.add_subplot(3,7,11)
        #
    ax12 = fig.add_subplot(3,7,12)
    ax13 = fig.add_subplot(3,7,13)
    ax14 = fig.add_subplot(3,7,14)
    #Third row
    ax15 = fig.add_subplot(3,7,15)
    ax16 = fig.add_subplot(3,7,16)
    ax17 = fig.add_subplot(3,7,17)
        #
    ax18 = fig.add_subplot(3,7,18)
        #
    ax19 = fig.add_subplot(3,7,19)
    ax20 = fig.add_subplot(3,7,20)
    ax21 = fig.add_subplot(3,7,21)
    ax4.set_visible(False)
    ax11.set_visible(False)
    ax18.set_visible(False)

    #x-axis
    xparams = {'axis':'x','which':'both','bottom':False,'top':False,'labelbottom':False}
    yparams = {'axis':'y','which':'both','left':False,'right':False,'labelleft':False}
    ax1.tick_params(**xparams)
    ax2.tick_params(**xparams)
    ax2.tick_params(**yparams)
    ax3.tick_params(**xparams)
    ax3.tick_params(**yparams)
    ax5.tick_params(**xparams)
    ax6.tick_params(**xparams)
    ax6.tick_params(**yparams)
    ax7.tick_params(**xparams)
    ax7.tick_params(**yparams)
    ax8.tick_params(**xparams)
    ax9.tick_params(**xparams)
    ax9.tick_params(**yparams)
    ax10.tick_params(**xparams)
    ax10.tick_params(**yparams)
    ax12.tick_params(**xparams)
    ax13.tick_params(**xparams)
    ax13.tick_params(**yparams)
    ax14.tick_params(**xparams)
    ax14.tick_params(**yparams)
    ax15.tick_params(**xparams)
    ax16.tick_params(**xparams)
    ax16.tick_params(**yparams)
    ax17.tick_params(**xparams)
    ax17.tick_params(**yparams)
    ax19.tick_params(**xparams)
    ax20.tick_params(**xparams)
    ax20.tick_params(**yparams)
    ax21.tick_params(**xparams)
    ax21.tick_params(**yparams)
    #y-axis
    ax1.set_ylabel(r'$m$ [GeV]',fontsize=15)
    ax5.set_ylabel(r'$m$ [GeV]',fontsize=15)
    ax8.set_ylabel(r'$m$ [GeV]',fontsize=15)
    ax12.set_ylabel(r'$m$ [GeV]',fontsize=15)
    ax15.set_ylabel(r'$m$ [GeV]',fontsize=15)
    ax19.set_ylabel(r'$m$ [GeV]',fontsize=15)
    ax15.set_xlabel(r'PDG21+',fontsize=12)
    ax16.set_xlabel(r'PDG16+',fontsize=12)
    ax17.set_xlabel(r'SMASH',fontsize=12)
    ax19.set_xlabel(r'PDG21+',fontsize=12)
    ax20.set_xlabel(r'PDG16+',fontsize=12)
    ax21.set_xlabel(r'SMASH',fontsize=12)

    ax1.set_yticks([i for i in np.arange(0.5,3.5,0.5)],minor=False)
    ax1.set_yticks([i for i in np.arange(0,3.5,0.1)],minor=True)
    ax5.set_yticks([i for i in np.arange(0.5,3.5,0.5)],minor=False)
    ax5.set_yticks([i for i in np.arange(0,3.5,0.1)],minor=True)
    ax8.set_yticks([i for i in np.arange(0,3.5,0.5)],minor=False)
    ax8.set_yticks([i for i in np.arange(0,3.5,0.1)],minor=True)
    ax12.set_yticks([i for i in np.arange(0,3.5,0.5)],minor=False)
    ax12.set_yticks([i for i in np.arange(0,3.5,0.1)],minor=True)
    ax15.set_yticks([i for i in np.arange(0,3.5,0.5)],minor=False)
    ax15.set_yticks([i for i in np.arange(0,3.5,0.1)],minor=True)
    ax19.set_yticks([i for i in np.arange(0,3.5,0.5)],minor=False)
    ax19.set_yticks([i for i in np.arange(0,3.5,0.1)],minor=True)

    ax1.set_xlim(0,1)
    ax2.set_xlim(0,1)
    ax3.set_xlim(0,1)
    ax4.set_xlim(0,1)
    ax5.set_xlim(0,1)
    ax6.set_xlim(0,1)
    ax7.set_xlim(0,1)
    ax8.set_xlim(0,1)
    ax9.set_xlim(0,1)
    ax10.set_xlim(0,1)
    ax11.set_xlim(0,1)
    ax12.set_xlim(0,1)
    ax13.set_xlim(0,1)
    ax14.set_xlim(0,1)
    ax15.set_xlim(0,1)
    ax16.set_xlim(0,1)
    ax17.set_xlim(0,1)
    ax18.set_xlim(0,1)
    ax19.set_xlim(0,1)
    ax20.set_xlim(0,1)
    ax21.set_xlim(0,1)

    # First row
    ax1.set_ylim(0.9,2.7)
    ax2.set_ylim(0.9,2.7)
    ax3.set_ylim(0.9,2.7)
    ax5.set_ylim(0.9,3.1)
    ax6.set_ylim(0.9,3.1)
    ax7.set_ylim(0.9,3.1)
    # Second row
    ax8.set_ylim(0.9,3.3)
    ax9.set_ylim(0.9,3.3)
    ax10.set_ylim(0.9,3.3)
    ax12.set_ylim(0.9,2.7)
    ax13.set_ylim(0.9,2.7)
    ax14.set_ylim(0.9,2.7)
    # Third row
    ax15.set_ylim(0.9,2.7)
    ax16.set_ylim(0.9,2.7)
    ax17.set_ylim(0.9,2.7)
    ax19.set_ylim(0.9,2.7)
    ax20.set_ylim(0.9,2.7)
    ax21.set_ylim(0.9,2.7)

    eps = 0.05
    lw = 0.5
    # Nucleons
    ax1.text(0.2,1.1, r"$N$", fontsize=14)
    for mass in PDG21Plus_masses_nucleons.to_list():
        ax1.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='r')
    for mass in PDG16Plus_masses_nucleons.to_list():
        ax2.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='g')
    for mass in SMASH_masses_nucleons.to_list():
        ax3.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='b')
    # Deltas
    ax5.text(0.2,1.3, r"$\Delta$", fontsize=14)
    for mass in PDG21Plus_masses_deltas.to_list():
        ax5.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='r')
    for mass in PDG16Plus_masses_deltas.to_list():
        ax6.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='g')
    for mass in SMASH_masses_deltas.to_list():
        ax7.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='b')
    # Sigmas
    ax8.text(0.2,2.9, r"$\Sigma$", fontsize=14)
    for mass in PDG21Plus_masses_sigmas.to_list():
        ax8.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='r')
    for mass in PDG16Plus_masses_sigmas.to_list():
        ax9.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='g')
    for mass in SMASH_masses_sigmas.to_list():
        ax10.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='b')
    # Lambdas
    ax12.text(0.2,1.175, r"$\Lambda$", fontsize=14)
    for mass in PDG21Plus_masses_lambdas.to_list():
        ax12.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='r')
    for mass in PDG16Plus_masses_lambdas.to_list():
        ax13.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='g')
    for mass in SMASH_masses_lambdas.to_list():
        ax14.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='b')
    # Xis
    ax15.text(0.2,1.1, r"$\Xi$", fontsize=14)
    for mass in PDG21Plus_masses_xis.to_list():
        ax15.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='r')
    for mass in PDG16Plus_masses_xis.to_list():
        ax16.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='g')
    for mass in SMASH_masses_xis.to_list():
        ax17.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='b')
    # Omegas
    ax19.text(0.2,1.1, r"$\Omega$", fontsize=14)
    for mass in PDG21Plus_masses_omegas.to_list():
        ax19.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='r')
    for mass in PDG16Plus_masses_omegas.to_list():
        ax20.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='g')
    for mass in SMASH_masses_omegas.to_list():
        ax21.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='b')

    plt.tight_layout(h_pad=-0.1,w_pad=-3.9)
    fname = '../../Results/output/Fig_PDG16Plus_vs_PDG21Plus_spectrum.pdf'
    plt.savefig(fname=fname, format='pdf')
    #plt.show()

def plot_mass_spectra_new(input_df):
    df = input_df.copy()

    # Nucleons
    PDG21Plus_masses_nucleons = df[(df['Baryon no.']!=0) &\
                                 (df['Electric charge']==0) &\
                                 (df['ID']>0) &\
                                 (df['Isospin']==0.5) &\
                                 (df['Strangeness no.']==0)]['Mass(GeV)']
    PDG21_masses_nucleons = df[(df['Baryon no.']!=0) &\
                                 (df['Electric charge']==0) &\
                                 (df['ID']>0) &\
                                 (df['Isospin']==0.5) &\
                                 (df['Strangeness no.']==0) &\
                                 (df['Stars']>=2)]['Mass(GeV)']
    # Deltas
    PDG21Plus_masses_deltas = df[(df['Baryon no.']!=0) &\
                                 (df['Electric charge']==0) &\
                                 (df['ID']>0) &\
                                 (df['Isospin']==1.5) &\
                                 (df['Strangeness no.']==0)]['Mass(GeV)']
    PDG21_masses_deltas = df[(df['Baryon no.']!=0) &\
                                 (df['Electric charge']==0) &\
                                 (df['ID']>0) &\
                                 (df['Isospin']==1.5) &\
                                 (df['Strangeness no.']==0) &\
                                 (df['Stars']>=2)]['Mass(GeV)']
    # Kaons
    PDG21Plus_masses_kaons = df[(df['Baryon no.']==0) &\
                              (abs(df['Strangeness no.'])==1) &\
                              (df['Electric charge']==0) &\
                              (df['ID']>0)]['Mass(GeV)']
    PDG21_masses_kaons = df[(df['Baryon no.']==0) &\
                          (abs(df['Strangeness no.'])==1) &\
                          (df['Electric charge']==0) &\
                          (df['ID']>0) &\
                          (abs(df['Stars'])>=2)]['Mass(GeV)']
    # Lambdas
    PDG21Plus_masses_lambdas = df[(df['Baryon no.']!=0) &\
                                 (df['Electric charge']==0) &\
                                 (df['ID']>0) &\
                                 (df['Isospin']==0) &\
                                 (df['Strangeness no.']==-1)]['Mass(GeV)']
    PDG21_masses_lambdas = df[(df['Baryon no.']!=0) &\
                                 (df['Electric charge']==0) &\
                                 (df['ID']>0) &\
                                 (df['Isospin']==0) &\
                                 (df['Strangeness no.']==-1) &\
                                 (df['Stars']>=2)]['Mass(GeV)']
    # Xis
    PDG21Plus_masses_xis = df[(df['Baryon no.']!=0) &\
                            (df['Isospin']==0.5) &\
                            (df['Electric charge']==-1) &\
                            (df['ID']>0) &\
                            (abs(df['Strangeness no.'])==2)]['Mass(GeV)']
    PDG21_masses_xis = df[(df['Baryon no.']!=0) &\
                            (df['Isospin']==0.5) &\
                            (abs(df['Strangeness no.'])==2) &\
                            (df['Electric charge']==-1) &\
                            (df['ID']>0) &\
                            (df['Stars']>=2)]['Mass(GeV)']
    # Sigmas
    PDG21Plus_masses_sigmas = df[(df['Baryon no.']!=0) &\
                                 (df['Electric charge']==0) &\
                                 (df['ID']>0) &\
                                 (df['Isospin']==1) &\
                                 (df['Strangeness no.']==-1)]['Mass(GeV)']
    PDG21_masses_sigmas = df[(df['Baryon no.']!=0) &\
                                 (df['Electric charge']==0) &\
                                 (df['ID']>0) &\
                                 (df['Isospin']==1) &\
                                 (df['Strangeness no.']==-1) &\
                                 (df['Stars']>=2)]['Mass(GeV)']
    # Omegas
    PDG21Plus_masses_omegas = df[(df['Baryon no.']!=0) &\
                                 (df['Electric charge']==-1) &\
                                 (df['ID']>0) &\
                                 (df['Isospin']==0) &\
                                 (df['Strangeness no.']==-3)]['Mass(GeV)']
    PDG21_masses_omegas = df[(df['Baryon no.']!=0) &\
                                 (df['Electric charge']==-1) &\
                                 (df['ID']>0) &\
                                 (df['Isospin']==0) &\
                                 (df['Strangeness no.']==-3) &\
                                 (df['Stars']>=2)]['Mass(GeV)']

    fig = plt.figure(figsize=(5,7.5))
    #First row
    ax1 = fig.add_subplot(3,5,1)
    ax2 = fig.add_subplot(3,5,2)
    ax3 = fig.add_subplot(3,5,3)
    ax4 = fig.add_subplot(3,5,4)
    ax5 = fig.add_subplot(3,5,5)
    #Second row
    ax6 = fig.add_subplot(3,5,6)
    ax7 = fig.add_subplot(3,5,7)
    ax8 = fig.add_subplot(3,5,8)
    ax9 = fig.add_subplot(3,5,9)
    ax10 = fig.add_subplot(3,5,10)
    #Third row
    ax11 = fig.add_subplot(3,5,11)
    ax12 = fig.add_subplot(3,5,12)
    ax13 = fig.add_subplot(3,5,13)
    ax14 = fig.add_subplot(3,5,14)
    ax15 = fig.add_subplot(3,5,15)
    ax3.set_visible(False)
    ax8.set_visible(False)
    ax13.set_visible(False)

    #x-axis
    xparams = {'axis':'x','which':'both','bottom':False,'top':False,'labelbottom':False}
    yparams = {'axis':'y','which':'both','left':False,'right':False,'labelleft':False}
    ax1.tick_params(**xparams)
    ax2.tick_params(**xparams)
    ax2.tick_params(**yparams)
    ax3.tick_params(**xparams)
    ax3.tick_params(**yparams)
    ax4.tick_params(**xparams)
    #ax4.tick_params(**yparams)
    ax5.tick_params(**xparams)
    ax5.tick_params(**yparams)
    ax6.tick_params(**xparams)
    ax7.tick_params(**xparams)
    ax7.tick_params(**yparams)
    ax8.tick_params(**xparams)
    ax8.tick_params(**yparams)
    ax9.tick_params(**xparams)
    #ax9.tick_params(**yparams)
    ax10.tick_params(**xparams)
    ax10.tick_params(**yparams)
    ax11.tick_params(**xparams)
    ax12.tick_params(**xparams)
    ax12.tick_params(**yparams)
    ax13.tick_params(**xparams)
    ax13.tick_params(**yparams)
    ax14.tick_params(**xparams)
    #ax14.tick_params(**yparams)
    ax15.tick_params(**xparams)
    ax15.tick_params(**yparams)
    #y-axis
    ax1.set_ylabel(r'$m$ [GeV]',fontsize=13)
    ax4.set_ylabel(r'$m$ [GeV]',fontsize=13)
    ax6.set_ylabel(r'$m$ [GeV]',fontsize=13)
    ax9.set_ylabel(r'$m$ [GeV]',fontsize=13)
    ax11.set_ylabel(r'$m$ [GeV]',fontsize=13)
    ax14.set_ylabel(r'$m$ [GeV]',fontsize=13)
    ax11.set_xlabel(r'PDG21+',fontsize=12)
    ax12.set_xlabel(r'PDG21',fontsize=12)
    ax14.set_xlabel(r'PDG21+',fontsize=12)
    ax15.set_xlabel(r'PDG21',fontsize=12)

    ax1.set_yticks([i for i in np.arange(0.5,3.5,0.5)],minor=False)
    ax1.set_yticks([i for i in np.arange(0,3.5,0.1)],minor=True)
    ax4.set_yticks([i for i in np.arange(0.5,3.5,0.5)],minor=False)
    ax4.set_yticks([i for i in np.arange(0,3.5,0.1)],minor=True)
    ax6.set_yticks([i for i in np.arange(0,3.5,0.5)],minor=False)
    ax6.set_yticks([i for i in np.arange(0,3.5,0.1)],minor=True)
    ax9.set_yticks([i for i in np.arange(0,3.5,0.5)],minor=False)
    ax9.set_yticks([i for i in np.arange(0,3.5,0.1)],minor=True)
    ax11.set_yticks([i for i in np.arange(0,3.5,0.5)],minor=False)
    ax11.set_yticks([i for i in np.arange(0,3.5,0.1)],minor=True)
    ax14.set_yticks([i for i in np.arange(0,3.5,0.5)],minor=False)
    ax14.set_yticks([i for i in np.arange(0,3.5,0.1)],minor=True)

    ax1.set_xlim(0,1)
    ax2.set_xlim(0,1)
    ax3.set_xlim(0,1)
    ax4.set_xlim(0,1)
    ax5.set_xlim(0,1)
    ax6.set_xlim(0,1)
    ax7.set_xlim(0,1)
    ax8.set_xlim(0,1)
    ax9.set_xlim(0,1)
    ax10.set_xlim(0,1)
    ax11.set_xlim(0,1)
    ax12.set_xlim(0,1)
    ax13.set_xlim(0,1)
    ax14.set_xlim(0,1)
    ax15.set_xlim(0,1)

    # First row
    ax1.set_ylim(0.9,2.7)
    ax2.set_ylim(0.9,2.7)
    ax4.set_ylim(0.9,3.1)
    ax5.set_ylim(0.9,3.1)
    # Second row
    ax6.set_ylim(0.9,3.3)
    ax7.set_ylim(0.9,3.3)
    ax9.set_ylim(0.9,2.7)
    ax10.set_ylim(0.9,2.7)
    # Third row
    ax11.set_ylim(0.9,2.7)
    ax12.set_ylim(0.9,2.7)
    ax14.set_ylim(0.9,2.7)
    ax15.set_ylim(0.9,2.7)

    eps = 0.05
    lw = 0.5
    # Nucleons
    ax1.text(0.2,1.1, r"$N$", fontsize=14)
    for mass in PDG21Plus_masses_nucleons.to_list():
        ax1.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='r')
    for mass in PDG21_masses_nucleons.to_list():
        ax2.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='c')
    # Deltas
    ax4.text(0.2,1.3, r"$\Delta$", fontsize=14)
    for mass in PDG21Plus_masses_deltas.to_list():
        ax4.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='r')
    for mass in PDG21_masses_deltas.to_list():
        ax5.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='c')
    # Sigmas
    ax6.text(0.2,2.9, r"$\Sigma$", fontsize=14)
    for mass in PDG21Plus_masses_sigmas.to_list():
        ax6.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='r')
    for mass in PDG21_masses_sigmas.to_list():
        ax7.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='c')
    # Lambdas
    ax9.text(0.2,1.175, r"$\Lambda$", fontsize=14)
    for mass in PDG21Plus_masses_lambdas.to_list():
        ax9.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='r')
    for mass in PDG21_masses_lambdas.to_list():
        ax10.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='c')
    # Xis
    ax11.text(0.2,1.1, r"$\Xi$", fontsize=14)
    for mass in PDG21Plus_masses_xis.to_list():
        ax11.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='r')
    for mass in PDG21_masses_xis.to_list():
        ax12.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='c')
    # Omegas
    ax14.text(0.2,1.1, r"$\Omega$", fontsize=14)
    for mass in PDG21Plus_masses_omegas.to_list():
        ax14.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='r')
    for mass in PDG21_masses_omegas.to_list():
        ax15.axhline(mass,xmin=eps,xmax=1-eps,linewidth=lw,color='c')

    plt.tight_layout(h_pad=-0.1,w_pad=-3.7)
    fname = '../../Results/output/Fig_PDG21Plus_spectrum.pdf'
    plt.savefig(fname=fname, format='pdf')
    #plt.show()
