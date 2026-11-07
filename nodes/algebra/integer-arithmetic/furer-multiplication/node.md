---
tag: V5N955
kind: algorithm
slug: furer-multiplication
name: Fürer's multiplication
aliases:
- Fürer's algorithm
- Fürer's integer multiplication
area: algebra/integer-arithmetic
level: research
summary: Integer multiplication in n log n 2^O(log* n) bit operations, improving Schönhage-Strassen.
solves: [integer-multiplication]
model: multitape-turing-machine
complexity:
  vars: {N: the length of each operand in binary digits}
  time: {worst: N log N 2^(O(log* N)), average: N log N 2^(O(log* N)), best: N log N 2^(O(log* N))}
properties: {deterministic: true, recursive: true, in_place: false}
history:
  note: Fürer (2007) broke the O(N log N log log N) bound of Schönhage and Strassen (1971) with an FFT over a ring that has cheap high-order roots of unity.
prereqs: [schonhage-strassen-multiplication, fast-fourier-transform, integer-multiplication]
see_also: [schonhage-strassen-multiplication, harvey-van-der-hoeven-multiplication, integer-multiplication, fast-fourier-transform, number-theoretic-transform, karatsuba-multiplication, toom-cook-multiplication, fft-polynomial-multiplication]
sources:
  - paper: doi:10.1137/070711761
    title: Martin Fürer, Faster integer multiplication, SIAM Journal on Computing 39(3), 2009
    locator: pp. 979 to 1005 (the ring C[x]/(x^P + 1), the root of unity whose power is x, the decomposition of the FFT, and the main theorem; conference version in STOC 2007, pp. 57 to 66)
  - paper: doi:10.1137/100811167
    title: Anindya De, Piyush P. Kurur, Chandan Saha and Ramprasad Saptharishi, Fast integer multiplication using modular arithmetic, SIAM Journal on Computing 42(2), 2013
    locator: pp. 685 to 699 (the same bound with coefficients in a ring of integers modulo a prime power instead of complex numbers; conference version in STOC 2008)
  - paper: doi:10.1016/j.jco.2016.03.001
    title: David Harvey, Joris van der Hoeven and Grégoire Lecerf, Even faster integer multiplication, Journal of Complexity 36, 2016
    locator: pp. 1 to 30 (the bound O(N log N 8^(log* N)), and Section 1 on Fürer's method and its analysis)
  - paper: doi:10.4007/annals.2021.193.2.4
    title: David Harvey and Joris van der Hoeven, Integer multiplication in time O(n log n), Annals of Mathematics 193(2), 2021
    locator: pp. 563 to 617 (Section 1, the history of the bounds from Schönhage-Strassen to Fürer and after)
---

Fürer's multiplication multiplies two $N$-bit integers in $N \log N \cdot 2^{O(\log^* N)}$ bit operations, where $\log^* N$ is the number of times the logarithm must be applied to bring $N$ down to 1. It was the first improvement, in 2007, on the $O(N \log N \log \log N)$ bound of [Schönhage-Strassen](/schonhage-strassen-multiplication/) from 1971. Like Schönhage-Strassen it cuts the numbers into pieces, multiplies them as polynomials with a [fast Fourier transform](/fast-fourier-transform/), and multiplies the transformed pieces by recursion. The new idea is the ring: $\mathbb{C}[x]/(x^P + 1)$, with $P$ about $\log N$, has a root of unity of high order whose $(N/2P)$-th power is $x$. Most multiplications by roots in the FFT then become multiplications by powers of $x$, which are shifts, and only a fraction $1/\log P$ of them are real products. The method is of theoretical interest only, and this page gives a small exact model of its structure.

## In plain words

Fast multiplication by Fourier transform has two kinds of work: adding and subtracting numbers, and multiplying them by "roots of unity", special numbers whose powers come back to 1. Schönhage and Strassen chose numbers in which multiplying by a root is just moving digits, which is cheap, but then the pieces had to be large, and the recursion lost a factor at every level.

Fürer found a number system with both properties at once: small pieces and many roots that are cheap. In his ring, one special root behaves like the cheap one when raised to a certain power. Arrange the transform in blocks so that, inside each block, only the cheap powers are needed. The expensive products then appear only between blocks, which cuts their number by a factor that grows with the input size.

## The problem

The input is two integers $u, v \ge 0$ of at most $N$ binary digits each, and the output is $uv$. Here the digits are grouped into limbs of $b$ bits, the base being $\beta = 2^b$. In Fürer's algorithm $b$ is about $\log N$, and the toy below takes $b$ as a parameter.

**Cost model.** The bound $N \log N \cdot 2^{O(\log^* N)}$ counts bit operations on a [multitape Turing machine](/multitape-turing-machine/); Fürer proves it for that model and for Boolean circuits, and it is not proved on this page, which gives the recurrence and its solution only as a sketch. The code is a toy structural model: it counts operations in the ring $R = \mathbb{Z}_q[x]/(x^m + 1)$, separating *shifts* (multiplications by a power of $x$) from *general products* in $R$. The exact counts of shifts, twiddle products and pointwise products of the toy, and its correctness, are proved below. Timings and the size at which the method would pay are not measured and are not claimed.

## The algorithm

Let $m$ be a power of 2, $K = 2m$ and $N_t = K^L$ the transform length. The ring is $R = \mathbb{Z}_q[x]/(x^m + 1)$ for the prime $q = 998244353 = 119 \cdot 2^{23} + 1$; Fürer uses complex coefficients, and the exact ring here follows the modular variant of De, Kurur, Saha and Saptharishi. In $R$, $x$ has order $K$, since $x^m = -1$. The root $\rho \in R$ is chosen so that $\rho^{N_t/K} = x$: since $x^m + 1$ splits into the linear factors $x - \zeta^{2i+1}$ modulo $q$, with $\zeta$ a primitive $K$-th root of unity in $\mathbb{Z}_q$, define $\rho$ by its values $\rho(\zeta^{2i+1}) = \omega^{2i+1}$, where $\omega$ is a primitive $N_t$-th root in $\mathbb{Z}_q$ with $\omega^{N_t/K} = \zeta$. This is Fürer's construction.

```pseudo id=main
FURER-MULTIPLY(u, v)              ▷ R = Z_q[x]/(x^m + 1), K = 2m, N_t = K^L, ρ^(N_t/K) = x
L1  cut u and v into N_t/2 blocks of m/2 limbs; each block is an element of R with its top m/2 coefficients 0
L2  â ← FFT(a, 1, +1); b̂ ← FFT(b, 1, +1)
L3  for j ← 0 to N_t − 1 do ĉ_j ← â_j · b̂_j       ▷ general products in R: recursive calls in Fürer
L4  c ← FFT(ĉ, 1, −1)
L5  return Σ_j (c_j(β)/N_t) · β^(j m/2)          ▷ evaluate at x = β, scale and carry

FFT(v, s, σ)                      ▷ |v| = K^ℓ, |v| · s = N_t; the root is ω = ρ^(σ s)
L6  if |v| = K then return the radix-2 DFT of v with root x^σ          ▷ shifts only
L7  J ← |v|/K; for n₁ ← 0 to J − 1 do y_{n₁} ← FFT((v_{J n₂ + n₁}) for n₂ < K, N_t/K, σ)
L8  for all n₁ < J, k₁ < K with ω^(n₁ k₁) ≠ 1 do y_{n₁,k₁} ← y_{n₁,k₁} · ω^(n₁ k₁)   ▷ the twiddles
L9  for k₁ ← 0 to K − 1 do (X_{k₁ + K k₂}) for k₂ < J ← FFT((y_{n₁,k₁}) for n₁ < J, s K, σ)
L10 return X
```

Line L7 does $J$ transforms of length $K$, all with the root $\omega^J = \rho^{N_t/K \cdot \sigma} = x^\sigma$, so they reach line L6 and use shifts only. Line L9 does $K$ transforms of length $J$ by recursion. General products appear only in line L8 and in line L3.

## Example

Take $m = 2$, so $R = \mathbb{Z}_q[x]/(x^2 + 1)$ and $K = 4$, with $L = 2$, so $N_t = 16$, and limbs of $b = 4$ bits. Then $\rho = 778973088 + 143879836\, x$, and indeed $\rho^4 = x$ and $\rho^8 = -1$ in $R$. Each element holds $m/2 = 1$ limb, so the transform holds operands of $8$ limbs. For $u = \mathtt{BEEF}$ and $v = \mathtt{CAFE}$ (hexadecimal), line L1 gives the limbs, lowest first, $(15, 14, 14, 11)$ and $(14, 15, 10, 12)$, padded with zeros to 16 elements. After line L4, the elements $c_j / 16$ are the constants

$$(210, 421, 556, 684, 473, 278, 132, 0, \dots, 0),$$

the coefficients of the product of the two digit polynomials. Line L5 carries them in base 16 and returns $\mathtt{97660722} = 2540046114 = uv$. The three transforms use $3 \cdot 32 = 96$ shifts and $3 \cdot 9 = 27$ twiddle products, and line L3 uses 16 products.

The table compares one transform of length $N_t$ in the toy with a radix-2 FFT of the same length over the same ring and root, where a butterfly is cheap when its root is a power of $x$. The counts are those of the code, which match the formulas of the Complexity section.

| $m$ | $K$ | $L$ | $N_t$ | shifts | twiddle products, toy | expensive products, radix 2 |
|---|---|---|---|---|---|---|
| 2 | 4 | 2 | 16 | 32 | 9 | 10 |
| 2 | 4 | 3 | 64 | 192 | 81 | 98 |
| 4 | 8 | 3 | 512 | 2304 | 833 | 1284 |
| 4 | 8 | 4 | 4096 | 24576 | 10241 | 16388 |
| 8 | 16 | 2 | 256 | 1024 | 225 | 392 |
| 8 | 16 | 3 | 4096 | 24576 | 7425 | 14344 |

The ratio in the last two columns grows like $\frac12 \log_2 K$: about 1.5 for $K = 8$ and about 2 for $K = 16$. In Fürer's algorithm $K = 2P$ grows like $\log N$, and so does the saving.

## Correctness

The full proof for the toy is in the proof file; it has three parts. First, $\rho$ is a principal $N_t$-th root of unity in $R$ with $\rho^{N_t/K} = x$: by the Chinese remainder theorem $R \cong \mathbb{Z}_q^m$ through evaluation at the $m$ roots $\zeta^{2i+1}$ of $x^m + 1$, and in each coordinate $\rho$ is $\omega^{2i+1}$, a primitive $N_t$-th root of unity in the field $\mathbb{Z}_q$. Second, FFT computes the DFT: lines L7 to L9 are the Cooley-Tukey split $n = J n_2 + n_1$, $k = k_1 + K k_2$, and line L6 is the radix-2 DFT with root $x^\sigma$, which equals $\omega$ since $\omega = \rho^{\sigma N_t/K}$ when $|v| = K$. Third, the cyclic convolution of the two padded vectors equals the plain product of the digit polynomials, since each has degree less than $N_t/2$ in the outer variable and less than $m/2$ in $x$, so neither the cyclic wrap nor $x^m = -1$ ever applies, and each coefficient is at most $(N_t/2)(m/2)(\beta - 1)^2 < q$, which the code checks, so no reduction modulo $q$ changes it.

## Complexity

**The toy, proved.** One FFT of length $N_t = K^L$ does $\frac{N_t}{2} \log_2 N_t$ shifts, since each of its $L N_t/K$ base transforms does $\frac K2 \log_2 K$, and

$$(L - 1)(K - 1)\frac{N_t}{K} - \frac{N_t}{K} + 1$$

twiddle products. *Proof.* Let $T(\ell)$ be the number of twiddle products for length $K^\ell$. Line L8 multiplies by $\omega^{n_1 k_1}$ with $n_1 k_1 < N_t/s$, which is 1 only when $n_1 = 0$ or $k_1 = 0$, so it does $(K^{\ell - 1} - 1)(K - 1)$ products, and $T(\ell) = (K^{\ell-1} - 1)(K - 1) + K\,T(\ell - 1)$ with $T(1) = 0$. Unrolling gives $T(L) = \sum_{i=0}^{L-2} K^i (K^{L-1-i} - 1)(K - 1)$, which is the formula. $\square$ So the twiddle products number about $N_t \log_2 N_t / \log_2 K$, against about $\frac{N_t}{2}(\log_2 N_t - \log_2 K)$ for the radix-2 FFT.

**Fürer's algorithm, a sketch.** With $P$ about $\log N$, each element of $R = \mathbb{C}[x]/(x^P + 1)$ carries $P/2$ pieces of about $\log N$ bits, so the transform length is about $N/\log^2 N$, and the coefficients are kept to $O(\log N)$ bits of precision. The shifts and additions cost $O(N \log N)$ bit operations in all. There are $O(\frac{N \log N}{\log^2 N \cdot \log \log N})$ general products in $R$, and each is done by packing its coefficients into one integer of $O(\log^2 N)$ bits and multiplying by recursion. So

$$T(N) \le C \frac{N \log N}{\log^2 N \cdot \log \log N}\, T(c \log^2 N) + C N \log N .$$

Writing $T(N) = N \log N \cdot t(N)$ gives $t(N) \le C' t(c \log^2 N) + C$, and the recursion reaches a constant size after $O(\log^* N)$ steps, so $t(N) = 2^{O(\log^* N)}$. The constant $C' > 1$ lost at each level is why the factor is $2^{O(\log^* N)}$ and not $O(1)$. The precision analysis and the details of the Turing machine implementation are in Fürer's paper.

## Properties

- **Deterministic.** No randomness and no unproved hypothesis are needed for the bound.
- **Recursive.** The recursion has depth $O(\log^* N)$ in the size of the products, and the FFT itself has depth $L$ in the toy.
- **Not in place.** The transforms need the padded vectors, about twice the input size.
- **Numerical in the original.** Fürer works with approximate complex numbers and bounds the rounding error; the modular variants are exact.

## Variants and improvements

- **Modular arithmetic.** De, Kurur, Saha and Saptharishi (2008) obtained the same bound with coefficients in a ring of integers modulo a prime power, which avoids the error analysis; the toy here uses exact coefficients modulo a prime in the same spirit.
- **Explicit constants.** Harvey, van der Hoeven and Lecerf (2016) gave $O(N \log N \cdot 8^{\log^* N})$, with a different organization of the transforms. Later papers lowered the base of the exponent to 4.
- **$O(N \log N)$.** [Harvey and van der Hoeven](/harvey-van-der-hoeven-multiplication/) removed the factor $2^{O(\log^* N)}$ in 2019 (published 2021), with multidimensional transforms that reduce the size of the recursive products much faster than $N \mapsto \log^2 N$.

## When to use it

Not in practice. The saving over Schönhage-Strassen is a factor $\log \log N / 2^{O(\log^* N)}$, which is tiny for any size that fits in a computer, and the constants are larger. GMP and other big-number libraries use [Toom-Cook](/toom-cook-multiplication/), Schönhage-Strassen or [number-theoretic transforms](/number-theoretic-transform/) for large operands. The value of the algorithm is in the idea: a ring whose roots of unity are partly cheap and partly not, with the transform arranged so that the expensive ones are rare.

## Pitfalls

- **Taking a root that is not compatible with $x$.** If line L7 used any primitive $N_t$-th root $\rho$ without $\rho^{N_t/K} = x$, the inner transforms would need general products, and the saving vanishes. The right choice is the one in the setup: $\rho$ defined by $\rho(\zeta^{2i+1}) = \omega^{2i+1}$, so that $\rho^{N_t/K} = x$ holds exactly.
- **Filling the whole element.** If line L1 put $m$ limbs in each element instead of $m/2$, the product of two elements would have degree up to $2m - 2$, and $x^m = -1$ would fold the top half back onto the bottom with a minus sign. Line L1 must leave the top $m/2$ coefficients zero.
- **Coefficient overflow.** In the toy, a coefficient of the product can reach $(N_t/2)(m/2)(\beta - 1)^2$; if this is $q$ or more, line L5 reads it modulo $q$ and returns a wrong product. The code refuses such parameters. In Fürer's complex version the same issue is the working precision, which must grow like $\log N$.
- **Forgetting the scaling.** The inverse transform of line L4 gives $N_t$ times the convolution; line L5 must multiply by $N_t^{-1} \bmod q$ before evaluating.

## Implementations

## History

Schönhage and Strassen (1971) gave $O(N \log N \log \log N)$ and conjectured that $N \log N$ is the right order. For 36 years nothing better was known. Martin Fürer presented his algorithm at STOC 2007, with the journal version in SIAM Journal on Computing in 2009, and proved $N \log N \cdot 2^{O(\log^* N)}$ for multitape Turing machines and Boolean circuits. De, Kurur, Saha and Saptharishi (STOC 2008) gave a version with modular arithmetic. Harvey, van der Hoeven and Lecerf (2016) made the constant in the exponent explicit, and Harvey and van der Hoeven reached $O(N \log N)$ in 2019, published in the Annals of Mathematics in 2021.

## References
