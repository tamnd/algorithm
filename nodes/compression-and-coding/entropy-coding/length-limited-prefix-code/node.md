---
tag: D5F6KM
kind: problem
slug: length-limited-prefix-code
name: Length-limited prefix code problem
aliases:
- length-restricted prefix code
- length-limited Huffman code
area: compression-and-coding/entropy-coding
level: advanced
summary: Find a prefix code of least weighted length whose codewords are at most L bits long. Package-merge solves it in O(nL) time; DEFLATE and JPEG use fast heuristics.
prereqs: [optimal-prefix-code, huffman-coding]
see_also: [package-merge, canonical-huffman-code, deflate, jpeg-compression, kraft-inequality, optimal-alphabetic-code]
sources:
  - paper: doi:10.1145/79147.79150
    title: Lawrence L. Larmore and Daniel S. Hirschberg, A fast algorithm for optimal length-limited Huffman codes, Journal of the ACM 37(3), 1990
    locator: pages 464 to 473
  - paper: doi:10.1145/3342555
    title: Alistair Moffat, Huffman coding, ACM Computing Surveys 52(4), 2019
    locator: Section 4.1, Length-limited codes (Algorithm 3 and the example of Figure 6)
  - paper: doi:10.1137/0122024
    title: T. C. Hu and K. C. Tan, Path length of binary search trees, SIAM Journal on Applied Mathematics 22(2), 1972
    locator: pages 225 to 234
  - paper: doi:10.1109/tit.1974.1055176
    title: David C. Van Voorhis, Constructing codes with bounded codeword lengths, IEEE Transactions on Information Theory 20(2), 1974
    locator: pages 288 to 290
  - paper: doi:10.1007/s00453-001-0060-4
    title: Ruy Luiz Milidiú and Eduardo Sany Laber, Bounding the inefficiency of length-restricted prefix codes, Algorithmica 31(4), 2001
    locator: pages 513 to 529
  - url: https://www.rfc-editor.org/rfc/rfc1951
    title: P. Deutsch, RFC 1951, DEFLATE Compressed Data Format Specification version 1.3, 1996
    locator: Section 3.2.7 (code lengths 0 to 15 and the code length alphabet)
  - url: https://www.w3.org/Graphics/JPEG/itu-t81.pdf
    title: ITU-T Recommendation T.81, Digital compression and coding of continuous-tone still images, 1992
    locator: Annex C (BITS lists code lengths 1 to 16) and Annex K, Clause K.2 (the adjustment of the code lengths to 16 bits)
  - paper: doi:10.1006/jagm.1998.0955
    title: Baruch Schieber, Computing a minimum weight k-link path in graphs with the concave Monge property, Journal of Algorithms 29(2), 1998
    locator: pages 204 to 222
  - url: https://github.com/libjpeg-turbo/libjpeg-turbo/blob/main/src/jchuff.c
    title: libjpeg-turbo, jchuff.c
    locator: function jpeg_gen_optimal_table (the reserved symbol and the adjustment of Clause K.2)
  - url: https://github.com/madler/zlib/blob/develop/trees.c
    title: Jean-loup Gailly and Mark Adler, zlib, trees.c
    locator: function gen_bitlen (the repair of lengths above the limit)
---

The length-limited prefix code problem asks for a [prefix code](/prefix-code/) of least weighted length, as in the [optimal prefix code problem](/optimal-prefix-code/), with the added constraint that no codeword is longer than a given $L$ bits. A Huffman code can have codewords of up to $n - 1$ bits, but file formats cap the length so that the lengths fit in a small field and the decoder tables stay small: [DEFLATE](/deflate/) allows 15 bits and JPEG 16. The [package-merge](/package-merge/) algorithm of Larmore and Hirschberg (1990) solves the problem exactly in $O(nL)$ time. Most encoders use a cheaper repair of the Huffman code instead, which is not always optimal but loses very little.

## In plain words

A Huffman code gives rare symbols long codewords. If some symbols are very rare, a codeword can be 20 or 30 bits long. Many formats do not allow that: the decoder may store the length of each codeword in four bits, or decode with a table that has one entry for each possible bit pattern of the longest length.

So the question is: what is the best code if no codeword may be longer than a fixed limit? The rare symbols must move up to shorter codewords. To make room for them, some common symbols must move down to longer codewords. The best way to do this trade is the length-limited problem. An exact method exists, and simple repairs come very close.

## Definition

**Input.** Weights $w_1, \ldots, w_n \ge 0$ for $n \ge 2$ symbols, and an integer limit $L$. Here $n$ is the alphabet size, written $\sigma$ in the notation of this area, and the weights are the probabilities or counts of a memoryless source.

**Output.** Integer lengths $1 \le l_i \le L$ that satisfy the [Kraft inequality](/kraft-inequality/) $\sum_i 2^{-l_i} \le 1$, and so are the lengths of a prefix code.

**Goal.** Minimize $\sum_i w_i l_i$.

**Feasibility.** A code exists if and only if $2^L \ge n$, that is $L \ge \lceil \log_2 n \rceil$: with $l_i = \lceil \log_2 n \rceil$ for all $i$ the Kraft sum is at most 1, and with $n > 2^L$ it exceeds 1 for any lengths at most $L$. If $L$ is at least the longest length of some Huffman code, the Huffman code is a solution, so the problem is only new for $\lceil \log_2 n \rceil \le L < L_{\text{Huff}}$.

**Why the limits are 15 and 16.** In DEFLATE, RFC 1951 sends each Huffman code as a list of code lengths, coded with a code length alphabet whose symbols 0 to 15 are the lengths themselves, so a length cannot exceed 15. In JPEG, a Huffman table is the list BITS of the number of codewords of each length 1 to 16, followed by the symbols, so a length cannot exceed 16. JPEG also reserves the codeword of all ones. Short limits also bound the size of the lookup tables of a fast decoder.

## Variants

- **Optimal versus heuristic.** The exact problem has polynomial algorithms. The heuristics of zlib and JPEG repair a Huffman code on the counts of each length, with one step for each pair of codewords that are too long, which can be $\Theta(n)$ steps. They are not always optimal.
- **Alphabetic codes with a limit.** The codewords must also keep the order of the symbols. This is a limited [optimal alphabetic code](/optimal-alphabetic-code/), a search tree of bounded height. The interval dynamic program for alphabetic codes then gets an extra index for the height.
- **$D$-ary codes.** The same problem with $D$ code letters; package-merge works with packages of $D$ items.
- **A reserved codeword.** JPEG needs a code with Kraft sum below 1, with the codeword of all ones unused. Adding a dummy symbol of weight 1 before the construction does this.

## Examples

Take the weights of Moffat (2019), $W = (20, 17, 6, 3, 2, 2, 2, 1, 1, 1)$, with $n = 10$, so $L \ge 4$.

| limit $L$ | optimal lengths | cost | JPEG adjustment | cost |
|---|---|---|---|---|
| none (Huffman) | 1, 2, 4, 5, 5, 5, 5, 5, 6, 6 | 140 | | |
| 6 | 1, 2, 4, 5, 5, 5, 5, 5, 6, 6 | 140 | no change | 140 |
| 5 | 2, 2, 3, 4, 4, 4, 4, 4, 5, 5 | 142 | 1, 2, 5, 5, 5, 5, 5, 5, 5, 5 | 144 |
| 4 | 2, 2, 4, 4, 4, 4, 4, 4, 4, 4 | 146 | 2, 2, 4, 4, 4, 4, 4, 4, 4, 4 | 146 |
| 3 | no code, since $2^3 < 10$ | | | |

For $L = 5$, the Huffman code has one codeword of each length 1, 2 and 4, five of length 5 and two of length 6. The JPEG step removes the two codewords of length 6: one takes the length 5 of their parent, and the codeword of length 4 becomes the parent of two codewords of length 5. The result has one codeword of length 1, one of length 2 and eight of length 5, and costs 144. The optimal code makes the two heaviest symbols longer instead, and costs 142. Both are above the Huffman cost of 140.

On random inputs where the limit cuts the Huffman code by 1 to 3 bits, with 8 to 40 symbols and very skewed weights, the JPEG adjustment was optimal in about a fifth of the cases, and its mean loss against the optimum was below 0.4 percent, with a worst case near 5 percent, in a run of 300 random inputs. The tests below check a smaller run of the same kind.

## Known algorithms

- **Package-merge.** Larmore and Hirschberg (1990) reduce the problem to the coin collector's problem and solve it by repeated pairing and merging, in $O(nL)$ time and space, or $O(n)$ space with a more complex version. Katajainen, Moffat and Turpin (1995) need only $O(L^2)$ extra space, and Turpin and Moffat (1995) give a reverse form in $O(n(L - \log_2 n + 1))$ time. See [package-merge](/package-merge/).
- **Dynamic programming.** Hu and Tan (1972) and Van Voorhis (1974) gave the first exact algorithms. A simple dynamic program sorts the weights in non-increasing order and builds the tree level by level, choosing how many of the next symbols become leaves at each depth. With the state (depth, symbols placed, free nodes) it takes $O(L n^3)$ time; the implementation below uses it as a check.
- **The JPEG adjustment.** Build a Huffman code and count the codewords of each length in BITS. For each length $i > L$, from the longest down, while BITS$[i] > 0$: find the longest length $j < i - 1$ in use, then set BITS$[i] \mathrel{-}= 2$, BITS$[i - 1] \mathrel{+}= 1$, BITS$[j + 1] \mathrel{+}= 2$ and BITS$[j] \mathrel{-}= 1$. Two leaves at depth $i$ leave; one takes the place of their parent and the other joins a leaf of depth $j$, which becomes an inner node. The Kraft sum stays 1. Then the symbols, in the order of their Huffman lengths, take the new lengths in order (T.81, Annex K, Clause K.2).
- **The zlib repair.** zlib clips all lengths above the limit to the limit. Then, once for each two clipped nodes, it takes a leaf at the longest length below the limit, moves it one level down, and puts one leaf of the longest length next to it as its sibling. Then it gives the new lengths to the symbols in order of weight.
- **Kraft-based heuristics.** Other methods scale the weights up, or fix lengths from $\lceil \log_2 (1/p_i) \rceil$ and spend the Kraft slack greedily. Moffat (2019) notes that such methods give costs close to or equal to the minimum in practice.

## Bounds

- **Cost.** The optimum is at least the Huffman cost and, for probabilities, at least the entropy $H$. Milidiú and Laber (2001) bound the loss against the Huffman cost and show that it is small except when $L$ is very close to $\lceil \log_2 n \rceil$.
- **Monotone lengths.** Some optimal solution gives a heavier symbol a codeword that is not longer, by the same swap as for Huffman codes. So the problem is to choose a non-decreasing length list, which is what the dynamic program and package-merge exploit.
- **Time.** Package-merge takes $O(nL)$ time; since $L < n$ is the only interesting range, this is $O(n^2)$ at worst and $O(n \log n)$ when $L = O(\log n)$.

## Reductions

- **Coin collector's problem.** Give each symbol $i$ one coin for each depth $d = 1, \ldots, L$, of face value $2^{-d}$ and cost $w_i$. Choose coins of total face value $n - 1$ at least cost. The number of chosen coins of symbol $i$ is its length $l_i$, because $\sum_i \sum_{d \le l_i} 2^{-d} = n - \sum_i 2^{-l_i}$, which is $n - 1$ exactly when the Kraft sum is 1. Package-merge solves this coin problem for face values that are powers of 2.
- **Shortest paths with a fixed number of edges.** The problem can be cast as a shortest path with exactly $L$ edges in a graph with the concave [Monge property](/monge-property/). Schieber (1998) solves that path problem fast and gives an algorithm for length-limited codes that is faster than $O(nL)$ for large $L$.

## Applications

- **DEFLATE.** zlib, gzip and PNG build each dynamic Huffman code with the 15-bit limit, and the code length code with a 7-bit limit, using the zlib repair.
- **JPEG.** An encoder that builds optimized Huffman tables, as libjpeg does with its optimize option, uses the Annex K adjustment to 16 bits with the reserved codeword. The libjpeg source notes that the difference from an optimal limited code is usually less than a hundredth of a percent of the file size.
- **Fast decoders.** A decoder with a single lookup table of $2^L$ entries needs a small $L$, so a coder that controls its own format can choose a limit well below 15 for speed.

## References
