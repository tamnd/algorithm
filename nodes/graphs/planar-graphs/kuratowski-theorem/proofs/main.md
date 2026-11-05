---
title: Proof of Kuratowski's theorem
proves: [statement]
status: full
---

We prove that a finite graph $G$ is planar if and only if it contains no subdivision of $K_5$ or $K_{3,3}$. Graphs are simple: loops and parallel edges do not change planarity. We write $TH$ for a subdivision of $H$, and say that $G$ *contains* $TH$ if some subgraph of $G$ is a $TH$. A **model** of $H$ in $G$ is a family of disjoint vertex sets $V_h$ ($h \in V(H)$), the branch sets, each inducing a connected subgraph, with an edge of $G$ between $V_h$ and $V_{h'}$ for each edge $hh'$ of $H$; $G$ has an $H$ [minor](/graph-minor/) exactly when it has a model of $H$. The proof follows the route of Diestel, Sections 4.4 and 3.2, with the minimal counterexample of Thomassen.

## The easy direction

A subgraph of a planar graph is planar: delete points and arcs from a drawing. If $G$ contains $TK_5$ or $TK_{3,3}$ and $G$ were planar, a drawing of the subdivision would give a drawing of $K_5$ or $K_{3,3}$, by reading each subdivided path as one arc. But $K_5$ has $10 > 3 \cdot 5 - 6$ edges, and $K_{3,3}$ is triangle-free with $9 > 2 \cdot 6 - 4$ edges, so neither is planar by the edge bounds from [Euler's formula](/euler-formula/). So a planar graph contains neither subdivision.

## From minors to subdivisions

**Lemma 1 (a center in a tree).** Let $T$ be a finite tree and let $k$ labels be placed on vertices of $T$ (several labels may sit on one vertex). If no edge $e$ of $T$ leaves at least 2 labels on each side of $T - e$, then there is a vertex $x$ such that each component of $T - x$ carries at most one label.

*Proof.* Each edge $e$ has a side with at most one label. Orient $e$ away from such a side (if both sides have at most one label, orient it either way). Start anywhere and follow the oriented edges. A walk along oriented edges in a tree cannot use an edge twice (it would have to go back against its orientation) and cannot close a cycle, so it never repeats a vertex and stops at a vertex $x$ with no outgoing edge. For each edge $xy$, the edge points to $x$, so the side of $y$, which is the component of $T - x$ that contains $y$, has at most one label. $\square$

Call such an $x$ a **center**. For a center $x$ and each label $\ell$ on a vertex $a_\ell$, the paths $x T a_\ell$ meet pairwise only in $x$: two of them lie in different components of $T - x$, or one is the trivial path $x$.

**Lemma 2.** (a) If $G$ has a $K_{3,3}$ minor, then $G$ contains $TK_{3,3}$. (b) If $G$ has a $K_5$ minor, then $G$ contains $TK_5$ or $TK_{3,3}$.

*Proof.* Let $(V_h)$ be a model of $H \in \{K_5, K_{3,3}\}$ in $G$. For each edge $hh'$ of $H$ fix an edge $a_{hh'} a_{h'h}$ of $G$ with $a_{hh'} \in V_h$ and $a_{h'h} \in V_{h'}$. In $V_h$, put the label $h'$ on $a_{hh'}$ for each neighbour $h'$ of $h$, and let $T_h$ be a spanning tree of $G[V_h]$.

Suppose first that every $T_h$ has a center $x_h$. For each edge $hh'$ of $H$, let $P_{hh'}$ be the path $x_h T_h a_{hh'}$, the edge $a_{hh'} a_{h'h}$, and $a_{h'h} T_{h'} x_{h'}$. Two such paths meet only in common ends: inside one tree $T_h$, the parts toward different labels meet only in $x_h$ by the remark after Lemma 1, and different trees are disjoint. So the paths $P_{hh'}$ with the vertices $x_h$ form a $TH$ in $G$.

For $H = K_{3,3}$ each vertex has 3 labels, and no edge of $T_h$ can leave 2 labels on each side, so Lemma 1 gives a center in every tree. This proves (a).

For $H = K_5$, if every $T_h$ has a center we get $TK_5$. Otherwise, by Lemma 1, some tree, say $T_1$ with labels $2, 3, 4, 5$, has an edge $u_1 u_2$ such that the component $U_1$ of $T_1 - u_1 u_2$ that contains $u_1$ carries two labels, say 2 and 3, and the component $U_2$ that contains $u_2$ carries 4 and 5. Then the sets $V(U_1), V_4, V_5$ and $V(U_2), V_2, V_3$ are the branch sets of a $K_{3,3}$ model with these two sides: $U_1$ and $U_2$ are connected and joined by the edge $u_1 u_2$; $U_1$ contains $a_{12}$ and $a_{13}$, so it is joined to $V_2$ and $V_3$; $U_2$ is joined to $V_4$ and $V_5$ in the same way; and each of $V_4, V_5$ is joined to each of $V_2, V_3$ because the $V_h$ form a $K_5$ model. So $G$ has a $K_{3,3}$ minor, and contains $TK_{3,3}$ by (a). $\square$

Since a $TH$ in $G$ gives an $H$ minor (contract the subdivided paths), Lemma 2 shows: **$G$ contains $TK_5$ or $TK_{3,3}$ if and only if $G$ has a $K_5$ or $K_{3,3}$ minor.** Minors of minors are minors, so if $G$ contains neither subdivision, neither does any minor of $G$.

## A contractible edge

A graph is 3-connected if it has more than 3 vertices and no set of at most 2 vertices separates it. In a 3-connected graph $G$, if $S$ is a set of 3 vertices that separates $G$, then each vertex $s \in S$ has a neighbour in every component of $G - S$: otherwise the other two vertices of $S$ would separate that component from the rest.

**Lemma 3 (Thomassen).** Every 3-connected graph $G$ other than $K_4$ has an edge $xy$ such that $G / xy$ is 3-connected.

*Proof.* The only 3-connected graph with 4 vertices is $K_4$, so $G$ has $n \ge 5$ vertices and each $G / xy$ has at least 4. Suppose that no contraction is 3-connected. Let $xy$ be an edge and $v_{xy}$ the vertex of $G/xy$ that replaces $x$ and $y$. Then $G / xy$ has a separating set $S$ of at most 2 vertices. If $v_{xy} \notin S$, then $S$ separates $G$ too, which is impossible. So $S$ contains $v_{xy}$, and $S = \{v_{xy}, z\}$ for a vertex $z$, since $\{v_{xy}\}$ alone would give the separating set $\{x, y\}$ of $G$. Then $\{x, y, z\}$ separates $G$.

Among all edges $xy$ and such vertices $z$, choose them so that $G - \{x, y, z\}$ has a component $C$ with as few vertices as possible. The vertex $z$ has a neighbour $v$ in $C$. By assumption $G / zv$ is not 3-connected either, so as above there is a vertex $w$ such that $\{z, v, w\}$ separates $G$, and each of $z, v, w$ has a neighbour in every component of $G - \{z, v, w\}$. Since $x$ and $y$ are adjacent, they lie in at most one component of $G - \{z, v, w\}$ together with possibly $w$; so there is a component $D$ that contains neither $x$ nor $y$. The vertex $v$ has a neighbour $d \in D$. Since $d \notin \{x, y, z\}$ and $d$ is adjacent to $v \in C$, $d$ lies in $C$. The subgraph $D$ is connected and avoids $x, y, z$, so $D \subseteq C$. And $v \in C \setminus D$, so $|D| < |C|$, which contradicts the choice of $C$, with the edge $zv$ and the vertex $w$. $\square$

## Two facts about drawings

We use two standard facts about plane graphs.

**(F1)** In a 2-connected plane graph, every face is bounded by a cycle of the graph (Diestel, Proposition 4.2.6). The region bounded by a cycle is homeomorphic to an open disk with the cycle as its boundary circle, by the Jordan-Schönflies theorem (Mohar and Thomassen, Section 2.1). So a new vertex placed in a face bounded by a cycle $C$ can be joined to any set of vertices of $C$ by arcs inside the face that meet only at the new vertex.

**(F2)** For each face $f$ of a plane graph, there is a drawing of the same graph with the same faces in which $f$ is the outer face (project the drawing onto the sphere and back from a point inside $f$). So for each edge $e$ there is a drawing with $e$ on the boundary of the outer face. If $G = G_1 \cup G_2$ with $V(G_1) \cap V(G_2) \subseteq \{x, y\}$, and if $G_1 + xy$ and $G_2 + xy$ are planar (or $G_1$, $G_2$ are planar and share at most one vertex $x$), then $G$ is planar: draw both parts with $xy$ (or $x$) on the outer face, put the drawing of the second part inside a face of the first next to $xy$ (or at $x$), and delete $xy$ if it is not an edge of $G$ (Diestel, Section 4.4).

## The main proof

Suppose the theorem is false, and let $G$ be a non-planar graph that contains no $TK_5$ and no $TK_{3,3}$, with $|V(G)| + |E(G)|$ as small as possible. Then $G$ has no isolated vertex, and every graph with a smaller value of $|V| + |E|$ and no $TK_5$, $TK_{3,3}$ is planar. Graphs with at most 4 vertices are planar (they are subgraphs of $K_4$), so $|V(G)| \ge 5$.

**$G$ is 2-connected.** Otherwise $G = G_1 \cup G_2$ for proper subgraphs $G_1, G_2$ that share at most one vertex, with no edge between $G_1 - G_2$ and $G_2 - G_1$, each with a vertex outside the other. Each $G_i$ has a smaller value of $|V| + |E|$ and no $TK_5$ or $TK_{3,3}$, so it is planar, and $G$ is planar by (F2). This is a contradiction.

**$G$ is 3-connected.** Suppose that $\{x, y\}$ separates $G$. Write $G = G_1 \cup G_2$ with $V(G_1) \cap V(G_2) = \{x, y\}$, each $G_i$ with a vertex outside $\{x, y\}$, and no edge between $G_1 - \{x, y\}$ and $G_2 - \{x, y\}$; put the edge $xy$, if it exists, into $G_1$. Let $H_i = G_i + xy$. Each component of $G - \{x, y\}$ inside $G_{3-i}$ has a neighbour at $x$ and one at $y$, since $G$ is 2-connected; so $G_{3-i}$ contains an $x$-$y$ path $P_{3-i}$ whose inner vertices lie outside $G_i$. The graph $H_i$ has fewer vertices than $G$ and at most one edge that $G$ lacks, while $G_{3-i}$ has at least two edges not in $G_i$; so $|V(H_i)| + |E(H_i)| < |V(G)| + |E(G)|$. If $H_i$ contained a $TK_5$ or $TK_{3,3}$, then replacing the edge $xy$ in it, if it is used, by $P_{3-i}$ would give one in $G$. So $H_1$ and $H_2$ are planar, and $G$ is planar by (F2), a contradiction. So $G$ is 3-connected, and $G \ne K_4$ since $|V(G)| \ge 5$.

**The contraction.** By Lemma 3, $G$ has an edge $xy$ with $G' = G / xy$ 3-connected. Let $v$ be the vertex of $G'$ that replaces $x$ and $y$. Since $G$ contains no $TK_5$ or $TK_{3,3}$, it has no $K_5$ or $K_{3,3}$ minor (by Lemma 2), so neither has its minor $G'$, so $G'$ contains no $TK_5$ or $TK_{3,3}$. It is smaller than $G$, so it is planar. Fix a drawing of $G'$.

The graph $G' - v$ is 2-connected, so by (F1) the face $f$ of $G' - v$ that contains the point of $v$ is bounded by a cycle $C$. The edges at $v$ run inside $f$, so all neighbours of $v$ lie on $C$. Let $X = N_G(x) \setminus \{y\}$ and $Y = N_G(y) \setminus \{x\}$. Both are subsets of $N_{G'}(v) \subseteq V(C)$, and $|X| \ge 2$, $|Y| \ge 2$ since $G$ is 3-connected. Let $x_1, \ldots, x_k$ be the vertices of $X$ in their cyclic order on $C$, and let $P_i$ be the path on $C$ from $x_i$ to $x_{i+1}$ that contains no other vertex of $X$ (indices mod $k$).

*Case 1: $Y \subseteq V(P_i)$ for some $i$.* Erase the edges at $v$ that do not go to $X$, and rename $v$ as $x$; the arcs from $x$ to $X$ divide $f$ into regions, and the region $R$ between the arcs to $x_i$ and $x_{i+1}$ is bounded by the cycle $x\, x_i\, P_i\, x_{i+1}\, x$. Put $y$ inside $R$ and join it to $x$ and to each vertex of $Y$ by arcs in $R$, which is possible by (F1). The result is a drawing of $G$, a contradiction.

*Case 2: $|X \cap Y| \ge 3$.* Let $a, b, c \in X \cap Y$. Split $C$ into three disjoint paths, each containing exactly one of $a, b, c$; they are connected and pairwise joined by edges of $C$. With $\{x\}$ and $\{y\}$, these are five branch sets of a $K_5$ model in $G$: $x$ and $y$ are adjacent, and both are adjacent to $a, b, c$. So $G$ has a $K_5$ minor and contains $TK_5$ or $TK_{3,3}$ by Lemma 2, a contradiction.

*Case 3: otherwise.* We find $y_1, y_2 \in Y$ and $x_i, x_j \in X$, four different vertices that alternate around $C$. If some $y_1 \in Y$ is not in $X$, it lies inside a unique path $P_i$, between $x_i$ and $x_{i+1}$. Since Case 1 fails, some $y_2 \in Y$ lies outside $V(P_i)$, and then $y_1, x_{i+1}, y_2, x_i$ alternate around $C$ (also when $k = 2$). If instead $Y \subseteq X$, then $|Y| \le 2$ because Case 2 fails, so $Y = \{x_a, x_b\}$ with $|Y| = 2$; since Case 1 fails, $x_a$ and $x_b$ are not consecutive in the cyclic order of $X$, so each of the two arcs of $C$ between them contains a vertex of $X$, say $x_c$ and $x_d$, and $x_a, x_c, x_b, x_d$ alternate. In both cases the four arcs of $C$ between consecutive vertices of $y_1, x_i, y_2, x_j$ (in this cyclic order), the edges $x x_i$, $x x_j$, $y y_1$, $y y_2$ and $xy$ form a $TK_{3,3}$ with sides $\{x, y_1, y_2\}$ and $\{y, x_i, x_j\}$: $x$ reaches $y$, $x_i$, $x_j$ by edges, and each of $y_1$, $y_2$ reaches $y$ by an edge and $x_i$, $x_j$ along $C$. This is a contradiction.

All cases are contradictory, so no counterexample exists. $\blacksquare$
