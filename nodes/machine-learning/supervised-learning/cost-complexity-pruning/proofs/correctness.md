---
title: Each alpha has a unique smallest optimal pruned subtree, these subtrees are nested, and the weakest-link algorithm lists all of them
proves: [correctness, termination]
status: full
---

Let $T$ be a finite rooted tree. Each node $t$ has a risk $R(t) \ge 0$, its risk as a leaf. We assume the *monotone* condition: for every internal node $t$, $R(t) \ge \sum_{u \text{ child of } t} R(u)$. Resubstitution risks satisfy it: the misclassification count and the sum of squared errors of a set are at least the sums over any partition of it, because one constant for all parts is a feasible choice of a constant for each part.

A *pruned subtree* (pruning) $T'$ of $T$ is a subtree with the same root such that each node of $T'$ has either all its children in $T'$ or none. For $\alpha \ge 0$, $R_\alpha(T') = R(T') + \alpha\, |\tilde T'|$, where $\tilde T'$ is the set of leaves of $T'$ and $R(T') = \sum_{u \in \tilde T'} R(u)$. Write $T_t$ for the branch of $T$ at $t$, and $T' \preceq T''$ when $T'$ is a pruning of $T''$, that is, $T'$ is contained in $T''$.

**The recursion.** Let $C_\alpha(t) = \min \{R_\alpha(T') : T' \preceq T_t\}$. A pruning of $T_t$ is either $\{t\}$ or $t$ together with an independent pruning of each child branch, and $R_\alpha$ adds over disjoint branches. So $C_\alpha(t) = R(t) + \alpha$ at a leaf, and at an internal node
$$C_\alpha(t) = \min\Big(R(t) + \alpha,\ \sum_{u} C_\alpha(u)\Big), \qquad D_\alpha(t) = \sum_u C_\alpha(u) - R(t) - \alpha,$$
with the sums over the children $u$ of $t$. Define $T(\alpha)$ as the set of nodes $t$ such that no proper ancestor $s$ of $t$ has $D_\alpha(s) \ge 0$. This is the tree that SMALLEST-OPTIMAL returns: it makes $t$ a leaf when $R(t) + \alpha \le \sum_u C_\alpha(u)$.

**Theorem 1 (smallest optimal subtree; Breiman et al. 1984, Chapter 3).** For each $\alpha \ge 0$, $T(\alpha)$ minimizes $R_\alpha$ over all prunings of $T$, and $T(\alpha) \preceq T'$ for every minimizer $T'$. So the smallest minimizer is unique.

*Proof.* We show by induction on the height of $t$ that $T(\alpha)_t$, the part of $T(\alpha)$ in $T_t$ computed with the same rule, attains $C_\alpha(t)$ and is contained in every pruning of $T_t$ that attains it. At a leaf both are $\{t\}$. At an internal node, if $D_\alpha(t) \ge 0$, then $T(\alpha)_t = \{t\}$ attains $R(t) + \alpha = C_\alpha(t)$, and $\{t\}$ is contained in every pruning. If $D_\alpha(t) < 0$, then $\{t\}$ costs more than $C_\alpha(t)$, so every minimizer keeps the children of $t$ and restricts to a minimizer on each child branch, which by induction contains $T(\alpha)_u$. And $T(\alpha)_t$, which is $t$ with all $T(\alpha)_u$, attains $\sum_u C_\alpha(u) = C_\alpha(t)$. $\square$

**Theorem 2 (nesting).** If $0 \le \alpha \le \beta$, then $T(\beta) \preceq T(\alpha)$.

*Proof.* Every pruning has at least one leaf, so $R_\beta(T') \ge R_\alpha(T') + (\beta - \alpha)$ for each $T'$, and taking minima, $C_\beta(u) \ge C_\alpha(u) + (\beta - \alpha)$ for each node $u$. An internal node has at least two children, so $D_\beta(t) \ge D_\alpha(t) + 2(\beta - \alpha) - (\beta - \alpha) \ge D_\alpha(t)$. Let $t \in T(\beta)$. Each proper ancestor $s$ of $t$ has $D_\beta(s) < 0$, so $D_\alpha(s) < 0$, and $t \in T(\alpha)$. $\square$

So $T(\alpha)$, as $\alpha$ grows from 0, is a nested family that changes only at finitely many values, since $T$ has finitely many prunings.

**Theorem 3 (the weakest-link algorithm).** Let $T_1 \succeq T_2 \succeq \cdots \succeq T_K$ and $0 = \alpha_1 < \alpha_2 < \cdots < \alpha_K$ be the output of lines L1 to L5. Then $T(\alpha) = T_k$ for all $\alpha \in [\alpha_k, \alpha_{k+1})$, where $\alpha_{K+1} = \infty$, and $T_K$ is the root alone.

*Proof.* *Start.* By the monotone condition and induction, $C_0(u) = R(T_u)$: the full branch has the least risk. So $D_0(t) = R(T_t) - R(t) \le 0$, with equality iff $R(t) = R(T_t)$. Line L1 collapses, bottom-up, exactly the nodes with $R(t) = R(T_t)$; collapsing such a node does not change the risk of any branch that contains it, so the test at each later node is the same as on the full tree. Hence $T_1 = T(0) = T(\alpha_1)$.

*Step.* Suppose $T_k = T(\alpha_k)$ and $T_k$ has an internal node. For an internal node $t$ of $T_k$, let $T_{k,t}$ be its branch in $T_k$, with $L_t \ge 2$ leaves, and
$$g(t) = \frac{R(t) - R(T_{k,t})}{L_t - 1}, \quad\text{so that}\quad R(t) + \alpha - R_\alpha(T_{k,t}) = (L_t - 1)\big(g(t) - \alpha\big).$$
By Theorem 1, $T_{k,t} = T(\alpha_k)_t$ attains $C_{\alpha_k}(t)$ and $t$ is not collapsed, so $R(t) + \alpha_k > R_{\alpha_k}(T_{k,t})$ and $g(t) > \alpha_k$. Lines L3 and L4 set $\alpha_{k+1} = \min_t g(t) > \alpha_k$.

Take $\alpha \in [\alpha_k, \alpha_{k+1}]$. By Theorem 2, $T(\alpha) \preceq T_k$, so $T(\alpha)$ is also the smallest minimizer over the prunings of $T_k$, and we may run the recursion on $T_k$. We claim that $C_\alpha(t) = R_\alpha(T_{k,t})$ for every node $t$ of $T_k$, with $D_\alpha(t) \ge 0$ iff $g(t) = \alpha$. At a leaf of $T_k$ this is clear. At an internal node, by induction $\sum_u C_\alpha(u) = \sum_u R_\alpha(T_{k,u}) = R_\alpha(T_{k,t})$, and $R(t) + \alpha - R_\alpha(T_{k,t}) = (L_t - 1)(g(t) - \alpha) \ge 0$ because $g(t) \ge \alpha_{k+1} \ge \alpha$. So $C_\alpha(t) = R_\alpha(T_{k,t})$, and $D_\alpha(t) = -(L_t - 1)(g(t) - \alpha)$ is $\ge 0$ iff $g(t) = \alpha$.

For $\alpha < \alpha_{k+1}$ no node has $g(t) = \alpha$, so nothing is collapsed and $T(\alpha) = T_k$. For $\alpha = \alpha_{k+1}$, $T(\alpha)$ is $T_k$ with every node of $g(t) = \alpha_{k+1}$ collapsed (a collapsed node below another collapsed node does not matter), which is $T_{k+1}$ of line L5.

*End.* Each step collapses at least one internal node, so the loop stops after fewer than $|T|$ steps, at the root alone. $T(\alpha) \preceq T_K$ for $\alpha \ge \alpha_K$, so $T(\alpha) = T_K$ there. $\blacksquare$

**Corollary (cost).** Each step of lines L3 to L5 is one postorder pass over $T_k$, which computes $R(T_{k,t})$, $L_t$ and $g(t)$ for all $t$ in $O(|T|)$ time. There are at most $|T|$ steps, so the sequence costs $O(|T|^2)$ in the worst case, and SMALLEST-OPTIMAL for one $\alpha$ costs $O(|T|)$.

**Cross-validation.** Lines L6 to L8 only choose an index $k$, so by Theorem 3 the returned tree is $T(\alpha)$ for every $\alpha$ in $[\alpha_k, \alpha_{k+1})$: an optimal pruning for some cost per leaf.
