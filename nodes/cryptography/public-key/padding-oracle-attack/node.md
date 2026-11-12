---
tag: 88GNSJ
kind: concept
slug: padding-oracle-attack
name: Padding oracle attack
aliases:
- Bleichenbacher attack
area: cryptography/public-key
level: advanced
summary: "A receiver that says whether the padding of a ciphertext was correct lets an attacker decrypt it. The class covers CBC mode and RSA PKCS #1 v1.5."
history:
  year: 1998
  people: [Daniel Bleichenbacher, Serge Vaudenay]
  note: Bleichenbacher gave the RSA version in 1998 and Vaudenay the CBC version in 2002. The class has broken SSL, TLS, IPsec, WTLS, XML encryption, ASP.NET, S/MIME and OpenPGP mail.
prereqs: [cbc-mode, pkcs7-padding]
see_also: [rsa-pkcs1-v1-5-encryption, chosen-ciphertext-attack, authenticated-encryption, ind-cca-security, timing-attack, rsa-oaep, tls-handshake]
sources:
  - paper: "Serge Vaudenay, Security flaws induced by CBC padding, applications to SSL, IPSEC, WTLS, EUROCRYPT 2002, LNCS 2332, pages 534 to 545"
    locator: Sections 2 and 3 (the padding oracle, the one block decryption with about 128 queries for each octet, and the applications)
  - paper: "Daniel Bleichenbacher, Chosen ciphertext attacks against protocols based on the RSA encryption standard PKCS #1, CRYPTO 1998, LNCS 1462, pages 1 to 12"
    locator: Section 3 (the oracle and the interval search)
  - url: "https://openssl-library.org/files/ssl-poodle.pdf"
    title: Bodo Möller, Thai Duong and Krzysztof Kotowicz, This POODLE bites, exploiting the SSL 3.0 fallback, 2014
    locator: Section 2 (the SSL 3.0 padding has no value check, so one octet needs about 256 requests)
  - paper: "Nadhem J. AlFardan and Kenneth G. Paterson, Lucky Thirteen, breaking the TLS and DTLS record protocols, IEEE Symposium on Security and Privacy 2013, pages 526 to 540"
    locator: Sections 3 and 4 (the timing difference from the number of hash compression calls, and the attack with many sessions)
  - url: "https://csrc.nist.gov/pubs/sp/800/38/a/final"
    title: Morris Dworkin, NIST Special Publication 800-38A, Recommendation for Block Cipher Modes of Operation, Methods and Techniques, 2001
    locator: Section 6.2 and Appendix F.2.1 (CBC mode and the AES-128 CBC example used by the code of this page)
  - url: "https://www.rfc-editor.org/rfc/rfc7366"
    title: Peter Gutmann, RFC 7366, Encrypt-then-MAC for Transport Layer Security (TLS) and Datagram Transport Layer Security (DTLS), 2014
    locator: Sections 1 and 3 (why MAC-then-encrypt is the problem, and the extension that swaps the order)
---

A padding oracle attack decrypts a ciphertext with the help of one bit: did the padding check of the receiver pass or fail. The attacker sends many changed copies of the target ciphertext, collects the answers, and recovers the plaintext without the key. The two classic members of the class are the [CBC](/cbc-mode/) attack of Vaudenay (2002), which breaks [PKCS #7 padding](/pkcs7-padding/) in SSL, IPsec and WTLS, and the RSA attack of Bleichenbacher (1998) on [PKCS #1 v1.5](/rsa-pkcs1-v1-5-encryption/). The lesson of both is the same: a decryption that reports why it failed is not [IND-CCA](/ind-cca-security/) secure, and the fix is [authenticated encryption](/authenticated-encryption/).

## In plain words

Encrypted data usually has filler at the end, so that its length fits the cipher. The receiver removes the filler and complains if it looks wrong. That complaint is the whole problem.

An attacker takes a captured ciphertext, changes one byte, and sends it. The answer "bad filler" or "accepted" depends on the secret plaintext in a way the attacker can work out. By trying the 256 values of one byte, the attacker learns one byte of the plaintext. Repeat for each byte, and the whole message comes out. The attacker needs no key.

The fix is to check a message authentication code before anything else, or to use a cipher mode that does both jobs. Then a changed ciphertext is thrown away before the filler is ever looked at, and the answer carries no information.

## The idea

Let $\mathrm{Dec}_K$ be a decryption that first inverts the cipher and then checks a structure, which can be a padding, a fixed prefix or a hash. The attacker gets access to

$$\mathcal{O}(C) = \begin{cases} 1 & \text{the structure check on } \mathrm{Dec}_K(C) \text{ passes},\\ 0 & \text{otherwise.}\end{cases}$$

Three conditions make the oracle useful:

1. **The ciphertext is malleable.** The attacker can change the ciphertext so that the plaintext changes in a known way. CBC gives this by the exclusive or with the previous block; RSA gives it by the product $c \cdot s^e$.
2. **The plaintext has a structure that is checked.** The check must accept a thin set of plaintexts, so that "accepted" says much.
3. **The answer is visible.** An error message, an error code, a connection reset, a timing difference or any later step that fails only for a bad padding.

### The CBC case

CBC decryption gives $P_i = D_K(C_i) \oplus C_{i-1}$, where $D_K$ is the block cipher decryption and $C_0$ is the IV. The attacker wants $D_K(C_i)$, since $P_i$ follows from it and from the public $C_{i-1}$. Send the two block ciphertext $R \Vert C_i$, where $R$ is chosen by the attacker. The receiver computes

$$P' = D_K(C_i) \oplus R$$

and checks the padding of $P'$. Work on the last octet first. Try all 256 values of $R[15]$. For exactly one or two of them the last octet of $P'$ is $\texttt{0x01}$, which is a valid PKCS #7 padding, so

$$D_K(C_i)[15] = R[15] \oplus \texttt{0x01} .$$

A second value can pass, because a plaintext that ends in $\texttt{0x02}\,\texttt{0x02}$ or in a longer run is also valid. To tell the two apart, flip a bit in $R[14]$ and ask again: a padding of one octet still passes, a longer one breaks. With octet 15 known, set $R[15] = D_K(C_i)[15] \oplus \texttt{0x02}$ and search $R[14]$ for the padding $\texttt{0x02}\,\texttt{0x02}$, and so on down to octet 0. Each octet costs at most 256 queries and about 128 on average, so a block costs about 2048 queries and the whole message about $128$ queries for each octet. The attacker never learns $K$.

The same forgery in the other direction gives an encryption oracle: with $D_K(C_i)$ known for a block of a captured ciphertext, the attacker can build a ciphertext that decrypts to a chosen plaintext block, which is how the ASP.NET attack of 2010 downloaded files.

### The RSA case

Here the structure is the $\texttt{0x00}\,\texttt{0x02}$ prefix of the [v1.5 encoding](/rsa-pkcs1-v1-5-encryption/). The malleability is $c' = c \cdot s^e \bmod N$, which gives the plaintext $ms \bmod N$. An answer of 1 means $2B \le ms \bmod N < 3B$, which bounds $m$ in a short interval; the search keeps a set of intervals and shrinks it. The structure of the search is different from the CBC case, because the information is an interval and not an octet, but the three conditions above are the same. The [OAEP](/rsa-oaep/) page has the matching story for Manger's attack, where the leaked bit is whether the plaintext integer is above $2^{8(k-1)}$.

### The fix

- **Check a MAC first.** Encrypt-then-MAC (RFC 7366) computes the tag over the ciphertext, so a changed ciphertext is thrown away before any padding is seen. The decryption has one error, and it does not depend on the plaintext.
- **Use an AEAD.** [GCM](/gcm-mode/) or [ChaCha20-Poly1305](/chacha20-poly1305/) do both jobs in one pass, with no padding at all. TLS 1.3 allows nothing else.
- **For public-key encryption, remove the check.** A [KEM](/key-encapsulation-mechanism/) with implicit rejection returns a pseudorandom key for a bad ciphertext, so there is no failure bit. This is the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) idea, and RSA-KEM and ML-KEM both do it.
- **If you cannot change the design**, make the failure invisible: one error value, one code path, and the same work in both cases. Twenty five years of broken attempts say that this is the weakest of the four options.

## Examples

**A toy CBC server.** The code of this page runs the attack against a local simulated server with AES-128 in CBC mode. The key and the IV are

$$K = \texttt{00112233445566778899aabbccddeeff}, \qquad \mathrm{IV} = \texttt{0f0e0d0c0b0a09080706050403020100},$$

and the secret plaintext is `attack at dawn`, 14 octets, so the PKCS #7 padding adds two octets of value `02`. There is one ciphertext block $C_1$. The attack asks the server 1394 questions, each one a forged two block ciphertext, and recovers

$$D_K(C_1) = \texttt{6e7a796d6861296973266165746c0302} .$$

The exclusive or with the IV gives `61747461636b206174206461776e0202`, which is the padded plaintext, and the padding comes off to give `attack at dawn`. The attacker used the oracle and the public ciphertext only. The test file also runs a two block message, and plaintexts that end in octets which look like padding, which is the case that needs the confirmation step.

**The same server with encrypt-then-MAC.** The test file then runs the attack against a server that checks a MAC over the ciphertext before it decrypts. Every forged query is rejected by the MAC, so the search finds no conforming octet and stops with an error after 256 queries on the first position. One bit that never depends on the plaintext is worth nothing.

**POODLE, 2014.** SSL 3.0 padding has no value check: only the last octet gives the length. So the attacker copies the target block over the last block of a record; the record is accepted exactly when the decrypted last octet is 15, which gives the octet in about 256 requests, with no search over values. The fix was to stop using SSL 3.0.

**Lucky Thirteen, 2013.** TLS 1.1 and 1.2 had already removed the padding error message, as the countermeasure to Vaudenay's attack asks. AlFardan and Paterson found that the MAC check still takes a different number of hash compression calls for different padding lengths, so the answer leaks in the timing of the response. The repair in the libraries was to equalize the work, and the real repair was to move to AEAD. See the [timing attack](/timing-attack/) page for the measurement side.

## Where it is used

The class is a checklist item for every protocol review:

- **SSL and TLS record layer.** Vaudenay 2002 for the padding error, Canvel and others in 2003 for the timing version, Lucky Thirteen in 2013, POODLE in 2014. TLS 1.3 removed CBC and all padding.
- **RSA key transport.** Bleichenbacher 1998, the TLS countermeasure of RFC 5246 Section 7.4.7.1, DROWN in 2016 and ROBOT in 2018, and the timing variants of the Marvin report in 2023. The details are on the [PKCS #1 v1.5](/rsa-pkcs1-v1-5-encryption/) page.
- **Web frameworks.** The ASP.NET attack of Rizzo and Duong (2010) read files from the server through a CBC padding oracle in a cookie, and the fix was a signature over the token.
- **Mail.** The Efail work of 2018 built CBC and CFB gadgets in S/MIME and OpenPGP messages, where the mail client itself leaked the result.
- **XML and JOSE.** XML Encryption fell to a padding oracle in 2011, and several JSON Web Encryption libraries have had the RSA version.

Through these failures the class shaped the modern rules: [authenticated encryption](/authenticated-encryption/) by default, encrypt-then-MAC when the order is a choice, implicit rejection in a [KEM](/key-encapsulation-mechanism/), and one error for every failure. A scheme that satisfies [IND-CCA](/ind-cca-security/) security has no padding oracle by definition, which is the clean way to state the lesson.

**The code of this page is for study only.** It is not constant time, and the attack runs only against the simulated server in the same folder, on keys that the test file makes.

## References
