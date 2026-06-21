# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton / GlacierEQ — All Rights Reserved
"""
grid_model.py — AC/DC Power Impedance & Load Balance Models
===========================================================
Helix Alpha Strand: Multi-Gigawatt Substation & Phase Angle Physics.
"""
import math

class EnergyGridModel:
    """Models load balancing and reactive impedance calculations for the 1.21 GW substation."""
    def __init__(self) -> None:
        # Standard power requirements: Back to the Future 1.21 GW Easter Egg
        self.bttf_load_w = 1.21e9 

    def calculate_apparent_power(self, real_power_w: float, power_factor: float) -> float:
        """
        Computes apparent power (VA) based on active power and power factor.
        Equation: S = P / PF
        """
        if not (0 < power_factor <= 1.0):
            raise ValueError("Power factor must be in range (0, 1.0]")
        return real_power_w / power_factor

    def calculate_voltage_drop(self, current_a: float, resistance_ohm: float, reactance_ohm: float, pf: float) -> float:
        """
        Estimates terminal voltage drop over high-voltage feed lines.
        Equation: V_drop = I * (R * cos(theta) + X * sin(theta))
        """
        theta = math.acos(pf)
        return current_a * (resistance_ohm * math.cos(theta) + reactance_ohm * math.sin(theta))
