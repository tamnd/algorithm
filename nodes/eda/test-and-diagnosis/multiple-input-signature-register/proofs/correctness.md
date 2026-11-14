---
title: The MISR signature is a remainder, and a single wrong bit always changes it
proves: [correctness]
status: full
---

We use the notation of the page. The ring is GF(2)[x], so plus and minus are the same. The register $r$ and the input words $w_t$ are polynomials of degree less than $k$, and $q$ has degree exactly $k \ge 1$. For a polynomial $a$, $a \bmod q$ is the unique polynomial $b$ of degree less than $k$ with $q \mid a - b$.

**Lemma 1 (one clock).** For a register $r$ and a word $w$, lines L1 to L4 of `CLOCK` leave $r' = (x\,r + w) \bmod q$.

*Proof.* Write $r = r_{k-1} x^{k-1} + r_{<}$ with $\deg r_< < k - 1$. Line L1 reads $r_{k-1}$. Line L2 forms $x\,r_<$, which has degree less than $k$. If $r_{k-1} = 0$, then $x\,r = x\,r_<$ and line L3 does nothing. If $r_{k-1} = 1$, then $x\,r = x^k + x\,r_<$, and line L3 forms $x\,r_< + (q - x^k) = x\,r + q$. In both cases the result after line L3 has degree less than $k$ and differs from $x\,r$ by a multiple of $q$, so it is $x\,r \bmod q$. Line L4 adds $w$, which has degree less than $k$, so the sum still has degree less than $k$ and differs from $x\,r + w$ by a multiple of $q$. So it is $(x\,r + w) \bmod q$. $\blacksquare$

**Theorem 1 (the signature).** After `RESET(s)` and the clocks with $w_0, \ldots, w_{m-1}$, the register holds
$$S_m = \Big( x^m s + \sum_{t=0}^{m-1} x^{m-1-t} w_t \Big) \bmod q.$$

*Proof.* By induction on $m$. For $m = 0$, `RESET(s)` stores $s$, and $s$ has degree less than $k$, so $s = s \bmod q$. Assume the claim for $m$. By Lemma 1 the next clock gives
$$\big(x S_m + w_m\big) \bmod q = \Big( x^{m+1} s + \sum_{t=0}^{m-1} x^{m-t} w_t + w_m \Big) \bmod q,$$
since $x S_m$ differs from $x$ times the polynomial in the claim for $m$ by a multiple of $q$. The sum is $x^{m+1} s + \sum_{t=0}^{m} x^{m-t} w_t$, which is the claim for $m + 1$. $\blacksquare$

**Corollary 1 (the stream view).** Write $w_{t,i}$ for the coefficient of $x^i$ in $w_t$ and $W_i = \sum_t w_{t,i}\, x^{m-1-t}$. Then $\sum_t x^{m-1-t} w_t = \sum_t \sum_i w_{t,i}\, x^{m-1-t+i} = \sum_i x^i W_i$, so the signature is $\big(x^m s + \sum_i x^i W_i\big) \bmod q$. $\blacksquare$

**Theorem 2 (errors).** Let the good words be $w_t$ and the faulty words $w_t + e_t$, with the same seed $s$. The two signatures differ by $E \bmod q$, where
$$E = \sum_{t=0}^{m-1} x^{m-1-t} e_t = \sum_{t, i} e_{t,i}\, x^{m-1-t+i}.$$
So the faulty signature equals the good one exactly when $q$ divides $E$.

*Proof.* The map $a \mapsto a \bmod q$ is linear over GF(2): if $q \mid a - a'$ and $q \mid b - b'$ then $q \mid (a + b) - (a' + b')$. By Theorem 1 the faulty signature is $\big(x^m s + \sum_t x^{m-1-t} w_t + E\big) \bmod q$, which is the good signature plus $E \bmod q$. The two are equal exactly when $E \bmod q = 0$, that is when $q \mid E$. $\blacksquare$

**Theorem 3 (single wrong bits).** If $q_0 = 1$, then a stream with exactly one wrong bit never gives the good signature.

*Proof.* One wrong bit, at clock $t$ on input $i$, gives $E = x^j$ with $j = m - 1 - t + i \ge 0$. Suppose $q \mid x^j$, so $x^j = q\,u$ for some $u$. Put $x = 0$. If $j \ge 1$ the left side is 0 and the right side is $q_0 u(0) = u(0)$, so $u(0) = 0$ and $x \mid u$, and we may divide both sides by $x$ and repeat with $j - 1$. After $j$ steps we reach $1 = q\,u'$, which is impossible since $\deg q = k \ge 1$. So $q \nmid E$, and by Theorem 2 the signatures differ. $\blacksquare$

**Theorem 4 (pairs of wrong bits).** Two wrong bits $(t, i)$ and $(t', i')$ give the exponents $a = m - 1 - t + i$ and $b = m - 1 - t' + i'$.

1. If $a = b$, the pair always aliases. This happens in particular for $(t, i)$ and $(t + 1, i + 1)$.
2. If $a > b$ and $q_0 = 1$, the pair aliases exactly when $q \mid x^{a-b} + 1$.

*Proof.* If $a = b$, then $E = x^a + x^a = 0$, and $q$ divides 0. For $(t + 1, i + 1)$ the exponent is $m - 1 - (t + 1) + (i + 1) = a$. If $a > b$, then $E = x^b (x^{a-b} + 1)$. As in Theorem 3, $q_0 = 1$ means that $q$ and $x^b$ have no common factor other than 1, since every common factor divides $x^b$ and so is a power of $x$, and $x \nmid q$. So $q \mid E$ exactly when $q \mid x^{a-b} + 1$. $\blacksquare$

For a primitive $q$ of degree $k$, the least $n \ge 1$ with $q \mid x^n + 1$ is $2^k - 1$, and $q \mid x^n + 1$ exactly when $2^k - 1$ divides $n$. So with a primitive $q$, two wrong bits with different exponents alias exactly when their exponents differ by a multiple of $2^k - 1$.
