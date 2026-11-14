---
title: BUILD computes the opposite corners, and SWING walks once around the fan of a vertex
proves: [correctness, termination]
status: full
---

**Setup.** The input is a list of $m$ triangles, each with three distinct vertices. Corner $c = 3t + k$ is corner $k$ of triangle $t$, with $V[c] = T[t][k]$, $\mathrm{next}(c) = 3\lfloor c/3 \rfloor + (c + 1) \bmod 3$ and $\mathrm{prev}(c) = \mathrm{next}(\mathrm{next}(c))$. The *edge of* $c$ is the directed edge $\epsilon(c) = (V[\mathrm{next}(c)], V[\mathrm{prev}(c)])$, the side of its triangle that does not touch $c$, in the direction of the triangle. Each directed side of each triangle is $\epsilon(c)$ for exactly one corner $c$ of that triangle.

**Claim 1.** If BUILD does not fail, then for each corner $c$, $O[c]$ is the corner $d$ with $\epsilon(d) = \mathrm{rev}(\epsilon(c))$, the reverse edge, if such a $d$ exists, and $-1$ if not. BUILD fails exactly when some directed edge is the edge of two corners.

*Proof.* Lines L3 to L6 insert the key $\epsilon(c)$ for each corner. Line L5 fails if the key is already there, that is, if two corners have the same directed edge. Otherwise $H$ maps each directed edge that occurs to the one corner that has it. Line L8 looks up the reverse $(V[\mathrm{prev}(c)], V[\mathrm{next}(c)])$ of $\epsilon(c)$, and line L9 stores the answer or $-1$. $\square$

*Consequence.* $O$ is an involution on the corners with $O[c] \ne -1$: if $\epsilon(d) = \mathrm{rev}(\epsilon(c))$, then $\epsilon(c) = \mathrm{rev}(\epsilon(d))$, so $O[d] = c$. Also $O[c] \ne c$ and $O[c]$ is in another triangle, because a triangle with three distinct vertices does not use one edge in both directions. If a mesh is consistently oriented and each edge has one or two triangles, then each inner edge is used once in each direction, so BUILD does not fail, and $O[c] = -1$ exactly for the corners whose edge is a border edge. An edge with three or more triangles has two uses in the same direction, so BUILD fails on it.

**Claim 2.** Let $c$ be a corner of vertex $v$ in the triangle $(v, a, b)$, so $V[\mathrm{next}(c)] = a$ and $V[\mathrm{prev}(c)] = b$. If the edge $\{v, b\}$ has a second triangle, then SWING$(c)$ is the corner of $v$ in that triangle. If not, SWING$(c) = -1$.

*Proof.* The edge of $\mathrm{next}(c)$ is $(V[\mathrm{prev}(c)], V[c]) = (b, v)$. By claim 1, $d = O[\mathrm{next}(c)]$ (line L12) is the corner whose edge is $(v, b)$, which is in the other triangle of the edge $\{v, b\}$, or $-1$ if there is none. Since $\epsilon(d) = (V[\mathrm{next}(d)], V[\mathrm{prev}(d)]) = (v, b)$, the corner $\mathrm{next}(d)$ has the vertex $v$. $\square$

In the same way UNSWING$(c) = \mathrm{prev}(O[\mathrm{prev}(c)])$ is the corner of $v$ in the other triangle of the edge $\{v, a\}$. The two maps are inverse to each other where both are defined: the triangle after $(v, a, b)$ across $\{v, b\}$ has $b$ as the vertex after $v$, so its UNSWING goes back across $\{v, b\}$.

**Claim 3.** RING$(c)$ (lines L13 and L14) returns each corner of the fan of $V[c]$ that contains $c$ exactly once, in the order of SWING, and stops.

*Proof.* Consider the graph on the corners of $v$ with an edge from $x$ to SWING$(x)$. By claim 2 each step crosses one edge $\{v, w\}$ into the other triangle at that edge, so the connected component of $c$ is exactly the fan of $c$: the triangles at $v$ that are joined to the triangle of $c$ through edges at $v$. SWING and UNSWING are inverse partial maps, so each corner has at most one successor and at most one predecessor, and the component is a single path or a single cycle. Line L13 walks back with UNSWING. On a cycle it comes back to $c$ and starts there. On a path it stops at the first corner, the one with no predecessor. The walk cannot repeat a corner of a path, because the predecessor is unique, so it stops after at most the number of corners in the fan. Line L14 then walks forward with SWING from the start until it reaches $-1$ (the end of the path) or the start again (the cycle is closed). It outputs each corner of the component once. $\square$

**Termination.** BUILD has two loops over the $3m$ corners. RING does at most two passes over one fan. So every operation stops. $\blacksquare$
