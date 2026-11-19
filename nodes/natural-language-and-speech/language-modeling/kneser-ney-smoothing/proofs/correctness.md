---
title: Interpolated Kneser-Ney gives a proper distribution after every history, and its continuation unigram is the one that keeps the unigram marginals
proves: [correctness]
status: full
---

We use the notation of the page. Every sentence is padded with $n - 1$ copies of <s> and one </s>. Level $n$ uses the raw counts $a_n(g) = c(g)$, and each level $m < n$ uses $a_m(g) = N_{1+}(\cdot\, g)$, the number of distinct tokens $x$ such that the $(m+1)$-gram $x g$ was seen. For a history $h$ of length $m - 1$, $T_m(h) = \sum_x a_m(h x)$ and $N_{1+}(h\, \cdot) = |\{x : a_m(h x) > 0\}|$. Level 0 is the uniform distribution $1/|V|$ on the vocabulary $V$.

**Lemma 1 (the counts of lines L1 and L2).** After lines L1 and L2, $a_n(g)$ is the number of positions where the $n$-gram $g$ ends at a predicted token, and for $m < n$, $a_m(g)$ is the number of distinct $x$ such that $x g$ occurs as an $(m+1)$-gram that ends at a predicted token.

*Proof.* Line L1 visits each predicted position once and adds 1 to the $n$-gram that ends there. For $m < n$, line L2 runs once for each distinct key $x g$ of $a_{m+1}$, and it adds 1 to the key $g$. So $a_m(g)$ counts the distinct first tokens $x$ of the keys of $a_{m+1}$ that end with $g$. The keys of $a_n$ are the seen $n$-grams. Because each sentence has $n - 1$ copies of <s> in front, every $(m+1)$-gram that ends at a predicted position is the suffix of the $n$-gram that ends at the same position, so by induction on $n - m$ the keys of $a_{m+1}$ are exactly the seen $(m+1)$-grams. $\square$

**Theorem 2 (a proper distribution).** Let $0 \le D_m \le 1$ for every level $m$. Then for every level $m \ge 0$ and every history $h$ of length $m - 1$ (no history for $m = 0$), $P_m(w \mid h) \ge 0$ for every $w \in V$ and $\sum_{w \in V} P_m(w \mid h) = 1$. If $D_1 = 0$, assume also that every word of $V$ was seen; then the same holds, and every $P_m(w \mid h)$ with $m \ge 1$ is positive when every $D_m$ with $m \ge 2$ is positive.

*Proof.* Induction on $m$. For $m = 0$ the uniform distribution sums to 1. Let $m \ge 1$ and assume the claim for $m - 1$. If $T_m(h) = 0$, line L6 returns $P_{m-1}(w \mid h')$, which sums to 1. Otherwise split $V$ into the set $S = \{w : a_m(h w) > 0\}$ and the rest. Every count in $S$ is an integer at least 1, so $a_m(h w) - D_m \ge 0$ there, and the max in line L8 is zero outside $S$. So

$$\sum_{w \in V} \frac{\max(a_m(h w) - D_m, 0)}{T_m(h)} = \frac{\sum_{w \in S} a_m(h w) - D_m |S|}{T_m(h)} = 1 - \frac{D_m N_{1+}(h\, \cdot)}{T_m(h)},$$

since $\sum_{w \in S} a_m(h w) = T_m(h)$ and $|S| = N_{1+}(h\, \cdot)$. The second term of line L8 adds $\gamma(h) \sum_w P_{m-1}(w \mid h') = D_m N_{1+}(h\, \cdot) / T_m(h)$ by the induction hypothesis. The total is 1, and every term is non-negative.

At level 1 with $D_1 = 0$, $P_1(w) = a_1(w) / T_1()$. Every seen word $w$ is predicted at some position, so it ends some bigram, and $a_1(w) \ge 1$ by Lemma 1 (for $n = 1$, $a_1(w) = c(w) \ge 1$). So $P_1(w) > 0$ on $V$. For $m \ge 2$ with $D_m > 0$, either $T_m(h) = 0$ and $P_m = P_{m-1} > 0$, or $\gamma(h) > 0$ and $P_m(w \mid h) \ge \gamma(h) P_{m-1}(w \mid h') > 0$. $\square$

The condition $D_m \le 1$ is needed. With $D_m > 1$, a word seen once after $h$ gets 0 from the first term, but the backoff weight still counts it in $D_m N_{1+}(h\,\cdot)$, and the total is $1 + \sum_{w \in S} \max(D_m - a_m(h w), 0) / T_m(h) > 1$.

**Theorem 3 (why continuation counts).** Take a bigram model ($n = 2$) and fix $0 < D \le 1$. Write $c(v w)$ for the bigram counts, $c(v) = \sum_w c(v w)$, $c(w) = \sum_v c(v w)$ and $N = \sum_{v, w} c(v w)$. Let the bigram level be

$$P(w \mid v) = \frac{\max(c(v w) - D, 0)}{c(v)} + \frac{D\, N_{1+}(v\, \cdot)}{c(v)}\, q(w)$$

for some distribution $q$. Then the model keeps the unigram marginals of the data, that is

$$\sum_v \frac{c(v)}{N} P(w \mid v) = \frac{c(w)}{N} \quad \text{for every } w,$$

if and only if $q(w) = N_{1+}(\cdot\, w) / N_{1+}(\cdot\, \cdot)$.

*Proof.* Multiply the bigram level by $c(v)$ and sum over $v$. Since $D \le 1$, the first term gives $\sum_{v : c(v w) > 0} (c(v w) - D) = c(w) - D\, N_{1+}(\cdot\, w)$. The second term gives $D\, q(w) \sum_v N_{1+}(v\, \cdot) = D\, q(w)\, N_{1+}(\cdot\, \cdot)$, because both sums count the distinct bigram types. So

$$\sum_v c(v) P(w \mid v) = c(w) - D\, N_{1+}(\cdot\, w) + D\, q(w)\, N_{1+}(\cdot\, \cdot),$$

and this equals $c(w)$ for every $w$ if and only if $q(w) = N_{1+}(\cdot\, w) / N_{1+}(\cdot\, \cdot)$, since $D\, N_{1+}(\cdot\, \cdot) > 0$. This $q$ is a distribution: its values are non-negative and sum to 1. $\square$

This is the derivation of Chen and Goodman (1999, Section 2.7) for the interpolated form. The same computation at each level $m < n$ against the level above gives the continuation counts $N_{1+}(\cdot\, h w)$ of every lower level. Kneser and Ney (1995) reached the same lower distribution for the backoff form by a different derivation, as Chen and Goodman note.
