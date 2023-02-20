import ROOT
# to be used to avoid display intermediate plotting results
# ROOT.gROOT.SetBatch(ROOT.kTRUE)


def isgoodlepton(tree, i):
    """
    If the lepton is a muon (pdg id = +/-13), apply basic quality checks to reject fake/non prompt muons.
    """

    if abs(tree.__lPdgId[i]) == 13 and not tree.__lPassTightID[i]:
        return False
    return True


def invariantmass4l(tree, i, j, k, l):
    """
    Computes the invariant mass of four leptons labelled i, j, k, l
    """
    mass = 0
    return mass


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
    if not logy:
        extraname += "_nolog"
    c.SaveAs("pdfs/"+histoname+extraname+"."+extension)
    outputfile.cd()
    c.Write()
    c.Close()
