import numpy as np

## GENERAL DATA PROCESSING
###

def inputNumbers(min_range=0, max_range=1, message='Select a number from the list:', any_float=False):
    """Input a number within a certain range. 
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

def listDictionary(dictionary):
    """ Prints all entries in a dictionary.
    """
    print("\nList of attributes in the event log:")
    for entry in dictionary:
        print(f"{entry} - {dictionary.get(entry)}") 

# check data type functions
def datatypeChecker(df, column):
    """ Returns the datatype (categorical, numerical, timestamp, other) of a column in a dataframe.
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

def attributelevelChecker(df, column, CASE_COLUMN):
    """ Returns the attribute type (case, event, or other) of a column in a dataframe.
    """
    attribute_level = ""
    type_amount = len(df.groupby([CASE_COLUMN], group_keys=True)[column].nunique().unique())
    
    if 1 == type_amount:
        attribute_level = "case"
    elif 1 < type_amount:
        attribute_level = "event"
    else:
        attribute_level = "other"
    
    return attribute_level


def functionListing(attribute_type, data_type):
    """Returns a list of possible attribute and data type functions for a certain attribute- and data type.
    """
    
    attribute_functions = []
    data_type_functions = []
    
    # case
    if attribute_type=='case':
        attribute_functions.extend(['case'])
    
    # event
    elif attribute_type=='event' and data_type=='numerical':
        attribute_functions.extend(['event_sum', 'event_mean', 'event_median'])
    else:
        attribute_functions.extend(['event_sum'])
    
    # categorial or numerical
    if data_type=='categorial' or 'numerical':
        data_type_functions.extend(['categories'])
    
        if data_type=='categorial':
            # Possible extensions: "selection of some attributes"
            None

        # numerical
        if data_type=='numerical':
            data_type_functions.extend(['threshold'])
            # Possible extensions: "binning"
    
    # datetime
    if data_type=='datetime' or '':
        None
        
    # other
    if data_type=='other':
        None

    return attribute_functions, data_type_functions

def functionInput(attribute_functions, data_type_functions):
    """ User can select one function from a list of functions. The selection is returned as a list.
    """
    
    # ToDo: Create an information function for each function
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

def propertyDefinition(df, CASE_COLUMN):
    """ Defines all properties. Returns a list of properties.
    """
    
    # list all attributes in event log
    attribute_list = {}
    for index, attribute in enumerate(df.columns.tolist()):
        attribute_list[index] = attribute
    listDictionary(attribute_list)
    
    # user chooses attributes for property definition
    message = "\nChoose all attributes to consider as a property.\nEnter the keys as a list separated by space:"
    property_keys = my_list = list(map(int,input(message).split()))
    attributes = [attribute_list[key] for key in property_keys]
    
    # user selects functions for properties
    print("\nCREATE PROPERTIES")
    print("Whenever possible, you will be able to create properties for each chosen attributes.")
    property_dict = propertySelection(df, CASE_COLUMN, attributes)
    
    # summary of properties created
    print("\n---------------")
    print(f"PROPERTY SUMMARY:")
    print("---------------")
    for p in property_dict:
        print(f"property {p}: {property_dict[p]}")
    
    return property_dict

def propertySelection(df, CASE_COLUMN, attributes):
    """ User selects type of properties.
    """
    # ToDo: Extend to create more property types for each attribute
    property_key = 0
    property_dict = {}

    for a in attributes:
        
        # Check if property is numerical or categorical
        attribute_type = attributelevelChecker(df, a, CASE_COLUMN)
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

