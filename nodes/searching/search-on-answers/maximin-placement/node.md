---
tag: 5WAY7B
kind: problem
slug: maximin-placement
name: Maximin placement (largest minimum distance)
aliases:
- aggressive cows problem
- largest minimum distance
- k-spacing problem
- maximum minimum spacing
area: searching/search-on-answers
level: core
summary: Place k points on a line so that the smallest gap between any two of them is as large as possible.
model: algebraic-decision-tree
complexity:
  vars: {n: the number of candidate positions}
  time: {worst: Θ(n log n)}
prereqs: [binary-search-on-answer, greedy-algorithm, exchange-argument]
see_also: [binary-search-on-answer, minimax-partition, kth-smallest-pair-distance, optimization-to-decision-reduction, sorted-matrix-selection, k-center-problem, element-distinctness, facility-location-problem]
sources:
  - url: https://www.spoj.com/problems/AGGRCOW/
    title: SPOJ, AGGRCOW, Aggressive cows
  - url: https://leetcode.com/problems/magnetic-force-between-two-balls/
    title: LeetCode 1552, Magnetic Force Between Two Balls
  - book: isbn:9783319725468
    title: Antti Laaksonen, Guide to Competitive Programming, first edition, Springer, 2017
    locator: Section 4.3.2, Finding Optimal Solutions
  - paper: doi:10.1137/0213002
    title: "Greg N. Frederickson and Donald B. Johnson, Generalized selection and ranking: sorted matrices, SIAM Journal on Computing 13(1) (1984), 14-30"
    note: selection in a sorted matrix, used for the exact search over the pairwise differences
---

Maximin placement chooses $k$ of $n$ given positions on a line so that the smallest distance between two chosen positions is as large as possible. The decision question "can $k$ positions be chosen with all gaps at least $d$?" is answered by a greedy pass in $O(n)$ time after sorting, and it is true for small $d$ and false for large $d$. So [binary search on the answer](/binary-search-on-answer/) solves the problem in $O(n \log n + n \log U)$ time for integer positions with span $U$, and a search over the pairwise differences by [sorted-matrix selection](/sorted-matrix-selection/) gives $O(n \log n)$, which is optimal. It is the standard example of a maximization solved by a "largest feasible" search.

## In plain words

A farmer has a long barn with stalls at fixed places, and some cows that fight when they are close. He wants to put each cow in its own stall so that the two closest cows are as far apart as possible.

Guessing the best distance is hard, but checking one distance is easy. Walk along the stalls from the left, put a cow in the first stall, and then put the next cow in the first stall that is far enough from the last cow. If you place all the cows this way, the distance works. A smaller distance also works, and a larger one may not. So you can search for the largest distance that works by halving the range of distances, as when you look up a word in a dictionary.

## Definition

**Input.** Real positions $x_1, \ldots, x_n$, not necessarily distinct, and an integer $k$ with $2 \le k \le n$.

**Output.** A set $S$ of $k$ indices that maximizes the smallest gap

$$\mathrm{gap}(S) = \min_{i, j \in S,\ i \ne j} |x_i - x_j|,$$

and the optimal value $\mathrm{OPT} = \max_{|S| = k} \mathrm{gap}(S)$. After sorting $x_1 \le \cdots \le x_n$, the minimum is attained by two indices that are consecutive in $S$, so $\mathrm{gap}(S)$ is the smallest of the $k - 1$ gaps between consecutive chosen positions.

**Decision version.** $\mathrm{FEASIBLE}(d)$: is there an $S$ with $|S| = k$ and $\mathrm{gap}(S) \ge d$? It is a [monotone predicate](/monotone-predicate/) that is true then false: a set that works for $d$ works for each $d' \le d$. By the [optimization-to-decision reduction](/optimization-to-decision-reduction/), $\mathrm{FEASIBLE}(d)$ holds if and only if $d \le \mathrm{OPT}$.

## Variants

- **On a circle.** The positions lie on a circle of length $C$, and the gap between the last and the first chosen position, around the circle, also counts. The greedy test must try a start; fixing the first chosen position at each of the $n$ candidates gives $O(n^2)$ per test, and a jump table over the next feasible position gives $O(n \log n)$ per test.
- **One point per interval.** Each of $k$ given intervals must receive one point, in order, and the smallest gap is maximized. The greedy test places each point as far left as allowed: at $\max(\ell_i, \text{previous} + d)$, and fails if this exceeds $r_i$.
- **Continuous placement.** If any real position in $[a, b]$ is allowed, the optimum is $(b - a)/(k - 1)$ with equal spacing; the problem is interesting only for a fixed set of positions.
- **Higher dimensions.** Choosing $k$ of $n$ points in the plane to maximize the smallest pairwise distance is the max-min dispersion problem, which is NP-hard for general distances. The line is special because the order of the positions makes the greedy test exact.
- **The dual problem.** Covering the positions with $k$ centers to minimize the largest distance to a center is the [k-center problem](/k-center-problem/); on a line it is also solved by a binary search with a greedy test.

## Examples

**Five stalls.** Stalls at $1, 2, 8, 4, 9$ and $k = 3$ cows. Sorted: $1, 2, 4, 8, 9$. The greedy test for $d = 3$ takes $1$, skips $2$, takes $4$, takes $8$: three positions, so $d = 3$ is feasible. For $d = 4$ it takes $1$, skips $2$ and $4$, takes $8$, skips $9$: two positions, infeasible. So $\mathrm{OPT} = 3$, attained by $\{1, 4, 8\}$. The span gives the bound $\mathrm{OPT} \le (9 - 1)/(k - 1) = 4$. The largest-feasible search on $[0, 4]$ tests $d = 2$ (yes), $d = 3$ (yes), $d = 4$ (no), and returns $3$.

**All positions.** For $k = n$, every position is chosen and $\mathrm{OPT}$ is the smallest gap between sorted neighbours. For $1, 2, 4, 8, 9$ it is $1$.

**Two positions.** For $k = 2$, $\mathrm{OPT} = x_n - x_1$, the span.

**A non-example of the greedy.** Starting the greedy at the median, or choosing the position closest to $\text{previous} + d$ from either side, can fail. The proof below depends on choosing the leftmost position and then always the first position that is far enough.

## Known algorithms

**The greedy test.** Sort the positions. Take $x_1$. Scan to the right, and take each position that is at least $d$ beyond the last taken one. Answer yes if at least $k$ positions are taken. This runs in $O(n)$ time.

*Proof that the greedy test is exact.* If the greedy takes $k$ or more positions, any $k$ of them in order have all consecutive gaps at least $d$, so $\mathrm{FEASIBLE}(d)$ holds. Conversely, let $y_1 < \cdots < y_k$ be chosen positions with consecutive gaps at least $d$, and let $g_1 < g_2 < \cdots$ be the positions the greedy takes. We show by induction that $g_i$ exists and $g_i \le y_i$ for $i \le k$. For $i = 1$, $g_1 = x_1 \le y_1$. If $g_i \le y_i$ and $i < k$, then $y_{i+1} \ge y_i + d \ge g_i + d$, so a position at least $d$ beyond $g_i$ exists, and the greedy takes the first one, $g_{i+1} \le y_{i+1}$. So the greedy takes at least $k$ positions. This is an [exchange argument](/exchange-argument/): the greedy choice stays ahead of every solution. $\square$

**Binary search on an integer answer.** For integer positions, $\mathrm{OPT}$ is an integer in $[0, \lfloor (x_n - x_1)/(k - 1) \rfloor]$, because the $k - 1$ consecutive gaps of a solution sum to at most $x_n - x_1$. A largest-feasible [binary search on the answer](/binary-search-on-answer/) with the greedy test costs $O(n \log n)$ for the sort and $O(n \log U)$ for the search, with $U = x_n - x_1$.

**Search over the candidates.** $\mathrm{OPT}$ is one of the differences $x_j - x_i$ with $i < j$, because it is a gap between two chosen positions. These differences are the entries above the diagonal of the matrix $M[i][j] = x_j - x_i$, whose rows increase and columns decrease when the $x_i$ are sorted. A binary search on the rank $r$ of the candidate, with the element of rank $r$ found by [sorted-matrix selection](/sorted-matrix-selection/) in $O(n)$ time (Frederickson and Johnson), makes $O(\log n^2) = O(\log n)$ probes of $O(n)$ each. The total is $O(n \log n)$, independent of the size of the numbers, and works for real positions.

**Real positions with a tolerance.** A [binary search on real numbers](/binary-search-on-real-numbers/) with the greedy test finds $\mathrm{OPT}$ within $\varepsilon$ in $O(n \log(U/\varepsilon))$ time after sorting.

## Bounds

- **Upper bound.** $O(n \log n)$ by the candidate search above. For integer positions with $U \le n^{O(1)}$, the simpler search on the integer answer also gives $O(n \log n)$.
- **Lower bound.** $\Omega(n \log n)$ in the [algebraic decision tree](/algebraic-decision-tree/) model, already for $k = n$. *Proof.* For $k = n$, $\mathrm{OPT}$ is the smallest gap between sorted neighbours, and $\mathrm{OPT} > 0$ holds exactly when the $x_i$ are distinct. So an algorithm for maximin placement decides [element distinctness](/element-distinctness/), which needs $\Omega(n \log n)$ operations in this model by Ben-Or's theorem. $\square$
- **The test alone.** On sorted input the greedy test takes $\Theta(n)$ time, and the search adds a logarithmic number of tests.

## Reductions

- **To a monotone decision.** The problem reduces to $O(\log n)$ calls of the greedy test by the candidate search, or to $O(\log U)$ calls by the integer search. This is the general [optimization-to-decision reduction](/optimization-to-decision-reduction/) for a maximization.
- **From element distinctness.** As in the lower bound, element distinctness reduces to the case $k = n$ in $O(1)$ extra time.
- **Relation to the k-th smallest pair distance.** Both problems search the same set of pairwise differences. The [k-th smallest pair distance](/kth-smallest-pair-distance/) counts pairs below a threshold; maximin placement runs a greedy below it.

## Applications

- **Spacing of facilities.** Placing $k$ shops, antennas or warehouses at allowed sites along a road so that they are as far apart as possible, to reduce interference or competition; a dispersion form of [facility location](/facility-location-problem/).
- **Sampling.** Choosing $k$ of $n$ time stamps or measurements that are as spread out as possible.
- **Teaching binary search on the answer.** The problem appears as "Aggressive cows" (SPOJ AGGRCOW) and as LeetCode 1552, as the first exercise of the maximization form of the technique.

## References
