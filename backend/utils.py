# backend/utils.py
from CoolProp.CoolProp import PropsSI

def steam_state_points(T0, V0, process_type, n_points=20):
    """
    Generate points for non-flow processes using CoolProp.
    T0: initial temperature (K)
    V0: initial specific volume (m³/kg)
    process_type: string
    n_points: number of points to calculate
    """
    points = []

    # Clamp T0 to realistic range
    T0 = max(273.15, min(T0, 1073.15))

    for i in range(n_points):
        T = T0
        V = V0

        # Define small increments based on process
        if process_type == "constant_volume":
            T = T0 + i * 2
        elif process_type == "constant_pressure":
            T = T0 + i * 2
            V = V0 * (T/T0)
        elif process_type == "isothermal":
            T = T0
            V = V0 * (1 + 0.02*i)
        elif process_type == "adiabatic":
            gamma = 1.4
            V = V0 * (1 + 0.02*i)
            T = T0 * (V0/V)**(gamma-1)
        elif process_type == "polytropic":
            n = 1.3
            V = V0 * (1 + 0.02*i)
            T = T0 * (V0/V)**(n-1)

        try:
            P = PropsSI("P", "T", T, "D", 1/V, "Water")  # Pa
            s = PropsSI("S", "T", T, "D", 1/V, "Water")  # J/kg.K
            points.append({
                "T": T,
                "P": P/1e5,  # convert Pa to bar
                "v": V,
                "s": s/1000  # convert J/kg.K to kJ/kg.K
            })
        except:
            points.append({
                "T": T,
                "P": None,
                "v": V,
                "s": None
            })

    return points
