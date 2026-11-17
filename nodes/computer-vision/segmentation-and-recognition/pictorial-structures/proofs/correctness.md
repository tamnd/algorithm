---
title: Tree dynamic programming with distance transforms finds a minimum-energy configuration in time linear in the number of locations
proves: [correctness]
status: full
---

We use the notation of the page. A model has $n$ parts on a tree with root $r$; each part $j \ne r$ has a parent $p(j)$. Each part has a match cost $m_j(l)$ for every location $l$ of a set $\mathcal{L}$ of $h$ grid cells, and each edge has the spring cost
$$d_j(l_{p}, l_j) = w_x (x_j - x_p - u_x)^2 + w_y (y_j - y_p - u_y)^2, \qquad w_x, w_y > 0.$$
The energy of a configuration $L = (l_1, \ldots, l_n)$ is $E(L) = \sum_j m_j(l_j) + \sum_{j \ne r} d_j(l_{p(j)}, l_j)$.

**Claim.** MATCH returns a configuration of minimum energy, and the energy it reports is that minimum. With the distance transform it takes $O(nh)$ time.

**Lemma 1 (the one-dimensional transform).** For $f : \{0, \ldots, N-1\} \to \mathbb{R}$, $w > 0$ and a real $u$, DT1 returns $D(p) = \min_q f(q) + w(q - p - u)^2$ for every $p$, and a minimizing $q$.

*Proof.* For each $q$, the function $t \mapsto f(q) + w(q - t)^2$ is a parabola with the same leading coefficient $w$. Two such parabolas, for $q < q'$, cross at exactly one point
$$s = \frac{(f(q') + w q'^2) - (f(q) + w q^2)}{2 w (q' - q)},$$
and the parabola of $q'$ is the lower one to the right of $s$. So the lower envelope of the parabolas is a sequence of pieces, with the indices of the pieces increasing from left to right. Lines L1 to L5 build the envelope of the first $q + 1$ parabolas from that of the first $q$: the new parabola of $q$ is lowest to the right of its crossing $s$ with the last piece; if $s \le z[k]$, the start of the last piece, then the last piece is nowhere lowest any more and line L4 removes it. When the loop stops, $s > z[k]$, the last piece keeps the part $[z[k], s]$, and the new piece covers $[s, \infty)$. This is the invariant that $v[0..k]$ are the indices of the envelope pieces and $z[i], z[i+1]$ bound piece $i$. Lines L6 to L9 then evaluate the envelope at $t = p + u$: since $t$ grows with $p$ and the pieces are ordered, the pointer of line L8 moves forward to the piece that contains $t$, and line L9 evaluates that parabola, which is the minimum over all $q$. $\square$

*Cost of Lemma 1.* Each index is appended once in line L5 and removed at most once in line L4, and the pointer of line L8 moves at most $k \le N$ times, so DT1 takes $O(N)$ time.

**Lemma 2 (the two-dimensional transform).** DT2 returns $D(x, y) = \min_{x', y'} f(x', y') + w_x (x' - x - u_x)^2 + w_y (y' - y - u_y)^2$ and a minimizer, in $O(h)$ time.

*Proof.* The cost is a sum of a term in $x'$ and a term in $y'$, so
$$D(x, y) = \min_{y'} \Big( w_y (y' - y - u_y)^2 + \min_{x'} \big( f(x', y') + w_x (x' - x - u_x)^2 \big) \Big).$$
The inner minimum is DT1 along row $y'$, and the outer one is DT1 along column $x$ of the result. The minimizer is the $y'$ of the outer transform and the $x'$ that the inner transform stored for row $y'$ and column $x$. Each of the two passes calls DT1 on lines of total length $h$. $\square$

**Lemma 3 (the messages).** For a part $j$, let $T_j$ be the subtree rooted at $j$, and define
$$f_j(l) = m_j(l) + \sum_{c \text{ child of } j} B_c(l), \qquad B_c(l) = \min_{l'} \big( f_c(l') + d_c(l, l') \big).$$
Then $f_j(l)$ is the minimum, over all placements of the parts of $T_j$ with $j$ at $l$, of the energy restricted to $T_j$ (the match costs of its parts and the springs of its edges).

*Proof.* By induction on the height of $T_j$. For a leaf, $f_j = m_j$. For an inner part with $j$ fixed at $l$, the energy of $T_j$ is $m_j(l)$ plus, for each child $c$, the spring $d_c(l, l_c)$ plus the energy of $T_c$. Once $l$ is fixed, the subtrees of different children share no part and no edge, so their terms can be minimized one at a time. For child $c$, the minimum over the placements of $T_c$ with $c$ at $l'$ is $f_c(l')$ by induction, and the minimum over $l'$ of $f_c(l') + d_c(l, l')$ is $B_c(l)$. $\square$

*Proof of the claim.* Line L10 visits the parts in postorder, so the messages of all children of $j$ exist when line L11 forms $f_j$. Line L12 computes $B_j$ with Lemma 2, with the parent location as the query point and the spring of $j$, and stores the minimizer $A_j(l)$ for each parent location $l$. By Lemma 3 with $T_r$ the whole tree, $\min_l f_r(l)$ is the minimum energy, and line L13 picks a location $l_r$ that attains it. Line L14 goes down the tree and sets $l_c = A_c(l_{p(c)})$. By induction from the root, the placement of each subtree $T_c$ that this builds attains $f_c(l_c)$, because $A_c(l_{p(c)})$ attains the minimum that defines $B_c(l_{p(c)})$. So the returned configuration has energy $f_r(l_r)$, the minimum.

Cost: each part other than the root costs $O(h)$ for line L11, counting each child once at its parent, and $O(h)$ for line L12 by Lemma 2. Lines L13 and L14 cost $O(h + n)$. The total is $O(nh)$. With a general cost $d_j$ instead of a squared distance, line L12 would need $O(h^2)$ time for each part. $\square$

**Remark (cycles).** Lemma 3 uses that the subtrees of different children are disjoint. If the parts form a graph with a cycle, this fails, and the minimization is NP-hard in general, as Felzenszwalb and Huttenlocher note for arbitrary graphs.
