from chemwave import ChemWave

wave = ChemWave()

print("🌊 Testing get_compound('caffeine')...")
caffeine_data = wave.get_compound("caffeine")
print(caffeine_data)

print("\n🌊 Testing custom property lookup for 'aspirin'...")
aspirin_data = wave.get_compound("aspirin", properties=["MolecularFormula", "MolecularWeight"])
print(aspirin_data)