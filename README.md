# Higgs to 4 lepton analysis with CMS Run 2 data

## Setup 
```
git clone https://github.com/iihe-ulb-students/CMSHiggs4Leptons
cd CMSHiggs4Leptons
```
You will need to download the file containing the data and the simulation MC (ask for their location).

The code is located in `example.ipynb`. You can either run it as a jupiter notebook or convert it into a more traditional python script.
A short example on how to access the data and the relevant variables is already provided.

## Goals
Study the 4 lepton final states, in the context of the H->ZZ->4l analysis. The data was collected by the CMS experiment from 2016 until 2018 (known as Run2). A light skimming is pre-applied to significanly reduce the input size.


## Instructions:
- Start analyzing the data.
  - Hint: When analyzing the simulation, don't use the whole samples for testing your code (it's quite large!).
- Choose a final state/channel (4m, 4e, 2e2m):
  - Joint task: You can compare your results with the inclusive channel (4l) and the other final states.
- Make a histogram of the number of reconstructed leptons (muons, electrons) in each event. How many events have (0, 1, 2, 3, 4) muons? And what about electrons?
  - Discussion: how can we select interesting events?
  - Hint: Split per relevant signature
- For events with >=4 leptons, compute the invariant mass of the first four leptons and fill a histogram with 500 bins ranging from 0 to 500 GeV.
  - Hint: To compute the invariant mass, you will first need to find the E, px, py, pz component of each lepton. The lepton pt, eta and phi can be used to retrieve those, see: https://en.wikipedia.org/wiki/Pseudorapidity. (Note that we are working in the ultrarelativistic limit and therefore one can assume E=|p| for leptons.)
  - What are the various peaks observed?
- Compute the invariant mass for each pair of leptons.
  - How does the picture change depending on the lepton flavour?
  - What are the various peaks observed?
  - Hint: Zoom in the low mass region. What do you observe?
- What are the lepton properties? Can we improve the "purity" of 4l mass?
  - Hints: Consider lepton and boson properties (eg. mass, kinematics, angles, ...)
- What are the Z boson properties? Can we improve the "purity" of 4l mass?
- Calculate number of events per mass region (To be discussed):
  - What's the selection efficiency in simulation?
  - Joint task: How does this compare to the other channels?
- Measure the production cross-section for a given final state:
  - What are the assumpions you have to make?
  - What is the uncertanties?
  - Joint task: How does this compare to the other channels?

​
### General recommandations:
- Test your code on a small number of events (eg. 5-10k). Once you think the code works as expected, run it with full statistics.