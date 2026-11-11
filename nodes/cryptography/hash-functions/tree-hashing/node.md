---
tag: EWH7SV
kind: technique
slug: tree-hashing
name: Tree hashing
aliases:
- parallel hashing
- hash tree mode
- tree hash mode
area: cryptography/hash-functions
level: advanced
summary: Hash the chunks of a message independently and combine their values in a tree, so many cores or SIMD lanes work at once. Domain separation of leaves, inner nodes and root keeps it sound.
prereqs: [merkle-tree, cryptographic-hash-function, indifferentiability-framework]
see_also: [blake3, blake2, skein, sponge-construction, merkle-damgard-construction, extendable-output-function, parallel-reduce, work-span-model]
sources:
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, Sufficient conditions for sound tree and sequential hashing modes, International Journal of Information Security 13(4), 2014, pages 335 to 353"
    locator: the three conditions tree-decodability, message-completeness and final-node separability, and the indifferentiability bound for modes that meet them (also ePrint 2009/210)
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, Sakura: a flexible coding for tree hashing, ACNS 2014, LNCS 8479"
    locator: the frame bits that mark message hops and chaining hops, and the proof that Sakura coding meets the sufficient conditions
  - url: "https://www.rfc-editor.org/rfc/rfc9861"
    title: "B. Viguier, D. Wong, G. Van Assche, Q. Dang and J. Daemen, RFC 9861, KangarooTwelve and TurboSHAKE, October 2025"
    locator: Section 3.2 (KT128, the 8192-byte chunks, the final node and the bytes 07, 0B and 06), Section 3.3 (length_encode), Section 5 (test vectors)
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters, Gilles Van Assche, Ronny Van Keer and Benoît Viguier, KangarooTwelve: fast hashing based on Keccak-p, ACNS 2018, LNCS 10892, pages 400 to 418"
    locator: the design of the tree mode with one level of leaves, and its speed with SIMD
  - url: "https://doi.org/10.6028/NIST.SP.800-185"
    title: "J. Kelsey, S. Chang and R. Perlner, NIST SP 800-185, SHA-3 Derived Functions: cSHAKE, KMAC, TupleHash and ParallelHash, December 2016"
    locator: Section 6 (ParallelHash, with blocks of B bytes hashed by cSHAKE and a single final call)
  - url: "https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.pdf"
    title: "Jack O'Connor, Jean-Philippe Aumasson, Samuel Neves and Zooko Wilcox-O'Hearn, BLAKE3: one function, fast everywhere, 2020"
    locator: Section 2 (the binary tree of 1024-byte chunks and the flags CHUNK_START, CHUNK_END, PARENT and ROOT), Section 4.3 (security of the mode)
  - url: "https://www.rfc-editor.org/rfc/rfc7693"
    title: "M.-J. Saarinen and J.-P. Aumasson, RFC 7693, The BLAKE2 Cryptographic Hash and Message Authentication Code (MAC), November 2015"
    locator: Section 2.5 (the parameter block, whose tree fields this RFC does not use)
  - paper: "Ralph C. Merkle, A digital signature based on a conventional encryption function, CRYPTO 1987, LNCS 293, pages 369 to 378"
    locator: the hash tree that authenticates many values with one root
---

Tree hashing is a way to build a hash function from a smaller one so that the work on a long message runs in parallel. The message is cut into chunks, each chunk is hashed on its own into a short chaining value, and the chaining values are hashed together, level by level, up to one root that gives the digest. A [Merkle tree](/merkle-tree/) does the same thing to authenticate many items, and the modern hash functions [BLAKE3](/blake3/), KangarooTwelve and ParallelHash use it for speed. A tree mode is secure only when each node input says what kind of node it is: a leaf, an inner node, or the root.

**Notation.** $F$ is the inner function, a [cryptographic hash function](/cryptographic-hash-function/) or a compression function with $n$-bit output, called the chaining value (CV). $M$ is the message, $B$ the chunk size in bytes, $k$ the number of chunks, and $a$ the arity (the number of children of an inner node). $\ell$ is the output length, and $\|$ is concatenation. LEAF, INNER and ROOT stand for the frame bits that mark the kind of a node. The security model is [indifferentiability](/indifferentiability-framework/) from a random oracle, with $F$ ideal and $q$ queries to it.

## In plain words

To hash a long file with one core, you read it from start to end. A chain cannot be split: each step needs the result of the step before.

A tree hash cuts the file into pieces. Each piece gets its own short hash, and many cores make these hashes at the same time. Then the short hashes are put in pairs, or in larger groups, and each group is hashed again. This goes on until only one hash is left.

Every input to the small hash function carries a label that says if it is a piece of the file, a group of hashes, or the last step. Without the labels, an attacker can pass a group of hashes off as a piece of a file and make two different files that give the same result.

## When it applies

- **Long messages and parallel hardware.** The speed-up needs at least as many chunks as there are cores or SIMD lanes. KangarooTwelve and BLAKE3 hash many chunks at once with vector instructions on one core.
- **Random access and incremental updates.** A change in one chunk needs only the path from that leaf to the root, $O(\log k)$ calls of $F$. A reader can check one chunk against the root with a proof of $O(\log k)$ CVs, as in verified streaming.
- **A fixed tree shape in the standard.** Both sides must build the same tree. The chunk size, the arity and the rule for the last, partial group must be fixed, or encoded in the node inputs.

It does not help for short messages, where one call of $F$ is the whole cost. Good modes, such as KangarooTwelve, then fall back to a single node with its own label.

## The template

```pseudo id=main
TREE-HASH(M)
L1  split M into chunks M0, …, Mk−1 of B bytes, with k ≥ 1   ▷ hole: chunk size B
L2  if k = 1 then return F(LEAF ‖ ROOT ‖ M0, ℓ)              ▷ hole: the single-node case
L3  for i ← 0 to k − 1 in parallel do
L4      vi ← F(LEAF ‖ i ‖ Mi, n)                               ▷ hole: the leaf encoding
L5  while more than a values are left do
L6      group the values, in order, into groups of at most a  ▷ hole: the tree shape
L7      replace each group (u1, …, uj) by F(INNER ‖ u1 ‖ … ‖ uj, n)
L8  return F(INNER ‖ ROOT ‖ the remaining values, ℓ)         ▷ hole: final-node separation
```

The holes are filled as follows by the main schemes.

- **Chunk size and shape.** BLAKE3 uses $B = 1024$ and a binary tree ($a = 2$) whose left subtree holds the largest power of 2 chunks that leaves at least one chunk on the right. KangarooTwelve uses $B = 8192$ and one level: all leaf CVs go into the final node. ParallelHash leaves $B$ to the caller and also has one level.
- **Labels.** BLAKE3 puts the flags CHUNK_START, CHUNK_END, PARENT and ROOT in the compression function input, and the chunk index as the counter. KangarooTwelve uses the Sakura coding: the leaves use the domain byte `0B`, the final node `06`, and a message of one chunk `07`. ParallelHash uses cSHAKE with an empty name for the leaves and the name "ParallelHash" for the final call.
- **The final node.** KangarooTwelve puts the first chunk $S_0$ into the final node, followed by `03 00 00 00 00 00 00 00`, the CVs, the number of CVs and `FF FF`. ParallelHash puts $B$, the CVs, the number of blocks and the output length into the final call.

**The sufficient conditions.** Bertoni, Daemen, Peeters and Van Assche (2014) show that a tree mode built on an ideal $F$ is indifferentiable from a random oracle, with an advantage of order $q^2 / 2^n$, if it meets three conditions.

1. **Tree-decodability.** From the inputs to $F$ alone, one can parse every node: which part is message, which part is CVs, and where each CV comes from. Line L4 and line L7 must not give the same kind of input.
2. **Message-completeness.** The whole message can be read back from the node inputs. Every bit of $M$ enters some call of $F$ once.
3. **Final-node separability.** The input to the final node differs from the input to every other node. So the output, which an attacker sees, is never a CV of a larger tree.

The bound is tight in the sense that a collision of $F$ on CVs, which costs about $2^{n/2}$ queries, breaks the mode. So the CV length $n$ must be twice the claimed collision security, for example $n = 256$ for 128-bit security.

## Classic examples

- **[Merkle trees](/merkle-tree/)**, with the leaf prefix `00` and the inner prefix `01` of RFC 6962, are a tree hash for authentication. Without the prefixes the mode is not tree-decodable, and a second preimage exists, as the tests of that page show.
- **[BLAKE3](/blake3/)** is a binary tree of 1024-byte chunks over a 7-round BLAKE2s compression function. Its flags meet the three conditions, and the root node can give output of any length.
- **KangarooTwelve** (KT128, RFC 9861) uses TurboSHAKE128, a Keccak-p permutation with 12 rounds, on 8192-byte chunks with one level of leaves, through Sakura coding. A message of up to 8192 bytes, after the customization string is added, costs one call.
- **ParallelHash** (SP 800-185, Section 6) hashes blocks of $B$ bytes with cSHAKE128 or cSHAKE256 and joins the CVs in one final cSHAKE call. It is a NIST standard with the same goal as KangarooTwelve, but it uses the full 24 rounds of Keccak.
- **[BLAKE2](/blake2/) tree mode.** The parameter block of BLAKE2 holds fanout, depth, leaf length, node offset, node depth and inner length, and a last-node flag. BLAKE2bp and BLAKE2sp use 4 and 8 leaves that take blocks in turn, not contiguous chunks, and one root.
- **[Skein](/skein/)** has an optional tree mode built from UBI calls, with the leaf size, fanout and maximum height in its configuration.

## Variations

- **Fixed number of leaves.** BLAKE2bp and BLAKE2sp always use 4 or 8 leaves, which is simple but caps the parallelism.
- **One level of leaves.** KangarooTwelve and ParallelHash have a final node that takes all CVs. The final node grows with $k$, but it is still cheap: 32 bytes per 8192 bytes of message for KT128.
- **Full trees of any height.** BLAKE3 and Merkle trees grow with $\log k$ levels, which allows proofs of one chunk and incremental updates.
- **Interleaved leaves.** BLAKE2bp gives block $j$ to leaf $j \bmod 4$, so each leaf sees a strided part of the message. Contiguous chunks are better for streaming and for proofs.
- **Sequential modes as a special case.** A tree of height $k$ with arity 2, where each inner node takes one CV and one chunk, is the [Merkle-Damgård construction](/merkle-damgard-construction/). The sufficient conditions cover both.

## Pitfalls

- **No label on leaves and inner nodes.** An inner node input is two CVs, which also looks like a leaf of $2n$ bits. The root of a tree is then also the root of a smaller tree whose leaves are CVs. RFC 6962 adds the prefixes `00` and `01` for this reason.
- **No final-node flag.** If the root is computed like an inner node, its output is a valid CV, and an attacker can extend the tree with it, as in a [length extension attack](/length-extension-attack/).
- **Shape that is not encoded.** If the rule for an odd last group duplicates the last CV, two messages of different length give the same root. Bitcoin had this flaw in its Merkle tree (CVE-2012-2459).
- **Different parameters give different functions.** BLAKE2bp and BLAKE2b give different digests for the same input, and a KT128 value is not a TurboSHAKE128 value. Fix the mode in the protocol.
- **Too short CVs.** A CV of $n$ bits gives at most $n/2$ bits of collision security for the whole tree, whatever the output length.
- **Memory for the CV stack.** A streaming hasher for a binary tree keeps up to $\log_2 k$ CVs. A one-level mode needs either the whole list of CVs or a running final node, as KangarooTwelve has.

## Exercises

1. A tree mode hashes a message of 3 chunks with a binary tree and computes the leaves as vi = F(Mi) and the root as F(v0 ‖ F(v1 ‖ v2)), with no labels, and a message of one chunk as F(M0). Find a different message, of one chunk, with the same root.
2. Count the calls of $F$ and the depth (the longest chain of dependent calls) of BLAKE3 for $k = 1000$ chunks, and of KT128 for the same message, with chunks of 8192 bytes.
3. Show that the Merkle-Damgård construction with length padding meets message-completeness and tree-decodability. Which change gives it final-node separability?

## References
