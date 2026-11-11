---
tag: SK12VS
kind: algorithm
slug: xxhash
name: xxHash
aliases:
- XXH32
- XXH64
- XXH3
area: cryptography/hash-functions
level: advanced
summary: A very fast non-cryptographic hash by Yann Collet, for checksums, hash tables and deduplication. It mixes 4 lanes with multiply and rotate steps. It gives no security against an attacker.
model: word-ram
complexity:
  vars: {n: the input length in bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2012
  people: [Yann Collet]
  note: Collet released XXH32 in 2012 with his LZ4 compressor, then XXH64 and later XXH3 and XXH128. The specification document is version 0.2.0 of June 2023.
prereqs: [hash-function, checksum]
see_also: [murmurhash, fnv-hash, siphash, cyclic-redundancy-check, hash-table, blake3, universal-hashing, avalanche-effect]
sources:
  - url: "https://github.com/Cyan4973/xxHash/blob/dev/doc/xxhash_spec.md"
    title: Yann Collet, xxHash fast digest algorithm, specification version 0.2.0, 29 June 2023
    locator: the sections XXH32 algorithm description and XXH64 algorithm description, steps 1 to 7, and the XXH3 overview
  - url: "https://github.com/Cyan4973/xxHash/blob/dev/cli/xsum_sanity_check.c"
    title: xxHash repository, the self-test of the xxhsum tool
    locator: XSUM_fillTestBuffer, and the tables XSUM_XXH32_testdata and XSUM_XXH64_testdata
  - url: "https://github.com/aappleby/smhasher"
    title: Austin Appleby, SMHasher, a test suite for the distribution and speed of non-cryptographic hash functions
    locator: the avalanche, collision and distribution tests that xxHash is reported to pass
  - paper: "Jean-Philippe Aumasson and Daniel J. Bernstein, SipHash: a fast short-input PRF, INDOCRYPT 2012, LNCS 7668"
    locator: Section 7, on hash flooding and why a fast hash with a seed is not enough
---

xxHash is a family of fast non-cryptographic hash functions by Yann Collet. XXH32 returns 32 bits and XXH64 returns 64 bits; XXH3 and XXH128 are later versions for 64 and 128 bits. They read the input in stripes, update four independent accumulators with a multiply, a rotation and a second multiply, and finish with a mixing step that spreads every input bit over the output. They run near the speed of memory on modern CPUs. Compression formats (LZ4, Zstandard), databases and file tools use xxHash as a [checksum](/checksum/) and as the [hash function](/hash-function/) of [hash tables](/hash-table/). xxHash is not a cryptographic hash: an attacker can find collisions and preimages.

**Notation.** All operations are on words of $w = 32$ bits (XXH32) or $w = 64$ bits (XXH64), modulo $2^w$. $+$ and $\times$ are modular addition and multiplication, $\lll$ is left rotation, $\gg$ a right shift, $\oplus$ XOR. $P_1, \ldots, P_5$ are the five odd prime constants of the specification. $s$ is the seed and $n$ the input length in bytes. A stripe is 16 bytes (XXH32) or 32 bytes (XXH64), split into 4 lanes. There is no security model: xxHash has no secret key and makes no claim against an adversary.

## In plain words

xxHash keeps four running numbers. It cuts the input into pieces of 16 bytes, and each piece gives one 4-byte word to each of the four numbers. Each number adds its word times a large odd constant, turns its bits around by a fixed amount, and multiplies by another constant. The four numbers are independent, so the CPU works on all four at the same time.

At the end, the four numbers are joined into one, the length and the leftover bytes are mixed in, and a last scramble of shifts and multiplies makes each input bit change about half of the output bits. The result is fast and spreads typical data well, but every step can be undone, so a person who wants two inputs with the same hash can make them.

## The problem

The goal is a function $h_s : \{0,1\}^{*} \to \{0,1\}^{w}$ that is as fast as possible and that behaves like a random function on data that is not chosen against it: few collisions among the keys of a hash table, and a good chance to detect accidental changes in a file. The quality is measured by statistical test suites such as SMHasher. There is no requirement against an adversary who knows the function and the seed.

## The algorithm

```pseudo id=main
XXH32(x, s)                                   ▷ xxhash_spec.md, steps 1 to 7
L1  if n ≥ 16 then a1 ← s + P1 + P2;  a2 ← s + P2;  a3 ← s;  a4 ← s − P1
    else h ← s + P5
L2  for each full stripe of 16 bytes, with little-endian lanes l1..l4:
        ai ← ((ai + li × P2) ⋘ 13) × P1   for i = 1..4
L3  if n ≥ 16 then h ← (a1 ⋘ 1) + (a2 ⋘ 7) + (a3 ⋘ 12) + (a4 ⋘ 18)
L4  h ← h + (n mod 2^32)
L5  for each remaining 4-byte word u:  h ← ((h + u × P3) ⋘ 17) × P4
    for each remaining byte b:        h ← ((h + b × P5) ⋘ 11) × P1
L6  h ← h ⊕ (h ≫ 15);  h ← h × P2;  h ← h ⊕ (h ≫ 13);  h ← h × P3;  h ← h ⊕ (h ≫ 16)
L7  return h  (the canonical byte form is big-endian)
```

XXH64 has the same shape with 64-bit words and 32-byte stripes. Its round is $a \gets ((a + l \times P_2) \lll 31) \times P_1$. After line L3 it also folds each accumulator in again with $h \gets (h \oplus \mathrm{round}(0, a_i)) \times P_1 + P_4$. Its tail takes 8-byte words, then one 4-byte word, then single bytes, and its final mix uses shifts of 33, 29 and 32. The code implements XXH32 and XXH64. It does not implement XXH3, which uses a 192-byte secret, 64-bit by 64-bit multiplications into 128 bits, and separate paths for inputs of up to 16, 17 to 240, and more than 240 bytes.

## Example

XXH32 of the empty input with seed 0. Line L1 sets $h$ = `165667B1` ($P_5$), and line L4 adds $n = 0$. Line L6 then gives, step by step: `16564B1D` after the first XOR, `7E00CC7B` after $\times P_2$, `7E033C7D` after the second XOR, `02CC5FC9` after $\times P_3$, and `02CC5D05` after the last XOR. The value `02CC5D05` is the first entry of `XSUM_XXH32_testdata` in the reference self-test. The intermediate values here are computed by the code of this page. The code also gives XXH32(`abc`) = `32D153FF` and XXH64(`abc`) = `44BC2CF5AD770999`.

**A collision by design.** With the seed known, take a 32-byte input $x$, flip one bit of lane 1 in stripe 1, and compute how accumulator $a_1$ changed after that stripe. Because $l \mapsto a + l \times P_2$ is a bijection modulo $2^{32}$ ($P_2$ is odd), one can choose lane 1 of stripe 2 so that $a_1$ becomes equal again. The two inputs differ and have the same XXH32 value. The tests build such a pair.

## Correctness

xxHash is defined by its specification, so the correctness of the code means that it computes that function. The tests check all 8 XXH32 values and all 9 XXH64 values of the xxhsum self-test, which cover the empty input, inputs shorter than a stripe, and 222 bytes with many stripes, each with seed 0 and with seed 2654435761.

**What the steps guarantee.** Each lane round $a \mapsto ((a + l P_2) \lll r) P_1$ is a bijection of $a$ for fixed $l$ and of $l$ for fixed $a$, since rotation is a bijection and $P_1$, $P_2$ are odd. So the round loses no information about the accumulator, and different lane values give different accumulators. The final mix in line L6 is also a bijection: $h \mapsto h \oplus (h \gg k)$ is invertible for $k \ge 1$, and multiplication by an odd constant is invertible. These are the reasons for its good distribution. They are also the reasons it is weak against an attacker: every step can be inverted, as the tests show by finding the 4-byte preimage of any 32-bit value.

**No security claim.** The specification says that xxHash "is not meant to avoid intentional collisions". There is no reduction and no security model.

## Complexity

XXH32 reads $\lfloor n / 16 \rfloor$ stripes, each with 4 multiplications by $P_2$, 4 by $P_1$, 4 additions and 4 rotations, plus at most 3 words and 3 bytes in the tail and a constant number of steps for the mix. XXH64 does the same per 32 bytes. The time is $\Theta(n)$ and the extra space is the four accumulators. The four lanes are independent, so the CPU overlaps their multiplications, which is why XXH64 reaches several gigabytes per second per core. XXH3 uses SIMD and is faster still on long inputs.

## Properties

- **Not cryptographic**: no collision, preimage or PRF security, even with a secret seed.
- **Good distribution on normal data**: passes the SMHasher tests of avalanche and distribution, according to its author.
- **Portable**: the same value on every CPU, with little-endian reads and a big-endian canonical form.
- **Seeded**: the seed selects a different function, which helps against accidental bad patterns, not against an attacker.
- **Streaming**: the accumulators can be updated stripe by stripe, so the input need not be in memory.

## Variants and improvements

- **XXH64** (2014), the 64-bit version, faster on 64-bit CPUs and with fewer collisions in large sets.
- **XXH3** and **XXH128** (stable in version 0.8.0 of 2020), with a 192-byte secret, special code for short inputs and SIMD for long inputs.
- **[MurmurHash](/murmurhash/)** and **[FNV](/fnv-hash/)**, older non-cryptographic hashes with a similar goal.
- **[CRC](/cyclic-redundancy-check/)**, which detects burst errors with a guarantee but is slower in software without special instructions.

## When to use it

Use xxHash to check that a file or a compressed block was not damaged by accident, to deduplicate data you control, and as the hash function of hash tables whose keys are not chosen by an attacker. Use [SipHash](/siphash/) for hash tables that hold keys from users or the network, because a known collision pattern lets an attacker flood one bucket. Use a cryptographic hash such as [BLAKE3](/blake3/) or [SHA-256](/sha-2/) when an attacker may change the data, for example for downloads or content addresses.

## Pitfalls

- **Using it as a MAC or an integrity check against attackers.** With the method of the example, an attacker who knows the seed finds collisions with a few operations.
- **Believing a random seed protects a hash table.** For seeded MurmurHash and CityHash, Aumasson, Bernstein and Boßlet found collisions that work for every seed; a seed is not a key unless the function is a PRF.
- **Byte order.** The canonical byte form is big-endian, while the input is read little-endian; printing the integer and printing the bytes in memory order give different strings.
- **Mixing variants.** XXH32, XXH64 and XXH3 give different values; a stored checksum must record which one made it.

## Implementations

The Python code is for study only, is not constant time, and gives no security. Use the `xxhash` C library or the `xxhash` Python package for speed, and a cryptographic hash when an attacker is present. The code gives `xxh32` and `xxh64` (lines L1 to L6) and `canonical32` and `canonical64` (line L7). The official values are copied by hand from `xsum_sanity_check.c`, and the test rebuilds the same input buffer with the generator of that file. The tests also check the big-endian form, that the seed changes the output, that all lengths from 0 to 99 give different values, that one changed bit changes about 32 of 64 output bits, the inversion of XXH32 on 4-byte inputs, and the two-stripe collision. Python's standard library has no xxHash, so there is no second check.

## History

Yann Collet wrote xxHash in 2012 as a fast checksum for his LZ4 compressor, and later used it in Zstandard. He added XXH64 for 64-bit CPUs. XXH3 and XXH128 were developed from 2019 and declared stable in version 0.8.0 in 2020. Collet wrote down the format of XXH32 and XXH64 in `xxhash_spec.md`, which later gained a description of XXH3; version 0.2.0 is dated 29 June 2023.

## References
