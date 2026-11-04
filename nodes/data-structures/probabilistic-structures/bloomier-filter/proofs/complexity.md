---
title: The false positive rate of a Bloomier filter
proves: [complexity]
status: full
---

**Model.** Assume ideal hashing: for a key $x \notin S$, the cells $h_0(x), h_1(x), h_2(x)$ and the mask $\mu(x)$ are independent of each other, uniform on their ranges, and independent of the hash values of the keys of $S$. The arrays $T$ and $R$ are functions of the hash values of the keys of $S$ and of $f$ only.

**Theorem.** For each $x \notin S$, $\Pr[\text{LOOKUP}(x) \ne \bot] = 3/2^q$.

*Proof.* Fix $T$, $R$ and the cells of $x$, and let $a = T[h_0(x)] \oplus T[h_1(x)] \oplus T[h_2(x)]$, a fixed $q$-bit value. Then $\tau = \mu(x) \oplus a$. The map $y \mapsto y \oplus a$ is a bijection on $q$-bit values, and $\mu(x)$ is uniform and independent of $a$, so $\tau$ is uniform on the $2^q$ values. LOOKUP returns a value exactly when $\tau \in \{0, 1, 2\}$, which has probability $3/2^q$ for $q \ge 2$. Averaging over $T$, $R$ and the cells keeps this value. $\square$

**Space.** The two arrays take $M(q + r)$ bits. With $q = \lceil \log_2(3/\varepsilon) \rceil$ the rate is at most $\varepsilon$, and with $M = 1.23 n + O(1)$ the space is $1.23 n (\lceil \log_2(3/\varepsilon) \rceil + r) + O(q + r)$ bits.

**Time.** LOOKUP and SET compute one hash, read three cells of $T$ and one of $R$, and take $\Theta(1)$ time on the word RAM with $q, r \le w$. One attempt of BUILD computes $n$ hashes, runs PEEL in $O(M + n)$ steps and the assignment in $O(n)$ steps. The number of attempts depends on the peeling threshold, which is a result of Molloy (2005) and is not proved here. $\blacksquare$
