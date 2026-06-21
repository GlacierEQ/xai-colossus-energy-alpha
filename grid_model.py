# SPDX-License-Identifier: Proprietary
# Copyright (c) 2026 Casey del Carpio Barton / GlacierEQ — All Rights Reserved
"""
grid_model.py — sCO2 Waste Heat Recovery & Emission-Free Gas Turbine Physics
===========================================================================
Helix Alpha Strand: Multi-Gigawatt Substation & Phase Angle Physics.
"""
import math

STEALTH_SIGIL = "MW-JGN-TIER1-SNTNL"

# 1. PREPARATION LEVEL
def verify_phase_synchronization(tva_phase_angle: float, local_generator_phase_angle: float) -> bool:
    delta = abs(tva_phase_angle - local_generator_phase_angle)
    return delta < 0.05

# 2. OPERATION LEVEL
class EnergyGridModel:
    def __init__(self) -> None:
        self.bttf_load_w = 1.21e9 

    def calculate_apparent_power(self, real_power_w: float, power_factor: float) -> float:
        if not (0 < power_factor <= 1.0):
            raise ValueError("Power factor must be in range (0, 1.0]")
        return real_power_w / power_factor

    def calculate_voltage_drop(self, current_a: float, resistance_ohm: float, reactance_ohm: float, pf: float) -> float:
        theta = math.acos(pf)
        return current_a * (resistance_ohm * math.cos(theta) + reactance_ohm * math.sin(theta))

    def calculate_sco2_efficiency_boost(self, exhaust_temp_k: float, mass_flow_kg_s: float) -> float:
        sink_temp_k = 298.15
        max_theoretical_eff = 1.0 - (sink_temp_k / exhaust_temp_k)
        actual_sco2_efficiency = max_theoretical_eff * 0.58
        heat_input_w = mass_flow_kg_s * 1200.0 * (exhaust_temp_k - sink_temp_k)
        return heat_input_w * actual_sco2_efficiency

# 3. EMERGENCY REACTION LEVEL
def shed_load_profile(grid_frequency_hz: float) -> float:
    if grid_frequency_hz < 59.5:
        print(f"[STEALTH-ALERT] {STEALTH_SIGIL}: Grid frequency drop ({grid_frequency_hz} Hz). Shedding 40% of compute load.")
        return 0.6
    return 1.0
