---
tag: VC3H34
kind: problem
slug: endianness-conversion
name: Endianness conversion
aliases:
- byte swap
- byte order conversion
area: techniques/bit-tricks
level: intro
summary: Converting a word between big-endian and little-endian byte order.
model: word-ram
complexity:
  vars: {b: the number of bytes in a word}
  time: {worst: O(log b)}
prereqs: [bitwise-operations]
see_also: [bit-reversal, bit-packing, variable-byte-encoding, table-lookup]
sources:
  - paper: doi:10.1109/C-M.1981.220208
    title: Danny Cohen, On Holy Wars and a Plea for Peace, IEEE Computer 14(10), 1981
    locator: pp. 48 to 54
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition
    locator: Section 7-1, Reversing Bits and Bytes
  - url: "https://en.wikipedia.org/wiki/Endianness"
    title: Endianness, Wikipedia
    locator: sections Overview, Networking and Byte swapping
---

Endianness conversion is the problem of reversing the order of the bytes of a word, so that a value stored with its most significant byte first (big-endian) can be read on a machine that stores the least significant byte first (little-endian), or the other way round. The operation is called a byte swap. For a word of $b$ bytes it takes $O(\log b)$ shift-and-mask steps on the [word RAM](/word-ram/), and most processors do it in one instruction. Danny Cohen named the two orders big-endian and little-endian in 1981, after the two parties of Gulliver's Travels that broke their eggs at different ends.

## In plain words

A number that needs four bytes is stored in four cells of memory. One kind of machine puts the most important byte in the first cell. Another kind puts the least important byte first. Both are fine on their own. The trouble starts when one machine writes the bytes to a file or a network and the other machine reads them: it gets the bytes in the wrong order and sees a different number.

The fix is to swap the order of the bytes: the first and the last change places, then the second and the second to last, and so on. Inside each byte the bits stay as they are. A program does this when it reads or writes data in a fixed byte order that is not the order of its own machine.

## Definition

**Input.** A word $x$ of $b$ bytes, $x = \sum_{j=0}^{b-1} x_j \, 256^j$ with $0 \le x_j \le 255$; byte $x_0$ is the least significant.

**Output.**
$$ \operatorname{bswap}_b(x) = \sum_{j=0}^{b-1} x_j \, 256^{\,b-1-j} . $$

**Memory reading.** Let the bytes $m_0, m_1, \ldots, m_{b-1}$ be stored at increasing addresses. A little-endian machine loads the value $L = \sum_j m_j 256^j$, and a big-endian machine loads $B = \sum_j m_j 256^{b-1-j}$. So $B = \operatorname{bswap}_b(L)$: converting between the two readings of the same bytes is one byte swap. Like [bit reversal](/bit-reversal/), $\operatorname{bswap}_b$ is an involution and only moves bits, so it commutes with AND, OR and XOR, but not with addition or comparison.

## Variants

- **Sizes.** $b = 2, 4, 8$ for 16-, 32- and 64-bit integers. For $b = 1$ there is nothing to do.
- **Host to network order.** Network byte order is big-endian, the order of the headers of the Internet protocols. The C functions `htonl`, `htons`, `ntohl` and `ntohs` convert 32- and 16-bit values; on a big-endian host they do nothing, and on a little-endian host they swap.
- **Mixed order.** The PDP-11 stored a 32-bit value as two 16-bit words, the more significant word first, each word little-endian. The value 0x0A0B0C0D is then stored as the bytes 0B 0A 0D 0C.
- **Bit order.** The order of the bits inside a byte is not visible to a byte-addressed program. It matters on serial links and in bit-packed formats, where it is a [bit reversal](/bit-reversal/) problem, not a byte swap.
- **Converting a whole array.** Swap each element. With SIMD instructions a byte shuffle swaps many elements in one step.
- **Floating-point values.** Swap the bytes of the bit pattern as an integer of the same size, not the value.

## Examples

| $b$ | $x$ | $\operatorname{bswap}_b(x)$ |
| --- | --- | --- |
| 2 | 0x1234 | 0x3412 |
| 4 | 0x0A0B0C0D | 0x0D0C0B0A |
| 4 | 0x12345678 | 0x78563412 |
| 8 | 0x0102030405060708 | 0x0807060504030201 |

The value 0x0A0B0C0D is stored as the bytes 0A 0B 0C 0D on a big-endian machine and as 0D 0C 0B 0A on a little-endian machine. A little-endian machine that reads the four big-endian bytes 0A 0B 0C 0D loads 0x0D0C0B0A, and one byte swap gives the right value.

A non-example: the decimal value 258 is 0x0102 in 16 bits, and its byte swap is 0x0201 = 513. Swapping the decimal digits, which would give 852, has nothing to do with byte order.

## Known algorithms

- **Shifts and masks, one byte at a time.** For 32 bits, `(x << 24) | ((x & 0xFF00) << 8) | ((x >> 8) & 0xFF00) | (x >> 24)`, with unsigned 32-bit arithmetic. This is $b$ terms, $O(b)$ operations.
- **Swap stages.** Swap the two halves, then the two quarters inside each half, down to bytes. For 64 bits:

  ```
  x = (x << 32) | (x >> 32)
  x = (x & 0x0000FFFF0000FFFF) << 16 | (x >> 16) & 0x0000FFFF0000FFFF
  x = (x & 0x00FF00FF00FF00FF) << 8  | (x >> 8)  & 0x00FF00FF00FF00FF
  ```

  This takes $\lg b$ stages of $O(1)$ operations, so $O(\log b)$ time.
- **Rotations.** With a rotate instruction, a 32-bit swap is $(\operatorname{rotl}(x, 24) \mathbin{\&} \mathtt{0xFF00FF00}) \mathbin{|} (\operatorname{rotl}(x, 8) \mathbin{\&} \mathtt{0x00FF00FF})$, two rotations, two ANDs and one OR.
- **One instruction.** BSWAP on x86 (since the 80486), REV on ARM, and a compiler builtin such as `__builtin_bswap32` in GCC and Clang, which also recognize the shift-and-mask pattern above and compile it to that instruction.
- **Assemble from bytes.** Code that reads a big-endian 32-bit value from a byte array as `p[0] << 24 | p[1] << 16 | p[2] << 8 | p[3]` is correct on every host, with no test of the host order.

## Bounds

- **Upper bound.** $O(\log b)$ time on the [word RAM](/word-ram/) with shifts and Boolean operations, by the swap stages; $O(1)$ with a byte-swap instruction.
- **Lower bound.** This page claims only the trivial $\Omega(1)$. As a circuit, a byte swap is only wiring and needs no gates.

## Reductions

- **Bit reversal reduces to it.** $\operatorname{rev}_{8b}(x) = \operatorname{bswap}_b(r(x))$, where $r$ reverses the bits inside each byte; see [bit reversal](/bit-reversal/).
- **It is a fixed permutation of bit positions.** So it is a special case of the bit permutations that Warren treats in Chapter 7, done by masked swaps of fields.

## Applications

- **Network protocols.** Packet headers carry integers in big-endian order, so a little-endian host swaps each field it reads or writes.
- **File formats.** Each binary format fixes a byte order, or marks it, as the byte order mark of UTF-16 does with the bytes FE FF or FF FE.
- **Integer compression.** Formats such as [variable-byte encoding](/variable-byte-encoding/) fix the order of the bytes of each code, so the decoder does not depend on the host.
- **Sort keys.** A big-endian unsigned integer compares like its byte string, so storing keys big-endian lets a byte-wise comparison, as in a radix tree or a key-value store, give numeric order.

## References
