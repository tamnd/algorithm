---
tag: RTX97D
kind: algorithm
slug: merkle-signature-scheme
name: Merkle signature scheme
aliases:
- Merkle hash-tree signatures
- Merkle tree signature
area: cryptography/signatures
level: intro
summary: "Puts 2^h one-time public keys under the root of one Merkle tree. A signature is a one-time signature, the leaf index and the authentication path. The signer must keep state."
model: word-ram
complexity:
  vars: {h: the tree height, k: the hash calls for one one-time key}
  time: {worst: Θ(2^h·k), average: Θ(2^h·k), best: Θ(2^h·k)}
  space: {extra: Θ(2^h)}
properties: {deterministic: true}
history:
  year: 1979
  people: [Ralph Merkle]
  note: Merkle's 1979 Stanford thesis has tree authentication of one-time keys. The paper A certified digital signature appeared at CRYPTO 1989.
prereqs: [winternitz-one-time-signature, merkle-tree]
see_also: [lamport-signature, leighton-micali-signature, xmss, sphincs-plus, forward-secure-signature, hash-based-signatures, collision-resistance, tree-hashing]
sources:
  - paper: "Ralph C. Merkle, Secrecy, authentication, and public key systems, PhD thesis, Stanford University, 1979"
    locator: the chapter on tree authentication, which authenticates many one-time public keys with one tree root
  - paper: "Ralph C. Merkle, A certified digital signature, CRYPTO 1989, LNCS 435, Springer, 1990, pages 218 to 238"
    locator: the tree of one-time signatures and the authentication path
  - paper: "Michael Szydlo, Merkle tree traversal in log space and time, EUROCRYPT 2004, LNCS 3027, pages 541 to 554"
    locator: the traversal algorithm with about 2h hash computations per path and about 3h stored nodes
  - paper: "Johannes Buchmann, Erik Dahmen and Michael Schneider, Merkle tree traversal revisited, PQCrypto 2008, LNCS 5299, pages 63 to 78"
    locator: the BDS traversal algorithm and its trade-off between stored nodes and leaf computations
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: chapter Hash-based Digital Signature Schemes, sections on the Merkle signature scheme, tree traversal, and the security of MSS
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 13, the section on signatures from hash functions (from one-time to stateful many-time signatures with a tree)
---

The Merkle signature scheme (MSS) turns a one-time signature into a scheme that signs $2^h$ messages under one short public key. The signer makes $2^h$ one-time key pairs, hashes each one-time public key to a leaf of a binary [Merkle tree](/merkle-tree/), and publishes the root. To sign, the signer uses the next unused one-time key, and attaches the leaf index and the authentication path, the $h$ sibling nodes from the leaf to the root. The verifier rebuilds the leaf from the one-time signature and climbs to the root. The signer must remember which keys it has used, so the scheme is *stateful*. MSS is the base of [LMS](/leighton-micali-signature/), [XMSS](/xmss/) and the hypertree of [SPHINCS+](/sphincs-plus/).

**Notation.** $h$ is the tree height, $q \in [0, 2^h)$ is the leaf index, $L_q$ is the hash of one-time public key $q$, and $P(a, b)$ is the hash of two child nodes. Node $j$ of level $i$ is $N_{i,j}$, the leaves are level 0, and the root is $N_{h,0}$. The one-time scheme here is the [Winternitz one-time signature](/winternitz-one-time-signature/) (WOTS), but any one-time scheme whose public key can be recomputed from a signature works, such as the [Lamport signature](/lamport-signature/). The security notion is existential unforgeability under chosen message attack (EUF-CMA) for up to $2^h$ signatures, in the standard model.

## In plain words

A one-time key signs only one message. To sign a thousand messages, you could make a thousand one-time keys and publish all of them, but that public key would be huge.

Merkle's idea is to publish one hash instead. Put the hashes of the thousand one-time public keys in a row, hash them in pairs, hash the results in pairs, and continue until one hash is left: the root. The root is the public key.

To sign message number 5, sign it with one-time key number 5, and add the few hashes that are needed to go from leaf 5 up to the root. The verifier gets leaf 5 back from the one-time signature, hashes upward with the given hashes, and checks that it reaches the root. Each one-time key must be used only once, so the signer counts.

## The problem

Given a one-time [signature scheme](/signature-scheme/) and a hash function, build a scheme that signs many messages, with a public key of one hash value and signatures of size about the one-time signature plus $h$ hash values. Security must follow from the one-time security of the leaves and the [collision resistance](/collision-resistance/) of the tree hash. The scheme may sign at most $2^h$ messages, and needs the signer to keep a counter.

## The algorithm

```pseudo id=main
KEYGEN(h)
L1  seed ← random                          ▷ one-time key q is made from (seed, q)
L2  for q ← 0 to 2^h − 1: N[0][q] ← hash of one-time public key q
L3  for i ← 1 to h, for each j: N[i][j] ← P(N[i−1][2j], N[i−1][2j+1])
L4  return sk = (seed, next = 0), pk = N[h][0]

SIGN(sk, M)
L5  q ← sk.next; if q = 2^h then fail
L6  sk.next ← q + 1                         ▷ store the new state first
L7  s ← one-time signature of M with key q
L8  a[i] ← N[i][⌊q / 2^i⌋ xor 1] for i ← 0 to h − 1
L9  return σ = (q, s, a)

VERIFY(root, M, (q, s, a))
L10 v ← hash of the one-time public key computed from (M, s)
L11 for i ← 0 to h − 1: if bit i of q is 0 then v ← P(v, a[i]) else v ← P(a[i], v)
L12 return v = root
```

Key generation (lines L1 to L4) makes the leaves from one seed with a pseudorandom function, so the secret key is the seed and a counter. Line L6 advances the counter before the signature leaves the signer, so a crash cannot make the signer reuse a leaf. Line L8 reads the authentication path from the stored tree. The verifier needs no one-time public key: line L10 recomputes it from the signature, which works for Lamport and Winternitz signatures. Bit $i$ of $q$ tells whether the current node is a left or a right child in line L11.

## Example

Take $h = 2$, so there are 4 leaves $L_0, \ldots, L_3$, two inner nodes $N_{1,0} = P(L_0, L_1)$ and $N_{1,1} = P(L_2, L_3)$, and the root $P(N_{1,0}, N_{1,1})$. The signer has signed two messages and its counter is 2. It signs $M$ with one-time key 2. The leaf index is $q = 2$, binary `10`. The authentication path is $a_0 = L_3$, the sibling of leaf 2, and $a_1 = N_{1,0}$, the sibling of $N_{1,1}$. The signature is $(2, s, (L_3, N_{1,0}))$, and the counter becomes 3.

The verifier computes $v_0 = L_2$ from $s$ and $M$. Bit 0 of $q$ is 0, so $v_1 = P(L_2, L_3) = N_{1,1}$. Bit 1 is 1, so $v_2 = P(N_{1,0}, N_{1,1})$, which is the root. The test file checks the same climb for leaf 6 of a tree of height 4.

## Correctness

**Correctness.** By induction on the level $i$, the value $v_i$ of line L11 is the node $N_{i, \lfloor q / 2^i \rfloor}$ on the path of leaf $q$: the last bit of $\lfloor q/2^i \rfloor$ is bit $i$ of $q$, and it says on which side the sibling $a_i$ goes. So an honest signature climbs to the root.

**Security.** If the one-time scheme is EUF-1-CMA secure and the hashes are collision resistant, MSS is EUF-CMA secure for $2^h$ signatures, with a loss of a factor $2^h$:

$$\varepsilon \le 2^h \cdot \varepsilon_{\mathrm{OTS}} + \varepsilon_{\mathrm{CR}}.$$

A valid forgery either climbs from a leaf value that differs from the real leaf $q^*$, and then the forged path and the real path meet at some level with different inputs, which is a collision; or it uses one-time key $q^*$ on a new message, which is a one-time forgery. The reduction puts its one-time challenge key at a random leaf, and the forgery lands on it with chance $2^{-h}$. The full proof is below.

## Complexity

Let $k$ be the hash calls for one one-time key pair ($k = \ell(w-1) = 1005$ chain steps for WOTS with $w = 16$ and 32-byte values).

- **Key generation** computes all $2^h$ leaves and $2^h - 1$ inner nodes: $\Theta(2^h k)$ hash calls. This is the main cost, and it limits $h$ to about 20 for one tree.
- **Signing** costs one one-time signature, about $k/2$ calls, plus the work to get the authentication path. Storing the whole tree needs $2^{h+1} - 1$ nodes and no extra hashing. Recomputing the path from scratch costs $\Theta(2^h k)$. Traversal algorithms sit in between: Szydlo (2004) computes each next path with about $2h$ leaf and node computations and about $3h$ stored nodes, and the BDS algorithm (Buchmann, Dahmen and Schneider 2008) trades stored nodes for fewer leaf computations per signature.
- **Verification** is one one-time public key recomputation, about $k/2$ calls, plus $h$ calls of $P$.

The signature is $\lceil h/8 \rceil$ bytes of index, one one-time signature, and $h$ hash values. With WOTS ($w = 16$, 32-byte values) and $h = 20$, it is $4 + 2144 + 640 = 2788$ bytes, for about one million signatures. The public key is one hash value.

## Properties

- **Stateful.** The signer must keep a counter and never reuse a leaf. The state must be written to stable storage before the signature is released, and must never be restored from an old backup or copied to a second machine.
- **Bounded.** One key signs at most $2^h$ messages.
- **Minimal assumptions.** Security needs a one-time scheme and a collision resistant hash, so it follows from hash function properties only, and it holds against quantum attackers that use the known algorithms.
- **Forward security for free.** If the signer deletes each one-time secret key after use, and derives keys with a forward-secure generator, a key leaked later cannot sign for earlier leaves; see [forward-secure signatures](/forward-secure-signature/).
- **Short public key, long signature.** The public key is one hash value, the signature is a few kilobytes.

## Variants and improvements

- **Hypertree (tree of trees).** Merkle (1989) already let one-time keys sign the roots of further trees. With $d$ layers of trees of height $h/d$, key generation needs only the top tree, $\Theta(2^{h/d} k)$ calls, and lower trees are made when needed; each signature carries $d$ one-time signatures. CMSS (2006) and GMSS (2007) followed this line, and it is the base of HSS in LMS, of XMSS$^{MT}$, and of the hypertree of SPHINCS+.
- **LMS (RFC 8554).** The standard form with LM-OTS leaves, a key identifier $I$ and the node number in each hash.
- **XMSS (RFC 8391).** WOTS+ leaves, an L-tree to compress the WOTS+ public key, and a bitmask for each tree hash, so second preimage resistance suffices.
- **Stateless schemes.** SPHINCS+ (SLH-DSA, FIPS 205) picks the leaf from a hash of the message in a huge hypertree, with a few-time signature at the bottom, so the signer needs no state.
- **Randomized message hash.** Hashing the message with a fresh random value before the one-time signature removes the need for collision resistance of the message hash.

## When to use it

Use MSS to learn hash-based signatures or to see how one-time keys become many-time keys. For real systems, use its standard forms: LMS/HSS or XMSS/XMSS$^{MT}$ (NIST SP 800-208), for example for firmware signing where one signer signs a limited number of images and can manage the state in hardware, or SLH-DSA when state management is not possible.

## Pitfalls

- **Reusing a leaf.** Restoring a backup, running two copies of the signer, or a crash between signing and saving the counter all reuse a one-time key, and then forgeries become possible. The test file shows that a restored backup signs with leaf 0 a second time.
- **Wrong order of the children.** Line L11 must put the current node on the left when bit $i$ of $q$ is 0, and on the right otherwise. Swapping them, or ignoring $q$, makes some valid signatures fail or lets an attacker choose the side.
- **No range check of $q$.** The verifier must reject $q \ge 2^h$ and paths of the wrong length.
- **No domain separation.** Leaves, inner nodes and one-time keys should use different hash inputs (tags, addresses), or a value of one kind can be presented as another.
- **Running out.** After $2^h$ signatures the key is dead. Plan $h$, or use a hypertree, so that the key lasts its lifetime.

## Implementations

The Python code is for study only. It is not constant time, and it must not protect real data. It uses classic Winternitz leaves ($w = 16$) with secret values derived from one seed, SHA-256 from `hashlib` with a one-byte domain tag, and a stored tree instead of a traversal algorithm, which is fine for the tested heights 4 and 6. The textbook MSS has no official test vectors, so the tests sign with every leaf of a tree of height 4, check the authentication path by hand, reject changed signatures and indices, and show the leaf reuse after a restored backup. The standard forms are tested against vectors on the LMS page and by round trips on the XMSS page.

## History

Ralph Merkle invented tree authentication in his 1979 Stanford thesis, to authenticate many Lamport and Winternitz one-time keys with one value, and published the scheme as "A certified digital signature" at CRYPTO 1989, with a tree of trees to sign an unbounded number of messages. The scheme received new attention as a post-quantum signature after 2000. Szydlo (2004) and Buchmann, Dahmen and Schneider (2008) made the computation of authentication paths fast with little memory, CMSS and GMSS added layers of trees, and XMSS (2011) gave a version that needs only second preimage resistance. The IETF standardized LMS in RFC 8554 (2019) and XMSS in RFC 8391 (2018), and NIST approved both in SP 800-208 (2020).

## References
