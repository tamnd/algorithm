---
tag: N2JG8C
kind: algorithm
slug: blake3
name: BLAKE3
aliases:
- BLAKE3 hash
area: cryptography/hash-functions
level: advanced
summary: A tree hash built from a 7-round BLAKE2s compression. One function gives hash, keyed hash, key derivation and output of any length, and it runs in parallel over 1 KiB chunks.
model: word-ram
complexity:
  vars: {n: the input length in bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(log n)}
properties: {deterministic: true}
history:
  year: 2020
  people: [Jack O'Connor, Jean-Philippe Aumasson, Samuel Neves, Zooko Wilcox-O'Hearn]
  note: BLAKE3 was announced in January 2020. It joins the BLAKE2s compression, cut to 7 rounds, with a binary tree of 1 KiB chunks.
prereqs: [blake2, merkle-tree, extendable-output-function]
see_also: [tree-hashing, shake, sha-3, sha-2, hkdf, hmac, indifferentiability-framework, xxhash]
sources:
  - url: "https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.pdf"
    title: "Jack O'Connor, Jean-Philippe Aumasson, Samuel Neves and Zooko Wilcox-O'Hearn, BLAKE3: one function, fast everywhere, 2020"
    locator: Section 2 (specification), Section 3 (performance), Section 4 (security goals, compression function, mode of operation, cryptanalysis), Section 5.1.2 (chaining value stack), Section 6.4 (verified streaming)
  - url: "https://github.com/BLAKE3-team/BLAKE3"
    title: BLAKE3 official repository, with the reference implementation and test vectors
    locator: reference_impl/reference_impl.rs and test_vectors/test_vectors.json
  - paper: "Joan Daemen, Bart Mennink and Gilles Van Assche, Sound hashing modes of arbitrary functions, permutations, and block ciphers, IACR Transactions on Symmetric Cryptology 2018(4), pages 197 to 228"
    locator: the conditions of subtree-freeness, radical-decodability and message-completeness, and Theorem 1, as applied in Section 4.3 of the BLAKE3 paper
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, Sufficient conditions for sound tree and sequential hashing modes, International Journal of Information Security 13(4), 2014, pages 335 to 353"
    locator: the earlier conditions of tree decodability, message completeness and final-node separability
  - paper: "Jean-Philippe Aumasson, Too much crypto, Real World Crypto 2020, IACR ePrint 2019/1492"
    locator: the argument for fewer rounds in BLAKE2 and other primitives, which BLAKE3 follows with 7 rounds
  - url: "https://www.rfc-editor.org/rfc/rfc7693"
    title: "M-J. Saarinen and J-P. Aumasson, RFC 7693, The BLAKE2 Cryptographic Hash and MAC, 2015"
    locator: Section 3.1 (the function G that BLAKE3 uses unchanged with the BLAKE2s rotations)
---

BLAKE3 is a cryptographic hash function by Jack O'Connor, Jean-Philippe Aumasson, Samuel Neves and Zooko Wilcox-O'Hearn (2020). It cuts the input into chunks of 1024 bytes, hashes each chunk with the [BLAKE2s](/blake2/) compression function reduced to 7 rounds, and joins the chunk results in a binary [Merkle tree](/merkle-tree/). The chunks are independent, so BLAKE3 can use all SIMD lanes and cores. The same function, with different flags, is a hash, a keyed hash (a MAC and a PRF), a key derivation function, and an [extendable-output function](/extendable-output-function/).

**Notation.** $C(k, b, t, \ell, d)$ is the compression function: chaining value $k$ (8 words of 32 bits), block $b$ (64 bytes), counter $t$ (64 bits), block length $\ell$ in bytes, and flags $d$. $IV$ is the SHA-256 initial value. A chaining value (CV) is the first 8 words of an output of $C$. The flags are CHUNK_START = 1, CHUNK_END = 2, PARENT = 4, ROOT = 8, KEYED_HASH = 16, DERIVE_KEY_CONTEXT = 32, DERIVE_KEY_MATERIAL = 64. $n$ is the input length in bytes. The security goal is 128-bit security for collisions, preimages and indifferentiability, in the model of the [indifferentiability framework](/indifferentiability-framework/) with an ideal compression function.

## In plain words

A normal hash reads the input from start to end, so one core does all the work. BLAKE3 cuts the input into pieces of 1 KiB and hashes each piece on its own, with the number of the piece mixed in. Then it hashes the piece results two at a time, then those results two at a time, and so on, until one value is left. This is a tree, and the work on each level can be done in parallel.

Every compression also gets flags that say what it is: a first or last block of a piece, a joining node, the root, or a keyed or key derivation use. So no value of one kind can be mistaken for a value of another kind. The root can be run again with a counter to give as many output bytes as needed.

## The problem

The goal is one hash function that is secure as a hash, a MAC, a PRF, a KDF and an XOF, and that is faster than [SHA-2](/sha-2/), [SHA-3](/sha-3/) and BLAKE2 on every platform. Speed on long inputs needs parallel work, which a sequential [Merkle-Damgård](/merkle-damgard-construction/) chain cannot give. The tree must be sound: a collision of the tree hash must give a collision of the compression function, and the output must look random even though the attacker can see how the tree is built.

## The algorithm

```pseudo id=main
BLAKE3(x, L, k = IV, d0 = 0)                     ▷ O'Connor et al., Section 2
L1  cut x into chunks of 1024 bytes (the last may be shorter; one empty chunk if x is empty)
L2  for each chunk j: cut it into blocks of 64 bytes;  c ← k
        for each block b except the last: c ← first 8 words of C(c, b, j, 64, d0 | START if first)
L3      the chunk node is (c, last block padded, j, its length, d0 | END | START if first)
L4  if there is one chunk, its node is the root;  otherwise split the chunks:
        the left subtree has the largest power of 2 chunks that leaves at least 1 chunk on the right;
        node ← (k, CV(left subtree) ‖ CV(right subtree), 0, 64, d0 | PARENT);  CV(node) = first 8 words of C(node)
L5  output: for i ← 0, 1, ... take the 64 bytes of C(root with counter i and flags | ROOT); return the first L bytes

C(k, b, t, ℓ, d)                                  ▷ Section 2.2
L6  s ← k[0..7] ‖ IV[0..3] ‖ (t mod 2^32, ⌊t / 2^32⌋, ℓ, d);  m ← the 16 words of b
L7  repeat 7 times: one BLAKE2s round of 8 calls to G on s with m in order;  permute m (not after the last round)
L8  return (s[i] ⊕ s[i + 8] for i = 0..7) ‖ (s[i + 8] ⊕ k[i] for i = 0..7)

L9  G is the BLAKE2s mixing function with rotations 16, 12, 8, 7
L10 modes:  hash: k = IV, d0 = 0.   keyed_hash(K): k = K, d0 = KEYED_HASH.
            derive_key(ctx, M): K' ← BLAKE3(ctx, 32, IV, DERIVE_KEY_CONTEXT);  BLAKE3(M, L, K', DERIVE_KEY_MATERIAL)
```

The permutation of the message words is $(2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)$. It replaces the ten SIGMA tables of BLAKE2. The output of $C$ has 16 words: the first 8 are a chaining value, and all 16 are 64 bytes of root output. Line L4 gives a left-heavy tree whose shape depends only on $n$. The incremental form of line L4 keeps a stack of CVs: after chunk number $c$ is done, it merges the top of the stack once for each trailing zero bit of $c$.

## Example

**Empty input.** Line L1 gives one empty chunk, so line L3 gives the node $(IV, 0^{64}, 0, 0, \text{START} \mid \text{END})$, and it is the root. Line L5 computes $C(IV, 0^{64}, 0, 0, 1 \mid 2 \mid 8 = 11)$, whose first bytes are `af1349b9f5f9a1a6 a0404dea36dcc949 9bcb25c9adc112b7 cc9a93cae41f3262`, the value in the official test vectors. With $i = 1$ and $i = 2$, line L5 extends this to the 131 bytes of the vector file.

**Tree shapes.** The official vectors use inputs of bytes $0, 1, \ldots, 250, 0, 1, \ldots$ For $n = 2049$ there are 3 chunks, the last of 1 byte. The left subtree gets 2 chunks, so the root is PARENT(PARENT(chunk 0, chunk 1), chunk 2). For $n = 3073$ there are 4 chunks and the root is PARENT(PARENT(0, 1), PARENT(2, 3)). For $n = 8193$ there are 9 chunks: the left subtree is the complete tree on chunks 0 to 7 and the right subtree is chunk 8 alone. The 32-byte hashes begin `5f4d72f4`, `7124b495` and `bab6c09c`.

## Correctness

The code computes BLAKE3: the tests check the full 131-byte outputs for the empty input in all three modes, and the first 32 bytes of hash, keyed_hash and derive_key for 8 more lengths from 1 to 8193 bytes, which cover partial blocks, one full chunk, and trees of depth 1 to 4. The incremental hasher gives the same values.

**The tree is sound.** Daemen, Mennink and Van Assche (2018) show that a tree mode over an ideal inner function is indifferentiable from a random oracle when three conditions hold, and Section 4.3 of the BLAKE3 paper checks them. Subtree-freeness: only the last compression has the ROOT flag, so no valid tree is a subtree of another, which stops length extension. Radical-decodability: the flags tell a chunk from a parent, so the shape of the tree cannot be read in two ways. Message-completeness: every input byte enters some compression, and the block length $\ell$ fixes how many bytes of the last block are data. The resulting bound, for $q$ queries and outputs up to 256 bits, is small while $q$ stays far below $2^{128}$, which is the 128-bit target. It is tight in that sense: a generic collision on 256-bit CVs costs about $2^{128}$ calls.

**The compression function.** Section 4.2 of the paper notes that the full 16-word output of $C$ is not indifferentiable from a random function, because the second half has a feed-forward and the first half has none, so an attacker can invert it as in Davies-Meyer. The truncated 8-word output, used everywhere except the root, is indifferentiable when the inner block cipher is ideal. For the root, the paper argues that the feed-forward plays the role of the truncation. The claim that the real 7-round $C$ behaves like an ideal one is a conjecture backed by ten years of analysis of BLAKE and BLAKE2 (Section 4.4).

**Domain separation of the modes.** The KEYED_HASH and DERIVE_KEY flags are inputs to every compression, so the three modes behave as unrelated functions even with the same key. The proofs file gives the arguments.

## Complexity

An input of $n \ge 1$ bytes has $c = \lceil n / 1024 \rceil$ chunks and $\lceil n / 64 \rceil$ blocks. BLAKE3 makes one compression per block, $c - 1$ parent compressions, and $\lceil L / 64 \rceil - 1$ extra root compressions for an output of $L$ bytes. Each compression makes 56 calls to $G$ (7 rounds of 8), so the cost is about 0.875 calls to $G$ per input byte, against 1.25 for BLAKE2s. The incremental form keeps at most $\lceil \log_2 c \rceil + 1$ CVs of 32 bytes, plus one chunk in progress. With $P$ processors the time is $O(n / P + \log n)$ calls to $G$, because the tree has depth $\lceil \log_2 c \rceil$.

## Properties

- **One function, many modes**: hash, keyed hash, key derivation and XOF, with domain separation by flags.
- **Output of any length.** The first 32 bytes are the default hash, and any longer output starts with them.
- **Parallel**: chunks are independent; on wide SIMD units, 8 or 16 chunks run at once.
- **Verified streaming.** A receiver who knows the root can check each chunk with its path of CVs, as in a Merkle tree; the Bao tool does this.
- **Fixed 128-bit security**. Longer outputs do not raise it; this differs from SHA-512.

## Variants and improvements

- **[BLAKE2](/blake2/)**, sequential, with 10 or 12 rounds and digest lengths in the parameter block.
- **Bao**, by O'Connor, a tool that encodes a file with its tree of CVs for verified streaming (Section 6.4).
- **KangarooTwelve**, the tree mode over Keccak-p with 12 rounds, the analogue of BLAKE3 in the Keccak family; see [tree hashing](/tree-hashing/).

## When to use it

Use BLAKE3 to hash large files, to build content-addressed storage, to check downloads, and to derive keys from a strong secret when no standard requires something else. Its XOF output replaces ad hoc counters around SHA-256. Use [SHA-2](/sha-2/) or [SHA-3](/sha-3/) where FIPS approval is needed. Do not use it for passwords; use [Argon2](/argon2/). For hash tables with attacker-chosen keys, [SipHash](/siphash/) is enough and smaller.

## Pitfalls

- **derive_key with a secret context.** The context string is meant to be a fixed constant chosen by the program; the secret goes into the key material.
- **Expecting more than 128-bit security from a longer output.** The CVs have 256 bits, so collisions inside the tree cost about $2^{128}$ whatever the output length.
- **Hashing a tree of your own over BLAKE3 outputs** with no flags or prefixes, which can lose the domain separation that BLAKE3 has inside.
- **Using a key that is not uniform.** keyed_hash needs a 32-byte random key; for a password or a short secret use derive_key or a password hash.

## Implementations

The Python code is for study only, is not constant time, and must not protect real data. Use the official `blake3` Rust crate, the C library in the same repository, or the `blake3` Python package. The code gives `g` (line L9), `compress` (lines L6 to L8), `chunk_node` (lines L2 and L3), `tree_node` (lines L1 and L4), `Node.root_output` (line L5), `blake3` and `derive_key` (line L10), and `Hasher`, the incremental form with a CV stack. The official vectors are copied by hand from `test_vectors.json`. The tests also check that the incremental hasher matches the recursive one, that the stack stays small, that a wrong key gives a different tag, that keyed_hash and derive_key differ, and that one changed input bit changes about half of the output bits. Python has no BLAKE3 in its standard library, so there is no second check from `hashlib`.

## History

BLAKE was a SHA-3 finalist in 2010, and BLAKE2 followed in 2012. Tree modes for hashing go back to Merkle, and Bertoni, Daemen, Peeters and Van Assche gave conditions for sound tree modes in 2014, which KangarooTwelve (2018) used over Keccak. Jack O'Connor had built Bao, a verified streaming tree, before BLAKE3. In January 2020 O'Connor, Aumasson, Neves and Wilcox-O'Hearn published BLAKE3, which joins a binary tree of 1 KiB chunks with a BLAKE2s compression cut from 10 to 7 rounds, in line with Aumasson's paper "Too much crypto" (Real World Crypto 2020), and adds the flags for the modes.

## References
