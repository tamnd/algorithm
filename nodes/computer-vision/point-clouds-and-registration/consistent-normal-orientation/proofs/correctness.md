---
title: The propagation makes the normals agree along every tree edge, and it recovers a true orientation whenever that orientation agrees along the tree
proves: [correctness]
status: full
---

Let the points be $p_1, \ldots, p_n$ with unit normals $\mathbf{n}_1, \ldots, \mathbf{n}_n$ of arbitrary signs. An *orientation* is a choice of signs $s_i \in \{+1, -1\}$, giving the normals $s_i \mathbf{n}_i$. Write $\mathbf{m}_i$ for the output normal of point $i$.

**Lemma 1 (a spanning tree).** Lines L1 to L4 build a spanning tree $T$ of the points, rooted at the point $r$ of largest $z$, that has the least total cost $\sum_{(i, j) \in T} (1 - |\mathbf{n}_i \cdot \mathbf{n}_j|)$ among the spanning trees of the Riemannian graph $G$.

*Proof.* The graph $G$ of line L1 contains the edges of a Euclidean minimum spanning tree of all the points, so it is connected. Line L4 is Prim's algorithm from $r$ on $G$ with the costs of line L2, so it returns a [minimum spanning tree](/minimum-spanning-tree/) of $G$; this is the cut property of minimum spanning trees. The cost of an edge does not change when either normal changes sign, because it uses $|\mathbf{n}_i \cdot \mathbf{n}_j|$. So $T$ does not depend on the input signs. $\square$

For a point $j \ne r$ let $\mathrm{par}(j)$ be its parent in $T$.

**Lemma 2 (agreement on tree edges).** The output satisfies $\mathbf{m}_r \cdot \mathbf{e}_z \ge 0$, $\mathbf{m}_i = \pm \mathbf{n}_i$ for every $i$, and $\mathbf{m}_j \cdot \mathbf{m}_{\mathrm{par}(j)} \ge 0$ for every $j \ne r$.

*Proof.* Line L5 sets the sign of the root so that its $z$ component is at least zero, and the root is never changed later, because it is no child. Every other point $j$ is pushed on the stack exactly once, as a child of its parent at line L11, so line L10 runs exactly once for $j$, after its parent was popped at line L8. At that time the parent's normal is final: the parent is changed only when it is handled as a child, which happened before it was pushed. Line L10 compares $\mathbf{m}_{\mathrm{par}(j)} \cdot \mathbf{n}_j$ with zero and flips $\mathbf{n}_j$ when it is negative, so afterwards the product is at least zero. Only signs change, so $\mathbf{m}_i = \pm \mathbf{n}_i$. $\square$

**Lemma 3 (uniqueness).** Suppose $\mathbf{n}_j \cdot \mathbf{n}_{\mathrm{par}(j)} \ne 0$ for every tree edge, and $\mathbf{n}_r$ has a nonzero $z$ component. Then the output of Lemma 2 is the only orientation with the three properties of Lemma 2. In particular, the output does not depend on the input signs.

*Proof.* The sign at the root is fixed by $\mathbf{m}_r \cdot \mathbf{e}_z > 0$. If the sign of the parent is fixed, the sign of a child $j$ is fixed by $\mathbf{m}_j \cdot \mathbf{m}_{\mathrm{par}(j)} > 0$, since the product is nonzero and changes sign with $s_j$. Induction over the depth in $T$ fixes every sign. By Lemma 1 the tree $T$ does not depend on the input signs, and the conditions only involve $\pm \mathbf{n}_i$, so the output does not either. $\square$

**Theorem (what the method guarantees).** Let $t_1, \ldots, t_n$ be a true orientation, for example the outward normals of a closed surface, and assume that $t_i \mathbf{n}_i \cdot t_j \mathbf{n}_j > 0$ for every edge $(i, j)$ of $T$. Then the output is $\mathbf{m}_i = \epsilon\, t_i \mathbf{n}_i$ for all $i$, with one global sign $\epsilon \in \{+1, -1\}$, and $\epsilon = +1$ when the true normal at the root has a positive $z$ component.

*Proof.* The orientation $\epsilon\, t_i \mathbf{n}_i$, with $\epsilon$ chosen so that the root normal has $z \ge 0$, satisfies all three properties of Lemma 2: the product along each tree edge is $\epsilon^2\, t_i \mathbf{n}_i \cdot t_j \mathbf{n}_j > 0$. The hypothesis also gives $\mathbf{n}_j \cdot \mathbf{n}_{\mathrm{par}(j)} \ne 0$ on all tree edges. If the root normal has $z = 0$, line L5 keeps it, and the same induction as in Lemma 3 shows that the output is $\epsilon t_i \mathbf{n}_i$ with the sign given at the root; otherwise Lemma 3 says the output is this orientation. On a closed surface the point of largest $z$ has the outward normal $+\mathbf{e}_z$ when the surface is smooth there, so $\epsilon = +1$. $\square$

**What is not guaranteed.** The hypothesis of the theorem is about the tree, and nothing forces it. If a tree edge joins two points whose true normals point in opposite directions, the method flips one side wrongly, and the error passes to the whole subtree below that edge. This happens on thin parts, where points of the two opposite sheets are near neighbors with parallel normals of cost 0, and at sharp edges, where the true normals of the two faces are near orthogonal and the sign test of line L10 decides on a product near zero. The cost $1 - |\mathbf{n}_i \cdot \mathbf{n}_j|$ makes the tree prefer paths over flat, smooth regions, which is why the method works well in practice, but it is a heuristic. $\blacksquare$
