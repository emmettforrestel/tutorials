#include "FCCAnalyses/MCParticle.h"

ROOT::VecOps::RVec<float> get_invariant_mass(const ROOT::VecOps::RVec<edm4hep::MCParticleData>& particles) {
  ROOT::VecOps::RVec<float> result;

  TLorentzVector max_energy_muon, max_energy_antimuon;
  float max_energy_mu = 0, max_energy_amu = 0;

  for (auto &p : particles) {
    TLorentzVector tlv;
    tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
    float energy = tlv.E();
    // Check if it's a muon or anti-muon
      if (p.PDG == 13 && energy > max_energy_mu) {
        max_energy_mu = energy;
        max_energy_muon = tlv;
      } else if (p.PDG == -13 && energy > max_energy_amu) {
        max_energy_amu = energy;
        max_energy_antimuon = tlv;
      }
  }
  // Calculate the invariant mass if both are found
  if (max_energy_mu > 0 && max_energy_amu > 0) {
    TLorentzVector combined = max_energy_muon + max_energy_antimuon;
    result.push_back(combined.M());
  }
  return result;
}