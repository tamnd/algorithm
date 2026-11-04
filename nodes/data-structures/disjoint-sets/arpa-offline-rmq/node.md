---
tag: 2G2RRV
kind: algorithm
slug: arpa-offline-rmq
name: Offline RMQ in linear time with union-find (Arpa's trick)
aliases:
- Offline RMQ in linear time with DSU (Arpa's trick)
area: data-structures/disjoint-sets
level: advanced
summary: A linear-time offline method for answering range minimum queries by processing the array with a stack and union-find, using near-constant amortized merges.
solves: [range-minimum-query]
model: word-ram
complexity:
  vars: {n: the length of the array, q: the number of queries}
  time: {worst: O((n + q) log n)}
  space: {extra: Θ(n + q)}
properties: {deterministic: true, online: false, recursive: false}
prereqs: [range-minimum-query, monotonic-stack, path-compression]
see_also: [range-minimum-query, monotonic-stack, cartesian-tree, tarjan-offline-lca, sparse-table, gabow-tarjan-union-find, offline-query-processing, path-compression]
sources:
  - url: https://cp-algorithms.com/data_structures/disjoint_set_union.html
    title: cp-algorithms, Disjoint Set Union
    locator: the section on range minimum queries offline (Arpa's trick)
  - paper: doi:10.1145/62.2160
    title: "Robert E. Tarjan and Jan van Leeuwen, Worst-case analysis of set union algorithms, Journal of the ACM 31(2) (1984), 245-281"
    locator: the bound for path compression with an arbitrary linking rule
  - paper: doi:10.1016/0022-0000(85)90014-5
    title: "Harold N. Gabow and Robert E. Tarjan, A linear-time algorithm for a special case of disjoint set union, Journal of Computer and System Sciences 30(2) (1985), 209-221"
    locator: the linear-time algorithm for static tree set union
---

Arpa's trick answers $q$ [range minimum queries](/range-minimum-query/) on an array of length $n$ offline, with one sweep from left to right, a [monotonic stack](/monotonic-stack/) and a union-find forest. When the sweep reaches position $i$, every element that $a[i]$ pops from the stack is linked to $i$. Then, for each query $[L, R]$ with $R = i$, the root of $L$ is the position of the minimum of $a[L..R]$. With [path compression](/path-compression/) alone, the sweep takes $O((n + q) \log n)$ time in the worst case and is close to linear in practice. Because the links form a tree that can be computed in advance, the [Gabow-Tarjan](/gabow-tarjan-union-find/) structure makes it $O(n + q)$. The method is short, needs no tables, and has no $\log n$ factor of space, unlike a [sparse table](/sparse-table/).

## In plain words

Read the array from left to right. Keep a stack of the positions that could still be the smallest value of some range that ends here. When a new value comes, every larger value on the top of the stack can never be the answer again, because the new value is smaller and further right. Pop it.

Each popped position now points to the new position. So if you start at a position and follow the pointers, you jump to smaller and smaller values on the right, until you reach a position that is still on the stack.

That position is the answer for every range that starts at your position and ends here. Shorten the pointers as you follow them, so that later walks are fast.

## The problem

**Input.** An array $a[0..n-1]$ of values with a total order, and $q$ queries $(L_k, R_k)$ with $0 \le L_k \le R_k \le n - 1$, all known in advance.

**Output.** For each query, the position $\arg\min_{L_k \le t \le R_k} a[t]$, the leftmost one if there are ties, or its value $a[t]$. See [range minimum query](/range-minimum-query/).

## The algorithm

```pseudo id=main
ARPA-RMQ(a[0..n−1], queries)
L1  for i ← 0 to n − 1 do p[i] ← i
L2  bucket the queries by their right end R
L3  S ← empty stack
L4  for i ← 0 to n − 1 do
L5      while S ≠ ∅ and a[top(S)] > a[i] do
L6          p[pop(S)] ← i                   ▷ the popped root joins the tree of i
L7      push i on S
L8      for each query k with R_k = i do
L9          ans[k] ← FIND(L_k)
L10 return ans

FIND(x)                                     ▷ two-pass path compression
L11 r ← x; while p[r] ≠ r do r ← p[r]
L12 while p[x] ≠ r do nx ← p[x]; p[x] ← r; x ← nx
L13 return r
```

Lines L5 to L7 are the usual stack of the next smaller element. The stack holds the roots of the forest. The link of line L6 points a root to $i$, which at that moment is a root with no children or with only the roots popped earlier in this step. Line L9 runs after $i$ is pushed, so a query with $L_k = R_k = i$ returns $i$.

The parent that line L6 gives to $j$ is the first position $i > j$ with $a[i] < a[j]$, the *next smaller element* of $j$. So the forest at the end is fixed by the array alone: it is the tree of next smaller elements. Path compression then only adds shortcuts toward the root.

## Example

Let $a = [3, 1, 4, 1, 5, 9, 2, 6]$, with positions 0 to 7, and the queries $(0, 2)$, $(2, 5)$, $(5, 5)$, $(2, 6)$, $(4, 7)$ and $(0, 7)$. The table shows the state after line L7 for each $i$, without path compression.

| $i$ | $a[i]$ | popped, now pointing to $i$ | stack | parents of 0 to 7 | queries with $R = i$ |
|---|---|---|---|---|---|
| 0 | 3 | | 0 | 0 1 2 3 4 5 6 7 | |
| 1 | 1 | 0 | 1 | 1 1 2 3 4 5 6 7 | |
| 2 | 4 | | 1 2 | 1 1 2 3 4 5 6 7 | $(0, 2)$: FIND(0) = 1, min 1 |
| 3 | 1 | 2 | 1 3 | 1 1 3 3 4 5 6 7 | |
| 4 | 5 | | 1 3 4 | 1 1 3 3 4 5 6 7 | |
| 5 | 9 | | 1 3 4 5 | 1 1 3 3 4 5 6 7 | $(2, 5)$: FIND(2) = 3, min 1; $(5, 5)$: FIND(5) = 5, min 9 |
| 6 | 2 | 5, 4 | 1 3 6 | 1 1 3 3 6 6 6 7 | $(2, 6)$: FIND(2) = 3, min 1 |
| 7 | 6 | | 1 3 6 7 | 1 1 3 3 6 6 6 7 | $(4, 7)$: FIND(4) = 6, min 2; $(0, 7)$: FIND(0) = 1, min 1 |

At $i = 3$, the value 1 does not pop position 1, because $a[1] = 1$ is not larger. So the query $(0, 7)$ returns position 1, the leftmost of the two minima. At $i = 6$, the value 2 pops 5 and then 4, and both point to 6.

## Correctness

**Invariant (A).** After line L7 for $i$, let the stack be $s_1 < s_2 < \cdots < s_k = i$. Then:

1. $a[s_1] \le a[s_2] \le \cdots \le a[s_k]$;
2. the roots of the forest on $0..i$ are exactly $s_1, \ldots, s_k$, and the tree of $s_j$ is the interval $(s_{j-1}, s_j]$, with $s_0 = -1$;
3. for each $t$ in the tree of $s_j$, every $u \in [t, s_j)$ has $a[u] > a[s_j]$.

Given (A), a query $(L, i)$ with $s_{j-1} < L \le s_j$ gets $\mathrm{FIND}(L) = s_j$. All of $[L, s_j)$ has values larger than $a[s_j]$, by part 3, and all of $(s_j, i]$ lies in later trees, whose nodes have values at least the value of their root, which is at least $a[s_j]$, by parts 3 and 1. So $s_j$ is the leftmost minimum of $a[L..i]$. Path compression keeps every node in its tree, so it does not change the roots. The proof of (A) by induction on $i$ is in [the correctness proof](proofs/correctness.md).

**Termination.** Each position is pushed once and popped at most once, and each FIND climbs at most $n$ edges, because parents have larger positions.

## Complexity

| quantity | bound |
|---|---|
| stack work | $O(n)$, each position pushed and popped at most once |
| links | at most $n - 1$ |
| finds | $q$, with path compression |
| total time | $O(n + q \log_{2 + q/n} n)$, so $O((n + q) \log n)$ |
| total time with [Gabow-Tarjan](/gabow-tarjan-union-find/) | $O(n + q)$ |
| extra space | $\Theta(n + q)$ |

- **With path compression alone.** The links do not follow a rank or size rule, so the bound is the one of Tarjan and van Leeuwen for compression with any linking: $n - 1$ links and $q$ finds cost $O(n + q \log_{2 + q/n} n)$. For $q = n$ this is $O(n \log n)$, and for $q \ge n^{1 + \varepsilon}$ it is $O(q/\varepsilon)$. cp-algorithms describes the cost as $O(\alpha(n))$ on average; that is how it behaves on typical inputs, not a worst-case bound for this linking.
- **Union by rank is not free here.** Linking by rank would make the root of a merged set an arbitrary element, while the answer must be the position $s_j$. Each root can store the position $s_j$ of its set, which restores the $O((n + q)\,\alpha(n))$ bound.
- **Linear time.** The tree of next smaller elements can be computed before the sweep with the same stack, and line L6 links only along its edges. So the sweep is an instance of [static tree set union](/static-tree-set-union/), and the [Gabow-Tarjan](/gabow-tarjan-union-find/) structure runs it in $O(n + q)$ time on a word RAM.

## Properties

- **Offline.** All queries must be known, and they are answered in the order of their right ends.
- **Leftmost minimum.** Line L5 pops only strictly larger values, so ties go to the leftmost position. With $\ge$ in line L5, ties go to the rightmost one.
- **Comparison only.** The values need only a total order, and the algorithm does $O(n)$ comparisons. The finds compare no values.
- **Small memory.** Besides the array, it needs a parent array, a stack and the buckets of queries, $\Theta(n + q)$ words in all.

## Variants and improvements

- **Range maximum.** Pop smaller values instead of larger ones.
- **Store values at the roots.** For other operations, such as a minimum of a key with a position, store a record at each root and return it from FIND.
- **Union by rank with a stored answer.** Link by rank and keep the position $s_j$ at each root, for a worst-case bound of $O((n + q)\,\alpha(n))$.
- **Through the Cartesian tree.** The minimum of $a[L..R]$ is the [lowest common ancestor](/lowest-common-ancestor/) of $L$ and $R$ in the [Cartesian tree](/cartesian-tree/) of $a$. [Tarjan's offline LCA algorithm](/tarjan-offline-lca/) on that tree gives the same answers with a union-find forest of the same kind. Arpa's trick does it in one sweep, without building the tree.
- **Online queries.** If the queries come online, use a [sparse table](/sparse-table/) in $O(n \log n)$ space and $O(1)$ time per query, or a linear-space method such as [Fischer-Heun](/fischer-heun-rmq/).

## When to use it

Use it when all queries are known in advance and memory is tight, or as a short and fast method in contest code. It needs only an array of parents and a stack. When the queries are online or very many, a [sparse table](/sparse-table/) or a [segment tree](/segment-tree/) may be simpler to use.

## Pitfalls

- **Answer at the wrong time.** The query $(L, R)$ must be answered right after position $R$ is pushed, not before, and not later: after position $R + 1$ is processed, the root of $L$ can be a position past $R$.
- **Returning the root as a value.** FIND returns a position. The answer is $a[\mathrm{FIND}(L)]$.
- **Linking in the wrong direction.** Line L6 makes the popped root a child of $i$. The other direction makes $i$ a child of an old root, and then the root is no longer the minimum of its interval.
- **Recursive find.** The links do not keep the trees shallow. A sorted decreasing array makes a chain of $n$ nodes, and a recursive FIND can overflow the stack. Use the two passes of lines L11 and L12.
- **Ties.** Using $\ge$ in line L5 changes which position is returned. Both are correct minima, but code that needs the leftmost one must use $>$.

## Implementations

The Python function `arpa_offline_rmq(a, queries)` returns the position of the leftmost minimum for each query, in the order of the input. It uses the iterative find of lines L11 to L13. The test compares it with a direct scan on random arrays with many ties.

## History

The method is known in competitive programming as Arpa's trick, after AmirReza Poorakhavan, who made it popular; cp-algorithms describes it in its page on disjoint set union. The idea is close to [Tarjan's offline LCA algorithm](/tarjan-offline-lca/), applied to the [Cartesian tree](/cartesian-tree/) of the array. The linear bound follows from the Gabow-Tarjan algorithm (1985) for static tree set union.

## References
