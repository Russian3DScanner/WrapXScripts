import wrap
import sys,os

sys.path.append(os.getcwd())
import BatchWizard_ControlPoints
reload(BatchWizard_ControlPoints)

tasks = BatchWizard_ControlPoints.parse_config()

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

    print "Rigid alignment..."
    basemeshAlignPoints = wrap.loadPoints(task['basemeshAlignPointsFileName'])
    scanAlignPoints = wrap.loadPoints(task['scanAlignPointsFileName'])
    transformMatrix = wrap.rigidAlignment(basemesh, basemeshAlignPoints, scan, scanAlignPoints)
    basemesh.transform(transformMatrix)
    wrap.fitToView()
    print "OK"

    print "Non-rigid registration..."
    basemeshWrapPoints = wrap.loadPoints(task['basemeshWrapPointsFileName'])
    scanWrapPoints = wrap.loadPoints(task['scanWrapPointsFileName'])
    wrapped = wrap.nonRigidRegistration(basemesh,scan,basemeshWrapPoints,scanWrapPoints)
    basemesh.hide()
    print "OK"

    print "Saving results..."
    wrapped.save(task['resultFileName'])
    print "Wrapped result saved to %s" % task['resultFileName']

    if scan.texture:
        wrapped.texture = wrap.transferTexture(scan, scan.texture, wrapped)
        wrapped.texture.save(task['resultTextureFileName'])
        print "Wrapped result saved to %s" % task['resultFileName']

    print
