---
title: ALIBI-HEAD returns the causal softmax attention with scores q_i . k_j / sqrt(d_k) - m (i - j), the head equals one with the key-only bias m j, the bias depends only on i - j, and the weight at distance r is at most exp(2B - m r)
proves: [correctness]
status: full
---

We use the notation of the page. A head has slope $m \ge 0$, queries $q_1, \ldots, q_n$, keys $k_1, \ldots, k_n$ and values $v_1, \ldots, v_n$. For $j \le i$ write $a_{ij} = q_i \cdot k_j / \sqrt{d_k}$, and define the target output

$$o_i^\ast = \sum_{j \le i} \frac{e^{a_{ij} - m(i - j)}}{\sum_{l \le i} e^{a_{il} - m(i - l)}}\, v_j .$$

**Lemma 1 (the procedure).** ALIBI-HEAD returns $o_i = o_i^\ast$ for every $i$.

*Proof.* Fix $i$ at line L1. The loop at line L2 visits $j = 1, \ldots, i$, so line L3 sets $s_j = a_{ij} - m(i - j)$ for exactly the visible keys. Line L4 sets $p_j = e^{s_j} / \sum_{l \le i} e^{s_l}$, and line L5 forms $\sum_{j \le i} p_j v_j$, which is $o_i^\ast$. The rows do not share state, and line L6 returns all of them. $\square$

The code subtracts the row maximum $\mu$ before the exponentials. This multiplies the numerator and the denominator by $e^{-\mu}$ and does not change $p$.

**Lemma 2 (shift).** For real $s_1, \ldots, s_i$ and any real $c$, $\mathrm{softmax}(s_1 + c, \ldots, s_i + c) = \mathrm{softmax}(s_1, \ldots, s_i)$.

*Proof.* $e^{s_j + c} / \sum_l e^{s_l + c} = e^c e^{s_j} / (e^c \sum_l e^{s_l}) = e^{s_j} / \sum_l e^{s_l}$. $\square$

**Theorem 3 (key-only bias).** Let a second head use the scores $a_{ij} + m\,j$ for $j \le i$ and the causal mask. Its outputs equal those of ALIBI-HEAD.

*Proof.* In row $i$, $a_{ij} + m j = (a_{ij} - m(i - j)) + m i$, and $m i$ is the same for all $j$ in the row. By Lemma 2 the weights are the same, so the outputs are the same. $\square$

**Theorem 4 (distance only).** The bias $b(i, j) = -m(i - j)$ satisfies $b(i + t, j + t) = b(i, j)$ for every integer $t$. Hence if the queries and keys of positions $j, \ldots, i$ are moved to positions $j + t, \ldots, i + t$ and no other key is visible, the outputs are the same.

*Proof.* $(i + t) - (j + t) = i - j$. The scores of the moved rows are then the same numbers, and by Lemma 1 so are the outputs. $\square$

**Theorem 5 (decay).** Suppose $|a_{ij}| \le B$ for all $j \le i$. Then the weight of key $j$ in row $i$ satisfies $p_j \le e^{2B - m(i - j)}$.

*Proof.* The denominator of $p_j$ is a sum of positive terms that includes the term $l = i$, so it is at least $e^{a_{ii}} \ge e^{-B}$. The numerator is $e^{a_{ij} - m(i - j)} \le e^{B - m(i - j)}$. Dividing gives $p_j \le e^{2B - m(i - j)}$. $\blacksquare$

With a key-value cache, the queries are at positions $p_i = i + (M - n)$ among $M$ keys, and every statement above holds with $i$ replaced by $p_i$. The code computes this case, and for $n = M$ it is the case above.
