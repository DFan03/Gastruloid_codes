
# Gastruloid Result Analysis



This package works with 2-level directory of Gastruloid pictures in czi format. The sub-directory name should indicate the condition and cell line, in the format of "Cell_line + Treatment(time)". naming of czi files inside each sub-directory is not important since they will be overrided by the program.

1.GastrulScan.ijm
This ijm files runs as a fiji script, choose the master directory of images as your input directory.

This program is designed to iterate among all sub-directories, when a mistake is made during the process, stop the program, delete the corresponding sub-directory in the output folder, and run the program again. The program will automatically skip all the directories that has been completed.

2.ResultsBatch.py

This python program is made to collect all the results and visualize them, to run this program, first install the requirements.txt to your local environment.
Put this python file into your master output directory made from GastrulScan.ijm. before use.

For mac users:
1. open Terminal
2. cd path/to/requirements folder
3. pip install -r requirements.txt

Read the program and function discriptions before use, examples are included in the program. Remove the example when you run your own analysis.
