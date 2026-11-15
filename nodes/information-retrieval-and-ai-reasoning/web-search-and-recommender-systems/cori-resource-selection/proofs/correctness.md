---
title: CORI computes its belief formula, and each belief lies between b and 1
proves: [correctness]
status: full
---

There are $K \ge 1$ collections $C_1, \ldots, C_K$. For collection $i$ and term $t$, $df_i(t)$ is the number of documents of $C_i$ that contain $t$, and $cw_i$ is the number of tokens of $C_i$. Let $\overline{cw} = \frac{1}{K} \sum_i cw_i > 0$, and let $c(t) = |\{i : df_i(t) > 0\}|$ be the number of collections that contain $t$. The constants are $b = 0.4$, $50$ and $150$. For $c(t) \ge 1$,

$$T_i(t) = \frac{df_i(t)}{df_i(t) + 50 + 150 \cdot cw_i / \overline{cw}}, \qquad I(t) = \frac{\log\left((K + 0.5)/c(t)\right)}{\log(K + 1)}, \qquad p_i(t) = b + (1 - b)\, T_i(t)\, I(t),$$

and $p_i(t) = b$ when $c(t) = 0$. For a query $q = (t_1, \ldots, t_r)$ with $r \ge 1$ terms, repeats kept, the score is $s_i = \frac{1}{r} \sum_{j=1}^{r} p_i(t_j)$.

**Theorem 1 (the procedure computes the formula).** Lines L1 to L11 set $s_i$ to the score above for every $i$, and line L12 returns the $n$ indexes with the largest scores, ties to the smaller index.

*Proof.* Lines L1 and L2 compute $cw_i$ and $\overline{cw}$ from the descriptions, and line L3 computes $c(t)$ for each distinct query term. For a fixed $i$, the loop of lines L6 to L10 keeps the invariant that after $j$ terms, $s_i = \sum_{l \le j} p_i(t_l)$: line L7 adds $b$ when $c(t_j) = 0$, and lines L8 to L10 add $b + (1 - b) T_i(t_j) I(t_j)$ otherwise. Line L11 divides by $r$. Line L12 sorts by the key $(-s_i, i)$, which puts larger scores first and, among equal scores, smaller indexes first, and keeps the first $n$. $\square$

**Lemma 2 (base of the logarithm).** $I(t)$ is the same for every base of the logarithm.

*Proof.* $\log_a x = \ln x / \ln a$, so the factor $1/\ln a$ appears in the numerator and the denominator and cancels. $\square$

**Theorem 3 (range).** For every collection and term, $b \le p_i(t) < 1$. So every score $s_i$ lies in $[b, 1)$.

*Proof.* If $c(t) = 0$, $p_i(t) = b$. Else $0 \le df_i(t)$ and the denominator of $T_i(t)$ exceeds $df_i(t)$ by at least $50$, so $0 \le T_i(t) < 1$. Since $1 \le c(t) \le K$, the ratio $(K + 0.5)/c(t)$ lies in $[(K + 0.5)/K,\ K + 0.5]$. The lower end is greater than $1$ and the upper end is less than $K + 1$, so $0 < \log((K + 0.5)/c(t)) < \log(K + 1)$ and $0 < I(t) < 1$. Then $0 \le T_i(t) I(t) < 1$ and $b \le p_i(t) < b + (1 - b) = 1$. A mean of numbers in $[b, 1)$ lies in $[b, 1)$. $\square$

**Theorem 4 (monotonicity).** Fix the term $t$ and all other statistics. Then $p_i(t)$ strictly increases with $df_i(t)$ and strictly decreases with $cw_i$ (when $df_i(t) > 0$, keeping $\overline{cw}$ fixed). $I(t)$ strictly decreases with $c(t)$.

*Proof.* Write $T = x/(x + a)$ with $x = df_i(t)$ and $a = 50 + 150\, cw_i / \overline{cw} > 0$. For $0 \le x < y$, $\frac{y}{y + a} - \frac{x}{x + a} = \frac{a (y - x)}{(x + a)(y + a)} > 0$. For fixed $x > 0$, $T$ falls when $a$ grows, and $a$ grows with $cw_i$. The factor $(1 - b) I(t)$ is positive by Theorem 3, so $p_i(t)$ moves in the same direction as $T$. The numerator of $I(t)$ is the logarithm of a value that falls when $c(t)$ grows, and the denominator does not depend on $c(t)$. $\square$

**Consequence.** For a one-term query, $I(t)$ and $b$ are the same for every collection, so the ranking of the collections is the ranking by $T_i(t)$: it depends only on $df_i(t)$ and on the size $cw_i$ relative to the mean. The idf-like factor $I(t)$ changes the ranking only when the query has two or more terms, because it then sets how much each term weighs against the others.

**The form of T.** With $k = 200$ and $\beta = 0.75$, $k\,((1 - \beta) + \beta\, cw_i / \overline{cw}) = 50 + 150\, cw_i / \overline{cw}$. So $T_i(t)$ is the term frequency part of [BM25](/bm25/), with the document frequency of the term in the collection in place of the term frequency, and the collection size in place of the document length.

**Cost.** Let $m$ be the number of query terms, with repeats. Line L3 costs $O(Km)$ dictionary lookups, and lines L4 to L11 cost $O(Km)$ arithmetic operations and lookups. Line L12 sorts $K$ scores in $O(K \log K)$. So a query costs $O(Km + K \log K)$ time with hash table lookups, expected, and $O(K)$ extra space. The descriptions take space proportional to the total size of the vocabularies of the collections.
