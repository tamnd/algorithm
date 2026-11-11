---
tag: F7H5VG
kind: algorithm
slug: ascon
name: Ascon
area: cryptography/symmetric-ciphers
level: advanced
summary: A family of lightweight AEAD, hash and XOF schemes on one 320-bit permutation, by Dobraunig, Eichlseder, Mendel and Schläffer. NIST chose it in 2023 and published SP 800-232 in 2025.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {m: the number of bytes of associated data and plaintext}
  time: {worst: Θ(m), average: Θ(m), best: Θ(m)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2014
  people: [Christoph Dobraunig, Maria Eichlseder, Florian Mendel, Martin Schläffer]
  note: Ascon was submitted to CAESAR in 2014, chosen as the first choice for lightweight use in the CAESAR portfolio in 2019, selected by NIST in February 2023, and standardized in NIST SP 800-232 in August 2025.
prereqs: [authenticated-encryption, sponge-construction]
see_also: [lightweight-cryptography, sponge-construction, keccak, authenticated-encryption, chacha20-poly1305, present, nonce, s-box]
sources:
  - url: "https://doi.org/10.6028/NIST.SP.800-232"
    title: "Meltem Sönmez Turan, Kerry A. McKay, Donghoon Chang, Jinkeon Kang and John Kelsey, NIST SP 800-232, Ascon-Based Lightweight Cryptography Standards for Constrained Devices: Authenticated Encryption, Hash, and Extendable Output Functions, August 2025"
    locator: Section 1 (the list of changes from the Ascon v1.2 submission), Section 3 (the permutation, Tables 5 and 6), Section 4 (Ascon-AEAD128, Algorithms 3 and 4, and the security strengths of Section 4.4) and Appendix A (implementation notes on the byte order)
  - paper: "Christoph Dobraunig, Maria Eichlseder, Florian Mendel and Martin Schläffer, Ascon v1.2: Lightweight authenticated encryption and hashing, Journal of Cryptology 34(3), 2021, article 33"
    locator: the design of the permutation and its S-box and linear layer, the monkeyDuplex mode with keyed initialization and finalization, and the security analysis
  - url: "https://github.com/ascon/ascon-c"
    title: The Ascon designers' reference C implementations, ascon-c, known-answer test file LWC_AEAD_KAT_128_128.txt for Ascon-AEAD128
    locator: the entries with Count 1, 2, 3, 34, 35, 545 and 765 (key 000102...0F, nonce 101112...1F)
---

Ascon is a family of lightweight symmetric schemes built on one 320-bit permutation, designed by Christoph Dobraunig, Maria Eichlseder, Florian Mendel and Martin Schläffer. It gives [authenticated encryption](/authenticated-encryption/) with associated data (AEAD), a hash function and extendable output functions. The AEAD mode is a keyed duplex [sponge](/sponge-construction/): the state absorbs data 128 bits at a time between calls of the permutation, and the key enters again at the end to protect against state recovery. Ascon was the first choice for lightweight use in the CAESAR portfolio (2019), NIST selected it for [lightweight cryptography](/lightweight-cryptography/) in February 2023, and NIST SP 800-232 (August 2025) standardizes Ascon-AEAD128, Ascon-Hash256, Ascon-XOF128 and Ascon-CXOF128. This page implements exactly Ascon-AEAD128 of SP 800-232.

## In plain words

Ascon keeps a state of 40 bytes. It fills the state with a fixed value, the key and a nonce, and scrambles it many times with a fixed mixing function. Then it XORs the key in again, so an attacker cannot run the mixing backward to reach the key. Next it takes the extra data that must be authenticated but not hidden, 16 bytes at a time: it XORs each piece into the first 16 bytes of the state and scrambles the state again. To encrypt, it XORs each 16 bytes of the message into the first 16 bytes of the state; the result is the ciphertext, and it stays in the state. At the end it XORs the key in once more, scrambles the state, and takes 16 bytes as the tag. The receiver repeats the steps and checks the tag.

## The problem

Given a 128-bit key $K$, a 128-bit nonce $N$ that is never reused under $K$, associated data $A$ and a plaintext $P$, compute a ciphertext $C$ with $|C| = |P|$ and a 128-bit tag $T$, such that $C$ hides $P$ and $(N, A, C, T)$ cannot be forged. The design must be small in hardware, fast on microcontrollers, and share one primitive between encryption and hashing.

## The algorithm

**The permutation.** The state $S = S_0 \| S_1 \| S_2 \| S_3 \| S_4$ is five 64-bit words. Ascon-p[$r$] applies $r$ rounds ($1 \le r \le 16$) of $p = p_L \circ p_S \circ p_C$:
- $p_C$ adds the round constant $c_i = \mathrm{const}_{16 - r + i}$ to $S_2$, with $\mathrm{const}_0, \ldots, \mathrm{const}_{15}$ = 3c, 2d, 1e, 0f, f0, e1, d2, c3, b4, a5, 96, 87, 78, 69, 5a, 4b (SP 800-232 Table 5). So p[12] uses f0 to 4b and p[8] uses b4 to 4b.
- $p_S$ applies a 5-bit S-box to each of the 64 bit slices $(s_{0,j}, \ldots, s_{4,j})$. As a table, with $x_0$ the most significant bit: 4, b, 1f, 14, 1a, 15, 9, 2, 1b, 5, 8, 12, 1d, 3, 6, 1c, 1e, 13, 7, e, 0, d, 11, 18, 10, c, 1, 19, 16, a, f, 17 (Table 6). It is affine-equivalent to the $\chi$ map of [Keccak](/keccak/) and is computed on whole 64-bit words with a few ANDs, NOTs and XORs, as in the code.
- $p_L$ sets $S_i \leftarrow S_i \oplus (S_i \ggg a_i) \oplus (S_i \ggg b_i)$ with $(a_i, b_i)$ = (19, 28), (61, 39), (1, 6), (10, 17), (7, 41).

**Ascon-AEAD128** (SP 800-232, Algorithm 3). The rate is 128 bits ($S_0, S_1$) and the capacity 192 bits. Bytes are loaded into words in little-endian order. $\mathrm{pad}(X)$ appends the byte 01 and then zero bytes up to 16 bytes.

```pseudo id=main
ASCON-P(S, r)
L1  for i ← 16 − r to 15 do
L2      S2 ← S2 ⊕ const_i                          ▷ p_C
L3      S ← S-box on each of the 64 bit slices      ▷ p_S
L4      Sj ← Sj ⊕ (Sj ⋙ aj) ⊕ (Sj ⋙ bj), j = 0..4   ▷ p_L

ASCON-AEAD128-ENCRYPT(K, N, A, P)
L5  S ← IV ‖ K ‖ N                                 ▷ IV = 0x00001000808c0001
L6  S ← ASCON-P(S, 12); S ← S ⊕ (0^192 ‖ K)
L7  if |A| > 0 then for each block Ai of A1 ‖ ... ‖ pad(A_last): S ← ASCON-P(S ⊕ (Ai ‖ 0^192), 8)
L8  S ← S ⊕ (0^319 ‖ 1)                            ▷ domain separation
L9  for each full 128-bit block Pi: S[0..127] ← S[0..127] ⊕ Pi; Ci ← S[0..127]; S ← ASCON-P(S, 8)
L10 S[0..127] ← S[0..127] ⊕ pad(P_last)            ▷ P_last has ℓ < 16 bytes, maybe 0
L11 C_last ← the first ℓ bytes of S[0..127]
L12 S ← ASCON-P(S ⊕ (0^128 ‖ K ‖ 0^64), 12)
L13 T ← S[192..319] ⊕ K
L14 return (C, T)                                  ▷ decryption checks T and returns ⊥ on a mismatch
```

Lines L5 and L6 make a state that depends on $K$ and $N$; the XOR of $K$ after the permutation means that even a full state recovered later cannot be run backward to $K$. Line L7 absorbs $A$ with 8 rounds per block; it is skipped when $A$ is empty. Line L8 flips the last bit of the state, so that $A$ and $P$ cannot be confused. Lines L9 to L11 encrypt: the ciphertext block is the new rate part, which is a duplex sponge. Lines L12 and L13 add the key again before and after the final 12 rounds, which binds the tag to $K$. Decryption runs the same steps but sets the rate to the ciphertext block, and compares the tag. Only the forward permutation is needed, so there is no inverse to implement.

The code on this page is for study only. It is not constant time as Python runs it (and its tag comparison is not constant time), and it must not protect real data. Use a vetted implementation, such as one in a FIPS 140 validated module.

## Example

Key 000102...0f and nonce 101112...1f, the setting of the ascon-c known-answer file. In little-endian words, the initial state of line L5 is

| word | $S_0$ | $S_1$ | $S_2$ | $S_3$ | $S_4$ |
|---|---|---|---|---|---|
| line L5 | 00001000808c0001 | 0706050403020100 | 0f0e0d0c0b0a0908 | 1716151413121110 | 1f1e1d1c1b1a1918 |
| after p[12] | cde34900cdfce2c8 | 948cba141a58c1cb | 1fec9b5dae69b43a | 620599fcd928dbac | 3d3290a90ed3b02f |
| after $\oplus K$ | cde34900cdfce2c8 | 948cba141a58c1cb | 1fec9b5dae69b43a | 65039cf8da2adaac | 323c9da505d9b927 |

The outputs (ciphertext followed by the tag) for some entries of the file:

| Count | $P$ | $A$ | $C \| T$ |
|---|---|---|---|
| 1 | empty | empty | 4f9c278211bec9316bf68f46ee8b2ec6 |
| 2 | empty | 30 | cccb674fe18a09a285d6ab11b35675c0 |
| 34 | 20 | empty | e8 dd576aba1cd3e6fc704de02aedb79588 |
| 545 | 20...2f (16 bytes) | 30...3f (16 bytes) | 6373ebb28be97c9bac090cf399c13ef1 3abfc0d209e8f4844c90814d13f32c59 |

For Count 545, the 16-byte $A$ is a full block, so line L7 absorbs it and then a block that holds only the padding byte. The tests check seven entries of the file, including Count 765 with a 23-byte plaintext.

## Correctness

Decryption reproduces the encryption state: both start from the same $(K, N)$ and process the same $A$. At line L9, encryption sets the rate to $S[0..127] \oplus P_i = C_i$, and decryption computes $P_i = S[0..127] \oplus C_i$ and then sets the rate to $C_i$, the same value. For the last partial block, decryption XORs $\mathrm{pad}(P_{\mathrm{last}})$ into the rate, as encryption does. So after line L11 both states are equal, they compute the same tag, and decryption returns $P$ for a valid $(C, T)$. The steps are a permutation and XORs, so all of this follows by induction over the blocks. The proof is in [proofs/correctness.md](proofs/correctness.md). Security is a different matter: SP 800-232 Section 4.4 claims 128-bit security for confidentiality and integrity in the single-key, nonce-respecting setting, with at most $2^{54}$ bytes of input under one key.

## Complexity

Each 16 bytes of $A$ or $P$ cost one p[8], and initialization and finalization each cost one p[12]. A round is a constant number of 64-bit word operations (a few dozen), so $m$ bytes cost $\Theta(m)$ and the state is $\Theta(1)$: 40 bytes plus the key. The S-box and linear layer have no table lookups, so a constant-time implementation is natural. On 32-bit processors each 64-bit word is split into two 32-bit halves with bit interleaving, as Appendix A of SP 800-232 describes.

## Properties

- **One permutation for everything.** Ascon-AEAD128, Ascon-Hash256, Ascon-XOF128 and Ascon-CXOF128 share Ascon-p, so a device can implement AEAD and hashing with one circuit.
- **Online and single pass.** Ciphertext block $i$ depends only on $K$, $N$, $A$ and the first $i$ plaintext blocks.
- **Inverse-free.** Only the forward permutation is used.
- **Keyed initialization and finalization.** Recovering an inner state does not give the key or allow universal forgery.
- **Not nonce-misuse resistant.** A repeated nonce leaks the XOR of plaintexts, as for each [stream cipher](/stream-cipher/).
- **Security claims.** 128-bit security in the single-key setting with a nonce never repeated; with $u$ keys, $128 - \log_2 u$ bits (SP 800-232 Section 4.4).

## Variants and improvements

- **Ascon v1.2 against SP 800-232.** The CAESAR and NIST submissions defined ASCON-128 (64-bit rate, p[6] between blocks), ASCON-128a (128-bit rate, p[8]) and ASCON-80pq. SP 800-232 specifies only Ascon-AEAD128, which is based on ASCON-128a, and it changes: the initial values (a new format), the byte order (from big-endian to little-endian, for little-endian microcontrollers), the round constants (defined for up to 16 rounds), and adds options for tag truncation and nonce masking. Ascon-AEAD128 outputs therefore differ from ASCON-128a v1.2 outputs, and the v1.2 test vectors do not apply.
- **Hash and XOF.** Ascon-Hash256 (based on ASCON-HASH) gives a 256-bit digest, Ascon-XOF128 an output of any length, and Ascon-CXOF128 adds a customization string.
- **Nonce masking.** An option of SP 800-232 (Section 4.2.2) with a 256-bit key $K_1 \| K_2$: it runs Ascon-AEAD128 with key $K_1$ and nonce $N \oplus K_2$. It keeps 128-bit security in the multi-key setting, but it should not be used where related-key security or context commitment matters.
- **Tag truncation.** Allowed down to 32 bits under conditions; a tag of $\lambda$ bits gives $\lambda$-bit security against forgery.

## When to use it

Use Ascon-AEAD128 for authenticated encryption on constrained devices: microcontrollers, sensors, RFID and smart cards, where AES-GCM is too large or slow, and where you want one primitive for AEAD and hashing. It is a NIST standard, with constant-time implementations that are simple to write. On processors with AES instructions, AES-GCM is often faster; on general CPUs without them, [ChaCha20-Poly1305](/chacha20-poly1305/) is also a good choice. Use a fresh nonce for each message, such as a counter.

## Pitfalls

- **Mixing up versions.** Ascon-128a v1.2 and Ascon-AEAD128 have the same structure but different IVs and byte order. A test vector of one fails on the other. Name the version.
- **Empty associated data.** When $A$ is empty, line L7 is skipped entirely. An implementation that absorbs one padding block for empty $A$ gives other tags.
- **The domain separation bit.** It is the last bit of the state, which in the little-endian word representation is bit 63 of $S_4$.
- **Releasing plaintext before the tag check.** Decryption must not return or use any plaintext until the tag verifies.
- **Nonce reuse.** It breaks confidentiality for the messages that share the nonce and weakens integrity.
- **Comparing tags with early exit.** The comparison of $T$ must be constant time.

## Implementations

## History

Dobraunig, Eichlseder, Mendel and Schläffer submitted Ascon to the CAESAR competition in 2014. In February 2019 the CAESAR final portfolio named Ascon the first choice for lightweight applications. The designers submitted Ascon v1.2 to the NIST lightweight cryptography process, and the Journal of Cryptology published the specification and analysis in 2021. On 7 February 2023 NIST announced the selection of the Ascon family. In August 2025 NIST published SP 800-232, which standardizes Ascon-AEAD128, Ascon-Hash256, Ascon-XOF128 and Ascon-CXOF128, with the changes from v1.2 listed above.

## References
