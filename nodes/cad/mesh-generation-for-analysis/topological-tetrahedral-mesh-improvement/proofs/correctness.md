---
title: The 2-3 and 3-2 flips keep the volume and the validity of a tetrahedral mesh, and hill climbing with them stops
proves: [correctness, termination]
status: full
---

**Notation.** $[p_0 p_1 p_2 p_3]$ is $\mathrm{orient3d}(p_0, p_1, p_2, p_3)$, six times the signed volume. A tetrahedral mesh is valid if every tetrahedron has $[\cdot] > 0$ in its stored order, the interiors are pairwise disjoint, and every face is shared by at most two tetrahedra. A face in one tetrahedron only is a boundary face. Two meshes of the same region with the same boundary faces can replace each other inside a larger mesh, and the result is again conforming.

**Lemma 1 (five points).** For any points $p_0, \dots, p_4$ in space, $\sum_{i=0}^{4} (-1)^i\,[p_0 \cdots \widehat{p_i} \cdots p_4] = 0$, where the hat means that $p_i$ is left out.

*Proof.* $[q_0 q_1 q_2 q_3]$ is, up to one fixed sign, the $4 \times 4$ determinant with rows $(1, q_j)$. Form the $5 \times 5$ matrix with rows $(1, p_i, 1)$. Its first and last columns are equal, so its determinant is zero. Expanding along the last column gives the alternating sum of the five $4 \times 4$ minors, which is the claim. $\square$

**Lemma 2 (the crossing test).** Let $d$ and $e$ lie strictly on opposite sides of the plane of the triangle $abc$, and let $p$ be the point where the segment $de$ meets that plane. Then $[a b d e]$, $[b c d e]$ and $[c a d e]$ have one strict sign if and only if $p$ is in the interior of the triangle $abc$.

*Proof.* Write $p = (1 - s)d + s e$ with $0 < s < 1$. The function $x \mapsto [a b d x]$ is affine and zero at $x = d$, so $[a b d p] = s\,[a b d e]$. The function $x \mapsto [a b x d]$ is affine and zero on the line $ab$, so on the plane of $abc$ it is a fixed multiple of the signed area $\sigma_{ab}(x)$ of the triangle $a, b, x$ in that plane: $[a b x d] = \frac{\sigma_{ab}(x)}{\sigma_{ab}(c)}\,[a b c d]$. Since $[a b d p] = -[a b p d]$,

$$[a b d e] = -\frac{1}{s}\,\lambda_c(p)\,[a b c d], \qquad \lambda_c(p) = \frac{\sigma_{ab}(p)}{\sigma_{ab}(c)}.$$

The same computation for the edges $bc$ and $ca$, with $[b c a d] = [c a b d] = [a b c d]$ (cyclic shifts of three entries are even permutations), gives $[b c d e] = -\frac1s\,\lambda_a(p)\,[a b c d]$ and $[c a d e] = -\frac1s\,\lambda_b(p)\,[a b c d]$. Here $\lambda_a, \lambda_b, \lambda_c$ are the barycentric coordinates of $p$ in $abc$, which sum to 1, so they cannot all be negative. Hence the three values have one strict sign if and only if all three barycentric coordinates are positive, that is, if and only if $p$ is inside the triangle. $\square$

**Theorem 3 (2-3 flip).** Let $abcd$ and $abce$ be two tetrahedra of a valid mesh that share the face $abc$. The flip that replaces them by $abde$, $bcde$ and $cade$ gives a valid mesh if and only if $[a b d e]$, $[b c d e]$ and $[c a d e]$ have one strict sign, which by Lemma 2 means that the segment $de$ crosses the interior of $abc$. Then the three new tetrahedra, ordered positively, have the same total volume and the same boundary faces as the two old ones.

*Proof.* In a valid mesh, the two tetrahedra on the face $abc$ lie on opposite sides of its plane, so $[abcd]$ and $[abce]$ have opposite strict signs, and Lemma 2 applies.

*Volume.* Lemma 1 with $(a, b, c, d, e)$ gives $[bcde] - [acde] + [abde] - [abce] + [abcd] = 0$. With $[acde] = -[cade]$,

$$[abcd] - [abce] = -\bigl([abde] + [bcde] + [cade]\bigr).$$

The left side is the sum of the two old volumes (times 6), in absolute value, because the two terms have opposite signs. If the three new values have one sign, the right side is the sum of their absolute values. So the volume is kept.

*Disjoint interiors.* The point $p$ of Lemma 2 is inside $abc$ and on the segment $de$. The plane through $b$, $d$, $e$ contains $p$ and $b$, so it meets the triangle $abc$ in the line $bp$, which separates $a$ from $c$. So $abde$ and $bcde$ lie on opposite sides of that plane. The same holds for the other two pairs.

*Same region and same boundary.* The three new tetrahedra lie in the convex hull $B$ of the five points, and so do the two old ones, which have disjoint interiors and together have the volume of $B$ (they form the bipyramid on $abc$, which is convex because $p$ is inside $abc$). The new ones have disjoint interiors and the same total volume, so their union is $B$ as well. The faces of $abde$, $bcde$, $cade$ are $abd, abe, bcd, bce, cad, cae$, each once, and $ade$, $bde$, $cde$, each twice. So the boundary faces are the six faces $abd, abe, bcd, bce, cad, cae$, the same as for $abcd$ and $abce$, whose shared face $abc$ is interior. The rest of the mesh does not change, so the mesh stays valid.

*Necessity.* If the three values do not have one strict sign, then either one of them is zero, and a new tetrahedron is flat, or $p$ is outside the closed triangle or on its boundary, and by Lemma 2 the new tetrahedra cannot all be positive with disjoint interiors: if two had opposite signs in the cyclic order around $de$, their wedges around the edge $de$ would overlap. $\square$

**Theorem 4 (3-2 flip).** Let $de$ be an interior edge of a valid mesh that lies in exactly three tetrahedra, whose other vertices form the ring $a, b, c$ in the order of rotation around $de$. The flip that replaces them by $abcd$ and $abce$ gives a valid mesh if and only if $d$ and $e$ lie strictly on opposite sides of the plane $abc$, that is, $[abcd]\,[abce] < 0$. The volume and the boundary faces are kept.

*Proof.* The three tetrahedra $abde$, $bcde$, $cade$ fill the space around the interior edge $de$ in three wedges that turn the same way and make one full turn, so $[abde]$, $[bcde]$ and $[cade]$ have one strict sign. If $d$ and $e$ are strictly on opposite sides of the plane $abc$, Lemma 2 shows that the segment $de$ crosses the interior of $abc$. The configuration is then exactly the result of a valid 2-3 flip of $abcd$ and $abce$, so by Theorem 3 the two meshes have the same region, the same boundary faces and the same volume, and the 3-2 flip is the inverse 2-3 flip. If $d$ and $e$ are on the same side, or one is on the plane, then $abcd$ and $abce$ overlap near the face $abc$ or one is flat, so the flip is invalid. $\square$

**Theorem 5 (hill climbing).** IMPROVE keeps a valid mesh of the same region with the same boundary faces, never lowers the smallest quality, and stops after finitely many flips.

*Proof.* Each flip is applied only after the exact tests of Theorems 3 and 4, so validity, the region and the boundary are kept. A flip is applied only if the smallest quality of the new tetrahedra is larger than the smallest quality $m$ of the old ones, so the smallest quality of the whole mesh does not go down.

For termination, list the qualities of the mesh in increasing order. A flip removes a set $R$ of tetrahedra whose smallest quality is $m$, and adds a set $R'$ whose qualities are all larger than $m$. The tetrahedra outside $R$ are the same before and after. In the sorted lists, the entries smaller than $m$ are the same; the old list has more entries equal to $m$ than the new list, since it has those of $R$ in addition; and the new list has an entry at that position, because it has at least $|L| + 2$ entries for the set $L$ of unchanged tetrahedra. So the new sorted list is lexicographically larger. The vertex set never changes, and a finite point set has finitely many tetrahedral meshes, since each is a set of 4-element subsets. The sorted list is a function of the mesh and strictly increases, so no mesh repeats and the loop stops. $\square$

The comparisons of quality are made in floats. The argument uses only that the computed quality is a fixed function of the four points, so it holds for the computed values.

**What is not proved.** No bound on the dihedral angles follows. Hill climbing stops at a mesh where no single 2-3 or 3-2 flip helps the worst tetrahedra, which can still be bad. In a measured run, a $2 \times 2 \times 2$ cube mesh of 48 tetrahedra with smallest dihedral angle $34.4°$ was scrambled by random valid flips to a mesh of 52 tetrahedra with smallest dihedral angle $2.53°$; hill climbing with 2-3 and 3-2 flips made 4 flips and left the smallest angle at $2.53°$. Larger moves, such as edge removal, multi-face removal, smoothing and vertex insertion, are needed, and their results too are measured, not proved.
