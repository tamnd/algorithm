---
tag: FDGDFJ
kind: technique
slug: hybrid-zero-dynamics
name: Hybrid zero dynamics
aliases:
- HZD
area: robotics/mobile-and-legged-robots
level: research
summary: "Designs feedback for underactuated bipeds by virtual constraints whose zero dynamics survive the foot impacts, so the stability of a gait reduces to a one dimensional return map."
prereqs: [zero-dynamics, input-output-linearization, relative-degree]
see_also: [zero-dynamics, passive-dynamic-walking, limit-cycle, hybrid-automata, bezier-curve, control-lyapunov-function, zeno-behavior, spring-loaded-inverted-pendulum]
sources:
  - paper: doi:10.1109/9.898695
    title: Jessy W. Grizzle, Gabriel Abba and Franck Plestan, Asymptotically stable walking for biped robots, analysis via systems with impulse effects, IEEE Transactions on Automatic Control 46(1), 2001
    locator: pages 51 to 64
  - paper: doi:10.1109/TAC.2002.806653
    title: Eric R. Westervelt, Jessy W. Grizzle and Daniel E. Koditschek, Hybrid zero dynamics of planar biped walkers, IEEE Transactions on Automatic Control 48(1), 2003
    locator: pages 42 to 56
  - book: isbn:9781420053722
    title: Eric R. Westervelt, Jessy W. Grizzle, Christine Chevallereau, Jun Ho Choi and Benjamin Morris, Feedback Control of Dynamic Bipedal Robot Locomotion, CRC Press, 2007
    locator: Chapter 4 (periodic orbits and Poincaré return maps), Chapter 5 (zero dynamics of bipedal locomotion), Chapter 6 (within-stride controllers) and Chapter 7 (event-based controllers)
---

Hybrid zero dynamics (HZD) is a method to design and analyze walking controllers for bipeds that have one degree of underactuation, such as robots with point feet. The controller makes the actuated joints follow functions of a single phase variable, called virtual constraints. If the impact at each footfall maps the set where the constraints hold into itself, that set carries a two dimensional hybrid system, the hybrid zero dynamics, and a periodic gait of the full robot is stable if a one dimensional map on this set has a stable fixed point and the constraints are enforced fast enough. Grizzle, Abba and Plestan (2001) gave the Poincaré analysis for walkers with impacts, and Westervelt, Grizzle and Koditschek (2003) formulated the hybrid zero dynamics. It extends the [zero dynamics](/zero-dynamics/) of nonlinear control to systems with impacts.

## In plain words

A robot with point feet cannot stand still. It can only stay up by walking, like a person on stilts. Most of its joints have motors, but the angle at which it leans over its foot has none.

The method picks one quantity that always moves forward during a step, for example the lean of the stance leg. Then it tells each motor to hold its joint at a fixed function of that quantity, like a gear that ties each joint to the lean. The robot then moves like a simple machine with one free part.

The designer also makes sure that the foot impact does not break these ties. Then each step of the robot is described by one number, a measure of its speed. If this number settles to the same value step after step, the gait is stable.

## When it applies

- The robot is a chain of rigid links with a Lagrangian model, and it has $N$ degrees of freedom in single support and $N - 1$ actuators: underactuation of one degree. Point feet and planar models are the base case.
- The gait has single support phases separated by impacts; double support is instantaneous. The impact is rigid and inelastic, and after it the legs swap roles.
- There is a phase variable $\theta(q)$ that is strictly monotone during a step, for example the angle of the line from the stance foot to the hip.
- The outputs that define the virtual constraints have [relative degree](/relative-degree/) 2 on the region of interest.
- The ground reaction force stays in the friction cone and the normal force stays positive. These are checked after the design; the method does not ensure them.

## The template

**The model.** The swing phase is $\dot x = f(x) + g(x) u$ with $x = (q, \dot q)$, derived from the [Euler-Lagrange equation](/euler-lagrange-equation/). The impact surface $S$ is the set where the swing foot touches the ground while it moves down. The impact map $\Delta$ gives the state just after the impact, including the swap of the legs. The closed loop is a system with impulse effects, a hybrid system as in [hybrid automata](/hybrid-automata/).

**Virtual constraints.** Choose the output

$$y = h(q) = q_a - h_d(\theta(q)),$$

where $q_a$ are the $N - 1$ actuated joints and $h_d$ gives their wanted values as functions of the phase. In practice $h_d$ is a [Bézier polynomial](/bezier-curve/) in the normalized phase, with a coefficient matrix $\alpha$.

**The zero dynamics manifold.** With relative degree 2, the set

$$Z = \{x : h(q) = 0, \ L_f h(x) = 0\}$$

is a smooth surface of dimension 2. The feedback of [input-output linearization](/input-output-linearization/) that makes $\ddot y = 0$ on $Z$ keeps the swing motion on $Z$. On $Z$, the state is $(\theta, \sigma)$, where $\sigma$ is the angular momentum about the stance foot, and the dynamics are $\dot \theta = \kappa_1(\theta) \sigma$ and $\dot \sigma = \kappa_2(\theta)$, where $\kappa_2$ comes from gravity.

**Hybrid invariance.** Require

$$\Delta(S \cap Z) \subset Z.$$

Then every impact from $Z$ lands on $Z$, and the restriction of the closed loop to $Z$ is the **hybrid zero dynamics**. The condition is linear in the first two and the last two columns of the Bézier coefficients $\alpha$, because a Bézier polynomial takes its end values and end slopes from them.

**The restricted Poincaré map.** Let $\zeta = \frac12 \sigma^2$, measured just before an impact. Integrating the zero dynamics over one step gives

$$\zeta_{k+1} = \delta_{\text{zero}}^2\, \zeta_k - V_{\text{zero}},$$

where $\delta_{\text{zero}}$ is the fraction of $\sigma$ that the impact keeps and $V_{\text{zero}}$ comes from the work of gravity over the step. Both are numbers computed from the model and $\alpha$. If $0 < \delta_{\text{zero}}^2 < 1$ and the fixed point

$$\zeta^* = \frac{-V_{\text{zero}}}{1 - \delta_{\text{zero}}^2}$$

lies in the domain where $\theta$ keeps moving forward through the whole step, then $\zeta^*$ is an exponentially stable fixed point of the restricted map.

**The theorem.** Westervelt, Grizzle and Koditschek (2003) prove that an exponentially stable periodic orbit of the hybrid zero dynamics is an exponentially stable periodic orbit of the full closed loop, when the controller drives $y$ to zero fast enough, for example in finite time within each step. So the stability test of the full robot reduces to the scalar map above.

**The design loop.**

1. Build the swing model, the impact map and the guard.
2. Choose the phase variable and the degree of the Bézier polynomials.
3. Optimize $\alpha$ for a cost such as energy per distance, with hybrid invariance as an equality constraint, and with limits on the torques, the friction, the normal force and the swing foot clearance.
4. Check $\delta_{\text{zero}}^2 < 1$ and the domain condition for the fixed point.
5. Implement the output controller and check the full stride map numerically, as in [passive dynamic walking](/passive-dynamic-walking/).

## Classic examples

**Planar five-link bipeds.** A planar biped with a torso, two thighs, two shanks and point feet has five degrees of freedom in single support and four actuators. HZD gives it a family of walking gaits, each with its own $\alpha$, and a controller can switch between them to change speed.

**The compass gait with a torso.** A three-link model, with two legs and a torso, is small enough to compute $\delta_{\text{zero}}$ and $V_{\text{zero}}$ with little work. On flat ground the impact removes energy at each step, so the actuators must supply it; with the virtual constraints, they do so through the torso and the legs.

**Running.** With a flight phase, the hybrid model has two continuous phases and two transitions. The same reduction applies, with invariance required at both transitions.

## Variations

- **Event-based control.** If hybrid invariance holds only for nominal parameters, the controller updates some Bézier coefficients once per step, at the impact, to restore it or to change the speed. The book calls these event-based controllers.
- **Control Lyapunov functions.** Instead of finite-time convergence, the output dynamics can be stabilized fast enough by a [control Lyapunov function](/control-lyapunov-function/), often solved as a quadratic program at each control step with the torque limits as constraints.
- **Feet and full actuation.** With feet and ankle torques, the robot is fully actuated in some phases. Multi-domain HZD treats a sequence of contact phases, each with its own outputs.
- **Three dimensional robots.** The same reduction works with more phase variables and more care with the lateral balance. The zero dynamics are then of higher dimension, and the restricted map is no longer scalar.

## Pitfalls

- **The reduction assumes exact tracking.** The proof needs the outputs to converge fast enough within each step. A slow PD controller, actuator saturation or model errors can break this, and then the stability of the reduced map says nothing about the robot.
- **A monotone phase variable.** If $\dot \theta$ goes to zero, the robot stops in mid step and falls back; the domain condition on $\zeta^*$ excludes this for the nominal gait, but not after a large disturbance.
- **Contact conditions are separate.** The method does not keep the normal force positive or the foot from slipping. These must be constraints in the optimization of $\alpha$ and must be checked on the final gait.
- **A local result.** Exponential stability of the orbit says nothing about how large a push the robot can survive. The basin is found by simulation.
- **Impact timing.** A model with an instant, inelastic impact can differ from a real foot that bounces or rolls. Bouncing and repeated impacts in the model are [Zeno behavior](/zeno-behavior/).

## Exercises

1. Let $\delta_{\text{zero}}^2 = 0.8$ and $V_{\text{zero}} = -2$ in some units. Find the fixed point and iterate the map from $\zeta_0 = 5$. *Answer:* $\zeta^* = 2 / 0.2 = 10$. The iterates are $6$, $6.8$, $7.44$, $7.952$ and $8.3616$, and the error shrinks by the factor $0.8$ at each step.
2. Show that if $\delta_{\text{zero}}^2 \ge 1$, the restricted map has no exponentially stable fixed point. What does this mean in terms of energy at the impact?
3. Show that a Bézier polynomial $b(s) = \sum_{k=0}^{M} \alpha_k \binom{M}{k} s^k (1 - s)^{M - k}$ has $b(0) = \alpha_0$, $b(1) = \alpha_M$, $b'(0) = M (\alpha_1 - \alpha_0)$ and $b'(1) = M (\alpha_M - \alpha_{M-1})$. Use this to explain why the hybrid invariance condition fixes only four columns of $\alpha$.
4. For the zero dynamics $\dot \theta = \kappa_1(\theta) \sigma$ and $\dot \sigma = \kappa_2(\theta)$, show that $\zeta = \frac12 \sigma^2$ satisfies $d\zeta / d\theta = \kappa_2(\theta) / \kappa_1(\theta)$, and so changes by a fixed amount over a step that does not depend on $\zeta$.

## References
