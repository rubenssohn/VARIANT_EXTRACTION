# VARIANT_EXTRACTION
This repository for a variant extraction tool based the paper "Variants of Variants: Context-based Variant Analysis for Process Mining."

## REQUIREMENTS (incl. recommended versions)
* Anaconda (2023.09): https://anaconda.org 
* Python (3.11.6): https://www.python.org
* PM4PY (2.7.8): https://pm4py.fit.fraunhofer.de
* Jupyter lab (3.6.3): https://jupyter.org
* Pandas (2.1.1): https://pandas.pydata.org
* NumPy (1.24.3): https://numpy.org
* Scikit-Learn (1.3.0): https://scikit-learn.org

## HOW TO USE APPLICATION: 
1. Download and place the "VARIANT_EXTRACTION" folder somewhere on your computer
2. Open the terminal on your computer (e.g., "Terminal" on MacOS)
3. In terminal: Navigate to the folder "VARIANT_EXTRACTION/variant_extraction" via the terminal
4. Execute the program: in the comman-line tool ($ python ve_main.py) or in the jupyter notebook "ve_jupyter.ipynb" ($ jupyterlab)

## ABOUT THE MODULES:
* ... -> TODO

## EXTENDING THE MODULES:
* ... -> TODO

## ABOUT IMPORT/EXPORT
* Event logs should be located in the "data/input" folder.
* All saved data are exported to "data/output/."

## PROBLEMSHOOTING
The notebooks were only tested on MacOS and not on any other OS. Unfortunately, this might cause problems.

A common problem is the different structure of the directories, leading to an import-error. 
If the import of logs might cause a problem on your OS, 
please consider adapting the import and export functions in "/ve_methods/ve_logprocessing.py".
