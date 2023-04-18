def build_decay_channel_number(input_df):
    """Fills up the decay channel column according to listed decays"""
    df = input_df.copy()
    count_series = df.groupby('ID')['ID'].transform('count')-1
    mask = df['No. of decay channels'].notnull()
    df.loc[mask, 'No. of decay channels'] = count_series
    return df