---
tag: Z5A66M
kind: definition
slug: chosen-message-attack
name: Chosen-message attack
aliases:
- CMA
- adaptive chosen-message attack
- non-adaptive chosen-message attack
- generic chosen-message attack
- directed chosen-message attack
area: cryptography/signatures
level: core
summary: The adversary gets signatures on messages of its choice, all at once or one after another, and then tries to forge a signature on a message it did not submit.
prereqs: [signature-scheme]
see_also: [existential-unforgeability, key-only-attack, strong-unforgeability, rsa-signature, signature-forgery, rsa-fdh, chosen-prefix-collision, blind-signature]
sources:
  - paper: "Shafi Goldwasser, Silvio Micali and Ronald L. Rivest, A digital signature scheme secure against adaptive chosen-message attacks, SIAM Journal on Computing 17(2), pages 281 to 308, 1988"
    locator: Section 3, key-only attacks and the message attacks (known-message, generic chosen-message, directed chosen-message, adaptive chosen-message), and the first scheme proved secure against the adaptive attack
  - paper: "Yvo Desmedt and Andrew M. Odlyzko, A chosen text attack on the RSA cryptosystem and some discrete logarithm schemes, CRYPTO 1985, LNCS 218, pages 516 to 522"
    locator: signatures on messages that factor over a set of small primes give signatures on other such messages
  - paper: "Jean-Sebastien Coron, David Naccache and Julien P. Stern, On the security of RSA padding, CRYPTO 1999, LNCS 1666, pages 1 to 18"
    locator: the chosen-message attack on RSA signatures with short encodings, applied to ISO/IEC 9796-2
  - paper: "Jean-Sebastien Coron, David Naccache, Mehdi Tibouchi and Ralf-Philipp Weinmann, Practical cryptanalysis of ISO/IEC 9796-2 and EMV signatures, CRYPTO 2009, LNCS 5677, pages 428 to 444"
    locator: a chosen-message forgery of ISO/IEC 9796-2 scheme 1 that was run in practice
  - paper: "Dan Boneh and Xavier Boyen, Short signatures without random oracles and the SDH assumption in bilinear groups, Journal of Cryptology 21(2), pages 149 to 177, 2008"
    locator: the weakly secure scheme g^(1/(x+m)), proved secure when the adversary sends all its messages before it sees the public key, and its fully secure extension
  - paper: "Susan Hohenberger and Brent Waters, Short and stateless signatures from the RSA assumption, CRYPTO 2009, LNCS 5677, pages 654 to 670"
    locator: the step from security against a non-adaptive (weak) chosen-message attack to full security with a chameleon hash, credited to Krawczyk and Rabin
  - url: "https://www.rfc-editor.org/rfc/rfc8017"
    title: "Kathleen Moriarty, Burt Kaliski, Jakob Jonsson and Andreas Rusch, RFC 8017, PKCS #1 Version 2.2, November 2016"
    locator: Section 8.2.2 (RSASSA-PKCS1-v1_5 verification, which compares the whole encoded block), Section 9.2 Note 1 (the DigestInfo prefixes)
  - url: "https://mailarchive.ietf.org/arch/msg/openpgp/5rnE9ZRN1AokBVj3VqblGlP63QE/"
    title: Hal Finney, Bleichenbacher's RSA signature forgery based on implementation error, message to the IETF OpenPGP list, August 2006
    locator: "the description of the e = 3 forgery of PKCS #1 v1.5 against verifiers that do not check that the hash ends the block"
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 11.2.4, types of attacks on signature schemes, and Note 11.15 on the adaptive chosen-message attack
---

A chosen-message attack is an attack model for a [signature scheme](/signature-scheme/) in which the adversary can get signatures on messages of its choice from the signer, and then tries to produce a valid signature that the signer did not give. In the *adaptive* form each message may depend on the signatures already received; in the *non-adaptive* forms the messages are fixed in advance. The adaptive form is the standard attack model: [existential unforgeability](/existential-unforgeability/) under it, EUF-CMA, is the usual security goal for signatures.

**Notation.** $\Pi = (\mathrm{KeyGen}, \mathrm{Sign}, \mathrm{Verify})$ is a signature scheme, $\lambda$ the security parameter, and $A$ an adversary that runs in time $t$ and makes $q_s$ signing queries. $Q$ is the set of messages that $A$ submitted. For RSA, $(N, e)$ is the public key and $d$ the private exponent.

## Definition

**The game $\mathrm{Exp}^{\mathrm{euf\text{-}cma}}_{\Pi, A}(\lambda)$ (adaptive).**

1. The challenger runs $(pk, sk) \leftarrow \mathrm{KeyGen}(1^\lambda)$ and sets $Q \leftarrow \emptyset$.
2. The challenger runs $A(pk)$ with access to a signing oracle. When $A$ submits $m$, the challenger returns $\sigma \leftarrow \mathrm{Sign}(sk, m)$ and adds $m$ to $Q$. $A$ may choose each query after it sees the answers to the earlier ones.
3. $A$ outputs $(m^*, \sigma^*)$.
4. The game outputs 1 if $\mathrm{Verify}(pk, m^*, \sigma^*) = 1$ and $m^* \notin Q$, and 0 otherwise.

$\Pi$ is EUF-CMA secure if $\Pr[\mathrm{Exp}^{\mathrm{euf\text{-}cma}}_{\Pi, A}(\lambda) = 1]$ is negligible for every probabilistic polynomial-time $A$. If step 4 asks only that $(m^*, \sigma^*)$ is not a pair that the oracle returned, the goal is [strong unforgeability](/strong-unforgeability/).

**Non-adaptive forms.** Goldwasser, Micali and Rivest (1988) name two weaker forms, in which $A$ sends all of $m_1, \ldots, m_{q_s}$ at once and receives all the signatures together.

- **Generic chosen-message attack.** The list is fixed before $A$ sees $pk$. Security in this game is often called *weak* security, as in Boneh and Boyen.
- **Directed chosen-message attack.** The list is chosen after $A$ sees $pk$, but before any signature.

**The order of strength.** Each game gives the adversary at least as much power as the one before it: key-only, known-message (signatures on messages that $A$ did not choose), generic, directed, adaptive. So security in a later game implies security in each earlier one, and the adaptive game gives the strongest guarantee. A scheme that is secure only against a generic attack can be made secure against the adaptive attack by signing the output of a chameleon hash of the message instead of the message, a method credited to Krawczyk and Rabin.

**Why the model is realistic.** Real signers often sign data that others choose in part: a certification authority signs a certificate request, a TLS server signs a handshake transcript that includes the client's random value, and a hardware token signs what the host sends. The rogue CA attack of 2008 used exactly this: the attackers sent a certificate request whose MD5 hash collided with that of a certificate they had built, and the signature on the request was also valid on their certificate. See [signature forgery](/signature-forgery/) and [chosen-prefix collision](/chosen-prefix-collision/).

## Examples and non-examples

- **Textbook RSA under a generic attack.** The signature of an integer $m$ is $m^d \bmod N$, and $(m_1 m_2)^d = m_1^d m_2^d$. So signatures on $m_1$ and $m_2$ give a signature on $m_1 m_2 \bmod N$ without the key. With the toy key $N = 3233 = 61 \cdot 53$, $e = 17$, $d = 2753$: the queries $2$ and $3$ return $1027$ and $1857$, and $1027 \cdot 1857 \bmod 3233 = 2902$ is the signature of the new message $6$, since $2902^{17} \bmod 3233 = 6$. The queries do not depend on the key, so this is a generic attack.
- **Textbook RSA under a directed attack.** To sign a target $m$, pick $r$ coprime to $N$ and ask for the signature $s'$ of $m' = m r^e \bmod N$. Then $s' = m^d r$, and $s = s' r^{-1} \bmod N$ signs $m$, which was never submitted. With $m = 100$ and $r = 5$ on the toy key: $m' = 1465$, $s' = 489$, and $s = 489 \cdot 5^{-1} \bmod 3233 = 1391 = 100^{2753} \bmod 3233$. One query gives a universal forgery. The same blinding gives Chaum's [blind signature](/blind-signature/), where the signer agrees to it.
- **Short encodings are not safe.** Desmedt and Odlyzko (1985) noted that if encoded messages are small, many of them factor over a set of small primes, and signatures on some of them give signatures on others by multiplication. Coron, Naccache and Stern (1999) applied this to RSA with the encodings of ISO/IEC 9796-2, and Coron, Naccache, Tibouchi and Weinmann (2009) ran such a forgery of ISO/IEC 9796-2 scheme 1 in practice.
- **Full-domain encodings resist it.** [RSA-FDH](/rsa-fdh/) and [RSA-PSS](/rsa-pss/) map each message to a value spread over $\mathbb{Z}_N$ by a hash, which breaks the multiplicative relation. Both are proved EUF-CMA in the random oracle model if the RSA function is hard to invert. The GMR scheme (1988) was the first one proved secure against the adaptive attack, without random oracles, under the hardness of factoring.
- **Weak security, proved.** The Boneh-Boyen signature $\sigma = g_1^{1/(x + m)}$ is proved secure only against a generic chosen-message attack, under the strong Diffie-Hellman assumption. Their fully secure scheme adds a random value to the exponent.
- **A broken verifier needs no query.** Bleichenbacher (2006) showed that some RSA verifiers for PKCS #1 v1.5 with $e = 3$ read the block $\mathtt{00}\ \mathtt{01}\ \mathtt{FF} \ldots \mathtt{FF}\ \mathtt{00}\ \mathit{DigestInfo}\ H(m)$ from the left and do not check that $H(m)$ ends it. A forger then needs an integer $s$ whose cube starts with $\mathtt{00}\ \mathtt{01}\ \mathtt{FF}\ \mathtt{00}\ \mathit{DigestInfo}\ H(m)$ and may end with anything: it is the integer cube root of the top of that range, and no reduction modulo $N$ takes place. This is a key-only attack on the implementation, not a chosen-message attack; it is here as a contrast, because a scheme that is EUF-CMA on paper can still fall to an adversary with no oracle if the verifier is wrong. With SHA-256 and a modulus of 2048 binary digits, the fixed part takes 55 bytes and leaves 201 bytes, or 1608 binary digits, free. Near the target the gap between consecutive cubes is about $3 s^2 \approx 2^{1357}$, far smaller than $2^{1608}$, so a cube lies in the range. With 1024 binary digits only 584 binary digits are free, less than the gap of about $2^{674}$, and this simple form fails. A verifier that rebuilds the whole expected block and compares it, as RFC 8017, Section 8.2.2 says, rejects the forgery.

**The code.** The implementation folder has a signing oracle that records its queries, the generic and directed forgeries on textbook RSA, a PKCS #1 v1.5 encoder with SHA-256, the right verifier, a flawed verifier of the 2006 kind, and the cube-root forgery. The tests check the toy values above, the same forgeries on a test key of 2048 binary digits with $e = 3$ made from a fixed seed, that the cube-root forgery passes only the flawed verifier, and that it has no room with a modulus of 1024 binary digits. No official vector exists for these attacks; the DigestInfo prefix is copied from RFC 8017, Section 9.2, Note 1. The code is for study only, is not constant time, and runs only against local simulated verifiers.

## Related definitions

- **[Key-only attack](/key-only-attack/).** The adversary has only the public key. It is the weakest attack model.
- **Known-message attack.** The adversary gets signatures on messages that it did not choose, for example random messages or messages from a fixed distribution.
- **[Existential unforgeability](/existential-unforgeability/).** The goal that is usually paired with the adaptive chosen-message attack.
- **[Strong unforgeability](/strong-unforgeability/).** The same attack with a stronger goal: a new signature on a queried message also counts.
- **Chosen-ciphertext attack.** The analogue for encryption, where the adversary gets decryptions of ciphertexts of its choice. For textbook RSA the two are the same operation, which is why the same multiplicative trick works for both.

## References
