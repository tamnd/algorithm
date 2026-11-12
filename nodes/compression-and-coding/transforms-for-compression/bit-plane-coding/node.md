---
tag: 8GXKH4
kind: technique
slug: bit-plane-coding
name: Bit-plane coding
aliases:
- bit-plane encoding
- embedded bit-plane coding
area: compression-and-coding/transforms-for-compression
level: advanced
summary: "Send integer coefficients one binary plane at a time, most significant plane first, so that every prefix of the stream decodes to a coarser quantization."
prereqs: [scalar-quantization]
see_also: [jpeg-2000, spiht, gray-code, context-modeling, arithmetic-coding, run-length-encoding, discrete-wavelet-transform, transform-coding]
sources:
  - paper: "Jay W. Schwartz and Richard C. Barker, Bit-plane encoding: a technique for source encoding, IEEE Transactions on Aerospace and Electronic Systems AES-2(4), 1966"
    locator: pages 385 to 392 (the method of coding a block of samples by bit planes)
  - paper: doi:10.1109/78.258085
    title: Jerome M. Shapiro, Embedded image coding using zerotrees of wavelet coefficients, IEEE Transactions on Signal Processing 41(12), 1993
    locator: pages 3445 to 3462 (successive-approximation quantization, the dominant and subordinate passes, and the embedded stream)
  - paper: doi:10.1109/76.499834
    title: Amir Said and William A. Pearlman, A new, fast, and efficient image codec based on set partitioning in hierarchical trees, IEEE Transactions on Circuits and Systems for Video Technology 6(3), 1996
    locator: pages 243 to 250 (bit-plane transmission with the sorting and refinement passes)
  - paper: doi:10.1109/83.847830
    title: David Taubman, High performance scalable image compression with EBCOT, IEEE Transactions on Image Processing 9(7), 2000
    locator: pages 1158 to 1170 (the fractional bit-plane coding passes, the contexts, and the truncation points of each code block)
  - book: isbn:9780792375197
    title: David S. Taubman and Michael W. Marcellin, JPEG2000, Image Compression Fundamentals, Standards and Practice, Kluwer, 2002
    locator: the chapters on embedded quantization and on the EBCOT block coder
---

Bit-plane coding sends a block of integers, most often the quantized coefficients of a [transform](/transform-coding/) or [wavelet](/discrete-wavelet-transform/) coder, one binary *plane* at a time: first the most significant bit of every magnitude, then the next bit of every magnitude, and so on down to the least significant bit. The sign of a value goes out just after its first 1 bit. The result is an *embedded* stream: a cut after any bit still decodes, and a cut after plane $p$ gives exactly the indices of a [dead-zone quantizer](/scalar-quantization/) with a step $2^p$ times larger. Schwartz and Barker described the method in 1966. Shapiro's EZW (1993), [SPIHT](/spiht/) (1996) and the EBCOT block coder of [JPEG 2000](/jpeg-2000/) (2000) are all bit-plane coders with better ways to say where the 1 bits are.

## In plain words

Write each number in binary, one under the other, with the most important digits on the left. Now read the table by columns, not by rows: first the leftmost column of every number, then the next column, and so on.

The first column tells the receiver which numbers are very large, and roughly how large. Each new column halves the remaining doubt about every number. If the stream stops early, the receiver still has a rough copy of all the numbers, not an exact copy of only the first few. So one stream serves every bit rate: a slow link takes the first part, a fast link takes all of it, and nobody has to code the data again.

Large numbers are rare in the output of a good transform, so the top columns are almost all zeros and cost very little after entropy coding.

## When it applies

Use bit-plane coding when one coded stream must serve several bit rates or qualities, when the coder must hit an exact size by cutting the stream, or when a picture must arrive progressively, coarse first. It suits integers whose magnitudes vary a lot and are mostly small, such as quantized wavelet or DCT coefficients. If the rate is fixed in advance and no prefix will ever be used, a coder that sends each value whole, like the run-length and Huffman layer of [JPEG](/jpeg-compression/), is simpler and as good.

**Planes.** Write each value $v_i$, $i = 1, \ldots, n$, in sign-magnitude form, $v_i = s_i m_i$ with $s_i \in \{+1, -1\}$ and $m_i \ge 0$. Let $P$ be the bit length of $\max_i m_i$. Bit plane $p$, for $p = P-1$ down to $0$, is the binary vector $b_i^{(p)} = \lfloor m_i / 2^p \rfloor \bmod 2$. Value $i$ is *significant* at plane $p$ if $m_i \ge 2^p$, so its first 1 bit is at plane $p$ or above. The threshold of plane $p$ is $2^p$.

**The stream.** The plain coder sends plane $P-1$, then plane $P-2$, and so on. Inside a plane it sends $b_i^{(p)}$ for $i = 1, \ldots, n$, and, when this bit is the first 1 bit of value $i$, the sign of $v_i$ right after it. Practical coders replace the raw bits by an entropy-coded description, but they keep this order of information.

**Decoding a prefix.** After the decoder reads all of planes $P-1, \ldots, p$, it knows $\hat m_i = 2^p \lfloor m_i / 2^p \rfloor$ and the signs of the significant values. The true magnitude lies in $[\hat m_i, \hat m_i + 2^p - 1]$. The decoder outputs 0 for a value that is not significant yet, and $s_i(\hat m_i + 2^{p-1})$, the middle of the interval, for a significant one.

**Theorem (error after plane $p$).** After the decoder reads planes $P-1$ down to $p$:

1. Without the midpoint, $0 \le m_i - \hat m_i \le 2^p - 1$, and the decoded value has the right sign or is 0.
2. With the midpoint, a significant value has error at most $2^{p-1}$ (0 when $p = 0$). A value that is not significant is output as 0, with error $m_i \le 2^p - 1$.
3. The index $\lfloor m_i / 2^p \rfloor$ that the decoder knows is the index of the dead-zone quantizer $q = \mathrm{sign}(v) \lfloor |v| / 2^p \rfloor$.

*Proof.* The unread bits are the planes $p-1, \ldots, 0$ of $m_i$, so $m_i - \hat m_i = m_i \bmod 2^p$, which is between $0$ and $2^p - 1$. For a significant value the midpoint $\hat m_i + 2^{p-1}$ is at most $2^{p-1}$ from every integer in $[\hat m_i, \hat m_i + 2^p - 1]$. A value is not significant exactly when $\hat m_i = 0$, which means $m_i \le 2^p - 1$, and then its sign is not known, so 0 is the safe output. Point 3 is the definition of $\hat m_i$. $\square$

So each plane halves the error bound of every value, and since a plane costs at most about $n$ bits before entropy coding, the error falls by about 6 dB per plane, the same rate as a [scalar quantizer](/scalar-quantization/) gains per bit. If the integers are themselves dead-zone indices with step $\Delta$, the cut after plane $p$ is a dead-zone quantizer with step $2^p \Delta$: the planes form a family of nested quantizers, and the decoder can stop in any of them.

A cut inside a plane is also fine. The values before the cut are known to plane $p$, and the values after it to plane $p+1$. If the cut falls between a first 1 bit and its sign, the decoder ignores that 1 bit.

## The template

```pseudo id=main
BIT-PLANE-ENCODE(v[1..n], P)                 ▷ P: bit length of the largest |v[i]|
L1  for p ← P − 1 down to 0                  ▷ hole: the order of the planes and passes
L2      for i ← 1 to n                       ▷ hole: the scan order inside a plane
L3          b ← bit p of |v[i]|
L4          emit b                           ▷ hole: the entropy coder and its context
L5          if b = 1 and |v[i]| < 2^(p+1) then emit the sign of v[i]   ▷ first 1 bit
L6  return the bits
BIT-PLANE-DECODE(bits, n, P)
L7  replay lines L1 to L5 until the bits end: set bit p of m[i], read the sign, k[i] ← p
L8  return s[i] · (m[i] + 2^(k[i] − 1)) if m[i] ≠ 0 and k[i] > 0, else s[i] · m[i]   ▷ hole: the reconstruction point
```

Both procedures cost $\Theta(nP)$ time. The plain stream has exactly $nP + z$ bits, where $z$ is the number of nonzero values: one bit per value per plane, and one sign per nonzero value. The decoder needs $O(n)$ memory for the magnitudes, signs and known planes.

**The holes.** The scan order inside a plane (line L2), the split of a plane into passes (line L1), the entropy coder and its context for each bit (line L4), and the reconstruction point (line L8: the lower end of the interval, its middle, or a point biased toward 0 for a peaked density).

### Worked example

Take $v = (5, -3, 0, 12, -1)$, so $P = 4$. The magnitudes in binary are 0101, 0011, 0000, 1100 and 0001. The stream, one plane per group, with each sign written after its first 1 bit, is

| plane $p$ | bits | the new information | decoded with the midpoint | squared error |
|---|---|---|---|---|
| 3 | 000100 | 12 is significant, sign + | $(0, 0, 0, 12, 0)$ | 35 |
| 2 | 100010 | 5 is significant, sign +; bit 2 of 12 is 1 | $(6, 0, 0, 14, 0)$ | 15 |
| 1 | 011000 | $-3$ is significant, sign $-$ | $(5, -3, 0, 13, 0)$ | 2 |
| 0 | 110011 | the last bits; $-1$ is significant, sign $-$ | $(5, -3, 0, 12, -1)$ | 0 |

The stream has $nP + z = 20 + 4 = 24$ bits. Without the midpoint, the cut after plane 2 gives $(4, 0, 0, 12, 0)$, which is the dead-zone index times $2^2$. With the midpoint, the error of 12 rises from 0 to 2 after plane 2: the midpoint bounds the worst case, not the error of each value, so the error of one value can grow while the bound falls.

**Gray-code planes.** For samples of a smooth picture, the planes of the [binary-reflected Gray code](/binary-reflected-gray-code/) $g = x \oplus \lfloor x/2 \rfloor$ change less often than the plain binary planes, because neighbouring integers differ in exactly one Gray bit. On the ramp $0, 1, \ldots, 255$ the eight binary planes change 502 times in total ($255 + 127 + \cdots + 1$), and the eight Gray planes change 255 times, once per step. Longer runs in each plane help a [run-length](/run-length-encoding/) or context coder that codes each plane as a bilevel image.

## Classic examples

- **EZW** (Shapiro 1993): the first embedded wavelet coder. Each plane has a dominant pass, which finds the newly significant coefficients and codes whole trees of insignificant ones with one zerotree symbol, and a subordinate pass, which sends one more bit of each coefficient found before. The symbols go to an adaptive [arithmetic coder](/arithmetic-coding/).
- **[SPIHT](/spiht/)** (Said and Pearlman 1996): each plane has a sorting pass, which tests the significance of single coefficients and of sets of descendants in a wavelet tree and splits the significant sets, and a refinement pass, which sends bit $p$ of each coefficient that was significant at an earlier plane. The order of the coefficients comes from the significance tests themselves, so the decoder needs no extra position data.
- **EBCOT in [JPEG 2000](/jpeg-2000/)** (Taubman 2000): each code block, often $64 \times 64$ coefficients, is coded on its own, plane by plane, in three passes per plane. The significance propagation pass codes the coefficients that are not yet significant but have a significant neighbour, the magnitude refinement pass codes one more bit of the significant coefficients, and the cleanup pass codes the rest, with a run mode for long runs of insignificant coefficients. Each bit is coded by the MQ coder, a binary arithmetic coder, with a context from the state of the eight neighbours ([context modeling](/context-modeling/)). The end of each pass is a possible cut, so the encoder can cut each block at the point that is best for the whole image.
- **Lossless and progressive coding of grey pictures**: the planes of the samples, plain or Gray coded, are sent as bilevel images, top plane first. The first planes give a rough picture, and the full stream is [lossless](/lossless-compression/).

## Variations

- **Fractional planes.** EBCOT splits each plane into passes so that the bits that reduce the error most per bit come first. This gives more cut points and a better curve of error against rate between whole planes.
- **Set significance.** Instead of one bit per value per plane, test whether a whole set (a tree in EZW and SPIHT, a quadtree of a block in SPECK and in the tag trees of JPEG 2000) has any significant value. One 0 then covers many values, which is the main source of gain at low rates.
- **Context-coded planes.** Code each bit with an adaptive binary arithmetic coder whose context is the significance of the neighbours, as in EBCOT, instead of sending raw bits.
- **Reconstruction offset.** For a peaked density such as the Laplacian, the mean of the magnitude interval lies below its middle, so decoders often use $\hat m + \delta 2^p$ with $\delta$ a little under $1/2$.
- **Gray-code planes** for raw samples, as in the worked example.
- **Bit-plane coding of residuals in video**: fine granularity scalability in MPEG-4 Part 2 codes the DCT residual of an enhancement layer by planes, so that a server can cut the layer at any rate.

## Pitfalls

- **Two's complement planes.** In two's complement, $-1$ has a 1 in every plane, so a small negative value looks large in the top planes. Use sign and magnitude, and send the sign once, at the first 1 bit.
- **Raw planes are expensive.** The plain stream costs $n$ bits per plane even when a plane is all zeros. Without entropy coding, set tests or run-length coding, the top planes waste most of the rate, and the coder is worse than a fixed quantizer at the same rate.
- **A cut between a first 1 bit and its sign.** The decoder must treat that 1 bit as unread, or it reconstructs a value with a guessed sign.
- **The reconstruction of insignificant values.** They must decode as 0, not as the middle of $[0, 2^p - 1]$, because their sign is not known.
- **The error of one value is not monotone.** The midpoint rule keeps every value within the bound of its plane, but a single value can move away from the truth when a new bit arrives, as 12 does in the worked example. The bound and, in practice, the mean squared error fall; the error of each value does not have to.
- **The decoder must know $P$ and $n$.** Send them in a header, or the decoder cannot tell where the planes start.

## Exercises

1. Show that the plain stream has exactly $nP + z$ bits, where $z$ is the number of nonzero values, and that the cut after plane $p$ has $n(P - p)$ magnitude bits plus the signs of the values with $|v_i| \ge 2^p$.
2. Show that on the ramp $0, 1, \ldots, 2^b - 1$ the $b$ binary planes change $2^{b+1} - b - 2$ times in total, and the $b$ Gray-code planes change $2^b - 1$ times.
3. Let the magnitudes be independent with $P(m \ge t) = 2^{-t/\sigma}$ for integer $t$. Find the expected number of values that become significant at plane $p$, and use it to explain why the top planes are nearly all zeros.
4. Prove that the cut after plane $p$ of the stream of dead-zone indices with step $\Delta$ gives the same indices as a dead-zone quantizer with step $2^p \Delta$ applied to the original real values.

## References
