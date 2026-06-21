# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grid_model import shed_load_profile
def test_emergency():
    shed = shed_load_profile(59.3)
    assert shed == 0.6
    print("  [PASS] Emergency grid drop load shedding boundaries validated.")
