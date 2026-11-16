---
tag: CQQDWX
kind: algorithm
slug: zmp-preview-control
name: ZMP preview control
aliases:
- Kajita preview control
area: robotics/mobile-and-legged-robots
level: advanced
summary: "Kajita's walking pattern generator: an LQ preview controller on the cart-table model that moves the center of mass so that the ZMP follows a planned reference known for the next N steps."
model: real-ram
complexity:
  vars: {N: "the number of preview steps; the state has 4 entries per horizontal axis"}
  time: {gains: O(N), per_step: O(N)}
  space: {extra: O(N)}
properties: {deterministic: true, online: true, exact: false}
history:
  year: 2003
  people: [Shuuji Kajita, Fumio Kanehiro, Kenji Kaneko, Kiyoshi Fujiwara, Kensuke Harada, Kazuhito Yokoi, Hirohisa Hirukawa]
  note: Kajita and colleagues applied the discrete-time preview control of Katayama et al. (1985) to the cart-table model to generate biped walking patterns.
prereqs: [zero-moment-point, linear-inverted-pendulum-model, lqr-problem, discrete-algebraic-riccati-equation]
see_also: [capture-point, footstep-planning, linear-mpc, model-predictive-control, infinite-horizon-lqr, centroidal-dynamics, whole-body-control, support-polygon]
sources:
  - paper: doi:10.1109/ROBOT.2003.1241826
    title: Shuuji Kajita, Fumio Kanehiro, Kenji Kaneko, Kiyoshi Fujiwara, Kensuke Harada, Kazuhito Yokoi and Hirohisa Hirukawa, Biped walking pattern generation by using preview control of zero-moment point, IEEE International Conference on Robotics and Automation, 2003
    locator: pages 1620 to 1626
  - paper: doi:10.1080/0020718508961156
    title: Tohru Katayama, Takahira Ohki, Toshio Inoue and Tomoyuki Kato, Design of an optimal controller for a discrete-time system subject to previewable demand, International Journal of Control 41(3), 1985
    locator: pages 677 to 699
  - book: isbn:9783642545351
    title: Shuuji Kajita, Hirohisa Hirukawa, Kensuke Harada and Kazuhito Yokoi, Introduction to Humanoid Robotics, Springer Tracts in Advanced Robotics 101, Springer, 2014
    locator: Chapter 4 (biped walking)
  - paper: doi:10.1109/ICHR.2006.321375
    title: Pierre-Brice Wieber, Trajectory free linear model predictive control for stable walking in the presence of strong perturbations, IEEE-RAS International Conference on Humanoid Robots, 2006
    locator: pages 137 to 142
---

ZMP preview control computes a center of mass (CoM) motion for a walking robot so that its [zero moment point](/zero-moment-point/) (ZMP) follows a reference that the footstep plan fixes in advance. It models the robot as a cart on a table, which is the [linear inverted pendulum](/linear-inverted-pendulum-model/) with the CoM acceleration as a state, and it solves a discrete-time linear quadratic problem in which the next $N$ reference values are known. The result is a fixed linear law: a state feedback plus a weighted sum of the future reference changes. It is optimal for the cart-table model only, and it is not a stability proof for the robot that executes the motion.

## In plain words

To walk, a robot must keep its ZMP inside the foot that carries it. The footstep plan says where each foot will be and when, so the wanted ZMP path is known for the next second or two.

The CoM cannot simply copy this path. To move the ZMP to the next foot, the body must already be moving toward that foot, because the ZMP sits behind the body when the body speeds up. So the body has to start moving before the step.

Preview control looks at the planned ZMP path for a fixed time ahead and chooses the body motion that keeps the ZMP close to the plan with small, smooth pushes. The weights on the future plan are computed once. While the robot walks, each control step needs only a sum over the window ahead.

## The problem

Take one horizontal axis; the other axis is the same problem with its own reference. The CoM moves at the constant height $z_c$ above flat ground, $g = 9.81$ m/s$^2$, and $h = z_c / g$. The state is $x = (c, \dot c, \ddot c)$ for the CoM position $c$, and the input is the jerk $u = \dddot c$. The ZMP of this cart-table model is

$$p = c - h \ddot c,$$

which is the LIPM equation $\ddot c = (g / z_c)(c - p)$ solved for $p$. With the sampling period $T$ and a jerk held constant over each period, the exact discrete model is

$$x_{k+1} = A x_k + B u_k, \quad p_k = C x_k, \quad A = \begin{bmatrix} 1 & T & T^2/2 \\ 0 & 1 & T \\ 0 & 0 & 1 \end{bmatrix}, \quad B = \begin{bmatrix} T^3/6 \\ T^2/2 \\ T \end{bmatrix}, \quad C = \begin{bmatrix} 1 & 0 & -h \end{bmatrix}.$$

A reference sequence $r_k$ for the ZMP is given, and at step $k$ the values $r_{k+1}, \dots, r_{k+N}$ are known. With the ZMP error $e_k = p_k - r_k$ and the increments $\Delta x_k = x_k - x_{k-1}$ and $\Delta u_k = u_k - u_{k-1}$, the task is to choose $\Delta u_k$ to minimize

$$J = \sum_{i=k}^{\infty} \left( Q_e e_i^2 + \Delta x_i^T Q_x \Delta x_i + R \Delta u_i^2 \right),$$

with $Q_e > 0$, $Q_x \succeq 0$ and $R > 0$. This is the form of Katayama et al. (1985) that Kajita et al. (2003) used. Because the cost is on the increments, the controller has integral action on the ZMP error.

## The algorithm

The incremental state $X_k = (e_k, \Delta x_k)$ obeys $X_{k+1} = \tilde A X_k + \tilde B \Delta u_k - e_1 (r_{k+1} - r_k)$, where $\tilde A = \begin{bmatrix} 1 & CA \\ 0 & A \end{bmatrix}$, $\tilde B = (CB, B)$ and $e_1 = (1, 0, 0, 0)$. The gains are computed once, offline.

```pseudo id=main
PREVIEW-GAINS(T, z_c, N, Q_e, Q_x, R)
L1  A, B, C ← cart-table model with period T and height z_c
L2  Ã, B̃ ← incremental model of (A, B, C)
L3  P ← stabilizing solution of the DARE for (Ã, B̃, diag(Q_e, Q_x), R)
L4  s ← R + B̃ᵀ P B̃ ; K ← s⁻¹ B̃ᵀ P Ã
L5  A_c ← Ã - B̃ K
L6  v ← P e_1
L7  for j ← 1 to N
L8      f_j ← s⁻¹ B̃ᵀ v                ▷ weight of the reference change j steps ahead
L9      v ← A_cᵀ v
    return K, f_1, ..., f_N

PREVIEW-CONTROL(r, x_0)
L10 x_prev ← x_0 ; u ← 0
L11 for k ← 0, 1, 2, ...
L12     e ← C x_k - r_k
L13     Δx ← x_k - x_prev
L14     Δu ← -K (e, Δx) + Σ_{j=1}^{N} f_j (r_{k+j} - r_{k+j-1})
L15     u ← u + Δu
L16     x_prev ← x_k ; x_{k+1} ← A x_k + B u    ▷ on a robot: pass x_{k+1} to the whole-body controller
```

Line L3 solves the [discrete algebraic Riccati equation](/discrete-algebraic-riccati-equation/); value iteration from $P = Q$ converges because the incremental model is controllable and the error is observable. Line L14 is the whole online law. Kajita et al. write it as an integral of the error, a state feedback on $x_k$ and a weighted sum of the future reference values $r_{k+j}$ themselves; that form is the same law after a summation by parts.

On a robot, the CoM trajectory of line L16 is the output. Inverse kinematics or a [whole-body controller](/whole-body-control/) then finds joint motions that realize it, and the real ZMP differs from the model ZMP by the effect of the limbs, which the cart-table model ignores.

## Example

Take $z_c = 0.8$ m, $T = 0.01$ s, $Q_e = 1$, $Q_x = 0$, $R = 10^{-6}$ and a preview of $N = 160$ steps (1.6 s). Lines L1 to L9 give, rounded,

| quantity | value |
|---|---|
| $K$ on $(e, \Delta c, \Delta \dot c, \Delta \ddot c)$ | $(500.3,\ 29441,\ 8810,\ 118.5)$ |
| $f_1, f_2, f_5$ | $500.3,\ 704.3,\ 927.5$ |
| $f_{20}, f_{40}, f_{80}$ | $537.1,\ 266.6,\ 65.7$ |
| $f_{160}$ | $3.99$ |

The first preview weight equals the error gain, the weights peak at $j = 4$ and then decay, and after 1.6 s they are below 1 percent of the peak. This is why a preview of about 1.5 s is enough for these weights; a longer window adds almost nothing.

Now let the robot stand at $c = 0$, and let the reference step from 0 to 0.1 m at $t = 2$ s ($k = 200$). The closed loop of lines L10 to L16 gives

| $t$ (s) | $c$ (m) | $\dot c$ (m/s) | $p$ (m) |
|---|---|---|---|
| 1.0 | 0.0014 | 0.0056 | -0.0001 |
| 1.5 | 0.0088 | 0.0310 | 0.0000 |
| 1.9 | 0.0358 | 0.1256 | 0.0001 |
| 2.0 | 0.0508 | 0.1699 | 0.0673 |
| 2.5 | 0.0915 | 0.0299 | 0.1000 |
| 4.0 | 0.1000 | 0.0002 | 0.1000 |

The CoM starts to move about a second before the step and is half way at the step time, while the ZMP stays near 0. Just before the step the ZMP moves 3.1 mm the wrong way, to $-0.0031$ m at $t = 1.96$ s, which is the non-minimum phase behavior of the cart-table model. With a preview of only 0.2 s ($N = 20$), the same step pushes the ZMP to $-0.0995$ m before the step: the controller sees the step too late and must throw the ZMP far back to start the CoM.

## Correctness

The proof file shows that the incremental model is controllable and the ZMP error observable for every $T > 0$ and $z_c > 0$, so the Riccati equation has a stabilizing solution and $A_c$ is Schur stable. It then shows by dynamic programming that, when the reference does not change after step $k + N$, line L14 gives the unique optimal first input of the problem, with $f_j = s^{-1} \tilde B^T (A_c^T)^{j-1} P e_1$. If the reference is constant from some step on, the ZMP error goes to zero. All of this is a theorem about the cart-table model. It is not a proof that the robot stays balanced; that depends on how well the whole-body motion realizes the CoM path and on the ZMP reference staying inside the [support polygon](/support-polygon/).

## Complexity

In the [real-RAM](/real-ram/) model, with $N$ preview steps and the 4-entry incremental state of one axis:

- Lines L4 to L9 take $O(N)$ operations, because each pass is a product of a $4 \times 4$ matrix and a vector.
- Line L3 by value iteration takes a number of iterations that depends on the decay rate of $A_c$, each of constant cost; a Schur method on the $8 \times 8$ symplectic pencil takes constant time.
- Each control step costs $O(N)$ for the sum in line L14, and the memory is $O(N)$ for the weights and the reference window.

## Properties

- **Optimal only for the model.** The law minimizes the quadratic cost for the cart-table model with a known reference. It does not enforce the support polygon, joint limits or torque limits.
- **Integral action.** The cost on increments puts the ZMP error through an integrator, so a constant offset of the ZMP is removed.
- **Linear and time invariant.** The gains do not depend on the reference, so they are computed once for a given $z_c$ and $T$.
- **Constant height.** The model needs a constant CoM height and zero change of angular momentum about the CoM; both are approximations on a real robot.

## Variants and improvements

- **Two-stage controller.** Kajita et al. (2003) run the preview controller a second time on the error between the model ZMP and the ZMP of the multibody model, to correct the effect of the limbs.
- **Model predictive control.** Wieber (2006) solves a finite-horizon quadratic program at each step and adds the ZMP constraint as a hard inequality, which gives better behavior under strong pushes. See [linear MPC](/linear-mpc/).
- **Divergent component of motion.** Controllers based on the [capture point](/capture-point/) plan only the unstable part of the LIPM and do not need a long preview window.
- **Varying height.** Without the constant height, the ZMP is a nonlinear function of the CoM motion, and the problem is usually solved as a nonlinear or sequential convex program.

## When to use it

Use it to generate CoM paths for walking on flat ground when the footstep timing and positions are fixed for the next second or more. It is cheap and robust as a pattern generator. If the ZMP must satisfy hard limits, or if the plan must change from step to step in reaction to pushes, a [model predictive controller](/model-predictive-control/) or a capture point controller is a better fit. For running, jumping or rough terrain, the LIPM assumptions fail, and [centroidal dynamics](/centroidal-dynamics/) models are used.

## Pitfalls

- **Short preview.** With a window much shorter than the time constant of the weights, the ZMP error before each step is large, as in the example above.
- **Reference outside the foot.** The controller tracks whatever reference it gets. A ZMP reference that leaves the support polygon gives a CoM path that the robot cannot realize.
- **Model ZMP versus real ZMP.** The limbs have mass, so the ZMP of the robot differs from the model ZMP. Without the second stage or a whole-body correction, this error is not corrected.
- **Ill-conditioned weights.** Very small $R$ with a small $T$ makes the gains large; a fixed number of Riccati iterations may not converge, so test the convergence.
- **Sign conventions.** Some texts write the law in terms of $r_{k+j}$, others in terms of $r_{k+j} - r_{k+j-1}$, and the signs of the gains differ. Mixing the two forms gives a controller that tracks the wrong reference.

## Implementations

## History

Katayama, Ohki, Inoue and Kato published the discrete-time LQ preview controller with integral action in 1985. Kajita and colleagues used it in 2003 on the cart-table model, which they obtained by writing the 3D linear inverted pendulum of 2001 with the CoM acceleration as a state, and used it to generate walking patterns for a humanoid. Wieber's 2006 linear MPC replaced the infinite-horizon law by a constrained quadratic program, and later work moved to the divergent component of motion and to centroidal models.

## References
