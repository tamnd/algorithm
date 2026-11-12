---
tag: SEKR0Q
kind: algorithm
slug: run-length-encoding
name: Run-length encoding
aliases:
- RLE
area: compression-and-coding/transforms-for-compression
level: intro
summary: Replace each maximal run of equal symbols by the symbol and the length of the run. It takes linear time and is lossless, and it gains only when runs are long.
model: word-ram
complexity:
  vars: {n: the length of the input, r: the number of maximal runs}
  time: {worst: Θ(n)}
  space: {extra: Θ(1), output: Θ(r)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1966
  people: [Solomon W. Golomb]
  note: Run lengths were coded long before 1966, but Golomb's paper of that year, Run-length encodings, gave an optimal code for them. PackBits and bzip2 use simple byte forms of the method.
prereqs: [lossless-compression]
see_also: [run-length-compression, burrows-wheeler-transform, move-to-front-transform, golomb-coding, delta-encoding, lz77, r-index, region-quadtree]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, 4th edition, Addison-Wesley, 2011
    locator: Section 5.5, Data Compression (run-length coding of bitstreams)
  - url: https://developer.apple.com/library/archive/technotes/tn/tn1023.html
    title: Apple Computer, Technical Note TN1023, Understanding PackBits
    locator: the packet format and the example of 24 unpacked bytes that pack to 15 bytes
  - paper: doi:10.1109/TIT.1966.1053907
    title: Solomon W. Golomb, Run-length encodings, IEEE Transactions on Information Theory 12(3), 1966
    locator: pages 399 to 401 (codes for the lengths of runs with a geometric distribution)
---

Run-length encoding (RLE) replaces each maximal run of equal symbols in a sequence by one copy of the symbol and the length of the run. The string `WWWWBWW` becomes the pairs $(W, 4), (B, 1), (W, 2)$. Encoding and decoding take one pass and $\Theta(n)$ time. The method gains only when the runs are long: on data with few runs, such as bilevel images, simple graphics, or the output of the [Burrows-Wheeler transform](/burrows-wheeler-transform/), the pairs are far fewer than the symbols, but on text with short runs the output is larger than the input. Byte formats such as PackBits and the first stage of bzip2 limit this growth. How to code the run lengths well, with a model of their distribution, is the [run-length compression](/run-length-compression/) problem.

## In plain words

Look for places where the same symbol repeats, one copy after the other. Instead of writing each copy, write the symbol once and say how many copies there are. "AAAAABBB" becomes "5 A, 3 B".

To decode, read each pair and write the symbol that many times.

This is a good method when the data has long stretches of the same value, such as a black and white scan of a page, which is mostly white. It is a bad method when values change all the time, because each single symbol now needs a count as well. Real formats add rules so that such data does not grow much.

## The problem

**Input.** A sequence $X = X[0 \ldots n-1]$ over an alphabet $\Sigma$.

**Output.** The list of pairs $(c_1, \ell_1), \ldots, (c_r, \ell_r)$ with $X = c_1^{\ell_1} c_2^{\ell_2} \cdots c_r^{\ell_r}$, each $\ell_k \ge 1$, and $c_k \ne c_{k+1}$. The last condition makes the runs maximal, and it makes the list unique: it is the canonical run-length form of $X$, and $r$ is the number of runs of $X$.

## The algorithm

```pseudo id=main
RLE-ENCODE(X[0 .. n − 1])
L1  i ← 0; out ← an empty list
L2  while i < n do
L3      j ← i
L4      while j < n and X[j] = X[i] do j ← j + 1
L5      append (X[i], j − i) to out
L6      i ← j                                ▷ X[j] starts a new run, or j = n
L7  return out
```

```pseudo id=decode
RLE-DECODE((c_1, ℓ_1), …, (c_r, ℓ_r))
D1  out ← an empty sequence
D2  for k ← 1 to r do
D3      append ℓ_k copies of c_k to out
D4  return out
```

**Byte formats.** The pairs must be written as bytes, and there are three common ways.

- **Count and byte.** Write each pair as a count byte $1 \ldots 255$ and the symbol byte; split a longer run into several pairs. Data with no runs doubles in size.
- **PackBits.** A header byte $h$, read as a signed number, starts each packet. If $0 \le h \le 127$, the next $h + 1$ bytes are literal. If $-127 \le h \le -1$, the next byte is repeated $1 - h$ times. The value $-128$ is a no-op that the encoder does not write. The encoder makes a repeat packet only for a run of 3 or more bytes, so the output is at most one byte longer per 128 input bytes.
- **The first stage of bzip2.** A run of 4 to 255 equal bytes becomes 4 copies followed by one byte with the number of extra copies, $0 \ldots 251$. A run shorter than 4 is left as it is. The decoder counts equal bytes, and after 4 of them reads a count.

## Example

The scan line `WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW` (67 symbols) has 7 runs:

$$(W, 12), (B, 1), (W, 12), (B, 3), (W, 24), (B, 1), (W, 14).$$

**PackBits.** Apple's Technical Note TN1023 gives this example of 24 bytes, in hexadecimal:

`AA AA AA 80 00 2A AA AA AA AA 80 00 2A 22 AA AA AA AA AA AA AA AA AA AA`

PackBits gives 15 bytes: `FE AA` (the run of 3, since $-2$ is `FE`), `02 80 00 2A` (3 literals), `FD AA` (the run of 4), `03 80 00 2A 22` (4 literals), and `F7 AA` (the run of 10, since $-9$ is `F7`).

**bzip2.** The first stage maps `AAAAAAA` (7 copies) to `AAAA` and the byte 3, and `AAA` to itself.

## Correctness

The encoder is correct by a loop invariant: at line L2, the pairs in $out$ are the canonical runs of $X[0 \ldots i-1]$, and $i = 0$ or $X[i] \ne X[i-1]$. Line L4 stops at the first $j$ with $X[j] \ne X[i]$, or at $n$, so $X[i \ldots j-1]$ is a maximal run that starts at $i$, and it has $j - i \ge 1$ symbols because $X[i] = X[i]$. Each step increases $i$, so the loop ends. When $i = n$, $out$ is the canonical form of $X$, and the decoder writes each run back. The full proof is below.

## Complexity

- **Time.** Each index $j$ is compared once in line L4 with a true result, and each run ends with at most one false comparison, so the encoder makes at most $n + r$ comparisons: $\Theta(n)$. The decoder writes $n$ symbols.
- **Space.** $O(1)$ beyond the output. The output has $r$ pairs, and $1 \le r \le n$ for $n \ge 1$.
- **Size.** With $b$ bits for each symbol and $b'$ bits for each count, the output has $r (b + b')$ bits, so it is smaller than the input only if $r (b + b') < n b$. For bytes with 1-byte counts, this needs an average run longer than 2.

## Properties

- **Lossless and canonical.** Each sequence has exactly one canonical run-length form, and the decoder inverts it.
- **Online.** The encoder outputs a pair as soon as a run ends, and needs to keep only the current symbol and its count.
- **Size depends on the runs, not on the frequencies.** The string $a^{50} b^{50}$ has 2 runs and $(ab)^{50}$ has 100, but both have the same symbol counts.
- **Not to be confused with sorted runs.** The runs of [replacement selection](/replacement-selection-run-length/) in external sorting are sorted runs, not runs of equal symbols.

## Variants and improvements

- **Escapes and thresholds.** Many formats write single symbols as they are and mark only long runs, with an escape symbol or with a run of $k$ copies that tells the decoder a count follows, as in the first stage of bzip2.
- **Binary runs.** For a bilevel image, the symbols alternate, so only the lengths need to be stored. Fax standards and Golomb codes code these lengths with a model of their distribution; see [run-length compression](/run-length-compression/) and [Golomb coding](/golomb-coding/).
- **Runs of zeros.** After the [move-to-front transform](/move-to-front-transform/), runs of zeros are the common case. bzip2 codes the length of each run of zeros in a base-2 number system with two digit symbols, RUNA and RUNB.
- **Two dimensions.** A [region quadtree](/region-quadtree/) is a run-length idea in two dimensions: it stores one value for each square block of equal pixels.
- **Indexing.** The run-length FM-index and the [r-index](/r-index/) store the BWT as its $r$ runs and take space proportional to $r$, not $n$.

## When to use it

Use RLE when the data has long runs: bilevel images, icons and simple graphics, masks, sparse bit vectors, and the output of the BWT and MTF stages. Use a byte format with literal packets, such as PackBits, when some parts of the data have no runs. Use a general compressor, such as [LZ77](/lz77/), when the data repeats longer patterns, not single symbols: RLE cannot see that `abcabcabc` repeats.

## Pitfalls

- **Expansion.** On data with no runs, a plain pair format doubles the size. Use literal packets or an escape.
- **Count overflow.** A count field of $k$ bits holds at most $2^k - 1$ (or $2^k$ if the count is stored minus one). Split longer runs, and make sure the decoder does not read a count of 0 as a run.
- **Off by one in the header.** In PackBits the literal count is $h + 1$ and the repeat count is $1 - h$. Writing $h$ or $-h$ instead loses one byte per packet.
- **The no-op header.** A PackBits decoder must skip the header $-128$ and read no data byte after it.
- **Reset after a count.** In the bzip2 form, the decoder must reset its count of equal bytes after it reads a count byte. Otherwise, for a run longer than 255, the copies after the count byte are counted together with the copies before it, and the decoder misses the next count byte.

## Implementations

## History

Coding the lengths of runs instead of the symbols is one of the oldest compression methods, used for television and facsimile signals. Golomb (1966) found the optimal prefix code for run lengths with a geometric distribution. The CCITT Group 3 fax standard (1980) codes the runs of white and black pixels of each scan line with fixed tables. Apple used the PackBits format in MacPaint and described it in Technical Note TN1023, and TIFF 6.0 (1992) includes it as compression scheme 32773. bzip2 (1996) applies a run-length stage before the Burrows-Wheeler sort and codes runs of zeros after the move-to-front stage.

## References
