---
tag: XRQ0DB
kind: algorithm
slug: schonhage-strassen-multiplication
name: Schönhage-Strassen multiplication
aliases:
- FFT multiplication
- Schönhage-Strassen algorithm
- SSA
- Fermat number transform multiplication
area: algebra/integer-arithmetic
level: advanced
summary: FFT-based multiplication in O(n log n log log n) bit operations.
solves: [integer-multiplication]
model: multitape-turing-machine
complexity:
  vars: {N: the length of each operand in binary digits}
  time: {worst: O(N log N log log N), average: O(N log N log log N), best: O(N log N log log N)}
  space: {extra: O(N)}
properties: {deterministic: true, recursive: true, in_place: false}
prereqs: [fast-fourier-transform, convolution-theorem, karatsuba-multiplication]
see_also: [toom-cook-multiplication, karatsuba-multiplication, furer-multiplication, harvey-van-der-hoeven-multiplication, number-theoretic-transform, fft-polynomial-multiplication, integer-multiplication, chinese-remainder-theorem-fft]
sources:
  - paper: doi:10.1007/BF02242355
    title: Arnold Schönhage and Volker Strassen, Schnelle Multiplikation großer Zahlen, Computing 7, 1971
    locator: pp. 281 to 292 (the method with arithmetic modulo Fermat numbers 2^(2^k) + 1, the bound O(N log N log log N), and the method with complex numbers)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 2.3, Fast Fourier transform (2.3.3, The Schönhage-Strassen algorithm, Algorithm FFTMulMod and its cost)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.3, How fast can we multiply? (discrete Fourier transforms, and the Schönhage-Strassen method with arithmetic modulo 2^e + 1)
  - paper: doi:10.1145/1277548.1277572
    title: Pierrick Gaudry, Alexander Kruppa and Paul Zimmermann, A GMP-based implementation of Schönhage-Strassen's large integer multiplication algorithm, ISSAC 2007
    locator: pp. 167 to 174 (the implementation in GMP, the sqrt 2 trick, the choice of parameters and timings)
  - url: https://gmplib.org/manual/FFT-Multiplication
    title: The GNU Multiple Precision Arithmetic Library manual, FFT Multiplication
    locator: Section 15.1.6 (the transform modulo 2^N' + 1, the split into 2^k pieces, and the threshold MUL_FFT_THRESHOLD)
---

Schönhage-Strassen multiplication computes the product of two $N$-digit binary numbers with a fast Fourier transform over a ring where the root of unity is a power of 2. It cuts each factor into $K \approx \sqrt{N}$ pieces, so that the product is a convolution of the two sequences of pieces. The transforms work modulo $2^{n'} + 1$, where 2 is a root of unity of order $2n'$, so every multiplication by a root of unity is a shift, and no rounding error is possible. The $K$ products of transformed values are products modulo $2^{n'} + 1$ with $n' \approx 2\sqrt{N}$, done by the same method recursively. On the multitape Turing machine this gives $O(N \log N \log \log N)$ bit operations. Published by Arnold Schönhage and Volker Strassen in 1971, it was the fastest known method for 36 years, until Fürer (2007), and it is the FFT method of GMP for very large numbers.

## In plain words

Multiplying two long numbers is the same as multiplying two polynomials, with the digits as coefficients, and then carrying. The fast Fourier transform multiplies polynomials quickly: transform both, multiply the results pointwise, and transform back. But the usual transform uses complex numbers, which a computer rounds.

Schönhage and Strassen made the transform exact. They computed modulo a number of the form $2^m + 1$. There, multiplying by 2 again and again eventually gives $-1$, so the number 2 plays the role of a complex root of unity, and multiplying by a power of 2 is just a shift. The transforms then need only shifts, additions and subtractions. The pointwise products are products of numbers of about $2\sqrt{N}$ digits, done by the same method again.

## The problem

The input is two nonnegative integers given as arrays of limbs in radix $\beta = 2^w$, of $N$ binary digits each. The output is their product; see [integer multiplication](/integer-multiplication/). The algorithm solves the more general task of multiplying modulo $2^n + 1$: for residues $0 \le A, B \le 2^n$, compute $AB \bmod (2^n + 1)$. Taking $n$ larger than the length of the product makes the residue equal to the product.

**Cost model.** Multitape Turing machine, or equivalently the bit complexity model: the cost is the number of bit operations, and the length $N$ is in binary digits. The bound $O(N \log N \log \log N)$ is proved in this model. On the [word RAM](/word-ram/), implementations work on limbs, and shifts, additions and subtractions of $m$-digit numbers cost $O(m/w)$ limb operations. Thresholds and running times are observed.

## The algorithm

Write $\llbracket x \rrbracket_m$ for $x \bmod (2^m + 1)$. Following Brent and Zimmermann's Algorithm FFTMulMod:

```pseudo id=main
SSA-MULMOD(A, B, n)                        ▷ returns A·B mod 2^n + 1
L1  if n is small then return the product by a base method, reduced mod 2^n + 1
L2  choose K = 2^k with K | n, about √n;  M ← n / K;  A = Σ a_j 2^(jM),  B = Σ b_j 2^(jM)
L3  choose n' ≥ 2M + k + 1 with K | n';  θ ← 2^(n'/K)       ▷ θ^K = 2^n' = −1 mod 2^n' + 1
L4  a_j ← ⟦θ^j a_j⟧_n',  b_j ← ⟦θ^j b_j⟧_n'  for j < K              ▷ weights, by shifts
L5  â ← DFT_ω(a),  b̂ ← DFT_ω(b)  over Z/(2^n' + 1), with ω = θ^2    ▷ butterflies with shifts
L6  ĉ_j ← SSA-MULMOD(â_j, b̂_j, n')  for j < K                     ▷ K recursive products
L7  c ← DFT_(ω^−1)(ĉ)
L8  c_j ← ⟦c_j / (K θ^j)⟧_n'                                         ▷ a shift by −(k + j n'/K)
L9  if c_j ≥ (j + 1) 2^(2M) then c_j ← c_j − (2^n' + 1)              ▷ the value is negative
L10 return ⟦Σ c_j 2^(jM)⟧_n
```

Line L1 also handles the residue $2^n$, which is $-1$: then the product is $\llbracket -B \rrbracket_n$. In line L2 the pieces $a_j$ have $M$ binary digits, and the product $AB$ modulo $2^n + 1$ is the *negacyclic* convolution of the pieces, because $2^{KM} = 2^n \equiv -1$: a term that would land at position $j + K$ comes back at position $j$ with a minus sign. The weights $\theta^j$ of line L4 turn this negacyclic convolution into the cyclic convolution that a transform of length $K$ computes. Line L9 recovers the sign: the true $c_j$ lies between $-(K - 1 - j)2^{2M}$ and $(j + 1)2^{2M}$, a range shorter than $2^{n'} + 1$ by the choice of $n'$.

## Example

**One level for $n = 16$.** Multiply $A = 4660 = \mathtt{1234}_{16}$ by $B = 22136 = \mathtt{5678}_{16}$ modulo $2^{16} + 1 = 65537$, with $K = 4$ pieces of $M = 4$ binary digits, $n' = 12$, $2^{12} + 1 = 4097$, $\theta = 2^3$ and $\omega = 2^6$. The pieces, least significant first, are $a = (4, 3, 2, 1)$ and $b = (8, 7, 6, 5)$.

| step | sequence |
|---|---|
| weighted $a$, line L4 | $4, 24, 128, 512$ |
| weighted $b$ | $8, 56, 384, 2560$ |
| $\hat a$, line L5 | $668, 1420, 3693, 2429$ |
| $\hat b$ | $3008, 3248, 1873, 97$ |
| $\hat c_j = \hat a_j \hat b_j \bmod 4097$, line L6 | $1814, 3035, 1253, 2084$ |
| inverse transform, line L7 | $4089, 1152, 2045, 4067$ |
| divided by $K\theta^j$, line L8 | $4095, 36, 56, 60$ |
| signed, line L9 | $-2, 36, 56, 60$ |

The last line is the negacyclic convolution: $c_0 = 4 \cdot 8 - (3 \cdot 5 + 2 \cdot 6 + 1 \cdot 7) = -2$, and $c_3 = 4 \cdot 5 + 3 \cdot 6 + 2 \cdot 7 + 1 \cdot 8 = 60$. Line L10 gives $-2 + 36 \cdot 2^4 + 56 \cdot 2^8 + 60 \cdot 2^{12} = 260670 \equiv 64059$, and indeed $4660 \cdot 22136 = 103153760 \equiv 64059 \pmod{65537}$. All values were computed by the implementation and are checked by its test.

## Correctness

Since $2^{KM} = 2^n \equiv -1 \pmod{2^n + 1}$, the product $AB = \sum_{i,l} a_i b_l 2^{(i+l)M}$ is congruent to $\sum_j c_j 2^{jM}$ with the negacyclic convolution $c_j = \sum_{i + l = j} a_i b_l - \sum_{i + l = j + K} a_i b_l$. Modulo $2^{n'} + 1$, the number $\omega = 2^{2n'/K}$ is a principal $K$-th root of unity: $\omega^{K/2} = 2^{n'} = -1$. So the [convolution theorem](/convolution-theorem/) holds in this ring, and lines L5 to L7 compute $K$ times the cyclic convolution of the weighted sequences, which is $K\theta^j c_j$ because $\theta^K = -1$ turns the wrapped terms into subtracted ones. The divisions of line L8 are exact, since $2$ is invertible modulo the odd number $2^{n'} + 1$. Since $|c_j| < K 2^{2M} \le 2^{n'}$, line L9 recovers $c_j$ as an integer, and line L10 reduces modulo $2^n + 1$. By induction, the recursive products of line L6 are correct. The full proof is below.

## Complexity

**One level.** Line L2 cuts $A$ and $B$ for free. Lines L4, L5, L7 and L8 consist of $O(K \log K)$ shifts, additions and subtractions of numbers of $n' + 1$ binary digits, about $K n' \log K = O(n \log n)$ bit operations, since $Kn' \approx 2n + K(k + 1)$. Line L6 makes $K$ recursive products of size $n'$, and line L10 adds $K$ overlapping numbers, $O(n)$. So

$$T(n) \le K \, T(n') + O(n \log n), \qquad K \approx \sqrt{n}, \quad n' \approx 2\sqrt{n} .$$

**The whole recursion.** Dividing by $n$ gives $T(n)/n \le 2 \, T(n')/n' + O(\log n)$. The recursion has $\log_2 \log_2 n + O(1)$ levels, since $n' \approx 2\sqrt n$ halves the length of $n$, and the factor 2 per level and the shrinking $O(\log n)$ terms combine to $T(n) = O(n \log n \log \log n)$ (Brent and Zimmermann, Section 2.3.3, with $K$ chosen near $\sqrt{n}$ at every level). For two $N$-digit numbers $n \approx 2N$, so the multiplication costs $O(N \log N \log \log N)$ bit operations. This bound is proved; Schönhage and Strassen proved it for multitape Turing machines.

**Measured.** In the implementation, two random numbers of $2^{14}$ binary digits are multiplied with $n = 33024$, $K = 128$ and $n' = 640$, then $K = 16$ and $n' = 96$, then $K = 8$ and $n' = 32$: three levels of recursion and $16384 = 128 \cdot 16 \cdot 8$ base products of at most 64 binary digits. For $2^{16}$ digits the levels are $(n, K, n') = (131584, 256, 1280)$, $(1280, 32, 96)$ and $(96, 8, 32)$, again three. The recursion depth grows as $\log \log N$.

**In practice.** The constant factors are moderate, and the method is used for very large sizes only: GMP switches to it at a threshold of some thousands of limbs, tuned for each machine. The method also has a $\log \log N$ factor that the later algorithms of Fürer and of Harvey and van der Hoeven remove or reduce, but those have not replaced it in practice.

## Properties

- **Exact.** All arithmetic is in integers modulo $2^{n'} + 1$; there is no floating point and no rounding analysis.
- **Multiplications by roots of unity are shifts.** Since $\omega$ is a power of 2, the transforms use only shifts, additions and subtractions.
- **Product modulo $2^n + 1$ for free.** The algorithm computes products modulo $2^n + 1$ directly, which is what the recursion needs and what Fermat-modulus applications want.
- **Recursion depth $\log \log N$.** Each level takes the square root of the size, roughly.
- **Not the fastest asymptotically.** $O(N \log N)$ is reached by Harvey and van der Hoeven, but with much larger constants.

## Variants and improvements

- **Complex FFT.** Schönhage and Strassen's paper also gives a version with complex numbers in fixed-point arithmetic of $O(\log N)$ binary digits, with the same bound; floating-point FFT multiplication with error bounds is common in practice, for example in programs for record computations of $\pi$.
- **Number-theoretic transforms over primes.** Pollard (1971) used transforms modulo word-sized primes with roots of unity, and the [Chinese remainder theorem](/chinese-remainder-theorem-fft/) to combine three or more of them; see [number-theoretic transform](/number-theoretic-transform/). This is fast for sizes that fit the primes.
- **The $\sqrt{2}$ trick.** In $\mathbb{Z}/(2^{n'} + 1)$ with $4 \mid n'$, $2^{3n'/4} - 2^{n'/4}$ is a square root of 2, which allows transforms of twice the length; Gaudry, Kruppa and Zimmermann use it with other improvements in GMP.
- **Truncated FFT and Mersenne moduli.** Truncated transforms avoid padding to a power of 2, and a second product modulo $2^m - 1$ can replace the doubling of $n$.
- **Fürer's algorithm (2007).** Uses a ring with complex numbers and fast roots of unity to bring the bound to $N \log N \cdot 2^{O(\log^* N)}$; see [Fürer multiplication](/furer-multiplication/).
- **Harvey and van der Hoeven (2019, published 2021).** $O(N \log N)$, with multidimensional transforms; see [Harvey-van der Hoeven multiplication](/harvey-van-der-hoeven-multiplication/).

## When to use it

Use Schönhage-Strassen, or another FFT method, for products of tens of thousands of limbs and more: computing constants to millions of digits, large Mersenne and Fermat number tests, polynomial arithmetic with large coefficients, and the fast division, square root and radix conversion algorithms that reduce to multiplication. Below that, [Toom-Cook](/toom-cook-multiplication/) and [Karatsuba](/karatsuba-multiplication/) are faster. Floating-point FFT multiplication can be faster still in a range of sizes, but needs a careful error analysis.

## Pitfalls

- **The residue $2^n$.** A residue modulo $2^n + 1$ can equal $2^n$, which does not fit in $n$ binary digits; its top piece is then $2^M$ and the bound on $c_j$ fails. Treat it as $-1$, as line L1 does.
- **Too small an $n'$.** With $n' < 2M + k + 1$, the values $c_j$ can exceed the modulus and line L9 recovers the wrong integer, silently.
- **Signs after the inverse transform.** The values $c_j$ of a negacyclic convolution can be negative; forgetting line L9 gives wrong results whenever a wrapped term exceeds the direct one.
- **Recursion that does not shrink.** For small $n$, $n' \ge 2n/K + k + 1$ can be as large as $n$; switch to the base case there. The implementation does this.
- **Divisibility.** $K$ must divide $n$ and $n'$; choosing sizes that are multiples of large powers of 2 avoids failing splits at lower levels.

## Implementations

## History

Arnold Schönhage and Volker Strassen published the method in 1971 in Computing, together with a version using complex numbers, and conjectured that $N \log N$ is the right order for multiplication. The same year Pollard described FFT multiplication over finite fields. Both build on the Cooley-Tukey FFT of 1965. The earlier fast methods were [Karatsuba's](/karatsuba-multiplication/) of 1962 and [Toom-Cook](/toom-cook-multiplication/), Toom 1963 and Cook 1966. The bound $O(N \log N \log \log N)$ stood until Fürer's algorithm of 2007, and the conjectured $O(N \log N)$ was reached by Harvey and van der Hoeven in 2019, published in 2021. Schönhage-Strassen became the large-number multiplication of GMP, improved by Gaudry, Kruppa and Zimmermann in 2007.

## References
