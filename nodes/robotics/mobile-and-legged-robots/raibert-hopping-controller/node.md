---
tag: V4NCCQ
kind: algorithm
slug: raibert-hopping-controller
name: Raibert hopping controller
aliases:
- Raibert three-part controller
area: robotics/mobile-and-legged-robots
level: advanced
summary: "Controls a hopping robot by three separate heuristic laws: a fixed leg thrust for hop height, foot placement for forward speed, and hip torque in stance for body attitude."
model: real-ram
complexity:
  vars: {s: "the fixed number of state variables of the hopper; the bounds are for one control step"}
  time: {per_step: O(1)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, exact: false}
history:
  year: 1984
  people: [Marc H. Raibert, H. Benjamin Brown, Michael Chepponis]
  note: Raibert and his colleagues balanced a planar and then a three-dimensional one-legged hopping machine with the three-part controller, and generalized it to bipeds and quadrupeds.
prereqs: [spring-loaded-inverted-pendulum, pid-controller]
see_also: [capture-point, linear-inverted-pendulum-model, passive-dynamic-walking, limit-cycle, hybrid-automata, convex-mpc-legged-locomotion, zero-moment-point, support-polygon]
sources:
  - book: isbn:9780262181174
    title: Marc H. Raibert, Legged Robots That Balance, MIT Press, 1986
    locator: "Chapter 2 (hopping on one leg in the plane) and Chapter 3 (hopping in three dimensions)"
  - paper: doi:10.1115/1.3149668
    title: Marc H. Raibert and H. Benjamin Brown, Experiments in balance with a 2D one-legged hopping machine, Journal of Dynamic Systems, Measurement, and Control 106(1), 1984
    locator: pages 75 to 81
  - paper: doi:10.1177/027836498400300207
    title: Marc H. Raibert, H. Benjamin Brown and Michael Chepponis, Experiments in balance with a 3D one-legged hopping machine, The International Journal of Robotics Research 3(2), 1984
    locator: pages 75 to 92
---

The Raibert hopping controller balances a one-legged robot that runs by hopping. It splits the task into three parts that act at different times of the hop cycle: a fixed thrust of the leg in stance sets the hop height, the position of the foot at touchdown sets the forward speed, and the hip torque in stance keeps the body level. Each part is a simple feedback law, and the three are tuned as if they did not interact. The controller is a heuristic: it works well on real machines, but there is no proof that the closed loop converges, and the speed law has a known bias.

## In plain words

A pogo stick rider stays up by doing three things. To hop higher, they push harder on the stick when it starts to spring back. To go faster or slower, they put the stick down behind or ahead of the body. To keep the body upright, they push the body against the stick while it is on the ground, because only then can the stick push back.

Raibert's controller does these three things with three small rules. The foot rule is the clever one. If the foot lands at a certain neutral spot, the body leaves the ground with the same speed it had when it landed. The rule estimates that spot from the speed and the time on the ground, and then moves the foot further ahead to slow down or further back to speed up.

## The problem

The robot is a body with mass $m$ and pitch inertia $I$, with the hip at its center of mass, and one telescoping leg. The leg is a spring of stiffness $k$ and rest length $\ell_r$, with damping $b$. An actuator can change $\ell_r$ in stance, and a hip actuator applies a torque $\tau$ between the body and the leg. The leg mass is small, so in flight the hip can swing the leg to any angle $\theta$ from the vertical without moving the body. The motion is in the vertical $x z$ plane, with gravity $g = 9.81$ m/s$^2$ along $-z$ and the body pitch $\phi$.

The robot runs through a cycle of flight and stance, which makes it a hybrid system (see [hybrid automata](/hybrid-automata/)). In stance the foot is pinned and the body moves like a [spring-loaded inverted pendulum](/spring-loaded-inverted-pendulum/) with a hip torque. The task is to reach a wanted forward speed $\dot x_d$ and a steady hop height, with the pitch $\phi$ near $\phi_d$.

## The algorithm

The controller reads the phase (flight or stance), the body state and the duration $T_s$ of the last stance.

```pseudo id=main
RAIBERT-CONTROL(phase, ẋ, φ, φ̇, T_s)
L1  if phase = flight
L2      x_f ← ẋ T_s / 2 + k_ẋ (ẋ - ẋ_d)      ▷ foot position ahead of the hip
L3      θ ← arcsin(x_f / ℓ_0) ; swing the leg to θ before touchdown
L4  else                                     ▷ stance
L5      if the leg has started to lengthen
L6          ℓ_r ← ℓ_0 + δ                    ▷ thrust
L7      else ℓ_r ← ℓ_0
L8      τ ← -k_p (φ - φ_d) - k_v φ̇           ▷ hip torque on the body
L9  at lift-off, T_s ← length of the stance that just ended
```

**Height (lines L5 to L7).** The leg actuator makes the leg longer by a fixed amount $\delta$ during the second half of stance. This puts the same energy into each hop, and friction and damping take energy out. The height settles where they balance. A feedback that changes $\delta$ from the error of the apex height is a common addition.

**Speed (lines L2 and L3).** In stance the hip moves forward by about $\dot x T_s$. If the foot is in the middle of that path, the stance is symmetric and the body leaves with the speed it had at touchdown. So $\dot x T_s / 2$ is an estimate of this neutral point. A foot ahead of it slows the body, and a foot behind it speeds the body up. The term $k_{\dot x}(\dot x - \dot x_d)$ moves the foot by an amount proportional to the speed error.

**Attitude (line L8).** In flight a hip torque would only swing the leg. In stance the foot is on the ground, so a hip torque turns the body. A PD law on the pitch keeps the body level.

## Example

The model has $m = 10$ kg, $I = 0.5$ kg m$^2$, $k = 4000$ N/m, $\ell_0 = 0.5$ m and $b = 20$ N s/m. The gains are $\delta = 0.02$ m, $k_{\dot x} = 0.03$ s, $k_p = 800$ N m/rad, $k_v = 60$ N m s/rad and $\dot x_d = 0$. The hopper starts at the apex $z = 0.7$ m with $\dot x = 0.5$ m/s and $\phi = 0.2$ rad. Stance is integrated with RK4 at $dt = 10^{-3}$ s, and flight is solved exactly.

Before the first hop there is no measured stance time, so the controller uses $T_s = \pi \sqrt{m / k} = 0.1571$ s, half the period of the spring. Line L2 gives $x_f = 0.5 \cdot 0.1571 / 2 + 0.03 \cdot 0.5 = 0.0543$ m, and line L3 gives $\theta = 0.1088$ rad. The hops then go as follows; the values are at the start of each flight, and $\phi$ is at touchdown.

| hop | $\dot x$ (m/s) | $\phi$ (rad) | apex $z$ (m) | $\theta$ (rad) | stance time (s) |
|---|---|---|---|---|---|
| 1 | 0.5000 | 0.2000 | 0.7000 | 0.1088 | 0.1758 |
| 2 | 0.0107 | -0.0882 | 0.7283 | 0.0025 | 0.1752 |
| 3 | 0.1550 | 0.0417 | 0.7408 | 0.0365 | 0.1747 |
| 4 | -0.0468 | -0.0204 | 0.7537 | -0.0110 | 0.1743 |
| 8 | -0.0043 | -0.0015 | 0.7854 | -0.0010 | 0.1731 |

The first stance stops the robot almost at once. On the second hop the pitch is $-0.088$ rad, and the hip torque that corrects it also pushes the body forward, so the speed jumps to 0.155 m/s. This is the coupling between the attitude and the speed loops. After that, speed and pitch shrink by about half each hop with alternating sign, and the apex rises toward the height where the thrust and the damper balance (about 0.81 m for this model).

## Correctness

There is no convergence proof for the closed loop, and the controller is a heuristic. The proof file shows the facts that the three laws use, for the model above. The leg force of a massless leg is the spring force along the leg plus $-\tau / \ell$ across it. Without damping and thrust the energy is conserved, so the thrust is the only source of energy. For a vertical bounce the stance time is $t_s = (2\pi - 2\alpha)/\omega$ with $\omega = \sqrt{k/m}$ and $\alpha = \operatorname{atan2}(v/\omega, m g / k)$; for $v = 1.981$ m/s (a drop from 0.7 m) this is 0.18135 s, longer than $\pi / \omega = 0.1571$ s because the leg leaves at its rest length, not at the spring's equilibrium. A conservative stance in which the hip passes over the foot at the lowest point is symmetric, so the speed out equals the speed in. That is the neutral point. The estimate $\dot x T_s / 2$ is exact only if the forward speed is constant in stance.

## Complexity

Each control step evaluates one of the three laws, so it takes $O(1)$ operations and $O(1)$ memory in the [real-RAM](/real-ram/) model. The cost of a simulation is the cost of the integrator: about $T_s / dt$ RK4 steps per stance, about 175 here.

## Properties

- **Decoupled by design.** Each law acts on one quantity and at one phase. The coupling that remains, mainly between attitude and speed, is treated as a disturbance.
- **Speed offset.** On the model above, with $\dot x_d = 0.5$ m/s the speed settles at 0.32 m/s for $k_{\dot x} = 0.02$ s and at 0.41 m/s for $k_{\dot x} = 0.05$ s. The offset comes from the bias of the neutral point estimate, and a larger gain makes it smaller. This is a measurement on this model.
- **Steady hopping is a limit cycle.** The steady gait is a [limit cycle](/limit-cycle/) of the hybrid system, and its stability is found by simulation or by numerically linearizing the hop-to-hop map.
- **Few parameters.** There are five gains, and each has a direct physical meaning.

## Variants and improvements

- **Three dimensions.** Raibert, Brown and Chepponis (1984) applied the same three laws to the forward and sideways directions of a 3D hopper, with the hip torque controlling pitch and roll.
- **Several legs.** Raibert's virtual leg idea makes legs that move together act as one leg, so the one-legged laws run a biped, a trotting or pacing quadruped, and a bounding quadruped (Raibert 1986).
- **Integral or learned speed terms.** An integral of the speed error, or a lookup table of the neutral point, removes the speed offset.
- **Model-based successors.** The [capture point](/capture-point/) gives a foot placement law with the same structure for the linear inverted pendulum, and [convex MPC](/convex-mpc-legged-locomotion/) replaces the three laws by an optimization over the ground forces.

## When to use it

Use it for running robots with springy legs and short stances, for a first controller on a new hopping or bounding machine, or as a baseline. It needs no model beyond the rough stance time and works with poor state estimates. For walking with long stances and a large foot, ZMP or capture point methods fit better. When the speed must be exact, add an integral term or a model-based foot placement.

## Pitfalls

- **Wrong sign of the speed gain.** A negative $k_{\dot x}$ puts the foot behind the neutral point when the robot is too fast, and the speed grows each hop. In the model above, one hop at $\dot x = 0.5$ m/s with $k_{\dot x} = -0.05$ s gives $\dot x = 0.95$ m/s.
- **Too large a speed gain.** The speed then alternates in sign and grows. With $k_{\dot x} = 0.08$ s, $k_p = 200$, $k_v = 20$ and $\dot x_d = 1$ m/s, the model above does not settle.
- **Hip torque in flight.** A torque in flight turns the leg, not the body; attitude control must wait for the stance.
- **Foot slip.** The attitude law and the foot placement assume the foot does not slip. A large hip torque with a short leg can exceed the friction at the foot.
- **First hop.** With no measured stance time the law uses a guess. A poor guess makes the first hops uneven.

## Implementations

## History

Marc Raibert built the planar one-legged hopper at Carnegie Mellon University in the early 1980s and reported its balance experiments with H. Benjamin Brown in 1984. The same year Raibert, Brown and Chepponis reported a 3D one-legged machine with the same three-part controller. Raibert's 1986 book Legged Robots That Balance extended the method to bipeds and quadrupeds through virtual legs. Later work explained the success of the controller with the spring-loaded inverted pendulum and with the symmetry of the stance phase.

## References
