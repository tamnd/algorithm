---
tag: V9AB4V
kind: technique
slug: eax-mode
name: EAX mode
aliases:
- EAX
area: cryptography/symmetric-ciphers
level: advanced
summary: "Two-pass AEAD of Bellare, Rogaway and Wagner (2004): CTR mode keyed by OMAC of the nonce, and a tag that XORs OMAC of nonce, header and ciphertext with three tweaks. On-line, any nonce length."
prereqs: [cmac, ctr-mode, authenticated-encryption]
see_also: [ccm-mode, gcm-mode, ocb-mode, chacha20-poly1305, cbc-mac, nonce]
sources:
  - url: "https://web.cs.ucdavis.edu/~rogaway/papers/eax.pdf"
    title: Mihir Bellare, Phillip Rogaway and David Wagner, The EAX Mode of Operation (A Two-Pass Authenticated-Encryption Scheme Optimized for Simplicity and Efficiency), full version, January 18, 2004
    locator: Figure 1 (CBC, CTR, pad, OMAC and OMAC^t), Figure 2 (EAX.Encrypt and EAX.Decrypt), Figure 4 (comparison with CCM), Section 4 (no patents), Theorem 5 and Corollary 6 (security), Appendix G (test vectors)
  - paper: "Mihir Bellare, Phillip Rogaway and David Wagner, The EAX mode of operation, Fast Software Encryption (FSE) 2004, LNCS 3017, pages 389 to 407"
    locator: the conference version of the paper above
  - paper: "Tetsu Iwata and Kaoru Kurosawa, OMAC: One-Key CBC MAC, Fast Software Encryption (FSE) 2003, LNCS 2887, pages 129 to 153"
    locator: the OMAC construction; EAX uses the variant with the constants 2L and 4L, which is CMAC
  - url: "https://www.rfc-editor.org/rfc/rfc4493"
    title: JH Song, Radha Poovendran, Jicheol Lee and Tetsu Iwata, RFC 4493, The AES-CMAC Algorithm, 2006
    locator: Section 4 (test vectors, Examples 1 and 2), used to check the OMAC part
  - paper: "Phillip Rogaway, Authenticated-encryption with associated-data, ACM CCS 2002, pages 98 to 107"
    locator: the nonce-based AEAD model in which EAX is proved secure
  - paper: "Kazuhiko Minematsu, Stefan Lucks, Hiraku Morita and Tetsu Iwata, Attacks and security proofs of EAX-prime, Fast Software Encryption (FSE) 2013"
    locator: the attacks on EAX-prime, the variant of the ANSI C12.22 smart meter standard
---

EAX is an [authenticated encryption](/authenticated-encryption/) mode for a [block cipher](/block-cipher/), designed by Bellare, Rogaway and Wagner and published at FSE 2004. It was built as a cleaner alternative to [CCM](/ccm-mode/): two passes, one for privacy with [CTR mode](/ctr-mode/) and one for authenticity with OMAC, which is the same function as [CMAC](/cmac/). Unlike CCM, it needs no length field and no special formatting, accepts a nonce and a header of any length, is on-line (it can encrypt a stream whose length it does not know yet), and lets a static header be processed once. The trick that makes this simple is the tweak: OMAC is called with a one-block prefix 0, 1 or 2, which turns one key into three independent functions, one each for the nonce, the header and the ciphertext. The authors put the design in the public domain and stated that they knew of no patents on it.

**Notation.** $E_K$ is the block cipher with key $K$ and block length $n$ (128 for AES). $N$ is the nonce, $H$ the header (the associated data), $M$ the message, $C$ the ciphertext and $\tau$ the tag length in bits, $0 \le \tau \le n$. $[t]_n$ is the integer $t$ as an $n$-bit block. $\mathrm{OMAC}^t_K(X) = \mathrm{OMAC}_K([t]_n \,\|\, X)$.

## In plain words

EAX computes three fingerprints with one MAC and one key. To keep them apart it puts a different first block in front of each input: a block of value 0 before the nonce, 1 before the header and 2 before the ciphertext. The fingerprint of the nonce is the starting counter for counter mode, which hides the message. The tag is the XOR of the three fingerprints. The receiver recomputes the fingerprints of the nonce, the header and the ciphertext, compares the tag, and only then runs counter mode to decrypt. Every input can have any length, and the ciphertext can be fingerprinted while it is being produced.

## When it applies

- **A two-pass AEAD with no patents and no special formatting.** EAX was offered to standards bodies at a time when the one-pass modes such as [OCB](/ocb-mode/) were under patents. It was included in ISO/IEC 19772:2009.
- **Streams of unknown length.** The OMAC of the ciphertext can absorb data as it is produced, so the sender needs constant memory. CCM must know the payload length before it starts.
- **A header that does not change.** $H' = \mathrm{OMAC}^1_K(H)$ can be computed once per session, so a long fixed header costs nothing per message.
- **Nonces of any length.** A nonce is passed through $\mathrm{OMAC}^0$, so it can be a counter, a long random string or a structured identifier.
- **Not for top speed.** EAX makes about two block cipher calls per message block, and the OMAC pass is serial. GCM and OCB are faster where speed matters.
- **Not where a NIST approved mode is required.** NIST has not approved EAX; use [GCM](/gcm-mode/) or CCM there.

## The template

```pseudo id=main
OMAC^t_K(X)                                    ▷ Figure 1, line 50
L1  return OMAC_K([t]_n ‖ X)                  ▷ OMAC = CMAC: B = 2L, P = 4L, L = E_K(0^n)

EAX-ENCRYPT(K, N, H, M)                        ▷ Figure 2, lines 10 to 16
L2  N' ← OMAC^0_K(N)
L3  H' ← OMAC^1_K(H)
L4  C ← CTR_K^{N'}(M)                          ▷ key stream E_K(N'), E_K(N'+1), … mod 2^n
L5  C' ← OMAC^2_K(C)
L6  Tag ← N' ⊕ C' ⊕ H'
L7  return C ‖ MSB_τ(Tag)

EAX-DECRYPT(K, N, H, CT)                       ▷ Figure 2, lines 20 to 29
L8  if |CT| < τ then return INVALID
L9  C ‖ T ← CT, where |T| = τ
L10 N' ← OMAC^0_K(N);  H' ← OMAC^1_K(H);  C' ← OMAC^2_K(C)
L11 if T ≠ MSB_τ(N' ⊕ C' ⊕ H') then return INVALID       ▷ constant-time comparison
L12 return CTR_K^{N'}(C)
```

The holes are the block cipher $E$ and the tag length $\tau$, both fixed for a session. OMAC is the one-key CBC-MAC of Iwata and Kurosawa in the form with the constants $2L$ and $4L$ in $\mathrm{GF}(2^n)$, which the EAX paper chose and which is the CMAC of SP 800-38B. The counter of L4 is the whole block $N'$, increased as an $n$-bit integer modulo $2^n$, not only its last 32 bits as in GCM.

**Why the tweaks.** If the three calls were plain OMAC, an attacker could swap the nonce and the header ($N = X$, $H = Y$ against $N = Y$, $H = X$) and keep $N' \oplus H'$ the same. The prefixes $[0]_n$, $[1]_n$ and $[2]_n$ make the three functions behave like independent random functions, because OMAC is a PRF and the three input sets do not overlap. The prefix is a full block, so for a nonempty input its first CBC step is $E_K([t]_n)$, a value that can be computed once per key.

**Why the order of L11 and L12.** The tag depends on $C$, not on $M$. So the receiver can check the tag before it decrypts, as in encrypt-then-MAC, and an invalid message costs only the OMAC pass, about half the work of a full decryption. The test `test_rejection_costs_about_half_of_decryption` counts block cipher calls: rejection skips exactly the 40 calls of the CTR pass for a 40-block message.

**Security model.** EAX is a nonce-based AEAD in the model of Rogaway (CCS 2002). Theorem 5 of the paper bounds, for $\sigma$ blocks of queries in total and a random permutation in place of $E$, the privacy advantage (indistinguishability from random bits) by $9\sigma^2/2^n$, and the authenticity advantage (forging a new valid ciphertext) by $10.5\sigma^2/2^n + 2^{-\tau}$. Corollary 6 passes to a real block cipher with an added PRP advantage term. The reduction to the PRP security of $E$ is tight, with a quadratic birthday term: the bounds become weak near $\sigma = 2^{n/2}$ blocks per key. The proof first shows that EAX2, the same scheme with two independent keys for CTR and OMAC, is secure by generic composition, and then that sharing one key costs only the stated terms. The proof needs nonces that do not repeat.

**About the code.** The Python code of this page is for study only. It is not constant time: AES uses table lookups and the doubling in OMAC branches on a secret bit. Do not use it to protect real data. EAX is in Botan and Crypto++, among others; where a validated module is required, use AES-GCM from a FIPS 140 validated module instead. The code gives `eax_encrypt` and `eax_decrypt` with the line markers, `EaxHeader` for a static header, and `EaxOnlineEncryptor`, which takes the message in chunks and is told only at the end that the message is over.

## Classic examples

### The second test vector of the paper

Appendix G of the full version, the vector with the two-byte message `f7fb`, under AES-128 with a 16-byte tag.

| step | value |
|---|---|
| $K$ | `91945d3f4dcbee0bf45ef52255f095a4` |
| $N$ | `becaf043b0a23d843194ba972c66debd` |
| $H$ | `fa3bfd4806eb53fa` |
| $L = E_K(0^{128})$ | `1178d366408dba28b7aeb17c4967e6e6` |
| $N' = \mathrm{OMAC}^0_K(N)$ | `9fa5076fb1ade0c5bfe3e82b7e55ab1d` |
| $H' = \mathrm{OMAC}^1_K(H)$ | `e2a488b0bb52aba00b310f4097fbe6b6` |
| $E_K(N')$ | `ee2647f463425ce6bb4f151b323b13d3` |
| $C = M \oplus \mathrm{MSB}_{16}(E_K(N'))$ | `f7fb` ⊕ `ee26` = `19dd` |
| $C' = \mathrm{OMAC}^2_K(C)$ | `214d1cee0e6240bf04f593631fd72a4e` |
| $\mathrm{Tag} = N' \oplus C' \oplus H'$ | `5c4c9331049d0bdab0277408f67967e5` |

The output $C \,\|\, T$ = `19dd5c4c9331049d0bdab0277408f67967e5` is the CIPHER line of the paper. The tests check all ten vectors of Appendix G (messages of 0 to 21 bytes), and check OMAC alone against Examples 1 and 2 of RFC 4493, because OMAC with $2L$ and $4L$ is AES-CMAC.

### On-line encryption

`test_online_encryption_does_not_need_the_length` feeds a 77-byte message in chunks of 1, 15, 16, 2, 30 and 13 bytes and gets the same output as the one-shot function. The encryptor keeps one partial block of key stream and the one block that OMAC must hold back, because the last block is masked with $B = 2L$ if it is full and with $P = 4L$ after padding if it is not. CCM cannot do this: its first MAC block $B_0$ holds the payload length.

### A static header

`EaxHeader` computes $H'$ once. Each message then costs one OMAC of the nonce, one CTR pass and one OMAC of the ciphertext, whatever the length of $H$.

## Variations

- **EAX2.** The generic composition with two keys, CTR under $K_1$ and OMAC under $K_2$. EAX is EAX2 with $K_1 = K_2$.
- **EAX-prime (EAX').** A variant proposed for the ANSI C12.22 smart meter standard, which saves block cipher calls by merging the nonce and the header and by changing the OMAC constants. Minematsu, Lucks, Morita and Iwata (FSE 2013) found practical forgeries and attacks on privacy for it. It is not EAX, and its weaknesses do not apply to EAX.
- **Other two-pass modes.** [CCM](/ccm-mode/) uses CBC-MAC over the plaintext with a length field; SIV (RFC 5297) uses S2V, a CMAC-based PRF, and keeps some security when nonces repeat.
- **One-pass modes.** [OCB](/ocb-mode/) does both jobs in one pass with about one block cipher call per block.
- **A MAC from EAX.** With an empty message and a fixed nonce, EAX is a PRF on the header, as the paper notes.

## Pitfalls

- **Repeating a nonce.** The CTR key stream repeats, so the XOR of the two ciphertexts is the XOR of the two messages, as the test `test_nonce_reuse_leaks_the_xor_of_plaintexts` shows. The security proof does not cover this case at all.
- **Plain OMAC without the tweaks.** It allows swaps between nonce, header and ciphertext.
- **Confusing EAX with EAX'.** EAX' is a different, broken scheme.
- **Short tags.** A $\tau$-bit tag gives at best a $2^{-\tau}$ chance per forgery attempt, and the attempts add up.
- **Too much data per key.** The birthday terms of Theorem 5 grow with $\sigma^2/2^n$. With a 64-bit block cipher this is a real limit after $2^{32}$ blocks.
- **Decrypting before the check.** L11 comes before L12 for a reason. A streaming decryptor that outputs plaintext early gives up the authenticity guarantee in practice.
- **Timing.** The doubling in OMAC and a table-based AES leak through timing if they branch or index on secret values.

## Exercises

1. Show that without the prefixes $[0]_n$ and $[1]_n$, the nonce $N = X$ with the header $H = Y$ and the nonce $N = Y$ with the header $H = X$ give the same tag for the empty message.
2. Count the block cipher calls of EAX for a nonce of 1 block, a header of $h$ blocks and a message of $m \ge 1$ blocks, and the calls when $H'$ and $E_K([t]_n)$ are cached.
3. Explain why OMAC must hold back one block of input in on-line use, and why it does not need to know the total length.
4. Two messages are encrypted with one key and one nonce. What does an eavesdropper learn? Can it also forge? Give an argument or an attack.
5. Write $\mathrm{OMAC}^2_K(C)$ for $C$ of exactly one block, and explain why the CBC chain starts from $E_K([2]_n)$.

## References

- Mihir Bellare, Phillip Rogaway and David Wagner, The EAX mode of operation, FSE 2004, and the full version of January 18, 2004.
- Tetsu Iwata and Kaoru Kurosawa, OMAC: One-Key CBC MAC, FSE 2003.
- JH Song, Radha Poovendran, Jicheol Lee and Tetsu Iwata, RFC 4493, 2006.
- Phillip Rogaway, Authenticated-encryption with associated-data, ACM CCS 2002.
- Kazuhiko Minematsu, Stefan Lucks, Hiraku Morita and Tetsu Iwata, Attacks and security proofs of EAX-prime, FSE 2013.
