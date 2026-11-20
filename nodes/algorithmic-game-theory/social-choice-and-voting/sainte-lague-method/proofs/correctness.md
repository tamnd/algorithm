---
title: Correctness and properties of the Sainte-Lague method
proves: [correctness]
status: full
---

Let $p_1, \ldots, p_n \ge 0$ be integers with $P = \sum_i p_i > 0$, and let $h \ge 0$. The quota of party $i$ is $q_i = h p_i / P$. The greedy rule gives $h$ seats one at a time; each goes to the party with the largest key $p_i/(2 a_i + 1)$, where $a_i$ is its current number of seats, the smallest index among ties. For a real $x \ge 0$ that is not of the form $k + 1/2$, let $[x]$ be the nearest integer.

**Claim 1 (the heap).** The method of the page gives the same seats as the greedy rule.

*Proof.* The heap compares $p_i/d_i$ with $p_j/d_j$ by $p_i d_j$ against $p_j d_i$, with $d_i, d_j \ge 1$, and breaks ties by the smaller index. It holds one key per party, $p_i/(2 a_i + 1)$: this holds after line L2, where $a_i = 0$, and lines L4 to L6 remove the key of the winner, add its seat and insert its new key $p_i/(2 a_i + 1)$ for the new $a_i$. So line L4 removes the key that the greedy rule picks.

**Claim 2 (the keys do not increase).** The keys of the seats, in the order they are given, do not increase, and each is at least $\ell = \max_i p_i/(2 a_i + 1)$ for the final seats $a$.

*Proof.* A seat changes only the key of its winner, to a smaller value. So the largest key never increases, and $\ell$ is the largest key at the end.

**Claim 3 (divisor form).** Let $u = \min_{i : a_i \ge 1} p_i/(2 a_i - 1)$ (or $u = \infty$ if $h = 0$). Then $\ell \le u$. If $\ell < u$, then for every $\mu$ with $\ell < \mu < u$ and $\lambda = 2 \mu$, $a_i = [p_i/\lambda]$ for every $i$: the method rounds $p_i/\lambda$ at one half, which is Webster's method. Conversely, a vector $b$ with $\sum_i b_i = h$ and $b_i = [p_i/\lambda]$ for some $\lambda$ satisfies the same inequalities, so the output is the only Webster apportionment when $\ell < u$.

*Proof.* The last seat of party $i$ had the key $p_i/(2 a_i - 1)$, which is at least $\ell$ by Claim 2. So $u \ge \ell$. If $\ell < \mu < u$, then $p_i/(2 a_i + 1) < \mu$ gives $p_i/\lambda < a_i + 1/2$, and for $a_i \ge 1$, $\mu < p_i/(2 a_i - 1)$ gives $p_i/\lambda > a_i - 1/2$. So $p_i/\lambda$ lies strictly between $a_i - 1/2$ and $a_i + 1/2$, and $a_i = [p_i/\lambda]$. The converse and the uniqueness follow as for the [D'Hondt method](/dhondt-method/), with $2 b + 1$ and $2 b - 1$ in place of $b + 1$ and $b$: if $b \ne a$, some $b_i > a_i$ and some $b_j < a_j$, and then $\lambda_b / 2 \le p_i/(2 b_i - 1) \le p_i/(2 a_i + 1) \le \ell$ and $\lambda_b / 2 \ge p_j/(2 b_j + 1) \ge p_j/(2 a_j - 1) \ge u$, which contradicts $\ell < u$.

**Claim 4 (least squares).** If every $p_i > 0$, the output minimizes $G(b) = \sum_i b_i^2/p_i$ over all integer vectors $b \ge 0$ with $\sum_i b_i = h$. Equivalently, it minimizes $\sum_i p_i (b_i/p_i - h/P)^2$, the spread of the seats per voter around the average weighted by the votes.

*Proof.* $G(b) = \sum_i \sum_{x = 0}^{b_i - 1} (2x + 1)/p_i$, a sum of marginal costs $(2x + 1)/p_i$ that increase in $x$. As for the D'Hondt method, the sum of any $h$ marginal costs taken as prefixes is at least the sum of the $h$ smallest ones, and the greedy rule takes the smallest marginal cost left, which is the largest key $p_i/(2 a_i + 1)$. For the second form, $\sum_i p_i (b_i/p_i - h/P)^2 = G(b) - 2 (h/P) \sum_i b_i + h^2/P = G(b) - h^2/P$, which differs from $G$ by a constant.

**Claim 5 (house and population monotone).** The seats for $h + 1$ are those for $h$ plus one seat. If $p'_i \ge p_i$ and $p'_j \le p_j$, then $a'_i < a_i$ and $a'_j > a_j$ cannot both hold, unless one of the two apportionments has $\ell = u$.

*Proof.* The first part holds because the greedy rule for $h + 1$ repeats the steps for $h$. For the second, take $\mu \in [\ell, u]$ for $p$ and $\mu' \in [\ell', u']$ for $p'$. If $a'_i < a_i$ and $a'_j > a_j$, then
$$\mu' \ge \frac{p'_i}{2 a'_i + 1} \ge \frac{p_i}{2 a_i - 1} \ge \mu \ge \frac{p_j}{2 a_j + 1} \ge \frac{p'_j}{2 a'_j - 1} \ge \mu',$$
so all are equal and $u \le \ell$ for $p$.

**Claim 6 (quota fails).** With $p = (26, 5, 3, 1)$ and $h = 19$, the method gives $(13, 3, 2, 1)$, while $q_1 = 494/35 \approx 14.11$, so party 1 gets less than its lower quota.

*Proof.* The keys $26/(2x + 1)$ of party 1 for $x = 0, \ldots, 13$ end with $26/25 = 1.04$ and $26/27 \approx 0.963$. Those of party 2 are $5, 5/3, 1, 5/7 \approx 0.714$; of party 3, $3, 1, 3/5 = 0.6$; of party 4, $1, 1/3$. The keys at least $1$ are the 13 of party 1 from $26$ down to $26/25$, the 3 keys $5, 5/3, 1$ of party 2, the 2 keys $3, 1$ of party 3, and the key $1$ of party 4: 19 keys in all, which are the 19 seats. The largest key left is $26/27$ and the smallest key used is $1$, so $\ell < u$ and there is no tie.
