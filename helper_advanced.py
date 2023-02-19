import ROOT
# to be used to avoid display intermediate plotting results
ROOT.gROOT.SetBatch(ROOT.kTRUE)


def isgoodlepton(tree, i):
    """
    If the lepton is a muon (pdg id = +/-13), apply basic quality checks to reject fake/non prompt muons.
    """

    if abs(tree.__lPdgId[i]) == 13 and not tree.__lPassTightID[i]:
        return False
    return True


def sum_four_vectors(pt1,pt2,eta1,eta2,phi1,phi2):
    """
    Computes the invariant mass of four leptons labelled i, j, k, l
    """
    return 2*pt1*pt2*(math.cosh(eta1-eta2)-math.cos(phi1-phi2))

def SameFlavOppCharge(ev,i,j):
    return ev["lep"+str(i)+"flavor"]==-1*ev["lep"+str(j)+"flavor"]

def dR(tree, i, j):
    lep1 = ROOT.TLorentzVector()
    lep2 = ROOT.TLorentzVector()
    lep1.SetPtEtaPhiM(tree._lPt[i],tree._lEta[i],tree._lPhi[i],0)
    lep2.SetPtEtaPhiM(tree._lPt[j],tree._lEta[j],tree._lPhi[j],0)
    return lep1.DeltaR(lep2)

def invariantmass2l(tree, i, j):
    lep1 = ROOT.TLorentzVector()
    lep2 = ROOT.TLorentzVector()
    lep1.SetPtEtaPhiM(tree._lPt[i],tree._lEta[i],tree._lPhi[i],0)
    lep2.SetPtEtaPhiM(tree._lPt[j],tree._lEta[j],tree._lPhi[j],0)
    Z = lep1+lep2
    return Z.M()

def invariantmass4l(tree, i, j, k, l):
    """
    Computes the invariant mass of four leptons labelled i, j, k, l
    """
    lep1 = ROOT.TLorentzVector()
    lep2 = ROOT.TLorentzVector()
    lep3 = ROOT.TLorentzVector()
    lep4 = ROOT.TLorentzVector()
    lep1.SetPtEtaPhiM(tree._lPt[i],tree._lEta[i],tree._lPhi[i],0)
    lep2.SetPtEtaPhiM(tree._lPt[j],tree._lEta[j],tree._lPhi[j],0)
    lep3.SetPtEtaPhiM(tree._lPt[k],tree._lEta[k],tree._lPhi[k],0)
    lep4.SetPtEtaPhiM(tree._lPt[l],tree._lEta[l],tree._lPhi[l],0)
    H = lep1+lep2+lep3+lep4
    return H.M()

def savehisto(outputfile, histo, histoname, logy=False, extraname="", extension="pdf"):
    """
    Draw histo
    """
    c = ROOT.TCanvas(histoname, histoname, 600, 600)
    if "2D" in histoname:
        c.SetLogz(True)
        histo.Draw("colz")
    else:
        histo.Draw()
    c.SetLogy(logy)
    if logy:
        extraname += "_nolog"
    c.SaveAs("pdfs/"+histoname+extraname+"."+extension)
    outputfile.cd()
    c.Write()
    c.Close()
