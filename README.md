# holdings-from-isbns
Python scripts and Jupyter Notebook to determine electronic holdings, print holdings, and print copies held on the basis of a list of ISBNs.  This process determines Alma electronic and print holdings for a list of ISBNs. The ISBNs may originate from any source, but the process was designed to produce an Excel spreadsheet report on the basis of a title offer list from a vendor or publisher.

## Process Overview
1. Place the vendor file (or list of ISBNs) in the working directory. If working with a vendor file, create a single-column `.txt` or `.csv` file of ISBNs extracted from the vendor file.
2. Run `alma_sru_sn.py` from the command line. You will need to edit the script to include the SRU base URL of your Alma institution. Provide the name of your ISBN `.txt` or `.csv` file when prompted. The script searches the list of ISBNs in Alma via SRU, gets MMS IDs of records retrieved for each ISBN, and outputs two files: a Python `.pkl` file and a `.csv` file with identical content, containing the MMS IDs retrieved for each ISBN. 
3. When `alma_sru_sn.py` is finished, run `dedup_split_ids.py` from the command line. Provide the name of the `.pkl` file output by `alma_sru_sn.py` as input. This script dedups the list of MMS IDs, and breaks the list into separate lists of whatever length you want; the default is 9,999 IDs (the maximum number of identifiers that can be entered into a filter in an Alma Analytics report).
4. Use the list(s) of found MMS IDs to populate reports in Alma Analytics. You will need at least one electronic holdings report and one physical holdings report. If 10,000 or more MMS IDs were found, you will need multiple reports for each inventory type. Sample reports are available in the Alma Analytics folder`/shared/Community/Reports/Institutions/UMinnesota/Sample reports for ISBN vendor list matching`.
5. Export the Alma Analytics reports as `.csv` files and place them in the working directory.
6. Run the Jupyter Notebook `create_hol_report.ipynb` and follow instructions in the notebook to complete the analysis. Thr Notebook outputs a summary spreadsheet of electronic and print holdings (with calculated number of copies) for the original title list supplied by vendors (or other list of ISBNs). Output is an Excel file with three worksheets: vendor data with indicators for local E and P holdings and copy counts, Alma E inventory data for titles found, and Alma P inventory data for titles found.

## Requirements
Anaconda is recommended, but two requirements files are included:
- `conda_requirements.txt` to create a conda environment (conda create --name <env> --file `conda_requirements.txt`)
- `requirements.txt` to create a pip virtual environment without Anaconda or conda.
