# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton / GlacierEQ — All Rights Reserved
import os
import sys
import time

# Ensure parent directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grid_model import EnergyGridModel, verify_phase_synchronization, shed_load_profile

def test_grid_calculations():
    print("[TEST] Running Grid Impedance & sCO2 thermodynamic cycles...")
    t0 = time.perf_counter()
    
    assert verify_phase_synchronization(1.2, 1.21) == True
    print("  - Verified TVA utility phase synchronization check")
    
    model = EnergyGridModel()
    apparent = model.calculate_apparent_power(1.21e9, 0.95)
    assert apparent > 1.21e9
    print(f"  - Calculated 1.21 GW apparent substation load: {apparent*1e-6:.2f} MVA")
    
    sco2_power = model.calculate_sco2_efficiency_boost(800.0, 50.0) # 800K exhaust, 50kg/s flow
    assert sco2_power > 0
    print(f"  - Calculated sCO2 waste-heat recovered power output: {sco2_power*1e-6:.2f} MWe")
    
    shed = shed_load_profile(59.4)
    assert shed == 0.6
    print(f"  - Verified grid drop emergency load-shed factor: {shed*100:.0f}%")
    
    duration_ms = (time.perf_counter() - t0) * 1000.0
    print(f"[TEST-METRICS] Status=SUCCESS Latency={duration_ms:.3f}ms")

if __name__ == '__main__':
    test_grid_calculations()
