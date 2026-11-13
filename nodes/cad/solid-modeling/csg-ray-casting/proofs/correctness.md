---
title: CSG ray casting returns the regularized classification of the line
proves: [correctness]
status: full
---

Let $T$ be a CSG tree whose leaves are bounded convex polyhedra $P_i = \{x : a_{ij} \cdot x \le b_{ij}\}$ with nonempty interior, and whose inner nodes are $\cup^*$, $\cap^*$ and $-^*$. Write $X_T$ for the solid of $T$. Let $\ell(t) = o + t d$ with $d \ne 0$, and let $I_T = \{t : \ell(t) \in X_T\}$. A *nice* list is a sorted list of disjoint closed intervals of positive length, no two of which share an end point.

**Assumption.** No face plane contains the line: for no $i, j$ are both $a_{ij} \cdot d = 0$ and $a_{ij} \cdot o = b_{ij}$.

Let $Z$ be the finite set of $t$ with $a_{ij} \cdot \ell(t) = b_{ij}$ and $a_{ij} \cdot d \ne 0$ for some $i, j$. A *cell* is a connected component of $\mathbb{R} \setminus Z$.

**Lemma 1.** Let $\kappa$ be a cell. Then for each subtree $S$ of $T$, either $\ell(\kappa) \subseteq \operatorname{int} X_S$ or $\ell(\kappa) \cap X_S = \emptyset$. Write $\phi_S(\kappa)$ for true in the first case and false in the second. Then $\phi_S(\kappa) = \operatorname{op}(\phi_{S.\text{left}}(\kappa), \phi_{S.\text{right}}(\kappa))$ at each inner node, where op is or, and, or and-not.

*Proof.* Each function $g_{ij}(x) = a_{ij} \cdot x - b_{ij}$ is affine. If $a_{ij} \cdot d \ne 0$, then $g_{ij}(\ell(t))$ has its only zero in $Z$, so it has a constant nonzero sign on $\kappa$. If $a_{ij} \cdot d = 0$, then $g_{ij}(\ell(t))$ is constant, and it is not zero by the assumption. Fix $t \in \kappa$. There is a ball $U$ around $\ell(t)$ on which every $g_{ij}$ keeps the sign it has at $\ell(t)$. So $U \subseteq \operatorname{int} P_i$ or $U \cap P_i = \emptyset$ for each leaf. At an inner node with children whose sets each fill $U$ or miss it, the plain set operation gives $U$ or $\emptyset$. The regularization $\operatorname{cl}(\operatorname{int} \cdot)$ does not change a set on the open set $U$ when that set is $U$ or $\emptyset$ there. So by induction $X_S \cap U$ is $U$ or $\emptyset$, as the Boolean formula says. The signs are the same for all $t \in \kappa$, so the choice is the same along the cell. $\square$

**Lemma 2.** Let $W_S$ be the union of the cells $\kappa$ with $\phi_S(\kappa)$ true, and let $J_S = \operatorname{cl} W_S$. Then $J_S = \operatorname{cl}(\operatorname{int} I_S)$, the regularization of $I_S$ on the line, and $I_S \setminus J_S$ is a finite subset of $Z$.

*Proof.* By Lemma 1, $I_S \setminus Z = W_S$. The set $W_S$ is open and lies in $I_S$, so $W_S \subseteq \operatorname{int} I_S$. Conversely, $\operatorname{int} I_S \setminus Z$ lies in $W_S$, and removing finitely many points from an open subset of $\mathbb{R}$ does not change its closure. So $\operatorname{cl}(\operatorname{int} I_S) = \operatorname{cl} W_S$. Finally $I_S \setminus J_S \subseteq I_S \setminus W_S \subseteq Z$. $\square$

The finite difference is real: a line through an edge where the solid touches itself along that edge only, or a line that grazes a vertex, meets $X_S$ in isolated points. The regularized classification of the line drops them, and the result is $J_S$.

**Theorem.** Under the assumption, CAST$(o, d, T)$ returns a nice list whose union is $J_T$, and FIRST-HIT returns $\min (J_T \cap [0, \infty))$, or none when this set is empty.

*Proof.* By induction on the tree.

*Leaf.* Line L2 takes $lo$ as the largest $\tau = (b - a \cdot o)/(a \cdot d)$ over the planes with $a \cdot d < 0$ and $hi$ as the smallest over the planes with $a \cdot d > 0$, and returns the empty list if a plane with $a \cdot d = 0$ has the line outside. The open interval $(lo, hi)$ is then the set of $t$ where all strict inequalities hold, which is $W_{P_i}$. If $lo < hi$, the closure is $[lo, hi]$. If $lo \ge hi$, then $W_{P_i}$ is empty and so is $J_{P_i}$. In both cases the output is a nice list for $J_{P_i}$.

*Inner node.* By the induction hypothesis, $A$ and $B$ are nice lists for $J_{\text{left}}$ and $J_{\text{right}}$. Let $E$ be the end points as in line L5. On an open piece $(e_j, e_{j+1})$ there is no end point of $A$ or $B$, so the piece lies in the interior of one interval of $A$ or misses all intervals of $A$, and the same holds for $B$. Every cell in the piece then has $\phi_{\text{left}}(\kappa)$ equal to the test "the midpoint is inside $A$", and the same for $B$, because $J_{\text{left}} \setminus Z = W_{\text{left}}$. By Lemma 1, line L7 computes $\phi_T(\kappa)$ for every cell in the piece. Outside $[\min E, \max E]$ both children are false, and op(false, false) is false for all three operations. So the true pieces cover $W_T$ up to finitely many points of $Z$, and the closure of their union is $J_T$. Line L8 adds the closed pieces in order and joins a piece to the previous interval when they share an end, so the output is sorted, its intervals have positive length, and no two share an end point.

*First hit.* FIRST-HIT scans the nice list in increasing order. If an interval $[t_0, t_1]$ has $t_1 \ge 0$, all earlier intervals lie in $t < 0$, and the least point of $[t_0, t_1] \cap [0, \infty)$ is $\max(t_0, 0)$. If no interval has $t_1 \ge 0$, then $J_T \cap [0, \infty)$ is empty. $\blacksquare$

**Termination.** CAST visits each node of the tree once, and each MERGE loops once over a finite list.

**A line in a face plane.** If the assumption fails, Lemma 1 fails. On a cell the line can lie in the boundary of a primitive, and the leaf interval then reports the line as inside while the primitive lies on one side of the line only. For the touching cubes $[0, 1]^3$ and $[1, 2] \times [0, 1]^2$ and the line $o = (1, -1, 1/2)$, $d = (0, 1, 0)$ in the shared face, both leaves give $[1, 2]$, so CAST returns $[1, 2]$ for the intersection, while the regularized intersection is empty. Such a line needs the neighborhoods of [set membership classification](/set-membership-classification/) or a perturbation.
