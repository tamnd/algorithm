---
tag: 373QBF
kind: algorithm
slug: admittance-control
name: Admittance control
aliases:
- position-based impedance control
area: robotics/grasping-and-manipulation
level: core
summary: "Measures the contact force and turns it into a motion through a virtual mass-spring-damper, for stiff position-controlled robots."
model: real-ram
complexity:
  vars: {n: "the dimension of the task space; the bounds are for one control period and exclude the inner position loop"}
  time: {per_step: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, online: true, exact: false}
history:
  year: 1985
  people: [Neville Hogan]
  note: Hogan described impedance and admittance as the two causal forms of the same interaction law; robots with stiff position servos realize it in the admittance form.
prereqs: [impedance-control]
see_also: [hybrid-position-force-control, pd-control-with-gravity-compensation, euler-method, peg-in-hole, wrench, passivity, operational-space-formulation, jacobian-statics-duality]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 11, Section 11.7.2 (admittance-control algorithm)
  - paper: doi:10.1115/1.3140702
    title: "Neville Hogan, Impedance control: an approach to manipulation: Part I, Theory, Journal of Dynamic Systems, Measurement, and Control 107(1), 1985"
    locator: pages 1 to 7
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 9 (force control, impedance control with an inner position loop)
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: Chapter 9 (Force Control, by Luigi Villani and Joris De Schutter)
---

Admittance control is the form of [impedance control](/impedance-control/) for robots that accept only position or velocity commands. A force sensor at the wrist measures the contact force. The controller feeds this force into a virtual mass-spring-damper, integrates it once per control period, and sends the resulting position to the robot's own stiff position loop. The robot then moves as the virtual system would: it gives way to a push and returns to its goal when the push stops. It works well in free space and against soft surfaces. Against stiff surfaces it can chatter or bounce, which is the opposite of impedance control with torque commands.

## In plain words

Most industrial robots are built to hold a position very stiffly. You cannot tell them "be soft"; you can only tell them where to go. Admittance control adds softness on top. A sensor feels the force on the tool. The controller asks: if the tool were a weight on a spring and a shock absorber, and this force pushed on it, where would it be a moment later? It sends that point to the robot as the next position.

When nothing touches the tool, the spring pulls the point back to the goal. When a person pushes the tool, the point moves along with the push. When the tool presses on a table, the point settles where the spring force equals the contact force.

## The problem

The robot has a position loop that makes its task position $x \in \mathbb{R}^n$ follow a command $x_c$ closely. A force sensor measures the force $F$ that the environment applies to the tool. A goal motion $x_0(t)$ and target matrices $M_a$, $D_a$, $K_a$ (symmetric positive definite, usually diagonal) are given. The task is to compute $x_c$ at each control period $\Delta t$ so that

$$M_a(\ddot x_c - \ddot x_0) + D_a(\dot x_c - \dot x_0) + K_a(x_c - x_0) = F,$$

and so that $x \approx x_c$ when the position loop is good. The version below takes $\ddot x_0 = 0$, which is the usual case of a fixed or slowly moving goal.

## The algorithm

The controller keeps the commanded position $x_c$ and speed $v_c$ as its state, with $x_c$ equal to the measured position and $v_c = 0$ at the start.

```pseudo id=main
ADMITTANCE-STEP(x_c, v_c, x_0, x_0', F, M_a, D_a, K_a, Δt)
L1  a_c ← M_a⁻¹ (F - D_a (v_c - x_0') - K_a (x_c - x_0))
L2  v_c ← v_c + Δt a_c
L3  x_c ← x_c + Δt v_c                  ▷ semi-implicit Euler: uses the new v_c
L4  return x_c, v_c                     ▷ x_c goes to the position loop
```

Line L3 uses the speed from line L2, which is the semi-implicit (symplectic) [Euler method](/euler-method/). It is more stable for the lightly damped spring than the explicit Euler step. A velocity-controlled robot takes $v_c$ instead of $x_c$. In a robot with joint position control, $x_c$ goes through inverse kinematics first.

## Example

Take a one-axis Cartesian robot: a mass of 5 kg with a position loop of stiffness $K_p = 10^5$ N/m and critical damping $K_v = 2\sqrt{K_p \cdot 5} = 1414$ N s/m. A wall at $x_w = 1$ m acts as a spring of stiffness $k_e$. The robot starts at rest at 0.98 m, the goal is $x_0 = 1.02$ m, 2 cm inside the wall, and the targets are $M_a = 1$ kg and $K_a = 1000$ N/m. The control period is 1 ms, and the plant is simulated with RK4.

In the first period, $F = 0$ and $x_c = 0.98$, so line L1 gives $a_c = 1000 \cdot 0.04 = 40$ m/s$^2$, line L2 gives $v_c = 0.04$ m/s, and line L3 gives $x_c = 0.98004$ m.

| case | $D_a$ (N s/m) | $k_e$ (N/m) | first contact (s) | peak force (N) | final behavior |
|---|---|---|---|---|---|
| A | 1000 | $10^5$ | 0.707 | 20.49 | rest at 19.608 N |
| B | 100 | $10^4$ | 0.087 | 38.3 | rest at 18.018 N |
| C | 100 | $10^5$ | 0.087 | 155.1 | bounces, force between 0 and 150 N |

At rest, three springs are in series: the environment, the position loop and the virtual spring. The rest force is

$$F = \frac{x_0 - x_w}{1/k_e + 1/K_p + 1/K_a},$$

which gives 19.608 N for case A and 18.018 N for case B. Case C shows the weak point of admittance control: with the same virtual mass and spring that work on the softer wall in case B, the stiff wall makes the tool bounce for ever. More virtual damping, as in case A, cures it here at the cost of a slow approach.

## Correctness

The claim has two parts. First, with an exact force measurement, lines L1 to L3 are one step of a consistent and first-order accurate integrator of the target equation, so as $\Delta t \to 0$ the command $x_c$ converges to the exact solution on every bounded time interval. Second, at a rest point of the whole loop, $K_a(x_c - x_0) = F$, and if the position loop is a spring $K_p$ and the environment is a spring $k_e$, the force is the series formula above. Stability of the loop is not claimed in general: it depends on the inner loop, the period and the environment, and case C shows a failure. The proof file gives the full argument, and also the exact condition under which the discrete virtual dynamics alone are stable in one axis: $2 D_a\Delta t + K_a\Delta t^2 < 4 M_a$.

## Complexity

In the [real-RAM](/real-ram/) model, with diagonal targets, one control period takes $O(n)$ operations and $O(n)$ memory, where $n$ is the task dimension (at most 6 for a rigid tool). With full target matrices, line L1 solves a linear system with $M_a$, which takes $O(n^3)$ once if the factorization is stored, and then $O(n^2)$ per period. The force sensor reading, the inverse kinematics and the inner position loop are not counted.

## Properties

- **Works on position-controlled robots.** No torque interface and no dynamic model of the robot are needed. The inner loop hides friction and the robot's own inertia, so the virtual dynamics are reproduced well in free space.
- **Good in free space, weak on stiff contact.** A light virtual mass makes the robot easy to guide by hand, but against a stiff surface the loop of sensor, virtual dynamics, position loop and environment can become unstable. Impedance control with torque commands has the opposite strengths.
- **Bounded rest force.** At rest, the force is at most $K_a$ times the depth of the goal inside the surface, as for impedance control.
- **Discrete dynamics matter.** The virtual system runs in discrete time. Each axis needs $2 D_a\Delta t + K_a\Delta t^2 < 4 M_a$, or the integration diverges even without contact. A light virtual mass with large damping breaks this first.

## Variants and improvements

- **Velocity form.** Send $v_c$ to a velocity loop instead of $x_c$ to a position loop.
- **Rotations.** For the orientation of the tool, integrate the virtual dynamics on the rotation group, with an orientation spring based on the [axis-angle](/axis-angle-representation/) error, instead of on Euler angles.
- **Admittance in joint space.** The same law in joint coordinates, with joint torque sensors, gives a compliant joint behavior on a position-controlled robot.
- **Switching or blending with impedance control.** Since admittance control is good for soft environments and impedance control for stiff ones, some controllers blend the two forms.
- **Direct force tracking.** Setting $K_a = 0$ and putting the force error in place of $F$ turns the law into an integral force controller along that axis, which is one way to realize the force directions of [hybrid position/force control](/hybrid-position-force-control/) on a position-controlled robot.

## When to use it

Use it on industrial arms with stiff joint position servos and a wrist force sensor: hand guiding, contact following on surfaces of moderate stiffness, and assembly with a compliant tool or fixture. If the robot accepts torque commands and the contact is stiff, use [impedance control](/impedance-control/) instead. If a precise contact force must be held on a stiff surface, add a low virtual mass only along that axis with a high damping, and check the stability with the real loop rates.

## Pitfalls

- **Stiff environments.** The force feedback loop includes the environment stiffness. Against a stiff surface, a light virtual mass and low damping lead to bouncing, as in case C. Raise the damping or the mass, or add compliance to the tool.
- **Delay and filtering.** Force sensors are noisy and are often filtered. The filter delay adds to the loop delay and lowers the stability margin.
- **Sensor offset and tool weight.** The sensor measures the weight of the tool and its inertial forces too. Subtract them, or the robot drifts in free space.
- **Large virtual damping slows free motion.** The damping that makes contact stable also makes the robot slow to follow a push or to return to the goal.
- **Explicit Euler.** Updating $x_c$ with the old speed instead of the new one makes the lightly damped virtual spring gain energy at each step.

## Implementations

## History

Hogan's 1985 papers on impedance control described the impedance and the admittance as the two causal forms of the same interaction law and argued that the robot should be the impedance. Robots with stiff position servos cannot take a torque command, so the admittance form, with an outer force loop around the position loop, became the usual way to give them compliant behavior. Textbooks such as Siciliano et al. present it as impedance control with an inner position loop, and Lynch and Park give it as the admittance-control algorithm.

## References
