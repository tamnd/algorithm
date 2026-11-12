---
title: Quartet-guided insertion rebuilds a binary tree from its tree metric
proves: [correctness]
status: full
---

**Setting.** $T$ is an unrooted binary tree (internal vertices of degree 3) with leaf set $X = \{1, \ldots, n\}$, $n \ge 3$, and positive edge lengths; $D$ is its leaf metric, and $d$ is the path length between any two vertices of $T$. For a set $S \subseteq X$ with $|S| \ge 3$, let $\mathrm{span}(S)$ be the smallest subtree of $T$ that contains $S$, and let $T|_S$ be $\mathrm{span}(S)$ with each vertex of degree 2 suppressed (its two edges joined into one, with the lengths added). We prove that after the leaves $1, \ldots, x - 1$ are inserted, the program holds $T|_{\{1, \ldots, x-1\}}$ with the right edge lengths, and that each stored representative $\mathrm{rep}(v, u)$ is a leaf on the side of $u$ when the edge $\{v, u\}$ is removed. For $x - 1 = n$ this is $T$ itself.

**Fact 1 (median).** For three leaves $p, q, s$ the three paths between them meet in one vertex $m$, and $d(p, m) = \frac{1}{2}\big(D_{pq} + D_{ps} - D_{qs}\big)$. *Proof.* Let $m$ be the vertex of $P_{qs}$ closest to $p$. The path from $p$ to $m$ meets $P_{qs}$ only at $m$, so $P_{pq}$ and $P_{ps}$ both run through $m$, and $D_{pq} + D_{ps} - D_{qs} = 2 d(p, m)$. $\square$

**Base.** For $S = \{1, 2, 3\}$, $T|_S$ is a star whose center is the median $m$ of the three leaves, and by Fact 1 the edge to leaf $i$ has the length of line L1. The representatives of line L1 are leaves on the right sides.

**Lemma 1 (where the new leaf attaches).** Let $|S| \ge 3$ and $x \notin S$. Let $a$ be the vertex where the path from $x$ to $\mathrm{span}(S)$ first meets $\mathrm{span}(S)$. Then $a$ has degree 2 in $\mathrm{span}(S)$, so it lies inside exactly one edge of $T|_S$, at positive distance from both ends. The tree $T|_{S \cup \{x\}}$ is $T|_S$ with that edge subdivided at $a$ and a new edge from $a$ to $x$ of length $d(x, a)$.

*Proof.* If $a$ were a leaf $s \in S$, the path from $x$ would enter $s$ through the only neighbor of $s$, which lies on $\mathrm{span}(S)$ because $|S| \ge 2$; that neighbor would be met first. If $a$ had degree 3 in $\mathrm{span}(S)$, it would have degree at least 4 in $T$, with the extra edge towards $x$. Both are impossible, so $a$ has degree 2 in $\mathrm{span}(S)$. The span of $S \cup \{x\}$ is $\mathrm{span}(S)$ plus the path from $a$ to $x$, and suppressing degree-2 vertices gives the stated tree. Edge lengths are positive, so $a$ is at positive distance from both ends of its edge. $\square$

**Lemma 2 (one quartet test).** Let $v$ be an internal vertex of $T|_S$ with neighbors $u_1, u_2, u_3$ in $T|_S$, and let $r_i \in S$ be a leaf on the side of $u_i$. Suppose $a$ lies on the side of $u_1$: inside the edge $\{v, u_1\}$ or in the part of $T|_S$ beyond $u_1$. Let $s_i = D_{x r_i} + D_{r_j r_k}$ for $\{i, j, k\} = \{1, 2, 3\}$. Then $s_1 < s_2 = s_3$.

*Proof.* In $T$, both $P_{v r_1}$ and $P_{v a}$ start with the first edge $e$ of the path in $T$ that the edge $\{v, u_1\}$ of $T|_S$ stands for. Let $q$ be the last common vertex of $P_{v r_1}$ and $P_{v x}$ (which runs through $a$). Then $q \ne v$, so $d(v, q) > 0$. The paths from $v$ to $r_2$ and to $r_3$ leave $v$ through edges other than $e$, so they meet $P_{vx}$ and $P_{v r_1}$ only at $v$. So the following concatenations have no repeated vertex and are the paths of $T$:
$$D_{x r_1} = d(x, q) + d(q, r_1), \quad D_{x r_t} = d(x, q) + d(q, v) + d(v, r_t), \quad D_{r_1 r_t} = d(r_1, q) + d(q, v) + d(v, r_t)$$
for $t = 2, 3$, and $D_{r_2 r_3} = d(r_2, v) + d(v, r_3)$. Substituting,
$$s_1 = d(x, q) + d(q, r_1) + d(v, r_2) + d(v, r_3), \qquad s_2 = s_3 = s_1 + 2\, d(q, v). \qquad \square$$

So the strict minimum in line L6 names the side that holds $a$. Ties do not occur on a tree metric.

**Lemma 3 (the walk).** The loop of lines L4 to L8 stops after at most $|S| - 2$ passes, at the edge $\{v, w\}$ of $T|_S$ that contains $a$.

*Proof.* We show: at the start of every pass after the first, $a$ lies on the side of $v$ as seen from $\mathit{from}$, that is, inside the edge $\{\mathit{from}, v\}$ or beyond $v$. Line L8 moves from $v$ to $u_i$ only when Lemma 2 puts $a$ on the side of $u_i$, so the claim holds at the next pass. At a pass, Lemma 2 gives the side $i$ of $v$ that holds $a$ ($a \ne v$ by Lemma 1).

- If $u_i = \mathit{from}$, then $a$ is on the side of $\mathit{from}$ seen from $v$ and on the side of $v$ seen from $\mathit{from}$. These two sets meet only inside the edge $\{v, \mathit{from}\}$.
- If $u_i$ is a leaf, the side of $u_i$ is the inside of the edge $\{v, u_i\}$ and the leaf itself, and $a$ is not a leaf.

In both cases line L7 stops at the right edge. The walk never returns along the edge it came by, and in a tree such a walk never visits a vertex twice; it visits only internal vertices, and $T|_S$ has $|S| - 2$ of them. $\square$

**Lemma 4 (the new edges).** Let the loop stop at the edge $\{v, w\}$ with $b = r_i$ on the side of $w$, and $r_j, r_k$ on the other two sides of $v$. Then line L10 gives $t_v = d(r_j, v)$ and $t_p = d(r_j, a)$, so line L11 gives the edge from $v$ to $a$ the length $d(v, a) = t_p - t_v$, the edge from $a$ to $w$ the length $d(a, w)$, and the edge from $a$ to $x$ the length $d(x, a)$.

*Proof.* The three paths between $r_j$, $b$ and $r_k$ all pass through $v$, so $v$ is their median, and Fact 1 gives $t_v$. The path from $r_j$ to $b$ runs through $v$, then along the edge $\{v, w\}$, so it contains $a$; the path from $x$ to it first meets it at $a$, so $a$ is the median of $r_j, b, x$, and Fact 1 gives $t_p$ and the length $d(x, a) = \frac{1}{2}(D_{x r_j} + D_{x b} - D_{r_j b})$. Along the path from $r_j$, $v$ comes before $a$, so $d(v, a) = t_p - t_v$, and the rest of the old edge is $d(a, w)$. $\square$

**Lemma 5 (representatives).** After line L11 each stored representative is still a leaf on the right side. *Proof.* Removing the edge $\{v, p\}$ leaves on the side of $p$ the old side of $w$ plus $x$, so the old $\mathrm{rep}(v, w)$ is still valid for $(v, p)$; the same holds for $(w, p)$ with the old $\mathrm{rep}(w, v)$. The side of $w$ seen from $p$ is the old side of $w$ seen from $v$, and the side of $v$ seen from $p$ is the old side of $v$ seen from $w$. The side of $x$ seen from $p$ is $\{x\}$, and the side of $p$ seen from $x$ contains every old leaf, among them $b$. For every other directed edge, the side gains $x$ or stays the same, so its old representative stays valid. $\square$

**Theorem.** On the leaf metric of a binary tree with positive edge lengths, the method returns that tree with its edge lengths.

*Proof.* By induction on the number of inserted leaves. The base gives $T|_{\{1,2,3\}}$. If the program holds $T|_S$ with valid representatives, Lemmas 2 and 3 find the edge that contains the attachment point $a$ of the next leaf $x$, Lemma 4 subdivides it at $a$ with the right lengths and attaches $x$ with the right length, and Lemma 5 keeps the representatives valid; by Lemma 1 the result is $T|_{S \cup \{x\}}$. After the last leaf, $T|_X = T$, because $T$ has no vertices of degree 2. $\blacksquare$
