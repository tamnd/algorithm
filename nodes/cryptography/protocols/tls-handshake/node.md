---
tag: VZ8M1C
kind: algorithm
slug: tls-handshake
name: TLS handshake
aliases:
- TLS 1.3 handshake
area: cryptography/protocols
level: advanced
summary: "The TLS 1.3 handshake of RFC 8446: ephemeral Diffie-Hellman, a signed transcript, Finished MACs and an HKDF key schedule, with PSK resumption and replayable 0-RTT data."
solves: [key-agreement-problem, entity-authentication]
model: word-ram
complexity:
  vars: {m: the total length in bytes of the handshake messages}
  time: {worst: O(m), average: O(m), best: O(m)}
  space: {extra: O(m)}
properties: {deterministic: false, randomized: true}
history:
  year: 2018
  people: [Eric Rescorla]
  note: RFC 8446 (August 2018) replaced the TLS 1.2 handshake after drafts that were analysed in parallel with symbolic tools and computational proofs.
prereqs: [authenticated-key-exchange, hkdf, x25519, digital-signature]
see_also: [perfect-forward-secrecy, sigma-key-exchange, hybrid-key-exchange, man-in-the-middle-attack, noise-protocol-framework, rsa-cryptosystem, kerberos, signal-protocol]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc8446"
    title: Eric Rescorla, RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3, August 2018
    locator: Section 2 (protocol overview), Section 4.1.3 (downgrade sentinel), Section 4.2.11 (pre-shared keys and binders), Section 4.4 (CertificateVerify and Finished; message_hash in Section 4.4.1), Section 7.1 (key schedule), Section 7.3 (traffic keys), Section 8 (0-RTT and anti-replay)
  - url: "https://www.rfc-editor.org/rfc/rfc8448"
    title: Martin Thomson, RFC 8448, Example Handshake Traces for TLS 1.3, January 2019
    locator: Section 3 (simple 1-RTT handshake with X25519 and TLS_AES_128_GCM_SHA256), the source of the test vectors
  - paper: doi:10.1145/3133956.3134063
    title: Cas Cremers, Marko Horvat, Jonathan Hoyland, Sam Scott and Thyla van der Merwe, A comprehensive symbolic analysis of TLS 1.3, ACM CCS 2017, pages 1773 to 1788
    locator: the Tamarin model of draft 21 with all handshake modes, and the unexpected behaviour of post-handshake client authentication
  - paper: doi:10.1007/s00145-021-09384-1
    title: Benjamin Dowling, Marc Fischlin, Felix Günther and Douglas Stebila, A cryptographic analysis of the TLS 1.3 handshake protocol, Journal of Cryptology 34(4), article 37, 2021
    locator: the multi-stage key exchange model and the reduction proofs for the full handshake and for the PSK modes
  - paper: doi:10.1007/BFb0055716
    title: Daniel Bleichenbacher, Chosen ciphertext attacks against protocols based on the RSA encryption standard PKCS #1, Crypto 1998, LNCS 1462, pages 1 to 12
    locator: the padding oracle attack on RSA key transport in SSL 3.0
  - paper: "Hanno Böck, Juraj Somorovsky and Craig Young, Return Of Bleichenbacher's Oracle Threat (ROBOT), USENIX Security Symposium 2018, pages 817 to 849"
    locator: the padding oracle still present in TLS implementations twenty years later
  - url: "https://www.rfc-editor.org/rfc/rfc5246"
    title: Tim Dierks and Eric Rescorla, RFC 5246, The Transport Layer Security (TLS) Protocol Version 1.2, August 2008
    locator: Section 7.4.7.1 (RSA-encrypted premaster secret) and Section 8.1 (master secret)
---

The TLS handshake is the first phase of a TLS connection. The client and the server agree on a cipher suite, the server proves its identity with a certificate and a signature, and both derive the keys that protect the rest of the connection. This page describes the handshake of TLS 1.3 (RFC 8446, August 2018). Every key exchange in TLS 1.3 is an ephemeral Diffie-Hellman exchange, so the connection has [forward secrecy](/perfect-forward-secrecy/). A key schedule built from [HKDF](/hkdf/) binds every key to the transcript of the handshake, and a Finished message with a MAC over the transcript closes each side's flight. A client that has connected before can resume with a pre-shared key (PSK) and can send 0-RTT data in its first flight, at the cost of replay.

**Notation.** $C$ is the client and $S$ the server. $g^x$ and $g^y$ are the X25519 public shares, and $g^{xy}$ the shared value. $H$ is SHA-256 and $L = 32$ its output length. $\mathrm{Extract}$ and $\mathrm{Expand}$ are HKDF with HMAC-SHA256. $\mathrm{EL}(S, \ell, c, n) = \mathrm{Expand}(S, \mathrm{HkdfLabel}(n, \text{"tls13 "} \| \ell, c), n)$ is HKDF-Expand-Label, and $\mathrm{DS}(S, \ell, T) = \mathrm{EL}(S, \ell, H(T), L)$ is Derive-Secret over a transcript $T$. $ES$, $HS$ and $MS$ are the early, handshake and master secrets. $\mathrm{fk}(s) = \mathrm{EL}(s, \text{"finished"}, \varepsilon, L)$ is the Finished key of a traffic secret $s$. CH, SH, EE, CT, CV and SF are the ClientHello, ServerHello, EncryptedExtensions, Certificate, CertificateVerify and server Finished; a range such as CH..CV is the concatenation of those messages.

## In plain words

Two people talk for the first time over a phone line that strangers can tap. Each picks a secret number and says a value made from it. From what they hear, both work out the same shared secret, but a listener cannot. The server signs a summary of everything said so far, so the client knows that it talks to the real server and that nobody changed the earlier words. Both then send a check value made from the secret and the summary.

All later keys come from the shared secret, mixed with the summary. A returning client gets a ticket, which lets it skip the signature and send its first request at once, but a stranger can copy that early request and send it again.

## The problem

A client wants a private and authentic channel to a server over a network that an attacker controls. The client knows the server's name and trusts some certificate authorities; the server has a signing key and a certificate. The two have no shared secret. They need a [session key](/session-key/) that only they know, the client must know that the key is shared with the named server ([entity authentication](/entity-authentication/) of the server), and a later theft of the server's signing key must not expose old sessions. This is [authenticated key exchange](/authenticated-key-exchange/) with server-only authentication, the common case on the web.

## The algorithm

```pseudo id=main
Client, first flight                                                ▷ RFC 8446 Sections 2 and 4.1.2
L1  C: x ← random; send CH = (random, g^x, and, to resume, a ticket identity with binder = HMAC(fk(DS(ES, "res binder", ε)), H(CH without the binder)))
L2  C: if resuming with early data: c_e ← DS(ES, "c e traffic", CH); send the data protected under c_e
Server                                                              ▷ Sections 4.1.3, 4.4 and 7.1
L3  S: ES ← Extract(0, PSK or 0^L); if a ticket is offered, look up its PSK and check the binder; with single-use tickets, delete the ticket
L4  S: y ← random; send SH = (random, g^y)
L5  S: HS ← Extract(DS(ES, "derived", ε), g^xy)
L6  S: c_hs ← DS(HS, "c hs traffic", CH..SH); s_hs ← DS(HS, "s hs traffic", CH..SH)
L7  S: under s_hs send EE; without a PSK also CT and CV = Sign(sk_S, 64 spaces ∥ "TLS 1.3, server CertificateVerify" ∥ 0 ∥ H(CH..CT)); then SF = HMAC(fk(s_hs), H(CH..CV))
L8  S: MS ← Extract(DS(HS, "derived", ε), 0^L)
L9  S: c_ap ← DS(MS, "c ap traffic", CH..SF); s_ap ← DS(MS, "s ap traffic", CH..SF)
Client                                                              ▷ Sections 4.4.2 to 4.4.4
L10 C: HS ← Extract(DS(ES, "derived", ε), g^xy); derive c_hs and s_hs as in line L6; decrypt the server's flight
L11 C: without a PSK: check that CT names the server and chains to a trusted root; verify CV with the key in CT
L12 C: check that SF = HMAC(fk(s_hs), H(CH..CV)), else abort
L13 C: derive MS, c_ap and s_ap as in lines L8 and L9; send CF = HMAC(fk(c_hs), H(CH..SF)) under c_hs
Server                                                              ▷ Sections 4.6.1 and 7.1
L14 S: check CF, else abort; rms ← DS(MS, "res master", CH..CF); send a ticket under s_ap; its PSK is EL(rms, "resumption", ticket nonce, L)
```

**The key schedule.** The schedule is a chain of three HKDF-Extract steps (lines L3, L5 and L8). The first takes the PSK, the second the Diffie-Hellman value, and the third nothing new. Between them, Derive-Secret with the label "derived" and the hash of the empty string carries the previous secret forward. Each traffic secret is Derive-Secret of one of the three secrets, with its own label and the transcript up to that point. The traffic key and IV of a secret are $\mathrm{EL}(s, \text{"key"}, \varepsilon, 16)$ and $\mathrm{EL}(s, \text{"iv"}, \varepsilon, 12)$, and the record nonce is the IV XOR the sequence number (Section 7.3). Because every label and every transcript hash enters the derivation, two secrets of one session are never equal, and a key of one session says nothing about another.

**Authentication.** In a full handshake the server signs the transcript through its Certificate (line L7). The signature binds the server's identity to both shares $g^x$ and $g^y$, as in the [SIGMA](/sigma-key-exchange/) design that TLS 1.3 follows, so a [man in the middle](/man-in-the-middle-attack/) who replaces a share cannot produce a valid CertificateVerify. The two Finished MACs then confirm that both sides hold the same keys and saw the same messages. In a PSK handshake, knowledge of the PSK authenticates the server: the binder proves that the client holds it, and the server's Finished, keyed through $ES$, proves that the server holds it.

**Resumption and 0-RTT.** After the handshake the server sends a NewSessionTicket. The ticket's PSK is derived from the resumption master secret and a ticket nonce (line L14). A later ClientHello offers the ticket with a binder, an HMAC over the ClientHello up to the binder, which ties the offer to the PSK (line L1). In the mode psk_dhe_ke the client also sends a fresh share, so the new session still has forward secrecy; in psk_ke it does not. With the ticket the client may send early data under $c\_e$ (line L2) before it hears from the server. The early data keys depend only on the PSK and the ClientHello, so an attacker who copies the first flight can send it again and the server will decrypt it again. Section 8 of RFC 8446 lists the defences: single-use tickets, a record of the ClientHellos seen within a time window, and a check of the ticket's age. Even with these, the application must only accept early data that is safe to repeat.

**HelloRetryRequest.** If the client sent no share for a group that the server accepts, the server answers with a HelloRetryRequest and the client sends a second ClientHello. To keep the transcript short, the first ClientHello is then replaced in the transcript by the synthetic message $254 \| 00\,00 \| L \| H(\text{CH1})$ (Section 4.4.1).

**About the code.** The Python code is for study only. It is not constant time and must not protect real data; use OpenSSL, BoringSSL, rustls, or the ssl module of the Python standard library. The key schedule, HkdfLabel, the traffic keys, the Finished values and the resumption PSK follow RFC 8446 exactly for TLS_AES_128_GCM_SHA256 with X25519, and the tests check them against the trace of RFC 8448 Section 3. X25519, Ed25519 and HKDF are local copies, checked with RFC 7748, RFC 8032 and RFC 5869. The simulated handshake is simpler than TLS: only the four-byte handshake headers are real, and the message bodies use a short private encoding; records use a study AEAD (encrypt-then-MAC with an HMAC-SHA256 key stream) keyed with the real traffic key and IV, not AES-GCM; the server's certificate is replaced by one Ed25519 key that the client trusts for the name; and there is no negotiation, no EndOfEarlyData and no client authentication. RFC 8448 does not print the transcript hash under the server Finished, so the server's verify_data is not tested; the application secrets are tested from the transcript hash that the RFC prints.

## Example

The trace of RFC 8448 Section 3, a full handshake with X25519 and TLS_AES_128_GCM_SHA256. Each value shows its first 16 hex digits; the tests check all of them in full.

| Line | Value | From | Result |
|---|---|---|---|
| L3 | $ES$ | Extract(0, 0^32) | 33ad0a1c607ec03b |
| L5 | DS(ES, "derived", ε) | hash of the empty string e3b0c442... | 6f2615a108c702c5 |
| L5 | $g^{xy}$ | client private 49af42ba..., server share c9828876... | 8bd4054fb55b9d63 |
| L5 | $HS$ | Extract(6f2615a1..., 8bd4054f...) | 1dc826e93606aa6f |
| L6 | H(CH..SH) | 196 + 90 bytes | 860c06edc07858ee |
| L6 | c_hs, s_hs | DS(HS, ...) | b3eddb126e067f35, b67b7d690cc16c4e |
| L7 | server key, IV | EL(s_hs, "key"), EL(s_hs, "iv") | 3fce516009c21727, 5d313eb2671276ee |
| L8 | $MS$ | Extract(43de77e0..., 0^32) | 18df06843d13a08b |
| L9 | c_ap, s_ap | DS(MS, ..., H(CH..SF) = 9608102a...) | 9e40646ce79a7f9d, a11af9f05531f856 |
| L13 | client verify_data | HMAC(fk(c_hs) = b80ad010..., 9608102a...) | a8ec436d677634ae |
| L14 | rms, ticket PSK | H(CH..CF) = 209145a9..., nonce 0000 | 7df235f2031d2a05, 4ecd0eb6ec3b4d87 |

The simulated handshake of the code gives a transcript of the handshake types 1, 2, 8, 11, 15, 20, 20 in a full handshake and 1, 2, 8, 20, 20 in a resumption. With a ticket and early data "pay 10", a server without anti-replay acts on a copied first flight twice; with single-use tickets it acts once, and the copy falls back to a full handshake.

## Correctness

**Claim.** If both sides follow the protocol and no message is changed, every check passes, and both sides derive the same handshake, application and resumption secrets. The reason is that each secret is a fixed function of the PSK, the Diffie-Hellman value and the transcript; X25519 gives both sides the same $g^{xy}$; and both sides see the same transcript. The signature and the two MACs are recomputed from equal inputs.

**A changed message is detected.** If an attacker changes, adds or drops a message and both sides still finish, then the transcripts differ, and one side accepted a Finished MAC that the other side did not make, or a CertificateVerify signature that the server did not make. So the attacker broke HMAC or the signature, or both sides derived different keys and the first record fails. Single-use tickets make one server act on each ticket's early data at most once. The proof page gives these arguments in full.

**Security.** Dowling, Fischlin, Günther and Stebila (J. Cryptology 2021) prove in a multi-stage key exchange model that the keys of the full handshake and of the PSK modes are secret and that the server is authenticated, under assumptions on Diffie-Hellman, the signature, HKDF and the hash. Cremers, Horvat, Hoyland, Scott and van der Merwe (CCS 2017) model all handshake modes of draft 21 in the Tamarin prover and prove the claimed properties symbolically. They also found an unexpected behaviour of post-handshake client authentication: a client cannot be sure that the server has accepted its authentication when it sends later data.

## Complexity

A full handshake takes one round trip before the client may send application data, and a 0-RTT resumption takes none. Each side does a constant number of public-key operations: two X25519 scalar multiplications, and one signature on the server and one verification on the client in a full handshake. Certificate chain checks add one verification per certificate. The rest is hashing: each transcript hash and each record covers the messages once, so with $m$ the total length of the handshake messages, the time is $O(m)$ plus a constant number of curve operations, which take constant time for a fixed curve. The code keeps the transcript, so its extra space is $O(m)$. A real implementation keeps a running hash and needs only $O(1)$ extra space for the transcript, apart from the binder computation.

## Properties

- **Forward secrecy.** Every full handshake and every psk_dhe_ke resumption uses fresh shares, so a later theft of the server's signing key or of the ticket key does not reveal past session keys.
- **Transcript binding.** Every secret after the ServerHello depends on the hash of the messages so far, and the signature and the MACs cover the whole transcript, so a downgrade of the cipher suite or the group is detected.
- **Server-only authentication by default.** The client is anonymous unless the server asks for a client certificate.
- **Encrypted handshake.** Everything after the ServerHello is encrypted, including the server's certificate. The server name in the ClientHello is still sent in clear unless Encrypted Client Hello is used.
- **Key separation.** Each traffic secret, the exporter secret and the resumption secret come from different labels, so learning one gives no information on the others.
- **Early data is replayable and has weaker secrecy.** 0-RTT data depends only on the PSK, so it has no forward secrecy against a later theft of the ticket key, and it can be replayed.

## Variants and improvements

- **TLS 1.2 and RSA key transport.** In the TLS 1.2 handshake (RFC 5246) the client could pick the premaster secret and encrypt it under the server's [RSA](/rsa-cryptosystem/) key with PKCS #1 v1.5 padding. This mode has no forward secrecy: anyone who records the traffic and later gets the server's RSA key can decrypt every session. It is also open to padding oracles. Bleichenbacher (Crypto 1998) showed that a server that reveals whether a decrypted value has valid padding lets an attacker decrypt a recorded premaster secret with about a million queries. Implementations added countermeasures, but Böck, Somorovsky and Young (USENIX Security 2018, ROBOT) found the oracle still present in the products of several vendors and on many large web sites. TLS 1.3 removed RSA key transport, static Diffie-Hellman, renegotiation, compression and the CBC and RC4 cipher suites, and it encrypts the server's certificate. A TLS 1.3 server that has to accept TLS 1.2 puts the bytes 44 4F 57 4E 47 52 44 01 at the end of its random (Section 4.1.3), so a TLS 1.3 client can detect a downgrade.
- **Client authentication.** The server sends a CertificateRequest, and the client answers with a Certificate, a CertificateVerify and its Finished. TLS 1.3 also allows client authentication after the handshake.
- **External PSKs.** A PSK can be set by hand instead of coming from a ticket; such keys are used in the Internet of Things and must have high entropy.
- **Post-quantum key exchange.** A [hybrid key exchange](/hybrid-key-exchange/) such as X25519 with ML-KEM-768 uses the key share extension unchanged and feeds the joined secret into the second Extract.
- **QUIC and DTLS.** QUIC (RFC 9001, 2021) carries the TLS 1.3 handshake in its own packets and uses the TLS key schedule for its packet protection. DTLS 1.3 (RFC 9147, 2022) adapts the handshake to datagrams.
- **Other designs.** The [Noise protocol framework](/noise-protocol-framework/) builds handshakes from the same parts with fixed patterns and no negotiation. The [Signal protocol](/signal-protocol/) replaces the online server signature with signed prekeys, so the receiver can be offline.

## When to use it

Use TLS 1.3 to protect any client-server connection over an untrusted network, through a maintained library and with certificates from a public or a private authority. Disable TLS 1.0 and 1.1, which RFC 8996 deprecated in 2021, and keep TLS 1.2 only with ECDHE and AEAD cipher suites for old clients. Enable 0-RTT only for requests that are safe to repeat, such as an HTTP GET without side effects. For peer-to-peer or embedded protocols with fixed keys, the Noise framework is often simpler.

## Pitfalls

- **0-RTT replay.** An attacker can send a copy of the first flight, and the server will act on the early data again (line L2). Use single-use tickets or a record of ClientHellos, accept only safe requests, and use the 425 Too Early status of HTTP (RFC 8470).
- **Certificate checks.** A client that skips line L11, or checks the chain but not the name, accepts any server, and a man in the middle reads everything.
- **Transcript order.** The CertificateVerify signs the transcript up to the Certificate, and the server Finished covers the transcript up to the CertificateVerify. A different order breaks interoperability and may break the proof.
- **The HelloRetryRequest transcript.** The first ClientHello must be replaced by the message_hash form; hashing it as is gives a different transcript from the other side.
- **Ticket keys.** The server encrypts tickets with a ticket key. A stolen ticket key reveals the PSK of every ticket, and so all 0-RTT data and every psk_ke session. Rotate ticket keys often.
- **The binder.** The binder covers the ClientHello up to the binders, but the length fields in it already count the binders. Computing the hash over a ClientHello with the wrong length fields gives a binder that the server rejects.
- **TLS 1.2 fallback.** Keeping RSA key transport enabled for old clients keeps the padding oracle risk. Turn it off.

## Implementations

## History

Netscape designed SSL; SSL 2.0 shipped in 1995 and SSL 3.0, by Freier, Karlton and Kocher, in 1996. The IETF published TLS 1.0 as RFC 2246 in 1999, TLS 1.1 in 2006 and TLS 1.2 as RFC 5246 in 2008. Bleichenbacher's attack of 1998 on RSA key transport was fixed by countermeasures rather than by a change of design. Years of attacks on TLS 1.2 and its predecessors, on padding, compression, renegotiation and downgrade, led the IETF to start TLS 1.3 in 2014, edited by Eric Rescorla. The design was analysed while it was written: Dowling, Fischlin, Günther and Stebila analysed candidate drafts at ACM CCS 2015, and Cremers, Horvat, Scott and van der Merwe used Tamarin at IEEE S&P 2016 to find an attack on draft 10 that combined resumption with delayed client authentication. RFC 8446 was published in August 2018, and Cremers et al. (CCS 2017) and Dowling et al. (J. Cryptology 2021) give the symbolic and computational analyses of the final design.

## References
