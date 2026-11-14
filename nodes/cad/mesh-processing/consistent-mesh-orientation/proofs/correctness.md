---
title: The breadth-first flip propagation finds a consistent orientation exactly when one exists, and the volume sign makes a closed component face outward
proves: [correctness, termination]
status: full
---

**Setup.** The input is a mesh whose faces each have at least 3 distinct vertices and whose edges each have one or two faces. For an edge $e = \{u, v\}$ with $u < v$ and a face $f$ that contains it, let $d_f(e) = +1$ if $f$ goes along $e$ from $u$ to $v$, and $-1$ if it goes from $v$ to $u$. A *flip vector* gives each face a bit $s_f \in \{0, 1\}$; the face is reversed when $s_f = 1$, and its direction along $e$ becomes $(-1)^{s_f} d_f(e)$. A flip vector is *consistent* if the two faces $f, g$ of each inner edge $e$ then go along $e$ in opposite directions. Let $\lambda(e) = 1$ if $d_f(e) = d_g(e)$ and $\lambda(e) = 0$ if not. Then the condition for $e$ is

$$(-1)^{s_f} d_f(e) \ne (-1)^{s_g} d_g(e) \iff s_f \oplus s_g = \lambda(e). \tag{1}$$

Let $G$ be the *dual graph*: one node for each face and one edge for each inner edge of the mesh, labelled $\lambda(e)$. A *component* is a connected component of $G$.

**Claim 1.** For each component $K$, the loop of lines L4 to L10 sets $s_g$ for every face $g$ of $K$ and for no other face. It reports a conflict (line L10) if and only if $K$ has no consistent flip vector. If there is no conflict, the bits it sets are consistent on $K$, and the only other consistent vector on $K$ is the complement.

*Proof.* Lines L5 to L9 are a [breadth-first search](/breadth-first-search/) of $G$ from $r$: line L7 visits each inner edge of $f$ and its other face $g$, and line L9 adds $g$ the first time it is reached. So the search reaches exactly the faces of $K$. Each face $g \ne r$ gets its bit at line L9 from its parent $f$ in the search tree, with $s_g = s_f \oplus \lambda(e)$ by line L8. So the bits satisfy (1) on every edge of the search tree.

Every edge of $G$ inside $K$ is checked by line L8 when its first end leaves the queue. If it is a tree edge, the check passes. If it is not, line L10 compares the bit already set with the bit that (1) asks for.

*No conflict implies consistent.* If no check fails, (1) holds on every edge of $K$, so the bits are a consistent vector on $K$.

*Conflict implies no consistent vector.* Suppose the check of an edge $e = \{f, g\}$ fails, and let $t$ be any vector that satisfies (1) on all edges of $K$. On the tree, (1) fixes $t$ from $t_r$: by induction along the tree path, $t_x = t_r \oplus s_x$ for every face $x$ of $K$, because both $t$ and $s$ change by $\lambda$ along each tree edge. Then $t_f \oplus t_g = s_f \oplus s_g \ne \lambda(e)$, so $t$ breaks (1) on $e$. So $K$ has no consistent vector.

*Uniqueness.* The same induction shows that a consistent vector on $K$ is $s$ when $t_r = 0$ and the complement of $s$ when $t_r = 1$. Both are consistent, because complementing all bits does not change $s_f \oplus s_g$. $\square$

Equivalently, $K$ is orientable if and only if every cycle of $G$ in $K$ has an even sum of labels, the parity condition of a two-coloring.

**Claim 2.** Let $K$ be a closed, orientable component with exact coordinates, oriented by the bits $s$, and let $W = \sum \det(p_a, p_b, p_c)$ over the triangles $(a, b, c)$ of the fan triangulation of each face (line L12). Then $W$ does not depend on the choice of the fan, it changes sign when all faces of $K$ are reversed, and if the faces of $K$ bound a region $R$ in space without self-intersection, $W = 6\,\mathrm{vol}(R)$ when the normals by the right-hand rule point out of $R$, and $W = -6\,\mathrm{vol}(R)$ when they point in.

*Proof.* Reversing a face reverses each of its fan triangles, which swaps two arguments of each determinant, so every term changes sign. For a triangle $(a, b, c)$, $\det(p_a, p_b, p_c) / 6$ is the signed volume of the tetrahedron $(0, p_a, p_b, p_c)$, which is $\frac{1}{3} \int_{\triangle} x \cdot n \, dA$ for the unit normal $n$ of the right-hand rule: the field $x \cdot n$ is constant on the plane of the triangle and equals the height of the tetrahedron over it. A planar face is cut into triangles with the same normal, and the integral is additive, so the sum over any fan triangulation is $\frac{1}{3} \int_{\partial R} x \cdot n \, dA$. By the divergence theorem with the field $x / 3$, whose divergence is 1, this is $\mathrm{vol}(R)$ when $n$ is the outward normal, and $-\mathrm{vol}(R)$ when it is the inward one. $\square$

So, for such a component, line L13 flips all faces of $K$ when $W < 0$, and after it the normals point out. By claim 1, the flip keeps the orientation consistent, because the complement of a consistent vector is consistent. The arithmetic is exact, so the sign of $W$ is the true sign.

**Termination.** Each face enters the queue once, at line L4 or line L9, and each face has finitely many edges, so the search does $O(c)$ steps for $c$ corners in total. The volume sum and the final flip take $O(c)$ steps. $\blacksquare$
