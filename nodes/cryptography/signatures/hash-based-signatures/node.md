---
tag: W9FJKK
kind: concept
slug: hash-based-signatures
name: Hash-based signatures
aliases:
- Hash-based signature
- hash-based cryptography
- hash-based signature schemes
- HBS
area: cryptography/signatures
level: intro
summary: "Signatures whose security rests only on properties of a hash function. They resist known quantum attacks and come in stateful (LMS, XMSS) and stateless (SLH-DSA) forms."
prereqs: [digital-signature, cryptographic-hash-function]
see_also: [lamport-signature, winternitz-one-time-signature, merkle-signature-scheme, leighton-micali-signature, xmss, sphincs-plus, second-preimage-resistance, post-quantum-cryptography]
sources:
  - paper: "Leslie Lamport, Constructing digital signatures from a one-way function, Technical Report CSL-98, SRI International, October 1979"
    locator: the one-time signature from a one-way function
  - paper: "Ralph C. Merkle, A certified digital signature, CRYPTO 1989, LNCS 435, Springer, 1990, pages 218 to 238"
    locator: the Winternitz improvement and the tree of one-time keys
  - url: "https://doi.org/10.6028/NIST.SP.800-208"
    title: "David A. Cooper, Daniel C. Apon, Quynh H. Dang, Michael S. Davidson, Morris J. Dworkin and Carl A. Miller, NIST SP 800-208, Recommendation for Stateful Hash-Based Signature Schemes, October 2020"
    locator: the approval of LMS, HSS, XMSS and XMSS^MT, the risk of state reuse, and the rule that keys are made and used in hardware modules
  - url: "https://doi.org/10.6028/NIST.FIPS.205"
    title: "NIST FIPS 205, Stateless Hash-Based Digital Signature Standard, August 2024"
    locator: Section 11, Table 2 (the SLH-DSA parameter sets and sizes)
  - url: "https://www.rfc-editor.org/rfc/rfc8554"
    title: "David McGrew, Michael Curcio and Scott Fluhrer, RFC 8554, Leighton-Micali Hash-Based Signatures, April 2019"
    locator: Section 5 (LMS signature format and sizes)
  - url: "https://www.rfc-editor.org/rfc/rfc8391"
    title: "Andreas Hülsing, Denis Butin, Stefan-Lukas Gazdag, Joost Rijneveld and Aziz Mohaisen, RFC 8391, XMSS: eXtended Merkle Signature Scheme, May 2018"
    locator: Section 5 (parameter sets and Table 3) and Section 9 (security from second preimage resistance)
---

Hash-based signatures are digital signatures built from a hash function and nothing else: no factoring, no discrete logarithm and no lattice problem. The base is a one-time signature, such as [Lamport's](/lamport-signature/) or [Winternitz's](/winternitz-one-time-signature/), in which the secret key is random values and the public key is their hashes; signing reveals some secret values or points on hash chains. A [Merkle tree](/merkle-tree/) (a binary tree in which each node is the hash of its two children) joins many one-time keys under one short public key. The only assumption is that the hash function is hard to invert in specific ways, and the known quantum algorithms only reduce the cost of those attacks by a square root or less, so these schemes are post-quantum. NIST approves two stateful schemes, LMS and XMSS, in SP 800-208 (2020), and one stateless scheme, SLH-DSA (SPHINCS+), in FIPS 205 (August 2024).

## In plain words

Pick many random secrets and publish their hashes. To sign, show some of the secrets: which ones depends on the message. Anyone can hash what you showed and compare. Nobody else can show a secret before you do, because that would mean undoing the hash.

The catch is that each set of secrets is safe for one message only, since every signature reveals some secrets. So the signer makes very many sets and links all their public parts with a tree of hashes, whose top is the public key.

Then the signer must never use a set twice. Either it keeps a counter (stateful schemes), or it picks a set at random from an enormous number of sets and uses a scheme that survives rare repeats (stateless schemes).

## The idea

**Security from the hash only.** A forger must find an input to a hash with a given output (a preimage), or a second input with the same output as a given input (a second preimage). Modern schemes are built so that collision resistance is not needed: XMSS and SPHINCS+ mask or tweak every hash call with a public seed and a unique address, and LMS puts a key identifier and a position into each call. Their proofs then use second preimage resistance or target collision resistance, which are much harder to break than collision resistance: a generic collision costs about $2^{n/2}$ hash calls for an $n$-bit hash, but a second preimage costs about $2^n$. The message itself is hashed with a random value, so the signer's choice cannot be attacked with collisions found in advance. The early schemes, Lamport's and Merkle's with a plain message hash, did need a collision resistant hash.

**Post-quantum.** Grover's algorithm finds a preimage of an $n$-bit hash in about $2^{n/2}$ quantum steps, and the best quantum collision search does not beat the classical $2^{n/2}$ in realistic cost models. A 256-bit hash output, or 128 bits for the second preimage style properties of SLH-DSA-128, therefore keeps a large margin. No other assumption can fail.

**Stateful vs stateless.** LMS ([Leighton-Micali](/leighton-micali-signature/), RFC 8554) and [XMSS](/xmss/) (RFC 8391) are Merkle trees of one-time keys with a counter, the leaf index. They have small signatures and fast operations, but the signer must update the counter before each signature is released. [SPHINCS+](/sphincs-plus/) (FIPS 205, SLH-DSA) has no counter: a hash of the message picks one of $2^{63}$ to $2^{68}$ few-time keys under a hypertree, and the few-time scheme FORS stays secure if a key is hit a few times. The price is a signature of 7.8 to 50 kilobytes and slower signing.

**The danger of state.** In a stateful scheme, a one-time key used twice lets an attacker forge signatures for that key, and from there for any message. Reuse is easy to cause: restoring a key from a backup, cloning a virtual machine, running two signers with one key, or a crash after a signature is sent but before the new counter is stored. NIST SP 800-208 therefore approves stateful schemes only with keys generated and used inside hardware modules that do not allow export of the private key, and recommends them for uses such as firmware signing, where the number of signatures is known and the signer is well controlled.

**Size and speed.** The table compares typical sizes in bytes (signatures that one key can make in the last column):

| scheme | public key | signature | signatures per key | state |
|---|---|---|---|---|
| Lamport, SHA-256 | 16,384 | 8,192 | 1 | none (one-time) |
| WOTS+, $n = 32$, $w = 16$ | 2,144 | 2,144 | 1 | none (one-time) |
| LMS, SHA-256, $h = 20$, $w = 8$ (bits per digit) | 56 | 1,772 | $2^{20}$ | counter |
| XMSS-SHA2_20_256 | 68 | 2,820 | $2^{20}$ | counter |
| SLH-DSA-128s | 32 | 7,856 | $2^{64}$ | none |
| SLH-DSA-128f | 32 | 17,088 | $2^{64}$ | none |
| SLH-DSA-256f | 64 | 49,856 | $2^{64}$ | none |

For comparison, ECDSA with P-256 has a 64-byte public key and a 64-byte signature. Within each family, the Winternitz parameter and the tree height trade size for speed: a larger $w$ gives shorter signatures but longer chains, and a taller tree allows more signatures but makes key generation slower. LMS and XMSS verify with a few thousand hash calls; SLH-DSA verifies quickly too, but signing takes about $10^5$ hash calls for the "f" sets and many times more for the "s" sets.

## Examples

- **[Lamport signature](/lamport-signature/) (1979).** Two secret values per digest bit; reveal one of each pair. One message per key.
- **[Winternitz one-time signature](/winternitz-one-time-signature/) (Merkle 1989).** Hash chains sign several bits at once; a checksum stops forgeries by moving along the chains.
- **[Merkle signature scheme](/merkle-signature-scheme/) (1979).** A tree of one-time public keys under one root, with an authentication path in each signature.
- **[LMS and HSS](/leighton-micali-signature/) (RFC 8554, 2019).** Merkle trees of Winternitz keys with position-dependent hashing, and a hierarchy of trees.
- **[XMSS and XMSS^MT](/xmss/) (RFC 8391, 2018).** Merkle trees with WOTS+, bitmasks and L-trees; security from second preimage resistance.
- **[SPHINCS+ (SLH-DSA)](/sphincs-plus/) (FIPS 205, 2024).** Stateless: FORS few-time keys under a hypertree of XMSS trees.
- **[Forward-secure signatures](/forward-secure-signature/).** XMSS with a forward-secure key generation is a forward-secure signature from hash functions only.

## Where it is used

- **Firmware and software signing.** SP 800-208 approves LMS and XMSS for this, and the NSA's CNSA 2.0 suite lists them for software and firmware signing.
- **Long-term roots of trust.** SLH-DSA serves where signatures are rare and must stay valid for decades, such as root certificates and code-signing roots, as a hedge against a break of lattice signatures.
- **Secure boot and hardware.** Boot ROMs and hardware security modules verify LMS signatures, because verification needs only a hash function, which the hardware already has.
- **Post-quantum migration.** Hash-based signatures are the most conservative choice among the NIST post-quantum signatures, because their security does not depend on a new hardness assumption.

## References
