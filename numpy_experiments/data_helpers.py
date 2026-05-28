import numpy as np

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
