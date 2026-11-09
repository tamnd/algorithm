---
tag: JK7PSR
kind: algorithm
slug: fourier-motzkin-elimination
name: Fourier-Motzkin elimination
aliases:
- Fourier-Motzkin
- Fourier-Motzkin elimination
- FM elimination
- Fourier elimination
area: optimization/linear-programming
level: core
summary: Decide feasibility by eliminating one variable at a time; exponential in general.
solves: [linear-feasibility]
model: real-ram
complexity:
  vars: {m: the number of inequalities, n: the number of variables}
  time: {worst: O(n (m + n) m^(2^n))}
  space: {extra: O((m + n) m^(2^n))}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1826
  people: [Joseph Fourier, Theodore Motzkin]
  note: Fourier described the method in 1826 and Motzkin rediscovered it in his 1936 thesis.
prereqs: [linear-feasibility]
see_also: [farkas-lemma, polyhedron, linear-programming-problem, gaussian-elimination, minkowski-weyl-theorem, vertex-enumeration, simplex-method, ellipsoid-method]
sources:
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Section 12.2, The Fourier-Motzkin elimination method (the method, its doubly exponential growth, and the historical notes)
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 2.8, Projections of polyhedra (Fourier-Motzkin elimination, and the projection of a polyhedron is a polyhedron)
  - book: isbn:9780387943657
    title: Günter M. Ziegler, Lectures on Polytopes, Graduate Texts in Mathematics 152, Springer, 1995
    locator: Chapter 1, Polytopes, polyhedra and cones (Fourier-Motzkin elimination as the tool for the main theorem and the Farkas lemma)
---

Fourier-Motzkin elimination decides whether a system of linear inequalities $Ax \le b$ has a solution, by removing the variables one at a time. To remove $x_k$, it pairs every inequality that bounds $x_k$ from above with every inequality that bounds it from below, and adds each pair with positive weights so that $x_k$ cancels. The new system has one variable fewer and has a solution exactly when the old one does. When all variables are gone, the system says $0 \le \beta$ for some numbers $\beta$, which is true or false by inspection. The method is the inequality version of [Gaussian elimination](/gaussian-elimination/). It is exact, it returns a solution or a [Farkas](/farkas-lemma/) certificate, and it proves that the projection of a [polyhedron](/polyhedron/) is a polyhedron, but the number of inequalities can grow doubly exponentially in $n$.

## In plain words

Each limit that involves a chosen unknown says either "this unknown is at most something" or "this unknown is at least something". A value for the unknown exists exactly when every "at least" bound is below every "at most" bound. So write down one new limit for each pair of a lower bound and an upper bound, saying that the lower one is at most the upper one, and throw the chosen unknown away. Repeat for every unknown. At the end only plain numbers are compared, and you can see at once whether all the limits can hold. Then go back up the chain and pick each unknown inside its range. The catch is that each step can square the number of limits.

## The problem

Given $A \in \mathbb{Q}^{m \times n}$ and $b \in \mathbb{Q}^m$, decide whether some $x \in \mathbb{R}^n$ satisfies $Ax \le b$. Return such an $x$, or a vector $y \ge 0$ with $y^\top A = 0$ and $y^\top b < 0$, which proves that no $x$ exists. This is the [linear feasibility problem](/linear-feasibility/). Equations and sign conditions are written as pairs of inequalities.

## The algorithm

Each row of the working system $R$ is a triple $(a, \beta, y)$ that stands for the inequality $a^\top x \le \beta$, together with the vector $y \ge 0$ of the multipliers that build it from the input: $y^\top A = a^\top$ and $y^\top b = \beta$.

```pseudo id=main
FOURIER-MOTZKIN(A, b)                            ▷ decide whether Ax ≤ b has a solution
L1  R ← the rows (a_i, b_i, e_i) for i = 1, …, m   ▷ e_i: the i-th unit vector
L2  for k ← n down to 1 do
L3      P ← rows of R with a[k] > 0,  N ← rows of R with a[k] < 0
L4      R_k ← R                                  ▷ the system in x_1, …, x_k, kept for later
L5      R′ ← rows of R with a[k] = 0
L6      for each p in P and each q in N do
L7          add (−q.a[k]) · p + p.a[k] · q to R′  ▷ the coefficient of x_k cancels
L8      R ← R′ without rows 0 ≤ β with β ≥ 0, and with only the tightest of parallel rows
L9  if R has a row 0 ≤ β with β < 0 then return (INFEASIBLE, its y)
L10 for k ← 1 to n do                             ▷ back-substitution
L11     lo ← max of the lower bounds on x_k given by R_k; hi ← min of its upper bounds
L12     x_k ← lo if lo > −∞, else hi if hi < +∞, else 0
L13 return (FEASIBLE, x)
```

Lines L2 to L8 are the elimination. A row $p$ in $P$ says $x_k \le (\beta_p - \sum_{j<k} a_{pj} x_j) / a_{pk}$, an upper bound, and a row $q$ in $N$ gives a lower bound in the same way. Line L7 multiplies $p$ by $-a_{qk} > 0$ and $q$ by $a_{pk} > 0$ and adds them: the result says "the lower bound of $q$ is at most the upper bound of $p$", and both multipliers are positive, so the new $y$ is still nonnegative. Line L8 removes rows that cannot matter: a row $0 \le \beta$ with $\beta \ge 0$ always holds, and of two rows with the same direction after scaling, the one with the larger right side is implied by the other. After the loop every coefficient is zero, so each remaining row is $0 \le \beta$ with $\beta < 0$, and its $y$ is a Farkas certificate. Lines L10 to L12 rebuild a solution: the system $R_k$ involves only $x_1, \ldots, x_k$, and with $x_1, \ldots, x_{k-1}$ fixed, it gives an interval for $x_k$.

## Example

Maximize $3x_1 + 2x_2$ over the running polygon $x_1 + x_2 \le 4$, $x_1 + 3x_2 \le 9$, $x_1 \le 3$, $x \ge 0$. Add a variable $z$ with the row $z - 3x_1 - 2x_2 \le 0$, and order the variables as $(z, x_1, x_2)$, so that $x_2$ is removed first and $z$ is left. The six rows are

$$\begin{aligned} &(1)\ x_1 + x_2 \le 4 && (2)\ x_1 + 3x_2 \le 9 && (3)\ x_1 \le 3 \\ &(4)\ -x_1 \le 0 && (5)\ -x_2 \le 0 && (6)\ z - 3x_1 - 2x_2 \le 0. \end{aligned}$$

*Remove $x_2$.* $P = \{1, 2\}$, $N = \{5, 6\}$, $Z = \{3, 4\}$. The four pairs give

| pair | combination | new row |
|---|---|---|
| (1), (5) | $1 \cdot (1) + 1 \cdot (5)$ | $x_1 \le 4$ |
| (1), (6) | $2 \cdot (1) + 1 \cdot (6)$ | $z - x_1 \le 8$ |
| (2), (5) | $1 \cdot (2) + 3 \cdot (5)$ | $x_1 \le 9$ |
| (2), (6) | $2 \cdot (2) + 3 \cdot (6)$ | $3z - 7x_1 \le 18$ |

With (3) and (4), line L8 keeps the tightest of the parallel rows $x_1 \le 3$, $x_1 \le 4$, $x_1 \le 9$, so four rows remain: $x_1 \le 3$, $-x_1 \le 0$, $z - x_1 \le 8$ and $3z - 7x_1 \le 18$.

*Remove $x_1$.* $P = \{x_1 \le 3\}$ and $N$ has the other three rows. The pairs give $0 \le 3$ (dropped), $z \le 11$, and $3z \le 18 + 21$, that is $z \le 13$. Line L8 keeps $z \le 11$.

*Remove $z$.* Only an upper bound is left, so nothing is added, and line L9 finds no contradiction.

*Back-substitution.* $z$ has only the upper bound 11, so $z = 11$. Then $x_1$ has the lower bounds $0$, $11 - 8 = 3$ and $(33 - 18)/7 = 15/7$ and the upper bound 3, so $x_1 = 3$. Then $x_2$ has the lower bounds $0$ and $(11 - 9)/2 = 1$ and the upper bounds $1$ and $2$, so $x_2 = 1$. The output $(z, x_1, x_2) = (11, 3, 1)$ is the optimum of the LP.

*The certificate.* The row $z \le 11$ carries the multipliers $2 \cdot (1) + 1 \cdot (3) + 1 \cdot (6)$. Its weights $(2, 0, 1)$ on the three constraints of the polygon are exactly the optimal [dual](/dual-linear-program/) solution. If the row $-z \le -12$ is added, the same multipliers plus one copy of the new row sum to $0 \le -1$, a certificate that the value 12 cannot be reached.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Each round keeps two invariants: every row of $R$ is $y^\top (A, b)$ for its stored $y \ge 0$ with zero coefficients on the removed variables, and the solutions of $R$ are exactly the projections of the solutions of $Ax \le b$ onto the remaining variables. The second invariant is the core lemma: a point $x'$ satisfies all the paired rows exactly when every lower bound on $x_k$ at $x'$ is at most every upper bound, which is exactly when some $x_k$ extends $x'$. When no variable is left, the system is feasible exactly when no row says $0 \le \beta$ with $\beta < 0$, and such a row is a certificate by the first invariant. The back-substitution picks each $x_k$ in a nonempty interval, by the same lemma.

## Complexity

**Rows.** If $R$ has $r$ rows before a round, the new system has at most $|Z| + |P| \cdot |N|$ rows, where $|P| + |N| + |Z| = r$. For fixed $|Z|$ the product is at most $((r - |Z|)/2)^2$, and the function $|Z| + ((r - |Z|)/2)^2$ is convex, so it is largest at $|Z| = 0$ or $|Z| = r$. So the new count is at most $\max(r, r^2/4)$. With $m_0 = m$, induction on $k$ gives

$$m_k \le \max\big(m,\ 4 (m/4)^{2^k}\big)$$

after $k$ rounds. For $m \ge 4$ this is $4 (m/4)^{2^k}$, which is doubly exponential in the number of removed variables.

**Time.** Each new row costs $O(n + m)$ arithmetic operations for its coefficients and its multipliers, and the cleaning of line L8 costs about the same with hashing. The back-substitution reads every saved system once. So the total is $O\big(n (m + n) M\big)$ operations, where $M = \max_k m_k \le m^{2^n}$, and the space is $O\big((m + n) M\big)$. In exact rational arithmetic the numbers also grow: each round can roughly double the bit length of the coefficients.

**Lower bounds.** The growth is real. Some systems produce doubly exponentially many rows when redundant rows are not removed, and even with all redundant rows removed, the projection of a polyhedron with few facets can have exponentially many facets. So no projection method can be polynomial in the worst case. For deciding feasibility alone, polynomial methods exist: the [ellipsoid method](/ellipsoid-method/) and [interior point methods](/interior-point-method/).

## Properties

- **Exact.** With rational input and exact arithmetic, the answer has no rounding error.
- **Certifying.** An infeasible input returns a Farkas vector $y$, and a feasible one returns a point; both can be checked by multiplication.
- **Projection.** After removing $x_{k+1}, \ldots, x_n$, the system $R_k$ describes exactly the projection of $\{x : Ax \le b\}$ onto the first $k$ coordinates. So projections of polyhedra are polyhedra.
- **No pivoting and no objective.** Unlike the [simplex method](/simplex-method/), the method needs no basis and no starting point. An objective is handled as in the example, by one extra variable kept to the end.
- **Order matters.** The final answer does not depend on the order of elimination, but the sizes of the intermediate systems do, often by a large factor.

## Variants and improvements

- **Chernikov's rule.** Each row of $R$ is built from a set of input rows, the support of $y$. After $k$ rounds, a row built from more than $k + 1$ input rows is redundant and can be dropped. This simple test removes many redundant rows and bounds the count after $k$ rounds by $\sum_{i \le k+1} \binom{m}{i}$, which is single exponential. Imbert's acceleration theorems refine it.
- **Full redundancy removal.** Testing each row with a small LP removes every redundant row, at the cost of one LP per row.
- **Integer variables.** The Omega test of Pugh (1991) extends the method to integer variables, with "dark" and "gray" shadows; it is used in compilers for dependence analysis.
- **Quantifier elimination.** For linear real arithmetic, Fourier-Motzkin is a quantifier elimination procedure: it removes $\exists x_k$ from a conjunction of linear inequalities. SMT solvers and program analyzers use it, often together with the simplex method.
- **The dual method.** Dantzig and Eaves (1973) showed that the elimination applied to the dual system gives a pivoting method, and that the method proves the [Farkas lemma](/farkas-lemma/) and the duality theorem without any reference to the simplex method.
- **Double description.** The double description method of Motzkin, Raiffa, Thompson and Thrall goes the other way, from inequalities to generators, and is the base of many [vertex enumeration](/vertex-enumeration/) codes.

## When to use it

Use Fourier-Motzkin for small systems, with a few variables, when exact answers, projections or certificates are needed: proving the [Farkas lemma](/farkas-lemma/) and the [Minkowski-Weyl theorem](/minkowski-weyl-theorem/), computing the projection of a polyhedron, or eliminating a few quantifiers in a decision procedure. For large systems that only need a yes or no, or an optimum, use the [simplex method](/simplex-method/) or an [interior point method](/interior-point-method/).

## Pitfalls

- **Floating point.** The method multiplies and adds many rows. In floating point, cancellation errors pile up, and a coefficient that should be zero is not. Use exact rationals, as the implementation does.
- **Forgetting the $Z$ rows.** Rows with a zero coefficient on $x_k$ must be copied to the new system. Dropping them gives a wrong answer.
- **Equations.** An equation can be used to substitute a variable away, as in Gaussian elimination, which does not increase the number of rows. Splitting it into two inequalities and pairing them is correct but wasteful.
- **Integer solutions.** The projection of the integer points is not the set of integer points of the projection. For $2x_2 = x_1$ with $x_1 = 1$, the projection allows $x_1 = 1$, but no integer $x_2$ works.
- **Back-substitution order.** The interval for $x_k$ must be read from $R_k$, the system before $x_k$ was removed, and not from the input system, which also involves the later variables.

## Implementations

## History

Joseph Fourier described the method in 1826 and 1827, in work on systems of linear inequalities that came from mechanics and from the best approximation of data. It was forgotten, and Lloyd Dines found it again around 1919. Theodore Motzkin gave a full treatment in his 1936 thesis in Basel, which also contains his transposition theorem; since then the method carries both names. Sergei Chernikov in the 1960s and Kohler in 1967 gave rules that remove redundant rows. The method has been used since the 1990s in compilers, through Pugh's Omega test, and in verification tools.

## References
