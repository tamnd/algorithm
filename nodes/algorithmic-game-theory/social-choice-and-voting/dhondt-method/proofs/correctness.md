---
title: Correctness and properties of the D'Hondt method
proves: [correctness]
status: full
---

Let $p_1, \ldots, p_n \ge 0$ be integers with $P = \sum_i p_i > 0$, and let $h \ge 0$. The quota of party $i$ is $q_i = h p_i / P$. The greedy rule gives $h$ seats one at a time; each goes to the party with the largest key $p_i/(a_i + 1)$, where $a_i$ is its current number of seats, the smallest index among ties.

**Claim 1 (the heap).** The method of the page gives the same seats as the greedy rule.

*Proof.* The order used by the heap compares $p_i/d_i$ and $p_j/d_j$ by the products $p_i d_j$ and $p_j d_i$, which is exact since $d_i, d_j > 0$, and breaks ties by the smaller index. It is a strict total order on the keys. At each pass of line L3 the heap holds exactly one key per party, $p_i/(a_i + 1)$: this holds after line L2, and lines L4 to L6 remove the key of $i$ and insert its new one. So line L4 removes the key that the greedy rule picks.

**Claim 2 (the keys do not increase).** Let $w_1, w_2, \ldots, w_h$ be the keys of the seats in the order they are given. Then $w_1 \ge w_2 \ge \cdots \ge w_h \ge \ell$, where $\ell = \max_i p_i/(a_i + 1)$ for the final seats $a$.

*Proof.* Each $w_t$ is the largest key at time $t$. Giving the seat changes only the key of the winner, from $p_i/(a_i + 1)$ to the smaller value $p_i/(a_i + 2)$. So the largest key never increases, and $\ell$ is the largest key at the end.

**Claim 3 (divisor form).** Let $u = \min_{i : a_i \ge 1} p_i / a_i$ (or $u = \infty$ if $h = 0$). Then $\ell \le u$, and for every $\lambda$ with $\ell < \lambda \le u$, $a_i = \lfloor p_i / \lambda \rfloor$ for every $i$. Conversely, if some $\lambda > 0$ gives $\sum_i \lfloor p_i/\lambda \rfloor = h$, then $b_i = \lfloor p_i/\lambda \rfloor$ satisfies $\max_i p_i/(b_i + 1) < \lambda \le \min_{i : b_i \ge 1} p_i/b_i$. So the output of the method is an apportionment of Jefferson's divisor method, and it is the only one when $\ell < u$.

*Proof.* The seats of party $i$ had the keys $p_i/1, \ldots, p_i/a_i$, so $p_i/a_i$ is one of the $w_t$, and by Claim 2 it is at least $\ell$. So $u \ge \ell$. If $\ell < \lambda \le u$, then $p_i/(a_i + 1) \le \ell < \lambda$ gives $p_i/\lambda < a_i + 1$, and, for $a_i \ge 1$, $\lambda \le p_i/a_i$ gives $p_i/\lambda \ge a_i$; for $a_i = 0$ this is trivial. So $a_i = \lfloor p_i/\lambda \rfloor$. The converse is the definition of the floor: $b_i \le p_i/\lambda < b_i + 1$. If $\ell < u$, any other vector $b$ of the divisor form with sum $h$ has its own interval $(\ell_b, u_b]$, and $b \ne a$ forces some $b_i > a_i$ and some $b_j < a_j$, so $\lambda_b \le p_i/b_i \le p_i/(a_i + 1) \le \ell$ and $\lambda_b > p_j/(b_j + 1) \ge p_j/a_j \ge u$, which contradicts $\ell < u$.

**Claim 4 (lower quota).** $a_i \ge \lfloor q_i \rfloor$ for every $i$.

*Proof.* Suppose $a_i < \lfloor q_i \rfloor$, so $a_i + 1 \le q_i$. Then $\ell \ge p_i/(a_i + 1) \ge p_i/q_i = P/h$. For every party $j$ with $a_j \ge 1$, Claim 3 gives $p_j/a_j \ge \ell \ge P/h$, so $a_j \le q_j$. Then $h = \sum_j a_j \le \sum_{j \ne i} q_j + a_i < \sum_j q_j = h$, a contradiction.

**Claim 5 (upper quota fails).** With $p = (8, 2, 1, 1)$ and $h = 7$, the method gives $(6, 1, 0, 0)$, but $q_1 = 14/3 < 5$.

*Proof.* The keys of party 1 are $8, 4, 8/3, 2, 8/5, 4/3, 8/7$, of party 2 they are $2, 1, \ldots$, and parties 3 and 4 have $1$. In decreasing order the first seven keys are $8, 4, 8/3, 2, 2, 8/5, 4/3$, and only one of them belongs to party 2. Here $\ell = \max(8/7, 1, 1, 1) = 8/7 < u = 4/3$, so there is no tie.

**Claim 6 (least cost).** If every $p_i > 0$, the output minimizes $F(b) = \sum_i b_i (b_i + 1)/p_i$ over all integer vectors $b \ge 0$ with $\sum_i b_i = h$.

*Proof.* $F(b) = \sum_i \sum_{x = 0}^{b_i - 1} c_i(x)$ with the marginal costs $c_i(x) = 2(x + 1)/p_i$, which increase in $x$. So $F(b)$ is a sum of $h$ marginal costs, taken as a prefix from each party, and it is at least the sum of the $h$ smallest marginal costs over all pairs $(i, x)$. Because each party's costs increase, the $h$ smallest costs form a prefix of each party, so some $b$ reaches this bound. The greedy rule takes at each step the smallest cost $c_i(a_i)$ left, which is the largest key $p_i/(a_i + 1)$, so it takes the $h$ smallest costs.

**Claim 7 (no paradoxes).** The method is house monotone: the seats for $h + 1$ are those for $h$ plus one seat. And it is population monotone: if the populations change from $p$ to $p'$ (and the house from $h$ to $h'$), with $p'_i \ge p_i$ and $p'_j \le p_j$, then it cannot happen that $a'_i < a_i$ and $a'_j > a_j$, unless both apportionments come from a tie ($\ell = u$).

*Proof.* The greedy rule for $h + 1$ seats repeats the first $h$ steps of the rule for $h$ seats. For the second part, take $\lambda \in [\ell, u]$ for $p$ and $\lambda' \in [\ell', u']$ for $p'$, so that $p_k/(a_k + 1) \le \lambda \le p_k/a_k$ for all $k$, and the same for $p'$. Suppose $a'_i < a_i$ and $a'_j > a_j$. Then $a_i \ge 1$, $a'_i + 1 \le a_i$ and $a'_j \ge a_j + 1$, so
$$\lambda' \ge \frac{p'_i}{a'_i + 1} \ge \frac{p_i}{a_i} \ge \lambda \ge \frac{p_j}{a_j + 1} \ge \frac{p'_j}{a'_j} \ge \lambda'.$$
So all are equal, and $p_i/a_i = p_j/(a_j + 1)$ gives $u \le \ell$, a tie.
