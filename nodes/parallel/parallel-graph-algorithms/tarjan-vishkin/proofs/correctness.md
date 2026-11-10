---
title: The Tarjan-Vishkin rules label each edge with its biconnected component
proves: [correctness]
status: full
---

**Setting.** $G$ is a simple undirected graph. After line L2, $T$ is a tree on $V \cup \{z\}$ rooted at $z$, made of a spanning forest of $G$ and one edge from $z$ to a root of each tree of the forest. The proof assumes that lines L3 to L6 give the parent $p$, the preorder numbers $pre$, the descendant counts $nd$, and $low$ and $high$ as defined on the page; that these steps compute them is the Euler tour technique and is not proved here. A tree edge is named by its lower end. For a nontree edge $e = \{x, y\}$, the fundamental cycle $C_e$ is $e$ together with the tree path from $x$ to $y$; it is a simple cycle. Edge sets are treated as vectors over $\{0,1\}$, and $\oplus$ is the symmetric difference.

The proof uses one standard fact, not proved here: the relation "$e = f$, or $e$ and $f$ lie on a common simple cycle" is an equivalence relation on $E$, and its classes are the blocks.

**Lemma 1 (subtrees are ranges).** The descendants of $v$ are exactly the vertices $u$ with $pre(v) \le pre(u) < pre(v) + nd(v)$. So $u$ is a proper ancestor of $w$ only if $pre(u) < pre(w)$, and if $pre(v) < pre(w)$ and $w$ is not a descendant of $v$, then $pre(v) + nd(v) \le pre(w)$.

*Proof.* Preorder numbers a vertex, then the subtree of each child in turn, so the subtree of $v$ gets the $nd(v)$ consecutive numbers from $pre(v)$ on. The two other claims follow. $\square$

**Lemma 2 (the test of rule 2).** Let $v = p(w)$. Then $low(w) < pre(v)$ or $high(w) \ge pre(v) + nd(v)$ if and only if some nontree edge $\{x, y\}$ has $x$ in the subtree of $w$ and $y$ outside the subtree of $v$.

*Proof.* $low(w)$ and $high(w)$ are the least and the largest of the numbers $pre(x)$ and $pre(y)$ over the descendants $x$ of $w$ and the nontree edges $\{x, y\}$. The numbers $pre(x)$ lie in the range of $w$, which is inside the range of $v$. So the least or the largest number is outside the range of $v$ if and only if some $pre(y)$ is, and by Lemma 1 that is the case if and only if $y$ is not a descendant of $v$. $\square$

**Lemma 3 (joins stay on fundamental cycles).** Each join of rule 1 or rule 2, and each assignment of rule 3, puts together two edges of $G$ that lie on one fundamental cycle. No join involves an edge at $z$.

*Proof.* A tree path between two vertices of one tree of the forest stays in that tree and does not pass through $z$, so no fundamental cycle holds an edge at $z$.

*Rule 1.* The nontree edge $\{v, w\}$ has $pre(v) < pre(w)$ and $pre(v) + nd(v) \le pre(w)$, so neither end is a descendant of the other, by Lemma 1. Their lowest common ancestor is a proper ancestor of both, so the tree path from $v$ to $w$ uses $\{p(v), v\}$ and $\{p(w), w\}$, and both lie on $C_{\{v,w\}}$.

*Rule 2.* By Lemma 2 there is a nontree edge $\{x, y\}$ with $x$ below $w$ and $y$ outside the subtree of $v$. The lowest common ancestor of $x$ and $y$ is then a proper ancestor of $v$, so the tree path from $x$ to $y$ climbs from $x$ through $w$, $v$ and $p(v)$. It uses $\{v, w\}$ and $\{p(v), v\}$. Since $y$ is in the tree of $x$, $v$ is not the root of its tree, so $\{p(v), v\}$ is an edge of $G$.

*Rule 3.* For a nontree edge $\{v, w\}$ with $pre(v) < pre(w)$, the vertex $w$ is not an ancestor of $v$, by Lemma 1. So the lowest common ancestor is a proper ancestor of $w$, and the tree path from $w$ to $v$ starts with $\{p(w), w\}$. $\square$

**Lemma 4 (a fundamental cycle gets one label).** For every nontree edge $e$, all edges of $C_e$ get the same label.

*Proof.* Let $e = \{x, y\}$ with $pre(y) < pre(x)$, and let $a$ be the lowest common ancestor. The tree path is $x = x_0, x_1, \ldots, x_s = a$ upward from $x$, and $y = y_0, \ldots, y_t = a$ upward from $y$, with $s \ge 1$; $t = 0$ when $y = a$. Take two consecutive tree edges on the $x$ side, $\{x_{i+1}, x_i\}$ and $\{x_{i+2}, x_{i+1}\}$ with $i + 2 \le s$. Put $w = x_i$ and $v = x_{i+1} = p(w)$. Then $x$ is below $w$, and $y$ is not below $v$, because $v$ is a proper descendant of $a$ on the branch of $x$, and $y$ is either $a$ or on another branch. So rule 2 joins $w$ and $v$ by Lemma 2. Hence all tree edges on the $x$ side are joined; the same holds on the $y$ side. If $t \ge 1$, neither of $x$ and $y$ is a descendant of the other, and rule 1 joins $\{p(y), y\}$ and $\{p(x), x\}$, one edge from each side. So all tree edges of $C_e$ are in one component of $G'$, and rule 3 gives $e$ the label of $x$, the end with the larger number, whose tree edge is on $C_e$. $\square$

**Lemma 5 (cycles are chains of fundamental cycles).** Let $C$ be a simple cycle of $G$ and $N$ the set of its nontree edges. Then $C = \bigoplus_{e \in N} C_e$, and the graph $H$ on $N$ that joins $e$ and $f$ when $C_e$ and $C_f$ share an edge is connected.

*Proof.* Let $D = C \oplus \bigoplus_{e \in N} C_e$. Every vertex has even degree in a cycle, and the degree of a vertex in a symmetric difference has the parity of the sum of its degrees, so every vertex has even degree in $D$. A nontree edge $e \in N$ lies in $C$ and in $C_e$ and in no other $C_f$, so it is not in $D$; a nontree edge outside $N$ is in none of the sets. So $D$ holds only tree edges. A nonempty edge set of a forest has a vertex of degree 1, so $D$ is empty, and $C = \bigoplus_{e \in N} C_e$. $N$ is not empty, because $T$ has no cycle.

Suppose $H$ is not connected, and split $N$ into two nonempty parts $A$ and $B$ with no edge of $H$ between them. Put $X = \bigoplus_{e \in A} C_e$ and $Y = \bigoplus_{f \in B} C_f$. $X$ lies in the union of the cycles of $A$ and $Y$ in the union of the cycles of $B$, and these unions share no edge, so $C = X \oplus Y$ is the disjoint union of $X$ and $Y$. $X$ holds every edge of $A$ and $Y$ every edge of $B$, so both are nonempty proper subsets of $C$. Walking around $C$, some edge of $X$ is followed by an edge not in $X$; their common vertex has degree 1 in $X$. But every vertex has even degree in $X$, by the parity argument above. This is a contradiction. $\square$

**Theorem.** Two edges of $G$ get the same label if and only if they are in the same block.

*Proof.* Let $e \ne f$ be in the same block. By the standard fact there is a simple cycle $C$ through both. By Lemma 5, every edge of $C$ lies in some $C_g$ with $g \in N$, so $e \in C_g$ and $f \in C_h$ for some $g, h \in N$, and a path $g = g_0, g_1, \ldots, g_k = h$ in $H$ gives fundamental cycles in which neighbours share an edge. By Lemma 4 each of them has one label, and neighbours share an edge, so they all have the same label, and so do $e$ and $f$.

Conversely, let $e$ and $f$ get the same label. Then each is a tree edge or is assigned by rule 3 to a tree edge, and the tree edges are joined in $G'$ by a path of joins from rules 1 and 2. By Lemma 3, every step of this chain puts together two edges on one simple cycle, so they are in the same block, and by transitivity of the relation, $e$ and $f$ are in the same block. The edges at $z$ are joined to nothing, by Lemma 3, and line L11 drops them. $\blacksquare$
