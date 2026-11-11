---
tag: 8KQ7AG
kind: concept
slug: perfect-forward-secrecy
name: Perfect forward secrecy
aliases:
- forward secrecy
- PFS
area: cryptography/key-exchange
level: intro
summary: A key exchange has forward secrecy when a later leak of the long-term keys does not reveal the keys of sessions that already ended. Ephemeral Diffie-Hellman gives it; RSA key transport does not.
prereqs: [diffie-hellman, session-key]
see_also: [authenticated-key-exchange, key-transport-problem, rsa-cryptosystem, tls-handshake, key-ratchet, double-ratchet, forward-secure-signature, hmqv]
sources:
  - paper: "Christoph G. Günther, An identity-based key-exchange protocol, EUROCRYPT 1989, LNCS 434, Springer, 1990, pages 29 to 37"
    locator: the protocol and the first use of the term perfect forward secrecy
  - paper: "Whitfield Diffie, Paul C. van Oorschot and Michael J. Wiener, Authentication and authenticated key exchanges, Designs, Codes and Cryptography 2(2), 1992, pages 107 to 125"
    locator: the definition of perfect forward secrecy and the station-to-station protocol that has it
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 12.2.3 (Definition 12.16, perfect forward secrecy, and Definition 12.17, known-key attacks) and the notes of Section 12.10 on Günther
  - paper: "Hugo Krawczyk, HMQV: a high-performance secure Diffie-Hellman protocol, CRYPTO 2005, LNCS 3621, Springer, 2005, pages 546 to 566"
    locator: the generic attack that shows that no two-message implicitly authenticated protocol has full PFS, and the definition of weak PFS; full version IACR ePrint 2005/176
  - url: "https://www.rfc-editor.org/rfc/rfc8446"
    title: "E. Rescorla, RFC 8446, The Transport Layer Security (TLS) Protocol Version 1.3, 2018"
    locator: Section 1.2 (static RSA and DH removed, all public key exchanges give forward secrecy), Section 2.2 and Section 4.2.9 (psk_ke and psk_dhe_ke), Section 2.3 (0-RTT data is not forward secret)
  - paper: "Drew Springall, Zakir Durumeric and J. Alex Halderman, Measuring the security harm of TLS crypto shortcuts, ACM Internet Measurement Conference (IMC) 2016"
    locator: the measurements of session ticket key and ephemeral value reuse on TLS servers
---

A key exchange protocol has perfect forward secrecy (PFS), or forward secrecy, when a leak of the long-term keys of the parties does not reveal the [session keys](/session-key/) of sessions that ended before the leak. Günther named the property in 1989, and Diffie, van Oorschot and Wiener defined it in 1992. Ephemeral [Diffie-Hellman](/diffie-hellman/), with the ephemeral secrets erased after use, gives it. [RSA](/rsa-cryptosystem/) key transport, where the client encrypts the session secret to the long-term key of the server, does not.

**Notation.** $G$ is a cyclic group of order $q$ with generator $g$. A party has a long-term secret ($a$, or an RSA private exponent $d$) and per session ephemeral secrets $x, y$ with public values $X = g^x$ and $Y = g^y$. $K$ is the session key and $\mathcal{A}$ the adversary.

## In plain words

An eavesdropper can record every message of a conversation today and keep the recording for years. If one day it steals the long-term secret key of a server, can it read the old recordings?

With some protocols the answer is yes. The client picks the session secret and locks it with the long-term key of the server, so that key opens all the old sessions at once.

Forward secrecy means the answer is no. Each session makes its key from fresh random numbers that both sides throw away when the session ends. The long-term key only proves who is talking. A thief who steals it later can pretend to be the server in future sessions, but the old recordings stay closed.

The word "perfect" is a historical name. It does not mean that the protection is perfect in the sense of information theory.

## The idea

### Definition

Diffie, van Oorschot and Wiener (1992) give the definition: an authenticated key exchange protocol provides perfect forward secrecy if disclosure of the long-term secret keying material does not compromise the secrecy of the keys exchanged in earlier runs. The Handbook of Applied Cryptography (Definition 12.16) states the same: compromise of long-term keys does not compromise past session keys.

In the game-based models of [authenticated key exchange](/authenticated-key-exchange/), the adversary may Corrupt a party *after* the Test session has expired (its key and ephemeral state are erased), and the Test session must stay indistinguishable from random. Two strengths are in use:

- **Full PFS.** The Test session is protected even if the adversary was active in it: it sent some of the messages itself, and corrupts the long-term key of the peer later.
- **Weak PFS (wPFS).** The Test session is protected only if the adversary did not change its messages, that is, the session has a matching partner session. Krawczyk (2005) introduced this name.

### Why two-message implicit protocols get only weak PFS

Krawczyk (2005) showed that no two-message key exchange protocol that authenticates the parties only implicitly through their public keys (no signature or MAC from the initiator on the responder's value, and no shared state set up before) can have full PFS. The attack is generic. The adversary $\mathcal{A}$ picks $x$, sends $X = g^x$ to $\hat B$ in the name of $\hat A$, and gets $Y$. $\hat B$ accepts and computes $K$ from $b$, $y$, $X$ and $A$. $\mathcal{A}$ waits until the session expires, then corrupts $\hat A$ and learns $a$. Now $\mathcal{A}$ knows everything that $\hat A$ would have known in that session ($a$ and $x$), so it computes $K$. No property of the formula for $K$ can prevent this, because the formula must let the real $\hat A$ compute $K$ from the same values. A third message in which $\hat A$ proves that it took part (a signature or a MAC under a key that needs $\hat A$'s ephemeral secret) closes the gap, which is why [SIGMA](/sigma-key-exchange/) and [STS](/station-to-station-protocol/) have full PFS and [HMQV](/hmqv/) has wPFS.

### What is needed

1. **Fresh secrets.** Each session uses new ephemeral secrets $x$ and $y$, and the key depends on $g^{xy}$ (or on a fresh KEM key pair).
2. **Erasure.** The parties erase $x$, $y$ and every value derived from them, other than the session key, once the session key is computed. They erase the session key when the session ends. A server that keeps $x$ in memory, or that reuses one $x$ for many sessions, loses the property for all of them.
3. **Long-term keys only authenticate.** The long-term key signs or MACs the exchange, or enters the key formula next to a fresh DH value; it never decrypts the session secret.

Forward secrecy protects only the past. After a leak, an active adversary can impersonate the victim in new sessions. The symmetric counterpart, protection of the *future* after a state compromise, is post-compromise security, which the [key ratchet](/key-ratchet/) and the [double ratchet](/double-ratchet/) give by mixing in fresh Diffie-Hellman values.

### TLS 1.3 and its weak points

[TLS 1.3](/tls-handshake/) (RFC 8446, 2018) removed the static RSA and static Diffie-Hellman cipher suites, so that each public key based handshake uses ephemeral (EC)DHE and has forward secrecy (Section 1.2). Two modes remain outside:

- **PSK-only resumption** (psk_ke, Section 4.2.9). The key comes from a pre-shared key (for example, a resumption secret from an earlier session) with no new Diffie-Hellman, so a leak of that PSK opens the session. The psk_dhe_ke mode adds an ephemeral exchange and restores forward secrecy with respect to the PSK.
- **0-RTT early data** (Section 2.3). It is encrypted only under keys derived from the PSK, so it is not forward secret (and it can be replayed).

**Session tickets.** A server that does not want to store state encrypts the resumption secret under a session ticket encryption key (STEK) and gives the result to the client as a ticket. A leak of the STEK then opens every ticket made under it, and so every PSK-only resumption, and in TLS 1.2 every session whose ticket was sent. Springall, Durumeric and Halderman (2016) found that many large sites kept the same STEK for long periods, so the forward secrecy of these sites lasted as long as the STEK, not as long as one connection. The fix is to rotate STEKs often and to resume with psk_dhe_ke.

### Cost

Forward secrecy costs one ephemeral key pair for each session: one fixed-base exponentiation to make $X$ and one variable-base exponentiation to compute $Y^x$, plus erasure. For RSA key transport the server does one private key operation instead. With elliptic curves such as [X25519](/x25519/), the ephemeral exchange costs less than one RSA-2048 decryption.

## Examples

**RSA key transport, toy numbers.** Let the server have $N = 61 \cdot 53 = 3233$, $e = 17$ and $d = 2753$. The client picks the premaster secret 65 and sends $c = 65^{17} \bmod 3233 = 2790$. A recorder stores 2790. Years later it steals $d$ and computes $2790^{2753} \bmod 3233 = 65$, which gives the session key and the whole conversation.

**Ephemeral Diffie-Hellman, toy numbers.** In the group of order 1019 in $\mathbb{Z}_{2039}^*$ with $g = 4$, the client picks $x = 57$ and sends $X = 1556$, and the server picks $y = 311$ and sends $Y = 1502$ with a signature. Both compute $Z = 661$ and then erase 57 and 311. The recorder has 1556, 1502 and the signature. The stolen signing key lets it sign new messages, but $Z$ is still the [computational Diffie-Hellman](/computational-diffie-hellman/) value of $(X, Y)$, which the signing key does not help to find.

**The code.** The Python code on this page runs both handshakes with a 1024-bit toy RSA key and a 256-bit prime order group. The test encrypts a record under each session key, then gives the private RSA key to an attack function. The RSA transport record opens; the ephemeral DH record does not. The same DH record opens if the client did not erase $x$ and $x$ leaks. A third test runs Krawczyk's attack on the two-message protocol $K = H(Y^a, B^x, Y^x)$: a passive recorder who later learns $a$ gets nothing, but an active attacker who chose $x$ itself opens $\hat B$'s session after it corrupts $\hat A$. A fourth test opens a PSK-only resumed session with a leaked ticket key.

The code is for study only. It uses textbook RSA and toy groups, it is not constant time, and it must not be used to protect real data. Use TLS 1.3 through a vetted library, or a FIPS 140 validated module.

**Non-example: forward-secure signatures.** A [forward-secure signature](/forward-secure-signature/) keeps old *signatures* valid after a key leak by evolving the signing key. It is a property of a signature scheme, not of a key exchange, although the idea of updating keys and erasing the old ones is the same.

## Where it is used

- [TLS 1.3](/tls-handshake/), SSH, [IKEv2](/ike-protocol/) and the [Noise framework](/noise-protocol-framework/) all use ephemeral Diffie-Hellman in each handshake.
- [Station-to-station](/station-to-station-protocol/) was designed in 1992 to have it, with signatures for authentication.
- [HMQV](/hmqv/) and other two-message implicit protocols reach only weak PFS, by the argument above.
- The [double ratchet](/double-ratchet/) of the Signal protocol gives forward secrecy for each message, not only for each session.

## References
