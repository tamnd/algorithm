---
tag: 8FV1QP
kind: algorithm
slug: lemke-algorithm
name: Lemke's algorithm
aliases:
- Lemke's complementary pivot algorithm
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: Solves a linear complementarity problem by adding an artificial variable and pivoting along almost complementary bases until it leaves.
solves: [linear-complementarity-problem]
model: real-ram
complexity:
  vars: {n: the size of the matrix M (the number of complementary pairs)}
  time: {worst: "O(2^n n^3)"}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1965
  people: [Carlton E. Lemke]
  note: Lemke generalized the Lemke-Howson method for bimatrix games to a pivoting method for the linear complementarity problem in Management Science in 1965.
prereqs: [linear-complementarity-problem, simplex-method, lemke-howson-algorithm]
see_also: [rigid-contact-complementarity, projected-gauss-seidel, quadratic-programming, kkt-conditions, sequence-form, ppad, support-enumeration, bland-rule]
sources:
  - paper: doi:10.1287/mnsc.11.7.681
    title: "C. E. Lemke, Bimatrix equilibrium points and mathematical programming, Management Science 11(7) (1965), 681-689"
    locator: the complementary pivot method with the artificial variable z0; the paper writes the problem as M z - w = q, which is the form w = M z + q of this page with the signs of M and q changed
  - book: "Richard W. Cottle, Jong-Shi Pang and Richard E. Stone, The Linear Complementarity Problem, Academic Press, 1992"
    title: Richard W. Cottle, Jong-Shi Pang and Richard E. Stone, The Linear Complementarity Problem
    locator: the chapter on pivoting methods (Lemke's method, the covering vector, ray termination, and the matrix classes that it processes)
  - paper: doi:10.1007/BFb0120782
    title: "Katta G. Murty, Computational complexity of complementary pivot methods, Mathematical Programming Study 7 (1978), 61-73"
    locator: for each n at least 2, an LCP of order n on which complementary pivot methods take 2^n pivots
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 3 (Bernhard von Stengel), the LCP of a bimatrix game and Lemke's algorithm with a covering vector
---

Lemke's algorithm solves a [linear complementarity problem](/linear-complementarity-problem/) (LCP): given an $n \times n$ matrix $M$ and a vector $q$, find $z \ge 0$ with $w = Mz + q \ge 0$ and $z_i w_i = 0$ for each $i$. In a contact simulation, $z_i$ is the impulse or force at contact $i$, $w_i$ is the gap velocity there, and the condition says that a contact pushes only while it is closed and never pulls ([rigid contact complementarity](/rigid-contact-complementarity/)). The method is a pivoting method like the [simplex method](/simplex-method/): it adds one artificial variable $z_0$ that makes the start feasible, then follows a unique path of bases in which every pair $(z_i, w_i)$ has at least one zero, except one pair, until $z_0$ leaves the basis. It gives an exact solution in a finite number of steps for important classes of $M$, and it can end on an unbounded edge, a ray, for others. Iterative methods such as [projected Gauss-Seidel](/projected-gauss-seidel/) are cheaper per step and are the usual choice in real-time physics, but they give only approximations. Lemke's algorithm generalizes the [Lemke-Howson algorithm](/lemke-howson-algorithm/), which is the special case for the equilibria of two-player games.

## In plain words

Each pair of numbers $z_i$ and $w_i$ must be nonnegative, and one of them must be zero. If $q$ has no negative entry, $z = 0$ works. Otherwise, add an extra unknown $z_0$ that lifts every $w_i$ by the same amount, enough to make all of them nonnegative. Now the only rule we break is that $z_0$ should be 0. Change one variable at a time, as in the simplex method: each step makes one variable zero, and the rule says that its partner in its pair must be the next one to grow. The path is forced at each step and never comes back. When $z_0$ falls to zero, we have the answer. If the variable that should grow can grow without limit, the method stops without an answer.

## The problem

The input is an $n \times n$ matrix $M$ and a vector $q \in \mathbb{R}^n$, with rational entries. The output is a pair $(z, w)$ with

$$w = Mz + q, \qquad z \ge 0, \qquad w \ge 0, \qquad z^{\mathsf T} w = 0,$$

or the answer "ray". Since $z, w \ge 0$, the condition $z^{\mathsf T} w = 0$ means $z_i w_i = 0$ for every $i$. The variables $z_i$ and $w_i$ are a complementary pair. A basis of the system $w - Mz = q$ is complementary if it holds exactly one variable of each pair.

The algorithm also takes a covering vector $d > 0$, by default $d = \mathbf 1$. The augmented system is

$$w = Mz + d\, z_0 + q, \qquad z, w, z_0 \ge 0, \qquad z^{\mathsf T} w = 0 .$$

A basis of it is **almost complementary** if $z_0$ is basic and, of the $n$ pairs, exactly one has both variables nonbasic and the others have one variable basic each.

## The algorithm

```pseudo id=main
LEMKE(M, q, d)                       ▷ w = M z + q; columns w_1..w_n, z_1..z_n, z_0; d > 0
L1  if q ≥ 0 then return z = 0, w = q
L2  build the tableau w - M z - d z_0 = q with the basis w
L3  enter z_0; the leaving row r is the lexicographic minimum of q_i / d_i (the most negative)
L4  e ← the complement of w_r, that is, z_r
L5  repeat
L6      if no row has a positive entry in column e then return "ray"
L7      enter e by the lexicographic minimum ratio test; if z_0 leaves then return (z, w)
L8      e ← the complement of the variable that left
```

After line L3 the basic solution is feasible: $z_0 = \max_i (-q_i / d_i) > 0$ makes every $w_i = q_i + d_i z_0$ nonnegative, and $w_r = 0$. The basis is almost complementary, and the pair $(z_r, w_r)$ has both variables nonbasic. Line L4 enters $z_r$, the partner of the variable that just left; this is the complementary pivot rule. Line L7 is the ratio test of the simplex method, so all variables stay nonnegative. If $z_0$ leaves, the basis is complementary with $z_0 = 0$, which is a solution. Otherwise a variable of some pair leaves, that pair now has both variables nonbasic, and line L8 enters the partner of the one that left.

The ratio test of line L7 is lexicographic: ties in the ratio are broken by comparing the rows of the current inverse basis (the columns of $w$ in the tableau), each divided by the pivot entry. This is the same as replacing $q$ by $q + (\varepsilon, \varepsilon^2, \ldots, \varepsilon^n)$ for a small $\varepsilon > 0$, and it makes every step unique, so the method cannot cycle on a degenerate input.

## Example

A two-contact example: $M = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ and $q = (-1, 1)$. Think of $q$ as the gap velocities before the impulses: contact 1 approaches at speed 1 and contact 2 separates at speed 1. $M$ says how impulses change the velocities, and it couples the two contacts.

| step | enters | leaves | $z_0$ | $z$ | $w$ |
|---|---|---|---|---|---|
| L3 | $z_0$ | $w_1$ | 1 | $(0, 0)$ | $(0, 2)$ |
| L7 | $z_1$ | $z_0$ | 0 | $(1/2, 0)$ | $(0, 3/2)$ |

In the second step $z_1 = t$ grows and $w_1 = -1 + 2t + z_0$ stays 0, so $z_0 = 1 - 2t$ and $w_2 = 1 + t + z_0 = 2 - t$. The ratio test stops at $t = 1/2$, where $z_0$ reaches 0 before $w_2$ does. The solution is an impulse $1/2$ at contact 1 and none at contact 2; contact 1 ends at rest and contact 2 separates at speed $3/2$.

A ray example: $M = (-1)$ and $q = (-1)$. Then $w = -z - 1 < 0$ for every $z \ge 0$, so no solution exists. Line L3 enters $z_0 = 1$, line L4 enters $z_1$, and its column has no positive entry, so line L6 returns "ray".

## Correctness

Each step keeps the basis almost complementary and feasible, so the solution it ends with, when $z_0$ leaves, is complementary with $z_0 = 0$, which is a solution of the LCP. The method ends: in the perturbed (lexicographic) problem each almost complementary basis has at most two neighbors on the path, one by entering each variable of its pair whose both members are nonbasic. The starting basis has only one, because the other direction is the ray of $z_0$ that starts at the initial point. So the path is a simple path in a finite graph and it cannot return to a basis, which means that it ends in a finite number of steps, either when $z_0$ leaves or on a ray (line L6). The proof file has the details.

Ray termination does not always mean that no solution exists, but for important classes of $M$ it does:

- If $M$ is a **P-matrix** (all principal minors positive, for example a positive definite matrix), the LCP has a unique solution for every $q$, and the method never ends on a ray.
- If $M$ is **copositive-plus** (for example positive semidefinite), a ray proves that the system $z \ge 0$, $Mz + q \ge 0$ has no solution.
- If $M$ is **strictly copositive** ($z^{\mathsf T} M z > 0$ for $z \ge 0$, $z \ne 0$, for example a matrix with positive entries), a solution exists for every $q$ and the method finds it.

## Complexity

Each pivot costs $O(n^2)$ arithmetic operations on a tableau of $n$ rows and $2n + 2$ columns. An almost complementary basis is fixed by the pair with both members nonbasic ($n$ choices) and by one member of each other pair ($2^{n-1}$ choices), so the path has at most $n 2^{n-1}$ steps, and the time is $O(2^n n^3)$ in the worst case. This is not only a weak bound: Murty (1978) gave, for each $n \ge 2$, an LCP of order $n$ on which complementary pivot methods take $2^n$ pivots. On many practical problems the number of pivots is much smaller than this bound.

In exact rational arithmetic the numbers stay of polynomial bit length, as in the simplex method. The general LCP is NP-complete, so no method solves every LCP in polynomial time unless P = NP. The space is the tableau, $O(n^2)$ numbers.

## Properties

- **Exact.** With rational data the output is an exact rational solution.
- **Finite.** With the lexicographic rule it ends on every input, either with a solution or on a ray.
- **A certificate for some classes.** For copositive-plus $M$ a ray is a proof of infeasibility.
- **Path following.** The path is the same kind of object as in Lemke-Howson, which is why the problems it solves for games are in [PPAD](/ppad/).
- **Depends on $d$.** Different covering vectors give different paths, and can give different solutions when the solution is not unique.

## Variants and improvements

- **Bimatrix games.** An equilibrium of a two-player game is a solution of an LCP. The plain form $M = \begin{pmatrix} 0 & C \\ D^{\mathsf T} & 0 \end{pmatrix}$, $q = -\mathbf 1$ with positive cost matrices $C$, $D$ is copositive but not copositive-plus, and with $d = \mathbf 1$ the method can end on a ray (the tests show a $2 \times 3$ game where it does). The Lemke-Howson algorithm solves this form from a dropped label instead. The code here uses the symmetrized game $S = \begin{pmatrix} 0 & A' \\ B'^{\mathsf T} & 0 \end{pmatrix}$ with costs $M = K - S > 0$, which is strictly copositive, so Lemke's method always succeeds.
- **Games in extensive form.** With the [sequence form](/sequence-form/), the equilibria of a two-player game tree with perfect recall are the solutions of an LCP of size linear in the tree, and Lemke's method with a covering vector computes one.
- **Quadratic programs.** The [KKT conditions](/kkt-conditions/) of a convex [quadratic program](/quadratic-programming/) form an LCP with a positive semidefinite $M$, and Lemke's method solves it exactly or proves it infeasible.
- **Other pivoting methods.** Principal pivoting methods (Murty's least index method, the Cottle-Dantzig method) need no artificial variable and work for P-matrices.
- **Iterative methods.** For large sparse problems, such as rigid-body contact in games and films, projected Gauss-Seidel, splitting methods and interior point methods are faster than pivoting, and give approximate solutions.

## When to use it

Use it for a small or medium LCP where an exact solution is needed, or where the answer must say for sure that there is no solution (for copositive-plus $M$). Use it on the LCP of a bimatrix game or of a sequence form game. For real-time contact with many bodies, use projected Gauss-Seidel; for large convex quadratic programs, use an interior point method.

## Pitfalls

- **The sign convention.** Lemke's 1965 paper writes $Mz - w = q$; this page writes $w = Mz + q$. Moving between them changes the signs of $M$ and $q$.
- **Reading a ray as "no solution".** That is right only for some classes of $M$. A general $M$ can have solutions that the method does not find.
- **A zero or negative covering vector.** If $d_i \le 0$ for a row with $q_i < 0$, line L3 cannot make that row feasible. Use $d > 0$.
- **Cycling.** Without the lexicographic rule, a degenerate problem can make the method cycle.
- **Floating point.** In floating point, small pivot entries make the path wrong. Exact arithmetic avoids this but is slow on large problems.

## Implementations

The Python code keeps the tableau in Fraction and follows lines L1 to L8 with the lexicographic ratio test; it can record the pivots. It also builds the strictly copositive LCP of a bimatrix game. The tests check the two examples above; random positive definite and diagonally dominant P-matrices, where the solution must be the only one found by a brute force over the $2^n$ complementary bases; random positive semidefinite matrices, where a ray must happen exactly when an exact LP shows that $z \ge 0$, $Mz + q \ge 0$ is infeasible; random general matrices, where each solution is checked; degenerate inputs with ties; and 60 random nondegenerate bimatrix games, where the output must be a Nash equilibrium by a check of all pure deviations and must be in the list of an independent support enumeration.

## History

Lemke and Howson gave the pivoting method for bimatrix games in 1964. Lemke (1965) added the artificial variable and the covering vector, which made the method work for a general LCP, and related it to mathematical programming. Murty (1978) showed that complementary pivot methods can need exponentially many steps. The theory of matrix classes and pivoting methods is collected in the book of Cottle, Pang and Stone (1992).

## References
