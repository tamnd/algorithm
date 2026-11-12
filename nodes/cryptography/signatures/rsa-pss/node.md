---
tag: CWNPMK
kind: algorithm
slug: rsa-pss
name: RSA-PSS
aliases:
- Probabilistic Signature Scheme
- RSASSA-PSS
- EMSA-PSS
area: cryptography/signatures
level: advanced
summary: "RSA signature with a random salt and a two-hash encoding (RFC 8017). Its reduction to the RSA problem in the random oracle model is tight. RFC 8017 requires it for new applications."
model: word-ram
complexity:
  vars: {b: the number of binary digits of the modulus N}
  time: {worst: Θ(b^3), average: Θ(b^3), best: Θ(b^3)}
  space: {extra: Θ(b)}
properties: {deterministic: false, randomized: true}
history:
  year: 1996
  people: [Mihir Bellare, Phillip Rogaway]
  note: "Introduced with its tight security proof at EUROCRYPT 1996. A changed version entered PKCS #1 v2.1 as RSASSA-PSS, and RFC 8017 (2016) keeps it as the scheme for new applications."
prereqs: [rsa-fdh]
see_also: [rsa-signature, rsa-oaep, random-oracle-model, rsa-problem, strong-unforgeability, rabin-signature, rsa-fault-attack, tls-handshake]
sources:
  - paper: "Mihir Bellare and Phillip Rogaway, The exact security of digital signatures: how to sign with RSA and Rabin, EUROCRYPT 1996, LNCS 1070, pages 399 to 416"
    locator: Section 4, the scheme PSS[k0, k1] and Theorem 4.1, ε = ε' + 3(q_sig + q_hash)^2 (2^-k0 + 2^-k1); Section 5, PSS-R; Section 6, PRab
  - paper: "Jean-Sébastien Coron, Optimal security proofs for PSS and other signature schemes, EUROCRYPT 2002, LNCS 2332, pages 272 to 287"
    locator: a salt of about log2 q_sig binary digits is enough for a tight reduction; FDH and other unique schemes cannot have one
  - url: "https://eprint.iacr.org/2001/053"
    title: Jakob Jonsson, Security proofs for the RSA-PSS signature scheme and its variants, Cryptology ePrint Archive, Report 2001/053
    locator: "the proofs of Bellare, Rogaway and Coron adapted to the PKCS #1 version of PSS"
  - url: "https://www.rfc-editor.org/rfc/rfc8017"
    title: "Kathleen Moriarty, Burt Kaliski, Jakob Jonsson and Andreas Rusch, RFC 8017, PKCS #1, RSA Cryptography Specifications Version 2.2, November 2016"
    locator: Section 8 (PSS is required for new applications), Section 8.1 (RSASSA-PSS, fixed salt), Section 9.1 (EMSA-PSS and Notes 1 to 5), Appendix B.2.1 (MGF1)
  - url: "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf"
    title: NIST, FIPS 186-5, Digital Signature Standard (DSS), February 2023
    locator: Section 5.4, RSASSA-PSS with an approved hash, MGF1 and a limit on the salt length
  - url: "https://www.rfc-editor.org/rfc/rfc8446"
    title: Eric Rescorla, RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3, August 2018
    locator: "Section 4.2.3, the rsa_pss schemes for handshake signatures; PKCS #1 v1.5 only in certificates"
  - url: "https://github.com/pyca/cryptography/blob/main/vectors/cryptography_vectors/asymmetric/RSA/pkcs-1v2-1d2-vec/pss-vect.txt"
    title: "RSA Laboratories, PKCS #1 v2.1 test vectors for RSASSA-PSS (pss-vect.txt)"
    locator: Example 1 (1024-bit key) with PSS Example 1.2, and Example 2 (1025-bit key) with PSS Example 2.1
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, 2020
    locator: Chapter 13, RSA-FDH and RSA signatures in practice
---

RSA-PSS (the Probabilistic Signature Scheme) signs a message by hashing it together with a random salt, building an encoded message of almost the size of the modulus from that hash with a mask generation function, and applying the RSA private operation. Bellare and Rogaway introduced it in 1996, because its reduction to the [RSA problem](/rsa-problem/) in the [random oracle model](/random-oracle-model/) is tight, while the reduction for [RSA-FDH](/rsa-fdh/) loses a factor of about the number of signatures. The version in PKCS #1, RSASSA-PSS of RFC 8017, is the RSA signature that the standard requires for new applications, and TLS 1.3 uses it for handshake signatures.

**Notation.** $N = pq$ is the modulus, $\mathit{modBits}$ its length in binary digits ($b$ in the complexity), $k = \lceil \mathit{modBits}/8 \rceil$ its length in octets, and $e$, $d$ the exponents. $\mathit{emBits} = \mathit{modBits} - 1$ and $\mathit{emLen} = \lceil \mathit{emBits}/8 \rceil$ are the length of the encoded message $EM$. $\mathrm{Hash}$ outputs $\mathit{hLen}$ octets, $\mathit{sLen}$ is the salt length in octets, and $\mathrm{MGF1}$ is the mask generation function of RFC 8017, Appendix B.2.1. $\|$ is concatenation, $\oplus$ is XOR, and $\mathtt{00}^8$ is eight zero octets. A forger runs in time $t$ with $q_s$ signing and $q_h$ hash queries and succeeds with probability $\varepsilon$; $\varepsilon'$ is the success of the derived RSA inverter.

## In plain words

Plain RSA signatures are easy to forge, and hashing the message first fixes that. The best known proof for the hashed scheme still loses strength in proportion to the number of signatures that the signer makes.

PSS adds a fresh random value, the salt, to every signature. The signer hashes the message with the salt, then stretches the hash into a long random-looking pattern that fills almost the whole RSA number. The salt is hidden inside that pattern, so the verifier can take it out and repeat the hash.

Because the salt is new each time, a forger must make a signature for a hash value that nobody has signed before. The proof can then convert every successful forgery into a solution of the RSA problem, with almost no loss. If the salt is not random, the scheme stays about as strong as the hashed scheme.

## The problem

Build a [signature scheme](/signature-scheme/) from the RSA permutation $x \mapsto x^e \bmod N$ that is [existentially unforgeable](/existential-unforgeability/) under [chosen-message attack](/chosen-message-attack/), with a reduction in which a forger with success $\varepsilon$ gives an RSA inverter with success close to $\varepsilon$ and time close to $t$. The encoding must fit below $N$, must let the verifier recover the salt, and must use only a hash function.

## The algorithm

```pseudo id=main
PSS-SIGN(sk, M)                        ▷ sk = (N, d), or its CRT form
L1  mHash ← Hash(M)
L2  if emLen < hLen + sLen + 2 then return "encoding error"
L3  salt ← sLen random octets           ▷ sLen = 0 gives the empty salt
L4  M' ← 00^8 ‖ mHash ‖ salt
L5  H ← Hash(M')
L6  DB ← 00^(emLen − sLen − hLen − 2) ‖ 01 ‖ salt
L7  maskedDB ← DB ⊕ MGF1(H, emLen − hLen − 1)
L8  set the leftmost 8·emLen − emBits binary digits of maskedDB to 0
L9  EM ← maskedDB ‖ H ‖ bc
L10 return I2OSP(OS2IP(EM)^d mod N, k)  ▷ RSASP1, with the CRT

PSS-VERIFY((N, e), M, S)
L11 if |S| ≠ k or OS2IP(S) ≥ N then return invalid
L12 m ← OS2IP(S)^e mod N; if m ≥ 256^emLen then return invalid; EM ← I2OSP(m, emLen)
L13 if emLen < hLen + sLen + 2 or the last octet of EM ≠ bc then return invalid
L14 split EM into maskedDB (emLen − hLen − 1 octets), H (hLen octets) and bc;
    if the leftmost 8·emLen − emBits binary digits of maskedDB are not 0 then return invalid
L15 DB ← maskedDB ⊕ MGF1(H, emLen − hLen − 1), with the same leftmost binary digits set to 0
L16 if DB is not 00^(emLen − hLen − sLen − 2) ‖ 01 ‖ (sLen octets) then return invalid
L17 salt ← the last sLen octets of DB; H' ← Hash(00^8 ‖ Hash(M) ‖ salt)
L18 return valid if H = H', else invalid
```

Lines L1 to L9 are EMSA-PSS-ENCODE and lines L13 to L18 are EMSA-PSS-VERIFY of RFC 8017, Section 9.1; lines L10 to L12 are the RSA layer of Section 8.1. The verifier must know $\mathit{sLen}$, the hash and the mask generation function in advance; they are part of the key's parameters, not of the signature. RFC 8017 recommends that MGF1 uses the same hash as line L1, so that an attacker cannot substitute a weaker hash.

**MGF1.** $\mathrm{MGF1}(Z, \ell)$ is the first $\ell$ octets of $\mathrm{Hash}(Z \| \mathtt{00000000}) \| \mathrm{Hash}(Z \| \mathtt{00000001}) \| \cdots$, with a 4-octet counter. It turns the short hash $H$ into a mask as long as $DB$.

**About the code.** The Python code is for study only. It is not constant time, its key generator uses a seeded non-cryptographic random source, and it must not protect real data. Use RSA-PSS from the pyca/cryptography library or from a FIPS 140 validated module. The hash comes from `hashlib`, because the page is about the signature and not the hash. The functions accept a given salt so that the tests can reproduce the official vectors; a real signer must draw the salt itself.

## Example

PSS Example 1.2 of the RSA Laboratories vectors uses a 1024-bit key, SHA-1 for the hash and for MGF1, and a salt of 20 octets. So $k = \mathit{emLen} = 128$, $\mathit{emBits} = 1023$, $\mathit{hLen} = \mathit{sLen} = 20$, and line L8 clears one binary digit. Applying $e$ to the signature of the vector (line L12) gives the encoded message, and lines L14 and L15 split it:

| part | octets | value in Example 1.2 |
|---|---|---|
| maskedDB | 107 | `5f ec ea aa 71 1c c4 a9 ...` |
| H | 20 | `06 a7 58 d5 c3 c9 21 63 bd 2c e0 18 81 0b 07 90 1a 76 2c 02` |
| trailer | 1 | `bc` |
| DB after unmasking | 107 | 86 zero octets, `01`, then the salt `ef 28 69 fa 40 c3 46 cb 18 3d ab 3d 7b ff c9 8f d5 6d f4 2d` |

The recovered salt is the one printed in the vector. Line L17 hashes $\mathtt{00}^8 \| \mathrm{SHA\text{-}1}(M) \| \mathit{salt}$ and gets the 20 octets of $H$ again, so the signature is valid. The tests check this, check that signing with the printed salt gives the printed signature, and check that a changed salt gives a different signature while a changed message, a wrong $\mathit{sLen}$ or a wrong hash makes verification fail.

The largest salt for this key and SHA-256 is $\mathit{emLen} - \mathit{hLen} - 2 = 128 - 32 - 2 = 94$ octets; with 95, line L2 returns "encoding error".

## Correctness

The proof that every signature made by the signer verifies, for every salt including the empty one, is in [proofs/correctness.md](proofs/correctness.md). It shows that line L8 keeps the encoded message below $N$, and that the verifier recovers $DB$, the salt and $H$ exactly.

**Security.** For the original scheme PSS$[k_0, k_1]$, with a salt of $k_0$ binary digits and a hash of $k_1$ binary digits, Bellare and Rogaway (1996, Theorem 4.1) prove: if RSA is $(t', \varepsilon')$-secure, then PSS is $(t, q_s, q_h, \varepsilon)$-secure with

$$t = t' - (q_s + q_h + 1) \cdot k_0 \cdot \Theta(k^3), \qquad \varepsilon = \varepsilon' + 3 (q_s + q_h)^2 \cdot (2^{-k_0} + 2^{-k_1}),$$

where $k$ is the length of $N$ in binary digits. The forger's success maps to the inverter's success with only an additive loss, which is tiny for $k_0 = k_1 = 160$. The idea: the inverter answers each hash query on a new (message, salt) pair with a value that has the RSA challenge $y$ planted in it, and it answers each signing query by choosing the salt itself and programming the hash so that it knows the $e$-th root. A forgery needs a valid encoding for a (message, salt) pair that the signer did not use, and every such pair carries $y$, so the inverter does not have to guess, unlike in the FDH proof.

- **Coron (2002)** shows that a salt of about $\log_2 q_s$ binary digits already gives a tight reduction, and that with no salt the loss of about $q_s$ is unavoidable, as for FDH.
- **Jonsson (2001)** adapts these proofs to the PKCS #1 version, which hashes $\mathtt{00}^8 \| \mathrm{Hash}(M) \| \mathit{salt}$, puts the salt inside $DB$ and adds the trailer octet $\mathtt{bc}$.
- **RFC 8017, Section 8.1** states that randomness is not critical: with a fixed salt or a counter, security is similar to that of FDH.

## Complexity

The cost is that of one RSA operation, $\Theta(b^3)$ for signing with schoolbook arithmetic, plus a few hash calls: one pass over the message, one hash of $8 + \mathit{hLen} + \mathit{sLen}$ octets, and $\lceil (\mathit{emLen} - \mathit{hLen} - 1)/\mathit{hLen} \rceil$ hashes in MGF1. Verification with $e = 65537$ is 17 modular multiplications, $\Theta(b^2)$, plus the same hashes. The signature has $k$ octets, the same as for PKCS #1 v1.5.

| operation | cost |
|---|---|
| sign | 1 private RSA exponentiation (2 of half size with the CRT), 2 hashes and MGF1 |
| verify | 1 exponentiation by $e$, 2 hashes and MGF1 |
| signature size | $k$ octets |

## Properties

- **Randomized.** With $\mathit{sLen} > 0$, two signatures on the same message differ (the tests check this). With $\mathit{sLen} = 0$ the scheme is deterministic.
- **Tight proof in the ROM.** The reduction to RSA loses only an additive term, under the condition that the salt is random and long enough.
- **Salt recovery.** The verifier gets the salt from the signature, so no extra field is sent.
- **Hash in a separate module.** RFC 8017, Section 9.1, Note 3: the proof still holds if an attacker controls $\mathit{mHash}$, so a smart card can receive only the digest.
- **Not unique.** Each message has many valid signatures, one per salt. A second valid signature on a signed message needs a new salt, and therefore a new hash point that carries the RSA challenge in the proof, which is why the same argument also gives [strong unforgeability](/strong-unforgeability/) in the random oracle model.

## Variants and improvements

- **PSS-R.** Bellare and Rogaway (1996, Section 5) also give a version with message recovery: part of the message is placed in the encoding instead of the salt area, which saves space.
- **PRab.** The same encoding with Rabin's squaring instead of RSA (Bellare and Rogaway 1996, Section 6). The 0xbc trailer of RFC 8017 was chosen for compatibility with the Rabin-Williams primitive of IEEE 1363; see [Rabin signatures](/rabin-signature/).
- **Salt length choices.** $\mathit{sLen} = \mathit{hLen}$ is typical, $\mathit{sLen} = 0$ gives a deterministic scheme with FDH-like security, and the maximum length fills $DB$. RFC 8017, Section 9.1, Note 4 names $\mathit{hLen}$ and 0 as the typical values.
- **Probabilistic FDH.** Signs $H(M \| r)$ with a random $r$ sent beside the signature; it has the same kind of tight proof but a longer signature.
- **RSA-OAEP.** The encryption counterpart from Bellare and Rogaway (1994), with a similar two-function masking structure; see [RSA-OAEP](/rsa-oaep/).

## When to use it

Use RSA-PSS for every new RSA signature: RFC 8017, Section 8 requires it for new applications and keeps RSASSA-PKCS1-v1_5 for compatibility, FIPS 186-5 approves it, and TLS 1.3 uses it for every RSA signature in the [handshake](/tls-handshake/). For a new design without a need for RSA, elliptic-curve schemes such as [Ed25519](/ed25519/) are smaller and faster, and lattice schemes such as [Dilithium](/crystals-dilithium/) resist quantum computers. RSA-PSS, like all RSA signatures, can be broken by a large quantum computer.

## Pitfalls

- **Salt length disagreement.** The verifier must use the signer's $\mathit{sLen}$. Libraries differ: some sign with the maximum length by default and others with $\mathit{hLen}$. A wrong value makes valid signatures fail, as the test with $\mathit{sLen} = 19$ shows. Some verifiers recover the salt length from $DB$ automatically.
- **Hash substitution.** Unlike PKCS #1 v1.5, the encoding does not name the hash. Fix the hash for the key and use the same hash in MGF1, as RFC 8017 recommends.
- **Incomplete checks.** A verifier must check the length of $S$, $s < N$, the cleared leftmost binary digits, the zero octets, the $\mathtt{01}$ separator and the trailer. Skipping a check lets through encodings that the proof does not cover.
- **Weak salt.** A predictable salt does not break the scheme, but it removes the tight proof. Unlike the nonce of [DSA](/dsa/) or [ECDSA](/ecdsa/), a repeated salt does not reveal the key, because the salt is public.
- **Faults.** A fault in the CRT computation of line L10 can reveal a factor of $N$; verify each signature before release ([RSA fault attack](/rsa-fault-attack/)).
- **Covert channel.** RFC 8017, Section 9.1, Note 5: a dishonest signing device can hide data in the salt.

## Implementations

The Python code gives `mgf1`, `emsa_pss_encode` (lines L1 to L9), `emsa_pss_verify` (lines L13 to L18), `sign` (line L10, with the CRT), `verify` (lines L11 and L12, then EMSA-PSS-VERIFY), and a seeded toy key generator. The tests use vectors copied by hand from `pss-vect.txt` of RSA Laboratories:

- PSS Example 1.2 with the printed salt, for signing and verification;
- PSS Example 2.1 on the 1025-bit key, for verification only, where $\mathit{emLen} = k - 1$;
- changed salts, messages, salt lengths and hashes, and single bit flips in the signature;
- round trips with SHA-256 for salt lengths 0, 20, 32 and 62, and the "encoding error" for a salt one octet too long.

## History

Bellare and Rogaway presented PSS, PSS-R and PRab at EUROCRYPT 1996, with exact security bounds that made the case for a salted encoding over FDH. They submitted PSS to IEEE P1363a. PKCS #1 v2.1 (2002) adopted a changed version as RSASSA-PSS, with the message hashed first, the salt inside $DB$ and the trailer octet $\mathtt{bc}$; Jonsson adapted the security proofs to it. Coron (2002) showed that a short salt suffices. RFC 8017 (2016, PKCS #1 v2.2) keeps PSS as the required scheme for new applications, TLS 1.3 (2018) made it the only RSA signature for handshake messages, and FIPS 186-5 (2023) approves it beside RSASSA-PKCS1-v1_5.

## References
