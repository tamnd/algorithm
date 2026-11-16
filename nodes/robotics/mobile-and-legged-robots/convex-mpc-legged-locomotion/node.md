---
tag: 01NY1Z
kind: algorithm
slug: convex-mpc-legged-locomotion
name: Convex MPC for legged locomotion
aliases:
- convex model predictive control of quadrupeds
area: robotics/mobile-and-legged-robots
level: research
summary: "Plans the ground reaction forces of a legged robot over a short horizon as one QP per control step, with a single rigid body model made linear by small roll and pitch and the reference yaw."
model: real-ram
complexity:
  vars: {n: "the number of steps in the horizon", c: "the number of feet in contact per step"}
  time: {build: O(n^3 c^2), per_iteration: O(n^3 c^3)}
  space: {extra: O(n^2 c^2)}
properties: {deterministic: true, online: true, exact: false}
history:
  year: 2018
  people: [Jared Di Carlo, Patrick M. Wensing, Benjamin Katz, Gerardo Bledt, Sangbae Kim]
  note: Di Carlo and colleagues ran the controller on the MIT Cheetah 3 quadruped for standing, trotting, bounding, pronking and galloping, with one convex QP per control step.
prereqs: [model-predictive-control, quadratic-programming, centroidal-dynamics, friction-cone]
see_also: [linear-mpc, polyhedral-friction-cone, contact-wrench-cone, hybrid-mpc, whole-body-control, interior-point-method, zmp-preview-control, raibert-hopping-controller]
sources:
  - paper: doi:10.1109/IROS.2018.8594448
    title: Jared Di Carlo, Patrick M. Wensing, Benjamin Katz, Gerardo Bledt and Sangbae Kim, Dynamic locomotion in the MIT Cheetah 3 through convex model-predictive control, IEEE/RSJ International Conference on Intelligent Robots and Systems, 2018
    locator: pages 1 to 9
  - paper: doi:10.1109/ICHR.2006.321375
    title: Pierre-Brice Wieber, Trajectory free linear model predictive control for stable walking in the presence of strong perturbations, IEEE-RAS International Conference on Humanoid Robots, 2006
    locator: pages 137 to 142
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 16 (quadratic programming, interior point methods for QP)
---

Convex MPC for legged locomotion is a model predictive controller that plans the forces that the feet of a legged robot push on the ground over the next fraction of a second. It treats the robot as one rigid body, fixes the timing of the steps and the foot positions in advance, and assumes small roll and pitch, so that the predicted motion is linear in the forces. Each control step is then one convex [quadratic program](/quadratic-programming/) with friction and force limits, which a solver finds to optimality in a millisecond or less. Di Carlo et al. (2018) used it for many gaits of the MIT Cheetah 3. The QP is solved exactly, but the closed loop has no stability proof.

## In plain words

A running quadruped touches the ground with two or four feet at a time, for a short time. In that time, the feet must push so that the body goes where it should and does not tip over. A foot can only push, not pull, and it slips if it pushes too much sideways.

The controller looks a short time ahead, for example half a second. It knows which feet will be on the ground and where. It treats the whole robot as one block and asks: which pushes, at each foot and each moment, keep the block closest to the plan? With the simplifications above, this question is a standard optimization problem with one best answer, and a computer finds it fast. The robot uses the first pushes, then asks the question again a few hundredths of a second later.

## The problem

The robot has mass $m$ and body inertia $I_B$ about its center of mass. Gravity is $g = 9.81$ m/s$^2$ along $-z$ in the world frame {s}. The state is

$$x = (\Theta, p, \omega, v, g) \in \mathbb{R}^{13},$$

with roll, pitch and yaw $\Theta$ (with $R = R_z(\psi) R_y(\theta) R_x(\phi)$), the position $p$ and velocity $v$ of the center of mass, and the angular velocity $\omega$ in the world frame. The constant $g$ is a state so that gravity enters the model linearly. Foot $i$ is at $r_i$ relative to the center of mass and pushes with the force $f_i$. The full single rigid body equations are

$$m \dot v = \sum_i f_i - m g e_z, \qquad \frac{d}{dt}(I_w \omega) = \sum_i r_i \times f_i.$$

The method makes three approximations. It assumes small roll and pitch, so that $\dot\Theta \approx R_z(\psi)^T \omega$ and $I_w \approx R_z(\psi) I_B R_z(\psi)^T$. It drops the gyroscopic term $\omega \times I_w \omega$. It takes the yaw $\psi_k$, the contact sequence and the foot positions $r_{i,k}$ from the reference trajectory, not from the solution. Then step $k$ of the horizon has the linear model $\dot x = A(\psi_k) x + B(\psi_k, r_{1,k}, \dots) u$, where $u$ stacks the forces of the feet in contact. The model is linear time-varying, not linearized about a fixed yaw.

Given the current state $x_0$, a reference $Y_1, \dots, Y_n$ for the next $n$ steps of length $\Delta t$, diagonal weights $L$ and $\alpha > 0$, the friction coefficient $\mu$ and the force limits $f_{\min} \le f_z \le f_{\max}$, the task is

$$\min_{U} \sum_{k=1}^{n} (X_k - Y_k)^T L (X_k - Y_k) + \alpha |U|^2$$

subject to the model, the friction constraints and the force limits, with zero force at the feet in swing.

## The algorithm

```pseudo id=main
CONVEX-MPC(x_0, Y, schedule, footholds, yaw reference)
L1  for k ← 0 to n - 1: A_k, B_k ← discrete model at yaw ψ_k with the feet in contact at step k
L2  Φ, S ← stacked prediction, so that X = Φ x_0 + S U
L3  H_qp ← 2 (Sᵀ L S + α I) ; g_qp ← 2 Sᵀ L (Φ x_0 - Y)
L4  for each step k and each foot i in contact at step k:
        add |f_x| ≤ μ f_z, |f_y| ≤ μ f_z and f_min ≤ f_z ≤ f_max
L5  U* ← argmin ½ Uᵀ H_qp U + g_qpᵀ U subject to the rows of line L4
L6  return the forces of step 0 in U*      ▷ swing feet get zero force
```

Line L1 discretizes with a zero-order hold. The continuous matrix $A$ is nilpotent ($A^3 = 0$), so the hold is exact with three terms of the series. Line L2 is the condensed form: the states are eliminated, and only the forces of the feet in contact are variables. Lines L4 and L5 form a QP whose friction cone is a [polyhedral friction cone](/polyhedral-friction-cone/) with $k = 4$ edges. This pyramid contains the Coulomb cone, so it slightly overestimates the friction; with $\mu / \sqrt 2$ in place of $\mu$ it lies inside the cone. Di Carlo et al. solve the QP with the active-set solver qpOASES. The implementation here uses a dense primal-dual [interior point method](/interior-point-method/).

On the robot, the forces of line L6 are mapped to the joint torques of each stance leg with the transpose of the leg Jacobian, and the swing legs follow a foot trajectory. Foot placement is set by a separate heuristic; Di Carlo et al. use a [Raibert-style](/raibert-hopping-controller/) law with an added term proportional to the speed error.

## Example

The robot has $m = 10$ kg, $I_B = \operatorname{diag}(0.1, 0.25, 0.3)$ kg m$^2$ and four feet in contact at $(\pm 0.2, \pm 0.12, -0.3)$ m from the center of mass. The weights are 20, 20 and 5 on roll, pitch and yaw, 1, 1 and 50 on the position, 0.5 on each angular velocity and 2 on each velocity, with $\alpha = 10^{-6}$, $\mu = 0.6$, $f_{\min} = 0$ and $f_{\max} = 150$ N.

**Standing.** With $x_0$ at the reference and $n = 3$ steps of 0.03 s, the QP gives $f_z = 24.54$ N at each foot and zero tangential force. The weight is $m g / 4 = 24.525$ N per foot; the difference of 0.05 percent is the effect of the force weight $\alpha$ on the plan over the short horizon.

**Push.** The robot starts at the reference height with a sideways velocity of 0.5 m/s and $\omega = (0.5, 0, 0.2)$ rad/s. The MPC runs every 0.05 s with $n = 3$, and the full nonlinear rigid body (with the gyroscopic term, rotation by the exponential map) is integrated at 1 ms with the forces held between solves.

| $t$ (s) | roll (rad) | $p_y$ (m) | $v_y$ (m/s) | $f_z$ left front, right front (N) | $f_y$ left front (N) |
|---|---|---|---|---|---|
| 0.00 | 0.000 | 0.000 | 0.500 | 57.6, 0.0 | -28.0 |
| 0.05 | 0.000 | 0.019 | 0.251 | 43.3, 0.0 | -12.1 |
| 0.10 | -0.020 | 0.028 | 0.130 | 44.8, 0.1 | -12.5 |
| 0.20 | -0.022 | 0.031 | -0.002 | 31.0, 18.2 | 0.0 |
| 1.00 | 0.000 | 0.030 | -0.002 | 30.7, 18.4 | 0.0 |

In the first solve the right feet carry no load: their bounds $f_z \ge 0$ are active, and the left feet push sideways to stop the body. The sideways motion stops in about 0.2 s. The body then rests 3 cm to the left, and the forces split as $(0.12 + 0.03)/0.24 \cdot 49.05 = 30.66$ N on each left foot, which is the static moment balance. The low weight on position and the short horizon make the return to $p_y = 0$ slow.

## Correctness

The proof file shows that the zero-order hold of line L1 is exact because $A^3 = 0$, that the condensed prediction of line L2 is the solution of the discrete model, that the $k = 4$ pyramid contains the Coulomb cone, and that with $\alpha > 0$ the QP of line L5 has a positive definite Hessian. So it has exactly one minimizer, which is characterized by the KKT conditions, and the solver returns it to the tolerance. This is a theorem about the model. The closed loop has no terminal cost or terminal set, and the model ignores roll and pitch in the kinematics, the gyroscopic term and the leg dynamics, so its stability on the robot is a measurement, not a theorem.

## Complexity

With $n$ horizon steps and $c$ feet in contact, the QP has $N = 3 c n$ variables and $6 c n$ inequality rows, in the [real-RAM](/real-ram/) model:

- Lines L1 and L2 take $O(n^2 c)$ operations, because $S$ has $13 n \times 3 c n$ entries and each block is a product of fixed-size matrices.
- Line L3 takes $O(n^3 c^2)$ operations in general. The code skips zero entries and is $O(n^2 c^2)$ per state row with a nonzero weight.
- Each interior point iteration factors an $N \times N$ matrix in $O(N^3) = O(n^3 c^3)$ operations. The friction rows touch only the forces of one foot, so adding them costs $O(N)$.
- The number of iterations is small in practice (about 10 here), but no bound is proved for the predictor-corrector version.

For $n = 10$ and $c = 4$ there are 120 variables. Di Carlo et al. report horizons of up to 0.5 s solved to optimality in under 1 ms, with the MPC running at 20 to 30 Hz.

## Properties

- **Convex and global.** Each step is a strictly convex QP, so the solver finds the global optimum of the model problem, with no initial guess and no local minima.
- **Fixed contact plan.** The contact sequence and foot positions are inputs. The method does not choose when or where to step; that is a [hybrid MPC](/hybrid-mpc/) or [footstep planning](/footstep-planning/) problem.
- **Single rigid body.** The legs are taken as massless. This works for robots with light legs, such as the Cheetah 3 and smaller quadrupeds, and less well for humanoids with heavy limbs.
- **Approximate friction.** The pyramid with $k = 4$ edges is an outer approximation of the Coulomb cone, so a planned force can slip by up to a factor $\sqrt 2$ in tangential size unless $\mu$ is reduced.

## Variants and improvements

- **Sparse form.** Keep the states as variables with the model as equality constraints. The QP is larger but sparse and banded in time, and structure-exploiting solvers scale linearly in $n$.
- **MPC plus whole-body control.** The MPC runs at about 30 Hz and a [whole-body controller](/whole-body-control/) at 500 Hz or more tracks its forces with the full robot model.
- **Full contact wrench.** For feet with area, the force at a point is replaced by a [contact wrench cone](/contact-wrench-cone/) constraint, as in humanoid centroidal MPC.
- **Nonlinear and centroidal MPC.** Without the small-angle assumptions, the problem is a nonlinear program, solved by sequential QP or by DDP-type methods, on the [centroidal dynamics](/centroidal-dynamics/) or the full model.

## When to use it

Use it for quadrupeds and other robots with light legs, for gaits with a fixed timing such as trot, pace, bound and gallop, when the body roll and pitch stay moderate. It is a good default when a fast, robust force planner is needed and the contact plan comes from another layer. For walking humanoids with heavy legs, use a centroidal or whole-body model; for choosing the contact sequence itself, use [hybrid MPC](/hybrid-mpc/) or [contact-implicit trajectory optimization](/contact-implicit-trajectory-optimization/).

## Pitfalls

- **Large roll or pitch.** The relation $\dot\Theta = R_z^T \omega$ is wrong for large roll and pitch, and the model degrades on steep slopes or in flips.
- **Infeasible QP.** With tight force limits and a large disturbance, the constraints can have no solution. Production code softens some constraints or falls back to a safe policy.
- **Swing feet in the plan.** A foot that is planned to be in contact but is not, because it lands late, gets force that it cannot apply. Contact detection must update the schedule.
- **Weight on the force.** With $\alpha = 0$, the Hessian is only semidefinite when the tracking cost does not fix all forces, and the solution is not unique; the solver may then jump between solutions from one step to the next.
- **The friction model.** Using $\mu$ in the pyramid lets the planned force exceed the true cone at the corners; slippage on low-friction ground often comes from this.

## Implementations

## History

Linear MPC for walking with the ZMP as a constraint goes back to Wieber (2006). For quadrupeds, Di Carlo, Wensing, Katz, Bledt and Kim presented the convex MPC of the MIT Cheetah 3 at IROS 2018. Their key steps were the single rigid body model with the yaw taken from the reference, which keeps the problem a QP, and the condensed form solved by an active-set solver. The method is now a common baseline for quadruped control.

## References
