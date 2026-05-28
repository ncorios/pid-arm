# pid-arm

1-DOF arm under gravity, controlled with PID. Warmup project before MISTI 2026.
gains emphasize what each term in PID does. not optimal.

## Layout
- `control/` — PID controller, FF model
- `notes/` — detailed PID and basic signal processing notes. referenced throughout project
- `numpy_experiments/` - code for P, PI, PID, PID + feedforward controllers with a simple numpy simulator. plots generated with run.
- `outputs/` - plots, arrays for each experiment
- `plants/` - pid arm dynamics
