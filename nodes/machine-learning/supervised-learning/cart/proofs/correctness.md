---
title: CART finds the best cut on each feature, never increases impurity, stops, and its pruning sequence gives the smallest optimal subtrees
proves: [correctness, termination]
status: full
---

We use the pseudocode and notation of the page: $I(t) = N(t)\, i(t)$, the decrease $\Delta I = I(t) - I(t_L) - I(t_R)$, and the resubstitution risk $R(t)$ of $t$ as a leaf.

**Claim 1 (the cut search is exact).** Let $v_1 < v_2 < \dots < v_r$ be the distinct known values of $x_j$ at node $t$. Every partition of these cases by a test $x_j \le \theta$ into two nonempty parts is produced by $\theta = (v_i + v_{i+1})/2$ for exactly one $i$. So line L2, which scans these $r - 1$ midpoints, finds a cut of largest decrease on $x_j$.

*Proof.* A test $x_j \le \theta$ sends left exactly the cases with $x_j \in \{v_1, \dots, v_i\}$, where $i$ is the number of values at most $\theta$. Both parts are nonempty iff $1 \le i \le r - 1$, which holds iff $v_1 \le \theta < v_r$, and then $v_i \le \theta < v_{i+1}$. The midpoint of $v_i$ and $v_{i+1}$ lies in the same interval, so it gives the same partition, and different $i$ give different partitions. The scan keeps running class counts (or sums of $y$ and $y^2$) of the left part, so it computes $\Delta I$ for each $i$ exactly. $\square$

**Claim 2 (the decrease is nonnegative).** For every split, $I(t) \ge I(t_L) + I(t_R)$, and $R(t) \ge R(t_L) + R(t_R)$.

*Proof.* Gini: $I(t) = N - \sum_k c_k^2 / N$, where $c_k$ counts class $k$. Write $a_k, b_k$ for the counts on the two sides, with totals $A$ and $B$. For each $k$, $\frac{(a_k + b_k)^2}{A + B} \le \frac{a_k^2}{A} + \frac{b_k^2}{B}$, which after multiplying out is $(a_k B - b_k A)^2 \ge 0$. Summing over $k$ gives $\sum_k c_k^2/N \le \sum_k a_k^2/A + \sum_k b_k^2/B$, and with $N = A + B$ this is $I(t) \ge I(t_L) + I(t_R)$.

Squared error: $I(t) = \min_c \sum_{t} (y - c)^2$, attained at the mean. Splitting the sum by side and minimizing each part with its own constant can only lower it.

The risk: $R(t) = \min_c \sum_t \ell(c, y)$, where $c$ is a class with $\ell$ the 0-1 loss, or a real number with $\ell$ the squared error. The same argument applies: one constant for both sides is one feasible choice of a constant for each side. $\square$

**Claim 3 (termination).** Growth stops, and the tree has at most $n$ leaves.

*Proof.* The primary cut lies between two distinct known values at $t$, so at least one case goes to each side, and each child has fewer cases than $t$. A node with fewer than $n_{\min} \ge 2$ cases, or a pure node, is a leaf, so the recursion stops. The leaves hold disjoint nonempty sets of cases, so there are at most $n$ of them. $\square$

**Claim 4 (surrogates).** A surrogate with agreement $a$ has $\lambda > 0$ iff it disagrees with the primary split on fewer cases than the rule that sends every case to the larger side.

*Proof.* The larger-side rule disagrees with the primary split on a fraction $\min(p_L, p_R)$ of the cases, and the surrogate on $1 - a$. So $\lambda = (\min(p_L, p_R) - (1 - a)) / \min(p_L, p_R)$ is positive iff $1 - a < \min(p_L, p_R)$. $\square$

**Claim 5 (pruning).** A *pruning* of a tree $T$ is a subtree $T'$ with the same root such that each internal node of $T'$ has both its children in $T'$. Let $R_\alpha(T') = \sum_{\text{leaves } u \text{ of } T'} R(u) + \alpha\, |\text{leaves}(T')|$. Let $(\alpha_k, T_k)$, $k = 1, \dots, K$, be the sequence of lines L7 to L9. Then $0 = \alpha_1 < \alpha_2 < \dots < \alpha_K$, and for every $\alpha$ with $\alpha_k \le \alpha < \alpha_{k+1}$ (with $\alpha_{K+1} = \infty$), $T_k$ minimizes $R_\alpha$ over all prunings of $T_{\max}$ and is contained in every minimizer.

*Proof.* For a node $t$ let $C_\alpha(t)$ be the least $R_\alpha$ over prunings of the branch $T_t$. A pruning of $T_t$ is either $t$ alone or $t$ with a pruning of each child branch, chosen independently, and $R_\alpha$ adds over the two branches. So $C_\alpha(t) = R(t) + \alpha$ at a leaf, and
$$C_\alpha(t) = \min\big(R(t) + \alpha,\; C_\alpha(t_L) + C_\alpha(t_R)\big)$$
at an internal node. Let $T(\alpha)$ be the pruning whose nodes are the $t$ such that no proper ancestor $u$ of $t$ has $R(u) + \alpha \le C_\alpha(u_L) + C_\alpha(u_R)$.

*(a) $T(\alpha)$ is the smallest minimizer.* By induction on the height of $t$: $T(\alpha)_t$ attains $C_\alpha(t)$ and is contained in every pruning of $T_t$ that attains it. If $R(t) + \alpha \le C_\alpha(t_L) + C_\alpha(t_R)$, then $T(\alpha)_t = \{t\}$, which attains the minimum and is contained in every pruning. Otherwise every minimizer of $T_t$ keeps both children, with minimizers of both branches, and by induction contains $T(\alpha)_{t_L}$ and $T(\alpha)_{t_R}$.

*(b) Nested.* Every pruning has at least one leaf, so for $\beta \ge \alpha$ each term $R(T') + \beta |T'|$ exceeds $R(T') + \alpha |T'|$ by at least $\beta - \alpha$, and $C_\beta(u) \ge C_\alpha(u) + (\beta - \alpha)$. So $D_\alpha(t) = C_\alpha(t_L) + C_\alpha(t_R) - R(t) - \alpha$ satisfies $D_\beta(t) \ge D_\alpha(t) + 2(\beta - \alpha) - (\beta - \alpha) \ge D_\alpha(t)$. If $t \in T(\beta)$, each proper ancestor $u$ has $D_\alpha(u) \le D_\beta(u) < 0$, so $t \in T(\alpha)$. Thus $T(\beta) \subseteq T(\alpha)$.

*(c) $T_1 = T(0)$.* By Claim 2 and induction, $C_0(u) = R(T_u)$, the risk of the whole branch. Line L7 collapses, bottom-up, each $t$ with $R(t) = R(T_t)$, which does not change any $R(T_u)$; by Claim 2 this is the condition $D_0(t) \ge 0$. So the nodes left are those with no such ancestor, which is $T(0)$.

*(d) The weakest link.* Suppose $T_k = T(\alpha_k)$. For an internal node $t$ of $T_k$ with branch $T_{k,t}$ of $L_t \ge 2$ leaves,
$$R(t) + \alpha - R_\alpha(T_{k,t}) = (L_t - 1)\big(g(t) - \alpha\big), \qquad g(t) = \frac{R(t) - R(T_{k,t})}{L_t - 1}.$$
Since $t$ was not collapsed at $\alpha_k$, $R(t) + \alpha_k > C_{\alpha_k}(t_L) + C_{\alpha_k}(t_R) = R_{\alpha_k}(T_{k,t})$ by (a), so $g(t) > \alpha_k$, and $\alpha_{k+1} = \min_t g(t) > \alpha_k$. Now take $\alpha_k \le \alpha \le \alpha_{k+1}$. By (b), $T(\alpha) \subseteq T_k$, so we may compute $C_\alpha$ on prunings of $T_k$ only. Bottom-up over $T_k$, $g(t) \ge \alpha$ gives $R(t) + \alpha \ge R_\alpha(T_{k,t}) = C_\alpha(t_L) + C_\alpha(t_R)$, so $C_\alpha(t) = R_\alpha(T_{k,t})$, and the inequality is strict iff $g(t) > \alpha$. Hence for $\alpha < \alpha_{k+1}$ no node of $T_k$ is collapsed and $T(\alpha) = T_k$; at $\alpha = \alpha_{k+1}$ exactly the nodes with $g(t) = \alpha_{k+1}$ satisfy the collapse condition, and $T(\alpha_{k+1})$ is $T_k$ with all of them collapsed, which is $T_{k+1}$ of line L9.

By induction on $k$, $T_k = T(\alpha_k)$ for every $k$ and $T(\alpha) = T_k$ on $[\alpha_k, \alpha_{k+1})$. The sequence ends at the root alone, whose $T(\alpha)$ holds for all $\alpha \ge \alpha_K$. With (a) this proves the claim. $\blacksquare$

Line L10 only chooses one tree from this sequence, so the returned tree is a pruning of $T_{\max}$ that is optimal for some $\alpha$.
