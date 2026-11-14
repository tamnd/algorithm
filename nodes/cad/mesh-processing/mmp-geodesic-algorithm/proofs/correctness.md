---
title: In exact arithmetic the window method returns the geodesic distance at every vertex, because every value is the length of a real path, a window chain along each shortest path survives the trimming, and pseudo-source vertices start with their final distance
proves: [correctness, termination]
status: full
---

**Setup.** The mesh is a connected manifold triangle mesh, possibly with border, and every face has positive area. $d(x)$ is the geodesic distance from the nearest source to a point $x$ of the surface. $\hat d(v)$ is the value that the algorithm holds for a vertex $v$, which only goes down. The arithmetic is exact and the tolerances are 0. A window $w$ on edge $e$ has the value $w(x) = \sigma + |(x, 0) - s|$ at the points $x$ of its interval. A *pseudo-source vertex* is a source, a border vertex, or a vertex with angle sum at least $2\pi$.

Two facts about shortest paths are used, both from the structure lemmas of Mitchell, Mount and Papadimitriou.

- **(F1)** A shortest path exists. It is straight in each face, and where it crosses the inside of an edge, it is straight in the unfolding of the two faces. So it does not bend at a point that is not a vertex.
- **(F2)** If a shortest path passes through a vertex $v$ that is not one of its ends, then $v$ is a border vertex or its angle sum is at least $2\pi$. *Reason:* the path cuts the faces around an inner vertex $v$ into two sides. If one side had an angle below $\pi$, a short cut on that side would make the path shorter. So both sides are at least $\pi$.

**Lemma 1 (soundness).** Every window value $w(x)$ and every value given to $\hat d$ is the length of a path on the surface from a source to that point. So $\hat d(v) \ge d(v)$, and $w(x) \ge d(x)$.

*Proof.* By induction in the order of creation. At a source, $\hat d = 0$. A window made by line L3 at the vertex $v$ in the face $g = (v, a, b)$ has $s$ at the image of $v$ and $\sigma = \hat d(v)$. For $x$ on $ab$, the segment from $v$ to $x$ lies in $g$, and its length is $|(x, 0) - s|$, because the frame is an isometric copy of $g$. Add a path of length $\hat d(v)$ to $v$, which exists by induction. A child window of $w$ in line L4 holds a point $X$ of the edge $pr$ or $rq$ only if the ray from $s$ to $X$ meets the edge $pq$ at a point $(g, 0)$ with $b_0 \le g \le b_1$. The segment from $(g, 0)$ to $X$ lies in the face $h$, which is convex. So the path of $w$ to $(g, 0)$ followed by this segment has length $\sigma + |s - (g, 0)| + |(g, 0) - X| = \sigma + |s - X|$, as the three points are on one line. This is the value of the child at $X$, written in the frame of the new edge. The values given to the third vertex $r$ and to the end points of a new window are values of windows at those points. Trimming only makes intervals smaller. $\square$

**Lemma 2 (keys never go down).** Every event that is pushed while an event of key $k$ is processed has a key at least $k$. So the keys are taken in an order that never goes down.

*Proof.* A child of $w$ has, at each of its points $X$, the value $\sigma + |s - X| \ge \sigma + |s - (g, 0)| = w(g) \ge \operatorname{key}(w)$. A window made at a vertex $v$ has all its values at least $\sigma = \hat d(v) = k$. A trimmed piece has a key at least that of the whole window. A vertex event is pushed with a value of one of these windows, or of $w$ itself at the third vertex, so it is at least $k$ too. $\square$

So once a vertex event with key $\hat d(v)$ is taken, $\hat d(v)$ does not change again, and the windows that $v$ starts in line L3 use its final value.

**Lemma 3 (trimming).** In line L5 a part of a window is removed only where another window that stays alive at that moment has a value at most as large. On each piece between two roots of the quadratic, the sign of the difference of the two distance functions does not change, so the test at the middle of the piece is right for the whole piece.

*Proof.* The new window loses a piece where an existing window is at most as good. An existing window loses a piece where the new window is strictly better, and that piece of the new window is kept at this step. For the second claim, $\sigma_1 + \sqrt{A(x)} = \sigma_2 + \sqrt{B(x)}$ with $A, B$ the squared distances to the two pseudo-sources implies, after squaring twice, the quadratic of the code, so every point where the two values are equal is a root, or the quadratic is identically 0. In the first case the difference is continuous with no zero inside a piece. In the second case the two windows have equal values on the whole overlap and the existing one is kept. $\square$

**Theorem 1 (completeness).** At the end, $\hat d(t) = d(t)$ for every vertex $t$.

*Proof.* Fix $t$ and a shortest path $\gamma$ from the nearest source $v_0$ to $t$. Cut $\gamma$ at each vertex it passes through. By (F2) these vertices $v_1, \dots, v_k$ are pseudo-source vertices, and each piece goes from $v_i$ to the next vertex $z$ without touching any other vertex. We show by induction on $i$ that $\hat d(v_i) = d(v_i)$ at the end and that $v_i$ starts its windows with $\sigma = d(v_i)$.

*Start of a pseudo-source.* If $\hat d(v_i) = d(v_i)$ at the end, then the vertex event pushed when $\hat d(v_i)$ took this value is taken later. At that time $\hat d(v_i) = d(v_i)$, because it cannot go lower by Lemma 1, and $v_i$ has not started yet, because a start at an earlier, larger value would be followed by a drop, which Lemma 2 forbids. So $v_i$ starts with $\sigma = d(v_i)$.

*One piece.* Let the piece from $u = v_i$ to $z$ cross the edges $e_1, \dots, e_m$ at inner points $x_1, \dots, x_m$, passing from face $h_{j-1}$ into face $h_j$ at $x_j$, with $h_0 \ni u$ and $h_m \ni z$. Call a window *good for $j$* if it lies on $e_j$, looks into $h_j$, holds $x_j$, has the value $d(x_j)$ there, and its pseudo-source lies on the line of $\gamma$ behind $x_j$ in the unfolding. Such a window carries $\gamma$ through $x_j$.

If $m = 0$, then $z$ is a vertex of a face $(u, a, b)$, and the window that $u$ puts on $ab$ in line L3, or the direct update for a border edge, sets $\hat d(z) \le d(u) + |uz| = d(z)$. Otherwise the window that $u$ puts on $e_1$, the far edge of $h_0$, is good for 1, since $x_1$ is inside $e_1$ and $\sigma = d(u)$.

A good window stays good where it holds $x_j$, and if trimming removes $x_j$ from it, another good window holds $x_j$. By Lemma 3, a good window loses $x_j$ only to a window $y$ with $y(x_j) \le d(x_j)$, so $y(x_j) = d(x_j)$ by Lemma 1. The path of $y$ to $x_j$ followed by the rest of $\gamma$ is then a shortest path to $z$. By (F1) it does not bend at $x_j$, so $y$ arrives along the line of $\gamma$ from the side of $h_{j-1}$, and $y$ is good for $j$. A good window cannot lose $x_j$ to a strictly better window, since nothing is below $d(x_j)$. So from the time the first good window for $j$ is made, some alive window is good for $j$. When the queue is empty, every alive window has been taken, so some good window $w$ for $j$ is taken in line L4.

When $w$ is taken, the ray through $x_j$ crosses $h_j$ straight. It does not pass through the third vertex $r$ of $h_j$, because $\gamma$ touches no vertex there. If $j < m$, it leaves $h_j$ at $x_{j+1}$, inside $e_{j+1}$. The part of $[b_0, b_1]$ on the same side of $g_r$ as $x_j$ has positive length, because $x_j \ne g_r$ and $w$ has positive length, so the child on $e_{j+1}$ is made and holds $x_{j+1}$, with the value $d(x_j) + |x_j x_{j+1}| = d(x_{j+1})$. It is good for $j + 1$. It is not skipped as grazing, because $\gamma$ crosses $e_{j+1}$ and does not run along it. If $j = m$, the ray reaches $z$, which is then the third vertex of $h_m$ (it cannot be an end of $e_m$, as the segment would run along $e_m$), and line L4 sets $\hat d(z) \le d(x_m) + |x_m z| = d(z)$.

So $\hat d(z) \le d(z)$, and with Lemma 1, $\hat d(z) = d(z)$. Applying this to the pieces in turn gives the claim for every $v_i$ and finally for $t$. $\square$

**Theorem 2 (termination).** The loop stops.

*Proof.* Let $D$ be the largest distance $d$ of a point on an edge, which is finite. The proof of Theorem 1 also works when $z$ is any point of an edge, so every edge point $x$ is held by a good window from the time its parent, of key at most $d(x)$, is taken. Once the key of the taken events is above $D$, every new window has all its values above $D$, so at each of its points an alive window is strictly better, and line L5 removes all of it. So no window with a key above $D$ is ever pushed after that, and vertex events above $D$ are stale. Each window with a key at most $D$ belongs to a pseudo-source vertex and the sequence of faces that its rays cross within length $D$. A straight segment of bounded length that avoids the vertices crosses a bounded number of faces, so there are finitely many such sequences, and each trimming step splits a window into at most three pieces per comparison. So finitely many windows are pushed, and each is taken once. $\square$

**What is not proved here.** The bounds of $O(n)$ windows per edge and $O(n^2 \log n)$ time are those of Mitchell, Mount and Papadimitriou for their data structures, and they are cited, not proved for this code. The code uses floating point with a relative tolerance of $10^{-10}$, so its exactness is checked by the tests, not proved: against an exhaustive search over unfoldings on convex polyhedra, exact visibility on an L-shape, Euclidean distance on flat grids, symmetry, and Steiner-point upper bounds on terrains.
