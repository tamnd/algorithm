---
tag: 9FDHGB
kind: data-structure
slug: merkle-tree
name: Merkle tree
aliases:
- hash tree
area: cryptography/hash-functions
level: core
summary: "A binary tree of hashes whose root commits to a list; an inclusion proof has about log2 n hashes. RFC 6962 hashes leaves with 0x00 and nodes with 0x01 to stop second preimages."
model: word-ram
complexity:
  vars: {n: the number of leaves}
  time: {worst: Θ(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [cryptographic-hash-function, binary-tree]
see_also: [hash-chain, tree-hashing, merkle-signature-scheme, second-preimage-resistance, collision-resistance, merkle-damgard-construction, blake3, xmss]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc6962"
    title: Ben Laurie, Adam Langley and Emilia Kasper, RFC 6962, Certificate Transparency, June 2013
    locator: Section 2.1 (Merkle Tree Hash with the 0x00 and 0x01 prefixes), Section 2.1.1 (audit paths), Section 2.1.2 (consistency proofs), Section 2.1.3 (the example tree with 7 leaves)
  - url: "https://www.rfc-editor.org/rfc/rfc9162"
    title: Ben Laurie, Eran Messeri and Rob Stradling, RFC 9162, Certificate Transparency Version 2.0, December 2021
    locator: Section 2.1 (Merkle trees, inclusion proofs and consistency proofs, and the algorithms to verify them)
  - url: "https://github.com/transparency-dev/merkle/blob/main/testonly/constants.go"
    title: transparency-dev/merkle, testonly/constants.go
    locator: LeafInputs, NodeHashes and RootHashes (the RFC 6962 hashes of 8 test leaves)
  - paper: "Ralph C. Merkle, A digital signature based on a conventional encryption function, CRYPTO 1987, LNCS 293, pages 369 to 378"
    locator: the tree authentication of many one-time public keys by one root
  - url: "https://patents.google.com/patent/US4309569A"
    title: Ralph C. Merkle, Method of providing digital signatures, US patent 4309569, filed 1979, granted 1982
    locator: the tree of hash values and the authentication path
  - url: "https://nvd.nist.gov/vuln/detail/CVE-2012-2459"
    title: National Vulnerability Database, CVE-2012-2459
    locator: the Bitcoin Merkle tree that duplicates the last hash of an odd level, so two transaction lists share a root
  - paper: "Scott A. Crosby and Dan S. Wallach, Efficient data structures for tamper-evident logging, USENIX Security Symposium 2009"
    locator: the history tree, which RFC 6962 cites as the model for its tree
---

A Merkle tree, or hash tree, is a binary tree in which each leaf holds the hash of a data block and each inner node holds the hash of its two children. The root hash, 32 bytes for SHA-256, commits to the whole list: anyone who trusts the root can check that a block is at a given position with an *inclusion proof* of about $\log_2 n$ hashes, and can check that an old list is a prefix of a new one with a *consistency proof*. Ralph Merkle introduced it in 1979 to sign many messages with one public key. Today it is the core of Certificate Transparency logs, Git and other content-addressed stores, blockchains, and hash-based signatures such as [XMSS](/xmss/).

**Notation.** $D[n] = (d_0, \ldots, d_{n-1})$ the list of leaves, $D[a:b]$ the sublist $d_a, \ldots, d_{b-1}$, $H$ = SHA-256, $\|$ concatenation, $k$ the largest power of two with $k < n$. $\mathrm{MTH}$ is the Merkle Tree Hash of RFC 6962. Security rests on the [collision resistance](/collision-resistance/) of $H$, in the standard model, and the reduction is tight.

## In plain words

Suppose a server keeps a long public list, such as all the certificates it has seen. You want a short fingerprint of the list, so that the server cannot later change an entry without everyone noticing. A hash of the whole list works, but to check one entry you would need the whole list.

A Merkle tree hashes the entries in pairs, then the pair hashes in pairs, and so on up to one root hash. To prove that an entry is in the list, the server sends only the hashes beside the path from that entry to the root, one per level. You hash your way up and compare with the root. For a million entries this is 20 hashes instead of a million entries.

## The abstract type

A Merkle tree is an authenticated list. Its operations are: ROOT, the commitment to the current list; APPEND$(d)$ in logs; PROVE-INCLUSION$(m)$ and VERIFY-INCLUSION$(m, n, d, \pi, r)$, which checks that $d$ is entry $m$ of the list of size $n$ with root $r$; and PROVE-CONSISTENCY$(m)$ and VERIFY-CONSISTENCY$(m, n, r_m, r_n, \pi)$, which checks that the list with root $r_m$ is the first $m$ entries of the list with root $r_n$. A verifier needs only roots and proofs, never the list.

## Representation

RFC 6962 defines the tree for any $n$ by a recursive split.

**Invariant (shape).** The tree of $n \ge 2$ leaves has the tree of $D[0:k]$ as its left child and the tree of $D[k:n]$ as its right child, where $k$ is the largest power of two below $n$. So the left subtree is always complete, and the shape depends only on $n$.

**Invariant (hashes).** A leaf stores $H(\texttt{00} \| d)$, an inner node stores $H(\texttt{01} \| \text{left} \| \text{right})$, and the empty list has the root $H(\text{empty string})$.

The prefix bytes `00` and `01` are the domain separation: a leaf hash and a node hash are hashes of strings that start with different bytes, so a leaf can never be read as a node.

## Operations

```pseudo id=main
MTH(D[n])                                ▷ RFC 6962, Section 2.1
L1  if n = 0 then return H("")
L2  if n = 1 then return H(00 ‖ d_0)
L3  return H(01 ‖ MTH(D[0:k]) ‖ MTH(D[k:n]))

PATH(m, D[n])                            ▷ inclusion proof, Section 2.1.1
L4  if m < k then return PATH(m, D[0:k]) : MTH(D[k:n]) else return PATH(m − k, D[k:n]) : MTH(D[0:k])

ROOT-FROM-PATH(m, n, h, π)               ▷ π = (π_1, …, π_t), with π_t the top sibling
L5  if n = 1 then return h
    if m < k then return H(01 ‖ ROOT-FROM-PATH(m, k, h, π_1..t−1) ‖ π_t)
    else return H(01 ‖ π_t ‖ ROOT-FROM-PATH(m − k, n − k, h, π_1..t−1))
L6  VERIFY-INCLUSION(m, n, d, π, r): return ROOT-FROM-PATH(m, n, H(00 ‖ d), π) = r

SUBPROOF(m, D[n], b)                     ▷ consistency proof, Section 2.1.2; PROOF(m, D[n]) = SUBPROOF(m, D[n], true)
    if m = n then return () if b else (MTH(D[n]))
L7  if m ≤ k then return SUBPROOF(m, D[0:k], b) : MTH(D[k:n])
    else return SUBPROOF(m − k, D[k:n], false) : MTH(D[0:k])

VERIFY-CONSISTENCY(m, n, r_m, r_n, π)
L8  walk the recursion of SUBPROOF from the top sibling down, and compute two hashes:
    the root of D[0:m] and the root of D[n], each from the proof (and from r_m when b is true)
L9  return both computed roots equal r_m and r_n
```

Here `:` appends one hash to a list. Paths are built from the bottom up, so the last hash in a proof is the sibling nearest the root.

**Inclusion.** Line L4 adds the root of the other half at each level, so a path has one hash per level of the tree. Lines L5 and L6 rebuild the root from the leaf hash and the path, choosing left or right by comparing $m$ with $k$ at each level.

**Consistency.** The old tree $D[0:m]$ is made of complete subtrees that also appear in the new tree, plus at most one partial subtree at each level. The proof gives the hashes needed to rebuild both roots. When the recursion reaches a subtree that is exactly $D[0:m]$ and the old root is known ($b$ true), the proof omits it and the verifier uses $r_m$.

**Append.** A log keeps the roots of the complete subtrees on the right edge, at most $\log_2 n + 1$ of them, and merges them like a binary counter when a leaf is added. The code recomputes from the list, which is simpler and $\Theta(n)$ per root.

## Example

The tree of RFC 6962, Section 2.1.3, with the 7 test leaves of transparency-dev: $d_0, \ldots, d_6$ = (empty), `00`, `10`, `2021`, `3031`, `40414243`, `5051525354555657`. Leaf hashes are $a, \ldots, f$ and $j$ for $d_6$; then $g = H(01 \| a \| b)$, $h = H(01 \| c \| d)$, $i = H(01 \| e \| f)$, $k = H(01 \| g \| h)$, $l = H(01 \| i \| j)$, and the root is $H(01 \| k \| l)$.

The audit path of $d_3$ is $[c, g, l]$, as in the RFC. The verifier rebuilds the root:

| step | input | value (first 8 bytes) |
|---|---|---|
| leaf hash of $d_3$ = `2021` | $H(00 \| d_3)$ | `07506a85fd9dd2f1` = $d$ |
| level 1, $d$ is a right child | $H(01 \| c \| d)$, $c$ = `0298d122906dcfc1` | `5f083f0a1a33ca07` = $h$ |
| level 2, $h$ is a right child | $H(01 \| g \| h)$, $g$ = `fac54203e7cc696c` | `d37ee418976dd957` = $k$ |
| level 3, $k$ is a left child | $H(01 \| k \| l)$, $l$ = `837dbb152e9b0790` | `ddb89be403809e32` = root |

The values for $d$, $c$, $h$, $g$, $k$ and the root are the published `NodeHashes` and `RootHashes` of transparency-dev for 7 leaves. The value of $l$, the root of an incomplete subtree, is not published; it is $H(01 \| i \| j)$ computed from the published $i$ and $j$. The consistency proof from the tree of 3 leaves to the tree of 7 is $[c, d, g, l]$, from 4 leaves it is $[l]$, and from 6 leaves it is $[i, j, k]$, as in the RFC.

**Without domain separation.** Let the leaves and nodes both be hashed with $H(x)$ and no prefix. For the leaves `tx0` to `tx3`, the two "leaves" $H(\texttt{tx0}) \| H(\texttt{tx1})$ and $H(\texttt{tx2}) \| H(\texttt{tx3})$, each 64 bytes, give the same root as the four real leaves. That is a second preimage: a different list with the same root. With the RFC 6962 prefixes, the two roots differ. The tests check both.

## Correctness

**Theorem (binding).** If $H$ is collision resistant, then no efficient adversary can produce two different lists with the same MTH, a valid inclusion proof for a value that is not at that position, or a valid consistency proof for a list that is not a prefix.

*Sketch.* Take two different lists $D \ne D'$ with $\mathrm{MTH}(D) = \mathrm{MTH}(D')$. Compare the two hash computations from the root down. At the root, the inputs to $H$ are equal or they form a collision. If they are equal, the prefix byte says whether both are leaves or both are nodes. If both are nodes, the children's hashes are equal and we go down into a child where the lists differ. If both are leaves, the data is equal. The lists differ somewhere, so somewhere the inputs differ while the outputs agree: a collision of $H$. Without the prefix bytes, a 64-byte leaf can match a node input, and this argument breaks, as the example shows. The same walk works for inclusion and consistency proofs. The proofs file has the details.

The reduction is tight: one forgery gives one collision, with one run of the adversary.

## Complexity

Let $n$ be the number of leaves. Computing the root takes $2n - 1$ hash calls for $n \ge 1$. An inclusion proof has $\lceil \log_2 n \rceil$ hashes at most, and verifying it takes as many hash calls. A consistency proof has at most $\lceil \log_2 n \rceil + 1$ hashes. Storing the full tree takes $2n - 1$ hashes; a log that only appends and proves from stored nodes needs $\Theta(n)$ space and $\Theta(\log n)$ time per proof. The code in this page recomputes subtree hashes from the list, so each proof costs $\Theta(n)$ hash calls there.

## Variants

- **Bitcoin's tree** duplicates the last hash of a level with an odd count. Then the lists $(a, b, c)$ and $(a, b, c, c)$ have the same root, which led to CVE-2012-2459. It also has no leaf and node prefixes, so a transaction of exactly 64 bytes can look like an inner node, another known weakness of that tree.
- **Sparse Merkle trees** have $2^{256}$ leaves indexed by a key, mostly empty, and give proofs of non-membership.
- **Merkle Patricia tries** (Ethereum) combine a trie with node hashes.
- **Hash-based signatures.** Merkle's scheme, [XMSS](/xmss/) and SPHINCS+ put one-time public keys at the leaves; see [Merkle signature scheme](/merkle-signature-scheme/).
- **Tree modes of hash functions.** [Tree hashing](/tree-hashing/) uses a tree inside one hash function for parallel speed, as in [BLAKE3](/blake3/). The goal there is a fast hash, not proofs about a list.
- **Hash chains** are the degenerate tree with one child per node; see [hash chain](/hash-chain/).

## When to use it

Use a Merkle tree when many parties need to check single entries of a large list, or to check that a log only grows: certificate and key transparency, software supply chain logs, content-addressed storage, file sync and replication (comparing trees finds the changed blocks in $O(\log n)$ hashes per change), and blockchain light clients. For a single file checked as a whole, a plain hash is enough.

## Pitfalls

- **No domain separation.** Without different prefixes for leaves and nodes, an inner node can be presented as a leaf, as in the example.
- **Ambiguous shapes.** Padding by duplication (Bitcoin) or with zero hashes lets two lists share a root unless the size is also bound. RFC 6962 fixes the shape by $n$, and a verifier must know $n$.
- **Unchecked proof lengths.** A verifier must reject proofs that are too long or too short for $(m, n)$; the code does.
- **Index not bound.** A path without its index $m$ proves that the value is somewhere, not where.
- **Short hashes.** Collision resistance of $H$ is the whole security; a 128-bit output gives only about $2^{64}$ security against collisions.

## Implementations

The Python code gives `leaf_hash`, `node_hash`, `mth` (lines L1 to L3), `audit_path` (line L4), `root_from_path` and `verify_inclusion` (lines L5 and L6), `consistency_proof` (line L7) and `verify_consistency` (lines L8 and L9). It also gives two insecure trees for the tests: `naive_root`, with no prefixes, and `bitcoin_style_root`. The tests check the leaf and node hashes and the 9 roots of the transparency-dev constants, the audit paths and consistency proofs of the RFC 6962 example, the verification of every inclusion and consistency proof for up to 8 leaves, the rejection of a changed leaf, a wrong index, a short path and changed proof hashes, the second preimage of the naive tree, and CVE-2012-2459.

## History

Ralph Merkle described hash trees in his 1979 Stanford thesis and in a patent filed that year, to authenticate many one-time signature keys with one root; the work was published at CRYPTO 1987. Hash trees were then used for timestamping (Haber and Stornetta), for file systems and peer-to-peer downloads, and in Bitcoin (2008) to commit to the transactions of a block. Crosby and Wallach (2009) defined history trees for tamper-evident logs, and RFC 6962 (2013) adapted them for Certificate Transparency, with the 0x00 and 0x01 prefixes and consistency proofs. RFC 9162 (2021) is the second version of that protocol.

## References
