import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


def plot_sys(sys, tspan, x0, title: str):
    result = solve_ivp(sys, t_span=tspan, y0=x0, t_eval = np.linspace(0,20,2000))
    plt.plot(result.t, result.y[0, :].T, label="theta_dot")
    plt.plot(result.t, result.y[1, :].T / np.pi, label="theta")
    plt.grid()
    plt.legend()
    plt.title(title)
    plt.ylim()
    plt.show()
