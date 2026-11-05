---
tag: HXY9Z7
kind: algorithm
slug: murmurhash
name: MurmurHash
aliases:
- Murmur3
- MurmurHash3
- MurmurHash3_x86_32
area: strings/string-hashing
level: core
summary: Fast non-cryptographic hash with good avalanche for hash tables.
model: word-ram
complexity:
  vars: {n: the number of bytes of the input}
  time: {worst: Θ(n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 2011
  people: [Austin Appleby]
  note: Appleby published the first MurmurHash and MurmurHash2 in 2008 and the final MurmurHash3 in 2011, together with the SMHasher test suite; in 2012 Aumasson, Bernstein and Bosslet showed collisions that hold for every seed.
prereqs: [hash-function, hash-table]
see_also: [fnv-hash, xxhash, siphash, avalanche-effect, multiplicative-hashing, universal-hash-family, algorithmic-complexity-attack, bloom-filter]
sources:
  - url: https://github.com/aappleby/smhasher
    title: Austin Appleby, SMHasher and MurmurHash (source code repository)
    locator: src/MurmurHash3.cpp (MurmurHash3_x86_32 and fmix32), src/KeysetTest.cpp (VerificationTest) and src/main.cpp (the verification value 0xB0F57EE3 of MurmurHash3_x86_32)
  - url: https://github.com/aappleby/smhasher/wiki/MurmurHash3
    title: Austin Appleby, MurmurHash3 (SMHasher wiki page)
    locator: the three variants, the speed table, and the note that the finalizer constants came from simulated annealing
  - url: https://www.aumasson.jp/siphash/siphashdos_29c3_slides.pdf
    title: Jean-Philippe Aumasson, Daniel J. Bernstein and Martin Bosslet, Hash-flooding DoS reloaded, attacks and defenses, talk at the 29th Chaos Communication Congress (29C3), December 2012
    locator: the slides on MurmurHash2 and MurmurHash3 (differences that cancel over two blocks, for every seed) and the conclusion that recommends SipHash
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 11.3, Hash functions (fixed hash functions against random families, and the multiplication method)
---

MurmurHash is a family of fast non-cryptographic hash functions by Austin Appleby, named after the two operations of its inner loop, multiply and rotate. This page describes MurmurHash3_x86_32, the 32-bit version for hash tables: it reads the input in 4-byte blocks, mixes each block with two multiplications and a rotation, folds it into a 32-bit state, and ends with a finalizer that makes every output bit depend on every input bit. It takes a 32-bit seed, but the seed is not a key in the sense of [universal hashing](/universal-hash-family/): there are inputs that collide for every seed, so MurmurHash gives no collision bound against chosen inputs.

## In plain words

MurmurHash turns a piece of data into a 32-bit number. It reads the data four bytes at a time. Each group of four bytes is first scrambled on its own, by multiplying it by a fixed large number, turning its bits around in a circle, and multiplying again. The scrambled group is then mixed into a running number, which is turned and multiplied too. At the end, the length is mixed in, and a final scramble spreads every change in the data over all 32 digits of the result.

The result looks random for ordinary data, and it is fast. A starting number, the seed, changes all the results. But the seed is not a real secret lock: some pairs of inputs get equal results for every seed.

## The problem

Given a byte string $b = b[0] \cdots b[n-1]$ with $b[i] \in \{0, \ldots, 255\}$ and a seed $s \in \{0, \ldots, 2^{32} - 1\}$, compute $h_s(b) \in \{0, \ldots, 2^{32} - 1\}$, the same value for the same input, such that ordinary distinct inputs collide about as often as under a random function and a change of one input bit changes each output bit with probability close to $1/2$ (the [avalanche effect](/avalanche-effect/)). The alphabet is the 256 bytes; text is first encoded, for example in UTF-8. Indices are 0-based. Blocks are read in little-endian order, so the results are the same on every machine when the code is written as below.

## The algorithm

All arithmetic is modulo $2^{32}$, and $\mathrm{ROTL}(x, r)$ rotates the 32 bits of $x$ left by $r$ places. The constants are $c_1 = \mathtt{0xcc9e2d51}$, $c_2 = \mathtt{0x1b873593}$, $f_1 = \mathtt{0x85ebca6b}$ and $f_2 = \mathtt{0xc2b2ae35}$; all four are odd.

```pseudo id=main
MURMUR3-32(b[0 .. n−1], seed)
L1  h ← seed
L2  for j ← 0 to ⌊n/4⌋ − 1 do
L3      k ← b[4j] + 2^8 · b[4j+1] + 2^16 · b[4j+2] + 2^24 · b[4j+3]
L4      h ← h XOR MIX(k)
L5      h ← (ROTL(h, 13) · 5 + 0xe6546b64) mod 2^32
L6  t ← 4 · ⌊n/4⌋
L7  k ← b[t] + 2^8 · b[t+1] + 2^16 · b[t+2]       ▷ only the n − t ≤ 3 tail bytes; 0 if none
L8  if n > t then
L9      h ← h XOR MIX(k)
L10 h ← h XOR (n mod 2^32)
L11 return FMIX(h)

MIX(k)                                         ▷ the block mix; it does not use the seed
L12 k ← ROTL((k · c1) mod 2^32, 15)
L13 return (k · c2) mod 2^32

FMIX(h)                                        ▷ the finalizer
L14 h ← h XOR (h >> 16)
L15 h ← (h · f1) mod 2^32
L16 h ← h XOR (h >> 13)
L17 h ← (h · f2) mod 2^32
L18 return h XOR (h >> 16)
```

Lines L2 to L5 process the full blocks; line L5 multiplies by 5 and adds a constant, which spreads the state after the XOR. Lines L6 to L9 process the last 1 to 3 bytes, if any, as one short block without the step of line L5. Line L10 mixes in the length, so that inputs that differ only by trailing zero bytes do not collide by construction. Line L11 applies FMIX; without it, the low output bits would depend on few input bits. The 128-bit versions MurmurHash3_x86_128 and MurmurHash3_x64_128 follow the same plan with four 32-bit or two 64-bit lanes; they give different values from each other and from the 32-bit version.

## Example

MurmurHash3_x86_32 of Hello, world! ($n = 13$) with the seed $\mathtt{0x9747b28c}$. All values are hexadecimal.

| step | bytes | $k$ | MIX($k$) | $h$ after L4 or L9 | $h$ after L5 |
|---|---|---|---|---|---|
| L1 | | | | | 9747b28c |
| block 0 | Hell | 6c6c6548 | 0153080c | 9614ba80 | dae4c92e |
| block 1 | o, w | 77202c6f | 7d238cad | a7c74583 | 71c6b43c |
| block 2 | orld | 646c726f | a9bc9655 | d87a2269 | 3bd692af |
| tail | ! | 00000021 | ac5e5123 | 9788c38c | |
| L10 | $n = 13$ | | | 9788c381 | |
| L11 | | | | 24884cba | |

The result is $\mathtt{0x24884cba}$. The hash of the empty string with seed 0 is 0, because FMIX(0) = 0; with seed 1 it is $\mathtt{0x514e28b7}$. The implementation below reproduces the verification value $\mathtt{0xB0F57EE3}$ of SMHasher, which hashes the 256 keys $(0), (0, 1), \ldots$, starting with the empty key, under the seeds $256, 255, \ldots, 1$ and then hashes the 1024 bytes of results with seed 0.

**A collision for every seed.** The block mix is a bijection and does not use the seed, so it can be inverted. Take any two blocks $x_1, x_2$, and choose $y_1, y_2$ with $\mathrm{MIX}(y_1) = \mathrm{MIX}(x_1) \oplus \mathtt{0x00040000}$ and $\mathrm{MIX}(y_2) = \mathrm{MIX}(x_2) \oplus \mathtt{0x80000000}$. After line L4 on the first block, the two states differ only in bit 18; ROTL by 13 moves it to bit 31; multiplying by 5 and adding a constant keep a difference in bit 31 alone, since $5 \cdot 2^{31} \equiv 2^{31} \pmod{2^{32}}$; and the XOR of the second block cancels it. For $x = $ abcdefgh, that is the bytes 61 62 63 64 65 66 67 68, this gives $y = $ 09 c1 42 6f 65 66 b6 2c. The two hashes are equal for every seed: $\mathtt{0x49ddccc4}$ for seed 0, $\mathtt{0x35098aba}$ for seed 1, $\mathtt{0x89432667}$ for seed $\mathtt{0xffffffff}$. With $t$ such pairs placed one after another, all $2^t$ choices of one block pair from each give strings of $8t$ bytes with one hash for every seed.

**Avalanche, measured.** For 2000 random 4-byte keys and each of the 32 input bits, flipping the bit flipped each of the 32 output bits in 45.7% to 53.3% of the keys, with a mean of 50.0%. This is a measurement, not a proof; for 2000 samples, the standard deviation of each fraction is about 1.1%.

## Correctness

MurmurHash3 is defined by its reference code, so correctness means that the procedure computes the same function as MurmurHash3.cpp of SMHasher and has the properties below. The test file checks the procedure against a direct transcription of the C code, with the fall-through of its switch statement written out, on random inputs, and against the SMHasher verification value. The proofs of the structural properties rest on one fact: each of the operations XOR with a constant, ROTL, multiplication by an odd constant, addition of a constant, and $x \mapsto x \oplus (x \gg r)$ for $r \ge 1$ is a bijection of the 32-bit words. So MIX and FMIX are bijections, and for a fixed input the map from the seed to the hash is a bijection. The proof file below gives the details.

## Complexity

- **Time.** Lines L3 to L5 run $\lfloor n/4 \rfloor$ times and lines L6 to L11 once, each with $O(1)$ word operations: $\Theta(n)$ in all. Reading every byte is necessary for a hash that depends on all bytes.
- **Space.** One 32-bit state and one block: $O(1)$.
- **In practice.** Each block costs three multiplications, but the two in MIX do not depend on the state, so a processor can overlap them with the work of the previous block; only the multiplication by 5 in line L5 is on the chain from block to block. The SMHasher wiki reports about 3 GB per second for the 32-bit version on a 2008 desktop processor, several times the speed of byte-at-a-time hashes such as [FNV](/fnv-hash/) on long inputs.

## Properties

- **Deterministic for a fixed seed.** The output depends only on the input and the seed.
- **Not collision-free, and no bound for chosen inputs.** With $2^{32}$ values, any $2^{32} + 1$ inputs contain a collision, and if the outputs behave like random values a collision is expected among about $\sqrt{\pi 2^{31}} \approx 82\,000$ inputs, by the [birthday paradox](/birthday-paradox/); this is a heuristic. The construction in the example gives inputs that collide for every seed, so a random seed gives no bound of the form $\Pr[h_s(x) = h_s(y)] \le \varepsilon$ for all fixed $x \ne y$.
- **Distinct seeds, distinct hashes.** For a fixed input, every step is a bijection of the state, so different seeds give different hashes of the same input.
- **One changed block.** Two inputs of the same length that differ only within one 4-byte block, or only within the tail, never collide.
- **Suffix extension.** Two inputs of the same length with equal states after line L5 at a block boundary stay equal for every common suffix. This is why the colliding pairs above extend to multicollisions and survive appended data.
- **Avalanche.** FMIX was tuned so that each input bit affects each output bit with probability close to $1/2$; the constants $f_1$, $f_2$ came from a simulated-annealing search, according to the SMHasher wiki. This is an empirical property.

## Variants and improvements

- **MurmurHash3_x86_128 and MurmurHash3_x64_128.** Four 32-bit lanes or two 64-bit lanes with cross mixing, for 128-bit identifiers of large blocks; the x64 version is the fastest on 64-bit machines.
- **MurmurHash2 and MurmurHash64A.** The earlier versions with one multiplier $\mathtt{0x5bd1e995}$ (or its 64-bit form); MurmurHash2 also has collisions that do not depend on the seed.
- **Use as a building block.** Many libraries use FMIX alone, or its 64-bit form fmix64, as an integer mixer, and some [Bloom filter](/bloom-filter/) libraries derive their $k$ hash functions from the two halves of one 128-bit MurmurHash3 value.
- **Successors.** [xxHash](/xxhash/) and later designs read more bytes per step and are faster on long inputs; for inputs an attacker may choose, [SipHash](/siphash/) is a keyed function designed to resist the attacks above.

## When to use it

Use MurmurHash3 for hash tables, Bloom filters, sharding and sketches when the keys come from trusted sources and speed matters, for example inside a database engine or a data pipeline. Use the 32-bit version for table indices and the x64 128-bit version for identifiers of large blocks, where the chance of an accidental collision must be tiny; for 128-bit values a random-looking hash collides by accident among about $2^{64}$ blocks. Do not use it where an attacker chooses the keys, as in a web server or a parser of external input: there use [SipHash](/siphash/) with a secret random key. Do not use it as a [cryptographic hash function](/cryptographic-hash-function/). When a provable collision bound is needed, use a member of a [universal hash family](/universal-hash-family/) chosen at random.

## Pitfalls

- **Treating the seed as a key.** A random seed per process does not stop hash flooding: the colliding inputs above do not depend on it. In 2012, Java and Ruby implementations that used MurmurHash with random seeds were shown to be open to this attack.
- **Endianness and alignment.** The reference code reads blocks with a native 32-bit load. On a big-endian machine this gives different hashes, unless the code reads the bytes in little-endian order as on this page. Unaligned loads may also fault on some processors.
- **Mixing up the variants.** The x86_32, x86_128 and x64_128 versions, and MurmurHash2, give different values. Stored hashes must name the variant and the seed.
- **Signed arithmetic and the length.** The length enters as `len` in line L10; in the reference code it is an `int`, so inputs of $2^{31}$ bytes or more are not covered by the reference. In languages without unsigned 32-bit integers, every operation must be reduced modulo $2^{32}$, and shifts must be logical.
- **Unequal hashes are proof, equal hashes are not.** A hash table must still compare keys. Using a 32-bit hash as the identity of a record mixes up records after about 82 000 records, by the birthday estimate.

## Implementations

## History

Austin Appleby published the first MurmurHash in 2008 and soon replaced it by MurmurHash2, which became widely used in hash tables. MurmurHash3, with the block mix, the finalizer and the 128-bit versions, was finished in 2011 together with SMHasher, Appleby's test suite for the distribution, collision and speed of non-cryptographic hashes. In December 2012, Jean-Philippe Aumasson, Daniel J. Bernstein and Martin Bosslet showed at the 29th Chaos Communication Congress that MurmurHash2 and MurmurHash3 have collisions independent of the seed, and used them to slow down Ruby and Java servers; they proposed SipHash as the replacement, and several language runtimes adopted it. The code moved from Google Code to GitHub in 2016.

## References
