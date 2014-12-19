# WrapX Batch Wizard

This set of scripts automates batch wrapping so use can do it without writing scripts by yourself. 

## Quickstart for "many scans - one basemesh" case

* Run *0_GenerateConfig_ManyScansOneBasemesh.py*. It will ask you to provide output directory, then list of scans and basemesh. Then it will create config file named *Config_Scans_Basemeshes.txt* in output directory.

* Run *1_SetControlPoints.py*. Select previously created config file. Then it will walk you through all pairs scan-basemesh and ask for select pairs of corresponding points between scan and basemesh.

* Run *2_Wrapping.py*. Select config file and relax. All wrapping will be done automatically. After done you can see the results by running *ShowResults_2_Wrapping.py*

* Run *3_PostProcessing.py*. This step needed if you want to extract details from scan or transfer textures. By default all enabled, you can control what to do by editing file *DefaultSettings_3_PostProcessing.txt*. Finally run *ShowResults_3_PostProcessing.py* to see the results.


## Almost all wrapped OK, how to repeat just specific pairs scan-basemesh?

Open *Config_Scans_Basemeshes.txt* in output directory and comment pairs which not needed. Comments are created by placing "#" in the beginning of line. Then run any step you want again.
