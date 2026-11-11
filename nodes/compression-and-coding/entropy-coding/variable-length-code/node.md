---
tag: 8GCPPW
kind: concept
slug: variable-length-code
name: Variable-length code
aliases:
- Variable-length encoding
area: compression-and-coding/entropy-coding
level: intro
summary: A code whose input blocks or output words have different lengths. It saves space on frequent symbols, but one bit error can shift the parse, and byte alignment trades space for speed.
prereqs: [prefix-code]
see_also: [huffman-coding, tunstall-coding, arithmetic-coding, variable-byte-encoding, uniquely-decodable-code, deflate, elias-gamma-coding, golomb-coding]
sources:
  - paper: doi:10.1109/TIT.1984.1056931
    title: T. J. Ferguson and J. H. Rabinowitz, Self-synchronizing Huffman codes, IEEE Transactions on Information Theory 30(4), 1984
    locator: The synchronizing codewords of a Huffman code and the choice of a code with given lengths that has one
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 5 (Data compression, codes with codewords of different lengths, Sections 5.1 to 5.8)
  - url: https://www.rfc-editor.org/rfc/rfc3629
    title: F. Yergeau, UTF-8, a transformation format of ISO 10646, RFC 3629, 2003
    locator: Section 3 (the byte patterns of UTF-8) and Section 10 (the fact that a character boundary can be found from any byte)
---

A variable-length code maps source blocks to code words where the input blocks, the output words, or both do not all have the same length. Frequent symbols get short codewords and rare ones get long codewords, so the mean length can approach the [entropy](/shannon-entropy/) of the source, which no fixed-length code can do in general. The price is in the decoder: it must find the boundaries between codewords, which a [prefix code](/prefix-code/) makes easy, and a single bit error can move every later boundary until the decoder falls back in step. Codes that keep their codewords aligned to bytes give up some compression to make decoding fast and to limit the damage.

## In plain words

A fixed code spends the same number of bits on every letter, whether it is common or rare. A variable-length code spends few bits on common letters and more on rare ones, so most messages come out shorter. Morse code works this way: the common letter E is a single dot. The cost is that the reader no longer knows where each letter ends by counting bits. The code must be built so that the letters can still be separated, and in the best codes each letter is known the moment its last bit arrives. If one bit is damaged, the reader may cut the stream at the wrong places for a while. Good codes get back in step after a few letters; some never do. Codes that use whole bytes are a little longer but are faster to read and lose less after an error.

## The idea

Notation. $\Sigma$ is the source alphabet, of size $\sigma$, and the code alphabet is $\{0, 1\}$. A source block is a string over $\Sigma$, and a code word is a bit string. $\ell(\cdot)$ is a length. The model, where one is named, is a memoryless source with law $p$ on $\Sigma$.

**Three shapes.** A code cuts the source into blocks and maps each block to a code word. Either side may have variable length.

| shape | source blocks | code words | examples |
|---|---|---|---|
| fixed-to-variable | one symbol, or $n$ symbols | different lengths | [Huffman coding](/huffman-coding/), the Shannon code, [Elias gamma](/elias-gamma-coding/) and [Golomb codes](/golomb-coding/) for integers |
| variable-to-fixed | different lengths, from a dictionary | all the same length | [Tunstall coding](/tunstall-coding/), the codes of LZW in each phase |
| variable-to-variable | different lengths | different lengths | run-length coding followed by a Huffman code, the LZ77 and Huffman stages of [DEFLATE](/deflate/) |

In a fixed-to-variable code, the codewords must be decodable: a [uniquely decodable](/uniquely-decodable-code/) code, and in practice a prefix code, which loses nothing by the [Kraft inequality](/kraft-inequality/). With probability law $p$, the best such code for single symbols has mean length between $H$ and $H + 1$ bits; on blocks of $n$ symbols the overhead per symbol falls to $1/n$. In a variable-to-fixed code the source blocks must form a complete prefix-free set, so that every source string can be parsed; the goal is long blocks on average, and each code word has the same length, so the output is easy to index and an error stays in one word. [Arithmetic coding](/arithmetic-coding/) is the limit of the first shape, with the whole message as one block.

**Synchronization and error propagation.** A decoder of a prefix code is in a state, a node of the code tree. If a bit flips, the decoder goes to a wrong node and may cut the following bits at the wrong places. It is back in step when the damaged parse and the true parse end a codeword at the same bit; from then on, the two decodings agree. Until then, it outputs wrong symbols, and possibly a wrong number of them, which shifts all later symbols if their positions matter.

- In a fixed-length code, the damage is always one symbol.
- In the code $\{0, 10, 110, 111\}$, every 0 ends a codeword, whatever the state of the decoder. So the parse is back in step at the first 0 after the error.
- Some complete prefix codes never recover from some errors. In the code $\{10, 000, 001, 011, 111, 0100, 0101, 1100, 1101\}$, if the second bit of the codeword $10$ flips, the two parses can follow each other forever without ending a codeword at the same bit. The same happens for a flip while the true parse is at the node $11$ or $01$ of the tree. The implementation on this page finds such cases by a search over pairs of tree nodes.

A *synchronizing word* of a code is a string of codewords after which the decoder is at the root, from any start state. Ferguson and Rabinowitz (1984) studied Huffman codes with this property, and showed that among the prefix codes with the same codeword lengths, and so the same compression, one can often choose a code that has a short synchronizing codeword. The choice of code, not only the lengths, decides how errors spread.

**Byte-aligned codes.** A code whose codewords are whole bytes, such as [variable-byte encoding](/variable-byte-encoding/) for integers or UTF-8 for Unicode, wastes up to 7 bits per codeword against a bit-level code. In return, the decoder reads bytes, not bits, which is faster on real hardware, and a lost or damaged byte affects one codeword. UTF-8 goes further: a byte that starts a character ($0xxxxxxx$, $110xxxxx$, $1110xxxx$ or $11110xxx$) can always be told apart from a continuation byte ($10xxxxxx$), so a decoder can start at any byte and find the next character boundary.

## Examples

**One bit error in a short message.** Encode $abacd$ with $\{a \mapsto 0, b \mapsto 10, c \mapsto 110, d \mapsto 111\}$: $0100110111$, 10 bits, with codeword ends after bits 1, 3, 4, 7 and 10.

| flipped bit (from 0) | damaged stream | decoded | wrong symbols before the parses meet |
|---|---|---|---|
| 0 | 1100110111 | $c\,a\,c\,d$ | 1 ($c$ in place of $a\,b$) |
| 1 | 0000110111 | $a\,a\,a\,a\,c\,d$ | 2 ($a\,a$ in place of $b$) |
| 5 | 0100100111 | $a\,b\,a\,b\,a\,d$ | 2 ($b\,a$ in place of $c$) |
| 7 | 0100110011 | $a\,b\,a\,c\,a$, then $11$ is left over | not measured: the stream ends inside a codeword first |

The number of decoded symbols changes (4 and 6 in place of 5), so a decoder that counts symbols will also misplace all the later ones.

**Measured error propagation.** The code on this page draws 2000 random messages of 200 symbols, flips one random bit in the first half, and counts the decoded symbols from the damaged one to the first common codeword end (seed 1).

| code | source law | mean symbols until in step | largest | never in step |
|---|---|---|---|---|
| fixed, 2 bits | uniform on 4 | 1.0 | 1 | 0 |
| $\{0, 10, 110, 111\}$ | $1/2, 1/4, 1/8, 1/8$ | 1.655 | 6 | 0 |
| $\{1, 01, 000, 0010, 0011\}$ | $0.4, 0.2, 0.2, 0.1, 0.1$ | 2.7155 | 10 | 0 |
| $\{00, 10, 11, 010, 011\}$ | $0.4, 0.2, 0.2, 0.1, 0.1$ | 1.9295 | 10 | 0 |

The last two rows are both Huffman codes for the same source, with the same mean length of 2.2 bits per symbol, but the second one recovers from an error about 30% faster. For the code above that never recovers from some errors, 121 of 1000 trials (seed 3) did not get back in step before the end of the message.

## Where it is used

- **Entropy coding in codecs.** [DEFLATE](/deflate/) (zip, gzip, PNG) codes literals, lengths and distances with prefix codes; JPEG uses Huffman codes for its coefficients. The codes are sent as lists of lengths and rebuilt as canonical codes. These formats limit the damage of errors by blocks and checksums, not by the code itself.
- **Integer codes in indexes.** Inverted indexes and columnar stores code gaps and counts with [Elias](/elias-gamma-coding/), [Golomb](/golomb-coding/) or byte-aligned codes, choosing between size and decoding speed.
- **Text encodings.** UTF-8 is a byte-aligned variable-length code that is self-synchronizing by design.
- **Variable-to-fixed codes** such as [Tunstall codes](/tunstall-coding/) are used where a fixed output size helps: random access into compressed data, and channels where a bit error must not spread.
- **Streams with errors.** Video codecs and other formats meant for lossy channels insert resynchronization markers, and some use reversible variable-length codes that can be decoded from both ends, so that the part after an error can be read backwards from the next marker.

## References
