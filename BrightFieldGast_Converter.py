
"""
Created on Mon Feb 19 18:49:27 2024

@author: donglifan
"""

from ij import IJ
from ij.io import FileSaver
import os
from ij.plugin import ZProjector

'''
This script works with 2-level directory, brightfield images without autoscale.

How it works:
1. copy the home directory "name + converted _to_jpg" to create a empty output folder
2. copy the name of each sub-directory, create empty folder in the output folder
3. process files in each sub-directory, each image are flattend, transfer to grayscale.
4. Create jpg file in the output directory, with subdirectory name + image counter

e.g.
	Master_Folder
		Sub_Folder
			snap_10.czi
			snap_11.czi

Output:

	Master_Folder_converted_to_jpg
		Sub_Folder
			Sub_Folder1.jpg
			Sub_Folder2.jpg


In such way you can create a folder for each different condition, and ignore naming of 
snapshots, save them directly into corresponding folder and run this script will assign 
the proper file name.

'''

def process_directory(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        image_counter = 1  # Initialize image counter for each directory
        print("Processing directory:", root)# Debugging output
        current_output_dir = os.path.join(output_dir, os.path.relpath(root, input_dir))
        if not os.path.exists(current_output_dir):
            os.makedirs(current_output_dir)
        for name in files:
        	#change to your file format here
            if name.lower().endswith(".czi"):
                file_path = os.path.join(root, name)
                print("Found .czi file:", file_path)  # Debugging output
                # Open the image using Bio-Formats
                imp = IJ.openImage(file_path)
                zp = ZProjector(imp)
                zp.setMethod(ZProjector.AVG_METHOD)  
                # Set the projection method to maximum intensity
                zp.doProjection()  # Perform the projection, flattened image
                imp = zp.getProjection()
                if imp is None:
                    print("Could not open image from file:", file_path)
                     
                    continue
                else:
                    print("Image opened successfully:", file_path)  
                    #Debugging
                    IJ.run(imp, "8-bit", "")
                # Ensure the image is read as grayscale
                
                # Construct the output filename
                output_file_name = os.path.join(current_output_dir,"{}_{}.jpg".format(os.path.basename(root),image_counter))
                print("Saving jpg as:", output_file_name) # Debugging
                
                # Save the image as jpg (somehow PNG doesn't work)
                fs = FileSaver(imp)
                if fs.saveAsPng(output_file_name):
                    print("Image saved successfully:", output_file_name)
                    #Debugging
                else:
                    print("Failed to save image:", output_file_name)
                image_counter += 1



input_directory = IJ.getDirectory("Choose the Home Directory")
if input_directory is None:
    print("No directory was selected.")
else:
    home_dir_name = os.path.basename(os.path.normpath(input_directory))
    output_directory = os.path.join(input_directory, home_dir_name + "_Converted_to_jpg")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    print("Output directory:", output_directory)  # Debugging
    process_directory(input_directory, output_directory)
    print("Processing completed.")
