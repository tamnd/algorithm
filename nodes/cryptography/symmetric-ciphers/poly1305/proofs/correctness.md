---
title: Poly1305 computes its polynomial, the encoding is injective, and the differential bound holds
proves: [correctness]
status: full
---

Let $p = 2^{130} - 5$, which is prime (Bernstein, Theorem 3.1, by Pocklington's theorem). For a message $M$ of $\ell \ge 0$ bytes, let $q = \lceil \ell / 16 \rceil$ and let $B_1, \ldots, B_q$ be its 16-byte chunks, the last of length $k_q \in \{1, \ldots, 16\}$. Line L5 sets $c_i = \mathrm{LE}(B_i) + 2^{8|B_i|}$. Write $\bar{M}(x) = \sum_{i=1}^{q} c_i x^{q+1-i}$, an integer polynomial with zero constant term, and $H_r(M) = (\bar{M}(r) \bmod p) \bmod 2^{128}$.

**Lemma 1 (range of the coefficients).** For every chunk, $2^8 \le c_i \le 2^{129} - 1$, and $c_i$ determines the length $|B_i|$ and the bytes of $B_i$.

*Proof.* $\mathrm{LE}(B_i) < 2^{8|B_i|}$, so $c_i$ has its highest set bit at position $8|B_i|$, with $1 \le |B_i| \le 16$. Hence $2^8 \le c_i < 2^{8|B_i|+1} \le 2^{129}$, and the position of the highest bit gives $|B_i|$, after which $\mathrm{LE}(B_i) = c_i - 2^{8|B_i|}$ gives the bytes. $\square$

**Lemma 2 (Horner's rule).** After the loop of lines L4 to L6, $a = \bar{M}(r) \bmod p$.

*Proof.* Let $a_j$ be the value after $j$ iterations, so $a_0 = 0$ and $a_j = (a_{j-1} + c_j) r \bmod p$. We show $a_j \equiv \sum_{i=1}^{j} c_i r^{j+1-i} \pmod p$ by induction. For $j = 0$ both sides are $0$. If it holds for $j - 1$, then $a_j \equiv \bigl(\sum_{i=1}^{j-1} c_i r^{j-i} + c_j\bigr) r = \sum_{i=1}^{j} c_i r^{j+1-i}$. Since $a_j$ is reduced into $[0, p)$, for $j = q$ it equals $\bar{M}(r) \bmod p$. $\square$

**Lemma 3 (correctness of the tag and of verification).** The tag is $T = (H_r(M) + s) \bmod 2^{128}$, and VERIFY accepts it.

*Proof.* By Lemma 2 and line L7, $T = ((\bar{M}(r) \bmod p) + s) \bmod 2^{128}$, and $((x \bmod 2^{128}) + s) \bmod 2^{128} = (x + s) \bmod 2^{128}$, which equals $(H_r(M) + s) \bmod 2^{128}$. The computation is deterministic, so line L9 recomputes the same 16 bytes, and the comparison of equal strings succeeds. $\square$

**Lemma 4 (injectivity; Bernstein, Theorem 3.2).** Let $M, M'$ be messages and $u$ an integer. If every coefficient of $\bar{M}'(x) - \bar{M}(x) - u$ is divisible by $p$, then $M = M'$.

*Proof.* Let $q, q'$ be the numbers of chunks. Suppose $q' > q$. The coefficient of $x^{q'}$ in $\bar{M}' - \bar{M} - u$ is $c'_1$, since $\bar{M}$ has degree at most $q < q'$ and $u$ is a constant ($q' \ge 1$). By Lemma 1, $0 < c'_1 < 2^{129} < p$, so $p \nmid c'_1$: a contradiction. In the same way $q > q'$ is impossible, so $q = q'$. For $1 \le i \le q$ the coefficient of $x^{q+1-i}$ is $c'_i - c_i$, with $|c'_i - c_i| < 2^{129} < p$ by Lemma 1, so divisibility by $p$ forces $c'_i = c_i$. By Lemma 1 the chunks are then equal, including the length of the last one, so $M = M'$. $\square$

**Theorem (differential bound; Bernstein, Theorem 3.3).** Let $M \ne M'$ be messages of at most $L$ bytes, let $g \in [0, 2^{128})$ and let $R$ be any set of integers in $[0, p)$. Then at most $8 \lceil L/16 \rceil$ values $r \in R$ satisfy $H_r(M) \equiv H_r(M') + g \pmod{2^{128}}$. So for $r$ uniform in the $2^{106}$ clamped values, this holds with probability at most $8 \lceil L/16 \rceil / 2^{106}$.

*Proof.* Let $U$ be the set of integers in $[-(p - 1), p - 1]$ that are congruent to $g$ modulo $2^{128}$. Since this interval has fewer than $2p < 2^{131} = 8 \cdot 2^{128}$ integers, $|U| \le 8$. If the congruence holds for $r$, then $d = (\bar{M}(r) \bmod p) - (\bar{M}'(r) \bmod p)$ lies in $[-(p-1), p-1]$ and is congruent to $g$ modulo $2^{128}$, so $d = u$ for some $u \in U$. Then $\bar{M}(r) - \bar{M}'(r) - u \equiv 0 \pmod p$, so $r$ is a root modulo $p$ of the polynomial $\bar{M} - \bar{M}' - u$. By Lemma 4 (applied with the roles of $M$ and $M'$ exchanged), this polynomial is nonzero modulo $p$. Its degree is at most $\max(q, q') \le \lceil L/16 \rceil$, and a nonzero polynomial of degree $d$ over the field $\mathbb{Z}_p$ has at most $d$ roots. Summing over the at most 8 values of $u$ gives at most $8 \lceil L/16 \rceil$ values of $r$. $\blacksquare$

**Remark (one-time security).** If $(r, s)$ is uniform with $r$ clamped and the attacker sees $T = (H_r(M) + s) \bmod 2^{128}$, then $T$ is uniform and independent of $r$, because $s$ is uniform modulo $2^{128}$. A forgery $(M', T')$ with $M' \ne M$ is accepted exactly when $H_r(M') \equiv H_r(M) + (T' - T) \pmod{2^{128}}$, and by the theorem with $g = T' - T \bmod 2^{128}$ this has probability at most $8\lceil L/16 \rceil / 2^{106}$. The key reuse attack of the main page is the opposite case: with two tags under one $s$, the difference $T_1 - T_2$ no longer has a mask, and Lemma 2 gives a linear equation for $r$ modulo $p$.
