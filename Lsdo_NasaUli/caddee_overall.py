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
x.add_system("geom", IFUNC, r"\text{Geometry Update}")
x.add_system("weight", SUBOPT, (r"\text{Aircraft Mass}", r"\text{Properties Estimation}"))
x.add_system("aeromech", IGROUP, r"\text{Mission Segment Aeromechanics}", stack=True)
x.add_system("energy_analy", IFUNC, r"\text{Power and Energy Analysis}")
x.add_system("cost_analy", IFUNC, r"\text{Cost Analysis}")

x.connect("opt", "geom", (r'\text{Geometric DVs}', r'\text{Motion DVs}'))
x.connect("opt", "aeromech", r'\text{Operating conditions}')
x.connect("opt", "weight", (r'\text{Thicknesses}', r'\text{Material}'))
x.connect("opt", "energy_analy", r'\text{Operating conditions}')

x.connect("geom", "weight", r'\text{Actuated geometry}')
x.connect("geom", "aeromech", r'\text{Actuated geometry}', stack=True)

x.connect("weight", "aeromech", r'\text{Mass properties}')
x.connect("weight", "opt", r'\text{c: Structural margins}')
x.connect("weight", "cost_analy", r'\text{Weight}')

x.connect("aeromech", "weight", r'\text{Loads}', stack=True)
x.connect("aeromech", "energy_analy", (r'\text{Torque}', r'\text{Thrust}', r'\text{Time}'), stack=True)
x.connect("aeromech", "opt", (r'\text{c: EoM residuals}',
                              r'\text{c: Handling qualities}',
                              r'\text{c: Noise maps}'), stack=True)

x.connect("energy_analy", "opt", r'\text{c: State of charge}')
x.connect("energy_analy", "cost_analy", r'\text{Energy usage}')

x.connect("cost_analy", "opt", r'\text{f: Direct operating cost}')

x.write("caddee_overall", cleanup=False)
