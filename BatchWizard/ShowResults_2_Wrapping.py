import wrap
import sys,os

sys.path.append(os.getcwd())
import ParseConfig; reload(ParseConfig)


print "Select config file"
configFile = wrap.openFileDialog("Select config file",filter="Text Files (*.txt)")
print "Config file is '%s'" %  configFile

tasks = ParseConfig.parseConfig(configFile)

taskNum = 0

while True:

    task = tasks[taskNum]

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

    if os.path.exists(task['wrappedResultFileName']):
        print "Loading wrapped basemesh '%s'..." % task['wrappedResultFileName']
        wrappedResult = wrap.Geom(task['wrappedResultFileName'], scaleFactor = scaleFactor, fitToView = False)
        print "OK"
    else:
        print "!!! Warning: No wrapped result found"

    print        


    title = "scan %d/%d    %s" % (taskNum+1, len(tasks), os.path.basename(task['scanFileName']))
    buttons = ["Stop"]
    if taskNum != (len(tasks)-1):
        buttons.insert(0,"Next ->")
    if taskNum > 0:
        buttons.insert(0,"<- Prev")
    ans = wrap.customDialog(title, buttons)

    if ans == "Stop":
        print "Stopped"
        break
    elif ans == "<- Prev":
        taskNum -= 1
    elif ans == "Next ->":
        taskNum += 1

    del scan
    if 'wrappedResult' in locals(): del wrappedResult



