---
tag: T1JQ3Z
kind: concept
slug: lightweight-cryptography
name: Lightweight cryptography
aliases:
- lightweight ciphers
area: cryptography/symmetric-ciphers
level: advanced
summary: Ciphers, hashes and modes for devices with little area, power, energy or memory. NIST chose Ascon in 2023 and published SP 800-232 in 2025. ISO/IEC 29192 is the ISO series.
prereqs: [block-cipher, stream-cipher, authenticated-encryption]
see_also: [ascon, present, simon-cipher, speck, trivium, grain, sponge-construction, birthday-attack]
sources:
  - url: "https://doi.org/10.6028/NIST.IR.8114"
    title: Kerry A. McKay, Larry Bassham, Meltem Sönmez Turan and Nicky Mouha, NIST IR 8114, Report on Lightweight Cryptography, March 2017
    locator: the description of constrained devices and the metrics of hardware and software cost (area, latency, throughput, power, energy, RAM and code size)
  - url: "https://doi.org/10.6028/NIST.IR.8454"
    title: Meltem Sönmez Turan and others, NIST IR 8454, Status Report on the Final Round of the NIST Lightweight Cryptography Standardization Process, June 2023
    locator: the timeline of the process (57 submissions, 56 first-round candidates, 32 second-round candidates, 10 finalists) and the reasons for the selection of Ascon
  - url: "https://doi.org/10.6028/NIST.SP.800-232"
    title: "Meltem Sönmez Turan, Kerry A. McKay, Donghoon Chang, Jinkeon Kang and John Kelsey, NIST SP 800-232, Ascon-Based Lightweight Cryptography Standards for Constrained Devices: Authenticated Encryption, Hash, and Extendable Output Functions, August 2025"
    locator: Section 1 (the scope and the four schemes Ascon-AEAD128, Ascon-Hash256, Ascon-XOF128 and Ascon-CXOF128)
  - paper: "ISO/IEC 29192-2:2019, Information technology, Security techniques, Lightweight cryptography, Part 2: Block ciphers"
    locator: the scope (the block ciphers PRESENT, CLEFIA and LEA)
  - paper: "ISO/IEC 29192-5:2016, Information technology, Security techniques, Lightweight cryptography, Part 5: Hash-functions"
    locator: the scope (the hash functions PHOTON, SPONGENT and Lesamnta-LW)
---

Lightweight cryptography is the part of symmetric cryptography that designs ciphers, hash functions and modes for constrained devices: RFID tags, smart cards, sensors, medical implants and small microcontrollers. Such a device may have a few thousand logic gates for the cipher, a few kilobytes of RAM, a battery that must last years, or a hard limit on latency. A lightweight design gives up some generality, such as long blocks, large security margins or fast software on big processors, to fit these limits, but it must still reach a stated security strength, usually 112 or 128 bits. NIST chose the Ascon family in February 2023 and published it as SP 800-232 in August 2025. ISO/IEC 29192 is the ISO series of lightweight standards.

## In plain words

A bank server can run any cipher it likes. A tag on a box, or a sensor that runs on one coin battery for ten years, cannot. Its chip has room for only a small circuit, and each operation costs energy that it does not have.

Lightweight cryptography makes ciphers that fit in such small places. The designers cut the size of the state, use simple steps that cost few gates, and drop features the device does not need. But they do not cut the security below a clear target. A lightweight cipher must still resist all known attacks for its stated key size.

There is no single best design. A cipher that is very small in hardware can be slow in software, and a cipher that is fast for one block can need a large circuit. So the field has several designs for different limits.

## The idea

**The goals.** NIST IR 8114 groups the costs that matter on constrained devices. In hardware they are the area of the circuit, measured in gate equivalents (GE), the latency of one operation, the throughput, the power and the energy for each bit. In software they are the code size, the RAM, the speed on small 8-bit, 16-bit and 32-bit processors, and the energy. A design that is "lightweight" for one metric can be heavy for another. A design must also allow protection against side-channel attacks, such as power analysis, at a reasonable cost, because an attacker often holds the device.

**The means.** Lightweight designs use a few techniques again and again:

- a small state, such as a 64-bit block in [PRESENT](/present/) or a 288-bit state in [Trivium](/trivium/), because each stored bit needs a flip-flop, which costs several times as much area as a simple gate;
- simple operations with few gates: small 4-bit or 5-bit [S-boxes](/s-box/), bit permutations, AND, XOR and rotation, or the addition, rotation and XOR (ARX) of [SPECK](/speck/);
- a simple or no key schedule, so that no extra key state is stored;
- one primitive for many jobs, such as a permutation in a [sponge construction](/sponge-construction/) that gives encryption, authentication and hashing, as in [Ascon](/ascon/);
- [authenticated encryption](/authenticated-encryption/) in one pass, so the device does not need both a cipher and a separate MAC.

**The trade-offs.**

- **Block size against data limit.** A 64-bit block saves area, but by the [birthday bound](/birthday-attack/) a mode of operation leaks information after about $2^{32}$ blocks under one key. So a 64-bit block cipher must change its key often.
- **Key size against security.** An 80-bit key saves area and was once common, but it gives less than the 112-bit minimum that NIST now requires. The current NIST standard uses 128-bit keys.
- **Area against throughput and latency.** A serial circuit that handles a few bits per cycle is very small but needs many cycles. An unrolled circuit is fast but large. Some designs, such as PRINCE, aim at low latency instead of low area.
- **Hardware against software.** Bit permutations are free in hardware and slow in software. ARX operations are fast in software and cost more gates.
- **Security margin.** Fewer rounds cost less, but they leave less margin against new attacks. Reduced-round attacks on lightweight ciphers are a large part of their public analysis.

## Examples

| design | type | key bits | main feature | standard |
|---|---|---|---|---|
| [PRESENT](/present/) | block cipher, 64-bit block, SPN | 80 or 128 | 4-bit S-box and a bit permutation | ISO/IEC 29192-2 |
| [SIMON](/simon-cipher/) and [SPECK](/speck/) | block ciphers, 32 to 128-bit blocks | 64 to 256 | AND-rotation-XOR and ARX, from the NSA | not adopted by ISO |
| [Trivium](/trivium/) | stream cipher | 80 | three shift registers and three AND gates | eSTREAM hardware portfolio |
| [Grain-128AEADv2](/grain/) | stream cipher with authentication | 128 | an LFSR and an NFSR | Grain-128AEAD was a NIST finalist |
| [Ascon](/ascon/) | permutation-based AEAD, hash and XOF | 128 | a 320-bit permutation with a 5-bit S-box | NIST SP 800-232 |
| [TEA](/tea/) and [XTEA](/xtea/) | block ciphers, 64-bit block | 128 | a few lines of code | none |

## Where it is used

- **NIST lightweight cryptography.** NIST IR 8114 (2017) described the need. NIST then ran a public process. It received 57 submissions in February 2019, accepted 56 for the first round in April 2019, kept 32 for the second round, and named 10 finalists in March 2021: ASCON, Elephant, GIFT-COFB, Grain-128AEAD, ISAP, PHOTON-Beetle, Romulus, SPARKLE, TinyJAMBU and Xoodyak. On 7 February 2023 NIST announced that it would standardize the Ascon family, and NIST IR 8454 gives the reasons. SP 800-232 of August 2025, "Ascon-Based Lightweight Cryptography Standards for Constrained Devices: Authenticated Encryption, Hash, and Extendable Output Functions", specifies Ascon-AEAD128, Ascon-Hash256, Ascon-XOF128 and Ascon-CXOF128.
- **ISO/IEC 29192.** This ISO series has separate parts for lightweight block ciphers (Part 2: PRESENT, CLEFIA and LEA in the 2019 edition), stream ciphers (Part 3, which includes Trivium and Enocoro), mechanisms with asymmetric techniques (Part 4) and hash functions (Part 5: PHOTON, SPONGENT and Lesamnta-LW), with later parts for other mechanisms. SIMON and SPECK were proposed for Part 2 but were not adopted.
- **Other selections.** The eSTREAM project (2004 to 2008) chose a hardware portfolio of stream ciphers, which includes Trivium and Grain. The CAESAR competition (2013 to 2019) chose Ascon for its lightweight use case.
- **Devices.** RFID and NFC tags, smart cards, car keys and in-vehicle networks, wireless sensor networks, and medical and industrial controllers. On devices that have an AES circuit or AES instructions, plain AES is often the best choice, and a lightweight cipher is useful when AES does not fit.

## References
