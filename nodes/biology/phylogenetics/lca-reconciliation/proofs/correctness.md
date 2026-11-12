---
title: The LCA map is the lowest valid map and has the fewest duplications and losses
proves: [correctness]
status: full
---

Let $G$ be a rooted binary gene tree, $S$ a rooted species tree and $\sigma$ the leaf map. For species nodes write $x \succeq y$ when $x$ is an ancestor of $y$ or equal to it, and $d(x, y)$ for the number of edges from $x$ down to $y$ when $x \succeq y$. For a valid map $M$ (a map with $M(\ell) = \sigma(\ell)$ at the leaves and $M(g) \succeq M(g')$ for each child $g'$ of $g$), a node $g$ with children $g_1, g_2$ is a speciation if $M(g_1)$ and $M(g_2)$ lie below two different children of $M(g)$, and a duplication otherwise, with $\delta_M(g) \in \{0, 1\}$ the duplication indicator. The costs are $D(M) = \sum_g \delta_M(g)$ and

$$L(M) = \sum_{g \text{ internal}} \sum_{i=1,2} \big( d(M(g), M(g_i)) - 1 + \delta_M(g) \big).$$

Let $M_0$ be the map that LCA-RECONCILE computes in lines L3 and L4.

**Lemma 1 (validity and events).** $M_0$ is valid. An internal node $g$ is a duplication under $M_0$ exactly when $M_0(g) \in \{M_0(g_1), M_0(g_2)\}$, as line L5 tests, and the number that line L7 adds up is $L(M_0)$.

*Proof.* The LCA of two nodes is an ancestor of each of them or equal to it, so $M_0(g) \succeq M_0(g_i)$. Let $x = M_0(g) = \mathrm{lca}(M_0(g_1), M_0(g_2))$. If neither image equals $x$, both lie strictly below $x$, and they lie below different children of $x$, since otherwise that child would be a lower common ancestor. So $g$ is a speciation. If one image equals $x$, it is not below any child of $x$, so $g$ is a duplication. The term of line L7 is $\mathrm{depth}(M_0(g_i)) - \mathrm{depth}(M_0(g)) - 1 + \delta = d(M_0(g), M_0(g_i)) - 1 + \delta$, which is the term of $L$. $\square$

**Lemma 2 (lowest map).** For every valid map $M$ and every node $g$, $M(g) \succeq M_0(g)$.

*Proof.* By induction from the leaves, in postorder. At a leaf both maps equal $\sigma$. At an internal node, validity and the induction hypothesis give $M(g) \succeq M(g_i) \succeq M_0(g_i)$ for $i = 1, 2$. So $M(g)$ is a common ancestor of $M_0(g_1)$ and $M_0(g_2)$, and therefore $M(g) \succeq \mathrm{lca}(M_0(g_1), M_0(g_2)) = M_0(g)$. $\square$

**Lemma 3 (one step down).** Let $M \ne M_0$ be valid. Let $g$ be a node with $M(g) \ne M_0(g)$ such that $M(g') = M_0(g')$ for every descendant $g'$ of $g$. Let $M'$ equal $M$ except $M'(g) = M_0(g)$, and let $h = d(M(g), M_0(g))$. Then $M'$ is valid, $D(M') \le D(M)$, and $L(M') \le L(M) - h < L(M)$.

*Proof.* Such a $g$ exists: among the nodes where the maps differ, take one of least height in $G$. It is internal, because the maps agree on leaves. By Lemma 2, $M(g) \succ M_0(g)$ strictly, so $h \ge 1$.

*Validity.* The children of $g$ have $M'(g_i) = M_0(g_i) \preceq M_0(g) = M'(g)$. If $g$ has a parent $p$, then $M'(p) = M(p) \succeq M(g) \succ M'(g)$. All other constraints are unchanged.

*The node $g$.* Under $M$, the images $M(g_i) = M_0(g_i)$ have LCA $M_0(g)$, which lies strictly below $M(g)$. So both images lie below the same child of $M(g)$, namely the child on the path to $M_0(g)$, and $g$ is a duplication: $\delta_M(g) = 1 \ge \delta_{M'}(g)$. The two terms of $g$ in $L$ change by $\sum_i \big(d(M_0(g), M_0(g_i)) - d(M(g), M_0(g_i))\big) + 2(\delta_{M'}(g) - 1) \le -2h$.

*The parent $p$, if any.* Let $s$ be the sibling of $g$. If $p$ is a speciation under $M$, then $M(g)$ and $M(s)$ lie below different children of $M(p)$. Since $M'(g) \preceq M(g)$, the node $M'(g)$ lies below the same child as $M(g)$, so $p$ is still a speciation under $M'$. So $\delta_{M'}(p) \le \delta_M(p)$. The term of the edge from $p$ to $g$ changes by $d(M(p), M_0(g)) - d(M(p), M(g)) = h$, and the change of $\delta(p)$ adds $2(\delta_{M'}(p) - \delta_M(p)) \le 0$ over the two child edges of $p$.

No other node changes its event or its terms, because events and terms depend only on the images of a node and of its children. So $D(M') \le D(M)$ and $L(M') - L(M) \le -2h + h = -h$. $\square$

**Theorem.** $M_0$ is the unique valid map with the fewest losses. It has the fewest duplications. For every $c_D \ge 0$ and $c_L > 0$, it is the unique valid map that minimizes $c_D D + c_L L$.

*Proof.* Let $M \ne M_0$ be valid. Lemma 3 gives a valid map $M'$ with $D(M') \le D(M)$ and $L(M') < L(M)$, which agrees with $M_0$ at one more node than $M$ does. Repeating the step at most $|G|$ times reaches $M_0$, so $D(M_0) \le D(M)$ and $L(M_0) < L(M)$. Then $c_D D(M_0) + c_L L(M_0) < c_D D(M) + c_L L(M)$ when $c_L > 0$. By Lemma 1, the algorithm outputs $M_0$ with its true events and loss count. $\blacksquare$

**Forced duplications.** In the step of Lemma 3, $\delta_{M'}(g) \le \delta_M(g)$, $\delta_{M'}(p) \le \delta_M(p)$, and no other event changes. So the duplication set of $M'$ is a subset of that of $M$. Along the chain of steps from $M$ to $M_0$, the duplication set of $M_0$ is a subset of that of $M$. So every duplication of $M_0$ is a duplication of every valid map.
