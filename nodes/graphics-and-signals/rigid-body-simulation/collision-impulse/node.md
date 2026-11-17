---
tag: RVWXT5
kind: algorithm
slug: collision-impulse
name: Impulse-based collision response
aliases:
- collision impulse
area: graphics-and-signals/rigid-body-simulation
level: intro
summary: Change the velocities of two colliding rigid bodies by an impulse along the contact normal whose size makes the restitution law hold.
solves: [rigid-body-simulation-problem]
model: real-ram
complexity:
  vars: {c: the number of contact points that are processed one at a time}
  time: {one_contact: O(1), one_pass: O(c)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, recursive: false, in_place: true}
history:
  year: 1988
  people: [James K. Hahn, Matthew Moore, Jane Wilhelms, David Baraff]
  note: The impulse of a frictionless collision is classical impact mechanics. Hahn (1988) and Moore and Wilhelms (1988) used impulses for rigid body collisions in computer animation, and Baraff's SIGGRAPH course notes give the formula in the form that most engines use.
prereqs: [contact-manifold, coefficient-of-restitution, newton-euler-equations, cross-product]
see_also: [impulse-based-simulation, projected-gauss-seidel, baraff-contact-force-algorithm, coulomb-friction-law, friction-cone, painleve-paradox, continuous-collision-detection, rigid-body-simulation-problem]
sources:
  - url: https://www.cs.cmu.edu/~baraff/sigcourse/notesd2.pdf
    title: "David Baraff, An Introduction to Physically Based Modeling: Rigid Body Simulation II, Nonpenetration Constraints, in Andrew Witkin and David Baraff, Physically Based Modeling: Principles and Practice, SIGGRAPH 97 course notes"
    locator: "Section 8, Colliding Contact: the relative velocity (8-3), Newton's law of restitution (8-10) and the impulse formula (8-18)"
  - paper: doi:10.1145/54852.378530
    title: "James K. Hahn, Realistic animation of rigid bodies, SIGGRAPH 88, Computer Graphics 22(4), 299-308, 1988"
    locator: the impulse-based treatment of collisions between rigid bodies
  - paper: doi:10.1145/54852.378528
    title: "Matthew Moore and Jane Wilhelms, Collision detection and response for computer animation, SIGGRAPH 88, Computer Graphics 22(4), 289-298, 1988"
    locator: the analytical collision response for rigid bodies
  - paper: doi:10.1145/199404.199436
    title: "Brian Mirtich and John Canny, Impulse-based simulation of rigid bodies, Proceedings of the 1995 Symposium on Interactive 3D Graphics, 181-188"
    locator: "Section 4, Computing collision impulses (the frictional version of the impulse, integrated along the collision)"
---

The collision impulse is the change of momentum that resolves a collision between two [rigid bodies](/rigid-body-simulation-problem/) at one contact point in one instant. It acts along the contact normal, and its size is chosen so that the normal relative velocity after the collision is $-e$ times the one before it, which is Newton's law with the [coefficient of restitution](/coefficient-of-restitution/) $e$. The formula takes the masses, the inertia tensors and the lever arms of both bodies into account, so a hit away from the center of mass makes the body spin. This page treats the frictionless case; friction is a variant.

## In plain words

Two objects hit each other at a point. In a real collision they press together for a very short time, and a large force pushes them apart. A simulation does not follow that short time. It replaces the whole push by one jump in the velocities, called an impulse.

The direction of the push is the direction that points straight out of the contact surface. The strength of the push is the only unknown. Pick it so that the two touching points separate at a given fraction of their approach speed: all of it for a perfect bounce, none of it for a dead stop.

The push changes how fast each object moves and how fast it spins. A light object reacts more than a heavy one. An object that is hit far from its center turns more. The formula adds up these effects to find the strength.

## The problem

At an instant $t_0$, two bodies $A$ and $B$ touch at the point $p$ with the unit normal $n$, which points from $B$ to $A$ (the convention of Baraff's notes). Body $X$ has its center of mass $x_X$, linear velocity $v_X$, angular velocity $\omega_X$, mass $m_X$ and world inertia tensor $I_X = R_X I_{body,X} R_X^T$. A static body, such as the ground, has $m_X^{-1} = 0$ and $I_X^{-1} = 0$. Let $r_X = p - x_X$. The velocity of the material point of $X$ at $p$ is $v_X + \omega_X \times r_X$, and the relative normal velocity is

$$v_{rel} = n \cdot \big((v_A + \omega_A \times r_A) - (v_B + \omega_B \times r_B)\big).$$

If $v_{rel} < 0$, the bodies approach and the contact is a collision. The output is the impulse $j n$ on $A$ and $-j n$ on $B$, with $j \ge 0$, and the new velocities, such that $v_{rel}^+ = -e\, v_{rel}^-$ for the given $e \in [0, 1]$. Positions do not change during the collision. Newton's law of restitution is an empirical model, and $e$ is a measured value for a pair of materials; see [coefficient of restitution](/coefficient-of-restitution/).

## The algorithm

```pseudo id=main
COLLISION-IMPULSE(A, B, p, n, e)
L1  r_A ← p - x_A;  r_B ← p - x_B
L2  v_rel ← n · ((v_A + ω_A × r_A) - (v_B + ω_B × r_B))
L3  if v_rel ≥ 0 then return 0                 ▷ not approaching: no impulse
L4  k ← 1/m_A + 1/m_B + n · ((I_A⁻¹ (r_A × n)) × r_A) + n · ((I_B⁻¹ (r_B × n)) × r_B)
L5  j ← -(1 + e) v_rel / k
L6  v_A ← v_A + (j / m_A) n;  ω_A ← ω_A + I_A⁻¹ (r_A × j n)
L7  v_B ← v_B - (j / m_B) n;  ω_B ← ω_B - I_B⁻¹ (r_B × j n)
L8  return j
```

Line L4 computes $k$, the change of $v_{rel}$ per unit of impulse. It is the inverse of the effective mass of the contact along $n$. Each rotation term equals $(r_X \times n)^T I_X^{-1} (r_X \times n)$, so it is never negative, and it is zero when the normal passes through the center of mass. Line L5 is the only solve: $v_{rel}$ is linear in $j$, so one division gives the exact value. Lines L6 and L7 apply equal and opposite impulses.

## Example

A box of mass $m = 1$ with sides 2, 1 and 1 along its own x, y and z axes has $I_{body} = \mathrm{diag}(1/6, 5/12, 5/12)$. It is turned about the z axis by the angle with $\cos = 4/5$ and $\sin = 3/5$, so that its lowest edge is parallel to z. Take the midpoint of that edge as the contact point: $r_A = (-1/2, -1, 0)$. The ground is static with $n = (0, 1, 0)$. The box moves with $v_A = (1, -2, 0)$ and $\omega_A = 0$, and $e = 1/2$.

| step | value |
|---|---|
| L2 | $v_{rel} = -2$ |
| L4 | $r_A \times n = (0, 0, -1/2)$, rotation term $= (1/2)^2 \cdot 12/5 = 3/5$, so $k = 1 + 3/5 = 8/5$ |
| L5 | $j = -(3/2)(-2) / (8/5) = 15/8$ |
| L6 | $v_A^+ = (1, -1/8, 0)$, $\omega_A^+ = (0, 0, -9/4)$ |
| after | contact point velocity $(-5/4, 1, 0)$, so $v_{rel}^+ = 1 = -e\, v_{rel}^-$ |

Only $(I^{-1})_{zz} = 12/5$ enters, because $r_A \times n$ is along z. The kinetic energy goes from $5/2$ to $25/16$. The loss $15/16$ equals $(1 - e^2) v_{rel}^2 / (2k) = (3/4) \cdot 4 / (16/5)$. The tangential velocity of the contact point changes from $1$ to $-5/4$, although the impulse is purely normal: the spin that the impulse starts moves the contact point sideways.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). By the [Newton-Euler equations](/newton-euler-equations/) integrated over a vanishing time, an impulse $J$ at $p$ changes $v_X$ by $J / m_X$ and $\omega_X$ by $I_X^{-1}(r_X \times J)$. These changes are linear in $J$, so $v_{rel}^+ = v_{rel}^- + j k$, and line L5 gives $v_{rel}^+ = -e\, v_{rel}^-$. These are proved properties of the model:

- Linear momentum and angular momentum about any fixed point are conserved, because the two impulses are equal, opposite and act at the same point.
- The kinetic energy drops by exactly $(1 - e^2) v_{rel}^2 / (2k)$. So $e = 1$ keeps the energy, and $e = 0$ leaves $v_{rel}^+ = 0$.
- $k > 0$ when at least one body is not static, so line L5 is defined.

## Complexity

One call does a fixed number of cross products, dot products and 3 by 3 matrix-vector products: $O(1)$ time and $O(1)$ extra space in the real RAM. The inverse world inertia $I^{-1} = R I_{body}^{-1} R^T$ is computed once per body per step. A pass over $c$ contacts costs $O(c)$. A pass is not a full solve when contacts interact (see Pitfalls); repeated passes are [projected Gauss-Seidel](/projected-gauss-seidel/), and their number is a measurement unless a convergence bound applies.

## Properties

- Exact in exact arithmetic: one linear equation in one unknown.
- Conserves linear and angular momentum for any $e$, and kinetic energy for $e = 1$.
- Never pulls: the result $j$ is $\ge 0$, and a separating contact gets no impulse.
- Local: it uses only the two bodies at the contact.
- Positions do not change, so a collision response does not remove an overlap. That is the job of the collision detection and of position correction such as [Baumgarte stabilization](/baumgarte-stabilization/).

## Variants and improvements

- **Friction.** With [Coulomb friction](/coulomb-friction-law/), the impulse has a tangential part. The simple version computes the impulse that stops the tangential motion and clamps it to the [friction cone](/friction-cone/) $|j_t| \le \mu j_n$. Mirtich and Canny integrate the impulse along the collision, so that sliding can stop or change direction during the collision; see [impulse-based simulation](/impulse-based-simulation/). With friction the energy statement above does not hold as stated; the coefficient of restitution page has an example in which Newton's law plus a sticking impulse adds energy.
- **Poisson and Stronge.** Instead of Newton's law on velocities, Poisson's hypothesis sets the normal impulse to $(1 + e)$ times the impulse at maximum compression, and Stronge's energetic coefficient compares the work of the normal force in the two phases. Without friction, the three give the same impulse as this page.
- **Several contacts at once.** The impulses of simultaneous contacts are coupled. They solve a [linear complementarity problem](/linear-complementarity-problem/), which [projected Gauss-Seidel](/projected-gauss-seidel/) solves by repeated calls of this formula, and a pivoting method such as [Baraff's algorithm](/baraff-contact-force-algorithm/) solves exactly for forces.
- **2D.** In the plane, $\omega$ is a scalar, $r \times n$ is the scalar $r_x n_y - r_y n_x$, and the rotation term of L4 is $(r \times n)^2 / I$.

## When to use it

Use it for the response to a collision at one point, between bodies with known masses and inertia, when the collision is short compared with the time step. It is the inner step of [impulse-based simulation](/impulse-based-simulation/) and of iterative velocity solvers. For a body that rests on several points, or a stack, one call per contact is not enough; use an iterative solver with accumulated impulses, or a complementarity solver.

## Pitfalls

- **Normal direction.** The formula assumes that $n$ points from $B$ to $A$, with the impulse $+j n$ on $A$. With the opposite normal and the same signs, the impulse pulls the bodies together.
- **Missing L3.** Without the test for separation, a contact that is already separating gets an impulse, and resting bodies stick to each other.
- **Body inertia instead of world inertia.** $I^{-1}$ must be $R I_{body}^{-1} R^T$ for the current orientation. With $I_{body}^{-1}$, the spin is wrong for any rotated body.
- **One contact at a time.** A 2D box of mass 1 with sides 2 and 1 lands flat on its two bottom corners with speed 1 m/s. With $e = 0$, one pass over the two corners leaves $v_y = -84/289$ and $\omega_z = 84/289$, and the first corner still approaches; each further pass multiplies the velocities by $49/289$, so the passes converge to rest only in the limit. With $e = 1$, the first corner still approaches after one pass, and after the second pass both corners separate with $v_y = 4697/4913$ and $\omega_z = 2232/4913$. The kinetic energy is still $1/2$, but part of it is now spin, while the symmetric answer is $v_y = 1$ and $\omega_z = 0$. The order of the contacts changes the result.
- **Bouncing at rest.** With $e > 0$ and gravity, a resting body makes many small bounces. A ball with $e = 1/2$ dropped from 1 m makes infinitely many bounces in a finite time (the [coefficient of restitution](/coefficient-of-restitution/) page has the numbers). Engines set $e = 0$ below a speed threshold; that threshold is a tuning value.
- **Rounding.** In floating point, the energy for $e = 1$ is kept only to rounding. Keep the contact normal exactly unit length.

## Implementations

## History

The impulse of a frictionless collision between rigid bodies comes from classical impact mechanics. In computer animation, Hahn (1988) treated collisions between rigid bodies with impulses, and Moore and Wilhelms (1988) gave an analytical collision response next to a spring method. Baraff's SIGGRAPH course notes give the formula with $k$ written as above, and it is the form used in many physics engines. Mirtich and Canny (1995) extended the impulse to Coulomb friction by integrating it along the collision, and built a whole simulator on impulses.

## References
