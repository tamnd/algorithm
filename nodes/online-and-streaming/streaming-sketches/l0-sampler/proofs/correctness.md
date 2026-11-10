---
title: The 1-sparse test is exact up to n/q, and the L0 sampler returns a uniform nonzero coordinate or fails with probability at most δ
proves: [correctness]
status: full
---

We use the notation of the page. The vector is $x \in \mathbb{Z}^n$ with $|x_i| \le M$. The prime $q$ satisfies $q > nM$, so every sum $A_j$ and every coordinate has absolute value below $q$. There are $R$ copies with independent seeds. A copy has a hash $h$, a base $z$ drawn uniformly from $\{1, \ldots, q - 1\}$ independently of $h$, and levels $0, \ldots, L$ with $L = \lceil \log_2 n \rceil + 2$.

For a copy and a level $j$, let $S_j = \{i : h(i) < q/2^j\}$ be the coordinates on level $j$, and let $y^{(j)}$ be $x$ restricted to $S_j$, with zeros elsewhere. Line L1 computes the deepest $t$ with $i \in S_t$, and the sets are nested, $S_0 \supseteq S_1 \supseteq \cdots \supseteq S_L$, so $i \in S_j$ exactly for $j \le t$. Line L2 therefore adds $d$ to the counters of exactly the levels $j$ with $i \in S_j$. By induction on the updates, at all times
$$A_j = \sum_{\ell} y^{(j)}_\ell, \qquad B_j = \sum_\ell \ell\, y^{(j)}_\ell, \qquad C_j \equiv \sum_\ell y^{(j)}_\ell z^\ell \pmod q. \tag{1}$$
This is the invariant that `check_invariant` tests. It also shows that the sketch is linear in $x$.

**Lemma 1 (the 1-sparse test).** Fix $y \in \mathbb{Z}^n$ with $|y_\ell| < q$ for all $\ell$ and $|\sum_\ell y_\ell| < q$, and let $A, B, C$ be given by (1) for $y$. Draw $z$ uniformly from $\{1, \ldots, q - 1\}$.

(a) If $y = 0$, DECODE returns ZERO.
(b) If $y$ has exactly one nonzero coordinate $y_i = v$, DECODE returns $(i, v)$.
(c) If $y$ has two or more nonzero coordinates, DECODE returns MANY except with probability at most $n/(q - 1)$.

*Proof.* (a) All three counters are 0, so line L3 returns ZERO.

(b) Here $A = v \ne 0$, $B = iv$ and $C \equiv v z^i$. Line L3 does not return, since $A \ne 0$. In line L4, $A$ divides $B$ with quotient $i$, which lies in $1..n$, and $C \equiv A z^i$, so DECODE returns $(i, A) = (i, v)$.

(c) Let $p(Z) = \sum_\ell y_\ell Z^\ell$, a polynomial over the field $\mathbb{Z}_q$. Each nonzero $y_\ell$ has $0 < |y_\ell| < q$, so it is nonzero modulo $q$. Hence $p$ has at least two nonzero coefficients, and its degree is at most $n$. The numbers $A$ and $B$ depend on $y$ only, not on $z$. There are two cases.

If $A = 0$ and $B = 0$, line L4 cannot return because it needs $A \ne 0$. The only wrong answer is ZERO from line L3, which needs $C = 0$, that is $p(z) \equiv 0$. A nonzero polynomial of degree at most $n$ over a field has at most $n$ roots, so this has probability at most $n/(q - 1)$.

Otherwise line L3 cannot return. The only wrong answer is ONE from line L4. If $A = 0$ or $A$ does not divide $B$ or $B/A \notin 1..n$, line L4 does not return, and the answer is MANY. Else let $i = B/A$, a fixed index. Line L4 returns only if $p(z) - A z^i \equiv 0$. The polynomial $p(Z) - AZ^i$ has the same coefficient as $p$ at every power $\ell \ne i$. Since $p$ has at least two nonzero coefficients, at least one of them is at a power $\ell \ne i$, so $p(Z) - AZ^i$ is a nonzero polynomial of degree at most $n$. So the probability is again at most $n/(q - 1)$.

In both cases, at most one wrong answer is possible, and it has probability at most $n/(q - 1)$. $\square$

The test `test_one_sparse_test_exactly` checks Lemma 1 for all $4^5$ vectors in $\{-1, 0, 1, 2\}^5$ and all $z$ modulo $q = 101$.

**The good event.** Let $G$ be the event that every call of DECODE on every level of every copy returns the answer of parts (a) and (b), or MANY on a level with two or more nonzero coordinates. The base $z$ of a copy is independent of $h$, so we may fix $h$ first; then each level vector is fixed and Lemma 1 applies. There are $R(L + 1)$ levels, so by the [union bound](/union-bound/)
$$\Pr[\text{not } G] \le \frac{R(L + 1)\,n}{q - 1}.$$
From here on we assume $G$.

**Lemma 2 (the answer of one copy).** Assume $G$, and let $U = \mathrm{supp}(x)$. If $U = \emptyset$, every level gives ZERO. If $U \ne \emptyset$, let $i^*$ be the coordinate of $U$ with the smallest hash value, and let $j^*$ be its deepest level. Then the copy returns $(i^*, x_{i^*})$ if no other coordinate of $U$ lies in $S_{j^*}$, and it stops with MANY otherwise.

*Proof.* If $U$ is empty, every level vector is zero and, under $G$, every DECODE returns ZERO. Now let $U \ne \emptyset$. A coordinate $\ell \in U$ lies in $S_j$ exactly when $h(\ell) < q/2^j$. For $j > j^*$, $h(i^*) \ge q/2^j$ by the choice of $j^*$, and every $\ell \in U$ has $h(\ell) \ge h(i^*)$, so $S_j \cap U = \emptyset$ and the level vector is zero. Under $G$, lines L7 go on past these levels. At level $j^*$, the vector is nonzero because $i^* \in S_{j^*}$. If $S_{j^*} \cap U = \{i^*\}$, the vector is 1-sparse and line L8 returns $(i^*, x_{i^*})$. Otherwise it has two or more nonzero coordinates, DECODE returns MANY, and line L8 stops the copy. $\square$

So under $G$ the query returns EMPTY exactly when $x = 0$ (line L9 is reached in the first copy), and otherwise it returns a correct pair $(i, x_i)$ with $x_i \ne 0$, or FAIL.

**Lemma 3 (one copy succeeds).** Model the hash as a truly random function: the values $h(\ell)/q$ for $\ell \in [n]$ are independent and uniform on $[0, 1)$, and $\ell \in S_j$ when $h(\ell)/q < 2^{-j}$. Let $s = |U| \ge 1$. Then, under $G$, one copy fails with probability at most $17/32$.

*Proof.* If $s = 1$, Lemma 2 shows that the copy never fails. Let $s \ge 2$, and let $u_1 < u_2$ be the two smallest values of $h(\ell)/q$ over $\ell \in U$ (ties have probability 0). By Lemma 2, the copy fails only if the coordinate with value $u_2$ also lies in $S_{j^*}$, that is $u_2 < 2^{-j^*}$.

If $j^* < L$, then $u_1 \ge 2^{-j^* - 1}$, since $j^*$ is the deepest level of $i^*$. So $u_2 < 2^{-j^*} \le 2u_1$. If $j^* = L$, then $u_2 < 2^{-L}$. Hence
$$\Pr[\text{fail}] \le \Pr[u_2 < 2u_1] + \Pr[u_2 < 2^{-L}].$$

For the first term, condition on $u_2 = t$. Given this, the one value below $t$ is uniform on $[0, t)$, because the $s$ values are independent and uniform. So $\Pr[u_1 > t/2 \mid u_2 = t] = 1/2$ for every $t$, and $\Pr[u_2 < 2u_1] = 1/2$.

For the second term, $u_2 < 2^{-L}$ needs two of the $s$ values below $2^{-L}$. By the union bound over pairs, this has probability at most $\binom{s}{2} 4^{-L} \le (s^2/2) \cdot (4n)^{-2} \le 1/32$, because $2^L \ge 4n$ and $s \le n$.

So one copy fails with probability at most $1/2 + 1/32 = 17/32$. $\square$

**Theorem 1 (correctness).** With a truly random hash in each copy and $R = \lceil \ln(1/\delta)/\ln(32/17) \rceil$ copies:

1. If $x = 0$, the query returns EMPTY, except with probability at most $R(L + 1)n/(q - 1)$.
2. If $x \ne 0$, the query returns FAIL with probability at most $\delta$, and a wrong answer with probability at most $R(L + 1)n/(q - 1)$. Every other answer is a pair $(i, x_i)$ with $x_i \ne 0$.
3. Under $G$, conditioned on not returning FAIL, the returned coordinate is uniform over $\mathrm{supp}(x)$.

*Proof.* Parts 1 and the second half of 2 follow from the bound on $\Pr[\text{not } G]$ and from Lemma 2. For the FAIL bound, the copies have independent seeds, so by Lemma 3 all $R$ copies fail together with probability at most $(17/32)^R \le \delta$, by the choice of $R$.

For part 3, look at one copy. By Lemma 2, whether it succeeds depends only on the sorted list of hash values of $U$, and when it succeeds it returns $i^*$, the coordinate with the smallest hash value. For a truly random $h$, the values $(h(\ell))_{\ell \in U}$ are independent and identically distributed, so the sorted list is independent of which coordinate takes the smallest value, and that coordinate is uniform over $U$. Hence, conditioned on the copy succeeding, $i^*$ is uniform over $U$. The query returns the answer of the first copy that succeeds, and the copies are independent, so conditioned on any copy succeeding, the returned coordinate is again uniform over $U$. $\square$

**Theorem 2 (space).** The sketch stores $3R(L + 1) = O(\log n \log(1/\delta))$ counters. If $M$ and $q$ are bounded by a polynomial in $n$, each counter has $O(\log n)$ bits, because $|A_j| \le nM$, $|B_j| \le n^2 M$ and $0 \le C_j < q$. Each copy also stores $k$ hash coefficients and $z$, $O(k \log n)$ bits. For constant $k$ the total is $O(\log^2 n \log(1/\delta))$ bits.

*Proof.* Count the counters: $R$ copies, $L + 1 = O(\log n)$ levels, three counters each, and $R = O(\log(1/\delta))$. The bounds on the counters follow from (1), since $|y^{(j)}_\ell| \le M$ and $\ell \le n$. $\square$

**What is not proved here.** Lemma 3 and part 3 of Theorem 1 use a truly random hash. The code uses a random polynomial of degree $k - 1$, which is only $k$-wise independent. Indyk (2001) showed that $O(\log(1/\varepsilon))$-wise independent families are $\varepsilon$-min-wise independent, which gives the uniformity up to a relative error $\varepsilon$; the success probability needs a similar argument. Jowhari, Sağlam and Tardos avoid this step with $s$-sparse recovery on $O(\log n)$ levels and obtain the same space with exact uniformity. The test `test_output_is_close_to_uniform` checks the uniformity of the code by experiment. $\blacksquare$
