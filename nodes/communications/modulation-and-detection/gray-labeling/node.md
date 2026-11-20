---
tag: FYXAPG
kind: technique
slug: gray-labeling
name: Gray labeling of a constellation
aliases:
- Gray mapping
- Gray-coded constellation
area: communications/modulation-and-detection
level: intro
summary: Assigns bit labels to constellation points so that nearest neighbors differ in one bit, so most symbol errors cause one bit error.
prereqs: [signal-constellation, gray-code]
see_also: [gray-code, bit-error-rate, symbol-error-rate, hamming-distance, quadrature-amplitude-modulation, phase-shift-keying, bit-interleaved-coded-modulation, trellis-coded-modulation]
sources:
  - url: https://patents.google.com/patent/US2632058A/en
    title: Frank Gray, Pulse code communication, US Patent 2,632,058, filed November 1947, issued March 17, 1953
    locator: the reflected binary code, in which successive code groups differ in one place
  - paper: doi:10.1109/TIT.2004.838367
    title: Erik Agrell, Johan Lassing, Erik G. Ström and Tony Ottosson, On the optimality of the binary reflected Gray code, IEEE Transactions on Information Theory 50(12), 3170-3182, 2004
    locator: the study of Gray labelings for PSK, PAM and QAM constellations and of when the binary reflected Gray code gives the lowest bit error probability
  - paper: doi:10.1109/TCOMM.2002.800818
    title: Kyongkuk Cho and Dongweon Yoon, On the general BER expression of one- and two-dimensional amplitude modulations, IEEE Transactions on Communications 50(7), 1074-1080, 2002
    locator: the exact bit error probability of Gray-coded PAM and QAM
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 3.2 (Gray coding of the PAM, PSK and QAM signal points) and Section 4.3 (bit error probability with Gray coding)
---

A Gray labeling of a [signal constellation](/signal-constellation/) gives each point a bit label so that every two points at the minimum distance have labels that differ in exactly one bit. In Gaussian noise at a useful SNR, almost every symbol error moves to a nearest neighbor, so with a Gray labeling almost every symbol error costs one bit. Then the [bit error rate](/bit-error-rate/) is close to the [symbol error rate](/symbol-error-rate/) divided by $\log_2 M$, which is the smallest value any labeling can have. The [Gray code](/gray-code/) page gives the code itself, a listing of all bit strings in which consecutive strings differ in one bit; this page is about its use as a constellation labeling and why it lowers the bit error rate.

## In plain words

Each point of a constellation stands for a group of bits. Noise sometimes makes the receiver pick a wrong point, and nearly always the wrong point is one of the nearest ones. The bits of the wrong point are then reported instead of the right ones.

If the nearest points have bit groups that are very different, one small mistake spoils several bits. If every two nearest points have bit groups that differ in only one place, one small mistake spoils only one bit. A Gray labeling arranges the bit groups that way. It costs nothing: the points, their energy and the chance of a wrong point all stay the same. Only the number of wrong bits per wrong point goes down.

## When it applies

- **Hard decisions or bit-wise soft decisions at moderate to high SNR.** The gain comes from the fact that nearest-neighbor errors dominate. At very low SNR, errors to distant points are common, and the labeling matters less.
- **Constellations whose neighbor graph fits in a hypercube.** Join two points by an edge if they are at the minimum distance. A Gray labeling is a map of this graph into the $k$-dimensional hypercube, $k = \log_2 M$, that sends edges to edges. So the graph must be bipartite, since the hypercube is, and no point may have more than $k$ nearest neighbors. PAM, PSK and square and rectangular QAM satisfy this. A part of the hexagonal lattice does not, because its neighbor graph has triangles. The 32-point cross constellation fails in a less obvious way: its graph is bipartite with degree at most 4, but it does not fit in the 5-dimensional hypercube, so some neighbors must differ in two bits.
- **Uncoded or bit-interleaved transmission.** With [bit-interleaved coded modulation](/bit-interleaved-coded-modulation/) and a decoder that does not feed back to the demapper, Gray labeling is the usual choice. Schemes that code the labels directly, such as [trellis-coded modulation](/trellis-coded-modulation/), use other labelings (see Variations).

## The template

1. **Find the neighbor graph.** List the pairs of points at the minimum distance.
2. **Label one dimension with the reflected code.** For points equally spaced on a line or on a circle, take the levels in order $m = 0, 1, \ldots$ and give level $m$ the label $g(m) = m \oplus \lfloor m/2 \rfloor$, the binary reflected Gray code. Consecutive integers have labels that differ in one bit, and on a circle the last and first labels, $g(2^k - 1) = 2^{k-1}$ and $g(0) = 0$, also differ in one bit.
3. **Take products for product constellations.** For square or rectangular QAM, label the in-phase level with one 1-dimensional Gray code and the quadrature level with another, and join the two labels. Nearest neighbors differ in one level on one axis, so they differ in one bit.
4. **Check the labeling.** For every pair at the minimum distance, the [Hamming distance](/hamming-distance/) of the labels must be 1.

**Why it works.** For any labeling, let $\ell_i$ be the label of point $i$, $k = \log_2 M$, and $P(j \mid i)$ the probability of deciding $j$ when $i$ was sent. The bit error rate is

$$P_b = \frac{1}{k}\sum_i \pi_i \sum_{j \ne i} P(j \mid i)\, d_H(\ell_i, \ell_j).$$

*Theorem.* For every labeling, $\mathrm{SER}/k \le P_b \le \mathrm{SER}$. *Proof.* Two distinct labels have $1 \le d_H \le k$, and $\mathrm{SER} = \sum_i \pi_i \sum_{j \ne i} P(j \mid i)$. $\square$

At high SNR in AWGN, $P(j \mid i) \approx Q(d_{\min}/\sqrt{2N_0})$ for each nearest neighbor $j$ and is much smaller for the other points. Then

$$P_b \approx \frac{\bar d_H}{k}\, \bar N_{\min}\, Q\!\left(\frac{d_{\min}}{\sqrt{2N_0}}\right) \approx \frac{\bar d_H}{k}\, \mathrm{SER},$$

where $\bar d_H$ is the average Hamming distance over the nearest-neighbor pairs. A Gray labeling has $\bar d_H = 1$, the least possible value, so it reaches the lower bound of the theorem to first order. This is a high-SNR approximation, not an identity: errors to points farther away add terms with $d_H \ge 1$ even for a Gray labeling.

## Classic examples

**4-PAM.** The Gray labels 00, 01, 11, 10 on the amplitudes $+3, +1, -1, -3$ (raw units). At $E_s/N_0 = 15$ dB, the exact bit error rate is $1.4090 \times 10^{-4}$, equal to $\mathrm{SER}/2$ to five digits. The natural labels 00, 01, 10, 11 put the labels 01 and 10 next to each other in the middle. That one pair differs in two bits, and the bit error rate becomes $1.8787 \times 10^{-4}$, larger by the factor 4/3.

**8-PSK.** Around the circle the Gray labels are 000, 001, 011, 010, 110, 111, 101, 100. The natural labels 000, 001, ..., 111 have Hamming distances 1, 2, 1, 3, 1, 2, 1, 3 between neighbors (the last is 111 to 000), an average of 14/8 = 1.75. At high SNR their bit error rate is about 1.75 times that of the Gray labeling.

**16-QAM.** The label is the 2-bit Gray code of the in-phase level followed by that of the quadrature level; the table is on the [QAM](/quadrature-amplitude-modulation/) page. At $E_b/N_0 = 10$ dB the exact bit error rate is $1.7542 \times 10^{-3}$, and $\mathrm{SER}/4 = 1.7511 \times 10^{-3}$. The small excess comes from diagonal and longer errors.

**QPSK.** The labeling by $g(m)$ around the circle and the labeling by in-phase bit then quadrature bit are both Gray labelings, with 01 and 10 in swapped places. Both give the bit error rate $Q(\sqrt{2E_b/N_0})$, the same as BPSK.

## Variations

- **Choice among Gray labelings.** A constellation can have many Gray labelings, and they differ in the terms for errors beyond the nearest neighbors. Agrell, Lassing, Ström and Ottosson (2004) studied which labeling gives the lowest bit error probability for PSK, PAM and QAM, and found the binary reflected Gray code optimal under their assumptions on the channel.
- **Quasi-Gray labelings.** When no Gray labeling exists, as for 32-point cross QAM, a labeling that keeps $\bar d_H$ as close to 1 as possible is used.
- **Set partitioning.** [Trellis-coded modulation](/trellis-coded-modulation/) labels points so that the low-order bits split the constellation into subsets with growing minimum distance. Nearest neighbors then often differ in several bits; the code, not the labeling, protects them.
- **Labelings for iterative demapping.** When the decoder feeds information back to the demapper, labelings far from Gray can give a better final error rate, because the feedback helps more when neighbors differ in many bits.
- **APSK and other rings.** Each ring gets a Gray code around its circle, and the ring index gets its own bits; when the rings have different numbers of points, neighbors on different rings often differ in more than one bit.

## Pitfalls

- **Two ends must agree.** The transmitter and the receiver must use the same labeling. QPSK has two common Gray labelings that swap two labels; a mismatch gives a high error rate that looks like a hardware fault.
- **Low SNR.** The approximation $P_b \approx \mathrm{SER}/\log_2 M$ fails when errors to distant points are common. Use the exact sum or a simulation there.
- **Not a property of the points.** Two constellations with the same points and different labels have the same symbol error rate but different bit error rates. A bit error rate given without the labeling is incomplete.
- **Wraparound on the circle.** For PSK, the first and last points are neighbors. A labeling that is Gray along a line but not around the circle has one pair that differs in several bits.
- **Gray code is not a channel code.** The labeling adds no redundancy and corrects nothing; it only makes the most likely errors cheap.

## Exercises

1. Show that $g(m) = m \oplus \lfloor m/2 \rfloor$ and $g(m+1)$ differ in exactly one bit.
   *Answer.* If $m$ ends in $t$ one bits, then $m \oplus (m+1) = 2^{t+1} - 1$. Since $g$ is linear over XOR, $g(m) \oplus g(m+1) = (2^{t+1} - 1) \oplus (2^t - 1) = 2^t$, a single bit.
2. How many of the $4! = 24$ labelings of QPSK are Gray labelings?
   *Answer.* 8. The neighbor graph is a 4-cycle and must go onto the 4-cycle 00, 01, 11, 10 of the square. There are 4 choices for the image of one point and 2 directions.
3. Prove that every labeling has $P_b \ge \mathrm{SER}/\log_2 M$.
   *Answer.* Every wrong decision changes at least one bit; see the theorem in The template.
4. Explain why a constellation from the hexagonal lattice has no Gray labeling.
   *Answer.* Three mutually nearest points form a triangle in the neighbor graph. Their three labels would differ pairwise in one bit, but $a \oplus b$ and $b \oplus c$ are single bits whose XOR $a \oplus c$ has 0 or 2 one bits, not 1.
5. Compute the average Hamming distance between neighbors for natural binary 8-PSK.
   *Answer.* $14/8 = 1.75$, as in Classic examples.

## References
