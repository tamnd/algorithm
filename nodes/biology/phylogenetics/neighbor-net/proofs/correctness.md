---
title: NeighborNet returns a circular order and the best nonnegative least squares weights for its circular splits
proves: [correctness]
status: full
---

**Setting.** $d$ is a symmetric matrix on $n$ taxa with zero diagonal. Lines L1 to L8 build a list `order` of the taxa. Lines L9 and L10 fit weights to the circular splits of that order. A split $A \mid B$ is *circular* for a circular order $x_0, x_1, \ldots, x_{n-1}$ if $A$ is a set of consecutive taxa around the circle. We write $\delta_S(p, q) = 1$ if the taxa $p$ and $q$ are on different sides of $S$, and $0$ otherwise. We prove three claims.

1. The list `order` holds each taxon exactly once.
2. The weights $w$ minimize $f(w) = \sum_{p < q} \big(\sum_S w_S \delta_S(p, q) - d(p, q)\big)^2$ over all $w \ge 0$, where $S$ runs over the circular splits of `order`.
3. If $d = \sum_S \lambda_S \delta_S$ with $\lambda \ge 0$ over the circular splits of `order`, then the result is exactly the splits with $\lambda_S > 0$ and the weights $\lambda_S$.

The claim that NeighborNet finds such an order for every circular metric is the consistency theorem of Bryant, Moulton and Spillner (2007). This file does not prove it. The tests check it on random circular metrics and tree metrics.

**Lemma 1 (the order).** Number the merges and reductions of lines L3 to L6 as events $1, 2, \ldots$, and let $\mathcal{C}_t$ be the list of clusters after event $t$. Each cluster is a chain of one or two nodes, and the reductions build chains of three or four nodes only for a moment. Undo the events in reverse order, as line L8 does for the reductions. Then for every $t$, after the events later than $t$ are undone, the cyclic list holds each node of $\mathcal{C}_t$ exactly once, and the nodes of each cluster of $\mathcal{C}_t$ are consecutive in it, in the chain order or in the reverse order.

*Proof.* Backward induction on $t$. For the last event, the loop of line L2 has stopped, so at most three nodes remain. Line L7 lists them cluster by cluster. Each node is there once, and each cluster of at most two nodes is consecutive, also across the end of the list, because a cycle of at most three nodes makes every pair adjacent.

Now assume the claim for $t$, and look at event $t$.

- If event $t$ is a reduction of the chain $x, y, z, r$ to $u, v, r$, where $r$ is an optional fourth node, then the block $u, v$ (possibly with $r$) is consecutive by the induction hypothesis. Line L8 replaces $u, v$ by $x, y, z$ in the same direction: if $v$ follows $u$, it writes $x, y, z$, and if $u$ follows $v$, it writes $z, y, x$. So the chain $x, y, z, r$ is consecutive. The other clusters do not change. Each of $x, y, z$ was removed from the distance table when $u, v$ were made, so none of them is in the list before this step, and each node still occurs once.
- If event $t$ is the merge of lines L3 to L5, which puts the chains $C_i$ and $C_j$ end to end, nothing is undone. The merged chain is consecutive, so its two parts $C_i$ and $C_j$ are consecutive.

At $t = 0$, the clusters are the $n$ taxa, so the list holds each taxon once. $\square$

**Lemma 2 (the circular splits are a basis).** Let $x_0, \ldots, x_{n-1}$ be the order, with indices modulo $n$, and let $S_{ij}$ be the split with side $\{x_i, \ldots, x_j\}$ for $1 \le i \le j \le n - 1$. These are $\binom{n}{2}$ distinct splits, and every circular split is one of them. If $D = \sum \lambda_{ij} \delta_{S_{ij}}$, then

$$2 \lambda_{ij} = D(x_{i-1}, x_j) + D(x_i, x_{j+1}) - D(x_i, x_j) - D(x_{i-1}, x_{j+1}),$$

where $D(x, x) = 0$. So the matrix with one row per pair of taxa and one column per circular split, the design matrix of line L9, is square and invertible.

*Proof.* A circular split has an interval side, and of its two sides exactly one avoids $x_0$. That side is an interval of $x_1, \ldots, x_{n-1}$, so it is $\{x_i, \ldots, x_j\}$ for one pair $i \le j$. Different pairs give different sides, so there are $\binom{n}{2}$ of them, which is also the number of pairs of taxa.

For a split $S$, put $\sigma(x) = 1$ on one side and $-1$ on the other. Then $\delta_S(p, q) = \frac{1}{2}(1 - \sigma(p) \sigma(q))$, also for $p = q$. Apply the combination on the right of the formula to $\delta_S$. The constant terms cancel, and we get

$$-\tfrac{1}{2}\big(\sigma(x_{i-1}) \sigma(x_j) + \sigma(x_i) \sigma(x_{j+1}) - \sigma(x_i) \sigma(x_j) - \sigma(x_{i-1}) \sigma(x_{j+1})\big) = -\tfrac{1}{2}\big(\sigma(x_{i-1}) - \sigma(x_i)\big)\big(\sigma(x_j) - \sigma(x_{j+1})\big).$$

This is nonzero only if $\sigma$ changes between $x_{i-1}$ and $x_i$ and also between $x_j$ and $x_{j+1}$. A circular split changes sides at exactly two places around the circle, so it must change exactly there, and $S = S_{ij}$. In that case $\sigma(x_i) = \sigma(x_j) = s$ and $\sigma(x_{i-1}) = \sigma(x_{j+1}) = -s$, and the value is $-\frac{1}{2}(-2s)(2s) = 2$. By linearity, the combination applied to $D$ gives $2 \lambda_{ij}$. So the map from $\lambda$ to $D$ is one to one, and a square matrix with this property is invertible. $\square$

**Lemma 3 (one active set step).** Let $G = A^\top A$ and $g(w) = A^\top b - G w$, so that $\nabla f(w) = -2 g(w)$. Let $P$ be a set of columns, let $w \ge 0$ be zero outside $P$ and minimize $f$ over the vectors that are zero outside $P$, and let $k \notin P$ with $g_k(w) > 0$. Then the minimizer $z$ of $f$ over the vectors that are zero outside $P \cup \{k\}$ is unique and has $z_k > 0$.

*Proof.* By Lemma 2 the columns of $A$ are independent, so $f$ is strictly convex on every coordinate subspace, and $z$ is unique. For a real $t$, let $\varphi(t)$ be the minimum of $f$ over the vectors that are zero outside $P \cup \{k\}$ and have $k$-th entry $t$. A partial minimum of a convex function is convex, so $\varphi$ is convex, and $\varphi(0) = f(w)$. The derivative of $f(w + t e_k)$ at $t = 0$ is $-2 g_k(w) < 0$, so there is $s > 0$ with $\varphi(s) \le f(w + s e_k) < \varphi(0)$. The entry $z_k$ minimizes $\varphi$. If $z_k \le 0$, then $0$ lies between $z_k$ and $s$, and convexity gives $\varphi(0) \le \max(\varphi(z_k), \varphi(s)) = \varphi(s) < \varphi(0)$, which is false. $\square$

**Lemma 4 (Lawson and Hanson).** The function `nnls` stops, and its result $w$ satisfies $w \ge 0$, $g_i(w) = 0$ for $w_i > 0$, and $g_i(w) \le 0$ for all $i$.

*Proof.* We show that at the top of each outer loop, $w \ge 0$, $w$ is positive exactly on `passive`, and $w$ minimizes $f$ over the vectors that are zero outside `passive`. At the start, `passive` is empty and $w = 0$, so this holds.

Assume it holds, and let $k$ be the chosen column, with $g_k(w) > 0$. In the inner loop, $z$ is the minimizer on the current set. If all its passive entries are positive, the loop sets $w = z$ and the invariant holds again. Otherwise, let $\theta = \min w_i / (w_i - z_i)$ over the passive $i$ with $z_i \le 0$. In the first pass, $z_k > 0$ by Lemma 3, so $k$ is not in this minimum, and the other passive entries of $w$ are positive. In later passes, all passive entries of $w$ are positive. So each term has $w_i > 0$ and $z_i \le 0$, and $0 < \theta \le 1$. The new point $w + \theta (z - w)$ is nonnegative, with a zero entry at each $i$ that attains the minimum, and these entries leave `passive`. Each pass that does not stop removes at least one column, so the inner loop stops, and the invariant holds at its end.

The value of $f$ goes down strictly in each outer loop. In the first inner pass, either $w$ becomes $z$, or it moves a positive distance toward $z$. In both cases, $f(z) < f(w)$ by Lemma 3, and convexity gives a strictly smaller value. Later passes and the final minimization on the passive set do not increase $f$. At the top of each outer loop, $f(w)$ is the minimum of $f$ over the subspace of `passive`, which depends only on the set. A strictly decreasing sequence of such values never repeats a set, and there are finitely many sets, so the outer loop stops. It stops only when $g_i(w) \le 0$ for every $i$ outside `passive`. For $i$ in `passive`, $g_i(w) = 0$, because $w$ minimizes $f$ on that subspace. $\square$

**Theorem.** Claims 1, 2 and 3 hold.

*Proof.* Claim 1 is Lemma 1 at $t = 0$. For claim 2, let $w$ be the result of `nnls` and $v \ge 0$ any vector. Since $f$ is convex,

$$f(v) - f(w) \ge \nabla f(w) \cdot (v - w) = -2 \sum_i g_i(w) v_i + 2 \sum_i g_i(w) w_i.$$

By Lemma 4, every $g_i(w) v_i \le 0$, and every $g_i(w) w_i = 0$, so $f(v) \ge f(w)$. Line L10 drops only the splits with weight zero, which do not change the fitted distances. For claim 3, the vector $\lambda$ is nonnegative and gives $f(\lambda) = 0$, so it is a minimizer, and by Lemma 2 the minimizer is unique. So $w = \lambda$. $\blacksquare$
