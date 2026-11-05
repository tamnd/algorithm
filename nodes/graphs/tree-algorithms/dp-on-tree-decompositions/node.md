---
tag: 97XH0N
kind: technique
slug: dp-on-tree-decompositions
name: Dynamic programming on tree decompositions
aliases:
- DP on tree decompositions
- treewidth DP
- treewidth dynamic programming
area: graphs/tree-algorithms
level: research
summary: Solve problems in time exponential only in treewidth by DP over a nice tree decomposition.
prereqs: [tree-decomposition, nice-tree-decomposition, treewidth, independent-set-on-trees]
see_also: [courcelle-theorem, cut-and-count, vertex-cover, three-coloring, dominating-set, hamiltonian-cycle, path-decomposition, baker-technique]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 7 (Treewidth), the nice tree decompositions and the dynamic programs for weighted independent set, dominating set and Steiner tree; Chapter 11 (Improving dynamic programming on tree decompositions), fast subset convolution, cut and count and the rank-based approach
  - paper: "Stefan Arnborg and Andrzej Proskurowski, Linear time algorithms for NP-hard problems restricted to partial k-trees, Discrete Applied Mathematics 23(1) (1989), 11-24"
    locator: the early dynamic programs over the tree structure of partial k-trees, the graphs of treewidth at most k
  - book: "Ton Kloks, Treewidth: Computations and Approximations, Lecture Notes in Computer Science 842, Springer, 1994"
    locator: the definition of nice tree decompositions and the conversion of any tree decomposition into a nice one with O(n) nodes
  - paper: "Johan M. M. van Rooij, Hans L. Bodlaender and Peter Rossmanith, Dynamic programming on tree decompositions using generalised fast subset convolution, ESA 2009, LNCS 5757"
    locator: the O*(3^k) algorithm for dominating set and the use of state changes and subset convolution in join nodes
  - paper: "Daniel Lokshtanov, Dániel Marx and Saket Saurabh, Known algorithms on graphs of bounded treewidth are probably optimal, SODA 2011"
    locator: the lower bounds under the strong exponential time hypothesis for independent set (2^k), dominating set (3^k) and q-coloring (q^k)
  - paper: "Marek Cygan, Jesper Nederlof, Marcin Pilipczuk, Michał Pilipczuk, Johan M. M. van Rooij and Jakub Onufry Wojtaszczyk, Solving connectivity problems parameterized by treewidth in single exponential time, FOCS 2011"
    locator: the cut and count technique for Hamiltonian cycle, Steiner tree and other connectivity problems
---

Dynamic programming on a [tree decomposition](/tree-decomposition/) solves many NP-hard graph problems in time $f(k) \cdot n$, where $k$ is the width of the decomposition and $f$ is usually exponential, so the problem becomes easy on graphs of small [treewidth](/treewidth/). Each node of the decomposition holds a small set of vertices, its *bag*, and the bag separates the vertices below the node from those above. A table at each node records, for each way the solution can look on the bag, the best partial solution below. Working with a [nice tree decomposition](/nice-tree-decomposition/), where each node introduces one vertex, forgets one vertex, or joins two copies of the same bag, the tables are filled bottom-up with four short rules. This generalizes the DP for [independent sets on trees](/independent-set-on-trees/), which is the case $k = 1$, and it is the algorithmic engine behind [Courcelle's theorem](/courcelle-theorem/).

## In plain words

Think of a large graph that is thin everywhere: it can be cut into pieces, arranged like a tree, so that neighboring pieces share only a few vertices. Those few shared vertices are the only connection between what lies below a piece and what lies above it.

So for each piece, you list every possible choice on its shared vertices, such as which of them are in the solution, and remember the best way to finish the part below for each choice. Going up the tree, a piece combines the lists of the pieces under it. Since only a few vertices are shared, each list is short, even though the graph can be huge.

At the top, the best entry of the list is the answer. The work grows quickly with the number of shared vertices, but only in proportion to the size of the graph.

## When it applies

- The input is an undirected graph $G$ with vertices numbered $0, \ldots, n - 1$, with vertex or edge weights when the problem has them, together with a tree decomposition $(T, \{X_t\})$ of width $k$: every vertex is in some bag, every edge has both ends in some bag, and the bags containing a vertex form a connected subtree of $T$. The tree $T$ is rooted at a chosen node $r$, its nodes are numbered $0, \ldots, N - 1$, and its edges are unweighted.
- The problem is *local enough*: whether a partial solution below a node can be extended depends only on a bounded summary of how it meets the bag. For independent set the summary is the subset of the bag that is chosen; for colorings it is the coloring of the bag; for connectivity problems it is a partition of the bag.
- The width $k$ is small, say up to 10 to 30 depending on the number of states. Finding an optimal decomposition is NP-hard, but for fixed $k$ it takes linear time (Bodlaender), and heuristics such as min-degree or min-fill elimination orders give good decompositions in practice.
- Trees are the case $k = 1$, with one bag $\{u, v\}$ per edge. A single vertex has one bag $\{0\}$; a path $0 - 1 - \cdots - (n-1)$ has the bags $\{i, i + 1\}$ in a path; a star with center 0 has the bags $\{0, i\}$, all attached to one node.

## The template

Make the decomposition nice and rooted, with empty bags at the root and at the leaves. Every other node $t$ has one of three forms, where $c$, $c_1$, $c_2$ are its children: *introduce* $v$, with $X_t = X_c \cup \{v\}$; *forget* $v$, with $X_t = X_c \setminus \{v\}$; and *join*, with $X_t = X_{c_1} = X_{c_2}$. Write $V_t$ for the vertices in the bags of the subtree of $t$, and $G_t$ for the subgraph of $G$ they induce. The table $f_t$ maps each *state* $s$ on the bag $X_t$ to the best value of a partial solution in $G_t$ whose restriction to $X_t$ is $s$.

```pseudo id=main
DP-ON-TREE-DECOMPOSITION(G, (T, X))   ▷ holes: STATES, LEAF, INTRODUCE, FORGET, JOIN, ANSWER
L1  convert (T, X) to a nice decomposition rooted at r with X_r = ∅
L2  for each node t of T in post-order, using an explicit stack do
L3      if t is a leaf then f_t ← LEAF()                          ▷ one state, the empty one
L4      else if t introduces v then f_t ← INTRODUCE(f_c, v)
L5      else if t forgets v then f_t ← FORGET(f_c, v)
L6      else f_t ← JOIN(f_{c1}, f_{c2})                            ▷ t joins c1 and c2
L7  return ANSWER(f_r)
```

The holes are the state space STATES on a bag and the four update rules. For maximum weight independent set, with weights $w(v) \ge 0$, the states on $X_t$ are the independent subsets $S \subseteq X_t$, and $f_t(S)$ is the largest weight of an independent set $I$ of $G_t$ with $I \cap X_t = S$:

- LEAF: $f_t(\emptyset) = 0$.
- INTRODUCE $v$: $f_t(S) = f_c(S)$ if $v \notin S$, and $f_t(S) = f_c(S \setminus \{v\}) + w(v)$ if $v \in S$ and $S$ is independent. The new vertex has no neighbors in $V_c \setminus X_c$, because every edge lies in some bag and the bags of $v$ are connected, so checking $S$ is enough.
- FORGET $v$: $f_t(S) = \max(f_c(S), f_c(S \cup \{v\}))$, the second term only when $S \cup \{v\}$ is independent.
- JOIN: $f_t(S) = f_{c_1}(S) + f_{c_2}(S) - w(S)$, since $V_{c_1} \cap V_{c_2} = X_t$ and the weight of $S$ is counted on both sides.
- ANSWER: $f_r(\emptyset)$.

**Why it works.** The bag $X_t$ separates $V_t \setminus X_t$ from $V \setminus V_t$: an edge between them would have to lie in a bag, but a vertex of $V_t \setminus X_t$ appears only in bags below $t$, and a vertex outside $V_t$ only in bags elsewhere. So a partial solution in $G_t$ interacts with the rest of the graph only through its state on $X_t$, and keeping the best partial solution per state loses nothing. Each rule is proved by induction from the leaves, by checking that it combines exactly the partial solutions of the children that are consistent with the state.

### Cost

From any decomposition of width $k$ with $O(n)$ nodes, a nice decomposition of the same width with $O(k n)$ nodes can be computed in $O(k^2 n)$ time. If a bag has at most $s(k)$ states and each rule costs $O(s(k) \cdot k^{O(1)})$, the total time is $O(s(k) \cdot k^{O(1)} \cdot n)$. For independent set, $s(k) = 2^{k+1}$, so the time is $O(2^k k^{O(1)} n)$; for $q$-coloring, $s(k) = q^{k+1}$. Only the tables of the children are needed when a node is processed, so each table can be freed once its parent is done. The space is $O(s(k) \cdot k)$ per stored table.

## Classic examples

**1. Maximum weight independent set, worked.** Take the graph on $0, \ldots, 5$ with edges $01, 12, 23, 30, 24, 34, 45$ (a 4-cycle, a triangle $2, 3, 4$ and a pendant edge $45$) and weights $w = [3, 2, 4, 1, 2, 5]$. A tree decomposition of width 2 has the bags $\{0, 1, 2\}$, $\{0, 2, 3\}$, $\{2, 3, 4\}$, $\{4, 5\}$, joined in that order. Root it at $\{0, 2, 3\}$ and make it nice: the root chain forgets 3, 2 and 0 above a join node with bag $\{0, 2, 3\}$; the left branch introduces 0, 1, 2, forgets 1 and introduces 3; the right branch introduces 4 and 5, forgets 5, introduces 2 and 3, forgets 4 and introduces 0. That gives 18 nodes. The independent subsets of $\{0, 2, 3\}$ are $\emptyset$, $\{0\}$, $\{2\}$, $\{3\}$, $\{0, 2\}$, and the tables at the join are

| $S$ | $\emptyset$ | $\{0\}$ | $\{2\}$ | $\{3\}$ | $\{0, 2\}$ |
|---|---|---|---|---|---|
| left child, $V = \{0, 1, 2, 3\}$ | 2 | 3 | 4 | 3 | 7 |
| right child, $V = \{0, 2, 3, 4, 5\}$ | 5 | 8 | 9 | 6 | 12 |
| join: left + right $- w(S)$ | 7 | 8 | 9 | 8 | 12 |

For example, the left entry 2 for $\emptyset$ is the set $\{1\}$, and the right entry 9 for $\{2\}$ is $\{2, 5\}$. The forget nodes above take the maximum, so the answer is 12, the set $\{0, 2, 5\}$, which a brute force over all 64 subsets confirms.

**2. Minimum vertex cover.** A set is a [vertex cover](/vertex-cover/) exactly when its complement is independent, so the same tables give it; directly, the states are subsets $S$ of the bag that cover the edges inside the bag.

**3. Three-coloring and $q$-coloring.** The states are the proper colorings of the bag, $q^{k+1}$ of them; introduce checks the new vertex against its neighbors in the bag, forget projects, and join takes the logical and (or the product, to count colorings). This decides [three-coloring](/three-coloring/) in $O(3^k k^{O(1)} n)$ and evaluates the [chromatic polynomial](/chromatic-polynomial/) at $q$.

**4. Dominating set.** Each bag vertex is in the set, dominated already, or not yet dominated. The naive join combines two states per vertex in 4 ways, giving $4^k$; changing the states to "in the set, dominated, or don't care" and using fast subset convolution brings the join to $O^*(3^k)$ (van Rooij, Bodlaender and Rossmanith). The answer is $f_r(\emptyset)$ with every forgotten vertex required to be dominated. See [dominating set](/dominating-set/).

**5. Connectivity problems.** For [Hamiltonian cycle](/hamiltonian-cycle/), [Steiner tree](/steiner-tree-problem/) and connected vertex cover, the state must also record which bag vertices are connected below, a partition of the bag, which gives $k^{O(k)} n$ time. [Cut and count](/cut-and-count/) (randomized) and the rank-based approach (deterministic) reduce this to $2^{O(k)} n$.

**6. Trees.** On a tree with the bags $\{u, v\}$ per edge, the independent set rules reduce to the two-state DP "take $v$ or not" of [independent sets on trees](/independent-set-on-trees/).

## Variations

- **Path decompositions.** If $T$ is a path, there are no join nodes, and the DP is a scan over a sequence of bags, as in the transfer-matrix method. [Path decompositions](/path-decomposition/) have larger width but simpler, often more cache-friendly, programs.
- **Courcelle's theorem.** Every property expressible in monadic second-order logic can be decided in $f(k) \cdot n$ time by such a DP, where the states are the types of a tree automaton. The theorem gives [fixed-parameter tractable](/fixed-parameter-tractable/) algorithms automatically but with a tower of exponentials in $k$; hand-written DPs are far faster.
- **Faster joins.** Join nodes are usually the bottleneck. Subset convolution, the zeta and Möbius transforms over subsets, and state changes make joins as fast as introduce and forget nodes for many problems.
- **Optimal lower bounds.** Under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/), independent set cannot be solved in $(2 - \varepsilon)^k n^{O(1)}$, dominating set in $(3 - \varepsilon)^k n^{O(1)}$, and $q$-coloring in $(q - \varepsilon)^k n^{O(1)}$ time (Lokshtanov, Marx and Saurabh), so the DPs above are probably optimal.
- **Planar graphs.** Planar graphs on $n$ vertices have treewidth $O(\sqrt{n})$, so the same DP gives subexponential algorithms, written $2^{O(n^{1/2})}$; [Baker's technique](/baker-technique/) uses graphs of bounded treewidth inside polynomial-time approximation schemes.
- **Counting and enumeration.** Replacing max and plus by plus and times counts solutions, for example independent sets or proper colorings, with the same table sizes.

## Pitfalls

- **Counting shared vertices twice.** In a join, the bag lies in both subtrees; the weights of bag vertices must be subtracted once. Equivalently, add the weight of a vertex when it is forgotten instead of when it is introduced, so that joins just add.
- **Checking constraints too late or too early.** A constraint on an edge $uv$ can be checked when both ends are in a bag, which happens at some node; a constraint on a vertex, such as "is dominated", can be checked only when the vertex is forgotten, since its last neighbor may come later.
- **Assuming the decomposition is good.** The running time is exponential in the width of the decomposition given, not in the treewidth. A poor heuristic decomposition can be much wider than the treewidth.
- **Recursion.** A recursive walk over $T$ fails on a decomposition of a path with $10^5$ vertices in Python; use an explicit stack or a precomputed post-order, as in line L2.
- **Memory.** Keeping every table costs $O(s(k) \cdot k n)$; free each child's table after its parent is computed, and store only what is needed for reconstruction.
- **Reconstruction.** The tables give values only. To output a solution, store the choice made at each entry, or re-run a top-down pass that picks, at each node, a child state consistent with the parent's state.

## Exercises

1. For a single vertex with weight $w(0)$, write down the nice decomposition (leaf, introduce 0, forget 0) and check that the rules return $w(0)$.
2. For the path $0 - 1 - \cdots - (n-1)$ with the bags $\{i, i+1\}$, show that the tables have at most 3 states and that the DP is the usual "take or skip" recurrence.
3. For the star with center 0 and leaves $1, \ldots, n-1$, build a nice decomposition with $n - 2$ join nodes on the bag $\{0\}$ and show that the answer is $\max(w(0), \sum_{i \ge 1} w(i))$.
4. In the worked example, compute the table of the node that forgets 1 in the left branch and check that the left row of the table follows from it.
5. Give the four rules for minimum dominating set with the three states "in the set", "dominated" and "not required to be dominated yet", and show that the join can be done in $O(4^k k^{O(1)})$ time by choosing, for each dominated bag vertex, the side that dominates it.
6. Show that every graph of treewidth $k$ has a nice tree decomposition of width $k$ with $O(k n)$ nodes, by converting an arbitrary decomposition with $O(n)$ nodes.
7. Modify the independent set DP to count the independent sets of the worked example graph.

## References
