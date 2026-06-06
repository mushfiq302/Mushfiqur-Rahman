import math

def calculate_current(kva, voltage):
    return (kva * 1000) / (math.sqrt(3) * voltage)

def calculate_core_area(kva):
    return 1.152 * math.sqrt(kva)

def calculate_tpv(core_area, frequency):
    B = 1.2
    return 1 / (4.44 * frequency * B * (core_area / 10000))