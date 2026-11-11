---
tag: NRR0YJ
kind: definition
slug: authenticated-encryption
name: Authenticated encryption
aliases:
- AEAD
- authenticated encryption with associated data
area: cryptography/symmetric-ciphers
level: core
summary: Encryption that hides the message and rejects every ciphertext the sender did not make. IND-CPA plus ciphertext integrity gives IND-CCA; encrypt-then-MAC builds it.
prereqs: [message-authentication-code, semantic-security]
see_also: [gcm-mode, chacha20-poly1305, ccm-mode, ocb-mode, ind-cca-security, padding-oracle-attack, nonce, ccm-decryption-check]
sources:
  - paper: "Mihir Bellare and Chanathip Namprempre, Authenticated encryption: relations among notions and analysis of the generic composition paradigm, ASIACRYPT 2000, LNCS 1976, pages 531 to 545; full version in Journal of Cryptology 21(4), 2008"
    locator: the notions INT-PTXT and INT-CTXT, the theorem that IND-CPA and INT-CTXT imply IND-CCA, and the table of the three generic compositions with their counterexamples
  - paper: "Phillip Rogaway, Authenticated-encryption with associated-data, ACM CCS 2002, pages 98 to 107"
    locator: the syntax of a nonce-based AEAD scheme with a header that is authenticated but not encrypted, and its privacy and authenticity games
  - paper: "Phillip Rogaway and Thomas Shrimpton, A provable-security treatment of the key-wrap problem, EUROCRYPT 2006, LNCS 4004, pages 373 to 390"
    locator: deterministic authenticated encryption (DAE) and the SIV construction
  - url: "https://www.rfc-editor.org/rfc/rfc5297"
    title: Dan Harkins, RFC 5297, Synthetic Initialization Vector (SIV) Authenticated Encryption Using the Advanced Encryption Standard (AES), 2008
    locator: Section 2.6 (SIV encryption) and Section 2.7 (SIV decryption)
  - url: "https://www.rfc-editor.org/rfc/rfc8452"
    title: Shay Gueron, Adam Langley and Yehuda Lindell, RFC 8452, AES-GCM-SIV, Nonce Misuse-Resistant Authenticated Encryption, 2019
    locator: Section 4 (encryption) and Section 9 (security considerations, including the limits for a repeated nonce)
  - paper: "Hugo Krawczyk, The order of encryption and authentication for protecting communications (or: how secure is SSL?), CRYPTO 2001, LNCS 2139, pages 310 to 331"
    locator: the example where MAC-then-encrypt fails, and the proof that it is secure with CBC or a stream cipher as the encryption
  - paper: "Chanathip Namprempre, Phillip Rogaway and Thomas Shrimpton, Reconsidering generic composition, EUROCRYPT 2014, LNCS 8441, pages 257 to 274"
    locator: generic composition for nonce-based AEAD, with the schemes N1, N2 and N3
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 5 (CCA security and authenticated encryption, with the generic constructions)
---

Authenticated encryption (AE) is symmetric encryption that gives two guarantees together. Confidentiality: the ciphertext hides the message. Integrity: the receiver rejects every ciphertext that the sender with the key did not make, so an attacker cannot change, cut or invent ciphertexts. Authenticated encryption with associated data (AEAD) also protects a header that is sent in the clear, such as a packet number or a record type. AEAD is the standard tool for a secure channel: [AES-GCM](/gcm-mode/) and [ChaCha20-Poly1305](/chacha20-poly1305/) are the only ciphers of TLS 1.3. Encryption alone is not enough: a [padding oracle](/padding-oracle-attack/) recovers CBC plaintexts from error messages, and CTR ciphertexts change bit by bit at will.

## Definition

**Notation.** $K$ is the key, $N$ a nonce, $A$ the associated data (the header), $P$ the plaintext and $C$ the ciphertext, which includes the tag. The symbol $\bot$ means "invalid". $\mathcal{A}$ is the adversary.

**Syntax (Rogaway 2002).** A nonce-based AEAD scheme is a pair of deterministic algorithms with a key from a key space.

1. $\mathsf{Enc}(K, N, A, P)$ returns a ciphertext $C$, usually $|P| + \tau$ bits long for a tag of $\tau$ bits.
2. $\mathsf{Dec}(K, N, A, C)$ returns a plaintext $P$ or $\bot$.
3. Correctness: $\mathsf{Dec}(K, N, A, \mathsf{Enc}(K, N, A, P)) = P$ for all inputs.

The sender must never use one nonce twice under one key; the games below allow only such nonce-respecting adversaries. The [nonce](/nonce/) can be a counter, so the scheme needs no randomness. The older randomized syntax of Bellare and Namprempre (2000) is the special case where $\mathsf{Enc}$ draws its own random value and puts it in $C$.

**Confidentiality (IND-CPA).** A bit $b$ is drawn. $\mathcal{A}$ sends queries $(N, A, P_0, P_1)$ with $|P_0| = |P_1|$ and gets $\mathsf{Enc}(K, N, A, P_b)$. It outputs a guess $b'$. Its advantage is $\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}(\mathcal{A}) = \Pr[b' = 1 \mid b = 1] - \Pr[b' = 1 \mid b = 0]$. See [semantic security](/semantic-security/) for why this captures "hides everything but the length".

**Confidentiality under chosen-ciphertext attack (IND-CCA).** The same game, with a decryption oracle $(N, A, C) \mapsto \mathsf{Dec}(K, N, A, C)$ as well. $\mathcal{A}$ may not send a triple that an encryption query returned. See [IND-CCA security](/ind-cca-security/).

**Integrity of plaintexts (INT-PTXT).** $\mathcal{A}$ gets an encryption oracle and a verification oracle, which says whether $\mathsf{Dec}(K, N, A, C) \ne \bot$. It wins if some verified triple decrypts to a pair $(A, P)$ that it never asked the encryption oracle for.

**Integrity of ciphertexts (INT-CTXT).** The same oracles. $\mathcal{A}$ wins if the verification oracle accepts a triple $(N, A, C)$ that the encryption oracle never returned. This is the stronger notion: a new ciphertext of an old message is already a win. INT-CTXT implies INT-PTXT, because a new plaintext needs a new ciphertext.

**Authenticated encryption.** A scheme is AE secure if it is IND-CPA and INT-CTXT, both with negligible advantage for every efficient adversary. Rogaway and Shrimpton (2006) give an equivalent single game: the real oracles $\mathsf{Enc}_K$ and $\mathsf{Dec}_K$ against an oracle that returns random strings of the right length and an oracle that always returns $\bot$.

### IND-CPA and INT-CTXT imply IND-CCA

**Theorem (Bellare and Namprempre 2000).** For every IND-CCA adversary $\mathcal{A}$ there are an INT-CTXT adversary $\mathcal{B}$ and an IND-CPA adversary $\mathcal{C}$, with about the running time and the queries of $\mathcal{A}$, such that
$$\mathrm{Adv}^{\mathrm{ind\text{-}cca}}(\mathcal{A}) \le 2 \, \mathrm{Adv}^{\mathrm{int\text{-}ctxt}}(\mathcal{B}) + \mathrm{Adv}^{\mathrm{ind\text{-}cpa}}(\mathcal{C}).$$

**Proof.** For $b \in \{0, 1\}$, let $G_b$ be the IND-CCA game with the bit fixed to $b$, and let $H_b$ be the same game except that the decryption oracle returns $\bot$ for every allowed query. Write $p(G)$ for the probability that $\mathcal{A}$ outputs 1 in game $G$, so that $\mathrm{Adv}^{\mathrm{ind\text{-}cca}}(\mathcal{A}) = p(G_1) - p(G_0)$.

Step 1: $|p(G_b) - p(H_b)| \le \mathrm{Adv}^{\mathrm{int\text{-}ctxt}}(\mathcal{B}_b)$. The games $G_b$ and $H_b$ give the same answers until $\mathcal{A}$ sends a decryption query that $G_b$ answers with a value other than $\bot$. Call this event $E$. The allowed queries are exactly the triples that the encryption oracle did not return, so $E$ means that $\mathcal{A}$ found a new valid ciphertext. Since the games are equal until $E$, the difference of the output probabilities is at most $\Pr[E]$ in $H_b$. Let $\mathcal{B}_b$ run $\mathcal{A}$ in the INT-CTXT game: it answers $(N, A, P_0, P_1)$ by an encryption query on $(N, A, P_b)$, and it answers each decryption query by $\bot$, after it sends the same triple to its verification oracle. Then $\mathcal{B}_b$ simulates $H_b$ exactly, and it wins when $E$ happens. Let $\mathcal{B}$ be the better of $\mathcal{B}_0$ and $\mathcal{B}_1$.

Step 2: $p(H_1) - p(H_0) \le \mathrm{Adv}^{\mathrm{ind\text{-}cpa}}(\mathcal{C})$. Let $\mathcal{C}$ run $\mathcal{A}$, send its encryption queries to the IND-CPA oracle, and answer every decryption query with $\bot$. With the hidden bit $b$, $\mathcal{C}$ simulates $H_b$ exactly, so its advantage is $p(H_1) - p(H_0)$.

Step 3: $p(G_1) - p(G_0) \le (p(H_1) + \mathrm{Adv}^{\mathrm{int\text{-}ctxt}}(\mathcal{B})) - (p(H_0) - \mathrm{Adv}^{\mathrm{int\text{-}ctxt}}(\mathcal{B}))$, which with Step 2 is the claim. $\blacksquare$

**Tightness.** The reduction is tight. $\mathcal{B}$ and $\mathcal{C}$ run in the time of $\mathcal{A}$ plus the cost of the oracle calls, they make the same number of queries, and the loss is a factor of 2 on one term only. The converse is false in general: IND-CCA does not imply INT-CTXT, since a scheme can be IND-CCA and still accept many ciphertexts that decrypt to random messages.

### Generic composition

Take an IND-CPA encryption scheme $\mathcal{E}$ and a strongly unforgeable [MAC](/message-authentication-code/), with independent keys $K_e$ and $K_m$. Bellare and Namprempre (2000) studied three ways to combine them.

| composition | output | IND-CPA | IND-CCA | INT-PTXT | INT-CTXT |
|---|---|---|---|---|---|
| encrypt-and-MAC (E&M) | $\mathcal{E}_{K_e}(P) \,\|\, \mathsf{Mac}_{K_m}(P)$ | not in general | not in general | yes | not in general |
| MAC-then-encrypt (MtE) | $\mathcal{E}_{K_e}(P \,\|\, \mathsf{Mac}_{K_m}(P))$ | yes | not in general | yes | not in general |
| encrypt-then-MAC (EtM) | $C \,\|\, \mathsf{Mac}_{K_m}(C)$ with $C = \mathcal{E}_{K_e}(P)$ | yes | yes | yes | yes |

"Not in general" means that some choice of a secure $\mathcal{E}$ and a secure MAC makes the composition fail. The two counterexamples below are the ones that the tests run on real code.

**E&M is not IND-CPA.** A MAC need not hide anything. A deterministic MAC such as [CMAC](/cmac/) gives equal tags for equal messages, under fresh nonces too. The adversary asks for the encryption of $P_0$, then for the challenge on $(P_0, P_1)$, and outputs 0 if the two tags are equal. It wins every time.

**MtE is not INT-CTXT, and so not IND-CCA.** Let $\mathcal{E}'$ be an IND-CPA scheme and let $\mathcal{E}$ append one byte to each ciphertext of $\mathcal{E}'$, a byte that decryption ignores. $\mathcal{E}$ is still IND-CPA, because the extra byte is a constant. In MtE with $\mathcal{E}$, a changed last byte gives a new ciphertext that decrypts to the same message with a valid tag, which wins INT-CTXT. In the IND-CCA game the adversary changes the last byte of the challenge and asks the decryption oracle, which returns $P_b$.

**EtM is secure.** IND-CPA holds, because the tag is a function of $C$ and of a key that $\mathcal{E}$ does not use. INT-CTXT holds, because a new valid triple is a new message for the MAC with a valid tag, which breaks strong unforgeability. The theorem above then gives IND-CCA. In the nonce-based setting the MAC must cover the nonce and the associated data as well, with an encoding that cannot be split in two ways (Namprempre, Rogaway and Shrimpton 2014).

## Examples and non-examples

- **Example: [AES-GCM](/gcm-mode/), [ChaCha20-Poly1305](/chacha20-poly1305/), [CCM](/ccm-mode/), [EAX](/eax-mode/) and [OCB](/ocb-mode/).** Nonce-based AEAD schemes. GCM and ChaCha20-Poly1305 are EtM with a one-time Carter and Wegman MAC; CCM is MtE in a form that is proved secure; OCB makes both guarantees in one pass.
- **Example: CTR mode with CMAC over $N \,\|\, A \,\|\, C \,\|\, |A| \,\|\, |C|$.** EtM with two keys. This is the scheme of the implementation folder. The lengths at the end stop an attacker from moving bytes between $A$ and $C$.
- **Example: IPsec ESP with CBC and HMAC.** EtM, as Bellare and Namprempre advised.
- **Non-example: CTR or CBC alone.** IND-CPA, but not INT-CTXT. Flipping a bit of a CTR ciphertext flips the same bit of the plaintext.
- **Non-example: TLS up to version 1.2 with CBC.** MtE with padding. Krawczyk (2001) proved that MtE with CBC is secure if the receiver gives no detail about the failure. In practice it did: padding oracles (Vaudenay 2002) and the timing attack Lucky Thirteen (AlFardan and Paterson 2013) read plaintext. RFC 7366 added EtM to TLS, and TLS 1.3 allows only AEAD.
- **Non-example: SSH with its default MAC order.** E&M on the plaintext. Bellare, Kohno and Namprempre (2004) analyzed it and proposed changes. It leaks equal plaintexts only if the MAC input repeats, and SSH puts a sequence number in it.
- **Non-example: WEP.** A CRC-32 of the plaintext, encrypted with RC4. The CRC is linear, so an attacker changes the ciphertext and fixes the checksum without the key (Borisov, Goldberg and Wagner 2001). A checksum is not a MAC.

The code in the implementation folder is for study only and is not constant time: the AES in `aes.py` uses table lookups that depend on the key. For real use, take AES-GCM from a FIPS 140 validated module, or `crypto_aead_xchacha20poly1305_ietf_encrypt` from libsodium. The file `authenticated_encryption.py` gives EtM with AES-CTR and AES-CMAC, and the weak E&M and MtE compositions. The tests check AES against FIPS 197, Appendix C.1, and the CMAC against RFC 4493, Section 4. They check EtM round trips, that EtM rejects every changed bit in the ciphertext, the tag, the associated data and the nonce, and that it rejects bytes moved from $C$ to $A$. They run the MtE counterexample to win INT-CTXT and IND-CCA in all trials, show that the same change fails against EtM, and win the IND-CPA game against E&M in all trials.

## Related definitions

- **[Message authentication code](/message-authentication-code/).** The integrity part alone, without secrecy. EtM needs strong unforgeability, so that a second tag for an old ciphertext is also a forgery.
- **[Semantic security](/semantic-security/) and [IND-CCA security](/ind-cca-security/).** The secrecy part alone. IND-CCA follows from AE, but it does not give integrity.
- **Deterministic authenticated encryption (DAE) and SIV.** Rogaway and Shrimpton (2006) defined AE with no nonce, or with a nonce that may repeat. The SIV construction computes a PRF of $(A, P)$ and uses it as the IV of CTR mode (RFC 5297). A repeated nonce then reveals only whether two whole inputs are equal. AES-GCM-SIV (RFC 8452) is a fast instance with POLYVAL in the PRF.
- **Release of unverified plaintext.** A decryption that returns plaintext before the tag check, or that returns it on failure, breaks the model. See the [CCM decryption check](/ccm-decryption-check/) page for a demonstration.
- **Key commitment.** AE does not require that a ciphertext decrypts validly under only one key. For GCM and ChaCha20-Poly1305 an attacker can make one ciphertext that is valid under two keys, which matters for message franking and for password-based encryption (Grubbs, Lu and Ristenpart 2017; Dodis, Grubbs, Ristenpart and Woodage 2018).

## References

- Mihir Bellare and Chanathip Namprempre, ASIACRYPT 2000 and Journal of Cryptology 2008. The integrity notions, the implication to IND-CCA and generic composition.
- Phillip Rogaway, ACM CCS 2002. Nonce-based AEAD with associated data.
- Phillip Rogaway and Thomas Shrimpton, EUROCRYPT 2006. DAE and SIV.
- Dan Harkins, RFC 5297, 2008. AES-SIV.
- Shay Gueron, Adam Langley and Yehuda Lindell, RFC 8452, 2019. AES-GCM-SIV.
- Hugo Krawczyk, CRYPTO 2001. The order of encryption and authentication.
- Chanathip Namprempre, Phillip Rogaway and Thomas Shrimpton, EUROCRYPT 2014. Generic composition with nonces.
- Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, Chapter 5.
