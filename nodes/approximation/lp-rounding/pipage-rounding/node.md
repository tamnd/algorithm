---
tag: 158NR5
kind: technique
slug: pipage-rounding
name: Pipage rounding
aliases:
- Ageev-Sviridenko pipage rounding
- pipage method
area: approximation/lp-rounding
level: advanced
summary: Move weight along pairs of fractional variables until one becomes integral, choosing the end that does not lower a nonlinear objective that is convex along each move.
prereqs: [linear-programming-rounding, lp-relaxation, convex-function, max-coverage]
see_also: [dependent-rounding, swap-rounding, max-coverage, greedy-max-coverage, max-coverage-inapproximability, maximum-cut, submodular-function, matroid]
sources:
  - paper: doi:10.1023/B:JOCO.0000038913.96607.c2
    title: Alexander A. Ageev and Maxim I. Sviridenko, Pipage rounding, a new method of constructing algorithms with proven performance guarantee, Journal of Combinatorial Optimization 8(3), 2004
    locator: pages 307 to 328
  - paper: doi:10.1137/080733991
    title: Gruia Calinescu, Chandra Chekuri, Martin Pál and Jan Vondrák, Maximizing a monotone submodular function subject to a matroid constraint, SIAM Journal on Computing 40(6), 2011
    locator: pages 1740 to 1766
---

Pipage rounding is a deterministic way to round a fractional solution for a maximization problem whose true objective $F$ is not linear. It uses two functions: a function $L$ that an LP can maximize, and the objective $F$, with $F(x) \ge c \cdot L(x)$ on the feasible region. Solve the LP for $x^*$. Then, while $x$ is fractional, move along a line $x + t(e_i - e_l)$ that keeps the constraints, in both directions, until a new coordinate is integral, and keep the end with the larger $F$. If $F$ is convex along each such line, the larger end is at least $F(x)$, so $F$ never falls. Ageev and Sviridenko (2004) introduced the method. For [maximum coverage](/max-coverage/) with a budget of $k$ sets it gives the ratio $1 - 1/e$ in the worst case, which is the best possible unless P = NP.

## In plain words

Suppose a fractional plan scores well, and you must make every choice whole without losing score. Pick two choices that are still partial, and shift weight from one to the other, so that the total stays the same.

Shift until one of them becomes whole. You can shift in either direction, and for the problems where this method works, the score along the shift is shaped like a bowl or a straight line. So at least one of the two ends scores at least as well as the start. Keep that end. Each shift makes one more choice whole, so after a few shifts the plan is fully whole and has not lost score.

## When it applies

- **A maximization problem with a nonlinear objective.** The value of a 0-1 solution is $F(x)$ for a function $F$ on $[0, 1]^n$ that agrees with the objective at integral points, such as the expected coverage of independent random choices.
- **A linear lower bound.** A function $L$, concave and piecewise linear so that an LP can maximize it, has $F(x) \ge c \cdot L(x)$ for all feasible $x$, and $L$ agrees with the objective at integral points, so $\max L \ge \text{OPT}$.
- **Convexity along moves.** The feasible region allows moves along $e_i - e_l$ for two fractional coordinates, as for a cardinality constraint $\sum_i x_i = k$ or the degree constraints of a bipartite graph, and $F$ is convex along each such move.

## The template

```pseudo id=main
PIPAGE(F, L, P)
L1  x ← an optimal solution of max L(x) over the polytope P             ▷ an LP
L2  while x has fractional coordinates
L3      d ← a move e_i − e_l, or a cycle or path of moves, that keeps P   ▷ hole: MOVE
L4      t₊ ← the largest t with x + t·d ∈ P
L5      t₋ ← the largest t with x − t·d ∈ P
L6      x ← whichever of x + t₊·d and x − t₋·d has the larger F          ▷ hole: EVALUATE F
L7  return x
```

**Claim.** If $F$ is convex along each move of line L3 and $F \ge c \cdot L$ on $P$, then PIPAGE returns an integral $\hat{x} \in P$ with $F(\hat{x}) \ge c \cdot \text{OPT}$.

*Proof.* On the segment from $x - t_- d$ to $x + t_+ d$, the function $g(t) = F(x + t d)$ is convex, so $g(0) \le \max(g(-t_-), g(t_+))$. So $F$ does not fall in a step. Each step makes at least one more coordinate integral, by the choice of $t_+$ and $t_-$, and an integral coordinate stays integral, so there are at most $n$ steps. At the end, $F(\hat{x}) \ge F(x^*) \ge c \cdot L(x^*) \ge c \cdot \text{OPT}$, since $L(x^*) = \max_P L \ge \text{OPT}$. $\square$

The LP of line L1 has polynomial size in the examples below, so it is solved in polynomial time with an interior point or ellipsoid method and no separation oracle. The loop has at most $n$ steps, each with two evaluations of $F$.

**The holes.**

- **MOVE.** With one constraint $\sum_i x_i = k$, any two fractional coordinates give a move, and two always exist when $x$ is fractional, because $k$ is an integer. With bipartite degree constraints, a move is a cycle or a maximal path of fractional edges, as in [dependent rounding](/dependent-rounding/).
- **EVALUATE F.** For coverage and cut problems, $F$ is a polynomial that can be computed in closed form. For the multilinear extension of a general [submodular function](/submodular-function/), $F$ is estimated by random sampling.

## Classic examples

- **Maximum coverage.** Elements $j$ with weights $w_j \ge 0$, sets $S_1, \ldots, S_m$, and a budget of $k$ sets. The LP maximizes $L(x) = \sum_j w_j \min(1, \sum_{i : j \in S_i} x_i)$ subject to $\sum_i x_i = k$ and $0 \le x \le 1$. Let $F(x) = \sum_j w_j \big(1 - \prod_{i : j \in S_i} (1 - x_i)\big)$, the expected coverage when each set is taken with probability $x_i$. If element $j$ is in $q_j$ sets, the inequality of arithmetic and geometric means gives $1 - \prod (1 - x_i) \ge \big(1 - (1 - 1/q_j)^{q_j}\big) \min(1, \sum x_i)$, so $F \ge (1 - 1/e) L$. Along $e_i - e_l$, the factor for an element in both sets is $(1 - x_i - t)(1 - x_l + t)$, whose $t^2$ term is $-t^2$, so $F$ gains $+t^2$ times a nonnegative product and is convex; for an element in one of the sets it is linear. So pipage gives $1 - 1/e$, and $1 - (1 - 1/q)^q$ when each element is in at most $q$ sets. Feige (1998) showed that no ratio $1 - 1/e + \varepsilon$ is possible unless P = NP; see [max coverage inapproximability](/max-coverage-inapproximability/). The [greedy algorithm](/greedy-max-coverage/) reaches the same ratio, but pipage also works with the extra constraints below.
- **A step in numbers.** Take $S_1 = \{a, b\}$, $S_2 = \{b, c\}$, $S_3 = \{a, c\}$ with unit weights and $k = 1$, at the point $x = (\frac12, \frac12, 0)$. Then $L(x) = 2$ and $F(x) = \frac12 + \frac34 + \frac12 = \frac74$. Along $e_1 - e_2$, $F(x + t(e_1 - e_2)) = \frac74 + t^2$ for $t \in [-\frac12, \frac12]$, and both ends, $(1, 0, 0)$ and $(0, 1, 0)$, have $F = 2$.
- **Coverage with a partition constraint.** The sets are split into groups, and at most $k_g$ sets may come from group $g$. A move is between two fractional sets of the same group, or along one coordinate when a group has only one fractional set. $F$ is convex along the first kind of move and linear along the second, so the ratio $1 - 1/e$ holds again. The greedy algorithm gives only $\frac12$ under a partition constraint.
- **Maximum cut with given part sizes.** Find a set $S$ with $|S| = p$ that maximizes the weight of the cut. With $F(x) = \sum_{uv \in E} w_{uv} (x_u + x_v - 2 x_u x_v)$ and $L(x) = \sum_{uv} w_{uv} \min(1, x_u + x_v, 2 - x_u - x_v)$ under $\sum_v x_v = p$, one has $F \ge \frac12 L$, and $F$ is convex along $e_u - e_v$. Ageev and Sviridenko got the ratio $\frac12$ in this way; see [maximum cut](/maximum-cut/).

## Variations

- **Randomized pipage.** Choose the end at random, with probabilities that keep the expectation of $x$. Convexity then gives $\mathbb{E}[F(\hat{x})] \ge F(x^*)$. On bipartite graphs this is [dependent rounding](/dependent-rounding/).
- **Pipage on a matroid.** Calinescu, Chekuri, Pál and Vondrák (2011) extended pipage to the base polytope of a [matroid](/matroid/), with the multilinear extension of a monotone submodular function as $F$. With the continuous greedy algorithm in place of the LP, this gives $1 - 1/e$ for a monotone submodular function under a matroid constraint.
- **Swap rounding.** A faster rounding for matroid polytopes, which merges bases and gives negative correlation; see [swap rounding](/swap-rounding/).

## Pitfalls

- **Concave in place of convex.** The method needs $F$ convex along each move. Along a move where $F$ is concave, both ends can be worse than the start.
- **Moves that leave the polytope.** Each move must keep all constraints. With more than one constraint per variable, a move between two coordinates can break a third constraint; use cycles and paths of the constraint graph.
- **Comparing with F at the LP point.** The bound is $F(\hat{x}) \ge F(x^*)$, not $F(\hat{x}) \ge L(x^*)$. The ratio comes from $F \ge c \cdot L$, which must be proved on the whole region.
- **Sampled F.** When $F$ is estimated by sampling, the comparison in line L6 can choose the wrong end, and the bound holds only with high probability and up to a small loss.

## Exercises

1. Prove that $1 - \prod_{i=1}^{q} (1 - x_i) \ge \big(1 - (1 - 1/q)^q\big) \min(1, \sum_i x_i)$ for $x \in [0, 1]^q$.
2. Show that the expected coverage $F$ is convex along $e_i - e_l$ for each pair $i \ne l$.
3. Show that if $x$ satisfies $\sum_i x_i = k$ with $k$ an integer and some coordinate is fractional, then at least two coordinates are fractional.
4. For maximum cut with given part sizes, prove $x_u + x_v - 2 x_u x_v \ge \frac12 \min(1, x_u + x_v, 2 - x_u - x_v)$ on $[0, 1]^2$.

## References
