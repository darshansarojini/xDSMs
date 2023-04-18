from pyxdsm.XDSM import (
    XDSM,
    OPT,
    SUBOPT,
    SOLVER,
    DOE,
    IFUNC,
    FUNC,
    GROUP,
    IGROUP,
    METAMODEL,
    LEFT,
    RIGHT,
)

x = XDSM()

x.add_system("opt", OPT, r"\text{Optimizer}")
x.add_system("cr_aero", FUNC, (r"\text{Cruise}", r"\text{Aerodynamics}"))
x.add_system("constr_analy", FUNC, (r"\text{Constraint}", r"\text{Analysis}"))
x.add_system("miss_analy", FUNC, (r"\text{Mission}", r"\text{Analysis}"))
x.add_system("ac_param", FUNC, (r"\text{Aircraft}", r"\text{Parameters}"))
x.add_system("fueltank", FUNC, (r"\text{Fuel Tank}", r"\text{Volume}"))

x.connect("opt", "cr_aero", r'AR_{eff}, \Lambda_{25}, \lambda_{eff}')
x.connect("opt", "constr_analy", (r'AR_{eff}, \Lambda_{25}, \lambda_{eff}', r'V/V_{md}'))
x.connect("opt", "miss_analy", r'AR_{eff}, \Lambda_{25}, \lambda_{eff}')
x.connect("opt", "fueltank", r'AR_{eff}, t/c, \lambda_{eff}')

x.connect("cr_aero", "constr_analy", r'\left( L/D \right)_{max}')
x.connect("cr_aero", "miss_analy", r'\left( L/D \right)_{max}')

x.connect("constr_analy", "ac_param", r'T_{TO}/W_{TO}, W_{TO}/S_W')

x.connect("miss_analy", "ac_param", r'W_{TO}')

x.connect("miss_analy", "fueltank", r'm_F')
x.connect("ac_param", "fueltank", r'S_W')

x.connect("ac_param", "cr_aero", r'S_W')

x.connect("miss_analy", "opt", (r'f: W_{TO}', r'c: L_{cr} > W_{TO}', r'c: m_L > m_{ZFW} + m_{F_{res}}'))
x.connect("cr_aero", "opt", r'f: V_{cr}>V_{stall}')
x.connect("fueltank", "opt", r'c: V_T>V_F')

x.add_output("miss_analy", r'W_{TO}')
x.add_output("ac_param", (r'T_{TO}', r'S_{W}'))

x.add_input("constr_analy", (r'M', r's_{TOFL}, s_{LFL}', r'C_{L_{max,TO}}, C_{L_{max,L}}'))
x.add_input("miss_analy", (r'M, R',  r'n_{pax}, m_{cargo}', r'd_{F_o}, BPR'))

x.write("loftin_aircraft_sizing", cleanup=False)
