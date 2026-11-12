---
tag: Y9ZKV2
kind: problem
slug: run-length-compression
name: Run-length compression
aliases:
- run-length coding of binary sources
area: compression-and-coding/transforms-for-compression
level: intro
summary: Code a sequence as the lengths of its runs of equal symbols, with a code for the lengths that fits their distribution. For geometric run lengths a Golomb code is optimal.
prereqs: [run-length-encoding, geometric-distribution, shannon-entropy]
see_also: [golomb-coding, rice-coding, huffman-coding, delta-encoding, elias-gamma-coding, inverted-index, r-index, lossless-compression]
sources:
  - paper: doi:10.1109/TIT.1966.1053907
    title: Solomon W. Golomb, Run-length encodings, IEEE Transactions on Information Theory 12(3), 1966
    locator: pages 399 to 401 (runs of a binary source with geometric lengths, and the code with parameter m)
  - paper: doi:10.1109/TIT.1975.1055357
    title: Robert G. Gallager and David C. Van Voorhis, Optimal source codes for geometrically distributed integer alphabets, IEEE Transactions on Information Theory 21(2), 1975
    locator: pages 228 to 230 (the Golomb code with m chosen by theta^m + theta^(m+1) <= 1 < theta^(m-1) + theta^m is an optimal prefix code)
  - url: https://www.itu.int/rec/T-REC-T.4
    title: ITU-T Recommendation T.4, Standardization of Group 3 facsimile terminals for document transmission
    locator: the one-dimensional coding scheme (modified Huffman code with terminating and make-up codes for white and black runs; section number not checked)
  - book: isbn:9780128094747
    title: Khalid Sayood, Introduction to Data Compression, 5th edition, Morgan Kaufmann, 2017
    locator: the chapter on lossless image compression (run-length coding of facsimile and the Golomb code; chapter number not checked)
---

Run-length compression is the problem of coding a sequence by the lengths of its runs of equal symbols, with a code for the lengths that is short for the lengths that are likely. [Run-length encoding](/run-length-encoding/) gives the runs; this problem is how to write them in as few bits as possible. For a binary source in which the bits are independent and a 0 has probability $\theta$, the length of a run of zeros has a [geometric distribution](/geometric-distribution/), and the [Golomb code](/golomb-coding/) with the parameter of Gallager and Van Voorhis is an optimal prefix code for it, so its expected length per run is less than the entropy plus one bit. Fax machines, inverted indexes and compressed bitmaps all solve forms of this problem.

## In plain words

Think of a black and white scan of a page. Most of each line is white, with a few short black parts. If you write down only how long each white part and each black part is, you need far fewer numbers than pixels.

The question is then how to write these numbers. Some lengths come up all the time and others almost never, so give the common lengths short codes and the rare ones long codes. If long white parts are as likely as the chance of white makes them, there is one best way to do this, and it is easy to compute: write the length divided by a fixed number in a simple count, and the rest in a few bits.

## Definition

**General form.** Given a sequence $X$ over $\Sigma$ with the runs $X = c_1^{\ell_1} \cdots c_r^{\ell_r}$, find a lossless code that writes the symbols $c_k$ and the lengths $\ell_k$, with the smallest expected length under a model of the runs, or the smallest length on a given input.

**Binary form.** For $\Sigma = \{0, 1\}$, cut $X$ into the pieces $0^{k_1} 1, 0^{k_2} 1, \ldots$, each a run of $k_j \ge 0$ zeros ended by a one, and let a virtual one end the last piece. Then $X$ is given by its length $n$ and the sequence $k_1, k_2, \ldots$, and the problem is to code the integers $k_j \ge 0$. If the bits are independent with $\Pr[0] = \theta$, then

$$\Pr[k] = (1 - \theta)\,\theta^k, \qquad k = 0, 1, 2, \ldots$$

and the entropy of one run length is $H = h(\theta) / (1 - \theta)$ bits, where $h(\theta) = -\theta \log_2 \theta - (1 - \theta) \log_2 (1 - \theta)$.

## Variants

- **Alternating runs.** Code the runs of zeros and the runs of ones in turn, each with its own model, as fax coding does for white and black runs. This fits a source in which both symbols come in runs, such as a Markov source with two states.
- **Larger alphabets.** Code each run as a symbol and a length, or code a run only when it is long and the symbol alone otherwise; see [run-length encoding](/run-length-encoding/).
- **Unknown parameter.** If $\theta$ is not known, estimate it from the data seen so far and choose the code parameter from the estimate, as adaptive Golomb and Rice coders do.
- **Two dimensions.** Code the runs of a line relative to the runs of the line above it, as the two-dimensional mode of fax coding does.

## Examples

Take $\theta = 0.9$. The smallest $m$ with $0.9^m + 0.9^{m+1} \le 1$ is $m = 7$. The Golomb code of $k$ is $q = \lfloor k / 7 \rfloor$ in unary ($q$ ones and a zero), then $r = k \bmod 7$ in truncated binary: $r = 0$ takes the 2 bits `00`, and $r = 1, \ldots, 6$ take 3 bits, the value $r + 1$.

The 31 bits $0^9\,1\,0^2\,1\,0^{14}\,1\,0^3$ have the run lengths $9, 2, 14, 3$, the last one closed by the virtual one:

| $k$ | $q$ | $r$ | code |
|---|---|---|---|
| 9 | 1 | 2 | `10` `011` |
| 2 | 0 | 2 | `0` `011` |
| 14 | 2 | 0 | `110` `00` |
| 3 | 0 | 3 | `0` `100` |

The code has 18 bits. The decoder reads the codes in turn and writes $0^k 1$ for each, and drops the last one, because it knows $n = 31$.

**Fax.** The modified Huffman code of ITU-T T.4 codes each scan line as alternating white and black runs, starting with a white run, which may have length 0. It has separate tables for white and black: a terminating code for each length from 0 to 63, and make-up codes for multiples of 64, so a long run is a make-up code followed by a terminating code. Each line ends with the end-of-line code `000000000001`.

## Known algorithms

```pseudo id=main
RUNS-ENCODE(X[0 .. n − 1], θ)                    ▷ X is a string of bits
L1  m ← the smallest m ≥ 1 with θ^m + θ^(m+1) ≤ 1
L2  k ← 0
L3  for each bit b of X do
L4      if b = 0 then k ← k + 1
L5      else write GOLOMB(k, m); k ← 0
L6  write GOLOMB(k, m)                            ▷ the last run, closed by a virtual 1
L7  return the bits written
```

Here $\mathrm{GOLOMB}(k, m)$ writes $\lfloor k / m \rfloor$ in unary and $k \bmod m$ in truncated binary, with $\lceil \log_2 m \rceil - 1$ bits for the first $2^{\lceil \log_2 m \rceil} - m$ remainders and $\lceil \log_2 m \rceil$ bits for the rest. The encoder and the decoder take $O(n)$ time plus the length of the code.

- **Golomb codes** (Golomb, 1966; the rule for $m$ by Gallager and Van Voorhis, 1975) are optimal prefix codes for geometric run lengths.
- **[Rice codes](/rice-coding/)** are Golomb codes with $m = 2^j$. The remainder is then $j$ plain bits, which makes the coder faster, at a small cost when the best $m$ is not a power of two.
- **[Huffman codes](/huffman-coding/) on the run lengths**, with long runs split into a make-up part and a terminating part, as in fax coding. They fit any distribution with fixed tables.
- **Elias codes** ([gamma](/elias-gamma-coding/), delta) need no parameter and suit run lengths with a heavy tail.
- **[Arithmetic coding](/arithmetic-coding/)** of the bits with a context model often beats run-length coding on images, because it uses the line above too; JBIG uses this method.

## Bounds

- **Entropy.** By the source coding theorem, no prefix code for the run length has an expected length below $H = h(\theta) / (1 - \theta)$. A Golomb code with the parameter of line L1 is an optimal prefix code (Gallager and Van Voorhis), so its expected length $E$ satisfies $H \le E < H + 1$, as for any [Huffman code](/huffman-coding/).
- **Rate per source bit.** A piece $0^k 1$ has $k + 1$ bits on average $1 / (1 - \theta)$, so the code uses $E (1 - \theta) < h(\theta) + (1 - \theta)$ bits per source bit. When ones are rare, $1 - \theta$ is small, and the rate is close to the entropy $h(\theta)$, which a code of single bits cannot reach (it needs 1 bit per bit).
- **The choice of $m$.** For $\theta$ close to 1, the best $m$ is close to $\ln 2 / (1 - \theta)$, about $0.69$ times the mean run length.
- **No gain for every input.** As for all lossless codes, some inputs get longer. Here an input with many ones and $\theta$ close to 1 costs about $\log_2 m$ bits for each one.

## Reductions

- **To coding gaps.** The positions of the ones in $X$ form a sorted set, and the run lengths are the gaps between them, minus one. So run-length compression of a binary string is the same problem as coding a sorted set of integers by [delta encoding](/delta-encoding/) and a code for the gaps. Inverted indexes code their lists of document numbers in this way, and a Golomb code with $m$ set from the density of the list suits a word that occurs at random places.
- **From compression of text.** The [Burrows-Wheeler transform](/burrows-wheeler-transform/) turns repetition in a text into runs, so after it, text compression becomes largely run-length compression. The number of runs $r$ of the BWT is a measure of repetition, and the [r-index](/r-index/) takes space proportional to $r$.

## Applications

- **Fax and bilevel images.** Group 3 and Group 4 fax code the runs of white and black pixels of each scan line.
- **Inverted indexes and bitmaps.** Gaps between document numbers, and runs of zeros in sparse bitmaps, are coded with Golomb, Rice or Elias codes, or with run containers in compressed bitmap formats.
- **Lossless image and audio coding.** Coders such as JPEG-LS switch to a run mode in flat parts of an image, and audio coders code the small residuals of [predictive coding](/predictive-coding/) with Rice codes.
- **After the BWT and MTF.** bzip2 codes the runs of zeros of the move-to-front output with a special pair of symbols.

## References
