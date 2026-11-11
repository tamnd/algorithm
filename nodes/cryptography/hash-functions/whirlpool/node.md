---
tag: C0V92H
kind: algorithm
slug: whirlpool
name: Whirlpool
aliases:
- Whirlpool hash
area: cryptography/hash-functions
level: advanced
summary: A 512-bit hash by Barreto and Rijmen (2000) that iterates an AES-like cipher W on 8 x 8 bytes in Miyaguchi-Preneel mode, with a 256-bit length field. Standardized in ISO/IEC 10118-3.
model: word-ram
complexity:
  vars: {n: the message length in bytes}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2000
  people: [Paulo S. L. M. Barreto, Vincent Rijmen]
  note: Submitted to NESSIE in 2000, revised as Whirlpool-T in 2001 and to the final version in 2003, then selected by NESSIE and adopted in ISO/IEC 10118-3.
prereqs: [miyaguchi-preneel-construction, advanced-encryption-standard]
see_also: [merkle-damgard-construction, block-cipher, substitution-permutation-network, s-box, compression-function, sha-2, groestl, collision-resistance]
sources:
  - paper: "Paulo S. L. M. Barreto and Vincent Rijmen, The Whirlpool hashing function, submitted to NESSIE, September 2000, revised May 2003"
    locator: the sections on the cipher W (the state, the S-box built from the mini-boxes E and R, the cyclical permutation pi, the linear diffusion layer theta, the key addition sigma, the round constants and the key schedule), on the Miyaguchi-Preneel hashing mode and padding, and the appendix on the changes from Whirlpool-0 and Whirlpool-T
  - paper: "ISO/IEC 10118-3, Information technology, Security techniques, Hash-functions, Part 3, Dedicated hash-functions"
    locator: the dedicated hash function Whirlpool and its test vectors
  - url: "https://github.com/randombit/botan/blob/master/src/tests/data/hash/whirlpool.vec"
    title: Botan, test data for Whirlpool
    locator: the section [Whirlpool], the first 8 entries, which reproduce the ISO/IEC 10118-3 vectors and are used in the tests
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 9.4.1, Algorithm 9.43 (the Miyaguchi-Preneel hash)
  - paper: "Taizo Shirai and Kyoji Shibutani, On the diffusion matrix employed in the Whirlpool hashing function, NESSIE public report, 2003"
    locator: the observation that the diffusion matrix of the earlier versions is not MDS, which led to the final matrix
  - paper: "Florian Mendel, Christian Rechberger, Martin Schläffer and Søren S. Thomsen, The rebound attack, cryptanalysis of reduced Whirlpool and Grøstl, Fast Software Encryption, FSE 2009, LNCS 5665, Springer, 2009"
    locator: the rebound attack and collisions for round-reduced Whirlpool
---

Whirlpool is a hash function with a 512-bit digest, designed by Paulo Barreto and Vincent Rijmen in 2000. Its compression function is a dedicated block cipher W in the [Miyaguchi-Preneel](/miyaguchi-preneel-construction/) mode: the chaining value is the key, the message block is the plaintext, and the output is $W_H(m) \oplus H \oplus m$. W is a close relative of the [AES](/advanced-encryption-standard/), co-designed by Rijmen: a [substitution-permutation network](/substitution-permutation-network/) on an $8 \times 8$ matrix of bytes, with 10 rounds and a key schedule that uses the same round function. The hash is a [Merkle-Damgard](/merkle-damgard-construction/) iteration from $H_0 = 0$ with a 256-bit length field. There were three versions: Whirlpool-0 (2000), Whirlpool-T (2001), which changed the S-box, and the final Whirlpool (2003), which changed the diffusion matrix. The final version is in ISO/IEC 10118-3 and is the one on this page.

**Notation.** The state is an $8 \times 8$ matrix of bytes; a 64-byte block fills it row by row, so entry $(i, j)$ is byte $8i + j$. Bytes are elements of $\mathrm{GF}(2^8)$ modulo $x^8 + x^4 + x^3 + x^2 + 1$ (hex $\texttt{11D}$). $\oplus$ is XOR. $W_K(m)$ is the cipher with key $K$ on the block $m$. $c^r$ is the round constant of round $r$. $n$ is the message length in bytes.

## In plain words

Whirlpool chops the message into 64-byte blocks and keeps a 64-byte chaining value, which starts at zero. For each block, it encrypts the block with a cipher whose key is the chaining value, and then XORs the result with both the block and the old chaining value. The XORs make the step one-way even though the cipher can be decrypted. The cipher looks like the AES on a bigger square: each round replaces every byte through an S-box, slides each column down by a different amount, mixes each row with a fixed matrix, and adds a round key. The round keys come from running the same rounds on the key with constants. After the last block, the chaining value is the digest.

## The problem

The input is a message $M$ of $n$ bytes, with $8n < 2^{256}$. The output is a 512-bit digest. It should be collision resistant up to about $2^{256}$ work and preimage resistant up to about $2^{512}$. The design goal was a hash of 512 bits whose security rests on the well-studied wide-trail design of the AES rather than on the MD4 family, which was under attack.

## The algorithm

One round $\rho[k] = \sigma[k] \circ \theta \circ \pi \circ \gamma$ of W has four layers:

- $\gamma$: replace each byte $a$ by $S[a]$. The 8-bit S-box is built from 4-bit mini-boxes: with $u = (u_h, u_l)$, let $a = E[u_h]$, $b = E^{-1}[u_l]$ and $r = R[a \oplus b]$; then $S[u] = (E[a \oplus r], E^{-1}[b \oplus r])$. $S[\texttt{00}] = \texttt{18}$.
- $\pi$: column $j$ moves down by $j$ places: $b_{i, j} = a_{(i - j) \bmod 8,\, j}$.
- $\theta$: multiply each row by the circulant matrix $C = \mathrm{cir}(\texttt{01}, \texttt{01}, \texttt{04}, \texttt{01}, \texttt{08}, \texttt{05}, \texttt{02}, \texttt{09})$ over $\mathrm{GF}(2^8)$: $b_{i, j} = \bigoplus_k C_{(j - k) \bmod 8}\, a_{i, k}$. $C$ is MDS, so a row with $t$ nonzero bytes becomes a row with at least $9 - t$ nonzero bytes.
- $\sigma[k]$: XOR the round key $k$.

The round constant $c^r$ has row 0 equal to $S[8(r - 1)], \ldots, S[8(r - 1) + 7]$ and zeros elsewhere. The key schedule is $K^0 = K$ and $K^r = \rho[c^r](K^{r-1})$.

```pseudo id=main
WHIRLPOOL(M)
L1  P ← M ‖ 80 ‖ 00…00 ‖ [8n]₂₅₆           ▷ zeros until |P| ≡ 32 mod 64, then the length big-endian
L2  H ← 0⁶⁴                                 ▷ 64 zero bytes
L3  for each 64-byte block Y of P, in order, do
L4      H ← COMPRESS(H, Y)
L13 return H

COMPRESS(H, Y)                              ▷ Miyaguchi-Preneel
L5  m ← Y as an 8 × 8 matrix, row by row
L6  return W(H, m) ⊕ H ⊕ m

W(K, m)                                     ▷ the block cipher, key K
L7  k ← K
L8  s ← m ⊕ k                               ▷ key whitening with K⁰
L9  for r ← 1 to 10 do
L10     k ← ρ[c^r](k)                       ▷ next round key K^r
L11     s ← ρ[k](s)                         ▷ σ[K^r] ∘ θ ∘ π ∘ γ
L12 return s
```

The code stores the matrix as a list of 64 bytes and multiplies with a table of the products $c \cdot x$ for the 6 coefficients of $C$.

## Example

**The first round key for $H = 0$.** For the first block, the key is all zero. $\gamma$ turns every byte into $S[\texttt{00}] = \texttt{18}$. $\pi$ does not change a constant matrix. $\theta$ multiplies each row of $\texttt{18}$s by $C$, which gives $\texttt{18} \cdot (\texttt{01} \oplus \texttt{01} \oplus \texttt{04} \oplus \texttt{01} \oplus \texttt{08} \oplus \texttt{05} \oplus \texttt{02} \oplus \texttt{09}) = \texttt{18} \cdot \texttt{03} = \texttt{28}$ in every byte. Then $\sigma[c^1]$ adds the first 8 entries of the S-box, $\texttt{18 23 C6 E8 87 B8 01 4F}$, to row 0. So $K^1$ has row 0 equal to $\texttt{30 0B EE C0 AF 90 29 67}$ and every other byte equal to $\texttt{28}$.

**Whirlpool("abc").** The padded message is one block: $\texttt{61 62 63 80}$, 59 zero bytes, and the bit length 24 in the last byte, $\texttt{18}$. With $K^0 = 0$, the state starts as the block. After $\gamma$, row 0 is $\texttt{0F D5 80 97 18 18 18 18}$, and after the whole first round it is $\texttt{0F 34 9A FF 3F F3 2F E0}$. After 10 rounds, row 0 of $W_0(m)$ is $\texttt{2F 46 2B 24 C6 F4 86 BB}$. Line L6 XORs in $H = 0$ and $m$, so row 0 of the digest is $\texttt{2F} \oplus \texttt{61} = \texttt{4E}$, $\texttt{46} \oplus \texttt{62} = \texttt{24}$, $\texttt{2B} \oplus \texttt{63} = \texttt{48}$, $\texttt{24} \oplus \texttt{80} = \texttt{A4}$, then $\texttt{C6 F4 86 BB}$. The full digest is

`4e2448a4c6f486bb16b6562c73b4020bf3043e3a731bce721ae1b303d97e6d4c7181eebdb6c57e277d0e34957114cbd6c797fc9d95d8b582d225292076d4eef5`.

**The ISO vectors.** The tests check the 8 short vectors of ISO/IEC 10118-3 as they appear in Botan's test data, among them:

| Message | First 32 bytes of Whirlpool |
|---|---|
| "" | `19fa61d75522a4669b44e39c1d2e1726c530232130d407f89afee0964997f7a7` |
| "a" | `8aca2602792aec6f11a67206531fb7d7f0dff59413145e6973c45001d0087b42` |
| "abc" | `4e2448a4c6f486bb16b6562c73b4020bf3043e3a731bce721ae1b303d97e6d4c` |
| "message digest" | `378c84a4126e2dc6e56dcc7458377aac838d00032230f53ce1f5700c0ffb4d3b` |

The tests also check that $S$ is a permutation with first row $\texttt{18 23 C6 E8 87 B8 01 4F}$, that $x^8 = x^4 + x^3 + x^2 + 1$ in the field, and the padding lengths: 31 bytes fit in one block, 32 bytes need two.

## Correctness

The padding is injective and gives whole blocks, and the loop is the Merkle-Damgard iteration, so the [Merkle-Damgard theorem](/merkle-damgard-theorem/) reduces collisions of Whirlpool to collisions of COMPRESS. Each layer of a round is a bijection of the state ($\gamma$ because $S$ is a permutation, $\pi$ because it moves bytes, $\theta$ because $C$ is invertible, $\sigma$ because it is an XOR), so $W_K$ is a permutation for every key, and COMPRESS has the Miyaguchi-Preneel form. If W were an ideal cipher, the Black-Rogaway-Shrimpton bounds for this form would apply. The proof file gives the details. That the code is the ISO function is checked by the vectors.

## Complexity

Each block takes 10 rounds of the cipher and 10 rounds of the key schedule, 20 applications of $\rho$, each a fixed amount of work on 64 bytes: $\Theta(1)$ per block. A message of $n$ bytes has $\lfloor (n + 32)/64 \rfloor + 1$ blocks, so the time is $\Theta(n)$ and the extra space is the state, the key and the block, $\Theta(1)$. Fast software merges $\gamma$, $\pi$ and $\theta$ into 8 tables of 256 entries of 64 bits, as for the AES. Even so, Whirlpool is slower than SHA-512, because the key schedule doubles the work.

## Properties

- **Wide-trail design.** $\theta$ is MDS with branch number 9, so any two-round trail activates at least 9 S-boxes and any four-round trail at least 81; the designers use this to bound differential and linear trails of W.
- **Miyaguchi-Preneel mode.** The compression function is one-way even though W is invertible, and the key input changes with every block, so related-key properties of W matter. There is no easy fixed point as in Davies-Meyer: $\mathrm{COMPRESS}(H, m) = H$ needs $W_H(m) = m$, a fixed point of $W_H$ for the given key $H$, and nobody knows how to find one faster than by trying blocks.
- **No length extension protection.** Whirlpool is a plain Merkle-Damgard hash, so $H(M)$ and $|M|$ give $H(M \| \mathrm{pad} \| S)$. Use [HMAC](/hmac/) for a MAC.
- **Cryptanalysis.** The rebound attack of Mendel, Rechberger, Schläffer and Thomsen (2009) was first shown on Whirlpool, with collisions on round-reduced versions. Later work reaches more rounds of the compression function with distinguishers and near-collisions, but no attack on the full hash is known.

## Variants and improvements

- **Whirlpool-0** (2000): the NESSIE submission, with an S-box chosen pseudo-randomly and the matrix $\mathrm{cir}(\texttt{01}, \texttt{01}, \texttt{03}, \texttt{01}, \texttt{05}, \texttt{08}, \texttt{09}, \texttt{05})$.
- **Whirlpool-T** (2001): the S-box replaced by the one built from the mini-boxes $E$ and $R$, which is much smaller in hardware.
- **Whirlpool** (2003): Shirai and Shibutani showed that the earlier matrix is not MDS (it has a singular $2 \times 2$ submatrix), and the designers replaced it with $\mathrm{cir}(\texttt{01}, \texttt{01}, \texttt{04}, \texttt{01}, \texttt{08}, \texttt{05}, \texttt{02}, \texttt{09})$, which is. The three versions give different digests.
- **[Grøstl](/groestl/)**, a SHA-3 finalist, reuses AES-like permutations in a different mode, and its analysis grew out of the Whirlpool attacks.

## When to use it

Use Whirlpool only for compatibility: some disk encryption tools, such as VeraCrypt, offer it as a key derivation hash, and some file formats and archives list it. For new designs, [SHA-2](/sha-2/) (SHA-512) and [SHA-3](/sha-3/) (SHA3-512) give the same digest length with far more analysis, more library support and better speed.

## Pitfalls

- **Three versions.** Whirlpool-0, Whirlpool-T and Whirlpool give different digests. Check a known vector: Whirlpool("") starts with `19fa61d7`.
- **Big-endian length of 256 bits.** The length field is 32 bytes, not 8 as in SHA-512, so a message of 32 to 63 bytes already needs a second block.
- **Table lookups.** The fast table form indexes by state and key bytes, which leaks through the cache. The code here also uses tables and is not constant time.
- **Not in hashlib.** Python's `hashlib` does not offer Whirlpool on most systems, so test against the ISO vectors.
- **For study only.** The code on this page is slow and not constant time. Use a vetted library if a format needs Whirlpool.

## Implementations

## History

Barreto and Rijmen submitted Whirlpool to the NESSIE project of the European Commission in 2000; Rijmen had co-designed Rijndael, which became the AES the same year. In 2001 they replaced the S-box with a structured one that is cheaper in hardware, giving Whirlpool-T. In 2003 Shirai and Shibutani showed that the diffusion matrix was not MDS, and the designers changed it, giving the final Whirlpool. NESSIE selected Whirlpool for its portfolio in 2003, and ISO/IEC 10118-3 adopted it in 2004. The name comes from the Whirlpool galaxy, M51.

## References
