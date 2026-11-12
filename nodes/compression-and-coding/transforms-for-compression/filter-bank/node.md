---
tag: A2J8ZX
kind: concept
slug: filter-bank
name: Filter bank
aliases:
- analysis-synthesis filter bank
area: compression-and-coding/transforms-for-compression
level: advanced
summary: Set of analysis filters and downsamplers, with synthesis filters that reconstruct the signal.
prereqs: [fir-filter, z-transform, polyphase-decomposition]
see_also: [perfect-reconstruction, subband-coding, modified-discrete-cosine-transform, discrete-wavelet-transform, aliasing, lifting-scheme, jpeg-2000, haar-wavelet]
sources:
  - book: isbn:9780136057185
    title: P. P. Vaidyanathan, Multirate Systems and Filter Banks, Prentice Hall, 1993
    locator: Chapter 4 (multirate building blocks, the noble identities and the polyphase representation), Chapter 5 (maximally decimated filter banks, alias cancellation and perfect reconstruction) and Chapter 6 (paraunitary filter banks)
  - book: isbn:9780130970800
    title: Martin Vetterli and Jelena Kovačević, Wavelets and Subband Coding, Prentice Hall, 1995
    locator: Chapter 3, Discrete-Time Bases and Filter Banks (two-channel and M-channel banks, the polyphase matrix, orthogonal and biorthogonal banks, tree-structured banks)
  - paper: doi:10.1109/MASSP.1987.1165589
    title: P. P. Vaidyanathan, Quadrature mirror filter banks, M-band extensions and perfect-reconstruction techniques, IEEE ASSP Magazine 4(3), 1987
    locator: pp. 4 to 20 (a tutorial on two-channel and M-channel banks, aliasing and the polyphase view)
  - paper: doi:10.1016/0165-1684(86)90101-5
    title: Martin Vetterli, Filter banks allowing perfect reconstruction, Signal Processing 10(3), 1986
    locator: pp. 219 to 244 (the polyphase matrix of an M-channel bank and the conditions for perfect reconstruction)
  - paper: doi:10.1002/j.1538-7305.1976.tb02929.x
    title: R. E. Crochiere, S. A. Webber and J. L. Flanagan, Digital coding of speech in sub-bands, Bell System Technical Journal 55(8), 1976
    locator: pp. 1069 to 1085 (splitting speech into frequency bands and coding each band with its own number of bits)
  - paper: doi:10.1109/ICASSP.1977.1170341
    title: D. Esteban and C. Galand, Application of quadrature mirror filters to split band voice coding schemes, Proceedings of ICASSP 1977, vol. 2
    locator: pp. 191 to 195 (the two-channel quadrature mirror filter bank that cancels aliasing)
  - paper: doi:10.1109/ICASSP.1988.196696
    title: D. Le Gall and A. Tabatabai, Sub-band coding of digital images using symmetric short kernel filters and arithmetic coding techniques, Proceedings of ICASSP 1988
    locator: pp. 761 to 764 (the 5/3 pair of linear-phase filters with perfect reconstruction)
---

A filter bank splits a signal into several channels, each filtered by its own analysis filter and then downsampled, and a synthesis bank upsamples the channels, filters them again and adds them to rebuild the signal. When the channels together keep exactly as many samples as the input, the bank is critically sampled (maximally decimated). Downsampling creates [aliasing](/aliasing/) in each channel, and the synthesis filters must be chosen so that the aliasing of the channels cancels in the sum; when, in addition, the output is a scaled and delayed copy of the input, the bank has [perfect reconstruction](/perfect-reconstruction/). Block transforms such as the DCT, lapped transforms such as the [MDCT](/modified-discrete-cosine-transform/), and the [discrete wavelet transform](/discrete-wavelet-transform/) are all filter banks, which is why the theory below covers them all.

## In plain words

A filter bank is a set of sieves for a signal. One sieve keeps the slow changes, another the fast ones, and others the speeds in between. Each sieve's output changes more slowly than the whole signal, so most of its samples can be dropped without losing what that sieve kept. In the end the parts together hold as many numbers as the original.

Dropping samples mixes some fast changes into the slow parts in a wrong way. A second set of sieves, matched to the first, puts the parts back together so that these wrong pieces cancel. With a good match, the signal comes back exactly, only shifted a little in time. A coder can then spend bits on each part according to how much it matters.

## The idea

**The two building blocks.** Write signals as sequences $x[n]$ and their [z-transforms](/z-transform/) $X(z) = \sum_n x[n] z^{-n}$. Downsampling by $M$ keeps $x[nM]$. Upsampling by $M$ puts $M - 1$ zeros after each sample, $Y(z) = X(z^M)$. Downsampling by 2 followed by upsampling by 2 sets the odd samples to zero:

$$V(z) \;\mapsto\; \tfrac12\big(V(z) + V(-z)\big).$$

The term $V(-z)$ is the spectrum shifted by half the sampling rate: the alias.

**An $M$-channel bank.** The analysis filters $h_0, \dots, h_{M-1}$ give the subbands

$$v_k[n] = \sum_j h_k[j]\, x[nM - j], \qquad 0 \le k < M,$$

and the synthesis filters $f_0, \dots, f_{M-1}$ give $\hat x[n] = \sum_k \sum_i f_k[n - iM]\, v_k[i]$. The bank is critically sampled because $M$ channels each keep one sample in $M$.

**Two channels.** For $M = 2$, the rule above gives

$$\hat X(z) = \underbrace{\tfrac12\big[F_0(z)H_0(z) + F_1(z)H_1(z)\big]}_{T(z)}\, X(z) \;+\; \underbrace{\tfrac12\big[F_0(z)H_0(-z) + F_1(z)H_1(-z)\big]}_{A(z)}\, X(-z).$$

$T(z)$ is the distortion function and $A(z)$ the alias function. The choice

$$F_0(z) = H_1(-z), \qquad F_1(z) = -H_0(-z)$$

makes $A(z) = 0$ for every pair of analysis filters. Then $\hat X(z) = T(z) X(z)$, and the bank is a linear time-invariant system. It has perfect reconstruction when $T(z) = c\, z^{-l}$; the conditions and the classic filter pairs are on the page [perfect reconstruction](/perfect-reconstruction/).

**The polyphase form.** Split each analysis filter into its [polyphase components](/polyphase-decomposition/), $H_k(z) = \sum_{j<M} z^{-j} E_{kj}(z^M)$, and split the input into the $M$ phases $x_j[n] = x[nM - j]$. Then

$$v_k = \sum_{j<M} e_{kj} * x_j ,$$

where $*$ is convolution at the low rate. So the analysis bank is a delay chain, $M$ downsamplers, and an $M \times M$ matrix $\mathbf E(z)$ of filters that runs at the low rate. The synthesis bank is a matrix $\mathbf R(z)$ followed by upsamplers and a delay chain. Two facts follow.

- **Cost.** The direct form filters at the full rate and then throws away $M - 1$ of every $M$ outputs. The polyphase form computes only the kept samples, so it does $M$ times less work: for filters of length $L$, each channel needs $L$ multiplications per kept output sample, that is $L/M$ per input sample, against $L$ per input sample in the direct form.
- **Reconstruction.** If $\mathbf R(z)\mathbf E(z) = c\, z^{-l_0} I$, the bank has perfect reconstruction. If $\mathbf E(z)$ is paraunitary, $\mathbf E^{\mathsf T}(z^{-1})\mathbf E(z) = I$, the synthesis is the time reverse of the analysis and the bank is an orthogonal transform of the signal.

**Orthogonal and biorthogonal banks.** In a two-channel orthogonal bank the lowpass filter is orthonormal to its own even shifts, $\sum_n h_0[n] h_0[n + 2k] = \delta_k$, the highpass is the conjugate quadrature filter $h_1[n] = (-1)^n h_0[L-1-n]$, and the synthesis filters are the time-reversed analysis filters. In a biorthogonal bank the synthesis filters differ from the analysis filters; this allows linear-phase (symmetric) filters, which an orthogonal two-channel FIR bank cannot have except for the Haar filter.

**Block and lapped transforms are filter banks.** An orthogonal $M \times M$ block transform $T$ is an $M$-channel bank with analysis filters $h_k[n] = T_{k, M-1-n}$ and synthesis filters $f_k[n] = T_{kn}$, all of length $M$, and its delay is $M - 1$. A lapped transform such as the MDCT has filters of length $2M$. Longer filters give better frequency selectivity, and so better [energy compaction](/energy-compaction/) for coding, at the cost of more computation and delay.

**Trees and wavelets.** Applying a two-channel bank again to its lowpass channel, several times, gives an octave-band (dyadic) bank. That iterated bank is the discrete wavelet transform; with suitable filters its limit functions are the wavelets of Daubechies.

## Examples

**Haar.** Take $h_0 = (1, 1)/\sqrt2$ and $h_1 = (1, -1)/\sqrt2$, and $x = (4, 6, 10, 12, 8, 6, 5, 5)$, with zeros outside. Filtering and keeping the even-indexed outputs gives

$$v_0 = \tfrac{1}{\sqrt2}(4, 16, 20, 11, 5), \qquad v_1 = \tfrac{1}{\sqrt2}(4, 4, -4, -1, -5).$$

Each entry is a sum or a difference of two neighbors, $x[2i] \pm x[2i-1]$; the first and last entries come from the zero edges. The alias-cancelling synthesis $f_0 = (1, 1)/\sqrt2$, $f_1 = (-1, 1)/\sqrt2$ returns $(0, 4, 6, 10, 12, 8, 6, 5, 5, 0, 0)$: the input delayed by one sample.

**LeGall 5/3.** The analysis pair $h_0 = (-1, 2, 6, 2, -1)/8$ and $h_1 = (-\frac12, 1, -\frac12)$ is symmetric (linear phase); $\sum h_0 = 1$ and $\sum h_1 = 0$. On the same $x$ it gives

$$v_0 = (-0.5, 3.25, 10.5, 8.625, 5.5, 0.625), \qquad v_1 = (-2, -1, 3, -0.5, 2.5).$$

With $F_0(z) = H_1(-z)$ and $F_1(z) = -H_0(-z)$, the output is $-x$ delayed by 3 samples, so $T(z) = -z^{-3}$; changing the sign of both synthesis filters gives $+z^{-3}$. The polyphase components of $h_0$ are $E_{00} = (-1, 6, -1)/8$ and $E_{01} = (2, 2)/8$. This pair, implemented by the [lifting scheme](/lifting-scheme/), is the reversible filter of [JPEG 2000](/jpeg-2000/).

**Daubechies 4-tap.** $h_0 = (0.4830, 0.8365, 0.2241, -0.1294)$, the values $(1 + \sqrt3, 3 + \sqrt3, 3 - \sqrt3, 1 - \sqrt3)/(4\sqrt2)$, is orthonormal to its shifts by 2. With the conjugate quadrature highpass, the bank is orthogonal and returns $x$ delayed by 3 samples.

**A bank that cancels aliasing but distorts.** The quadrature mirror choice $H_1(z) = H_0(-z)$ with $h_0 = (1, 2, 1)\sqrt2/4$ cancels the alias term, but its distortion function is $T(z) = \frac12 z^{-1} + \frac12 z^{-3}$, not a single delay. On $x$ the output is $(0, 2, 3, 7, 9, 9, 9, 6.5, 5.5, 2.5, 2.5, 0)$: the average of $x$ delayed by 1 and by 3.

**The block DCT.** The $4 \times 4$ orthonormal DCT-II, seen as a 4-channel bank with $h_k[n] = c_k[3 - n]$ and $f_k = c_k$, produces in its subbands exactly the coefficients of the blocks $x[4b .. 4b+3]$, and returns $x$ delayed by 3 samples.

## Where it is used

- **Subband coding.** Crochiere, Webber and Flanagan (1976) split speech into bands and coded each band with its own bit rate; Esteban and Galand (1977) used two-channel quadrature mirror filters for this. See [subband coding](/subband-coding/), which is the whole coder, while the filter bank is its transform.
- **Audio coding.** MPEG-1 audio uses a 32-band cosine-modulated filter bank with near-perfect reconstruction; MP3 follows it with an MDCT, and AAC, Vorbis and Opus use the MDCT alone.
- **Image coding.** JPEG 2000 applies a two-channel bank to rows and columns and iterates it on the low band, with the 5/3 filter for lossless coding and the Cohen-Daubechies-Feauveau 9/7 filter for lossy coding; see [JPEG 2000](/jpeg-2000/) and [SPIHT](/spiht/).
- **Wavelets.** The [discrete wavelet transform](/discrete-wavelet-transform/) and the [Haar wavelet](/haar-wavelet/) are iterated two-channel banks.
- **Communications.** A synthesis bank followed by an analysis bank is a transmultiplexer, which carries several signals on one channel; OFDM is the case of DFT filters. Channelizers in radio receivers use polyphase DFT banks.
- **Spectral analysis.** The short-time Fourier transform is an oversampled DFT-modulated filter bank. The mel filter bank of speech recognition is a different object: it is analysis only, it is not critically sampled, and it is not meant to be inverted.

## References
