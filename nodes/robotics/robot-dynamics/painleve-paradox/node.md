---
tag: EASV78
kind: concept
slug: painleve-paradox
name: Painleve paradox
aliases:
- frictional paradox of rigid bodies
area: robotics/robot-dynamics
level: advanced
summary: With rigid bodies and Coulomb friction, the equations in forces and accelerations can have no solution or several; an impulse at the contact, as in time-stepping methods, restores existence.
prereqs: [newton-euler-equations, rigid-contact-complementarity]
see_also: [stewart-trinkle-time-stepping, friction-cone, gauss-principle-of-least-constraint, grasp-contact-models, contact-implicit-trajectory-optimization, hybrid-automata, np-complete, singular-perturbation-method]
sources:
  - paper: Paul Painlevé, Sur les lois du frottement de glissement, Comptes Rendus de l'Académie des Sciences 121, 1895
    title: Paul Painlevé, Sur les lois du frottement de glissement
    locator: "pages 112 to 115; later notes in volumes 140 and 141, 1905"
  - paper: doi:10.1023/A:1008292328909
    title: "Mihai Anitescu and Florian A. Potra, Formulating dynamic multi-rigid-body contact problems with friction as solvable linear complementarity problems, Nonlinear Dynamics 14(3), 1997"
    locator: pages 231 to 247
  - paper: doi:10.1016/S0997-7538(99)00144-8
    title: "Franck Génot and Bernard Brogliato, New results on Painlevé paradoxes, European Journal of Mechanics A/Solids 18(4), 1999"
    locator: pages 653 to 677
  - paper: doi:10.1093/imamat/hxw027
    title: Alan R. Champneys and Péter L. Várkonyi, The Painlevé paradox in contact mechanics, IMA Journal of Applied Mathematics 81(3), 2016
    locator: pages 538 to 588
  - paper: doi:10.1007/s002050050129
    title: "David E. Stewart, Convergence of a time-stepping scheme for rigid-body dynamics and resolution of Painlevé's problem, Archive for Rational Mechanics and Analysis 145(3), 1998"
    locator: pages 215 to 260
  - paper: doi:10.1137/S0036144599360110
    title: "David E. Stewart, Rigid-body dynamics with friction and impact, SIAM Review 42(1), 2000"
    locator: pages 3 to 39
  - paper: doi:10.1145/122718.122722
    title: "David Baraff, Coping with friction for non-penetrating rigid body simulation, Computer Graphics (SIGGRAPH '91 Proceedings) 25(4), 1991"
    locator: the sections on inconsistent and indeterminate configurations
---

The Painlevé paradox is the observation that rigid body mechanics with Coulomb friction is not always consistent: for some states of a sliding body, no contact force satisfies the contact laws, and for others, several do. Painlevé (1895) pointed this out in a note on the laws of sliding friction. The standard example is a rod whose lower end slides on a rough floor. The paradox goes away when the contact may apply an impulse, a very large force for a very short time, which is what the impulse form of [rigid contact](/rigid-contact-complementarity/) and [time-stepping methods](/stewart-trinkle-time-stepping/) allow.

## In plain words

Lean a stick against the floor and drag its lower end away from you along a rough floor. Friction pulls the end back, and because the stick leans, that pull also tends to turn the stick so that its end digs into the floor. If the floor is rough enough and the stick leans at the right angle, there is a problem. The harder the floor pushes up, the more friction there is, and the more the end digs in, so a larger push makes things worse instead of better. Then the textbook rules give no answer at all: no push from the floor is right. In other states they give two answers: the stick may lift off, or it may stay down with a large push. A real stick settles the matter with a sudden jolt, and its end stops at once.

## The idea

Take a uniform rod of mass $m$ and length $2l$, so that its inertia about the center of mass is $I = m l^2 / 3$. It makes the angle $\theta$ with the floor, and its lower end touches the floor and slides away from the center of mass, in the direction from the center to the end. The floor applies the normal force $N \ge 0$ and the Coulomb friction force $\mu N$, which points against the slip. The Newton-Euler equations give the normal acceleration of the lower end:
$$a = b + \frac{A}{m} N, \qquad b = -g + l \sin\theta\, \dot\theta^2, \qquad A = 1 + 3\cos\theta\,(\cos\theta - \mu\sin\theta).$$
The rigid contact law is the complementarity $N \ge 0$, $a \ge 0$, $N a = 0$: either the end lifts off with no force, or it stays on the floor with zero normal acceleration.

- If $A > 0$, there is exactly one solution: $N = 0$ if $b \ge 0$, and $N = -m b / A$ if $b < 0$.
- If $A < 0$, a larger normal force pushes the end into the floor. Then for $b < 0$ there is no solution (inconsistency), and for $b > 0$ there are two, $N = 0$ and $N = -m b / A$ (indeterminacy).

$A < 0$ needs $\mu > (1 + 3\cos^2\theta)/(3 \cos\theta \sin\theta)$. The right side is smallest at $\tan\theta = 2$, about 63.43 degrees, where it equals $4/3$. So the paradox occurs for this rod only when $\mu > 4/3$, a large friction coefficient. This is a theorem about the model; the threshold depends on the shape of the body.

The resolution is to allow impulses. In impulse and velocity form, the contact law asks for a normal impulse and a friction impulse that change the velocity at once, and such a problem has a solution (Anitescu and Potra 1997 for the linearized time-stepping form). For the rod in an inconsistent state, the floor stops the sliding end with an impulse inside the friction cone, a tangential impact without a collision. Stewart (1998) proved that a time-stepping scheme in impulses converges as the step goes to 0 and that its limits solve the problem in a measure sense, which resolves Painlevé's problem. Génot and Brogliato (1999) analysed how the rod can reach the states where $A$ changes sign, and Champneys and Várkonyi (2016) surveyed the paradox, including the resolution with a compliant contact.

## Examples

**The inconsistent rod.** Take $m = 1$ kg, $l = 0.5$ m, $g = 9.81$ m/s$^2$, $\mu = 1.5$ and $\tan\theta = 2$. Then $\cos\theta = 1/\sqrt5$, $\sin\theta = 2/\sqrt5$ and
$$A = 1 + 3 \cdot \tfrac15 (1 - 1.5 \cdot 2) = -0.2 .$$
With $\dot\theta = 0$, $b = -9.81$ m/s$^2$, so $a = -9.81 - 0.2 N < 0$ for every $N \ge 0$: no normal force keeps the end out of the floor, and $N = 0$ does not either.

**The indeterminate rod.** The same rod with $\dot\theta = 6$ rad/s has $b = -9.81 + 0.5 \cdot (2/\sqrt5) \cdot 36 = 6.2897$ m/s$^2$. Both $N = 0$ (the end lifts off) and $N = 6.2897 / 0.2 = 31.45$ N (the end stays down) satisfy the contact law. The switch from no solution to two solutions happens at $\dot\theta = \sqrt{g / (l \sin\theta)} = 4.684$ rad/s, where $b = 0$.

**The impulsive stop.** Let the inconsistent rod slide with velocity $1$ m/s, with $\dot\theta = 0$. The inverse of the effective mass at the lower end, for impulses along the floor and normal to it, is
$$K = \begin{pmatrix} 1/m + r_y^2 / I & -r_x r_y / I \\ -r_x r_y / I & 1/m + r_x^2 / I \end{pmatrix} = \begin{pmatrix} 3.4 & -1.2 \\ -1.2 & 1.6 \end{pmatrix} \text{ 1/kg},$$
with $r = (-l\cos\theta, -l\sin\theta)$ from the center of mass to the end. The impulse that stops the end is $K^{-1} (1, 0) = (0.4, 0.3)$ N s: a friction impulse of 0.4 N s and a normal impulse of 0.3 N s. Their ratio is $4/3 < \mu = 1.5$, so the impulse lies inside the friction cone and the end sticks. A Stewart-Trinkle step with $h = 10^{-3}$ s gives about this impulse, and it tends to $(0.4, 0.3)$ as $h \to 0$.

## Where it is used

- **Simulation.** The paradox is the reason that robot simulators with rigid contacts write the dynamics in impulses over a time step, as in [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/), and not in forces. Baraff (1991) showed that deciding whether a configuration with friction has consistent forces is [NP-complete](/np-complete/).
- **Manipulation and legged robots.** A pushed or dragged object, a robot finger that slides on a surface, or a leg that brakes on a rough floor can enter a state of the paradox. In practice the result is a sudden stop, a jump or a chatter of the contact.
- **Planning with contact.** Planners that use the complementarity conditions, such as [contact-implicit trajectory optimization](/contact-implicit-trajectory-optimization/), work with the impulse form so that every candidate motion has a solution.

## References
