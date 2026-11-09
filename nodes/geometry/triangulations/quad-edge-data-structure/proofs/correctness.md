---
title: Splice keeps the edge algebra valid, and Connect and DeleteEdge split and merge faces
proves: [correctness, termination]
status: full
---

**Setting.** Directed edges are integers $e = 4q + r$. The maps $\mathrm{Rot}(e) = 4q + ((r + 1) \bmod 4)$, $\mathrm{Sym} = \mathrm{Rot}^2$ and $\mathrm{Rot}^{-1} = \mathrm{Rot}^3$ are fixed bijections (line L1). An edge is **primal** if $r$ is even and **dual** if $r$ is odd; $\mathrm{Rot}$ swaps the two kinds. The only stored map is the permutation $O = \mathrm{Onext}$ of all directed edges. Write $O^{-1}$ for its inverse. Lines L2 define $\mathrm{Oprev}(e) = \mathrm{Rot}(O(\mathrm{Rot}(e)))$ and $\mathrm{Lnext}(e) = \mathrm{Rot}(O(\mathrm{Rot}^{-1}(e)))$. All splices in the code are applied to primal edges.

**Invariant (D).** For every dual edge $f$, $O(f) = \mathrm{Rot}^{-1}(O^{-1}(\mathrm{Rot}^{-1}(f)))$. In words, the dual rings are determined by the primal rings.

**Lemma 1 (consequences of D).** If (D) holds then, for every primal edge $e$: (a) $\mathrm{Oprev}(e) = O^{-1}(e)$; (b) $\mathrm{Lnext}(e) = O^{-1}(\mathrm{Sym}(e))$; (c) $\mathrm{Rot}(O(\mathrm{Rot}(O(x)))) = x$ for every directed edge $x$.

*Proof.* (a) $\mathrm{Rot}(e)$ is dual, so by (D), $O(\mathrm{Rot}(e)) = \mathrm{Rot}^{-1}(O^{-1}(e))$, and applying $\mathrm{Rot}$ gives $O^{-1}(e)$. (b) $\mathrm{Rot}^{-1}(e)$ is dual, so $O(\mathrm{Rot}^{-1}(e)) = \mathrm{Rot}^{-1}(O^{-1}(\mathrm{Rot}^{-2}(e)))$, and applying $\mathrm{Rot}$ gives $O^{-1}(\mathrm{Sym}(e))$. (c) If $x$ is dual, (D) gives $\mathrm{Rot}(O(x)) = O^{-1}(\mathrm{Rot}^{-1}(x))$, so $O(\mathrm{Rot}(O(x))) = \mathrm{Rot}^{-1}(x)$, and applying $\mathrm{Rot}$ gives $x$. If $x$ is primal, $y = \mathrm{Rot}(O(x))$ is dual, and (D) applied to $y$ gives $O(y) = \mathrm{Rot}^{-1}(O^{-1}(O(x))) = \mathrm{Rot}^{-1}(x)$, so $\mathrm{Rot}(O(y)) = x$. $\square$

Part (c) is the axiom $e\,\mathrm{Rot}\,\mathrm{Onext}\,\mathrm{Rot}\,\mathrm{Onext} = e$ of Guibas and Stolfi.

**Lemma 2 (MakeEdge).** Lines L3 to L5 keep (D) and add one primal edge whose two directions $e$ and $\mathrm{Sym}(e)$ each form a ring of size 1.

*Proof.* With $e = 4q$, line L4 sets $O(e) = e$, $O(e + 2) = e + 2$, $O(e + 1) = e + 3$, $O(e + 3) = e + 1$. For $f = e + 1$: $\mathrm{Rot}^{-1}(f) = e$, $O^{-1}(e) = e$, $\mathrm{Rot}^{-1}(e) = e + 3 = O(f)$. For $f = e + 3$: $\mathrm{Rot}^{-1}(f) = e + 2$, $O^{-1}(e + 2) = e + 2$, $\mathrm{Rot}^{-1}(e + 2) = e + 1 = O(f)$. Other edges are unchanged. $\square$

**Lemma 3 (Splice).** If (D) holds and $a \ne b$ are primal, lines L6 to L8 keep (D). On primal edges the new permutation is $O' = O \circ (a\ b)$: $O'(a) = O(b)$, $O'(b) = O(a)$, and $O'(x) = O(x)$ otherwise. Splice is an involution.

*Proof.* Line L7 is exactly $O' = O \circ (a\ b)$ on primal edges. Then $O'^{-1}(x) = O^{-1}(x)$ except $O'^{-1}(O(a)) = b$ and $O'^{-1}(O(b)) = a$. The right side of (D) for a dual $f$ changes only if $\mathrm{Rot}^{-1}(f) \in \{O(a), O(b)\}$, that is, $f \in \{\alpha, \beta\}$ with $\alpha = \mathrm{Rot}(O(a))$ and $\beta = \mathrm{Rot}(O(b))$ as computed on line L6 (before the swap). The required new values are $O'(\alpha) = \mathrm{Rot}^{-1}(b)$ and $O'(\beta) = \mathrm{Rot}^{-1}(a)$. The old values are $O(\alpha) = \mathrm{Rot}^{-1}(O^{-1}(O(a))) = \mathrm{Rot}^{-1}(a)$ and $O(\beta) = \mathrm{Rot}^{-1}(b)$, so the required new values are the old ones swapped, which is line L8. Since $a \ne b$, $O(a) \ne O(b)$ and $\alpha \ne \beta$, and $\alpha, \beta$ are dual, so the two swaps touch disjoint entries. Applying the same splice again swaps the same pairs back, because $\alpha$ and $\beta$ are recomputed from $O'(a) = O(b)$ and $O'(b) = O(a)$ and give the same pair. $\square$

By Lemma 3, if $a$ and $b$ lie in different rings, Splice merges them into one ring in which $a$ is followed by the old successor of $b$ and $b$ by the old successor of $a$; if they lie in the same ring, it splits it into two. In particular, splicing an isolated edge $e$ (with $O(e) = e$) with $c$ inserts $e$ into the ring of $c$ directly after $c$.

**Faces.** By Lemma 1(b), $\mathrm{Lnext} = O^{-1} \circ \mathrm{Sym}$ on primal edges, a permutation; its cycles are the **faces**, and the face traced from $e$ is the face left of $e$. The loop of line L18 follows one cycle and stops when it returns to a visited edge, so it terminates, and each directed primal edge lies in exactly one face. At the origin of $x$ the face left of $x$ occupies the wedge from $x$ to $O(x)$, and at the destination of $x$ it occupies the wedge from $\mathrm{Lnext}(x)$ to $\mathrm{Sym}(x) = O(\mathrm{Lnext}(x))$.

**Lemma 4 (Connect).** Let $a$ and $b$ be primal edges with the same left face $F$, traced as $a, \mathrm{Lnext}(a) = c, \ldots, b, \ldots$. Lines L9 to L11 add an edge $e$ from $\mathrm{Dest}(a)$ to $\mathrm{Org}(b)$ and replace $F$ by the two faces $(a, e, b, \mathrm{Lnext}(b), \ldots, \mathrm{Lprev}(a))$ and $(\mathrm{Sym}(e), c, \ldots, \mathrm{Lprev}(b))$; every other face is unchanged.

*Proof.* Line L10 inserts the isolated $e$ after $c$ in the ring at $\mathrm{Dest}(a)$, inside the wedge of $F$ there, and line L11 inserts $\mathrm{Sym}(e)$ after $b$ at $\mathrm{Org}(b)$, inside the wedge of $F$ there. So $O'(c) = e$, $O'(e) = O(c) = \mathrm{Sym}(a)$, $O'(b) = \mathrm{Sym}(e)$, $O'(\mathrm{Sym}(e)) = O(b)$. With $\mathrm{Lnext}' = O'^{-1} \circ \mathrm{Sym}$: $\mathrm{Lnext}'(a) = O'^{-1}(\mathrm{Sym}(a)) = e$, $\mathrm{Lnext}'(e) = O'^{-1}(\mathrm{Sym}(e)) = b$, $\mathrm{Lnext}'(\mathrm{Sym}(e)) = O'^{-1}(e) = c$, and for $x = \mathrm{Lprev}(b)$, $\mathrm{Sym}(x) = O(b)$, so $\mathrm{Lnext}'(x) = O'^{-1}(O(b)) = \mathrm{Sym}(e)$. All other values of $\mathrm{Lnext}$ are unchanged. Following the cycles gives the two faces of the statement. $\square$

**Lemma 5 (DeleteEdge).** Lines L12 and L13 remove $e$ from its two rings, and the two faces at $e$ merge into one; it is the inverse of Connect.

*Proof.* By Lemma 1(a), $O(\mathrm{Oprev}(e)) = e$. Splicing $e$ with $p = \mathrm{Oprev}(e)$ gives $O'(e) = O(p) = e$ and $O'(p) = O(e)$: $e$ becomes a ring of size 1 and the ring at $\mathrm{Org}(e)$ closes over the gap. Line L13 does the same at the destination. The result is the state before a Connect that would create $e$, so by Lemma 4 read backwards the two faces merge. $\square$

**Lemma 6 (Flip).** Let $e$ be a primal edge whose two faces are triangles $(e, x, y)$ and $(\mathrm{Sym}(e), u, v)$. Lines L14 to L17 turn them into two triangles sharing the edge $e$, now from $\mathrm{Dest}(a)$ to $\mathrm{Dest}(b)$ with $a = \mathrm{Oprev}(e)$ and $b = \mathrm{Oprev}(\mathrm{Sym}(e))$.

*Proof.* Since $O(a) = e$, the face left of $a$ is the face right of $e$, one of the two triangles; likewise the face left of $b$ is the other triangle. Lines L14 and L15 are DeleteEdge with $a$ and $b$ saved, so by Lemma 5 the two triangles merge into one quadrilateral face $Q$, which is left of both $a$ and $b$. Lines L16 and L17 insert $e$ after $\mathrm{Lnext}(a)$ at $\mathrm{Dest}(a)$ and $\mathrm{Sym}(e)$ after $\mathrm{Lnext}(b)$ at $\mathrm{Org}(\mathrm{Lnext}(b)) = \mathrm{Dest}(b)$, and set the end points. This is exactly Connect of $a$ and $\mathrm{Lnext}(b)$, two edges of $Q$, so by Lemma 4 it splits $Q$ into two triangles along the diagonal from $\mathrm{Dest}(a)$ to $\mathrm{Dest}(b)$. That diagonal is not the old one, since $\mathrm{Dest}(a)$ and $\mathrm{Dest}(b)$ are the two corners of $Q$ that are not end points of the old $e$. $\square$

Geometric validity is a precondition and not part of the structure: Connect produces a planar drawing only if the segment lies inside $F$, and Flip only if the quadrilateral is convex.

**Correctness of the drivers.** `polygon` splices consecutive edges at their common vertex and closes the cycle with Connect; by Lemma 4 the cycle has two faces, the inner one left of the first edge. `fan` applies Connect to $\mathrm{Lnext}(b)$ and $b$ while the face left of $b$ has more than 3 edges; by Lemma 4 each call cuts off one triangle and leaves a face with one edge fewer, so it stops after $k - 3$ calls on a face with $k$ edges. `insert_in_face` makes one edge from a corner to $p$ and inserts it into the face, then connects each next corner to $p$; each Connect cuts off the triangle formed by $p$ and one side, by Lemma 4, until the side before the starting edge is reached, after $k - 1$ calls.

**Termination and cost.** Every operation on lines L1 to L17 does a constant number of array reads and writes, with no loops. The traversal loops follow cycles of permutations and stop after at most the number of directed edges.
