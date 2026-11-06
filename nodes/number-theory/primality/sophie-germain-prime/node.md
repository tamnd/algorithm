---
tag: WED7E4
kind: definition
slug: sophie-germain-prime
name: Sophie Germain prime
aliases:
- Germain prime
area: number-theory/primality
level: core
summary: A prime q such that 2q+1 is also prime. The number 2q+1 is then a safe prime. Nobody has proved that there are infinitely many, but a conjecture predicts about 1.32 x/(log x)^2 of them up to x.
prereqs: [prime-number, euler-criterion]
see_also: [safe-prime, mersenne-prime, random-prime-generation, aks-primality-test, prime-number-theorem, prime-counting-function, quadratic-reciprocity, diffie-hellman]
sources:
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 5.5.5 (definition, Conjectures 5.24 and 5.25), Exercises 10.5 and 10.6, and Section 21.3 (notes) with Exercise 21.1
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Exercise 1.47 (Sophie Germain primes and Mersenne numbers) and Section 4.5.2 (Sophie Germain primes in the AKS test)
---

A Sophie Germain prime is a [prime](/prime-number/) $q$ such that $2q + 1$ is also prime. The prime $2q + 1$ is then called a [safe prime](/safe-prime/), and cryptography uses such pairs because the group of units modulo $2q + 1$ has order $2q$. Whether there are infinitely many Sophie Germain primes is an open problem, but a precise conjecture predicts how many there are, and algorithms such as the [AKS test](/aks-primality-test/) run faster if that conjecture is true.

## Definition

A prime $q$ is a **Sophie Germain prime** if $2q + 1$ is also prime (Shoup, Section 5.5.5). Write $\pi^*(x)$ for the number of Sophie Germain primes $q \le x$.

**Residues.** Each Sophie Germain prime $q > 5$ satisfies $q \equiv 11$, $23$ or $29 \pmod{30}$. *Proof.* $q$ is odd. If $q \equiv 1 \pmod 3$, then $3 \mid 2q + 1$, and $2q + 1 > 3$ is not prime; so $q \equiv 2 \pmod 3$. If $q \equiv 2 \pmod 5$, then $5 \mid 2q + 1$; so $q \equiv 1, 3$ or $4 \pmod 5$. The odd residues modulo 30 that are $2 \bmod 3$ and $1$, $3$ or $4 \bmod 5$ are $11$, $23$ and $29$. $\square$ In particular $q \equiv 5 \pmod 6$ for $q > 3$, and the safe prime $2q + 1$ is then $\equiv 11 \pmod{12}$.

**Density conjecture** (Shoup, Conjecture 5.24). $\pi^*(x) \sim C x / (\log x)^2$, where
$$C = 2 \prod_{p > 2} \frac{p(p-2)}{(p-1)^2} \approx 1.32032,$$
and the product is over the odd primes. This is a special case of Dickson's conjecture on several linear forms $a_i m + b_i$ being prime at once (Shoup, Conjecture 5.25). The heuristic behind it: a random $q$ near $x$ is prime with probability about $1/\log x$, and so is $2q + 1$; the constant $C$ corrects for the fact that the two events are not independent modulo each small prime. No proof is known even of $\pi^*(x) \to \infty$.

**Divisors of Mersenne numbers.** Let $q$ be a Sophie Germain prime and $p = 2q + 1$. If $q \equiv 3 \pmod 4$, then $p \mid 2^q - 1$; if $q \equiv 1 \pmod 4$, then $p \mid 2^q + 1$. *Proof.* $2^q = 2^{(p-1)/2} \equiv \left(\frac{2}{p}\right) \pmod p$ by [Euler's criterion](/euler-criterion/). By the second supplement to [quadratic reciprocity](/quadratic-reciprocity/), $\left(\frac{2}{p}\right) = 1$ exactly when $p \equiv \pm 1 \pmod 8$. If $q \equiv 3 \pmod 4$ then $p \equiv 7 \pmod 8$, and if $q \equiv 1 \pmod 4$ then $p \equiv 3 \pmod 8$. $\square$ So for a Sophie Germain prime $q > 3$ with $q \equiv 3 \pmod 4$, the Mersenne number $2^q - 1$ is composite, since its factor $2q + 1$ is smaller than it (Crandall and Pomerance, Exercise 1.47).

## Examples and non-examples

**Examples.**

- The Sophie Germain primes below 1000 are $2, 3, 5, 11, 23, 29, 41, 53, 83, 89, 113, 131, 173, 179, 191, 233, 239, 251, 281, 293, 359, 419, 431, 443, 491, 509, 593, 641, 653, 659, 683, 719, 743, 761, 809, 911, 953$. There are 37 of them, against 168 primes.
- Counts against the conjecture:

| $x$ | $10^3$ | $10^4$ | $10^5$ | $10^6$ | $10^7$ |
|---|---|---|---|---|---|
| $\pi^*(x)$ | 37 | 190 | 1171 | 7746 | 56032 |
| $C x / (\ln x)^2$, rounded | 28 | 156 | 996 | 6917 | 50822 |
| ratio | 1.337 | 1.221 | 1.176 | 1.120 | 1.103 |
| $C \int_2^x dt / (\ln t)^2$, rounded | 46 | 214 | 1249 | 8248 | 58754 |

The ratio moves slowly toward 1, as for $x/\ln x$ in the [prime number theorem](/prime-number-theorem/). The integral form of the estimate is closer for $x \ge 10^4$.

- $q = 11$: $2q + 1 = 23$ is prime, and $11 \equiv 3 \pmod 4$, so $23 \mid 2^{11} - 1 = 2047 = 23 \cdot 89$. Likewise $47 \mid 2^{23} - 1 = 47 \cdot 178481$ and $167 \mid 2^{83} - 1$.
- $q = 5$ and $q = 29$ are $\equiv 1 \pmod 4$: $11 \mid 2^5 + 1 = 33$ and $59 \mid 2^{29} + 1$.
- **Cunningham chains.** Repeating $q \mapsto 2q + 1$ can give several primes in a row: $2, 5, 11, 23, 47$ (then $95$ is composite), and $89, 179, 359, 719, 1439, 2879$ (then $5759 = 13 \cdot 443$). Each member except the last is a Sophie Germain prime, and each member except the first is a safe prime.
- Crandall and Pomerance (Exercise 1.47) quote the Sophie Germain prime $q = 18458709 \cdot 2^{32611} - 1$, found by Kerchner and Gallot; as $q \equiv 3 \pmod 4$, the Mersenne number $2^q - 1$ is composite.

**Non-examples.**

- $7$: $2 \cdot 7 + 1 = 15 = 3 \cdot 5$. $13$: $27 = 3^3$. $17$: $35 = 5 \cdot 7$. $19$: $39 = 3 \cdot 13$. These fail by the residue rule: $7, 13, 19 \equiv 1 \pmod 3$, and $17 \equiv 2 \pmod 5$.
- $9$: $2 \cdot 9 + 1 = 19$ is prime, but $9$ is not.
- $37 \equiv 7 \pmod{30}$ is prime, and $75$ is divisible by 3 and 5, so the residue rule excludes it before any test.

## Related definitions

- **[Safe prime](/safe-prime/).** The prime $p = 2q + 1$ for a Sophie Germain prime $q$. The group $\mathbb{Z}_p^*$ has order $2q$, which is the structure [Diffie-Hellman](/diffie-hellman/) groups want.
- **Generation.** Shoup (Exercises 10.5 and 10.6) gives a [random prime generation](/random-prime-generation/) method: draw $q$, run Miller-Rabin on $q$ and then on $2q + 1$. Under Conjecture 5.24 it runs in expected time $O(\ell^5 + k \ell^3)$ for numbers of $\ell$ bits and $k$ rounds, and outputs a non-Sophie-Germain number with probability $O(4^{-k} \ell^2)$. The improved version reaches error $O(\gamma(m, k) \ell)$, where $\gamma(m, k)$ is the error of the plain prime generator. The expected number of candidates grows like $\ell^2$ under the conjecture, against $\ell$ for a plain random prime.
- **Use in AKS.** The [AKS test](/aks-primality-test/) needs a small modulus $r$ with a large order of $n$ modulo $r$. If $r = 2q + 1$ for a Sophie Germain prime $q$, then the order of $n$ modulo $r$ is $1$, $2$, $q$ or $2q$, and it is large unless $r \mid n \pm 1$. If Conjecture 5.24 is true, a suitable $r = O((\log n)^2)$ exists, and the running time drops from $O((\log n)^{10.5 + o(1)})$ to $O((\log n)^{6 + o(1)})$ (Shoup, Section 21.3 and Exercise 21.1; Crandall and Pomerance, Section 4.5.2). Lenstra and Pomerance later reached the bound $O((\log n)^{6 + o(1)})$ with no conjecture, by a different method.
- **Twin primes and Dickson's conjecture.** Pairs $(m, m + 2)$ and $(m, 2m + 1)$ of primes are both special cases of Dickson's conjecture, and neither is known to be infinite.
- **[Mersenne prime](/mersenne-prime/).** A prime $2^q - 1$. The divisibility rule above removes the exponents $q \equiv 3 \pmod 4$ that are Sophie Germain primes greater than 3.

## References
