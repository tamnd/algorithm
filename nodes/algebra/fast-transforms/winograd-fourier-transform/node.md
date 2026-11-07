---
tag: XCA95E
kind: algorithm
slug: winograd-fourier-transform
name: Winograd Fourier transform algorithm
aliases:
- WFTA
- Winograd FFT
- nested Winograd algorithm
area: algebra/fast-transforms
level: research
summary: Minimal-multiplication DFT for small lengths built from nested prime-factor decompositions.
solves: [discrete-fourier-transform]
model: real-ram
complexity:
  vars: {n: the transform length (a product of pairwise coprime factors from 2 3 4 5 7 8), d: the number of factors, M: the product of the module sizes m_i (at most 1.55 n)}
  time: {worst: O(d M)}
  space: {extra: O(M)}
  additions: {worst: O(d M)}
  multiplications: {worst: O(M)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1976
  people: [S. Winograd]
  note: Winograd (1976 and 1978) computed short DFTs with few multiplications by reducing them to cyclic convolutions, using his result on the multiplicative complexity of products modulo a polynomial, and nested them with the prime-factor index map of Good (1958) so that all multiplications of a long transform happen in one stage. Silverman (1977) gave a programming guide and Kolba and Parks (1977) compared it with the prime-factor algorithm built from the same modules.
prereqs: [discrete-fourier-transform, chinese-remainder-theorem-fft, rader-fft]
see_also: [kronecker-product, circular-convolution, bilinear-complexity, mixed-radix-fft, split-radix-fft, multidimensional-fft, toom-cook-multiplication, fast-fourier-transform]
sources:
  - paper: doi:10.1073/pnas.73.4.1005
    title: S. Winograd, On computing the discrete Fourier transform, Proceedings of the National Academy of Sciences 73(4), 1976
    locator: pp. 1005 to 1006 (announcement; substantially fewer multiplications for n from a few tens to a few thousands)
  - paper: doi:10.1090/S0025-5718-1978-0468306-4
    title: Shmuel Winograd, On computing the discrete Fourier transform, Mathematics of Computation 32(141), 1978
    locator: pp. 175 to 199 (the short modules from convolution algorithms and their nesting)
  - paper: doi:10.1007/BF01683270
    title: S. Winograd, Some bilinear forms whose multiplicative complexity depends on the field of constants, Mathematical Systems Theory 10(1), 1977
    locator: pp. 169 to 180 (the multiplicative complexity of products modulo a polynomial)
  - paper: doi:10.1109/TASSP.1977.1162924
    title: Harvey F. Silverman, An introduction to programming the Winograd Fourier transform algorithm (WFTA), IEEE Transactions on Acoustics, Speech, and Signal Processing 25(2), 1977
    locator: pp. 152 to 165
  - paper: doi:10.1109/TASSP.1977.1162973
    title: David P. Kolba and Thomas W. Parks, A prime factor FFT algorithm using high-speed convolution, IEEE Transactions on Acoustics, Speech, and Signal Processing 25(4), 1977
    locator: pp. 281 to 294 (comparison of the prime-factor algorithm and the WFTA in multiplications and additions)
  - paper: doi:10.1111/j.2517-6161.1958.tb00300.x
    title: I. J. Good, The interaction algorithm and practical Fourier analysis, Journal of the Royal Statistical Society Series B 20(2), 1958
    locator: pp. 361 to 372 (the index map for coprime factors)
  - paper: doi:10.1109/PROC.1968.6477
    title: C. M. Rader, Discrete Fourier transforms when the number of data samples is prime, Proceedings of the IEEE 56(6), 1968
    locator: pp. 1107 to 1108
  - paper: doi:10.1016/0196-8858(84)90005-8
    title: L. Auslander, E. Feig and S. Winograd, The multiplicative complexity of the discrete Fourier transform, Advances in Applied Mathematics 5(1), 1984
    locator: pp. 87 to 109
---

The Winograd Fourier transform algorithm (WFTA) computes a [discrete Fourier transform](/discrete-fourier-transform/) of length $n = q_1 q_2 \cdots q_d$, with pairwise coprime factors, using fewer multiplications than other FFTs of similar length. Each short DFT of length $q_i$ is written as a product $C_i \,\mathrm{diag}(\mu_i)\, A_i$: a matrix $A_i$ of additions, a vector $\mu_i$ of $m_i$ constants to multiply by, and a matrix $C_i$ of additions. The [prime-factor index map](/chinese-remainder-theorem-fft/) turns the long DFT into a $d$-dimensional one, which is the [Kronecker product](/kronecker-product/) of the short ones, and the mixed-product rule regroups it as $(\bigotimes C_i)\,\mathrm{diag}(\bigotimes \mu_i)\,(\bigotimes A_i)$. So all the additions of the $A_i$ come first, then a single pointwise product of size $M = m_1 \cdots m_d$, then all the additions of the $C_i$. The short modules for prime lengths come from [Rader's reduction](/rader-fft/) to a cyclic convolution, done with the fewest multiplications.

## In plain words

A long Fourier transform whose length splits into small coprime pieces, such as 840, which is 8 times 3 times 5 times 7, can be rearranged into a table with one direction per piece, and the transform becomes a short transform along each direction. Winograd found ways to do each short transform as three steps: some additions, then a few multiplications by fixed numbers, then more additions. Normally one would finish the short transforms one direction at a time. Winograd instead does the first addition step in every direction, then all the multiplications at once, then the last addition step in every direction. This puts all the multiplications in one place, and their number is the product of the small counts, which is barely more than the length itself. The price is somewhat more additions.

## The problem

**Notation.** As on all pages of fast transforms, $X_k = \sum_{j=0}^{n-1} x_j \omega^{jk}$ for $0 \le k < n$, with no factor on the forward transform; the inverse uses $\omega^{-1}$ and the factor $1/n$. Over $\mathbb{C}$, $\omega = \omega_n = e^{-2\pi i/n}$ (the sign of signal processing, FFTW and NumPy; CLRS uses the other sign). Over $\mathbb{Z}/p\mathbb{Z}$, $\omega$ is a principal $n$-th root of unity, an element of order exactly $n$, as for the [number-theoretic transform](/number-theoretic-transform/). The length $n$ is not a power of two in general: it is a product of pairwise coprime factors $q_i$, each a length for which a short module exists. The implementation has modules for $q \in \{2, 3, 4, 5, 7, 8\}$, so $n$ divides $840$; Winograd's papers also give modules of lengths $9$ and $16$, which reach $5040$.

**Input.** $x_0, \ldots, x_{n-1}$, the factors $q_1, \ldots, q_d$, and $\omega$.

**Output.** $X_0, \ldots, X_{n-1}$, exactly in $\mathbb{Z}/p\mathbb{Z}$ and up to rounding over $\mathbb{C}$.

**Cost model.** Unit-cost ring operations. Additions (with subtractions) and multiplications by constants are counted separately; multiplications by the constant $1$ are not performed. Over $\mathbb{C}$, every constant of every module is real or purely imaginary, and so are their products, so each multiplication of complex data costs $2$ real multiplications, and each complex addition $2$ real additions.

## The algorithm

**Short modules.** For each $q$, with a root $w$ of order $q$, a module gives $A_q$ (from $q$ inputs to $m_q$ values by $a_q$ additions), constants $\mu_q \in R^{m_q}$, and $C_q$ (from $m_q$ values to $q$ outputs by $c_q$ additions), with $C_q\, \mathrm{diag}(\mu_q)\, A_q = (w^{jk})_{k, j}$. With $C(e) = (w^e + w^{-e})/2$ and $S(e) = (w^e - w^{-e})/2$:

| q | m_q | a_q + c_q additions | constants equal to 1 | constants |
|---|---|---|---|---|
| 2 | 2 | 2 + 0 | 2 | 1, 1 |
| 3 | 3 | 3 + 3 | 1 | 1, C(1) − 1, S(1) |
| 4 | 4 | 6 + 2 | 3 | 1, 1, 1, w |
| 5 | 6 | 8 + 9 | 1 | 1, (C(1) + C(2))/2 − 1, (C(1) − C(2))/2, S(2), S(1) − S(2), −S(1) − S(2) |
| 7 | 9 | 17 + 19 | 1 | 1, H/3 − 1, three values g, T/3, three values h (below) |
| 8 | 8 | 16 + 10 | 4 | 1, 1, 1, J, 1, J, c, cJ with J = w², c = w/(1 + J) |

For prime $q$, the inputs are paired as $t^\pm_j = x_j \pm x_{q-j}$, and the real and imaginary parts (the $C$ and $S$ sums) become a cyclic and a negacyclic convolution of length $(q-1)/2$ after Rader's reordering by a primitive root. For $q = 7$ these are convolutions of length $3$, each done with $4$ multiplications: the mean part ($H$ or $T$ is the sum of the kernel, $H = C(1) + C(3) + C(2)$, $T = S(1) - S(3) + S(2)$) and three products for the rest. The constant $1$ multiplies $X_0 = x_0 + \sum_j t^+_j$, and the next constant subtracts the $1$ again, Winograd's way of sharing $X_0$ with the other outputs. For $q = 8$, $c^2 = 1/2$, so $c = 1/\sqrt 2$ over $\mathbb{C}$.

**Nesting.**

```pseudo id=main
WFTA(x, (q_1, …, q_d), ω)            ▷ n = q_1 ⋯ q_d, pairwise coprime
L1  a[j_1, …, j_d] ← x_((j_1 n/q_1 + ⋯ + j_d n/q_d) mod n)           ▷ input index map
L2  for i ← 1 to d do  μ_i ← constants of module q_i with root ω^(n/q_i)
L3  for i ← 1 to d do  apply A_(q_i) along axis i                  ▷ axis i grows from q_i to m_i
L4  for every index (t_1, …, t_d) with some μ_i[t_i] ≠ 1 do  a[t] ← a[t] · μ_1[t_1] ⋯ μ_d[t_d]
L5  for i ← d down to 1 do  apply C_(q_i) along axis i             ▷ axis i shrinks from m_i to q_i
L6  return X with X_k = a[k mod q_1, …, k mod q_d]                ▷ output index map
```

The products $\mu_1[t_1] \cdots \mu_d[t_d]$ depend only on $n$ and are precomputed once. The order of the factors changes the number of additions but not the number of multiplications.

## Example

Over $\mathbb{Z}/7\mathbb{Z}$, $n = 6 = 2 \cdot 3$, $\omega = 3$ (order $6$), and $x = (3, 1, 4, 1, 5, 2)$. The roots of the modules are $\omega^3 = -1$ and $\omega^2 = 2$. For $q = 3$, $C(1) = (2 + 4)/2 = 3$ and $S(1) = (2 - 4)/2 = -1$, so $\mu_3 = (1, 2, 6)$, and $\mu_2 = (1, 1)$.

- Line L1, with $j = 3 j_1 + 2 j_2 \bmod 6$: rows $(x_0, x_2, x_4) = (3, 4, 5)$ and $(x_3, x_5, x_1) = (1, 2, 1)$.
- Line L3, axis 1 (length 2): sum and difference of the rows, $(4, 6, 6)$ and $(2, 2, 4)$. Axis 2 (length 3): each row $(y_0, y_1, y_2)$ becomes $(y_0 + y_1 + y_2,\ y_1 + y_2,\ y_1 - y_2)$, giving $(2, 5, 0)$ and $(1, 6, 5)$.
- Line L4: multiply by $(1, 2, 6)$ in both rows: $(2, 3, 0)$ and $(1, 5, 2)$; $4$ multiplications, since the first column is all ones.
- Line L5, axis 2: $(m_0, m_1, m_2) \mapsto (m_0,\ m_0 + m_1 + m_2,\ m_0 + m_1 - m_2)$: $(2, 5, 5)$ and $(1, 1, 4)$. Axis 1: $C_2$ is the identity.
- Line L6: $X_k$ is the entry in row $k \bmod 2$ and column $k \bmod 3$: $X = (2, 1, 5, 1, 5, 4)$.

This equals the direct sum $X_k = \sum_j x_j 3^{jk} \bmod 7$; the run and every intermediate table were checked by script. It used $4$ multiplications and $2 \cdot 3 + 2 \cdot 6 = 18$ additions.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) has three parts. First, the index maps: $j \mapsto (j_1, \ldots, j_d)$ with $j = \sum_i j_i n/q_i$ and $k \mapsto (k \bmod q_i)_i$ are bijections by the Chinese remainder theorem, and $\omega^{jk} = \prod_i \omega_{q_i}^{j_i k_i}$ with $\omega_{q_i} = \omega^{n/q_i}$ of order $q_i$, so $X$ is the $d$-dimensional DFT of the array $a$. Second, each module satisfies $C_q \,\mathrm{diag}(\mu_q)\, A_q = \mathrm{DFT}_q$; this is checked by expanding the formulas, using the pairing for prime $q$, the identities for short cyclic and negacyclic convolutions, and $c(1 + J) = w$ for $q = 8$. Third, applying a matrix along axis $i$ is multiplying by $I \otimes \cdots \otimes L \otimes \cdots \otimes I$, so lines L3 to L5 compute $(\bigotimes C_i)\, \mathrm{diag}(\bigotimes \mu_i)\, (\bigotimes A_i)$, which by the mixed-product rule equals $\bigotimes (C_i \mathrm{diag}(\mu_i) A_i) = \bigotimes \mathrm{DFT}_{q_i}$, the $d$-dimensional DFT.

## Complexity

**Multiplications.** $M - U$, where $M = \prod_i m_{q_i}$ and $U = \prod_i u_{q_i}$ is the number of index tuples whose constants are all $1$ ($u_q$ is the count in the table). Over $\mathbb{C}$, each is a complex number times a real or imaginary constant, $2$ real multiplications. The $m_q/q$ are at most $9/7$, so $M \le \frac{9}{7} \cdot \frac65\, n < 1.55\, n$.

**Additions.** With the post-additions in reverse order (line L5),
$$A = \sum_{i=1}^{d} (a_{q_i} + c_{q_i}) \prod_{j < i} m_{q_j} \prod_{j > i} q_j,$$
which for $d = 2$ is $q_2 A_1 + m_1 A_2$. Since $(a_q + c_q)/m_q \le 4$, $A \le 4 d M$.

| n | factors (order) | additions | multiplications (not by 1) |
|---|---|---|---|
| 6 | 2, 3 | 18 | 4 |
| 56 | 8, 7 | 470 | 68 |
| 60 | 3, 4, 5 | 444 | 69 |
| 120 | 8, 3, 5 | 1038 | 140 |
| 420 | 4, 3, 5, 7 | 5700 | 645 |
| 840 | 3, 8, 7, 5 | 12402 | 1292 |
| 840 | 5, 7, 8, 3 | 14844 | 1292 |

For $n = 840$ over $\mathbb{C}$ this is $2584$ real multiplications and $24804$ real additions; for comparison, a radix-2 FFT of length $1024$ does $\frac n2 \lg n = 5120$ complex twiddle multiplications before trivial ones are removed. The counts were checked exactly by the tests with an instrumented number type.

**Time and space.** The index maps and the passes over the array cost $O(d M)$ in all, and the array has at most $M$ entries.

**Error.** *Proved:* exact in $\mathbb{Z}/p\mathbb{Z}$ and in exact complex arithmetic. *Observed:* over $\mathbb{C}$ with doubles, the relative $\ell_2$ error against a direct sum with exactly reduced angles was about $9u$, $14u$ and $16u$ for $n = 56$, $105$ and $840$, and the round trip about $11u$, $18u$ and $20u$, with $u = 2^{-53}$. No bound is proved here.

## Properties

- **Few multiplications.** The count $M - U$ is close to $n$; the multiplications of all stages are merged into one.
- **More additions.** The nesting expands each axis from $q_i$ to $m_i$ before the other axes are processed, so additions grow by the factors $m_j/q_j$, and the order of the factors matters.
- **No twiddle factors.** Coprime factors need none, as in the prime-factor algorithm.
- **Not in place.** The middle array has $M > n$ entries, and the index maps permute the data.
- **Limited lengths.** Only products of coprime lengths with known modules.
- **Exact over finite fields.** The constants are built from $\omega$, $1/2$ and $1/3$, so the same code is exact in $\mathbb{Z}/p\mathbb{Z}$ whenever $\omega$ of order $n$ exists there.

## Variants and improvements

- **Prime-factor algorithm with Winograd modules.** Kolba and Parks (1977) used the same short modules one dimension at a time, with $\sum_i (n/q_i) m_{q_i}$ multiplications instead of $\prod_i m_{q_i}$, and fewer additions. Which is faster depends on the relative cost of the two operations.
- **Larger modules.** Modules for $9$ and $16$ extend the lengths to divisors of $5040$; prime powers need the convolution structure of the group of units modulo $q$.
- **Minimal multiplications.** Winograd (1977) proved that multiplying two polynomials modulo a polynomial $P$ of degree $N$ with $k$ irreducible factors over the field of constants needs $2N - k$ multiplications; for a cyclic convolution of length $N$ over $\mathbb{Q}$ this is $2N$ minus the number of divisors of $N$. The modules for $3$, $5$ and $7$ reach these counts for their convolutions of lengths $2$, $4$ and $6$ (in the real and imaginary halves). Auslander, Feig and Winograd (1984) determined the multiplicative complexity of the DFT for general lengths.
- **Real data.** Since every constant is real or imaginary, real inputs keep the real and imaginary parts separate through the middle stage, which halves the work.

## When to use it

It suited hardware in which multiplication was much more expensive than addition, such as early signal processors, and lengths like $240$, $504$, $840$ or $1008$ that are not powers of two. On modern processors, where a multiplication costs about as much as an addition and memory traffic dominates, the larger number of additions and the irregular data movement make power-of-two FFTs such as the [split-radix FFT](/split-radix-fft/) or a [mixed-radix FFT](/mixed-radix-fft/) usually faster. Its ideas live on in exact settings, where the count of multiplications by constants is the measure of interest, and in the theory of [bilinear complexity](/bilinear-complexity/).

## Pitfalls

- **Coprimality.** $8$ and $4$, or $3$ and $9$, cannot be nested; the index maps require pairwise coprime factors.
- **Index maps.** The input map $\sum_i j_i n/q_i$ and the output map $k \bmod q_i$ go together; swapping them gives a permuted transform. Other valid pairs of maps exist, but each module must then use the matching root $\omega^{e_i}$.
- **Order of the axes.** Post-additions in the same order as the pre-additions are still correct but can cost more, since the formula above then changes; and the factor orders for $n = 840$ differ by about $20$ percent in additions.
- **Constants for the inverse.** Recompute the module constants from $\omega^{-1}$; reusing the forward ones with conjugated data works only over $\mathbb{C}$.
- **Rounding of constants.** Over $\mathbb{C}$, compute constants such as $(C(1) - C(2))/2$ from accurately evaluated roots; an error in one constant enters every output that uses it.

## Implementations

The Python implementation in [impl/python/winograd_fourier_transform.py](impl/python/winograd_fourier_transform.py) contains the six modules as straight-line code and the nesting of the main block, over $\mathbb{C}$ or $\mathbb{Z}/p\mathbb{Z}$, with the inverse. The tests compare every module and every order of every coprime combination up to length $210$, and lengths $420$ and $840$, with the $O(n^2)$ DFT in exact arithmetic modulo $998244353$, $2521$, $97$ and $17$; they compare complex transforms with a tolerance scaled to $n$; they check the inverse, the exact counts of additions and multiplications, $n = 1$ and $2$, zeros, an impulse, a constant, invalid factors, and the worked example.

## History

Rader (1968) reduced a DFT of prime length to a cyclic convolution, and Good (1958) gave the index map that turns a DFT with coprime factors into a multidimensional one. Winograd (1976) announced new DFT algorithms that, for $n$ from a few tens to a few thousands, use substantially fewer multiplications than the best ones known and about the same number of additions. The full paper (1978) built them from his convolution algorithms, which rest on his theorem on the multiplicative complexity of products modulo a polynomial (1977), and nested the short modules. Silverman (1977) published a guide to programming the WFTA with running times, and Kolba and Parks (1977) compared it with a prime-factor algorithm using the same convolutions. Auslander, Feig and Winograd (1984) determined the multiplicative complexity of the DFT.

## References
