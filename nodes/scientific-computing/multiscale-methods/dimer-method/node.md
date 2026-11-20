---
tag: JXAQP4
kind: algorithm
slug: dimer-method
name: Dimer method
area: scientific-computing/multiscale-methods
level: advanced
summary: Finds saddle points from one minimum using only gradients, by rotating a pair of close images to the lowest curvature mode and climbing along it.
model: real-ram
complexity:
  vars: {I: the number of translations, r: the number of rotations per translation, G: the cost of one gradient, d: the number of coordinates}
  time: {worst: O(I r (G + d))}
  space: {extra: O(d)}
properties: {deterministic: true, randomized: false, exact: false, iterative: true}
history:
  year: 1999
  people: [Graeme Henkelman, Hannes Jonsson]
  note: Henkelman and Jonsson gave the method in 1999. Heyden, Bell and Keil gave in 2005 the rotation angle from a fit of the curvature, with one extra gradient per rotation.
prereqs: [eigenvalue-problem, energy-landscape]
see_also: [nudged-elastic-band, harmonic-transition-state-theory, kinetic-monte-carlo, rayleigh-quotient-iteration, lanczos-algorithm, power-iteration, string-method, temperature-accelerated-dynamics]
sources:
  - paper: doi:10.1063/1.480097
    title: Graeme Henkelman and Hannes Jonsson, A dimer method for finding saddle points on high dimensional potential surfaces using only first derivatives, Journal of Chemical Physics 111(15), 1999, 7010-7022
    locator: the dimer, the curvature from two gradients, the rotation to the lowest mode and the modified force of the translation
  - paper: doi:10.1063/1.2104507
    title: "Andreas Heyden, Alexis T. Bell and Frerich J. Keil, Efficient methods for finding transition states in chemical reactions: comparison of improved dimer method and partitioned rational function optimization method, Journal of Chemical Physics 123(22), 2005, 224101"
    locator: the improved rotation, with the curvature fitted as a function of the rotation angle
  - paper: doi:10.1007/BF00547608
    title: Klaus Muller and Leo D. Brown, Location of saddle points and minimum energy paths by a constrained simplex optimization procedure, Theoretica Chimica Acta 53(1), 1979, 75-93
    locator: the two-dimensional test potential of the example
---

The dimer method finds a first-order saddle point of a potential energy, starting from a point near a minimum, without knowing the final state and without computing the Hessian. It uses a dimer: two points close together, at $R \pm \Delta R\, N$. The two gradients give the curvature along the direction $N$. The method rotates the dimer to the direction of the lowest curvature, then moves its centre uphill along that direction and downhill in all others. Each step needs only a few gradient evaluations, so it works for systems with thousands of atoms. Saddles found from one minimum give the possible escapes and, by [harmonic transition state theory](/harmonic-transition-state-theory/), their rates, for example for the event catalog of [kinetic Monte Carlo](/kinetic-monte-carlo/).

## In plain words

You stand in a valley in fog and want to find the lowest passes out of it. You cannot see the shape of the land, but you can feel the slope under your feet. With a short stick held at two points, you can feel how the slope changes along the stick, which tells you how much the ground bends in that direction.

Turn the stick until it points in the direction where the ground bends upward the least, or bends down. That is the easiest way out of the valley. Then walk uphill along the stick and downhill across it. In a valley, this takes you up the softest side. Near a pass, it takes you to the top of the pass and keeps you in the middle of it. Different starts lead to different passes.

## The problem

The input is a potential $V: \mathbb{R}^d \to \mathbb{R}$ with its gradient, a start point $R_0$ (often a minimum plus a small random displacement) and a start direction $N_0$. The output is a first-order saddle $R_s$: $\nabla V(R_s) = 0$ and the Hessian $H(R_s)$ has exactly one negative eigenvalue $\lambda_1$, together with its eigenvector $N$, the direction of the reaction. The final state is not given. For atoms, the coordinates are mass weighted if the masses differ.

## The algorithm

```pseudo id=main
DIMER-METHOD(V, R, N, ΔR, h, tol)
L1  N ← N / |N|
L2  repeat
L3      F ← -∇V(R), F_1 ← -∇V(R + ΔR N), F_2 ← 2F - F_1
L4      C ← (F_2 - F_1) · N / (2 ΔR)                      ▷ curvature along N
L5      F_rot ← (F_1 - F_2) - ((F_1 - F_2) · N) N, Θ ← F_rot / |F_rot|
L6      from C, dC/dφ and the curvature at one trial angle, fit C(φ) = a_0/2 + a_1 cos 2φ + b_1 sin 2φ and take its minimum φ
L7      N ← cos φ N + sin φ Θ                             ▷ repeat L3 to L7 until |F_rot| is small
L8      if |F| < tol and C < 0 then return R, N, C
L9      F† ← F - 2 (F · N) N if C < 0, else F† ← -(F · N) N
L10     R ← R + h F†, with the length of the step at most s_max (equal to s_max where C ≥ 0)
```

Line L3 evaluates the gradient at the centre and at one end of the dimer; the other end follows from a central difference. Line L4 is the curvature along $N$, which is $N^{\mathsf T} H N + O(\Delta R^2)$. Lines L5 to L7 rotate the dimer. The rotational force $F_{\mathrm{rot}}$ is the part of $F_1 - F_2$ perpendicular to $N$; it is zero when $N$ is an eigenvector of $H$. The rotation of line L6 is the one of Heyden, Bell and Keil: the curvature in the plane of $N$ and $\Theta$ is exactly $a_0/2 + a_1 \cos 2\varphi + b_1 \sin 2\varphi$ for a quadratic $V$, so one trial rotation by a small angle $\varphi_1$, with one more gradient, fixes the three numbers and gives the angle of the minimum. Henkelman and Jonsson's original rotation used a trial angle and a fit of the rotational force instead. Line L9 is the force of the translation: where the curvature is negative, the component along $N$ is inverted, which turns the saddle into a minimum of the modified landscape. Where $C \ge 0$ the dimer is still in the convex region of the basin, so it moves only along $N$, uphill, with a full step of length $s_{\max}$.

## Example

**One rotation by hand.** Take the quadratic $V(x, y) = \frac12 (3x^2 + 2xy - y^2)$ with $H = \begin{pmatrix} 3 & 1 \\ 1 & -1 \end{pmatrix}$, eigenvalues $1 \pm \sqrt5$, and start with $N = (1, 0)$. Then $C(0) = N^{\mathsf T} H N = 3$. $F_1 - F_2 = -2\Delta R\, H N = -2\Delta R\, (3, 1)$, its part perpendicular to $N$ is $(0, -2\Delta R)$, so $\Theta = (0, -1)$. The fit numbers are $b_1 = \Theta^{\mathsf T} H N = -1$, $a_1 = \frac12 (3 - (-1)) = 2$ and $a_0 = 2$. The curvature in the plane is $1 + 2\cos 2\varphi - \sin 2\varphi = 1 + \sqrt5 \cos(2\varphi - 2\varphi^*)$, with $2\varphi^* = \operatorname{atan2}(-1, 2) = -0.4636$. The minimum is at $\varphi = \varphi^* + \pi/2 = 1.3390$, with $C = 1 - \sqrt5 = -1.2361$, the lowest eigenvalue, and the new $N = (\cos 1.3390, -\sin 1.3390) = (0.2298, -0.9732)$ is its eigenvector. In two dimensions one rotation is exact. The translation with $h = 0.2$ from $(0.3, 0.2)$ then reaches the saddle $(0, 0)$ to $10^{-10}$ in 76 steps.

**Searches on the Muller-Brown surface.** From each of the three minima, 20 searches started at the minimum plus a Gaussian displacement of standard deviation 0.05 in each coordinate, with a random $N$ (`random.Random(1)`), $\Delta R = 10^{-4}$, $h = 10^{-3}$, $s_{\max} = 0.02$ and $|\nabla V| < 10^{-6}$, gave:

| start | found S1 $(-0.82200, 0.62431)$, $V = -40.6648$ | found S2 $(0.21249, 0.29299)$, $V = -72.2489$ | no saddle in 2000 steps |
|---|---|---|---|
| minimum C | 6 | 14 | 0 |
| minimum B | 0 | 13 | 7 |
| minimum A | 3 | 0 | 17 |

From C, all 20 searches converged, in 55 translations for the median search and at most 145, and the curvature at the end agrees with the negative eigenvalue of the Hessian ($-750.86$ at S1, $-735.25$ at S2). From A and B, the soft direction of the basin often points away from both saddles, and the search climbs the walls of the surface into the region where $V$ grows without bound. This is the typical behavior: a set of searches from one minimum gives some of the saddles, not all, and some searches are lost.

## Correctness

The proof below has three parts. First, by a Taylor expansion, the difference of the two forces is $-2\Delta R\, H N + O(\Delta R^3)$, so the dimer measures $H N$ and the curvature $N^{\mathsf T} H N$ with two gradients. Second, the curvature along $\cos\varphi\, N + \sin\varphi\, \Theta$ is a Rayleigh quotient, which is a constant plus a sinusoid in $2\varphi$; three values fix it, and its minimum is the lowest eigenvalue of $H$ in that plane. In two dimensions this is the lowest eigenvalue, so one rotation is exact. Third, the modified force is $F^{\dagger} = (I - 2NN^{\mathsf T}) F$, a reflection of $F$, so it is zero only where the gradient is zero; and near a first-order saddle, with $N$ the eigenvector of the negative eigenvalue, the step of line L10 is a contraction for $h < 2 / \max_i |\lambda_i|$. So a first-order saddle is an attracting fixed point. The proof does not show that a search from a minimum reaches a saddle, or which one.

## Complexity

One translation costs one gradient at the centre and two gradients for each rotation (one at the dimer end, one at the trial angle), so $1 + 2r$ gradients for $r$ rotations, plus $O(r d)$ arithmetic in the [real RAM](/real-ram/) model. The memory is $O(d)$. For atoms, the gradient costs $G$ (a force call) and dominates. The number of translations depends on the start and the landscape; near the saddle it falls like the linear rate of steepest descent on the reflected Hessian, and with a quasi-Newton step it is much smaller. The method never stores or factors the $d \times d$ Hessian, which is why it is used where $d$ is large.

## Properties

- **First derivatives only.** The curvature and the lowest mode come from finite differences of gradients.
- **One end state.** The final state is not needed. The final state is found after the search, by a relaxation from both sides of the saddle along $\pm N$.
- **Local and incomplete.** A search finds one saddle near its start, and a set of searches samples the saddles around a minimum without a guarantee of completeness.
- **Deterministic.** The same start and the same $N$ give the same saddle. The randomness in practice is in the choice of the starts.

## Variants and improvements

- **Rotation by a fit of the curvature.** The rotation of line L6 (Heyden, Bell and Keil 2005) uses the exact form of the curvature as a function of the angle. The original rotation of Henkelman and Jonsson used a fit of the rotational force at a trial angle.
- **Conjugate gradient rotations.** In many dimensions, the search directions of the rotation are chosen by a [conjugate gradient](/conjugate-gradient-method/) rule instead of the plain rotational force, as in an eigenvalue solver.
- **Translation with memory.** A conjugate gradient or limited memory [BFGS](/bfgs/) step on the modified force converges faster than the fixed step of line L10.
- **Other lowest mode solvers.** The lowest eigenvector can also come from the [Lanczos algorithm](/lanczos-algorithm/) on the Hessian applied by finite differences, as in the activation relaxation technique; the dimer rotation is a gradient method for the [Rayleigh quotient](/rayleigh-quotient-iteration/).
- **Use in on-the-fly KMC.** Many dimer searches from one state give the event catalog of adaptive [kinetic Monte Carlo](/kinetic-monte-carlo/); the rates follow from harmonic transition state theory.

## When to use it

Use the dimer method when you know the initial state and want the escapes from it, with no guess of the final state: to explore the events of a defect, to build an event catalog, or to refine a saddle from the highest image of a short [nudged elastic band](/nudged-elastic-band/). Use the nudged elastic band when both end states are known and you also need the whole path. For a small system where the Hessian is cheap, a Newton method on the gradient with the eigenvector following of the Hessian is simpler.

## Pitfalls

- **A dimer that is too short or too long.** A large $\Delta R$ gives an error of $O(\Delta R^2)$ in the curvature. A very small one gives rounding error: the error in $F_1 - F_2$ is about $\varepsilon |F|$ for the machine epsilon $\varepsilon$, so the error in $C$ grows like $\varepsilon |F| / \Delta R$. Noisy forces, for example from an electronic structure code, make this much worse. Check that $C$ changes little when $\Delta R$ changes by a factor of 2.
- **Runaway searches.** In the convex region the dimer climbs along the softest mode, which may lead to a high wall instead of a saddle. Limit the step and the number of steps, and drop searches that go too far.
- **The same saddle again.** Many searches find the same low saddles; compare each new saddle with those already found, by energy and position.
- **A higher-order saddle.** If the lowest mode is not resolved (a rotation that stops too early), the dimer can converge to a point with two negative curvatures. Check the curvature along a second direction at the end.
- **Stop tests on the force only.** The stop test must also check $C < 0$; a small force with $C > 0$ is a minimum.

## Implementations

## History

Henkelman and Jonsson introduced the dimer method in 1999 for saddle searches on high-dimensional potential surfaces where only forces are available, for example from density functional theory. Heyden, Bell and Keil improved the rotation in 2005 with the fit of the curvature as a function of the rotation angle and compared the method with Hessian-based saddle searches. The method became a standard tool for building event catalogs in adaptive kinetic Monte Carlo.

## References
