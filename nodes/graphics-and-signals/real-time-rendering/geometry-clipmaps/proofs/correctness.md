---
title: The clipmap windows nest, the rings and the zero-area triangles form a surface without cracks, and the toroidal update gives the same arrays as a fresh fill
proves: [correctness]
status: full
---

We use the notation of the page. Domain points are integer pairs in units of the finest grid. Level $l$ has $n \times n$ vertices with the spacing $s_l = 2^l$, so its window has the side $(n - 1) s_l$. For the viewer $v$, line L1 sets the origin $o_l$ (the lower corner of the window) to the multiple of $s_{l+1}$ nearest to $v - (n - 1) s_l / 2$, per coordinate. The levels are $0, \ldots, L - 1$, and $h$ is the height of a domain point. The arithmetic is exact.

## The windows nest

**Lemma 1.** If $(n - 1)/4 > 3/2$, then for each $l \ge 1$ the window of level $l - 1$ lies strictly inside the window of level $l$, its corners are vertices of level $l$, and on each side the ring between them is at least $(n - 1)/4 - 3/2$ cells of level $l$ wide.

*Proof.* Per coordinate, $|o_l - (v - (n - 1) s_l / 2)| \le s_{l+1}/2 = s_l$ and $|o_{l-1} - (v - (n - 1) s_{l-1} / 2)| \le s_{l-1} = s_l / 2$. So

$$o_{l-1} - o_l \ge \frac{(n - 1)(s_l - s_{l-1})}{2} - s_l - \frac{s_l}{2} = s_l \left(\frac{n - 1}{4} - \frac{3}{2}\right).$$

The upper sides differ by $(o_l + (n - 1) s_l) - (o_{l-1} + (n - 1) s_{l-1}) = (n - 1) s_l / 2 - (o_{l-1} - o_l)$, and the same two bounds give $o_{l-1} - o_l \le s_l ((n - 1)/4 + 3/2)$, so this gap has the same lower bound. The origin $o_{l-1}$ is a multiple of $s_l$, and the side of the fine window is $(n - 1) s_{l-1}$, an even multiple of $s_{l-1}$ because $n$ is odd, so all four corners of the fine window are vertices of level $l$. $\square$

For $n = 15$ the bound is 2 cells, and for the $n = 255$ of Asirvatham and Hoppe it is 62. The test of the code asserts the strict nesting.

Because the corners of the fine window are vertices of level $l$, each cell of level $l$ lies inside the fine window or meets it only on its boundary. Line L5 keeps the cells of the second kind: the ring.

## The mesh tiles the domain

**Lemma 2.** The triangles of line L5 for all levels tile the window of level $L - 1$: the triangles have disjoint interiors and their union is the window.

*Proof.* By induction on $l$. Level 0 has all its cells, so its triangles tile its window. The ring of level $l$ is the set of cells of the window of level $l$ that are not in the window of level $l - 1$, so by the remark after Lemma 1 the ring and the window of level $l - 1$ tile the window of level $l$. $\square$

## No cracks

Lines L5 and L6 output triangles in the counterclockwise order of the domain. Two triangles are *paired* along an edge when one has it as the directed edge $p \to q$ and the other as $q \to p$.

**Lemma 3.** Every directed edge of the mesh, with the zero-area triangles of line L6, is paired with exactly one other edge, except the edges on the border of the window of level $L - 1$.

*Proof.* Inside one level, an edge between two cells or across a diagonal is used once in each direction by the two counterclockwise triangles that share it. The only other edges are on the border of a window of level $l - 1 < L - 1$. Take a cell edge of level $l$ on this border, from $a$ to $b$ in the counterclockwise order around the fine window, and let $o$ be its midpoint, which is a vertex of level $l - 1$. The ring of level $l$ lies outside the fine window, so its counterclockwise triangle traverses this edge as $b \to a$. The fine triangles lie inside, so they traverse the two half edges as $a \to o$ and $o \to b$. Line L6 adds the triangle $(a, b, o)$ with the directed edges $a \to b$, $b \to o$ and $o \to a$. These are paired with $b \to a$, $o \to b$ and $a \to o$, in this order. $\square$

So, as a set of triangles over the domain, the mesh is closed except on its outer border. A T-junction, where the vertex $o$ of the fine level lies inside the coarse edge $a b$, is closed by a triangle of zero area. It remains to show that the heights make this triangle flat in space, so that no gap shows.

**Theorem 4.** Let $w \le (n - 1)/4 - 3/2$, with $w > 0$. With the heights of line L7, (a) a domain point that is a vertex of two levels has the same height in both, and (b) the three corners of each triangle of line L6 are collinear in space. So the surface has no cracks.

*Proof.* Line L7 gives a vertex $p$ of level $l < L - 1$ the height $(1 - \alpha) h(p) + \alpha (h(a) + h(c))/2$, where $a$ and $c$ are the ends of the edge of level $l + 1$ through $p$ (`coarse_parents`), and $a = c = p$ when $p$ is a vertex of level $l + 1$. The factor $\alpha$ is 1 on the border of the window of level $l$ and 0 at $w$ or more cells of level $l$ from it. The coarsest level keeps $h$.

(a) A vertex $p$ of level $l$ that is also a vertex of level $l + 1$ has $a = c = p$, so its height at level $l$ is $h(p)$ for every $\alpha$. At level $l + 1$, a domain point that is shared with level $l$ and is drawn by a ring triangle of level $l + 1$ lies on the border of the window of level $l$. By Lemma 1 it is at least $(n - 1)/4 - 3/2 \ge w$ cells of level $l + 1$ from the border of its own window, so $\alpha = 0$ there and its height is $h(p)$ as well. (Vertices of level $l + 1$ that lie strictly inside the window of level $l$ are not used by any triangle.)

(b) A triangle of line L6 has the corners $a$ and $b$ of level $l$, with the height $h$ by (a), and the midpoint $o$ of level $l - 1$ on the border of the window of level $l - 1$. There $\alpha = 1$, and the edge of level $l$ through $o$ is $a b$ itself, so $o$ has the height $(h(a) + h(b))/2$. The point $(o, (h(a) + h(b))/2)$ is the midpoint of the segment between $(a, h(a))$ and $(b, h(b))$. $\square$

The condition of the theorem holds for the transition width $w = n/10$ of Asirvatham and Hoppe when $n \ge 15$: $n/10 \le (n - 1)/4 - 3/2$ is $n \ge 35/3$. The width $n/10$ itself is a tuning. Over the transition region the height of each vertex is affine in $\alpha$, and $\alpha$ is continuous in the position of the viewer except where the origin moves, so the morph removes the jumps that a level switch would make inside the region; the proof that the surface does not jump when the origin moves is not given here, and the page only tests the static mesh.

## The toroidal update

**Proposition 5.** The array index $(\lfloor p_x / s_l \rfloor \bmod n, \lfloor p_y / s_l \rfloor \bmod n)$ is one to one on the vertices of a window of level $l$. After MOVE (lines L2 to L4) the array equals the array of a fresh fill of the new window, and the move writes exactly the vertices of the new window that are not in the old one.

*Proof.* The vertices of a window have $p_x / s_l$ in $n$ consecutive integers, and these have $n$ distinct residues mod $n$; the same holds for $p_y$. So the index is one to one on a window. The index depends only on $p$, so a vertex in both windows keeps its slot and its stored value $h(p)$. Line L3 writes $h(p)$ into the slot of each new vertex, and line L4 sets the origin. So each vertex $p$ of the new window has $h(p)$ in its slot, as in a fresh fill. Lines L2 and L3 write only when $p$ is not in the old window. $\square$

So a move of the origin by $s_{l+1} = 2 s_l$ along one axis, the smallest move that line L1 makes, writes $2n$ samples, and a move by $(d_x, d_y)$ cells writes $n^2 - (n - |d_x|)(n - |d_y|)$ samples when $|d_x|, |d_y| \le n$.
