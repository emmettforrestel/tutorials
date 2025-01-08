import ROOT

# Open the file
file = ROOT.TFile("/ceph/submit/data/group/cms/store/fccee/samples/winter2023/CLD_FullSim/wzp6_ee_mumuH_ecm240/mumuH_rec_16610_191.root")

# Get the tree of events
tree = file.Get("events")

# Create a histogram to store the energies
h_mass = ROOT.TH1D("h_mass", "Invariant Mass [GeV]", 100, 0, 120)

# for loop over the first 10 events, and print information about the MC particles
for i in range(1000):
    
    print("Processing event", i)
    tree.GetEntry(i)
    # get the MC particles for this event
    MCParticles = tree.MCParticles
    # Variables to store the most energetic muon and anti-muon
    max_muon = None
    max_antimuon = None
    max_muon_energy = -1
    max_antimuon_energy = -1
   
    for j in range(len(MCParticles)):
        particle = MCParticles[j]
        energy = (particle.momentum.x**2 + particle.momentum.y**2 + particle.momentum.z**2 + particle.mass**2)**0.5
        if particle.PDG == 13 and energy > max_muon_energy:
            max_muon = particle
            max_muon_energy = energy
        elif particle.PDG == -13 and energy > max_antimuon_energy:
            max_antimuon = particle
            max_antimuon_energy = energy
            
    if max_muon and max_antimuon:
        # Create TLorentzVectors for the muon and anti-muon
        muon_vector = ROOT.TLorentzVector()
        antimuon_vector = ROOT.TLorentzVector()

        # Set the 4-momentum for the muon & antimuon
        muon_vector.SetPxPyPzE(max_muon.momentum.x, max_muon.momentum.y, max_muon.momentum.z, max_muon_energy)
        antimuon_vector.SetPxPyPzE(max_antimuon.momentum.x, max_antimuon.momentum.y, max_antimuon.momentum.z,max_antimuon_energy)
        
        invariant_mass = (muon_vector + antimuon_vector).M()
        h_mass.Fill(invariant_mass)

# draw the histogram, this is done using a Canvas
c = ROOT.TCanvas()
c.SetLogy()
h_mass.Draw()

# label the axes
h_mass.GetXaxis().SetTitle("Invariant Mass [GeV]")
h_mass.GetYaxis().SetTitle("Number of particles")

# draw the canvas
c.Draw()

# save the plot to a file
c.SaveAs("mass.png")

# save the histogram to a .root file
file_out = ROOT.TFile("output_mass.root", "RECREATE")
h_mass.Write()
file_out.Close()

print("All done!")