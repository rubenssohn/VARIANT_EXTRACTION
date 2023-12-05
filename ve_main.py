from ve_methods.ve_logprocessing import * 
from ve_methods.ve_propertydefinition import * 
from ve_methods.ve_featuregeneration import * 

def main():
    
    print("\n###############\nSTART")
    print("VARIANT ANALYSIS\n---")
    
    # IMPORT
    print("\nTASK: Log import")
    df, COLUMNS = importLog("data/input/sepsis-log.xes")

    # PROPERTY DEFINITION
    print("\nTASK: Property definition")
    #property_columns = propertyDefinition2(df) # OLD
    property_dict = propertyDefinition(df, CASE_COLUMN)
    
    # INSTANCE DEFINITION
    print("\nTASK: Instance definition")
    #df_in = instancelogConversion2(df, COLUMNS, property_columns) # OLD
    df_in = instancelogConversion(df, COLUMNS, property_dict)
    
    print(df_in)

    # BINARY MAPPING and VARIANT CLASSICATION
    print("\nTASK: Binary mapping.")
    df_var, df_binary = binaryMapping(df_in)
    
    print(df_var)
    
    # EXTEND AND EXPORT LOGS
    print("\nTASK: Binary mapping.")
    df = exportLogs(df, df_var, COLUMNS)
    print("Files were exported.")
    
    print("\n END\n###############")
    return df

if __name__ == "__main__":
    main()