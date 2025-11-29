'''
VARIANT_EXTRACTION — A Python package and CLI tool to extract and visualize process behaviors from complex event data.
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
### DEFINITIONS FOR PROPERTY DEFINITIONS
#######

import numpy as np


## GENERAL DATA PROCESSING
###

def inputNumbers(min_range=0, max_range=1, message='Select a number from the list:', any_float=False):
    """An input-prompt function, which allows an integer within a range or any float number. 

    Keyword arguments:
    min_range -- lower bound range for input (default 0)
    max_range -- upper bound range for input (default 1)
    message -- message for input (default 'Select a number from the list:')
    any_float -- accept any float (default False)
    """
    number = 0
    if any_float == False:
        while True:
            try:
                number = int(input(message))
            except ValueError:
                   print('No integer. Try again.')
            else:
                if min_range <= number <= max_range:
                    break
                else:
                    print('Out of range. Try again')  
    elif any_float == True:
        while True and type(number)!=float:
            try:
                number = float(input(message))
            except ValueError:
                print('No float. Try again.')   
    print(f"You chose: {number}")
    return number

def listDictionary(dictionary: dict):
    """Prints all entries in a dictionary."""
    for entry in dictionary:
        print(f"{entry} - {dictionary.get(entry)}") 

def datatypeChecker(df, column: str):
    """Returns the datatype (categorical, numerical, timestamp, other) of a column in a dataframe.

    Keyword arguments:
    df -- dataframe
    column -- column name
    """
    data_type = ""
    if column in df.select_dtypes(include=['object']):
        data_type = "categorical"
    elif column in df.select_dtypes(include=[np.number, 'number']): # alternative: df._get_numeric_data()
        data_type = "numerical"
    elif column in df.select_dtypes(include=[np.datetime64, 'datetime', 'datetime64', 'datetimetz', 'datetime64[ns, UTC]']):
        data_type = "datetime"
    else:
        data_type = "other"
    return data_type

def attributelevelChecker(df, column: str, COLUMNS: dict):
    """Returns the attribute type (case, event, or other) of a column in a dataframe.

    Keyword arguments:
    df -- event log as dataframe
    column -- column name
    COLUMNS -- dictionary with column names to indicate e.g., case attribute
    """
    attribute_level = ""
    type_amount = len(df.groupby([COLUMNS.get('case')], group_keys=True)[column].nunique().unique())
    if 1 == type_amount:
        attribute_level = "case"
    elif 1 < type_amount:
        attribute_level = "event"
    else:
        attribute_level = "other"
    return attribute_level

def functionListing(attribute_type: str, data_type :str):
    """Returns a list of possible attribute- and data type functions for a certain attribute- and data type.

    Keyword arguments:
    attribute_type -- for instance 'event' or 'case'
    data_type -- for instance 'categorial' or 'numerical'
    """
    attribute_functions = []
    data_type_functions = []
    # attribute type: case
    if attribute_type=='case':
        attribute_functions.extend(['case'])
    # attribute type: event
    elif attribute_type=='event' and data_type=='numerical':
        attribute_functions.extend(['event_sum', 'event_mean', 'event_median'])
    else:
        attribute_functions.extend(['event_sum'])
    # datatype: categorial or numerical
    if data_type=='categorial' or 'numerical':
        data_type_functions.extend(['categories'])
        if data_type=='categorial':
            # Possible extensions: "selection of some attributes"
            None
        # datatype: numerical
        if data_type=='numerical':
            data_type_functions.extend(['threshold'])
            # Possible extensions: "binning"
    # datatype: datetime
    if data_type=='datetime' or '':
        None
    # datatype: other
    if data_type=='other':
        None
    return attribute_functions, data_type_functions

def functionInput(attribute_functions: list, data_type_functions: list):
    """User can select one function from a list of functions. The selection is returned as a list.

    Keyword arguments:
    attribute_functions -- list of all possible attribute functions 
    data_type_functions -- list of all possible data type functions
    """ 
    # TODO: Create an information function for each function
    if len(attribute_functions) > 1:
        print("\nThe following functions are available to summarize the attribute values:")
        attribute_functions_options = {}
        i = 0
        for f in attribute_functions:
            i+=1
            attribute_functions_options.update({i:f})
            print(f"{i} - {f}")
    if len(data_type_functions) > 1:
        print("\nThe following property functions are available for this attribute:")
        data_type_functions_options = {}
        i = 0
        for f in data_type_functions:
            i+=1
            data_type_functions_options.update({i:f})
            print(f"{i} - {f}")

    # Select an attribute & data type functions
    property_set = []
    if len(attribute_functions) > 1:
        message = "Please choose a function to summarize the attribute values: "
        selection = inputNumbers(min_range=1, max_range=len(attribute_functions_options), message=message)
        #print(attribute_functions_options[selection])
        property_set.append(attribute_functions_options[selection])
    else: 
        #print(attribute_functions)
        property_set.extend(attribute_functions)
    if len(data_type_functions) > 1:
        message = "Please choose a property function: "
        selection = inputNumbers(min_range=1, max_range=len(data_type_functions_options), message=message)
        #print(data_type_functions_options[selection])
        property_set.append(data_type_functions_options[selection])
        if 'threshold' in data_type_functions_options[selection]:
            message = "Define a threshold (float):"
            selection = inputNumbers(min_range=1, max_range=len(data_type_functions_options), message=message, any_float=True)
            property_set.append(selection)
    else: 
        #print(data_type_functions)
        property_set.extend(data_type_functions)
    return property_set


## PROPERTY DEFINITION
####

def propertyDefinition(df, COLUMNS: dict):
    """A function to define properties for an event log. Returns a property dictionary.

    Keyword arguments:
    df -- event log as dataframe
    COLUMNS -- dictionary with column names to indicate e.g., case attribute
    """
    # list all attributes in event log
    attribute_list = {}
    for index, attribute in enumerate(df.columns.tolist()):
        attribute_list[index] = attribute
    print("\nList of attributes in the event log:")
    listDictionary(attribute_list)
    # user chooses attributes for property definition
    message = "\nChoose all attributes to consider as a property.\nEnter the keys as a list separated by space:"
    property_keys = my_list = list(map(int,input(message).split()))
    attributes = [attribute_list[key] for key in property_keys]
    # user selects functions for properties
    print("\nCREATE PROPERTIES")
    print("Whenever possible, you will be able to create properties for each chosen attributes.")
    property_dict = propertySelection(df, COLUMNS, attributes)
    # summary of properties created
    print("\n---------------")
    print(f"PROPERTY SUMMARY:")
    print("---------------")
    for p in property_dict:
        print(f"property {p}: {property_dict[p]}")
    return property_dict

def propertySelection(df, COLUMNS: dict, attributes: list):
    """Function to prompt user to select type of properties.

    Keyword arguments:
    df -- event log as dataframe
    COLUMNS -- dictionary with column names to indicate e.g., case attribute
    attributes -- list of attributes to consider in input
    """
    # TODO: Extend to create more property types for each attribute
    property_key = 0
    property_dict = {}
    for a in attributes:
        # Check if property is numerical or categorical
        attribute_type = attributelevelChecker(df, a, COLUMNS)
        data_type = datatypeChecker(df, a)
        # Description of attribute to help analyst when creating the properties
        print("\n---------------")
        print(f"Attribute: {a}")
        print("---------------")
        print(f"attribute type: {attribute_type}")
        print(f"data type: {data_type}")
        print(f"max value: {df[a].dropna().unique().max()}")
        print(f"min value: {df[a].dropna().unique().min()}")

        loop = True
        while loop:
            property_key+=1
            property_attributes = {}
            
            # Info
            print(f"\n--\nProperty number: {property_key}")
            
            # Input a function
            attribute_functions, data_type_functions = functionListing(attribute_type, data_type)
            property_set = functionInput(attribute_functions, data_type_functions)

            # Automatic: List all property-functions available for a specific attribute type
            attribute_functions, data_type_functions = functionListing(attribute_type, data_type)

            # Create a property column
            property_attributes.update({a:property_set})

            # Create another property of the attribute
            if len(attribute_functions)>1 or len(data_type_functions)>1:
                print("\nDo you want to create an additional attribute of the same attribute (1=yes; 2=no)?")
                message = "Enter 1 or 2:"
                selection = inputNumbers(min_range=1, max_range=2, message=message)
                if selection == 2:
                    print(f"=> property {property_key} finished.")
                    loop = False
            else:
                print(f"=> property {property_key} finished (no options available).")
                loop = False
            property_dict.update({property_key: property_attributes})
    return property_dict

