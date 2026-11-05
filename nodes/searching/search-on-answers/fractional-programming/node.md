---
tag: TJ9ARW
kind: concept
slug: fractional-programming
name: Fractional programming
aliases:
- linear fractional programming
- parametric ratio optimization
area: searching/search-on-answers
level: advanced
summary: Optimization of a ratio of functions, typically handled by parametric reformulation.
prereqs: [optimization-to-decision-reduction, binary-search-on-real-numbers, linear-programming-problem]
see_also: [dinkelbach-algorithm, minimum-ratio-problem, parametric-search, minimum-mean-cycle-problem, maximum-density-segment, quasiconvex-function, binary-search-on-real-numbers, lagrangian-relaxation]
sources:
  - paper: doi:10.1287/mnsc.13.7.492
    title: "Werner Dinkelbach, On nonlinear fractional programming, Management Science 13(7) (1967), 492-498"
  - paper: doi:10.1002/nav.3800090303
    title: "A. Charnes and W. W. Cooper, Programming with linear fractional functionals, Naval Research Logistics Quarterly 9(3-4) (1962), 181-186"
  - paper: doi:10.1287/moor.4.4.414
    title: "Nimrod Megiddo, Combinatorial optimization with rational objective functions, Mathematics of Operations Research 4(4) (1979), 414-424"
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 3.4, Quasiconvex functions, and Section 4.3.2, Linear-fractional programming
---

Fractional programming is the optimization of a ratio $N(x)/D(x)$ of two functions over a feasible set, with $D > 0$, such as cost per unit of time, profit per unit of weight or the average of a chosen set. A ratio is not linear even when $N$ and $D$ are, but the parametric function $F(\lambda) = \min_x \big(N(x) - \lambda D(x)\big)$ is decreasing in $\lambda$ and is zero exactly at the optimal ratio. So the ratio problem reduces to a search for the root of $F$, and each evaluation of $F$ is an ordinary problem with the linear objective $N - \lambda D$. The search is a [binary search on real numbers](/binary-search-on-real-numbers/), the Newton iteration of [Dinkelbach's algorithm](/dinkelbach-algorithm/), or [parametric search](/parametric-search/); linear ratios over a polyhedron also reduce to one linear program by the Charnes-Cooper transformation.

## In plain words

Many goals are ratios: the cheapest cost per hour, the best average grade, the most profit per kilogram. A ratio is hard to optimize directly, because making the top larger can make the bottom larger too.

The trick is to guess the answer. Suppose you guess that a cost per hour of 7 is possible. Then the question becomes: is there a choice where the cost minus 7 times the hours is at most zero? That question has no ratio in it, so ordinary methods can answer it. If the answer is yes, the true best ratio is 7 or less; if no, it is more than 7. So you can search for the best ratio by guessing, as in a binary search, or by a smarter guess each time.

## The idea

**The problem.** Let $X$ be a set of feasible solutions, and $N, D : X \to \mathbb{R}$ with $D(x) > 0$ for all $x \in X$. Fractional programming asks for

$$\lambda^* = \min_{x \in X} \frac{N(x)}{D(x)},$$

assuming the minimum is attained, as it is for a finite $X$, or for a compact $X$ with continuous $N$ and $D$. A maximization is the same with $-N$.

**The parametric function.** For a real $\lambda$, let

$$F(\lambda) = \min_{x \in X} \big(N(x) - \lambda D(x)\big).$$

**Lemma (Dinkelbach).** $F(\lambda) > 0$ for $\lambda < \lambda^*$, $F(\lambda^*) = 0$, and $F(\lambda) < 0$ for $\lambda > \lambda^*$. Moreover, $x$ minimizes the ratio exactly when $x$ minimizes $N - \lambda^* D$.

*Proof.* For each $x$, $N(x) - \lambda D(x) = D(x)\big(N(x)/D(x) - \lambda\big)$, and $D(x) > 0$. If $\lambda < \lambda^*$, then $N(x)/D(x) \ge \lambda^* > \lambda$ for every $x$, so every term is positive and the attained minimum $F(\lambda)$ is positive. If $\lambda > \lambda^*$, an optimal $x^*$ gives $D(x^*)(\lambda^* - \lambda) < 0$, so $F(\lambda) < 0$. At $\lambda = \lambda^*$ every term is at least $0$, with $0$ exactly for the $x$ whose ratio is $\lambda^*$. $\square$

**Shape of $F$.** $F$ is the minimum of the affine functions $\lambda \mapsto N(x) - \lambda D(x)$, one for each $x$, so it is concave. Each has slope $-D(x) < 0$, so $F$ is strictly decreasing. For a finite $X$, $F$ is piecewise linear, with at most $|X|$ pieces.

**Consequence: a monotone decision.** The predicate "$F(\lambda) \le 0$" is false for $\lambda < \lambda^*$ and true for $\lambda \ge \lambda^*$. It is the decision question "is there an $x$ with $N(x)/D(x) \le \lambda$?", rewritten without a ratio. So the [optimization-to-decision reduction](/optimization-to-decision-reduction/) applies, and the root of $F$ can be found in three ways.

- **Bisection.** Search $\lambda$ on an interval that holds $\lambda^*$, by the sign of $F$. Each step needs one minimization of $N - \lambda D$; the error halves per step.
- **Newton's method on $F$.** If $x_k$ minimizes $N - \lambda_k D$, then $-D(x_k)$ is a supergradient of $F$ at $\lambda_k$, and the Newton step to its root is $\lambda_{k+1} = N(x_k)/D(x_k)$, the ratio of the current solution. This is [Dinkelbach's algorithm](/dinkelbach-algorithm/). It ends after finitely many steps for a finite $X$, and converges superlinearly.
- **Parametric search.** Run an algorithm for the minimization of $N - \lambda D$ at the unknown $\lambda^*$, and resolve each comparison it makes, a sign of a linear function of $\lambda$, by one evaluation of $F$. Megiddo introduced this to get strongly polynomial algorithms for ratio problems; see [parametric search](/parametric-search/).

**Linear fractional programs.** For $\min (c^\top x + \alpha)/(d^\top x + \beta)$ subject to $Ax \le b$, with $d^\top x + \beta > 0$ on a nonempty bounded feasible set, the Charnes-Cooper substitution $t = 1/(d^\top x + \beta)$ and $y = t x$ gives the [linear program](/linear-programming-problem/)

$$\min\ c^\top y + \alpha t \quad \text{subject to} \quad Ay - bt \le 0,\quad d^\top y + \beta t = 1,\quad t \ge 0.$$

A feasible $x$ maps to a feasible $(y, t)$ with the same objective, and an optimal $(y, t)$ with $t > 0$ maps back to $x = y/t$. So one linear program replaces the search.

**Convexity.** A ratio $N/D$ with $N$ convex and $N \ge 0$, $D$ concave and $D > 0$, on a convex set, is [quasiconvex](/quasiconvex-function/): its sublevel set $\{x : N(x) \le \lambda D(x)\}$ is convex for $\lambda \ge 0$. A linear-fractional function is both quasiconvex and quasiconcave. So continuous ratio problems of this kind are solved by bisection on $\lambda$ with a convex feasibility problem at each step.

**What does not reduce.** A sum of ratios $\sum_i N_i(x)/D_i(x)$ has no such parametric form and is hard in general. A maximum of ratios, $\min_x \max_i N_i(x)/D_i(x)$, still has a monotone decision "$N_i(x) - \lambda D_i(x) \le 0$ for all $i$", and Dinkelbach's method has a version for it.

## Examples

**Best average of $k$ items.** Choose $2$ of the items $(a, b) = (1, 5), (3, 4), (2, 2)$ to maximize $\sum a / \sum b$. The three choices give $4/9$, $3/7$ and $5/6$. For the maximization, $G(\lambda) = \max \sum (a_i - \lambda b_i)$ over choices of 2 items, found by taking the 2 largest values $a_i - \lambda b_i$. At $\lambda = 1/2$ the values are $-1.5, 1, 1$, so $G = 2 > 0$ and $\lambda^* > 1/2$. At $\lambda = 5/6$ they are $-19/6, -1/3, 1/3$, so $G = 0$ and $\lambda^* = 5/6$, attained by the last two items. Each evaluation of $G$ is a sort, so the ratio problem costs a sort per step.

**Largest average of a long segment.** The largest average of a contiguous segment of length at least $k$ is a ratio of the segment sum to its length. For a guess $t$, the test "is there a segment with $\sum (a_i - t) \ge 0$?" takes one pass over the prefix sums; the page on [binary search on real numbers](/binary-search-on-real-numbers/) gives a trace. The exact problem is the [maximum density segment](/maximum-density-segment/).

**Minimum mean cycle.** In a directed graph with edge costs, the cycle with the smallest average cost per edge is a ratio problem with $D(C) = |C|$. The test "is there a cycle with $\sum (c_e - \lambda) < 0$?" is a negative-cycle test. Karp's algorithm solves the [minimum mean cycle problem](/minimum-mean-cycle-problem/) directly in $O(nm)$ time.

**A linear fractional program.** Minimize $(x_1 + 2)/(x_2 + 1)$ subject to $0 \le x_1, x_2 \le 1$. The Charnes-Cooper program is to minimize $y_1 + 2t$ subject to $y_2 + t = 1$, $0 \le y_1 \le t$, $0 \le y_2 \le t$, $t \ge 0$. Its optimum is $y_1 = 0$, $y_2 = t = 1/2$, with value $1$, which maps back to $x = (0, 1)$ with ratio $2/2 = 1$.

## Where it is used

- **Combinatorial ratio problems.** Minimum ratio cycles, ratio spanning trees, the densest subgraph (edges per vertex), and ratio versions of paths and matchings: the [minimum ratio problem](/minimum-ratio-problem/).
- **Economics and operations research.** Cost per unit of output, return on investment, and the efficiency scores of data envelopment analysis, which Charnes, Cooper and Rhodes defined as linear fractional programs.
- **Engineering.** Energy efficiency, in bits per joule, in the design of wireless networks, where Dinkelbach's method is a standard tool; the signal-to-noise ratio in the design of filters and beamformers.
- **Programming contests.** "Maximize the average" or "minimize cost over length" problems, solved by a binary search on $\lambda$ with a greedy, a sort or a shortest-path test.
- **Lagrangian methods.** The parametric function is a [Lagrangian relaxation](/lagrangian-relaxation/) of the constraint "$N(x) \le \lambda D(x)$"; the same idea, a search on a price, also appears in the [Aliens trick](/aliens-trick/).

## References
