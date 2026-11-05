---
title: The root of the sparsification tree holds the minimum spanning forest
proves: [correctness]
status: full
---

Fix a strict total order $\prec$ on the edges: $e \prec f$ if $w(e) < w(f)$, or $w(e) = w(f)$ and $e$ has the smaller id. For a finite multigraph $G$ on the vertex set $V$, let $\mathrm{MSF}(G)$ be the minimum spanning forest for this order. It is unique, because all weights are distinct under $\prec$, and Kruskal's algorithm computes it.

**Lemma 1 (cycle rule).** An edge $e$ of $G$ is not in $\mathrm{MSF}(G)$ if and only if $G$ has a cycle on which $e$ is the $\prec$-largest edge.

*Proof.* Kruskal's algorithm scans the edges in $\prec$-order and rejects $e$ exactly when its ends are already joined by earlier, so smaller, edges; those edges and $e$ form a cycle with $e$ largest. Conversely, if $e = \{u, v\}$ is largest on a cycle $Z$, then when Kruskal scans $e$, every other edge of $Z$ has been scanned, and each of them is either in the forest or has its ends already joined, so $u$ and $v$ are already joined and $e$ is rejected. $\square$

**Lemma 2 (strong certificate).** For any multigraphs $G$ and $H$ on $V$, $\mathrm{MSF}(G \cup H) = \mathrm{MSF}(\mathrm{MSF}(G) \cup H)$.

*Proof.* Write $G' = \mathrm{MSF}(G) \cup H$, a subgraph of $G \cup H$. First, $\mathrm{MSF}(G \cup H) \subseteq G'$: an edge of $G$ outside $\mathrm{MSF}(G)$ is largest on a cycle of $G$ by Lemma 1, hence largest on a cycle of $G \cup H$, hence not in $\mathrm{MSF}(G \cup H)$. Now take any edge $e$ of $G'$. If $e \notin \mathrm{MSF}(G \cup H)$, then by Lemma 1 there is a cycle in $G \cup H$ on which $e$ is largest. Take such a cycle and replace each edge $f$ on it that is not in $G'$: such an $f$ is in $G \setminus \mathrm{MSF}(G)$, so its ends are joined in $\mathrm{MSF}(G)$ by a path of edges $\prec f \prec e$. The result is a closed walk in $G'$ through $e$ once, all of whose other edges are $\prec e$; it contains a cycle through $e$ with $e$ largest. So $e \notin \mathrm{MSF}(G')$. Conversely, if $e \notin \mathrm{MSF}(G')$, then $e$ is largest on a cycle of $G'$, which is a cycle of $G \cup H$, so $e \notin \mathrm{MSF}(G \cup H)$. Hence the two forests have the same edges. $\square$

**Corollary.** $\mathrm{MSF}(G_1 \cup G_2) = \mathrm{MSF}(\mathrm{MSF}(G_1) \cup \mathrm{MSF}(G_2))$, by applying Lemma 2 twice: once with $G = G_1$, $H = G_2$, then with $G = G_2$, $H = \mathrm{MSF}(G_1)$.

**Stability.** The time bound of the paper uses one more fact, which the correctness proof below does not need: if one edge is inserted into or deleted from $G_1$, then $\mathrm{MSF}(G_1 \cup G_2)$ changes by at most one inserted and one deleted edge. For an insertion of $e$, the new forest is the old one plus $e$, minus the largest edge on the cycle that $e$ closes, if any. For a deletion of a forest edge, the new forest is the old one minus that edge, plus the smallest edge that reconnects the two parts, if any.

**Theorem.** After each operation, $F(\text{root}) = \mathrm{MSF}(G)$ for the current graph $G$.

*Proof.* For a node $x$, let $E(x)$ be the union of the groups at the leaves below $x$. Claim: after each operation, $F(x) = \mathrm{MSF}(E(x))$ for every node $x$. It holds after a build, by induction from the leaves: at a leaf by definition, and at an internal node by the Corollary, since $E(x) = E(\mathrm{left}(x)) \cup E(\mathrm{right}(x))$.

Assume the claim before an update. INSERT changes one group (line L1), and DELETE changes at most two groups, the group $E_i$ and the last group (lines L3 and L4). For a node $x$, the set $E(x)$ changes only if a changed group is below $x$, that is, if $x$ is on the path from a changed leaf to the root. Lines L2 and L5 call RECOMPUTE-PATH on every changed leaf. RECOMPUTE-PATH goes from the leaf upward (line L6), so when it recomputes $F(x)$ in line L7, both children of $x$ already hold the correct forests: a child on a recomputed path was done earlier in this or the previous call, and a child on no such path has an unchanged $E$. By the Corollary, $F(x)$ is then $\mathrm{MSF}(E(x))$. Nodes on no recomputed path keep their correct forests. When the number of groups exceeds the number of leaves, the implementation rebuilds the whole tree, which is again correct by the build argument.

At the root, $E(\text{root})$ is the set of all current edges, because every edge is in exactly one group and moving an edge in line L4 keeps it in some group. So $F(\text{root}) = \mathrm{MSF}(G)$, which line L8 reports. $\blacksquare$
