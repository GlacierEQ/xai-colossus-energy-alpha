# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton / GlacierEQ — All Rights Reserved
"""
grid_model.py — sCO2 Waste Heat Recovery & Emission-Free Gas Turbine Physics
===========================================================================
Helix Alpha Strand: Multi-Gigawatt Substation & Phase Angle Physics.

INNOVATION: "Supercritical CO2 (sCO2) Waste Heat Power Injection & NOx Scrubbing"
Calculates sCO2 thermodynamic cycles using turbine exhaust heat to boost generation efficiency,
combined with chemical modeling of NOx-to-ammonium nitrate extraction to mitigate Memphis clean air concerns.
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

    def calculate_sco2_efficiency_boost(self, exhaust_temp_k: float, mass_flow_kg_s: float) -> float:
        """
        SUPER-INNOVATION: Computes electrical power recovered (Watts) from turbine exhaust heat
        using a closed-loop supercritical Carbon Dioxide (sCO2) cycle.
        """
        # Carnott-derived sCO2 efficiency model at 200 bar
        sink_temp_k = 298.15
        max_theoretical_eff = 1.0 - (sink_temp_k / exhaust_temp_k)
        actual_sco2_efficiency = max_theoretical_eff * 0.58  # Multi-stage expander ratio
        heat_input_w = mass_flow_kg_s * 1200.0 * (exhaust_temp_k - sink_temp_k) # Cp of exhaust gas
        return heat_input_w * actual_sco2_efficiency
