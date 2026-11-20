---
tag: F7HF6T
kind: algorithm
slug: lincs-algorithm
name: LINCS algorithm
aliases:
- linear constraint solver
- LINCS
area: scientific-computing/molecular-simulation
level: advanced
summary: Resets bond constraints after an unconstrained step by a truncated matrix expansion of the constraint equations, faster and more parallel than SHAKE.
model: real-ram
complexity:
  vars: {N: the number of atoms, C: the number of constraints, k: the expansion order, t: the number of rotation corrections}
  time: {worst: O(N + C k t)}
  space: {extra: O(N + C)}
properties: {deterministic: true, iterative: false, parallel: true}
history:
  year: 1997
  people: [Berk Hess, Henk Bekker, Herman J. C. Berendsen, Johannes G. E. M. Fraaije]
  note: Hess, Bekker, Berendsen and Fraaije gave LINCS in 1997, and Hess gave the parallel version P-LINCS in 2008.
prereqs: [shake-constraint-algorithm]
see_also: [rattle-algorithm, neumann-series, sparse-matrix, power-iteration, lagrange-multiplier, verlet-integration, position-based-dynamics, molecular-dynamics]
sources:
  - paper: doi:10.1002/(SICI)1096-987X(199709)18:12<1463::AID-JCC4>3.0.CO;2-H
    title: Berk Hess, Henk Bekker, Herman J. C. Berendsen and Johannes G. E. M. Fraaije, LINCS, A linear constraint solver for molecular simulations, Journal of Computational Chemistry 18(12), 1997, 1463-1472
    locator: the matrix form of the constraint equations, its series expansion, and the correction for rotation
  - paper: doi:10.1021/ct700200b
    title: Berk Hess, P-LINCS, A parallel linear constraint solver for molecular simulation, Journal of Chemical Theory and Computation 4(1), 2008, 116-122
    locator: the parallel version of the method
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Section 7.5, Parallel constraints
---

LINCS, the linear constraint solver, resets fixed bond lengths after an unconstrained molecular dynamics step. It solves the same equations as [SHAKE](/shake-constraint-algorithm/): the new positions are the free step plus corrections along the old bond directions, with multipliers chosen so that every bond has its length. SHAKE finds the multipliers by sweeping over the constraints one at a time until they converge. LINCS writes the linearised equations as one sparse matrix system, scales it so that the matrix is $I - A$ with a coupling matrix $A$ that is zero on the diagonal, and replaces the inverse by the truncated series $I + A + \cdots + A^k$. A second solve corrects the lengthening that comes from the rotation of the bonds. The work is a fixed number of sparse matrix products, with no test for convergence, so it is fast and runs well in parallel. The price is that the series only converges when the spectral radius of $A$ is below 1, which fails for rings of constraints that are nearly flat.

## In plain words

After a free step, every bond in a molecule is a little too long or too short. Each bond needs a push along its old direction to fix it. The pushes are linked, because two bonds that share an atom both move that atom.

SHAKE fixes the bonds one by one and goes round and round until all are right. LINCS instead writes down all the pushes as one system of equations and solves it with a short formula: the push each bond needs on its own, plus a correction for its neighbours, plus a correction for the neighbours of the neighbours, and so on for a fixed number of terms. Then it fixes the small error that comes from the bonds turning during the step. Every bond does the same amount of work, so many processors can share it.

## The problem

There are $N$ atoms with inverse masses $w_i$, old positions $x^{\text{old}}$ that satisfy $C$ constraints $c = (i, j, d_c)$, and free positions $x^{\text{unc}}$ from an unconstrained step. Let $n_c$ be the unit vector of the old bond $x^{\text{old}}_i - x^{\text{old}}_j$, and let $B$ be the $C \times 3N$ matrix whose row $c$ has $n_c$ at atom $i$ and $-n_c$ at atom $j$. Find multipliers $\Lambda$ such that
$$x = x^{\text{unc}} - W B^{\mathsf T} \Lambda$$
has $|x_i - x_j| = d_c$ for every constraint, where $W$ is the diagonal matrix of the $w_i$. LINCS first asks for the linear condition $B x = d$, which gives $B W B^{\mathsf T} \Lambda = B x^{\text{unc}} - d$.

## The algorithm

Let $S$ be diagonal with $S_c = 1 / \sqrt{w_i + w_j}$. Then $B W B^{\mathsf T} = S^{-1} (I - A) S^{-1}$, where for two constraints $c \ne d$ that share the atom $a$,
$$A_{cd} = -\sigma_c \sigma_d \, w_a S_c S_d \, (n_c \cdot n_d),$$
with $\sigma = +1$ if $a$ is the first atom of the constraint and $-1$ if it is the second. All other entries of $A$ are zero.

```pseudo id=main
LINCS(x_old, x_unc, w, bonds, k, t)
L1  for each constraint c = (i, j, d): n_c ← unit vector of x_old_i - x_old_j;  S_c ← 1 / √(w_i + w_j)
L2  A_cd ← -σ_c σ_d w_a S_c S_d (n_c · n_d) for each pair c ≠ d that shares an atom a
L3  x ← x_unc;  p_c ← d_c;  y_c ← S_c (n_c · (x_i - x_j) - p_c)
L4  z ← y + A y + A² y + ... + A^k y           ▷ k sparse products
L5  x_i ← x_i - w_i S_c z_c n_c;  x_j ← x_j + w_j S_c z_c n_c for each c
L6  repeat t times: q_c ← the part of x_i - x_j normal to n_c;  p_c ← √(max(0, d_c² - |q_c|²));  redo L3 to L5 with these p
L7  return x
```

The matrix $A$ and the factors $S$ depend only on the old positions, so lines L1 and L2 run once per step. Line L6 is needed because a bond that turns during the step and keeps its projection $d_c$ on the old direction is too long, by a factor of $1 / \cos$ of the angle it turned through.

## Example

**A chain.** Six atoms in a zigzag chain with five bonds, masses 12, 14, 12, 16, 12 and 1, moved by random amounts in $[-0.03, 0.03]$ (seed 2), so the largest bond error is $4.6\%$. The coupling matrix has the spectral radius $\rho = 0.232$. The largest relative bond error after LINCS, for each order $k$ and number of rotation corrections $t$:

| order $k$ | $t = 0$ | $t = 1$ | $t = 2$ | $t = 4$ |
|---|---|---|---|---|
| 0 | $7.65 \times 10^{-3}$ | $2.08 \times 10^{-3}$ | $4.45 \times 10^{-4}$ | $2.36 \times 10^{-5}$ |
| 1 | $2.18 \times 10^{-3}$ | $1.17 \times 10^{-4}$ | $6.02 \times 10^{-6}$ | $1.50 \times 10^{-8}$ |
| 2 | $1.36 \times 10^{-3}$ | $6.11 \times 10^{-6}$ | $4.35 \times 10^{-8}$ | $2.04 \times 10^{-12}$ |
| 4 | $1.11 \times 10^{-3}$ | $1.11 \times 10^{-5}$ | $4.74 \times 10^{-8}$ | $1.46 \times 10^{-12}$ |
| 8 | $1.10 \times 10^{-3}$ | $1.13 \times 10^{-5}$ | $4.39 \times 10^{-8}$ | $1.18 \times 10^{-12}$ |

Without the rotation correction the error does not fall below $1.1 \times 10^{-3}$ at any order: that column is the error of the linearisation, not of the series. Once $t \ge 1$, an order of 2 is already enough for this chain, and the corrections bring the error down by two orders of magnitude each.

**A triangle.** Three atoms of mass 1 with all three distances fixed, two sides of length 1 at an angle $\theta$, moved by up to 0.01 (seed 5), with $k = 8$ and $t = 2$:

| angle $\theta$ | $\rho$ | bond error |
|---|---|---|
| 60° | 0.5 | $3.4 \times 10^{-10}$ |
| 120° | 0.75 | $1.2 \times 10^{-6}$ |
| 150° | 0.933 | $1.5 \times 10^{-4}$ |
| 170° | 0.9924 | $1.8 \times 10^{-4}$ |

As the triangle becomes flat, $\rho$ tends to 1 (it is 0.99970 at 178°), the series converges slowly, and LINCS with a fixed order leaves a large error.

## Correctness

The proof below shows these claims:

1. **The matrix.** $B W B^{\mathsf T} = S^{-1} (I - A) S^{-1}$, with $A$ symmetric and zero on the diagonal.
2. **One projection.** With an exact inverse in line L4, lines L3 to L5 give positions of the required form with $Bx = p$.
3. **The series.** With order $k$, the error of line L4 is at most $\rho^{k+1} / (1 - \rho)$ times the size of its input, where $\rho < 1$ is the spectral radius of $A$. For $\rho \ge 1$ the series does not converge.
4. **The rotation correction.** If the corrections of line L6 converge with exact solves, the limit has every bond at its length and the form of the constrained step, so it is the SHAKE solution.
5. **The centre of mass** does not move.

The tests check the series against a direct solve, the agreement with a SHAKE solution to $10^{-11}$ at a high order, the fall of the error with $k$ and $t$, the centre of mass, and the spectral radius of the triangle.

## Complexity

Lines L1 and L2 cost $\Theta(N + C b)$, where $b$ is the largest number of constraints that share an atom with one constraint. Each solve costs $\Theta(C b k)$ for the $k$ sparse products, and there are $t + 1$ solves. For molecules, $b$ is a small constant, so a step costs $\Theta(N + C k t)$. There is no loop that runs to convergence, so the cost is the same in every step, and each constraint only reads its neighbours, which suits parallel machines.

## Properties

- **Fixed cost.** The work does not depend on how far the free step broke the bonds.
- **Parallel.** Each sparse product needs only the values of neighbouring constraints. P-LINCS (Hess, 2008) splits the constraints between processors on this basis.
- **Approximate.** The result holds the bonds only to the error of the series and the corrections, not to a set tolerance.
- **Centre of mass.** Each projection keeps the centre of mass.
- **Ring sensitive.** Coupled triangles, as in angle constraints, push $\rho$ toward 1 and make the series slow.

## Variants and improvements

- **P-LINCS.** The parallel version of Hess (2008) passes the coupling between processors that share constraints.
- **A higher order for coupled constraints.** Raising $k$ helps when $\rho$ is close to but below 1, at a linear cost in $k$.
- **Velocities.** The same series, applied to the velocities, removes their component along the bonds, as in the velocity stage of [RATTLE](/rattle-algorithm/).
- **Mixed methods.** Codes often use LINCS for bonds and a closed-form method such as SETTLE for rigid water.

## When to use it

Use LINCS to hold bonds to hydrogen fixed in large simulations of proteins, membranes or polymers, especially in parallel. Do not use it for angle constraints or rigid rings that are nearly flat, where the series converges slowly or not at all. There SHAKE, a direct sparse solve, or a closed-form method is safer.

## Pitfalls

- **No rotation correction.** With $t = 0$ every bond that turns comes out too long, by an amount of the size of the square of the angle it turned.
- **A spectral radius near 1.** The error then hardly falls with the order. Check $\rho$ for the molecules you use, for example by [power iteration](/power-iteration/) on $A$.
- **Energy drift.** The bonds do not hold exactly, so the step is not exactly reversible. Choose $k$ and $t$ so that the bond error is well below the other errors of the simulation.
- **The sign convention of $A$.** A wrong sign in $\sigma_c \sigma_d$ gives a matrix with the right size and the wrong coupling, and the bonds then come out wrong without any error message.

## Implementations

## History

Hess, Bekker, Berendsen and Fraaije (1997) gave LINCS as a faster replacement for SHAKE. They wrote the constraint equations as a matrix system, expanded the inverse as a series, and added the correction for the rotation of the bonds. Hess (2008) gave P-LINCS, a version for parallel computers.

## References
