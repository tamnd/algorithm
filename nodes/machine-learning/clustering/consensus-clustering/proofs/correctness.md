---
title: The reduction to correlation clustering and the guarantees of consensus clustering
proves: [correctness]
status: full
---

We use the pseudocode of the page. The inputs are partitions $P_1, \ldots, P_m$ of $V$, $|V| = n$, with $m \ge 1$. For a partition $P$ let $J(P)$ be the set of unordered pairs that $P$ joins. The distance is $d(P, Q) = |J(P) \,\triangle\, J(Q)|$ and $D(P) = \sum_i d(P, P_i)$. $\mathrm{OPT} = \min_P D(P)$ over all partitions of $V$.

**Lemma 1 (d is a metric).** For partitions $P, Q, S$: $d(P, Q) \ge 0$ with equality iff $P = Q$; $d(P, Q) = d(Q, P)$; and $d(P, S) \le d(P, Q) + d(Q, S)$.

*Proof.* $d$ is the Hamming distance between the indicator vectors of $J(P)$ and $J(Q)$ over the $\binom{n}{2}$ pairs, which is a metric on these vectors. A partition is determined by $J(P)$ (its clusters are the classes of the relation "equal or joined"), so $d(P, Q) = 0$ forces $P = Q$. $\square$

**Lemma 2 (the reduction).** Let $w^+_{uv} = |\{i : uv \in J(P_i)\}|/m$ and $w^-_{uv} = 1 - w^+_{uv}$. For every partition $P$,

$$D(P) = m \Bigl( \sum_{uv \notin J(P)} w^+_{uv} + \sum_{uv \in J(P)} w^-_{uv} \Bigr).$$

*Proof.* Write $D(P) = \sum_i \sum_{uv} [\,uv \in J(P) \,\triangle\, J(P_i)\,] = \sum_{uv} c_{uv}$ with $c_{uv} = |\{i : \text{exactly one of } P, P_i \text{ joins } uv\}|$. If $P$ splits $uv$, then $c_{uv}$ counts the $i$ with $uv \in J(P_i)$, that is $m w^+_{uv}$. If $P$ joins $uv$, then $c_{uv}$ counts the $i$ with $uv \notin J(P_i)$, that is $m - m w^+_{uv} = m w^-_{uv}$. $\square$

So a partition is a median iff it is an optimum of weighted correlation clustering with the weights $(w^+, w^-)$, and $\mathrm{OPT}$ is $m$ times that optimum.

**Lemma 3 (properties of the weights).** $0 \le w^\pm_{uv} \le 1$, $w^+_{uv} + w^-_{uv} = 1$, and $w^-_{uv} \le w^-_{uw} + w^-_{wv}$ for all distinct $u, v, w$.

*Proof.* The first two are clear. For one partition $P_i$, let $s_i(u, v) = 1$ if $P_i$ splits $uv$, else 0. If $s_i(u, w) = s_i(w, v) = 0$, then $u, w, v$ are in one cluster of $P_i$ and $s_i(u, v) = 0$. So $s_i(u, v) \le s_i(u, w) + s_i(w, v)$ in all cases. Average over $i$: $w^- = \frac{1}{m}\sum_i s_i$. $\square$

**Lemma 4 (the output is a partition).** Lines L3 to L7 stop after at most $n$ rounds and $Q$ is a partition of $V$. Line L9 returns a partition of $V$.

*Proof.* Invariant: the clusters in $Q$ and the set $R$ partition $V$. It holds after line L3. In each round, $C \subseteq R$ and $p \in C$, and line L7 moves exactly $C$ from $R$ to $Q$, so the invariant is kept and $|R|$ drops by at least 1. At the end $R = \emptyset$. $B$ is one of the inputs, so it is a partition of $V$, and line L9 returns $Q$ or $B$. $\square$

**Lemma 5 (the contingency formula).** For partitions $P$ with clusters $P_a$ and $Q$ with clusters $Q_b$, and $n_{ab} = |P_a \cap Q_b|$,

$$d(P, Q) = \sum_a \binom{|P_a|}{2} + \sum_b \binom{|Q_b|}{2} - 2 \sum_{a, b} \binom{n_{ab}}{2}.$$

*Proof.* $|J(P)| = \sum_a \binom{|P_a|}{2}$ and $|J(Q)| = \sum_b \binom{|Q_b|}{2}$. A pair is in $J(P) \cap J(Q)$ iff both items lie in one $P_a \cap Q_b$, so $|J(P) \cap J(Q)| = \sum_{a,b} \binom{n_{ab}}{2}$. Then $|J(P) \triangle J(Q)| = |J(P)| + |J(Q)| - 2|J(P) \cap J(Q)|$. $\square$

**Theorem 1 (the best input).** $D(B) \le 2\bigl(1 - \frac{1}{m}\bigr)\mathrm{OPT}$ for the input $B$ chosen in line L8.

*Proof.* Let $P^*$ be a median and choose $j$ with $d(P_j, P^*)$ least. Then $m \, d(P_j, P^*) \le \sum_i d(P_i, P^*) = \mathrm{OPT}$. The term $i = j$ of $D(P_j)$ is 0. By Lemma 1,

$$D(P_j) = \sum_{i \ne j} d(P_j, P_i) \le \sum_{i \ne j} d(P_j, P^*) + \sum_{i \ne j} d(P^*, P_i) = (m - 1)\, d(P_j, P^*) + \mathrm{OPT} - d(P^*, P_j).$$

The right side is $(m - 2)\, d(P_j, P^*) + \mathrm{OPT} \le \frac{m - 2}{m}\mathrm{OPT} + \mathrm{OPT} = \bigl(2 - \frac{2}{m}\bigr)\mathrm{OPT}$; for $m = 1$ the left side is 0, and the bound reads $0 \le 0$. Line L8 picks an input with $D(B) \le D(P_j)$. $\square$

**Theorem 2 (the returned clustering).** The output $O$ satisfies $D(O) = \min(D(Q), D(B)) \le 2\bigl(1 - \frac{1}{m}\bigr)\mathrm{OPT}$ in every run.

*Proof.* Line L9 returns the one of $Q$ and $B$ with the smaller $D$, and Theorem 1 bounds $D(B)$. $\square$

**The randomized bounds (cited).** By Lemmas 2 and 3, the instance of lines L3 to L7 is weighted correlation clustering whose weights satisfy the probability constraints and the triangle inequality. For such weights, Ailon, Charikar and Newman (Journal of the ACM 55(5), 2008) prove that the pivot rule of line L6 has $\mathbb{E}[D(Q)] \le 2 \cdot \mathrm{OPT}$, and that for consensus clustering $\mathbb{E}[\min(D(Q), D(B))] \le \frac{11}{7}\mathrm{OPT}$. Their proof charges the cost to triangles, as in the unweighted analysis of the [pivot algorithm](/pivot-algorithm/), and checks a set of triangle inequalities. We do not reproduce it here. The tests check both bounds exactly with fractions, by averaging over all $n!$ pivot orders on random ensembles with $n \le 6$ and comparing with a brute-force median.

**NP-hardness (cited).** Computing $\mathrm{OPT}$ is NP-hard (Křivánek and Morávek 1986; Wakabayashi 1986), so no polynomial algorithm is known to return a median in general.
