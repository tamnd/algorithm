---
tag: 01DETK
kind: algorithm
slug: blum-micali
name: Blum-Micali generator
aliases:
- Blum-Micali pseudorandom generator
- discrete logarithm generator
area: numerical/random-number-generation
level: advanced
summary: Iterates x ↦ g^x mod p for a prime p and primitive root g and outputs whether each x lies in the lower half of [1, p - 1]; predicting the output is as hard as discrete logarithms.
model: word-ram
complexity:
  vars: {k: the number of output values, L: the length of p in machine words}
  time: {worst: Θ(k L^3)}
  space: {extra: Θ(L)}
properties: {deterministic: true, recursive: false, cryptographic: true}
history:
  year: 1984
  people: [Manuel Blum, Silvio Micali]
  note: Blum and Micali defined cryptographically strong generators, introduced hard-core predicates, and built the first such generator from the hardness of the discrete logarithm (conference version 1982, journal version 1984).
prereqs: [discrete-logarithm-problem, primitive-root, hard-core-predicate, cryptographically-secure-prng]
see_also: [blum-blum-shub, yao-next-bit-unpredictability, one-way-function, pseudorandom-generator, dual-ec-drbg, modular-exponentiation, safe-prime, modular-square-root]
sources:
  - paper: "Manuel Blum and Silvio Micali, How to generate cryptographically strong sequences of pseudo-random bits, SIAM Journal on Computing 13(4), 1984, 850-864"
    locator: the definition of cryptographically strong generators, the predicate B on discrete logarithms, the proof that predicting B with any noticeable advantage solves the discrete logarithm problem, and the generator built by iterating modular exponentiation
  - book: isbn:9780521791724
    title: Oded Goldreich, Foundations of Cryptography, Volume 1, Basic Tools, Cambridge University Press, 2001
    locator: Section 2.5 (hard-core predicates) and Section 3.4 (pseudorandom generators from one-way permutations and hard-core predicates)
  - paper: "Andrew C. Yao, Theory and applications of trapdoor functions, 23rd IEEE Symposium on Foundations of Computer Science, 1982, 80-91"
    locator: the equivalence of unpredictability and indistinguishability used to turn the Blum-Micali construction into a pseudorandom generator
  - paper: "Rosario Gennaro, An improved pseudo-random generator based on the discrete logarithm problem, Journal of Cryptology 18(2), 2005, 91-110"
    locator: the generator that outputs many bits per exponentiation under a short-exponent discrete logarithm assumption
---

The Blum-Micali generator was the first pseudorandom generator with a security proof from a standard hardness assumption. It works in the multiplicative group modulo a large prime $p$ with a primitive root $g$. The state is a number $x \in \{1, \ldots, p-1\}$, and each step outputs one bit, whether $x$ lies in the lower half $\{1, \ldots, (p-1)/2\}$, and replaces $x$ by $g^x \bmod p$. Blum and Micali proved that predicting this bit with any noticeable advantage gives an algorithm for [discrete logarithms](/discrete-logarithm-problem/) modulo $p$. Their construction, a one-way permutation iterated with a [hard-core predicate](/hard-core-predicate/) as output, is the template behind every provable [CSPRNG](/cryptographically-secure-prng/).

## In plain words

Fix a large prime and a number $g$ whose powers run through every nonzero remainder. Start from a secret number $x$. At each step, write down 1 if $x$ is in the lower half of the possible values and 0 if it is in the upper half, then replace $x$ by $g$ raised to the power $x$, modulo the prime.

Raising to a power is easy; undoing it (finding the exponent from the result) is the discrete logarithm problem, believed hard for large primes. Each output bit is a fact about the exponent hidden in the next state. The proof shows that even a slightly better than even guess at that fact could be turned into a way of computing whole discrete logarithms.

## The problem

Given a seed of about $\log_2 p$ uniformly random bits, produce a longer bit string that no polynomial-time algorithm distinguishes from uniform, assuming that discrete logarithms modulo $p$ are hard to compute. In the notation of generators, the state space is $S = \{1, \ldots, p-1\}$, the transition is $f(x) = g^x \bmod p$, and the output is the predicate
$$B(x) = \begin{cases} 1 & \text{if } 1 \le x \le (p-1)/2, \\ 0 & \text{if } (p-1)/2 < x \le p - 1. \end{cases}$$

Because $g$ is a [primitive root](/primitive-root/), $f$ is a permutation of $S$, and computing $f^{-1}(y)$ is the discrete logarithm of $y$ (with $p - 1$ standing for the exponent 0). The two square roots of $g^{2x}$ are $g^x$ and $g^{x + (p-1)/2} = -g^x$, and $B$ tells them apart, which is why $B$ is called the principal square root predicate. Conventions differ in where the boundary element goes; any version that splits the exponents into the two halves works.

## The algorithm

```pseudo id=main
BLUM-MICALI(p, g, x_0, k)          ▷ p prime, g a primitive root mod p, seed x_0 ∈ {1, …, p − 1}
L1  x ← x_0
L2  for i ← 0 to k − 1
L3      b_i ← 1 if x ≤ (p − 1)/2 else 0    ▷ B(x_i)
L4      x ← g^x mod p                    ▷ x_(i+1) = f(x_i)
L5  return b_0 b_1 … b_(k−1)
```

Line L4 is a [modular exponentiation](/modular-exponentiation/) by square-and-multiply with an exponent as long as $p$. The parameters $p$ and $g$ are public; the seed and the current state are secret.

## Example

Take $p = 23$ and $g = 5$, a primitive root modulo 23, and the seed $x_0 = 10$. The lower half is $\{1, \ldots, 11\}$.

| $i$ | $x_i$ | $b_i = B(x_i)$ | $x_{i+1} = 5^{x_i} \bmod 23$ |
|---|---|---|---|
| 0 | 10 | 1 | 9 |
| 1 | 9 | 1 | 11 |
| 2 | 11 | 1 | 22 |
| 3 | 22 | 0 | 1 |
| 4 | 1 | 1 | 5 |
| 5 | 5 | 1 | 20 |
| 6 | 20 | 0 | 12 |
| 7 | 12 | 0 | 18 |

The permutation $x \mapsto 5^x \bmod 23$ of $\{1, \ldots, 22\}$ has cycles of lengths 1, 1, 3, 4 and 13; the seed 10 lies on the 13-cycle. Unlike for [Blum Blum Shub](/blum-blum-shub/), there is no formula for these cycle lengths, and for cryptographic sizes of $p$ short cycles are reached with negligible probability.

**The reduction in action.** Suppose an oracle returns $B(\log_5 z)$ for any $z$. To find $\log_5 21$ modulo 23: 21 is a non-residue, so the exponent is odd (digit 1), and $21 \cdot 5^{-1} = 18 = 5^{12}$. The square roots of 18 are 8 and 15; the oracle says $B(\log 8) = 1$, so $8 = 5^6$ halves the exponent. 8 is a residue (digit 0); its roots are 10 and 13, and the oracle picks $10 = 5^3$. 10 is a non-residue (digit 1), $10 \cdot 5^{-1} = 2$, whose roots are 5 and 18; the oracle picks 5. 5 is a non-residue (digit 1), and $5 \cdot 5^{-1} = 1$ ends the loop. The digits $1, 0, 1, 1$ give $\log_5 21 = 1 + 4 + 8 = 13$. The tests run this reduction for every $y$ modulo 23, 1019, 1033 and 7681.

## Correctness

**What it computes.** By induction, before iteration $i$ the variable $x$ holds $x_i = f^i(x_0)$, so the output is $B(x_0), B(x_1), \ldots, B(x_{k-1})$. Since $f$ is a permutation of a finite set, the state sequence is purely periodic.

**Why the bits are unpredictable (Blum and Micali 1984).** The bit $b_i = B(x_i)$ is a function of $x_i = \log_g x_{i+1}$, and all later bits are functions of $x_{i+1}$. Blum and Micali proved that if some polynomial-time algorithm computes $B(\log_g y)$ from $y$ correctly for a fraction $\tfrac12 + \varepsilon$ of the $y$, with $\varepsilon$ at least an inverse polynomial in $\log p$, then discrete logarithms modulo $p$ can be computed in polynomial time with high probability. With a perfect predictor the reduction is the procedure in the example: the Legendre symbol of $y$ gives the parity of the exponent, and $B$ selects the square root that halves it. Their contribution was making this work for a predictor that is right only slightly more often than not, by randomizing the queries ($y g^r$ for random $r$) and taking majority votes. So no efficient algorithm predicts $b_i$ from $b_{i+1}, b_{i+2}, \ldots$, and by [Yao's theorem](/yao-next-bit-unpredictability/) the output is indistinguishable from uniform, assuming discrete logarithms in $\mathbb{Z}_p^*$ are hard. The proof page proves the permutation property, the output, and the perfect-oracle reduction.

## Complexity

Each step is one exponentiation with an exponent of $\ell = \lceil \log_2 p \rceil$ bits: about $\ell$ squarings and $\ell/2$ multiplications of $L$-word numbers, so $\Theta(L^3)$ word operations with schoolbook arithmetic ($\ell = \Theta(w L)$ and each multiplication with reduction costs $\Theta(L^2)$). For $k$ outputs that is $\Theta(k L^3)$, with $\Theta(L)$ words of state. This is a factor of about $\ell$ slower than [Blum Blum Shub](/blum-blum-shub/), which uses one squaring per step, and many orders of magnitude slower than a block cipher or hash-based generator.

## Properties

- **Proved security from the discrete logarithm**, asymptotically; as for BBS, the reduction loses a polynomial factor, so concrete guarantees need large $p$.
- **Backtracking resistance.** Capturing the state $x_{i+1}$ reveals all later outputs but not $b_i$ or earlier ones, since those need $\log_g x_{i+1}$.
- **Exactly balanced predicate.** $B$ is 1 on exactly $(p-1)/2$ of the $p-1$ states.
- **No trapdoor.** Unlike BBS, nobody can run the generator backwards; there is no secret factorization.
- **Generic structure.** Only two facts are used: $f$ is a one-way permutation, and $B$ is hard-core for it. Any such pair gives a generator by the same loop.

## Variants and improvements

- **More bits per step.** Long and Wigderson and Peralta showed that $O(\log \log p)$ bits of the discrete logarithm are simultaneously hard-core, so as many bits of $x_i$ can be output per exponentiation. Under the stronger assumption that discrete logarithms with short exponents are hard, Gennaro (2005) outputs almost all bits of each state and uses short exponents to make each step faster.
- **Elliptic curve and other groups.** The construction works in any group where the discrete logarithm is hard and a suitable permutation and hard-core predicate exist; Kaliski gave an elliptic curve version.
- **General one-way permutations.** Goldreich and Levin showed that every one-way permutation $f$ has the hard-core predicate $\langle x, r \rangle \bmod 2$ for a random public $r$, so the loop $x \leftarrow f(x)$ with that output yields a generator from any one-way permutation; Håstad, Impagliazzo, Levin and Luby extended this to any [one-way function](/one-way-function/).
- **Dual_EC_DRBG.** The NIST [Dual_EC_DRBG](/dual-ec-drbg/) has the same shape, a state update by scalar multiplication on an elliptic curve and an output derived from a second point, but it outputs nearly all bits of a point coordinate and has no security proof in this sense; its second point admitted a backdoor.

## When to use it

It is a teaching and theory construction: the clean example of how one-wayness plus a hard-core predicate gives pseudorandomness. Practical systems use block-cipher, hash or stream-cipher generators such as [CTR_DRBG](/ctr-drbg/), [HMAC_DRBG](/hmac-drbg/) or [ChaCha20](/chacha20/), which are far faster and whose security rests on cryptanalysis of the primitives.

## Pitfalls

- **Outputting the state.** The state $x_{i+1}$ determines every later output; outputting more of it than the hard-core bits breaks the proof and, in the extreme, reveals the future.
- **Not a primitive root.** If $g$ has smaller order $d$, then $f$ takes only $d$ values and is not a permutation of $S$; states collapse onto a smaller set. Check $g^{(p-1)/r} \ne 1$ for each prime $r \mid p - 1$, which needs the factorization of $p - 1$; a [safe prime](/safe-prime/) $p = 2q + 1$ makes this easy.
- **Weak primes.** If $p - 1$ has only small prime factors, Pohlig-Hellman computes discrete logarithms quickly and the proof gives nothing. Use primes with a large prime factor of $p - 1$ and a size that resists index calculus, at least 2048 bits today.
- **Seed entropy.** A seed with fewer than about 128 bits of min-entropy can be found by exhaustive search, whatever the size of $p$.
- **Timing leaks.** Modular exponentiation with the secret state as exponent must run in constant time, otherwise the state leaks through timing.

## Implementations

## History

Blum and Micali presented the generator at FOCS 1982 and published it in the SIAM Journal on Computing in 1984. The paper introduced the notion of a hard-core predicate and the iterate-and-output-a-bit construction, and proved its security by a reduction from the discrete logarithm. At the same 1982 conference, Yao showed that unpredictability is equivalent to passing every polynomial-time statistical test, which turned the Blum-Micali notion into the modern definition of a pseudorandom generator. Blum, Blum and Shub (1986) gave the faster squaring-based instance, and Goldreich and Levin (1989) and Håstad, Impagliazzo, Levin and Luby (1999) generalized the construction to arbitrary one-way permutations and functions.

## References
