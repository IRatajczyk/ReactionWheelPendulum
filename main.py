import numpy as np

import custom_rule_controller
import hybrid_controller
import lq_controller
import reaction_pendulum_plant
import trivial_observer
from utils import plot_sys

RP_params = reaction_pendulum_plant.ReactionPendulumParameters(control_saturation=1.0)
RP = reaction_pendulum_plant.ReactionPendulumPlant(RP_params)

TO_params = trivial_observer.TrivialObserverParameters()
TO = trivial_observer.TrivialObserver(TO_params)

Q = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1e-3]])
R = np.array([1])

LQ_params = lq_controller.LQRParameters(Q, R)
LQ = lq_controller.LQRController(LQ_params)

RBC_params = custom_rule_controller.CustomRuleControllerParameters()
RBC = custom_rule_controller.RuleController(RBC_params)

if __name__ == '__main__':
    f = RP.transition_function(saturated=True)
    o = TO.get_observation()
    x_ = np.array([0, np.pi, 0])
    A, B = RP.linearize(x_)

    LQ.tune_controller(A, B, x_)
    u = LQ.get_controller()
    RBC.tune_controller()
    rb = RBC.get_controller()

    HC_params = hybrid_controller.HybridControllerParameters(u, rb)
    HC = hybrid_controller.HybridController(HC_params)
    HC.tune_controller(threshold=.1)
    hc = HC.get_controller()

    hs = lambda t, x: f(x, hc(x))
    x0 = np.array([0, 0, 0])
    tspan = [0, 20]
    plot_sys(hs, tspan, x0, "RB system")


