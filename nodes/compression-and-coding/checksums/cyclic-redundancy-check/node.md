---
tag: JEXCDN
kind: algorithm
slug: cyclic-redundancy-check
name: Cyclic redundancy check
aliases:
- CRC
- CRC-32
- polynomial checksum
area: compression-and-coding/checksums
level: intro
summary: Remainder of the message divided by a generator polynomial over GF(2), used in link-layer and storage error detection.
model: word-ram
complexity:
  vars: {n: the number of message bytes, r: the CRC width}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1961
  people: [W. Wesley Peterson, D. T. Brown]
  note: Peterson and Brown described cyclic codes for error detection and the shift-register circuit that computes the check bits.
prereqs: [checksum, gf2-polynomial-arithmetic]
see_also: [table-driven-crc, crc-generator-polynomial, crc-error-detection-guarantees, crc32c, cyclic-code, error-detection, internet-checksum, cryptographic-hash-function]
sources:
  - paper: doi:10.1109/JRPROC.1961.287814
    title: W. W. Peterson and D. T. Brown, Cyclic codes for error detection, Proceedings of the IRE 49(1), 1961
    locator: pp. 228 to 235 (the code as a remainder of division by the generator, the shift-register encoder, and the classes of errors that are detected)
  - url: http://www.ross.net/crc/download/crc_v3.txt
    title: Ross N. Williams, A painless guide to CRC error detection algorithms, version 3, 1993
    locator: Sections 9 to 15 (the shift register, the reflected form, and the Rocksoft parameter model with width, poly, init, refin, refout, xorout and check)
  - url: https://reveng.sourceforge.io/crc-catalogue/all.htm
    title: Greg Cook, Catalogue of parametrised CRC algorithms
    locator: Entries CRC-8/SMBUS, CRC-16/ARC, CRC-16/IBM-3740, CRC-16/KERMIT, CRC-16/XMODEM, CRC-16/MODBUS, CRC-32/ISO-HDLC, CRC-32/ISCSI, CRC-32/BZIP2, CRC-32/MPEG-2 and CRC-64/XZ (parameters, check and residue)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 5 (cyclic codes, the generator polynomial, systematic encoding by division, and encoding with a shift register)
---

A cyclic redundancy check (CRC) is the remainder of the message, read as a polynomial with bit coefficients, after division by a fixed generator polynomial of degree $r$. The sender appends the $r$ remainder bits, and the receiver divides again to check them. A shift register of $r$ bits computes the remainder in one pass, so a CRC is cheap in hardware and in software. Ethernet, HDLC, zip, gzip, PNG, SATA, iSCSI and many file systems use a CRC to detect accidental errors.

## In plain words

Think of the message as one very long binary number. Divide it by a fixed short number, but with a special kind of division in which you never carry or borrow. Keep only the remainder. That remainder is the CRC. Send it after the message.

The receiver does the same division on what arrives. If the remainder does not match, some bits changed. The divisor is chosen so that the typical faults of a wire or a disk, such as one flipped bit, two flipped bits, or a short run of damaged bits, always change the remainder.

A machine does not need to keep the whole message for the division. It keeps a small register of the size of the divisor, and it updates the register as each bit arrives.

## The problem

The input is a byte string of $n$ bytes and the parameters of one CRC. The output is the CRC value of the string. The parameters follow the model of Ross Williams (1993), which the [CRC catalogue](https://reveng.sourceforge.io/crc-catalogue/all.htm) of Greg Cook uses for more than one hundred named CRCs.

| parameter | meaning |
|---|---|
| width | $r$, the degree of the generator and the number of check bits |
| poly | the generator $G(x)$ without its $x^r$ term, as an $r$-bit word, top bit for $x^{r-1}$ |
| init | the register value before the first bit |
| refin | if true, each byte enters least significant bit first |
| refout | if true, the final register is bit-reversed |
| xorout | a word that is XORed into the result |
| check | the CRC of the 9 ASCII bytes `123456789`, to test an implementation |
| residue | the register after a whole codeword with no error, before xorout |

The polynomials are in [GF(2)[x]](/gf2-polynomial-arithmetic/): the sum is XOR, and the product has no carries. The model is the [word RAM](/word-ram/) with $r$ at most the word size, so one step on the register is $O(1)$ time.

## The algorithm

The register holds a polynomial of degree less than $r$. Each message bit enters at the top end. When the bit that falls out of the top, XORed with the input bit, is 1, the register is XORed with poly. This is the remainder step of [polynomial long division](/polynomial-long-division/).

```pseudo id=main
CRC(data, width, poly, init, refin, refout, xorout)
L1  top ← 2^(width − 1), mask ← 2^width − 1
L2  reg ← init
L3  for each byte v of data do
L4      if refin then v ← the 8 bits of v in reverse order
L5      for i ← 7 down to 0 do                 ▷ bit i of v, top bit first
L6          f ← bit i of v XOR (reg AND top ≠ 0)
L7          reg ← (reg · 2) AND mask
L8          if f = 1 then reg ← reg XOR poly
L9  if refout then reg ← the width bits of reg in reverse order
L10 return reg XOR xorout
```

When refin and refout are both true, most software keeps the register in reversed bit order. Then it shifts right, XORs each byte into the low end, and uses the reversed poly, for example `0xEDB88320` for CRC-32. This form gives the same value with no reversal of bytes. The implementation has both forms and tests that they agree.

| name | width | poly | init | refin | refout | xorout | check |
|---|---|---|---|---|---|---|---|
| CRC-8/SMBUS | 8 | 0x07 | 0x00 | false | false | 0x00 | 0xF4 |
| CRC-16/ARC | 16 | 0x8005 | 0x0000 | true | true | 0x0000 | 0xBB3D |
| CRC-16/IBM-3740 | 16 | 0x1021 | 0xFFFF | false | false | 0x0000 | 0x29B1 |
| CRC-16/KERMIT | 16 | 0x1021 | 0x0000 | true | true | 0x0000 | 0x2189 |
| CRC-16/XMODEM | 16 | 0x1021 | 0x0000 | false | false | 0x0000 | 0x31C3 |
| CRC-16/MODBUS | 16 | 0x8005 | 0xFFFF | true | true | 0x0000 | 0x4B37 |
| CRC-32/ISO-HDLC | 32 | 0x04C11DB7 | 0xFFFFFFFF | true | true | 0xFFFFFFFF | 0xCBF43926 |
| CRC-32/ISCSI | 32 | 0x1EDC6F41 | 0xFFFFFFFF | true | true | 0xFFFFFFFF | 0xE3069283 |
| CRC-32/BZIP2 | 32 | 0x04C11DB7 | 0xFFFFFFFF | false | false | 0xFFFFFFFF | 0xFC891918 |
| CRC-32/MPEG-2 | 32 | 0x04C11DB7 | 0xFFFFFFFF | false | false | 0x00000000 | 0x0376E6E7 |
| CRC-64/XZ | 64 | 0x42F0E1EBA9EA3693 | all ones | true | true | all ones | 0x995DC9BBDF1939FA |

CRC-32/ISO-HDLC is the CRC-32 of Ethernet, zip, gzip and PNG, and `binascii.crc32` in Python. CRC-16/IBM-3740 is often called CRC-16/CCITT-FALSE, and CRC-16/KERMIT is often called CRC-16/CCITT. CRC-32/ISCSI is [CRC-32C](/crc32c/).

## Example

**By hand.** Take $G(x) = x^3 + x + 1$ (binary 1011, $r = 3$) and the message 1101, with init 0 and no reflection. Append three zeros and divide: 1101000 divided by 1011 gives the quotient 1111 and the remainder 001. The codeword is 1101001. It is a multiple of $G$, and it is a codeword of the [Hamming code](/hamming-code/) of length 7, which is a [cyclic code](/cyclic-code/) with this generator.

**The register.** CRC-8/SMBUS has poly 0x07, which is $G(x) = x^8 + x^2 + x + 1$, init 0 and no reflection. Feed the one byte `1`, which is 0x31 = 00110001.

| step | input bit | f (line L6) | register after line L8 |
|---|---|---|---|
| start | | | 00000000 |
| 1 | 0 | 0 | 00000000 |
| 2 | 0 | 0 | 00000000 |
| 3 | 1 | 1 | 00000111 |
| 4 | 1 | 1 | 00001001 |
| 5 | 0 | 0 | 00010010 |
| 6 | 0 | 0 | 00100100 |
| 7 | 0 | 0 | 01001000 |
| 8 | 1 | 1 | 10010111 |

The CRC is 0x97. In step 4 the register is 00000111, shifted to 00001110, then XORed with 00000111 to give 00001001. The CRC of the full string `123456789` is 0xF4, the check value of the catalogue.

## Correctness

Write $M_j(x)$ for the polynomial of the first $j$ message bits and $I(x)$ for init. One pass of lines L6 to L8 maps the register $R$ to $(xR + b x^r) \bmod G$, because $x^r \equiv \text{poly} \pmod G$. By induction, after $j$ bits the register holds

$$(I(x)\, x^j + M_j(x)\, x^r) \bmod G(x).$$

With init 0 this is $M(x) x^r \bmod G(x)$, the remainder of the message with $r$ zero bits appended. A nonzero init adds $I(x) x^k$, which is the same as an XOR of init into the first $r$ message bits. Lines L9 and L10 only rename the result.

When the sender appends the CRC, the receiver accepts a received word if and only if the error polynomial $E(x)$ is a multiple of $G(x)$. Every guarantee of a CRC follows from this fact. The [error-detection guarantees](/crc-error-detection-guarantees/) page gives them, and the full proof of the invariant and of this fact is below.

## Complexity

- **Time.** Lines L6 to L8 run once for each bit, so the time is $\Theta(8n) = \Theta(n)$ in each case on the word RAM, with $r$ at most the word size.
- **Space.** The register and the loop index need $\Theta(1)$ words.
- **Streaming.** The register is the whole state. So a CRC can be computed on a stream, one part at a time, with no buffer.

The bit loop is slow in software: 8 steps for each byte. [Table-driven CRC](/table-driven-crc/) does one step for each byte, [slicing-by-8](/slicing-by-8/) does one step for each 8 bytes, and [CRC folding with carry-less multiplication](/clmul-crc-folding/) does 64 bytes in a few instructions.

## Properties

- **Affine.** For messages $a$, $b$, $c$ of the same length, $\mathrm{crc}(a \oplus b \oplus c) = \mathrm{crc}(a) \oplus \mathrm{crc}(b) \oplus \mathrm{crc}(c)$. With init 0 and xorout 0 the CRC is linear.
- **Detects single-bit errors.** $G(x)$ has at least two terms, so it does not divide $x^i$.
- **Detects all bursts of length at most $r$**, and all errors of odd weight when $(x + 1)$ divides $G(x)$. See [CRC error-detection guarantees](/crc-error-detection-guarantees/).
- **Constant residue.** After a whole codeword with no error, the register holds a fixed value, the residue, which does not depend on the message. For CRC-32/ISO-HDLC it is 0xDEBB20E3. A receiver can test for this value and need not compare the CRC.
- **No security.** For each message and each target value, some $r$ appended bits give that CRC, because $x^r$ has an inverse modulo $G(x)$. For example, the bytes `hello` followed by 45 7E 34 30 have the CRC-32 0xDEADBEEF. Use a [cryptographic hash function](/cryptographic-hash-function/) or a [message authentication code](/message-authentication-code/) against an attacker.

## Variants and improvements

- **Augmented form.** The register of Williams first takes $r$ zero bits after the message, and init then has another meaning. An augmented init of 0xFFFF for poly 0x1021 equals a direct init of 0x1D0F, which is $\text{0xFFFF} \cdot x^{16} \bmod G$.
- **Table-driven CRC.** Process a byte at a time with a table of 256 entries. See [table-driven CRC](/table-driven-crc/).
- **Slicing and folding.** [Slicing-by-8](/slicing-by-8/) uses 8 tables; [CRC folding](/clmul-crc-folding/) uses a carry-less multiply instruction.
- **Hardware.** A linear feedback shift register with XOR gates at the taps of $G$ computes the CRC at one bit per clock, and parallel circuits do many bits per clock. See [linear feedback shift register](/linear-feedback-shift-register/).
- **Choice of generator.** The generator decides which errors are detected. See [CRC generator polynomial](/crc-generator-polynomial/).

## When to use it

Use a CRC to detect accidental errors in a frame, a packet, a disk block or a file. For the same number of check bits, a good CRC detects more error patterns than a sum such as the [Internet checksum](/internet-checksum/), the [Fletcher checksum](/fletcher-checksum/) or [Adler-32](/adler-32/). A sum is a little faster in plain software without tables. Do not use a CRC where an attacker can change the data.

## Pitfalls

- **Notation.** The same generator has a normal, a reversed and a Koopman notation: CRC-32 is 0x04C11DB7, 0xEDB88320 or 0x82608EDB. A wrong notation gives a different and often weak CRC. See [CRC generator polynomial](/crc-generator-polynomial/).
- **Bit and byte order.** With refout, the CRC goes on the wire least significant byte first. Only then is the whole codeword a multiple of $G(x)$ and the residue constant.
- **Zero init.** With init 0, leading zero bytes do not change the CRC, so a message and the same message with zeros in front have the same CRC. A nonzero init fixes this.
- **One name, many CRCs.** People use the name "CRC-16" for many different parameter sets. Always state all the parameters, and test with the check value.

## Implementations

## History

W. Wesley Peterson and D. T. Brown published the cyclic codes for error detection in 1961, with the shift-register circuit and the proof of the burst-detection property. The 16-bit polynomial 0x1021 came into use in ITU (then CCITT) recommendations such as V.41, and the 32-bit polynomial 0x04C11DB7 in Ethernet, HDLC and ITU-T V.42. In 1988 Dilip Sarwate published the table-driven method for software. In 1993 Ross Williams wrote a guide that defined the parameter model in use today. Greg Cook keeps the catalogue of named CRCs with their check values.

## References
