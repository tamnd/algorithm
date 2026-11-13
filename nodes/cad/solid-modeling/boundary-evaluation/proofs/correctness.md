---
title: Generate and classify returns the oriented boundary of the solid
proves: [correctness]
status: full
---

Let $T$ be a CSG tree with leaves $P_0, \ldots, P_{L-1}$, in the order of the leaves, and inner nodes $\cup^*$, $\cap^*$ and $-^*$. Each $P_i = \{x : a \cdot x \le b \text{ for } (a, b) \in H_i\}$ is a bounded convex polyhedron with nonempty interior. Let $X$ be the solid of $T$, and let $\Pi$ be the finite set of all planes $a \cdot x = b$ with $(a, b)$ in some $H_i$. Write $\Phi$ for the plain Boolean formula of $T$, so that $\Phi(\chi_0, \ldots, \chi_{L-1})$ is computed from the truth values of the leaves. A *piece* is a polygon in the list $Q$ after line L5.

**Lemma 1 (pieces are cells).** Let $g$ be a piece of a face $f$ of $P_i$, in the plane $\pi_f$. No plane of $\Pi$ meets the relative interior $\operatorname{ri} g$ unless it contains $\pi_f$. So $g$ is the closure of a cell of the arrangement that the planes of $\Pi$ cut in $\pi_f$, restricted to $f$.

*Proof.* A plane $\sigma$ of some $P_j$ with $j \ne i$ was used at line L5. After the cut by $\sigma$, every part lies in one closed side of $\sigma$, and later cuts keep this. So either $g \subseteq \sigma$, in which case $\sigma = \pi_f$, or $\operatorname{ri} g$ lies in one open side of $\sigma$. A plane $\sigma$ of $P_i$ other than $\pi_f$ supports the convex set $P_i$, so it meets $f \subseteq P_i$ only on the relative boundary of $f$, and so it misses $\operatorname{ri} g$. $\square$

**Lemma 2 (the side tests).** Let $c \in \operatorname{ri} g$ with unit normal $n$ of $\pi_f$ out of $P_i$, and $s = \pm 1$. There is a ball $U$ around $c$ cut by $\pi_f$ into two open half-balls $U^+$ (the side of $n$) and $U^-$. Each $P_j$ contains $U^s$ or misses it, and SIDE-MEMBER$(P_j, c, n, s)$ at line L9 returns which. Hence $X \supseteq U^s$ if $\Phi$ of the side tests is true, and $X \cap U^s = \emptyset$ otherwise. The same holds with $c$ replaced by any point $q \in \operatorname{ri} g$, with the same answers.

*Proof.* By Lemma 1, the only planes of $\Pi$ through $c$ are copies of $\pi_f$. Take $U$ so small that it meets no other plane of $\Pi$. For a half-space with $a \cdot c < b$ or $a \cdot c > b$, the sign holds on all of $U$. For a half-space with $a \cdot c = b$, the plane is $\pi_f$, so $a$ is a nonzero multiple of $n$ and $a \cdot (c + t n) - b = t \, (a \cdot n)$. This is negative on $U^s$ exactly when $s \, (a \cdot n) < 0$. These are the tests of SIDE-MEMBER, and on $U^s$ every inequality of $P_j$ holds strictly or one fails everywhere. So $P_j \supseteq U^s$ or $P_j \cap U^s = \emptyset$. On the open set $U^s$ each leaf is all or nothing, so the plain formula is all or nothing with the value of $\Phi$. By fact 7 of the [regularized set operations](/regularized-set-operations/), $X$ and the plain set differ only on the union of the boundaries of the $P_j$, which misses $U^s$, and $X$ is closed, so the claim holds. For another point $q \in \operatorname{ri} g$, the signs $a \cdot q - b$ are the same as at $c$: they are nonzero and constant on the connected set $\operatorname{ri} g$ for the planes that miss it, and zero for the copies of $\pi_f$. $\square$

So each piece $g$ has two values: front $= \Phi$ on $U^+$ and back $= \Phi$ on $U^-$, the same at every point of $\operatorname{ri} g$.

**Lemma 3 (boundary points).** A point $q \in \operatorname{ri} g$ lies on $\partial X$ if and only if front $\ne$ back. If back is true and front is false, $X$ lies on the side of $-n$ near $q$, and if front is true and back is false, it lies on the side of $n$.

*Proof.* Near $q$, by Lemma 2, $X$ is the closure of $U^+$, $U^-$, both or neither, intersected with $U$. These four cases give the whole ball, the empty set, or a closed half-ball. Only a half-ball has $q$ on its boundary. $\square$

**Lemma 4 (copies).** Let $g$ be a piece of a face of $P_i$ with $c \in \operatorname{ri} g$ on the boundary of $P_j$, $j \ne i$. Then the face $f'$ of $P_j$ through $c$ lies in the plane of $g$, and among the pieces of $f'$ there is one with the same point set as $g$.

*Proof.* The point $c$ lies on a plane of $P_j$, which by Lemma 1 is $\pi_f$. So $c$ is in the face $f'$ of $P_j$ in $\pi_f$. By Lemma 1 applied to both faces, the pieces of $f$ and of $f'$ are the closures of the cells of one arrangement, the trace of $\Pi$ on $\pi_f$: the planes of $P_i$ do not cut $\operatorname{ri} f$, and those of $P_j$ do not cut $\operatorname{ri} f'$. The cell through $c$ is in both lists. $\square$

**Theorem.** The polygons returned at line L12 have pairwise disjoint relative interiors, their union is $\partial X$, and each one is ordered counterclockwise around the normal that points out of $X$.

*Proof.* *Cover.* The boundary of $X$ lies in the union of the boundaries of the $P_j$ (fact 7 again: off that union, $X$ is locally all or nothing). Each boundary point of $P_i$ is in a face $f$, which is the union of its pieces. So $\partial X$ lies in the union of all pieces. Let $q \in \partial X$ be in the relative interior of a piece $g$. By Lemma 3, $g$ has front $\ne$ back. If $g$ is skipped at line L8, its center lies on the boundary of some $P_j$ with $j < i$. Take the least such $j$. By Lemma 4, $P_j$ has a copy of $g$, whose center is the same point and lies on no boundary of $P_k$ with $k < j$, so the copy is not skipped. It has the same front and back, or both swapped when the normals are opposite. So the point set is kept at line L10 or L11. It remains to cover the points of $\partial X$ on the set $S$, the union of the relative boundaries of all pieces, which is a finite union of segments. Let $p \in \partial X$ and let $U$ be a ball around $p$. Then $U \setminus S$ is connected, because a finite union of segments does not separate a ball. It meets $\operatorname{int} X$, because $p \in \operatorname{cl}(\operatorname{int} X)$ and $S$ has no interior, and it meets the open complement of $X$ for the same reason. So $U \setminus S$ meets $\partial X$. Hence $p$ is a limit of points of $\partial X \setminus S$, which lie in kept polygons, and the union of the kept polygons is closed, so it contains $p$.

*Only boundary.* A kept polygon has front $\ne$ back, so by Lemma 3 its relative interior lies in $\partial X$, and so does its closure.

*Disjoint.* Two pieces of the same face are distinct cells of one arrangement. Two pieces in different planes: one of them, say $g$, was cut by the plane of the other, or both lie in faces of one convex $P_i$, which meet only along edges. In both cases $\operatorname{ri} g$ misses the other piece. Two pieces in one plane from different primitives are equal or have disjoint relative interiors by Lemma 4, and line L8 keeps one copy of each point set.

*Orientation.* The faces of $P_i$ are counterclockwise around their outward normal $n$. Line L10 keeps $g$ when $X$ is on the side of $-n$, so $n$ points out of $X$. Line L11 keeps the reversed list when $X$ is on the side of $n$, and the reversed order is counterclockwise around $-n$, which points out of $X$. $\blacksquare$

**Termination.** Each loop runs over finite lists. Line L5 replaces a polygon by at most two polygons, and the number of planes is finite.

**Degenerate input.** Coplanar faces, touching primitives and faces that meet along edges are part of the input. They need no special case: Lemma 1 holds for them, the side tests use only signs computed exactly, and line L8 removes the copies of coplanar pieces. The proof needs the signs to be exact. With rounded arithmetic, Lemma 1 can fail for a piece that a plane only nearly misses.
