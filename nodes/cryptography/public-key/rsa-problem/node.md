---
tag: 07Z52Q
kind: problem
slug: rsa-problem
name: RSA problem
aliases:
- RSA assumption
area: cryptography/public-key
level: intro
summary: Given N, e and c, find m with m^e = c mod N. Factoring N solves it. Whether the two problems are equally hard is open.
prereqs: [rsa-cryptosystem, modular-exponentiation, integer-factorization]
see_also: [rsa-cryptosystem, computational-hardness-assumption, integer-factorization, trapdoor-one-way-function, rsa-blinding]
sources:
  - url: "https://doi.org/10.1145/359340.359342"
    title: Ronald L. Rivest, Adi Shamir and Leonard Adleman, A method for obtaining digital signatures and public-key cryptosystems, Communications of the ACM 21(2), pages 120 to 126, 1978
    locator: Section 7 (the difficulty of computing the private exponent and of factoring)
  - url: "https://www.ams.org/notices/199902/boneh.pdf"
    title: Dan Boneh, Twenty years of attacks on the RSA cryptosystem, Notices of the AMS 46(2), pages 203 to 213, 1999
    locator: Section 1 and Fact 1 (the exponent pair gives the factorization, with the probabilistic algorithm)
  - paper: "Dan Boneh and Ramarathnam Venkatesan, Breaking RSA may not be equivalent to factoring, EUROCRYPT 1998, LNCS 1403, pages 59 to 71"
    locator: the result on algebraic reductions, for a public exponent e with e = O(log N) and a straight line program reduction
  - paper: "Divesh Aggarwal and Ueli Maurer, Breaking RSA generically is equivalent to factoring, EUROCRYPT 2009, LNCS 5479, pages 36 to 53"
    locator: the main theorem, for generic ring algorithms over Z_N
  - paper: "Gary L. Miller, Riemann's hypothesis and tests for primality, Journal of Computer and System Sciences 13(3), pages 300 to 317, 1976"
    locator: the probabilistic step that turns a multiple of lambda(N) into a factorization of N
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 3, Section 3.3 (the RSA problem and its relation to factoring) and Note 8.9
---

The RSA problem is: given a modulus $N = pq$, a public exponent $e$ with $\gcd(e, \lambda(N)) = 1$, and a value $c$, find the unique $m$ with $0 \le m < N$ and $m^e \equiv c \pmod N$. It is the problem that an attacker on textbook [RSA](/rsa-cryptosystem/) must solve. Knowledge of the factors of $N$ solves it at once. Whether the RSA problem is as hard as [integer factorization](/integer-factorization/) is open, and there is evidence on both sides.

**Notation.** $N = pq$ with distinct odd primes $p$ and $q$, $\varphi(N) = (p-1)(q-1)$, $\lambda(N) = \mathrm{lcm}(p-1, q-1)$, $e$ the public exponent, $d$ the private exponent, $\lambda$ the security parameter, $\mathcal{A}$ an adversary and $t$ its running time.

## In plain words

Somebody gives you a big number that is the product of two secret primes, a small public power, and a scrambled value. Your job is to find the number that gives the scrambled value when you raise it to that power and keep the remainder.

If you know the two primes, the job is easy: the primes give you a second power that undoes the first. So breaking the product into its primes is one way to win. Nobody knows whether it is the only way. Forty years of work found no better way, and two theory results say that whole families of methods cannot do better, but no proof covers all methods.

## Definition

**The RSA problem.** The input is $(N, e, c)$, where $N$ is the product of two distinct primes of about the same size, $\gcd(e, \lambda(N)) = 1$ and $c \in \mathbb{Z}_N$. The output is the $m \in \mathbb{Z}_N$ with $m^e \equiv c \pmod N$. The solution is unique, because $x \mapsto x^e$ is a bijection on $\mathbb{Z}_N$ when $\gcd(e, \lambda(N)) = 1$.

**The RSA assumption.** For a key generator $\mathrm{Gen}(\lambda)$ that outputs $(N, e)$ with $N$ of $\lambda$ binary digits, and for every probabilistic polynomial time $\mathcal{A}$,

$$\mathrm{Adv}^{\mathrm{RSA}}(\mathcal{A}) = \Pr\left[\mathcal{A}(N, e, c) = c^{d} \bmod N \;\middle|\; (N, e) \leftarrow \mathrm{Gen}(\lambda),\, c \leftarrow \mathbb{Z}_N \right]$$

is negligible in $\lambda$. The value $c$ is uniform, so this is an average case assumption. It is a [computational hardness assumption](/computational-hardness-assumption/) of the standard kind: it is falsifiable, and it is the assumption under which [RSA-OAEP](/rsa-oaep/) is proved IND-CCA2 in the random oracle model.

## Variants

- **The strong RSA assumption.** Given $N$ and $c$, it is hard to find any pair $(m, e)$ with $e > 1$ odd and $m^e \equiv c \pmod N$. Here the adversary chooses the exponent, so the assumption is stronger than the RSA assumption. The signature schemes of Cramer and Shoup and of Gennaro, Halevi and Rabin need it.
- **The RSA inversion problem with a known part of $m$.** When part of $m$ is known or has a fixed form, the [Coppersmith method](/coppersmith-method/) solves the problem in polynomial time if the unknown part is below $N^{1/e}$.
- **The $\phi$-hiding and the $\varphi(N)$ problems.** Computing $\varphi(N)$ or $\lambda(N)$ is as hard as factoring: from $\varphi(N)$ and $N$ you get $p + q$ and $pq$, so $p$ and $q$ are the roots of a quadratic.
- **The decision form.** Given $(N, e, c, m)$, decide whether $m^e \equiv c$. This is easy: compute $m^e \bmod N$. So RSA has no decisional gap of the kind that separates [CDH](/computational-diffie-hellman/) from [DDH](/decisional-diffie-hellman/).

## Examples

With $N = 6012707 = 2357 \cdot 2551$ and $e = 3674911$, the instance $c = 3650502$ has the solution $m = 5234673$. The factors give $d = 422191$, and $3650502^{422191} \bmod 6012707 = 5234673$.

A small instance with a cube: for $e = 3$ and a modulus above $m^3$, the problem is not hard at all. If $c = m^3$ as an integer, an exact integer cube root gives $m$ with no modular work. This is why no scheme sends a short message with no padding.

## Known algorithms

| method | cost | note |
|---|---|---|
| factor $N$, then invert $e$ | the cost of factoring, $\exp(O((\log N)^{1/3} (\log \log N)^{2/3}))$ with the [general number field sieve](/general-number-field-sieve/) | the only general method known |
| exhaustive search over $m$ | $O(N)$ exponentiations | useless, except for a message space that is small or guessable |
| [Coppersmith method](/coppersmith-method/) | polynomial time | only when the unknown part of $m$ is below $N^{1/e}$ |
| [Shor's algorithm](/shor-algorithm/) | polynomial time on a quantum computer | factors $N$, so it solves the problem; Shor 1994 |

No algorithm is known that solves the RSA problem faster than factoring $N$. The record factorization is RSA-250 (829 binary digits, February 2020), with about 2700 core years of computation.

## Bounds

The best known upper bound on the work is the cost of factoring, which is subexponential in $\log N$ with the general number field sieve. No lower bound is known in any standard model. In the restricted models of the two results below, the lower bound is the cost of factoring.

## Reductions

**Factoring implies RSA.** Given $p$ and $q$, compute $\lambda(N) = \mathrm{lcm}(p-1, q-1)$, then $d = e^{-1} \bmod \lambda(N)$ with the [extended Euclidean algorithm](/extended-euclidean-algorithm/), then $m = c^d \bmod N$. The extra cost over one exponentiation is negligible.

**The exponent pair implies factoring.** The algorithm below gets $p$ and $q$ from $(N, e, d)$.

```pseudo id=main
FACTOR-FROM-EXPONENTS(N, e, d, rounds)   ▷ e·d ≡ 1 mod λ(N); write e·d − 1 = 2^s·t with t odd
L1  for round ← 1 to rounds do
L2      a ← a uniform value in {2, ..., N − 2}
L3      if gcd(a, N) > 1 then return gcd(a, N) and N / gcd(a, N)
L4      x ← a^t mod N
L5      for i ← 1 to s do
L6          y ← x² mod N
L7          if y = 1 then
L8              if x ≠ 1 and x ≠ N − 1 then
L9                  f ← gcd(x − 1, N)
L10                 if 1 < f < N then return f and N / f
                break out of the inner loop
L11         x ← y
L12 return "failed"
```

If you know $(N, e, d)$ with $ed \equiv 1 \pmod{\lambda(N)}$, then $k = ed - 1$ is a multiple of $\lambda(N)$, so $a^{k} \equiv 1 \pmod N$ for every $a$ that is coprime to $N$. Write $k = 2^s t$ with $t$ odd. For a random $a$, walk the chain $a^{t}, a^{2t}, \ldots, a^{2^s t}$ modulo $N$. The chain ends at 1. The step before the first 1 is a square root of 1. There are four square roots of 1 modulo $N = pq$, and two of them are $1$ and $N-1$. If the walk finds one of the other two, call it $x$, then $p \mid x-1$ and $q \nmid x-1$ or the other way round, so $\gcd(x-1, N)$ is $p$ or $q$. A random $a$ gives a useful $x$ with probability at least $1/2$, so $64$ bases fail with probability at most $2^{-64}$. The idea is Miller's (1976), and Fact 1 of Boneh's survey states it for RSA. The code of this page runs it on a toy key of 256 binary digits. So the private exponent is not easier to find than the factorization, which answers the question "can I keep $N$ and leak $d$": no.

**Random self reducibility.** Let $r$ be uniform among the invertible residues modulo $N$ and set $c' = c \cdot r^e \bmod N$. Then $c'$ is uniform among the invertible residues, whatever $c$ is, and the solution $m'$ of the instance $(N, e, c')$ gives $m = m' r^{-1} \bmod N$. So an algorithm that solves a $1/\mathrm{poly}$ fraction of the instances solves every instance with high probability after a few tries. There is no class of weak ciphertexts. The same trick is [RSA blinding](/rsa-blinding/), used there as a defence.

**Is RSA as hard as factoring?** Open. Two results mark the border.

- Boneh and Venkatesan (Eurocrypt 1998) show that for a small public exponent, with $e = O(\log N)$, an algebraic reduction, written as a straight line program, that factors $N$ with the help of an oracle for the $e$-th root can be turned into a factoring algorithm that does not use the oracle. So such a reduction would show that factoring is easy. The conclusion is that breaking low exponent RSA is probably not equivalent to factoring, or at least not by an algebraic reduction.
- Aggarwal and Maurer (Eurocrypt 2009) show the other side: an algorithm that computes $e$-th roots and is generic, meaning that it uses only the ring operations and equality tests on $\mathbb{Z}_N$ and does not look at the bit representation, must be able to factor $N$. So in that model the two problems are equivalent.

**The code of this page is for study only.** It is not constant time, and it runs only on toy keys made in the test file. Do not use it to protect real data.

## Applications

The RSA assumption is the base of [RSA-OAEP](/rsa-oaep/) encryption and of the [RSA signature](/rsa-signature/) family ([PSS](/rsa-pss/) and [full domain hash](/rsa-fdh/)). The strong RSA assumption is the base of the Cramer-Shoup signature scheme of 1999 and of some cryptographic accumulators. Because the problem is random self reducible, the proofs can use a single average case assumption with no loss. It is also the standard example of a [trapdoor one-way function](/trapdoor-one-way-function/) candidate, where the trapdoor is the factorization.

## References
