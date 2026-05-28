import numpy as np
import matplotlib.pyplot as plt
from control.control import PID
from plants.arm import Arm

# simple experiment to test the PI terms of the PID controller on the arm. We will apply a step input in desired angle and see how the arm responds under PI control.
#k_p will be kept from last experiment to reflect steady state error, and the failure of linear approximation.
#k_i will be added to eliminate steady state error, but will cause overshoot and oscillations due to the non linearity and low friction.
# lower n, smaller dt for forward euler stability
# you should see non decaying oscillations around the setpoint. close to the setpoint, but needs k_d to dampen the oscillations.

#define function to save data
def save_run(filename, t, states, taus, theta_d, arm, pid):
    np.savez(
        filename,
        t=t,
        theta=states[:, 0],
        theta_dot=states[:, 1],
        tau=taus,
        setpoint=theta_d,
        kp=pid.kp, ki=pid.ki, kd=pid.kd,
        m=arm.m, l=arm.l, g=arm.g, b=arm.b, dt=arm.dt,
    )

# define function for exact e_ss using the non linear equation e_ss = theta_d - mgl*sin(theta_d - e_ss)/kp, can be solved iteratively
def solve_ss(theta_d, mgl, kp, n_iter=100):
    theta_ss = theta_d
    for _ in range(n_iter):
        theta_ss = theta_d - mgl * np.sin(theta_ss) / kp
    return theta_ss


if __name__ == "__main__":
    arm = Arm(m=1.0, l=1.0, g=9.81, b=0.1, theta = 0.0, dt=0.001) # initialize arm with mass=1kg, length =1m, gravity=9.81m/s^2, damping=0.1, initial angle= 0 radians, timestep=0.001s
    states =[]# list to store states for plotting
    taus = [] # list to store torques for arrays
    n = 50000 # n = timesteps, lower than last experiment
    pid = PID(kp=10.0, ki=1.0, kd=0.0, dt=arm.dt) # initialize PID controller with kp from last experiment and add ki 
    theta_d = np.pi/2 # desired angle step input (90 degrees)
    exact_settle = solve_ss(theta_d, arm.m * arm.g * arm.l, pid.kp) # solves exact e_ss
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
    
    axes[0].axhline(theta_d, color='k', linestyle='--', alpha=0.5, label='setpoint (pi/2 rad)')
    linear_prediction = arm.m * arm.g * arm.l / pid.kp #calculation for linear prediction of e_ss = mgl/kp
    axes[0].axhline(.98, color='green', linestyle='--', alpha=0.5, label=f'linear ss prediction ({linear_prediction:.3f} rad)')
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
    plt.savefig('outputs/plots/pi.png', dpi=120)
    plt.show()
    
    save_run('outputs/arrays/pi.npz', t_arr, states, np.array(taus), theta_d, arm, pid) # save data for later analysis

