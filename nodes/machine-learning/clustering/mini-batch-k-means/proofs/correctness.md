---
title: Each center of mini-batch k-means is the mean of the samples it has received
proves: [correctness]
status: full
---

Fix a center $j$. Let $y_1, y_2, \ldots$ be the points that line L9 applies to center $j$, in this order, and let $c_j^{(v)}$ be the center after the $v$-th of these updates. Let $c_j^{(0)}$ be the initial center.

**Lemma 1 (count).** Just before the $v$-th update of center $j$, line L7 makes $v_j = v$.

*Proof.* Line L2 sets $v_j = 0$, and line L7 adds 1 exactly once before each update of center $j$ by line L9. No other line changes $v_j$. $\square$

**Theorem 1 (running mean).** For each $v \ge 1$, $c_j^{(v)} = \frac{1}{v}\sum_{l=1}^{v} y_l$.

*Proof.* By Lemma 1 the $v$-th update uses $\eta = 1/v$. For $v = 1$, $\eta = 1$ and $c_j^{(1)} = 0 \cdot c_j^{(0)} + y_1 = y_1$. For $v \ge 2$, by induction,
$$c_j^{(v)} = \Big(1 - \frac1v\Big) \frac{1}{v - 1}\sum_{l=1}^{v - 1} y_l + \frac1v y_v = \frac1v \sum_{l=1}^{v - 1} y_l + \frac1v y_v = \frac1v\sum_{l=1}^{v} y_l . \qquad \square$$

So the initial center has no effect on $c_j$ after the first update of $j$; it only affects which points go to $j$.

**Theorem 2 (a full batch is a Lloyd step).** If the counts are 0 and the batch $M$ holds each data point once, then after one iteration each center $j$ that is nearest to at least one point equals the mean of the points nearest to it (with ties broken as in line L5), and each other center is unchanged.

*Proof.* Line L5 computes $j(x)$ for all $x$ with the initial centers before any update. So the points applied to center $j$ are exactly $\{x : j(x) = j\}$. By Theorem 1 the center is then their mean. A center with no point is not updated. This is the update step of Lloyd's algorithm after one assignment step. $\square$

**Theorem 3 (the update is a gradient step).** Line L9 equals $c_j \leftarrow c_j - \eta \nabla_{c_j} \frac12\|x - c_j\|^2$.

*Proof.* The gradient is $c_j - x$, and $c_j - \eta(c_j - x) = (1 - \eta)c_j + \eta x$. $\square$

**Remark (no monotone decrease).** Take the points $0, 1, 10$ on a line with $k = 1$. After a first batch that holds only the point $10$, the center is $10$, with full cost $100 + 81 + 0 = 181$, while the initial center $0$ has cost $0 + 1 + 100 = 101$. So one iteration with $b = 1$ can raise the full cost. This is why the method is a heuristic without a descent property.
