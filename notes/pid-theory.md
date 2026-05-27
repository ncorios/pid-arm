# PID theory notes

Working notes from learning PID 

big picture formula

torque(e,theta)= K_p*e + K_i*integrator + K_d*de/dt + torque_ff(theta)

where:
e = theta_d - theta (error)
integrator += e * dt (integral/accumulated error)
de/dt = rate of change of error, (D often also can be -K_d*dtheta/dt)
torque_ff(theta) = torque computed from a model, not inherently standard but complements. pid can usually eliminate error without modeling
## TODO
- [error]:
    say our system has theta, our current angle, and theta_d, our desired angle. error (e) = desired angle - current angle. e = theta_d - theta. positive error means we under shot, needs to move forward. negative error means we over shot, we need to move back. every controller takes in error as an input to a function and outputs some change in the angle.
- [proportional]
    P term: physical intuition, steady-state error under load

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

- [integral] 
    I term: why it kills steady-state error, windup

    P (proportional) 
    torque_integral = k_i * integrator
    integrator += e * dt (error * timestep)

    the integral term has memory. it uses accumulated error to increae torque until error is zero. at this point e = 0, the integrator stops increasing and the torque is held constant at theta_d, and in the case of the arm we've been talking about would be equal to graviational torque. so at theta_d in the arm at pi/2 case, torque_p = 0, torque_i = mgl.
    k_i tuning behaves similarly to k_p. small k_i takes forever. large k_i causes oscillations.

    if we have a pretty good model of our system, then p + ff should take care of the majority of output, and then the i term will handle our disturbances. this is because i does not require a model, it uses pure error to calculate output and does not fall into steady state error. the integrator grows until e = 0, at which point the controller "learns" the torque required without any modeling. i alone is unstable. p handles fast transient errors, ff handles modeled dynamics, i handles smaller disturbances, residuals, steady state error, etc.

    integral windup:

    I has a probelm that formulas dont know: actuator saturation
    motors have limits on torque, when the integrator i is unlimited, the torque accumulated by the I term can grow past this limit. once theta_d is reached, and the p term contributes no torque, the I term produces much larger torque than needed, causing massive overshoot, and eventually oscillations.

    how do we fix this?

    flag on the integral term
    "if not saturated" as a conditon for integration, but you want to allow helpful integration so if theres saturation in the direction opposing error thats fine. 

    pseudo(ish)code:
    if not saturated:
    integrator += e * dt
    else:  # saturated
        if sign(e) != sign(integrator):
            integrator += e * dt   # this would shrink integrator, allow
        # else: skip integration, would make windup worse
    
    back-calculation
    take the lost torque (commanded-applied) and feed it back to the integrator with a negative gain

    integrator claming
    integ = clip(integ,-max,+max) 
    works but u have to tune limits

    the larger lesson is that pid doesnt always carry cleanly into the real world. pid is simple. correct pid isn't.

- [derivative] 
    D term: damping, noise amplification, derivative kick

    2 forms

    error:
    torque_d = k_d * de/dt


    measurement:
    torque_d = -k_d * dtheta/dt
    negative bc error = theta_d - theta, dtheta_d/dt = 0

    de/dt = (e(n) - e(n -1))/dt
    behavior:
    setpoint = theta_d
    setpoint doesnt change: identical
    setpoint changes smoothly: both are fine, but measurement ignores the changes in setpoint
    setpoint change by step: error spikes, measurement is calm

    use -dtheta/dt for hardware applications, avoiding derivative kick (spikes with de/dt)

    what does d do?
    smooths the transient response, reduces overshoot, damps
    doesnt kill steady state error (de/dt = 0)
    d slows things down
    d doesnt fix noise, it creates noise problems without filtering

    tuning k_d:

    small k_d: system doesnt damp much, still oscillates
    large k_d: system is overdamped and sluggish
    
    D is damping. it pushes against motion.

    D suffers heavily from noise
    check signal-processing.md for noise and more


- [ ] discretization: continuous → discrete-time form
- [ ] anti-windup strategies
- [ ] tuning intuition + Ziegler-Nichols