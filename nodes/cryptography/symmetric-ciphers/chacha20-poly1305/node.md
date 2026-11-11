---
tag: 5G1J5X
kind: algorithm
slug: chacha20-poly1305
name: ChaCha20-Poly1305
area: cryptography/symmetric-ciphers
level: advanced
summary: The AEAD of RFC 8439. ChaCha20 block 0 gives a one-time Poly1305 key, blocks 1 and up encrypt, and Poly1305 tags the padded AAD, ciphertext and both lengths.
solves: [symmetric-encryption]
model: word-ram
complexity:
  vars: {n: the plaintext length in bytes, a: the associated data length in bytes}
  time: {worst: Θ(n + a), average: Θ(n + a), best: Θ(n + a)}
  space: {extra: Θ(1)}
properties: {deterministic: true}
history:
  year: 2015
  people: [Daniel J. Bernstein, Adam Langley, Yoav Nir]
  note: Bernstein designed Poly1305 (2005) and ChaCha (2008). Langley proposed the pair for TLS in 2013. Nir and Langley fixed the AEAD in RFC 7539 (2015), replaced by RFC 8439 (2018).
prereqs: [chacha20, poly1305, authenticated-encryption]
see_also: [gcm-mode, ocb-mode, eax-mode, nonce, stream-cipher, universal-hash-family, timing-attack, ccm-decryption-check]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc8439"
    title: Yoav Nir and Adam Langley, RFC 8439, ChaCha20 and Poly1305 for IETF Protocols, June 2018
    locator: Section 2.1.1, 2.3.2, 2.4.2, 2.5.2 and 2.6.2 (test vectors of the parts), Section 2.8 (the AEAD construction and its parameters), Section 2.8.1 (pseudocode), Section 2.8.2 (example and test vector), Section 4 (security considerations) and Appendix A.5 (decryption test vector)
  - url: "https://eprint.iacr.org/2014/613"
    title: Gordon Procter, A Security Analysis of the Composition of ChaCha20 and Poly1305, Cryptology ePrint Archive, Report 2014/613, August 2014
    locator: the proof that the composition is a secure AEAD if the ChaCha20 block function is a PRF, with a forgery term from the Poly1305 bound
  - url: "https://www.rfc-editor.org/rfc/rfc7539"
    title: Yoav Nir and Adam Langley, RFC 7539, ChaCha20 and Poly1305 for IETF Protocols, May 2015
    locator: Section 2.8, the first RFC text of the AEAD, obsoleted by RFC 8439
  - url: "https://datatracker.ietf.org/doc/html/draft-irtf-cfrg-xchacha-03"
    title: Scott Arciszewski, XChaCha, eXtended-nonce ChaCha and AEAD_XChaCha20_Poly1305, Internet-Draft draft-irtf-cfrg-xchacha-03, January 2020 (expired, not an RFC)
    locator: Section 2.2 (HChaCha20), Section 2.2.1 (HChaCha20 test vector), Section 2.3 (XChaCha20) and Appendix A.3.1 (AEAD_XChaCha20_Poly1305 test vector)
  - url: "https://cr.yp.to/chacha/chacha-20080128.pdf"
    title: Daniel J. Bernstein, ChaCha, a variant of Salsa20, January 2008
    locator: the quarter round and the column and diagonal rounds
  - paper: "Daniel J. Bernstein, The Poly1305-AES message-authentication code, FSE 2005, LNCS 3557, pages 32 to 49"
    locator: Theorem 3.3, the bound 8⌈L/16⌉/2^106 on the forgery probability of each try
  - paper: "Julia Len, Paul Grubbs and Thomas Ristenpart, Partitioning Oracle Attacks, USENIX Security 2021"
    locator: one ciphertext that decrypts under many keys, for ChaCha20-Poly1305 and AES-GCM, because neither commits to the key
---

ChaCha20-Poly1305 is the authenticated encryption with associated data (AEAD) of RFC 8439, Section 2.8. It takes a 256-bit key $K$, a 96-bit nonce $N$, associated data $A$ and a plaintext $P$, and it returns a ciphertext $C$ of the same length as $P$ and a 16-byte tag $T$. It uses the [ChaCha20](/chacha20/) block function three ways. Block 0 of the key stream gives a fresh 32-byte key for the one-time MAC [Poly1305](/poly1305/). Blocks 1, 2, … encrypt $P$ as a [stream cipher](/stream-cipher/). Poly1305 then tags a string made from $A$ and $C$, each padded to 16 bytes, and the two lengths. The receiver checks the tag on the ciphertext before it decrypts anything. TLS 1.3, QUIC, WireGuard, OpenSSH (in a different variant) and many other systems use it, often where AES has no hardware support.

**Notation.** $\mathrm{CB}(K, j, N)$ is the 64-byte ChaCha20 block for key $K$, block counter $j$ and nonce $N$. $\mathrm{pad16}(X)$ is the 0 to 15 zero bytes that bring $|X|$ to a multiple of 16. $\mathrm{le64}(x)$ is $x$ as 8 bytes, least significant byte first. $|X|$ is a length in bytes.

## In plain words

ChaCha20 turns a key, a counter and a nonce into 64 bytes that look random. ChaCha20-Poly1305 asks it for many such blocks under one nonce. It keeps the first half of block 0 as a secret key for Poly1305, a fingerprint function that is safe for one message only. It XORs the plaintext with blocks 1, 2, 3 and so on to hide it. Then it fingerprints everything the receiver must be able to trust: the associated data, the ciphertext, and their lengths. Because each nonce gives a new fingerprint key, each fingerprint key is used once, which is exactly what Poly1305 needs. If a nonce is used twice, both parts fail together: the attacker sees the XOR of the two plaintexts, and can solve for the fingerprint key and then forge.

## The problem

Input: a key $K$ of 32 bytes, a nonce $N$ of 12 bytes that is never used twice with the same key, associated data $A$ with $|A| < 2^{64}$, and a plaintext $P$ with $|P| \le 274{,}877{,}906{,}880$ bytes (that is, $(2^{32} - 1) \cdot 64$). Output: $(C, T)$, such that the receiver who knows $K$ and gets $(N, A, C, T)$ recovers $P$, while an attacker learns nothing about $P$ beyond its length and cannot make any new $(N, A, C, T)$ that the receiver accepts. In the language of [authenticated encryption](/authenticated-encryption/), the goal is IND-CPA privacy plus integrity of ciphertexts (INT-CTXT) against a nonce-respecting adversary, which together give IND-CCA security.

## The algorithm

```pseudo id=main
CHACHA20-BLOCK(K, j, N)                     ▷ RFC 8439, Section 2.3
L1  s ← "expand 32-byte k" ‖ K ‖ j ‖ N         ▷ sixteen 32-bit words, read little-endian
L2  x ← s after 10 double rounds              ▷ column round, then diagonal round
L3  x ← x + s                                 ▷ word by word, modulo 2^32
L4  return x as 64 bytes, little-endian

AEAD-ENCRYPT(K, N, A, P)                    ▷ Section 2.8
L5  otk ← first 32 bytes of CHACHA20-BLOCK(K, 0, N)
L6  C ← P ⊕ (CHACHA20-BLOCK(K, 1, N) ‖ CHACHA20-BLOCK(K, 2, N) ‖ …)
L7  M ← A ‖ pad16(A) ‖ C ‖ pad16(C) ‖ le64(|A|) ‖ le64(|C|)
L8  T ← POLY1305(otk, M)
L9  return (C, T)

AEAD-DECRYPT(K, N, A, C, T)
L10 otk ← first 32 bytes of CHACHA20-BLOCK(K, 0, N)
L11 T' ← POLY1305(otk, A ‖ pad16(A) ‖ C ‖ pad16(C) ‖ le64(|A|) ‖ le64(|C|))
L12 if T' ≠ T then return FAIL                ▷ read every byte; no early exit
L13 return C ⊕ (CHACHA20-BLOCK(K, 1, N) ‖ CHACHA20-BLOCK(K, 2, N) ‖ …)
```

The quarter round of L2 on the words $(a, b, c, d)$ is: $a \mathrel{+}= b$; $d \mathrel{\oplus}= a$; $d \lll 16$; $c \mathrel{+}= d$; $b \mathrel{\oplus}= c$; $b \lll 12$; then the same with the rotations 8 and 7. A column round applies it to the columns $(0, 4, 8, 12)$ to $(3, 7, 11, 15)$, and a diagonal round to $(0, 5, 10, 15)$, $(1, 6, 11, 12)$, $(2, 7, 8, 13)$ and $(3, 4, 9, 14)$. POLY1305 at L8 clamps the first 16 bytes of otk to $r$, reads the other 16 bytes as $s$, and computes $\bigl(\sum_i c_i r^{q+1-i} \bmod (2^{130} - 5) + s\bigr) \bmod 2^{128}$ over the 16-byte blocks $c_i$ of $M$, each with a 1 byte appended (see the [Poly1305](/poly1305/) page). Because $M$ at L7 is padded, every block of $M$ is full.

**About the code.** The Python code of this page is for study only. It is not constant time: Python big integers in Poly1305 take time that depends on their values, and Python gives no timing guarantees at all. Do not use it to protect real data. Use `crypto_aead_chacha20poly1305_ietf_encrypt` of libsodium, or the ChaCha20-Poly1305 AEAD of a FIPS 140 validated module that offers it. The code has its own ChaCha20 block function, tested against RFC 8439, Section 2.3.2, and its own Poly1305. It also has XChaCha20-Poly1305 from the expired draft draft-irtf-cfrg-xchacha-03, which is not a standard.

## Example

RFC 8439, Section 2.8.2. The key is the 32 bytes `80 81 82 … 9f`. The nonce is the 32-bit constant `07000000` followed by the 8-byte IV `4041424344454647`. $A$ = `50515253c0c1c2c3c4c5c6c7` (12 bytes) and $P$ is the 114-byte text "Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, sunscreen would be it."

| step | value |
|---|---|
| L1 | the words `61707865 3320646e 79622d32 6b206574`, `83828180 … 9f9e9d9c`, counter `00000000`, nonce `00000007 43424140 47464544` |
| L5 | otk = `7bac2b252db447af09b67a55a4e95584` `0ae1d6731075d9eb2a9375783ed553ff`; after the clamp $r$ = `0x0455e9a4057ab6080f47b42c052bac7b` |
| L6 | block 1 starts `9f7be95d01fd40ba15e28ffb36810aae`; so $C$ starts `4c616469…` ⊕ `9f7be95d…` = `d31a8d34648e60db7b86afbc53ef7ec2` and ends `…61 16` |
| L7 | $M$ has 160 bytes: $A$, 4 zero bytes, the 114 bytes of $C$, 14 zero bytes, `0c00000000000000`, `7200000000000000` |
| L8 | $T$ = `1ae10b594f09e26a7e902ecbd0600691` |
| L10 to L13 | the same otk and the same $T'$; $T' = T$, so the receiver XORs the key stream again and gets $P$ |

If any bit of $C$, $T$, $A$ or $N$ changes, L12 returns FAIL; the tests try every bit of $C$ and $T$.

## Correctness

Three claims hold, with $\mathrm{Enc}$ and $\mathrm{Dec}$ the two procedures above. (1) Completeness: $\mathrm{Dec}(K, N, A, \mathrm{Enc}(K, N, A, P)) = P$, because both sides compute the same otk and the same $M$, and the XOR with the same key stream is its own inverse. (2) The encoding at L7 is injective: from $M$ one reads $|A|$ and $|C|$ in the last 16 bytes, and then $A$ and $C$ at known offsets. So no two different pairs $(A, C)$ give the same Poly1305 input; without the lengths, $(A, C) = (X, \varepsilon)$ and $(\varepsilon, X)$ would collide when $|X|$ is a multiple of 16. (3) Canonical verification and no release: $\mathrm{Dec}$ accepts $(N, A, C, T)$ only if $(C, T) = \mathrm{Enc}(K, N, A, P)$ for the unique $P$ it returns, and on failure it returns the constant FAIL, computed before any plaintext exists. The full proof is below.

## Complexity

ChaCha20 runs one block for every 64 bytes of $P$, plus block 0 for the key. Poly1305 does one multiplication modulo $2^{130} - 5$ for each 16-byte block of $M$, and $M$ has $\lceil a/16 \rceil + \lceil n/16 \rceil + 1$ blocks. So both encryption and decryption take $\Theta(n + a)$ time. A rejected ciphertext still costs $\Theta(n + a)$ for the MAC, but no key stream beyond block 0. The extra space is $\Theta(1)$: encryption can stream, and decryption can make two passes over $C$, first the MAC and then the XOR, without a plaintext buffer. On a CPU without AES instructions, a vectorized ChaCha20 is several times faster than a table-free, constant-time AES, which is the main reason for its use on phones and small devices (RFC 8439, Appendix B, quotes speeds measured by Langley in 2014).

## Properties

- **Deterministic.** The same $(K, N, A, P)$ always gives the same $(C, T)$. Security comes from the nonce, not from randomness.
- **Security model.** Procter (ePrint 2014/613) proves IND-CPA privacy and INT-CTXT integrity for a nonce-respecting adversary, assuming the ChaCha20 block function, keyed by $K$ and indexed by $(j, N)$, is a pseudorandom function. The reduction is tight: the bound is the PRF advantage of an adversary that makes about as many block calls as the attack, plus a forgery term that grows linearly with the number of verification queries $q_v$ and the length $\ell$ in bytes, about $q_v \cdot 8\lceil \ell/16 \rceil / 2^{106}$. There is no birthday term from a 128-bit block, unlike GCM.
- **Forgery probability.** RFC 8439, Section 4, states that Poly1305 rejects a forgery for a message of $16m$ bytes with probability at least $1 - m/2^{102}$, by the Poly1305 bound of Bernstein. A 16-byte tag must not be cut short (RFC 8439, Section 4).
- **Encrypt-then-MAC.** The tag covers the ciphertext, so a receiver can check it before it decrypts, and never handles unverified plaintext.
- **Online for the sender.** Encryption reads $P$ once and can output $C$ as it goes. The receiver must wait for the tag before it releases any plaintext.
- **Not nonce-misuse resistant.** A repeated nonce reveals $P_1 \oplus P_2$ and the one-time key $(r, s)$; see the pitfalls.
- **Not key-committing.** One $(N, A, C, T)$ can be valid under two different keys.

## Variants and improvements

- **The original TLS draft (2013).** Langley's first version for TLS and the first Chrome code used a 64-bit nonce and a MAC input without the padding to 16 bytes. RFC 7539 changed both. The two forms do not interoperate.
- **RFC 7539 to RFC 8439.** RFC 8439 (2018) fixed errata and replaced RFC 7539. The algorithm did not change.
- **XChaCha20-Poly1305.** A 24-byte nonce, long enough to pick at random. HChaCha20, the 20 rounds without the final addition and with output words 0 to 3 and 12 to 15, maps $K$ and the first 16 nonce bytes to a subkey. The AEAD of this page then runs with that subkey and the nonce `00000000` followed by the last 8 nonce bytes. It is in draft-irtf-cfrg-xchacha-03, an expired Internet-Draft, not an RFC, but libsodium and others ship it. The code and tests of this page include it.
- **The OpenSSH variant.** `chacha20-poly1305@openssh.com` uses two 256-bit keys, one to encrypt the packet length and one for the payload, a 64-bit nonce, and a MAC over the encrypted length and payload. It is a different construction with the same parts.
- **ChaCha12 and ChaCha8.** Fewer rounds give more speed. Some disk and random number designs use them, but the AEAD of RFC 8439 fixes 20 rounds.
- **Key-committing variants.** Adding a commitment to the key, for example a hash of the key in the ciphertext, or a padding check after decryption, stops the multi-key attacks. These are additions on top of the RFC, not part of it.

## When to use it

Use ChaCha20-Poly1305 when you need an AEAD and the platform has no AES hardware, or when you want one code path that is easy to make constant time on every CPU: it has only additions, XORs and rotations, with no table lookups. It is a standard cipher suite in TLS 1.3 and in QUIC, and the only AEAD of WireGuard. Use a counter or a sequence number as the nonce, or XChaCha20-Poly1305 with random nonces. With the 96-bit nonce, do not pick nonces at random for many messages under one key: by the birthday bound, about $2^{48}$ random nonces give a likely repeat, and a much smaller number gives an unsafe risk. Do not use it where nonces can repeat (use a misuse-resistant mode such as AES-GCM-SIV there), or where one ciphertext must bind one key (add a key commitment).

## Pitfalls

- **Nonce reuse.** Two messages under one $(K, N)$ share the key stream and the Poly1305 key. The XOR of the ciphertexts is the XOR of the plaintexts. Worse, $T_1 - T_2$ is a known polynomial in $r$ modulo $2^{130} - 5$, up to a small carry from the reduction modulo $2^{128}$. The test `test_nonce_reuse_recovers_the_poly1305_key_and_forges` uses two one-block messages: then $T_1 - T_2 \equiv (c_1 - c_2) r^2$, it takes the square root modulo $p = 2^{130} - 5$ (since $p \equiv 3 \pmod 4$, a root is $x^{(p+1)/4}$), keeps the root that passes the clamp, gets $s$, and forges a tag for a new message and new AAD under that nonce.
- **Random 96-bit nonces.** Safe for a few messages, not for billions. Count the messages per key, or use XChaCha20-Poly1305.
- **Counter overflow.** The 32-bit block counter limits one message to about 256 GB. Code must refuse a longer plaintext instead of letting the counter wrap to block 0, which is the Poly1305 key block.
- **Releasing plaintext before the tag check.** A streaming decryptor that outputs plaintext before L12 is a decryption oracle, as on the [CCM decryption-verification](/ccm-decryption-check/) page. The MAC is over the ciphertext, so check first.
- **Early-exit tag comparison.** RFC 8439, Section 4, requires a constant-time comparison. An early exit leaks the length of the correct prefix through a [timing attack](/timing-attack/).
- **No key commitment.** Len, Grubbs and Ristenpart (USENIX Security 2021) built ciphertexts that decrypt under many keys at once, and used them to guess passwords with few queries. The test `test_not_key_committing_one_ciphertext_opens_under_two_keys` builds one ciphertext that opens under two chosen keys.
- **Constant-time Poly1305.** The arithmetic modulo $2^{130} - 5$ must use fixed-size limbs and no data-dependent branches. The Python of this page does not, which is why it is for study only.

## Implementations

The Python code gives `chacha20_block` (L1 to L4), `aead_encrypt` (L5 to L9) and `aead_decrypt` (L10 to L13), with the helpers `quarter_round`, `chacha20_encrypt`, `poly1305_mac`, `mac_data`, `poly1305_key_gen` and `tags_equal`, and the draft functions `hchacha20`, `xchacha20_poly1305_encrypt` and `xchacha20_poly1305_decrypt`. The tests check, against RFC 8439, the quarter round (Section 2.1.1), the block function (Section 2.3.2), ChaCha20 encryption (Section 2.4.2), Poly1305 (Section 2.5.2), the key generation (Section 2.6.2), the AEAD with its one-time key and MAC input (Section 2.8.2), and the decryption vector of Appendix A.5. They check HChaCha20 (Section 2.2.1) and XChaCha20-Poly1305 (Appendix A.3.1) of the draft. They check round trips for many lengths, that every changed bit of $C$ and $T$ and a changed AAD or nonce give FAIL, and that the length block separates $(X, \varepsilon)$ from $(\varepsilon, X)$. Three attack tests run against this code: key recovery and forgery after a nonce reuse, a check that fresh nonces give unrelated one-time keys, and one ciphertext that is valid under two keys.

## History

Daniel J. Bernstein published Poly1305 at FSE 2005, as Poly1305-AES, and ChaCha, a variant of his Salsa20 with more diffusion per round, in 2008. In 2013 Adam Langley proposed ChaCha20 with Poly1305 as a TLS cipher suite, and Google deployed it in Chrome and its servers, mainly for phones without AES hardware. Gordon Procter published a security analysis of the composition in August 2014. Yoav Nir and Adam Langley wrote RFC 7539 in May 2015 with the 96-bit nonce, the counter that starts at 1 and the padded MAC input. RFC 7905 (2016) added the TLS 1.2 cipher suites, TLS 1.3 (RFC 8446, 2018) made it one of its cipher suites, and RFC 8439 (June 2018) replaced RFC 7539. Scott Arciszewski proposed XChaCha in a CFRG draft whose last version, draft 03, expired in 2020 without becoming an RFC.

## References

- Yoav Nir and Adam Langley, RFC 8439, Sections 2.1 to 2.8, Section 4 and Appendix A.5, 2018.
- Gordon Procter, A Security Analysis of the Composition of ChaCha20 and Poly1305, ePrint 2014/613.
- Yoav Nir and Adam Langley, RFC 7539, 2015.
- Scott Arciszewski, draft-irtf-cfrg-xchacha-03, 2020 (expired draft).
- Daniel J. Bernstein, ChaCha, a variant of Salsa20, 2008.
- Daniel J. Bernstein, The Poly1305-AES message-authentication code, FSE 2005.
- Julia Len, Paul Grubbs and Thomas Ristenpart, Partitioning Oracle Attacks, USENIX Security 2021.
