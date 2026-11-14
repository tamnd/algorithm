---
title: Each phase of isotropic remeshing stops, the split phase leaves every edge at most 4L/3, the collapse guard keeps this bound, the flip phase ends at a local optimum of the valence excess, and the mesh keeps its topology and border
proves: [correctness, termination]
status: full
---

**Setup.** The input is an oriented manifold triangle mesh, possibly with border, in which every face has positive area. $L > 0$ is the target length, $\mathrm{high} = \frac{4}{3}L$ and $\mathrm{low} = \frac{4}{5}L$. A vertex is a border vertex if it lies on a border edge, an edge with only one face. The valence $\operatorname{val}(v)$ is the number of neighbours of $v$, and the valence excess is $E = \sum_v |\operatorname{val}(v) - t(v)|$ with $t(v) = 4$ on the border and $6$ inside. The claims are about the combinatorics of the operators and the exact geometry of the midpoints. The floating-point length tests only decide which operator runs, and do not change the arguments.

**Lemma 1 (a split keeps the surface and the topology).** Splitting the edge $uv$ at its midpoint $m$ gives a manifold mesh with the same oriented surface, the same border curve and the same Euler characteristic.

*Proof.* Each face $(a, b, w)$ that contains the directed edge $a \to b$, with $\{a, b\} = \{u, v\}$, is replaced by $(a, m, w)$ and $(m, b, w)$. Since $m$ lies on the segment $ab$, these two triangles lie in the plane of the old one, keep its orientation, and cover it with no overlap, so the surface and the area do not change. Every other face is untouched. The star of $m$ is a disk (two faces from each old face, joined along $mw$), or a half-disk if $uv$ was a border edge, and the stars of $u$, $v$ and the opposite vertices only replace one edge by another. For an inner edge, $V$ grows by 1, $E$ by 3 (the halves $um$, $mv$ and two spokes) and $F$ by 2. For a border edge, $V$ grows by 1, $E$ by 2 and $F$ by 1. In both cases $V - E + F$ is the same. The border curve is the same point set, because a border edge $uv$ becomes the border edges $um$ and $mv$. $\square$

**Lemma 2 (longest-first splits are longest-side bisections).** In line L2, every split cuts each of its one or two faces through a longest side of that face.

*Proof.* The heap holds every edge longer than $\mathrm{high}$, with stale entries skipped, and a split pushes every new edge longer than $\mathrm{high}$. So the popped edge is a longest edge of the whole mesh, and so a longest side of each face that contains it. $\square$

**Theorem 1 (the split phase stops and bounds the edges).** Line L2 makes finitely many splits, and when it stops every edge has length at most $\frac{4}{3}L$.

*Proof.* Let $\alpha > 0$ be the smallest angle of the mesh when line L2 starts, and $\beta = \alpha/2$. Every face made in line L2 comes from a face $T$ of the starting mesh by repeated bisection through a longest side (Lemma 2). By the theorem of Rosenberg and Stenger, every triangle made in this way from $T$ has all its angles at least half the smallest angle of $T$, so at least $\beta$. Their argument allows either side when two sides are equally long.

Take a face that is split. Its longest side has length $\ell > \frac{4}{3}L$. Let $A, B$ be the angles at the ends of that side and $h$ the height of the opposite vertex above it. Both $A$ and $B$ are at most the third angle, so they are acute, and the foot of the height splits the side into parts $x$ and $\ell - x$ with $h = x\tan A = (\ell - x)\tan B$. So $h = \ell\,\frac{\tan A \tan B}{\tan A + \tan B}$. The function $\frac{ab}{a + b}$ grows in each of $a, b > 0$, and $\tan A, \tan B \ge \tan\beta$, so $h \ge \frac{\ell}{2}\tan\beta$ and the area is at least $a_0 = \frac{1}{4}\ell^2\tan\beta > \frac{4}{9}L^2\tan\beta$.

A bisection halves the area. So a face made by $j$ bisections from $T$ has area $\operatorname{area}(T)/2^j$, and it can be split only if $\operatorname{area}(T)/2^j \ge a_0$, that is, $j \le \log_2(\operatorname{area}(T)/a_0)$. Each split bisects one or two faces, and each face is bisected at most once, because the face disappears. So the number of splits is at most the number of faces ever made at a depth $j$ that can be split, which is finite. When the heap is empty, no edge is longer than $\mathrm{high}$. $\square$

**Lemma 3 (a safe collapse keeps the manifold and the topology).** If $uv$ is an inner edge with faces $(u, v, c)$ and $(v, u, d)$, neither $u$ nor $v$ is a border vertex, and the link condition $N(u) \cap N(v) = \{c, d\}$ holds, then merging $v$ into $u$ gives an oriented manifold mesh with the same Euler characteristic and the same border.

*Proof.* The two faces of $uv$ vanish, and every other face of $v$ gets $u$ in place of $v$. Since $u$ and $v$ are inner vertices, their stars are disks, with link cycles $c, v, d, \ldots$ around $u$ and $d, u, c, \ldots$ around $v$. The new link of $u$ is the first cycle with $v$ removed, joined at $c$ and $d$ to the second cycle with $u$ removed. The link condition says that these two paths share only $c$ and $d$, so the join is a single simple cycle, and the new star of $u$ is a disk. A vertex $w \notin \{u, v, c, d\}$ in the link of $v$ is not a neighbour of $u$, so its link changes only by the name $v \to u$ and stays a cycle. The vertices $c$ and $d$ each lose one neighbour ($v$ merges into $u$) and keep a link cycle of length $\operatorname{val} - 1 \ge 3$, because the guard asks $\operatorname{val}(c), \operatorname{val}(d) \ge 4$. No directed edge is used twice: a repeated directed edge would need a common neighbour of $u$ and $v$ other than $c$ and $d$. The faces keep their vertex order, so the orientation stays. The counts change by $V - 1$, $E - 3$ (the edge $uv$, and $vc$, $vd$ merge into $uc$, $ud$) and $F - 2$, so $V - E + F$ is the same. No border vertex is involved, so the border does not change. This is the inner case of the result of Dey, Edelsbrunner, Guha and Nekhayev on topology-preserving edge contraction. $\square$

**Theorem 2 (the collapse phase stops and keeps the bound).** Line L3 makes fewer than $V$ collapses, where $V$ is the vertex count at its start. If every edge is at most $\mathrm{high}$ at the start, this still holds at the end.

*Proof.* Each collapse removes one vertex and adds none, and a mesh with faces keeps at least 3 vertices, so there are fewer than $V$ collapses. Each sweep over the edges either collapses one or ends the loop. The new edges of a collapse are the edges from the midpoint $p$ to the old neighbours of $u$ and $v$, and the guard refuses the collapse if one of them is longer than $\mathrm{high}$. All other edges keep their length. $\square$

**Lemma 4 (a flip keeps the topology and changes four valences).** Flipping a legal inner edge $uv$ with faces $(u, v, c)$ and $(v, u, d)$ into $(u, d, c)$ and $(d, v, c)$ gives an oriented manifold mesh with the same $V$, $E$ and $F$, the same border, and new valences $\operatorname{val}(u) - 1$, $\operatorname{val}(v) - 1$, $\operatorname{val}(c) + 1$, $\operatorname{val}(d) + 1$, all others unchanged.

*Proof.* The legality test asks $c \ne d$ and that $cd$ is not an edge, so the new edge $cd$ is new and no directed edge is used twice. The four outer edges $uc$, $cv$, $vd$, $du$ keep one face each on the same side. The edge $uv$ leaves and $cd$ comes in, so the counts stay. $u$ and $v$ keep valence at least 3, because the test asks at least 4 before the flip. Border status depends only on border edges, which flips do not touch, so the targets $t$ do not change. $\square$

**Theorem 3 (the flip phase stops at a local optimum).** Line L4 makes at most $E_0$ flips, where $E_0$ is the valence excess at its start. When it stops, no legal flip lowers the excess.

*Proof.* A flip is made only if it lowers $\sum_{w \in \{u, v, c, d\}} |\operatorname{val}(w) - t(w)|$. By Lemma 4 no other term of $E$ changes, so $E$ drops by this positive integer, at least 1. Since $E \ge 0$, there are at most $E_0$ flips. The loop ends after a sweep with no flip, and in that sweep every edge was tested, so no legal flip lowers $E$. $\square$

**Theorem 4 (topology and border are kept).** The output is an oriented manifold mesh with the Euler characteristic and the border curve of the input, and every vertex of the input border that was there at the start is still in place.

*Proof.* Lines L2, L3 and L4 keep both by Lemmas 1, 3 and 4. Line L5 moves only inner vertices, and does not change the faces. Border vertices are never moved, never collapsed, and border edges are only split at their midpoints, so the border curve is the same point set in every round. $\square$

**Termination.** Each round stops by Theorems 1, 2 and 3, and line L5 is one pass over the vertices, so the $k$ rounds stop.

**What is not proved here.** The upper bound of Theorem 1 holds after line L3, but flips and the relaxation of line L5 can make edges longer than $\frac{4}{3}L$ again, and edges shorter than $\frac{4}{5}L$ remain where no collapse is safe. Line L5 can also, in principle, move a vertex so far that a face turns over. That the final edge lengths, angles and valences are close to the targets, and that the faces stay oriented, is measured in the tests and the examples, not proved. Theorem 1 uses exact midpoints, and the Rosenberg and Stenger bound gives no useful count of the splits beyond finiteness.
