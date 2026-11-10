---
title: The AMS sketch gives a (1 ± ε) estimate of F_2 with probability 1 − δ using 4-wise independent signs
proves: [correctness]
status: full
---

Let $f \in \mathbb{Z}^n$ be the frequency vector at query time and $F_2 = \sum_i f_i^2$. Probabilities are over the sign functions; the stream is fixed in advance.

**Lemma 1 (the sign family).** Let $q(x) = a_3 x^3 + a_2 x^2 + a_1 x + a_0$ with $a_0, \ldots, a_3$ independent and uniform in the field $GF(2^b)$, and let $s(x) = (-1)^{\beta(q(x))}$, where $\beta(y)$ is the lowest bit of $y$ in the polynomial basis. For any four distinct field elements $x_1, \ldots, x_4$, the signs $s(x_1), \ldots, s(x_4)$ are independent and each is $\pm 1$ with probability $1/2$. The same holds for any two or three distinct elements.

*Proof.* The map $(a_0, a_1, a_2, a_3) \mapsto (q(x_1), \ldots, q(x_4))$ is linear over the field, with the Vandermonde matrix of $x_1, \ldots, x_4$. This matrix has determinant $\prod_{k < l} (x_l - x_k) \ne 0$, so the map is a bijection of $GF(2^b)^4$. A uniform input therefore gives a uniform output: the four values are independent and uniform in the field. Exactly half of the field elements have $\beta(y) = 1$, so each sign is fair, and functions of independent values are independent. For fewer than four points, take any extra distinct points and forget them. $\square$

**Lemma 2 (the table is linear).** After AMS-UPDATE is used for every update, $Z[g][k] = \sum_i s_{g,k}(i) f_i$ for every counter.

*Proof.* By induction on the updates: an update $(i, c)$ adds $c$ to $f_i$ and lines L1 and L2 add $s_{g,k}(i) c$ to every counter. $\square$

So line L5 gives the counters of $f + g$, and the sketch of $f - g$ is the difference.

**Theorem 1 (one counter).** Let $Z = \sum_i s(i) f_i$, where $s$ is 4-wise independent with fair signs. Then
$$ \mathbb{E}[Z^2] = F_2 , \qquad \mathrm{Var}[Z^2] = 4 \sum_{i < j} f_i^2 f_j^2 \le 2F_2^2 . $$

*Proof.* Write $s_i = s(i)$. For a list of items $i_1, \ldots, i_\ell$ with $\ell \le 4$, let $D$ be the set of the items that appear an odd number of times in the list. Since $s_i^2 = 1$, the product $s_{i_1} \cdots s_{i_\ell}$ equals $\prod_{i \in D} s_i$. The set $D$ has at most four items, so by 4-wise independence this product has mean $\prod_{i \in D} \mathbb{E}[s_i]$, which is 1 if $D$ is empty and 0 otherwise.

*The mean.* $Z^2 = \sum_{i, j} f_i f_j s_i s_j$. The term has mean 1 if $i = j$ and 0 otherwise, so $\mathbb{E}[Z^2] = \sum_i f_i^2 = F_2$.

*The fourth moment.* $Z^4 = \sum_{i, j, k, l} f_i f_j f_k f_l \, s_i s_j s_k s_l$. A term has mean 1 when every item in $(i, j, k, l)$ appears an even number of times, and 0 otherwise. Two kinds of lists survive:

- all four items equal to one item $a$: these give $\sum_a f_a^4$;
- two items $a \ne b$, each twice: for each pair $a < b$ there are $\binom{4}{2} = 6$ ordered lists, and these give $6 \sum_{a < b} f_a^2 f_b^2$.

So $\mathbb{E}[Z^4] = \sum_a f_a^4 + 6 \sum_{a < b} f_a^2 f_b^2$. Also $F_2^2 = (\sum_a f_a^2)^2 = \sum_a f_a^4 + 2 \sum_{a < b} f_a^2 f_b^2$. Hence
$$ \mathrm{Var}[Z^2] = \mathbb{E}[Z^4] - F_2^2 = 4 \sum_{a < b} f_a^2 f_b^2 \le 2 F_2^2 , $$
where the last step uses $2 \sum_{a < b} f_a^2 f_b^2 \le F_2^2$, which holds because $\sum_a f_a^4 \ge 0$. $\square$

**Theorem 2 (one group).** Let $Y = \frac{1}{t} \sum_{k=1}^t Z_k^2$ for counters $Z_k$ with independent sign functions, as in line L3. If $t \ge 6/\varepsilon^2$, then $\Pr[|Y - F_2| > \varepsilon F_2] \le 1/3$.

*Proof.* If $F_2 = 0$ then $f = 0$, every $Z_k = 0$ and $Y = 0 = F_2$. Otherwise, by Theorem 1 and the independence of the counters, $\mathbb{E}[Y] = F_2$ and $\mathrm{Var}[Y] = \mathrm{Var}[Z^2]/t \le 2F_2^2/t$. By Chebyshev's inequality,
$$ \Pr[|Y - F_2| > \varepsilon F_2] \le \frac{2F_2^2}{t \, \varepsilon^2 F_2^2} = \frac{2}{t \varepsilon^2} \le \frac{1}{3} . \qquad \square $$

**Theorem 3 (the estimate).** If $t \ge 6/\varepsilon^2$ and $r \ge 18 \ln(1/\delta)$, the output $M$ of line L4 satisfies $\Pr[|M - F_2| > \varepsilon F_2] \le \delta$.

*Proof.* The groups use disjoint sets of independent sign functions, so $Y_1, \ldots, Y_r$ are independent. Call group $g$ bad if $|Y_g - F_2| > \varepsilon F_2$; by Theorem 2 each group is bad with probability $p_g \le 1/3$. Let $M$ be the value at position $\lceil r/2 \rceil$ of the sorted $Y_g$. If $M > (1 + \varepsilon) F_2$, then the values at positions $\lceil r/2 \rceil, \ldots, r$ are bad, at least $r/2$ groups. If $M < (1 - \varepsilon) F_2$, the values at positions $1, \ldots, \lceil r/2 \rceil$ are bad, again at least $r/2$ groups. Let $B$ be the number of bad groups. Then $B \ge r/2$ implies $B - \sum_g p_g \ge r/6$, and the Hoeffding bound for $r$ independent indicators gives
$$ \Pr[B \ge r/2] \le \exp\left(-\frac{2 (r/6)^2}{r}\right) = e^{-r/18} \le \delta . \qquad \blacksquare $$

**Remark.** The bound $\mathrm{Var}[Z^2] \le 2F_2^2$ is tight up to the constant: for $f$ with $n$ equal entries, $4 \sum_{a < b} f_a^2 f_b^2 = 2(1 - 1/n) F_2^2$.
