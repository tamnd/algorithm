---
tag: 8XGGPB
kind: algorithm
slug: invertible-finite-elements
name: Invertible finite elements
aliases:
- diagonalized invertible FEM
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: Compute stresses in the diagonal space of the SVD of the deformation gradient, with a modified model, so that inverted elements recover their shape.
model: real-ram
complexity:
  vars: {n: "the number of nodes", m: "the number of elements"}
  time: {forces_per_step: "Θ(m)", explicit_step: "Θ(n + m)"}
  space: {extra: "Θ(n + m)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 2004
  people: [Geoffrey Irving, Joseph Teran, Ronald Fedkiw]
  note: Irving, Teran and Fedkiw computed the stress in the diagonal frame of a signed SVD and extended the constitutive models past the flat state, so that inverted elements get forces that restore them.
prereqs: [corotational-fem, neo-hookean-model, singular-value-decomposition]
see_also: [stable-neo-hookean, st-venant-kirchhoff-model, hyperelastic-material, deformation-gradient, finite-element-method, mass-spring-system, projective-dynamics, material-point-method]
sources:
  - paper: doi:10.1145/1028523.1028541
    title: Geoffrey Irving, Joseph Teran and Ronald Fedkiw, Invertible finite elements for robust simulation of large deformation, ACM SIGGRAPH/Eurographics Symposium on Computer Animation (SCA 2004), 131-140
    locator: Section 4 (force G = P B_m), Section 5 (diagonalization, Eq. 1, the sign rule for inverted elements), Section 6 and Figure 3 (the modified neo-Hookean and the rotated linear models)
  - paper: doi:10.1145/1073368.1073394
    title: Joseph Teran, Eftychios Sifakis, Geoffrey Irving and Ronald Fedkiw, Robust quasistatic finite elements and flesh simulation, ACM SIGGRAPH/Eurographics Symposium on Computer Animation (SCA 2005)
    locator: the definiteness fix of the stiffness in the diagonal frame for implicit and quasistatic solves (general locator)
  - paper: doi:10.1145/2343483.2343501
    title: Eftychios Sifakis and Jernej Barbič, FEM simulation of 3D deformable solids, a practitioner's guide to theory, discretization and model reduction, SIGGRAPH 2012 Courses, article 20
    locator: the isotropic stress from the singular values and the corotated model (general locator)
---

Invertible finite elements compute the elastic force of each element in a frame where its deformation is diagonal, so that the force stays finite and points back to the rest shape even when the element is flat or turned inside out.
Each [deformation gradient](/deformation-gradient/) is written as $F = U\hat F V^T$ with rotations $U$ and $V$ and a diagonal $\hat F$ whose smallest entry is negative when the element is inverted.
The stress of an isotropic model is diagonal in this frame, $P = U\hat P(\hat F)V^T$, and the model is changed below a compression threshold so that $\hat P$ is defined for every $\hat F$.
Irving, Teran and Fedkiw (2004) gave the method for tetrahedra, and the same steps work for triangles in 2D.

## In plain words

In a simulation with many small triangles or tetrahedra, some elements get crushed flat or pushed through themselves.
Many material models have no answer there: their energy goes to infinity, or their force pushes the element further inside out.
This method first finds two turns, one before and one after the stretch, that make the stretch of the element a plain scaling along two or three axes.
If the element is inside out, it marks this by making the smallest scaling negative.
It then asks the material model only about these scalings, and it changes the model where the scaling gets very small, so that the push back stays finite.
At last it turns the answer back into the world.
So every element gets a sensible force, and a crushed element unfolds again.

## The problem

The input is a mesh of triangles (in 2D) or tetrahedra (in 3D) with rest positions $X$, current positions $x$, and an isotropic hyperelastic model with the Lamé parameters $\mu$ and $\lambda$.
Each element has the rest edge matrix $D_m$ with $\det D_m > 0$, the current edge matrix $D_s$, $F = D_s D_m^{-1}$, and the rest area $V_0 = \det D_m / 2$.
The output is the elastic force on every node.

The force must be finite and must push toward the rest shape for every $x$, including elements with $\det F \le 0$.
It must be rotation invariant, and where the element is not too compressed it must agree with the chosen model.
A model such as the [neo-Hookean model](/neo-hookean-model/) has the energy term $-\mu\log J$ with $J = \det F$, which is undefined for $J \le 0$.
The [St. Venant-Kirchhoff model](/st-venant-kirchhoff-model/) is defined there, but its force can keep an inverted element inverted.

This page gives the method in 2D.
It uses two diagonal models: the corotated model $\hat P_i = 2\mu(\sigma_i - 1) + \lambda(\sigma_1 + \sigma_2 - 2)$, which the paper calls the rotated linear model, and the neo-Hookean model $\hat P_i = \mu\sigma_i - \mu/\sigma_i + \lambda\log(\sigma_1\sigma_2)/\sigma_i$.

## The algorithm

```pseudo id=main
INVERTIBLE-FORCES(x, c)                ▷ D_m^(-1) and B_m = -V_0 D_m^(-T) precomputed per element, c > 0
L1  f ← 0 on every node
L2  for each element e with nodes a_0, a_1, a_2 do
L3      F ← D_s D_m^(-1)
L4      (U, σ, V) ← signed SVD of F with det U = det V = +1, σ_1 ≥ |σ_2|
L5      σ̃_i ← max(σ_i, c) for each i
L6      P̂ ← P̂(σ̃) + J(σ̃)(σ - σ̃)         ▷ J is the Jacobian of P̂; the identity when σ̃ = σ
L7      P ← U diag(P̂) V^T
L8      G ← P B_m                          ▷ the forces on a_1 and a_2 as columns
L9      f_(a_k) ← f_(a_k) + G_k for k = 1, 2, and f_(a_0) ← f_(a_0) - G_1 - G_2
return f
```

Line L4 is the key step.
In 2D it has a closed form: with $e = (F_{00} + F_{11})/2$, $g = (F_{00} - F_{11})/2$, $h = (F_{10} + F_{01})/2$ and $k = (F_{10} - F_{01})/2$, set $q = \sqrt{e^2 + k^2}$, $r = \sqrt{g^2 + h^2}$, $\sigma_1 = q + r$ and $\sigma_2 = q - r$.
Then $U = \operatorname{rot}(\varphi)$ and $V = \operatorname{rot}(-\theta)$ with $\varphi + \theta = \operatorname{atan2}(k, e)$ and $\varphi - \theta = \operatorname{atan2}(h, g)$.
Since $\det F = q^2 - r^2$, $\sigma_2$ is negative exactly when the element is inverted.
In 3D, Irving et al. take an SVD from the eigenvectors of $F^T F$ and then fix the signs: if $\det V = -1$ they negate a column of $V$, and if $\det U = -1$ they negate the smallest entry of $\hat F$ and its column of $U$.

Lines L5 and L6 change the model below the threshold $c$: they replace the stress by its first order Taylor expansion about the clamped point.
The paper describes this choice as linearizing the model at a compression limit, or clamping the stress, and gives no value of $c$; the value is a tuning choice.
For the corotated model the stress is affine, so lines L5 and L6 change nothing.
Line L8 is the force formula $G = P B_m$ of Section 4 of the paper.
Any time integrator can use these forces; the test code uses [symplectic Euler](/symplectic-euler-method/) with velocity damping.

## Example

Take one triangle with the rest nodes $(0, 0)$, $(1, 0)$ and $(0, 1)$ in m, $E = 1$ Pa and $\nu = 0.3$, so $\mu = 5/13$ N/m and $\lambda = 15/26$ N/m, and $c = 0.3$. The table uses the six-place values $\mu = 0.384615$ N/m and $\lambda = 0.576923$ N/m, as the tests do, so its last digits can differ from the exact values by a few units (the extended neo-Hookean $\hat P_2$ at $(0, 0)$ is $-9.117844$ with the exact $\mu$ and $\lambda$).
Nodes 0 and 1 stay in place, and node 2 moves down.

| Node 2 at | $\det F$ | $(\sigma_1, \sigma_2)$ | plain neo-Hookean $\hat P_2$ | extended neo-Hookean $\hat P_2$ | force on node 2, extended neo-Hookean (N) | force on node 2, corotated (N) |
|---|---|---|---|---|---|---|
| $(0, 1)$ | 1 | $(1, 1)$ | 0 | 0 | $(0, 0)$ | $(0, 0)$ |
| $(0, 0.5)$ | 0.5 | $(1, 0.5)$ | $-1.376708$ | $-1.376708$ | $(0, 0.688354)$ | $(0, 0.336538)$ |
| $(0, 0.1)$ | 0.1 | $(1, 0.1)$ | $-17.091831$ | $-7.239226$ | $(0, 3.619613)$ | $(0, 0.605769)$ |
| $(0, 0)$ | 0 | $(1, 0)$ | undefined | $-9.117841$ | $(0, 4.558920)$ | $(0, 0.673076)$ |
| $(0, -0.5)$ | $-0.5$ | $(1, -0.5)$ | undefined | $-18.510913$ | $(0, 9.255456)$ | $(0, 1.009615)$ |
| $(0.3, -0.5)$ | $-0.5$ | $(1.056401, -0.473305)$ | undefined | $-17.631926$ | $(1.757483, 8.040864)$ | $(0.292784, 0.872589)$ |

Above the threshold the extended and the plain stresses agree.
Below it the plain neo-Hookean stress grows without bound and is undefined at and past the flat state, while the extended stress continues along a straight line.
In every row the force on node 2 points up, so it unfolds the triangle, also when the triangle is flat or inverted.
In the last row $F$ is not diagonal, and the signed SVD finds the rotations; the negative entry is still the one of smallest magnitude.
That force also has a part along $+x$, because the diagonal frame is turned; the damped run of the test code still brings node 2 back to $(0, 1)$.

## Correctness

The [proof](proofs/correctness.md) shows these facts, each a proved property.

- Line L4 gives $F = U\hat F V^T$ with rotations $U$, $V$, $\sigma_1 \ge |\sigma_2|$, and $\sigma_2 < 0$ exactly when $\det F < 0$.
- When $\sigma_1 + \sigma_2 \ne 0$, the stress of line L7 does not depend on which such SVD is used, so it is a function of $F$. It is rotation equivariant: $P(QFQ') = Q P(F) Q'$ for rotations $Q$ and $Q'$, and it is zero at every rotation.
- The extension of lines L5 and L6 is finite for every $F$ and has continuous first derivatives at $\sigma_i = c$.
- For the corotated model, the force is the exact negative gradient of $\sum_e V_0(\mu|F - R|_F^2 + \frac{\lambda}{2}\operatorname{tr}(S - I)^2)$ with $R = UV^T$ and $S = V\hat F V^T$, for inverted elements too. In 2D this energy is $\mu(|F|_F^2 - 4q + 2) + 2\lambda(q - 1)^2$, smooth wherever $q > 0$.
- For the neo-Hookean model, the force is the exact negative gradient of the neo-Hookean energy while all $\sigma_i \ge c$. Below $c$ the extended force is not the gradient of any energy.
- The net force and the net torque of each element are zero for every diagonal $\hat P$, because $F P^T = U\hat F\hat P U^T$ is symmetric.

The key step is the sign rule of line L4: the rotations $U$ and $V$ carry no reflection, so the inversion shows up as a negative $\sigma_2$, where the diagonal model can see it and push against it.

## Complexity

Each element costs a constant amount of work: a closed form SVD in 2D (in 3D, a 3 by 3 symmetric eigenproblem) and a few small matrix products.
So the forces cost $\Theta(m)$ for $m$ elements, and an explicit step costs $\Theta(n + m)$ for $n$ nodes.
Memory is $\Theta(n + m)$: $D_m^{-1}$, $B_m$ and $V_0$ per element and the state per node.
An implicit step also needs the stiffness, which in the diagonal frame splits into small blocks; see the variants.

## Properties

- **Defined everywhere but a thin set.** The force is finite for every configuration, and it is a function of $F$ wherever $\sigma_1 + \sigma_2 \ne 0$. This is proved.
- **Rotation invariant and isotropic.** Rotating the world or the rest shape rotates the stress, and a rigid motion gives no force. This is proved.
- **Same as the model where it matters.** For $\sigma_i \ge c$ the stress is the stress of the chosen model. This is proved.
- **Not conservative below $c$.** The extended neo-Hookean force is not the gradient of an energy in the extended region, so an energy based integrator or a line search on the energy does not apply there. This is proved.
- **Recovery.** In the diagonal models of this page an inverted element is pushed back. That a mesh recovers from a given crushed state is a measurement: in the test code a triangle with node 2 at $(0.3, -0.5)$, a flat triangle, and a 2 by 2 grid with three inverted triangles all return to rest under damped symplectic Euler.
- **A modelling choice.** The change of the model below $c$ is a heuristic. It is not a law of physics, and Irving et al. note that most models lose accuracy long before inversion.

## Variants and improvements

- **Other diagonal models.** Any isotropic model in terms of the singular values can be used, for example a model with a cubic spline between threshold values, which the paper uses for a volumetric Buddha model, or the corotated model, which needs no change at all.
- **Definite stiffness.** Teran, Sifakis, Irving and Fedkiw (2005) used the diagonal frame to split the stiffness of each element into small blocks and to make each block positive definite. This gives a robust implicit and quasistatic solver.
- **Inversion-safe energies.** The [stable neo-Hookean model](/stable-neo-hookean/) of Smith, de Goes and Kim (2018) is defined for inverted elements without any threshold, so its force stays the gradient of an energy.
- **Anisotropy.** For an anisotropic model $\hat P$ is not diagonal. Section 6.1 of the paper rotates the anisotropic terms into the diagonal frame.
- **Other discretizations.** [Projective dynamics](/projective-dynamics/) projects each element onto rotations, and the [material point method](/material-point-method/) often applies a signed SVD to the deformation gradient of each particle.

## When to use it

Use invertible elements whenever a mesh can be crushed: collisions with thin objects, coarse meshes of soft tissue, or large time steps.
Use it with the corotated model if speed matters more than the response at large strain, and with an extended neo-Hookean or a similar model for rubbery materials.
If an implicit solver needs a smooth energy everywhere, use the [stable neo-Hookean model](/stable-neo-hookean/) instead of a model with a threshold.
For cloth and shells in 3D the triangles cannot invert, and the plain [finite element method](/finite-element-method/) is enough.

## Pitfalls

- **Unsigned SVD.** A standard SVD returns $\sigma_i \ge 0$ and lets $U$ or $V$ be a reflection. With line L4 written that way, an inverted element looks like an uninverted one, and the force keeps it inverted. Both $U$ and $V$ must be rotations.
- **The wrong entry negated.** In line L4 the negative entry must be the one of smallest magnitude. Negating another entry gives a valid factorization, but it asks for the long way back and gives large forces.
- **Evaluating the model at $\sigma \le 0$.** Without lines L5 and L6, the neo-Hookean $\hat P$ takes $\log$ of a negative number. A threshold of $c = 0$ does not help, because the stress is infinite there.
- **A threshold that is too small.** For a small $c$ the slope $J(\tilde\sigma)$ of line L6 is very large, so the extended force is very stiff and an explicit step needs a much smaller $\Delta t$.
- **Treating the extended force as conservative.** Below $c$ the force of line L6 is not the gradient of an energy. A Newton solver that checks the energy, or an energy diagnostic, gives wrong results there.
- **Using $U V^T$ as the polar rotation of an inverted element.** For $\det F < 0$, $R = UV^T$ is a rotation but $S = V\hat F V^T$ is not positive definite, so it is not the polar decomposition of line L5 in [corotational finite elements](/corotational-fem/). The corotated force is correct with it; formulas that assume a positive $S$ are not.

## Implementations

## History

Before 2004, simulations in graphics used springs or an extra volume term to resist inversion, or turned to a linear model in a rotated frame, which works for inverted elements but limits the material.
Irving, Teran and Fedkiw (2004) diagonalized $F$ with rotations, put the sign of the inversion on the smallest entry, and extended the constitutive models past the flat state with $C^0$ or $C^1$ continuity.
Teran, Sifakis, Irving and Fedkiw (2005) used the same frame to build a positive definite stiffness for implicit and quasistatic solves.
Sifakis and Barbič (2012) explain the corotated model and the stress from the singular values in their course notes, and Smith, de Goes and Kim (2018) designed an energy that needs no threshold.

## References
