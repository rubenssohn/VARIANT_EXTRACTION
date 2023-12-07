###########
###  LOG PROCESSING METHODS
#######
import pandas as pd
import pm4py
from ve_methods.ve_propertydefinition import inputNumbers, listDictionary

## IMPORT
####

def selectLog():
    # Input the name of the log in "data/input" folder
    print("Please write the name of the event log file (e.g., log.xes):")
    message = "Enter the filename:"
    logname = str(input(message))
    
    # Choose column names for some log attributes
    COLUMNS = {
        'case': 'case:concept:name',
        'activity': 'concept:name',
        'time': 'time:timestamp'
    }
    while True:
        print('\nThe program defines the following case/event attributes as follows:')
        listDictionary(COLUMNS)
        print("\nDo you confirm? (1=yes, 2=no)")
        selection = inputNumbers(min_range=1, max_range=2)
        if selection == 1:
            break
        elif selection == 2:
            message = "Enter the name of the case attribute:"
            COLUMNS['case'] = str(input(message))
            message = "Enter the name of the activity attribute:"
            COLUMNS['activity'] = str(input(message))
            message = "Enter the name of the timestamp attribute:"
            COLUMNS['time'] = str(input(message))
    return logname, COLUMNS

def importLog(path: str, COLUMNS: dict):
    """Simple event log importer (XES).

    Keyword arguments:
    path -- path to folder with event log
    case_col -- column name for case attribute
    activity_col -- column name for activity attribute
    time_col -- column name for timestamp attribute
    """

    # TODO: Extend to .csv-files
    df = pm4py.read_xes(path)
    df = df.sort_values(by=COLUMNS.get('time'))
    return df

def exportLogs(df, df_var, COLUMNS: dict, path='data/output/'):
    """Simple event log exporter (from dataframe to .CSV).

    Keyword arguments:
    df -- original event log as dataframe
    df_var -- event log extended with variant column as dataframe
    COLUMNS -- dictionary with column names to indicate e.g., case attribute
    path --path to folder (default 'data/output/')
    """
    df = extendwithVariants(df, df_var, COLUMNS)
    # Export CSV file
    df.to_csv(path+"variant_log.csv")
    df_var.to_csv(path+"variant_calculation.csv")
    # Export XES file
    pm4py.write_xes(df, path+"variant_log.xes")
    return df

def extendwithVariants(df, df_var, COLUMNS: dict):
    """Map variants from instances to cases in original log.

    Keyword arguments:
    df -- original event log as dataframe
    df_var -- event log extended with variant column as dataframe
    COLUMNS -- dictionary with column names to indicate e.g., case attribute
    """
    df['Variant'] = df[COLUMNS.get('case')].map(df_var["variant"])
    return df


## INSTANCE LOG PROCESSING
####
# TODO property_columns : change to "property_dict"

def extendInstancelog(df, df_in, COLUMNS: dict, property_dict: dict): # COLUMNS was deleted
    """Extends an instance dataset with attribute values. 

    Keyword arguments:
    df -- event log as dataframe
    df_in -- instance event log as dataframe
    COLUMNS -- dictionary with column names to indicate e.g., case attribute
    property_dict -- dictionary with defined properties
    """
    # creates a new column in the log for each property defined in the property dictionary
    for p in property_dict:
        attribute = list(property_dict[p].keys())[0] 
        function_list = property_dict[p][attribute] 
        try: 
            property_name = f"p{p}_{attribute}_{function_list[0]}_{function_list[1]}_>={function_list[2]}"
        except:
            property_name = f"p{p}_{attribute}_{function_list[0]}_{function_list[1]}"
        # TRANSFORMATION FUNCTIONS (I):
        # - case attribute function
        if function_list[0] == 'case':
            col = df.groupby(COLUMNS.get('case'))[attribute].max() 
        # - event_sum sums up event attribute values
        if function_list[0] == 'event_sum':
            col = df.groupby(COLUMNS.get('case'))[attribute].sum()
        # - event_mean returns the mean event attribute value
        if function_list[0] == 'event_mean':
            col = df.groupby(COLUMNS.get('case'))[attribute].mean()
        # - event_median returns the mean event attribute value
        if function_list[0] == 'event_median':
            col = df.groupby(COLUMNS.get('case'))[attribute].median()  
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
        # - threshold defines a 
        if function_list[1] == 'threshold':
            col = col >= function_list[2]

        # extend instance log with the new "property" column
        df_in[property_name] = col
    return df_in

def instancelogConversion(df, COLUMNS: dict, property_dict: dict):
    """Extracts cases from a log and creates new dataframe where each row represents an instance.

    Keyword arguments:
    df -- original event log as dataframe
    COLUMNS -- dictionary with column names to indicate e.g., case attribute
    property_dict -- dictionary with defined properties
    """
    # TODO: Change "case" to some other value such as "instance"
    
    # Create dataframe with only instances and set instance names as index
    instances = df[COLUMNS.get("case")].unique().tolist()
    df_in = pd.DataFrame({'instance': instances}).set_index('instance')
    # Extend the instance log with features based on the property dictionary
    df_in = extendInstancelog(df, df_in, COLUMNS, property_dict)
    return df_in