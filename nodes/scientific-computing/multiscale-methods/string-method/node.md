---
tag: SDPAV5
kind: algorithm
slug: string-method
name: String method
aliases:
- zero-temperature string method
- simplified string method
area: scientific-computing/multiscale-methods
level: advanced
summary: Moves a curve between two minima by the potential force and reparametrizes it by arc length, converging to the minimum energy path.
model: real-ram
complexity:
  vars: {N: the number of segments of the string, d: the number of coordinates, G: the cost of one gradient, I: the number of iterations}
  time: {worst: O(I N (G + d))}
  space: {extra: O(N d)}
properties: {deterministic: true, randomized: false, exact: false, iterative: true}
history:
  year: 2002
  people: [Weinan E, Weiqing Ren, Eric Vanden-Eijnden]
  note: E, Ren and Vanden-Eijnden gave the string method in 2002, with the projected force and a reparametrization by arc length. Their simplified string method of 2007 drops the projection.
prereqs: [gradient-descent, energy-landscape]
see_also: [nudged-elastic-band, dimer-method, harmonic-transition-state-theory, transition-path-sampling, collective-variable, lagrange-interpolation, stochastic-differential-equation, metadynamics]
sources:
  - paper: doi:10.1103/PhysRevB.66.052301
    title: Weinan E, Weiqing Ren and Eric Vanden-Eijnden, String method for the study of rare events, Physical Review B 66(5), 2002, 052301
    locator: the evolution of the string by the perpendicular force and the reparametrization by arc length
  - paper: doi:10.1063/1.2720838
    title: Weinan E, Weiqing Ren and Eric Vanden-Eijnden, Simplified and improved string method for computing the minimum energy paths in barrier-crossing events, Journal of Chemical Physics 126(16), 2007, 164103
    locator: the simplified method, with the full force followed by the reparametrization, and the interpolation step
  - paper: doi:10.1007/BF00547608
    title: Klaus Muller and Leo D. Brown, Location of saddle points and minimum energy paths by a constrained simplex optimization procedure, Theoretica Chimica Acta 53(1), 1979, 75-93
    locator: the two-dimensional test potential of the example
---

The string method finds a minimum energy path (MEP) between two minima of a potential energy: the curve on which the gradient is parallel to the curve at every point, and whose highest point is a saddle. It represents the path by a list of points, the images, and repeats two steps: every image takes a step of steepest descent, then the images are redistributed along the curve through them so that they are equally spaced in arc length. The second step cancels any motion along the curve, so the curve moves only across itself, until it lies in the bottom of the channel between the minima. Unlike the [nudged elastic band](/nudged-elastic-band/), it needs no springs and no projections of the force.

## In plain words

Lay a chain of beads across the hills between two valleys. Let every bead roll downhill for a short time. Most beads roll partly along the chain, and they bunch up at the bottom of the valleys.

So after each roll, slide the beads back along the chain until they are evenly spaced again. The slide only moves beads along the chain, so it does not change where the chain lies. What is left of each roll is the part across the chain. The chain moves sideways until rolling downhill only pushes the beads along it. Then it lies on the lowest route from one valley to the other. The two end beads roll into the bottoms of the valleys.

## The problem

The input is a potential $V: \mathbb{R}^d \to \mathbb{R}$ with its gradient, two points near two minima, and the number $N$ of segments. The output is a string $\varphi_0, \ldots, \varphi_N$ that approximates an MEP: a curve $\varphi$ with $(\nabla V)^{\perp} = 0$ along it, where $\perp$ is the part perpendicular to the tangent. The highest image approximates the saddle on the path. For atoms the coordinates are mass weighted if the masses differ; in the finite temperature version, the space is a set of [collective variables](/collective-variable/).

## The algorithm

```pseudo id=main
STRING-METHOD(V, a, b, N, h, tol)
L1  φ_i ← a + (i/N)(b - a) for i = 0, ..., N
L2  repeat
L3      φ*_i ← φ_i - h ∇V(φ_i) for i = 0, ..., N          ▷ evolve, the ends too
L4      s_0 ← 0, s_i ← s_{i-1} + |φ*_i - φ*_{i-1}|, α_i ← s_i / s_N
L5      φ_i ← the linear interpolation of the points (α_j, φ*_j) at α = i/N
L6  until max_i |φ_i (new) - φ_i (old)| / h < tol
L7  return φ_0, ..., φ_N
```

Line L3 moves every image by the full force $-\nabla V$, with a step $h$; any other ODE step works too. Line L4 computes the normalized arc length at each image of the evolved polygon. Line L5 puts the new images at equal arc length along this polygon. It is a linear interpolation, the simplest form of [Lagrange interpolation](/lagrange-interpolation/); a cubic spline in $\alpha$ is more accurate. The ends are not moved by line L5, so they do steepest descent on their own and fall into the two minima. Line L6 stops when the string no longer moves; the motion divided by $h$ is a force.

## Example

**A reparametrization by hand.** Take the polygon $(0, 0), (1, 0), (1, 2), (3, 2)$ with segment lengths $1, 2, 2$ and total length 5, so $\alpha = 0, 0.2, 0.6, 1$. With $N = 3$, the targets are $\alpha = 1/3$ and $2/3$. The first lies on the second segment at the fraction $(1/3 - 0.2)/0.4 = 1/3$, which is $(1, 2/3)$. The second lies on the third segment at $(2/3 - 0.6)/0.4 = 1/6$, which is $(4/3, 2)$. The new points are $(0, 0), (1, 2/3), (4/3, 2), (3, 2)$, each $5/3$ apart along the polygon.

**A path that is a circle.** For $V = 4(r - 1)^2 + \sin^2\theta$ in polar coordinates, the minima are $(\pm 1, 0)$, the saddles are $(0, \pm 1)$ with $V = 1$, and the MEP through $(0, 1)$ is the upper half of the unit circle. A string started on $y = 0.8 \sin(\pi i / N)$, with $h = 0.02$, converges in about 85 iterations. The middle image is at $(0, 1)$ to $10^{-7}$, with $V = 1$, by symmetry. The largest distance of an image from the circle is $0.0213$, $0.0095$ and $0.0036$ for $N = 8, 16, 32$. It falls roughly like $1/N$, because the linear interpolation shifts the images to the inside of the bend.

**The Muller-Brown surface.** From $A = (-0.55822, 1.44173)$ to $C = (-0.05001, 0.46669)$, with $h = 2 \times 10^{-4}$ and $\mathrm{tol} = 10^{-2}$, the ends stay at the two minima and the highest image is:

| $N$ | iterations | highest image | $V$ there |
|---|---|---|---|
| 8 | 120 | $(-0.8566, 0.7199)$ | $-44.319$ |
| 16 | 134 | $(-0.8178, 0.6223)$ | $-40.672$ |
| 32 | 121 | $(-0.8231, 0.6255)$ | $-40.666$ |

The saddle is $S1 = (-0.82200, 0.62431)$ with $V = -40.6648$. The straight line from A to C goes over a hill with $V = 3.39$, so the string moves far to find the path. The highest image approaches the saddle as $N$ grows; to locate the saddle exactly, interpolate $V$ along the string, or start a [dimer](/dimer-method/) search or a climbing image from the highest image.

## Correctness

The proof below makes three points. First, lines L4 and L5 put the images at exactly equal arc lengths on the evolved polygon, and keep the ends. Second, a motion along the string does not change the string after the reparametrization, so only the perpendicular part of the force moves it. The iteration is a splitting scheme for the string equation $\partial_t \varphi = -\nabla V(\varphi)^{\perp} + \lambda \hat\tau$ of the 2002 paper, where the tangential term $\lambda \hat\tau$ keeps the parametrization by arc length. Third, a curve is a stationary solution of this equation exactly when $\nabla V^{\perp} = 0$ along it, which is the definition of an MEP: the two terms are orthogonal, so both must vanish. The converged discrete string has an error that depends on $N$ and on the interpolation, as the circle example shows. The proof does not show that the iteration converges or which MEP it finds.

## Complexity

One iteration costs $N + 1$ gradients and $O(N d)$ arithmetic for the arc lengths and the interpolation, in the [real RAM](/real-ram/) model, and $O(N d)$ memory. The gradients are independent and run in parallel. The number of iterations is that of steepest descent on the perpendicular motion: the step must satisfy $h < 2 / \lambda_{\max}$ for the largest curvature, and the rate depends on the smallest curvature across the path. The reparametrization is cheap; with a cubic spline it is still $O(N d)$.

## Properties

- **No springs.** The spacing is set by the reparametrization, so there is no spring constant to choose and no interaction between the spacing and the force.
- **Any parametrization.** Equal arc length is one choice; a weight can put more images near the saddle, by targets $\alpha_i$ that are not equally spaced.
- **Simple to code.** An existing steepest descent or ODE step for single images is reused; only the interpolation is new.
- **Deterministic and local.** The same start gives the same path, and the string finds an MEP near its start.

## Variants and improvements

- **The original string method.** The 2002 method moves the images by the perpendicular force $-\nabla V^{\perp}$ and then reparametrizes. The simplified method of 2007 uses the full force, which removes the need for a tangent in the evolution step.
- **Higher order steps.** The evolution step can be a Runge-Kutta step or another ODE solver, and the interpolation a cubic spline, which improves the accuracy of the converged string.
- **Climbing string.** The highest image moves by the force with the parallel component inverted, as in the climbing image of NEB, to converge to the saddle exactly.
- **Finite temperature string method.** In a space of [collective variables](/collective-variable/), the images are averages over restrained [molecular dynamics](/molecular-dynamics/), and the string approximates a principal curve of the transition, with the free energy along it.
- **Swarms of trajectories.** This variant in collective variables moves each image by the mean drift of many short unbiased runs.

## When to use it

Use the string method when both end states are known and you want the MEP, in the same setting as the nudged elastic band. It is simpler to add to an existing code, and it is the base of the finite temperature methods in collective variables, which have a free energy along the path. Use the [dimer method](/dimer-method/) when only the initial state is known, and [transition path sampling](/transition-path-sampling/) when you need the dynamics of the transitions, not one path.

## Pitfalls

- **A step that is too large.** As for steepest descent, $h > 2 / \lambda_{\max}$ makes the stiff directions oscillate. On Muller-Brown, $\lambda_{\max} \approx 4068$ at the minimum A, so $h < 4.9 \times 10^{-4}$.
- **Too few images.** A coarse string cuts corners and its highest image is below the saddle, by 3.7 for $N = 8$ in the table.
- **Ends that are not minima.** If the ends start on the far side of a ridge, they fall into other minima, and the string joins the wrong states.
- **Intermediate minima.** If the MEP passes through another minimum, the string goes through it, and the highest image is the highest of the barriers on the way.
- **The interpolation error.** Linear interpolation shifts the images to the inside of a bend by an amount that falls only like $1/N$ in the example; use a spline when the path bends strongly.

## Implementations

## History

E, Ren and Vanden-Eijnden introduced the string method in 2002, as a method that evolves a curve by the perpendicular force and keeps its parametrization by an explicit reparametrization step instead of springs. In 2007 they gave the simplified and improved string method, which moves the images by the full force before the reparametrization. The same authors developed the finite temperature string method for transitions in collective variables.

## References
