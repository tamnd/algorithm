---
tag: 7AWXWS
kind: algorithm
slug: number-theoretic-transform
name: Number-theoretic transform
aliases:
- NTT
- finite field FFT
- modular FFT
area: algebra/fast-transforms
level: core
summary: FFT over a finite field Z_p with a primitive root of unity, giving exact convolution modulo p.
solves: [discrete-fourier-transform]
model: word-ram
complexity:
  vars: {n: the transform length (a power of two dividing p - 1), p: the prime modulus (p^2 below 2^w for the word size w)}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
  additions: {worst: n lg n}
  multiplications: {worst: (n/2) lg n}
properties: {deterministic: true, recursive: false, in_place: true, exact: true}
history:
  year: 1971
  people: [John M. Pollard]
  note: Pollard (1971) described the FFT in a finite field. Schönhage and Strassen (1971) used transforms over the rings Z/(2^m + 1) for integer multiplication, and Agarwal and Burrus (1975) surveyed number theoretic transforms for digital convolution.
prereqs: [fast-fourier-transform, roots-of-unity, primitive-root, modular-exponentiation, modular-inverse]
see_also: [iterative-fft, inverse-fft, fft-polynomial-multiplication, convolution-via-fft, chinese-remainder-theorem, garner-algorithm, schonhage-strassen-multiplication, montgomery-multiplication]
sources:
  - paper: doi:10.1090/S0025-5718-1971-0301966-0
    title: J. M. Pollard, The fast Fourier transform in a finite field, Mathematics of Computation 25(114), 1971
    locator: pp. 365 to 374 (the transform over a finite field with a root of unity of order n, and its use for exact convolution)
  - paper: doi:10.1007/BF02242355
    title: A. Schönhage and V. Strassen, Schnelle Multiplikation großer Zahlen, Computing 7(3-4), 1971
    locator: pp. 281 to 292 (FFT over Z/(2^m + 1) for integer multiplication)
  - paper: doi:10.1109/PROC.1975.9791
    title: Ramesh C. Agarwal and C. Sidney Burrus, Number theoretic transforms to implement fast digital convolution, Proceedings of the IEEE 63(4), 1975
    locator: pp. 550 to 560 (the conditions on the modulus and the root, the Fermat and Mersenne transforms)
  - paper: doi:10.1109/TASSP.1974.1162555
    title: Ramesh C. Agarwal and C. Sidney Burrus, Fast convolution using Fermat number transforms with applications to digital filtering, IEEE Transactions on Acoustics, Speech, and Signal Processing 22(2), 1974
    locator: pp. 87 to 97 (transforms modulo 2^(2^r) + 1 with powers of two as roots)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 8, Sections 8.2 and 8.3 (the FFT over a ring with a primitive root of unity, and fast convolution); Chapter 5 (the Chinese remainder algorithm)
  - paper: doi:10.1109/TEC.1959.5219515
    title: Harvey L. Garner, The residue number system, IRE Transactions on Electronic Computers EC-8(2), 1959
    locator: pp. 140 to 147 (conversion from residues by the mixed-radix form)
  - paper: doi:10.1016/j.jsc.2013.09.002
    title: David Harvey, Faster arithmetic for number-theoretic transforms, Journal of Symbolic Computation 60, 2014
    locator: pp. 113 to 119 (butterflies with lazy reduction and precomputed quotients)
---

The number-theoretic transform (NTT) is the [discrete Fourier transform](/discrete-fourier-transform/) over the field $\mathbb{Z}/p\mathbb{Z}$ for a prime $p$, computed by the [FFT](/fast-fourier-transform/). It needs a root of unity of order $n$ modulo $p$, which exists exactly when $n \mid p - 1$; for $n$ a power of two one takes a prime $p = c \cdot 2^k + 1$, such as $998244353 = 119 \cdot 2^{23} + 1$, and $\omega = g^{(p-1)/n}$ for a [primitive root](/primitive-root/) $g$. Every operation is exact, so the NTT gives the cyclic convolution modulo $p$ with no rounding at all, and the integer convolution itself whenever its entries are smaller than $p$, or smaller than a product of several such primes by the [Chinese remainder theorem](/chinese-remainder-theorem/). This makes it the standard tool for exact [polynomial multiplication](/fft-polynomial-multiplication/) in computer algebra and programming contests.

## In plain words

The fast Fourier transform needs a number that comes back to $1$ after exactly $n$ steps of multiplying by itself, like a hand going round a clock. In ordinary arithmetic that number is a point on the unit circle, and computers can only store it approximately, so small errors creep in.

Clock arithmetic modulo a prime has such numbers too, if the prime is chosen well. There, every number is a whole number and every result is exact. The NTT runs the same fast transform in this world. To multiply two polynomials with whole-number coefficients, transform both, multiply entry by entry, and transform back. If the true coefficients are smaller than the prime, the answer is exactly right. If they are larger, do the same with two or three primes and combine the answers.

## The problem

**Notation.** As on all pages of fast transforms: $n$ is the transform length, here a power of two; $\omega$ is a principal $n$-th [root of unity](/roots-of-unity/) in the ring, here $\mathbb{Z}/p\mathbb{Z}$; the transform is $X_k = \sum_j x_j \omega^{jk}$, and the inverse has the factor $n^{-1}$. Over $\mathbb{C}$ the corresponding root is $\omega_n = e^{-2\pi i/n}$; the NTT has no sign convention, since every element of order $n$ works.

**Input.** A prime $p$, a primitive root $g$ modulo $p$, and two integer sequences $a$ and $b$ of lengths $\ell_a, \ell_b \ge 1$ with $n \mid p - 1$, where $n$ is the least power of two with $n \ge \ell_a + \ell_b - 1$.

**Output.** The coefficients of $a(t) b(t)$ modulo $p$, that is $c_m = \sum_{i + j = m} a_i b_j \bmod p$ for $0 \le m < \ell_a + \ell_b - 1$.

**Cost model.** The [word RAM](/word-ram/) with words of $w$ bits, $p < 2^{w/2}$, so that a product of two residues fits in one word. An addition modulo $p$ is one addition and one compare-and-subtract; a multiplication modulo $p$ is one word multiplication and one reduction, by division, [Barrett reduction](/barrett-reduction/) or [Montgomery multiplication](/montgomery-multiplication/), each $O(1)$ word operations. We count additions (with subtractions) and multiplications modulo $p$ separately. There is no rounding error: every result is exact.

## The algorithm

```pseudo id=main
NTT-MULTIPLY(a, b, p, g)       ▷ p prime, g a primitive root mod p; returns a·b mod p
L1  m ← |a| + |b| − 1
L2  n ← the least power of two with n ≥ m
L3  if (p − 1) mod n ≠ 0 then error "no root of unity of order n"
L4  ω ← g^((p − 1)/n) mod p                       ▷ order exactly n
L5  A ← a padded with zeros to length n; B ← b padded likewise
L6  NTT(A, ω, p); NTT(B, ω, p)
L7  C[k] ← A[k] · B[k] mod p for k = 0, …, n − 1
L8  NTT(C, ω^(−1) mod p, p)
L9  return (n^(−1) · C[j] mod p for j = 0, …, m − 1)

NTT(x, ω, p)                   ▷ in place; n = |x| a power of two; ω of order n
L10 apply the bit-reversal permutation to x
L11 W[k] ← ω^k mod p for k = 0, …, n/2 − 1         ▷ W[k] = W[k − 1] · ω, exact
L12 h ← 1
L13 while h < n do
L14     for s ← 0 to n − 1 step 2h do
L15         for k ← 0 to h − 1 do
L16             u ← x[s + k], v ← W[k · n/(2h)] · x[s + k + h] mod p
L17             x[s + k] ← (u + v) mod p, x[s + k + h] ← (u − v) mod p
L18     h ← 2h
```

Line L4 is the only place where number theory enters. Since $g$ has order $p - 1$, the power $\omega = g^{(p-1)/n}$ has order exactly $n$, and in a field an element of order $n$ is a principal $n$-th root of unity. Moreover $\omega^{n/2} = g^{(p-1)/2} = -1$, by Euler's criterion, since a primitive root is not a square. Lines L10 to L18 are the radix-2 decimation-in-time [iterative FFT](/iterative-fft/) with every result reduced modulo $p$. In contrast to the complex FFT, the twiddle table of line L11 can be built by repeated multiplication, because there is no rounding to accumulate (see [twiddle factor](/twiddle-factor/)). Line L8 is the [inverse FFT](/inverse-fft/) by the inverse root $\omega^{-1} = \omega^{n-1}$, and line L9 multiplies by $n^{-1}$, which exists because $n < p$. The zero padding of line L5 makes the cyclic convolution of length $n$ equal to the linear one, since $n \ge m$.

**Exact integer results.** If $0 \le a_i < A$ and $0 \le b_j < B$, then $0 \le \sum_{i + j = m} a_i b_j \le \min(\ell_a, \ell_b)(A - 1)(B - 1)$. When this is less than $p$, the residues returned are the integer coefficients. For signed inputs, read the residues in $(-p/2, p/2)$ and require each $|c_m| < p/2$. For larger results, run the algorithm modulo primes $p_1, \ldots, p_r$ and combine by the Chinese remainder theorem, for instance by [Garner's algorithm](/garner-algorithm/); this is exact when every $|c_m| < p_1 \cdots p_r / 2$.

## Example

Multiply $a(t) = 1 + 2t + 3t^2$ by $b(t) = 4 + 5t$. Here $m = 4$, $n = 4$, and the true product is $4 + 13t + 22t^2 + 15t^3$.

Modulo $p = 17$ with $g = 3$: line L4 gives $\omega = 3^4 = 81 \equiv 13$, which has order $4$ since $13^2 = 169 \equiv -1$. Then $\omega^{-1} = 4$ and $n^{-1} = 4^{-1} = 13$.

| step | values modulo 17 |
|---|---|
| $A = \mathrm{NTT}(1, 2, 3, 0)$ | 6 7 2 6 |
| $B = \mathrm{NTT}(4, 5, 0, 0)$ | 9 1 16 7 |
| $C = A \cdot B$ | 3 7 15 8 |
| $\mathrm{NTT}(C, 4)$ | 16 1 3 9 |
| times $13$ | 4 13 5 15 |

The result $(4, 13, 5, 15)$ is the product modulo $17$: the coefficient $22$ became $5$. The bound for exact results does not hold here: with $A = 4$ and $B = 6$ it is $\min(3, 2) \cdot 3 \cdot 5 = 30 > 17$. Modulo $p = 998244353$ with $g = 3$ the same steps return $(4, 13, 22, 15)$, the integer product. For instance, $A_1 = 1 + 2 \cdot 13 + 3 \cdot 13^2 = 534 \equiv 7 \pmod{17}$. All values were checked by script.

## Correctness

The root of line L4 has order $n$, and $\omega^{n/2} = -1$, so $\omega$ is a principal $n$-th root of unity and the radix-2 split applies. By the correctness of the decimation-in-time FFT, NTT$(x, \omega, p)$ returns $\mathrm{DFT}_\omega(x)$ in $\mathbb{Z}/p\mathbb{Z}$. By the [convolution theorem](/convolution-theorem/), $C = \mathrm{DFT}_\omega(A \ast B)$ where $\ast$ is the cyclic convolution of length $n$, and $\mathrm{DFT}_{\omega^{-1}}$ followed by the factor $n^{-1}$ inverts $\mathrm{DFT}_\omega$. Since $A$ and $B$ have zeros beyond positions $\ell_a - 1$ and $\ell_b - 1$ and $n \ge \ell_a + \ell_b - 1$, no product $a_i b_j$ wraps around, so $A \ast B$ is the linear product. The full proof, with the bound for exact integer results and the Chinese remainder step, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

**Ring operations.** One NTT of length $n$ does $n \lg n$ additions and subtractions and $\frac{n}{2} \lg n$ multiplications modulo $p$, plus $\frac{n}{2} - 1$ multiplications for the table. NTT-MULTIPLY does three transforms, $n$ pointwise products and $n$ scalings: $3 n \lg n$ additions and $\frac{3}{2} n \lg n + 2n$ multiplications modulo $p$, plus $O(\log p)$ multiplications for $\omega$, $\omega^{-1}$ and $n^{-1}$ by [fast exponentiation](/modular-exponentiation/). With $n < 2(\ell_a + \ell_b)$ this is $O((\ell_a + \ell_b) \log(\ell_a + \ell_b))$.

**Time and space.** Each operation modulo $p$ is $O(1)$ word operations, so the time is $\Theta(n \log n)$ in every case. The transform runs in place; the twiddle table and the padded copies take $\Theta(n)$ extra space.

**Errors.** None. All arithmetic is exact, so there is no error bound to prove, in contrast to the complex FFT. The only failure is overflow of the true coefficients past $p/2$, which the bound above rules out.

**Limits on the length.** The length must divide $p - 1$: up to $2^{23}$ for $998244353$, $2^{25}$ for $167772161 = 5 \cdot 2^{25} + 1$, and $2^{26}$ for $469762049 = 7 \cdot 2^{26} + 1$. The number $3$ is a primitive root of all three, as one checks by $3^{(p-1)/q} \ne 1$ for the prime factors $q$ of $p - 1$.

## Properties

- **Exact.** Every value is an integer in $[0, p)$.
- **In place.** Each butterfly writes back into the cells it read.
- **Oblivious.** The operations depend only on $n$, as for every radix-2 FFT.
- **Linear over $\mathbb{Z}/p\mathbb{Z}$.** $\mathrm{NTT}(\alpha x + \beta y) = \alpha\,\mathrm{NTT}(x) + \beta\,\mathrm{NTT}(y)$ modulo $p$.
- **No physical meaning.** The outputs are residues, not frequencies; the transform satisfies the same algebraic identities as the DFT (convolution theorem, inversion, [Parseval's theorem](/parseval-theorem/) in the form $\sum_k X_k Y_{-k} = n \sum_j x_j y_j$), but there is no notion of magnitude or phase.

## Variants and improvements

- **Several primes.** With the three primes above, whose product $P$ is about $7.9 \cdot 10^{25}$, a little more than $2^{86}$, a product is exact when every $|c_m| < P/2$. For example, for $\ell_a, \ell_b \le 2^{20}$ and inputs of absolute value below $2^{32}$, the coefficients are below $2^{84}$, so three primes suffice.
- **Lazy reduction.** Keep values in $[0, 2p)$ or $[0, 4p)$ and reduce only when needed, and multiply by fixed twiddle factors with a precomputed quotient; Harvey (2014) analyses such butterflies for $p < 2^{62}$.
- **Montgomery form.** Keep all residues as $x R \bmod p$ and use [Montgomery multiplication](/montgomery-multiplication/) in the butterfly, so no division is needed.
- **Fermat number transforms.** Modulo $F_r = 2^{2^r} + 1$, the number $2$ has order $2^{r+1}$, so the twiddle factors are powers of $2$ and the multiplications become shifts. Agarwal and Burrus (1974) used these transforms for digital filtering; the length is limited to $2^{r+2}$ with the root $\sqrt 2$. [Schönhage-Strassen multiplication](/schonhage-strassen-multiplication/) uses the rings $\mathbb{Z}/(2^m + 1)$ with $m$ growing with the input.
- **Mersenne transforms.** Modulo $2^q - 1$, the number $2$ has order $q$, which is prime for a [Mersenne prime](/mersenne-prime/) exponent; Rader (1972) proposed these transforms, which have prime length and so are not radix-2.
- **Other lengths.** Any length $n \mid p - 1$ works with a [mixed-radix FFT](/mixed-radix-fft/) or [Rader's algorithm](/rader-fft/) over $\mathbb{Z}/p\mathbb{Z}$.
- **Without bit reversal.** Use decimation in frequency forward and decimation in time backward, as on the [iterative FFT page](/iterative-fft/).

## When to use it

Use the NTT for exact multiplication of polynomials with integer or modular coefficients, for convolution modulo a prime (as in counting problems modulo $998244353$), and inside fast algorithms of computer algebra: division, multipoint evaluation, interpolation, and [polynomial arithmetic](/polynomial-multiplication/) in general. Use it for big integers through several primes or through Schönhage-Strassen. Prefer the complex FFT when the data are real measurements and an error of order $u \log n$ is acceptable, or when the needed range would require many primes.

## Pitfalls

- **Length does not divide $p - 1$.** Then no root of order $n$ exists, and an arbitrary $g^{(p-1)/n}$ with non-integer exponent is meaningless. Check line L3.
- **Wrong primitive root.** If $g$ is not a primitive root, $\omega$ may have order smaller than $n$, and the transform is not invertible. For $97$, the number $3$ is not a primitive root, but $5$ is.
- **Overflow of coefficients.** The result is modulo $p$; if the true coefficients may exceed $p/2$ in absolute value, use more primes.
- **Overflow of machine words.** The product of two residues needs $2 \lg p$ bits; with $p$ near $2^{31}$ that is $62$ bits, and with $p$ near $2^{62}$ it needs 128-bit products.
- **Negative residues.** In languages where the remainder of a negative number is negative, $(u - v) \bmod p$ must be corrected by adding $p$.
- **Padding.** Without padding to $n \ge \ell_a + \ell_b - 1$, the result is the cyclic, wrapped product.

## Implementations

The Python file `impl/python/number_theoretic_transform.py` has `root_of_unity`, `ntt` (lines L10 to L18), `multiply_mod` (lines L1 to L9), and `multiply_exact`, which uses the three primes and Garner's form of the Chinese remainder theorem and returns signed coefficients. The tests compare `ntt` with the direct $O(n^2)$ DFT modulo $17$, $97$ and $998244353$ with exact equality, invert it, compare products with schoolbook multiplication, check exact products with coefficients up to $10^9$ in absolute value and lengths up to $120$, cover zeros, impulses, constants and lengths $1$ and $2$, check the error for a length not dividing $p - 1$, and check the example above.

## History

Pollard (1971) described the fast Fourier transform in a finite field, with a root of unity of order $n$ in the field, and its use for exact convolution and multiplication. In the same year, Schönhage and Strassen (1971) published integer multiplication in $O(N \log N \log \log N)$ bit operations using transforms over $\mathbb{Z}/(2^m + 1)$, where $2$ is a root of unity. Agarwal and Burrus (1974) proposed Fermat number transforms for digital filtering, and their survey (1975) treats number theoretic transforms in general: the conditions on the modulus for a transform of length $n$ with the convolution property, and the Fermat and Mersenne cases. Garner (1959) gave the mixed-radix conversion from residues used to combine several primes.

## References
