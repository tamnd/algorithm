---
tag: PVNJ5C
kind: algorithm
slug: modified-discrete-cosine-transform
name: Modified discrete cosine transform
aliases:
- MDCT
area: compression-and-coding/transforms-for-compression
level: advanced
summary: Lapped, critically sampled DCT used in MP3, AAC and Vorbis audio coding.
model: real-ram
complexity:
  vars: {N: the number of coefficients per frame (a frame has 2N samples), L: the signal length}
  time: {worst: "Θ((L + N) log N)", average: "Θ((L + N) log N)", best: "Θ((L + N) log N)"}
  space: {extra: Θ(N)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1986
  people: [John P. Princen, Alan B. Bradley, A. W. Johnson]
  note: Princen and Bradley introduced time domain aliasing cancellation in 1986; Princen, Johnson and Bradley gave the oddly stacked form now called the MDCT in 1987.
prereqs: [discrete-cosine-transform, filter-bank, perfect-reconstruction]
see_also: [fast-fourier-transform, window-functions, aliasing, subband-coding, transform-coding, lossy-compression, energy-compaction, fast-dct]
sources:
  - paper: doi:10.1109/TASSP.1986.1164954
    title: John P. Princen and Alan B. Bradley, Analysis/synthesis filter bank design based on time domain aliasing cancellation, IEEE Transactions on Acoustics, Speech, and Signal Processing 34(5), 1986
    locator: pp. 1153 to 1161 (critically sampled overlapping frames whose time domain aliasing cancels in the overlap-add, and the window condition)
  - paper: doi:10.1109/ICASSP.1987.1169405
    title: John P. Princen, A. W. Johnson and Alan B. Bradley, Subband/transform coding using filter bank designs based on time domain aliasing cancellation, Proceedings of ICASSP 1987
    locator: pp. 2161 to 2164 (the oddly stacked TDAC filter bank, the transform now called the MDCT)
  - paper: doi:10.1109/29.56057
    title: Henrique S. Malvar, Lapped transforms for efficient transform/subband coding, IEEE Transactions on Acoustics, Speech, and Signal Processing 38(6), 1990
    locator: pp. 969 to 978 (the modulated lapped transform, the same transform with the sine window, and its fast algorithm)
  - book: isbn:9780890064672
    title: Henrique S. Malvar, Signal Processing with Lapped Transforms, Artech House, 1992
    locator: Chapter 5, Modulated Lapped Transforms (the MLT and its extensions)
  - paper: doi:10.1109/ICASSP.1991.150853
    title: Pierre Duhamel, Yannick Mahieux and Jean-Pierre Petit, A fast algorithm for the implementation of filter banks based on time domain aliasing cancellation, Proceedings of ICASSP 1991, vol. 3
    locator: pp. 2209 to 2212 (the MDCT by one complex FFT of a quarter of the frame length)
  - paper: doi:10.1007/978-1-4615-0327-9
    title: Marina Bosi and Richard E. Goldberg, Introduction to Digital Audio Coding and Standards, Springer, 2003
    locator: Chapter 5, Time to Frequency Mapping Part II, The MDCT, pp. 103 to 147; Chapters 11 (MPEG-1 Audio), 13 (MPEG-2 AAC) and 14 (Dolby AC-3) for the uses
  - url: https://www.rfc-editor.org/rfc/rfc6716
    title: J.-M. Valin, K. Vos and T. Terriberry, Definition of the Opus Audio Codec, RFC 6716, 2012
    locator: Section 4.3, CELT Decoder (the inverse MDCT and the low-overlap window of the CELT layer)
  - url: https://xiph.org/vorbis/doc/Vorbis_I_spec.html
    title: Xiph.Org Foundation, Vorbis I specification
    locator: the window shape and the inverse MDCT of the audio packet decode (two block sizes, powers of two from 64 to 8192)
---

The modified discrete cosine transform (MDCT) maps a frame of $2N$ samples to $N$ coefficients. Consecutive frames overlap by half, so the signal still gives one coefficient per sample: the transform is critically sampled. One frame alone cannot be inverted, because the inverse returns the frame plus a mirrored copy of each half, the time domain aliasing. With a window that meets the Princen-Bradley condition, the aliasing of each frame cancels against that of its neighbor in the overlap-add, and the signal comes back exactly. The MDCT is a [filter bank](/filter-bank/) with [perfect reconstruction](/perfect-reconstruction/), it is an orthogonal transform of the whole signal, and it is computed in $\Theta(N \log N)$ per frame through a DCT-IV and an FFT. MP3, AAC, Vorbis, AC-3 and Opus code audio with it.

## In plain words

Audio coders work on short pieces of sound, but if each piece is coded on its own, the edges between pieces click. The MDCT lets the pieces overlap by half, and fades each piece in and out with a smooth window, so there are no hard edges.

Overlap usually costs extra numbers, but the MDCT returns only as many numbers as there are new samples. The price is that each piece, rebuilt alone, comes back with a mirrored copy of itself mixed in. When the window has the right shape, the mirrored copy in one piece is the exact negative of the one in the next piece, and adding the overlapping halves cancels it. The sound comes back exactly, and the coder still gets the energy compaction of a cosine transform.

## The problem

**Input.** A real signal $s$ of length $L$, a hop size $N$, and a window $w$ of length $2N$.

**Output.** Frames of $N$ coefficients each, and a synthesis that maps the frames back to $s$.

**The transform.** For a frame $x$ of $2N$ samples, the windowed orthonormal MDCT and its inverse (IMDCT) are

$$X[k] = \sqrt{\tfrac{2}{N}} \sum_{n=0}^{2N-1} w[n]\, x[n] \cos\!\Big(\frac{\pi}{N}\big(n + \tfrac12 + \tfrac N2\big)\big(k + \tfrac12\big)\Big), \qquad 0 \le k < N,$$

$$y[n] = \sqrt{\tfrac{2}{N}}\, w[n] \sum_{k=0}^{N-1} X[k] \cos\!\Big(\frac{\pi}{N}\big(n + \tfrac12 + \tfrac N2\big)\big(k + \tfrac12\big)\Big), \qquad 0 \le n < 2N .$$

**The window conditions.** The window is symmetric, $w[2N-1-n] = w[n]$, and meets the Princen-Bradley condition

$$w[n]^2 + w[n+N]^2 = 1, \qquad 0 \le n < N .$$

Two common windows meet both. The sine window is $w[n] = \sin\big(\pi(n + \frac12)/(2N)\big)$. The Kaiser-Bessel-derived (KBD) window with parameter $\alpha$ takes a Kaiser window $v$ of length $N+1$ and sets $w[n] = \sqrt{\sum_{j \le n} v[j] / \sum_{j \le N} v[j]}$ for $n < N$, then mirrors it.

**MDCT and DCT.** The [DCT](/discrete-cosine-transform/) maps $N$ samples to $N$ coefficients and is invertible block by block. The MDCT maps $2N$ samples to $N$ coefficients; it is invertible only for the whole sequence of overlapping frames. Its kernel is that of the DCT-IV with a shift of $N/2$ in time, and the fast algorithm below folds each frame into a DCT-IV.

## The algorithm

```pseudo id=main
MDCT(x, w)                                ▷ one frame, x[0 .. 2N − 1]
L1  for k ← 0 to N − 1 do
L2      X[k] ← √(2/N) Σ_{n=0}^{2N−1} w[n] x[n] cos(π/N · (n + 1/2 + N/2)(k + 1/2))
    return X

IMDCT(X, w)                               ▷ 2N samples with time domain aliasing
L3  for n ← 0 to 2N − 1 do
L4      y[n] ← √(2/N) w[n] Σ_{k=0}^{N−1} X[k] cos(π/N · (n + 1/2 + N/2)(k + 1/2))
    return y

ANALYSIS(s, N, w)
    p ← N zeros, then s, then zeros up to a multiple of N, then N zeros
L5  for t ← 0, 1, ... while tN + 2N ≤ |p| do
L6      F[t] ← MDCT(p[tN .. tN + 2N − 1], w)
    return F

SYNTHESIS(F, N, w, L)                     ▷ overlap-add with hop N
    out ← zeros
L7  for each frame index t do
L8      y ← IMDCT(F[t], w)
L9      out[tN + n] ← out[tN + n] + y[n] for 0 ≤ n < 2N
L10 return out[N .. N + L − 1]
```

The padding puts every sample of $s$ in exactly two frames: block $j$ of $N$ samples is the second half of frame $j-1$ and the first half of frame $j$.

**The fast algorithm.** Let $N$ be even, $h = N/2$, and $z[n] = w[n]\,x[n]$. Fold the $2N$ values of $z$ into $N$ values:

$$u[j] = -z[3h-1-j] - z[3h+j] \quad (0 \le j < h), \qquad u[j] = z[j-h] - z[3h-1-j] \quad (h \le j < N).$$

Then $X = \sqrt{2/N}\, C_4 u$, where $C_4$ is the unnormalized DCT-IV, $(C_4 u)[k] = \sum_{j<N} u[j] \cos\big(\frac{\pi}{N}(j + \frac12)(k + \frac12)\big)$. For $N$ a power of two, compute $C_4 u$ by one complex [FFT](/fast-fourier-transform/) of length $N/2$: let

$$c[n] = \big(u[2n] + i\, u[N-1-2n]\big)\, e^{-i\pi(4n+1)/(4N)}, \qquad D[k] = e^{-i\pi k/N} \sum_{n<N/2} c[n]\, e^{-2\pi i nk/(N/2)},$$

then $(C_4 u)[2k] = \operatorname{Re} D[k]$ and $(C_4 u)[N-1-2k] = -\operatorname{Im} D[k]$ for $0 \le k < N/2$. The IMDCT computes $v = C_4 X$ in the same way, because $C_4^2 = \frac N2 I$, and unfolds: $y[n] = \sqrt{2/N}\, w[n]\, v'[n + h]$, where $v'[m] = v[m]$ for $m < N$, $v'[m] = -v[2N-1-m]$ for $N \le m < 2N$, and $v'[m] = -v[m-2N]$ for $m \ge 2N$. This is the method of Duhamel, Mahieux and Petit (1991).

## Example

**Aliasing of one frame.** Take $N = 4$, the rectangular window $w = 1$, and $x = (1,2,3,4,4,3,2,1)$. The MDCT is $(-7.7238, 0.2235, 0.5016, 0.2042)$, and the IMDCT of it is

$$(-3, -1, 1, 3, 5, 5, 5, 5).$$

Write $x = (a, b)$ with halves $a = (1,2,3,4)$ and $b = (4,3,2,1)$, and let $J$ reverse a block. The output is $(a - Ja,\ b + Jb)$: the first half carries an odd mirror image and the second half an even mirror image. This is the time domain aliasing.

**Cancellation with the sine window.** Take $N = 4$ and the sine window

$$w = (0.1951, 0.5556, 0.8315, 0.9808, 0.9808, 0.8315, 0.5556, 0.1951),$$

which meets $w[n]^2 + w[n+4]^2 = 1$. The signal $s = (3,1,4,1,5,9,2,6)$ is padded to $(0,0,0,0, 3,1,4,1, 5,9,2,6, 0,0,0,0)$, which gives three frames:

| frame | samples | coefficients |
|---|---|---|
| 0 | $(0,0,0,0,3,1,4,1)$ | $(-3.9625, -1.3626, 0.9762, 0.8113)$ |
| 1 | $(3,1,4,1,5,9,2,6)$ | $(-10.0693, -2.8524, -0.8468, 2.8895)$ |
| 2 | $(5,9,2,6,0,0,0,0)$ | $(-1.4682, 2.0937, 1.2848, -5.2007)$ |

The IMDCT of frame 0 ends with $(3.0772, 2.5391, 1.6966, 0.6121)$ and the IMDCT of frame 1 starts with $(-0.0772, -1.5391, 2.3034, 0.3879)$. Neither is the block $(3,1,4,1)$, but their sum is. In the same way the end of frame 1, $(5.9577, 7.1460, 4.7748, 1.1851)$, plus the start of frame 2, $(-0.9577, 1.8540, -2.7748, 4.8149)$, is $(5,9,2,6)$. The twelve coefficients have the energy 173, the same as $s$.

**A window that fails.** With the rectangular window, $w[n]^2 + w[n+N]^2 = 2$. The aliasing still cancels, but the overlap-add returns $2s = (6,2,8,2,10,18,4,12)$. Scaling the window to $1/\sqrt2$ fixes the gain, so the PR condition holds, but such a window has poor frequency selectivity. A window that is not symmetric and does not meet the condition leaves aliasing in the output.

## Correctness

The full proofs are in [the correctness proof](proofs/correctness.md). In short:

1. **The aliasing term.** Let $C$ be the $N \times 2N$ matrix of the MDCT cosines. Using $\sum_{k<N} \cos\frac{\pi p(2k+1)}{2N} = 0$ unless $2N \mid p$, one gets $\frac2N C^{\mathsf T} C = I + \begin{pmatrix} -J & 0 \\ 0 & J \end{pmatrix}$. This is the formula $(a - Ja, b + Jb)$ of the example.
2. **Cancellation (TDAC).** Let $W_1$ and $W_2$ be the diagonal matrices of the two halves of the window. Block $B$ gets $W_2^2 B + W_2 J W_2 B$ from the frame before it and $W_1^2 B - W_1 J W_1 B$ from the frame after it. The sum is $(W_1^2 + W_2^2)B + (W_2 J W_2 - W_1 J W_1)B$. The Princen-Bradley condition makes the first matrix $I$, and the symmetry $w[N + i] = w[N-1-i]$ makes $W_2 J W_2 = W_1 J W_1$, so the sum is $B$.
3. **Energy.** The same two identities give $\sum_t \|F[t]\|^2 = \|s\|^2$: the analysis is an isometry, and on an infinite signal it is an orthogonal transform.
4. **The fast algorithm.** The kernel $\phi_k(m) = \cos(\frac{\pi}{N}(m + \frac12)(k + \frac12))$ satisfies $\phi_k(2N-1-m) = -\phi_k(m)$ and $\phi_k(m + 2N) = -\phi_k(m)$; these turn the sum over $2N$ samples into the fold $u$. The FFT step follows from $(4n+1)(4k+1) = 16nk + 4n + 4k + 1$.

## Complexity

- **Direct.** MDCT and IMDCT take $\Theta(N^2)$ operations per frame. A signal of length $L$ has $\lceil L/N \rceil + 1$ frames, so the direct method takes $\Theta((L + N) N)$.
- **Fast.** The fold and unfold take $\Theta(N)$, the FFT of length $N/2$ takes $\Theta(N \log N)$, and the twiddle factors $\Theta(N)$. So the whole analysis or synthesis takes $\Theta((L + N) \log N)$.
- **Space.** $\Theta(N)$ beyond the input and the output: one frame, its fold, and the FFT buffer.
- **Latency.** The decoder can output block $j$ only after it has frame $j$, which ends $N$ samples after block $j$, so the transform alone adds a delay of up to $2N - 1$ samples. This is why speech coders such as the CELT layer of Opus use short frames and a low-overlap window.

## Properties

- **Critically sampled.** $N$ new samples give $N$ coefficients, although each frame sees $2N$ samples.
- **Orthogonal as a whole.** With a symmetric Princen-Bradley window, the synthesis is the transpose of the analysis, and quantization error in the coefficients becomes error of at most the same energy in the signal (equal energy on an infinite signal).
- **A cosine-modulated filter bank.** Row $k$ of the windowed MDCT is a filter of length $2N$ centered at the frequency $(k + \frac12)\pi/N$; the MDCT is an $N$-channel [filter bank](/filter-bank/) with perfect reconstruction. The window is the prototype low-pass filter.
- **No blocking edges.** The basis functions taper to small values at both ends, so quantization does not create jumps at frame edges as a block DCT does.
- **Window choice.** The sine window has a narrow main lobe; the KBD window with a larger $\alpha$ has a wider main lobe and stronger rejection far from it.
- **Not shift invariant.** A small shift of the input changes the coefficients a lot, because the MDCT is real and critically sampled.

## Variants and improvements

- **Window switching.** Coders switch to short frames around sudden sounds (transients) to limit the spread of quantization noise in time (pre-echo). Transition windows keep the Princen-Bradley condition across the change of size.
- **Low-overlap windows.** Make the window flat in the middle and overlap less than $N$ samples, to cut the delay; CELT in Opus does this.
- **Modulated lapped transform.** Malvar's MLT (1990) is the MDCT with the sine window; extended lapped transforms use windows longer than $2N$.
- **Different analysis and synthesis windows.** Biorthogonal versions relax the Princen-Bradley condition to a condition on the product of the two windows.
- **Integer MDCT.** Lifting steps give an integer-to-integer approximation for lossless audio coding.
- **The MDST and complex lapped transforms.** The sine counterpart, paired with the MDCT, gives a complex transform with better shift behavior, used for analysis and in some stereo tools.
- **Evenly stacked TDAC.** Princen and Bradley's first form (1986) alternates cosine and sine kernels; the MDCT is the oddly stacked form of 1987.

## When to use it

Use the MDCT for lossy coding of audio and other long signals where block edges would be audible or visible, and where critical sampling matters: perceptual audio coders, low-delay speech and music codecs. For still images, a block DCT or a wavelet transform is the usual choice. For lossless coding, use an integer version. For pure spectral analysis without coding, an oversampled transform such as the short-time Fourier transform is simpler, because the MDCT coefficients of a steady sine wave fluctuate from frame to frame.

## Pitfalls

- **Inverting one frame.** IMDCT(MDCT(x)) is not $x$. Only the overlap-add of neighboring frames is exact.
- **Edges.** The first and last blocks need a zero frame on the outside, as in ANALYSIS, or they come back with aliasing.
- **The window applies twice.** It multiplies before the MDCT and again after the IMDCT. Forgetting either breaks the cancellation.
- **Scaling conventions.** Libraries use factors $1$, $2/N$, $1/N$ or $\sqrt{2/N}$, and some put the $N/2$ shift or a sign in a different place. Check a round trip and compare with a direct sum.
- **Odd $N$.** The fold uses $N/2$, so the fast algorithm needs $N$ even, and the FFT step a power of two; the direct formula works for every $N$.
- **Pre-echo.** Quantization noise spreads over the whole frame of $2N$ samples, so it can be heard before a sharp onset. Use window switching.
- **Non-orthogonal edges of a finite signal.** On a padded finite signal the analysis is an isometry but has more coefficients than samples, so the error in the signal can be smaller than the error in the coefficients.

## Implementations

## History

John Princen and Alan Bradley described analysis-synthesis filter banks based on time domain aliasing cancellation (TDAC) in 1986, with the condition on the window that now bears their names. In 1987 Princen, Johnson and Bradley gave the oddly stacked version, with a single cosine kernel, that is now called the MDCT. Henrique Malvar developed the same transform with the sine window as the modulated lapped transform (1990), within his theory of lapped transforms. Duhamel, Mahieux and Petit gave the FFT algorithm in 1991. The MDCT became the transform of Dolby AC-3, of the hybrid filter bank of MPEG-1 Layer III (MP3), where it follows a 32-band polyphase filter bank, and of MPEG-2 and MPEG-4 AAC, with a choice between the sine and KBD windows. Vorbis and the CELT layer of Opus (RFC 6716, 2012) also use it.

## References
