---
tag: 7HJ2KD
kind: algorithm
slug: utf-16
name: UTF-16
aliases:
- UTF-16 encoding
- surrogate pairs
area: strings/text-processing-and-typesetting
level: intro
summary: Encode each scalar value below 10000 as one 16-bit unit and each larger one as a surrogate pair that carries 10 bits each of the value minus 10000. Surrogates themselves are not encoded.
model: word-ram
complexity:
  vars: {n: the number of 16-bit code units}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [unicode-code-point]
see_also: [utf-8, extended-grapheme-cluster, unicode-text-segmentation, variable-length-code, prefix-code, bitwise-operations]
sources:
  - book: isbn:9781936213344
    title: The Unicode Consortium, The Unicode Standard, Version 16.0.0, 2024
    locator: "Chapter 3: Section 3.8 Surrogates (D71 to D75) and Section 3.9 Unicode Encoding Forms (D76 Unicode scalar value, D91 UTF-16)"
  - url: https://www.rfc-editor.org/rfc/rfc2781
    title: P. Hoffman and F. Yergeau, UTF-16, an encoding of ISO 10646, RFC 2781, February 2000
    locator: Section 2 (UTF-16 definition, 2.1 Encoding UTF-16, 2.2 Decoding UTF-16) and Section 3 (Labelling UTF-16 text, 3.2 Byte order mark)
  - url: https://www.unicode.org/versions/Unicode16.0.0/core-spec/
    title: The Unicode Standard, Version 16.0.0, core specification (online)
    locator: Chapter 3, Sections 3.8 and 3.9; Chapter 23, Section 23.6 Surrogates Area
  - url: https://docs.python.org/3/library/codecs.html#standard-encodings
    title: Python documentation, codecs
    locator: Standard Encodings (utf_16, utf_16_be, utf_16_le) and Error Handlers
---

UTF-16 is the encoding form of Unicode that writes each [scalar value](/unicode-code-point/) as one or two 16-bit code units. A scalar value below 10000 (hexadecimal) is one unit with the same value. A larger one becomes a *surrogate pair*: a high surrogate in D800..DBFF and a low surrogate in DC00..DFFF, which together carry the 20 bits of the value minus 10000. The surrogate code points are reserved for this use, so they are never characters and are not encoded themselves. Windows, Java, JavaScript and .NET keep their strings in UTF-16.

## In plain words

The first version of Unicode had room for 65,536 characters, and many systems stored each character in 16 bits. When Unicode grew to more than a million code points, these systems needed a way to store the new characters without changing their 16-bit strings.

The answer was to set aside 2,048 of the 16-bit values. A character beyond the first 65,536 is written as two of these values: the first one comes from one block of 1,024 and the second one from another block of 1,024. Together they give 1,024 times 1,024 choices, which covers the new characters. Every other character is one 16-bit value, as before.

Because the two blocks are different, a program always knows whether a 16-bit value is a whole character, the first half of a pair or the second half.

## The problem

**Encoding.** The input is a scalar value $c$: $0 \le c \le \mathtt{10FFFF}$ and $c$ not in D800..DFFF. The output is its UTF-16 code unit sequence (D91).

**Decoding.** The input is a sequence $U$ of $n$ code units. A well-formed sequence is a concatenation of single units that are not surrogates and of pairs of a high surrogate followed by a low surrogate. The output is the sequence of scalar values. An *unpaired* surrogate, that is, a high surrogate without a low one after it or a low surrogate without a high one before it, is ill-formed. A strict decoder reports it, and a replacing decoder writes one U+FFFD REPLACEMENT CHARACTER for it.

**Bytes.** To store or send UTF-16, each unit becomes two bytes. UTF-16BE puts the high byte first and UTF-16LE the low byte first. The label "UTF-16" without a byte order allows a byte order mark, U+FEFF, at the start (RFC 2781, section 3.2). Its bytes FE FF mean big-endian and FF FE little-endian.

## The algorithm

```pseudo id=main
UTF16-ENCODE(c)
L1  if c < 0x10000 then return [c]
L2  v <- c - 0x10000
L3  return [0xD800 + (v >> 10), 0xDC00 + (v AND 0x3FF)]

UTF16-DECODE(U[0..n-1])
L4  out <- empty list; i <- 0
L5  while i < n do
L6      u <- U[i]
L7      if u < 0xD800 or u > 0xDFFF then append u to out; i <- i + 1
L8      else if u <= 0xDBFF and i + 1 < n and 0xDC00 <= U[i + 1] <= 0xDFFF then
L9          append 0x10000 + ((u - 0xD800) << 10) + (U[i + 1] - 0xDC00) to out; i <- i + 2
L10     else append 0xFFFD to out; i <- i + 1
L11 return out
```

Line L2 maps 10000..10FFFF onto the 20-bit range 0..FFFFF. Line L3 puts the high 10 bits into the high surrogate and the low 10 bits into the low surrogate. Line L10 handles a low surrogate that starts a step and a high surrogate that is not followed by a low surrogate. A strict decoder raises an error there instead.

The byte layer of the implementation turns each two bytes into a unit and then runs UTF16-DECODE. An odd final byte is a truncated unit and gives one more U+FFFD. If the unit before it is a high surrogate, Python counts the 3 bytes as one truncated sequence and writes one U+FFFD for them, and the implementation does the same.

## Example

Encode U+1F600 GRINNING FACE. Line L2 gives $v = \mathtt{F600}$, which is 0000111101 1000000000 in 20 bits. The high 10 bits are 3D and the low 10 bits are 200, so line L3 returns D83D DE00. In UTF-16BE the bytes are D8 3D DE 00, and in UTF-16LE they are 3D D8 00 DE.

| code point | UTF-16 code units |
|---|---|
| U+0041 | 0041 |
| U+20AC | 20AC |
| U+FFFD | FFFD |
| U+10000 | D800 DC00 |
| U+1F600 | D83D DE00 |
| U+10FFFF | DBFF DFFF |

Decode the units 0041 D83D 0042 DE00 D83D DE00 with replacement. The first unit is U+0041. D83D is a high surrogate followed by 0042, which is not a low surrogate, so it gives U+FFFD. Then comes U+0042. DE00 is a low surrogate at the start of a step, so it gives U+FFFD. The last two units form a pair, and line L9 gives $\mathtt{10000} + (\mathtt{3D} \ll 10) + \mathtt{200} = \mathtt{1F600}$. The output is U+0041 U+FFFD U+0042 U+FFFD U+1F600, the same as Python's `bytes.decode("utf-16-be", "replace")`.

## Correctness

The map of lines L1 to L3 is a bijection from the scalar values onto the well-formed one-character sequences. Values below 10000 that are not surrogates map to themselves. The values 10000..10FFFF map to pairs, because $v$ has exactly 20 bits and each half of it fits the 1,024 values of one surrogate block. The decoder keeps the invariant that the unit at $i$ is never the second unit of a pair that starts before $i$. So line L9 reads exactly the pairs, line L7 the single units, and line L10 exactly the unpaired surrogates, one at a time. Each step moves $i$ by 1 or 2, so the loop stops after at most $n$ steps. The full proof is in proofs/correctness.md.

## Complexity

In the [word-RAM model](/word-ram/), encoding takes $O(1)$ time per code point and decoding $\Theta(n)$ time for $n$ units, with $O(1)$ extra space besides the output.

| claim | value |
|---|---|
| units per code point | 1 below U+10000, 2 from U+10000 to U+10FFFF |
| bytes per code point | 2 or 4 |
| decoding time | $\Theta(n)$ |

Finding the $i$th code point of a UTF-16 string takes $\Theta(i)$ time in general, as in [UTF-8](/utf-8/), because of the pairs. Indexing by unit is $O(1)$, and that is what `String.charAt` in Java and string indexing in JavaScript do.

## Properties

- **Self-synchronizing.** Single units, high surrogates and low surrogates are three disjoint ranges, so from any unit at most one step back reaches the start of a code point.
- **Not order-preserving.** Comparing UTF-16 strings unit by unit does not sort them by code point. U+FF61 is the unit FF61, but U+10000 is D800 DC00, and D800 is smaller than FF61. The test `test_unit_order_is_not_code_point_order` checks this. A comparison can fix it by mapping the units D800..DFFF above the units E000..FFFF before it compares them.
- **Length in units.** Java's `String.length()` and JavaScript's `length` count units, so "😀".length is 2. The function `length_in_code_units` computes this value, and the test `test_length_in_code_units` checks it.
- **Byte order.** The two byte forms differ, so files and protocols need a label or a byte order mark. [UTF-8](/utf-8/) has no such issue.
- **Size.** Text in the BMP, including Chinese, Japanese and Korean, takes 2 bytes per character. ASCII text takes twice the space it takes in UTF-8.

## Variants and improvements

- **UCS-2.** The 16-bit form of the first Unicode versions, with no surrogate pairs. It covers only the BMP. Old code that treats each unit as a character works like UCS-2 and breaks supplementary characters into two.
- **WTF-16, or potentially ill-formed UTF-16.** Windows file names, Java strings and JavaScript strings may contain unpaired surrogates. Software that must keep such data exactly treats the units as opaque and converts it with a lossless form such as WTF-8.
- **UTF-32.** One 32-bit unit per scalar value. It gives $O(1)$ access to the $i$th code point but takes 4 bytes per character.
- **CESU-8.** The UTF-16 units of a string, each encoded as if it were a code point in a 3-byte UTF-8 form. Used inside some databases. It is not UTF-8.

## When to use it

Use UTF-16 when the platform already uses it: the Windows API, Java, JavaScript, .NET, and libraries built on them. Converting at each call costs time and can lose unpaired surrogates. For files and network data, prefer [UTF-8](/utf-8/), which has no byte order and is smaller for most markup and source code. Never use a unit count as the number of characters that a user sees. For that, count [extended grapheme clusters](/extended-grapheme-cluster/) with the rules of [text segmentation](/unicode-text-segmentation/).

## Pitfalls

- **Splitting a pair.** Cutting a string after a fixed number of units can leave a high surrogate at the end of one piece and a low surrogate at the start of the next. Both pieces are then ill-formed.
- **Unpaired surrogates from other sources.** A JavaScript string such as "\uD800" is valid in the language but cannot be encoded in UTF-8. Python's `encode("utf-8")` raises an error for it. The test `test_unpaired_surrogates` checks the replacing and strict decoders on such input.
- **Encoding a surrogate code point.** UTF16-ENCODE must reject D800..DFFF. Otherwise a lone U+DC00 and the second half of a pair would look the same. The test `test_surrogates_are_not_scalar_values` checks this.
- **The byte order mark.** U+FEFF at the start of a UTF-16 stream is a signature, not text. Strip it when you read with the plain "UTF-16" label, and do not add it when the label is UTF-16BE or UTF-16LE.
- **Odd byte counts.** A UTF-16 byte stream with an odd length is truncated. The test `test_odd_lengths` checks the treatment of the final byte.

## Implementations

## History

Unicode 1.0 (1991) was a 16-bit code, and early adopters such as Windows NT and Java stored each character in one 16-bit unit, the form now called UCS-2. When it became clear that 65,536 code points were not enough, Unicode 2.0 (1996) and an amendment to ISO/IEC 10646 defined UTF-16, which reserves 2,048 code points of the BMP as surrogates. The pairs give exactly 1,048,576 more code points, planes 1 to 16, which is why the Unicode codespace ends at 10FFFF. RFC 2781 (2000) registered the labels UTF-16, UTF-16BE and UTF-16LE for Internet use, and RFC 3629 (2003) limited [UTF-8](/utf-8/) to the same range.

## References
