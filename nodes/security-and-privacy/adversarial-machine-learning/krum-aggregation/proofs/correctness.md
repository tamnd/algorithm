---
title: Krum returns the update of smallest score, and that update is close to an honest one
proves: [correctness]
status: full
---

**Setting.** The input is $V_1, \ldots, V_n \in \mathbb{R}^d$ and an integer $f \ge 0$ with $n > 2f + 2$. Write $k = n - f - 2$, so $k \ge f + 1 \ge 1$. For $i \ne j$ let $d_{ij} = \lVert V_i - V_j \rVert^2$. The score is

$$s(i) = \min \Big\{ \sum_{j \in S} d_{ij} \ :\ S \subseteq \{1, \ldots, n\} \setminus \{i\},\ |S| = k \Big\}.$$

**Claim 1 (the computation).** Line L5 sets $s(i)$ to this minimum, and line L7 returns $V_{i^*}$ where $i^*$ is the smallest index with $s(i^*) = \min_i s(i)$.

*Proof.* Line L3 builds the list of the $n - 1$ values $d_{ij}$, $j \ne i$, and line L4 sorts it, so that $D[1] \le D[2] \le \cdots \le D[n-1]$. Let $S$ be any set of $k$ indices other than $i$, and list its values in increasing order as $e_1 \le \cdots \le e_k$. For each $t \le k$, at least $t$ entries of $D$ are at most $e_t$ (the values $e_1, \ldots, e_t$ themselves), so $D[t] \le e_t$. Summing over $t$ gives $D[1] + \cdots + D[k] \le \sum_{j \in S} d_{ij}$. The first $k$ entries of $D$ are themselves the values of one such set $S$. So line L5 computes the minimum $s(i)$. Line L6 replaces the current index only on a strict decrease, so after the loop of line L2 the kept index is the first index whose score equals the minimum, and line L7 returns its vector. Line L1 rejects every input with $n \le 2f + 2$, so no other input reaches lines L2 to L7. $\square$

**Claim 2 (closeness to an honest update).** Let $H \subseteq \{1, \ldots, n\}$ be a set of honest indices whose complement $B$ has $|B| \le f$. Let

$$\rho^2 = \min_{i \in H} \max_{j \in H} d_{ij}, \qquad \text{with } d_{ii} = 0 .$$

Then the index $i^*$ returned by Krum satisfies

$$\min_{j \in H} \lVert V_{i^*} - V_j \rVert^2 \ \le\ \frac{n - f - 2}{n - 2f - 1}\, \rho^2 .$$

*Proof.* If $i^* \in H$, the left side is $0$ and there is nothing to prove. So let $i^* \in B$, and let $c \in H$ be an index that attains $\rho^2$, so that $d_{cj} \le \rho^2$ for every $j \in H$.

*Upper bound on $s(c)$.* The honest indices other than $c$ number $|H| - 1 \ge n - f - 1 \ge k$. Take any $k$ of them as the set $S$ in the definition of $s(c)$. Each term is at most $\rho^2$, so $s(c) \le k \rho^2 = (n - f - 2) \rho^2$.

*Lower bound on $s(i^*)$.* Let $S^*$ be a set of $k$ indices other than $i^*$ that attains $s(i^*)$. The Byzantine indices other than $i^*$ number $|B| - 1 \le f - 1$, so $S^*$ holds at least $k - (f - 1) = n - 2f - 1$ honest indices. This count is positive because $n > 2f + 2$. Let $\delta^2 = \min_{j \in H} d_{i^* j}$. Each honest $j \in S^*$ has $d_{i^* j} \ge \delta^2$, and every term is nonnegative, so $s(i^*) \ge (n - 2f - 1) \delta^2$.

*Combination.* By Claim 1, $s(i^*) \le s(c)$. Hence $(n - 2f - 1) \delta^2 \le (n - f - 2) \rho^2$, and dividing by the positive number $n - 2f - 1$ gives the claim. $\square$

**Remarks.** The bound does not depend on the values of the Byzantine updates, on the dimension, or on any probability model; it is the deterministic core of the proof of Proposition 1 of Blanchard et al. (arXiv:1703.02757v1, Section 4), with the count $n - 2f - 1$ that holds for a Byzantine winner in place of their count $n - 2f - 2$, which holds for any index. The argument of Claim 2 uses only $n - 2f - 1 \ge 1$, that is $n \ge 2f + 2$; Krum itself, as defined by Blanchard et al. and in line L1, requires $n > 2f + 2$. The constant $\rho^2$ grows with the spread of the honest updates, which in dimension $d$ with per-coordinate noise $\sigma$ is of order $d \sigma^2$; the claim therefore says that the damage of a Byzantine winner is at most a constant times the honest noise, not that it is small. $\blacksquare$
