---
tag: NADX4Y
kind: algorithm
slug: shiloach-vishkin
name: Shiloach-Vishkin connectivity
aliases:
- Shiloach-Vishkin algorithm
- Awerbuch-Shiloach
- SV connectivity
area: parallel/parallel-graph-algorithms
level: advanced
summary: Parallel connected components by alternating hooking of trees and pointer-jumping shortcuts, in O(log n) rounds.
solves: [connected-components]
model: crcw-pram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O((n + m) log n)}
  depth: {worst: O(log n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
prereqs: [connected-components, pointer-jumping, crcw-pram, graph-contraction]
see_also: [union-find-connectivity, random-mate-contraction, parallel-minimum-spanning-tree, tarjan-vishkin, distributed-connected-components, spanning-forest, low-diameter-decomposition, work-efficiency]
sources:
  - paper: doi:10.1016/0196-6774(82)90008-6
    title: Yossi Shiloach and Uzi Vishkin, An O(log n) parallel connectivity algorithm, Journal of Algorithms 3(1), 1982
    locator: pp. 57 to 67 (hooking, shortcutting and stagnant trees on the CRCW PRAM, O(log n) time with O(n + m) processors)
  - paper: doi:10.1109/TC.1987.1676868
    title: Baruch Awerbuch and Yossi Shiloach, New connectivity and MSF algorithms for shuffle-exchange network and PRAM, IEEE Transactions on Computers C-36(10), 1987
    locator: pp. 1258 to 1263 (the star form with conditional and unconditional star hooking, and the proof of O(log n) iterations)
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 5, the section on connected components (the star test, hooking and pointer jumping); section number to be checked
---

Shiloach-Vishkin connectivity is a deterministic algorithm for the [connected components](/connected-components/) of an undirected graph on the [CRCW PRAM](/crcw-pram/), in $O(\log n)$ time with one processor for each vertex and each edge. It keeps a forest of parent pointers over the vertices, one tree for a set of vertices known to be connected. In each iteration, trees that are stars hook their root under a neighbouring tree, and one step of [pointer jumping](/pointer-jumping/) halves the height of every tree. This page gives the simpler star form of Awerbuch and Shiloach (1987), proves its correctness, and proves an $\lceil \log_2 n \rceil + 1$ bound on the iterations for the form that flattens all trees in each iteration.

Notation on this page: $n$ is the number of vertices, $m$ the number of edges, $W$ the work, $S$ the span and $T_p$ the time on $p$ processors. An iteration is one pass of the loop of lines L2 to L10. The model is the synchronous CRCW PRAM with the arbitrary write rule: when many processors write one cell in a step, one of them, not known in advance, succeeds. All bounds on this page are worst case over the write choices; the algorithm uses no random choices.

## In plain words

Every vertex starts as its own group, with a pointer to itself. A group is a small tree of pointers, and the vertex at the top names the group.

In each round, every edge between two groups lets one group join the other: the top of a flat group points to a member of the other group. To avoid loops, a group joins only a group with a smaller name, unless it was left out of every join in this round; then it may join any neighbouring group, which is safe because that group does not move.

After the joins, every vertex replaces its pointer by its pointer's pointer. This halves the height of every tree, so the trees stay flat.

When no join happens and every tree is flat, each group is one connected piece of the graph. The rounds grow with the logarithm of the number of vertices.

## The problem

The input is an undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, given as a list of $m$ edges. The output is an array $P$ with $P[u] = P[v]$ if and only if $u$ and $v$ are in the same connected component. At the end, $P[v]$ is the root of the tree of $v$, so it is a vertex of the component.

## The algorithm

$P$ is a forest: following $P$ from any vertex reaches a root $r$ with $P[r] = r$. A tree is a star when its height is at most 1, that is, $P[P[v]] = P[v]$ for all its vertices. Each edge $\{u, v\}$ gives two arcs, $(u, v)$ and $(v, u)$, each with its own processor.

```pseudo id=main
SHILOACH-VISHKIN(V, E)
L1  for all v in parallel do P[v] ← v
L2  repeat
L3      compute star[v] for all v by the star test
L4      for all arcs (u, v) in parallel do                    ▷ conditional star hooking
L5          if star[u] and P[u] > P[v] then P[P[u]] ← P[v]    ▷ concurrent write, an arbitrary writer wins
L6      for all v in parallel do stagnant[v] ← star[v], the root of v was not written in L5, and no root written in L5 now points into the star of v
L7      for all arcs (u, v) in parallel do                    ▷ unconditional hooking of stagnant stars
L8          if stagnant[u] and P[u] ≠ P[v] then P[P[u]] ← P[v]
L9      for all v in parallel do P[v] ← P[P[v]]               ▷ shortcut
L10 until no entry of P changed in this iteration
L11 return P
```

The star test of line L3 takes three steps: set $star[v] \gets true$ for all $v$; then for each $v$ with $P[v] \ne P[P[v]]$, set $star[v] \gets false$ and $star[P[P[v]]] \gets false$; then set $star[v] \gets star[v] \wedge star[P[v]]$. A vertex at depth 2 or more marks itself and, through its grandparent, the root; the vertices at depth 1 then read the mark of the root. Line L6 also takes $O(1)$ steps with a copy $Q$ of $P$ from before line L5: each root $r$ with $P[r] \ne Q[r]$ was written, and it sets a flag on $Q[P[r]]$, the old root of the vertex it now points to, with common concurrent writes of the value true. So a star is stagnant exactly when line L5 left it as it was: its root did not move and no other root moved into it.

The test in line L5 makes each hook go from a root to a smaller vertex, which rules out cycles. The restriction of line L8 to stagnant stars is needed: with the arcs of the edges $\{5,1\}$, $\{5,3\}$ and $\{3,2\}$, line L5 can give $P[5] = 1$ and $P[3] = 2$; if line L8 then let both new stars hook, it would set $P[1] = 2$ and $P[2] = 1$, a cycle. Neither of these stars is stagnant, so line L8 does nothing.

## Example

The graph is a star with center 4 and leaves 0, 1, 2 and 3. At the start every vertex is a one-vertex star.

| step | what happens | $P[0..4]$ |
|---|---|---|
| L1 | | 0 1 2 3 4 |
| L5 | the arcs $(4, 0)$ to $(4, 3)$ all write $P[4]$; say the write of 2 wins | 0 1 2 3 2 |
| L6 | the root 4 hooked, the star of 2 was hooked into, so the stagnant vertices are 0, 1 and 3 | |
| L8 | the arcs $(0, 4)$, $(1, 4)$, $(3, 4)$ read $P[4] = 2$ and set $P[0]$, $P[1]$, $P[3]$ to 2 | 2 2 2 2 2 |
| L9 | every vertex already points to the root 2 | 2 2 2 2 2 |

The second iteration changes nothing, so the algorithm stops after 2 iterations with one tree. The unconditional step did the work here: the leaves have smaller names than every vertex they see, so line L5 never lets them hook.

On the path with the edges $\{5,4\}$, $\{4,3\}$, $\{3,2\}$, $\{2,1\}$, $\{1,0\}$, line L5 of the first iteration hooks every vertex to its smaller neighbour, which gives the path $5 \to 4 \to 3 \to 2 \to 1 \to 0$ of height 5. The shortcuts then give heights 3, 2 and 1 after iterations 1, 2 and 3, and iteration 4 changes nothing: 4 iterations.

## Correctness

The proof in the proof file shows four facts. The pointers always form a forest: a hook in line L5 goes from a star root to a smaller vertex, and a cycle of such hooks would need a cycle of decreasing names; a hook in line L8 goes from a stagnant root into a tree that is not a stagnant star, because of two stars joined by an edge, the one with the larger root hooks in line L5, so they cannot both be stagnant. Each tree lies inside one component, because hooks follow edges and shortcuts stay inside a tree. Each iteration that changes something lowers the pair (number of trees, sum of the depths) in lexicographic order, so the loop ends. At the end, every tree is a star, every star is stagnant, and no arc joins two different trees, so each tree is a whole component.

## Complexity

The model is the CRCW PRAM, arbitrary write, with $n + 2m$ processors.

- **One iteration.** Every line is $O(1)$ steps with one processor for each vertex and each arc. The test of line L10 is an OR of $n$ flags, which is one step of common concurrent writes. So an iteration costs $O(n + m)$ work and $O(1)$ time.
- **Iterations, star form.** Awerbuch and Shiloach (1987) prove that their star form stops after $O(\log n)$ iterations. This page cites that bound and does not prove it. Their form decides which stars hook unconditionally by a second star test after the conditional hooking; the stagnant rule of line L6 is a variant of it, for which the proof file shows safety but not the iteration bound. In outline, their proof follows a measure of the heights of the trees, summed over all trees, and shows that it falls by a constant factor in each iteration; accounts of the proof give the factor $3/2$, which yields about $\log_{3/2} n$ iterations. The tests check $\lceil \log_{3/2} n \rceil + 3$ iterations for the form on this page on every run.
- **Iterations, full-shortcut form.** If line L9 is repeated until every tree is a star, the proof file shows that each iteration at least halves the number of trees in each component that has more than one, so there are at most $\lceil \log_2 n \rceil + 1$ iterations. Each iteration then costs $O(\log n)$ time for the shortcuts.

For the star form, with the cited bound,

$$W = O((n + m) \log n), \qquad S = O(\log n),$$

and for the full-shortcut form, proved here, $W = O((n + m) \log n + n \log^2 n)$ and $S = O(\log^2 n)$. By [Brent's theorem](/brent-theorem/), $T_p = O((n + m) \log n / p + \log n)$. The sequential [union-find](/union-find-connectivity/) or a BFS does $O(n + m)$ work, so the algorithm is not [work-efficient](/work-efficiency/): it pays a factor $\log n$ for its short span. Over random winners in the simulation, the mean number of iterations of the star form on paths with random vertex names is between $\log_2 n$ and $\log_2 n + 0.25$ for $n$ from 16 to 1,024 (20 trials for each $n$), well below the $\lceil \log_{3/2} n \rceil$ form of the bound.

## Properties

- **Deterministic algorithm, nondeterministic output.** The algorithm makes no random choices, but the final roots depend on which concurrent writes win. The partition into components does not.
- **Labels are vertices.** The label of each component is one of its vertices, the root of its star.
- **Forest at every step.** The pointer structure never has a cycle, at any step of any iteration.
- **Spanning forest for free.** If each hook records the arc that caused it, the recorded arcs form a [spanning forest](/spanning-forest/) of $G$: each hook joins two different trees.

## Variants and improvements

- **The original algorithm.** Shiloach and Vishkin (1982) hook trees that need not be stars, and they use the notion of a stagnant tree to make sure every tree that can grow does grow. The star form of Awerbuch and Shiloach is simpler to state and to prove.
- **Random mate.** Replace the name comparisons by coins: see [random-mate contraction](/random-mate-contraction/). The bounds become expected or with high probability.
- **Work-efficient connectivity.** Randomized algorithms reach $O(n + m)$ work and polylogarithmic span, for example through [low-diameter decomposition](/low-diameter-decomposition/), and Cole, Klein and Tarjan (1996) give linear-work randomized algorithms for minimum spanning forests and connectivity. These are not covered here.
- **Practice.** Shared-memory codes often drop the star test and alternate hooking of any root to a smaller neighbour with full pointer jumping. This is close to the full-shortcut form above, with the same correctness argument for the conditional hooks.
- **Minimum spanning forests.** Awerbuch and Shiloach also adapt the method to minimum spanning forests. See [parallel minimum spanning tree](/parallel-minimum-spanning-tree/).

## When to use it

Use it when connected components are needed in $O(\log n)$ parallel time on any graph, including graphs with a large diameter, where [parallel BFS](/parallel-bfs/) or label propagation needs as many rounds as the diameter. It also serves inside other parallel algorithms, such as [Tarjan-Vishkin](/tarjan-vishkin/) biconnectivity. On a machine with few cores and a small-diameter graph, a work-efficient method usually wins, because the extra factor $\log n$ in the work is paid on every core.

## Pitfalls

- **Unconditional hooking of every star.** As the example in the algorithm section shows, letting every star hook in line L8 can create a cycle of two roots. Only stagnant stars may hook unconditionally.
- **A wrong star test.** Testing only $P[P[v]] = P[v]$ at each $v$ misses the vertices at depth 1 of a tree of height 2 or more: such a vertex has $P[P[v]] = P[v]$, the root, but its tree is not a star. The third step of the star test is what marks them.
- **Hooking a non-root.** Line L5 writes $P[P[u]]$, the parent of the root of $u$'s star, not $P[u]$. Writing $P[u]$ moves one vertex out of its tree and can break the forest.
- **Reading and writing in one step.** All reads of a step see the state before the step. A simulation that applies the writes of line L5 one at a time, and lets later arcs see them, follows a different algorithm, and its cycle-freedom needs its own proof.
- **Stopping on "no hook".** A round without a hook can still leave trees of height 2 or more. The loop must also wait until the shortcut changes nothing.

## Implementations

## History

Shiloach and Vishkin (1982) gave the first $O(\log n)$ time connectivity algorithm on the CRCW PRAM, with hooking, shortcutting and stagnant trees. Awerbuch and Shiloach (1987) simplified it to the star form on this page, with a cleaner proof of the $O(\log n)$ bound, and extended it to minimum spanning forests and to the shuffle-exchange network.

## References
