---
tag: AE3QKK
kind: algorithm
slug: groestl
name: Grostl
aliases:
- Groestl
- Grøstl
- Grøstl-256
- Grøstl-512
area: cryptography/hash-functions
level: advanced
summary: A SHA-3 finalist hash with a wide-pipe iteration of f(h, m) = P(h ⊕ m) ⊕ Q(m) ⊕ h, where P and Q are two fixed AES-like permutations of 512 or 1024 bits.
model: word-ram
complexity:
  vars: {N: the message length in bits}
  time: {worst: Θ(N), average: Θ(N), best: Θ(N)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2008
  people: [Praveen Gauravaram, Lars R. Knudsen, Krystian Matusiewicz, Florian Mendel, Christian Rechberger, Martin Schläffer, Søren S. Thomsen]
  note: Submitted to the SHA-3 competition in 2008. The constants were changed for the final round in January 2011, and the old version is called Grøstl-0. NIST chose Keccak in 2012.
prereqs: [cryptographic-hash-function, merkle-damgard-construction, advanced-encryption-standard]
see_also: [whirlpool, skein, jh-hash, keccak, sha-3, compression-function, length-extension-attack, indifferentiability-framework]
sources:
  - url: "https://www.groestl.info/Groestl.pdf"
    title: "P. Gauravaram, L. R. Knudsen, K. Matusiewicz, F. Mendel, C. Rechberger, M. Schläffer and S. S. Thomsen, Grøstl, a SHA-3 candidate, version 2.0.1, 2 March 2011"
    locator: Section 3 (specification; 3.2 compression function, 3.3 output transformation, 3.4 permutations, 3.5 initial values, 3.6 padding), Section 4.1 (security of the construction), Section 7.6 (security claims), Section 8.1 (Table 1, speed), Appendix B (s-box)
  - url: "https://www.groestl.info/Groestl.zip"
    title: "Grøstl final-round submission package, January 2011"
    locator: KAT_MCT/ShortMsgKAT_256.txt and ShortMsgKAT_512.txt (Len = 0, 8, 16, 512, 1024), and KAT_MCT/IntermediateValues_1BlockMsg_256.txt (input abc)
  - paper: "Pierre-Alain Fouque, Jacques Stern and Sébastien Zimmer, Cryptanalysis of tweaked versions of SMASH and Reparation, SAC 2008, LNCS 5381, pages 136 to 150"
    locator: the bounds of 2^(ℓ/4) for collisions and 2^(ℓ/2) for preimages of f(h, m) = P(h ⊕ m) ⊕ Q(m) ⊕ h with ideal P and Q, as cited in Section 4.1 of the specification
  - paper: "Elena Andreeva, Bart Mennink and Bart Preneel, On the indifferentiability of the Grøstl hash function, SCN 2010, LNCS 6280, pages 88 to 105"
    locator: indifferentiability of Grøstl from a random oracle up to about 2^(n/2) queries with ideal and independent P and Q
  - paper: "Florian Mendel, Christian Rechberger, Martin Schläffer and Søren S. Thomsen, The rebound attack: cryptanalysis of reduced Whirlpool and Grøstl, FSE 2009, LNCS 5665, pages 260 to 276"
    locator: the rebound technique and its first attacks on reduced rounds of Grøstl-0
  - url: "https://doi.org/10.6028/NIST.IR.7896"
    title: "S. Chang, R. Perlner, W. E. Burr, M. S. Turan, J. M. Kelsey, S. Paul and L. E. Bassham, NIST IR 7896, Third-Round Report of the SHA-3 Cryptographic Hash Algorithm Competition, November 2012"
    locator: the sections on Grøstl (security margin and performance)
---

Grøstl is a cryptographic hash function by Gauravaram, Knudsen, Matusiewicz, Mendel, Rechberger, Schläffer and Thomsen, and one of the five finalists of the NIST SHA-3 competition. It iterates a compression function over a chaining value at least twice as wide as the output (a wide pipe), and builds that function from two fixed permutations $P$ and $Q$ that reuse the S-box and the design ideas of [AES](/advanced-encryption-standard/). An output transformation $\Omega(x) = \mathrm{trunc}_n(P(x) \oplus x)$ makes the final digest. Grøstl-256 runs at about 12 cycles per byte with AES instructions. NIST chose Keccak as SHA-3 in 2012, and Grøstl is now mainly of interest for its clean design and its proofs.

**Notation.** $n$ is the output size in bits (8 to 512) and $\ell$ the state size: $\ell = 512$ for $n \le 256$ and $\ell = 1024$ otherwise. The state is a matrix of 8 rows and $v = \ell / 64$ columns of bytes, filled column by column. $P$ and $Q$ are permutations of $\{0,1\}^\ell$ with $r = 10$ rounds ($\ell = 512$) or $r = 14$ rounds ($\ell = 1024$). $\oplus$ is XOR, and arithmetic on bytes is in $\mathrm{GF}(2^8)$ with the AES polynomial $x^8 + x^4 + x^3 + x + 1$. $N$ is the message length in bits. The security model is the ideal permutation model: $P$ and $Q$ are random and independent permutations.

## In plain words

Grøstl reads the message in blocks of 64 bytes (or 128 bytes for the long outputs). It keeps a running value that is twice as long as the final hash. For each block, it scrambles the running value mixed with the block, scrambles the block alone in a different way, and adds both results and the old running value together.

The two scramblers $P$ and $Q$ are like AES with a fixed key. They work on a grid of bytes: add a constant, replace each byte through the AES table, slide each row by a different amount, and mix each column. At the end, Grøstl scrambles the running value once more, adds it back, and keeps the last $n$ bits.

## The problem

Build a hash function $H : \{0,1\}^{*} \to \{0,1\}^{n}$ with collision resistance $2^{n/2}$ and preimage resistance $2^n$, fast on 64-bit and 8-bit CPUs and in hardware, and immune to the generic weaknesses of the narrow [Merkle-Damgård construction](/merkle-damgard-construction/): length extension, multicollisions and long-message second preimages. These were the goals of the SHA-3 competition.

## The algorithm

```pseudo id=main
GROESTL(M, n)                                       ▷ Section 3
L1  ℓ ← 512 if n ≤ 256 else 1024;  h ← the ℓ-bit encoding of n
L2  pad M: one 1 bit, w = (−N − 65) mod ℓ zero bits, then the 64-bit number of blocks
L3  for each ℓ-bit block m:  h ← P(h ⊕ m) ⊕ Q(m) ⊕ h
L4  return the last n bits of P(h) ⊕ h

P or Q on an 8 × v byte matrix A                    ▷ Section 3.4
L5  for round i ← 0 to r − 1 do
L6      AddRoundConstant: P adds (16j ⊕ i) to row 0 of column j; Q adds FF to all bytes and (16j ⊕ i) to row 7
L7      SubBytes: each byte goes through the AES S-box
L8      ShiftBytes: row k moves σk places left; σ = 0..7 for P and (1, 3, 5, 7, 0, 2, 4, 6) for Q
L9      MixBytes: each column is multiplied by B = circ(02, 02, 03, 04, 05, 03, 05, 07)
```

For $\ell = 1024$ the shift vectors are $(0, 1, 2, 3, 4, 5, 6, 11)$ for $P$ and $(1, 3, 5, 11, 0, 2, 4, 6)$ for $Q$. $N$ is the message length in bits. The initial values for $n = 224, 256, 384, 512$ end in the bytes `00 E0`, `01 00`, `01 80` and `02 00`.

## Example

Grøstl-256 of `abc`, with the values of the official file `IntermediateValues_1BlockMsg_256.txt`.

1. Line L1 sets $\ell = 512$ and $h$ to 64 bytes whose last two are `01 00`. In the matrix this is a 1 in row 6 of column 7.
2. Line L2 gives one block: `61 62 63 80`, then 52 zero bytes, then the block count `00 00 00 00 00 00 00 01`.
3. Line L3 computes $P(h \oplus m) \oplus Q(m) \oplus h$. The first column of the new chaining value is `03 76 99 02 7B 7F 61 A2` and the last is `46 9E 93 21 CA 21 7D 9A`.
4. Line L4 computes $P(h) \oplus h$ and keeps the last 32 bytes, which are columns 4 to 7: `F3C1BB19C048801326A7EFBCF16E3D7887446249829C379E1840D1A3A1E7D4D2`.

The code of this page gives the same values, and the tests check them.

## Correctness

The code is checked against the official short-message known-answer tests for Grøstl-256 and Grøstl-512 (messages of 0, 1, 2, 64 and 128 bytes) and against the intermediate values for `abc`. The proof page shows that a collision of Grøstl gives a collision of $f$ or of the output transformation.

**Security of the construction.** Write $f(h, m) = P(h \oplus m) \oplus Q(m) \oplus h$. If $P$ and $Q$ are ideal, finding a collision of $f$ needs about $2^{\ell/4}$ queries and a preimage $2^{\ell/2}$ (Fouque, Stern and Zimmer). Since $\ell \ge 2n$, these are at least $2^{n/2}$ and $2^n$, the generic bounds for an $n$-bit hash. Andreeva, Mennink and Preneel prove that Grøstl is indifferentiable from a random oracle up to about $2^{n/2}$ queries with ideal and independent $P$ and $Q$. Both results are bounds in the ideal permutation model, and the designers state that they do not claim that $P$ and $Q$ are ideal.

**Why the wide pipe.** The chaining value has $\ell \ge 2n$ bits and the output only $n$, so an internal collision costs $2^{\ell/2} \ge 2^n$ work, more than a collision of the output. This defeats the multicollision attack of Joux and the long-message second-preimage attacks, which need internal collisions. The output does not reveal $h$, so a [length extension attack](/length-extension-attack/) does not apply.

## Complexity

Each block of $\ell$ bits costs one evaluation of $P$ and one of $Q$, so $2r$ rounds over a state of $\ell / 8$ bytes: for Grøstl-256, 20 rounds of 64 S-box lookups and 8 column mixes per 64-byte block. The output step costs one more $P$. So the time is $\Theta(N)$ for a message of $N$ bits, and the extra space is the chaining value. $P$ and $Q$ on the same block are independent and run in parallel. The specification reports 12.45 cycles per byte for Grøstl-256 and 17.85 for Grøstl-512 with AES-NI on an Intel Core i7 M620.

## Properties

- **Claimed security** (Section 7.6): collision $2^{n/2}$, preimage $2^n$, second preimage $2^{n-k}$ for a first message of up to $2^k$ blocks.
- **Wide pipe**: internal state at least $2n$ bits.
- **AES components**: the S-box and the style of MixBytes, so AES instructions and AES hardware help, and the analysis of AES carries over.
- **No key input**: keyed use is through HMAC or the envelope MAC $H(K \| M \| K)$ proposed in Section 6.1.
- **Two permutations**: $P$ and $Q$ differ only in constants and shifts, so one circuit can compute both.

## Variants and improvements

- **Grøstl-0**, the version of 2008, had other round constants and shifts for $Q$. Rebound attacks reached more rounds on it, and the final-round tweak of 2011 changed the constants to raise the margin.
- **Grøstl-224, -256, -384 and -512** differ only in $\ell$, the IV and the truncation. Any output of 8 to 512 bits in steps of 8 is defined.
- **[Whirlpool](/whirlpool/)** is an older AES-like hash with a single 512-bit block cipher in Miyaguchi-Preneel mode; the rebound attack was first shown on Whirlpool and Grøstl together.

## When to use it

Do not choose Grøstl for new systems: few libraries support it, and [SHA-3](/sha-3/), [SHA-2](/sha-2/) and [BLAKE2](/blake2/) are standard and faster in software without AES instructions. Grøstl is still worth study as a hash with a proof in the ideal permutation model and a wide pipe, and it is used in some cryptocurrencies (Groestlcoin) that chose it for that reason.

## Pitfalls

- **Grøstl-0 and Grøstl give different values.** Check which version a library or a test vector uses.
- **Byte order of the state.** Bytes fill the matrix column by column, as in AES. A row-by-row fill gives wrong digests while the round functions look right.
- **Truncating the wrong end.** $\Omega$ keeps the trailing $n$ bits of $P(h) \oplus h$, not the leading ones.
- **Q constants.** $Q$ XORs `FF` into every byte, not just a row, before the round counter; missing this still gives a permutation and so passes simple tests.
- **Table lookups and timing.** An S-box implemented as a table in memory leaks through the cache, as for AES. Use bitsliced code or AES instructions.

## Implementations

The Python code is for study only. It is not constant time, because the S-box is a table, and it must not protect real data; use the reference or optimized C code of the designers (in `Groestl.zip` and in eBASH), or a standard hash. The code gives `permutation` (lines L5 to L9), `compress` and `pad`, and `groestl(msg, n)` (lines L1 to L4) with `groestl256` and `groestl512`. It handles whole bytes only. The S-box is computed from its definition and checked against Appendix B. The tests copy by hand the known answers of the final-round package and the `abc` intermediate values. They also check the padding, that Grøstl-224 is not a truncation of Grøstl-256, that $P$ and $Q$ differ, and that one changed bit changes about half of the output bits. Python's standard library has no Grøstl, so there is no second check.

## History

Grøstl was designed at the Technical University of Denmark and TU Graz and submitted to the SHA-3 competition in October 2008. Its authors also invented the rebound attack, which they applied to reduced Grøstl-0 and Whirlpool in 2009. Grøstl reached the second round in 2009 and the final round in December 2010, with the tweaked constants of version 2.0 of January 2011. NIST IR 7896 (2012) found no attack on the full function and chose Keccak, which differed most from SHA-2 and was fastest in hardware.

## References
