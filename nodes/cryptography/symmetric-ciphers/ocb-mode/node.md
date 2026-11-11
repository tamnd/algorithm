---
tag: 0FNP6K
kind: technique
slug: ocb-mode
name: Offset codebook mode
aliases:
- OCB
area: cryptography/symmetric-ciphers
level: advanced
summary: "One-pass AEAD of Rogaway and others: each block is enciphered between two copies of a secret offset, and the tag enciphers a checksum of the plaintext. OCB3 is RFC 7253; OCB2 is broken."
prereqs: [ecb-mode, authenticated-encryption, pseudorandom-permutation]
see_also: [gcm-mode, eax-mode, ccm-mode, chacha20-poly1305, xts-mode, cmac, nonce]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc7253"
    title: Ted Krovetz and Phillip Rogaway, RFC 7253, The OCB Authenticated-Encryption Algorithm, May 2014
    locator: Section 2 (double and ntz), Section 4.1 (HASH), Section 4.2 (OCB-ENCRYPT), Section 4.3 (OCB-DECRYPT), Section 5 and 5.1 (security and nonce requirements), Appendix A (sample results)
  - paper: "Phillip Rogaway, Mihir Bellare, John Black and Ted Krovetz, OCB: A block-cipher mode of operation for efficient authenticated encryption, ACM CCS 2001, pages 196 to 205"
    locator: OCB1, its offsets from Gray codes, and the proof of privacy and authenticity
  - paper: "Phillip Rogaway, Efficient instantiations of tweakable blockciphers and refinements to modes OCB and PMAC, ASIACRYPT 2004, LNCS 3329, pages 16 to 31"
    locator: the XE and XEX tweakable block ciphers and OCB2
  - paper: "Ted Krovetz and Phillip Rogaway, The software performance of authenticated-encryption modes, Fast Software Encryption (FSE) 2011, LNCS 6733, pages 306 to 327"
    locator: the definition of OCB3 and its speed compared with CCM and GCM
  - paper: "Akiko Inoue, Tetsu Iwata, Kazuhiko Minematsu and Bertram Poettering, Cryptanalysis of OCB2: attacks on authenticity and confidentiality, CRYPTO 2019, LNCS 11692, pages 3 to 31"
    locator: the minimal forgery on OCB2, universal forgeries and plaintext recovery, and the flaw in the OCB2 proof
  - paper: "Charanjit S. Jutla, Encryption modes with almost free message integrity, EUROCRYPT 2001, LNCS 2045, pages 529 to 544"
    locator: IAPM, the first one-pass authenticated encryption mode with a proof, which OCB builds on
  - url: "https://mailarchive.ietf.org/arch/msg/cfrg/qLTveWOdTJcLn4HP3ev-vrj05Vg/"
    title: Phillip Rogaway, OCB patents are abandoned; freely usable, message to the IRTF CFRG mailing list, February 2021
    locator: the statement that the OCB patents are abandoned and the related IP placed in the public domain
---

OCB (offset codebook) is an [authenticated encryption](/authenticated-encryption/) mode that gets privacy and authenticity in one pass, with about one block cipher call per block of message. Each block is enciphered like [ECB](/ecb-mode/), but between two copies of a secret offset that changes from block to block: $C_i = \Delta_i \oplus E_K(P_i \oplus \Delta_i)$. The tag is the encipherment of the XOR of all plaintext blocks, under one more offset. Rogaway, Bellare, Black and Krovetz published OCB1 at ACM CCS 2001. Rogaway gave OCB2 in 2004, and Krovetz and Rogaway gave OCB3 in 2011, which is the version of RFC 7253 (2014) and the only one to use today. OCB2 was broken in 2018 and 2019: its proof was wrong, and a forgery needs one query. For twenty years OCB was held back by patents; Rogaway abandoned them in 2021.

**Notation.** $E_K$ is a block cipher with 128-bit blocks, and $D_K$ its inverse. $N$ is the nonce of 1 to 120 bits, $A$ the associated data, $P = P_1 \cdots P_m P_*$ the plaintext in full blocks and a possibly empty last part $P_*$. $\mathrm{double}$ is multiplication by $x$ in $\mathrm{GF}(2^{128})$ modulo $x^{128} + x^7 + x^2 + x + 1$, and $\mathrm{ntz}(i)$ is the number of trailing zero bits of $i$. TAGLEN is the tag length in bits.

## In plain words

OCB hides each block of the message by mixing it with a secret mask, enciphering it, and mixing it with the same mask again. The mask is different for each position and for each nonce, so equal blocks do not give equal ciphertext, and blocks cannot be moved. Going from one mask to the next costs only one XOR with a value from a small table. While it encrypts, OCB also XORs all the plaintext blocks together into a checksum. At the end it enciphers the checksum under one more mask to get the tag. A change anywhere in the ciphertext changes some decrypted block in a way the attacker cannot predict, so it changes the checksum, and the tag no longer fits.

## When it applies

- **Speed in software and hardware.** About $m + 2$ block cipher calls for $m$ blocks, all of them parallel, and no field multiplication. Krovetz and Rogaway (FSE 2011) measured OCB3 faster than GCM and CCM on the processors of that time.
- **A unique nonce for every message.** Like GCM and CCM, OCB needs a nonce that never repeats under one key. RFC 7253 allows nonces of 1 to 15 bytes.
- **Uses.** OCB is in RFC 7253, in OpenSSL (since 1.1.0), in the OpenPGP AEAD packet of RFC 9580, and in some messaging and voice systems. After the patents were abandoned in 2021, more libraries added it.
- **Not where NIST approval is required.** NIST has not approved OCB, in part because of the patents of the past.
- **Not where nonces may repeat.** A repeated nonce breaks both privacy and authenticity, as shown below. RFC 7253, Section 5.1, says that OCB "is not such a scheme" and points to SIV.

## The template

```pseudo id=main
HASH(K, A)                                     ▷ RFC 7253, Section 4.1
L1  Sum ← 0^128;  Offset ← 0^128
L2  for i ← 1 to m do  Offset ← Offset ⊕ L_ntz(i);  Sum ← Sum ⊕ E_K(A_i ⊕ Offset)
L3  if A_* ≠ ε then  Offset ← Offset ⊕ L_*;  Sum ← Sum ⊕ E_K((A_* ‖ 1 ‖ 0^*) ⊕ Offset)
L4  return Sum

OCB-ENCRYPT(K, N, A, P)                         ▷ Section 4.2
L5  L_* ← E_K(0^128);  L_$ ← double(L_*);  L_0 ← double(L_$);  L_i ← double(L_{i−1})
L6  Nonce ← num2str(TAGLEN mod 128, 7) ‖ 0^(120−|N|) ‖ 1 ‖ N;  bottom ← Nonce[123..128]
L7  Ktop ← E_K(Nonce[1..122] ‖ 0^6);  Stretch ← Ktop ‖ (Ktop[1..64] ⊕ Ktop[9..72])
L8  Offset ← Stretch[1+bottom .. 128+bottom];  Checksum ← 0^128
L9  for i ← 1 to m do  Offset ← Offset ⊕ L_ntz(i);  C_i ← Offset ⊕ E_K(P_i ⊕ Offset);  Checksum ← Checksum ⊕ P_i
L10 if P_* ≠ ε then  Offset ← Offset ⊕ L_*;  C_* ← P_* ⊕ E_K(Offset)[1..|P_*|];  Checksum ← Checksum ⊕ (P_* ‖ 1 ‖ 0^*)
L11 Tag ← E_K(Checksum ⊕ Offset ⊕ L_$) ⊕ HASH(K, A)
L12 return C_1 ‖ … ‖ C_m ‖ C_* ‖ Tag[1..TAGLEN]

OCB-DECRYPT(K, N, A, C)                         ▷ Section 4.3
L13 compute L_*, L_$, L_i and the first Offset as in L5 to L8;  split C into C_1 … C_m, C_*, T
L14 for i ← 1 to m do  Offset ← Offset ⊕ L_ntz(i);  P_i ← Offset ⊕ D_K(C_i ⊕ Offset);  Checksum ← Checksum ⊕ P_i
L15 if C_* ≠ ε then  Offset ← Offset ⊕ L_*;  P_* ← C_* ⊕ E_K(Offset)[1..|C_*|];  Checksum ← Checksum ⊕ (P_* ‖ 1 ‖ 0^*)
L16 Tag ← E_K(Checksum ⊕ Offset ⊕ L_$) ⊕ HASH(K, A)
L17 if Tag[1..TAGLEN] ≠ T then return INVALID          ▷ constant-time comparison; P stays buffered
L18 return P_1 ‖ … ‖ P_m ‖ P_*
```

The holes are the block cipher (AES in all named parameter sets) and TAGLEN (128, 96 or 64 in Section 3.1). Decryption uses $D_K$, the inverse cipher, unlike CTR-based modes.

**The offsets.** All offsets are XOR combinations of the values $L_i = 2^{i+2} L_*$ and of the nonce-dependent start value. The update $\mathrm{Offset}_i = \mathrm{Offset}_{i-1} \oplus L_{\mathrm{ntz}(i)}$ walks through a Gray code: consecutive indices differ in one Gray code bit, and the bit that changes is bit $\mathrm{ntz}(i)$. So each step costs one XOR with a value from a table of about $\log_2 m$ entries. OCB2 used the powers $2^i L$ instead, which cost one doubling per step.

**The nonce stretch.** Computing the first offset with one block cipher call per message would cost one call. OCB3 saves it in the common case of a counter nonce: it enciphers the nonce with its last 6 bits cleared, so 64 consecutive nonces share one $K_{top}$, and it takes the start offset as a 128-bit window of a 192-bit string, shifted by the 6 low bits (bottom). An implementation can cache $K_{top}$ and get the next 63 offsets with shifts only.

**The tag length in the nonce.** L6 puts TAGLEN mod 128 into the first 7 bits of the formatted nonce. So a ciphertext under a 64-bit tag is not a prefix of one under a 128-bit tag, and an attacker cannot trade tag length for forgery chances. The test `test_tag_length_is_bound_into_the_nonce` checks this.

**Security model.** RFC 7253, Section 5, states the model: privacy as indistinguishability from random bits, and authenticity of ciphertexts, against nonce-respecting adversaries, if the block cipher is a strong pseudorandom permutation (secure even when the adversary can query the inverse, because decryption uses $D_K$). The bounds are of the form $c\,\sigma^2/2^{128}$ plus the strong PRP advantage, for $\sigma$ blocks in total, plus $q_v/2^{\mathrm{TAGLEN}}$ for $q_v$ forgery attempts. The reduction is tight up to this birthday term. The RFC advises at most $2^{48}$ blocks per key. The proof views OCB as a mode of a tweakable block cipher $\tilde{E}^{N,i}_K(X) = \Delta \oplus E_K(X \oplus \Delta)$ (the XEX construction), first proves the mode with an ideal tweakable cipher, and then bounds the cost of XEX.

**About the code.** The Python code of this page is for study only. It is not constant time: AES uses table lookups and double branches on a secret bit. Do not use it to protect real data. Use AES-OCB from a maintained library, such as OpenSSL (EVP_aes_128_ocb) or Botan, or AES-GCM from a FIPS 140 validated module where a NIST mode is required. The code follows RFC 7253 with blocks as 128-bit integers, so that bit 1 of a string of the RFC is the high bit of the integer. It buffers the plaintext in decryption and returns it only after L17.

## Classic examples

### The internal values of RFC 7253

RFC 7253, Appendix A, lists the internal values for its last sample: $K$ = `000102030405060708090a0b0c0d0e0f`, $N$ = `bbaa9988776655443322110f`, no $A$, and $P$ = `000102…2627` (40 bytes, so $m = 2$ and an 8-byte $P_*$).

| value | hex |
|---|---|
| $L_*$ | `c6a13b37878f5b826f4f8162a1c8d879` |
| $L_\$$ | `8d42766f0f1eb704de9f02c54391b075` |
| $L_0$ | `1a84ecde1e3d6e09bd3e058a8723606d` |
| $L_1$ | `3509d9bc3c7adc137a7c0b150e46c0da` |
| bottom | 15 |
| $K_{top}$ | `9862b0fdee4e2dd56dba6433f0125aa2` |
| $\mathrm{Offset}_0$ | `587ef72716eab6dd3219f8092d517d69` |
| $\mathrm{Offset}_1 = \mathrm{Offset}_0 \oplus L_0$ | `42fa1bf908d7d8d48f27fd83aa721d04` |
| $\mathrm{Offset}_2 = \mathrm{Offset}_1 \oplus L_1$ | `77f3c24534ad04c7f55bf696a434ddde` |
| $\mathrm{Offset}_* = \mathrm{Offset}_2 \oplus L_*$ | `b152f972b3225f459a1477f405fc05a7` |
| $\mathrm{Checksum}_2 = P_1 \oplus P_2$ | `10101010101010101010101010101010` |
| $\mathrm{Checksum}_*$ | `30313233343536379010101010101010` |

$\mathrm{Offset}_0$ is bits 16 to 143 of the 192-bit Stretch, and $\mathrm{Checksum}_*$ adds $P_* \,\|\, 1 \,\|\, 0^{63}$ = `20212223242526278000000000000000`. The test `test_rfc7253_appendix_a_internal_values` checks each line. The other tests run all 16 samples of Appendix A, the sample with a 96-bit tag, and the iterated test of Appendix A for all nine parameter sets (AES-128, AES-192 and AES-256 with tags of 128, 96 and 64 bits). The iterated test builds 22,400 bytes of ciphertext for TAGLEN 128, 20,864 for 96 and 19,328 for 64; the RFC writes "TAGLEN == 192" for the middle case, which is a typo for 96.

### Nonce reuse breaks privacy and authenticity

With one nonce, all offsets are the same for both messages. So full blocks act like ECB per position: equal blocks at equal positions give equal ciphertext blocks, as `test_nonce_reuse_acts_like_ecb_per_position` shows. Worse, the tag can be reused. Take a message $B \,\|\, s$ of one full block and a partial block. The partial block is encrypted as $C_* = s \oplus \mathrm{pad}$, where the pad depends only on the nonce and $m$. Ask for the encryption of $B \,\|\, s$ and, under the same nonce, of $(B \oplus (\delta \,\|\, 0^*)) \,\|\, s$. The checksum of the second message equals the checksum of the new message $B \,\|\, (s \oplus \delta)$, and the offsets are the same, so the second tag is valid for the ciphertext $C_1 \,\|\, (C_* \oplus \delta) \,\|\, T_2$. The test `test_nonce_reuse_forges_a_new_message` turns "amount=0100" into "amount=9999" this way, with two encryption queries and no decryption query.

## Variations

- **OCB1 (2001).** The first version, with offsets $\gamma_i \cdot L \oplus R$ from a Gray code, no associated data, and a proof under a PRP. It built on IAPM of Jutla (EUROCRYPT 2001) and XECB of Gligor and Donescu.
- **OCB2 (2004).** Rogaway recast OCB as a mode of the tweakable block cipher XEX and added associated data with PMAC. OCB2 was in ISO/IEC 19772:2009. **OCB2 is broken.** Inoue and Minematsu found in 2018 that one encryption query of two blocks gives a forgery of a one-block message. OCB2 mixes the XE form (for the last block) and the XEX form (for the other blocks) under one key, and for the tweaks that the last block uses, this mix is not a secure tweakable cipher; the proof had assumed that it was. Poettering and Iwata extended this to plaintext recovery and universal forgery, and the four authors published the full attacks at CRYPTO 2019. The flaw is in the OCB2 proof, not in the general method; OCB1 and OCB3 are not affected.
- **OCB3 (2011, RFC 7253).** The version on this page: $L_*$, $L_\$$ and the $L_i$ table, the stretch for the first offset, and the tag length bound into the nonce.
- **The patents.** Rogaway held US patents on OCB, and Jutla (IBM) and Gligor and Donescu held patents on related one-pass modes. Rogaway gave free licenses for some uses, in 2013 for open source software, for non-military software and for OpenSSL, and asked fees in other cases. This kept OCB out of most standards and products for years, and it is why two-pass modes such as CCM and EAX were designed. In February 2021 Rogaway wrote to the IRTF CFRG list that he had abandoned all OCB patents and placed his OCB-related IP in the public domain. His patents were filed only in the US.
- **PMAC.** The MAC of the same family: the sum of $E_K(A_i \oplus \mathrm{Offset}_i)$, as in HASH. HASH of L1 to L4 is PMAC without its last encipherment.
- **OCB with other block sizes.** Draft work defines OCB for 64-bit and 256-bit blocks with other constants. RFC 7253 covers only 128-bit blocks.
- **Nonce-misuse resistant modes.** SIV (RFC 5297) and AES-GCM-SIV (RFC 8452) keep authenticity and leak only equality if a nonce repeats. OCB does not.

## Pitfalls

- **Repeating a nonce.** Privacy and authenticity fail, as the example above shows. RFC 7253 warns that the attacker can "recover secret information used to provide authenticity, making subsequent forgeries trivial".
- **Using OCB2.** It is broken. Old code or old standards that name "OCB" without a version may mean OCB2. Use OCB3 as in RFC 7253.
- **A weak block cipher.** The proof needs a strong PRP, because decryption calls $D_K$. Use AES.
- **Accepting several tag lengths under one key.** RFC 7253, Section 5, asks receivers to fix TAGLEN per key.
- **Too much data per key.** The bounds grow with $\sigma^2/2^{128}$. Keep under $2^{48}$ blocks per key, as the RFC advises.
- **Releasing plaintext before L17.** OCB decryption produces plaintext blocks before the tag is known. A streaming decryptor that outputs them early gives up authenticity in practice.
- **Timing.** double and a table-based AES leak through timing unless written in constant time. RFC 7253 notes that double is the only conditional operation on secret data.

## Exercises

1. Show that $\mathrm{Offset}_i = \mathrm{Offset}_0 \oplus \bigoplus_j L_j$, where $j$ ranges over the bits set in the Gray code $i \oplus (i \gg 1)$.
2. Why does OCB need a strong PRP, while CTR, GCM and EAX need only a PRP?
3. Compute the number of block cipher calls of OCB3 for a message of $m$ full blocks and a partial block, with $a$ full blocks of associated data, and with the $K_{top}$ cache hit.
4. Explain why the forgery of the nonce reuse example needs a partial last block. Can you build a forgery under a repeated nonce with full blocks only?
5. Read the OCB2 attack of Inoue and Minematsu, and say which assumption of the XEX proof fails for the last block.

## References

- Ted Krovetz and Phillip Rogaway, RFC 7253, The OCB Authenticated-Encryption Algorithm, 2014.
- Phillip Rogaway, Mihir Bellare, John Black and Ted Krovetz, OCB, ACM CCS 2001.
- Phillip Rogaway, Efficient instantiations of tweakable blockciphers and refinements to modes OCB and PMAC, ASIACRYPT 2004.
- Ted Krovetz and Phillip Rogaway, The software performance of authenticated-encryption modes, FSE 2011.
- Akiko Inoue, Tetsu Iwata, Kazuhiko Minematsu and Bertram Poettering, Cryptanalysis of OCB2, CRYPTO 2019.
- Charanjit S. Jutla, Encryption modes with almost free message integrity, EUROCRYPT 2001.
- Phillip Rogaway, OCB patents are abandoned; freely usable, CFRG mailing list, 2021.
