import numpy as np
import matplotlib.pyplot as plt
from control.control import PID, feedforward
from plants.arm import Arm
from numpy_experiments import data_helpers

# simple experiment to test the PID controller + feedforward torque on the arm. We will apply a step input in desired angle and see how the arm responds under PI control.
# gains tuned through practical method described in pid-theory
# feedforward torque added to compliment pid, makes convergence faster
# tuned for fast convergence and accuracy. 
# <.5 second convergence, no overshoot. critically dampened
# only distrubances to the system are gravity and friction.
# low friction, so ff handles gravity and i term isnt needed. tiny ki added bc why not
# tuned for hypothetical infinite torque actuator. would saturate most real motors immediately

if __name__ == "__main__":
    arm = Arm(m=1.0, l=1.0, g=9.81, b=0.1, theta = 0.0, dt=0.001) # initialize arm with mass=1kg, length =1m, gravity=9.81m/s^2, damping=0.1, initial angle= 0 radians, timestep=0.001s
    states =[]# list to store states for plotting
    taus = [] # list to store torques for arrays
    n = 10000 # n = timesteps, lower than last experiment
    pid = PID(kp=200.0, ki=0.3, kd=26.0, dt=arm.dt) # initialize PID controller with kp, ki, high kd to show the effect of the D term
    theta_d = np.pi/2 # desired angle step input (90 degrees)
    exact_settle = data_helpers.solve_ss(theta_d, arm.m * arm.g * arm.l, pid.kp) # solves exact e_ss
    for _ in range(n):
        pid.update_theta(arm.theta)
        tau = pid.calc_torque(theta_d) + feedforward(arm.theta, arm.m, arm.l, arm.g) # add feedforward torque to compliment PID
        state = arm.step(tau) # apply torque to the arm and get new state
        states.append(state) # for plotting
        taus.append(tau) # for data saving
       
    states = np.array(states)
    taus = np.array(taus)
    t_arr = np.arange(n) * arm.dt

    # plot

    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    title = f"PID + FF: Kp={pid.kp}, Ki={pid.ki}, Kd={pid.kd}"
    fig.suptitle(title)
    
    axes[0].axhline(theta_d, color='k', linestyle='--', alpha=0.5, label='setpoint (pi/2 rad)')
    axes[0].plot(t_arr, states[:, 0], label='θ')
    axes[0].set_ylabel('angle (rad)')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    axes[1].plot(t_arr, states[:, 1], color='tab:orange', label='θ̇')
    axes[1].set_ylabel('angular velocity (rad/s)')
    axes[1].set_xlabel('time (s)')
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('outputs/plots/pidf.png', dpi=120)
    plt.show()
    
    data_helpers.save_run('outputs/arrays/pidf.npz', t_arr, states, np.array(taus), theta_d, arm, pid) # save data for later analysis
