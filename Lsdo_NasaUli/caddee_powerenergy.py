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
x.add_system("sizing", GROUP, r"\text{Sizing}")
x.add_system("dummy2", GROUP, r"\text{....}")
x.add_system("ms_am", IGROUP, (r"\text{Mission Segment}", r"\text{ Aeromechanics}"), stack=True)
x.add_system("dummy3", GROUP, r"\text{....}")
x.add_system("motor_analy", IFUNC, (r"\text{Motor}", r"\text{Analysis}"), stack=True)
x.add_system("batt_analy", IFUNC, (r"\text{Battery}", r"\text{Analysis}"))
x.add_system("dummy4", GROUP, r"\text{....}")
# endregion

# region Connections
# Sizing to other blocks
x.connect("sizing", "motor_analy", (r"\text{Motor length}",
                                    r"\text{Motor diameter}"))
x.connect("sizing", "batt_analy", r"\text{Battery}")
# Aeromechanics to other blocks
x.connect("ms_am", "motor_analy", (r"\text{Segment torque}",
                                   r"\text{Segment RPM}"), stack=True)
x.connect("ms_am", "batt_analy", r"\text{Segment time}", stack=True)
# Motor analysis to other blocks
x.connect("motor_analy", "batt_analy", r"\text{Power}", stack=True)
x.connect("batt_analy", "motor_analy", r"\text{Voltage}")
# endregion

# region Inputs and Outputs
# Outputs
x.add_output("batt_analy",
             r"\text{SoC}")
# x.add_output("motor_sizing",
#              r"\text{Motor weight}")
# # endregion


# # endregion

x.write("caddee_powerenergy", build=True, outdir=os.path.dirname(os.path.realpath(__file__)))
