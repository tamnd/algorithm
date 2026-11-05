---
tag: EAW1JK
kind: algorithm
slug: independent-set-on-trees
name: Independent set on trees
area: graphs/tree-algorithms
level: core
summary: Dynamic programming on a tree finds a maximum weight independent set in linear time by combining results from child subtrees.
solves: [maximum-independent-set-in-trees]
model: word-ram
complexity:
  vars: {n: the number of vertices of the tree}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [tree-dynamic-programming, independent-set, breadth-first-search]
see_also: [maximum-independent-set-in-trees, company-party-planning, maximum-independent-set, vertex-cover, dp-on-tree-decompositions, rerooting-technique]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 10.2, Solving NP-Hard Problems on Trees (the greedy algorithm for independent set on trees, and the dynamic program for maximum-weight independent set)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 6, Section 6.7, Independent sets in trees
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 14, Dynamic Programming, the end-of-chapter problem Planning a company party
---

This algorithm finds a maximum-weight [independent set](/independent-set/) of a tree in $\Theta(n)$ time by [dynamic programming on the tree](/tree-dynamic-programming/). For each vertex $v$ of the tree, rooted at any vertex, it computes two numbers: the best weight in the subtree of $v$ with $v$ in the set, and the best weight with $v$ out of the set. Each pair comes from the pairs of the children of $v$, so one pass from the leaves to the root gives the optimum, and one pass from the root to the leaves gives a set that reaches it. On general graphs the problem is NP-hard; on trees it is easy because each subtree meets the rest of the tree only through its root.

## In plain words

You want to pick some points of a tree, each with a value, with the biggest total, but you may never pick two points that are joined by a line.

Hang the tree from any point. Look at one point and everything below it. There are only two cases. If the point is picked, none of its children may be picked, so you need the best total of each child's part with that child left out. If the point is not picked, each child's part is free, and you take the better of its two cases. So each point needs only two numbers from each child. Fill these numbers in from the bottom up. At the top, take the better case. Then walk down again and read off which points the best totals used.

## The problem

The input is a tree on the vertices $0, \ldots, n-1$, $n \ge 1$, given by its $n - 1$ undirected edges, and an integer weight $w(v)$ for each vertex, which may be zero or negative. The tree is unrooted; the algorithm roots it at a vertex $r$ of its choice, which changes neither the answer nor the cost. The output is a set $S$ of vertices with no edge inside $S$ that maximizes $w(S) = \sum_{v \in S} w(v)$, and the value $w(S)$. The empty set is independent, so the optimum is at least 0. This is the weighted [maximum independent set in trees](/maximum-independent-set-in-trees/) problem; with all weights 1 it is the unweighted one.

## The algorithm

Write $p(v)$ for the parent of $v$ in the rooted tree. The arrays $in$ and $out$ start at 0.

```pseudo id=main
MWIS-TREE(T, w, r)
L1  BFS from r: the parent p(v) of each v, and the list B of the vertices in BFS order
L2  for each v in B in reverse order do        ▷ each child comes before its parent
L3      in[v] ← in[v] + w(v)                    ▷ in[v] already holds Σ out[c] over the children c
L4      if v ≠ r then in[p(v)] ← in[p(v)] + out[v];  out[p(v)] ← out[p(v)] + max(in[v], out[v])
L5  best ← max(in[r], out[r])
L6  for each v in B do                          ▷ each parent comes before its children
L7      if v ≠ r and p(v) ∈ S then continue      ▷ v must stay out
L8      if in[v] > out[v] then add v to S
L9  return (best, S)
```

The meaning of the two arrays, once $v$ is processed in line L2:

$$in[v] = \max\{\, w(I) : I \subseteq \mathrm{sub}(v) \text{ independent}, v \in I \,\}, \qquad out[v] = \max\{\, w(I) : I \subseteq \mathrm{sub}(v) \text{ independent}, v \notin I \,\},$$

where $\mathrm{sub}(v)$ is the set of descendants of $v$. They satisfy, with the sums over the children $c$ of $v$,

$$in[v] = w(v) + \sum_c out[c], \qquad out[v] = \sum_c \max(in[c], out[c]).$$

Lines L2 to L4 compute this recurrence. Instead of reading the children of $v$, each child adds its share to its parent when it is processed; reverse BFS order makes every child finish before its parent. The second pass, lines L6 to L8, decides each vertex after its parent. A vertex whose parent is in $S$ stays out. A free vertex goes in exactly when $in[v] > out[v]$, which is the case that line L5 took at the root. Both passes are loops, with no recursion, so a path of $10^5$ vertices needs no deep call stack.

## Example

The tree has 8 vertices rooted at 0, with the parent array $[-, 0, 0, 1, 1, 2, 2, 4]$ and the weights $w = [6, 7, 2, 3, 4, 5, 1, 8]$.

```
0 (6)
├── 1 (7)
│   ├── 3 (3)
│   └── 4 (4)
│       └── 7 (8)
└── 2 (2)
    ├── 5 (5)
    └── 6 (1)
```

The BFS order is $0, 1, 2, 3, 4, 5, 6, 7$. Line L2 visits the vertices in the order $7, 6, \ldots, 0$:

| $v$ | children | $in[v]$ | $out[v]$ |
|---|---|---|---|
| 7 | none | 8 | 0 |
| 6 | none | 1 | 0 |
| 5 | none | 5 | 0 |
| 4 | 7 | $4 + 0 = 4$ | $\max(8, 0) = 8$ |
| 3 | none | 3 | 0 |
| 2 | 5, 6 | $2 + 0 + 0 = 2$ | $5 + 1 = 6$ |
| 1 | 3, 4 | $7 + 0 + 8 = 15$ | $3 + 8 = 11$ |
| 0 | 1, 2 | $6 + 11 + 6 = 23$ | $15 + 6 = 21$ |

Line L5 gives $best = 23$. The second pass: $in[0] = 23 > 21$, so 0 is in $S$. Its children 1 and 2 stay out. Vertex 3 is free and $3 > 0$, so it is in. Vertex 4 is free and $4 < 8$, so it is out. Vertices 5 and 6 are free and positive, so they are in. Vertex 7 is free (its parent 4 is out) and $8 > 0$, so it is in. So $S = \{0, 3, 5, 6, 7\}$ and $w(S) = 6 + 3 + 5 + 1 + 8 = 23$.

Three small shapes:

- **One vertex.** $in[0] = w(0)$ and $out[0] = 0$. The answer is $\{0\}$ if $w(0) > 0$, and the empty set otherwise.
- **A path of $n$ vertices with weight 1.** The answer is $\lceil n/2 \rceil$, for example every second vertex starting at an end.
- **A star with center 0 and $n - 1$ leaves.** $in[0] = w(0)$ and $out[0]$ is the sum of the positive leaf weights. With $w(0) = 5$ and nine leaves of weight 1 the answer is the nine leaves, total 9; with $w(0) = 100$ it is the center alone.

## Correctness

The recurrence is correct by induction on the height of $v$: an independent set of $\mathrm{sub}(v)$ that contains $v$ is $\{v\}$ plus, for each child $c$, an independent set of $\mathrm{sub}(c)$ without $c$; one without $v$ is any choice of independent sets of the $\mathrm{sub}(c)$; and the choices for different children are independent of each other because no edge joins two different child subtrees. The second pass is correct by a top-down induction: the part of $S$ in $\mathrm{sub}(v)$ has weight $\max(in[v], out[v])$ when the parent of $v$ is out, and $out[v]$ when it is in. The full proof is in the proof file below.

## Complexity

- **Time.** The BFS of line L1 takes $\Theta(n)$ time on adjacency lists. Each of the loops of lines L2 and L6 visits each vertex once with $O(1)$ work. So the time is $\Theta(n)$ in each case, with integer weights of $O(1)$ words in the word RAM.
- **Space.** The arrays $p$, $in$, $out$, $B$ and the marks of $S$ take $\Theta(n)$ words beyond the input.

No algorithm can do better than $\Omega(n)$, since it must read each weight: changing one weight can change the answer.

## Properties

- **Root-free answer.** The optimum does not depend on $r$. The set $S$ may depend on $r$ when there are ties.
- **Ties.** The strict test of line L8 leaves a vertex out when both cases are equal. With weights that are all positive, any choice in a tie is optimal.
- **Negative weights.** A vertex with $w(v) \le 0$ never helps; line L8 leaves it out, because $in[v] = w(v) + \sum out[c] \le \sum \max(in[c], out[c]) = out[v]$.
- **Vertex cover.** The complement $V \setminus S$ of a maximum-weight independent set is a minimum-weight [vertex cover](/vertex-cover/), so the same pass solves weighted vertex cover on trees.

## Variants and improvements

- **Unweighted greedy.** With all weights 1, there is a maximum independent set that contains every leaf. Kleinberg and Tardos give the greedy rule: take a leaf, delete it and its neighbor, and repeat. It also runs in $O(n)$ time. The rule fails with weights, as the pitfalls show.
- **Recursive form.** The same recurrence written as a post-order recursion is the form of most textbooks. It is fine in languages with a large stack, and fails on deep trees in Python.
- **Rerooting.** To know, for each vertex $v$, the best weight of an independent set that contains $v$, run a second pass with the [rerooting technique](/rerooting-technique/): $O(n)$ in total.
- **Graphs of bounded treewidth.** The same idea, with one table entry per subset of a bag, solves the problem in $O(2^k n)$ time on a [tree decomposition](/tree-decomposition/) of width $k$. See [DP on tree decompositions](/dp-on-tree-decompositions/).
- **Other tree problems with the same shape.** Minimum dominating set, maximum matching and the [company party](/company-party-planning/) all use a small state per vertex and one bottom-up pass.

## When to use it

Use this algorithm whenever the conflict graph is a tree or a forest (run it on each tree of a forest and add the results). For a graph that is close to a tree, use a tree decomposition. For a general graph, the problem is NP-hard and needs exponential or approximate methods; see [maximum independent set](/maximum-independent-set/).

## Pitfalls

- **Greedy by weight.** Taking the heaviest vertex, deleting its neighbors and repeating gives $\{7, 1, 5, 6\}$ with weight 21 on the example, not 23. The fix is the recurrence of lines L3 and L4.
- **Reading the set from the values alone.** Taking every $v$ with $in[v] > out[v]$ can take a vertex and its child: on the example, $in[1] = 15 > out[1] = 11$ and $in[0] > out[0]$, but 0 and 1 are adjacent. Line L7 must check the parent first.
- **Wrong order.** If line L2 runs in BFS order instead of reverse BFS order, a parent reads its children before they are complete. The order must put each child first.
- **Recursion on deep trees.** A recursive DFS on a path of $10^5$ vertices fails in Python. Lines L1, L2 and L6 use BFS order and loops.
- **Answer below zero.** With negative weights, $\max(in[r], out[r])$ is never negative, since $out$ can always choose the empty set. Code that starts $in$ and $out$ at $-\infty$ breaks this.

## Implementations

## History

The dynamic program is a standard textbook example of dynamic programming on trees: Kleinberg and Tardos treat it in Section 10.2 as an NP-hard problem that becomes easy on trees, Dasgupta, Papadimitriou and Vazirani in Section 6.7, and CLRS as the problem of planning a company party.

## References
