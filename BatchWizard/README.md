# WrapX Batch Wizard

This set of scripts automates batch wrapping so use can do it without writing scripts by yourself. All you need is place scans and basemeshes in two directories and write text file with pairs - which basemesh wrap to which scan. 

Batch processing divided into two steps - setting control points and doing wrapping:

1. In the first step wizard will walk you through all of selected pairs scan-basemesh and ask how to align them to each other. Then it will ask you to provide hints (corresponding points) for wrapping algorithm. Then it saves your input. 
2. In the second step you just run wrappiing and it does all automatically. After wrapping you can quicky examine results and correct them by running step 1 again (it will remember all you done before, so you change just what you want to change). Rerun step 2, see results, get happy.

## How to use

You need to create some directory layout and set up config file. Let's look at the example (from SampleConfig directory). Place scans and textures with the same names in **Scans+Textures** directory:

* Scans+Textures\
  * FaceScan_Ten24.obj
  * FaceScan_Ten24.jpg
  * TorsoScan.obj

You see there are two .obj-files and one texture. It's OK, TorsoScan just doesn't have texture. Textures can be of extension jpg or png. Then place basemeshes (what wrap to scans) to **Basemeshes** directory:

* Basemeshes\
  * HeadPolygroups_MakeHuman.obj
  * TorsoTemplate_NickZ.obj

Final step - place here config file like this:

* Scans_Basemeshes.txt

It will consist of pairs scan - basemesh:

```
FaceScan_Ten24.obj  HeadPolygroups_MakeHuman.obj

# this is comment line. Place # in the start and line will be ignored
TorsoScan.obj       TorsoTemplate_NickZ.obj  

```

One basemesh can be used with any number of scans. After setting directory layout run scripts.


## Scripts

* SetControlPoints.py - Start with this. It is step 1.
* DoWrapping.py - Step 2. It will create Results directory and fill it.
* LineUp.py - Line up scans and basemeshes (if run after step 1) and results (after step 2). All objects will be scaled in viewport to have the same width.
* ParseConfig.py - You don't need to run it manually. All scripts above use it while the start.
