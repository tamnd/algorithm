---
tag: WPA8X5
kind: definition
slug: extendable-output-function
name: Extendable-output function
aliases:
- XOF
area: cryptography/hash-functions
level: advanced
summary: A hash-like function whose output can be extended to any length, where a shorter output is always a prefix of a longer one. SHAKE, cSHAKE, KangarooTwelve and BLAKE3 are XOFs.
prereqs: [cryptographic-hash-function, sponge-construction]
see_also: [shake, sha-3, keccak, blake3, kmac, hkdf, tree-hashing, random-oracle-model]
sources:
  - paper: doi:10.6028/NIST.FIPS.202
    title: NIST, FIPS 202, SHA-3 Standard, Permutation-Based Hash and Extendable-Output Functions, August 2015
    locator: Section 1 and the glossary (the definition of an XOF), Section 6.2 (SHAKE128 and SHAKE256), Appendix A.1 (Table 4) and Appendix A.2 (related outputs)
  - paper: doi:10.6028/NIST.SP.800-185
    title: NIST, SP 800-185, SHA-3 Derived Functions, cSHAKE, KMAC, TupleHash and ParallelHash, December 2016
    locator: Section 2.3 (left_encode, encode_string, bytepad), Section 3 (cSHAKE), Section 4 (KMAC and KMACXOF), and the cSHAKE sample values
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters, Gilles Van Assche, Ronny Van Keer and Benoît Viguier, KangarooTwelve, fast hashing based on Keccak-p, Applied Cryptography and Network Security, ACNS 2018, LNCS 10892, Springer, 2018"
    locator: the definition of KangarooTwelve with Keccak-p[1600, 12], the tree mode and the single-node case for short inputs
  - paper: "Jack O'Connor, Jean-Philippe Aumasson, Samuel Neves and Zooko Wilcox-O'Hearn, BLAKE3, one function, fast everywhere, specification, 2020"
    locator: the root node output with the counter t = 0, 1, 2 and so on, and the extendable output
  - paper: "Guido Bertoni, Joan Daemen, Michaël Peeters and Gilles Van Assche, On the indifferentiability of the sponge construction, Advances in Cryptology, EUROCRYPT 2008, LNCS 4965, Springer, 2008"
    locator: the sponge is indifferentiable from a random oracle with an infinite output
  - paper: doi:10.17487/RFC8017
    title: Kathleen Moriarty, Burt Kaliski, Jakob Jonsson and Andreas Rusch, PKCS #1, RSA Cryptography Specifications Version 2.2, RFC 8017, 2016
    locator: Appendix B.2.1, the mask generation function MGF1
---

An extendable-output function, or XOF, is a function on messages whose output can be made as long as the caller wants. The caller asks for $d$ bits and gets the first $d$ bits of one long output string that is fixed by the message alone. So a shorter output is always a prefix of a longer one: this is the prefix property. FIPS 202 (2015) standardized the first two XOFs, SHAKE128 and SHAKE256, which come from the [sponge construction](/sponge-construction/), and SP 800-185 added cSHAKE with a customization string. KangarooTwelve and [BLAKE3](/blake3/) are fast XOFs outside the NIST standards. An XOF replaces the old tricks of hashing with a counter or truncating a hash when a protocol needs a non-standard length, a mask or a stream of key material.

**Notation.** $X(M, d)$ is the first $d$ bits of the output of the XOF $X$ on the message $M$. $\mathrm{Trunc}_d(Z)$ is the first $d$ bits of $Z$. $s$ is the security strength of $X$ in bits. $c$ is the capacity of a sponge. All digests below were computed with `hashlib` or with short scripts, and the cSHAKE, KangarooTwelve and BLAKE3 values agree with the published sample values.

## Definition

### Extendable output

**Definition (FIPS 202).** An extendable-output function is a function on bit strings in which the output can be extended to any desired length.

Formally, $X$ takes a message $M \in \{0,1\}^*$ and a length $d \ge 0$ and returns a string of exactly $d$ bits, with the **prefix property**: for all $M$ and all $d \le d'$,

$$X(M, d) = \mathrm{Trunc}_d(X(M, d')).$$

Equivalently, $X$ defines one infinite string $X(M)$ for each message, and $X(M, d)$ is its first $d$ bits. The length is not an input to the computation of the bits; it only says where to stop (FIPS 202 Appendix A.2).

### Security

The ideal object is a random oracle with an infinite output: a function that maps each message to an independent uniform infinite string. A real XOF is built to behave like it up to a security strength $s$. For a $d$-bit output, FIPS 202 Table 4 gives SHAKE128 ($s = 128$) and SHAKE256 ($s = 256$) these strengths:

| Function | Collision | Preimage | Second preimage |
|---|---|---|---|
| SHAKE128 | $\min(d/2, 128)$ | $\ge \min(d, 128)$ | $\min(d, 128)$ |
| SHAKE256 | $\min(d/2, 256)$ | $\ge \min(d, 256)$ | $\min(d, 256)$ |

In both cases $s = c/2$, from the generic sponge bound. So the collision strength is $\min(d/2, c/2)$: a long output does not buy more than $c/2$ bits, and a short one is limited as any $d$-bit function is. FIPS 202 notes that for $d = 224$ both give 112 bits against collisions, but SHAKE128 gives 128 bits against preimages and SHAKE256 gives 224. For a sponge, the indifferentiability theorem of BDPV (2008) covers outputs of any length, which makes the infinite random oracle the right reference.

### Related outputs

The prefix property is the one way in which an XOF differs from a family of hash functions with different lengths. For any $d$, $e$ and $M$, $\mathrm{Trunc}_d(\mathrm{SHAKE128}(M, d + e)) = \mathrm{SHAKE128}(M, d)$ (FIPS 202 Appendix A.2). Distinct fixed-length hashes do not behave this way: SHA3-256$(M)$ is not an extension of SHA3-224$(M)$, and SHA-512/256 is not a prefix of SHA-512, because their inputs to the permutation or their initial values differ. A protocol that takes two values from the same message with two lengths therefore gets related values, unless the length or a label is part of the input.

## Examples and non-examples

### Examples

- **SHAKE128 and SHAKE256** (FIPS 202). Keccak with $c = 256$ and $c = 512$ and the suffix bits 1111. For "abc", $\mathrm{SHAKE128}(\text{abc}, 128) = \texttt{5881092dd818bf5cf8a3ddb793fbcba7}$ and $\mathrm{SHAKE128}(\text{abc}, 256) = \texttt{5881092dd818bf5cf8a3ddb793fbcba7}\,\texttt{4097d5c526a6d35f97b83351940f2cc8}$, which starts with the shorter output. For the empty string, the first 256 bits are $\texttt{7f9c2ba4e88f827d616045507605853ed73b8093f6efbc88eb1a6eacfa66ef26}$ for SHAKE128 and $\texttt{46b9dd2b0ba88d13233b3feb743eeb243fcd52ea62b81b82b50c27646ed5762f}$ for SHAKE256. See [SHAKE](/shake/).
- **cSHAKE** (SP 800-185). $\mathrm{cSHAKE128}(X, L, N, S)$ adds a function name $N$ and a customization string $S$: if both are empty it is $\mathrm{SHAKE128}(X, L)$, and otherwise it is $\mathrm{KECCAK}[256](\mathrm{bytepad}(\mathrm{encode\_string}(N) \| \mathrm{encode\_string}(S), 168) \| X \| 00, L)$. The suffix 00, in place of 1111, keeps cSHAKE apart from SHAKE, and different $S$ give independent XOFs. The first sample of SP 800-185, with $X = \texttt{00010203}$, $N$ empty, $S$ = "Email Signature" and $L = 256$, gives $\texttt{c1c36925b6409a04f1b504fcbca9d82b4017277cb5ed2b2065fc1d3814d5aaf5}$. KMAC, TupleHash and ParallelHash are built on cSHAKE.
- **KangarooTwelve** (BDPVVV 2018). A sponge over Keccak-p[1600] with 12 rounds instead of 24, rate 1344 and capacity 256, for 128-bit security. Long inputs are cut into 8192-byte chunks hashed in a tree, so the work can run in parallel. A short input $M$ with customization $C$ is a single sponge call on $M \| C \| \mathrm{length\_encode}(|C|)$ with the domain byte $\texttt{07}$. For $M$ and $C$ empty, the first 32 bytes are $\texttt{1ac2d450fc3b4205d19da7bfca1b37513c0803577ac7167f06fe2ce1f0ef39e5}$.
- **BLAKE3** (O'Connor, Aumasson, Neves and Wilcox-O'Hearn 2020). Not a sponge: the output is made by running the compression function of the root node again with an output counter $t = 0, 1, 2, \ldots$, 64 bytes per value of $t$. Any part of the output can be computed directly, without the bytes before it. The default 256-bit hash of the empty string is $\texttt{af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262}$, and the 64-byte output starts with it.
- **MGF1** (RFC 8017, Appendix B.2.1). $\mathrm{MGF1}(z, \ell)$ is the first $\ell$ bytes of $H(z \| \langle 0 \rangle) \| H(z \| \langle 1 \rangle) \| \cdots$ with a 4-byte counter. It has the prefix property and is used as an XOF inside [RSA-OAEP](/rsa-oaep/) and [RSA-PSS](/rsa-pss/), though it predates the name. The expand step of [HKDF](/hkdf/) has the same property for a fixed info string.

### Non-examples

- **A fixed-length hash.** SHA3-256 gives exactly 256 bits; there is no defined way to ask for more.
- **Truncated hashes with their own initial values.** SHA-512/256 and SHA-512/224 are SHA-512 with different initial values and truncation. They are distinct hash functions, not prefixes of one stream.
- **KMAC with a stated length.** $\mathrm{KMAC128}(K, X, L, S)$ appends $\mathrm{right\_encode}(L)$ to the input, so outputs of different lengths are unrelated: it is deliberately not an XOF in the length. KMACXOF128 encodes $L = 0$ and is an XOF.
- **A stream cipher keystream.** It has the prefix property in the length, but its input is a secret key and a nonce, not a message, and it need not be collision resistant.

## Related definitions

- **[Cryptographic hash function](/cryptographic-hash-function/).** A fixed output length; an XOF with a fixed $d$ can be used as one, with the strength $\min(d/2, s)$ against collisions.
- **[Sponge construction](/sponge-construction/).** The mode that gives XOFs most naturally, since squeezing can go on for as long as needed.
- **[Random oracle model](/random-oracle-model/).** The ideal object, with outputs of unbounded length.
- **[Tree hashing](/tree-hashing/).** KangarooTwelve, ParallelHash and BLAKE3 hash long inputs in a tree.
- **[KMAC](/kmac/).** The keyed function of SP 800-185, with the length bound into the input.
- **[Pseudorandom generator](/pseudorandom-generator/).** An XOF on a secret seed is used as one, for example to expand seeds in post-quantum schemes.

## References
