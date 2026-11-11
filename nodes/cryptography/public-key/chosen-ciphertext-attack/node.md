---
tag: PWVD1W
kind: concept
slug: chosen-ciphertext-attack
name: Chosen-ciphertext attack
aliases:
area: cryptography/public-key
level: advanced
summary: The attack model in which the adversary gets decryptions, or only a valid or invalid answer, for ciphertexts of its choice. Bleichenbacher, Vaudenay and EFAIL are real cases.
prereqs: [public-key-encryption, chosen-plaintext-attack]
see_also: [ind-cca-security, padding-oracle-attack, non-malleability, rsa-pkcs1-v1-5-encryption, rsa-oaep, authenticated-encryption, timing-attack, cbc-mode]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 8, Section 8.1.1 (indifferent and adaptive chosen-ciphertext attacks), Section 8.2.2 (v) (the attack on RSA), Note 8.13 (ii) (the attack on Rabin)
  - paper: "Daniel Bleichenbacher, Chosen ciphertext attacks against protocols based on the RSA encryption standard PKCS #1, CRYPTO 1998, LNCS 1462, pages 1 to 12"
    locator: the attack with a padding validity oracle on PKCS #1 v1.5 in SSL 3.0
  - paper: "Serge Vaudenay, Security flaws induced by CBC padding, applications to SSL, IPSEC, WTLS, EUROCRYPT 2002, LNCS 2332, pages 534 to 545"
    locator: the padding oracle attack on CBC mode
  - paper: "James Manger, A chosen ciphertext attack on RSA optimal asymmetric encryption padding (OAEP) as standardized in PKCS #1 v2.0, CRYPTO 2001, LNCS 2139, pages 230 to 238"
    locator: the attack with an oracle that reports whether the first byte is zero
  - paper: "Damian Poddebniak, Christian Dresen, Jens Müller, Fabian Ising, Sebastian Schinzel, Simon Friedberger, Juraj Somorovsky and Jörg Schwenk, Efail, breaking S/MIME and OpenPGP email encryption using exfiltration channels, USENIX Security 2018"
    locator: the CBC and CFB malleability gadgets and the exfiltration channels
  - paper: "Hanno Böck, Juraj Somorovsky and Craig Young, Return of Bleichenbacher's oracle threat (ROBOT), USENIX Security 2018"
    locator: the scan of TLS servers that still gave a PKCS #1 v1.5 oracle
  - paper: "Moni Naor and Moti Yung, Public-key cryptosystems provably secure against chosen ciphertext attacks, STOC 1990, pages 427 to 437"
    locator: the lunchtime (non-adaptive) chosen-ciphertext model
  - paper: "Charles Rackoff and Daniel R. Simon, Non-interactive zero-knowledge proof of knowledge and chosen ciphertext attack, CRYPTO 1991, LNCS 576, pages 433 to 444"
    locator: the adaptive chosen-ciphertext model
  - paper: "Tibor Jager, Jörg Schwenk and Juraj Somorovsky, Practical invalid curve attacks on TLS-ECDH, ESORICS 2015"
    locator: key recovery from a decryption oracle that does not check points
---

A chosen-ciphertext attack (CCA) is an attack in which the adversary can make the victim decrypt ciphertexts of the adversary's choice and learn something about the result: the whole plaintext, or only whether decryption succeeded. Servers, mail clients and smart cards that decrypt whatever arrives give such an oracle, so this model describes real attackers, not only theorists. Textbook RSA and ElGamal fall to it with one query, PKCS #1 v1.5 and CBC padding fall to it with a one-bit oracle, and the defence is a scheme that is [IND-CCA secure](/ind-cca-security/). This page describes the model and the attacks; the formal definition is on the IND-CCA page.

**Notation.** $c^*$ is the target ciphertext and $m^*$ its plaintext. $\mathcal{A}$ is the adversary, $q_d$ its number of decryption queries, and $t$ its time. $(n, e, d)$ is an RSA key, $(p, q, g, h = g^x)$ an ElGamal key with $q$ the prime order of $g$. All attacks below are against the real schemes, in the standard model; none uses a random oracle.

## In plain words

An attacker has captured a locked message and wants to read it. It cannot ask the receiver to open that exact message, but it can send the receiver other locked messages of its own making and watch what happens. Sometimes it gets the full opened text back. Sometimes it only sees whether the receiver accepted the message or complained.

If the attacker can change the captured message in a controlled way and the receiver opens the changed one, the attacker can often undo the change and read the original. Even a yes or no answer, repeated many thousands of times, can reveal the whole message. A scheme that resists this must make every changed message useless: the receiver must reject it, and the rejection must not leak anything.

## The idea

**Kinds of oracle.** The attacker may have

- a *decryption oracle*, which returns $\mathrm{Dec}(sk, c)$ for any $c \ne c^*$;
- a *validity oracle*, which returns only whether $\mathrm{Dec}(sk, c) \ne \bot$, often through an error message, a different alert, or a timing difference. This is a [padding oracle](/padding-oracle-attack/) when validity means correct padding;
- a *partial oracle*, which reveals some function of the plaintext, for example whether a server parsed it as HTML and loaded a link.

**When the oracle is available.** Handbook of Applied Cryptography (Section 8.1.1) separates an *indifferent* attack, where all queries come before the target ciphertext is seen, from an *adaptive* attack, where queries continue after it. Naor and Yung (1990) formalized the first as the "lunchtime" attack (CCA1): the attacker uses the decryption box while the owner is at lunch. Rackoff and Simon (1991) formalized the second (CCA2). Only the target itself is excluded.

**Why it works.** Most attacks use one of three weaknesses.

1. *Malleability.* A known change of the ciphertext causes a known change of the plaintext. The attacker turns $c^*$ into a different $c'$, gets $m'$, and computes $m^*$ from $m'$. See [non-malleability](/non-malleability/).
2. *Leaky rejection.* The decryptor rejects badly formed plaintexts, and the reason for the rejection, or its timing, depends on the plaintext. Each query then gives a bit of information about a value related to $m^*$.
3. *Missing checks.* The decryptor uses an input that is not in the expected group, for example a point on another curve, and its answer reveals the private key modulo a small number.

Attacks of the third kind recover the key itself, so one success breaks every past and future ciphertext.

**The defence.** Use a scheme proved [IND-CCA](/ind-cca-security/) secure: [RSA-OAEP](/rsa-oaep/), [Cramer-Shoup](/cramer-shoup-cryptosystem/), [ECIES](/ecies/), a KEM made with the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/), or [hybrid encryption](/hybrid-encryption/) with [authenticated encryption](/authenticated-encryption/). Implement it so that every rejection looks the same and takes the same time, and check that inputs lie in the right group.

## Examples

**Textbook RSA, one query.** RSA is multiplicative: $(c \cdot s^e)^d = m s \bmod n$. Take the toy key $n = 3233 = 61 \cdot 53$, $e = 17$, $d = 2753$ and the target $c^* = 65^{17} \bmod 3233 = 2790$.

| step | computation | value |
|---|---|---|
| choose $s$ | $s = 2$, $s^e \bmod n$ | 1752 |
| changed ciphertext | $c' = 2790 \cdot 1752 \bmod 3233$ | 3017 |
| oracle answer | $3017^{2753} \bmod 3233$ | 130 |
| undo the change | $130 \cdot 2^{-1} \bmod 3233$ | 65 |

Handbook of Applied Cryptography (Section 8.2.2 (v)) attributes this attack to Davida. A random $s$ also hides the relation from the victim.

**ElGamal, one query.** $(c_1, t c_2)$ decrypts to $t m^*$ for any $t$ in the group, so the attacker divides the answer by $t$. The [ElGamal](/elgamal-encryption/) page has the numbers.

**Rabin and Blum-Goldwasser, key recovery.** For [Rabin](/rabin-cryptosystem/), the attacker picks $m$, asks for the decryption of $m^2 \bmod n$, and gets a square root $y$. With probability $\tfrac12$, $y \ne \pm m$ and $\gcd(y - m, n)$ is a factor of $n$ (Note 8.13 (ii)). [Blum-Goldwasser](/blum-goldwasser-cryptosystem/) has the same weakness (Note 8.58 (iii)).

**Bleichenbacher 1998.** SSL 3.0 servers decrypted an RSA PKCS #1 v1.5 key exchange message and sent a different alert when the plaintext did not start with the bytes 00 02. This validity oracle, together with the multiplicative property, lets the attacker narrow the set of possible plaintexts of $c^* s^e$ for a sequence of values $s$ until one value remains. The paper estimated about one million queries for a 1024-bit key, hence the name "million message attack". ROBOT (2018) found the same oracle in many TLS servers twenty years later. See [RSA PKCS #1 v1.5 encryption](/rsa-pkcs1-v1-5-encryption/).

**Manger 2001.** An implementation of RSA-OAEP that reveals whether the integer $c^d \bmod n$ is below $2^{8(k-1)}$, for example through a distinct error code, lets the attacker recover $m$ with about $\log_2 n$ queries. OAEP is IND-CCA secure; the leak in the implementation is not covered by the proof.

**Vaudenay 2002.** For [CBC mode](/cbc-mode/) with padding, a server that tells whether the padding of a decrypted message is valid lets the attacker recover each plaintext byte with at most 256 queries, by changing the previous ciphertext block. It applied to SSL, IPsec and WTLS, and later to ASP.NET and XML Encryption. This is a symmetric attack, but it is the same model.

**EFAIL 2018.** S/MIME and OpenPGP used CBC or CFB without a check of integrity before decryption. An attacker changes captured ciphertext blocks to insert an HTML image tag around the unknown plaintext; the mail client decrypts it and sends the plaintext to the attacker's server as part of a URL. The partial oracle here is the client's HTML renderer.

**Invalid curve attacks.** A TLS server that does elliptic curve Diffie-Hellman with a static key and does not check that the client's point is on the curve computes $x \cdot P$ for a point $P$ of small order on another curve. Each answer reveals $x$ modulo that small order, and the Chinese remainder theorem gives $x$ (Jager, Schwenk and Somorovsky, 2015). See [elliptic curve cryptography](/elliptic-curve-cryptography/) and the [small subgroup attack](/small-subgroup-attack/).

## Where it is used

- **Security definitions.** The model gives [IND-CCA1 and IND-CCA2](/ind-cca-security/) and NM-CCA. Proofs of [Cramer-Shoup](/cramer-shoup-cryptosystem/), OAEP, [Fujisaki-Okamoto](/fujisaki-okamoto-transform/) and [Naor-Yung](/naor-yung-paradigm/) schemes show that no chosen-ciphertext attacker succeeds.
- **Protocol design.** TLS 1.3 removed RSA key transport and CBC cipher suites, the two sources of the Bleichenbacher and Vaudenay oracles. HPKE, JOSE and CMS now recommend KEMs and AEADs.
- **Implementation review.** A reviewer asks for every decryption path what an attacker can observe: error codes, alerts, timing, and side effects such as loaded links. A [timing attack](/timing-attack/) can turn a correct scheme into an oracle.
- **Key-recovery tests.** Libraries test that they reject points off the curve, values out of range and malformed paddings, because these are the inputs a chosen-ciphertext attacker sends.

## References
