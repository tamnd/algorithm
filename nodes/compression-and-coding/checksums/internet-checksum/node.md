---
tag: EH9YR6
kind: algorithm
slug: internet-checksum
name: Internet checksum
aliases:
- ones' complement checksum
- RFC 1071 checksum
area: compression-and-coding/checksums
level: intro
summary: The 16-bit checksum of IPv4, ICMP, UDP and TCP. Add the data as 16-bit words in ones' complement arithmetic and send the bitwise complement of the sum (RFC 1071).
model: word-ram
complexity:
  vars: {n: the number of message bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1988
  people: [Robert Braden, David Borman, Craig Partridge]
  note: The ones' complement checksum is the checksum of IPv4 and TCP as specified in 1981 (RFC 791 and RFC 793). RFC 1071 (1988) collected its properties and the fast ways to compute it.
prereqs: [ones-complement-arithmetic]
see_also: [incremental-checksum-update, additive-checksum, fletcher-checksum, adler-32, cyclic-redundancy-check, crc32c, checksum, undetected-error-probability]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc1071
    title: R. Braden, D. Borman and C. Partridge, RFC 1071, Computing the Internet Checksum, September 1988
    locator: Section 1 (the three steps and the -0 test), Section 2 (properties and techniques), Section 3 (numerical examples), Section 4 (sample code), and the appendix IEN 45 by Plummer (TCP Checksum Function Design, 1978)
  - url: https://www.rfc-editor.org/rfc/rfc791
    title: J. Postel, RFC 791, Internet Protocol, September 1981
    locator: Section 3.1, Header Checksum
  - url: https://www.rfc-editor.org/rfc/rfc768
    title: J. Postel, RFC 768, User Datagram Protocol, August 1980
    locator: Fields, Checksum (the pseudo header, and a computed zero sent as all ones)
  - url: https://www.rfc-editor.org/rfc/rfc9293
    title: W. Eddy, editor, RFC 9293, Transmission Control Protocol (TCP), August 2022 (obsoletes RFC 793)
    locator: Section 3.1, Header Format, the Checksum field and the pseudo header
  - url: https://www.rfc-editor.org/rfc/rfc8200
    title: S. Deering and R. Hinden, RFC 8200, Internet Protocol, Version 6 (IPv6) Specification, July 2017
    locator: Section 8.1, Upper-Layer Checksums (the IPv6 pseudo header, and the UDP checksum is mandatory)
  - paper: doi:10.1145/347059.347561
    title: Jonathan Stone and Craig Partridge, When the CRC and TCP checksum disagree, Proceedings of ACM SIGCOMM 2000, pages 309 to 319
    locator: Section 3.1 (the errors the checksum always detects, and its weakness on non-uniform data) and Section 4.4 (the estimated rate of undetected errors)
---

The Internet checksum is the 16-bit check field of IPv4 headers, ICMP messages, UDP datagrams and TCP segments. The sender adds the data as 16-bit big-endian words in [ones' complement arithmetic](/ones-complement-arithmetic/), takes the bitwise complement of the sum, and puts it in the checksum field. The receiver adds everything, the field included, and expects all ones. RFC 1071 (1988) is the standard reference for how to compute it. The checksum is cheap, does not depend on the byte order of the machine, and can be [updated incrementally](/incremental-checksum-update/), but it cannot see the order of the words. Compared with the two's complement [additive checksum](/additive-checksum/), the only change is the end-around carry, which makes the top bit as strong as the others.

## In plain words

Cut the message into pairs of bytes. Treat each pair as one number and add all the numbers. Whenever the total grows past 16 bits, take the overflow and add it back in at the bottom. At the end, flip every bit of the 16-bit total. That is the checksum, and it goes into a field in the header.

The receiver adds all the pairs again, this time with the checksum field. A number plus its flipped self is all ones, so a good message gives all ones. Anything else means the message changed. The check is very fast, but two words that swap places give the same total, so that error slips through.

## The problem

The input is a message of $n$ bytes $B[0], \ldots, B[n-1]$ in which the checksum field holds zero. If $n$ is odd, a zero byte is added at the end for the computation only. The words are $x_j = 256 \cdot B[2j] + B[2j+1]$. Let $S$ be their ones' complement sum, as defined on [ones' complement arithmetic](/ones-complement-arithmetic/). The output is the checksum $C = \lnot S$, the bitwise complement of $S$ in 16 bits. A receiver accepts a message when the ones' complement sum of all its words, with the checksum in place, is 0xFFFF ($-0$). We count word operations in the [word RAM](/word-ram/) model with registers of at least 32 bits.

## The algorithm

```pseudo id=main
INTERNET-CHECKSUM(B[0 .. n − 1])             ▷ the checksum field holds 0
L1  if n is odd then append one zero byte     ▷ for the sum only, it is not sent
L2  s ← 0                                     ▷ a register of 32 bits or more
L3  for i ← 0, 2, 4, …, n − 2 do
L4      s ← s + (256 · B[i] + B[i + 1])       ▷ defer the carries into the high bits of s
L5  while s ≥ 2^16 do
L6      s ← (s and 0xFFFF) + (s >> 16)        ▷ fold: add the carries back in at bit 0
L7  return (not s) and 0xFFFF
```

Lines L3 and L4 add the words as plain integers and keep the carries in the high part of a wide register. This is the deferred carry of RFC 1071 Section 2 (1). Lines L5 and L6 add those carries back in, which gives the ones' complement sum. A 32-bit register can take up to 65537 words, which is 131074 bytes, before the high part could overflow. That covers any IPv4 packet. A longer input must fold from time to time. Line L7 takes the complement.

The protocols differ only in what they sum.
- **IPv4** (RFC 791): the header only, 20 to 60 bytes, with the checksum at bytes 10 and 11. A router that changes the TTL must update it, see [incremental checksum update](/incremental-checksum-update/).
- **ICMP** (RFC 792): the whole ICMP message.
- **UDP** (RFC 768) and **TCP** (RFC 793, now RFC 9293): a 12-byte *pseudo header* with the source address, the destination address, a zero byte, the protocol number (17 or 6) and the UDP or TCP length, then the header and the data. The pseudo header is not sent. It makes a datagram that reaches the wrong host or protocol fail the check.
- **UDP zero rule.** In UDP over IPv4, a checksum field of 0 means "no checksum". So a computed checksum of 0x0000 is sent as 0xFFFF, which is the same value in ones' complement (RFC 768). Over IPv6 the UDP checksum is mandatory (RFC 8200 Section 8.1).

## Example

**RFC 1071 Section 3.** The bytes 00 01 f2 03 f4 f5 f6 f7 give the words 0001, f203, f4f5 and f6f7. The plain total is 0x2DDF0. Lines L5 and L6 fold it to $0xDDF0 + 0x2 = 0xDDF2$, the sum that the RFC prints. The checksum is $\lnot 0xDDF2 = 0x220D$. (The RFC prints the sum, not the checksum.)

**An IPv4 header.** The header 4500 0073 0000 4000 4011 xxxx c0a8 0001 c0a8 00c7 is the 20-byte header of a 115-byte IPv4 packet (total length 0x73) that carries UDP from 192.168.0.1 to 192.168.0.199. The checksum field xxxx counts as 0000.

| word | 4500 | 0073 | 0000 | 4000 | 4011 | 0000 | c0a8 | 0001 | c0a8 | 00c7 |
|---|---|---|---|---|---|---|---|---|---|---|
| $s$ after L4 | 4500 | 4573 | 4573 | 8573 | c584 | c584 | 1862c | 1862d | 246d5 | 2479c |

The fold gives $0x479C + 0x2 = 0x479E$, and the checksum is $\lnot 0x479E = 0xB861$. The receiver sums the same ten words with b861 in place: the total is 0x2FFFD, which folds to $0xFFFD + 0x2 = 0xFFFF$. The header is accepted.

## Correctness

After line L4 runs for every word, $s$ is the plain integer total $T$ of the words. Lines L5 and L6 keep $s$ modulo 65535 and stop at a value below $2^{16}$, which is the ones' complement sum $S$. Line L7 returns $C = 0xFFFF - S$. A message with $C$ in its field sums to $S \oplus C = 0xFFFF$, because $S + C = 0xFFFF$ with no carry. The proofs, together with the exact list of the errors that are missed, are in the correctness file below.

## Complexity

Line L4 runs $\lceil n/2 \rceil$ times. The fold runs at most twice for a 32-bit total and at most four times for a 64-bit total. So the time is $\Theta(n)$ and the extra space is one register, in each case. Real code is faster by a constant factor:
- add 32 or 64 bits at a time with an end-around carry, and fold at the end (RFC 1071 Section 2 (C));
- add on a little-endian machine in its own byte order and swap the bytes of the result once (Section 2 (B));
- unroll the loop, and compute the sum while the data is copied (Section 2 (2) and (3)).

Since the sum is commutative and associative, partial sums from several cores or from a network card can be combined.

## Properties

- **Exact miss rule.** A change is missed if and only if the new words have the same ones' complement sum. Apart from the special case of an all-zero message, this means the total changes by a multiple of 65535.
- **Detected always.** Every single-bit error. Every error in a single word, except 0x0000 replaced by 0xFFFF or back. Every burst of at most 15 bits. Every 16-bit burst except one that turns 16 zero bits into 16 one bits or back, at any offset, not only in one word: 0x1200 0x0034 to 0x12FF 0xFF34 is missed (Stone and Partridge, Section 3.1).
- **Missed always.** Any reordering of 16-bit words, such as two swapped aligned words. Any insertion or deletion of 0x0000 words. Changes that cancel, such as $+d$ in one word and $-d$ in another.
- **Rate on random data.** On uniform random corruption the miss rate is near $1/65535$. On real data the sums of the words are not uniform, and Stone and Partridge found the checksum much weaker than that figure suggests. They cite a study with a rate near 1 in $2^{10}$.
- **Byte order independence.** The same code works on big-endian and little-endian machines if it swaps the result. See [ones' complement arithmetic](/ones-complement-arithmetic/).
- **Incremental.** A change of one word from $m$ to $m'$ changes the checksum by a formula in $m$, $m'$ and the old checksum. See [incremental checksum update](/incremental-checksum-update/).

## Variants and improvements

- **Wider sums.** Adding 32-bit or 64-bit chunks with end-around carry and then folding gives the same 16-bit result. See [ones' complement arithmetic](/ones-complement-arithmetic/).
- **Hardware offload.** Most network cards compute the TCP and UDP checksum, or a raw ones' complement sum of the packet that the driver adjusts.
- **Stronger checks.** The [Fletcher checksum](/fletcher-checksum/) adds a second sum and so sees the order of the data. RFC 1146 proposed it as a TCP option. SCTP first used [Adler-32](/adler-32/) and then switched to [CRC32C](/crc32c/), and link layers such as Ethernet use a 32-bit [CRC](/cyclic-redundancy-check/). The Internet checksum stays as an end-to-end check on top of these.
- **IPv6.** IPv6 drops the header checksum. The upper-layer checksum is the same algorithm over a pseudo header with the 128-bit addresses (RFC 8200 Section 8.1).

## When to use it

Use it when a protocol requires it: IPv4, ICMP, UDP and TCP. It is also a fair choice for a new protocol where software must compute the check fast on any machine and where routers or proxies must patch the check after they edit a field. Do not use it as the only check where errors come in bursts longer than 16 bits or where data can be reordered, and never as a defense against deliberate change. A CRC on each link and the Internet checksum end to end is the usual design. Stone and Partridge estimate that between 1 in 16 million and 1 in 10 billion TCP packets carry an error that the TCP checksum misses, so applications that need more add their own check.

## Pitfalls

- **Not zeroing the field.** Compute the checksum with the checksum field set to 0. To verify, either sum everything and test for 0xFFFF, or zero the field, recompute, and compare.
- **Testing for 0 instead of 0xFFFF.** The full sum of a correct message is $-0$, 0xFFFF. Its complement is 0. Code that mixes the two tests rejects good packets.
- **Odd length.** The last odd byte is the high byte of a word padded with zero on the right, not the low byte.
- **Forgetting the pseudo header,** or giving it the wrong length or protocol number, for TCP and UDP.
- **The UDP zero.** In UDP over IPv4, a computed checksum of 0x0000 must be sent as 0xFFFF.
- **Overflow of the accumulator.** A 32-bit accumulator without folding overflows after 65537 words. Fold inside the loop for long data, or use 64 bits.
- **Incremental updates that create $-0$.** The update rule of RFC 1141 can give 0xFFFF where a full recompute gives 0x0000. Use RFC 1624.

## Implementations

## History

The ones' complement checksum is older than the RFCs that now define it. It is the checksum of IPv4 and TCP in the specifications that Postel edited in 1981, RFC 791 and RFC 793, and UDP (RFC 768, 1980) uses it with the pseudo header. In 1978, William Plummer's note IEN 45, "TCP Checksum Function Design", compared it with other choices. RFC 1071 reprints that note as an appendix. In September 1988, Braden, Borman and Partridge published RFC 1071, which collected the mathematical properties of the sum and the fast ways to compute it. RFC 1141 (1990) and RFC 1624 (1994) added the incremental update. RFC 9293 (2022) replaced RFC 793 as the TCP standard and kept the checksum. In 2000, Stone and Partridge measured real traffic and showed that the checksum misses far more errors than its 16 bits suggest.

## References
