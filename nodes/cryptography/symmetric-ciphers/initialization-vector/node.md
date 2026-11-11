---
tag: TZ0Q2Q
kind: definition
slug: initialization-vector
name: Initialization vector
aliases:
- IV
area: cryptography/symmetric-ciphers
level: intro
summary: A public extra input to encryption, sent with the ciphertext, that makes equal messages encrypt differently. CBC and CFB need it uniformly random and unpredictable.
prereqs: [symmetric-encryption, chosen-plaintext-attack]
see_also: [nonce, cbc-mode, cfb-mode, ofb-mode, ctr-mode, ind-cpa-security, gcm-mode]
sources:
  - url: "https://doi.org/10.6028/NIST.SP.800-38A"
    title: Morris Dworkin, NIST Special Publication 800-38A, Recommendation for Block Cipher Modes of Operation, Methods and Techniques, 2001
    locator: Section 5.3 (initialization vectors) and Appendix C (generation of initialization vectors)
  - paper: "Phillip Rogaway, Nonce-based symmetric encryption, Fast Software Encryption (FSE 2004), LNCS 3017, pages 348 to 359"
    locator: the syntax of IV-based and nonce-based encryption, and the insecurity of CBC when the IV is a nonce
  - url: "https://cseweb.ucsd.edu/~mihir/papers/sym-enc.html"
    title: Mihir Bellare, Anand Desai, Eron Jokipii and Phillip Rogaway, A concrete security treatment of symmetric encryption, FOCS 1997 (full version on the authors' pages)
    locator: Section 6 of the full version (CBC with a random IV)
  - paper: "Gregory V. Bard, The vulnerability of SSL to chosen plaintext attack, IACR Cryptology ePrint Archive, report 2004/111"
    locator: the attack on CBC with an IV that the adversary can predict
---

An initialization vector (IV) is an extra input to an encryption algorithm. It has a fixed length, usually one block, it is not secret, and it is sent with the ciphertext so that the receiver can decrypt. Its job is to make two encryptions of the same message under the same key look different, which every [IND-CPA](/ind-cpa-security/) secure scheme must do. What an IV must be depends on the mode. For [CBC](/cbc-mode/) and [CFB](/cfb-mode/), SP 800-38A requires an IV that the adversary cannot predict; for [OFB](/ofb-mode/) and [CTR](/ctr-mode/) the starting value only has to be unique, and is better called a [nonce](/nonce/).

## Definition

**Notation.** $K$ is the key, $M$ the message, $n$ the block length in bits, and $\mathcal{A}$ the adversary in a [chosen-plaintext attack](/chosen-plaintext-attack/).

**IV-based encryption.** An IV-based encryption scheme has a deterministic encryption function $\mathcal{E}(K, IV, M)$ and a decryption function $\mathcal{D}(K, IV, C)$ with $\mathcal{D}(K, IV, \mathcal{E}(K, IV, M)) = M$. The IV is one more input; the full ciphertext is the pair $(IV, C)$.

**Random IV.** The scheme is used with a random IV when the encryptor draws $IV$ uniformly from $\{0,1\}^n$, independently for each message, and the adversary sees it only together with the ciphertext. Formally, the encryption oracle of the IND-CPA game is $M \mapsto (IV, \mathcal{E}(K, IV, M))$ with fresh $IV$, and the adversary has no control over the IV and no way to learn it before it picks $M$. Rogaway (FSE 2004) calls this probabilistic use of an IV-based scheme.

**Unpredictable IV.** SP 800-38A, Section 5.3, requires that for CBC and CFB the IV be unpredictable: for any message, it must not be possible to predict the IV that will go with it. This is the property the proofs need. A value that is random but known to the adversary before it chooses the message, for example the last ciphertext block of the previous message, is not unpredictable in this sense.

**How to make one.** SP 800-38A, Appendix C, gives two methods. (1) Apply the forward cipher, under the same key, to a nonce, and use the output as the IV. (2) Use an approved random bit generator. Method 1 is safe because $E_K$ of a fresh input is pseudorandom and the adversary does not know $K$.

### What fails when the IV is predictable

**Claim.** If the adversary can predict the IV of the next CBC encryption, CBC is not IND-CPA secure: one query gives advantage 1.

**Proof.** The adversary has seen an earlier ciphertext $(IV_1, C_1)$ whose first plaintext block $P_1$ it wants to test against a guess $G$. It knows that the next IV will be $IV_2$. It asks for the encryption of the one-block message $M = G \oplus IV_1 \oplus IV_2$. CBC computes $E_K(M \oplus IV_2) = E_K(G \oplus IV_1)$, and this equals $C_1 = E_K(P_1 \oplus IV_1)$ exactly when $G = P_1$, because $E_K$ is a permutation. In the IND-CPA game the adversary uses this to test which of two challenge messages was encrypted, and it is never wrong. $\blacksquare$

Bard (ePrint 2004/111) pointed this out for SSL 3.0 and TLS 1.0, which used the last ciphertext block of the previous record as the next IV. Duong and Rizzo turned it into the practical BEAST attack in 2011. TLS 1.1 fixed it with an explicit random IV per record. The [CBC mode](/cbc-mode/) page and its tests run this attack. The same kind of attack works on CFB: a predictable IV lets the adversary choose a first ciphertext block equal to the next IV and so learn the keystream block that the next message will use.

## Examples and non-examples

- **Example: CBC with a fresh random 128-bit IV.** Secure in the IND-CPA sense up to about $\sigma^2/2^{128}$ for $\sigma$ blocks, by the result of Bellare, Desai, Jokipii and Rogaway.
- **Example: CBC with $IV = E_K(N)$ for a message counter $N$.** The adversary cannot compute $E_K(N)$, so the IV is unpredictable. This is method 1 of SP 800-38A and the fix that Rogaway (FSE 2004) gives for turning nonce-based use of CBC into a secure scheme.
- **Non-example: CBC with $IV = 0^n$ for every message.** The scheme is deterministic, so it leaks equal messages and equal prefixes. No deterministic scheme is IND-CPA.
- **Non-example: CBC with IV equal to a counter.** Unique but predictable. The attack above applies, and in addition two messages whose first blocks differ in the same bits as their counters encrypt to the same first block.
- **Non-example: CBC with the IV chained from the previous message.** Unpredictable to a passive observer before it is sent, but known to an active adversary before it chooses the next plaintext. This is the BEAST setting.
- **Not needed: OFB and CTR.** They need only uniqueness. A random IV is allowed, but then the risk is a repeat by chance, a birthday event, see [nonce](/nonce/).
- **Not an IV: a salt.** A salt randomizes a key derivation or a password hash and is stored with the result. It plays a similar role but for key derivation, not encryption.

## Related definitions

- **[Nonce](/nonce/).** A value that must never repeat under one key but may be predictable. Modes built for nonces (CTR, GCM, CCM, ChaCha20-Poly1305) are secure with a counter. Modes built for random IVs (CBC, CFB) are not.
- **Nonce-based encryption (Rogaway, FSE 2004).** Encryption is a deterministic function of key, nonce and message, and security holds for any adversary that never repeats a nonce. This is the syntax of every modern AEAD.
- **Tweak.** A public input of a tweakable block cipher, such as the sector number in [XTS](/xts-mode/). It changes the permutation but is not sent with the ciphertext.
- **IV in GCM.** SP 800-38D calls the nonce of [GCM](/gcm-mode/) an IV, although GCM needs only uniqueness. The name IV in a standard does not tell which rule applies; the mode does.
- **[IND-CPA](/ind-cpa-security/).** The security goal that a random IV makes possible.

## References
