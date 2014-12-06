import wrap
import sys,os
import shutil

directory = "ManyScansOneBasemesh"

# Change to False if you don't need some stages
projectMesh = True
subdivide = True
transferTexture = True


scansDirectory = os.path.join(directory,"Scans+Textures")
basemeshesDirectory = os.path.join(directory,"Basemeshes")
resultsDirectory = os.path.join(directory,"Results")

for dirName in [scansDirectory,basemeshesDirectory,resultsDirectory]:
    if not os.path.exists(dirName):
        print "Creating %s" % dirName
        os.makedirs(dirName) 
        
        
print "Select scans..."
scanFileNames = wrap.openFilesDialog("Select scans",filter="Files (*.obj)")
for scanFileName in scanFileNames:
    print "\t", scanFileName

print "Select basemesh..."
basemeshFileName = wrap.openFileDialog("Select basemesh",filter="Files (*.obj)")
print "\t", basemeshFileName

pairs = []
for scanFileName in scanFileNames:
    pairs.append("%s\t%s\r\n" % (scanFileName, basemeshFileName))

configFileName = os.path.join(directory,"Scans_Basemeshes.txt")
with open(configFileName,"w") as file:
    file.write("".join(pairs))
    
print "Config written to %s" % os.path.abspath(configFileName)
print "Please run SetContolPoints.py and select it"





    






