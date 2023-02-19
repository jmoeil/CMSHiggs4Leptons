import os,sys,socket,argparse
import os
import ROOT
import math
from array import array
import numpy as np
from collections import OrderedDict

#Importing a helper file where some functions are defined
from helper import *

debug=False
doIDs=True
doPTs=False
do4Lep=True

selections = OrderedDict([
    ('nocuts', None),
    ('4Lep', 4),
    ("Cat", None),
    ("matching", None),
    ("NoJPsi", None),
    ("RealZ", 10),
    ])

hists = {}

def recreatehistograms():
    for key in list(hists.keys()):
        del hists[key]
    hists['cutflow'] = ROOT.TH1F("cutflow",";cutflow;Events", len(selections), -0.5, len(selections)-0.5)
    for ind,sel in enumerate(selections.keys()):
        hists[str(ind)+'_'+sel+'_nEvents'] = ROOT.TH1F(sel+"nEvents", ";Counting experiment;Events", 1, -0.5, 1.5)
        hists[str(ind)+'_'+sel+'_npv'] = ROOT.TH1F(sel+"hist_NPV", ";Number of reconstructed vertices;Events", 100, 0, 100)
        # hists['dR_Lep'] = ROOT.TH1F("dR_LEP",";#Delta R(lep_i,lep_j);Events", 100, 0, 5)
        for lep in ['Muo','Ele','Lep']:
            hists[str(ind)+'_'+sel+'_n'+lep] = ROOT.TH1F(sel+"n"+lep,";n"+lep+";Events", 11, -0.5, 10.5)
            hists[str(ind)+'_'+sel+'_pt'+lep] = ROOT.TH1F(sel+"pt"+lep,";p_{T}^{"+lep+"};Events", 60, 0, 300)
            # hists[str(ind)+'_'+sel+'_eta'+lep] = ROOT.TH1F(sel+"_eta"+lep,";#eta^{"+lep+"};Events", 60, -3.0, 3.0)
            # hists[str(ind)+'_'+sel+'_phi'+lep] = ROOT.TH1F(sel+"_phi"+lep,";#phi^{"+lep+"};Events", 70, -3.5, 3.5)
            # hists[str(ind)+'_'+sel+'_id'+lep] = ROOT.TH1F(sel+"_id"+lep,";passID;Events", 2, -0.5, 1.5)
            # hists[str(ind)+'_'+sel+'_dR'+lep] = ROOT.TH1F(sel+"dR"+lep,";#Delta R("+lep+",lep_j);Events", 100, 0, 5)
        if ind<4: continue
        hists[str(ind)+'_'+sel+'_massH'] = ROOT.TH1F(sel+"hist_massH",";Four Lepton Invariant Mass;Events", 125, 0, 500)
        hists[str(ind)+'_'+sel+'_massZ1'] = ROOT.TH1F(sel+"_massZ1",";M(Z1);Events", 250, 0, 500)
        hists[str(ind)+'_'+sel+'_massZ2'] = ROOT.TH1F(sel+"_massZ2",";M(Z2);Events", 250, 0, 500)
        hists[str(ind)+'_'+sel+'_massJpsi'] = ROOT.TH1F(sel+"_massjpsi",";M(ll);Events", 200, 0, 10)
        hists[str(ind)+'_'+sel+'_massZ1_vs_Z2'] = ROOT.TH2F(sel+"_massZ1_vs_Z2",";M(Z1);M(Z2);Events", 250, 0, 500, 250, 0, 500)
        # hists[str(ind)+'_'+sel+'_dRZ1'] = ROOT.TH1F(sel+"_dRZ1",";#Delta R(lep_1,lep_2)^{Z_1};Events", 100, 0, 5)
        # hists[str(ind)+'_'+sel+'_dRZ2'] = ROOT.TH1F(sel+"_dRZ2",";#Delta R(lep_1,lep_2)^{Z_2};Events", 100, 0, 5)
        # hists[str(ind)+'_'+sel+'_dRZ1Z2'] = ROOT.TH1F(sel+"_dRZ1Z2",";#Delta R(Z_1,Z_2);Events", 100, 0, 5)

def fillhist(events,selections, sel):
    index = list(selections.keys()).index(sel)
    hname = str(index)+'_'+sel
    hists['cutflow'].SetBinContent(index+1,len(events))
    for ev in events:
        hists[hname+'_nEvents'].Fill(1)
        hists[hname+'_npv'].Fill(ev['npv'])
        for flav in ['Muo','Ele','Lep']:
            nLep = ev["n"+flav]
            hists[hname+'_n'+flav].Fill(nLep)
        for ind in range(0,10):
            if not "lep"+str(ind) in ev: continue
            lep = ev["lep"+str(ind)]
            flavor = ev["lep"+str(ind)+"flavor"]
            for flav in ['Muo','Ele','Lep']:
                if flav=='Muo' and abs(flavor)!=13: continue
                if flav=='Ele' and abs(flavor)!=11: continue
                hists[hname+'_pt'+flav].Fill(lep.Pt())
                # hists[hname+'_eta'+flav].Fill(lep.Eta())
                # hists[hname+'_phi'+flav].Fill(lep.Phi())
                # hists[hname+'_id'+flav].Fill(ev["lep"+str(ind)+"passID"])
        if index<4: continue
        hists[hname+'_massH'].Fill(ev['H'].M())
        hists[hname+'_massZ1'].Fill(ev['Z1'].M())
        hists[hname+'_massZ2'].Fill(ev['Z2'].M())
        hists[hname+'_massJpsi'].Fill(ev['Z1'].M())
        hists[hname+'_massJpsi'].Fill(ev['Z2'].M())
        hists[hname+'_massZ1_vs_Z2'].Fill(ev['Z1'].M(),ev['Z2'].M())
        # hists[hname+'_dRZ1Z2'].Fill(ev['Z1'].DeltaR(ev['Z2']))
        # if 'allPairs' in ev:
        #     indices = ev["allPairs"][0].copy()
        #     hists[hname+'_dRZ1'].Fill(ev["lep"+indices[0]].DeltaR(ev["lep"+indices[1]]))
        #     hists[hname+'_dRZ2'].Fill(ev["lep"+indices[2]].DeltaR(ev["lep"+indices[3]]))

def main(category):
    recreatehistograms()
    # inputfile = ROOT.TFile("events4leptonsCMS_FullRun2.root","READ")
    # tree = inputfile.Get("tree")
    inputfile = ROOT.TFile("Run2data_SkimFourLeptons.root","READ")
    tree = inputfile.Get("ntuplizer/tree")

    outputfile = ROOT.TFile("output.root","RECREATE")
    nentries = tree.GetEntries()
    # print("Number of entries: ", nentries)
    ntot = 0
    n4muo = 0
    n4ele = 0
    n2m2e = 0
    #Loop over entries
    min_pt = 1000
    events = []
    for i in range(0, tree.GetEntries()):
        #Load entry number i
        tree.GetEntry(i)
        event = {}
        event["npv"] = tree._n_PV
        event["nMuo"] = 0
        event["nEle"] = 0
        event["nLep"] = 0
        event["H"] = ROOT.TLorentzVector()
        event["Z1"] = ROOT.TLorentzVector()
        event["Z2"] = ROOT.TLorentzVector()
        for ind in range(0,len(tree._lPt)):
            if doIDs and abs(tree._lpdgId[ind])==13 and not tree._lPassTightID[ind]: continue
            lep = ROOT.TLorentzVector()
            lep.SetPtEtaPhiM(tree._lPt[ind],tree._lEta[ind],tree._lPhi[ind],0)
            event["lep"+str(ind)] = lep
            event["lep"+str(ind)+"flavor"] = tree._lpdgId[ind]
            event["lep"+str(ind)+"passID"] = tree._lPassTightID[ind]
            event["nLep"] += 1
            if (abs(event["lep"+str(ind)+"flavor"])==11): event["nEle"] += 1
            if (abs(event["lep"+str(ind)+"flavor"])==13): event["nMuo"] += 1
        # print(event["nMuo"],event["nEle"],event["nLep"])
        events.append(event)

    fillhist(events, selections, "nocuts")

    # # TO BE IMPROVED TODO
    for ev in events.copy():
        if do4Lep and ev['nLep']!=selections["4Lep"]: events.remove(ev)
    fillhist(events, selections, "4Lep")

    for ev in events.copy():
        if category=="4Muo" and ev['nMuo']!=4: events.remove(ev)
        if category=="4Ele" and ev['nEle']!=4: events.remove(ev)
        if category=="2M2E" and ev['nMuo']!=2 and ev['nEle']!=2: events.remove(ev)
    fillhist(events, selections, "Cat")

    for ev in events:
        ev["allPairs"] = []
        for i in range(0,10):
            if not "lep"+str(i) in ev: continue
            for j in range(0,10):
                if j<=i: continue
                if not "lep"+str(j) in ev: continue
                if not SameFlavOppCharge(ev,i,j):continue
                for k in range(0,10):
                    if not "lep"+str(k) in ev: continue
                    if k==i or k==j: continue
                    for l in range(0,10):
                        if l==i or l==j or l<=k: continue
                        if not "lep"+str(l) in ev: continue
                        if not SameFlavOppCharge(ev,k,l):continue
                        if any([str(i),str(j),str(k),str(l)]==x or [str(k),str(l),str(i),str(j)]== x for x in ev["allPairs"]): continue
                        ev["allPairs"].append([str(i),str(j),str(k),str(l)])

    for ev in events.copy():
        if len(ev["allPairs"])==0: events.remove(ev)

    fillhist(events, selections, "matching")

    for ev in events.copy():
        for pair in ev["allPairs"].copy():
            ev["Z1"] = ev["lep"+str(pair[0])]+ev["lep"+str(pair[1])]
            ev["Z2"] = ev["lep"+str(pair[2])]+ev["lep"+str(pair[3])]
            if ev["Z1"].M()<4 or ev["Z2"].M()<4 or ev['Z1'].DeltaR(ev['Z2'])<0.4: ev["allPairs"].remove(pair)
        if len(ev["allPairs"])==0: events.remove(ev)

    for ev in events:
        indices = ev["allPairs"][0].copy()
        ev["H"] = ev["lep"+indices[0]]+ev["lep"+indices[1]]+ev["lep"+indices[2]]+ev["lep"+indices[3]]
        ev["Z1"] = ev["lep"+indices[0]]+ev["lep"+indices[1]]
        ev["Z2"] = ev["lep"+indices[2]]+ev["lep"+indices[3]]
        if ev["Z1"].M() < ev["Z2"].M():
            ev["Z2"] = ev["lep"+indices[0]]+ev["lep"+indices[1]]
            ev["Z1"] = ev["lep"+indices[2]]+ev["lep"+indices[3]]
            ev["allPairs"][0] = [indices[2],indices[3],indices[0],indices[1]]
    fillhist(events, selections, "NoJPsi")


    for ev in events.copy():
        for pair in ev["allPairs"].copy():
            ev["Z1"] = ev["lep"+str(pair[0])]+ev["lep"+str(pair[1])]
            ev["Z2"] = ev["lep"+str(pair[2])]+ev["lep"+str(pair[3])]
            toremove=False
            if ev["Z1"].M()<40 and ev["Z2"].M()<40: toremove=True
            if ev["Z1"].M()<12 or ev["Z2"].M()<12: toremove=True
            if ev["Z1"].M()>120 or ev["Z2"].M()>120: toremove=True
            if toremove: ev["allPairs"].remove(pair)

        if len(ev["allPairs"])==0: events.remove(ev)

    for ev in events:
        # print (ev["allPairs"])
        closestMass = 4
        pair_index = -1
        for index,pair in enumerate(ev["allPairs"]):
            z1 = ev["lep"+pair[0]]+ev["lep"+pair[1]]
            z2 = ev["lep"+pair[2]]+ev["lep"+pair[3]]
            # print(z1.M(),z2.M())
            if abs(z1.M()-91)<abs(closestMass-91):
                closestMass = z1.M()
                pair_index = index
            if abs(z2.M()-91)<abs(closestMass-91):
                closestMass = z2.M()
                pair_index = index
        # print("Chosen", pair_index)
        ev["pair_index"] = int(pair_index)
        indices = ev["allPairs"][ev["pair_index"]].copy()
        ev["H"] = ev["lep"+indices[0]]+ev["lep"+indices[1]]+ev["lep"+indices[2]]+ev["lep"+indices[3]]
        ev["Z1"] = ev["lep"+indices[0]]+ev["lep"+indices[1]]
        ev["Z2"] = ev["lep"+indices[2]]+ev["lep"+indices[3]]
        if ev["Z1"].M() < ev["Z2"].M():
            ev["Z2"] = ev["lep"+indices[0]]+ev["lep"+indices[1]]
            ev["Z1"] = ev["lep"+indices[2]]+ev["lep"+indices[3]]
            ev["allPairs"][ev["pair_index"]] = [indices[2],indices[3],indices[0],indices[1]]
    fillhist(events, selections, "RealZ")


    eff_Z = 0
    eff_H = 0
    eff_OS = 0
    for ev in events:
        if ev["H"].M()>80  and ev["H"].M()<100: eff_Z+=1
        if ev["H"].M()>120 and ev["H"].M()<130: eff_H+=1
        if ev["H"].M()>200 and ev["H"].M()<501: eff_OS+=1
        indices = ev["allPairs"][ev["pair_index"]].copy()
    print ("Efficiency Z ", category, eff_Z, eff_H, eff_OS, len(events))

    hists['cutflow_norm'] = hists['cutflow'].Clone('cutflow_norm')
    for i in range(len(selections), 0, -1):
        val = hists['cutflow_norm'].GetBinContent(i) if i>1 else 1
        norm = hists['cutflow_norm'].GetBinContent(i-1 if i>2 else 2)
        hists['cutflow_norm'].SetBinContent(i,val/norm)
    for name,hist in hists.items():
        logy= False if any([x in name for x in ['mass','pt','cutflow']]) else True
        savehisto(outputfile, hist, name, logy=logy, extraname='_'+category)
    inputfile.Close()
    outputfile.Close()


if __name__:
    main(category = "4Lep")
    main(category = "4Muo")
    main(category = "4Ele")
    main(category = "2M2E")
