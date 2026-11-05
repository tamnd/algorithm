---
tag: QPM3H8
kind: algorithm
slug: karger-stein
name: Karger-Stein algorithm
aliases:
- recursive contraction
- recursive contraction algorithm
- recursive contraction min-cut
area: graphs/flows-and-cuts
level: advanced
summary: Recursive random contraction improving Karger's running time to near O(n^2).
solves: [global-min-cut-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n^2 log^3 n)}
  space: {extra: Θ(n^2)}
properties: {deterministic: false, recursive: true}
prereqs: [karger-min-cut, global-min-cut-problem, graph-contraction, monte-carlo-algorithm]
see_also: [stoer-wagner, nagamochi-ibaraki, minimum-cut-count-bound, edge-connectivity, randomized-contractions, master-theorem, hao-orlin]
sources:
  - paper: doi:10.1145/234533.234534
    title: David R. Karger and Clifford Stein, A new approach to the minimum cut problem, Journal of the ACM 43(4), 601 to 640 (1996)
    locator: the whole paper (the contraction algorithm, the recursive contraction algorithm with its success probability and O(n^2 log^3 n) bound, and its weighted and parallel versions)
  - paper: doi:10.1145/331605.331608
    title: David R. Karger, Minimum cuts in near-linear time, Journal of the ACM 47(1), 46 to 76 (2000)
    locator: the whole paper (the later O(m log^3 n) method by tree packing)
---

The Karger-Stein algorithm, or recursive contraction, finds a [global minimum cut](/global-min-cut-problem/) of an undirected graph with high probability in $O(n^2 \log^3 n)$ time. It starts from [Karger's random contraction](/karger-min-cut/), and notices that a fixed minimum cut is rarely destroyed in the early contractions but often in the late ones. So it contracts only from $n$ to about $n / \sqrt{2}$ vertices, where the cut still survives with probability at least $\frac12$, and then recurses twice, independently, on the smaller graph. One run takes $O(n^2 \log n)$ time and succeeds with probability $\Omega(1 / \log n)$, and $O(\log^2 n)$ runs push the error below $1/n$. It is a [Monte Carlo algorithm](/monte-carlo-algorithm/): the answer is always a real cut, never below the minimum.

## In plain words

Karger's method merges two random neighbors again and again until two groups are left, and hopes it never merged across the cheapest split. Early merges are safe, because there are many links and few of them belong to the cheapest split. The last few merges are risky.

Karger-Stein spends its effort where the risk is. It does the safe merges once, until about seven tenths of the points are left. Then it makes two independent copies and continues each one in the same way, so the risky end is tried many times while the cheap start is shared. When only a handful of points are left, it checks every split directly. The best split found by any branch is the answer.

## The problem

The input is an undirected graph $G = (V, E)$ with $n \ge 2$ vertices and weights $w(e) \ge 0$, integer or real; parallel edges add up and self-loops are ignored. The graph may be disconnected. The output is a set $S$ with $\emptyset \ne S \subsetneq V$ that minimizes the weight $w(S, V \setminus S)$ of the edges that leave $S$. There is no source or sink, and edges have no direction. Write $\lambda$ for the minimum.

## The algorithm

A contraction picks an edge $\{u, v\}$ with probability $w(u, v) / W$, where $W$ is the total weight of the current graph, and merges $v$ into $u$: the weights to each other vertex add up and the edge between them disappears. Each vertex of a contracted graph stands for a group of original vertices.

```pseudo id=main
KARGER-STEIN(G, R)
L1  best ← ∞
L2  repeat R times
L3      (k, S) ← RECURSIVE-CONTRACT(G); if k < best then best ← k, bestS ← S
L4  return best, bestS

RECURSIVE-CONTRACT(G)
L5  k ← the number of vertices of G
L6  if k ≤ 6 then return a minimum cut of G found by trying all 2^(k−1) − 1 cuts
L7  t ← ⌈1 + k / √2⌉
L8  for i ← 1, 2 do G_i ← CONTRACT(G, t); (k_i, S_i) ← RECURSIVE-CONTRACT(G_i)
L9  return the pair (k_i, S_i) with the smaller k_i

CONTRACT(G, t)
L10 while G has more than t vertices do
L11     pick an edge {u, v} with probability w(u, v) / W and merge v into u
L12 return G
```

The two calls of line L8 contract the same graph independently. If line L11 finds $W = 0$ while more than $t$ vertices remain, the graph is disconnected, and the group of any vertex is a cut of weight 0, which the call returns at once. With an adjacency matrix, line L11 picks $u$ with probability proportional to its weighted degree and then $v$ with probability proportional to $w(u, v)$, which gives the edge $\{u, v\}$ probability $w(u, v) / W$; both choices and the merge take $O(k)$.

## Example

The graph has the 8 vertices $a, b, c, d, e, f, g, h$. The sets $\{a, b, c, g\}$ and $\{d, e, f, h\}$ are complete graphs with edges of weight 2, and the edges $c d$ and $b e$ have weight 1. So $W = 26$, every vertex has weighted degree at least 6, and the unique minimum cut is $\{a, b, c, g\}$ with $\lambda = 2$.

One run: line L7 gives $t = \lceil 1 + 8/\sqrt2 \rceil = 7$, so each of the two branches makes one contraction. That contraction avoids $c d$ and $b e$ with probability $24/26 = 12/13$. Each branch then has 7 vertices, sets $t = \lceil 1 + 7/\sqrt2 \rceil = 6$, and makes two branches with one more contraction each, after which line L6 solves 6 vertices exactly. The tree of calls has 4 leaves, and the run fails only if the cut is lost on every root-to-leaf path. In 50,000 runs of the implementation, about 99.4% returned $\lambda = 2$. Plain contraction from 8 vertices down to 2 keeps the cut in only about 44% of the trials.

Edge cases. With $n \le 6$ the answer is exact. A disconnected graph returns 0, and an edge of weight 0 is never contracted, so it acts as no edge.

## Correctness

Every returned pair $(k, S)$ is an actual cut and its exact weight, since a vertex of a contracted graph is a group of original vertices and the edges between groups keep their weights. So the answer is never below $\lambda$. Contraction never lowers the minimum cut, because each cut of a contracted graph is a cut of $G$.

For success, fix a minimum cut $C$. While the current graph has $k$ vertices and $C$ survives, every vertex has weighted degree at least $\lambda$, so $W \ge k \lambda / 2$, and the next contraction hits $C$ with probability at most $2/k$. Contracting from $k$ to $t$ vertices keeps $C$ with probability at least $t(t-1) / (k(k-1))$, which is at least $\frac12$ for $t = \lceil 1 + k/\sqrt2 \rceil$. If a call of depth $D$ succeeds with probability at least $p$, each branch of its parent succeeds with probability at least $p/2$, and the two branches are independent; this gives the bound $p_D \ge 2 / (D + 2)$. The proof file below gives the details.

## Complexity

The model is the [word RAM](/word-ram/) with a source of random numbers; weights fit in a word.

- **One call.** Contracting from $k$ to $t$ vertices costs $O(k^2)$ with an adjacency matrix, and copying the matrix for each branch is also $O(k^2)$. So $T(k) = 2\,T(\lceil 1 + k/\sqrt2 \rceil) + O(k^2)$. At depth $j$ there are $2^j$ calls on graphs of about $k / 2^{j/2}$ vertices, so each level costs $O(n^2)$, and there are $O(\log n)$ levels: $T(n) = O(n^2 \log n)$.
- **Success of one run.** At least $2/(D + 2)$ with depth $D = O(\log n)$, so $\Omega(1/\log n)$.
- **Many runs.** $R$ runs fail with probability at most $(1 - 2/(D+2))^R \le e^{-2R/(D+2)}$. With $R = \Theta(\log^2 n)$ this is $n^{-c}$ for a constant $c$ of choice, for a total of $O(n^2 \log^3 n)$. The implementation uses $R = \lceil \log_2 n \rceil^2 + 1$ by default.
- **Space.** Only the calls on one root-to-leaf path are alive at a time, when the two branches run one after the other as in the implementation. Their matrices have about $n^2, n^2/2, n^2/4, \ldots$ entries, which sum to $O(n^2)$.

## Properties

- **Monte Carlo, one-sided error.** The answer is an upper bound on $\lambda$ that is exact with high probability.
- **Real weights.** Only additions, comparisons and weighted random choices are used.
- **Finds all minimum cuts.** Each fixed minimum cut is found by one run with probability $\Omega(1/\log n)$, so $O(\log^2 n)$ runs, with a union bound over the at most $\binom{n}{2}$ minimum cuts, list every minimum cut with high probability.
- **Undirected only.** The degree bound $W \ge k\lambda/2$ needs undirected edges.

## Variants and improvements

- **Sparse graphs.** Karger's later algorithm uses tree packings instead of contraction and runs in $O(m \log^3 n)$ time with high probability.
- **Approximate cuts.** The same recursion finds all cuts of weight at most $\alpha \lambda$, with the contraction stopped earlier.
- **Parallel.** The two branches are independent, so they run in parallel, and the contraction to $t$ vertices can itself be done in parallel; Karger and Stein give an RNC version.
- **Deterministic alternatives.** [Stoer-Wagner](/stoer-wagner/) and [Nagamochi-Ibaraki](/nagamochi-ibaraki/) take $O(nm + n^2 \log n)$ with no error.

## When to use it

Use it for global minimum cuts of dense undirected graphs when a short randomized method with a clear guarantee is wanted, or when all minimum cuts are needed. On sparse graphs, Stoer-Wagner or near-linear methods are faster, and they are deterministic or nearly so. For a minimum $s$-$t$ cut, use a [maximum flow](/max-flow-problem/), since contraction may merge $s$ and $t$.

## Pitfalls

- **Contracting too far before branching.** The split size $\lceil 1 + k/\sqrt2 \rceil$ is what keeps the survival chance at $\frac12$; contracting to $k/2$ gives only about $\frac14$, and the success bound falls to a power of $n$.
- **Sharing randomness between branches.** The two calls of line L8 must contract independently; reusing one contracted graph for both doubles the cost for no gain.
- **Choosing a random vertex pair.** The edge must be chosen with probability proportional to its weight, not uniformly among adjacent pairs.
- **Too few runs.** One run succeeds with probability about $1/\log n$, not with high probability.
- **Disconnected input.** If no edge is left to contract, the graph is disconnected and the answer is 0; code that assumes an edge always exists loops or crashes.

## Implementations

## History

Karger gave the random contraction algorithm in 1993. Karger and Stein presented recursive contraction at STOC 1993, and the full version appeared in the Journal of the ACM in 1996. Karger later found the $O(m \log^3 n)$ algorithm by tree packing, published in 2000.

## References
