// Select the master directory and set up the destination directory
masterDir = getDirectory("Choose Master Source Directory ");
outputBaseDir = getDirectory("Choose Base Destination Directory ");

// Extract the name of the master directory to use as the base for the output directory

outputDir = outputBaseDir+"/Converted/"

if (!File.exists(outputBaseDir+"/Converted")){
	File.makeDirectory(outputBaseDir+"/Converted");
}
// Create the output directory if it doesn't exist

// Get the list of sub-folders within the master directory
subFolders = getFileList(masterDir);
for (subFolderIndex = 0; subFolderIndex < subFolders.length; subFolderIndex++) {
    subFolderName = subFolders[subFolderIndex];
    subFolderPath = masterDir + subFolderName + "/";
    
    // Check if the item is a directory
    if (File.isDirectory(subFolderPath)) {
        // Create a corresponding sub-folder in the output directory
        outputSubDir = outputDir + subFolderName + "/";
        if (File.isDirectory(outputSubDir)){
        	continue;
        	}
        File.makeDirectory(outputSubDir);
        
        // Get the list of files within the sub-folder
        list = getFileList(subFolderPath);
        for (i = 0; i < list.length; i++) {
            if (endsWith(list[i], ".czi")) {
            	
                path = subFolderPath + list[i];
                run("Bio-Formats Importer", "open=[" + path  + "]");
                run("Z Project...", "projection=[Average Intensity]");
                selectWindow("AVG_" + list[i]);
                original = getTitle();
                fileName="_"+subFolderName.substring(0,subFolderName.length()-1)+"_"+(i+1);
                rename(fileName);
                run("Grays");
                run("8-bit");
                run("Duplicate...", "title=duplicate" + i);
                selectWindow("duplicate" + i);
                run("Gaussian Blur...", "sigma=3");
                selectWindow("duplicate" + i);
                run("Normalize Local Contrast", "block_radius_x=200 block_radius_y=200 standard_deviations=3 center");
                run("Threshold...", "Otsu dark");
                waitForUser("Adjust the proper threshold");
                run("Convert to Mask");
                run("Invert");
                run("Fill Holes");
                run("Analyze Particles...", "size=10000-Infinity show=Outlines display exclude include add");
                // Check if there are no objects larger than 500
                if (roiManager("count") < (i+1)) {
                	xCenter = 50; // X coordinate of the center
					yCenter = 50; // Y coordinate of the center
					radius = 1; // Smallest radius for a visible circle
										// Make the image active
					setBatchMode(true);
					newImage("TempBlank", "8-bit white", 100, 100, 1);
					
					
					setBatchMode(false);
					
										// Draw a circle ROI
					makeOval(xCenter - radius, yCenter - radius, radius, radius);
					setColor("black");
					fill();
					run("Threshold...", "Otsu dark");
					run("Convert to Mask");
					run("Invert");		
					run("Analyze Particles...", "size=1-Infinity show=Outlines display exclude include add");

                }

                selectWindow(fileName);
                run("Duplicate...", "title=duplicate2");
                run("Scale Bar...", "width=300 height=8 font=28 color=White background=None location=[Lower Right] bold overlay");
                saveAs("TIFF", outputSubDir + fileName);
                selectWindow(fileName);
                roiManager("Select", i);
                run("Flatten");
                run("Scale Bar...", "width=300 height=8 font=28 color=White background=None location=[Lower Right] bold overlay");
                saveAs("Jpeg", outputSubDir + fileName + "_segmented");        
            }
        }
        selectWindow("Results");
        saveAs("Results", outputSubDir + "Results.csv");
        run("Close");
        roiManager("deselect");
        roiManager("Save", outputSubDir + "RoiSet.zip");
        roiManager("reset");
        run("Close All");
    }
}
