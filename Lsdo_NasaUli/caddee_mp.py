from inspect import stack
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
import os


x = XDSM()

# region Analysis blocks
x.add_system("opt", OPT, r"\text{Optimizer}")
x.add_system("dummy1", GROUP, r"\text{....}")
x.add_system("struc_wt", IGROUP, (r"\text{Structural}", r"\text{Weight Estimation}"))
x.add_system("bat_wt", SOLVER, (r"\text{Battery}", r"\text{Sizing}"))
x.add_system("motor_wt", SOLVER, (r"\text{Motor Sizing}", r"m=1,\ldots, M"))
x.add_system("acmp", IFUNC, (r"\text{Aircraft MP}", r"\text{Computation}"))
x.add_system("aeromech", IGROUP, (r"\text{Mission Segment}", r"\text{Aeromechanics}"), stack=True)
x.add_system("powerenergy", IGROUP, (r"\text{Power and}", r"\text{Energy Analysis}"))
x.add_system("dummy2", GROUP, r"\text{....}")

x.connect("opt", "motor_wt", (r"\text{Rated speed}", r"\text{Rated power}"))
x.connect("opt", "bat_wt", (r"\text{Number of cells}"))
x.connect("opt", "struc_wt", (r'\text{Thicknesses}', r'\text{Material}'))

x.connect("struc_wt", "acmp", r"MP_{struc}")
x.connect("bat_wt", "acmp", r"MP_{battery}")
x.connect("motor_wt", "acmp", (r"MP_{motor}",
                               r"m=1,\ldots, M"))
x.connect("motor_wt", "aeromech", (r"\text{Max T, Q}",
                                   r"m=1,\ldots, M"))
x.connect("aeromech", "struc_wt", r'\text{Loads}', stack=True)
x.connect("acmp", "aeromech", r"MP_{AC}")

x.connect("bat_wt", "powerenergy", r"\text{Battery}")
x.connect("motor_wt", "powerenergy", (r"\text{Motor}", r"m=1,\ldots, M"))

x.add_output("acmp", r"MP_{AC}")
x.add_output("motor_wt", (r"\text{c: Motor L, D}",
                          r"m=1,\ldots, M"))

x.write("caddee_mp", build=True, outdir=os.path.dirname(os.path.realpath(__file__)))
