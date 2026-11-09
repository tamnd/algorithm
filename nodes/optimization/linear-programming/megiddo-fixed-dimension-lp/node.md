---
tag: FG0RRG
kind: algorithm
slug: megiddo-fixed-dimension-lp
name: Megiddo's algorithm for fixed-dimension linear programming
aliases:
- Megiddo's linear-time LP
- Megiddo's algorithm
- linear programming in fixed dimension
area: optimization/linear-programming
level: research
summary: Deterministic linear-time LP in fixed dimension via prune-and-search.
solves: [linear-programming-problem]
model: real-ram
complexity:
  vars: {n: the number of variables (fixed), m: the number of constraints}
  time: {worst: O(2^(2^n) m)}
  space: {extra: O(m)}
properties: {deterministic: true, exact: true, online: false, recursive: true}
history:
  year: 1983
  people: [Nimrod Megiddo, Martin E. Dyer]
  note: Megiddo (1983) and Dyer (1984) gave linear-time algorithms for two and three variables; Megiddo (1984) extended the method to every fixed dimension.
prereqs: [prune-and-search, median-of-medians, linear-programming-problem]
see_also: [seidel-linear-programming, prune-and-search, lp-type-problem, clarksons-algorithm, minimum-enclosing-circle, simplex-method, ellipsoid-method, half-plane-intersection]
sources:
  - paper: doi:10.1137/0212052
    title: Nimrod Megiddo, Linear-time algorithms for linear programming in R^3 and related problems, SIAM Journal on Computing 12(4), 1983
    locator: pages 759 to 776, the algorithm for two variables with the oracle on a vertical line, and its extension to three variables
  - paper: doi:10.1145/2422.322418
    title: Nimrod Megiddo, Linear programming in linear time when the dimension is fixed, Journal of the ACM 31(1), 1984
    locator: pages 114 to 127, multidimensional search and the bound O(2^(2^d) n)
  - paper: doi:10.1137/0213003
    title: Martin E. Dyer, Linear time algorithms for two- and three-variable linear programs, SIAM Journal on Computing 13(1), 1984
    locator: pages 31 to 45
  - paper: doi:10.1137/0215052
    title: Martin E. Dyer, On a multidimensional search technique and its application to the Euclidean one-centre problem, SIAM Journal on Computing 15(3), 1986
    locator: pages 725 to 738, the improved bound O(3^(d^2) n)
  - paper: doi:10.1016/0020-0190(86)90037-2
    title: Kenneth L. Clarkson, Linear programming in O(n 3^(d^2)) time, Information Processing Letters 22(1), 1986
    locator: pages 21 to 24
  - paper: doi:10.1006/jagm.1996.0060
    title: Bernard Chazelle and Jiří Matoušek, On linear-time deterministic algorithms for optimization problems in fixed dimension, Journal of Algorithms 21(3), 1996
    locator: pages 579 to 597, the deterministic bound d^(O(d)) n
---

Megiddo's algorithm solves a [linear program](/linear-programming-problem/) with a fixed number $n$ of variables and $m$ constraints in $O(m)$ time, with no randomness. In two variables it is a direct use of [prune and search](/prune-and-search/): pair the constraints, take the median of the points where the pairs cross, ask on which side of the median the optimum lies, and drop one constraint of every pair that crosses on the wrong side. In $n$ variables, a *multidimensional search* answers such questions by solving linear programs in $n - 1$ variables. The time is linear in $m$, but the constant grows as $2^{2^n}$, so the method matters most in theory and for $n = 2$ and $3$.

## In plain words

A program in two variables asks for the lowest point of a region in the plane that many straight lines cut out. Only two of the lines meet at the answer; the others are spare. The method throws spare lines away in rounds. In each round it pairs the lines. Two lines of a pair cross somewhere, and on one side of the crossing, only one of them matters. The method picks the middle crossing and finds out, with a cheap test along a vertical line, on which side of it the answer lies. For half of the pairs, the crossing is on the far side, so one line of each such pair can go.

At least a quarter of the lines go in each round. So the rounds get shorter and shorter, and the total work is only a few times the number of lines.

## The problem

Minimize $c^\top x$ subject to $a_i^\top x \le b_i$ for $i = 1, \ldots, m$, with $x \in \mathbb{R}^n$ and $n$ a constant. The answer is an optimal point, INFEASIBLE, or UNBOUNDED. Many problems in computational geometry have this form with $n = 2$ or $3$: the separation of two point sets by a line, the intersection of half-planes, the lowest point of a convex polygon given by its edges. The [minimum enclosing circle](/minimum-enclosing-circle/) is not a linear program, but Megiddo solved it with the same method.

## The algorithm

*Two variables.* Change the variables so that the objective is "minimize $y$" (for $c = (c_1, c_2)$ with $c_2 \ne 0$, use $u = x_1$ and $y = c_1 x_1 + c_2 x_2$). Then each constraint is of one of three types: a *lower line* $y \ge s x + t$, an *upper line* $y \le s x + t$, or a bound on $x$. Let $F(x)$ be the largest of the lower lines at $x$ and $G(x)$ the smallest of the upper lines. $F$ is convex and $G$ is concave, both piecewise linear. The program is: minimize $F(x)$ over $lo \le x \le hi$ with $F(x) \le G(x)$.

The *oracle* at a point $x_m$ computes $F(x_m)$, $G(x_m)$, and the least and largest slopes $f_-$, $f_+$ of the lower lines that attain $F(x_m)$ (and $g_-$, $g_+$ for $G$), in $O(m)$ time.

- If $F(x_m) \le G(x_m)$, then $x_m$ is feasible. If $f_+ < 0$, then $F$ falls to the right, and the optimum is to the right. If $f_- > 0$, it is to the left. Otherwise $0$ is a subgradient of $F$ at $x_m$, and $x_m$ is optimal.
- If $F(x_m) > G(x_m)$, then the convex function $F - G$ has the slopes $f_- - g_+$ to $f_+ - g_-$ at $x_m$. If $f_- - g_+ > 0$, every feasible point is to the left; if $f_+ - g_- < 0$, every feasible point is to the right; otherwise $F - G$ has its minimum at $x_m$, and that minimum is positive, so the program is infeasible.

```pseudo id=main
MEGIDDO-2D(A, b, c)
L1  change the variables so that the objective is "minimize y"; split the constraints into lower lines, upper lines and the bounds lo ≤ x ≤ hi
L2  if there is no lower line then return UNBOUNDED if lo ≤ hi, else INFEASIBLE
L3  while more than 6 lines remain
L4      pair the lower lines and pair the upper lines; for a pair that is parallel or crosses outside (lo, hi), drop the line that is redundant on [lo, hi]
L5      x_m ← the median of the crossing points of the remaining pairs     ▷ linear-time selection
L6      ask the oracle at x_m: OPTIMAL or INFEASIBLE ends the run; LEFT sets hi ← x_m; RIGHT sets lo ← x_m
L7      for each pair whose crossing point is now outside (lo, hi), drop its redundant line
L8  solve the program on the at most 6 lines that remain by brute force
```

On one side of its crossing point, one line of a pair is above the other. For a pair of lower lines, the lower of the two cannot be the maximum $F$ there, so it can go; for a pair of upper lines, the higher one can go. The base case of line L8 checks the crossing points of the few remaining lines and the bounds, and the behavior of $F$ and $G$ as $x \to \pm\infty$, which decides UNBOUNDED.

*Any fixed dimension.* Megiddo (1984) replaces the vertical line by a hyperplane. For a set of hyperplanes through the space of $x$, the *multidimensional search* finds, with a constant number of oracle calls, on which side of a constant fraction of them the optimum lies. Each oracle call solves a linear program in $n - 1$ variables, on the query hyperplane, by the same method. One line of each pair of constraints can then go, as in the plane. The recursion over the dimension gives the time $O(2^{2^n} m)$.

## Example

Minimize $x_2$ subject to the twelve constraints $x_2 \ge s x_1 - s^2 + 2s$ for $s = 5, -5, 9, -1, -9, 1, 11, -3, -7, 3, -11, 7$ (in this order). The objective is already "minimize $y$" with $x = x_1$ and $y = x_2$, all twelve are lower lines, and there are no bounds. Two of these lines cross at $x = s + s' - 2$. The optimum is $(-2, -1)$, where the lines with $s = -1$ and $s = 1$ meet.

| round | lines | pairs and their crossings | median | oracle | dropped |
|---|---|---|---|---|---|
| 1 | 12 | $(5, -5)$ at $-2$; $(9, -1)$ at $6$; $(-9, 1)$ at $-10$; $(11, -3)$ at $6$; $(-7, 3)$ at $-6$; $(-11, 7)$ at $-6$ | $-6$ | RIGHT | $s = -9, -7, -11$ |
| 2 | 9 | $(5, -5)$ at $-2$; $(9, -1)$ at $6$; $(1, 11)$ at $10$; $(-3, 3)$ at $-2$; the line $7$ alone | $-2$ | OPTIMAL | none |

In round 1, $F(-6)$ is $3$, attained by the lines $s = -3$ and $s = -1$. Both slopes are negative, so $F$ falls to the right, and the optimum lies right of $-6$. The three pairs that cross at $-10$ or $-6$ each lose the line of smaller slope, which is the lower of the two on $[-6, \infty)$. In round 2, $F(-2) = -1$ is attained by the slopes $-1$ and $1$, so $0$ is a subgradient, and $x_1 = -2$ is optimal with $x_2 = F(-2) = -1$.

## Correctness

Pruning a pair never changes $F$ or $G$ on the current interval $[lo, hi]$, since the dropped line is below its partner (or above it, for upper lines) on the whole interval. The oracle is correct by convexity: a subgradient $g$ of a convex function at $x_m$ gives $F(x) \ge F(x_m) + g(x - x_m)$, so all points on one side are worse than $x_m$, or infeasible. So each new interval contains an optimal point if one exists, keeps the program unbounded if it is unbounded, and keeps it infeasible if it is infeasible. The proof file gives the details, and the count of dropped lines below.

## Complexity

Model: arithmetic operations on reals have unit cost (the [real RAM](/real-ram/)).

- **Two variables.** Let $N$ be the number of lines at the start of a round and $P \ge (N - 2)/2$ the number of pairs. Each pair either is dropped at line L4, or has a crossing point in $(lo, hi)$. At least half of the crossing points lie on the far side of the median, so at least $\lceil P/2 \rceil$ lines go, about $N/4$. A round costs $O(N)$ with [linear-time selection](/median-of-medians/). The sizes fall at least as fast as $N, \frac34 N, (\frac34)^2 N, \ldots$, a geometric series, so the total is $O(m)$.
- **$n$ variables.** Megiddo's bound is $O(2^{2^n} m)$. Dyer (1986) and Clarkson (1986) improved it to $O(3^{n^2} m)$, and Chazelle and Matoušek (1996) to $n^{O(n)} m$, all deterministic.
- **Space.** $O(m)$.

## Properties

- **Deterministic and exact.** With rational input the implementation works in exact fractions, and it returns an optimal vertex, or a correct report of infeasibility or unboundedness.
- **Linear in $m$.** Optimal for fixed $n$, since each constraint must be read.
- **Huge constant in $n$.** The double exponential limits the method to small $n$. For larger fixed $n$, randomized methods are much better.
- **Oracle-based.** It needs only the answer to "on which side is the optimum", which also solves related problems such as the minimum enclosing circle and the one-center problem.

## Variants and improvements

- **[Seidel's algorithm](/seidel-linear-programming/).** A randomized incremental method with expected time $O(n!\, m)$, much simpler to code and better in $n$.
- **[Clarkson's algorithm](/clarksons-algorithm/).** Random sampling with $O(n^2 m + n^{O(\sqrt n)} \log m)$ expected time, when it is combined with a subexponential base method.
- **Subexponential methods.** Kalai, and Matoušek, Sharir and Welzl, gave methods with $e^{O(\sqrt{n \log m})}$ expected time for the base case, which lead to the best bounds for [LP-type problems](/lp-type-problem/).
- **Dyer's version.** Found at the same time for two and three variables, with the same pairing idea.

## When to use it

Use it for linear programs in two or three variables when a worst-case bound with no randomness is required, and for problems that only give a side-of-the-optimum oracle. In code with a random source, [Seidel's algorithm](/seidel-linear-programming/) is simpler and faster in practice. For linear programs in many variables, use the [simplex method](/simplex-method/) or an [interior-point method](/interior-point-method/).

## Pitfalls

- **Parallel lines.** Two lines of a pair with the same slope do not cross. Keep the one that matters (the higher lower line, the lower upper line) at once.
- **Crossings on the boundary.** A crossing point equal to $lo$ or $hi$ is outside the open interval, and one line of the pair can go; the two lines agree at that point.
- **Unboundedness and infeasibility.** A version that only handles bounded programs is common in textbooks. A full version needs the oracle cases for infeasible points and the base-case checks as $x \to \pm\infty$.
- **Sorting instead of selection.** Taking the median by sorting gives $O(m \log m)$ time per round and $O(m \log m)$ in total.

## Implementations

The Python version solves programs in two variables in exact fractions, with the median of medians for selection. The tests compare it with a brute force over all vertices and all candidate rays on 800 random programs with up to 14 constraints, which cover the optimal, unbounded and infeasible cases. They check that at least a quarter of the lines, less two, go in each round on bounded programs with up to 54 constraints, and they also run programs whose lower lines are all tangent to a parabola, so that every line matters for some objective.

## History

Megiddo found the method for two and three variables in 1982, published in 1983, and Dyer found it independently (1984). Megiddo's paper of 1984 showed that linear programming in any fixed dimension takes linear time. The question of a better dependence on the dimension led to the randomized methods of Clarkson and Seidel, to the subexponential methods of Kalai and of Matoušek, Sharir and Welzl, and to the framework of [LP-type problems](/lp-type-problem/).

## References
