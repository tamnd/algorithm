---
tag: 5DRDH3
kind: technique
slug: kustaanheimo-stiefel-regularization
name: Kustaanheimo-Stiefel regularization
aliases:
- KS regularization
area: scientific-computing/n-body-and-particle-methods
level: advanced
summary: Maps the Kepler problem to a harmonic oscillator in four dimensions with a new time variable, so close binaries can be integrated without singularity.
prereqs: [gravitational-n-body-problem, hamiltonian-systems]
see_also: [block-time-steps, hermite-n-body-integrator, wisdom-holman-integrator, gravitational-softening, direct-n-body-summation, symplectic-integrators, runge-kutta-methods, adaptive-step-size-control]
sources:
  - paper: doi:10.1515/crll.1965.218.204
    title: "Paul Kustaanheimo and Eduard Stiefel, Perturbation theory of Kepler motion based on spinor regularization, Journal fur die reine und angewandte Mathematik 218, 1965, 204-219"
    locator: the four-dimensional map and the regularized equations of motion
  - book: isbn:9780521432726
    title: Sverre J. Aarseth, Gravitational N-Body Simulations, Tools and Algorithms, Cambridge University Press, 2003
    locator: Section 4.3 (Levi-Civita regularization), Section 4.4 (Kustaanheimo-Stiefel regularization), Section 4.7 (Stumpff functions)
---

Kustaanheimo-Stiefel (KS) regularization removes the $1/r^2$ singularity of the two-body force. It replaces the relative position $\mathbf{x} \in \mathbb{R}^3$ of a close pair by a vector $\mathbf{u} \in \mathbb{R}^4$ with $|\mathbf{x}| = |\mathbf{u}|^2$, and the physical time $t$ by a fictitious time $s$ with $dt = r\, ds$. In these variables the unperturbed Kepler motion becomes a harmonic oscillator, $\mathbf{u}'' = \frac{h}{2} \mathbf{u}$, where $h$ is the two-body energy per unit reduced mass. The equations are smooth and linear even through a collision, so a step in $s$ of fixed size follows a binary of any eccentricity with the same relative accuracy. Direct [N-body](/gravitational-n-body-problem/) codes for star clusters use KS for hard binaries and close encounters, where an ordinary step would have to shrink by many orders of magnitude.

## In plain words

When two stars pass very close, the pull between them becomes huge and changes very fast. A normal integrator must then take tiny steps, and at a collision it fails.

KS regularization changes the variables of the pair. The position is written as the "square" of a new vector with four entries, and the clock is slowed in proportion to the distance, so the close passage takes many small physical moments but a normal amount of new time. With both changes, the orbit of the pair becomes the motion of a weight on a spring, which has no bad points at all. The pair is integrated in the new variables, and the result is changed back when the positions are needed.

## When it applies

- Two bodies are much closer to each other than to all other bodies, so their motion is a Kepler orbit plus a small perturbation $\mathbf{P}$ from the rest of the system.
- The forces are point-mass gravity, without [softening](/gravitational-softening/), and collisions or very eccentric binaries must be followed accurately.
- The integrator can use its own time variable for the pair, as in the NBODY codes with [block time steps](/block-time-steps/), where the KS pair is a single body for the rest of the system.

It does not apply to three or more bodies at once, unless they are put in a chain of pairs; and when the pair is far from isolated, the perturbation dominates and the regularized equations lose their advantage.

## The template

Write $\mu = G(m_1 + m_2)$, $\mathbf{x} = \mathbf{x}_2 - \mathbf{x}_1$, $\mathbf{v} = \dot{\mathbf{x}}$ and $r = |\mathbf{x}|$.

1. **The map.** For $\mathbf{u} = (u_1, u_2, u_3, u_4)$ let

$$L(\mathbf{u}) = \begin{pmatrix} u_1 & -u_2 & -u_3 & u_4 \\ u_2 & u_1 & -u_4 & -u_3 \\ u_3 & u_4 & u_1 & u_2 \\ u_4 & -u_3 & u_2 & -u_1 \end{pmatrix},$$

and set $(\mathbf{x}, 0) = L(\mathbf{u}) \mathbf{u}$, that is, $x_1 = u_1^2 - u_2^2 - u_3^2 + u_4^2$, $x_2 = 2(u_1 u_2 - u_3 u_4)$ and $x_3 = 2(u_1 u_3 + u_2 u_4)$. The matrix satisfies $L(\mathbf{u})^T L(\mathbf{u}) = |\mathbf{u}|^2 I$, so $r = |\mathbf{u}|^2$.

2. **The inverse map.** If $x_1 \ge 0$, take $u_1 = \sqrt{(r + x_1)/2}$, $u_2 = x_2 / (2u_1)$, $u_3 = x_3 / (2u_1)$ and $u_4 = 0$. Otherwise take $u_2 = \sqrt{(r - x_1)/2}$, $u_1 = x_2 / (2u_2)$, $u_3 = 0$ and $u_4 = x_3 / (2u_2)$. Each $\mathbf{x} \ne 0$ has a circle of preimages; this choice is one of them.

3. **The new time and the velocity.** Set $dt = r\, ds$ and write $' = d/ds$. Then $\mathbf{v} = 2 L(\mathbf{u}) \mathbf{u}' / r$, and from $\mathbf{v}$ take $\mathbf{u}' = \frac{1}{2} L(\mathbf{u})^T (\mathbf{v}, 0)$. This $\mathbf{u}'$ satisfies the bilinear relation $u_4 u_1' - u_3 u_2' + u_2 u_3' - u_1 u_4' = 0$, which is the fourth row of $L(\mathbf{u}) \mathbf{u}' = 0$ and which the equations of motion keep.

4. **The equations of motion.** With $h = v^2/2 - \mu/r = (2|\mathbf{u}'|^2 - \mu)/r$ and a perturbing acceleration $\mathbf{P}$ on the relative motion,

$$\mathbf{u}'' = \frac{h}{2} \mathbf{u} + \frac{r}{2} L(\mathbf{u})^T (\mathbf{P}, 0), \qquad h' = 2\, \mathbf{u}' \cdot L(\mathbf{u})^T (\mathbf{P}, 0), \qquad t' = |\mathbf{u}|^2.$$

These ten equations have no singularity at $\mathbf{u} = 0$. Integrate them with any accurate method in $s$, for example [Runge-Kutta](/runge-kutta-methods/) or a Hermite scheme in $s$.

5. **Back to physical variables.** When the positions of the pair are needed at a physical time, map $\mathbf{u}$ and $\mathbf{u}'$ back with steps 1 and 3 and place the two bodies about their center of mass.

## Classic examples

**A circular orbit.** Take $\mu = 1$, $\mathbf{x} = (1, 0, 0)$ and $\mathbf{v} = (0, 1, 0)$, so $h = -\frac{1}{2}$. Step 2 gives $\mathbf{u} = (1, 0, 0, 0)$, and step 3 gives $\mathbf{u}' = (0, \frac{1}{2}, 0, 0)$. The equation $\mathbf{u}'' = -\frac{1}{4} \mathbf{u}$ has the solution $\mathbf{u}(s) = (\cos \frac{s}{2}, \sin \frac{s}{2}, 0, 0)$, and the map gives $\mathbf{x}(s) = (\cos s, \sin s, 0)$. Here $r = 1$, so $t = s$, and the orbit closes after $t = 2\pi$ while $\mathbf{u}$ makes only half a turn. In the plane $u_3 = u_4 = 0$ the map is the square $u_1 + i u_2 \mapsto (u_1 + i u_2)^2$ of a complex number, which is the Levi-Civita map.

**Kepler's third law.** For any bound orbit, $\omega^2 = -h/2$ and $\mathbf{u}(s) = \mathbf{u}_0 \cos \omega s + (\mathbf{u}'_0 / \omega) \sin \omega s$. Since $\mathbf{x}$ is quadratic in $\mathbf{u}$, the orbit closes after $s = \pi / \omega$, and

$$T = \int_0^{\pi/\omega} |\mathbf{u}(s)|^2\, ds = \frac{\pi}{2\omega} \left( |\mathbf{u}_0|^2 + \frac{|\mathbf{u}'_0|^2}{\omega^2} \right) = \frac{\pi}{2\omega} \cdot 2a = 2\pi \sqrt{a^3 / \mu},$$

with $a = -\mu / (2h)$, because $|\mathbf{u}_0|^2 = r_0$ and $|\mathbf{u}'_0|^2 / \omega^2 = 2a - r_0$. For $\mathbf{x} = (1.5, 0.2, -0.3)$, $\mathbf{v} = (0.1, 0.6, 0.25)$ and $\mu = 1$, the oscillator returns $\mathbf{x}$ to its start at $s = \pi/\omega$ to rounding, and a numerical quadrature of $t'$ gives $T = 7.8249044$, equal to $2\pi a^{3/2}$ with $a = 1.15753$ (measurement).

**Binaries in star cluster codes.** The NBODY codes of Aarseth treat each hard binary and each close encounter as a KS pair, with its perturbation from the neighbors, and they switch the pair back to ordinary bodies when it separates (Aarseth 2003, Section 4.4).

## Variations

- **Levi-Civita regularization.** The same idea in the plane, with $\mathbf{u} \in \mathbb{R}^2$ and the complex square $x_1 + i x_2 = (u_1 + i u_2)^2$ (Aarseth 2003, Section 4.3). There is no quadratic map of this kind from $\mathbb{R}^3$ to $\mathbb{R}^3$ with $|\mathbf{x}| = |\mathbf{u}|^2$ and a matrix $L$ with orthogonal columns, which is why KS goes to four dimensions (theorem of Hurwitz on composition of quadratic forms).
- **Sundman time transformation alone.** Only $dt = r\, ds$, or $dt = r^\alpha ds$, without the change of position. It spreads the steps more evenly around the pericenter but does not remove the singularity of the equations.
- **Stumpff function solutions.** For a weakly perturbed pair, the oscillator part can be advanced exactly with Stumpff functions, and only the perturbation is integrated (Aarseth 2003, Section 4.7).
- **Chain and many-body regularization.** For three or more close bodies, regularize each pair along a chain of the closest neighbors (Mikkola and Aarseth), or use a time transformation with the Lagrangian, as in the algorithmic regularization of Mikkola and Tanikawa.
- **Hamiltonian form.** KS can also be written as a canonical transformation of an extended Hamiltonian, so that a [symplectic integrator](/symplectic-integrators/) applies in the new variables.

## Pitfalls

- **The bilinear relation.** The equations keep $\ell(\mathbf{u}, \mathbf{u}') = u_4 u_1' - u_3 u_2' + u_2 u_3' - u_1 u_4' = 0$ only if it holds at the start. Starting with any other $\mathbf{u}'$ gives a velocity $\mathbf{v}$ that is not the derivative of $\mathbf{x}$. Always take $\mathbf{u}'$ from step 3.
- **Energy as a variable.** The coefficient $h$ must be integrated with its own equation $h' = 2\, \mathbf{u}' \cdot L^T \mathbf{P}$, not recomputed from $\mathbf{u}$ and $\mathbf{u}'$, or the oscillator equation picks up errors near pericenter where $r$ is small.
- **Physical time output.** The step is fixed in $s$, not in $t$. To get the state at a given $t$, iterate on $s$ with the equation $t' = |\mathbf{u}|^2$, for example by Newton's method.
- **Strong perturbations.** When a third body comes close, $\mathbf{P}$ becomes as large as the pair force, the oscillator form gives no gain, and the pair must be ended or put into a chain.
- **Unbound pairs.** For $h > 0$ the oscillator becomes $\mathbf{u}'' = \frac{h}{2} \mathbf{u}$ with exponential solutions; the equations stay regular, but the closed-form solutions use $\cosh$ and $\sinh$.

## Exercises

1. Show that $L(\mathbf{u})^T L(\mathbf{u}) = |\mathbf{u}|^2 I$, and conclude that $|\mathbf{x}| = |\mathbf{u}|^2$ and $|\mathbf{v}|^2 = 4 |\mathbf{u}'|^2 / r$.
2. Show that $\mathbf{u}$ and $(u_1 \cos\varphi - u_4 \sin\varphi,\ u_2 \cos\varphi + u_3 \sin\varphi,\ u_3 \cos\varphi - u_2 \sin\varphi,\ u_4 \cos\varphi + u_1 \sin\varphi)$ map to the same $\mathbf{x}$ for every $\varphi$.
3. Starting from $\ddot{\mathbf{x}} = -\mu \mathbf{x} / r^3$, $dt = r\, ds$ and the bilinear relation, derive $\mathbf{u}'' = \frac{h}{2} \mathbf{u}$.
4. A radial orbit starts at rest at $\mathbf{x} = (1, 0, 0)$ with $\mu = 1$. Show that $\mathbf{u}(s) = (\cos \frac{s}{\sqrt{2}}, 0, 0, 0)$, that $\mathbf{u}$ passes through 0 smoothly at $s = \pi / \sqrt{2}$, and that the time to the collision is $t = \pi / (2\sqrt{2})$. What happens to $\mathbf{x}$ after the collision?

## References
