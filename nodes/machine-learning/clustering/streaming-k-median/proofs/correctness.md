---
title: The multi-level streaming k-median has cost at most ((1 + 2c)(1 + 2b)^L - 1) times the optimum
proves: [correctness]
status: full
---

We use the pseudocode of the page. The points lie in a metric space $(X, d)$. The stream is a multiset $S$ of $n$ points of weight 1. A weighted point set is a multiset of pairs $(y, w)$ with $w > 0$; its cost with centers $C$ is $\sum w\, d(y, C)$, where $d(y, C) = \min_{c \in C} d(y, c)$. Let $\mathrm{OPT}^*$ be the least cost of $S$ with $k$ centers anywhere in $X$, and $\mathrm{OPT} \ge \mathrm{OPT}^*$ the least cost with $k$ centers taken from $S$. The local solver is a $b$-approximation for the discrete weighted problem (the centers are among the given weighted points) on the buffers, and a $c$-approximation in the final step. The single-swap local search has $b = c = 5$ (Arya et al. 2004, whose proof holds with weights); the exact solver has $b = c = 1$.

**Lemma 1 (bookkeeping).** At all times each original point $x$ is represented by exactly one buffered point $y(x)$, and the weight of a buffered point is the number of original points that it represents. Each buffer holds fewer than $m$ points after each insertion.

*Proof.* Line L2 adds $x$ with weight 1 at level 0. When a buffer is full, line L4 replaces its points by medians; each point goes to exactly one median, and the weight of a median is the sum of the weights of its points, so the represented sets are joined. Line L3 empties a buffer as soon as it has $m$ points, and line L5 sends at most $k < m$ medians one level up, where the same rule applies. $\square$

Follow one original point $x$. It starts as $y_0(x) = x$. Each time its representative is in a reduction at level $i$, the representative moves from $y_i(x)$ to the median $y_{i+1}(x)$ that serves it. Let $L$ be the number of levels at which a reduction took place. Then $x$ passes at most $L$ reductions. Let $A_i$ be the total cost of all reductions at level $i$, that is, $A_i = \sum_x d(y_i(x), y_{i+1}(x))$ over the points $x$ whose representative was reduced at level $i$ (a weighted point of weight $w$ counts $w$ times). Let $P_i = A_0 + \cdots + A_{i-1}$, with $P_0 = 0$.

**Lemma 2 (moving to a piece).** Let $Q$ be a weighted point set and $O^*$ a set of $k$ points of $X$. Then the least cost of $Q$ with $k$ centers from $Q$ is at most $2 \sum_{(y, w) \in Q} w\, d(y, O^*)$.

*Proof.* For each $o \in O^*$ that serves some point of $Q$, let $q(o)$ be the point of $Q$ nearest to $o$. For a point $y$ served by $o$, $d(y, q(o)) \le d(y, o) + d(o, q(o)) \le 2 d(y, o)$. These at most $k$ points of $Q$ give the bound. $\square$

**Lemma 3 (one level).** $A_i \le 2b(\mathrm{OPT}^* + P_i)$ for each level $i$.

*Proof.* Let $O^*$ be an optimal set of $k$ centers for $S$ in $X$. A reduction of a buffer $Q$ at level $i$ costs at most $b$ times the discrete optimum of $Q$, which by Lemma 2 is at most $2\sum_{(y, w) \in Q} w\, d(y, O^*)$. The weighted point $y = y_i(x)$ stands for the original points $x$ that it represents, and for each of them, by the triangle inequality,
$$d(y_i(x), O^*) \le d(x, O^*) + d(x, y_i(x)) \le d(x, O^*) + \sum_{j < i} d(y_j(x), y_{j+1}(x)).$$
Each original point is in at most one buffer that is reduced at level $i$, because its representative leaves level $i$ after the reduction. Summing over all reductions at level $i$ gives $A_i \le 2b\left(\sum_x d(x, O^*) + \sum_{j < i} A_j\right) = 2b(\mathrm{OPT}^* + P_i)$. $\square$

**Lemma 4 (all levels).** $\mathrm{OPT}^* + P_L \le (1 + 2b)^L\, \mathrm{OPT}^*$.

*Proof.* By Lemma 3, $\mathrm{OPT}^* + P_{i+1} = \mathrm{OPT}^* + P_i + A_i \le (1 + 2b)(\mathrm{OPT}^* + P_i)$. Start from $P_0 = 0$ and use induction on $i$. $\square$

**Theorem.** Let $C$ be the medians that line L7 returns. Then
$$\sum_{x \in S} d(x, C) \le \big((1 + 2c)(1 + 2b)^L - 1\big)\, \mathrm{OPT}^* \le \big((1 + 2c)(1 + 2b)^L - 1\big)\, \mathrm{OPT}.$$

*Proof.* Let $F$ be the final pool of line L6. By Lemma 1, each $x$ has its representative $y(x) = y_t(x)$ in $F$ for some $t \le L$. The final step is a $c$-approximation for $F$, and by Lemma 2 and the triangle inequality as in Lemma 3, $\mathrm{cost}(F, C) \le 2c \sum_x d(y(x), O^*) \le 2c(\mathrm{OPT}^* + P_L)$. For each $x$, $d(x, C) \le d(x, y(x)) + d(y(x), C) \le \sum_{j < t} d(y_j(x), y_{j+1}(x)) + d(y(x), C)$. Summing over $x$ gives
$$\sum_x d(x, C) \le P_L + \mathrm{cost}(F, C) \le P_L + 2c(\mathrm{OPT}^* + P_L) = (1 + 2c)(\mathrm{OPT}^* + P_L) - \mathrm{OPT}^*,$$
and Lemma 4 finishes the proof. $\blacksquare$

**Constants.** For $L = 1$ the factor is $2b + 2c + 4bc$, which is the factor $2c(1 + 2b) + 2b$ of Theorem 4 of Guha et al. (2003). With the exact solver ($b = c = 1$) the factor is $3^{L+1} - 1$, which is 8 for one level. With single-swap local search ($b = c = 5$) it is $11^{L+1} - 1$, which is 120 for one level and 1330 for two. For a stream of length $n$ and buffer size $m$, level $i$ receives at most $n (k/m)^i$ weighted points, so $L \le \lceil \log(n/m) / \log(m/k) \rceil + 1$. With $m = n^{\varepsilon}$ and $k \le m^{1/2}$ this is $O(1/\varepsilon)$ levels, so the factor is a constant $2^{O(1/\varepsilon)}$ for constant $\varepsilon$, as in Theorem 6 of Guha et al.
