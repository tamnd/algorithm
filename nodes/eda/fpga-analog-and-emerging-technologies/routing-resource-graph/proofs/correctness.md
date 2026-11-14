---
title: Minimal legal routings on a routing resource graph are exactly families of vertex-disjoint out-trees, and ROUTE-NET finds such a tree whenever one exists
proves: [correctness]
status: full
---

Let $G = (V, E)$ be a routing resource graph with capacity 1 on every node. A net $i$ has a source $s_i$ and a nonempty set $K_i$ of sinks, $s_i \notin K_i$. An *out-tree* rooted at $r$ is a subgraph in which $r$ has in-degree 0, every other node has in-degree 1, and every node is reachable from $r$; it has one edge fewer than it has nodes and no cycle. We take a subgraph to be its edge set together with its root, so its node set is $\{s_i\}$ and the ends of its edges.

**Lemma 1.** Let $R$ be a subgraph of $G$ with root $s$ in which every sink of $K$ is reachable from $s$. Then $R$ is minimal (no edge can be removed with every sink of $K$ still reachable from $s$) if and only if $R$ is an out-tree rooted at $s$ whose leaves are all in $K$.

*Proof.* ($\Leftarrow$) Let $R$ be such an out-tree and $(u, v)$ one of its edges. The subtree below $v$ is finite and nonempty, so it has a leaf, which is a sink $k$. In an out-tree the only path from $s$ to $k$ passes through the unique in-edge of $v$, since every node other than $s$ has exactly one in-edge. So removing $(u, v)$ makes $k$ unreachable, and no edge is removable.

($\Rightarrow$) Let $R$ be minimal. First, every edge $(u, v)$ of $R$ has $u$ reachable from $s$ in $R$: otherwise no path from $s$ uses the edge, and it could be removed. So every node of $R$ is reachable. Take a breadth-first search tree $A$ of $R$ from $s$: it is an out-tree rooted at $s$, it uses only edges of $R$, and it reaches every node of $R$, in particular every sink. If $R$ had an edge outside $A$, removing it would keep $A$ and so keep every sink reachable, against minimality. So $R = A$ is an out-tree. If a leaf $v$ of it were not a sink, its in-edge could be removed: only $v$ becomes unreachable, and $v \notin K$. So every leaf is in $K$. $\square$

**Theorem 2 (routings are disjoint trees).** A family of minimal routes $R_1, \ldots, R_m$ is a legal routing if and only if the $R_i$ are pairwise vertex-disjoint out-trees, $R_i$ rooted at $s_i$, holding all of $K_i$, with only sinks of $K_i$ as leaves.

*Proof.* By Lemma 1, each minimal route is an out-tree of this kind, and each such out-tree is a minimal route. With capacity 1, the routing is legal exactly when no node is in two routes, that is, when the node sets are pairwise disjoint. $\square$

The theorem also says that any legal routing contains a legal routing by such trees: removing edges from a route one at a time, while every sink stays reachable, ends in a minimal route after at most $|E|$ steps, and removing edges never makes two node sets meet.

**Lemma 3 (one search step).** At line L8, let $T$ be the current tree, $U$ the set used, and $F = V \setminus U$ the free nodes. The search finds $k$ if and only if $k$ is reachable from some node of $T$ by a path whose nodes after the first are in $F \setminus T$. When it finds $k$, the path that line L10 follows back has the fewest edges among such paths, its first node is in $T$, and its other nodes are not in $T$.

*Proof.* Add a new node $z$ with an edge to each node of $T$. The search of line L8 is a breadth-first search from $z$ in the graph induced on $\{z\} \cup T \cup (F \setminus T)$, in which the nodes of $T$ are at distance 1 and are never entered again. Breadth-first search reaches exactly the nodes reachable from $z$, and its search links give paths with the fewest edges ([breadth-first search](/breadth-first-search/)). A node of $T$ never gets a search link, since it is marked seen at the start. So the walk back from $k$ stops at the first node of $T$ that it meets, and every node before it is outside $T$. $\square$

**Theorem 4 (ROUTE-NET).** Let $s \notin U$. If ROUTE-NET$(G, s, K, U)$ returns, it returns an out-tree rooted at $s$ that holds $K$, has only sinks of $K$ as leaves, and has no node in $U$. It returns FAIL if and only if some $k \in K$ is not reachable from $s$ in the subgraph induced by $F = V \setminus U$.

*Proof.* The invariant of the loop of line L7 is: tree and route form an out-tree rooted at $s$, every node of it is in $F$, every leaf is a sink of $K$, and every node of it is reachable from $s$ in $F$. It holds at the start, with the single node $s \in F$. By Lemma 3, a step adds a path whose first node is in the tree and whose other nodes are new and free. Adding such a path to an out-tree keeps an out-tree: each new node gets one in-edge, and it is reachable through the first node. The only new leaf is $k$, and the first node of the path, if it was a leaf, now has an out-edge. So the invariant holds after line L10, and when the loop ends, every $k \in K$ is in the tree.

If the search fails for some $k$, Lemma 3 says that no path from the tree to $k$ runs through free nodes outside the tree. Suppose $k$ were reachable from $s$ in $F$, by a path $P$. The path starts in the tree. Let $u$ be its last node in the tree; the rest of $P$ after $u$ avoids the tree, is free, and ends at $k$, a contradiction. So $k$ is not reachable from $s$ in $F$. Conversely, if every $k$ is reachable from $s$ in $F$, then at each step $k$ is reachable from the tree by the same argument, so the search finds it, and the procedure does not fail. $\square$

**Corollary 5.** Route the nets one by one with ROUTE-NET, adding the nodes of each returned tree to $U$. The returned trees form a legal routing of the nets that did not fail, and each tree is minimal for its net.

*Proof.* Each tree avoids the $U$ of its call, which holds all earlier trees, so the trees are pairwise disjoint. By Theorem 4 each is an out-tree of the right kind, and by Lemma 1 it is minimal. Theorem 2 then gives legality. $\blacksquare$
