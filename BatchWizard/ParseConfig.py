import sys, os

def parseConfig(configFileName):

    directory = os.path.dirname(configFileName)

    tasks = []
    lines = open(configFileName).readlines()
    for line in lines:

        line = line.strip()

        if not line:
            continue

	if line.startswith('#'):
            continue

        (scanRelativeFileName, basemeshRelativeFileName) = line.split()

        scanFileName = os.path.join(directory,'Scans+Textures',scanRelativeFileName)
        basemeshFileName = os.path.join(directory,'Basemeshes',basemeshRelativeFileName)
        resultFileName = os.path.join(directory,'Results',scanRelativeFileName)

        if not os.path.exists(scanFileName):
            print "No such file: %s, ignoring" % scanFileName
            continue

        if not os.path.exists(scanFileName):
            print "No such file: %s, ignoring" % basemehsFileName
            continue
        task = {
            'scanFileName': scanFileName,
            'basemeshFileName': basemeshFileName,
            'resultFileName': resultFileName,
        }

        # search textures
        textureExtensions = [".jpg",".png"]
        for extension in textureExtensions:
            textureFileName = os.path.join(directory,'Scans+Textures',os.path.splitext(scanRelativeFileName)[0]+extension)
            resultTextureFileName = os.path.join(directory,'Results',os.path.splitext(scanRelativeFileName)[0]+extension)

            if os.path.exists(textureFileName):
                task['textureFileName'] = textureFileName
                task['resultTextureFileName'] = resultTextureFileName
                break

        # filenames of contol points                            
        task['scanAlignPointsFileName'] = scanFileName + "_alignPoints.txt"
        task['basemeshAlignPointsFileName'] = basemeshFileName + "_alignPoints.txt"

        task['scanWrapPointsFileName'] = scanFileName + "_wrapPoints.txt"
        task['basemeshWrapPointsFileName'] = basemeshFileName + "_wrapPoints.txt"

        tasks.append(task)

    return tasks
