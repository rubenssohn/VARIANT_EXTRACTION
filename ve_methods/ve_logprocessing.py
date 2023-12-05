import pandas as pd

# Columns
CASE_COLUMN = 'case:concept:name'
ACTIVITY_COLUMN = 'concept:name'
TIMESTAMP_COLUMN = 'time:timestamp'
RESOURCE_COLUMN = 'org:group'

## IMPORT
####

import pm4py

def importLog(path):
    """ Simple event log importer (XES).
    """
    
    # ToDo: Try out different column names
    # Columns
    COLUMNS = {
        'case': 'case:concept:name',
        'activity': 'concept:name',
        'time': 'time:timestamp',
        'resource': 'org:group'
    }
    
    # ToDo: Extend to .csv-files
    df = pm4py.read_xes(path)
    df = df.sort_values(by=COLUMNS.get('time'))
    return df, COLUMNS

def exportLogs(df, df_var, COLUMNS, path='data/output/'):
    
    df = extendwithVariants(df, df_var, COLUMNS)
    
    # ToDo: 
    df.to_csv(path+"variant_log.csv")
    df_var.to_csv(path+"variant_calculation.csv")
    
    return df

def extendwithVariants(df, df_var, COLUMNS):
    """ Map variants from instances to cases in original log.
    """
    df['Variant'] = df[COLUMNS.get('case')].map(df_var["variant"])
    
    return df

## INSTANCE LOG PROCESSING
####

# ToDo property_columns : change to "property_dict"

def extendInstancelog(df, COLUMNS, df_in, property_dict):
    """ Extends an instance dataset with attribute values. 
    """

    for p in property_dict:
        
        attribute = list(property_dict[p].keys())[0] 
        function_list = property_dict[p][attribute] 
        try: 
            property_name = f"p{p}_{attribute}_{function_list[0]}_{function_list[1]}_>={function_list[2]}"
        except:
            property_name = f"p{p}_{attribute}_{function_list[0]}_{function_list[1]}"

        # TRANSFORMATION FUNCTIONS (I):
        # - case
        if function_list[0] == 'case':
            col = df.groupby(CASE_COLUMN)[attribute].max()
            
        # - event_sum
        if function_list[0] == 'event_sum':
            col = df.groupby(CASE_COLUMN)[attribute].sum()
        # - event_mean
        if function_list[0] == 'event_mean':
            col = df.groupby(CASE_COLUMN)[attribute].mean()
        # - event_median
        if function_list[0] == 'event_median':
            col = df.groupby(CASE_COLUMN)[attribute].median()
            
        # - event_datetime: none
        if function_list[0] == 'datetime':
            None
        # - event_other: none
        if function_list[0] == 'other':
            None

        # TRANSFORMATION FUNCTIONS (II):
        # - categories
        if function_list[1] == 'categories':
            None
        # - threshold
        if function_list[1] == 'threshold':
            col = col >= function_list[2]
        
        # extend instance log with new column
        df_in[property_name] = col
        
    return df_in

def instancelogConversion(df, COLUMNS, property_dict):
    """ Extracts cases from a log and creates new dataframe where each row represents an instance.
    """
    # ToDo: Change "case" to some other value such as "instance"
    
    # Create dataframe with only instances and set instance names as index
    instances = df[COLUMNS.get("case")].unique().tolist()
    df_in = pd.DataFrame({'instance': instances}).set_index('instance')
    
    # Extend the instance log with features based on the property dictionary
    df_in = extendInstancelog(df, COLUMNS, df_in, property_dict)
    
    return df_in