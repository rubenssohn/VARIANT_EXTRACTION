# VARIANT_EXTRACTION
This repository comprises the variant extraction tool proposed in the paper "Variants of Variants: Context-based Variant Analysis for Process Mining," which was published in the Advanced Information Systems Engineering Proceeding from Springer 2024. 

Reference:
Rubensson, C., Mendling, J., Weidlich, M. (2024). Variants of Variants: Context-Based Variant Analysis for Process Mining. In: Guizzardi, G., Santoro, F., Mouratidis, H., Soffer, P. (eds) Advanced Information Systems Engineering. CAiSE 2024. Lecture Notes in Computer Science, vol 14663. Springer, Cham. https://doi.org/10.1007/978-3-031-61057-8_23

---

## Setup
1. Install the necessary packages (see the requirements below)
2. Download and place the "VARIANT_EXTRACTION" folder somewhere on your computer
3. Add an event log (.xes) in the folder `"/data/input"` (e.g., the sepsis log: https://data.4tu.nl/articles/_/12707639/1) 

**REQUIREMENTS (incl. recommended versions)**
* Anaconda (2023.09): https://anaconda.org 
* Python (3.11.6): https://www.python.org
* PM4PY (2.7.8): https://pm4py.fit.fraunhofer.de
* Jupyter lab (3.6.3): https://jupyter.org
* Pandas (2.1.1): https://pandas.pydata.org
* NumPy (1.24.3): https://numpy.org
* Scikit-Learn (1.3.0): https://scikit-learn.org

---
## HOW TO USE APPLICATION: 
## Execute Program
1. Open the terminal on your computer (e.g., "Terminal" on MacOS)
2. In the terminal: Navigate to the folder "VARIANT_EXTRACTION" via the terminal (`$cd ./VARIANT_EXTRACTION`)
3. Execute the program:
  a. in the command-line tool: (`$ python ve_main.py`), or
  b. in a Jupyter notebook: Open the Jupyter notebook "ve_jupyter.ipynb" with (`$ jupyterlab`).
4. After execution, you can retrieve the extended log and its calculations in the folder `"/data/output"`. 

## Usage
The program will guide you through five stages:
1. IMPORT: You are prompted to select a log and confirm the standard event/case attributes (case, activity, and timestamp).
2. PROPERTY DEFINITION: You are able to define properties to calculate variants.
3. INSTANCE DEFINITION: The program creates a new instance log (automatically).
4. BINARY MAPPING & VARIANT CLASSIFICATION: The program utilizes a one-hot encoder to transform the log based on the properties and calculate the variants.
5. EXTEND & EXPORT LOGS: The calculated variants are integrated into the original log as a new column with variant numbers and exported as both a .xes as well as a .csv file together with a .csv file containing the calculations and the properties as a .txt file.

The exported log can be used for further calculations in another program (.xes and .csv). The calculation .csv file can be used to gain more insights about the calculations. The properties are exported as a .txt file.

### Property Definition (Pre-Processing Functions)
Whenever the program prompts you to define properties, you are able to define various properties depending on the type of attribute (case/event) or type of data (categorical/numerical). 
Based on these properties, the program first creates a new log, a so-called instance log, in which each row refers to a case, and every column is the summarized value based on the properties defined. 
The instance log is later used by the program to create the variants.

**The functions implemented for each attribute and data type are as follows:**

#### A. Attribute type
**Case attributes:** Represent one value per case. These values are used in the instance log. Ignores empty cells.

**Event attributes:** Must first be summarized into a value that represents the complete instance:
- _categorical data:_ combines the numbers into a string (e.g., "A, B" => "AB").
- _numerical data (sum):_ calculates the sum (e.g., "1, 2, 3" => "6").
- _numerical data (median):_ calculates the median (e.g., "1, 2, 3" => 2).
- _numerical data (mean):_ calculates the mean (e.g., "1, 2, 3" => 2).

#### B. Data type

**Categorical data** (e.g., A, B):
- _categorical:_ partitions the log based on different nominal categories (e.g., A, B => two possible partitions).

**Numerical data** (e.g., 1, 2):
- _categorical:_ partitions the log based on different nominal categories (e.g., 1, 2 => two possible partitions).
- _threshold:_ partitions the log based on a threshold (e.g., "100" => two possible partitions, partition 1 < 100 ≤ partition 2).

The properties are limited to the functions above. However, there is a possibility of extending the program with further functions. This can be done in `"ve_methods/ve_propertydefinition.py"`. 
  
---
## TROUBLESHOOTING
**(1) Import problem/Directory problem:**
The program was only tested in MacOS. On other OS, the program might have trouble finding the folders in the directories of your computer. 
Please consider adapting the import and export functions in "/ve_methods/ve_logprocessing.py."

**(2) Log transformation problem/Property definition problem:**
The program might not be able to map all data types properly. The reason for this might be two-fold:
1. First, the program is limited to case and event attributes, which are either categorical (str, int, float) or numerical (int, float). Attributes containing any other data types, such as DateTime, Objects, or similar, may cause problems.
2. Second, the program may not handle logs with attributes of mixed data types (e.g., str + int), or case attributes with no value (all cells for a case are empty). 
   
In these cases, please consider pre-processing the log, e.g., using Disco, PM4Py, or ProM. 
