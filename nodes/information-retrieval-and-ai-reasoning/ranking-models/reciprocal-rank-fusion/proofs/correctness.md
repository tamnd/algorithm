---
title: RRF computes its formula, keeps the order of one list, and becomes the total-rank order for large k
proves: [correctness]
status: full
---

Let $L_1, \ldots, L_m$ be the input rankings. Each holds distinct documents, best first, and may be partial. For a ranking $L$ that holds $d$, $L(d)$ is its rank, from 1. Let $k > 0$ be the constant. The RRF score is

$$s(d) = \sum_{l \,:\, d \in L_l} \frac{1}{k + L_l(d)}.$$

**Lemma 1 (the code computes $s$).** After lines L1 to L4, the map holds exactly the documents that appear in at least one ranking, each with the value $s(d)$, and line L5 returns them by decreasing $s$, with ties broken by the document id.

*Proof.* Line L1 starts with an empty map. Invariant of the loop of line L2: after the first $j$ rankings, the map holds the documents of $L_1, \ldots, L_j$, each with the sum of $1/(k + L_l(d))$ over the $l \le j$ with $d \in L_l$. It holds for $j = 0$. Lines L3 and L4 visit each document of $L_{j+1}$ once, with its rank, and add $1/(k + L_{j+1}(d))$ to its entry, creating it with value 0 if needed. So the invariant holds for $j + 1$, and for $j = m$ it is the claim. The scores are exact fractions in the code, so the comparison in line L5 has no rounding error. $\square$

**Lemma 2 (one ranking).** With $m = 1$, line L5 returns $L_1$ unchanged.

*Proof.* $1/(k + i)$ is strictly decreasing in $i$, so the scores strictly decrease down the list and no tie occurs. $\square$

**Lemma 3 (agreement).** If every ranking that holds $y$ also holds $x$ and ranks $x$ above $y$, and some ranking holds $x$, then $s(x) > s(y)$.

*Proof.* For each ranking that holds $y$, its term for $x$ is strictly larger than its term for $y$. The rankings that hold $x$ but not $y$ add a positive amount to $s(x)$ only. If no ranking holds $y$, $s(y) = 0 < s(x)$. $\square$

So RRF never puts a document below another document that every relevant ranking places it above: it is unanimous in the sense of the Pareto rule.

**Theorem 1 (large $k$).** Let all $m$ rankings be full rankings of the same $n$ documents, and let $R(d) = \sum_l L_l(d)$ be the total rank of $d$. If $k > m n^2$, then $R(x) < R(y)$ implies $s(x) > s(y)$. So for such $k$, line L5 orders the documents by increasing total rank, which is the Borda order, with ties in $R$ left to the tie rule.

*Proof.* Write $\frac{1}{k + r} = \frac{1}{k} \left( 1 - \frac{r}{k + r} \right)$. Then $s(d) = \frac{1}{k} (m - g(d))$ with $g(d) = \sum_l \frac{L_l(d)}{k + L_l(d)}$. Since $1 \le L_l(d) \le n$, each term satisfies $\frac{L_l(d)}{k + n} \le \frac{L_l(d)}{k + L_l(d)} \le \frac{L_l(d)}{k}$, so

$$\frac{R(d)}{k + n} \le g(d) \le \frac{R(d)}{k}.$$

Let $R(x) < R(y)$; the ranks are integers, so $R(y) \ge R(x) + 1$. Then $g(x) \le R(x)/k$ and $g(y) \ge (R(x) + 1)/(k + n)$. Now $R(x)/k < (R(x) + 1)/(k + n)$ is equivalent to $R(x)(k + n) < (R(x) + 1) k$, that is, to $n R(x) < k$. Since $R(x) \le m n$, this holds when $k > m n^2$. So $g(x) < g(y)$ and $s(x) > s(y)$. $\square$

**Remark (small $k$ is not the total-rank order).** For finite $k$ the two orders can differ. With $k = 60$ and two rankings, a document $x$ at ranks 1 and 41 has total rank 42 and score $1/61 + 1/101 \approx 0.026294$, while a document $y$ at ranks 20 and 20 has total rank 40 and score $2/80 = 0.025$. So $x$ is above $y$, although $y$ has the smaller total rank. This is the intended effect: a top rank in one list counts for more than a uniform middle rank.

**Remark (depth).** Cutting each ranking to its first $c$ documents before line L2 removes every term with $L_l(d) > c$. The cut scores are therefore the full scores minus a nonnegative amount, and the order can change. On the toy runs of the page, the full fusion is $1, 2, 8, 4, 6, 7$ and the fusion at depth 2 is $1, 2, 6$.

The tests in `impl/python/test_reciprocal_rank_fusion.py` check Lemma 1 against a direct computation of the sum, Theorem 1 with $k = m n^2 + 1$ on random full rankings, the two remarks, and the toy runs.
