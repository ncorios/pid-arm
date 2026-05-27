import numpy as np
import matplotlib.pyplot as plt

class PID:
    # define a PID controller class with methods for P, I, D terms and a method to compute the control output given the current error.
    # torque(e,theta)= K_p*e + K_i*integrator + K_d*de/dt + torque_ff(theta)
    # where:
    # e = theta_d - theta (error)
    # integrator += e * dt (integral/accumulated error)
    # de/dt = rate of change of error, (D often also can be -K_d*dtheta/dt)
    # torque_ff(theta) = torque computed from a model, not inherently standard but complements. pid can usually eliminate error without modeling

    def __init__(self, kp, ki, kd, theta, theta_d, dt):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.theta = theta
        self.theta_d = theta_d
        self.error = self.theta_d - self.theta
        self.integrator = 0
        self.last_theta = self.theta

    def update_theta(self, theta, theta_d):
        self.last_theta = self.theta
        self.theta = theta
        self.theta_d = theta_d
        return self.theta
    
    def update_error(self):
        self.last_error = self.error
        self.error = self.theta_d - self.theta
        return self.error
    
    def calc_P(self):
        self.p = self.kp * self.error
        return self.p
    
    def calc_I(self):
        self.integrator += self.error * self.dt
        self.i = self.ki * self.integrator
        return self.i
    
    def calc_D(self):
        # using dtheta/dt, will add filtering later
        self.theta_dot = (self.theta - self.last_theta) / self.dt
        self.d = -self.kd * self.theta_dot
        return self.d
    
    def calc_torque(self):
        self.update_error()
        self.torque = self.calc_P() + self.calc_I() + self.calc_D()
        return self.torque
    


        

   
    


        


 