import pandas as pd

def test_charge_conservation(input_df):
    """Verifies that decay products conserve baryon, strange, charm,
    bottom, and electric numbers and charges"""
    # TO DO
    df = input_df.copy()
    return ('Charge conservation', True)

def test_mass_conservation(input_df):
    """Verifies that decay products have less mass than the decaying particle"""
    # TO DO
    df = input_df.copy()
    return ('Mass conservation', True)

def test_decay_products_existence(input_df):
    """Verifies that all particles referenced in decaying channels exist"""
    # TO DO
    df = input_df.copy()
    return ('Decay products existence', True)

def test_decay_products_number(input_df):
    """Verifies that the number of products matches the listed products"""
    # TO DO
    df = input_df.copy()
    return ('Decay products number', True)

def test_BR_sum(input_df):
    """Verifies the sum of all branching ratios is equal to 1"""
    # TO DO
    df = input_df.copy()
    return ('Branching ratio sum equals 1', True)

def test_no_repeating_IDs(input_df):
    """Verifies that no ID number is used for more than one particle"""
    # TO DO
    df = input_df.copy()
    return ('No repeating IDs', True)

def test_no_repeating_decay_channels(input_df):
    """Verifies that decaying channels are not repeated"""
    df = input_df.copy()
    duplicated = df[df.duplicated()]
    return ('No repeating decay channels', duplicated.empty)

def test_particles_vs_antiparticles_decays(input_df):
    """Verifies that the number and type of decays for particles
    and antiparticles is the same in all decays"""
    # TO DO
    df = input_df.copy()
    return ('Particle-antiparticle decay balance', True)

def all_tests(input_df):
    test_list = [test_charge_conservation(input_df),\
                 test_mass_conservation(input_df),\
                 test_decay_products_existence(input_df),\
                 test_decay_products_number(input_df),\
                 test_BR_sum(input_df),\
                 test_no_repeating_IDs(input_df),\
                 test_no_repeating_decay_channels(input_df),\
                 test_particles_vs_antiparticles_decays(input_df)]
    passed_tests = []
    failed_tests = []
    for test_name, test_outcome in test_list:
        if test_outcome == True:
            passed_tests.append(test_name)
        else:
            failed_tests.append(test_name)
    if len(failed_tests) > 0:
        return (failed_tests,False)
    else:
        return (passed_tests,True)
