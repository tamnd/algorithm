---
title: The K-best metrics are the ML metrics, K at least M^(n-1) gives ML, and K = 1 is ZF successive cancellation
proves: [correctness]
status: full
---

The model is $y = H x + w$ with $H \in \mathbb{C}^{m \times n}$ of full column rank and $x \in \mathcal{S}^n$, $|\mathcal{S}| = M$. Let $H^H H = R^H R$ with $R$ upper triangular with a positive diagonal (the Cholesky factor of line L1), let $\bar y$ solve $R^H \bar y = H^H y$, and let $c = \|y\|^2 - \|\bar y\|^2$.

**Theorem 1 (the triangular metric).** For every $x \in \mathbb{C}^n$, $\|y - H x\|^2 = \|\bar y - R x\|^2 + c$.

*Proof.* Expand both sides. $\|y - H x\|^2 = \|y\|^2 - 2 \,\mathrm{Re}(x^H H^H y) + x^H H^H H x$. Also $\|\bar y - R x\|^2 = \|\bar y\|^2 - 2 \,\mathrm{Re}(x^H R^H \bar y) + x^H R^H R x$. Now $R^H \bar y = H^H y$ and $R^H R = H^H H$, so the two expressions differ by $\|y\|^2 - \|\bar y\|^2 = c$. $\square$

For $1 \le i \le n$ define the level term

$$t_i(x_i, \ldots, x_n) = \Big|\bar y_i - \sum_{j > i} R_{ij} x_j - R_{ii} x_i\Big|^2 \ge 0,$$

and the partial metric $D_i = \sum_{l = i}^{n} t_l$, with $D_{n+1} = 0$. Because $R$ is upper triangular, row $i$ of $\bar y - R x$ is the expression inside $t_i$, so $\|\bar y - R x\|^2 = D_1$.

**Lemma 2 (partial metrics never decrease).** $D_i = D_{i+1} + t_i \ge D_{i+1}$, and $D_i$ depends only on $(x_i, \ldots, x_n)$.

*Proof.* Immediate from the definition, since $t_i \ge 0$ and $t_l$ for $l \ge i$ involves only $x_l, \ldots, x_n$. $\square$

**Invariant.** After the loop body for level $i$, every survivor is a pair $(D_i(v), v)$ with $v \in \mathcal{S}^{n - i + 1}$, and line L5 computes $D_i$ of each child correctly from $D_{i+1}$ of its parent. This follows from Lemma 2, because line L5 adds exactly $t_i$. So the metrics returned by line L7 are $D_1 + c = \|y - H x\|^2$ by Theorem 1.

**Theorem 3 (large K is exact ML).** If $K \ge M^{n-1}$, line L7 returns the $K$ vectors of $\mathcal{S}^n$ with the smallest metrics, in increasing order of metric, and the first one is an ML vector.

*Proof.* Before level $i$ is processed, there are at most $M^{n-i}$ partial vectors of length $n - i$. For $i \ge 2$, line L5 creates at most $M \cdot M^{n-i} = M^{n-i+1} \le M^{n-1} \le K$ candidates, so line L6 keeps all of them. By induction, before the last level ($i = 1$) the survivors are all $M^{n-1}$ vectors $(x_2, \ldots, x_n)$. Line L5 then creates all $M^n$ vectors with their exact metrics, and line L6 keeps the $K$ smallest. The first of them minimizes $\|y - H x\|^2$ over $\mathcal{S}^n$. $\square$

**Theorem 4 (K = 1 is ZF successive cancellation).** With $K = 1$, the K-best detector returns the decisions of ZF nulling and cancelling in the fixed order $x_n, x_{n-1}, \ldots, x_1$, with the nearest-point slicer (with the same tie rule).

*Proof.* With $K = 1$ there is one survivor. At level $i$ the candidates differ only in $x_i = s$, and $t_i = |u - R_{ii} s|^2 = R_{ii}^2 |u / R_{ii} - s|^2$ with $u = \bar y_i - \sum_{j > i} R_{ij} \hat x_j$. Since $D_{i+1}$ is common, line L6 keeps the $s$ nearest to $z_i = u / R_{ii}$.

Now compare with ZF nulling and cancelling. After the decisions $\hat x_{i+1}, \ldots, \hat x_n$ are cancelled, the residual is $r = y - \sum_{j > i} h_j \hat x_j$, and the ZF output for stream $i$ uses the first $i$ columns $H_i = [h_1, \ldots, h_i]$. Its value is the last entry of $(H_i^H H_i)^{-1} H_i^H r$. The leading $i \times i$ block $R_i$ of $R$ satisfies $H_i^H H_i = R_i^H R_i$, because the leading block of $R^H R$ involves only the leading block of $R$ when $R$ is upper triangular. So the ZF output is the last entry of $R_i^{-1} R_i^{-H} H_i^H r$. The first $i$ entries of $H^H r$ are $H_i^H r$, and

$$H^H r = H^H y - \sum_{j > i} H^H h_j \hat x_j = R^H \bar y - R^H R \hat x_{> i},$$

where $\hat x_{> i}$ is the vector with $\hat x_j$ in the positions $j > i$ and zeros elsewhere. Let $v = \bar y - R \hat x_{> i}$. The first $i$ entries of $R^H v$ are $R_i^H v_{1:i}$, because $R^H$ is lower triangular. So $R_i^{-H} H_i^H r = v_{1:i}$, and the ZF output is the last entry of $R_i^{-1} v_{1:i}$. Since $R_i$ is upper triangular, the last entry of $R_i^{-1} v_{1:i}$ is $v_i / R_{ii}$, and $v_i = \bar y_i - \sum_{j > i} R_{ij} \hat x_j = u$. So the ZF output is $z_i = u / R_{ii}$, the same value, and the two detectors slice the same number. $\square$

**Why pruning can fail.** Lemma 2 says a partial metric is a lower bound on the final metric of every completion. It does not bound the final metric from above. A path with a large partial metric at a high level can have small terms below, and a path with a small partial metric can have large terms below. When the ML path is not among the $K$ best at some level $i > 1$, it is pruned and never returns. The example on the page shows this for $K = 1$: the ML path has partial metric 0.578 at level 2, against 0.018 for the other path, but final metric 0.61, against 2.61.
