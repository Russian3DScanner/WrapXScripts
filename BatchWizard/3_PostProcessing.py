import wrap
import sys,os

sys.path.append(os.getcwd())
import ParseConfig; reload(ParseConfig)

print "Select config file"
configFile = wrap.openFileDialog("Select config file",filter="Text Files (*.txt)")
print "Config file is '%s'" %  configFile

tasks = ParseConfig.parseConfig(configFile, "DefaultSettings_3_PostProcessing.txt")

for taskNum, task in enumerate(tasks):

    if 'wrapped' in locals(): del wrapped
    if 'scan' in locals(): del scan

    print "Task %d of %d" % (taskNum + 1, len(tasks))
    print "Loading scan '%s'..." % task['scanFileName']
    scan = wrap.Geom(task['scanFileName'], fitToView = False)
    scan.wireframe = False
    scaleFactor = 100.0 / scan.boundingBoxSize[0]
    scan.scale(scaleFactor)
    wrap.fitToView()
    print "OK"

    if 'textureFileName' in task:
        print "Loading texture '%s'" % task['textureFileName']
        scan.texture = wrap.Image(task['textureFileName'])
        print "OK"
    else:
        print "No texture found"

    print "Loading wrapped basemesh '%s'..." % task['wrappedResultFileName']
    wrapped = wrap.Geom(task['wrappedResultFileName'], scaleFactor = scaleFactor, fitToView = False)
    print "OK"

    if task['useMethods']['subdivide']:
        print "Subdivision..."
        wrapped = wrap.subdivide(wrapped, **task['methodsSettings']['subdivide'])
        print "OK"
    else:
        print 'Skipping subdivide'

    if task['useMethods']['projectMesh']:
        print "Extracting details..."
        wrapped = wrap.projectMesh(wrapped, scan, **task['methodsSettings']['projectMesh'])
        print "OK"
    else:
        print 'Skipping projectMesh'

    if not os.path.exists(os.path.dirname(task['postprocResultFileName'])):
        try: os.mkdir(os.path.dirname(task['postprocResultFileName']))
        except: pass

    print "Saving result..."
    wrapped.save(task['postprocResultFileName'], scaleFactor = 1.0/scaleFactor)
    print "Result saved to '%s'" % task['postprocResultFileName']

    if scan.texture and task['useMethods']['transferTexture']:
        print "Saving result texture..."
        wrapped.texture = wrap.transferTexture(scan, scan.texture, wrapped)
        wrapped.texture.extrapolate()
        wrapped.texture.save(task['postprocResultTextureFileName'])
        print "Result texture saved to '%s'" % task['postprocResultTextureFileName']
    else:
        print "Skipping texture transfer"

    print

print
print "Post processing done, please use 'ShowResults_3_PostProcessing.py' to see results"
print

