---
tag: 8DMG35
kind: technique
slug: parametric-search
name: Parametric search
aliases:
- Cole's parametric search
- Megiddo parametric search
- Megiddo's parametric search
- parametric search
area: searching/search-on-answers
level: advanced
summary: Solve an optimization problem by simulating a parallel decision algorithm on the unknown optimum and resolving comparisons with a decision procedure.
prereqs: [optimization-to-decision-reduction, binary-search-on-real-numbers, pram-model, sorting-network]
see_also: [fractional-programming, minimum-ratio-problem, dinkelbach-algorithm, sorted-matrix-selection, kth-smallest-pair-distance, aks-sorting-network, cole-merge-sort, megiddo-fixed-dimension-lp]
sources:
  - paper: doi:10.1145/2157.322410
    title: "Nimrod Megiddo, Applying parallel computation algorithms in the design of serial algorithms, Journal of the ACM 30(4) (1983), 852-865"
  - paper: doi:10.1287/moor.4.4.414
    title: "Nimrod Megiddo, Combinatorial optimization with rational objective functions, Mathematics of Operations Research 4(4) (1979), 414-424"
    note: the first form of the method, for ratio objectives
  - paper: doi:10.1145/7531.7537
    title: "Richard Cole, Slowing down sorting networks to obtain faster sorting algorithms, Journal of the ACM 34(1) (1987), 200-208"
  - paper: doi:10.1145/299917.299918
    title: "Pankaj K. Agarwal and Micha Sharir, Efficient algorithms for geometric optimization, ACM Computing Surveys 30(4) (1998), 412-458"
    note: the section on parametric search and its applications in geometry
---

Parametric search finds the exact real value $\lambda^*$ at which a monotone decision changes its answer, without a tolerance. It runs an algorithm $A$ for the decision at the unknown value $\lambda^*$: each time $A$ compares two quantities that depend on $\lambda$, the sign of the comparison at $\lambda^*$ is found by calling the decision procedure at the root of the comparison. Megiddo introduced it in 1979 for ratio objectives and in 1983 showed that running a *parallel* algorithm for $A$ cuts the number of decision calls to a logarithmic number per parallel step, because the roots of one step can be resolved together by a [binary search](/binary-search/) over them. With Cole's improvement for sorting, the method gives near-linear algorithms for many problems in geometry and combinatorial optimization, where a [binary search on real numbers](/binary-search-on-real-numbers/) would only give an approximation.

## In plain words

Suppose you can check a guess quickly: "is the answer below this value, equal to it or above it?". A binary search on guesses gets close to the answer but never exactly to it, because the answer could be any real number.

Parametric search finds it exactly. Take the checking program itself and run it on the answer, which you do not know. The program only compares numbers. Each comparison is a question such as "is $3 - 2x$ below $1 + x$?", and its answer flips at one value of $x$. So ask your checker about that one value: this tells you which side the answer is on, and hence how the comparison comes out. When the program ends, the answer is one of the values you asked about.

## When it applies

- **A three-way monotone decision.** There is an unknown real $\lambda^*$ and a procedure $C(\lambda)$ that tells, for any given $\lambda$, whether $\lambda < \lambda^*$, $\lambda = \lambda^*$ or $\lambda > \lambda^*$, in time $T_C$. In an optimization, $\lambda^*$ is the optimum and $C$ is a decision procedure for "is $\mathrm{OPT} \le \lambda$?" that also detects equality, as in the [optimization-to-decision reduction](/optimization-to-decision-reduction/).
- **A decision algorithm that only compares polynomials in $\lambda$.** There is an algorithm $A$ that, given $\lambda$, answers the same three-way question, and whose control flow depends only on the signs of polynomials of bounded degree $d$ in $\lambda$, built from the input. Often $A$ is $C$ itself. In most uses the polynomials are linear: comparisons of weights $c_e - \lambda t_e$, or of positions of lines at time $\lambda$.
- **The critical-value property.** This follows from the two items. *Claim.* If no comparison of $A$ at $\lambda^*$ is $0$, the signs of all comparisons that $A$ makes at $\lambda^*$ are constant on an open interval $I$ around $\lambda^*$, so $A$ follows the same path and gives the same answer for every $\lambda \in I$. But $A(\lambda^*)$ says "equal" and $A(\lambda)$ says "less" or "greater" for $\lambda \ne \lambda^*$. So some comparison of $A$ at $\lambda^*$ is $0$, and $\lambda^*$ is a root of a polynomial that $A$ evaluates. $\square$ This is why the simulation finds $\lambda^*$ exactly.

## The template

The generic simulation keeps an interval $(\alpha, \beta)$ that holds $\lambda^*$, and the value $\lambda^*$ once found.

```pseudo id=main
PARAMETRIC-SEARCH(A, C)                    ▷ run A at the unknown λ*
L1  (α, β) ← (−∞, +∞)
L2  run A step by step; when A asks for the sign of p(λ*):
L3      for each real root r of p in (α, β), in sorted order:
L4          s ← C(r)                         ▷ λ* < r, λ* = r or λ* > r
L5          if s is "equal" then return r
L6          if s is "less" then β ← r else α ← r
L7      give A the sign of p on (α, β)        ▷ constant: p has no root in (α, β)
L8  return α                                ▷ not reached when the claim holds
```

**Correctness.** The invariant is $\alpha < \lambda^* < \beta$, and every answer given to $A$ is the true sign of the comparison at $\lambda^*$. Line L6 keeps the invariant by the meaning of $C$. After the roots in $(\alpha, \beta)$ are processed, $p$ has no root in $(\alpha, \beta)$, so its sign there is constant and equal to its sign at $\lambda^*$. So the simulation follows the true path of $A$ at $\lambda^*$. By the critical-value claim, some comparison has $\lambda^*$ as a root; it lies in $(\alpha, \beta)$ at that moment, and line L5 returns it.

**Cost of the serial simulation.** If $A$ makes $K$ comparisons with polynomials of degree at most $d$, the simulation calls $C$ at most $dK$ times, so it takes $O(T_A + d K T_C)$ time. With $K = \Theta(T_A)$ this is $O(T_A T_C)$, often worse than a binary search to a tolerance.

**Megiddo's parallel simulation.** Let $A$ be a parallel algorithm with $P$ processors and $S$ steps, as in the [PRAM model](/pram-model/), where each step makes up to $P$ independent comparisons. Collect the roots of all $P$ comparisons of one step, at most $dP$ numbers. Find their median in $O(P)$ time, call $C$ on it, and discard the half of the roots on the wrong side; after $O(\log P)$ calls the interval $(\alpha, \beta)$ contains no root of the step, and all $P$ comparisons are resolved. The total time is

$$O\big(P S + S\,T_C \log P\big),$$

the time to simulate $A$ serially plus $O(S \log P)$ calls of $C$. A parallel algorithm with $P = O(n)$ processors and $S = O(\log n)$ steps gives $O(n \log n + T_C \log^2 n)$.

**Cole's improvement.** When $A$ is a sorting algorithm, the comparisons of later steps do not all depend on all comparisons of earlier steps. Cole resolves the comparisons of a sorting network with weights, and resolves only the median-weight ones at each round. For a network of depth $O(\log n)$, such as the [AKS network](/aks-sorting-network/), this gives $O(n \log n + T_C \log n)$: a single logarithmic factor of decision calls.

## Classic examples

### A ratio problem by simulated selection

Choose $2$ of the items $A = (8, 1)$, $B = (4, 2)$, $C = (9, 4)$, $D = (2, 2)$, $E = (9, 5)$, given as (cost, time), to minimize total cost over total time. By [fractional programming](/fractional-programming/), $\lambda^*$ is the root of $F(\lambda)$, the sum of the two smallest values $w_i(\lambda) = c_i - \lambda t_i$, and $C(\lambda)$ is the sign of $F(\lambda)$. Simulate the algorithm "find the smallest, then the second smallest" at $\lambda^*$:

| comparison | difference | root | $C$ at the root | sign at $\lambda^*$ | interval |
|---|---|---|---|---|---|
| A vs B | $4 + \lambda$ | $-4$ | $F = 22 > 0$: $\lambda^* > -4$ | B smaller | $(-4, \infty)$ |
| B vs C | $2\lambda - 5$ | $2.5$ | $F = -6.5 < 0$: $\lambda^* < 2.5$ | B smaller | $(-4, 2.5)$ |
| B vs D | $2$ | none | | D smaller | $(-4, 2.5)$ |
| D vs E | $3\lambda - 7$ | $7/3$ | $F = -16/3 < 0$: $\lambda^* < 7/3$ | D smaller | $(-4, 7/3)$ |
| B vs E | $3\lambda - 5$ | $5/3$ | $F = -2/3 < 0$: $\lambda^* < 5/3$ | B smaller | $(-4, 5/3)$ |
| $F$ vs 0 | $6 - 4\lambda$ | $1.5$ | $F = 0$ | equal | found |

The two smallest at $\lambda^*$ are $D$ and $B$, so $F(\lambda^*) = (2 - 2\lambda^*) + (4 - 2\lambda^*)$, and the final sign test has the root $1.5$, where $C$ answers "equal". So $\lambda^* = 3/2$, exactly, after 5 calls of $C$. A bisection would give only an interval.

### The minimum ratio spanning tree

The decision at $\lambda$ is a minimum spanning tree with weights $c_e - \lambda t_e$. Kruskal's algorithm compares weights, which are linear in $\lambda$, only in its sort. Simulating a parallel sort of the $m$ weights at $\lambda^*$, with the minimum spanning tree as $C$, finds the optimal ratio exactly with $O(\log m)$ or $O(\log^2 m)$ spanning tree computations, depending on the sort. Megiddo's 1979 paper gave the first strongly polynomial algorithms for this problem and for the minimum ratio cycle in this way; see the [minimum ratio problem](/minimum-ratio-problem/).

### Geometric optimization

Many geometric problems have a monotone decision: "can $k$ disks of radius $r$ cover the points?", "is the $k$-th smallest distance at most $r$?", "is the slope of rank $k$ at most $s$?". The comparisons of a decision algorithm are signs of low-degree polynomials in the parameter, and parametric search turns a near-linear decision into a near-linear optimization. Slope selection, distance selection and many facility location problems were first solved this way; Agarwal and Sharir survey these uses.

## Variations

- **Search over an explicit set of candidates.** When $\lambda^*$ is known to be one of a structured set of values, such as the entries of a sorted matrix, a direct search by [sorted-matrix selection](/sorted-matrix-selection/) can replace the simulation; Frederickson and Johnson's method does this for many path and partition problems.
- **Prune and search.** Megiddo's linear programming in fixed dimension resolves many comparisons by one median test and discards a constant fraction of the constraints per round; see [prune and search](/prune-and-search/) and [Megiddo's algorithm](/megiddo-fixed-dimension-lp/).
- **Randomized versions.** Sample a few roots of the pending comparisons, test the sample with $C$, and narrow the interval so that only few roots remain; this avoids the AKS network and its huge constant, and gives simple algorithms with the same expected bounds for many problems.
- **Newton's method.** For ratio problems, [Dinkelbach's algorithm](/dinkelbach-algorithm/) uses the solution of the decision, not just its sign, and often needs fewer calls; parametric search gives the cleaner worst-case bounds.
- **Several parameters.** The method extends to a parameter in $\mathbb{R}^d$, where each comparison is a hyperplane and the location of $\lambda^*$ is found by cutting the arrangement; the cost grows with $d$.

## Pitfalls

- **A decision that is not three-way.** The simulation needs to recognize $\lambda^* = r$. A two-way test "is $\lambda^* \le r$?" leaves an interval $(\alpha, \beta]$ at the end, and $\lambda^*$ must then be identified as the critical value $\beta$, which needs the critical-value claim to be checked for the given $A$.
- **Exact arithmetic.** The roots are algebraic numbers, and $C$ is called at them. With linear comparisons and rational input they are rational, so exact rational arithmetic works; with higher degrees, computing with roots exactly is costly.
- **The constant of AKS.** Cole's bound uses a sorting network of depth $O(\log n)$, and the known networks of this depth have enormous constants. Implementations use a parallel quicksort, a randomized variant, or Batcher's network with an extra logarithmic factor.
- **The serial version is slow.** Without parallelism, each comparison of $A$ costs a call of $C$, so the simulation costs about $T_A \cdot T_C$, the square of the decision time. Most of the value of the method comes from the parallel simulation.
- **Comparisons that do not depend on $\lambda$ only through their sign.** If $A$ uses $\lambda$ in a floor, a hash or an index computation, the critical-value claim fails; the simulation needs an algorithm whose branches are signs of polynomials.

## Exercises

1. Prove the critical-value claim for a decision algorithm whose comparisons are signs of polynomials of degree at most $d$, and show that the serial simulation calls $C$ at most $d$ times per comparison.
2. Simulate an odd-even merge sort of the 5 weights of the example at $\lambda^*$, resolving each round of comparisons by a median search over its roots. How many calls of $C$ does it make?
3. For the [k-th smallest pair distance](/kth-smallest-pair-distance/), the decision "are at least $k$ distances at most $d$?" has a two-pointer algorithm. Explain why its comparisons are linear in $d$, and why the exact search over the sorted matrix is simpler than a parametric search here.
4. Show that Megiddo's parallel simulation with $P$ processors and $S$ steps makes at most $S \lceil \lg(dP + 1) \rceil$ calls of $C$.

## References
