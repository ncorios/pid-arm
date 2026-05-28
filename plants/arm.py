import numpy as np
import matplotlib.pyplot as plt

class Arm:
    """
    1-DOF revolute arm under gravity. Point mass m at distance l from pivot.
    
    State: theta (angle from vertical, rad), theta_dot (angular velocity, rad/s)
    Input: tau (applied torque at the joint, Nm)
    """
    
    def __init__(self, m, l, g, b, theta, dt):
        # store parameters and initial state
        self.m = m
        self.l = l
        self.g = g
        self.b = b
        self.dt = dt
        self.theta = theta
        self.theta_dot = 0.0
    
    def step(self, tau):
        # advance the simulation by one timestep dt under applied torque tau.
        # return the new (theta, theta_dot).
        tau_gravity = self.m * self.g * self.l * np.sin(self.theta) #t_g = m * g * l * sin(theta)
        tau_friction = self.b * self.theta_dot #t_f = b * theta_dot, where b is the damping coefficient.
        tau_net = tau - tau_gravity - tau_friction
        theta_ddot = tau_net / (self.m * self.l**2) #theta_ddot = tau_net / I, where I = m * l^2 is the moment of inertia of the point mass at distance l
        self.theta_dot += theta_ddot * self.dt 
        self.theta += self.theta_dot * self.dt
        return (self.theta, self.theta_dot)

    
    def reset(self, theta=0.0, theta_dot=0.0):
        # reset to initial state, useful between experiments
        self.theta = theta
        self.theta_dot = theta_dot
    
    @property
    def state(self):
        # return (theta, theta_dot) as a tuple
        return (self.theta, self.theta_dot)
    

# if __name__ == "__main__":
#         # simple test of the arm dynamics
#         states = []
#         n = 5000 # n = timesteps
#         arm = Arm(m=1.0, l=1.0, g=9.81, b=0.1, theta = np.pi/2, dt=0.01) #initialize arm with mass=1kg, length=1m, gravity=9.81m/s^2, damping=0.1, initial angle= pi/2 radians, timestep=0.01s
#         for t in range(n):
#             state = arm.step(tau = 0) # apply zero torque, should see gravity oscillations + decay due to friction
#             # add state to a list for plotting
#             states.append(state)

#         states = np.array(states)
#         t = np.arange(n) * arm.dt
#         plt.plot(t, states[:,0], label='theta (rad)')
#         plt.plot(t, states[:,1], label='theta_dot (rad/s)')
#         plt.legend()
#         plt.title('Arm Dynamics under Gravity with Damping')
#         plt.xlabel('Time (s)')
#         plt.show()
