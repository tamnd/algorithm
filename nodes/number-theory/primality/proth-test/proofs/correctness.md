---
title: Correctness of Proth's test
proves: [correctness, termination, error]
status: full
---

Let $n = k \cdot 2^m + 1$ with $k$ odd, $m \ge 1$ and $k < 2^m$, so $n \ge 3$ is odd. We prove that PROTH-TEST stops on $n$, that it returns PRIME only if $n$ is prime, and that it returns COMPOSITE only if $n$ is composite. Since it is deterministic, it then has no error.

**Lemma 1** (Proth's theorem; Crandall and Pomerance, Exercise 4.10). If $a^{(n-1)/2} \equiv -1 \pmod n$ for some integer $a$, then $n$ is prime.

*Proof.* Let $p$ be a prime factor of $n$; $p$ is odd. From $a^{(n-1)/2} \equiv -1 \pmod p$ we get $p \nmid a$, $a^{n-1} \equiv 1 \pmod p$, and $a^{(n-1)/2} \not\equiv 1 \pmod p$, because $-1 \not\equiv 1$ modulo an odd prime. Let $d$ be the order of $a$ modulo $p$. Then $d \mid n - 1 = k \cdot 2^m$ and $d \nmid (n-1)/2 = k \cdot 2^{m-1}$. If $2^m \nmid d$, then $d \mid k \cdot 2^{m-1}$, since $d \mid k \cdot 2^m$ and the power of 2 in $d$ is at most $2^{m-1}$; that is false. So $2^m \mid d$, and $d \mid p - 1$ by Fermat's little theorem, so $p \ge 2^m + 1$. As $k \le 2^m - 1$, $n \le (2^m - 1) 2^m + 1 < 2^{2m}$, so $\sqrt n < 2^m < p$. Every prime factor of $n$ exceeds $\sqrt n$. If $n$ were composite, it would be a product of at least two primes, each larger than $\sqrt n$, so $n > n$, a contradiction. $\square$

**Lemma 2** (Euler's criterion). If $n$ is an odd prime and $\left(\frac{a}{n}\right) = -1$, then $a^{(n-1)/2} \equiv -1 \pmod n$.

*Proof.* For a prime modulus the Jacobi symbol is the Legendre symbol, and Euler's criterion states $a^{(n-1)/2} \equiv \left(\frac{a}{n}\right) \pmod n$ for $n \nmid a$. $\square$

**Lemma 3.** If $n$ is odd and not a perfect square, then some integer $a$ with $2 \le a \le n - 1$ has $\left(\frac{a}{n}\right) \ne 1$.

*Proof.* Write $n = \prod p_i^{e_i}$. Since $n$ is not a square, some $e_j$ is odd. Choose $b$ a quadratic non-residue modulo $p_j$, and by the Chinese remainder theorem an $a$ with $a \equiv b \pmod {p_j}$ and $a \equiv 1 \pmod {p_i}$ for $i \ne j$, with $0 < a < n$. Then $\left(\frac{a}{n}\right) = \prod \left(\frac{a}{p_i}\right)^{e_i} = (-1)^{e_j} = -1$. As $\left(\frac{1}{n}\right) = 1$, $a \ne 1$, so $2 \le a \le n - 1$. $\square$

**Termination.** Line L1 computes $k$ and $m$ by halving $n - 1$ at most $\lg n$ times. If line L2 does not return, $n$ is not a square, and by Lemma 3 the loop of line L4 stops at some $a \le n - 1$. Lines L5 to L8 are a fixed number of steps. So the test stops.

**PRIME is right.** Line L7 returns PRIME only if $a^{(n-1)/2} \bmod n = n - 1$, that is $a^{(n-1)/2} \equiv -1 \pmod n$. By Lemma 1, $n$ is prime.

**COMPOSITE is right.** There are three cases.

- *Line L2.* A perfect square $n = r^2$ with $n \ge 3$ has $r \ge 2$ and $1 < r < n$, so $n$ is composite.
- *Line L5.* Here $\left(\frac{a}{n}\right) = 0$, which happens only if $g = \gcd(a, n) > 1$. By the termination argument $a \le n - 1$, so $g \le a < n$ and $g$ is a proper factor of $n$.
- *Line L8.* Here line L4 stopped with $\left(\frac{a}{n}\right) \ne 1$, line L5 did not return, so $\left(\frac{a}{n}\right) = -1$, and line L7 found $a^{(n-1)/2} \not\equiv -1 \pmod n$. If $n$ were prime, Lemma 2 would give $a^{(n-1)/2} \equiv -1$. So $n$ is composite.

**Error.** The test uses no randomness and both answers are proved, so it is exact on every Proth number. For an input that is not a Proth number, line L1 raises an error and no answer is given. $\blacksquare$
