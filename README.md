# Higgs to 4 lepton analysis with CMS Run 2 data

## Setup 
```
git clone https://github.com/iihe-ulb-students/CMSHiggs4Leptons
cd CMSHiggs4Leptons
```
You will need to download the file containing the data that is named `events4leptonsCMS_FullRun2.root` (ask for its location)

The code is located in `example.ipynb`


## Instructions:
- Make a histogram of the number of reconstructed leptons (muons, electrons) in each event. How many have 0, 1, 2, 3, 4 muons? 
- For events with >=4 leptons, compute the invariant mass of the first four leptons and fill a histogram with 500 bins ranging from 0 to 500 GeV. *=>Tip: To compute the invariant mass, you will first need to find the E, px, py, pz component of each lepton. The lepton pt, eta and phi can be used to retrieve those, see: https://en.wikipedia.org/wiki/Pseudorapidity Note that we are working in the ultrarelativistic limit and therefore one can assume E=|p| for leptons.*
  - What are the various peaks observed? 
​
