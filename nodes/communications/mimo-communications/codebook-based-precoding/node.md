---
tag: CWWEE6
kind: technique
slug: codebook-based-precoding
name: Codebook-based precoding
aliases:
- limited feedback precoding
- Grassmannian beamforming
area: communications/mimo-communications
level: advanced
summary: The receiver picks a precoder from a codebook known at both ends and feeds back its index, so the transmitter needs only a few bits of feedback in place of the full channel.
prereqs: [maximum-ratio-transmission, svd-precoding, mimo-channel-model]
see_also: [welch-bound, zero-forcing-precoding, block-diagonalization, hybrid-beamforming, k-means, scalar-quantization, spatial-multiplexing, beamforming]
sources:
  - paper: doi:10.1109/TIT.2003.817466
    title: "David J. Love, Robert W. Heath Jr. and Thomas Strohmer, Grassmannian beamforming for multiple-input multiple-output wireless systems, IEEE Transactions on Information Theory 49(10), 2735-2747, 2003"
    locator: "the selection of a beam vector at the receiver with the index sent back, and the codebook design criterion of the largest minimum chordal distance, which relates the design to Grassmannian line packing for i.i.d. Rayleigh fading"
  - paper: "David J. Love and Robert W. Heath Jr., Limited feedback unitary precoding for spatial multiplexing systems, IEEE Transactions on Information Theory 51(8), 2005"
    locator: "codebooks of matrices with orthonormal columns for several streams, and the selection criteria based on the minimum singular value, the capacity and the mean squared error"
  - paper: doi:10.1109/TIT.2006.883550
    title: "Nihar Jindal, MIMO broadcast channels with finite-rate feedback, IEEE Transactions on Information Theory 52(11), 5045-5060, 2006"
    locator: "zero-forcing precoding on quantized channel directions, and the result that the feedback bits per user must grow linearly with the SNR in dB to keep the full multiplexing gain"
  - book: isbn:9780521762281
    title: "Robert W. Heath Jr. and Angel Lozano, Foundations of MIMO Communication, Cambridge University Press, 2018"
    locator: "the chapters on single-user MIMO and on multiuser MIMO, the parts on quantized channel feedback"
---

Codebook-based precoding is a way to give the transmitter of a [MIMO link](/mimo-channel-model/) enough channel knowledge to beamform with only a few bits of feedback. The transmitter and the receiver share a fixed list of $N = 2^B$ precoders, the codebook. The receiver estimates the channel, picks the codebook entry that gives the best link, and sends back its $B$-bit index. The transmitter then uses that entry. With perfect channel knowledge at the transmitter, the best single-stream precoder is [maximum ratio transmission](/maximum-ratio-transmission/) for one receive antenna and the dominant right singular vector of [SVD precoding](/svd-precoding/) for several; a codebook quantizes this vector. The quality of a codebook depends on how evenly its vectors cover the space of beam directions, which is a packing problem of lines in $\mathbb{C}^n$. [Hybrid beamforming](/hybrid-beamforming/) also restricts the precoder, but by hardware, not by feedback.

## In plain words

A transmitter with several antennas can aim its signal at a receiver, but only if it knows the channel. The receiver can measure the channel, but sending the whole measurement back takes too much capacity. So both sides agree in advance on a short list of possible aiming directions. The receiver tries every direction on the list in its head, picks the one that would give the strongest signal, and sends back only its number in the list. With 16 directions, that is 4 bits.

The list must spread its directions evenly, so that every possible channel has a direction on the list that is close to the best one. A bad list wastes entries on directions that are almost the same.

## When it applies

- The transmitter cannot learn the channel by itself. This is the usual case in frequency division duplex, where the uplink and the downlink use different frequencies and the channel is not reciprocal. In time division duplex the transmitter can estimate the channel from uplink pilots, and a codebook is not needed.
- There is a feedback link from the receiver to the transmitter with a small, fixed number of bits per channel coherence interval.
- The receiver knows its channel $H$ (CSIR), for example from pilots, and the transmitter knows the codebook.
- The channel changes slowly enough that the index is still valid when the transmitter uses it.

## The template

The link is $y = H f s + w$ with $H \in \mathbb{C}^{m \times n}$ for $n$ transmit and $m$ receive antennas, a unit-norm precoder $f$, a symbol with $\mathbb{E}|s|^2 = P$ and $w \sim \mathcal{CN}(0, N_0 I)$. With [maximal ratio combining](/maximal-ratio-combining/) at the receiver, the SNR is $\rho \|H f\|^2$ with $\rho = P/N_0$.

1. **Design the codebook once, offline.** Choose $\mathcal{F} = \{f_1, \ldots, f_N\}$ of unit vectors in $\mathbb{C}^n$, $N = 2^B$. Store it at both ends.
2. **Select at the receiver.** For each channel realization, compute $i^\star = \arg\max_i \|H f_i\|^2$. This costs $O(N m n)$ operations in the real-RAM model.
3. **Feed back** the $B$ bits of $i^\star$.
4. **Transmit** with $x = f_{i^\star} s$.

The phase of a beam vector does not matter, since $\|H f e^{j\phi}\| = \|H f\|$. So a codebook is a set of lines (one-dimensional subspaces), not of vectors. The distance between two lines is the chordal distance

$$d(f_i, f_j) = \sqrt{1 - |f_i^H f_j|^2}.$$

**Design criterion.** For i.i.d. Rayleigh fading, the best direction $v$ (the dominant right singular vector of $H$) is uniform on the lines, and its quantization error drives the SNR loss. Love, Heath and Strohmer (2003) bound the average loss and derive the criterion: maximize the minimum chordal distance between the codebook lines. This is Grassmannian line packing. For $N$ lines in $\mathbb{C}^n$, the [Welch bound](/welch-bound/) gives $\max_{i \ne j} |f_i^H f_j|^2 \ge (N - n)/(n (N - 1))$ when $N \ge n$, so the minimum chordal distance is at most $\sqrt{1 - (N - n)/(n(N - 1))}$; packings that meet it with equality exist only for some $N$ and $n$.

**Full diversity (a proved condition).** If the codebook vectors span $\mathbb{C}^n$, then $c = \min_{\|u\| = 1} \max_i |u^H f_i|^2 > 0$, because the minimum of a continuous function on the compact unit sphere is attained, and a unit $u$ with $\max_i |u^H f_i| = 0$ would be orthogonal to a spanning set. For one receive antenna, $H = h^H$ and the selected gain is $|h^H f_{i^\star}|^2 \ge c \|h\|^2$. So the SNR is at least $c$ times the SNR of perfect maximum ratio transmission, and the diversity order is $n$, the same as with full channel knowledge, in i.i.d. Rayleigh fading. A codebook needs at least $N \ge n$ entries to span.

## Classic examples

**Two antennas, one receive antenna.** Take $n = 2$, $m = 1$ and the channel $h = (0.6 + 0.8j,\ -1 + 0.5j)$, with $\|h\|^2 = 2.25$, and the 2-bit codebook

$$f_1 = \tfrac{1}{\sqrt 2}(1, 1), \quad f_2 = \tfrac{1}{\sqrt 2}(1, -1), \quad f_3 = \tfrac{1}{\sqrt 2}(1, j), \quad f_4 = \tfrac{1}{\sqrt 2}(1, -j),$$

which is the rank-one codebook of the LTE standard for two antennas. The gains $|h^H f_i|^2$ are 0.925, 1.325, 2.225 and 0.025. The receiver feeds back index 3 (bits 10), and the gain is $2.225$ against the optimum $\|h\|^2 = 2.25$ of maximum ratio transmission, a loss of 0.049 dB. Index 4 would almost cancel the signal.

**Average gain in i.i.d. Rayleigh fading.** With $h \sim \mathcal{CN}(0, I_2)$, the norm $\|h\|^2$ (mean 2) and the direction $u = h/\|h\|$ are independent, so the mean gain is $2\, \mathbb{E} \max_i |u^H f_i|^2$. A unit vector in $\mathbb{C}^2$, up to phase, maps to a point $b$ on the unit sphere in $\mathbb{R}^3$ (the Bloch sphere), with $|u^H f|^2 = (1 + b_u \cdot b_f)/2$, and a uniform $u$ gives a uniform $b_u$.

| codebook | bits | $\max |f_i^H f_j|^2$ | mean gain | loss | worst case $c$ |
|---|---|---|---|---|---|
| one fixed vector (no feedback) | 0 | none | 1 | 3.01 dB | 0 |
| $\{f_1, f_2\}$ | 1 | 0 | 1.5 | 1.25 dB | 0.5 |
| $\{f_1, f_2, f_3, f_4\}$ above | 2 | 0.5 | 1.7071 | 0.69 dB | 0.5 |
| 4 lines of a regular tetrahedron | 2 | 1/3 | 1.745 | 0.59 dB | 2/3 |
| perfect maximum ratio transmission | none | none | 2 | 0 | 1 |

The values for one and two vectors with the axes $\pm \hat x$ and $\pm \hat x, \pm \hat y$ are exact: $\mathbb{E}|b_x| = 1/2$ gives $(1 + 1/2)/2 = 0.75$, and $\mathbb{E}\max(|b_x|, |b_y|) = (\pi/4)(2\sqrt 2/\pi) = \sqrt 2/2$ gives $(1 + \sqrt 2/2)/2 = 0.85355$. The tetrahedral value is a Monte Carlo average over $2 \times 10^6$ directions. The tetrahedral lines are $(1, 0)$ and $(1/\sqrt 3,\ \sqrt{2/3}\, e^{j 2\pi k/3})$ for $k = 0, 1, 2$; every pair has $|f_i^H f_j|^2 = 1/3$, which meets the Welch bound $(4 - 2)/(2 \cdot 3) = 1/3$. So it is an optimal line packing, and it beats the LTE codebook on both the mean and the worst case. The LTE codebook has other reasons for its form: its entries come from $\{\pm 1, \pm j\}$, so it needs no multiplications.

## Variations

- **Several streams.** For $r$ streams the codebook holds $n \times r$ matrices with orthonormal columns, and the receiver selects by the smallest singular value, the capacity or the mean squared error of its detector (Love and Heath 2005). The design is then a packing of subspaces.
- **Codebook design by training.** In place of a packing, a codebook can be found by the Lloyd algorithm (the vector quantizer form of [k-means](/k-means/)) on samples of the best beam direction, with $|u^H f|^2$ as the similarity. This adapts the codebook to correlated channels, where the best direction is not uniform.
- **Structured codebooks.** DFT codebooks, whose vectors are columns of an oversampled DFT matrix, match the array response of a uniform linear array and are the base of the codebooks for larger arrays in the 4G and 5G standards. Standards also feed back a rank indicator and a channel quality indicator with the precoder index.
- **Multiuser precoding.** Each user feeds back a quantized channel direction, and the base station applies [zero-forcing precoding](/zero-forcing-precoding/) or [block diagonalization](/block-diagonalization/) to the quantized directions. The quantization error leaves residual interference that grows with the transmit power. Jindal (2006) showed that the feedback bits per user must grow linearly with the SNR in dB to keep the full multiplexing gain, unlike the single-user case, where a fixed codebook keeps the full diversity at every SNR.
- **Random codebooks.** Codebooks of independent isotropic vectors (random vector quantization) are easy to analyze, and their average loss has closed forms in i.i.d. Rayleigh fading; Jindal (2006) uses them for the multiuser analysis.
- **Differential and predictive feedback.** For slowly varying channels, the receiver feeds back a small rotation of the previous precoder, which tracks the channel with fewer bits.

## Pitfalls

- **Selecting with the wrong metric.** For one stream with maximal ratio combining, the metric is $\|H f_i\|^2$. With a linear detector and several streams, a capacity metric and a minimum singular value metric can choose different entries; use the metric of the actual receiver.
- **Feedback delay.** The index is computed from an old channel. In fast fading, a stale index can be worse than a fixed beam. Check the coherence time against the feedback delay.
- **Treating lines as vectors.** Two vectors that differ only by a phase are the same beam. A codebook design that counts them as different wastes entries, and the chordal distance, not the Euclidean distance, is the right measure.
- **Too few entries.** With $N < n$ the vectors cannot span $\mathbb{C}^n$, and some channels are orthogonal to every entry, so the diversity drops.
- **Ignoring the multiuser case.** A codebook that is good for one user leaves residual interference in multiuser precoding, and the rate then saturates at high SNR unless the codebook size grows.
- **Power normalization.** Every entry must have unit norm; otherwise the selection favors the longest vectors, not the best directions.

## Exercises

1. For the channel $h = (1, j)$, compute $|h^H f_i|^2$ for the four LTE vectors above, and find the selected index and the loss in dB against maximum ratio transmission.
2. Prove that the chordal distance between lines satisfies the triangle inequality. (Hint: it equals $\frac{1}{\sqrt 2}\|f_i f_i^H - f_j f_j^H\|_F$.)
3. Show that for $n = 2$ the map from lines to the Bloch sphere sends $|f_i^H f_j|^2$ to $(1 + b_i \cdot b_j)/2$, and use it to prove that the tetrahedral codebook is an optimal packing of four lines.
4. Show that a codebook of $n$ orthonormal vectors in $\mathbb{C}^n$ (antenna selection when the vectors are the unit vectors) has worst case $c = 1/n$.
5. With $N$ independent isotropic vectors in $\mathbb{C}^2$, find $\mathbb{E}\max_i |u^H f_i|^2$ for $N = 1$ and $N = 2$, and compare with the table.

## References
