# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grid_model import EnergyGridModel
def test_nominal():
    g = EnergyGridModel()
    s = g.calculate_apparent_power(1.21e9, 0.98)
    assert s > 1.21e9
    drop = g.calculate_voltage_drop(1000.0, 0.02, 0.01, 0.95)
    assert drop > 0
    print("  [PASS] Nominal line impedance voltage drop analysis successful.")
