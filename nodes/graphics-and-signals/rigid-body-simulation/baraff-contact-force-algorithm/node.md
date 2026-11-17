---
tag: APAZTF
kind: algorithm
slug: baraff-contact-force-algorithm
name: Baraff's contact force algorithm
aliases:
- Baraff fast contact force computation
area: graphics-and-signals/rigid-body-simulation
level: advanced
summary: Compute nonnegative contact forces that prevent interpenetration of resting rigid bodies by a pivoting method on a linear complementarity problem.
solves: [rigid-body-simulation-problem]
model: real-ram
complexity:
  vars: {n: the number of contact points}
  time: {per_pivot_fresh_solve: O(n^3), per_pivot_incremental: O(n^2), drives: O(n)}
  space: {matrix: O(n^2)}
properties: {deterministic: true, online: false, recursive: false, in_place: false}
history:
  year: 1994
  people: [David Baraff, George B. Dantzig, Richard W. Cottle]
  note: Baraff gave a physical reading of Dantzig's principal pivoting method for the frictionless contact LCP and extended it to static and dynamic friction, so that contact forces could be computed without a general optimization package.
prereqs: [contact-manifold, newton-euler-equations, positive-definite-matrix, gaussian-elimination, kkt-conditions]
see_also: [projected-gauss-seidel, linear-complementarity-problem, lemke-algorithm, quadratic-programming, rigid-contact-complementarity, painleve-paradox, stewart-trinkle-time-stepping, impulse-based-simulation]
sources:
  - paper: doi:10.1145/192161.192168
    title: "David Baraff, Fast contact force computation for nonpenetrating rigid bodies, SIGGRAPH 94, 23-34"
    locator: "Section 4 (4.3 the procedures compute-forces, drive-to-zero, fdirection and maxstep; 4.4 termination; 4.5 implementation) and Appendix A (Theorems 2 to 5)"
  - paper: doi:10.1145/74333.74356
    title: "David Baraff, Analytical methods for dynamic simulation of non-penetrating rigid bodies, SIGGRAPH 89, 223-232"
    locator: the contact force problem for resting contact
  - paper: doi:10.1145/127719.122722
    title: "David Baraff, Coping with friction for non-penetrating rigid body simulation, Computer Graphics 25(4), 31-41, 1991"
    locator: the NP-hardness of consistent contact forces with Coulomb friction
  - book: isbn:9780898716863
    title: "Richard W. Cottle, Jong-Shi Pang and Richard E. Stone, The Linear Complementarity Problem, SIAM Classics in Applied Mathematics, 2009"
    locator: the chapters on pivoting methods and on the existence and uniqueness of LCP solutions
---

Baraff's contact force algorithm computes the normal forces at the contact points of [rigid bodies](/rigid-body-simulation-problem/) that rest on each other. The forces must push and never pull, the contacts must not accelerate into each other, and a contact that separates must carry no force. These conditions form a [linear complementarity problem](/linear-complementarity-problem/) with a symmetric positive semidefinite matrix. The algorithm solves it by raising one force at a time until its contact stops accelerating inward, while it keeps all contacts handled so far consistent. It is Dantzig's principal pivoting method, which Baraff (1994) explained in physical terms and extended to friction.

## In plain words

A book lies on a table, and a cup stands on the book. Gravity pulls everything down. At each touching point, the table or the book must push up just hard enough to stop things from sinking in. A point that is about to lift off must not pull.

The algorithm looks at the touching points one by one. For a point that would sink, it slowly turns up the push at that point. While it does that, the pushes at the points it has already handled change too, so that those points neither sink nor pull. If one of those old points would need to pull, it lets that point go and lifts it off instead. If a lifted point starts to sink again, it takes that point back. When the current point stops sinking, it moves on to the next.

## The problem

Bodies are at rest relative to each other at $n$ contact points; colliding contacts are handled first with [impulses](/collision-impulse/). At contact $i$, the normal $n_i$ points from $B$ to $A$, $f_i \ge 0$ is the size of the normal force, and $a_i$ is the normal relative acceleration: $a_i > 0$ means the contact separates. With the contact Jacobian $J$ and the mass matrix $M$, the accelerations depend linearly on the forces,

$$a = A f + b, \qquad A = J M^{-1} J^T, \qquad b = J M^{-1} F_{ext} + (\text{velocity terms}),$$

by the [Newton-Euler equations](/newton-euler-equations/). The problem is: find $f$ with

$$f \ge 0, \qquad a = A f + b \ge 0, \qquad f_i a_i = 0 \text{ for all } i.$$

$A$ is symmetric and positive semidefinite, and $b$ lies in the column space of $A$ (Baraff, Section 4.1). $A$ is singular whenever there are more contacts than independent directions, for example a box on four corners, or a 2D box on three points along its bottom edge. This model has no friction; it is the frictionless case of [rigid contact complementarity](/rigid-contact-complementarity/).

## The algorithm

```pseudo id=main
COMPUTE-FORCES(A, b)
L1  f ← 0; a ← b
L2  C ← ∅; NC ← ∅                ▷ C: clamped, a_i = 0; NC: not clamped, f_i = 0
L3  while some d has a_d < 0
L4    DRIVE-TO-ZERO(d)

DRIVE-TO-ZERO(d)
L5  loop
L6    Δf ← FDIRECTION(d); Δa ← A Δf
L7    (s, j) ← MAXSTEP(f, a, Δf, Δa, d)
L8    f ← f + s Δf; a ← a + s Δa
L9    if j ∈ C then move j from C to NC
L10   else if j ∈ NC then move j from NC to C
L11   else add d to C; return       ▷ j = d, and a_d = 0

FDIRECTION(d)
L12 Δf ← 0; Δf_d ← 1
L13 solve A_CC x = -A_Cd           ▷ keep a_i = 0 for i in C
L14 Δf_i ← x_i for i in C; return Δf

MAXSTEP(f, a, Δf, Δa, d)
L15 s ← ∞; j ← none
L16 if Δa_d > 0 then s ← -a_d / Δa_d; j ← d
L17 for i in C with Δf_i < 0: if -f_i / Δf_i < s then s ← -f_i / Δf_i; j ← i
L18 for i in NC with Δa_i < 0: if -a_i / Δa_i < s then s ← -a_i / Δa_i; j ← i
L19 return (s, j)
```

FDIRECTION finds how all clamped forces must change, per unit increase of $f_d$, so that the clamped contacts keep $a_i = 0$. MAXSTEP finds the first event along that direction: $a_d$ reaches zero, a clamped force falls to zero, or a free contact starts to accelerate inward.

## Example

A 2D box of mass $m = 1$ and width 2, with $I = 5/12$, rests on the ground on three contacts, numbered 1, 2, 3 from left to right, at the horizontal offsets $x = -1, 0, 1$ from its center. Take $g = 10$ and an applied torque of $-15$ (clockwise). For a contact at offset $x$, $a = \ddot y + \alpha x$, so $A_{ij} = 1/m + x_i x_j / I$ and $b_i = -10 + x_i \cdot (-15/I)$:

$$A = \begin{pmatrix} 17/5 & 1 & -7/5 \\ 1 & 1 & 1 \\ -7/5 & 1 & 17/5 \end{pmatrix}, \qquad b = (26, -10, -46).$$

$A$ has rank 2, since three collinear contacts in 2D give only two independent rows.

| pass | driven $d$ | $C$ before | $\Delta f$ | limit $j$ | step $s$ | $f$ after | $a$ after |
|---|---|---|---|---|---|---|---|
| 1 | 2 (middle) | $\{\}$ | $(0, 1, 0)$ | $d$ | 10 | $(0, 10, 0)$ | $(36, 0, -36)$ |
| 2 | 3 (right) | $\{2\}$ | $(0, -1, 1)$ | 2 leaves $C$ | 10 | $(0, 0, 10)$ | $(12, 0, -12)$ |
| 3 | 3 (right) | $\{\}$ | $(0, 0, 1)$ | $d$ | $60/17$ | $(0, 0, 230/17)$ | $(120/17, 60/17, 0)$ |

Contact 1 starts with $a_1 = 26 > 0$ and is never driven. In pass 2, pushing at the right corner while keeping the middle clamped needs less force in the middle, and the middle force reaches zero: the middle contact moves to $NC$. The result is the tipping box: only the right corner pushes, with $230/17$, and the left and middle contacts lift off with $a = 120/17$ and $60/17$. Check: $\ddot y = -10 + 230/17 = 60/17$ and $\alpha = -36 + (230/17)(12/5) = -60/17$, so the right corner has $\ddot y + \alpha = 0$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The steps:

- **Invariants.** Clamped contacts have $a_i = 0$ and $f_i \ge 0$, free contacts have $f_i = 0$ and $a_i \ge 0$, and contacts not yet handled have $f_i = 0$. MAXSTEP takes the largest step that keeps them, so when no $a_d$ is negative, $f$ solves the LCP.
- **The driven contact moves.** $\Delta a_d = \Delta f^T A \Delta f$, the Schur complement of $A_{CC}$; it is positive for positive definite $A$ (Baraff's Theorem 2).
- **Each drive is finite.** For positive definite $A$, the state is the unique solution of a smaller LCP that depends on $f_d$ alone. Each set $C$ is valid on an interval of $f_d$, and $f_d$ only grows, so no set $C$ repeats in one drive (Baraff's Theorem 3), if no step has length zero.
- **At most $n$ drives.** Each drive adds the driven contact to $C$ for good, and no drive removes a handled contact.
- **Uniqueness.** For positive definite $A$ the forces are unique. For positive semidefinite $A$ with $b$ in its column space, all solutions have the same accelerations $a$, because the LCP is the optimality condition of the convex [quadratic program](/quadratic-programming/) $\min \tfrac12 f^T A f + b^T f$ over $f \ge 0$ (see [KKT conditions](/kkt-conditions/)).

Termination for singular $A$ and for degenerate steps is proved by Baraff in Appendix A, not on this page.

## Complexity

There are at most $n$ calls of DRIVE-TO-ZERO. Each pass solves one linear system with $A_{CC}$: $O(n^3)$ with a fresh [Gaussian elimination](/gaussian-elimination/), as in Baraff's first implementation, or $O(n^2)$ with a factorization that is updated by one row and column per pass, since consecutive sets $C$ differ in one index. The proof bounds the passes of one call only by the number of subsets of the handled contacts, so no polynomial bound on the total is given here. Baraff reports about three times the work of one Gaussian elimination of size $n$ on his frictionless examples, which is a measurement. Storing $A$ takes $O(n^2)$ space; it is sparse when each body touches few others.

## Properties

- Exact in exact arithmetic: the result satisfies the complementarity conditions exactly, not to a tolerance.
- No pulling forces, and no inward acceleration at any contact.
- Works for singular $A$, which is the normal case with redundant contacts.
- The result depends on the order of the contacts when $A$ is singular, but the accelerations do not.
- Finite: it ends after a finite number of pivots, while an iterative method such as [projected Gauss-Seidel](/projected-gauss-seidel/) gives a sequence of approximations.

## Variants and improvements

- **Bilateral constraints.** Joints have $a_i = 0$ with forces of either sign. Baraff keeps them in $C$ for the whole run, so that MAXSTEP never removes them.
- **Friction.** Later sections of Baraff's paper add static and dynamic Coulomb friction. The matrix is then no longer symmetric, and the static friction version is not proved to terminate. With friction, a consistent set of forces may not exist (the [Painlevé paradox](/painleve-paradox/)), and deciding whether one exists is NP-hard (Baraff 1991).
- **Impulse level.** The same LCP with $b = J v$ and impulses in place of forces gives inelastic contact impulses for one time step, as in [Stewart-Trinkle time stepping](/stewart-trinkle-time-stepping/).
- **Lemke's method.** [Lemke's algorithm](/lemke-algorithm/) is a complementary pivoting method that applies to wider classes of LCPs, at the cost of an extra artificial variable.
- **Iterative solvers.** [Projected Gauss-Seidel](/projected-gauss-seidel/) trades exactness for a fixed cost per iteration and is the usual choice in game engines.

## When to use it

Use it when you need accurate resting contact forces for a moderate number of contacts: robotics and engineering simulation, grasping, offline animation. It handles redundant contacts, and its result is exact up to rounding. For thousands of contacts per frame at interactive rates, an iterative solver with a fixed number of sweeps is cheaper. With friction, the pivoting extensions lose their termination guarantees, and a time-stepping formulation at the impulse level is more robust.

## Pitfalls

- **Rounding and singular $A_{CC}$.** In exact arithmetic the matrices $A_{CC}$ that the algorithm forms are nonsingular when $b$ is in the column space of $A$ (Baraff, Section 4.4). In floating point, rounding can let an index enter $C$ that makes $A_{CC}$ singular or nearly singular. Use a solver that detects this, and do not trust a pivot on a tiny value.
- **$b$ not in the column space.** If the data are inconsistent, MAXSTEP may find no limit, and the driven force grows without bound. Check for this and stop.
- **Forces are not unique.** With redundant contacts, the force split between contacts can jump between frames even though the motion is the same. Do not read individual forces as measured loads.
- **Collisions first.** The acceleration LCP assumes that no contact approaches with a nonzero velocity. Resolve colliding contacts with impulses before calling it, and correct the slow drift of positions, for example with [Baumgarte stabilization](/baumgarte-stabilization/).
- **Tolerances.** In floating point, use a small tolerance in the tests $a_d < 0$, $\Delta f_i < 0$ and $\Delta a_i < 0$, or the method can pivot on rounding noise.

## Implementations

## History

Baraff (1989) posed the computation of resting contact forces between rigid bodies as a quadratic program, which needed a general optimization package. In 1991 he showed that the problem with Coulomb friction is NP-hard. His 1994 paper used Dantzig's algorithm for the frictionless LCP, described by Cottle and Dantzig and attributed to Dantzig, gave it a physical reading as "drive one contact to zero acceleration at a time", and extended it to static and dynamic friction. Cottle, Pang and Stone treat pivoting methods for the LCP in general.

## References
