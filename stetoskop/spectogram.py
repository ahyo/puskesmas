import os
from imaging import generate_spectogram

sources = [
    "/Users/mac/Downloads/ICBHI/102_1b1_Ar_sc_Meditron.wav",
    "/Users/mac/Downloads/ICBHI/104_1b1_Ar_sc_Litt3200.wav",
    "/Users/mac/Downloads/ICBHI/105_1b1_Tc_sc_Meditron.wav",
    "/Users/mac/Downloads/ICBHI/108_1b1_Al_sc_Meditron.wav",
    "/Users/mac/Downloads/ICBHI/111_1b2_Tc_sc_Meditron.wav"
]
# 102	Healthy
# 103	Asthma
# 104	COPD
# 105	URTI
# 108	LRTI
# 111	Bronchiectasis

for source in sources:
    target = os.path.basename(source).replace("wav", "png")
    print(target)
    generate_spectogram(source, target)
