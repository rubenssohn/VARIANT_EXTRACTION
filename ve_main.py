###########
### VARIANT EXTRACTION MAIN METHOD
#######
from ve_methods.ve_logprocessing import * 
from ve_methods.ve_propertydefinition import * 
from ve_methods.ve_featuregeneration import * 


def main():
    """Returns an event log extended with variants."""
    
    print("\n###############\nSTART")
    print("VARIANT ANALYSIS\n---")
    
    # IMPORT
    print("\nTASK: Log import")
    logname, COLUMNS = selectLog()
    df  = importLog(f"data/input/{logname}", COLUMNS)

    # PROPERTY DEFINITION
    print("\nTASK: Property definition")
    property_dict = propertyDefinition(df, COLUMNS)
    
    # INSTANCE DEFINITION
    print("\nTASK: Instance definition")
    df_in = instancelogConversion(df, COLUMNS, property_dict)
    
    print(df_in)

    # BINARY MAPPING and VARIANT CLASSICATION
    print("\nTASK: Binary mapping.")
    df_var, df_binary = binaryMapping(df_in)
    
    print(df_var)
    
    # EXTEND AND EXPORT LOGS
    print("\nTASK: Binary mapping.")
    df = exportLogs(df, df_var, COLUMNS)
    print("Files were exported. Please see the output folder.")
    
    print("\n END\n###############")
    return df

if __name__ == "__main__":
    main()