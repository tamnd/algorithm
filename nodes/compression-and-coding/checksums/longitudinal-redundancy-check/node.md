---
tag: QJA1A5
kind: algorithm
slug: longitudinal-redundancy-check
name: Longitudinal redundancy check
aliases:
- LRC
- block parity
- longitudinal parity
area: compression-and-coding/checksums
level: intro
summary: Parity bits computed per column over a block, which together with row parity detect multi-bit errors.
model: word-ram
complexity:
  vars: {n: the number of message bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1978
  people: [ISO]
  note: ISO 1155 specified longitudinal parity, the XOR of the characters of a message, as a check character for information interchange. The ASCII mode of Modbus later used the two's complement of the byte sum under the same name.
prereqs: [parity-bit]
see_also: [checksum, additive-checksum, cyclic-redundancy-check, product-codes, internet-checksum, fletcher-checksum, burst-errors, undetected-error-probability]
sources:
  - url: https://modbus.org/docs/Modbus_over_serial_line_V1_02.pdf
    title: Modbus Organization, MODBUS over serial line specification and implementation guide V1.02, 2006
    locator: Section 2.5.2.2 (LRC checking in ASCII mode, the two's complement of the 8-bit sum of the message bytes, without the colon and CR LF) and Section 6.2.1 (LRC generation, the C function)
  - paper: "ISO 1155:1978, Information processing, Use of longitudinal parity to detect errors in information messages"
    title: Use of longitudinal parity to detect errors in information messages
    locator: The block check character, one parity bit for each bit position of the characters of a message
  - paper: doi:10.1109/TDSC.2007.70216
    title: Theresa C. Maxino and Philip J. Koopman, The effectiveness of checksums for embedded control networks, IEEE Transactions on Dependable and Secure Computing 6(1), 2009
    locator: Sections on the XOR checksum and the two's complement addition checksum (Hamming distance 2, the undetected two-bit errors in one column, and the effect of the top bit)
---

A longitudinal redundancy check (LRC) is a check byte computed over a block of bytes, column by column: bit $j$ of the check depends only on bit $j$ of each byte. Its classic form is the XOR of all bytes, one [parity bit](/parity-bit/) for each bit position. The ASCII mode of Modbus uses a different function under the same name, the two's complement of the sum of the bytes. Both detect every single-bit error and every burst of at most 8 bits, but both miss some pairs of errors in the same bit column.

## In plain words

Write the bytes of a message one under the other, so that the bits form columns. For each column, add one bit that makes the number of 1 bits in that column even. These eight bits form one extra byte, the check byte, and the sender appends it. The receiver does the same and compares.

One flipped bit makes its column wrong, so it is always caught. Two flipped bits in the same column cancel out, so they are missed. The Modbus form adds the bytes instead, so carries move between columns, but it still misses many pairs in one column.

## The problem

Input: a message of $n$ bytes $M[0], \ldots, M[n-1]$.

Output: one check byte $v$, such that the receiver, given the message and $v$, can detect the common errors of a serial line: single flipped bits and short bursts. The cost must be one cheap operation per byte, with no tables, so that it fits on a small controller.

## The algorithm

```pseudo id=main
LRC-XOR(M[0..n−1])                      ▷ longitudinal parity, as in ISO 1155
L1  x ← 0
L2  for i ← 0 to n − 1 do
L3      x ← x XOR M[i]
L4  return x

LRC-MODBUS(M[0..n−1])                   ▷ Modbus ASCII mode
L5  s ← 0
L6  for i ← 0 to n − 1 do
L7      s ← (s + M[i]) mod 256
L8  return (256 − s) mod 256

CHECK-XOR(M, v)
L9  return LRC-XOR(M) XOR v = 0

CHECK-MODBUS(M, v)
L10 return (M[0] + ⋯ + M[n−1] + v) mod 256 = 0
```

In the XOR form the check byte is the parity of each column. In the Modbus form it is the value that makes the sum of all bytes of the frame, check byte included, a multiple of 256. In Modbus ASCII the bytes travel as hexadecimal characters: a frame is a colon, two hex characters for each byte and for the LRC, then CR LF. The LRC is computed on the bytes before they are turned into characters.

## Example

Read 3 holding registers starting at address 0x006B from device 0x11: the bytes 11 03 00 6B 00 03. The Modbus specification gives no complete frame with its LRC, so the values below are computed by hand and checked by the implementation.

| i | M[i] | x after L3 | s after L7 |
|---|---|---|---|
| 0 | 0x11 | 0x11 | 0x11 |
| 1 | 0x03 | 0x12 | 0x14 |
| 2 | 0x00 | 0x12 | 0x14 |
| 3 | 0x6B | 0x79 | 0x7F |
| 4 | 0x00 | 0x79 | 0x7F |
| 5 | 0x03 | 0x7A | 0x82 |

The XOR form returns 0x7A. The Modbus form returns $256 - 0x82 = 0x7E$, and the ASCII frame is `:1103006B00037E` followed by CR LF. The receiver adds the six bytes and 0x7E: $0x82 + 0x7E = 0x100 \equiv 0$, so it accepts. If the last byte arrives as 0x02, the sum is 0xFF and the frame is rejected.

## Correctness

Lines L2 and L3 keep the invariant $x = M[0] \oplus \cdots \oplus M[i-1]$, so line L4 returns the XOR of all bytes. Lines L6 and L7 keep $s = \sum_{t<i} M[t] \bmod 256$, and line L8 returns the only $v \in 0..255$ with $s + v \equiv 0$. Each loop runs $n$ times, so both terminate.

What each form misses, with the check byte counted as part of the frame:

- **XOR form.** An error is missed if and only if every bit column has an even number of errors. So it detects every error of odd weight, and every burst of at most 8 bits, because such a burst puts at most one error in each column. It misses two errors in the same column, such as bit 3 of two different bytes, which is a burst of 9 bits when the bytes are adjacent.
- **Modbus form.** An error changes the sum by $D = \sum \pm 2^j$, with $+$ when a 0 becomes a 1, and is missed if and only if $D \equiv 0 \pmod{256}$. A single error gives $D = \pm 2^j \ne 0$. Two errors are missed if and only if they are in the same column and flip in opposite directions, or both are in bit 7, where $128 + 128 = 256$. Every burst of at most 8 bits is detected, in either bit order on the line.

The [proof](proofs/correctness.md) gives the details, and the tests check the rules for pairs and for bursts exhaustively on a frame of 7 bytes.

## Complexity

Time $\Theta(n)$ with one XOR or one addition per byte, and $\Theta(1)$ extra space. On a word RAM with $w$-bit words the XOR form takes $\Theta(n/w)$ word operations: XOR the message a word at a time, then fold the word, for example $x \oplus (x \gg 32)$, then $\gg 16$, then $\gg 8$. The sum form can also add words, but the byte sums of the lanes must be kept apart, for example by adding the bytes into wider lanes and reducing at the end.

## Properties

- Both forms are linear: the XOR form over GF(2), the Modbus form over the integers modulo 256. So the check of a concatenation is the XOR, or the sum, of the checks of the parts, and the order of the bytes does not matter: swapping two bytes is never detected.
- Both have [Hamming distance](/hamming-distance/) 2, with any message length: some errors of two bits are always missed.
- For uniformly random errors, each form misses a fraction of about $2^{-8}$, the same as any 8-bit check. For two random errors in a frame of $N$ bytes, the XOR form misses the pair with probability $(N - 1)/(8N - 1)$, about 1 in 8.
- With a parity bit on each character, the vertical redundancy check, the XOR form becomes two-dimensional parity, a [product code](/product-codes/) of distance 4 that can correct one error.

## Variants and improvements

- **LRC plus VRC.** Old character protocols sent each 7-bit character with a parity bit and ended a block with an LRC character. A single error then fails one row and one column, which locates it.
- **Other sums.** The Intel HEX format ends each record with the two's complement of the sum of its bytes, the same function as the Modbus LRC. An [additive checksum](/additive-checksum/) with 16-bit words, or with [one's complement](/ones-complement/) arithmetic as in the [Internet checksum](/internet-checksum/), is the same idea with wider columns.
- **Position-dependent sums.** The [Fletcher checksum](/fletcher-checksum/) adds a second sum of the running sums, so that swapped bytes and pairs in one column are mostly detected, at about twice the cost.
- **CRC.** The Modbus RTU mode uses CRC-16/MODBUS instead of the LRC. A [cyclic redundancy check](/cyclic-redundancy-check/) of 16 bits detects all errors of 1, 2 and 3 bits in Modbus-sized frames and all bursts of up to 16 bits.

## When to use it

Use an LRC when a protocol or a file format requires it, as in Modbus ASCII, in some meter and card reader protocols, and in Intel HEX records. Use it on very small devices, where a byte loop without tables matters. For a new design, a CRC of the same width costs only a 256-entry table and gives much stronger guarantees.

## Pitfalls

- **Two functions, one name.** "LRC" means the XOR form in some documents and the Modbus sum form in others. They give different values: 0x7A and 0x7E in the example above. Check which one the protocol uses.
- **Modbus ASCII: bytes, not characters.** The LRC covers the binary bytes of the address, the function code and the data. It does not cover the colon or CR LF, and it is not computed on the hex characters.
- **Sum, then negate.** The Modbus LRC is $(-\text{sum}) \bmod 256$, not the sum and not its one's complement. In C, an 8-bit unsigned sum and a negation give the right value; a sum in a wider type must be masked to 8 bits.
- **Top-bit pairs.** In the Modbus form, any two errors in bit 7 of two bytes cancel, because the carry out of bit 7 is lost. Data whose high bits change together, such as signed values near zero, is weakly protected.
- **Errors on the line, not in the bytes.** In Modbus ASCII the line carries characters. A flipped bit often makes a character that is not a hex digit, which the parser rejects. The analysis of the LRC applies to the bytes after decoding.

## Implementations

## History

Longitudinal parity is older than the standards that name it: magnetic tape and punched tape stored a parity bit for each character and a check character for each block. ISO 1155 standardized the XOR form for messages of information interchange. The Modbus protocol, published by Modicon in 1979, used the name LRC for the two's complement of the byte sum in its ASCII mode, and the Modbus serial line guide V1.02 (2006) gives the C function. Maxino and Koopman (2009) measured both functions against Fletcher, Adler and CRC checks and recommended a CRC when the cost allows.

## References
