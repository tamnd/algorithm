---
tag: 59B85A
kind: algorithm
slug: utf-8
name: UTF-8
aliases:
- UTF-8 encoding
area: strings/text-processing-and-typesetting
level: intro
summary: Encode each scalar value in one to four bytes. The count of leading one bits in the first byte gives the length, and each continuation byte starts with the bits 10.
model: word-ram
complexity:
  vars: {n: the number of bytes of the encoded string}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [unicode-code-point, prefix-code]
see_also: [utf-16, simd-utf-8-validation, punycode, variable-byte-encoding, variable-length-code, uniquely-decodable-code, deterministic-finite-automaton, bitwise-operations]
sources:
  - book: isbn:9781936213344
    title: The Unicode Consortium, The Unicode Standard, Version 16.0.0, 2024
    locator: "Chapter 3, Section 3.9 Unicode Encoding Forms: D92 (UTF-8), Table 3-7 (well-formed UTF-8 byte sequences), D93b (maximal subpart) and Section 3.9.6 U+FFFD Substitution of Maximal Subparts"
  - url: https://www.rfc-editor.org/rfc/rfc3629
    title: F. Yergeau, UTF-8, a transformation format of ISO 10646, RFC 3629, November 2003
    locator: Section 3 (UTF-8 definition), Section 4 (Syntax of UTF-8 byte sequences) and Section 10 (Security considerations)
  - url: https://www.unicode.org/versions/Unicode16.0.0/core-spec/
    title: The Unicode Standard, Version 16.0.0, core specification (online)
    locator: Chapter 3, Section 3.9
  - url: https://docs.python.org/3/library/codecs.html#error-handlers
    title: Python documentation, codecs
    locator: Error Handlers (strict, replace, surrogatepass)
---

UTF-8 is the encoding form of Unicode that writes each [scalar value](/unicode-code-point/) as a sequence of one to four bytes. The bytes 00 to 7F stand for themselves, so ASCII text is valid UTF-8 without change. In a longer sequence, the first byte says how many bytes follow, and every following byte has the form 10xxxxxx, so the code is a [prefix code](/prefix-code/) and a reader can find the start of a character from any position. UTF-8 is the encoding of most web pages and of the text files and APIs of most current systems.

## In plain words

A computer stores text as bytes, and one byte holds only 256 values, but Unicode has more than a million code points. UTF-8 uses one byte for the common English letters, digits and signs, and two, three or four bytes for everything else.

Each byte says what role it plays. A byte that begins with the bit 0 is a whole character. A byte that begins with 110, 1110 or 11110 starts a character of two, three or four bytes. A byte that begins with 10 continues a character. The free bits of all the bytes, put together, give the number of the character.

Because the roles are visible in the bytes, a program can jump into the middle of a text and find the next character start, and a search for an English word never matches inside a longer character.

## The problem

**Encoding.** The input is a scalar value $c$, that is, an integer with $0 \le c \le \mathtt{10FFFF}$ that is not in D800..DFFF. The output is its UTF-8 byte sequence.

**Decoding.** The input is a byte string $B$ of length $n$. If $B$ is well-formed, the output is the sequence of scalar values that it encodes. If it is not, a strict decoder reports an error, and a replacing decoder writes U+FFFD REPLACEMENT CHARACTER for each bad piece and goes on.

Table 3-7 of the core specification lists all well-formed sequences. Each row is a product of byte ranges, and bytes after the second are always in 80..BF.

| code points | byte 1 | byte 2 | byte 3 | byte 4 |
|---|---|---|---|---|
| U+0000..U+007F | 00..7F | | | |
| U+0080..U+07FF | C2..DF | 80..BF | | |
| U+0800..U+0FFF | E0 | A0..BF | 80..BF | |
| U+1000..U+CFFF | E1..EC | 80..BF | 80..BF | |
| U+D000..U+D7FF | ED | 80..9F | 80..BF | |
| U+E000..U+FFFF | EE..EF | 80..BF | 80..BF | |
| U+10000..U+3FFFF | F0 | 90..BF | 80..BF | 80..BF |
| U+40000..U+FFFFF | F1..F3 | 80..BF | 80..BF | 80..BF |
| U+100000..U+10FFFF | F4 | 80..8F | 80..BF | 80..BF |

The bytes C0, C1 and F5..FF never occur. The narrow second byte ranges after E0, ED, F0 and F4 exclude the overlong forms, the surrogates and the values above 10FFFF.

The replacing decoder follows the practice of section 3.9.6: a *maximal subpart* (D93b) is the longest prefix of a well-formed sequence that starts at the current position, or a single byte if no well-formed sequence starts with that byte, and each maximal subpart becomes one U+FFFD. The standard recommends this practice but does not require it for conformance.

## The algorithm

```pseudo id=main
UTF8-ENCODE(c)
L1  if c < 0x80 then return [c]
L2  if c < 0x800 then return [0xC0 OR (c >> 6), 0x80 OR (c AND 0x3F)]
L3  if c < 0x10000 then return [0xE0 OR (c >> 12), 0x80 OR ((c >> 6) AND 0x3F), 0x80 OR (c AND 0x3F)]
L4  return [0xF0 OR (c >> 18), 0x80 OR ((c >> 12) AND 0x3F), 0x80 OR ((c >> 6) AND 0x3F), 0x80 OR (c AND 0x3F)]

UTF8-DECODE(B[0..n-1])
L5  out <- empty list; i <- 0
L6  while i < n do
L7      b <- B[i]
L8      if b < 0x80 then append b to out; i <- i + 1; continue
L9      (k, lo, hi) <- LEAD-INFO(b)
L10     if k = 0 then append 0xFFFD to out; i <- i + 1; continue
L11     c <- b AND (0x7F >> (k + 1)); j <- 1
L12     while j <= k do
L13         (lo2, hi2) <- (lo, hi) if j = 1 else (0x80, 0xBF)
L14         if i + j >= n or B[i + j] < lo2 or B[i + j] > hi2 then break
L15         c <- (c << 6) OR (B[i + j] AND 0x3F); j <- j + 1
L16     if j = k + 1 then append c to out else append 0xFFFD to out
L17     i <- i + j
L18 return out
```

LEAD-INFO$(b)$ reads Table 3-7. It returns the number $k$ of bytes that follow a first byte $b$ and the range $lo..hi$ of the second byte, or $k = 0$ if $b$ is in 80..C1 or F5..FF. Line L11 keeps the payload bits of the first byte: 5 bits for $k = 1$, 4 for $k = 2$ and 3 for $k = 3$. Line L14 stops at the first byte that is missing or out of its range, and that byte is not consumed: it is read again as the start of the next sequence. A strict decoder raises an error at line L10 or in the else branch of line L16 instead of writing U+FFFD.

## Example

Encode U+20AC EURO SIGN. It is at least 800 and below 10000, so line L3 applies. In binary, 20AC is 0010 000010 101100. The three bytes are 1110 0010, 10 000010 and 10 101100, that is, E2 82 AC.

| text | code points | UTF-8 bytes |
|---|---|---|
| A | U+0041 | 41 |
| é | U+00E9 | C3 A9 |
| € | U+20AC | E2 82 AC |
| 😀 | U+1F600 | F0 9F 98 80 |
| U+10FFFF | U+10FFFF | F4 8F BF BF |

Decode, with replacement, the 13 bytes 61 F1 80 80 E1 80 C2 62 80 63 80 BF 64.

| bytes | what happens | output |
|---|---|---|
| 61 | ASCII | U+0061 |
| F1 80 80 | F1 needs 3 more bytes, but E1 is not in 80..BF | U+FFFD |
| E1 80 | E1 needs 2 more bytes, but C2 is not in 80..BF | U+FFFD |
| C2 | C2 needs 1 more byte, but 62 is ASCII | U+FFFD |
| 62 | ASCII | U+0062 |
| 80 | a continuation byte cannot start a sequence | U+FFFD |
| 63 | ASCII | U+0063 |
| 80 | as above | U+FFFD |
| BF | as above | U+FFFD |
| 64 | ASCII | U+0064 |

The output is U+0061 U+FFFD U+FFFD U+FFFD U+0062 U+FFFD U+0063 U+FFFD U+FFFD U+0064, the same as Python's `bytes.decode("utf-8", "replace")`. The overlong form C0 AF of "/" gives two U+FFFD, because C0 starts no sequence, and the surrogate form ED A0 80 gives three, because A0 is out of range after ED.

## Correctness

Each row of Table 3-7 is the set of encodings of one range of scalar values. Lines L1 to L4 put the payload bits of $c$ behind the fixed prefixes, and the range limits of the rows are the conditions that $c$ is in the range of its line, is not a surrogate and is at most 10FFFF. So encoding is a bijection from the scalar values onto the sequences of the table. No sequence is a proper prefix of another, because the first byte fixes the length. The decoder keeps the invariant that the bytes before $i$ have been turned into output and $i$ is the start of a sequence or of a maximal subpart. In each pass it either matches a whole row and writes the value of line L15, or stops at the first byte that cannot extend a prefix of a well-formed sequence. Because each row is a product of ranges, that prefix is the maximal subpart. Every pass moves $i$ forward by at least one byte. The full proof is in proofs/correctness.md.

## Complexity

In the [word-RAM model](/word-ram/), with $n$ the number of bytes:

- **Encoding** costs $O(1)$ per code point, and the output has 1 to 4 bytes per code point.
- **Decoding** reads each byte at most twice: once inside a sequence, and once more if it ended a failed sequence at line L14. So it takes $\Theta(n)$ time, and the output has at most $n$ code points.
- **Space.** Besides the output, both use $O(1)$ space.

| claim | value |
|---|---|
| bytes per code point | 1 for U+0000..U+007F, 2 up to U+07FF, 3 up to U+FFFF, 4 up to U+10FFFF |
| decoding time | $\Theta(n)$ |
| U+FFFD per maximal subpart | exactly 1 |

Branch-free decoders that work on one byte at a time, and [vectorized validators](/simd-utf-8-validation/) that check 16 to 64 bytes per step, have the same asymptotic cost with much smaller constants.

## Properties

- **ASCII-compatible.** The bytes 00..7F encode only U+0000..U+007F, and they never occur inside a longer sequence. A program that looks for "/" or for a zero byte works on UTF-8 without change.
- **Self-synchronizing.** A continuation byte has the form 10xxxxxx and a first byte does not, so from any position at most 3 steps back reach the start of the code point. The function `code_point_start` does this, and the test `test_code_point_start` checks it.
- **Prefix code.** No encoding is a prefix of another, so a byte search for a well-formed string finds only matches that start and end at character boundaries.
- **Order-preserving.** Sorting UTF-8 strings byte by byte sorts them by code point. The test `test_byte_order_is_code_point_order` checks this. [UTF-16](/utf-16/) does not have this property.
- **No byte order.** The unit is a byte, so there are no big-endian and little-endian forms. A leading EF BB BF (the encoding of U+FEFF) is allowed but carries no information.
- **Size.** Text in Latin script takes little more than 1 byte per character, and Chinese, Japanese and Korean text 3 bytes per character, where UTF-16 needs 2.

## Variants and improvements

- **Original UTF-8 (RFC 2279).** It allowed sequences of up to 6 bytes for values up to 7FFFFFFF. RFC 3629 limited UTF-8 to 4 bytes and 10FFFF, the range of UTF-16.
- **Modified UTF-8.** Java's serialization and JNI write U+0000 as C0 80 and code points above U+FFFF as two 3-byte sequences, one for each UTF-16 surrogate. It is not UTF-8, and a strict decoder rejects it.
- **CESU-8.** The same treatment of supplementary code points as Modified UTF-8, but U+0000 is the byte 00.
- **WTF-8 and surrogatepass.** They allow the 3-byte forms of lone surrogates, so that any sequence of 16-bit units, valid or not, survives a round trip. Python's error handler "surrogatepass" encodes U+D800 as ED A0 80.
- **DFA decoding.** A [deterministic finite automaton](/deterministic-finite-automaton/) with 8 states and a reject state accepts exactly the well-formed byte strings. The states are "at a sequence start", "1, 2 or 3 bytes still needed", and the four states for the narrow second byte ranges after E0, ED, F0 and F4. A table-driven decoder runs it with one lookup per byte.
- **SIMD validation.** The [Keiser-Lemire validator](/simd-utf-8-validation/) checks the same rules with vector table lookups on nibbles.

## When to use it

Use UTF-8 for files, network protocols and the storage of text unless an interface demands another form. It is the required encoding of JSON text exchanged between systems, and the default of HTML5, XML and most programming languages. Use [UTF-16](/utf-16/) when an API (Windows, Java, JavaScript) already holds text in it. Use UTF-32 inside a program when you need $O(1)$ access to the $i$th code point, and remember that the $i$th code point is not the $i$th [grapheme cluster](/extended-grapheme-cluster/). For domain names, which must be ASCII, use [Punycode](/punycode/).

## Pitfalls

- **Overlong forms.** A lax decoder that only reads the payload bits accepts C0 AF as "/" and C0 AE as ".". RFC 3629 section 10 describes a check that rejects the bytes 2F 2E 2E 2F ("/../") but lets 2F C0 AE 2E 2F through, which such a decoder then reads as "/../". The rows of Table 3-7 forbid these forms, and the test `test_replacement_check_values` checks them.
- **Surrogates and large values.** ED A0 80 (U+D800) and F4 90 80 80 (above 10FFFF) are ill-formed. A decoder that only counts the leading one bits lets them through.
- **Truncated input.** A buffer can end inside a sequence. A streaming decoder must keep up to 3 bytes for the next buffer, not replace them with U+FFFD.
- **Different numbers of U+FFFD.** Section 3.9.6 is not required for conformance, and other decoders write one U+FFFD per bad byte or per bad run. Do not compare replaced output between libraries.
- **Length in bytes is not length in characters.** Cutting a UTF-8 string after a fixed number of bytes can split a code point. Move the cut back to a code point start, and better to a grapheme cluster boundary.
- **Encoding lone surrogates.** A Python `str` can hold U+D800. `encode("utf-8")` raises an error for it, and the test `test_surrogates_rejected_or_passed` checks this and the "surrogatepass" form.

## Implementations

## History

Ken Thompson designed UTF-8 with Rob Pike in September 1992, as an improvement on a proposal of X/Open for a file system safe transformation format of the Universal Character Set. The goals were ASCII compatibility, no zero bytes or "/" inside multi-byte sequences, self-synchronization, and a first byte that gives the length. Their Plan 9 system changed to it soon after, and Pike and Thompson described it in their paper at the USENIX Winter 1993 conference. RFC 2044 (1996) and RFC 2279 (1998) registered it for Internet use with sequences of up to 6 bytes. RFC 3629 (2003) restricted it to the 4-byte range that UTF-16 can also reach, and Unicode defines the same set of sequences in D92 and Table 3-7.

## References
