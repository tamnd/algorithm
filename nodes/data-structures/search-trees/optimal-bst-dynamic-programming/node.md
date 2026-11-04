---
tag: 5HF5N0
kind: algorithm
slug: optimal-bst-dynamic-programming
name: Optimal binary search tree dynamic programming
aliases:
- Knuth optimal BST algorithm
- OPTIMAL-BST
area: data-structures/search-trees
level: core
summary: O(n^3) interval dynamic program over key ranges that computes the minimum expected search cost tree.
solves: [optimal-binary-search-tree]
model: real-ram
complexity:
  vars: {n: the number of keys}
  time: {worst: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, comparison: false, recursive: false, in_place: false}
prereqs: [optimal-binary-search-tree, expected-search-cost-bst, interval-dp]
see_also: [knuth-optimization, optimal-substructure, matrix-chain-multiplication, hu-tucker-algorithm, garsia-wachs-algorithm, huffman-coding, static-optimality-theorem, binary-search-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.5 (Optimal binary search trees), OPTIMAL-BST and the example with five keys
  - paper: doi:10.1007/BF00264289
    title: Donald E. Knuth, Optimum binary search trees, Acta Informatica 1(1), 1971
    locator: pages 14 to 25
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2 (Binary tree searching), optimum binary search trees and Algorithm K
---

The optimal BST dynamic program computes a [binary search tree](/binary-search-tree/) of minimum [expected search cost](/expected-search-cost-bst/) for $n$ sorted keys with known search probabilities $p_1, \ldots, p_n$ and gap probabilities $q_0, \ldots, q_n$. It is an [interval DP](/interval-dp/): the best tree on the keys $k_i, \ldots, k_j$ has some root $k_r$, and its two subtrees are best trees on smaller intervals. Trying every root for every interval takes $\Theta(n^3)$ time and $\Theta(n^2)$ space; this is OPTIMAL-BST of CLRS, Section 14.5. Knuth (1971) showed that the optimal roots are monotone, which cuts the time to $\Theta(n^2)$ ([Knuth optimization](/knuth-optimization/)).

## In plain words

You want the best search tree for keys whose search frequencies you know. Some key must be the root. Whichever key it is, the keys to its left form the left subtree and the keys to its right form the right subtree, and each of these should itself be as good as possible.

So first solve all the small problems: the best tree for each single key, then for each run of two neighbouring keys, then three, and so on. For each run, try every key of the run as the root, look up the best costs of the two sides from the table, and keep the cheapest choice. When the run is the whole list of keys, you have the answer.

## The problem

The input is $n \ge 0$, key weights $p_1, \ldots, p_n \ge 0$ and gap weights $q_0, \ldots, q_n \ge 0$ for the sorted keys $k_1 < \cdots < k_n$ and the gaps $d_0, \ldots, d_n$ between them. For a BST $T$ on the keys, with each gap $d_j$ as a leaf, the cost is
$$\mathrm{cost}(T) = \sum_{i=1}^{n} p_i\,(\mathrm{depth}_T(k_i) + 1) + \sum_{j=0}^{n} q_j\,(\mathrm{depth}_T(d_j) + 1).$$
The output is the minimum cost and a tree that reaches it, given as a table of roots. The weights need not sum to 1; frequencies work the same way. This is the [optimal binary search tree](/optimal-binary-search-tree/) problem.

## The algorithm

For $1 \le i \le n + 1$ and $i - 1 \le j \le n$, let $e[i, j]$ be the least cost of a subtree on the keys $k_i, \ldots, k_j$ (with the gaps $d_{i-1}, \ldots, d_j$), and let $w[i, j] = \sum_{l=i}^{j} p_l + \sum_{l=i-1}^{j} q_l$ be its weight. The empty interval $j = i - 1$ holds only the gap $d_{i-1}$. If the root is $k_r$, every node of the subtree goes one level down when it hangs below a parent, so
$$e[i, j] = \min_{i \le r \le j} \left( e[i, r - 1] + e[r + 1, j] + w[i, j] \right), \qquad e[i, i - 1] = q_{i-1}.$$

```pseudo id=main
OPTIMAL-BST(p, q, n)
L1  for i ← 1 to n + 1 do e[i, i−1] ← q[i−1]; w[i, i−1] ← q[i−1]
L2  for ℓ ← 1 to n do                              ▷ the length of the interval
L3      for i ← 1 to n − ℓ + 1 do
L4          j ← i + ℓ − 1; e[i, j] ← ∞; w[i, j] ← w[i, j−1] + p[j] + q[j]
L5          for r ← i to j do                      ▷ try each root
L6              t ← e[i, r−1] + e[r+1, j] + w[i, j]
L7              if t < e[i, j] then e[i, j] ← t; root[i, j] ← r
L8  return e, root
```

Line L1 fills in the empty intervals. The loops of lines L2 and L3 visit the intervals by increasing length, so the two subintervals used in line L6 are already done. Line L4 gets the weight from the weight of a shorter interval in $O(1)$ time. Lines L5 to L7 try each root and keep the best. The tree is read off the table: the root is $k_{root[1, n]}$, and the subtrees of $k_r$ on $[i, j]$ are given by $root[i, r - 1]$ and $root[r + 1, j]$.

## Example

The CLRS example has $n = 5$, $p = (0.15, 0.10, 0.05, 0.10, 0.20)$ and $q = (0.05, 0.10, 0.05, 0.05, 0.05, 0.10)$.

Intervals of length 1. For $[1, 1]$: $w = q_0 + p_1 + q_1 = 0.30$, and the only root $k_1$ gives $e = q_0 + q_1 + 0.30 = 0.45$. In the same way $e[2,2] = 0.40$, $e[3,3] = 0.25$, $e[4,4] = 0.30$, $e[5,5] = 0.50$.

Interval $[1, 2]$, with $w[1, 2] = 0.30 + 0.10 + 0.05 = 0.45$:

| root $r$ | $e[1, r-1]$ | $e[r+1, 2]$ | $t$ |
|---|---|---|---|
| 1 | $e[1,0] = 0.05$ | $e[2,2] = 0.40$ | $0.90$ |
| 2 | $e[1,1] = 0.45$ | $e[3,2] = 0.05$ | $0.95$ |

So $e[1, 2] = 0.90$ with root $k_1$. Going on to the full interval:

| $\ell$ | intervals and $e[i, j]$ (root) |
|---|---|
| 1 | $[1,1]$ 0.45 ($k_1$); $[2,2]$ 0.40 ($k_2$); $[3,3]$ 0.25 ($k_3$); $[4,4]$ 0.30 ($k_4$); $[5,5]$ 0.50 ($k_5$) |
| 2 | $[1,2]$ 0.90 ($k_1$); $[2,3]$ 0.70 ($k_2$); $[3,4]$ 0.60 ($k_4$); $[4,5]$ 0.90 ($k_5$) |
| 3 | $[1,3]$ 1.25 ($k_2$); $[2,4]$ 1.20 ($k_2$); $[3,5]$ 1.30 ($k_5$) |
| 4 | $[1,4]$ 1.75 ($k_2$); $[2,5]$ 2.00 ($k_4$) |
| 5 | $[1,5]$ 2.75 ($k_2$) |

The minimum cost is $e[1, 5] = 2.75$. The root is $k_2$; its left subtree is $root[1, 1] = k_1$, its right subtree has root $root[3, 5] = k_5$, then $root[3, 4] = k_4$ is the left child of $k_5$, and $k_3$ is the left child of $k_4$. A balanced tree with root $k_3$ costs $3.00$.

## Correctness

Each subtree of a BST on $k_i, \ldots, k_j$ holds the keys of a subinterval, and the recursion is exact: the cost of a tree with root $k_r$ is $\mathrm{cost}(L) + \mathrm{cost}(R) + w[i, j]$, because the root costs $p_r$ and each node of $L$ and $R$, real or dummy, is one level deeper than in its own subtree. So a tree is optimal only if both subtrees are optimal for their intervals (else swap in a better one), and the minimum over $r$ of the best costs is the best cost. Induction on the length $\ell$ shows that line L7 sets $e[i, j]$ to the best cost and $root[i, j]$ to the root of a best tree. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Line L6 runs once for each triple $i \le r \le j$, that is
$$\sum_{\ell=1}^{n} (n - \ell + 1)\,\ell = \frac{n(n+1)(n+2)}{6}$$
times, and the rest of the work is $O(n^2)$. So the time is $\Theta(n^3)$ for every input. For $n = 5$ the count is 35. The tables $e$, $w$ and $root$ take $\Theta(n^2)$ space. The cost model is the [real RAM](/real-ram/) or the [word RAM](/word-ram/) with $O(1)$-time additions and comparisons of weights; the keys themselves are never compared.

With Knuth's speed-up, the loop of line L5 runs only from $root[i, j-1]$ to $root[i+1, j]$, and the sum of these ranges over each diagonal telescopes to $O(n)$, so the time is $\Theta(n^2)$.

## Properties

- **Exact.** It returns a tree of least cost, not an approximation.
- **Offline and static.** It needs all weights in advance, and the tree does not change later.
- **Independent of the key values.** Only the weights and the order matter.
- **Ties.** With the strict test of line L7, ties go to the smallest root; other rules give other trees of the same cost.
- **Zero weights.** Zero weights are allowed; with all $p_i = 0$ it solves the optimal alphabetic tree problem, but more slowly than Hu-Tucker.

## Variants and improvements

- **Knuth's speed-up.** Knuth (1971) proved $root[i, j-1] \le root[i, j] \le root[i+1, j]$, which gives $O(n^2)$ time. It is Algorithm K in Volume 3, Section 6.2.2, and the first example of [Knuth optimization](/knuth-optimization/). The Python file includes this version.
- **Approximate trees.** Mehlhorn's rule picks the root that splits the weight most evenly and builds, much faster than the DP, a tree whose cost is within an additive $O(1)$ of the entropy bound; see [expected search cost](/expected-search-cost-bst/).
- **Only gaps.** With $p = 0$, the [Hu-Tucker](/hu-tucker-algorithm/) and [Garsia-Wachs](/garsia-wachs-algorithm/) algorithms find the optimal alphabetic tree in $O(n \log n)$ time.
- **Height limit.** If the tree must have height at most $L$, add $L$ as a third index; the DP then takes $O(n^3 L)$ time.
- **Unknown weights.** A [splay tree](/splay-tree/) needs no weights and is within a constant factor of the optimal static tree on each long access sequence, by the [static optimality theorem](/static-optimality-theorem/).
- **The same scheme.** [Matrix chain multiplication](/matrix-chain-multiplication/) has the same interval structure, with a split point in the place of the root.

## When to use it

Use it to build a static lookup table, such as a keyword table, a symbol table of a fixed program, or a decision procedure over sorted thresholds, when the access frequencies are known and stable and $n$ is at most a few thousand. For larger $n$, use Knuth's $O(n^2)$ version or an approximate method. If the frequencies are not known or change, use a balanced tree or a splay tree. If all weights are equal, a balanced tree is already optimal up to the last level, and the DP is not needed.

## Pitfalls

- **Forgetting the gaps.** With only the $p_i$ and no $q_j$, the empty intervals have cost 0, and the program gives the optimal tree for successful searches only. That tree can be far from optimal if misses are common.
- **Off-by-one in the empty intervals.** The table $e$ must have the entries $e[i, i - 1]$ for $i = 1, \ldots, n + 1$, including $e[n + 1, n] = q_n$. A table indexed only from 1 to $n$ in both coordinates has no room for them.
- **Wrong loop order.** Filling the table row by row for increasing $i$ uses $e[r + 1, j]$ before it is computed. Loop by interval length, or by decreasing $i$ and increasing $j$.
- **Recomputing weights.** Summing $w[i, j]$ from scratch in line L4 adds $\Theta(n)$ per interval; this keeps $\Theta(n^3)$ but costs more, and it breaks the $O(n^2)$ bound of the Knuth version. Use $w[i, j - 1] + p_j + q_j$, or prefix sums.
- **Float ties.** With floating-point weights, two roots of equal true cost can compare as different, so two correct programs return different trees. Compare costs, not trees, in tests, or use integer or rational weights.
- **Recursion without memoization.** The plain recursion on $e$ takes exponential time; each interval must be solved once.

## Implementations

The Python function follows the main block with 1-based tables, and works for integer, rational and float weights. The file also has the Knuth version and helpers that rebuild the tree from the root table and recompute its cost.

## History

Knuth (1971) gave the dynamic program together with the monotonicity of the roots, which made it run in $O(n^2)$ time from the start. CLRS presents the cubic version as an example of dynamic programming, and notes Knuth's improvement as an exercise.

## References
