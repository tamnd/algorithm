---
title: One depth-first search finds the articulation points, the bridges and the blocks
proves: [correctness]
status: full
---

Let $G = (V, E)$ be an undirected graph. Parallel edges and loops are allowed, and every edge has its own identifier. Loops are output as blocks by line L2 and are skipped by the search (the test $v \neq u$ of line L6); a loop lies on no cycle with another edge and changes no articulation point and no bridge, so from here on $G$ has no loops.

**Depth-first search facts.** The calls of line L3 build a [depth-first forest](/dfs-forest/). An edge is a *tree edge* if it is pushed by line L8, and every other edge is a *back edge*. Since the search skips the tree edge into $u$ only by its identifier, a parallel copy of a tree edge is a back edge. Each back edge joins a vertex $x$ to a proper ancestor $w$ of $x$ ([edge classification](/edge-classification/)); we call $x$ its *lower end*. For a tree edge, the lower end is the child. Write $T(v)$ for the subtree of $v$, and

$$\ell(v) = \min\big(\{ d[v] \} \cup \{ d[w] : \text{a back edge joins some } x \in T(v) \text{ to } w \}\big).$$

**Lemma 1.** When VISIT$(v, p)$ returns, $\mathrm{low}[v] = \ell(v)$.

*Proof.* By induction on the order in which the calls return. Line L5 sets $\mathrm{low}[v] = d[v]$. Each edge $e = \{v, w\}$ at $v$ other than $p$ is one of three kinds. If $d[w] = 0$, it becomes a tree edge, and line L9 takes the minimum with $\mathrm{low}[w] = \ell(w)$ by induction. If $d[w] < d[v]$, $w$ is an ancestor of $v$, so $e$ is a back edge with lower end $v$, and line L15 takes $d[w]$. If $d[w] > d[v]$, $w$ is a descendant of $v$ that is already visited, so $e$ is a back edge with lower end $w$, already counted in $\ell$ of a child; its value $d[v]$ is not below $d[v]$ anyway. So $\mathrm{low}[v]$ is the minimum over $v$, its own back edges and the subtrees of its children, which is $\ell(v)$. $\square$

**Lemma 2 (where an edge out of a subtree can go).** Let $(u, v)$ be a tree edge. Every edge with exactly one end in $T(v)$ is the tree edge $(u, v)$ or a back edge from a vertex of $T(v)$ to a proper ancestor of $v$, and the smallest discovery time among the ends of such back edges is $\ell(v)$ when it is below $d[v]$.

*Proof.* A tree edge with one end in $T(v)$ is $(u, v)$. A back edge joins a vertex to an ancestor, so if one end is in $T(v)$ and the other is not, the lower end is in $T(v)$ and the upper end is an ancestor of $v$ outside $T(v)$. The rest is the definition of $\ell$. $\square$

**Theorem 1 (bridges, line L13).** An edge $e$ is a bridge if and only if it is a tree edge $(u, v)$ with $\mathrm{low}[v] > d[u]$.

*Proof.* A back edge from $x$ to $w$ lies on the cycle formed with the tree path from $w$ to $x$, so it is not a bridge. For a tree edge $(u, v)$, the graph $G - e$ joins $T(v)$ to the rest if and only if some other edge has exactly one end in $T(v)$. By Lemma 2, such an edge is a back edge from $T(v)$ to an ancestor $w$ of $u$ (possibly $u$ itself, through a parallel copy of $e$), which has $d[w] \le d[u]$. So $e$ is not a bridge if and only if $\ell(v) \le d[u]$. Lemma 1 finishes the proof. $\square$

**Theorem 2 (articulation points, lines L4 and L12).** A root $r$ is an articulation point if and only if it has at least two children. A vertex $u$ that is not a root is one if and only if it has a child $v$ with $\mathrm{low}[v] \ge d[u]$.

*Proof.* Root. By Lemma 2 no edge joins the subtrees of two children of $r$, since a back edge goes to an ancestor. With two or more children, $G - r$ splits them. With one child $v$, $G - r$ contains the tree $T(v)$, which spans the rest of the component.

Not a root. Suppose a child $v$ has $\ell(v) \ge d[u]$. By Lemma 2, every edge that leaves $T(v)$ goes to an ancestor $w$ of $v$ with $d[w] \ge d[u]$, so to $u$. In $G - u$, the set $T(v)$ has no edge to the root $r \neq u$, so $u$ is an articulation point. Conversely, suppose every child $v$ has $\ell(v) < d[u]$. Then each $T(v)$ has a back edge to a proper ancestor of $u$. The vertices of the component that are not in $T(u)$ form a subtree that contains $r$, so they stay connected in $G - u$, and each $T(v)$ is joined to them. So $G - u$ has as many components as $G$. $\square$

**Theorem 3 (blocks, line L11).** Each block of $G$ is output exactly once, as the set of edges popped by line L11.

*Proof.* Call a vertex $y$ that is not a root a *head* if $\mathrm{low}[y] \ge d[\pi(y)]$, where $\pi(y)$ is the parent of $y$; these are the children for which line L10 succeeds. Every child of a root is a head. For an edge $f$ with lower end $x$, let $h(f)$ be the first head on the tree path from $x$ up to the root, starting at $x$. Let $R(y)$ be $T(y)$ without the subtrees $T(y')$ of the heads $y' \neq y$ inside $T(y)$.

*Step 1: line L11 pops exactly the edges $f$ with $h(f) = y$ when it closes the tree edge $(\pi(y), y)$.* The edges pushed from the push of $(\pi(y), y)$ until VISIT$(y)$ returns are the edges whose lower end is in $T(y)$, since line L8 and line L15 push an edge when its lower end is the current vertex. The pops for heads inside $T(y)$ happen earlier, since a call returns after its descendants; by induction they removed the edges whose $h$ is such a head. The remaining edges above $(\pi(y), y)$ on the stack are those with $h(f) = y$.

*Step 2: all ends of an edge $f$ with $h(f) = y$ lie in $R(y) \cup \{\pi(y)\}$.* The lower end $x$ is in $R(y)$. If $f$ is a back edge to $w$, then $d[w] \ge \ell(x) \ge \ell(y) \ge d[\pi(y)]$, so $w$ is on the tree path from $\pi(y)$ to $x$; an inner vertex of this path in some $T(y')$ would put $x$ in $T(y')$ too, so $w \in R(y) \cup \{\pi(y)\}$.

*Step 3: two edges on a common cycle have the same $h$.* Let $y'$ be a head. By Lemma 2 and $\ell(y') \ge d[\pi(y')]$, every edge with exactly one end in $T(y')$ has its other end at $\pi(y')$. A cycle that enters $T(y')$ must enter and leave it through $\pi(y')$, and it passes $\pi(y')$ only once, so the whole cycle lies in $T(y') \cup \{\pi(y')\}$. So every cycle $C$ either lies in $T(y') \cup \{\pi(y')\}$ or has no vertex in $T(y')$. Take the deepest head $y$ with $C \subseteq T(y) \cup \{\pi(y)\}$; it exists because $C$ lies in the subtree of one child of a root. Every head $y' \neq y$ inside $T(y)$ has $T(y')$ disjoint from $C$, so all lower ends of edges of $C$ are in $R(y)$, and all edges of $C$ have $h = y$.

*Step 4: the edges with $h = y$ are pairwise on common cycles.* Write $u = \pi(y)$. Let $(a, b)$ be a tree edge with $b \in R(y)$ and $b \neq y$. Then $b$ is not a head, so $\ell(b) < d[a]$, and some back edge goes from $x' \in T(b)$ to a proper ancestor of $a$. If $x'$ were in $T(y')$ for a head $y'$ inside $T(b)$, the edge would end at $\pi(y') \in T(b)$, which is not an ancestor of $a$; so $x' \in R(y)$. The cycle of this back edge and the tree path contains $(a, b)$ and the tree edge into $a$. So by induction upward, every tree edge with lower end in $R(y)$ lies on a common cycle with $(u, y)$, in the sense of the relation $\equiv$ of the [biconnected components](/biconnected-components/) page. A back edge $f$ with $h(f) = y$ from $x$ to $w$ lies on a cycle with the first tree edge below $w$ on the path to $x$, and by Step 2 that tree edge has its lower end in $R(y)$. Since $\equiv$ is transitive, all edges with $h = y$ are in one class.

Steps 3 and 4 show that the classes of $\equiv$ on the non-loop edges are exactly the sets $\{ f : h(f) = y \}$ for the heads $y$, each one non-empty because it contains $(\pi(y), y)$. Step 1 shows that line L11 outputs each of these sets once. $\square$

**Termination and output.** Each vertex is visited once, each list entry is read once, and each non-loop edge is pushed once and popped once. So the procedure stops, it outputs every block once (Theorem 3 and line L2), and it marks exactly the articulation points and the bridges (Theorems 1 and 2). $\blacksquare$
