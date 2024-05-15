def calculate_energy(solar_radiation: float) -> float:
    installation_power = 2.5  # kW
    panel_efficiency = 0.2
    exposure_time = solar_radiation / 3600  # convert from Joules to hours

    energy = installation_power * exposure_time * panel_efficiency
    return energy
