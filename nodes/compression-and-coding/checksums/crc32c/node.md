---
tag: 7288F4
kind: algorithm
slug: crc32c
name: CRC-32C
aliases:
- Castagnoli CRC
- iSCSI CRC
area: compression-and-coding/checksums
level: intro
summary: CRC-32 with the Castagnoli polynomial, which has a dedicated CPU instruction on modern processors.
model: word-ram
complexity:
  vars: {n: the number of message bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1993
  people: [Guy Castagnoli, Stefan Bräuer, Martin Herrmann]
  note: Castagnoli, Bräuer and Herrmann searched for 24-bit and 32-bit generators with a large minimum distance; their polynomial 0x1EDC6F41 became CRC-32C.
prereqs: [cyclic-redundancy-check, crc-generator-polynomial]
see_also: [table-driven-crc, slicing-by-8, clmul-crc-folding, crc-error-detection-guarantees, minimum-distance, hamming-distance, internet-checksum]
sources:
  - paper: doi:10.1109/26.231911
    title: Guy Castagnoli, Stefan Bräuer and Martin Herrmann, Optimization of cyclic redundancy-check codes with 24 and 32 parity bits, IEEE Transactions on Communications 41(6), 1993
    locator: pp. 883 to 892 (the search for 32-bit generators with a large minimum distance)
  - url: https://www.rfc-editor.org/rfc/rfc3720
    title: J. Satran et al., RFC 3720, Internet Small Computer Systems Interface (iSCSI), 2004
    locator: Section 12.1 (HeaderDigest and DataDigest, generator 0x11EDC6F41) and Appendix B.4 (CRC examples)
  - url: https://www.rfc-editor.org/rfc/rfc4960
    title: R. Stewart (ed.), RFC 4960, Stream Control Transmission Protocol, 2007
    locator: Section 6.8 (the CRC32c checksum) and Appendix B (CRC32c checksum calculation)
  - url: https://www.rfc-editor.org/rfc/rfc3309
    title: J. Stone, R. Stewart and D. Otis, RFC 3309, Stream Control Transmission Protocol (SCTP) Checksum Change, 2002
    locator: Sections 1 and 2 (the move of SCTP from Adler-32 to CRC32c)
  - url: https://users.ece.cmu.edu/~koopman/crc/crc32.html
    title: Philip Koopman, CRC polynomial zoo, 32-bit polynomials
    locator: Entries 0x82608edb (IEEE 802.3) and 0x8f6e37a0 (CRC-32C), maximum data lengths for each Hamming distance
  - url: https://reveng.sourceforge.io/crc-catalogue/all.htm
    title: Greg Cook, Catalogue of parametrised CRC algorithms
    locator: Entry CRC-32/ISCSI (check 0xE3069283, residue 0xB798B438)
---

CRC-32C is the 32-bit [cyclic redundancy check](/cyclic-redundancy-check/) with the generator 0x1EDC6F41, found by Castagnoli, Bräuer and Herrmann in 1993. It has the same structure as the CRC-32 of Ethernet and zip, but a different polynomial, which detects more errors in messages of a few kilobytes. iSCSI, SCTP, ext4 and Btrfs use it, and x86 CPUs with SSE4.2 have an instruction that computes it. Its catalogue name is CRC-32/ISCSI.

## In plain words

All CRCs work the same way: divide the message by a fixed number in carry-free arithmetic, and keep the remainder. The choice of the divisor decides which errors are always caught.

The common CRC-32 uses a divisor that was chosen in the 1970s. In 1993 Castagnoli and his co-authors searched by computer for a better divisor of the same size. Their divisor always catches up to five wrong bits in a message of about 600 bytes, where the old one always catches only three, and both miss about one random error in four billion. Because it is better and Intel put it into the CPU, new protocols and file systems use CRC-32C.

## The problem

The input is a byte string of $n$ bytes. The output is its CRC with these parameters, from the CRC-32/ISCSI entry of the catalogue:

| width | poly | init | refin | refout | xorout | check | residue |
|---|---|---|---|---|---|---|---|
| 32 | 0x1EDC6F41 | 0xFFFFFFFF | true | true | 0xFFFFFFFF | 0xE3069283 | 0xB798B438 |

The generator in other notations is 0x82F63B78 (reversed) and 0x8F6E37A0 (Koopman); see [CRC generator polynomial](/crc-generator-polynomial/). The model is the [word RAM](/word-ram/).

## The algorithm

The implementation is the reflected [table-driven CRC](/table-driven-crc/) with the reversed poly 0x82F63B78.

```pseudo id=main
CRC32C(data, c = 0)                     ▷ pass c = a previous CRC to continue it
L1  for v ← 0 to 255: T[v] ← v shifted right 8 times, with an XOR of 0x82F63B78 after each 1 bit that falls out
L2  reg ← c XOR 0xFFFFFFFF
L3  for each byte v of data do
L4      reg ← (reg >> 8) XOR T[(reg XOR v) AND 255]
L5  return reg XOR 0xFFFFFFFF
```

The x86 instruction `CRC32` (SSE4.2) does the loop of lines L3 and L4 for 1, 2, 4 or 8 bytes. It does not do lines L2 and L5, so software must XOR 0xFFFFFFFF before and after. The instruction has a latency of several cycles, so fast code runs three streams in parallel and joins them with the combine method of the table-driven CRC, or uses [CRC folding](/clmul-crc-folding/).

**Byte order on the wire.** iSCSI and SCTP send the CRC least significant byte first. RFC 3720 says that bit 7 of the lowest numbered byte is the most significant bit of the message polynomial, which is the reflected order of the catalogue. With this byte order, the CRC of a whole codeword leaves the register at the residue 0xB798B438.

## Example

The first three bytes of `123456789`. The register starts at 0xFFFFFFFF.

| byte | index | T[index] | register |
|---|---|---|---|
| `1` (0x31) | 0xCE | 0x6FF599E3 | 0x6F0A661C |
| `2` (0x32) | 0x2E | 0x8CC531F9 | 0x8CAA3B9F |
| `3` (0x33) | 0xAC | 0xEF087A76 | 0xEF84D04D |

After all 9 bytes and the final XOR, the result is 0xE3069283, the check value.

RFC 3720, Appendix B.4, gives these test vectors. The RFC lists the four CRC bytes in the order of transmission, so 0x8A9136AA appears as `aa 36 91 8a`.

| data | CRC-32C |
|---|---|
| 32 bytes of 0x00 | 0x8A9136AA |
| 32 bytes of 0xFF | 0x62A8AB43 |
| 32 bytes 0x00, 0x01, …, 0x1F | 0x46DD794E |
| 32 bytes 0x1F, 0x1E, …, 0x00 | 0x113FDB5C |
| a 48-byte iSCSI Read (10) command PDU | 0xD9963A56 |

## Correctness

The code is the reflected table-driven CRC with init and xorout all ones, so it is correct by the proof on that page. The tests also show the guarantee that makes CRC-32C better: no codeword of 1056 bits (1024 data bits and 32 check bits) has weight 2 or 4, and none has odd weight, because the generator has 18 terms and so the factor $(x + 1)$. A search with pairs of syndromes $x^i \bmod G$ shows this in under a second. The same search finds a codeword of weight 5 for the IEEE CRC-32 at this length. The full proof is below.

## Complexity

- **Time.** $\Theta(n)$ with one table lookup for each byte. With the CRC32 instruction, about one instruction for each 8 bytes; with three parallel streams or carry-less folding, the speed is limited by the load of the data.
- **Space.** One table of 1 KiB, or none with the instruction.

## Properties

- **Hamming distance.** From the CRC zoo of Philip Koopman: CRC-32C has Hamming distance 6 for data words up to 5243 bits and 4 up to 2147483615 bits. The IEEE CRC-32 has distance 6 only up to 268 bits, 5 up to 2974 bits, and 4 up to 91607 bits. See [CRC error-detection guarantees](/crc-error-detection-guarantees/).
- **Odd errors.** The generator has the factor $(x + 1)$, so CRC-32C detects every error with an odd number of flipped bits. The IEEE CRC-32 has no such factor.
- **Bursts.** As every CRC of width 32, it detects every burst of 32 bits or less.
- **Random errors.** For long random errors, it misses a fraction of about $2^{-32}$, as the IEEE CRC-32 does. See [undetected error probability](/undetected-error-probability/).
- **No security.** It is affine, and any CRC value can be reached by changing 4 bytes.

## Variants and improvements

- **Table-driven and slicing-by-8.** The portable software forms. See [table-driven CRC](/table-driven-crc/) and [slicing-by-8](/slicing-by-8/).
- **SSE4.2 CRC32 instruction.** Intel added it with SSE4.2 in 2008. It computes only CRC-32C, not the IEEE CRC-32.
- **ARMv8 CRC32C instructions.** ARM has instructions for both CRC-32 and CRC-32C.
- **Carry-less folding.** With PCLMULQDQ, [CRC folding](/clmul-crc-folding/) computes CRC-32C at many bytes per cycle, and it combines with the CRC32 instruction.
- **Masked CRC.** Some storage formats store a rotated and offset CRC-32C so that the CRC of data that holds CRCs is not trivial.

## When to use it

Use CRC-32C for a new protocol or a new storage format that needs a 32-bit check against accidental errors. It detects more errors than the IEEE CRC-32 in messages up to several kilobytes, and it is faster on x86 and ARM. Use the IEEE CRC-32 only when a format such as zip, gzip, PNG or Ethernet needs it. For long messages or high error rates, use a 64-bit CRC; against an attacker, use a [message authentication code](/message-authentication-code/).

## Pitfalls

- **Wrong polynomial.** Code for CRC-32 with 0xEDB88320 does not give CRC-32C. Use 0x82F63B78 in the reflected loop.
- **Missing XOR around the instruction.** The CRC32 instruction alone gives the register, not the CRC. XOR 0xFFFFFFFF before the first byte and after the last byte.
- **Byte order of the digest.** iSCSI and SCTP send the low byte first. An implementation that writes the CRC big-endian breaks the constant residue and fails against other implementations.
- **Not the IEEE CRC.** The name "CRC-32" alone means the IEEE polynomial. Always write "CRC-32C" or "Castagnoli".

## Implementations

## History

Castagnoli, Bräuer and Herrmann published their search for good 24-bit and 32-bit CRC generators in 1993. The iSCSI working group chose one of their polynomials for the header and data digests, and RFC 3720 (2004) specifies it. RFC 3309 (2002) moved SCTP from Adler-32 to CRC-32C, and RFC 4960 (2007) gives the code in its Appendix B. Intel added the CRC32 instruction for this polynomial with SSE4.2 in 2008. Later, the ext4 file system used CRC-32C for its metadata checksums, and Btrfs used it as its default checksum. In 2004 Koopman and Chakravarty published tables of the Hamming distance of many CRCs, which show the gain of CRC-32C at medium lengths.

## References
