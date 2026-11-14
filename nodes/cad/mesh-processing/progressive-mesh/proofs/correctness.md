---
title: A legal edge collapse keeps the Euler characteristic and is undone exactly by its vertex split, so every level of a progressive mesh is rebuilt exactly
proves: [correctness, termination]
status: full
---

**Setting.** $M$ is an oriented manifold mesh of triangles with stable vertex and face ids, faces oriented by the right-hand rule. For a vertex $v$ let $N_v$ be the map $a \mapsto b$ over the faces $(v, a, b)$ of $v$, written with $v$ first in their cyclic order. Being an oriented manifold mesh means: every directed edge is in at most one face, so $N_v$ is a function and is one to one; no face repeats a vertex; and for each $v$ the arcs $a \to N_v(a)$ form one cycle (an inner vertex) or one path (a boundary vertex). The *start* of a path is the vertex that is a key but not a value, and its *end* is the value that is not a key. ECOL, VSPLIT and LINK are lines L1 to L13 of the page. A collapse of $v_s v_t$ is *legal* if line L2 does not fail: the edge exists, $v_l \ne v_r$, and the link condition holds.

**Claim.**

1. A legal collapse leaves no face with a repeated vertex and no two faces on the same three vertices, and it keeps $V - E + F$.
2. Let $T$ be the set of faces of $v_t$ other than $f_l$ and $f_r$ before a legal collapse. After the collapse, the walk of line L8 visits exactly the faces of $T$.
3. VSPLIT applied right after the ECOL that returned the record restores the mesh exactly. Hence if $s_0, \dots, s_{m-1}$ are the records of BUILD in refinement order, applying $s_0, \dots, s_{k-1}$ to $M^0$ gives the mesh $M^k$ that BUILD had after $m - k$ collapses, for every $k$.
4. ECOL, VSPLIT and BUILD terminate.

**Facts from the link condition.** In a manifold mesh the vertices of the link of $v$ are the neighbours of $v$, plus $\omega$ when $v$ is on the boundary, and its edges are the pairs $\{a, N_v(a)\}$, plus $\{a, \omega\}$ for each boundary edge $va$. The link of the edge $v_s v_t$ has the vertices $v_l$ and $v_r$ that exist, plus $\omega$ if the edge is on the boundary, and no edges. So the link condition says:

- (a) the common neighbours of $v_s$ and $v_t$ are exactly the vertices $v_l$, $v_r$ that exist;
- (b) no edge $\{x, y\}$ is in a face of $v_s$ and in a face of $v_t$ opposite to them, and no boundary edge $v_s x$ goes with a boundary edge $v_t x$;
- (c) if $v_s v_t$ is an inner edge, $v_s$ and $v_t$ are not both on the boundary, since then $\omega$ would be a common link vertex that is not in the link of the edge.

**Proof of 1.** A face that contains both $v_s$ and $v_t$ contains the edge $v_s v_t$ in one direction, and each direction is in at most one face, so these faces are $f_l$ and $f_r$, which line L4 removes. So the faces of $T$ do not contain $v_s$, and renaming $v_t$ to $v_s$ in them, in line L5, makes no face with a repeated vertex. Suppose a face $(v_s, x, y)$ of $T$ after the renaming has the same vertex set as another face. That face is not in $T$ (two faces of $T$ with the same vertices would have been equal before), so it is an old face $\{v_s, x, y\}$ of $v_s$. Then the edge $\{x, y\}$ is opposite $v_s$ and opposite $v_t$, which (b) forbids.

Counting: one vertex goes away. An edge $v_t x$ with $x \ne v_s$ becomes $v_s x$, and it merges with an old edge exactly when $x$ is a common neighbour, which by (a) is $v_l$ or $v_r$. So the edges lost are $v_s v_t$ and one per face among $f_l$, $f_r$, and the faces lost are $f_l$ and $f_r$. Inside the surface the change of $V - E + F$ is $-1 + 3 - 2 = 0$, and on a boundary edge it is $-1 + 2 - 1 = 0$. $\square$

**Proof of 2.** Write $N_t$ and $N_s$ for the maps before the collapse. Since $f_l = (v_s, v_t, v_l)$ and $f_r = (v_t, v_s, v_r)$, the map $N_t$ has the arcs $v_l \to v_s$ (from $f_l$) and $v_s \to v_r$ (from $f_r$), and $N_s$ has the arcs $v_r \to v_t$ and $v_t \to v_l$. Let $A_t$ be $N_t$ without its arcs from $f_l$ and $f_r$; its arcs are the faces of $T$. Let $A_s$ be $N_s$ without the arcs from $f_l$ and $f_r$. After the collapse the map $N'$ of $v_s$ has the arcs of $A_s$ and of $A_t$, since the renamed faces of $T$ have $v_s$ in the place of $v_t$ and contain neither $v_s$ nor $v_t$ otherwise (proof of 1).

*The keys of $A_s$ and $A_t$ are disjoint.* A common key is a common neighbour, so it is $v_l$ or $v_r$ by (a). In $N_t$ the key $v_l$ belongs to the arc $v_l \to v_s$, which is not in $A_t$, and $N_t$ has one arc per key, so $v_l$ is not a key of $A_t$. In $N_s$ the key $v_r$ belongs to $v_r \to v_t$, so $v_r$ is not a key of $A_s$. In the same way the values are disjoint. So $N'$ is a function, and the walk of line L8 is well defined.

*Case 1: both faces exist, $v_t$ inner.* $N_t$ is the cycle $\dots \to v_l \to v_s \to v_r \to \dots$, so $A_t$ is a path from $v_r$ to $v_l$. The walk starts at $v_r$, follows $A_t$, since $v_r$ is a key of $A_t$ only, and the path never meets $v_l$ before its last vertex. It stops at $v_l$ after the faces of $A_t$, which are $T$.

*Case 2: both faces exist, $v_t$ on the boundary.* By (c), $v_s$ is inner, so $A_s$ is a path from $v_l$ to $v_r$. $N_t$ is a path that contains $v_l \to v_s \to v_r$, so $A_t$ is two paths, $Q_1$ from $v_r$ to the end of $N_t$ and $Q_2$ from the start of $N_t$ to $v_l$, either of which may have no arcs. Then $N'$ is the single path $Q_2$, $A_s$, $Q_1$. The walk goes from $v_r$ along $Q_1$ to the end of $N'$, where the vertex is not a key, jumps to the start of $N'$, which is the start of $Q_2$ (or $v_l$ if $Q_2$ is empty), and follows $Q_2$ to $v_l$. It visits $Q_1 \cup Q_2 = T$ and nothing of $A_s$.

*Case 3: $f_r$ is missing.* Then $v_t \to v_s$ is a boundary edge, and both ends are on the boundary. The arc $v_l \to v_s$ is the last arc of the path $N_t$ and $v_t \to v_l$ is the first arc of $N_s$, so $A_t$ is a path from the start of $N_t$ to $v_l$ and $A_s$ a path from $v_l$ to the end of $N_s$. $N'$ is the path $A_t$, $A_s$. It is not a cycle: the start of $N_t$ and the end of $N_s$ are neighbours of $v_t$ and $v_s$; if they were equal, this vertex would be a common neighbour other than $v_l$, against (a), or both paths would be empty and the link edge $\{v_l, \omega\}$ would be common, against (b). The walk starts at the start of $N'$ and stops at $v_l$, after exactly the arcs of $A_t$.

*Case 4: $f_l$ is missing.* This is case 3 with the directions reversed: $A_s$ is a path from the start of $N_s$ to $v_r$ and $A_t$ a path from $v_r$ to the end of $N_t$. The walk starts at $v_r$ and stops at the end of $N'$, after exactly the arcs of $A_t$. $\square$

**Proof of 3.** Line L3 stores the old positions and the ids and corner tuples of $f_l$ and $f_r$. Lines L4 to L6 change only $f_l$, $f_r$, the faces of $T$, the position of $v_s$ and the vertex $v_t$. By claim 2, line L9 renames $v_s$ to $v_t$ in exactly the faces of $T$, at the same place in each tuple where line L5 renamed $v_t$ to $v_s$, and these tuples contained no $v_s$ before, so they get back their old tuples. Line L10 restores both positions, and line L11 puts $f_l$ and $f_r$ back with their old ids and tuples. No other entry was changed by either operation, so the mesh is equal to the one before the collapse, entry by entry, and the stars, which are computed from the faces, are equal as well.

For the levels, BUILD makes meshes $M = K_0, K_1, \dots, K_m$ by collapses $c_1, \dots, c_m$, and returns $M^0 = K_m$ and $s_j$ = the record of $c_{m-j}$. By induction on $k$, applying $s_0, \dots, s_{k-1}$ to $K_m$ gives $K_{m-k}$: for $k = 0$ it is $K_m$, and if the first $k$ splits gave $K_{m-k}$, then $s_k$ is the record of $c_{m-k}$, which turned $K_{m-k-1}$ into $K_{m-k}$, so $s_k$ applied right after it gives $K_{m-k-1}$ by the first part. So $M^k = K_{m-k}$, and $M^m = M$. $\square$

**Proof of 4.** ECOL and LINK do a fixed amount of work for each face of $v_s$ and $v_t$. Each step of the walk of line L8 visits a new arc of $N'$ (the arcs form a cycle or a path and the walk stops at $v_l$ or at the end, and jumps to the start at most once), so it takes at most as many steps as $v_s$ has faces. Each round of BUILD either removes one vertex or stops, so it runs at most $V$ rounds. $\square$

The link condition also keeps the mesh a manifold of the same topological type; this is the theorem of Dey, Edelsbrunner, Guha and Nekhayev, cited and not proved here. Claims 1 to 4 give what the page states: legal collapses keep $V - E + F$, and the stored splits rebuild every level and the input exactly. $\blacksquare$
