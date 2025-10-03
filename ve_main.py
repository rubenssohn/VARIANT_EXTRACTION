'''
VARIANT_EXTRACTION — A CLI tool to extract context-based process variants from conventional event logs.
Copyright (C) 2023  Christoffer Rubensson

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Website: https://hu-berlin.de/rubensson
E-Mail: {firstname.lastname}@hu-berlin.de
'''

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
    df = exportLogs(df, df_var, property_dict, COLUMNS)
    print("Files were exported. Please see the output folder.")
    
    print("\n END\n###############")
    return df

if __name__ == "__main__":
    main()