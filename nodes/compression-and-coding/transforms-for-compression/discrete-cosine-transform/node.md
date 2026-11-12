---
tag: C2X14P
kind: algorithm
slug: discrete-cosine-transform
name: Discrete cosine transform
aliases:
- DCT
- DCT-II
area: compression-and-coding/transforms-for-compression
level: core
summary: Real orthogonal transform that compacts smooth signal energy into low-frequency coefficients.
model: real-ram
complexity:
  vars: {N: the block length (a power of two for the fast algorithm)}
  time: {worst: Θ(N log N), average: Θ(N log N), best: Θ(N log N)}
  space: {extra: Θ(N)}
properties: {deterministic: true, recursive: true, in_place: false}
history:
  year: 1974
  people: [Nasir Ahmed, T. Natarajan, K. R. Rao]
  note: Ahmed, Natarajan and Rao defined the DCT in 1974 and showed that it is close to the Karhunen-Loève transform of a first-order Markov source.
prereqs: [orthogonal-transform, discrete-fourier-transform]
see_also: [fast-dct, discrete-sine-transform, karhunen-loeve-transform, modified-discrete-cosine-transform, jpeg-compression, energy-compaction, zigzag-scan, transform-coding]
sources:
  - paper: doi:10.1109/T-C.1974.223784
    title: Nasir Ahmed, T. Natarajan and K. R. Rao, Discrete cosine transform, IEEE Transactions on Computers C-23(1), 1974
    locator: pp. 90 to 93 (the definition, the computation by a DFT of length 2N, and the comparison with the KLT of a first-order Markov source)
  - paper: doi:10.1109/TASSP.1984.1164443
    title: Byeong Gi Lee, A new algorithm to compute the discrete cosine transform, IEEE Transactions on Acoustics, Speech, and Signal Processing 32(6), 1984
    locator: pp. 1243 to 1245 (the recursive split into two half-length DCTs)
  - paper: doi:10.1109/TCOM.1977.1093941
    title: Wen-Hsiung Chen, C. Harrison Smith and S. C. Fralick, A fast computational algorithm for the discrete cosine transform, IEEE Transactions on Communications 25(9), 1977
    locator: pp. 1004 to 1009 (a sparse matrix factorization of the DCT)
  - paper: doi:10.1109/ICASSP.1989.266596
    title: Christoph Loeffler, Adriaan Ligtenberg and George S. Moschytz, Practical fast 1-D DCT algorithms with 11 multiplications, Proceedings of ICASSP 1989, vol. 2
    locator: pp. 988 to 991 (8-point DCT with 11 multiplications and 29 additions)
  - paper: "Yukihiro Arai, Takeshi Agui and Masayuki Nakajima, A fast DCT-SQ scheme for images, Transactions of the IEICE E71(11), 1988, pp. 1095 to 1097"
    title: Yukihiro Arai, Takeshi Agui and Masayuki Nakajima, A fast DCT-SQ scheme for images
    locator: the scaled 8-point DCT with 5 multiplications, the output scale folded into the quantizer
  - url: https://www.w3.org/Graphics/JPEG/itu-t81.pdf
    title: ITU-T Recommendation T.81 (09/92), Information technology, Digital compression and coding of continuous-tone still images, Requirements and guidelines
    locator: Annex A.3.3, FDCT and IDCT (the 8 x 8 forward and inverse transforms)
  - paper: doi:10.1109/78.295213
    title: Stephen A. Martucci, Symmetric convolution and the discrete sine and cosine transforms, IEEE Transactions on Signal Processing 42(5), 1994
    locator: pp. 1038 to 1051 (the 16 discrete trigonometric transforms and the symmetric extensions they imply)
  - paper: "Zhongde Wang, Fast algorithms for the discrete W transform and for the discrete Fourier transform, IEEE Transactions on Acoustics, Speech, and Signal Processing 32(4), 1984, pp. 803 to 816"
    title: Zhongde Wang, Fast algorithms for the discrete W transform and for the discrete Fourier transform
    locator: the four types DCT-I to DCT-IV and their sparse factorizations
  - paper: doi:10.1137/S0036144598336745
    title: Gilbert Strang, The discrete cosine transform, SIAM Review 41(1), 1999
    locator: pp. 135 to 147 (the DCT bases as eigenvectors of second-difference matrices with different boundary conditions)
  - paper: doi:10.1049/ip-f-1.1981.0061
    title: R. J. Clarke, Relation between the Karhunen-Loève and cosine transforms, IEE Proceedings F 128(6), 1981
    locator: pp. 359 to 360 (the KLT of a first-order Markov source tends to the DCT-II as the correlation goes to 1)
---

The discrete cosine transform (DCT) maps a block of $N$ real samples to $N$ real coefficients, each the inner product of the block with a sampled cosine of a different frequency. The type used in compression is the DCT-II, and with the orthonormal scaling it is an [orthogonal transform](/orthogonal-transform/) whose inverse is the DCT-III. For smooth signals it gives an [energy compaction](/energy-compaction/) very close to that of the optimal [Karhunen-Loève transform](/karhunen-loeve-transform/), but it is fixed and fast: $\Theta(N \log N)$ operations by Lee's recursive split. The 8 x 8 two-dimensional DCT-II is the transform of [JPEG compression](/jpeg-compression/).

## In plain words

Take a row of eight pixel values. Ask how much the row looks like a flat line, how much like one slow half-wave of a cosine, how much like a slightly faster wave, and so on up to the fastest wave that eight samples can show. The eight answers are the DCT of the row.

A smooth row looks mostly like the flat line and a little like the slow waves. So the first answer is large and the later answers are small. A coder keeps the large answers with care and rounds the small ones, often to zero. The decoder adds the waves back together and gets a row close to the original. For a square block of pixels, the coder does this for each row and then for each column.

## The problem

**Input.** A real vector $x = (x[0], \dots, x[N-1])$, $N \ge 1$. In image coding it is a row of a block of pixels after the level shift, so with 8-bit samples the values are in $[-128, 127]$.

**Output.** The orthonormal DCT-II coefficients

$$X[k] = a_k \sum_{n=0}^{N-1} x[n] \cos\frac{\pi (2n+1) k}{2N}, \qquad k = 0, \dots, N-1, \qquad a_0 = \sqrt{\tfrac1N},\; a_k = \sqrt{\tfrac2N} \ (k \ge 1).$$

The inverse (the orthonormal DCT-III) is

$$x[n] = \sum_{k=0}^{N-1} a_k X[k] \cos\frac{\pi (2n+1) k}{2N}, \qquad n = 0, \dots, N-1.$$

In matrix form $X = Cx$ with $C_{kn} = a_k \cos(\pi(2n+1)k/(2N))$, and $C^{\mathsf T} C = I$. The two-dimensional DCT of an $N \times N$ block $B$ is $C B C^{\mathsf T}$. The coefficient $X[0] = \sqrt N \cdot \overline{x}$ is the *DC coefficient*; the others are the *AC coefficients*. Other books use other scale factors (for example no $a_k$ at all, or a factor 2); the scale changes the numbers but not the shape of the transform.

**Model.** The cost is counted in the [real RAM](/real-ram/): one step for each real addition or multiplication, and the cosines are constants that a program computes once.

## The algorithm

The definition gives a direct algorithm in $\Theta(N^2)$ operations. DCT-2D applies it to the rows and then to the columns.

```pseudo id=main
DCT(x)                                    ▷ x[0 .. N − 1]; orthonormal DCT-II
L1  for k ← 0 to N − 1 do
L2      a ← √(1/N) if k = 0, else √(2/N)
L3      X[k] ← a · Σ_{n=0}^{N−1} x[n] · cos(π(2n + 1)k / (2N))
L4  return X

IDCT(X)                                   ▷ orthonormal DCT-III, the inverse of DCT
L5  for n ← 0 to N − 1 do
L6      x[n] ← Σ_{k=0}^{N−1} a_k · X[k] · cos(π(2n + 1)k / (2N))
L7  return x

DCT-2D(B)                                 ▷ B is an N × N block
L8  R ← the DCT of each row of B
L9  S ← the DCT of each column of R
L10 return S
```

The fast algorithm is the split of B. G. Lee (1984). It computes the unnormalized sums $\hat X[k] = \sum_n x[n] \cos(\pi(2n+1)k/(2N))$ for $N$ a power of two; then $X[k] = a_k \hat X[k]$.

```pseudo id=fast
LEE(x)                                    ▷ N = |x| is a power of two
F1  if N = 1 then return (x[0])
F2  for i ← 0 to N/2 − 1 do
F3      u[i] ← x[i] + x[N − 1 − i]
F4      v[i] ← (x[i] − x[N − 1 − i]) / (2 cos(π(2i + 1) / (2N)))
F5  U ← LEE(u);  V ← LEE(v);  V[N/2] ← 0
F6  for m ← 0 to N/2 − 1 do
F7      X̂[2m] ← U[m]
F8      X̂[2m + 1] ← V[m] + V[m + 1]
F9  return X̂
```

The even outputs are a DCT of half the length of the folded sums $u$. The odd outputs come from a half-length DCT of the scaled differences $v$, followed by one addition each. The inverse runs the same steps backward: $V[m] = \hat X[2m+1] - V[m+1]$ from $m = N/2 - 1$ down to 0, two half-length inverses, then $x[i] = (u[i] + d_i)/2$ and $x[N-1-i] = (u[i] - d_i)/2$ with $d_i = 2\cos(\pi(2i+1)/(2N))\, v[i]$.

**A DCT from a DFT.** The DCT-II is also a [discrete Fourier transform](/discrete-fourier-transform/) in disguise. Extend $x$ to length $2N$ by its mirror image, $y = (x[0], \dots, x[N-1], x[N-1], \dots, x[0])$, and let $Y$ be the DFT of $y$. Then

$$X[k] = \tfrac12\, a_k\, \operatorname{Re}\!\left(e^{-i\pi k/(2N)}\, Y[k]\right).$$

This is how Ahmed, Natarajan and Rao computed the DCT in 1974. Makhoul (1980) reduced it further to one DFT of length $N$; that method is on the page [fast DCT](/fast-dct/).

## Example

Take the smooth row $x = (10, 11, 12, 14, 15, 15, 14, 12)$, $N = 8$. Its energy is $\|x\|^2 = 1351$.

**Lee's split, first level.** The folded sums and scaled differences are

- $u = (10 + 12, 11 + 14, 12 + 15, 14 + 15) = (22, 25, 27, 29)$,
- $v = (-2, -3, -3, -1)$ divided by $2\cos(\pi/16), 2\cos(3\pi/16), 2\cos(5\pi/16), 2\cos(7\pi/16)$, that is $v = (-1.0196, -1.8040, -2.6999, -2.5629)$.

The half-length transforms are $U = (103, -7.2325, -0.7071, -0.8310)$ and $V = (-8.0865, 1.7687, 0.6516, -0.2371)$, with $V[4] = 0$. Lines F7 and F8 give

$$\hat X = (103,\; -8.0865 + 1.7687,\; -7.2325,\; 1.7687 + 0.6516,\; -0.7071,\; 0.6516 - 0.2371,\; -0.8310,\; -0.2371)$$

$$= (103, -6.3178, -7.2325, 2.4203, -0.7071, 0.4145, -0.8310, -0.2371).$$

**Scaling.** With $a_0 = 1/\sqrt 8 = 0.35355$ and $a_k = 1/2$ for $k \ge 1$,

$$X = (36.4160, -3.1589, -3.6163, 1.2101, -0.3536, 0.2072, -0.4155, -0.1185).$$

The energy of $X$ is again 1351. The DC coefficient alone carries $36.416^2 / 1351 = 98.16$ percent of it.

**Truncation.** Keep $X[0], X[1], X[2]$ and set the rest to zero. The IDCT gives $(9.655, 10.870, 12.689, 14.237, 14.854, 14.444, 13.496, 12.754)$. The squared error is $1.819$, the energy of the five dropped coefficients, because the transform is orthogonal.

**The AAN scaled transform** of the same row returns $(103, -12.3928, -13.364, 4.0247, -1.0, 0.4605, -0.636, -0.0925)$. Output $k$ is $\hat X[k]$ times $s_0 = 1$ or $s_k = 2\cos(k\pi/16)$ for $k \ge 1$: for example $-6.3178 \cdot 2\cos(\pi/16) = -12.3928$.

## Correctness

The full proofs are in [the correctness proof](proofs/correctness.md). In short:

1. **Orthonormality.** For $0 \le j, k < N$, $\sum_n \cos\frac{\pi(2n+1)j}{2N} \cos\frac{\pi(2n+1)k}{2N}$ is $N$ if $j = k = 0$, $N/2$ if $j = k \ne 0$, and 0 otherwise. The proof writes the product as a sum of two cosines and uses the sum $\sum_{n=0}^{N-1} \cos\frac{\pi(2n+1)p}{2N} = 0$ for $0 < |p| < 2N$, a geometric sum of roots of unity. With the factors $a_k$ the rows of $C$ are orthonormal, so $C^{\mathsf T}C = I$ and IDCT inverts DCT.
2. **Lee's split.** Pairing $n$ with $N-1-n$ gives $\hat X[2m] = \sum_{i<N/2} u[i] \cos\frac{\pi(2i+1)m}{N}$, a DCT of length $N/2$ of $u$. For the odd outputs, $2\cos\alpha\cos\beta = \cos(\alpha+\beta) + \cos(\alpha-\beta)$ with $\alpha = \frac{\pi(2i+1)(2m+1)}{2N}$ and $\beta = \frac{\pi(2i+1)}{2N}$ gives $\hat X[2m+1] = V[m] + V[m+1]$, and $V[N/2] = 0$ because $\cos\frac{\pi(2i+1)}{2} = 0$. The divisor at line F4 is never zero, because $0 < \frac{\pi(2i+1)}{2N} < \frac{\pi}{2}$.
3. **The 2D transform.** $C B C^{\mathsf T}$ is the row transform followed by the column transform, and its inverse is $C^{\mathsf T} S C$.

## Complexity

**Direct.** DCT and IDCT take $N^2$ multiplications and $N(N-1)$ additions, with the $N^2$ cosines in a table. The 2D transform of an $N \times N$ block takes $2N$ one-dimensional transforms, so $2N^3$ multiplications directly.

**Lee's algorithm.** Let $M(N)$ and $A(N)$ be the multiplications and additions for $N$ a power of two. Lines F3 and F4 cost $N$ additions and $N/2$ multiplications (the reciprocals $1/(2\cos\cdot)$ are constants), and line F8 costs $N/2 - 1$ additions, since $V[N/2] = 0$. So

$$M(N) = 2M(N/2) + \tfrac{N}{2}, \qquad A(N) = 2A(N/2) + \tfrac{3N}{2} - 1, \qquad M(1) = A(1) = 0,$$

which solve to $M(N) = \frac N2 \log_2 N$ and $A(N) = \frac{3N}{2}\log_2 N - N + 1$. For $N = 8$ this is 12 multiplications and 29 additions, plus 8 multiplications for the factors $a_k$ (often folded into the quantizer). The recursion has depth $\log_2 N$ and uses $\Theta(N)$ extra space at each level, $\Theta(N)$ in total if the buffers are reused.

**Known counts for $N = 8$.**

| algorithm | multiplications | additions |
|---|---|---|
| direct definition | 64 | 56 |
| Chen, Smith and Fralick (1977) | 16 | 26 |
| Lee (1984), unscaled output | 12 | 29 |
| Loeffler, Ligtenberg and Moschytz (1989) | 11 | 29 |
| Arai, Agui and Nakajima (1988), scaled output | 5 | 29 |

The AAN algorithm gets 5 multiplications because it returns each output times a known factor $s_k$; a JPEG coder divides the quantization table by these factors once, so the 8 scale multiplications cost nothing per block. Loeffler, Ligtenberg and Moschytz state that 11 multiplications is the lower bound for an 8-point DCT with an unscaled output.

A 2D 8 x 8 DCT by rows and columns with Loeffler's algorithm costs $16 \cdot 11 = 176$ multiplications.

## Properties

- **Orthogonal.** With the factors $a_k$, the DCT keeps energy and squared error (see [orthogonal transform](/orthogonal-transform/)).
- **Real.** Real input gives real output, unlike the DFT, which gives complex coefficients with a conjugate symmetry.
- **Symmetric extension.** The DCT-II of $x$ is the DFT of the even extension of $x$ of length $2N$ that repeats the end samples. That extension has no jump at the block boundary, so the coefficients of a smooth block decay fast. The DFT treats $x$ as one period of a periodic signal; if $x[N-1] \ne x[0]$ that signal has a jump, and its DFT coefficients decay slowly.
- **Close to the KLT of an AR(1) source.** For the covariance $R_{ij} = \rho^{|i-j|}$, $(1-\rho^2) R^{-1}$ is tridiagonal, and as $\rho \to 1$ it tends to the second-difference matrix whose eigenvectors are exactly the DCT-II basis vectors (Strang 1999). So the KLT tends to the DCT-II (Clarke 1981); the proof is in the correctness file. For $N = 8$ the largest value of $1 - |\langle c_k, v_k \rangle|$ between a DCT basis vector $c_k$ and the matching KLT eigenvector $v_k$ is 0.0312 at $\rho = 0.5$, 0.00171 at $\rho = 0.9$, $4.44 \cdot 10^{-4}$ at $\rho = 0.95$, $1.83 \cdot 10^{-5}$ at $\rho = 0.99$ and $1.84 \cdot 10^{-7}$ at $\rho = 0.999$. The coding gain of the DCT is 6.276 dB at $\rho = 0.9$, against 6.311 dB for the KLT.
- **Separable.** The 2D DCT is the product of 1D transforms on rows and columns.
- **Not shift invariant.** A shift of the signal by one sample changes the coefficients in a complex way, not by a phase factor as with the DFT.

## Variants and improvements

- **The other types.** Wang (1984) named four types of DCT, and Martucci (1994) gave the full family of eight DCTs and eight DSTs, one for each pair of symmetries at the two ends of the block. With the unnormalized forms:
  - DCT-I: $\sum_{n=0}^{N-1} x[n] \cos\frac{\pi nk}{N-1}$ with the end terms halved (whole-sample symmetry at both ends);
  - DCT-II: $\sum_n x[n] \cos\frac{\pi(2n+1)k}{2N}$, this page;
  - DCT-III: $\sum_k X[k] \cos\frac{\pi(2n+1)k}{2N}$ with the $k = 0$ term halved, the inverse of the DCT-II up to scale;
  - DCT-IV: $\sum_n x[n] \cos\frac{\pi(2n+1)(2k+1)}{4N}$, which is its own inverse up to the factor $2/N$ and is the core of the [modified discrete cosine transform](/modified-discrete-cosine-transform/).
  The [discrete sine transform](/discrete-sine-transform/) is the sine family.
- **Makhoul's algorithm.** One complex FFT of length $N/2$ (or a real FFT of length $N$) and $O(N)$ extra operations. See [fast DCT](/fast-dct/).
- **Scaled DCTs.** AAN and its relatives return the outputs times fixed factors and fold the factors into quantization. The IJG libjpeg float and fast integer DCTs use this method.
- **Integer approximations.** H.264 and HEVC use integer matrices that approximate the DCT, so that the encoder and the decoder compute the same inverse exactly.
- **2D algorithms.** Direct 2D factorizations of the 8 x 8 DCT use fewer multiplications than 16 one-dimensional transforms.

## When to use it

Use the DCT-II for block transform coding of smooth, highly correlated data: image blocks (JPEG, MPEG), video residuals, and the cepstrum of speech features. It is the right choice when the source is close to a first-order Markov process with high correlation, when the transform must be fixed (no side information), and when it must be fast. If the statistics of the source are known and far from AR(1), the [Karhunen-Loève transform](/karhunen-loeve-transform/) does better but costs $O(N^2)$ per block and must be sent or agreed on. For audio, where block edges cause audible clicks, use the lapped [modified discrete cosine transform](/modified-discrete-cosine-transform/). For images at low bit rates, where the 8 x 8 blocks of JPEG become visible, wavelet coders such as [JPEG 2000](/jpeg-2000/) avoid blocks.

## Pitfalls

- **Scale conventions.** Libraries differ. SciPy's `dct` with no `norm` argument returns $2\hat X[k]$; JPEG's formula in T.81 A.3.3 has the factor $\frac14 C_u C_v$ with $C_0 = 1/\sqrt2$, which for $N = 8$ equals the orthonormal 2D DCT. Mixing conventions gives wrong quantizer steps by a factor of $\sqrt 2$ or 2.
- **Forgetting the level shift.** JPEG subtracts 128 from 8-bit samples before the FDCT (T.81 A.3.1). Without it the DC coefficient is $8 \cdot 128 = 1024$ larger for each block.
- **Lee's divisors.** Line F4 divides by $2\cos(\pi(2i+1)/(2N))$, which is close to $\pi/N$ for $i = N/2 - 1$. For large $N$ this amplifies rounding errors in fixed-point arithmetic. In double precision the errors stay near $10^{-14}$ for $N = 1024$ on random input, but fixed-point coders prefer factorizations with bounded constants, such as Loeffler's.
- **Block edges.** Coarse quantization of each block on its own leaves visible steps at the block boundaries (blocking artifacts). Deblocking filters or lapped transforms address this.
- **Not the KLT.** The DCT is near optimal only for smooth, highly correlated sources. On white noise it gives no gain, and on blocks with sharp edges it spreads energy over many coefficients (ringing after quantization).

## Implementations

## History

Nasir Ahmed, T. Natarajan and K. R. Rao published the DCT in 1974. They computed it by a DFT of length $2N$ and showed that for a first-order Markov source its performance is close to that of the Karhunen-Loève transform. Chen, Smith and Fralick gave a fast factorization in 1977, and Makhoul reduced the DCT to an FFT of the same length in 1980. Lee gave the recursive split on this page in 1984, the same year that Wang classified the types of the DCT. Arai, Agui and Nakajima published the 5-multiplication scaled DCT in 1988, and Loeffler, Ligtenberg and Moschytz the 11-multiplication algorithm in 1989. Clarke showed in 1981 that the KLT of a first-order Markov source tends to the DCT-II as the correlation tends to 1. The 8 x 8 DCT became the transform of the JPEG standard, ITU-T T.81 (1992).

## References
