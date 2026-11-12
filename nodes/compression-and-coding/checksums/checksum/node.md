---
tag: B82EKR
kind: definition
slug: checksum
name: Checksum
aliases:
- check value
area: compression-and-coding/checksums
level: intro
summary: A short value computed from data to detect accidental changes in transmission or storage.
prereqs: [error-detection]
see_also: [cyclic-redundancy-check, parity-bit, longitudinal-redundancy-check, internet-checksum, adler-32, undetected-error-probability, cryptographic-hash-function, message-authentication-code]
sources:
  - paper: doi:10.1109/TDSC.2007.70216
    title: Theresa C. Maxino and Philip J. Koopman, The effectiveness of checksums for embedded control networks, IEEE Transactions on Dependable and Secure Computing 6(1), 2009
    locator: Sections 3 to 5 (XOR, two's complement and one's complement sums, Fletcher, Adler and CRC compared by Hamming distance and by the fraction of undetected errors)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 1 (error detection with retransmission versus forward error correction) and Section 3.6 (undetected errors of a linear code)
  - url: http://www.ross.net/crc/download/crc_v3.txt
    title: Ross N. Williams, A painless guide to CRC error detection algorithms, version 3, 1993
    locator: Sections 2 and 3 (the purpose of a checksum, and why a plain sum is weaker than a division)
  - url: https://www.rfc-editor.org/rfc/rfc1071
    title: R. Braden, D. Borman and C. Partridge, RFC 1071, Computing the Internet checksum, 1988
    locator: Section 1 (the one's complement sum used as the checksum of IP, UDP and TCP)
  - url: https://reveng.sourceforge.io/crc-catalogue/all.htm
    title: Greg Cook, Catalogue of parametrised CRC algorithms
    locator: Entries CRC-8/SMBUS (check 0xF4) and CRC-32/ISO-HDLC (check 0xCBF43926)
---

A checksum is a short value, computed from a block of data, that is stored or sent with the data so that the receiver can detect accidental changes. The receiver computes the value again and compares; if the two differ, the data was damaged. A checksum detects errors but does not correct them. The word covers simple sums, parity bits, cyclic redundancy checks and check digits, and each family has its own guarantees and cost.

## Definition

Let $\Sigma$ be an alphabet, usually bits or bytes, and let $r \ge 1$. A *checksum* of $r$ bits is a function $c : \Sigma^* \to \{0, 1\}^r$ that the sender and the receiver agree on. The value $c(M)$ is the *check value* of the message $M$. The sender sends $M$ together with $v = c(M)$. The receiver gets $M'$ and $v'$ and accepts if and only if $c(M') = v'$.

An error is *detected* if the receiver rejects. An error is *undetected* if $(M', v') \ne (M, v)$ and the receiver accepts. For a fixed class of errors, for example all changes of at most $t$ bits, the checksum *detects the class* if no error in the class is undetected, for every message $M$.

[Error detection](/error-detection/) differs from correction. A checksum lets the receiver find that the data is wrong, and the usual action is to ask for the data again or to discard it. To correct errors without a new copy, the code needs more redundancy and a decoder, as in a [Hamming code](/hamming-code/). A check of $r$ bits can take only $2^r$ values, so for any messages longer than $r$ bits many different messages have the same value: errors that change $M$ into such a message are always undetected. A good checksum makes sure that the likely errors are not among them.

Three goals are often confused.

- **Checksums and CRCs** protect against accidental errors: noise, bad memory, a broken disk. A [cyclic redundancy check](/cyclic-redundancy-check/) is a checksum with proven guarantees for bursts and small numbers of bit errors.
- **[Cryptographic hash functions](/cryptographic-hash-function/)** make it infeasible to find two messages with the same value. They have no guarantee for a small number of flipped bits, they are slower, and they protect against an attacker only if the hash value itself arrives by a trusted path.
- **[Message authentication codes](/message-authentication-code/)**, such as [HMAC](/hmac/), depend on a secret key, so an attacker who changes the data cannot compute the new tag. A checksum without a key gives no protection against deliberate changes: an attacker computes the new checksum.

The main families, each with its own page:

- [Parity bit](/parity-bit/): one bit, the XOR of all bits. Detects every odd number of bit errors.
- [Longitudinal redundancy check](/longitudinal-redundancy-check/): one parity bit for each bit column of a block of characters.
- [Additive checksum](/additive-checksum/): the sum of the words modulo $2^w$, or with [one's complement arithmetic](/ones-complement-arithmetic/) as in the [Internet checksum](/internet-checksum/), which also allows an [incremental update](/incremental-checksum-update/).
- [Fletcher checksum](/fletcher-checksum/) and [Adler-32](/adler-32/): two running sums, so that the order of the words matters.
- [Rolling checksum](/rolling-checksum/): a sum over a sliding window that is updated in constant time per step, as in rsync.
- [Cyclic redundancy check](/cyclic-redundancy-check/): the remainder of a polynomial division over GF(2), such as CRC-32 and [CRC-32C](/crc32c/).
- [Check digits](/check-digit-computation/) for numbers that people type: the [Luhn algorithm](/luhn-algorithm/), the [Verhoeff algorithm](/verhoeff-algorithm/) and the [Damm algorithm](/damm-algorithm/), and the older test of [casting out nines](/casting-out-nines/).

## Examples and non-examples

**Examples.** For the ASCII message "123456789", the bytes 0x31 to 0x39:

| checksum | width | value |
|---|---|---|
| even parity of all bits | 1 bit | 1 |
| XOR of the bytes (LRC) | 8 bits | 0x31 |
| sum of the bytes modulo 256 | 8 bits | 0xDD |
| CRC-8/SMBUS | 8 bits | 0xF4 |
| CRC-32/ISO-HDLC | 32 bits | 0xCBF43926 |

The two CRC values are the check values in the catalogue of Greg Cook.

**How often they miss errors.** The implementation flips bits of 10000 random messages of 64 bytes for each kind of error, with the fixed seed 2024, and counts the errors that each checksum misses. Bit positions run from the most significant bit of the first byte, the order in which CRC-8/SMBUS reads the bits. A burst of length $b$ flips its first and last bit and each bit between with probability 1/2.

| errors | parity | LRC | sum mod 256 | CRC-8 | CRC-32 |
|---|---|---|---|---|---|
| 1 bit | 0 | 0 | 0 | 0 | 0 |
| 2 bits | 1.0000 | 0.1179 | 0.0641 | 0.0053 | 0 |
| burst of 2 to 8 bits | 0.5714 | 0 | 0 | 0 | 0 |
| burst of 9 to 32 bits | 0.5049 | 0.0039 | 0.0037 | 0.0040 | 0 |

The values follow from the structure. Parity misses every even number of errors. The LRC misses two errors in the same bit column, with probability $63/511 \approx 0.123$ for random positions in 512 bits. The sum misses two errors in the same column when one flips a 0 to 1 and the other a 1 to 0, and also any two errors in the top bit, where $128 + 128 = 256$: probability $\frac{63}{511} \cdot \frac{9}{16} \approx 0.069$. CRC-8/SMBUS misses two errors only when they are a multiple of 127 bits apart, its period: probability $778/130816 \approx 0.006$. For long bursts the three 8-bit checks all miss about $2^{-8} \approx 0.0039$. CRC-32 missed nothing. The tests also check the rules for two errors exhaustively over every pair of positions in a message of 32 bytes.

**Non-examples.**

- A copy of the whole message, sent twice. The receiver detects any difference, but the redundancy is as long as the data, so it is not a short value.
- A message authentication code. It is computed from the data like a checksum, but it also needs a secret key, and its purpose is to stop deliberate changes.
- A [hash function](/hash-function/) for a hash table. It maps keys to buckets, and equal values are expected and resolved; nothing is checked.
- A fast non-cryptographic hash such as [xxHash](/xxhash/) is often used as a checksum, for example in file formats. It is a checksum in that use, but it has no proven guarantee for bursts or small numbers of errors, as a CRC has.

## Related definitions

- [Error detection](/error-detection/): the general problem, of which the checksum is the simplest solution.
- [Hamming distance](/hamming-distance/): a checksum that detects every change of at most $t$ bits gives a code of distance at least $t + 1$.
- [Undetected error probability](/undetected-error-probability/): the probability that random errors give a message with the same check value.
- [CRC error-detection guarantees](/crc-error-detection-guarantees/): the error classes that a CRC always detects.
- [Check digit computation](/check-digit-computation/): checksums over decimal digits that detect the errors people make when they type.
- [Cryptographic hash function](/cryptographic-hash-function/): a check value that is hard to forge, but without guarantees for small errors.

## References
