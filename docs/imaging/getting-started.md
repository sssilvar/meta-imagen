# Imaging pipeline (ENIGMA Shape)
This part is a dockerized version of the [ENIGMA Shape Analysys Project](http://enigma.ini.usc.edu/ongoing/enigma-shape-analysis/ "ENIGMA Shape Site"). You can go to the documentiation at the project's site if you need more information.

To make this structural analysis work is necessary to follo these instructions:

## 1. Have the preprocessed data
This software works over a Freesurfer preprocessed folder (after performing a `recon-all` process). After you process your MRI data, you will have a folder that contains all the results in a structure like this:

![alt text](img/recon-all-dataset.png "Dataset folder after recon-all")

As you may see, each folder corresponds to one subject's image processed. Inside each folder (subject), you will find a structure like this:
![alt text](img/recon-all-subject.png "Inside a subject's folder after recon-all")