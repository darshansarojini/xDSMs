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

x.add_system("aero", SOLVER, r"\text{Aerodynamics}")
x.add_system("prop", SOLVER, r"\text{Propulsion}")
x.add_system("struc", SOLVER, r"\text{Structural Dynamics}")
x.add_system("iner_loads", SOLVER, r"\text{Inertial Loads}")
x.add_system("eom", IFUNC, r"\text{EoM}")
x.add_system("stab", FUNC, r"\text{Stability}")
x.add_system("noise", IFUNC, r"\text{Acoustics}")

x.add_input("aero", (r'\Vec{x}, \Vec{u}', r'\text{Geometry DVs}'))
x.add_input("prop", (r'\Vec{x}, \Vec{u}', r'\text{Geometry DVs}'))
x.add_input("struc",  (r'\text{Thicknesses}', r'\text{Material}'))
x.add_input("iner_loads", r'\Vec{x}')
x.add_input("eom", r'\Vec{x}, \Vec{u}')
x.add_input("noise", (r'\Vec{u}', r'\text{Geometry DVs}'))

x.add_output("aero", r'\vec{f}_{a}, \vec{m}_{a}')
x.add_output("prop", r'\vec{F}_{p_{n_p}}, \vec{M}_{p_{n_p}}')
x.add_output("eom", r'{r_{eom}}', side=LEFT)
x.add_output("stab", r'\text{Handling qualities}', side=LEFT)
x.add_output("noise", r'\text{Noise maps}', side=LEFT)

x.connect("aero", "eom", (r'\vec{F}_{a}, \vec{M}_{a}', r' \frac{\partial \vec{F}_{a}}{\partial \vec{x}} \& \frac{\partial \vec{M}_{a}}{\partial \vec{x}}'))
x.connect("aero", "struc", (r'\vec{f}_{a}, \vec{m}_{a}'))
x.connect("prop", "aero", r'\text{Wake}')

x.connect("prop", "struc", r'\vec{F}_{p_{n_p}}, \vec{M}_{p_{n_p}}')
x.connect("prop", "eom", (r'\vec{F}_{p}, \vec{M}_{p}', r' \frac{\partial \vec{F}_{p}}{\partial \vec{x}} \& \frac{\partial \vec{M}_{p}}{\partial \vec{x}}'))
x.connect("prop", "noise", r'T, \tau')

x.connect("struc", "aero", r'\text{Deflection}')
x.connect("struc", "prop", r'\text{Deflection}')

x.connect("iner_loads", "eom", (r'\vec{F}_{g}, \vec{M}_{g}', r' \frac{\partial \vec{F}_{g}}{\partial \vec{x}} \& \frac{\partial \vec{M}_{g}}{\partial \vec{x}}'))

x.connect("eom", "stab", (r'A, B'))

x.write("caddee_aeromechanics", cleanup=False)
