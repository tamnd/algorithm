---
title: The build returns a junction tree of the triangulated graph
proves: [correctness]
status: full
---

We use the pseudocode BUILD-JUNCTION-TREE of the page. The input is a graph $G$ on $n$ vertices and an order $\pi = (v_1, \ldots, v_n)$. Let $H = G_\pi^+$ be the filled graph: $G$ with all the fill edges of lines L3 and L4. For a vertex $v$ let $N^+(v)$ be its neighbours in $H$ that come after it in $\pi$; these are exactly the neighbours of $v$ in the current graph when line L3 runs, so the set of line L3 is $B_v = \{v\} \cup N^+(v)$. Line L4 makes $N^+(v)$ a clique of $H$, so each $B_v$ is a clique of $H$, and $H$ is chordal with $\pi$ as a perfect elimination ordering.

**Claim 1.** The list $C$ after line L5 holds exactly the maximal cliques of $H$, each once.

*Proof.* Let $K$ be a maximal clique of $H$ and $v$ its first vertex in $\pi$. Each other vertex of $K$ is a later neighbour of $v$, so $K \subseteq B_v$, and $K = B_v$ because $K$ is maximal and $B_v$ is a clique. So each maximal clique is some $B_v$, with $v$ its first vertex. Now take the vertices in the order of the loop. If $B_v$ is a maximal clique, it is not a subset of an earlier kept set $B_u$: such a $u$ comes before $v$ and is not in $B_v$, so $B_u \ne B_v$, and $B_v \subsetneq B_u$ is impossible for a maximal clique. So $B_v$ is kept. If $B_v$ is not maximal, it lies in a maximal clique $K = B_u$ where $u$ is the first vertex of $K$; $u \ne v$ and $v \in K$, so $u$ comes before $v$, and $B_u$ was kept by the first case. So line L5 skips $B_v$. $\blacksquare$

**Claim 2 (a clique tree exists).** The maximal cliques of $H$ can be joined by a tree with the running intersection property: for each vertex $x$, the cliques that hold $x$ form a connected subtree.

*Proof.* Induction on $i$ from $n$ down to 1, on the graph $H_i = H[\{v_i, \ldots, v_n\}]$. For $i = n$ the graph has one vertex and one clique. Assume a tree $T'$ for $H_{i+1}$, and let $S = N^+(v_i)$, a clique of $H_{i+1}$ and the full neighbourhood of $v_i$ in $H_i$. The cliques of $H_i$ that hold $v_i$ lie in $S \cup \{v_i\}$, so the maximal cliques of $H_i$ are those of $H_{i+1}$, possibly without one equal to $S$, plus $S \cup \{v_i\}$. If $S$ is empty, add the node $\{v_i\}$ with an edge to any node. If $S$ is a node of $T'$, replace that node by $S \cup \{v_i\}$. Otherwise $S$ lies in some node $K$ of $T'$; add the node $S \cup \{v_i\}$ with an edge to $K$. In each case $v_i$ is in one node only. A vertex $x \in S$ was in a connected set of nodes that holds $K$ (or the replaced node), and the new node is next to it, so the set stays connected. Other vertices are not affected. $\blacksquare$

**Claim 3 (Jensen and Jensen).** Let $C_1, \ldots, C_k$ be the maximal cliques of $H$, and give the pair $\{i, j\}$ the weight $|C_i \cap C_j|$. A spanning tree $T$ of the complete graph on the $k$ cliques has the running intersection property if and only if it has the maximum weight.

*Proof.* For a vertex $x$, let $k_x$ be the number of cliques that hold $x$, and let $T_x$ be the subgraph of $T$ on these cliques, with the edges of $T$ whose two ends hold $x$. Counting each pair $(x, \text{edge})$ with $x$ in the separator once,
$$\mathrm{weight}(T) = \sum_{\{i,j\} \in T} |C_i \cap C_j| = \sum_x |E(T_x)|.$$
$T_x$ is a subgraph of a tree, so it is a forest on $k_x$ nodes and $|E(T_x)| \le k_x - 1$, with equality if and only if $T_x$ is connected. So $\mathrm{weight}(T) \le \sum_x (k_x - 1)$, with equality if and only if every $T_x$ is connected. Every $T_x$ is connected exactly when $T$ has the running intersection property: if the cliques that hold $x$ are connected in $T$, the path between two of them uses only nodes that hold $x$, so its edges are in $T_x$. By Claim 2 some tree reaches the bound. So the maximum weight is $\sum_x (k_x - 1)$, and the trees of maximum weight are exactly the trees with the property. $\blacksquare$

**Claim 4.** Lines L6 to L10 return a spanning tree of maximum weight, so the result has the running intersection property.

*Proof.* Lines L8 to L10 are [Kruskal's algorithm](/kruskal/) on the complete graph of the cliques, with the edges taken in order of decreasing weight. Kruskal's algorithm returns a spanning tree of maximum weight when it takes the edges by decreasing weight, by the same exchange argument as for a minimum spanning tree. The complete graph is connected (pairs of weight 0 are in the list), so the result is a spanning tree. By Claim 3 it has the running intersection property. $\blacksquare$

**Conclusion.** Each edge of $G$ is an edge of $H$ and lies in a maximal clique of $H$, and by Claim 1 that clique is a node. With Claim 4, the nodes and the tree form a [tree decomposition](/tree-decomposition/) of $G$ and of $H$, of width $\max_i |C_i| - 1 = w(\pi)$, the induced width of the order. The separator of a tree edge is the intersection of its two cliques. $\blacksquare$
