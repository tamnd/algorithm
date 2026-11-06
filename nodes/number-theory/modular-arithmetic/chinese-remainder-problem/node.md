---
tag: MYVHJH
kind: problem
slug: chinese-remainder-problem
name: Chinese remainder problem
aliases:
- solving systems of linear congruences with coprime moduli
area: number-theory/modular-arithmetic
level: core
summary: Given x ≡ a_i (mod n_i) for pairwise coprime n_i, find x mod the product of the n_i.
prereqs: [chinese-remainder-theorem, modular-inverse]
see_also: [garner-algorithm, linear-congruence, residue-number-system, subproduct-tree, fast-interpolation, chinese-remainder-theorem-fft, multimodular-determinant, extended-euclidean-algorithm]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.5, The Chinese remainder theorem (the computation of a from its residues with the coefficients m_i, and its cost)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.3.2, Modular arithmetic (conversion from residues to the mixed-radix form, with precomputed constants c_ij)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 2.4.3, Algorithm 2.121 (Gauss's algorithm) and Example 2.122; Section 14.5.2, Algorithm 14.71 (Garner's algorithm) and Note 14.74
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 5.4, The Chinese Remainder Algorithm (the algorithm for integers and polynomials and its quadratic cost), and Section 10.3, Fast Chinese remaindering (the subproduct tree method)
---

The **Chinese remainder problem** asks for an integer $x$ from its remainders: given residues $a_1, \ldots, a_k$ and pairwise [coprime](/coprime-integers/) moduli $n_1, \ldots, n_k$, find the unique $x$ with $0 \le x < N = n_1 \cdots n_k$ and $x \equiv a_i \pmod{n_i}$ for each $i$. The [Chinese remainder theorem](/chinese-remainder-theorem/) says that this $x$ exists and is unique; the problem is to compute it fast. It is the reconstruction step of every computation by residues: [RSA](/rsa-cryptosystem/) decryption by halves, the [residue number system](/residue-number-system/), multimodular methods such as the [multimodular determinant](/multimodular-determinant/), and large convolutions with several [NTT primes](/chinese-remainder-theorem-fft/). The classical solutions take quadratic time in the size of $N$: Gauss's formula, incremental merging and [Garner's algorithm](/garner-algorithm/). A [subproduct tree](/subproduct-tree/) brings the cost down to $O(M(n) \log n)$ bit operations.

## In plain words

Suppose you know what an unknown number leaves when you divide it by three, by five and by seven. The task is to find the number itself, between zero and one hundred and four.

One way is to try the numbers in order until all three remainders fit. That works for small cases, but the range grows as the product of the divisors, so it soon becomes far too slow.

The fast way builds the answer one divisor at a time. First find a number that fits the first two remainders. Then correct it by a multiple of their product until it also fits the third, and so on. Each correction needs one division in the style of a remainder calculation.

## Definition

**Input.** An integer $k \ge 1$, moduli $n_1, \ldots, n_k \ge 1$ with $\gcd(n_i, n_j) = 1$ for $i \ne j$, and integers $a_1, \ldots, a_k$.

**Output.** The integer $x$ with $0 \le x < N = \prod_i n_i$ and $x \equiv a_i \pmod{n_i}$ for all $i$.

Residues are represented by their least non-negative representatives. A modulus $n_i = 1$ adds no condition. The input size is measured by $n = \lceil \lg N \rceil$, the number of binary digits of $N$, which is about the total size of the moduli.

**Cost models.** On the [word RAM](/word-ram/) with $N < 2^w$, arithmetic on residues and on $x$ costs $O(1)$. In arbitrary precision, the cost is counted in bit operations, with $M(n)$ the cost of multiplying two $n$-digit integers ([integer multiplication](/integer-multiplication/)).

## Variants

- **General moduli.** Without coprimality, the system is solvable if and only if $a_i \equiv a_j \pmod{\gcd(n_i, n_j)}$ for all $i, j$, and the solution is unique modulo $\operatorname{lcm}(n_1, \ldots, n_k)$. Incremental merging with [linear congruences](/linear-congruence/) handles this case and reports when there is no solution.
- **Many systems with the same moduli.** In a residue number system or a multimodular computation, the moduli are fixed and only the residues change. Then the constants, such as the inverses in Garner's algorithm, are computed once, and each reconstruction costs only the multiplications.
- **Balanced output.** For signed results, the answer is wanted in $(-N/2, N/2]$; subtract $N$ when $x > N/2$.
- **Polynomials.** The same problem over a polynomial ring $F[t]$, with coprime polynomial moduli, includes [polynomial interpolation](/polynomial-interpolation/) as the case of linear moduli $t - u_i$.
- **Rational reconstruction.** When the hidden value is a fraction $p/q$ with small $p$ and $q$, the CRT result modulo $N$ is followed by a step of the [extended Euclidean algorithm](/extended-euclidean-algorithm/) that recovers $p$ and $q$.

## Examples

- **Sunzi's problem.** $x \equiv 2 \pmod 3$, $x \equiv 3 \pmod 5$, $x \equiv 2 \pmod 7$. Merging the first two gives $x \equiv 8 \pmod{15}$; merging with the third gives $x = 23$, the unique solution in $0$ to $104$.
- **Gauss's formula.** For $x \equiv 3 \pmod 7$ and $x \equiv 7 \pmod{13}$, $N = 91$, $13^{-1} \equiv 6 \pmod 7$ and $7^{-1} \equiv 2 \pmod{13}$, so $x = 3 \cdot 13 \cdot 6 + 7 \cdot 7 \cdot 2 = 332 \equiv 59 \pmod{91}$ (HAC, Example 2.122).
- **Residues of a number.** The residues of $500$ modulo $7$, $11$ and $13$ are $3$, $5$ and $6$. The problem with these inputs returns $500$, since $500 < 1001$.
- **General moduli, solvable.** $x \equiv 1 \pmod 4$ and $x \equiv 3 \pmod 6$: the condition $1 \equiv 3 \pmod 2$ holds, and the solution is $x \equiv 9 \pmod{12}$.
- **General moduli, unsolvable.** $x \equiv 1 \pmod 4$ and $x \equiv 2 \pmod 6$: $1 \not\equiv 2 \pmod 2$, so no $x$ exists.

## Known algorithms

| algorithm | idea | bit operations | word RAM, $N < 2^w$ |
|---|---|---|---|
| exhaustive search | try $x = 0, 1, \ldots, N - 1$ | $O(N \cdot n)$ | $O(N k)$ |
| step search | try $x = a_k + j n_k$ for $j < N/n_k$ | $O(N n / n_k)$ | $O(N k / n_k)$ |
| Gauss's formula | $x = \sum_i a_i N_i M_i \bmod N$ with $N_i = N/n_i$ and $M_i = N_i^{-1} \bmod n_i$ | $O(n^2)$ | $O(\log N)$ |
| incremental merging | solve two congruences, replace them by one modulo the product, repeat | $O(n^2)$ | $O(\log N)$ |
| [Garner's algorithm](/garner-algorithm/) | compute the mixed-radix digits of $x$ with precomputed inverses, then evaluate | $O(n^2)$ | $O(k^2)$ with fixed moduli |
| [subproduct tree](/subproduct-tree/) | combine the residues in a balanced binary tree of products | $O(M(n) \log n)$ | not needed |

The bounds for Gauss's formula, merging and Garner's algorithm assume schoolbook arithmetic and moduli with a total of $n$ binary digits. The word RAM bound $O(\log N)$ counts the steps of the extended Euclidean algorithm over all moduli, since the step counts of the inverse computations add up to $O(\sum_i \log n_i) = O(\log N)$. The tree method is the integer analogue of [fast interpolation](/fast-interpolation/) (von zur Gathen and Gerhard, Section 10.3).

## Bounds

**Upper bounds.** The quadratic methods take $O(n^2)$ bit operations (von zur Gathen and Gerhard, Section 5.4). The subproduct tree method takes $O(M(n) \log n)$ bit operations, so $O(n \log^2 n)$ with an $O(n \log n)$ multiplication.

**Lower bounds.** Every algorithm must read the residues and write $x$, so $\Omega(n)$ bit operations are needed. No better lower bound is known in general, so the gap between $\Omega(n)$ and $O(M(n) \log n)$ is open, as for the inverse task of computing all residues of one number, which has the same upper bound.

**Search is exponential.** Exhaustive search takes time proportional to $N$, which is exponential in the input size $n$. For moduli of a few binary digits each and small $k$ it can still be the simplest choice.

## Reductions

- **To modular inverses.** Gauss's formula needs the $k$ inverses $N_i^{-1} \bmod n_i$, and merging and Garner's algorithm need $k - 1$ inverses. These are [modular inverses](/modular-inverse/), computed by the extended Euclidean algorithm, or many at once by [batch modular inversion](/batch-modular-inverse/).
- **To linear congruences.** Merging $x \equiv a_1 \pmod{n_1}$ with $x \equiv a_2 \pmod{n_2}$ is the [linear congruence](/linear-congruence/) $n_1 t \equiv a_2 - a_1 \pmod{n_2}$ in $t$.
- **Inverse problem.** Going from $x$ to its residues is $k$ divisions, or a remainder tree with the same subproduct tree. In a residue number system, the two directions are the conversions at the input and the output.
- **From polynomial interpolation.** Interpolation of a polynomial from its values at distinct points is the Chinese remainder problem in $F[t]$ with the moduli $t - u_i$; the integer and polynomial versions share their algorithms.

## Applications

- **RSA with the CRT.** Decryption modulo $p$ and $q$ separately and one recombination; see [Chinese remainder theorem](/chinese-remainder-theorem/).
- **Multimodular algorithms.** Determinants, resultants, polynomial gcds and exact linear algebra are computed modulo many word-sized primes, then reconstructed. See [modular methods](/modular-methods/).
- **Large convolutions.** Products of polynomials with large coefficients are computed with the number theoretic transform modulo two or three primes, then combined by CRT ([CRT with FFT](/chinese-remainder-theorem-fft/)).
- **Pohlig-Hellman.** The [Pohlig-Hellman](/pohlig-hellman/) algorithm finds a discrete logarithm modulo each prime power that divides the group order and combines the results by CRT.
- **Secret sharing.** Threshold schemes based on CRT give each participant a residue of the secret; see [secret sharing](/secret-sharing/).

## References
