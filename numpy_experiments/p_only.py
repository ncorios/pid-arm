import numpy as np
import matplotlib.pyplot as plt
from control.control import PID
from plants.arm import Arm
from numpy_experiments import data_helpers

# simple experiment to test the P term of the PID controller on the arm. We will apply a step input in desired angle and see how the arm responds under just P control.
# the linear small error prediction is e_ss = mgl/kp which is around .98 rad. the actual reponse gives e_ss of around .84 rad
# this reflects non linear gravity term, and a low friction environment.
#k_p tuned to reflect steady state error, and the failure of linear approximation
# longer run for convergence to steady state error




if __name__ == "__main__":
    arm = Arm(m=1.0, l=1.0, g=9.81, b=0.1, theta = 0.0, dt=0.001) # initialize arm with mass=1kg, length
    states =[]# list to store states for plotting
    taus = [] # list to store torques for arrays
    n = 100000 # n = timesteps
    pid = PID(kp=10.0, ki=0.0, kd=0.0, dt=arm.dt) # initialize PID controller with only P term
    theta_d = np.pi/2 # desired angle step input (90 degrees)
    exact_settle = data_helpers.solve_ss(theta_d, arm.m * arm.g * arm.l, pid.kp) # solves exact e_ss
    for _ in range(n):
        pid.update_theta(arm.theta)
        tau = pid.calc_torque(theta_d)
        state = arm.step(tau) # apply torque to the arm and get new state
        states.append(state) # for plotting
        taus.append(tau) # for data saving
       
    states = np.array(states)
    taus = np.array(taus)
    t_arr = np.arange(n) * arm.dt


    # plot
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    
    title = f"P: Kp={pid.kp}, Ki={pid.ki}, Kd={pid.kd}"
    fig.suptitle(title)

    axes[0].axhline(theta_d, color='k', linestyle='--', alpha=0.5, label='setpoint (pi/2 rad)')
    linear_prediction = arm.m * arm.g * arm.l / pid.kp #calculation for linear prediction of e_ss = mgl/kp
    axes[0].axhline(linear_prediction, color='green', linestyle='--', alpha=0.5, label=f'linear ss prediction ({linear_prediction:.3f} rad)')
    axes[0].axhline(exact_settle, color='red', linestyle=':', alpha=0.8, label=f'exact ss pred. ({exact_settle:.3f} rad)')
    axes[0].plot(t_arr, states[:, 0], label='θ')
    axes[0].set_ylabel('angle (rad)')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    axes[1].plot(t_arr, states[:, 1], color='tab:orange', label='θ̇')
    axes[1].set_ylabel('angular velocity (rad/s)')
    axes[1].set_xlabel('time (s)')
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('outputs/plots/p_only.png', dpi=120)
    plt.show()
    
    data_helpers.save_run('outputs/arrays/p_only.npz', t_arr, states, np.array(taus), theta_d, arm, pid) # save data for later analysis