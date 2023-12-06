###########
### FEATURE GENARATION METHODS
#######

import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def binaryMapping(df_in):
    """Binary mapping function to transform an instance log."""
    # binary mapping from dataframe
    encoder = OneHotEncoder()
    binary_map = pd.DataFrame(encoder.fit_transform(df_in).toarray())
    feature_columns = encoder.get_feature_names_out()
    # merge dataframes
    df_binary = binary_map.set_axis(feature_columns, axis=1)
    df_binary = binarysequenceClassification(df_binary)
    df_var, df_binary = mergeInstanceDataframes(df_in, df_binary)
    return df_var, df_binary

def binarysequenceClassification(df_binary):
    """Converts a binary sequence onto a decimal numbers in a log with a binary sequence column. 
    Returns an extended log."""
    binary_codes = []
    for index in df_binary.index:
        sequence = df_binary.loc[index].tolist()
        binary_codes.append(''.join(str(int(number)) for number in sequence))
    df_binary['property_code'] = binary_codes
    df_binary["variant"] = pd.Categorical(df_binary['property_code']).codes
    return df_binary

def mergeInstanceDataframes(df_in, df_binary):
    """ Merges an instance log dataframe with binary log dataframe.
    """
    df_binary["instance"] = df_in.index
    df_binary.set_index('instance')
    df_var = df_in.merge(df_binary,left_on='instance', right_on='instance').set_index("instance")
    return df_var, df_binary