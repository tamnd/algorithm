---
title: chrF computes the F-score of the averaged character n-gram precision and recall, a value in [0, 1]
proves: [correctness]
status: full
---

Fix the maximum order $N \ge 1$, the weight $\beta > 0$ and a corpus of pairs $(y^{(s)}, x^{(s)})$ of a hypothesis and the reference chosen for it, each a string. Let $h^{(s)}$ and $r^{(s)}$ be the strings with all white space removed. For a string $z$ and a string $g$ of $n$ characters, $\mathrm{count}_z(g)$ is the number of positions where $g$ occurs in $z$. The definition is

$$M_n = \sum_s \sum_g \min\bigl(\mathrm{count}_{h^{(s)}}(g), \mathrm{count}_{r^{(s)}}(g)\bigr), \quad H_n = \sum_s \max(|h^{(s)}| - n + 1, 0), \quad E_n = \sum_s \max(|r^{(s)}| - n + 1, 0),$$

the set $K = \{n \le N : H_n > 0 \text{ and } E_n > 0\}$, the averages $P = \frac{1}{|K|} \sum_{n \in K} M_n / H_n$ and $R = \frac{1}{|K|} \sum_{n \in K} M_n / E_n$, and

$$\mathrm{chrF}_\beta = \frac{(1 + \beta^2) P R}{\beta^2 P + R},$$

with $\mathrm{chrF}_\beta = 0$ when $K$ is empty or $P + R = 0$.

**Lemma 1 (the counts).** After lines L1 to L6, the statistics hold $M_n$, $H_n$ and $E_n$.

*Proof.* Line L1 sets them to 0. For each pair, line L3 removes the white space, and for each order line L5 adds $\sum_g \min(\mathrm{count}_h(g), \mathrm{count}_r(g))$ over the distinct $n$-grams $g$ of $h$. An $n$-gram that does not occur in $h$ adds 0 to the definition, so this is the sum over all $g$. A string of length $\ell$ has $\max(\ell - n + 1, 0)$ positions where an $n$-gram starts, which line L6 adds. The sums over $s$ follow because addition is commutative. $\square$

**Lemma 2 (precision and recall).** For each $n \in K$, $0 \le M_n / H_n \le 1$ and $0 \le M_n / E_n \le 1$. Hence $0 \le P \le 1$ and $0 \le R \le 1$.

*Proof.* Each term of $M_n$ is at most $\mathrm{count}_h(g)$ and at most $\mathrm{count}_r(g)$. Summing over $g$ gives $M_n \le H_n$ and $M_n \le E_n$ for each pair, and so for the sums. An average of numbers in $[0, 1]$ is in $[0, 1]$. $\square$

**Theorem.** The procedure returns $\mathrm{chrF}_\beta$ of the definition, and $0 \le \mathrm{chrF}_\beta \le 1$. Moreover, when $P > 0$ and $R > 0$,

$$\frac{1}{\mathrm{chrF}_\beta} = \frac{1}{1 + \beta^2} \cdot \frac{1}{P} + \frac{\beta^2}{1 + \beta^2} \cdot \frac{1}{R},$$

so the score is a weighted harmonic mean of $P$ and $R$ with weight $\beta^2$ on the recall, and $\min(P, R) \le \mathrm{chrF}_\beta \le \max(P, R)$.

*Proof.* By Lemma 1, line L7 computes $K$. Lines L8 and L10 return 0 in the two cases where the definition gives 0. Otherwise line L9 computes $P$ and $R$ and line L11 returns the formula. The denominator $\beta^2 P + R$ is positive because $P + R > 0$ and $\beta > 0$.

If $P = 0$ or $R = 0$ (but not both), the numerator is 0 and the score is 0, which is in $[0, 1]$ and equal to $\min(P, R)$. If both are positive, dividing $\beta^2 P + R$ by $(1 + \beta^2) P R$ gives the displayed identity. A weighted harmonic mean with positive weights that sum to 1 lies between the smallest and the largest of the values, so the score is between $\min(P, R)$ and $\max(P, R)$, which are in $[0, 1]$ by Lemma 2. $\square$

**Corollary (recall weight).** For fixed $P, R > 0$, the score tends to $R$ as $\beta \to \infty$ and to $P$ as $\beta \to 0$. With $\beta = 1$ the score is symmetric: exchanging the hypotheses and the references exchanges $H_n$ and $E_n$, which keeps $K$ and exchanges $P$ and $R$, and $2PR/(P + R)$ does not change.

*Proof.* The weights of the identity are $1/(1 + \beta^2)$ and $\beta^2/(1 + \beta^2)$, which tend to $(0, 1)$ and $(1, 0)$. The symmetry follows because $M_n$ is symmetric in the two strings and the condition for $K$ is symmetric. $\square$

**Remark (several references).** For a sentence with several references, the implementation computes the sentence score against each and keeps the statistics of the best one, the first on a tie. The theorem holds for any choice of one reference per sentence, so it holds for this one.

**Remark (chrF++).** With word $n$-grams of orders $1, \ldots, N_w$, the statistics of the word orders are appended to those of the character orders, and lines L7 to L11 average over all of them. Lemma 1 and Lemma 2 hold for each order with words in place of characters, so the theorem holds unchanged.

**Remark (complexity).** For a hypothesis of $\ell$ characters and a reference of $\ell'$, order $n$ needs the counts of $\ell + \ell'$ strings of $n$ characters, which takes $O(n (\ell + \ell'))$ expected time with hashing. Over $n \le N$, all references and the whole corpus with $L$ characters, this is $O(N^2 L)$ expected time.
