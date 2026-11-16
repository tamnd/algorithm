---
tag: 46ZAPN
kind: concept
slug: passive-dynamic-walking
name: Passive dynamic walking
aliases: []
area: robotics/mobile-and-legged-robots
level: advanced
summary: "Walking down a shallow slope with no motors and no control, where gravity powers a periodic gait of a leg mechanism; stable gaits are found as fixed points of the stride map."
prereqs: [limit-cycle]
see_also: [hybrid-zero-dynamics, spring-loaded-inverted-pendulum, limit-cycle, hybrid-automata, newton-raphson-method, eigenvalue, linear-inverted-pendulum-model, zero-moment-point]
sources:
  - paper: doi:10.1177/027836499000900206
    title: Tad McGeer, Passive dynamic walking, International Journal of Robotics Research 9(2), 1990
    locator: pages 62 to 82
  - paper: doi:10.1115/1.2798313
    title: Mariano Garcia, Anindya Chatterjee, Andy Ruina and Michael Coleman, The simplest walking model, stability, complexity, and scaling, Journal of Biomechanical Engineering 120(2), 1998
    locator: pages 281 to 288
  - book: isbn:9781420053722
    title: Eric R. Westervelt, Jessy W. Grizzle, Christine Chevallereau, Jun Ho Choi and Benjamin Morris, Feedback Control of Dynamic Bipedal Robot Locomotion, CRC Press, 2007
    locator: Chapter 4 (periodic orbits and Poincaré return maps)
---

Passive dynamic walking is walking by a leg mechanism that has no motors and no controller. Placed on a shallow slope and started with the right push, the mechanism walks down the slope in a steady gait: gravity supplies energy at each step, and the impact of the foot with the ground takes the same amount away. McGeer (1990) built and analyzed such walkers, and showed that a well designed mechanism has a stable gait, to which it returns after small disturbances. The gait is found as a fixed point of the stride map, by a numerical search, and its stability is checked from the eigenvalues of that map.

## In plain words

A toy that walks down a ramp has no motor. Each step, it drops a little height, and this gives it speed. Each time a foot hits the ramp, the hit takes some speed away. When the two are equal, the toy repeats the same step again and again.

If the toy is pushed, the next steps are a bit different, but for a good design they become the same as before. That is a stable gait.

Engineers find such a gait with a computer. They guess the state of the walker at one footfall, simulate one step, and change the guess until the step ends where it began. Then they check if small errors grow or shrink from step to step.

Robots built on this idea use very little energy, because their motors only replace what the impacts take.

## The idea

A walker has a stance phase, governed by smooth equations, and a short impact when the swing foot strikes the ground. At the impact the velocities jump, and the legs exchange roles. Let $x$ be the state just before a footfall. One full step defines the **stride map** $x \mapsto P(x)$: integrate the smooth motion until the next footfall, then apply the impact map. A periodic gait is a fixed point $P(x^*) = x^*$, which is a [limit cycle](/limit-cycle/) of the hybrid system.

The gait is locally stable if every eigenvalue of the Jacobian $DP(x^*)$ has modulus less than 1 (with the eigenvalue that belongs to the direction along the orbit removed, when the map is defined on a full state rather than on a section). For a walker with legs of mass, $P$ has no closed form. So the procedure is numerical:

1. Choose a section, for example the state just after a heel strike, with the coordinates of the section.
2. Compute $P$ by numerical integration of one step, with event detection for the footfall.
3. Solve $P(x) - x = 0$ by the [Newton method](/newton-raphson-method/), with $DP$ found by finite differences or by integration of the variational equations.
4. Compute the [eigenvalues](/eigenvalue/) of $DP(x^*)$.

The result is a statement about one design and one slope, found up to numerical error. It is a computation, not a proof that the gait is stable from every start: the region of starts that converge can be small.

The energy balance gives the speed of the gait. In one step on a slope of angle $\gamma$, gravity supplies $m g d \sin \gamma$, where $d$ is the step length along the slope. The impact removes kinetic energy, because the velocity of the hip must turn from the old stance leg to the new one. A steeper slope gives a faster gait.

## Examples

**The rimless wheel.** A wheel with no rim is a hub of mass $m$ with spokes of length $l$, with the angle $2\alpha$ between neighboring spokes. It rolls down a slope of angle $\gamma$ on one spoke at a time, and the hub swings like an inverted pendulum. When the next spoke hits the ground, the angular momentum about the new contact point is conserved, so the angular speed drops from $\omega^-$ to $\omega^+ = \cos(2\alpha)\, \omega^-$. During the next step the hub falls by $2 l \sin \alpha \sin \gamma$. The energy balance gives the stride map in closed form:

$$(\omega_{n+1}^-)^2 = \cos^2(2\alpha)\, (\omega_n^-)^2 + \frac{4 g}{l} \sin \alpha \sin \gamma,$$

provided that the hub passes over the top of each spoke, which needs $(\omega_n^+)^2 > (2 g / l)(1 - \cos(\alpha - \gamma))$. In the variable $u = (\omega^-)^2$, the map is affine with slope $\cos^2(2\alpha) < 1$, so for $0 < 2\alpha < \pi/2$ it has one fixed point and every start that keeps rolling converges to it. With $l = 1$ m, $\alpha = \pi / 8$ (eight spokes), $\gamma = 0.08$ rad and $g = 9.81$ m/s², the fixed point is $\omega^- = 1.5492$ rad/s, with $\omega^+ = 1.0955$ rad/s. The error in $u$ halves at each step. From $\omega^- = 1.4$ the speeds before impact are $1.4765$, $1.5133$, $1.5314$, $1.5403$ and $1.5448$; from $2.5$ they are $2.0797$, $1.8337$, $1.6974$, $1.6250$ and $1.5876$. Below $\omega^- = 1.3794$ rad/s the hub does not pass over the next spoke and the wheel stops. The rimless wheel is the rare case in which the fixed point and its stability follow from a formula.

**The compass gait and the simplest walking model.** Two rigid legs joined at a hip, with a point mass at the hip and much smaller masses at the feet, walk down a slope in a periodic gait. Garcia et al. (1998) study the limit in which the foot masses go to zero. They find the gait and its stability by numerical search, show that it is stable only for small slopes, and describe how the gait changes as the slope grows, including period doubling of the gait. The legs have no knees, so the swing foot passes through the ground for a short time in mid swing; the model ignores this scuffing.

**McGeer's walker.** McGeer (1990) built a planar walker with curved feet that walked down a shallow slope with no power, and found its gaits by the fixed point procedure above.

## Where it is used

- **Efficient walking robots.** Robots that add small motors to a passive design, to replace the energy lost at impacts or to walk on level ground, aim to use less energy per distance than robots that track a fixed joint trajectory, because the motors only replace the impact losses. The design gives the gait, and the controller only helps.
- **Analysis of walking controllers.** The stride map, its fixed points and their eigenvalues are the standard tools for gaits with impacts. [Hybrid zero dynamics](/hybrid-zero-dynamics/) uses them for actuated bipeds, on a low dimensional reduced model.
- **Models of human gait.** The swing leg of a human moves almost passively, and simple passive models predict the relation of step length, step time and speed.
- **Contrast with ZMP walking.** A passive walker has point or round feet and no flat foot contact, so it never satisfies the [zero moment point](/zero-moment-point/) criterion of flat-footed walking. Its balance is a property of the whole periodic motion, not of each instant.

## References
