---
tag: N3GN92
kind: algorithm
slug: feasibility-pump
name: Feasibility pump
aliases:
- Fischetti-Glover-Lodi feasibility pump
- FP
area: optimization/integer-programming
level: research
summary: Heuristic that alternates between rounding an LP solution and projecting back onto the LP polyhedron to find a feasible point.
solves: [binary-integer-programming, integer-feasibility]
model: real-ram
complexity:
  vars: {N: the iteration limit, L: the time of one linear program solve, n: the number of variables}
  time: {worst: O(N (L + n log n))}
  space: {extra: O(n)}
properties: {deterministic: false, recursive: false}
prereqs: [lp-relaxation, mixed-integer-programming, simplex-method]
see_also: [local-branching, relaxation-induced-neighborhood-search, diving-heuristic, branch-and-cut, randomized-rounding, integer-feasibility]
sources:
  - paper: doi:10.1007/s10107-004-0570-3
    title: M. Fischetti, F. Glover and A. Lodi, The feasibility pump, Mathematical Programming 104(1), 2005
    locator: pp. 91 to 104; Figure 1 (basic scheme), Section 1 (perturbation), Section 2 (computational results)
  - paper: doi:10.1016/j.disopt.2006.10.001
    title: L. Bertacco, M. Fischetti and A. Lodi, A feasibility pump heuristic for general mixed-integer problems, Discrete Optimization 4(1), 2007
    locator: pp. 63 to 76
  - paper: doi:10.1016/j.disopt.2006.10.004
    title: T. Achterberg and T. Berthold, Improving the feasibility pump, Discrete Optimization 4(1), 2007
    locator: pp. 77 to 86 (objective feasibility pump)
  - paper: doi:10.1007/s12532-009-0007-3
    title: M. Fischetti and D. Salvagnin, Feasibility pump 2.0, Mathematical Programming Computation 1, 2009
    locator: whole paper (rounding with constraint propagation)
---

The feasibility pump is a heuristic that looks for a feasible point of a [0-1 mixed integer program](/binary-integer-programming/). It keeps two points: a point of the [LP relaxation](/lp-relaxation/) and a 0-1 point, and it moves each one in turn to the nearest point of the other kind, until they meet. Fischetti, Glover and Lodi published it in 2005. It does not aim at the optimum, and it can stop without a solution even when one exists.

## In plain words

A mixed integer program has two kinds of conditions: the linear constraints, and the rule that some variables are 0 or 1. It is easy to meet each kind alone, but hard to meet both at once.

The pump keeps one point that meets the linear constraints and one point that meets the 0 or 1 rule. In each round it rounds the first point to get a new second point, and then it asks a linear program for the point that meets the constraints and is as close as possible to the second point. When the two points are equal, that point meets all conditions. If the rounding gives the same point again, the pump changes a few of its values to escape. After a fixed number of rounds without success, it gives up.

## The problem

The input is a 0-1 mixed integer program

$$\min\ c^\top x \quad \text{subject to} \quad A x \le b,\quad x \ge 0,\quad x_j \in \{0, 1\}\ (j \in I),$$

with rational data and a set $I$ of binary variables. The other variables are continuous. Let $P = \{x \ge 0 : A x \le b,\ x_j \le 1\ (j \in I)\}$ be the polyhedron of the [LP relaxation](/lp-relaxation/). A point $x$ is *integer* if $x_j \in \{0, 1\}$ for all $j \in I$. The output is a point $x \in P$ that is integer, or INFEASIBLE when $P$ is empty, or FAIL. The pump uses the cost $c$ only for its first point.

For a point $x \in P$ and a 0-1 vector $\tilde{x} \in \{0,1\}^I$, the *distance* is

$$\Delta(x, \tilde{x}) = \sum_{j \in I:\ \tilde{x}_j = 0} x_j + \sum_{j \in I:\ \tilde{x}_j = 1} (1 - x_j),$$

the $\ell_1$ distance of $x_I$ from $\tilde{x}$. It is linear in $x$ for a fixed $\tilde{x}$. The *rounding* $[x]$ sets $[x]_j = 1$ when $x_j \ge 1/2$ and $[x]_j = 0$ otherwise, for $j \in I$.

## The algorithm

The parameters are the iteration limit $N$, the flip count $T$ and the restart period $R$.

```pseudo id=main
FEASIBILITY-PUMP(c, A, b, I, N, T, R)
L1  k ← 0;  x* ← a point of P of minimum cost (any point of P if the cost is unbounded);  if P = ∅ then return INFEASIBLE
L2  if x* is integer then return x*
L3  x̃ ← [x*]
L4  while k < N do
L5      k ← k + 1;  x* ← a point of P that minimizes Δ(x, x̃)
L6      if x* is integer then return x*
L7      if k is a multiple of R, or [x*] ≠ x̃ and [x*] is one of the x̃ of the last 3 iterations then
L8          for each j ∈ I: draw ρⱼ uniformly in [−0.3, 0.7]; flip x̃ⱼ if |x*ⱼ − x̃ⱼ| + max(ρⱼ, 0) > 1/2
L9      else if [x*] ≠ x̃ then x̃ ← [x*]
L10     else flip the TT entries x̃ⱼ with the largest |x*ⱼ − x̃ⱼ|, with TT drawn uniformly from ⌊T/2⌋ to ⌊3T/2⌋
L11 return FAIL
```

To *flip* $\tilde{x}_j$ means to replace it with $1 - \tilde{x}_j$. Line L5 is one linear program: its objective is $\Delta(x, \tilde{x})$, a linear function, and it is bounded below by 0 on $P$. Line L9 is the normal move. Line L10 handles a cycle of length 1, where the rounding gives back the same $\tilde{x}$; the flips change the variables that are the most fractional with respect to $\tilde{x}$. Lines L7 and L8 handle longer cycles with a random restart, and they also run every $R$ iterations. The code keeps TT between 1 and $|I|$. Fischetti, Glover and Lodi detect a cycle by a comparison with the last 3 iterations, as line L7 does, and they used $T = 20$ and $R = 100$ in their tests.

## Example

Take three binary variables and

$$\min\ -3x_2 - 2x_3 \quad \text{subject to} \quad -x_1 + 3x_3 \le 1,\quad 3x_1 + 2x_2 - x_3 \le 3,\quad x \in \{0, 1\}^3,$$

with $T = 1$, so that TT $= 1$. Ties in line L10 go to the smaller index.

| step | $\tilde{x}$ before | $x^*$ | $\Delta(x^*, \tilde{x})$ | move | $\tilde{x}$ after |
|---|---|---|---|---|---|
| L1 to L3 | none | $(1/2, 1, 1/2)$ | none | round | $(1, 1, 1)$ |
| iteration 1 | $(1, 1, 1)$ | $(1/2, 1, 1/2)$ | 1 | flip $x_1$ (line L10) | $(0, 1, 1)$ |
| iteration 2 | $(0, 1, 1)$ | $(0, 1, 1/3)$ | 2/3 | round (line L9) | $(0, 1, 0)$ |
| iteration 3 | $(0, 1, 0)$ | $(0, 1, 0)$ | 0 | return | none |

The first linear program has the optimal value $-4$ at $(1/2, 1, 1/2)$. In iteration 1 the closest point of $P$ to $(1, 1, 1)$ is the same point, so the rounding gives no progress and line L10 flips $x_1$, one of the two entries at distance $1/2$. In iteration 3 the distance is 0, so $x^* = \tilde{x}$ is a feasible 0-1 point. Of the 8 binary points, only $(0,0,0)$, $(0,1,0)$ and $(1,0,0)$ are feasible, so the returned point with cost $-3$ is also optimal here. The pump does not aim for this, and on other instances its point has a worse cost.

## Correctness

A heuristic has a weaker correctness claim than an exact algorithm. The proof below shows four facts.

1. Each point returned at lines L2 and L6 is feasible, because it lies in $P$ and is integer.
2. INFEASIBLE is returned only when $P$ is empty, and then the program has no feasible point, since each feasible point lies in $P$.
3. The method stops after at most $N + 1$ linear programs.
4. If at line L5 the vector $\tilde{x}$ is the 0-1 part of some feasible point, then the linear program of line L5 returns a feasible point. The reason: $\Delta(x, \tilde{x}) \ge 0$ on $P$, with equality exactly when $x_I = \tilde{x}$.

Between two rounding moves the distance does not grow: the rounding $[x^*]$ is the 0-1 vector closest to $x^*$ in the distance $\Delta$, and line L5 is the point of $P$ closest to $\tilde{x}$. So the plain pump is an alternating minimization of $\Delta$ over its two arguments. A FAIL answer proves nothing: the program may still have a feasible point. The full proof is below.

## Complexity

Each iteration solves one linear program in time $L$ and does $O(n)$ work for the rounding and the restart, plus $O(n \log n)$ for the sort of line L10. So the time is $O(N(L + n \log n))$ in the worst case, and the extra space beyond the linear program solver is $O(n)$. A linear program can be solved in polynomial time by the [ellipsoid method](/ellipsoid-method/) or by interior point methods, so for a fixed $N$ the pump runs in polynomial time. Since the question "does a 0-1 program have a feasible point" is [NP-complete](/np-complete/), no polynomial method finds a point on every feasible instance unless P = NP. In practice the linear programs of consecutive iterations differ only in the objective, so the [primal simplex method](/simplex-method/) starts each one from the last basis.

## Properties

- **Not complete.** It can return FAIL on a feasible instance, and it never proves infeasibility unless the LP relaxation is empty.
- **Randomized.** Lines L8 and L10 use random numbers. A fixed seed makes a run repeatable.
- **Blind to the cost.** After line L1 the cost does not enter the method, so the first point found can be far from the optimum.
- **Monotone between perturbations.** In a run of rounding moves, the sequence of distances $\Delta(x^*, \tilde{x})$ does not increase.

## Variants and improvements

- **General integer variables.** Bertacco, Fischetti and Lodi extend the distance to general integer variables with extra variables for the positive and negative parts of $x_j - \tilde{x}_j$, and they change the perturbation.
- **Objective feasibility pump.** Achterberg and Berthold replace $\Delta$ with a convex combination of $\Delta$ and the scaled cost $c^\top x$. The weight of the cost decreases geometrically from one iteration to the next. They report better solutions at a moderate extra cost.
- **Feasibility pump 2.0.** Fischetti and Salvagnin round one variable at a time and propagate the constraints after each choice, so that the rounded point violates fewer rows.
- **As a start for other heuristics.** The point that the pump returns can serve as the incumbent for [local branching](/local-branching/) or [RINS](/relaxation-induced-neighborhood-search/), which improve the cost.

## When to use it

Use the feasibility pump at the root node of a [branch and cut](/branch-and-cut/) search when the solver has no feasible point and the problem has many binary variables. The cost is a few linear programs. A feasible point gives an upper bound and allows pruning by bound in the tree. If the problem is easy for rounding or [diving](/diving-heuristic/), those are cheaper. If the problem has few feasible points, such as a tightly constrained scheduling model, the pump often fails, and a tree search is the only reliable way to find a point or to prove that none exists.

## Pitfalls

- **Treating FAIL as a proof.** Only the empty LP relaxation proves infeasibility. The test with $2x_1 + 2x_2 = 1$, where the LP relaxation is not empty but has no 0-1 point, must end with FAIL.
- **Endless cycles.** Without lines L7 to L10, the pump can visit the same pair of points again and again. The flips handle cycles of length 1, and the restart handles longer ones.
- **The rounding at exactly 1/2.** The code and the proof use one fixed rule ($x_j \ge 1/2$ rounds up). A rule that changes between calls can break the cycle test.
- **Unbounded first linear program.** If the cost is unbounded on $P$, line L1 has no minimum. Take any point of $P$, as the code does. The linear programs of line L5 are always bounded.
- **Tolerance.** With floating-point arithmetic, the test "x* is integer" needs a tolerance, and the returned point must be checked against the constraints again.

## Implementations

The Python code uses `fractions.Fraction` and an exact two-phase simplex with [Bland's rule](/bland-rule/), so the integer test at line L6 is exact. It uses a seeded `random.Random` for lines L8 and L10. The tests check that each returned point is feasible, that INFEASIBLE comes only when no 0-1 point exists, that no point is returned when no 0-1 point exists, and that the example above gives the trace in the table. They do not check that the pump finds a point, because it is a heuristic.

## History

Fischetti, Glover and Lodi presented the feasibility pump in 2005 for 0-1 mixed integer programs. In their tests on 83 instances (44 from MIPLIB 2003 and 39 more hard 0-1 problems), with $T = 20$, $R = 100$ and a time limit of 1800 seconds, the pump failed to find a feasible point on 3 instances, while the root node heuristics of ILOG-Cplex 8.1 failed on 19. These are measured results on one test set, not a guarantee. Bertacco, Fischetti and Lodi, and Achterberg and Berthold, published the extensions to general integers and to the cost in 2007, and Fischetti and Salvagnin published Feasibility pump 2.0 in 2009.

## References
