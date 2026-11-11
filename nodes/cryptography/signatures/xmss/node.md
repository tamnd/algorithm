---
tag: CAW1KT
kind: algorithm
slug: xmss
name: XMSS
aliases:
- XMSS-MT
- eXtended Merkle Signature Scheme
- XMSS^MT
- Multi-tree XMSS
area: cryptography/signatures
level: advanced
summary: "Stateful hash-based signature of RFC 8391 and NIST SP 800-208. WOTS+ keys are compressed by L-trees into a Merkle tree, and every hash call gets its own key and bitmask."
model: word-ram
complexity:
  vars: {h: the tree height, l: the number of WOTS+ chains, w: the chain length}
  time: {worst: Θ(2^h·l·w), average: Θ(2^h·l·w), best: Θ(2^h·l·w)}
  space: {extra: Θ(2^h)}
properties: {deterministic: true}
history:
  year: 2011
  people: [Johannes Buchmann, Erik Dahmen, Andreas Hülsing]
  note: XMSS appeared at PQCrypto 2011. RFC 8391 (May 2018) by Hülsing, Butin, Gazdag, Rijneveld and Mohaisen specified XMSS and XMSS^MT with WOTS+.
prereqs: [merkle-signature-scheme, winternitz-one-time-signature]
see_also: [leighton-micali-signature, sphincs-plus, forward-secure-signature, lamport-signature, hash-based-signatures, second-preimage-resistance, merkle-tree, sha-2]
sources:
  - paper: doi:10.1007/978-3-642-25405-5_8
    title: "Johannes Buchmann, Erik Dahmen and Andreas Hülsing, XMSS: A practical forward secure signature scheme based on minimal security assumptions, PQCrypto 2011, LNCS 7071, pages 117 to 129"
    locator: the XMSS tree with bitmasks, the L-tree, the forward secure key generation, and the security proof from second preimage resistance and a pseudorandom function family
  - url: "https://www.rfc-editor.org/rfc/rfc8391"
    title: "Andreas Hülsing, Denis Butin, Stefan-Lukas Gazdag, Joost Rijneveld and Aziz Mohaisen, RFC 8391, XMSS: eXtended Merkle Signature Scheme, May 2018"
    locator: Section 2.5 (addresses), Section 3.1 (WOTS+), Section 4.1 (XMSS, L-trees, signing and verification), Section 4.2 (XMSS^MT), Section 5 (parameter sets and Table 3), Section 9 (security)
  - paper: doi:10.1007/978-3-662-49384-7_15
    title: "Andreas Hülsing, Joost Rijneveld and Fang Song, Mitigating multi-target attacks in hash-based signatures, PKC 2016, LNCS 9614"
    locator: the security proof of the RFC form with addresses and keyed hash calls (multi-function multi-target second preimage resistance)
  - paper: doi:10.1007/978-3-642-40588-4_14
    title: "Andreas Hülsing, Lea Rausch and Johannes Buchmann, Optimal parameters for XMSS^MT, CD-ARES 2013, LNCS 8128"
    locator: the multi-tree variant and the choice of its parameters
  - url: "https://doi.org/10.6028/NIST.SP.800-208"
    title: "David A. Cooper and others, NIST SP 800-208, Recommendation for Stateful Hash-Based Signature Schemes, October 2020"
    locator: the approval of XMSS and XMSS^MT and the rules on state management
---

XMSS (eXtended Merkle Signature Scheme) is the [Merkle signature scheme](/merkle-signature-scheme/) built so that its security needs only second preimage resistance and a pseudorandom function, not collision resistance. Its leaves are [WOTS+](/winternitz-one-time-signature/) one-time keys, each compressed to one value by an unbalanced hash tree, the L-tree. Every hash call in the tree, the L-trees and the chains uses its own key and bitmask, made by a pseudorandom function from a public seed and the 32-byte address of the call. The message is hashed with a fresh random value, the root and the index. XMSS is stateful, and XMSS$^{MT}$ stacks trees to sign up to $2^{60}$ messages. RFC 8391 (2018) and NIST SP 800-208 (2020) standardize it.

**Notation.** The page follows RFC 8391. $n = 32$ bytes, $w = 16$ is the WOTS+ chain length (RFC 8391 meaning), $len = 67$ is the number of chains, and $h$ is the tree height (10, 16 or 20 in the standard sets). $SEED$ is the public seed, $SK\_SEED$ and $SK\_PRF$ are secret seeds, $idx$ is the leaf index (the state), and $ADRS$ is the address. $F$, $H$, $H\_msg$ and PRF are SHA-256 with the prefixes 0, 1, 2 and 3 (as 32-byte numbers), a key and the input. The security notion is EUF-CMA for at most $2^h$ signatures, in the standard model.

## In plain words

XMSS is a Merkle tree of one-time keys, like LMS, with two extra ideas.

First, it never relies on the hash being collision resistant. Each time it hashes, it first XORs the input with a random mask and uses a random key, and each hash call in the whole structure gets its own key and mask. A forger then must find a second input for a hash value it did not choose, which is a harder task than finding any collision.

Second, the one-time public key has 67 values, and XMSS hashes them into one leaf with a small tree of its own, the L-tree, which uses masks too.

As with every Merkle scheme, each leaf signs one message, so the signer keeps a counter.

## The problem

Build a many-time signature from a hash function with the weakest possible assumption. Collision resistance can be broken in time about $2^{n/2}$ (and maybe $2^{n/3}$ with quantum computers), while second preimage resistance costs $2^n$ to break generically. A scheme that needs only second preimage resistance can therefore use hash values of half the length for the same security, which halves the signature. The scheme should also be forward secure if the key is evolved, and should give exact formats for interoperation.

## The algorithm

```pseudo id=main
RAND_HASH(L, R, ADRS)                            ▷ one masked tree hash
L1  KEY ← PRF(SEED, ADRS, 0); BM0 ← PRF(SEED, ADRS, 1); BM1 ← PRF(SEED, ADRS, 2)
L2  return H(KEY, (L ⊕ BM0) ‖ (R ⊕ BM1))

LTREE(pk[0..len−1], ADRS)                        ▷ compress a WOTS+ public key
L3  while len > 1: hash pairs (2i, 2i+1) with RAND_HASH, move an odd last value up, len ← ⌈len/2⌉
L4  return pk[0]

XMSS_SIGN(SK, M)
L5  idx ← SK.idx; if idx = 2^h then fail; SK.idx ← idx + 1    ▷ store the state first
L6  r ← PRF(SK_PRF, toByte(idx, 32))
L7  M' ← H_msg(r ‖ root ‖ toByte(idx, n), M)
L8  σ_ots ← WOTS+_SIGN(M', key idx); auth ← authentication path of leaf idx
L9  return (idx, r, σ_ots, auth)

XMSS_VERIFY((root, SEED), M, (idx, r, σ_ots, auth))
L10 M' ← H_msg(r ‖ root ‖ toByte(idx, n), M)
L11 node ← LTREE(WOTS+_PK_FROM_SIG(σ_ots, M', idx))
L12 for k ← 0 to h − 1: node ← RAND_HASH(node, auth[k]) if bit k of idx is 0, else RAND_HASH(auth[k], node)
L13 return node = root
```

The address of a call has eight 32-bit words: the layer and tree (for XMSS$^{MT}$), a type (0 for a chain step, 1 for an L-tree node, 2 for a tree node), the leaf index or L-tree number, the chain number or node height, the step number or node index, and a last word that selects the key (0) or a bitmask (1, 2). Line L1 derives the key and both bitmasks of one tree hash from $SEED$ and the address. A WOTS+ chain step is the same with one bitmask: $x \mapsto F(KEY, x \oplus BM)$. The public key is the root and $SEED$ (64 bytes, plus a 4-byte type code). The message hash of line L7 includes the root and the index, so each hash value that an attacker sees belongs to one key and one position.

The L-tree of line L3 halves the list in each round. With $len = 67$ it goes $67 \to 34 \to 17 \to 9 \to 5 \to 3 \to 2 \to 1$: seven rounds and 66 masked hashes, with an odd value carried up three times.

## Example

The signature of XMSS-SHA2_10_256 ($h = 10$, $n = 32$, $w = 16$, $len = 67$) is 2500 bytes:

| field | bytes |
|---|---|
| index $idx$ | 4 |
| randomness $r$ | 32 |
| WOTS+ signature, 67 values | 2144 |
| authentication path, 10 nodes | 320 |

Take leaf $idx = 6$ of a tree of height 4 (the test height). Its bits from the bottom are 0, 1, 1, 0. The verifier rebuilds leaf 6 through the L-tree, then hashes it with $auth_0$ (leaf 7) on the right, with the address of height 0 and index 3; then with $auth_1$ (node 2 of height 1) on the left, at height 1 and index 1; then with $auth_2$ (node 0 of height 2) on the left, at height 2 and index 0; and last with $auth_3$ (node 1 of height 3) on the right, at height 3 and index 0. The result must be the root. Each of these four calls has its own key and two bitmasks.

## Correctness

**Correctness.** Each hash call has a key and bitmasks fixed by its address, so the chain steps, L-tree nodes and tree nodes are fixed functions of their positions. The verifier continues each WOTS+ chain from the signed position with the same steps that key generation used, gets the same WOTS+ public key, the same L-tree value, and climbs the path as in the Merkle signature scheme to the root. The full proof is below.

**Security.** Section 9.1 of RFC 8391 points to the proof of Hülsing, Rijneveld and Song (2016): a forger must break the multi-function multi-target second preimage resistance of $F$ or $H$, the pseudorandomness of PRF, or the multi-target extended target collision resistance of $H\_msg$. The bitmasks let a reduction place its challenge as the honest input of any one hash call. The RFC message hash $H\_msg(r \| root \| idx, M)$ differs from the hash in the proof; the RFC argues that it stops multi-user attacks on the message hash and costs $2^n$ calls in the random oracle model.

## Complexity

With the whole tree stored, signing costs one WOTS+ signature and no tree work; key generation costs $2^h$ leaves. With the BDS traversal (as in the RFC reference code), RFC 8391 Table 3 counts the worst-case calls of $F$ and $H$:

| parameter set | signature (bytes) | key generation | signing | verification | signatures |
|---|---|---|---|---|---|
| XMSS-SHA2_10_256 | 2500 | 1,238,016 | 5,725 | 1,149 | $2^{10}$ |
| XMSS-SHA2_16_256 | 2692 | $79 \cdot 10^6$ | 9,163 | 1,155 | $2^{16}$ |
| XMSS-SHA2_20_256 | 2820 | $1268 \cdot 10^6$ | 11,455 | 1,159 | $2^{20}$ |

Each $F$ or $H$ call also needs two or three PRF calls for its key and masks, which the table does not count. Key generation is $\Theta(2^h \cdot len \cdot w)$; this is why XMSS$^{MT}$ exists.

## Properties

- **Stateful.** The index must never repeat. RFC 8391 Section 4.1.12 allows split keys for load balancing only if each index is still used once.
- **Minimal assumptions.** Second preimage resistance and a pseudorandom function suffice; collision resistance is not needed, so $n = 32$ bytes gives about 256 classical bits for the tree hashes.
- **Deterministic.** The randomness $r$ comes from $SK\_PRF$ and the index, so signing needs no random source.
- **Forward security (in the 2011 design).** If the WOTS+ seeds come from a forward-secure pseudorandom generator, and the signer deletes old seeds, a key that leaks at index $i$ cannot sign with an earlier index. The RFC derives all seeds from one fixed seed, which is not forward secure. See [forward-secure signatures](/forward-secure-signature/).
- **Many PRF calls.** Each masked hash costs two or three extra PRF calls, more than in [LMS](/leighton-micali-signature/), which uses one hash per step.

## Variants and improvements

- **XMSS$^{MT}$ (RFC 8391 Section 4.2).** A hypertree of $d$ layers of XMSS trees of height $h/d$. The tree on each layer signs the root of a tree below it with WOTS+, and the bottom trees sign messages. The signature holds $d$ WOTS+ signatures and $d$ paths, and the index has $\lceil h/8 \rceil$ bytes. Key generation needs only the top tree, so $h = 60$ is possible. The parameter sets range from XMSSMT-SHA2_20/2_256 to XMSSMT-SHA2_60/12_256.
- **SHAKE and 512-bit sets.** RFC 8391 defines SHAKE128 and SHA2-512 versions; SP 800-208 adds SHA-256/192 and SHAKE256 with 24 and 32 bytes.
- **[SPHINCS+](/sphincs-plus/) (SLH-DSA).** A stateless hypertree of XMSS-like trees with a few-time signature at the bottom. It reuses the address and masking ideas of XMSS.
- **The 2011 design.** The original XMSS used a Winternitz scheme built on a pseudorandom function family and a forward-secure key generation. RFC 8391 uses WOTS+ and the address scheme of Hülsing, Rijneveld and Song.

## When to use it

Use XMSS or XMSS$^{MT}$ where a stateful signature fits: firmware and software signing, code signing with a hardware module, or a certificate authority that signs a bounded number of objects. Compared with LMS it has stronger proofs (no random oracle for the tree hashes) and slower operations; both are approved in SP 800-208 and listed in CNSA 2.0 for firmware. Use SLH-DSA if the state cannot be managed.

## Pitfalls

- **State reuse.** As for every Merkle scheme: backups, clones and crashes between signing and storing the index reuse WOTS+ keys and allow forgeries.
- **Address errors.** A missed reset of the address words, or the wrong height or index in a tree hash, gives different keys and masks than other implementations, and signatures do not interoperate. With no test vectors in the RFC, compare with the reference implementation.
- **The checksum shift.** The WOTS+ checksum is shifted left by $8 - ((len_2 \lg w) \bmod 8)$ bits before it is split into digits; leaving it out reads the wrong digits.
- **Confusing $SEED$ and $SK\_SEED$.** $SEED$ is public and randomizes the hash calls; $SK\_SEED$ makes the WOTS+ secret values and must stay secret.
- **Wrong use of $w$.** XMSS's $w = 16$ is the chain length, like LMS type W4.

## Implementations

The Python code is for study only. It is not constant time, and it must not protect real data. It follows the algorithms of RFC 8391 for the SHA-256 set with $n = 32$ and $w = 16$, but the tests use tree heights 4 and 5, which are not standard parameter sets. The WOTS+ secret values come from $SK\_SEED$ with PRF and the address, a choice that the RFC leaves to the implementation. RFC 8391 has no test vectors in its text, and no other vectors were used, so the code is checked only by round trips, by the signature size of 2340 bytes for $h = 5$ (the formula of the RFC), by a hand computation of a small L-tree, and by the rejection of changed signatures; byte compatibility with other implementations is not tested.

## History

Johannes Buchmann, Erik Dahmen and Andreas Hülsing presented XMSS at PQCrypto 2011 as a forward-secure Merkle scheme whose security needs only a second preimage resistant hash and a pseudorandom function. Hülsing introduced WOTS+ in 2013, and with Lea Rausch and Buchmann the multi-tree XMSS$^{MT}$. Hülsing, Rijneveld and Song (2016) added the address scheme against multi-target attacks. The IRTF Crypto Forum Research Group published XMSS as RFC 8391 in May 2018, the first RFC for a post-quantum signature, and NIST approved it in SP 800-208 in October 2020.

## References
