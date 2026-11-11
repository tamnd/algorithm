---
tag: WAM1AS
kind: algorithm
slug: skein
name: Skein
aliases:
- Skein-256
- Skein-512
- Skein-1024
- Threefish
- UBI
area: cryptography/hash-functions
level: advanced
summary: A SHA-3 finalist hash built from Threefish, a tweakable ARX block cipher, in the UBI chaining mode. The tweak gives each block its position and type, which also yields MAC, KDF and tree modes.
model: word-ram
complexity:
  vars: {n: the message length in bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2008
  people: [Niels Ferguson, Stefan Lucks, Bruce Schneier, Doug Whiting, Mihir Bellare, Tadayoshi Kohno, Jon Callas, Jesse Walker]
  note: Submitted to the NIST SHA-3 competition in 2008. Version 1.2 changed the rotation constants and version 1.3 of October 2010 the key schedule constant. Skein was a finalist; NIST chose Keccak in 2012.
prereqs: [block-cipher, merkle-damgard-construction, cryptographic-hash-function]
see_also: [sha-3, keccak, blake2, groestl, jh-hash, tree-hashing, threefry, hmac]
sources:
  - url: "https://www.schneier.com/wp-content/uploads/2015/01/skein.pdf"
    title: "N. Ferguson, S. Lucks, B. Schneier, D. Whiting, M. Bellare, T. Kohno, J. Callas and J. Walker, The Skein Hash Function Family, version 1.3, 1 October 2010"
    locator: Section 3.3 (Threefish, Tables 2 to 4), Section 3.4 (UBI, Table 5), Section 3.5 (Skein, Tables 6 and 7, tree mode in 3.5.6), Section 6 (security claims), Section 8.3 (the constant C240), Appendix B (initial chaining values), Appendix C (test vectors)
  - paper: "Mihir Bellare, Tadayoshi Kohno, Stefan Lucks, Niels Ferguson, Bruce Schneier, Doug Whiting, Jon Callas and Jesse Walker, Provable security support for the Skein hash family, version 1.0, April 2009"
    locator: the reductions that show UBI preserves collision resistance, pseudorandomness and indifferentiability of the Threefish compression function
  - paper: "Moses Liskov, Ronald L. Rivest and David Wagner, Tweakable block ciphers, CRYPTO 2002, LNCS 2442, pages 31 to 46"
    locator: the definition of a tweakable block cipher, which Threefish instantiates
  - paper: "Dmitry Khovratovich and Ivica Nikolić, Rotational cryptanalysis of ARX, FSE 2010, LNCS 6147, pages 333 to 346"
    locator: the related-key rotational attack on reduced Threefish with the old constant C5, cited in Section 9.5.2 of the specification
  - paper: "Dmitry Khovratovich, Ivica Nikolić and Christian Rechberger, Rotational rebound attacks on reduced Skein, ASIACRYPT 2010, LNCS 6477"
    locator: the known-key distinguisher on reduced Threefish and the compression function of reduced Skein
  - url: "https://doi.org/10.6028/NIST.IR.7896"
    title: "S. Chang, R. Perlner, W. E. Burr, M. S. Turan, J. M. Kelsey, S. Paul and L. E. Bassham, NIST IR 7896, Third-Round Report of the SHA-3 Cryptographic Hash Algorithm Competition, November 2012"
    locator: the sections on Skein (security margin and performance) and the reasons for the choice of Keccak
---

Skein is a family of cryptographic hash functions by Ferguson, Lucks, Schneier, Whiting, Bellare, Kohno, Callas and Walker, and one of the five finalists of the NIST SHA-3 competition. Its core is Threefish, a tweakable [block cipher](/block-cipher/) with blocks of 256, 512 or 1024 bits that uses only 64-bit addition, rotation and XOR. The UBI chaining mode feeds each message block to Threefish as plaintext, with the chaining value as key and a 128-bit tweak that holds the number of bytes so far and the type of the data. The same machine computes a plain hash, a MAC, a KDF, a personalized hash and a tree hash, and it gives output of any length. Skein-512 hashes long messages at about 6 cycles per byte on a 64-bit CPU of 2008.

**Notation.** $N_b$ is the state size in bytes (32, 64 or 128) and $N_w = N_b / 8$ the number of 64-bit words. $N_o$ is the output size in bits, and $n$ the message length in bytes. $E(K, T, P)$ is Threefish encryption with key $K$, tweak $T$ and plaintext $P$, and $N_r$ its number of rounds (72, 72 or 80). Words are little-endian, $+$ is addition modulo $2^{64}$, $\lll$ left rotation and $\oplus$ XOR. A type value $T_x$ (Table 6 of the specification) is placed in bits 120 to 125 of the tweak, written $T_x 2^{120}$. The security model for the mode is a reduction to the compression function $(K, T, P) \mapsto E(K, T, P) \oplus P$.

## In plain words

Skein has a block cipher at its center. Normally a cipher uses a secret key to scramble a block. Skein uses the hash value so far as the key, scrambles the next piece of the message with it, and adds the piece back in. The result becomes the key for the next piece.

The cipher has a third input, the tweak, which works like a label on each call. The label says how many bytes of the message have been read so far, whether this is the first or the last piece, and what kind of data it is: the settings, a key, the message, or the output step. Because every call has a different label, pieces cannot be moved around or reused, and the end of a message cannot be extended.

## The problem

Build a hash function $H : \{0,1\}^{*} \to \{0,1\}^{N_o}$ that has collision resistance of $2^{m/2}$ and preimage resistance of $2^m$, with $m = \min(8 N_b, N_o)$. It must also be a good pseudorandom function under a key, resist length extension, and be fast in software on 64-bit CPUs. These were the requirements of the SHA-3 competition. Skein further wants one construction for all the uses of a hash: MAC, KDF, randomized hashing and tree hashing.

## The algorithm

```pseudo id=main
SKEIN(M, Nb, No, K)                                    ▷ Section 3.5.5, with no tree
L1  K′ ← 0^Nb  if K is empty, else UBI(0^Nb, K, T_key 2^120)
L2  G ← UBI(K′, C, T_cfg 2^120)                        ▷ C: "SHA3", version 1, No, tree fields 0
L3  G ← UBI(G, M, T_msg 2^120)                         ▷ also personalization, nonce, ... in type order
L4  return the first No bits of UBI(G, 0, T_out 2^120) ‖ UBI(G, 1, T_out 2^120) ‖ …

UBI(G, M, Ts)                                          ▷ Section 3.4
L5  pad M with zero bytes to k ≥ 1 blocks M0, …, Mk−1 of Nb bytes
L6  for i ← 0 to k − 1: tweak ← Ts + min(n, (i + 1) Nb) + First·[i = 0] + Final·[i = k − 1]
L7      G ← E(G, tweak, Mi) ⊕ Mi
    return G

E(K, T, P)                                             ▷ Threefish, Section 3.3
L8  k_Nw ← C240 ⊕ k0 ⊕ … ⊕ k_(Nw−1);  t2 ← t0 ⊕ t1;  subkey s uses k, t and s
L9  for d ← 0 to Nr − 1: add subkey d/4 if 4 | d; MIX each pair (x0, x1) ↦ (x0 + x1, (x1 ⋘ R) ⊕ (x0 + x1)); permute words
L10 return the state plus subkey Nr/4
```

The constant $C_{240}$ is `1BD11BDAA9FC1A22`. Subkey $s$ is the words $k_{(s+i) \bmod (N_w+1)}$, with $t_{s \bmod 3}$ added to word $N_w - 3$, $t_{(s+1) \bmod 3}$ added to word $N_w - 2$, and $s$ added to the last word. First is bit 126 and Final is bit 127 of the tweak. The 32-byte configuration string $C$ does not depend on $M$, so the value $G$ after line L2 is a fixed initial chaining value for each pair $(N_b, N_o)$, listed in Appendix B.

## Example

Skein-256-256 of the single byte `FF`, as in Appendix C.1.

1. Line L1 sets $K'$ to 32 zero bytes, since there is no key.
2. Line L2 hashes the configuration $C$ = `53 48 41 33 01 00 00 00 00 01 00 ...` ("SHA3", version 1, $N_o = 256$) with tweak `C4000000 00000000 00000000 00000020`: type 4, First, Final, position 32. The result is the initial value of Appendix B.4, which begins with the word `FC9DA860D048B449`.
3. Line L3 pads `FF` with 31 zero bytes and uses tweak `F0000000 00000000 00000000 00000001`: type 48, First, Final, position 1. The position records the true length, so `FF` and `FF 00` give different tweaks. The new chaining value begins `1E035A91ED39AE27`.
4. Line L4 encrypts the 8-byte counter 0 with type 63 and position 8, and gives `0B98DCD198EA0E50A7A244C444E25C23DA30C10FC9A1F270A6637F1F34E67ED2`, the value of Appendix C.1.

The chaining value of step 3 is computed by the code of this page. With the initial value stored, a short message costs two Threefish calls: one for the message block and one for the output.

## Correctness

The code is checked against all 9 test vectors of Appendix C (three each for Skein-256-256, Skein-512-512 and Skein-1024-1024) and against 5 initial chaining values of Appendix B. The proof page shows why UBI is injective on its inputs.

**Why the mode is sound.** Write $F(G, T, M) = E(G, T, M) \oplus M$, which is the Matyas-Meyer-Oseas form of a compression function from a block cipher, with a tweak. Each call of $F$ in one Skein evaluation gets a different tweak: the type separates the configuration, key, message and output calls, and the position, First and Final bits separate the blocks within one UBI call. So the sequence of tweaks, together with the padded blocks, determines the input. Bellare et al. (2009) show that UBI preserves collision resistance, pseudorandomness under a key, and indifferentiability from a random oracle when $F$ has the matching property. The reductions are tight up to the number of calls of $F$.

**No length extension.** The output is not the last chaining value but UBI of the chaining value with type $T_{out}$, so an attacker who sees $H(M)$ does not have a chaining value. To extend $M$, it must invert the output step.

## Complexity

UBI makes $\lceil n / N_b \rceil$ Threefish calls for $n \ge 1$ bytes and one call for the empty message. Threefish-512 has 72 rounds of 4 MIX steps, so 288 additions, 288 rotations and 288 XORs, plus 19 subkey additions of 8 words, per 64-byte block. The output step costs one call per $8 N_b$ bits of output. So Skein runs in $\Theta(n)$ time with $\Theta(1)$ extra space. Section 5 of the specification reports 6.1 cycles per byte for Skein-512 in assembly on a 64-bit Core 2 CPU, and about 1000 cycles for a short message. The code of this page hashes 64 KB with Skein-512 in about 2 seconds.

## Properties

- **Claimed security** (Section 6.1): preimage and second preimage $2^m$, collision $2^{m/2}$, MAC and PRF security $\min(2^{4 N_b}, 2^m)$, where $m = \min(8 N_b, N_o)$.
- **Any output length**: one state gives any $N_o$, and $N_o$ is in the configuration, so a shorter output is not a prefix of a longer one.
- **Built-in MAC**: keyed Skein processes the key in its own UBI call, at the cost of one Threefish call, instead of the two hash passes of [HMAC](/hmac/).
- **ARX only**: no tables, so no cache timing leaks in a careful implementation.
- **Optional arguments**: key, personalization, public key, key identifier and nonce, each with its own type.

## Variants and improvements

- **Skein-256, Skein-512 and Skein-1024**, with Skein-512 the main proposal. Each supports any $N_o$; Skein-512-256 is a drop-in for SHA-256.
- **Tree mode** (Section 3.5.6): leaves of $N_b 2^{Y_l}$ bytes, fan-out $2^{Y_f}$ and maximum height $Y_m$, with the tree level in bits 112 to 118 of the tweak. See [tree hashing](/tree-hashing/). The code of this page does not implement it.
- **Threefish as a cipher**: a tweakable block cipher with large blocks, usable in normal modes. [Threefry](/threefry/), a counter-based random number generator, uses a reduced Threefish.
- **Version changes**: version 1.2 (2009) changed the rotation constants for more diffusion, and version 1.3 (2010) changed the key schedule constant from `5555...5` to $C_{240}$, to block rotational attacks.

## When to use it

Skein is a sound hash with a large security margin, but it is not a standard, and few libraries support it. For new systems use [SHA-3](/sha-3/), [SHA-2](/sha-2/), [BLAKE2](/blake2/) or BLAKE3. Use Skein when a protocol already specifies it, or to study how a tweakable block cipher gives a clean hash mode. The tweak-based domain separation of UBI is a model for later designs.

## Pitfalls

- **Old versions.** Skein 1.0, 1.1 and 1.2 give different values from 1.3. A library or a test vector must say which version it uses.
- **Bit-length messages.** Messages whose length is not a multiple of 8 use the BitPad flag; code that handles only bytes, like this page, must reject them, not pad them silently.
- **Output size in the configuration.** Truncating Skein-512-512 to 256 bits does not give Skein-512-256. Use the right $N_o$.
- **Treating the MAC as HMAC.** Keyed Skein is not HMAC-Skein; they give different values, and a protocol must name one.

## Implementations

The Python code is for study only. It is not constant time and must not protect real data; use a maintained library that offers Skein, such as Crypto++ or the reference code of the authors, or better a standard hash. The code gives `threefish_encrypt` (lines L8 to L10), `ubi` (lines L5 to L7), `skein` (lines L1 to L4) with a key and optional typed arguments, and `skein256`, `skein512` and `skein1024`. It supports whole bytes only and no tree mode. The tests copy by hand the 9 vectors of Appendix C and 5 initial values of Appendix B. They also check that a wrong MAC key fails, that a personalization changes the output, that a shorter output is not a prefix, that zero padding is not ambiguous, and that one changed bit changes about 128 of 256 output bits. Python's standard library has no Skein, so there is no second check.

## History

Skein was submitted to the SHA-3 competition in October 2008 by a team from industry and academia, with Threefish and UBI designed for it. It reached the second round in 2009, where the designers changed the rotation constants, and the final round in December 2010, with the new key schedule constant of version 1.3. The best published attacks reached about half of the rounds of Threefish. In October 2012 NIST chose Keccak as SHA-3. NIST IR 7896 credits Skein with good software speed and a solid security margin, and prefers Keccak for its hardware speed and its different design from SHA-2.

## References
