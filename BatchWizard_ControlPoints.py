import wrap
import sys, os

def parse_config():
    directory = '/home/ivan/R3DS/WrapX/Wizard'

    tasks = []
    lines = open(os.path.join(directory,'Scans_Basemeshes.txt'))
    for line in lines:

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

if __name__ == "__main__":

    tasks = parse_config()
    for task in tasks:

        print "Loading scan %s..." % task['scanFileName']
        scan = wrap.Geom(task['scanFileName'])
        scan.wireframe = False
        print "OK"

        if 'textureFileName' in task:
            print "Loading texture %s" % task['textureFileName']
            scan.texture = wrap.Image(task['textureFileName'])
            print "OK"
        else:
            print "No texture found"

        print "Loading basemesh %s..." % task['basemeshFileName']
        basemesh = wrap.Geom(task['basemeshFileName'])
        print "OK"

        # Rigid alignment

        basemeshAlignPoints = []
        if os.path.exists(task['basemeshAlignPointsFileName']):
            basemeshAlignPoints = wrap.loadPoints(task['basemeshAlignPointsFileName'])

        scanAlignPoints = []
        if os.path.exists(task['scanAlignPointsFileName']):
            scanAlignPoints = wrap.loadPoints(task['scanAlignPointsFileName'])


        print "Select THREEE rigid alignment point correspondences between basemesh and scan..."
        (basemeshAlignPoints, scanAlignPoints) = wrap.selectPoints(basemesh, scan, basemeshAlignPoints, scanAlignPoints)
        print "OK"
        # save
        wrap.savePoints(basemeshAlignPoints,task['basemeshAlignPointsFileName'])
        wrap.savePoints(scanAlignPoints,task['scanAlignPointsFileName'])
        print "Rigid alignment point correspondences saved"

        transformMatrix = wrap.rigidAlignment(basemesh, basemeshAlignPoints, scan, scanAlignPoints)
        basemesh.transform(transformMatrix)
        wrap.fitToView()

        # Non-rigid registration
        basemeshWrapPoints = []
        if os.path.exists(task['basemeshWrapPointsFileName']):
            basemeshWrapPoints = wrap.loadPoints(task['basemeshWrapPointsFileName'])

        scanWrapPoints = []
        if os.path.exists(task['scanWrapPointsFileName']):
            scanWrapPoints = wrap.loadPoints(task['scanWrapPointsFileName'])


        print "Select wrapping point correspondences between basemesh and scan..."
        (basemeshWrapPoints, scanWrapPoints) = wrap.selectPoints(basemesh, scan, basemeshWrapPoints, scanWrapPoints)
        print "OK"
        # save
        wrap.savePoints(basemeshWrapPoints,task['basemeshWrapPointsFileName'])
        wrap.savePoints(scanWrapPoints,task['scanWrapPointsFileName'])
        print "Wrapping point correspondences saved"
        print
