import ROOT
import numpy as np

# to be used to avoid display intermediate plotting results
# ROOT.gROOT.SetBatch(ROOT.kTRUE)


def isgoodlepton(tree, i):
    """
    If the lepton is a muon (pdg id = +/-13), apply basic quality checks to reject fake/non prompt muons.
    """

    if abs(tree.__lPdgId[i]) == 13 and not tree.__lPassTightID[i]:
        return False
    return True


def invariantmass4l(tree, e, p, mu_minus, mu_plus):
    """
    Computes the invariant mass of four leptons labelled e, p, mu_minus, mu_plus
    """
    
    pt = np.array([tree._lPt[e],tree._lPt[p],tree._lPt[mu_minus],tree._lPt[mu_plus]])
    phi = np.array([tree._lPhi[e],tree._lPhi[p],tree._lPhi[mu_minus],tree._lPhi[mu_plus]])
    eta = np.array([tree._lEta[e],tree._lEta[p],tree._lEta[mu_minus],tree._lEta[mu_plus]])

    px = pt*np.cos(phi)
    py = pt*np.sin(phi)
    pz = pt*np.sinh(eta)
    
    p_e = np.array([px[0],py[0],pz[0]])
    p_p = np.array([px[1],py[1],pz[1]])
    p_mu_minus = np.array([px[2],py[2],pz[2]])
    p_mu_plus = np.array([px[3],py[3],pz[3]])

    E_e = np.linalg.norm(p_e)
    E_p = np.linalg.norm(p_p)
    E_mu_minus = np.linalg.norm(p_mu_minus)
    E_mu_plus = np.linalg.norm(p_mu_plus)

    E = E_e+E_p+E_mu_minus+E_mu_plus

    mass = np.sqrt(E**2 - np.linalg.norm(p_e+p_p+p_mu_minus+p_mu_plus)**2)
    
    return mass

def invariantmass2l(tree,lep1,lep2):
    '''
    Computes the invariant mass of 2 laptons labelled lep1,lep2
    '''

    pt = np.array([tree._lPt[lep1],tree._lPt[lep2]])
    phi = np.array([tree._lPhi[lep1],tree._lPhi[lep2]])
    eta = np.array([tree._lEta[lep1],tree._lEta[lep2]])

    px = pt*np.cos(phi)
    py = pt*np.sin(phi)
    pz = pt*np.sinh(eta)

    p_1 = np.array([px[0],py[0],pz[0]])
    p_2 = np.array([px[1],py[1],pz[1]])

    E_1 = np.linalg.norm(p_1)
    E_2 = np.linalg.norm(p_2)

    E = E_1+E_2

    mass = np.sqrt(E**2-np.linalg.norm(p_1+p_2)**2)

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
