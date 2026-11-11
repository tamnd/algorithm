---
tag: RP1KY4
kind: concept
slug: avalanche-effect
name: Avalanche effect
aliases:
- diffusion property
- strict avalanche criterion
area: cryptography/hash-functions
level: intro
summary: A one-bit change in the input of a good hash or cipher flips each output bit with probability about 1/2. It is a quick test of mixing, not a proof of security.
prereqs: [cryptographic-hash-function, hamming-weight]
see_also: [cryptographic-hash-function, collision-resistance, hamming-distance, feistel-network, s-box, sha-2, differential-cryptanalysis, confusion-and-diffusion]
sources:
  - paper: doi:10.1038/scientificamerican0573-15
    title: "Horst Feistel, Cryptography and computer privacy, Scientific American 228(5), May 1973, pages 15 to 23"
    locator: the description of how a change of one input bit spreads through the rounds of a product cipher, later called the avalanche effect
  - paper: "A. F. Webster and Stafford E. Tavares, On the design of S-boxes, CRYPTO 1985, LNCS 218, pages 523 to 534"
    locator: the definitions of the strict avalanche criterion and the bit independence criterion, and the tests on DES S-boxes
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 7, the notes on confusion, diffusion and the avalanche property of block ciphers
  - paper: doi:10.6028/NIST.FIPS.180-4
    title: NIST FIPS 180-4, Secure Hash Standard (SHS), 2015
    locator: Section 6.2 (SHA-256), the hash measured on this page
---

The avalanche effect is the property that a small change in the input of a hash function or a cipher, such as one flipped bit, changes about half of the output bits, in a way that looks random. Feistel described it in 1973 for product ciphers, where each round spreads a change further. Webster and Tavares made it precise in 1985 with the strict avalanche criterion (SAC): for every input bit $i$ and output bit $j$, flipping bit $i$ flips bit $j$ with probability $1/2$ over random inputs. A [cryptographic hash function](/cryptographic-hash-function/) must have it, since a hash where a small change gives a small change leaks its input and is easy to attack. But the converse is false. Avalanche is a heuristic test, and a function can pass it and still be weak.

## In plain words

Change one letter of a message, and the fingerprint made by a good hash should change completely. About half of its bits should flip, and you should not be able to tell which ones.

A poor hash changes only a few bits, or always the same ones. Then two close messages give close fingerprints, and an attacker learns something from the fingerprint.

The test is easy to run. But passing it does not prove that a hash is secure.

## The idea

**The avalanche measure.** Let $H$ have $n$ output bits. For a random input $x$ and an input bit $i$, let $e_i$ be the input that differs from $x$ only at bit $i$. The number of flipped output bits is the [Hamming weight](/hamming-weight/) $\mathrm{wt}(H(x) \oplus H(x \oplus e_i))$. For a random function, this count follows the binomial distribution with mean $n/2$ and standard deviation $\sqrt{n}/2$. So for SHA-256 the mean should be 128 and the deviation 8.

**The strict avalanche criterion.** For each pair $(i, j)$, let $p_{ij}$ be the probability, over random $x$, that output bit $j$ flips when input bit $i$ flips. The SAC asks for $p_{ij} = 1/2$ for all pairs. With $s$ samples per input bit, an estimate of $p_{ij}$ for an ideal function has deviation $0.5/\sqrt{s}$ from $1/2$, and the mean absolute deviation is about $\sqrt{2/\pi} \cdot 0.5/\sqrt{s}$.

**The bit independence criterion.** Webster and Tavares also ask that, for each input bit $i$, the changes of any two output bits $j$ and $k$ be independent. This rules out functions where outputs flip together.

**Why it matters.** If one input bit affects only a few output bits, an attacker can find inputs with close outputs, follow the change through the rounds, and build differential attacks. In a cipher, fast avalanche is what the rounds of a [Feistel network](/feistel-network/) and the [S-boxes](/s-box/) are for. It is the "diffusion" half of Shannon's [confusion and diffusion](/confusion-and-diffusion/).

**Why it is not enough.** The avalanche test looks at one input bit and one random $x$ at a time. A function can pass it and still have a structure that an attacker can use:

- a fixed key or a known fixed point;
- a [length extension](/length-extension-attack/) property, which SHA-256 has and which no avalanche test sees;
- a high-probability differential over many bits at once;
- a short output, which gives collisions by the [birthday attack](/birthday-attack/) whatever the mixing.

MD5 and SHA-1 have very good avalanche, and both are broken for [collision resistance](/collision-resistance/). So a good avalanche score is a necessary sign of mixing, not a security claim.

## Examples

**One bit of one message.** The input `avalanche` and the input with the low bit of its first byte flipped (`` `valanche ``) differ in 1 of 72 bits.

| Hash | First digest | Second digest | Bits changed |
|---|---|---|---|
| SHA-256 | `bb93cff8851d49ac...` | `3326b117c86666e3...` | 138 of 256 |
| weak toy hash | `9e26e3cd` | `9e26e2cd` | 1 of 32 |

The weak toy hash is $h \leftarrow \mathrm{rotl}_5(h) \oplus b$ for each byte $b$, on 32 bits. It has no nonlinear step, so a change in one input bit moves to one place and stays one bit.

**A full measurement.** The page's code takes 100 random 8-byte inputs, flips each of their 64 bits in turn, and counts the output bits that change. It also estimates every $p_{ij}$.

| Measure | SHA-256 (seed 1973) | weak toy hash (seed 1985) | ideal |
|---|---|---|---|
| mean fraction of bits flipped | 0.49982 | 0.03125 | 0.5 |
| deviation of the count | 7.857 | 0 | $\sqrt{n}/2$, so 8.0 and 2.83 |
| SAC, largest $\lvert p_{ij} - 1/2 \rvert$ | 0.2 | 0.5 | near 0 |
| SAC, mean $\lvert p_{ij} - 1/2 \rvert$ | 0.0402 | 0.5 | 0.0399 for 100 samples |

SHA-256 matches a random function within the noise. The largest SAC deviation of 0.2 is expected: it is the largest of 16384 noisy estimates, each with deviation 0.05. The toy hash always flips exactly one bit, so each $p_{ij}$ is 0 or 1. The test also checks that the toy hash is linear: $h(x \oplus y) = h(x) \oplus h(y) \oplus h(0)$ for all equal-length $x$ and $y$, which makes it trivial to invert and to collide. For MD5 the same measure gives a mean fraction of 0.5006 and a deviation of 5.642 against 5.657, a perfect score for a hash with practical collisions.

The code is for study only and not constant time. The toy hash must not be used for anything. Use SHA-256 or SHA-3 from the standard library, a FIPS 140 validated module, or libsodium.

## Where it is used

- **Design of ciphers and hashes.** Designers count how many rounds are needed for full diffusion, the point after which every output bit depends on every input bit, and add a margin. The SAC is a design rule for S-boxes, with nonlinearity and differential uniformity.
- **Quick checks of non-cryptographic hashes.** Tools such as SMHasher test the avalanche of hash table functions, since poor avalanche gives clustered buckets.
- **Teaching.** The one-bit test shows in a few lines why a checksum such as CRC or a sum of bytes is not a cryptographic hash.
- **Not for proofs.** Security claims rest on cryptanalysis of differential, linear and algebraic attacks, and on generic bounds such as $2^{n/2}$ for collisions. An avalanche score adds nothing to them.

## References
