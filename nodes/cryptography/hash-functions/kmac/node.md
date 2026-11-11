---
tag: J3VNX8
kind: algorithm
slug: kmac
name: KMAC
aliases:
- KECCAK MAC
- KMAC128
- KMAC256
area: cryptography/hash-functions
level: advanced
summary: "The Keccak MAC of NIST SP 800-185: cSHAKE with name KMAC on bytepad(encode_string(K)) || X || right_encode(L). One sponge call; no nesting is needed. KMACXOF gives any output length."
solves: [message-authentication]
model: word-ram
complexity:
  vars: {n: the message length in bytes, r: the rate in bytes (168 or 136), l: the output length in bytes}
  time: {worst: Θ((n + l)/r + 1), average: Θ((n + l)/r + 1), best: Θ((n + l)/r + 1)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2016
  people: [John Kelsey, Shu-jen Chang, Ray Perlner]
  note: NIST published SP 800-185 (cSHAKE, KMAC, TupleHash and ParallelHash) in December 2016, based on the keyed sponge ideas of the Keccak team.
prereqs: [sponge-construction, keccak, message-authentication-code, pseudorandom-function]
see_also: [hmac, nmac, shake, extendable-output-function, sha-3, length-extension-attack, tree-hashing]
sources:
  - url: "https://doi.org/10.6028/NIST.SP.800-185"
    title: John Kelsey, Shu-jen Chang and Ray Perlner, NIST SP 800-185, SHA-3 Derived Functions, cSHAKE, KMAC, TupleHash and ParallelHash, December 2016
    locator: Section 2.3 (left_encode, right_encode, encode_string, bytepad), Section 3 (cSHAKE), Section 4 (KMAC, with 4.3.1 KMACXOF), Section 6 (ParallelHash), Section 8 (security considerations)
  - url: "https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/KMAC_samples.pdf"
    title: NIST, Cryptographic Standards and Guidelines, Examples with Intermediate Values, KMAC_samples.pdf
    locator: KMAC Samples #1 to #6 (KMAC128 and KMAC256, key 40 to 5F, outputs called Outval)
  - url: "https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/cSHAKE_samples.pdf"
    title: NIST, Cryptographic Standards and Guidelines, Examples with Intermediate Values, cSHAKE_samples.pdf
    locator: cSHAKE Samples #1 and #2 (cSHAKE128, S = Email Signature)
  - url: "https://doi.org/10.6028/NIST.FIPS.202"
    title: NIST FIPS 202, SHA-3 Standard, Permutation-Based Hash and Extendable-Output Functions, August 2015
    locator: Section 3 (Keccak-p and Keccak-f[1600], the step maps theta, rho, pi, chi and iota), Section 4 (the sponge and pad10*1), Section 6 (SHA-3 and SHAKE, and the domain bits)
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, On the indifferentiability of the sponge construction, EUROCRYPT 2008, LNCS 4965, pages 181 to 197"
    locator: the sponge with a random permutation is indifferentiable from a random oracle up to about N^2/2^(c+1) for N permutation calls
  - paper: "Elena Andreeva, Joan Daemen, Bart Mennink and Gilles Van Assche, Security of keyed sponge constructions using a modular proof approach, FSE 2015, LNCS 9054, pages 364 to 384"
    locator: PRF bounds for the keyed sponge with the key in the first blocks, as in KMAC
---

KMAC is the [message authentication code](/message-authentication-code/) and keyed [pseudorandom function](/pseudorandom-function/) of NIST SP 800-185 (2016), built on the [Keccak](/keccak/) permutation. It is one call of cSHAKE, the customizable form of [SHAKE](/shake/): the key, padded to a full block, goes in first, then the message, then the output length. KMAC128 uses the rate of SHAKE128 and KMAC256 the rate of SHAKE256; KMACXOF128 and KMACXOF256 give output of any length. Unlike [HMAC](/hmac/), KMAC has no inner and outer hash: the [sponge](/sponge-construction/) never outputs its capacity, so a keyed hash of key and message is already secure.

**Notation.** $f$ = Keccak-f[1600], a permutation of 1600 bits. $r$ the rate in bytes (168 for KMAC128, 136 for KMAC256), $c = 1600 - 8r$ the capacity in bits (256 or 512). $K$ the key, $X$ the message, $L$ the output length in bits, $S$ the customization string, $N$ the function name (`KMAC`). $\|$ is concatenation. $A$ an adversary with $q$ queries, $N_f$ the number of calls of $f$ it makes in the ideal permutation model.

## In plain words

A sponge hash keeps a big internal state. It mixes the input into one part of the state, the rate, and stirs the whole state with a fixed permutation after each piece. At the end, it reads the output from the rate part only. The other part, the capacity, is never shown.

To make a MAC, KMAC first absorbs the key, padded to fill whole pieces, then the message, then the wanted output length. Because the capacity stays hidden, an attacker who sees a tag cannot continue the hash from it, as is possible with older hashes. So one pass with the key in front is enough, and no second hash is needed. A short label and an optional custom string at the very start keep KMAC outputs apart from the outputs of every other function built on the same permutation.

## The problem

[Message authentication](/message-authentication/), and more: KMAC aims to be a PRF with variable output length. For a uniform key $K$ of at least the security strength (128 or 256 bits), the map $(X, L, S) \mapsto \mathrm{KMAC}(K, X, L, S)$ must be indistinguishable from a random function. SP 800-185 also names its use as a key derivation function.

## The algorithm

SP 800-185, Section 2.3, defines four encodings. Each makes the parsing of a concatenation unique.

- $\mathrm{left\_encode}(x)$: the number $n \ge 1$ of bytes of $x$, as one byte, then $x$ in $n$ big-endian bytes. For example $\mathrm{left\_encode}(0)$ = `01 00` and $\mathrm{left\_encode}(168)$ = `01 a8`.
- $\mathrm{right\_encode}(x)$: $x$ in $n$ big-endian bytes, then $n$. For example $\mathrm{right\_encode}(256)$ = `01 00 02`.
- $\mathrm{encode\_string}(S) = \mathrm{left\_encode}(|S|) \| S$, with $|S|$ in bits.
- $\mathrm{bytepad}(X, w) = \mathrm{left\_encode}(w) \| X$, followed by zero bytes up to a multiple of $w$ bytes.

```pseudo id=main
KMAC(K, X, L, S, r)                       ▷ r = 168 (KMAC128) or 136 (KMAC256); SP 800-185 Section 4.3
L1  newX ← bytepad(encode_string(K), r) ‖ X ‖ right_encode(L)   ▷ KMACXOF uses right_encode(0)
L2  prefix ← bytepad(encode_string("KMAC") ‖ encode_string(S), r)
L3  return SPONGE(prefix ‖ newX, domain bits 00, L, r)            ▷ this is cSHAKE(newX, L, "KMAC", S)

SPONGE(M, d, L, r)                        ▷ Keccak[c] of FIPS 202, Section 4
L4  P ← M ‖ d ‖ pad10*1, to a multiple of r bytes
L5  s ← 0^1600;  for each r-byte block P_i of P: s ← f(s ⊕ (P_i ‖ 0^c))
L6  Z ← the first r bytes of s;  while |Z| < L: s ← f(s), append the first r bytes of s to Z
L7  return the first L bits of Z
```

The two domain bits `00` of line L3 mark cSHAKE; SHAKE uses `1111` and SHA-3 uses `01` (FIPS 202, Section 6). With the domain bits and the first bit of pad10*1, the byte appended after $M$ in line L4 is `04` for cSHAKE, `1f` for SHAKE and `06` for SHA-3. When both $N$ and $S$ are empty, cSHAKE is plain SHAKE; KMAC always has $N$ = `KMAC`, so it never collides with SHAKE.

**Why no nested structure.** In a [Merkle-Damgård](/merkle-damgard-construction/) hash the output is the full chaining value, so $H(K \| X)$ can be extended by anyone ([length extension](/length-extension-attack/)), and HMAC needs a second keyed hash to hide it. A sponge outputs only the rate part of the state; the $c$ capacity bits never appear. To continue the sponge from a tag, an attacker would need those $c$ bits, so extension costs about $2^{c}$ work for a guess, or $2^{c/2}$ by a generic collision in the capacity. The key in its own padded block (line L1, `bytepad`) is absorbed before the message, and the encoded length $L$ at the end binds the output length into the input, so a short KMAC tag is not a prefix of a longer one.

**About the code.** The Python code is for study only, is not constant time, and must not protect real data. Use a vetted library, such as a FIPS 140 validated module or the KMAC of OpenSSL 3. `hashlib.shake_128` cannot take $N$ and $S$, so the code implements Keccak-f[1600] of FIPS 202 in pure Python and checks plain SHAKE128, SHAKE256 and SHA3-256 against `hashlib`.

## Example

KMAC_samples.pdf, Sample #1: KMAC128 with the 32-byte key `40 41 ... 5f`, data `00 01 02 03`, $L = 256$ and an empty $S$.

| step | bytes |
|---|---|
| L2: prefix (168 bytes) | `01 a8 01 20 4b 4d 41 43 01 00`, then 158 zero bytes |
| L1: $\mathrm{encode\_string}(K)$ | `02 01 00 40 41 ... 5f` (35 bytes) |
| L1: newX (175 bytes) | `01 a8 02 01 00 40 41 ...`, zero bytes to 168, then `00 01 02 03`, then `01 00 02` |
| L4: input to the sponge | $168 + 175 = 343$ bytes, padded to $3 \times 168 = 504$ bytes |
| L7: Outval | `e5780b0d3ea6f7d3a429c5706aa43a00fadbd7d49628839e3187243f456ee14e` |

The sponge calls $f$ three times to absorb and none to squeeze, because 32 bytes fit in one rate block. The prefix block does not depend on the key or the message, and the key block does not depend on the message, so an implementation can precompute the state after the first two blocks for a fixed key. With $S$ = `My Tagged Application` (Sample #2) the output is `3b1fba963cd8b0b59e8c1a6d71888b7143651af8ba0a7070c0979e2811324aa5`, unrelated to the first.

## Correctness

**Claim 1 (unique encoding).** The map $(K, X, L, S) \mapsto \mathrm{prefix} \| \mathrm{newX}$ is injective for messages of whole bytes. The proof is below. So two different inputs never give the same sponge input, and KMAC inherits the security of the sponge with no ambiguity.

**Claim 2 (domain separation).** No KMAC input equals a SHAKE, SHA-3 or cSHAKE input with another name, because the domain bits differ from SHAKE and SHA-3, and the encoded $N$ = `KMAC` at a fixed place in the first block differs from every other name.

**Security.** In the ideal permutation model, the sponge with a random permutation is indifferentiable from a random oracle up to about $N_f^2 / 2^{c+1}$ (Bertoni, Daemen, Peeters and Van Assche, EUROCRYPT 2008). With a random oracle, the function $X \mapsto \mathcal{RO}(\mathrm{prefix} \| \mathrm{bytepad}(\mathrm{encode\_string}(K)) \| X \| \ldots)$ is a PRF unless the adversary queries the oracle on the key, which it does with probability about $N_f / 2^{|K|}$. Direct proofs for keyed sponges with the key in the first blocks give sharper bounds (Andreeva, Daemen, Mennink and Van Assche, FSE 2015). SP 800-185 states security strengths of 128 bits for KMAC128 and 256 bits for KMAC256 when the key is at least that long. These results are for an ideal permutation; for the real Keccak-f[1600], the security rests on cryptanalysis of its 24 rounds, where the best known attacks reach far fewer rounds.

## Complexity

The sponge input has one block of prefix (for a short $S$), one block of padded key (for a key of at most $r - 5$ bytes), the $n$ message bytes, and at most 3 bytes of $\mathrm{right\_encode}(L)$ for $L < 2^{16}$. With the padding byte, absorbing takes $\lceil (n + 4)/r \rceil + 2$ calls of $f$, and squeezing $\lceil l/r \rceil - 1$ more calls for $l$ output bytes. With the precomputed keyed state, a short message costs one call of $f$, against two compression calls for HMAC-SHA-256 with precomputed keys. The extra space is the 200-byte state.

## Properties

- **One pass, deterministic, no nonce.**
- **Variable output.** KMAC binds $L$ into the input; KMACXOF uses $\mathrm{right\_encode}(0)$ instead, so its outputs of different lengths are prefixes of each other, as for an [XOF](/extendable-output-function/).
- **Customization.** The string $S$ separates uses of one key, for example a MAC key and a KDF key, without a second key.
- **Keys of any length**, encoded with their length, so `key` and `key\x00` are different keys, unlike HMAC.
- **No length extension**, by the hidden capacity.

## Variants and improvements

- **KMACXOF128 and KMACXOF256** (SP 800-185, Section 4.3.1): arbitrary output length, used as a KDF.
- **cSHAKE** (Section 3): the unkeyed base, with a function name $N$ for NIST use and a string $S$ for users.
- **TupleHash and ParallelHash** (Sections 5 and 6): a hash of a tuple of strings with unique encoding, and a [tree hash](/tree-hashing/) for long messages.
- **Keyed Keccak with fewer rounds.** KangarooTwelve and its keyed modes use Keccak-p with 12 rounds; they are not in SP 800-185.
- **HMAC-SHA-3.** HMAC with SHA-3 is allowed by FIPS 198-1 and is secure, but it is wasteful: the nested form protects against an attack that a sponge does not have.

## When to use it

Use KMAC where SHA-3 is already present, or when one primitive must give a MAC, a PRF and a KDF with domain separation by $S$. Where SHA-2 hardware is present and SHA-3 is not, HMAC-SHA-256 is faster in practice.

## Pitfalls

- **Forgetting the encodings.** Writing $\mathrm{SHAKE}(K \| X)$ by hand is secure against length extension but has no domain separation, and $K$ and $X$ are not separated: the pairs $(K, X)$ = (`ab`, `c`) and (`a`, `bc`) give the same input.
- **Bit and byte order.** FIPS 202 numbers bits from the least significant bit of each byte, and the lanes are little-endian. The domain bits are then the bytes `04`, `1f` and `06`, not the strings as written left to right.
- **Bit lengths, not byte lengths.** encode_string and right_encode take lengths in bits: $L = 256$ for a 32-byte output.
- **Comparing tags with an early exit.** Use a constant-time compare, as for every MAC.
- **Short keys.** A key shorter than the security strength gives less security than the name says.

## Implementations

The Python code implements Keccak-f[1600] (`keccak_f1600`, the five step maps), the sponge with domain bits (lines L4 to L7), SHAKE128, SHAKE256 and SHA3-256, the four encodings, cSHAKE (lines L2 and L3), and KMAC128, KMAC256, KMACXOF128 and KMACXOF256 (line L1). The tests check all six KMAC samples and two cSHAKE samples of the NIST example files, the encodings and the "Encoded K" bytes of Sample #1, SHAKE128, SHAKE256 and SHA3-256 against `hashlib` at the rate boundaries, that a changed key, message or $S$ changes the tag, that $L$ is bound into KMAC but not into KMACXOF, and that one changed message bit changes about half of the output bits.

## History

Bertoni, Daemen, Peeters and Van Assche proposed the sponge construction in 2007 and Keccak for the SHA-3 competition in 2008; from the start they pointed out that a keyed sponge MAC needs no HMAC nesting. NIST chose Keccak in October 2012, published FIPS 202 in August 2015, and published SP 800-185 with cSHAKE, KMAC, TupleHash and ParallelHash in December 2016.

## References
