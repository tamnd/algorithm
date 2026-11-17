---
title: The MDD tree is well defined, ends, and gives a probability distribution
proves: [correctness]
status: full
---

Let $D$ be a non-empty list of $N$ aligned sites of length $p$ over $\Sigma = \{A, C, G, T\}$, let $c$ be a consensus string of length $p$, let $R \subseteq \{0, \ldots, p - 1\}$ be the positions to model, and let $\kappa$ (the cutoff), $m \ge 1$ (the minimum subset size) and $\alpha > 0$ (the pseudocount) be fixed.

**Lemma 1 (the statistic).** For positions $i \ne j$, the statistic $\chi^2(C_i, X_j)$ of line L2 is at least 0, and it is 0 if and only if the empirical distribution of the base $x_j$ is the same among the sites with $x_i = c_i$ and among the others (when both groups are non-empty).

*Proof.* The statistic is $\sum (O - E)^2 / E$ over the cells of the $2 \times 4$ table with $E > 0$, where $E = (\text{row total})(\text{column total}) / N$. Each term is at least 0. A cell with $E = 0$ lies in an empty row or column, so its count $O$ is 0 too. The sum is 0 if and only if $O = E$ in every cell, that is, if and only if every count equals the product of its row and column totals divided by $N$, which is the stated equality of the two conditional distributions. $\square$

**Lemma 2 (termination and partition).** The recursion ends, the tree has depth at most $|R| - 1$, and the sets of sites at the leaves form a partition of $D$.

*Proof.* Each split (line L7) removes the position $i^*$ from $R$ for both children, and a node with $|R| \le 1$ is a leaf (line L1). So along any path $|R|$ drops by 1 at each level, and the depth is at most $|R| - 1$. A split puts each site of its set into exactly one child, according to whether $x_{i^*} = c_{i^*}$ (line L5). By induction on the depth, the sets at the leaves under a node partition the set of that node. $\square$

**Lemma 3 (the choice of the split).** At a node that is split, $i^*$ maximizes $S_i = \sum_{j \in R, j \ne i} \chi^2(C_i, X_j)$ over $i \in R$, with ties broken by the smaller position; some pair of $R$ has a statistic above $\kappa$; and both parts have at least $m$ sites.

*Proof.* Line L3 returns a leaf if no statistic exceeds $\kappa$, and line L6 returns a leaf if a part is smaller than $m$. Otherwise line L4 chooses $i^*$ by the largest pair $(S_i, -i)$. $\square$

**Theorem (a probability distribution).** For every node $v$ with position set $R_v$, the function $P_v$ defined by

$$P_v(x) = \prod_{j \in R_v} w_v[j](x_j) \text{ if } v \text{ is a leaf}, \qquad P_v(x) = q_v(x_{i}) \, P_{v'}(x) \text{ if } v \text{ splits on } i,$$

where $v'$ is the child that $x_i = c_i$ selects, depends only on the bases of $x$ at $R_v$, satisfies $P_v(x) > 0$, and sums to 1 over the $4^{|R_v|}$ choices of these bases.

*Proof.* Every distribution $w_v[j]$ and $q_v$ is $(\text{count} + \alpha)/(|D_v| + 4\alpha)$ with $\alpha > 0$, so it is positive and sums to 1 over $\Sigma$. By induction on the height of $v$. For a leaf, the sum of the product over all $x \in \Sigma^{R_v}$ factors into $\prod_{j} \sum_{b} w_v[j](b) = 1$. For a split on $i$, both children have the position set $R_v \setminus \{i\}$. Fix the base $b$ at $i$. The child $v'$ is then fixed (the match child if $b = c_i$, the other child if not), and by the induction hypothesis the sum of $P_{v'}$ over the bases at $R_v \setminus \{i\}$ is 1. So the total is $\sum_{b} q_v(b) \cdot 1 = 1$. $\square$

So the root defines a proper probability model of the sites, and $\ln P$ (lines L8 and L9) is the sum of the logarithms of the factors along the path from the root to the leaf that $x$ selects, which can be used in a log-likelihood ratio against a background model.

**Running time.** At a node with $|D_v| = N_v$ sites and $r = |R_v|$ positions, line L2 fills $r(r - 1)$ tables with one pass over the sites each, in $O(r^2 N_v)$ time, and the rest of the node costs $O(r^2 + r N_v)$. The nodes of one depth have disjoint sets of sites (Lemma 2), so one depth costs $O(p^2 N)$, and with at most $p$ depths the build takes $O(p^3 N)$ time. If the root is a leaf, the time is $\Theta(p^2 N)$. Scoring a site follows one path of length at most $p - 1$ and multiplies at most $p$ factors in total, so it takes $O(p)$ time.
