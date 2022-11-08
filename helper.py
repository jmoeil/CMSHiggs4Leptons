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
    mass = 0
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
    
