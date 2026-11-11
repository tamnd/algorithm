---
tag: MNZ6ET
kind: algorithm
slug: leighton-micali-signature
name: Leighton-Micali signatures
aliases:
- HSS
- Leighton-Micali hash-based signature
- Leighton-Micali signature
- LM-OTS
- Hierarchical Signature System
area: cryptography/signatures
level: advanced
summary: "Stateful hash-based signature of RFC 8554 and NIST SP 800-208. LM-OTS one-time keys sit under a Merkle tree (LMS), and HSS stacks trees. Each hash input carries I, q and a domain tag."
model: word-ram
complexity:
  vars: {h: the tree height, p: the number of chains, w: the bits per digit}
  time: {worst: Θ(2^h·p·2^w), average: Θ(2^h·p·2^w), best: Θ(2^h·p·2^w)}
  space: {extra: Θ(2^h)}
properties: {deterministic: false, randomized: true}
history:
  year: 1995
  people: [Tom Leighton, Silvio Micali, David McGrew, Michael Curcio, Scott Fluhrer]
  note: Leighton and Micali, US patent 5,432,852 (July 1995). McGrew, Curcio and Fluhrer specified LMS and HSS in RFC 8554 (April 2019).
prereqs: [merkle-signature-scheme, winternitz-one-time-signature]
see_also: [xmss, sphincs-plus, lamport-signature, hash-based-signatures, sha-2, merkle-tree, forward-secure-signature]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc8554"
    title: "David McGrew, Michael Curcio and Scott Fluhrer, RFC 8554, Leighton-Micali Hash-Based Signatures, April 2019"
    locator: Section 4 (LM-OTS), Section 5 (LMS), Section 6 (HSS), Section 9 (security), Appendix A (key generation from SEED) and Appendix F (test cases)
  - paper: "Tom Leighton and Silvio Micali, Large provably fast and secure digital signature schemes based on secure hash functions, U.S. Patent 5,432,852, July 1995"
    locator: the one-time signature with a key identifier and position in each hash input, which limits multi-target attacks
  - url: "https://doi.org/10.6028/NIST.SP.800-208"
    title: "David A. Cooper, Daniel C. Apon, Quynh H. Dang, Michael S. Davidson, Morris J. Dworkin and Carl A. Miller, NIST SP 800-208, Recommendation for Stateful Hash-Based Signature Schemes, October 2020"
    locator: the approval of LMS and HSS, the added SHA-256/192 and SHAKE256 parameter sets, and the rules on state and hardware modules
  - paper: doi:10.1007/978-3-319-49100-4_12
    title: "Jonathan Katz, Analysis of a proposed hash-based signature standard, SSR 2016, LNCS 10074, pages 261 to 273"
    locator: the security proof of the LMS proposal in the random oracle model
  - url: "https://eprint.iacr.org/2017/553"
    title: "Scott Fluhrer, Further analysis of a proposed hash-based signature standard, Cryptology ePrint Archive 2017/553"
    locator: the effect of repeated identifiers I on security
---

Leighton-Micali signatures (LMS) are the [Merkle signature scheme](/merkle-signature-scheme/) in the exact form of RFC 8554, with a one-time signature, LM-OTS, that is a variant of the [Winternitz one-time signature](/winternitz-one-time-signature/). Every hash input starts with a random 16-byte key identifier $I$, the leaf number $q$ and a position or a domain tag, so that no two hash calls in any key share an input, and an attacker cannot attack many hash values at once. The Hierarchical Signature System (HSS) stacks LMS trees: each tree signs the public key of the tree below it. LMS is stateful: the signer must never use a leaf twice. NIST approved LMS and HSS in SP 800-208 (2020), and they are used for firmware and software signing.

**Notation.** The page follows RFC 8554. $n = m = 32$ bytes is the hash length (SHA-256). LM-OTS has $w \in \{1, 2, 4, 8\}$ bits per digit (so chains of length $2^w$; this $w$ is not the chain length $w$ of XMSS), $p$ chains, and a left shift $ls$ for the checksum. An LMS tree has height $h \in \{5, 10, 15, 20, 25\}$. $u32(x)$ and $u16(x)$ are big-endian encodings, and $D\_PBLC = $ `8080`, $D\_MESG = $ `8181`, $D\_LEAF = $ `8282`, $D\_INTR = $ `8383` are domain tags. Tree nodes are numbered $r = 1$ (root) to $2^{h+1} - 1$, with leaf $q$ at $r = 2^h + q$. The security notion is EUF-CMA for at most $2^h$ signatures per tree.

## In plain words

LMS is a Merkle tree of one-time keys, written down precisely enough that every implementation gives the same bytes.

Each key pair gets a random name $I$. Every hash that the scheme computes includes $I$, the number of the one-time key, and where in the computation the hash is: which chain and which step, or which tree node. So every hash in the whole system hashes a different input. An attacker who wants to break one of millions of hash values cannot try all of them at once.

To sign more messages than one tree holds, HSS uses a tree of trees. The top tree signs the key of a lower tree, and the lower tree signs messages. When it runs out, a new lower tree is made and signed.

## The problem

Specify a stateful hash-based signature so exactly that independent implementations interoperate, with security from the properties of SHA-256 only, a public key of 60 bytes, and a choice between short signatures and fast signing. The scheme must resist attacks that spread over many hash targets (many keys, chains and messages), and must allow keys that sign billions of messages without a long key generation.

## The algorithm

```pseudo id=main
LMOTS_SIGN(I, q, x[0..p−1], M)
L1  C ← random n bytes
L2  Q ← H(I ‖ u32(q) ‖ u16(D_MESG) ‖ C ‖ M)
L3  a ← the p digits of w bits of Q ‖ Cksm(Q)
L4  y[i] ← CHAIN(i, x[i], 0, a[i]) for i ← 0 to p − 1
L5      ▷ CHAIN(i, t, a, b): for j ← a to b − 1: t ← H(I ‖ u32(q) ‖ u16(i) ‖ u8(j) ‖ t)
L6  return u32(otstype) ‖ C ‖ y[0] ‖ … ‖ y[p−1]

LMS_SIGN(sk, M)
L7  q ← sk.q; if q = 2^h then fail; sk.q ← q + 1
L8  ots ← LMOTS_SIGN(I, q, x_q, M)
L9  path[i] ← T[⌊(2^h + q) / 2^i⌋ xor 1] for i ← 0 to h − 1
L10 return u32(q) ‖ ots ‖ u32(lmstype) ‖ path[0] ‖ … ‖ path[h−1]

LMS_VERIFY((lmstype, otstype, I, T1), M, σ)
L11 parse σ; reject on a wrong type, a wrong length, or q ≥ 2^h
L12 Q ← H(I ‖ u32(q) ‖ u16(D_MESG) ‖ C ‖ M); a ← digits of Q ‖ Cksm(Q)
L13 z[i] ← CHAIN(i, y[i], a[i], 2^w − 1) for i ← 0 to p − 1
L14 Kc ← H(I ‖ u32(q) ‖ u16(D_PBLC) ‖ z[0] ‖ … ‖ z[p−1])
L15 r ← 2^h + q; t ← H(I ‖ u32(r) ‖ u16(D_LEAF) ‖ Kc)
L16 for i ← 0 to h − 1: t ← H(I ‖ u32(⌊r/2⌋) ‖ u16(D_INTR) ‖ (path[i] ‖ t if r is odd, else t ‖ path[i])); r ← ⌊r/2⌋
L17 return t = T1

HSS_VERIFY((L, pub0), M, (Nspk, sig[0], pub[1], …, sig[Nspk−1], pub[Nspk], sig[Nspk]))
L18 if Nspk ≠ L − 1 then return false
L19 key ← pub0; for i ← 0 to Nspk − 1: if not LMS_VERIFY(key, pub[i+1], sig[i]) return false; key ← pub[i+1]
L20 return LMS_VERIFY(key, M, sig[Nspk])
```

LM-OTS (lines L1 to L6) differs from textbook Winternitz in three ways. The message hash is randomized by $C$ and bound to $I$ and $q$. Each chain step hashes $I$, $q$, the chain number $i$ and the step number $j$. The checksum Cksm$(Q)$ sums $2^w - 1 - $ digit over the $8n/w$ digits of $Q$ and is shifted left by $ls$ bits, so that its significant bits are the first digits that line L3 reads. The secret values come from a seed: $x_q[i] = H(I \| u32(q) \| u16(i) \| u8(\text{ff}) \| SEED)$ (Appendix A of the RFC). The byte `ff` cannot be a chain step $j \le 254$, so these inputs never meet chain inputs.

An LMS leaf is the hash of the LM-OTS public key hash $K_q$ with the tag $D\_LEAF$, and an inner node $r$ hashes its two children with the tag $D\_INTR$ and its own number $r$. The public key is $u32(lmstype) \| u32(otstype) \| I \| T[1]$, 56 bytes. HSS adds the number of levels $L$ in front (60 bytes). An HSS signature lists, from the top, each LMS signature of the next public key, followed by that public key, and ends with the LMS signature of the message.

## Example

Test Case 1 of RFC 8554 is an HSS key with $L = 2$ levels. Both trees are LMS_SHA256_M32_H5 (type 5, $h = 5$, 32 leaves) with LMOTS_SHA256_N32_W8 (type 4, $w = 8$, $p = 34$, $ls = 0$). The 2644-byte signature of the 162-byte message (a sentence of the US Constitution) is laid out as follows.

| bytes | field | value |
|---|---|---|
| 0 to 3 | $N_{spk}$ | 1 |
| 4 to 7 | $q$ of the top tree | 5 |
| 8 to 11 | LM-OTS type | 4 |
| 12 to 43 | $C$ | `d32b5667…` |
| 44 to 1131 | 34 chain values $y_i$ | |
| 1132 to 1135 | LMS type | 5 |
| 1136 to 1295 | 5 path nodes | |
| 1296 to 1351 | public key of the lower tree | type 5, type 4, $I$ = `d2f14ff6…`, root |
| 1352 to 2643 | LMS signature of the message | $q = 10$, type 4, $C$ = `0703c491…`, … |

Each LMS signature is $4 + (4 + 32 \cdot 35) + 4 + 5 \cdot 32 = 1292$ bytes. To verify, the verifier checks the top signature on the 56 bytes of the lower public key with the top public key, and then the lower signature on the message with the lower public key. In the lower tree, leaf $q = 10$ is node $r = 32 + 10 = 42$. The path climbs through nodes 21, 10, 5, 2 and 1, and node 42 is even, so the first path node, $T[43]$, goes to the right.

The tests verify Test Case 1, and for Test Case 2 (top tree $h = 10$, $w = 4$; lower tree $h = 5$, $w = 8$) they rebuild both trees from the private seeds in the RFC and reproduce the whole 3860-byte signature.

## Correctness

**Correctness.** LM-OTS verification continues each chain from step $a_i$ to step $2^w - 2$, which together with the signer's steps $0$ to $a_i - 1$ is the whole chain, so it recomputes the one-time public key hash $K_q$. The leaf is node $2^h + q$, and halving the node number climbs one level: at each level the sibling is node $r \oplus 1$, on the left if $r$ is odd. After $h$ levels the node number is 1, the root. HSS correctness follows level by level. The proofs are below.

**Security.** RFC 8554 relies on the analysis of Katz (2016), who proved the proposal secure in the random oracle model with a tight bound. The key ingredients are the randomizer $C$, which removes the need for collision resistance of the message hash, and the distinct prefix $I \| u32(q) \| u16(i) \| u8(j)$ of every hash input, which keeps an attacker from attacking many targets with one computation. Fluhrer (2017) showed that a repeated $I$ in a few keys has only a limited effect. As with every Merkle scheme, the proof needs that no leaf signs twice.

## Complexity

Counting SHA-256 calls of one LMS tree with $p$ chains of $2^w - 1$ steps:

- **Key generation** computes all $2^h$ one-time public keys: about $2^h \cdot p (2^w - 1)$ calls, plus $2^{h+1}$ calls for the tree. This dominates, and is the reason for HSS: a two-level key generates only the top tree and the first lower tree.
- **Signing** costs about half a one-time key on average, plus the path (free if the tree is stored, or $\Theta(h)$ node computations with a traversal algorithm).
- **Verification** costs at most $p(2^w - 1)$ chain steps and $h + 2$ further calls.

The LM-OTS signature lengths of RFC 8554 Table 1:

| LM-OTS type | $w$ | $p$ | $ls$ | LM-OTS signature (bytes) |
|---|---|---|---|---|
| LMOTS_SHA256_N32_W1 | 1 | 265 | 7 | 8516 |
| LMOTS_SHA256_N32_W2 | 2 | 133 | 6 | 4292 |
| LMOTS_SHA256_N32_W4 | 4 | 67 | 4 | 2180 |
| LMOTS_SHA256_N32_W8 | 8 | 34 | 0 | 1124 |

An LMS signature adds $8 + 32h$ bytes. Table 3 of RFC 8554 reports, for $w = 8$ on a 3.3 GHz Xeon with threads, a key generation of 6 seconds for $h = 15$, 3 minutes for $h = 20$ and 1.5 hours for $h = 25$, and a two-level 20/10 key with signatures of 3332 bytes.

## Properties

- **Stateful.** The counter $q$ of each tree must never repeat. SP 800-208 asks that keys be generated and used inside hardware cryptographic modules that do not export the private key, so that the state cannot be copied.
- **Randomized signing.** The value $C$ is fresh for each signature. The security does not rest on the collision resistance of SHA-256.
- **Exact formats.** Typecodes fix all parameters, and the byte formats are fully specified, so signatures interoperate.
- **Small public key.** 56 bytes for LMS, 60 for HSS. Signatures are 1 to 9 KB per level.
- **Simple verification.** Only SHA-256 calls and byte parsing, which suits small verifiers such as boot ROMs.

## Variants and improvements

- **HSS with $L$ levels (up to 8).** Each level multiplies the number of signatures by $2^{h_i}$ and adds one LMS signature and one public key to the signature. Lower trees can be made when needed.
- **SP 800-208 parameter sets.** NIST added SHA-256/192 (24-byte values, shorter signatures) and SHAKE256 with 32 or 24 bytes.
- **[XMSS](/xmss/) (RFC 8391).** The other stateful standard. It uses WOTS+ with bitmasks and an L-tree, so its proofs need only second preimage resistance in the standard model, at the price of more hash calls per step.
- **Stateless SLH-DSA ([SPHINCS+](/sphincs-plus/)).** No state at all, with larger signatures and slower signing.

## When to use it

Use LMS or HSS when the signer can manage state reliably and signs a known number of times, as in firmware and boot image signing; NSA's CNSA 2.0 lists LMS and XMSS for this use. Verification is simple, so it suits constrained verifiers. Prefer SLH-DSA when the state cannot be protected, for example when keys are backed up, cloned or used on several machines.

## Pitfalls

- **State reuse.** Restoring a backup, cloning a virtual machine, or signing on two servers with one key reuses leaves. Reserve a range of $q$ values and write the new counter to stable storage before any signature leaves the signer.
- **Mixed meanings of $w$.** In LMS $w$ is the bits per digit; in XMSS and SLH-DSA it is the chain length. LMOTS W4 matches WOTS+ with $w = 16$.
- **No type check.** The verifier must check that the LM-OTS type in the signature matches the public key and that the lengths match the types, before it parses the rest.
- **Wrong node order.** Line L16 puts the path node on the left when $r$ is odd. The node number $r$, not $q$, enters the hash.
- **Checksum without the shift.** Leaving out the left shift $ls$ makes the checksum digits read the wrong bits.

## Implementations

The Python code is for study only. It is not constant time, and it must not protect real data. It covers the SHA-256 parameter sets of RFC 8554, stores the whole tree, and takes SHA-256 from `hashlib`. The tests use the official vectors of RFC 8554 Appendix F. Test Case 1 is verified from the public key and the signature copied from the RFC, with a SHA-256 digest of the copied signature as a guard against copy errors. For Test Case 2, the code rebuilds both trees from the seeds and identifiers of the RFC, checks both public keys, and signs with the leaf numbers and randomizers $C$ of the RFC; the resulting 3860-byte signature has the same SHA-256 digest as the RFC signature, and verifies.

## History

Tom Leighton and Silvio Micali patented their form of hash-based signatures in 1995 (US patent 5,432,852, now expired), with an identifier and a position in each hash call to defeat attacks on many targets. David McGrew and Michael Curcio wrote the first Internet-Draft in 2013, Scott Fluhrer joined, and Katz analyzed the proposal in 2016. The IRTF Crypto Forum Research Group published it as RFC 8554 in April 2019. NIST approved LMS and HSS together with XMSS in SP 800-208 in October 2020, as the first post-quantum signatures that it standardized.

## References
