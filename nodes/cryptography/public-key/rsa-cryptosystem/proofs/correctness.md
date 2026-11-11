---
title: RSA decryption inverts RSA encryption for every message representative
proves: [correctness]
status: full
---

Let $p \ne q$ be odd primes, $n = pq$, $\varphi(n) = (p-1)(q-1)$ and $\lambda(n) = \mathrm{lcm}(p-1, q-1)$. Let $e \ge 3$ with $\gcd(e, \lambda(n)) = 1$, and let $d$ be a positive integer with $ed \equiv 1 \pmod{\lambda(n)}$. The public key is $(n, e)$ and the private key holds $d$, or the quintuple $(p, q, dP, dQ, qInv)$ with $e \cdot dP \equiv 1 \pmod{p-1}$, $e \cdot dQ \equiv 1 \pmod{q-1}$ and $q \cdot qInv \equiv 1 \pmod p$, as in RFC 8017 Section 3.2.

**Lemma 1.** For every integer $a$ and every prime $r$ with $r \mid n$, and every multiple $L$ of $r - 1$, we have $a^{1+L} \equiv a \pmod r$.

*Proof.* Two cases. If $r \mid a$, then both sides are $0$ modulo $r$, because $1 + L \ge 1$. If $r \nmid a$, then Fermat's little theorem gives $a^{r-1} \equiv 1 \pmod r$. Write $L = (r-1)t$ with $t \ge 0$ an integer. Then $a^{1+L} = a \cdot (a^{r-1})^{t} \equiv a \cdot 1^{t} = a \pmod r$. $\square$

**Theorem 1 (correctness of the single exponent form).** For every integer $m$ with $0 \le m < n$, $(m^e)^d \equiv m \pmod n$, and the reduction of $(m^e \bmod n)^d$ modulo $n$ equals $m$.

*Proof.* Because $ed \equiv 1 \pmod{\lambda(n)}$ and $ed \ge 1$, we can write $ed = 1 + L$ with $L = k \lambda(n)$ for an integer $k \ge 0$. Now $p - 1$ divides $\lambda(n)$, so $p-1$ divides $L$. Lemma 1 with $r = p$ gives $m^{ed} \equiv m \pmod p$. The same argument with $r = q$ gives $m^{ed} \equiv m \pmod q$. So $p$ and $q$ both divide $m^{ed} - m$. The primes are distinct, so their product $n$ divides $m^{ed} - m$, which is the first claim. The number $m^{ed} \bmod n$ is therefore $m \bmod n$, and $0 \le m < n$ gives $m \bmod n = m$. The exponentiation can be done in two steps, because $(m^e \bmod n)^d \equiv m^{ed} \pmod n$. $\blacksquare$

The proof uses $\lambda(n)$, and it works the same with $\varphi(n)$ in place of $\lambda(n)$, because $\lambda(n)$ divides $\varphi(n)$: each multiple of $\varphi(n)$ is a multiple of $p-1$ and of $q-1$. Nothing in the proof needs $\gcd(m, n) = 1$. An argument through Euler's theorem alone, which needs an invertible $m$, misses the messages that are a multiple of $p$ or of $q$.

**Theorem 2 (correctness of CRT decryption).** Let $0 \le c < n$. Let $m_1 = c^{dP} \bmod p$, $m_2 = c^{dQ} \bmod q$, $h = (m_1 - m_2) \cdot qInv \bmod p$ and $m = m_2 + qh$. Then $0 \le m < n$ and $m \equiv c^{d} \pmod n$, so $m = c^d \bmod n$.

*Proof.* First, $dP \ge 1$: the condition $e \cdot dP \equiv 1 \pmod{p-1}$ with $p - 1 \ge 2$ excludes $dP = 0$, since $0 \not\equiv 1 \pmod{p-1}$. The same holds for $dQ$.

**Lemma 2.** Let $r$ be a prime, and let $u \ge 1$ and $v \ge 1$ be integers with $u \equiv v \pmod{r-1}$. Then $c^u \equiv c^v \pmod r$ for every integer $c$.

*Proof.* If $r \mid c$, then both sides are $0$ modulo $r$, because both exponents are at least 1. If $r \nmid c$, then $c$ is invertible modulo $r$ and $c^{r-1} \equiv 1 \pmod r$ by Fermat's little theorem. Write $u - v = k(r-1)$ with $k$ an integer, possibly negative. Then $c^{u-v} = (c^{r-1})^{k} \equiv 1^{k} = 1 \pmod r$, where a negative $k$ is read with the inverse of $c$ modulo $r$. Multiply by $c^v$ to get $c^u \equiv c^v \pmod r$. $\square$

Now $d$ and $dP$ are both at least 1 and are congruent modulo $p-1$: from $e \cdot d \equiv 1 \equiv e \cdot dP \pmod{p-1}$ and the fact that $e$ is invertible modulo $p-1$ (it is invertible modulo $\lambda(n)$, and $p-1$ divides $\lambda(n)$). Lemma 2 with $r = p$ gives $c^{dP} \equiv c^{d} \pmod p$, so $m_1 = c^{d} \bmod p$. The same argument modulo $q$ gives $m_2 = c^{d} \bmod q$.

Now the bounds. We have $0 \le m_2 < q$ and $0 \le h < p$, so $0 \le m = m_2 + qh \le (q-1) + q(p-1) = pq - 1 < n$.

Last, the two congruences. Modulo $q$: $m = m_2 + qh \equiv m_2 \equiv c^d \pmod q$. Modulo $p$: $q \cdot qInv \equiv 1$, so $qh \equiv q (m_1 - m_2) qInv \equiv m_1 - m_2 \pmod p$, and therefore $m \equiv m_2 + m_1 - m_2 = m_1 \equiv c^d \pmod p$. The two primes are distinct, so by the Chinese remainder theorem $m \equiv c^d \pmod n$. With $0 \le m < n$ this gives $m = c^d \bmod n$. $\blacksquare$

**Corollary.** With $c = m^e \bmod n$ and $0 \le m < n$, CRT decryption returns $m$. This follows from Theorem 2 and then Theorem 1.

**Termination of key generation.** Each round of the loop of line L1 draws two primes. The round stops the loop when $p \ne q$, when $\gcd(e, (p-1)(q-1)) = 1$ and when $pq$ has the wanted number of bits. Each of the three conditions holds with a probability bounded away from 0 for a fixed $e$ and a fixed bit length, so the expected number of rounds is finite. The number of rounds is a geometric random variable, so the loop stops with probability 1.
