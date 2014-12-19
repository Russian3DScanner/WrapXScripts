import wrap
import sys,os

sys.path.append(os.getcwd())
import ParseConfig; reload(ParseConfig)

print "Select config file"
configFile = wrap.openFileDialog("Select config file",filter="Text Files (*.txt)")
print "Config file is '%s'" %  configFile

tasks = ParseConfig.parseConfig(configFile)

tasksCount = len(tasks)
for taskNum, task in enumerate(tasks):

    print "Task %d of %d" % (taskNum + 1, tasksCount)
    print "Loading scan '%s'..." % task['scanFileName']
    scan = wrap.Geom(task['scanFileName'])
    scan.wireframe = False
    print "OK"


    if 'textureFileName' in task:
        print "Loading texture '%s'" % task['textureFileName']
        scan.texture = wrap.Image(task['textureFileName'])
        print "OK"
    else:
        print "No texture found"

    print "Loading wrapped basemesh '%s'..." % task['wrappedResultFileName']
    wrapped = wrap.Geom(task['wrappedResultFileName'])
    wrapped.fitToView()
    print "OK"

    if task['useMethods']['subdivide']:
        print "Subdivision..."
        wrapped = wrap.subdivide(wrapped, **task['methodsArgs']['subdivide'])
        print "OK"
    else:
        print 'Skipping subdivide'

    if task['useMethods']['projectMesh']:
        print "Extracting details..."
        wrapped = wrap.projectMesh(wrapped, scan, **task['methodsArgs']['projectMesh'])
        print "OK"
    else:
        print 'Skipping projectMesh'

    print "Saving results..."
    if not os.path.exists(os.path.dirname(task['postprocResultFileName'])):
        try: os.mkdir(os.path.dirname(task['postprocResultFileName']))
        except: pass

    wrapped.save(task['postprocResultFileName'])
    print "Postprocessed result saved to '%s'" % task['postprocResultFileName']

    if scan.texture and task['useMethods']['transferTexture']:
        wrapped.texture = wrap.transferTexture(scan, scan.texture, wrapped)
        wrapped.texture.extrapolate()
        wrapped.texture.save(task['postprocResultTextureFileName'])
        print "Postprocessed result texture saved to '%s'" % task['postprocResultTextureFileName']
    else:
        print "Skipping texture transfer"

    print

print
print "Post processing done, please use 'ShowResults.py' to see them"
print

