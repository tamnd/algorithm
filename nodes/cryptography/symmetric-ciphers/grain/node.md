---
tag: VM4425
kind: algorithm
slug: grain
name: Grain
area: cryptography/symmetric-ciphers
level: advanced
summary: A family of bit-oriented hardware stream ciphers built from one LFSR and one NFSR. This page implements Grain-128AEADv2, a NIST lightweight finalist with a 128-bit key and a 64-bit tag.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the number of bits of associated data and message}
  time: {worst: Θ(n + 512), average: Θ(n + 512), best: Θ(n + 512)}
  space: {extra: Θ(384)}
properties: {deterministic: true}
history:
  year: 2005
  people: [Martin Hell, Thomas Johansson, Willi Meier]
  note: Grain was submitted to eSTREAM in 2005, and Grain v1 entered the eSTREAM hardware portfolio in 2008. Grain-128 (2006), Grain-128a (2011) and Grain-128AEADv2 (NIST LWC finalist, 2021) followed.
prereqs: [stream-cipher, lfsr]
see_also: [trivium, lfsr, stream-cipher, authenticated-encryption, ascon, lightweight-cryptography, a5-1]
sources:
  - paper: "Martin Hell, Thomas Johansson, Alexander Maximov, Willi Meier, Jonathan Sönnerup and Hirotaka Yoshida, Grain-128AEADv2: A lightweight AEAD stream cipher, specification for the final round of the NIST Lightweight Cryptography standardization process, 2021"
    locator: Sections 2.1 to 2.6 (the algorithm and the NIST byte API), Section 3.1 (history of the family) and Section 7 (test vectors)
  - paper: "Martin Hell, Thomas Johansson and Willi Meier, Grain: a stream cipher for constrained environments, International Journal of Wireless and Mobile Computing 2(1), 2007, pp. 86-93"
    locator: the Grain v1 design with an 80-bit key, a 64-bit IV and 160 initialization clocks
  - paper: "Martin Hell, Thomas Johansson, Alexander Maximov and Willi Meier, A stream cipher proposal: Grain-128, IEEE International Symposium on Information Theory (ISIT 2006)"
    locator: the 128-bit key version with a 96-bit IV and quadratic NFSR feedback
  - paper: "Martin Ågren, Martin Hell, Thomas Johansson and Willi Meier, Grain-128a: a new version of Grain-128 with optional authentication, International Journal of Wireless and Mobile Computing 5(1), 2011, pp. 48-59"
    locator: the higher-degree feedback and the accumulator-based authentication
  - paper: "Itai Dinur, Tim Güneysu, Christof Paar, Adi Shamir and Ralf Zimmermann, An experimentally verified attack on full Grain-128 using dedicated reconfigurable hardware, ASIACRYPT 2011, LNCS 7073, pp. 327-343"
    locator: the dynamic cube attack that breaks full Grain-128
---

Grain is a family of [stream ciphers](/stream-cipher/) by Martin Hell, Thomas Johansson and Willi Meier, made for very small hardware. Each member joins a linear feedback shift register ([LFSR](/lfsr/)) and a nonlinear feedback shift register (NFSR) of the same length, and a nonlinear filter makes one output bit per clock. Grain v1, with an 80-bit key, is in the eSTREAM hardware portfolio. This page implements the newest member, **Grain-128AEADv2**. It takes a 128-bit key and a 96-bit nonce, encrypts the message, authenticates the message and the associated data with a 64-bit tag, and was one of the ten finalists of the NIST lightweight cryptography process.

## In plain words

Grain has two rows of 128 bits. The first row (the LFSR) changes in a simple, linear way, which gives a very long period. The second row (the NFSR) changes in a nonlinear way, and the first row feeds into it at each step. A small function reads a few bits of both rows and makes one output bit. At the start, the key goes into the second row and the nonce into the first, and the cipher runs 512 steps to mix them. After that, the output bits take turns: one bit encrypts a message bit, and the next bit goes into a 64-bit register that makes the tag. Each message bit that is 1 adds that register into a tag accumulator, so any change to the message changes the tag.

## The problem

The input is a key $K$ of 128 bits, a nonce $N$ of 96 bits, associated data $A$ and a message $P$. The output is a ciphertext $C$ of the same length as $P$ and a 64-bit tag $T$. Decryption takes $(K, N, A, C, T)$ and returns $P$, or rejects if the tag is wrong. A nonce must not repeat under one key, and at most $2^{80}$ keystream bits may be made for one (key, nonce) pair.

In the notation of this area, $K$ is the key, $A$ an adversary and $\mathrm{Adv}$ its advantage. The goals are confidentiality (no efficient $A$ tells $C$ apart from random bits) and integrity (no efficient $A$ makes a new valid $(N, A, C, T)$ with a probability much above $2^{-64}$ per attempt), see [authenticated encryption](/authenticated-encryption/).

## The algorithm

The LFSR state is $s_0 \ldots s_{127}$ and the NFSR state is $b_0 \ldots b_{127}$. One clock outputs a pre-output bit $y$ and shifts both registers by one place: $s_i \leftarrow s_{i+1}$, $b_i \leftarrow b_{i+1}$, and new bits enter at $s_{127}$ and $b_{127}$. The functions are:

- $L(S) = s_0 + s_7 + s_{38} + s_{70} + s_{81} + s_{96}$, the LFSR feedback (a primitive polynomial of degree 128).
- $F(B) = b_0 + b_{26} + b_{56} + b_{91} + b_{96} + b_3 b_{67} + b_{11} b_{13} + b_{17} b_{18} + b_{27} b_{59} + b_{40} b_{48} + b_{61} b_{65} + b_{68} b_{84} + b_{22} b_{24} b_{25} + b_{70} b_{78} b_{82} + b_{88} b_{92} b_{93} b_{95}$, the NFSR feedback.
- $h = b_{12} s_8 + s_{13} s_{20} + b_{95} s_{42} + s_{60} s_{79} + b_{12} b_{95} s_{94}$, and $y = h + s_{93} + b_2 + b_{15} + b_{36} + b_{45} + b_{64} + b_{73} + b_{89}$.

A normal clock sets $s_{127} \leftarrow L(S)$ and $b_{127} \leftarrow s_0 + F(B)$, with $S$ and $B$ taken before the shift. All sums are XOR and all products are AND.

```pseudo id=main
GRAIN-128AEADv2-ENCRYPT(K, N, A, P)
L1  B ← K;  S ← N ‖ 1^31 ‖ 0                     ▷ k_0..k_127 into b, n_0..n_95 into s
L2  repeat 320 times: clock with y fed into s_127 and b_127
L3  for t ← 320 to 383: clock with y + k_(t−256) into s_127 and y + k_(t−320) into b_127
L4  for j ← 0 to 63: clock, a_j ← y                ▷ accumulator
L5  for j ← 0 to 63: clock, r_j ← y                ▷ shift register
L6  m ← ENCODE(|A|) ‖ A ‖ P;  M ← bit length of ENCODE(|A|) ‖ A
L7  for i ← 0 to |m| − 1 do
L8      z ← clock;  z′ ← clock                     ▷ even bits encrypt, odd bits authenticate
L9      if i ≥ M then output c_(i−M) ← m_i + z
L10     if m_i = 1 then A_acc ← A_acc + R
L11     R ← (r_1, ..., r_63, z′)
L12 T ← A_acc + R                                  ▷ the padding bit m_|m| = 1
L13 return (C, T)                                  ▷ decryption compares T in constant pattern
```

Lines L1 to L5 are the 512 initialization clocks. Lines L1 and L2 load the key into the NFSR and the nonce into the LFSR, fill the last 32 LFSR bits with 31 ones and one zero, and then clock 320 times with the output $y$ fed back into both registers. Line L3 clocks 64 more times and shifts the key in again, $k_0 \ldots k_{63}$ into the NFSR and $k_{64} \ldots k_{127}$ into the LFSR, so that a known state after initialization does not give the key at once. Lines L4 and L5 fill the 64-bit accumulator and the 64-bit register with the next 128 output bits.

Line L6 builds the bit string that the mode processes. $\mathrm{ENCODE}(|A|)$ is a DER-style length: one byte if $A$ has fewer than 128 bytes, otherwise a byte $\mathtt{0x80} + \ell$ followed by the length in $\ell$ big-endian bytes. Each byte is read least significant bit first. The associated data bits ($i < M$) are authenticated but not encrypted: this is the AEAD mask $d_i = 0$ of the specification. Each bit costs two clocks (line L8). The even output bit encrypts it (line L9), and the odd output bit enters the register (line L11) after the accumulator absorbed the register for a message bit 1 (line L10). Line L12 adds the register once more for the padding bit $1$, and the 64 accumulator bits form the tag. Decryption runs the same lines, recovers $m_i = c_i + z$ before line L10, and compares the tag in time that does not depend on where it differs.

The code on this page is for study only. It is not constant time as Python runs it, and it must not protect real data. For real use, take a vetted AEAD such as ChaCha20-Poly1305 or AES-GCM from libsodium, OpenSSL or a FIPS 140 validated module.

## Example

Take the second test vector of the specification: $K$ = 000102...0f, $N$ = 000102...0b, $A$ = 0001020304050607 and $P$ = 0001020304050607. Each hex string lists the bytes in order, and each byte is read least significant bit first.

| stage | NFSR $B$ | LFSR $S$ | accumulator | register |
|---|---|---|---|---|
| after line L1 | 000102030405060708090a0b0c0d0e0f | 000102030405060708090a0bffffff7f | | |
| after line L5 | b3c2e1b1eec1f08c2d6eae957f6af9d0 | 0e1f950d45e05087c4cd63fd00eab310 | c77202737ae7c7ee | 33126dd7a21b9073 |

The last LFSR byte after loading is 7f: bits $s_{120} \ldots s_{126}$ are 1 and $s_{127}$ is 0, as line L1 says. Line L6 gives $\mathrm{ENCODE}(8)$ = the byte 08, so $M = 8 \cdot 9 = 72$ bits are authenticated only, and the 64 message bits follow. The result is $C$ = 96d1bda7ae11f0ba and $T$ = 22b0c12039a20e28, as in Section 7. For the first test vector (zero key, zero nonce, empty $A$ and $P$), $\mathrm{ENCODE}(0)$ is the byte 00, the mode processes 8 zero bits, and $T$ = 7137d5998c2de4a5.

In the first clocks of the first vector, $S$ has ones only at $s_{96} \ldots s_{126}$, so $L(S) = s_{96} = 1$ and $y = 0$ for clocks 0, 1 and 2. At clock 3 the first one reaches $s_{93}$, and $y = 1$ from then on for some clocks, so the new LFSR bit $L(S) + y$ becomes 0 and the new NFSR bit becomes 1. The key and nonce spread through both registers in this way.

## Correctness

Encryption and decryption run the same 512 initialization clocks, and line L8 does not depend on the data, so both sides make the same $z$ and $z'$ bits. Decryption gets $c_i + z = m_i + z + z = m_i$ at line L9. Then line L10 sees the same $m_i$ on both sides, so the accumulator and the register evolve in the same way, and the tag of line L12 is the same. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- Initialization is 512 clocks for each (key, nonce). Each bit of $\mathrm{ENCODE}(|A|) \| A \| P$ costs 2 clocks, so $n$ bits cost $\Theta(n + 512)$ clocks.
- One clock is a fixed number of ANDs and XORs. In hardware the designers make it up to 32 times parallel, because the highest tap that the functions read is $b_{96}$ and $s_{96}$, which leaves 31 cells that no tap reads before their bits are needed.
- The state is 256 bits for the registers and 128 bits for the accumulator and the register, 384 bits in total.

## Properties

- **LFSR plus NFSR.** After initialization the LFSR runs alone, and from a nonzero state it has period $2^{128} - 1$ because $f(x) = 1 + x^{32} + x^{47} + x^{58} + x^{90} + x^{121} + x^{128}$ is primitive. The NFSR and the filter $h$ add nonlinearity, so the linear attacks on [LFSR](/lfsr/) keystreams do not apply directly.
- **Authentication by a linear accumulator.** The tag is $\sum_i m_i R_i$ plus a final register value, a linear function of the message with keystream-dependent coefficients. It is a form of a universal hash that the keystream masks. The tag is 64 bits, so a forgery succeeds with probability about $2^{-64}$ per attempt.
- **Bit-level associated data.** The mask $d$ can mark any bit as associated data. Section 2.5 of the specification warns that, with variable-length associated data, a bit can move from the message to the associated data and keep the same tag. In the byte API, line L6 puts the length of $A$ into the authenticated string, so such a change also changes the tag.
- **Key re-introduction.** Line L3 means that a known state after initialization does not give the key by running the cipher back. This was the change from Grain-128AEAD to v2, after the analysis of Chang and Turan.

## Variants and improvements

- **Grain v0 and v1.** The first eSTREAM submission (2005) had an 80-bit LFSR and an 80-bit NFSR. Early attacks showed that its filter was too weak, and Grain v1 changed the functions. It has an 80-bit key, a 64-bit IV and 160 initialization clocks, and it was chosen for eSTREAM profile 2 in 2008.
- **Grain-128.** The 2006 version with 128-bit registers, a 128-bit key and a 96-bit IV. Its NFSR feedback has degree 2. Dynamic cube attacks broke it: Dinur, Güneysu, Paar, Shamir and Zimmermann (ASIACRYPT 2011) recovered keys of the full cipher, and it should not be used.
- **Grain-128a.** The 2011 version raised the degree of $F$ to 4, as on this page, and added an optional 32-bit authentication mode.
- **Grain-128AEAD and v2.** The NIST versions dropped the encryption-only mode, made the tag 64 bits, limited the keystream to $2^{80}$ bits, and (in v2) added line L3.

## When to use it

Use Grain-128AEADv2 for a protocol that already specifies it, or in very small hardware where its gate count matters and an authenticated stream cipher is the right shape. NIST chose [Ascon](/ascon/) for its lightweight standard, SP 800-232, so new designs that want a standard should use Ascon-AEAD128. See [lightweight cryptography](/lightweight-cryptography/). Do not use Grain-128 or Grain v0.

## Pitfalls

- **Nonce reuse.** Two messages under one (key, nonce) pair share the keystream, which leaks $P \oplus P'$ and also the tag mask, so forgeries become easy.
- **Bit order.** The vectors read each byte least significant bit first. A byte read most significant bit first gives a valid-looking but different cipher.
- **The padding.** The specification writes the padding as the byte 0x80 in the NIST API. The vectors match a single padding bit 1 that adds the register once (line L12). Do not clock seven extra zero bits.
- **Releasing plaintext before the tag check.** Decryption must compare the tag before it returns any plaintext.
- **Mixing up versions.** Grain-128a, Grain-128AEAD and Grain-128AEADv2 have different initialization, so their vectors differ.

## Implementations

## History

Hell, Johansson and Meier submitted Grain to eSTREAM in 2005. Analysis in 2005 and 2006 showed weaknesses in its filter, and the modified Grain v1 joined the eSTREAM hardware portfolio in 2008. Grain-128 followed in 2006, with Maximov as a co-author, and Grain-128a in 2011 with Ågren. The authors entered Grain-128AEAD in the NIST lightweight cryptography process in 2019. It became one of the ten finalists in 2021, and the authors updated it to Grain-128AEADv2 for the final round. NIST selected Ascon in February 2023.

## References
