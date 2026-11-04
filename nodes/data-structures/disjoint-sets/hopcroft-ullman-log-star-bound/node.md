---
tag: K0VR0A
kind: theorem
slug: hopcroft-ullman-log-star-bound
name: Hopcroft-Ullman bound
aliases:
- O(m log* n) union-find bound
area: data-structures/disjoint-sets
level: advanced
summary: Early bound of O(m log* n) total time for union-find with path compression and linking by size.
prereqs: [disjoint-set-forest, union-by-rank, path-compression, iterated-logarithm]
see_also: [union-find-amortized-bound, iterated-logarithm, inverse-ackermann-function, union-by-size, union-find-lower-bound, accounting-method]
sources:
  - paper: doi:10.1137/0202024
    title: "John E. Hopcroft and Jeffrey D. Ullman, Set merging algorithms, SIAM Journal on Computing 2(4) (1973), 294-303"
    locator: the analysis of the tree algorithm with path compression and merging by size, and its O(n log* n) bound
  - paper: doi:10.1145/321879.321884
    title: "Robert Endre Tarjan, Efficiency of a Good But Not Linear Set Union Algorithm, Journal of the ACM 22(2) (1975), 215-225"
    locator: the introduction, on the earlier bounds, and the main theorem, which improves the bound to O(m alpha(m, n))
  - paper: doi:10.1145/62.2160
    title: "Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2) (1984), 245-281"
    locator: the history of the bounds for linking with compaction
---

The Hopcroft-Ullman bound states that a [disjoint-set forest](/disjoint-set-forest/) with [union by size](/union-by-size/) or [by rank](/union-by-rank/) and [path compression](/path-compression/) runs $m$ operations on $n$ elements in $O(m \lg^* n)$ time, where $\lg^*$ is the [iterated logarithm](/iterated-logarithm/). Hopcroft and Ullman proved it in 1973. Two years later Tarjan proved the sharper and tight bound $O(m\,\alpha(m, n))$ of [Tarjan's union-find bound](/union-find-amortized-bound/), but the $\lg^*$ proof stays the shortest way to see that the forest is almost linear. Since $\lg^* n \le 5$ for all $n \le 2^{65536}$, the bound already says that each operation costs a small constant in practice.

## Statement

Let a disjoint-set forest use union by rank and full path compression, and start empty.

**Theorem.** A sequence of $m$ operations MAKE-SET, UNION and FIND, of which $n$ are MAKE-SET, takes $O(m \lg^* n)$ time.

Here $\lg^* n$ is the number of times that $\lg$ must be applied to $n$ to get a value at most 1. The model is the [word RAM](/word-ram/) or the [pointer machine](/pointer-machine/), and the bound is amortized: one FIND can cost $\Theta(\log n)$. The same bound holds for union by size, the rule of Hopcroft and Ullman; the proof below covers both.

| $n$ | 2 | 4 | 16 | 65536 | $2^{65536}$ |
|---|---|---|---|---|---|
| $\lg^* n$ | 1 | 2 | 3 | 4 | 5 |

## In plain words

A find walks up a tree to its root, and path compression then points every node of the walk at the root. We must show that the walks are short on average.

Sort the possible ranks into a few blocks, where each block ends at a power of two of the end of the block before. There are only $\lg^* n$ blocks. A step of a walk is cheap to pay for in one of two ways. If it crosses into a new block, the find pays; that happens at most once per block. Otherwise the node pays, and it gets a much higher parent. A node can pay only until its parent is in a higher block, and the blocks are made so that the high-rank nodes are few. Each block pays at most $n$ in total.

## Proof

The full proof is in [the proof of the bound](proofs/main.md). Here is its outline.

1. **Rank facts.** Ranks increase strictly along each path, a non-root keeps its rank, each rank is at most $\lfloor \lg n \rfloor$, and at most $n/2^r$ nodes have rank $r$.
2. **Blocks.** Let $t(0) = 1$ and $t(g) = 2^{t(g-1)}$, so $t = 1, 2, 4, 16, 65536, \ldots$. Block 0 holds the ranks 0 and 1, and block $g \ge 1$ holds the ranks $r$ with $t(g - 1) < r \le t(g)$. All ranks lie in the blocks $0$ to $\lg^* n$.
3. **Charging a find.** In a FIND on the path $x_1, \ldots, x_s$, charge the step at $x_j$ to the FIND if $x_j$ or its parent is the root, or if its parent is in a higher block. Charge it to the node $x_j$ otherwise. A FIND gets at most $\lg^* n + 2$ charges: its own unit, the child of the root, and one for each change of block, since ranks rise along the path.
4. **Charging a node.** Each time $x$ is charged, its new parent, the root, has a rank larger than its old parent. So a node in block $g$ is charged at most $t(g)$ times before its parent leaves block $g$, and after that it is never charged.
5. **Few nodes in high blocks.** Block $g \ge 1$ has at most $\sum_{r > t(g-1)} n/2^r = n/t(g)$ nodes, so its nodes take at most $n$ charges in all. Block 0 takes at most $n$. With $\lg^* n + 1$ blocks, the nodes take at most $n(\lg^* n + 1)$ charges.
6. **Sum.** With at most $3m$ operations, the total is $O(m) + 3m(\lg^* n + 2) + n(\lg^* n + 1) = O(m \lg^* n)$, since $n \le m$. $\blacksquare$

**The blocks in numbers.** For $n = 2^{16}$, ranks are at most 16, and the blocks are $\{0, 1\}$, $\{2\}$, $\{3, 4\}$ and $\{5, \ldots, 16\}$. Block 3 has at most $n/2^4 = 4096$ nodes, each charged at most 16 times, which is $65536 = n$ charges.

## Consequences

- **Union-find is almost linear.** Every algorithm that does $O(m)$ union-find operations, such as [Kruskal's algorithm](/kruskal/) or [connected component labeling](/connected-component-labeling/), spends $O(m \lg^* n)$ time on them. The sharper [Tarjan bound](/union-find-amortized-bound/) gives $O(m\,\alpha(m, n))$.
- **The method.** The charging argument, with blocks of ranks that grow as a tower, is the model for the finer analysis with the [Ackermann function](/ackermann-function/). Replacing the tower $t$ by the levels $A_k$ gives the proof of Tarjan's bound in CLRS.
- **Rank counts.** The fact that at most $n/2^r$ nodes ever have rank $r$ is the key count of the proof, and it is used again in the analysis of Tarjan's bound.

## Tightness

The bound is not tight. Since $\alpha(m, n) \le \lg^* n$ for $m \ge n$ and $\alpha$ grows much more slowly, Tarjan's bound $O(m\,\alpha(m, n))$ is better, and Tarjan (1975) showed sequences that take $\Omega(m\,\alpha(m, n))$ time on this algorithm. So the true cost lies between these two functions, and it is $\Theta(m\,\alpha(m, n))$. The [union-find lower bound](/union-find-lower-bound/) shows that no structure does better than $\Omega(m\,\alpha(m, n))$.

Within its own method, the proof loses at two places: a node in block $g$ may be charged far fewer than $t(g)$ times, and most blocks hold far fewer than $n/t(g)$ nodes. The analysis by levels of the Ackermann function counts both more precisely.

## History

Galler and Fischer (1964) introduced the forest of parent pointers, and the rules of linking by size and path compression came into use soon after. Fischer (1972) proved an $O(m \log \log n)$ bound for linking by size with compression. Hopcroft and Ullman (1973) improved it to $O(m \lg^* n)$, in a paper that studies several set merging algorithms. Tarjan (1975) proved the tight bound $\Theta(m\,\alpha(m, n))$ for this algorithm, and Tarjan and van Leeuwen (1984) extended the bounds to other linking and compaction rules.

## References
