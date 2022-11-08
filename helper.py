import ROOT


def isgoodlepton(tree, i):
    """
    If the lepton is a muon (pdg id = +/-13), apply basic quality checks to reject fake/non prompt muons.
    """

    if abs(tree.__lPdgId[i]) == 13 and not tree.__lPassTightID[i]:
        return False
    return True


def invariantmass(tree, i, j, k, l):
    """
    Computes the invariant mass of four leptons labelled i, j, k, l
    """
    l1, l2, l3, l4 = ROOT.TLorentzVector(), ROOT.TLorentzVector(), ROOT.TLorentzVector(), ROOT.TLorentzVector()
    l1.SetPtEtaPhiM(tree._lPt[i], tree._lEta[i], tree._lPhi[i], 0.)
    l2.SetPtEtaPhiM(tree._lPt[j], tree._lEta[j], tree._lPhi[j], 0.)
    l3.SetPtEtaPhiM(tree._lPt[k], tree._lEta[k], tree._lPhi[k], 0.)
    l4.SetPtEtaPhiM(tree._lPt[l], tree._lEta[l], tree._lPhi[l], 0.)

    mass = (l1 + l2 + l3 + l4).Mag()
    return mass


def savehisto(outputfile, histo, histoname):
    """
    Draw histo
    """
    c = ROOT.TCanvas("c_" + histoname, "", 600, 600)
    histo.Draw()
    c.SaveAs("c_"+histoname+".png")
    outputfile.cd()
    c.Write()
    