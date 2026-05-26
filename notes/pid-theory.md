# PID theory notes

Working notes from learning PID 

## TODO
- error:
    say our system has theta, our current angle, and theta_d, our desired angle. error (e) = desired angle - current angle. e = theta_d - theta. positive error means we under shot, needs to move forward. negative error means we over shot, we need to move back. every controller takes in error as an input to a function and outputs some change in the angle.
- [ proportional ] P term: physical intuition, steady-state error under load
    this is the simplest controller. multiply your error by a constant, that output is your command.

    example: torque = K_p * error (where K_p is a gain, a constant setting how aggresively the controller responds)
    P acts as a spring, pushing harder the larger the error is.

    trouble shooting:
    small K_p takes forever to reach the setpoint. might never reach with other forces
    big K_p causes fast response, but the system never reaches a small enough error to stabilize, it ends up oscillating.

    why is P alone not enough?
    imagine an arm at angle theta, of mass m, distance l with gravity g. torque on the arm is tau = -m g l sintheta, and the desired angle is theta_d = pi/2. for the controller to hold that angle, it must cancel out the gravitational torque at theta_d, so mgl. thus mgl = e * k_p, e = mgl/K_p. error can never be zero, because then torque from controller is zero, and gravity causes the arm to fall. P must hold a permanent error to generate the torque it needs. error must be non zero for torque from the controller to match gravitational torque. this is called STEADY-STATE ERROR. P only controllers can not eliminate steady-state error against constant load. steady state error in this case = mgl/k_p. basically force_on_system/gain, formally disturbance/gain.

    whats the solution?
    cranking k_p shrinks e_ss (steady state error), but can never eliminate it (asympotically), and a large k_p will eventually cause overshooting and oscillations. you cant tune P to eliminate e_ss, you need another term (I)

    thoughts i had:
    (note that i derived gravity compensation independently. thinking about how to improve things is useful for developing intuition here.)

    well then why not make theta_d past pi/2? example theta_d = pi/2 + phi (offset)
    then the error when the arm is at pi/2 = phi. thus phi = mgl/k_p. this works! its actually called feedforward compensation, or gravity compensation in this case. 

    standard way to go about this:
    torque = k_p * e + t_ff (torque feed forward)
    t_ff is a function of theta, modeling gravity
    t_ff = mglsin(theta)

    this works for perfect systems, but mass can change, friction exists, there can be gusts of wind, or any disturbance. then the model breaks. this is standard on arm controllers. feeforward handles what you can model, and PID handle the residuals. because P can never fully eliminate the residuals, this is where I comes in.

- [ integral ] I term: why it kills steady-state error, windup
- [ ] D term: damping, noise amplification, derivative kick
- [ ] discretization: continuous → discrete-time form
- [ ] anti-windup strategies
- [ ] tuning intuition + Ziegler-Nichols