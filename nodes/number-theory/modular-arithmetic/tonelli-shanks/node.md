---
tag: 5CEZWX
kind: algorithm
slug: tonelli-shanks
name: Tonelli-Shanks algorithm
aliases:
- Shanks-Tonelli algorithm
area: number-theory/modular-arithmetic
level: advanced
summary: Computes a square root of a quadratic residue a modulo an odd prime p by correcting the guess a^((q+1)/2) with powers of a nonresidue, where p − 1 = q·2^s.
solves: [modular-square-root]
model: word-ram
complexity:
  vars: {p: the odd prime modulus, s: the exponent of 2 in p − 1, N: the least quadratic nonresidue modulo p, k: the number of binary digits of p}
  time: {worst: O(N log p + s^2), best: Θ(log p)}
  space: {extra: Θ(1)}
  bit_operations: {worst: O((N k + s^2) k^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 1891
  people: [Alberto Tonelli, Daniel Shanks]
  note: Tonelli published the method in 1891; Shanks rediscovered it and gave the form used today, called RESSOL, in 1973.
prereqs: [modular-square-root, euler-criterion, multiplicative-order]
see_also: [cipolla-algorithm, quadratic-residue, legendre-symbol, modular-exponentiation, pohlig-hellman, hensel-lifting, rabin-cryptosystem]
sources:
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Springer GTM 138
    locator: Section 1.5.1, The Algorithm of Tonelli and Shanks (Algorithm 1.5.1 and its analysis)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1997
    locator: Section 3.5.1, Algorithm 3.34 (finding square roots modulo a prime p) with Fact 3.35, and Algorithms 3.36 and 3.37 for p ≡ 3 (mod 4) and p ≡ 5 (mod 8)
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition
    locator: Section 2.3.2, Square roots
  - paper: "Alberto Tonelli, Bemerkung über die Auflösung quadratischer Congruenzen, Nachrichten von der Königlichen Gesellschaft der Wissenschaften und der Georg-Augusts-Universität zu Göttingen, 1891"
    locator: pages 344 to 346
  - paper: "Daniel Shanks, Five number-theoretic algorithms, Proceedings of the Second Manitoba Conference on Numerical Mathematics, 1972, Congressus Numerantium VII, 1973"
    locator: pages 51 to 70 (the algorithm RESSOL)
---

The Tonelli-Shanks algorithm computes a [modular square root](/modular-square-root/): given an odd prime $p$ and a [quadratic residue](/quadratic-residue/) $a$, it finds $x$ with $x^2 \equiv a \pmod p$. Write $p - 1 = q \cdot 2^s$ with $q$ odd. The first guess $x = a^{(q+1)/2}$ satisfies $x^2 = a \cdot a^q$, and the error $t = a^q$ lies in the subgroup of order $2^s$; the algorithm removes it step by step with powers of $z^q$, where $z$ is a quadratic nonresidue. It uses $O(\log p + s^2)$ multiplications modulo $p$ plus the search for $z$, which takes two trials on average with random candidates. Tonelli published the method in 1891, and Shanks gave its modern form in 1973.

## In plain words

You want a number whose square, on a prime clock, lands on a given position. A first guess is easy to compute, but its square is off by an error factor. This error factor belongs to a small family of positions that cycle with a length that is a power of two. To cancel the error, you need one helper number that is not a square, and from it you build a matching family of correction factors. In each round, you measure how far the error is from 1, pick the correction of the right size, and fold it into both the guess and the error. The error comes closer to 1 in each round, and when it equals 1 the guess is the answer.

## The problem

The input is an odd prime $p$ and an integer $a$. The output is an $x \in \{0, \ldots, p - 1\}$ with $x^2 \equiv a \pmod p$, or "none" when $a$ is a quadratic nonresidue. If $x$ is a root, so is $p - x$, and there are no others when $a \not\equiv 0$.

**Cost model.** On the [word RAM](/word-ram/) with $p < 2^w$, a multiplication modulo $p$ costs $O(1)$ (with a double-width product), and the bounds count such operations. For $p$ of $k$ binary digits with arbitrary precision, each multiplication modulo $p$ costs $O(k^2)$ bit operations with schoolbook arithmetic. Residues are integers in $[0, p)$. The algorithm does not check that $p$ is prime; for composite $p$ its output has no meaning.

## The algorithm

```pseudo id=main
TONELLI-SHANKS(a, p)                    ▷ p an odd prime; all arithmetic mod p
L1  a ← a mod p; if a = 0 then return 0
L2  if a^((p−1)/2) ≠ 1 then return NONE          ▷ Euler's criterion
L3  write p − 1 = q · 2^s with q odd
L4  if s = 1 then return a^((p+1)/4)
L5  z ← 2; while z^((p−1)/2) ≠ −1 do z ← z + 1   ▷ least nonresidue
L6  c ← z^q; x ← a^((q+1)/2); t ← a^q; M ← s
L7  while t ≠ 1 do          ▷ x² = a·t, ord(c) = 2^M, ord(t) divides 2^(M−1)
L8      i ← least i ≥ 1 with t^(2^i) = 1         ▷ by repeated squaring
L9      b ← c^(2^(M−i−1))                        ▷ square c, M − i − 1 times
L10     M ← i; c ← b²; t ← t·c; x ← x·b
L11 return x
```

Line L2 rejects nonresidues with [Euler's criterion](/euler-criterion/). Line L4 is the case $p \equiv 3 \pmod 4$, where $q = (p - 1)/2$ and $x = a^{(p+1)/4}$ is a root directly, since $x^2 = a \cdot a^{(p-1)/2} = a$. Line L5 finds the least quadratic nonresidue $z$; a random search works as well. In line L6, $c = z^q$ has [multiplicative order](/multiplicative-order/) exactly $2^s$, and the error $t = a^q$ has order dividing $2^{s-1}$.

Each pass of the loop finds the exact order $2^i$ of $t$, with $1 \le i < M$, and multiplies $t$ by $b^2$, an element whose $2^{i-1}$-th power is also $-1$. This makes the order of $t$ drop to at most $2^{i-1}$, and multiplying $x$ by $b$ keeps $x^2 = a t$. Since $M$ strictly decreases, the loop runs at most $s - 1$ times.

## Example

Find a square root of $a = 5$ modulo $p = 41$. Euler's criterion: $5^{20} \equiv 1$, so 5 is a residue. $p - 1 = 40 = 5 \cdot 2^3$, so $q = 5$ and $s = 3$. The least nonresidue: $2^{20} \equiv 1$, since $41 \equiv 1 \pmod 8$, and $3^{20} \equiv 40 \equiv -1$, so $z = 3$. Line L6: $c = 3^5 \bmod 41 = 38$, $x = 5^3 \bmod 41 = 2$, $t = 5^5 \bmod 41 = 9$ and $M = 3$.

| pass | squares of $t$ | $i$ | $b$ | $M$ | $c$ | $t$ | $x$ | $x^2$ and $a t$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| start | | | | 3 | 38 | 9 | 2 | 4 and 4 |
| 1 | $9^2 = 81 \equiv 40$, $40^2 \equiv 1$ | 2 | 38 | 2 | 9 | 40 | 35 | 36 and 36 |
| 2 | $40^2 \equiv 1$ | 1 | 9 | 1 | 40 | 1 | 28 | 5 and 5 |

The result is $x = 28$: $28^2 = 784 = 19 \cdot 41 + 5$. The other root is $41 - 28 = 13$.

A shorter run: for $a = 2$ and $p = 113$, with $112 = 7 \cdot 2^4$, the least nonresidue is 3, and one pass gives $x = 62$, with $62^2 = 3844 = 34 \cdot 113 + 2$.

## Correctness

At line L6, $x^2 = a^{q+1} = a t$; $c^{2^{s-1}} = z^{(p-1)/2} = -1$, so $c$ has order exactly $2^s$; and $t^{2^{s-1}} = a^{(p-1)/2} = 1$. Suppose at the start of a pass $x^2 = at$, $c^{2^{M-1}} = -1$ and $t^{2^{M-1}} = 1$, with $t \ne 1$. Then the order of $t$ is $2^i$ with $1 \le i \le M - 1$, so line L8 finds $i$, and $t^{2^{i-1}} = -1$, because in the field $\mathbb{Z}_p$ the only square roots of 1 are $\pm 1$. Then $b^{2^i} = c^{2^{M-1}} = -1$, so the new $c = b^2$ satisfies $c^{2^{i-1}} = -1$, and the new $t$ satisfies $(t b^2)^{2^{i-1}} = (-1)(-1) = 1$. Also $(xb)^2 = a t b^2$. So the three facts hold again with $M = i$. Since $M$ strictly decreases and $M \ge 1$, the loop stops, and then $t = 1$ gives $x^2 = a$. The full proof is below.

## Complexity

Count multiplications modulo $p$.

- Line L2, line L4 or the three powers of line L6: $O(\log p)$ each, by [modular exponentiation](/modular-exponentiation/).
- Line L5: one exponentiation per candidate, so $O(N \log p)$ with $N$ the least nonresidue. With random candidates instead, each trial succeeds with probability $1/2$, so the expected cost is $O(\log p)$.
- The loop: at most $s - 1$ passes. A pass with current $M$ and found $i$ makes $i$ squarings in line L8, $M - i - 1$ in line L9 and 3 in line L10, at most $M + 2$ in total. Summing over the passes, with $M \le s$ decreasing, gives $O(s^2)$.

So the time is $O(N \log p + s^2)$ in the worst case, and $O(\log p + s^2)$ expected with random candidates. Since $s \le \lg p$, this is $O(\log^2 p)$ multiplications in the worst case for the loop. The best case is $s = 1$, that is $p \equiv 3 \pmod 4$, with two exponentiations: $\Theta(\log p)$. The extra space is a constant number of residues. With schoolbook arithmetic on $k$-digit primes, the bit cost is $O((Nk + s^2) k^2)$.

The least nonresidue $N$ is small in practice: it is 2 for all $p \equiv \pm 3 \pmod 8$, and under the generalized Riemann hypothesis it is below $2 (\ln p)^2$ (Bach, 1990). Without that hypothesis, no deterministic polynomial-time method is known to find a nonresidue, so the deterministic form of line L5 has no proven polynomial bound.

## Properties

- **Las Vegas or deterministic.** With random candidates in line L5 it is a Las Vegas algorithm: the output is always right and only the running time is random. With the sequential search shown, it is deterministic, with a running time bounded by $N$.
- **Sensitive to $s$.** The cost grows with the power of 2 in $p - 1$. For primes such as $p = 2^{224} - 2^{96} + 1$, where $s = 96$, the loop dominates.
- **Output.** It returns one of the two roots, not a canonical one. Taking $\min(x, p - x)$ gives a canonical root.
- **Iterative.** No recursion, constant extra space.

## Variants and improvements

- **Special primes.** For $p \equiv 3 \pmod 4$, $x = a^{(p+1)/4}$ (line L4). For $p \equiv 5 \pmod 8$, Atkin's formula uses one exponentiation and no nonresidue: with $v = (2a)^{(p-5)/8}$ and $i = 2av^2$, the root is $x = av(i - 1)$ (HAC, Algorithm 3.37).
- **Cipolla's algorithm.** [Cipolla's algorithm](/cipolla-algorithm/) finds $t$ with $t^2 - a$ a nonresidue and computes $(t + \sqrt{t^2 - a})^{(p+1)/2}$ in $\mathbb{F}_{p^2}$. It costs $O(\log p)$ multiplications regardless of $s$, so it is better when $s$ is large.
- **Precomputation for a fixed prime.** $z$ and $c = z^q$ depend only on $p$, so they can be computed once. Bernstein (2001) and Sutherland (2011) use tables of powers of $c$ to bring the loop below $s^2$ multiplications.
- **Higher roots.** The Adleman-Manders-Miller algorithm (1977) extends the method to $r$-th roots modulo $p$, using the $r$-part of $p - 1$.
- **Discrete logarithm view.** The loop is the [Pohlig-Hellman](/pohlig-hellman/) method in the subgroup of order $2^s$: it computes the binary digits of the discrete logarithm of $t$ to the base $c$ one at a time.
- **Other moduli.** Roots modulo $p^e$ follow by [Hensel lifting](/hensel-lifting/), and roots modulo a product of primes by the [Chinese remainder theorem](/chinese-remainder-theorem/).

## When to use it

Use it to take square roots modulo a prime with a small or moderate $s$, which covers most primes, and always with a precomputed nonresidue when the prime is fixed, as in elliptic curve point decompression. For $p \equiv 3 \pmod 4$ use the single exponentiation, and for $p \equiv 5 \pmod 8$ Atkin's formula. For primes with a large $s$, such as NTT primes and $2^{224} - 2^{96} + 1$, prefer Cipolla's algorithm or a table-based variant. For a composite modulus with unknown factors, no efficient method exists: computing square roots modulo $n = pq$ is as hard as factoring $n$, which is the basis of the [Rabin cryptosystem](/rabin-cryptosystem/).

## Pitfalls

- **Skipping the residue test.** If $a$ is a nonresidue, then $t^{2^{s-1}} = -1$, line L8 gives $i = M$, and line L9 is undefined. Implementations without line L2 return garbage or loop forever.
- **A composite modulus.** For composite $p$, line L5 may never succeed, or line L8 may never reach 1. Check primality, or bound the loops.
- **A fixed guess for the nonresidue.** Using $z = 2$ always is wrong for $p \equiv \pm 1 \pmod 8$, where 2 is a residue.
- **$a \equiv 0$.** Euler's criterion gives 0, not 1, so without line L1 the value 0 is wrongly rejected.
- **$p = 2$.** The method assumes $p$ odd. Modulo 2, every $a$ is its own square root.
- **Overflow.** For $p$ close to $2^{64}$, products need 128 binary digits. Use a double-width product or [Montgomery multiplication](/montgomery-multiplication/).

## Implementations

## History

Alberto Tonelli published the algorithm in 1891 in the *Göttinger Nachrichten*. Daniel Shanks rediscovered it and described it, as RESSOL, among his "Five number-theoretic algorithms" at the Manitoba conference of 1972, published in 1973; his version is the one with the loop on $M$ shown here. Cipolla gave the alternative method in $\mathbb{F}_{p^2}$ in 1903. Adleman, Manders and Miller generalized the approach to higher roots in 1977, and Cohen's textbook (1993) made the Tonelli-Shanks form standard in computational number theory.

## References
