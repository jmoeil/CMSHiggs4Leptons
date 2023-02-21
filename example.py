# %%
import os,sys, math, ROOT
from array import array
import numpy as np
# %jsroot on

#Importing a helper file where some functions are defined
from helper import *

#Input file
inputfile = ROOT.TFile("events4leptonsCMS_FullRun2.root","READ")

#Output file
outputfile = ROOT.TFile("output.root","RECREATE")

#Accessing the "TTree" from root that contains the data (one entry per event)
tree = inputfile.Get("tree")

nentries = tree.GetEntries()
print("Number of entries: ", nentries)

# %%
#Example of histograms 
#The arguments are the following: 
#"name", "title;x axis title;yaxis title", nb of bins, min value, max value
hist_npv = ROOT.TH1F("hist_NPV", "NPV;Number of reconstructed vertices;Events", 100, 0, 100)
hist_massfourleptons = ROOT.TH1F("hist_massfourleptons",";Four Lepton Invariant Mass;Events", 5000, 0, 500)

# %%
#Loop over entries
for i in range(0, nentries):
    #Load entry number i
    tree.GetEntry(i)
    #Every 1000th entry, print some info
    if i%1000==0: print("Event number",i,"\nNb of reconstructed vertices: ",tree._n_PV)
    #Fill the number of reconstructed vertices in a histogram
    hist_npv.Fill(tree._n_PV)
    for lep in range(0,len(tree._lPt)):
    #Every 1000th entry, print some info about the leptons in the event
        if i%1000==0: 
            print("Lepton number",lep,
                "pt:", '%.3f'%tree._lPt[lep],",", 
                "eta:", '%.3f'%tree._lEta[lep],",", 
                "phi:", '%.3f'%tree._lPhi[lep],",", 
                "pdgid:", tree._lpdgId[lep]) #pdgid: e-=11, e+=-11, mu-=13, mu+=-13
      
    #Here you should do several loops and compute the invariant mass of the four leptons
    #The following 
    mass = invariantmass4l(tree, 0, 1, 2, 3)
    hist_massfourleptons.Fill(mass)

# %%
#Draw the histogram and the canvas
c = ROOT.TCanvas("canvas","c_NPV",600,600)
hist_npv.Draw()
c.Draw()
savehisto(outputfile, hist_massfourleptons, "hist_MassFourLeptons")


