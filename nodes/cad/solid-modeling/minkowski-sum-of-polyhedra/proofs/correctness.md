---
title: The candidate normals and support faces give exactly the facets of the Minkowski sum of two convex polytopes
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $P$ and $Q$ are convex polytopes in $\mathbb{R}^3$ with nonempty interior, given by finite point sets with integer coordinates. For $u \neq 0$, $h_K(u) = \max_{x \in K} u \cdot x$ and $F(K, u) = \{x \in K : u \cdot x = h_K(u)\}$. Every face of a polytope is $F(K, u)$ for some $u$, and its dimension is the dimension of its affine hull. For a finite set $S$ we write $F(S, u)$ for the points of $S$ that attain the maximum; then $\operatorname{conv} F(S, u) = F(\operatorname{conv} S, u)$, since a linear function attains its maximum over a polytope on the hull of the points of $S$ where it is maximal.

**Lemma 1 (support functions and faces add).** For nonempty compact convex sets $K$ and $L$ and every $u \neq 0$: $h_{K \oplus L}(u) = h_K(u) + h_L(u)$ and $F(K \oplus L, u) = F(K, u) \oplus F(L, u)$.

*Proof.* For $x \in K$ and $y \in L$, $u \cdot (x + y) = u \cdot x + u \cdot y \le h_K(u) + h_L(u)$, with equality when $x$ and $y$ attain their maxima, so $h_{K \oplus L}(u) = h_K(u) + h_L(u)$. A point $z \in K \oplus L$ attains this value exactly when some, and then every, decomposition $z = x + y$ with $x \in K, y \in L$ has $u \cdot x + u \cdot y = h_K(u) + h_L(u)$. Since each term is at most its maximum, both are equal to their maxima, so $x \in F(K, u)$ and $y \in F(L, u)$. Conversely, the sum of two such points attains the maximum. $\square$

**Lemma 2 (the dimension of a sum).** For nonempty convex sets $A$ and $B$, $\dim (A \oplus B) = \dim(\operatorname{lin}(A - A) + \operatorname{lin}(B - B))$, where $\operatorname{lin}(A - A)$ is the linear space parallel to the affine hull of $A$.

*Proof.* The affine hull of $A \oplus B$ is $\operatorname{aff} A + \operatorname{aff} B$, a translate of $\operatorname{lin}(A - A) + \operatorname{lin}(B - B)$. $\square$

**Lemma 3 (edges from adjacent facets).** Let $u_1$ and $u_2$ be the outer normals of two facets $G_1$ and $G_2$ of $P$ that share an edge $g$. Then $F(P, u_1 + u_2) = g$. Every edge of $P$ arises this way from some pair of facet normals.

*Proof.* For $x \in P$, $(u_1 + u_2) \cdot x \le h_P(u_1) + h_P(u_2)$, with equality exactly when $x \in G_1 \cap G_2$. The bound is attained, since $g \subseteq G_1 \cap G_2$ is not empty, so $F(P, u_1 + u_2) = G_1 \cap G_2$. Two distinct facets of a 3-polytope meet in a face of dimension at most 1, and here it contains $g$, so it is $g$. Every edge of a 3-polytope lies in exactly two facets. $\square$

So the edge directions of line L2, found as the faces $F(P, u_1 + u_2)$ of dimension 1 over all pairs of facet normals, are exactly the directions of the edges of $P$, and likewise for $Q$. A pair of facets that are not adjacent gives a vertex or nothing new, since its face $F(P, u_1 + u_2)$ is a vertex or an edge in that case, and an edge found this way is still an edge of $P$.

**Lemma 4 (the normal of a facet).** A facet $G$ of a polytope $K$ with nonempty interior has exactly one outer normal up to a positive factor: the $u$ with $F(K, u) = G$ form the open ray of the outer normal of the plane of $G$.

*Proof.* If $F(K, u) = G$, then $u$ is perpendicular to the plane of $G$, since $u \cdot x$ is constant on $G$ and $G$ spans the plane, and $u$ points away from $K$, since $K$ lies in $\{u \cdot x \le h_K(u)\}$ and has points off the plane. $\square$

**Theorem.** MINKOWSKI-SUM-CONVEX returns a map whose keys are exactly the primitive outer normals of the facets of $P \oplus Q$, and whose value at $u$ is the vertex cycle of the facet $F(P \oplus Q, u)$.

*Proof.* (Soundness.) Let $u \in N$ pass line L7. By Lemma 1, applied to the hulls, and the remark on finite sets, $\operatorname{conv}\{a + b : a \in A, b \in B\} = F(P, u) \oplus F(Q, u) = F(P \oplus Q, u)$. This face spans a plane, so it is a facet, and line L8 stores the plane hull of the points, which is the facet. By Lemma 4 the facet has only the normal $u$ up to scaling, so no facet is stored twice under two keys.

(Completeness.) Let $G$ be a facet of $P \oplus Q$ with primitive outer normal $u$, and let $A' = F(P, u)$ and $B' = F(Q, u)$, so $G = A' \oplus B'$ by Lemma 1. By Lemma 2 the spaces of $A'$ and $B'$ add to a plane. If $A'$ is a facet of $P$, then by Lemma 4 $u$ is its primitive outer normal, which line L1 put in $N$. The same holds if $B'$ is a facet of $Q$. Otherwise $\dim A' \le 1$ and $\dim B' \le 1$, and their spaces add to dimension 2 only if both are edges, with directions $e$ and $f$ that are not parallel. By Lemma 3 these directions are found in line L2. The vector $u$ is perpendicular to $e$ and to $f$, since $u \cdot x$ is constant on each face, so $u$ is a nonzero multiple of $e \times f$. Both primitive vectors on that line are added in line L3, so $u \in N$. Line L7 accepts $u$, since $A \oplus B$ spans the plane of $G$ by the soundness part.

(The cycle.) The plane hull in line L8 projects the points onto the coordinate plane that drops the coordinate where $|u_k|$ is largest. This projection is a bijection on the plane of the facet, since $u_k \neq 0$, and it keeps or reverses orientation by the sign of $u_k$, reversed once more for the middle axis since $(x, z)$ is a left-handed pair. The monotone chain gives the vertices of the projected hull in counterclockwise order, and the code reverses the list when the orientation is reversed, so the cycle is counterclockwise seen from the side $u$ points to.

(Termination.) $N$ is finite, at most $F_P + F_Q + 2 E_P E_Q$ vectors, and each step of lines L5 to L8 does finitely many integer operations. $\square$

**Corollary (the vertices).** The vertices of $P \oplus Q$ are the points that occur in the facet cycles. Each vertex $v$ of the sum is $F(P \oplus Q, u)$ for some $u$, and a face of a 3-polytope that is a vertex lies in at least three facets, so it occurs in their cycles; conversely every point of a facet cycle is a vertex of that facet, so a vertex of the sum.

**Corollary (the size).** The sum has at most $F_P + F_Q + 2 E_P E_Q$ facets, which is $O(nm)$ for summands with $n$ and $m$ vertices, since a 3-polytope with $n$ vertices has at most $3n - 6$ edges and $2n - 4$ facets. By Euler's formula, the numbers of vertices and edges of the sum are also $O(nm)$.
