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
x.add_system("motor_sizing", SUBOPT, (r"\text{Motor}", r"\text{Sizing}"))
x.add_system("motor_analy", IFUNC, (r"\text{Motor}", r"\text{Analysis}"), stack=True)
x.add_system("batt_analy", IFUNC, (r"\text{Battery}", r"\text{Analysis}"))
# endregion

# region Connections
# Motor sizing to other blocks
x.connect("motor_sizing", "motor_analy",
          (r"\text{Motor length}",
           r"\text{Motor diameter}"))
# Motor analysis to other blocks
x.connect("motor_analy", "batt_analy", r"\text{Power}", stack=True)
x.connect("batt_analy", "motor_analy", r"\text{Voltage}")
# endregion

# region Inputs and Outputs
# Inputs
x.add_input("motor_sizing", (r"\text{Maximum thrust}",
                             r"\text{Cruise RPM}",
                             r"\text{Rotor diameter}"))
x.add_input("motor_analy",
            (r"\text{Segment torque}",
             r"\text{Segment RPM}"),
            stack=True)
x.add_input("batt_analy",
            (r"\text{Segment time}",
             r'\text{Number of cells}'),
            stack=True)

# Outputs
x.add_output("batt_analy",
             (r"\text{SoC}",
              r"\text{Battery weight}"))
x.add_output("motor_sizing",
             r"\text{Motor weight}")
# # endregion

# # region Process connect
# x.add_process(
#     ["doe", "aero_anal", "sae_loads", "struc_sizing", "cert_anal"],
#     arrow=True,
# )
# # endregion

x.write("caddee_powerenergy", build=True, outdir=os.path.dirname(os.path.realpath(__file__)))