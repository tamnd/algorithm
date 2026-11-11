---
tag: 4VXR26
kind: algorithm
slug: opaque
name: OPAQUE
aliases:
- OPAQUE aPAKE
- OPAQUE-3DH
area: cryptography/key-exchange
level: research
summary: The augmented PAKE selected by the CFRG in 2020. An OPRF turns the password into a key that opens an envelope with the client's AKE key, then 3DH runs. No precomputation before a breach. RFC 9807.
solves: [password-authenticated-key-exchange]
model: word-ram
complexity:
  vars: {n: the number of binary digits of the group order}
  time: {worst: O(n^3), average: O(n^3), best: O(n^3)}
  space: {extra: Θ(n)}
properties: {deterministic: false, randomized: true}
history:
  year: 2018
  people: [Stanislaw Jarecki, Hugo Krawczyk, Jiayu Xu]
  note: Jarecki, Krawczyk and Xu defined OPAQUE and strong aPAKE security at EUROCRYPT 2018. The CFRG selected it in 2020, and RFC 9807 specified it in July 2025.
prereqs: [password-authenticated-key-exchange, diffie-hellman, pseudorandom-function, hkdf]
see_also: [secure-remote-password, cpace, key-compromise-impersonation, password-hashing, argon2, universal-composability, verifiable-random-function, perfect-forward-secrecy]
sources:
  - paper: "Stanislaw Jarecki, Hugo Krawczyk and Jiayu Xu, OPAQUE: an asymmetric PAKE protocol secure against pre-computation attacks, EUROCRYPT 2018, LNCS 10822, pages 456 to 486"
    locator: the strong aPAKE functionality in the UC framework, the OPRF-based compiler from an AKE with KCI security, and the proof in the random oracle model
  - url: "https://www.rfc-editor.org/rfc/rfc9807"
    title: Daniel Bourdrez, Hugo Krawczyk, Kevin Lewi and Christopher A. Wood, RFC 9807, The OPAQUE Augmented Password-Authenticated Key Exchange (aPAKE) Protocol, July 2025
    locator: Section 3 (overview), Section 4.1.2 and 4.1.3 (envelope creation and recovery), Section 5 (registration), Section 6.3 (credential retrieval with the masked response), Section 6.4 (3DH and its key schedule), Section 10.2 (security analysis), Section 10.9 (client enumeration), Section 10.11 (salt and precomputation)
  - url: "https://www.rfc-editor.org/rfc/rfc9497"
    title: Alex Davidson, Armando Faz-Hernandez, Nick Sullivan and Christopher A. Wood, RFC 9497, Oblivious Pseudorandom Functions (OPRFs) Using Prime-Order Groups, December 2023
    locator: Section 3 (the OPRF protocol, Blind, BlindEvaluate and Finalize), the base mode 0x00
---

OPAQUE is an augmented [password-authenticated key exchange](/password-authenticated-key-exchange/) of Jarecki, Krawczyk and Xu (2018). The server never sees the password, not even at registration. It holds a secret key for an oblivious pseudorandom function (OPRF), and the client uses the OPRF to turn its password into a strong key without revealing the password to the server. That key opens an "envelope", stored on the server, which yields the client's long-term key pair; then client and server run an authenticated Diffie-Hellman exchange (3DH). Because the OPRF key is secret, an attacker cannot build a table of password guesses before it breaks into the server. The CFRG selected OPAQUE as its augmented PAKE in 2020, and RFC 9807 (July 2025) specifies it.

**Notation.** $G$ a group of prime order $q$ with generator $g$ (ristretto255 or P-256 in RFC 9807), written multiplicatively. $H'$ a hash to $G$ and $H$ a hash to strings. $k_C$ the server's OPRF key for credential $C$, and $F(k, pw) = H(pw, H'(pw)^k)$ the OPRF. KSF a key stretching function, such as [Argon2](/argon2/). Extract and Expand the two halves of [HKDF](/hkdf/), and MAC is [HMAC](/hmac/). $(sk_S, pk_S)$ and $(sk_U, pk_U)$ the long-term keys of server and client; $(esk_S, epk_S)$ and $(esk_U, epk_U)$ their ephemeral keys.

## In plain words

A user logs in to a server with a password. Most systems send the password to the server, which checks it against a stored hash. OPAQUE never shows the password to the server.

At sign-up, the client and the server compute a function of the password together. The client learns the result, a strong secret, but the server learns nothing about the password, and the client learns nothing about the server's own key. The client uses the strong secret to lock a small box that holds its private key, and the server stores the box.

At login, the client and the server repeat the computation. The client opens the box, takes out its private key, and runs a normal key exchange with the server. Someone who steals the server's data must still guess passwords one at a time, and could not prepare any guesses before the theft.

## The problem

[Password-authenticated key exchange](/password-authenticated-key-exchange/) in the augmented setting: the client knows a password, the server stores a record derived from it, and they want a mutually authenticated [session key](/session-key/). An attacker who steals the server's records should still need an offline dictionary search to recover the password or to log in as the client. OPAQUE adds a stronger goal: that search must not start before the theft, so precomputed tables, as in a [rainbow table](/rainbow-table/) attack, are useless. Jarecki, Krawczyk and Xu call this strong aPAKE security.

## The algorithm

```pseudo id=main
OPAQUE(pw)                      ▷ RFC 9807; client U, server S; k_C the server's OPRF key for U
                                ▷ registration, over an authenticated channel
L1  U: r ← random in [1, q);  M ← H'(pw)^r;  send M         ▷ blind
L2  S: Z ← M^(k_C);  send Z, pk_S                            ▷ blind evaluation
L3  U: y ← H(pw, Z^(1/r));  rwd ← Extract("", y ‖ KSF(y))     ▷ y = F(k_C, pw)
L4  U: nonce random;  (sk_U, pk_U) ← DeriveKeyPair(Expand(rwd, nonce ‖ "PrivateKey"))
L5  U: tag ← MAC(Expand(rwd, nonce ‖ "AuthKey"), nonce ‖ pk_S ‖ ids);  S stores pk_U, masking_key, envelope = nonce ‖ tag
                                ▷ login: KE1, KE2, KE3
L6  U → S: KE1 = (M = H'(pw)^r, nonce_U, epk_U)
L7  S: Z ← M^(k_C);  masked ← Expand(masking_key, masking_nonce) ⊕ (pk_S ‖ envelope);  3DH with esk_S, sk_S;  S → U: KE2 with a MAC under Km2
L8  U: y ← H(pw, Z^(1/r));  rwd as in L3;  unmask pk_S and envelope;  re-derive (sk_U, pk_U) and check tag, else abort
L9  U: dh1 ← epk_S^(esk_U), dh2 ← pk_S^(esk_U), dh3 ← epk_S^(sk_U);  derive Km2, Km3, session_key;  check the server MAC, else abort
L10 U → S: KE3 = MAC(Km3, Hash(preamble ‖ server MAC))
L11 S: check KE3, else abort;  both output session_key
```

**The OPRF** (lines L1 to L3 and L7 to L8). The client sends the blinded value $M = H'(pw)^r$, which is a uniformly random group element whatever the password. The server raises it to its key, and the client removes the blinding: $Z^{1/r} = H'(pw)^{k_C}$. The client gets $F(k_C, pw)$ and learns nothing else; the server learns nothing about $pw$. This is the 2HashDH OPRF that RFC 9497 specifies; the site has no OPRF page. The output is then hardened with a slow KSF, so a thief pays for each guess.

**The envelope** (lines L4, L5 and L8). The randomized password rwd is expanded into an authentication key, an export key and a seed for the client's key pair, all bound to a fresh nonce (RFC 9807, Section 4.1.2). The envelope holds only the nonce and a MAC tag over the server's public key and the identities: the client's private key is derived again at each login, not stored. A wrong password gives a different rwd, and the tag check of line L8 fails.

**The masked response** (line L7). The server XORs $pk_S$ and the envelope with a pad derived from masking_key and a fresh nonce. An attacker who asks about a user that does not exist gets random bytes of the same form, so it cannot tell which users are registered (RFC 9807, Section 10.9).

**3DH** (lines L7, L9 to L11). The three Diffie-Hellman values combine ephemeral-ephemeral, ephemeral-static and static-ephemeral keys. The key schedule of RFC 9807, Section 6.4.2.2, extracts a key from $dh_1 \| dh_2 \| dh_3$ and derives a handshake secret and the session key from the hash of the transcript; Km2 and Km3 give the server and client MACs. The AKE must resist [key compromise impersonation](/key-compromise-impersonation/), so that a thief who has the server's key still cannot log in as the client without first finding the password.

**About the code.** The Python code is for study only. It is not constant time, and it must not protect real data. It is a simplified OPAQUE with the same steps and order as RFC 9807, and its simplifications are these. The group is the subgroup of quadratic residues modulo the 1024-bit safe prime of RFC 5054, not ristretto255 or P-256. The hash to the group squares a wide hash modulo $p$. The OPRF follows the 2HashDH design of RFC 9497 without its exact encodings. The KSF is the identity, where a real deployment must use a memory-hard function. The key schedule uses HKDF with plain labels instead of the Expand-Label format. Because of these changes, the code does not use the RFC 9807 test vectors and would not reproduce them.

## Example

The tests show the property that makes OPAQUE "strong". Two servers register the same user with the same password `123456`. Their records share nothing: masking_key and $pk_U$ differ, because each server has its own OPRF key. A table of hashes of common passwords, built in advance, matches neither record.

After a breach, the attacker has the record and the OPRF key $k_C$. For each guess $w$ it computes $H'(w)^{k_C}$ (one exponentiation), the finalization hash, the KSF, and Expand, and compares the result with the stored masking_key. The test tries `123456`, `password`, `qwerty`, `dragon` and `letmein`, and finds the registered password `dragon`. This offline search after a breach is unavoidable for any single-server aPAKE (RFC 9807, Section 10.11); OPAQUE makes it start only after the breach and makes each guess cost a KSF call.

## Correctness

**Claim.** With the right password, the client recovers the same $y$ as at registration, so the same rwd, keys and envelope tag; both sides compute the same three Diffie-Hellman values and the same session key, and both MACs verify. The OPRF unblinding gives $(H'(pw)^{r k_C})^{1/r} = H'(pw)^{k_C}$, and the 3DH values agree: $dh_1 = g^{esk_U esk_S}$, $dh_2 = g^{sk_S esk_U}$, $dh_3 = g^{sk_U esk_S}$ on both sides. With a wrong password, $y$ changes, and the tag check of line L8 fails unless the MAC is forged. See the [full proof](/opaque/proofs/correctness/).

**Security.** Jarecki, Krawczyk and Xu prove that OPAQUE realizes their strong aPAKE functionality in the [UC](/universal-composability/) framework, in the [random oracle model](/random-oracle-model/), assuming a UC-secure OPRF (2HashDH is one under the one-more Diffie-Hellman assumption) and an AKE with KCI security and forward secrecy. RFC 9807, Section 10.2, notes that the proof covers one server key and no batching, and that the RFC differs from the paper in details listed in Section 10.1.

## Complexity

In a login, the client does 7 exponentiations in $G$: one to blind, one to unblind (after an inversion modulo $q$), one to re-derive $pk_U$, one for $epk_U$ and three for 3DH. The server does 5: one OPRF evaluation, one for $epk_S$ and three for 3DH. With schoolbook arithmetic each exponentiation costs $O(n^3)$ word operations, so a run is $O(n^3)$. The KSF adds a cost chosen by the application, often the largest part. A login has three messages (KE1, KE2, KE3), one and a half round trips; registration has three (request, response, record). Each party keeps $O(1)$ group elements and keys. The server stores per user the record $(pk_U, \text{masking\_key}, \text{envelope})$ and derives $k_C$ from one seed.

## Properties

- **Augmented**: the server stores no password equivalent. A thief must run a dictionary search to log in as the user.
- **Security against precomputation**: the OPRF key acts as a secret salt (RFC 9807, Section 10.11).
- **The password never leaves the client**, even at registration.
- **Mutual authentication** and explicit key confirmation through the two MACs.
- **Forward secrecy** from the ephemeral keys of 3DH.
- **Export key**: an extra key that only the client learns, for example to encrypt data stored on the server.
- **Client enumeration protection** through the masked response.
- **Modular**: OPAQUE is a compiler from any AKE with KCI security; RFC 9807 fixes 3DH, and HMQV or a TLS handshake also fit.

## Variants and improvements

- **Threshold OPAQUE**: the OPRF key is shared among several servers (for example with the TOPPSS scheme), so a breach of one server does not allow a dictionary search.
- **Other AKEs**: OPAQUE-HMQV with [HMQV](/hmqv/), and integrations with TLS 1.3 handshakes.
- **AuCPace** (Haase and Labrique 2019), the other augmented candidate in the CFRG selection, builds on [CPace](/cpace/) and sends a salt in the clear, so it allows precomputation unless strengthened.
- **[SRP](/secure-remote-password/)** is the older augmented PAKE; it sends the salt before authentication and has no proof in a standard model.

## When to use it

Use OPAQUE for client-server password logins where the server should never handle the password and a database breach should not reveal weak passwords at once. WhatsApp uses OPAQUE to protect the keys of its end-to-end encrypted backups. For two peers that share a pairing code, a balanced PAKE such as [CPace](/cpace/) is simpler.

## Pitfalls

- **A fast KSF.** With the identity KSF, as in the page's code, a thief tests guesses at the speed of one exponentiation. Use a memory-hard KSF such as Argon2id in line L3.
- **One OPRF key for all users.** The key must be per credential (RFC 9807 derives it from a seed and the credential identifier), or one evaluation helps an attacker against many users.
- **No check of the blinded element.** Line L7 must check that $M$ is a valid group element other than the identity.
- **No identities in the envelope tag.** Line L5 binds $pk_S$ and the identities; without them a malicious server could swap keys.
- **An AKE without KCI security.** Then a thief with the server key can log in as the client without any dictionary search.
- **Early abort leaks.** The server must answer a request for an unknown user with a fake masked response of the same form (RFC 9807, Section 10.9).
- **Server-side password rules.** Checking the password on the server undoes the main benefit (RFC 9807, Section 10.11).

## Implementations

The Python code gives the OPRF (`hash_to_group`, `blind`, `evaluate`, `finalize`), the envelope (`store`, `recover`), a `Server` with per-credential OPRF keys, `registration_response`, `ke2` and `finish`, and the client functions `register` and `login`, with the line markers of the pseudocode. The tests check that the hash lands in the group, registration and login with equal session and export keys, a wrong password, a wrong client identity, that two servers give unrelated records for the same password, and that after a breach a guess loop finds the password.

## History

Ford and Kaliski (2000) used a blind hash of the password in password-hardened protocols, and Boyen (2009) and Jarecki, Kiayias, Krawczyk and Xu (2016) built related password protocols. Jarecki, Krawczyk and Xu (2018) combined an OPRF with an AKE, defined strong aPAKE security against precomputation, and proved OPAQUE secure. In the CFRG PAKE selection of 2019 and 2020, OPAQUE was chosen as the augmented PAKE, beside [CPace](/cpace/) as the balanced one. The OPRF became RFC 9497 in December 2023, and OPAQUE became RFC 9807 in July 2025, by Bourdrez, Krawczyk, Lewi and Wood.

## References
