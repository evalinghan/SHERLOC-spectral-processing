# SHERLOC Spectral processing

*** These scripts are currently only for portfolio purposes during my job search ***\
*** Relevant data has not been released yet and as such is not uploaded here ***\
*** You can only use this directory to assess the code in question ***

Here you will find two scripts that I have build to process and visualize the Raman spectral grid retrieved from the SHERLOC instrument on the Perseverance rover. 

This directory includes the following python scripts: 

SHERLOC_Downlink_ProcessingAndBaselineRemoval.ipynb

SHERLOCGrid_DashBoard.py
 
## SHERLOC_Downlink_ProcessingAndBaselineRemoval.ipynb

This script retrieves relevant datasets from the huge directory of SHERLOC data. 
It then computes some basic statistics (mean, median, STD) on all of the spectra in the grid. 
A number of baseline removal models are applied. 
A default baseline removal model is then fitted and subtracted (you can change to any preferred model). 
The script then retrieves the relevant grid coordinates from a specified context image of the spectral retrievals. 

It saves all of this information in several processed files: 
Raw spectra with their grid information
Fitted baselines with their grid information
Baseline removed spectra with their grid information
Spectral statistics of raw spectra
Spectral statistics of baselined spectra

## SHERLOCGrid_DashBoard.py

Change the input files to the SHERLOCGrid_DashBoard.py to the raw, fitted baseline, and baseline spectral grids that you have just processed. This script will then display the results in an interactive dashboard that allows you to hover over each grid node and see the spectral information stored within that note. You'll be able to zoom and stretch axes however you like within the dashboard app. 

## Dependencies

For SHERLOC_Downlink_ProcessingAndBaselineRemoval, you need to install: 

pandas - best installed with pip or anaconda

Baseline removal algorithms come from: 

https://github.com/derb12/pybaselines
https://pypi.org/project/pybaselines/

You will need to install using pip: pip install --upgrade pybaselines[full]

All credit for these baseline removal models goes to Donald Erb (github user derp12).

For SHERLOCGrid_DashBoard, you need to install: 

pandas\
plotly dash - best installed with conda-forge\
Pillow - best installed with conda




 
