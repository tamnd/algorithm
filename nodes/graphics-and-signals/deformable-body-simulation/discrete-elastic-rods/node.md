---
tag: 56ZBR0
kind: algorithm
slug: discrete-elastic-rods
name: Discrete elastic rods
aliases:
- DER
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: Simulate hair and cables as a polyline with a bending energy from discrete curvature and a twist energy measured against a parallel transported frame.
model: real-ram
complexity:
  vars: {n: "the number of edges of the rod"}
  time: {forces_per_step: "Θ(n)"}
  space: {extra: "Θ(n)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 2008
  people: [Miklós Bergou, Max Wardetzky, Stephen Robinson, Basile Audoly, Eitan Grinspun]
  note: Bergou et al. built a discrete Kirchhoff rod from the curvature binormal of a polyline and a twist measured against the Bishop frame, with the exact gradient of the twist through the holonomy.
prereqs: [cosserat-rod, rotation-minimizing-frame]
see_also: [double-reflection-method, frenet-frame, mass-spring-system, cloth-simulation, discrete-shells, position-based-dynamics, symplectic-euler-method, finite-difference-method]
sources:
  - paper: doi:10.1145/1360612.1360662
    title: Miklós Bergou, Max Wardetzky, Stephen Robinson, Basile Audoly and Eitan Grinspun, Discrete elastic rods, ACM Transactions on Graphics 27(3), article 63 (SIGGRAPH 2008)
    locator: the curvature binormal, the Bishop frame, the quasistatic twist and the gradient of the holonomy (general locator)
  - paper: doi:10.1145/1778765.1778853
    title: Miklós Bergou, Basile Audoly, Etienne Vouga, Max Wardetzky and Eitan Grinspun, Discrete viscous threads, ACM Transactions on Graphics 29(4) (SIGGRAPH 2010)
    locator: the reference frame carried by parallel transport in time (general locator)
---

Discrete elastic rods model a thin elastic rod, such as a hair, a cable or a thread, as a polyline with a twist angle on each edge.
The bending energy at each interior vertex uses the curvature binormal

$$\kappa b_i = \frac{2\, e^{i-1} \times e^i}{|e^{i-1}||e^i| + e^{i-1} \cdot e^i},$$

and the twist is measured against the Bishop frame, the frame of the first edge carried along the rod by parallel transport.
When the centerline moves, the Bishop frame at the far end turns by the holonomy, so bending and twisting are coupled.
Bergou, Wardetzky, Robinson, Audoly and Grinspun (2008) gave the method, with the exact gradient of this coupling.

## In plain words

A hair or a cable is long and thin, so it is drawn as a chain of short straight pieces.
It resists bending at each joint, and it resists twisting along its length.
Bending is easy to measure: look at the angle between the two pieces at a joint.
Twisting is harder, because a chain has no natural "up" direction.
The method makes one by sliding a marker along the chain without spinning it.
The twist is how far the real end of the cable has turned compared with that marker.
A strange fact follows: if you bend the chain into a loop in space, the marker comes back turned.
So bending the cable changes its twist, and a twisted cable wants to bend.
The method computes this effect exactly, at low cost.

## The problem

The input is a rod with the vertices $x_0, \dots, x_n$, the edges $e^j = x_{j+1} - x_j$, and the rest edges $\bar e^j$.
This page treats an isotropic rod that is straight at rest, with the bending stiffness $\alpha$ (EI, in N m²), the twisting stiffness $\beta$ (GJ, in N m²), and a stretching penalty $k_s$ in N.
The rod is clamped at both ends: the first two and the last two vertices are fixed, the material director $u^0$ of edge 0 is given, and the material director $d_{end}$ of the last edge is given.
The output is the force on every vertex and a time step.

The energy is

$$E = \sum_j \tfrac{k_s}{2}|\bar e^j|\Bigl(\tfrac{|e^j|}{|\bar e^j|} - 1\Bigr)^2 + \sum_i \frac{\alpha|\kappa b_i|^2}{\bar l_i} + \frac{\beta\,\Delta\theta^2}{\bar L},$$

with $\bar l_i = |\bar e^{i-1}| + |\bar e^i|$ and $\bar L = \sum_i \bar l_i$.
The last term is the quasistatic twist: the material frames of the interior edges are at their minimum, so the total twist $\Delta\theta$ spreads along the rod in proportion to $\bar l_i$.
$\Delta\theta$ is the angle about the last tangent from the Bishop director $u^{n-1}$ to $d_{end}$.
The paper writes the bending term with natural curvatures and material curvatures for rods that are curved or not round at rest; constant factors in $\alpha$ differ between conventions.
With the $\bar l_i$ above, $\alpha$ equals the EI of a beam (see Properties).

## The algorithm

```pseudo id=main
DER-STEP(x, v, Δθ_prev, Δt)            ▷ u^0, d_end, l̄_i, L̄ fixed; ends clamped
L1  e^j ← x_(j+1) - x_j for each edge j
L2  κb_i ← 2 e^(i-1) × e^i / (|e^(i-1)||e^i| + e^(i-1)·e^i) for each interior vertex i
L3  u^j ← P(t^(j-1) → t^j) u^(j-1) for j = 1, ..., n-1       ▷ parallel transport
L4  Δθ ← signed angle from u^(n-1) to d_end about t^(n-1), nearest to Δθ_prev
L5  f ← -∇E_stretch
L6  f_k ← f_k - (2α / l̄_i) (∂κb_i/∂x_k)^T κb_i for k = i-1, i, i+1, each interior i
L7  f_k ← f_k + (2βΔθ / L̄) ∇_k ψ_i for k = i-1, i, i+1, each interior i
L8  v ← v + Δt M^(-1) f, x ← x + Δt v on the free vertices
return x, v, Δθ
```

Line L3 uses the minimal rotation $P(t_1 \to t_2) = cI + [b] + bb^T/(1 + c)$, with $c = t_1 \cdot t_2$, $b = t_1 \times t_2$ and $[b]y = b \times y$.
Line L4 counts full turns by taking the angle nearest to the value of the previous step.
Line L6 uses the Jacobians of $\kappa b$ with respect to the two edges $a = e^{i-1}$ and $b = e^i$,

$$\frac{\partial\kappa b}{\partial a} = \frac{-2[b] - \kappa b\,(|b|\,a/|a| + b)^T}{D}, \qquad \frac{\partial\kappa b}{\partial b} = \frac{2[a] - \kappa b\,(|a|\,b/|b| + a)^T}{D}, \qquad D = |a||b| + a \cdot b.$$

Line L7 is the twist force through the holonomy: $\nabla_{i-1}\psi_i = \kappa b_i/(2|e^{i-1}|)$, $\nabla_{i+1}\psi_i = -\kappa b_i/(2|e^i|)$ and $\nabla_i\psi_i = -(\nabla_{i-1}\psi_i + \nabla_{i+1}\psi_i)$.
Line L8 is a [symplectic Euler](/symplectic-euler-method/) step with lumped masses; the paper also enforces the edge lengths with a projection, and the stretching penalty of line L5 stands in for it here.

## Example

Take five vertices $(0, 0, 0)$, $(1, 0, 0)$, $(1, 1, 0)$, $(1, 1, 1)$ and $(2, 1, 1)$ in m, a straight rest shape with unit edges, $\alpha = \beta = 1$ N m², and $u^0 = d_{end} = (0, 0, 1)$.
The rod turns by 90 degrees at each of the three interior vertices, and its last edge is parallel to its first.
So $\bar l_i = 2$ m and $\bar L = 6$ m.

| Edge or vertex | Tangent $t^j$ | Bishop director $u^j$ | $\kappa b_i$ at the vertex after the edge | $|\kappa b_i|$ |
|---|---|---|---|---|
| edge 0 | $(1, 0, 0)$ | $(0, 0, 1)$ | $(0, 0, 2)$ | 2 |
| edge 1 | $(0, 1, 0)$ | $(0, 0, 1)$ | $(2, 0, 0)$ | 2 |
| edge 2 | $(0, 0, 1)$ | $(0, -1, 0)$ | $(0, 2, 0)$ | 2 |
| edge 3 | $(1, 0, 0)$ | $(0, -1, 0)$ | none | none |

Each turn of 90 degrees gives $|\kappa b| = 2\tan 45° = 2$, so the bending energy is $3 \cdot 4/2 = 6$ J.
The last edge points the same way as the first, but the Bishop director came back turned by 90 degrees: it is $(0, -1, 0)$, not $(0, 0, 1)$.
This turn is the holonomy of the path.
So the clamp $d_{end} = (0, 0, 1)$ is twisted by $\Delta\theta = -\pi/2$ relative to the Bishop frame, and the twist energy is $(\pi/2)^2/6 = 0.411234$ J, although the two clamps point the same way.
A planar rod never shows this effect: the director that starts normal to the plane stays normal to it.

## Correctness

The [proof](proofs/correctness.md) shows that lines L5 to L7 return the exact negative gradient of $E$.
These are proved properties.

- $|\kappa b_i| = 2\tan(\varphi_i/2)$ for the turning angle $\varphi_i$, and $\kappa b_i$ is perpendicular to both edges.
- Line L3 is the rotation about $t^{j-1} \times t^j$ that takes $t^{j-1}$ to $t^j$.
- **The key step.** Write the transport as the product of two reflections, $P = H_m H_{t_1}$ with the bisector $m$ of $t_1$ and $t_2$. Then the rate at which a variation turns the transported frame about the tangent is $-\frac12\kappa b \cdot (\delta t_1 + \delta t_2)$ at each vertex. Summed along the rod this is the holonomy, and it gives the formulas of line L7.
- The quasistatic twist energy $\beta\Delta\theta^2/\bar L$ is the minimum of $\sum_i \beta(\theta^i - \theta^{i-1})^2/\bar l_i$ over the interior angles, by the Cauchy-Schwarz inequality.
- The energy does not change under rigid motions, so the net force and the net torque of a free rod are zero, and a straight rod has no force for any twist.

The twist term needs the first and the last edges to be fixed; the proof uses this to keep $u^0$ and $d_{end}$ fixed.

## Complexity

Each line touches each edge or vertex a constant number of times, so one step costs $\Theta(n)$ time.
Line L4 needs the whole transport of line L3, which is also $\Theta(n)$.
Memory is $\Theta(n)$ for the positions, the velocities, the rest lengths and the frames.
An implicit step needs the Hessian, which is banded with a constant band width, so a direct banded solve also costs $\Theta(n)$ per Newton iteration.
An explicit step is cheap but its stable time step shrinks with the edge length: for bending, the highest frequency grows like $1/h^2$ for edge length $h$.

## Properties

- **Frame invariant.** A rigid motion of the rod and of both clamps does not change the energy or the twist. This is proved.
- **Exact forces.** The forces are the exact gradient, including the coupling of twist and bending through the holonomy. This is proved.
- **No holonomy in a plane.** For a planar rod, $\Delta\theta$ depends only on the clamps. This is proved (a planar rod transports the plane normal to itself).
- **Bending stiffness.** For a small turn $\varphi$ at a vertex between edges of length $h$, $|\kappa b|^2 \approx \varphi^2$ and the discrete energy is $\alpha\varphi^2/(2h)$, the energy $\frac12 EI\kappa^2 h$ of a beam with $\kappa = \varphi/h$, so $\alpha = EI$. This is a proved limit.
- **First order convergence of a cantilever.** A rod of length 0.9 m, clamped at one end, with $\alpha = 1$ N m² under a load of 0.1 N/m, has the tip deflection 0.0082 m by Euler-Bernoulli beam theory. The rod settles at 0.0118 m with 5 free edges and at 0.0099 m with 10, so the error falls by about half when $h$ halves. This is a measurement on the test code.
- **Not a law.** The rod model is the Kirchhoff model of an inextensible, unshearable rod. The penalty $k_s$ of this page and the damping are tuning.

## Variants and improvements

- **Natural curvature and anisotropy.** Bergou et al. (2008) store the material curvatures $(\kappa b \cdot m_2, -\kappa b \cdot m_1)$ in the material frame and compare them with their rest values, which gives curly hair and ribbons. The twist angles of the edges are then degrees of freedom, solved quasistatically or in time.
- **Time parallel reference frame.** Bergou et al. (2010) carry the reference frame of each edge forward in time by parallel transport from its previous direction, not along the rod in space. This keeps each update local and avoids the $\Theta(n)$ dependence of the twist on the far end.
- **Inextensibility.** The paper projects the vertex positions onto constant edge lengths after each step. [Position based dynamics](/position-based-dynamics/) uses a similar projection.
- **Cosserat rods.** A [Cosserat rod](/cosserat-rod/) also allows stretching and shearing, with an independent frame at each point.
- **Frames.** The Bishop frame is a [rotation minimizing frame](/rotation-minimizing-frame/), and the [double reflection method](/double-reflection-method/) computes a similar frame on sampled curves. The [Frenet frame](/frenet-frame/) is undefined where the curve is straight, so it is not used.

## When to use it

Use discrete elastic rods for hair, fur, cables, ropes, knots and threads, where twist matters and the rod is thin enough that it does not shear.
For many hairs, use the reduced cost variants with the time parallel reference frame and an implicit solver.
If twist does not matter, a chain of springs with bending springs, as in a [mass spring system](/mass-spring-system/), is simpler.
For thick or soft rods that stretch and shear, use a [Cosserat rod](/cosserat-rod/) model.

## Pitfalls

- **Using the turning angle as the curvature.** Line L2 uses $2\tan(\varphi/2)$, not $\varphi$. Mixing the two changes the energy at large turns and breaks the gradient of line L6.
- **Dropping the holonomy.** With line L7 missing, the twist of a clamped rod never makes it bend, and a twisted cable never forms loops. The forces are then not the gradient of the energy.
- **Wrapping the twist.** The angle of line L4 is only known modulo $2\pi$. Taking it in $(-\pi, \pi]$ at each step loses full turns; keep the value nearest to the previous one.
- **Transport between opposite tangents.** Line L3 divides by $1 + t^{j-1} \cdot t^j$, which is zero when the rod folds back on itself. Keep the time step small enough that no vertex turns by close to 180 degrees.
- **Moving the clamped edges.** The twist force of line L7 assumes that the first and the last edges are fixed. If an end is free, the quasistatic twist is zero and line L7 must be left out.
- **Too large a time step.** Line L8 is explicit, and bending is stiff on short edges. Halving the edge length needs about a quarter of the time step.

## Implementations

## History

Kirchhoff's rod theory of the 19th century describes an inextensible rod by its bending and twisting, and Cosserat rods (1909) add stretching and shearing.
In graphics, hair was long simulated with chains of springs or of rigid links.
Bergou, Wardetzky, Robinson, Audoly and Grinspun (2008) built a discrete rod from discrete differential geometry: the curvature binormal, the Bishop frame and its holonomy, with forces that are exact gradients.
Bergou, Audoly, Vouga, Wardetzky and Grinspun (2010) changed the reference frame to one carried in time and added viscous threads.

## References
