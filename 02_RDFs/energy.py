import ROOT

ROOT.gInterpreter.ProcessLine("""
#include "energy.h"
"""
)

# Open the file
f = ROOT.TFile.Open("/ceph/submit/data/group/cms/store/fccee/samples/winter2023/CLD_FullSim/wzp6_ee_mumuH_ecm240/mumuH_rec_16610_191.root")

# Get the tree
tree = f.Get("events")

# Create the RDF
df = ROOT.RDataFrame(tree)

# Define the energy of the particles, and save if above 10 GeV
df = df.Define("Invariant_Mass", "get_invariant_mass(MCParticles)")

# Fill the histogram with the calculated energies
# We defined 100 bins between 0 and 1000 GeV
h = df.Histo1D(("MCParticles_InvariantMass", "", *(100, 0, 120)), "Invariant_Mass")

# Draw the histogram
c = ROOT.TCanvas()
h.Draw()
c.Draw()

# save the histogram
c.SaveAs("mass.png")