import wrap
import sys,os

sys.path.append(os.getcwd())
import ParseConfig; reload(ParseConfig)


print "Select config file"
configFile = wrap.openFileDialog("Select config file",filter="Text Files (*.txt)")
print "Config file is %s" %  configFile

tasks = ParseConfig.parseConfig(configFile)

tasksCount = len(tasks)
for taskNum, task in enumerate(tasks):
    print "Task %d of %d" % (taskNum + 1, tasksCount)
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


    print "Select THREE rigid alignment point correspondences between basemesh and scan..."
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
    print "Wrapping point correspondences saved, please run DoWrapping.py"
    print
