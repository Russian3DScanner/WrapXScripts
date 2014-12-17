import wrap
import sys,os
import shutil

# Set directory which will store configs and results
outputDirectory = "ManyScansOneBasemesh"

# Do not touch lines below
scansDirectory = os.path.join(outputDirectory,"Scans+Textures")
basemeshesDirectory = os.path.join(outputDirectory,"Basemeshes")
resultsDirectory = os.path.join(outputDirectory,"Results")

for directory in [scansDirectory,basemeshesDirectory,resultsDirectory]:
    if not os.path.exists(directory):
        print "Creating directory '%s'" % directory
        os.makedirs(directory)


print "Select scans..."
scanFileNames = wrap.openFilesDialog("Select scans",filter="Files (*.obj)")
if not scanFileNames:
    raise ValueError("Scan filename list cannot be empty")

for scanFileName in scanFileNames:
    print "\t", scanFileName

print "Select basemesh..."
basemeshFileName = wrap.openFileDialog("Select basemesh",filter="Files (*.obj)")
if not basemeshFileName:
    raise ValueError("Basemesh filename cannot be empty")

print "\t", basemeshFileName

# Generating config
pairs = []
for scanFileName in scanFileNames:
    pairs.append("%s\t%s" % (scanFileName, basemeshFileName))

configFileName = os.path.join(outputDirectory,"Scans_Basemeshes.txt")
with open(configFileName,"wb") as file:
    file.write(os.linesep.join(pairs))

print "Config written to '%s'" % os.path.abspath(configFileName)

# Generating args to skip stages if thy set to False
sys.path.append(os.getcwd())
import ParseConfig; reload(ParseConfig)
tasks = ParseConfig.parseConfig(configFileName)

argsTemplate = open(tasks[0]['defaultArgsFileName'],"rb").read()
for task in tasks:
    with open(task['customArgsFileName'],"wb") as file:
        file.write(argsTemplate)
    #print task['argsFileName']

print
print "Please run 'SetContolPoints.py' and select them"
print


