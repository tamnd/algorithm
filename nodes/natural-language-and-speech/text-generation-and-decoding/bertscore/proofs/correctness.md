---
title: BERTScore computes the defined precision, recall and F1, and greedy matching is never below the best one-to-one matching
proves: [correctness]
status: full
---

Let the reference have token vectors $x_1, \ldots, x_n$ and the candidate $\hat x_1, \ldots, \hat x_m$ in $\mathbb{R}^d$, all nonzero, with $n, m \ge 1$. Let $w_i > 0$ and $\hat w_j > 0$ be the weights (all 1 without idf). The definitions of the paper are

$$R = \frac{\sum_i w_i \max_j \cos(x_i, \hat x_j)}{\sum_i w_i}, \qquad P = \frac{\sum_j \hat w_j \max_i \cos(x_i, \hat x_j)}{\sum_j \hat w_j}, \qquad F = \frac{2PR}{P + R}.$$

**Lemma 1.** After line L1, $S_{ij}$ of line L2 equals $\cos(x_i, \hat x_j)$.

*Proof.* Line L1 sets $u_i = x_i / \|x_i\|$ and $v_j = \hat x_j / \|\hat x_j\|$. Then $u_i \cdot v_j = (x_i \cdot \hat x_j) / (\|x_i\| \|\hat x_j\|) = \cos(x_i, \hat x_j)$. $\square$

**Theorem 1 (the output is the definition).** Lines L3 to L7 return $P$, $R$ and $F$ as defined, and $-1 \le P, R \le 1$.

*Proof.* By Lemma 1, $r_i = \max_j S_{ij}$ of line L3 is $\max_j \cos(x_i, \hat x_j)$, and $p_j$ of line L4 is $\max_i \cos(x_i, \hat x_j)$. Lines L5 and L6 are the weighted means of the definition, and line L7 is the formula for $F$. A cosine is in $[-1, 1]$ by the Cauchy-Schwarz inequality, and a weighted mean with positive weights of numbers in $[-1, 1]$ is in $[-1, 1]$. $\square$

**Theorem 2 (identity).** If the candidate is the reference, then $P = R = F = 1$.

*Proof.* For each $i$, $\max_j \cos(x_i, x_j) \ge \cos(x_i, x_i) = 1$, and no cosine is above 1, so $r_i = 1$. In the same way $p_j = 1$. Then $R = P = 1$ and $F = 2/2 = 1$. $\square$

**Theorem 3 (invariances).** $P$, $R$ and $F$ do not change if a token vector is multiplied by a positive number, or if the tokens of either side are permuted together with their weights. Exchanging the reference and the candidate (with their weights) exchanges $P$ and $R$ and keeps $F$.

*Proof.* The cosine does not change when a vector is scaled by $c > 0$. A permutation reorders the terms of the sums and the sets over which the maxima are taken, and neither changes the value. Exchanging the two sides turns the formula for $R$ into the formula for $P$ and back, and $F$ is symmetric in $P$ and $R$. $\square$

**Theorem 4 (greedy and one-to-one matching).** Let $n \le m$ and let $\sigma$ be any injective map from $\{1, \ldots, n\}$ to $\{1, \ldots, m\}$. Then $R \ge \frac{\sum_i w_i \cos(x_i, \hat x_{\sigma(i)})}{\sum_i w_i}$. Equality holds for the best $\sigma$ when the maxima $\arg\max_j \cos(x_i, \hat x_j)$ can be chosen pairwise distinct.

*Proof.* For each $i$, $\max_j \cos(x_i, \hat x_j) \ge \cos(x_i, \hat x_{\sigma(i)})$. Multiply by $w_i > 0$, add over $i$ and divide by $\sum_i w_i$. If the maxima $j_i$ are distinct, the map $\sigma(i) = j_i$ is injective and reaches the bound, so it is the best one-to-one matching. $\square$

**Theorem 5 (F lies between P and R).** If $P > 0$ and $R > 0$, then $\min(P, R) \le F \le \frac{P + R}{2} \le \max(P, R)$.

*Proof.* $F$ is the harmonic mean of $P$ and $R$. Write $a = \min(P, R)$ and $b = \max(P, R)$. Then $F - a = a(b - a)/(a + b) \ge 0$, and $\frac{a + b}{2} - F = \frac{(a + b)^2 - 4ab}{2(a + b)} = \frac{(b - a)^2}{2(a + b)} \ge 0$. $\square$

**Theorem 6 (rescaling keeps the order).** For a baseline $b < 1$, the map $s \mapsto (s - b)/(1 - b)$ is strictly increasing, maps $b$ to 0 and 1 to 1. So two candidates scored against the same reference keep their order, and the correlation with human scores at the system level or the segment level by a rank statistic does not change.

*Proof.* The map is affine with slope $1/(1 - b) > 0$. The two values follow by substitution. $\blacksquare$

**Remark (cost).** Line L1 takes $O((n + m)d)$ time, line L2 takes $O(nmd)$ time and $O(nm)$ space, and lines L3 to L7 take $O(nm)$ time. The network that makes the vectors costs much more and is outside the algorithm.
