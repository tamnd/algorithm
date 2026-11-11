---
tag: 53493G
kind: concept
slug: challenge-response-authentication
name: Challenge-response authentication
aliases:
- challenge-response
- challenge-response identification
area: cryptography/protocols
level: intro
summary: The verifier sends a fresh challenge and the prover answers with a value that only a key holder can compute (a MAC, a signature or a decryption). HOTP and TOTP are counter and time variants.
prereqs: [entity-authentication, message-authentication-code, nonce]
see_also: [hmac, digital-signature, schnorr-identification-protocol, zero-knowledge-proof, kerberos, needham-schroeder, tls-handshake, man-in-the-middle-attack]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 10, Section 10.3 (challenge-response identification, with time-variant parameters, symmetric-key and public-key techniques) and Section 10.5 (attacks on identification protocols, including reflection and interleaving)
  - url: "https://www.rfc-editor.org/rfc/rfc4226"
    title: David M'Raihi, Mihir Bellare, Frank Hoornaert, David Naccache and Ohad Ranen, RFC 4226, HOTP, an HMAC-based one-time password algorithm, December 2005
    locator: Section 5 (the algorithm and dynamic truncation), Section 5.4 (security formula Sec = sv/10^Digit), Section 7 (throttling and resynchronization), Appendix D (test values, used by the code)
  - url: "https://www.rfc-editor.org/rfc/rfc6238"
    title: David M'Raihi, Salah Machani, Mingliang Pei and Johan Rydell, RFC 6238, TOTP, time-based one-time password algorithm, May 2011
    locator: Section 4 (the algorithm), Section 5.2 (time step and the rule to accept an OTP once), Appendix A (reference code and seeds), Appendix B (test vectors, used by the code)
  - paper: "Ray Bird, Inder Gopal, Amir Herzberg, Phil Janson, Shay Kutten, Refik Molva and Moti Yung, Systematic design of two-party authentication protocols, CRYPTO 1991, LNCS 576, pages 44 to 61"
    locator: oracle and reflection attacks on symmetric challenge-response, and protocols that resist them
  - paper: "ISO/IEC 9798-2, 9798-3 and 9798-4, Information technology, Security techniques, Entity authentication"
    locator: Part 2 (mechanisms with symmetric encipherment), Part 3 (with digital signatures), Part 4 (with a cryptographic check function)
---

Challenge-response authentication is a technique for [entity authentication](/entity-authentication/): the verifier sends a fresh value, the challenge, and the prover answers with a function of the challenge and a secret key that only the claimed party holds. Because the challenge is new, an old answer is of no use to an attacker, which stops the replay of a password. The answer can be a [message authentication code](/message-authentication-code/), a symmetric encryption, a [digital signature](/digital-signature/) or the decryption of a [public-key](/public-key-encryption/) ciphertext. HOTP and TOTP are one-pass variants in which a counter or the clock takes the place of the challenge.

**Notation.** $K$ is a key that $A$ and $B$ share; $\mathrm{MAC}_K$ is a MAC such as [HMAC](/hmac/); $r_B$ is a [nonce](/nonce/) of $n$ bits chosen by $B$; $t_A$ is a timestamp of $A$; $\mathrm{Sig}_A$ is a signature with $A$'s private key. $A$ is the prover (claimant) and $B$ the verifier. An adversary is $\mathcal{A}$, and $q$ is the number of sessions it starts.

## In plain words

A guard at a gate does not ask for the password, because anyone who hears it can use it later. Instead, the guard says a new random word, and the visitor must answer with a code that you can only work out if you know the shared secret and the word. The guard checks the code. Since the word is new each time, a code that someone heard yesterday does not work today.

The details matter. If a guard will also answer codes for others, a trickster can ask the guard to answer the guard's own question, and then hand the answer back. To stop this, the answer must also say who made it. Some systems use a counter or the time instead of a spoken word, so that one message is enough. The code on a phone app for a bank login works in this way.

## The idea

### The three ways to make an answer fresh

The answer must depend on something that the verifier knows to be new (HAC Section 10.3.1).

- **A random nonce.** $B$ picks $r_B$ uniformly. It needs two passes and no shared state, and the verifier keeps $r_B$ only for the run.
- **A timestamp.** $A$ includes $t_A$, and $B$ accepts only if $|t_B - t_A|$ is at most a window $w$ and $B$ has not seen the same answer in the window. It needs one pass, loosely synchronized clocks, and a cache of the answers in the window.
- **A counter.** $A$ and $B$ keep a counter that grows by one in each run. It needs one pass and state on both sides, and a way to resynchronize.

### The mechanisms

With a shared key $K$, the two-pass unilateral form of ISO/IEC 9798-4 is

$$B \to A: r_B, \qquad A \to B: \mathrm{MAC}_K(r_B \,\|\, B).$$

$B$ recomputes the MAC and compares. ISO/IEC 9798-2 uses an encryption $E_K(r_B \,\|\, B)$ in the same place, and the mutual three-pass form adds $r_A$ and a reply from $B$. With a signature key, ISO/IEC 9798-3 has $A$ sign $(r_A, r_B, B)$, which needs no shared secret and gives a proof that a third party can check. With public-key encryption, $B$ sends $E_{pk_A}(r)$ and $A$ returns $r$; $B$ must also send a witness $h(r)$ and its identity, or else $A$ acts as a decryption oracle for anyone (HAC Section 10.3.3).

**A security claim.** Let the MAC be EUF-CMA secure, let $B$ draw each $r_B$ uniformly from $n$-bit strings, and let each party, as a prover, put the name of the verifier that it answers into the MAC, and never answer a challenge that claims to come from itself. So only $A$ ever computes a tag on a string that ends in $B$. Then the chance that $B$ accepts in a session whose answer $A$ did not compute on that session's $r_B$ is at most $\mathrm{Adv}^{\text{euf-cma}}_{\mathrm{MAC}} + q^2/2^{n+1}$.

*Proof.* Suppose that $B$ accepts in a session with nonce $r_B$. Then the adversary delivered a valid tag on $r_B \,\|\, B$. If $A$ computed this tag at some time, it computed it on a challenge equal to $r_B$; either that was this session's challenge, or two sessions of $B$ drew the same nonce, which has probability at most $\binom{q}{2} 2^{-n} \le q^2/2^{n+1}$. If $A$ never computed this tag, the adversary output a valid tag on a message that was never queried, and a forger that runs the adversary and answers $A$'s MAC calls with its own oracle wins the EUF-CMA game. $\square$

The claim says that someone holding $K$ answered this challenge. It does not say that $A$ meant to talk to $B$ in the same run, and it does not stop a relay: a [man in the middle](/man-in-the-middle-attack/) can pass the challenge to $A$ and the answer to $B$. Binding a run to both ends is the job of matching conversations (see [entity authentication](/entity-authentication/)), and binding it to a key is the job of a [key exchange](/authenticated-key-exchange/).

### The reflection attack

In the naive symmetric protocol the answer is $\mathrm{MAC}_K(r)$, and both parties play both roles with the same $K$. The attacker $\mathcal{A}$ poses as $A$ to $B$:

1. Session 1: $B \to \mathcal{A}$: $r_B$.
2. Session 2: $\mathcal{A} \to B$: $r_B$, posed as a challenge from $A$.
3. Session 2: $B \to \mathcal{A}$: $\mathrm{MAC}_K(r_B)$.
4. Session 1: $\mathcal{A} \to B$: $\mathrm{MAC}_K(r_B)$, and $B$ accepts.

$B$ has answered its own challenge. The fix is to make the answers of the two directions different: put an identity or a direction bit inside the MAC, or use two keys, one for each direction (Bird et al. 1991). In the ISO form above, $B$ expects $\mathrm{MAC}_K(r_B \,\|\, B)$, but in step 3 $B$ computes $\mathrm{MAC}_K(r_B \,\|\, A)$, because it answers someone that it takes to be $A$, so the reflected answer fails. Other attacks on the same class are the replay of an answer (stopped by freshness), the interleaving of runs, and the chosen-text attack in which the verifier picks challenges to learn about the key (HAC Section 10.5).

### HOTP and TOTP

HOTP (RFC 4226) replaces the nonce by a counter $C$ of 8 bytes, big endian:

$$\mathrm{HOTP}(K, C) = \mathrm{Truncate}(\mathrm{HMAC\text{-}SHA\text{-}1}(K, C)) \bmod 10^{d}.$$

Dynamic truncation takes the low 4 bits of the last byte of the 20-byte HMAC as an offset $o$, reads the 4 bytes at $o$ as a big-endian integer, and clears the top bit, which gives a 31-bit number. The server accepts a value for any counter in a look-ahead window of size $s$, then moves its counter past the value used, so the value cannot be used again.

TOTP (RFC 6238) uses the time as the counter: $T = \lfloor (\text{now} - T_0) / X \rfloor$ with the default step $X = 30$ seconds and $T_0 = 0$, and $\mathrm{TOTP} = \mathrm{HOTP}(K, T)$, with HMAC-SHA-1, HMAC-SHA-256 or HMAC-SHA-512. RFC 6238 Section 5.2 recommends that the server accept at most one step of network delay, and it must not accept the same value twice.

For brute force guessing, RFC 4226 Section 5.4 gives the success chance as $\mathrm{Sec} = s v / 10^{d}$ for $v$ attempts and a window of $s$, which is why the server must limit the number of attempts. A one-time password stops replay, but it does not stop a phishing page that relays the current code at once.

## Examples

**HOTP by hand (RFC 4226 Appendix D).** The key is the ASCII string `12345678901234567890` and $C = 0$. The HMAC is `cc93cf18508d94934c64b65d8ba7667fb7cde4b0`. Its last byte is `b0`, so $o = 0$. The 4 bytes at offset 0 are `cc93cf18`; with the top bit cleared this is `4c93cf18` $= 1284755224$, and $1284755224 \bmod 10^6 = 755224$. For $C = 1$ to $9$ the values are 287082, 359152, 969429, 338314, 254676, 287922, 162583, 399871 and 520489.

**TOTP (RFC 6238 Appendix B).** At time 59, $T = 1$ and the 8-digit SHA-1 code is 94287082; at time 1111111109, $T$ = `23523EC` (hex) and the code is 07081804; at time 1111111111, two seconds later, $T$ is one more and the code is 14050471. The SHA-256 and SHA-512 rows of the table use seeds of 32 and 64 bytes from the reference code in Appendix A, although the text of Appendix B names only the 20-byte seed. A program that uses the 20-byte seed for every hash gets the SHA-1 rows right and the other rows wrong.

**The window.** With a look-ahead window of 3, a server at counter 0 accepts 755224 and moves to counter 1. A second use of 755224 fails. The value 969429 (counter 3) passes, and the server moves to 4. The value 520489 (counter 9) is out of the window and fails.

**The reflection attack, run.** The test code builds the naive protocol with HMAC-SHA-256 and runs the four steps above against a simulated party $B$: $B$ accepts in each of 20 runs. With the identity of the prover inside the MAC, the same four steps fail in each run, while honest runs in both directions still pass.

**The code.** The Python code implements HOTP and TOTP, the naive and the fixed symmetric protocols, and a timestamp form with a window and a replay cache. The tests check all ten HOTP values and intermediate HMACs of RFC 4226 Appendix D, and all eighteen TOTP values of RFC 6238 Appendix B, copied by hand. The code is for study only. It is not constant time apart from the final comparison, and it must not protect real data. Use the standard library's `hmac` with a maintained OTP library, or a FIPS 140 validated module. The reflection attack runs only against a local simulated party.

## Where it is used

- **Network authentication.** [Kerberos](/kerberos/) authenticators are timestamp-based answers under a session key, and the [Needham-Schroeder](/needham-schroeder/) protocols use nonce handshakes. CHAP and many challenge-response logins of older network protocols are of the naive symmetric kind.
- **Key exchange.** In the [TLS handshake](/tls-handshake/), the server's CertificateVerify is a signature over a transcript that contains the client's random value, which is a signature-based challenge-response. [Authenticated key exchange](/authenticated-key-exchange/) protocols build on this pattern.
- **Second factors.** HOTP and TOTP run in hardware tokens and phone apps. FIDO and WebAuthn security keys sign a server challenge together with the web origin, which also stops the phishing relay.
- **Zero-knowledge identification.** The [Schnorr identification protocol](/schnorr-identification-protocol/) and other [zero-knowledge](/zero-knowledge-proof/) protocols are challenge-response protocols in which the answer shows nothing about the key.
- **Smart cards and car keys.** A card or key fob answers a reader's challenge with a MAC or an encryption under a key in the device.

## References
