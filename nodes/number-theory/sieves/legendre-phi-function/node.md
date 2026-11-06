---
tag: VQFBZV
kind: definition
slug: legendre-phi-function
name: Legendre's phi function
aliases:
- phi(x, a)
- Legendre sum
- partial sieve function
area: number-theory/sieves
level: advanced
summary: phi(x, a) counts the n <= x that none of the first a primes divides. It obeys phi(x, a) = phi(x, a - 1) - phi(x / p_a, a - 1) and gives pi(x) = phi(x, a) + a - 1 for a = pi(x^(1/2)).
prereqs: [prime-counting-function, inclusion-exclusion-principle]
see_also: [meissel-lehmer-algorithm, prime-counting-function, lucy-hedgehog-prime-counting, buchstab-function, smooth-number, sieve-of-eratosthenes, mobius-function, sieve-theory]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 3.7.1, Combinatorial method (the function phi(x, a), its recursion, and Legendre's formula)
  - paper: doi:10.1090/S0025-5718-96-00674-6
    title: M. Deléglise and J. Rivat, Computing pi(x), the Meissel, Lehmer, Lagarias, Miller, Odlyzko method, Mathematics of Computation 65(213), 1996
    locator: Lemma 5.1 (the recursion for phi(x, a)) and the surrounding definitions
  - paper: doi:10.1090/S0025-5718-1985-0777285-5
    title: J. C. Lagarias, V. S. Miller and A. M. Odlyzko, Computing pi(x), the Meissel-Lehmer method, Mathematics of Computation 44(170), 1985
    locator: Section 2 (the Meissel-Lehmer formula in terms of phi(x, a))
---

Legendre's phi function $\phi(x, a)$ is the number of integers $n$ with $1 \le n \le x$ that are not divisible by any of the first $a$ primes $p_1 = 2, p_2 = 3, \ldots, p_a$. It is the count left after the first $a$ rounds of the [sieve of Eratosthenes](/sieve-of-eratosthenes/), and it gives Legendre's formula $\pi(x) = \phi(x, a) + a - 1$ for $a = \pi(\sqrt x)$, the first exact way to compute the [prime-counting function](/prime-counting-function/) without listing the primes. Its recursion $\phi(x, a) = \phi(x, a - 1) - \phi(x / p_a, a - 1)$ drives the [Meissel-Lehmer algorithm](/meissel-lehmer-algorithm/).

## Definition

For a real $x \ge 0$ and an integer $a \ge 0$, let $p_1 < p_2 < \cdots$ be the primes, and

$$\phi(x, a) = \#\{ n \in \mathbb{Z} : 1 \le n \le x,\ p_i \nmid n \text{ for } i = 1, \ldots, a \}.$$

So $\phi(x, 0) = \lfloor x \rfloor$, and the number $n = 1$ is always counted when $x \ge 1$. Two forms follow from the definition.

**Inclusion and exclusion.** With $P_a = p_1 p_2 \cdots p_a$ and the [Möbius function](/mobius-function/) $\mu$,

$$\phi(x, a) = \sum_{d \mid P_a} \mu(d) \left\lfloor \frac{x}{d} \right\rfloor,$$

since $\lfloor x/d \rfloor$ counts the multiples of $d$ up to $x$, and $\sum_{d \mid \gcd(n, P_a)} \mu(d)$ is 1 when $\gcd(n, P_a) = 1$ and 0 otherwise. This is the [inclusion-exclusion principle](/inclusion-exclusion-principle/), with $2^a$ terms.

**Recursion.** For $a \ge 1$,

$$\phi(x, a) = \phi(x, a - 1) - \phi\!\left( \frac{x}{p_a}, a - 1 \right).$$

*Proof.* The numbers counted by $\phi(x, a - 1)$ but not by $\phi(x, a)$ are the $n \le x$ free of $p_1, \ldots, p_{a-1}$ that are divisible by $p_a$. Write them as $n = p_a k$; then $1 \le k \le x / p_a$, and $k$ is free of $p_1, \ldots, p_{a-1}$, because $n$ is. Conversely each such $k$ gives such an $n$. So there are exactly $\phi(x / p_a, a - 1)$ of them. $\square$

Since $\lfloor \lfloor x \rfloor / m \rfloor = \lfloor x / m \rfloor$ for integers $m \ge 1$, the arguments can be kept as the integers $\lfloor x / m \rfloor$.

**Legendre's formula.** Let $a = \pi(\sqrt x)$. Then

$$\pi(x) = \phi(x, a) + a - 1.$$

*Proof.* A number $1 < n \le x$ counted by $\phi(x, a)$ has no prime factor $p \le \sqrt x$. If it were composite, its least prime factor $q$ would satisfy $q^2 \le n \le x$, which is impossible; so it is a prime $p > \sqrt x$. Conversely every prime $\sqrt x < p \le x$ is counted. So $\phi(x, a) = 1 + (\pi(x) - a)$, where the 1 is for $n = 1$. $\square$

**Periodicity.** Whether $n$ is free of $p_1, \ldots, p_a$ depends only on $n \bmod P_a$, so $\phi(x + k P_a, a) = \phi(x, a) + k \varphi(P_a)$ for integers $k \ge 0$, where $\varphi$ is [Euler's totient](/euler-totient/). Programs use this, with a table for $a \le 6$ or 7, to answer small values of $a$ in $O(1)$.

**Size.** For fixed $a$, $\phi(x, a) = x \prod_{i \le a} (1 - 1/p_i) + O(2^a)$, from the inclusion-exclusion sum. When $a$ grows with $x$, the error term $2^a$ is useless, and the right size comes from the [Buchstab function](/buchstab-function/): with $p_a \approx x^{1/u}$, $\phi(x, a) \sim u \, \omega(u) \, x / \ln x$ for fixed $u > 1$.

## Examples and non-examples

| $a$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $p_a$ | | 2 | 3 | 5 | 7 |
| $\phi(100, a)$ | 100 | 50 | 33 | 26 | 22 |

- **The recursion at work.** $\phi(100, 2) = \phi(100, 1) - \phi(33, 1) = 50 - 17 = 33$, and $\phi(100, 4) = \phi(100, 3) - \phi(14, 3) = 26 - 4 = 22$, where $\phi(14, 3)$ counts 1, 7, 11 and 13.
- **Legendre's formula.** For $x = 100$, $a = \pi(10) = 4$, and $\phi(100, 4) = 22$ counts 1 and the 21 primes from 11 to 97. So $\pi(100) = 22 + 4 - 1 = 25$. For $x = 1000$, $a = \pi(31) = 11$, $\phi(1000, 11) = 158$ and $\pi(1000) = 158 + 10 = 168$.
- **Periodicity.** With $P_3 = 30$ and $\varphi(30) = 8$: $\phi(190, 3) = \phi(100, 3) + 3 \cdot 8 = 50$.
- **Non-example: dropping 1.** The count of $2 \le n \le x$ free of the first $a$ primes is $\phi(x, a) - 1$, not $\phi(x, a)$. Mixing the two conventions shifts Legendre's formula by one.
- **Non-example: $a$ too small.** With $a = \pi(x^{1/3})$, Legendre's formula fails: $\phi(x, a)$ then also counts products of two primes larger than $p_a$. For $x = 100$ and $a = \pi(4) = 2$, $\phi(100, 2) = 33$ includes $25 = 5^2$, $35$, $49$, $55$, $65$, $77$, $85$, $91$ and $95$. The [Meissel-Lehmer algorithm](/meissel-lehmer-algorithm/) adds the correction $P_2(x, a)$ for exactly these numbers.

## Related definitions

- **$P_k(x, a)$.** The number of $n \le x$ with exactly $k$ prime factors, counted with multiplicity, all larger than $p_a$. Then $\phi(x, a) = \sum_{k \ge 0} P_k(x, a)$ with $P_0 = 1$ and $P_1 = \pi(x) - a$; the Meissel-Lehmer method computes $P_2$.
- **The rough number count $\Phi(x, y)$.** The number of $n \le x$ all of whose prime factors exceed $y$, so $\Phi(x, p_a) = \phi(x, a)$. Its asymptotics give the [Buchstab function](/buchstab-function/).
- **Smooth numbers.** The complementary notion of [smooth numbers](/smooth-number/): $\Psi(x, y)$ counts $n \le x$ with all prime factors at most $y$.
- **Sieve functions.** In [sieve theory](/sieve-theory/), $S(\mathcal{A}, \mathcal{P}, z)$ counts the elements of a set $\mathcal{A}$ free of the primes of $\mathcal{P}$ below $z$; $\phi(x, a)$ is the case $\mathcal{A} = \{1, \ldots, \lfloor x \rfloor\}$ and $z = p_a + 1$.

## References
