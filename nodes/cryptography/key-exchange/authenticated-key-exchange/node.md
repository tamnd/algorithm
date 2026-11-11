---
tag: NYN6YJ
kind: concept
slug: authenticated-key-exchange
name: Authenticated key exchange
aliases:
- AKE
- authenticated key agreement
area: cryptography/key-exchange
level: advanced
summary: Key exchange in which each party also learns who holds the other copy of the key. Defined by game-based models (Bellare-Rogaway 1993, Canetti-Krawczyk 2001, eCK 2007) with a Test query.
prereqs: [diffie-hellman, digital-signature, session-key]
see_also: [key-agreement-problem, man-in-the-middle-attack, perfect-forward-secrecy, key-confirmation, key-compromise-impersonation, unknown-key-share-attack, sigma-key-exchange, hmqv]
sources:
  - paper: "Mihir Bellare and Phillip Rogaway, Entity authentication and key distribution, CRYPTO 1993, LNCS 773, Springer, 1994, pages 232 to 249"
    locator: the model with oracles, Send, Reveal and Test queries, matching conversations, and the protocols MAP1 and AKEP1, AKEP2
  - paper: "Ran Canetti and Hugo Krawczyk, Analysis of key-exchange protocols and their use for building secure channels, EUROCRYPT 2001, LNCS 2045, Springer, 2001, pages 453 to 474"
    locator: the CK model (session-state reveal, corruption, session expiration), SK-security, and the composition with secure channels; full version IACR ePrint 2001/040
  - paper: "Brian LaMacchia, Kristin Lauter and Anton Mityagin, Stronger security of authenticated key exchange, ProvSec 2007, LNCS 4784, Springer, 2007, pages 1 to 16"
    locator: the eCK model with the EphemeralKeyReveal query, its freshness condition, and the NAXOS protocol
  - paper: "Cas Cremers, Examining indistinguishability-based security models for key exchange protocols: the case of CK, CK-HMQV, and eCK, ASIACCS 2011, ACM, 2011, pages 80 to 91"
    locator: the proof that the CK and eCK models are incomparable; full version IACR ePrint 2009/253
  - paper: "Hugo Krawczyk, SIGMA: the SIGn-and-MAc approach to authenticated Diffie-Hellman and its use in the IKE protocols, CRYPTO 2003, LNCS 2729, Springer, 2003, pages 400 to 425"
    locator: the discussion of the ISO signature-based protocol (signatures over both DH values and the peer identity), which the code on this page follows
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 12, Section 12.2 (Definitions 12.6 to 12.9 on key authentication, key confirmation and authenticated key establishment) and Protocol 12.20 (AKEP2)
---

An authenticated key exchange (AKE) is a protocol in which two parties agree on a fresh [session key](/session-key/) and each party also learns which party holds the other copy of it. Plain [Diffie-Hellman](/diffie-hellman/) gives a shared key but not the second part, so an active attacker can run a [man-in-the-middle attack](/man-in-the-middle-attack/). AKE adds authentication from long-term keys (signatures, static Diffie-Hellman keys, or a shared secret), and the security models of Bellare and Rogaway (1993), Canetti and Krawczyk (2001) and LaMacchia, Lauter and Mityagin (2007) say exactly what "secure" means.

**Notation.** $G$ is a cyclic group of prime order $q$ with generator $g$. A party $\hat A$ has a long-term secret $a$ and public key $A = g^a$ (or a signature key pair). In a session it picks an ephemeral secret $x$ and sends $X = g^x$. $K$ is the session key, $\lambda$ the security parameter, and $\mathcal{A}$ the adversary. $\mathrm{Adv}$ is its advantage in the named game.

## In plain words

Two people want to talk in secret over a network that an enemy controls. They can make a shared secret from public numbers, as in Diffie-Hellman. But the enemy can stand in the middle, make one secret with each of them, and read everything.

An authenticated key exchange fixes this with long-term keys that the world already links to names, for example through certificates. Each side proves, inside the exchange, that the numbers it sent came from it and were meant for this run with this peer. At the end each side holds a key and the name of the only other party that can hold it.

The models ask for more. The key must look random to the enemy, even when the enemy sees other keys. Old keys must stay safe when a long-term key leaks later.

## The idea

### The setting

Each party has a long-term key pair, and every party knows the authentic public keys of the others (for example through certificates). A party can run many *sessions*, as initiator or responder, at the same time. The adversary controls the network: it reads, drops, changes, delays and injects messages, and it can start sessions. This is the setting of all the models below. The models differ in what the adversary can also learn, and in which sessions it may attack.

A session that ends with "accept" outputs a key $K$, the identity of its *peer*, and a *session identifier* $\mathrm{sid}$. Two sessions are *partners* (or *matching*) when they have the same sid and opposite roles. Bellare and Rogaway define partners by *matching conversations*: the two transcripts are equal. Canetti and Krawczyk let the protocol output the sid; for Diffie-Hellman protocols it is usually $(\hat A, \hat B, X, Y)$.

### The queries

| Query | What the adversary gets | Models |
|---|---|---|
| Send$(\pi, m)$ | the reply of session $\pi$ to message $m$ | all |
| Reveal$(\pi)$ (SessionKeyReveal) | the session key of an accepted session | all |
| Corrupt$(\hat A)$ (StaticKeyReveal) | the long-term secret of $\hat A$ (in CK, all its state) | all |
| SessionStateReveal$(\pi)$ | the internal state of an incomplete session, as the protocol defines it | CK |
| EphemeralKeyReveal$(\pi)$ | the ephemeral secret $x$ of a session | eCK |
| Expire$(\pi)$ | deletes the key and state of a session, for forward secrecy | CK |
| Test$(\pi)$ | the real key of $\pi$ if a hidden bit $b = 1$, a uniform key if $b = 0$ | all |

The adversary makes one Test query on a *fresh* session and outputs a guess $b'$. Its advantage is

$$\mathrm{Adv}^{\mathrm{ake}}(\mathcal{A}) = \left| 2 \Pr[b' = b] - 1 \right|.$$

A session is fresh when the adversary has not learned its key in a trivial way: no Reveal of it or of its partner, and no corruption that gives the key away. Each model draws this line in its own place, and this line is where the models differ.

### The security goals

- **Key secrecy (indistinguishability).** For every efficient $\mathcal{A}$, $\mathrm{Adv}^{\mathrm{ake}}(\mathcal{A})$ is negligible in $\lambda$. The key of a fresh session looks like a random string, even when the adversary knows the keys of all other sessions. This is the Test query. A secrecy notion of the form "the adversary cannot compute the key" is too weak: a key that leaks half its bits is not safe to use in a cipher.
- **Consistency.** Two partner sessions that both accept hold the same key, and each names the other as peer. With the key secrecy above, this gives *implicit key authentication* (HAC Definition 12.6): only the named peer can know the key.
- **Entity authentication.** When a session accepts, a partner session exists (or will exist), that is, the peer really took part. Bellare and Rogaway define it by matching conversations. A protocol with a final key confirmation message gives *explicit* authentication; see [key confirmation](/key-confirmation/).
- **Forward secrecy.** A Corrupt query on a party after a session expired does not help to attack that session. Full forward secrecy holds against an adversary that was active in the session; *weak* forward secrecy only for sessions where the adversary did not change the messages. See [perfect forward secrecy](/perfect-forward-secrecy/).
- **Resistance to key compromise impersonation.** The Test session may belong to a party whose own long-term key is corrupted, as long as the peer is not. See [key compromise impersonation](/key-compromise-impersonation/).
- **Resistance to unknown key-share.** No two sessions with different views of who the peer is may hold the same key. In the models this follows from key secrecy, because the adversary may Reveal the "wrong" session and use its key on the Test session. See [unknown key-share attack](/unknown-key-share-attack/).

### The three models

**Bellare and Rogaway (1993).** The first game-based model. Each party instance is an oracle $\Pi^s_{i,j}$. The paper treats two parties with a shared long-term symmetric key, defines mutual authentication by matching conversations and key secrecy by the Test query, and proves the protocols MAP1 (mutual authentication) and AKEP2 secure from a pseudorandom function. Later papers moved the model to the public key setting.

**Canetti and Krawczyk (2001), the CK model.** It adds SessionStateReveal and session expiration, defines SK-security (consistency plus key secrecy), and proves that an SK-secure protocol, combined with a MAC and a symmetric cipher, gives a secure channel. The model also gives a modular way to build protocols: prove the protocol in an ideal network where messages are authenticated, then add an *authenticator* that makes it work on a real network. The [SIGMA](/sigma-key-exchange/) proof and the [HMQV](/hmqv/) proof are in this model.

**LaMacchia, Lauter and Mityagin (2007), the eCK model.** It replaces SessionStateReveal by EphemeralKeyReveal and lets the adversary learn any combination of secrets, except both the long-term and the ephemeral secret of one side of the Test session. One definition then covers KCI resistance, weak forward secrecy, and the leak of ephemeral keys from a weak random number generator. The paper gives the protocol NAXOS, which hashes the ephemeral secret with the long-term secret, so that the leak of $x$ alone does not give the exponent.

**CK and eCK are incomparable.** Cremers (2011) proved that neither model implies the other. There are protocols that are secure in CK and insecure in eCK, and protocols that are secure in eCK and insecure in CK. The reasons are in the details: SessionStateReveal in CK can reveal values that EphemeralKeyReveal in eCK does not cover, eCK allows the reveal of the ephemeral key of the Test session itself, and the two models define matching sessions in different ways. So "secure in eCK" is not "stronger than CK", and a proof in one model does not carry over to the other.

### The cost

A Diffie-Hellman based AKE costs each party at least one fixed-base exponentiation (its ephemeral $X$) and one variable-base exponentiation (the shared value). Signature-based protocols add one signature and one verification for each party. Implicitly authenticated protocols such as [MQV](/mqv/) and [HMQV](/hmqv/) replace the signatures by a second exponentiation that can share squarings with the first. The signed protocol in the examples below needs three messages, because each side signs a fresh value of the other side.

## Examples

**Plain Diffie-Hellman is not an AKE.** Take the toy group of order $q = 1019$ in $\mathbb{Z}_{2039}^*$ with $g = 4$. Alice picks $x = 57$ and sends $X = 1556$. Bob picks $y = 311$ and sends $Y = 1502$. Both compute $Z = 661$. Now let Eve stand in the middle with $e = 100$. She sends $E = 4^{100} \bmod 2039 = 1153$ to both. Alice computes $E^{57} = 739$ and Eve computes $X^{100} = 739$. Bob computes $E^{311} = 1075$ and Eve computes $Y^{100} = 1075$. In the Test game, Alice's session has no partner, so it is fresh, and Eve knows its key: she outputs $b' = 1$ exactly when the challenge equals 739, and wins with advantage 1.

**Signed Diffie-Hellman is an AKE.** The code on this page runs the three-message protocol below, with Schnorr signatures in a group of order $q$ with 255 binary digits.

```text
m1  A -> B : A, X = g^x
m2  B -> A : B, Y = g^y, SIG_B(X, Y, A)
m3  A -> B : SIG_A(Y, X, B)
K = H(A, B, X, Y, g^(xy)),   sid = (A, B, X, Y)
```

Eve's substitution now fails: Alice checks Bob's signature on $(X, E, \hat A)$, and Bob never signed $E$. Each signature covers the fresh value of the other side, so an old $m_2$ does not verify in a new session. Each signature also names the peer, which stops the [unknown key-share attack](/unknown-key-share-attack/) of the "sign only your own values" design. This is the ISO/IEC 9798-3 based protocol that Krawczyk (2003) discusses. It does not hide the identities from a passive observer; [SIGMA](/sigma-key-exchange/) adds a MAC and encryption for that.

**A Test game run.** The tests on this page play the Test game against both protocols. Against plain Diffie-Hellman, the adversary in the middle wins 20 of 20 rounds. Against the signed protocol, the same substitution makes Alice's session reject, so there is no fresh accepted session to test.

**Implicit and explicit authentication.** [MQV](/mqv/) and [HMQV](/hmqv/) send only $X$ and $Y$: the key depends on the long-term keys, so only the right peer can compute it, but neither side knows that the peer took part (implicit). [Station-to-station](/station-to-station-protocol/), [SIGMA](/sigma-key-exchange/) and the [TLS 1.3 handshake](/tls-handshake/) add signatures and MACs, so each side knows that the peer holds the key (explicit).

**Symmetric AKE.** AKEP2 of Bellare and Rogaway (HAC Protocol 12.20) uses a long-term shared key and two keyed functions. The server-based protocols [Needham-Schroeder](/needham-schroeder-protocol/), [Otway-Rees](/otway-rees-protocol/) and [Yahalom](/yahalom-protocol/) predate the models, and several of them fail the goals above.

The code is for study only. It is not constant time, it branches on secret data, and it must not be used to protect real data. Use TLS 1.3 or a Noise protocol through a vetted library such as libsodium, or a FIPS 140 validated module.

## Where it is used

- The [TLS 1.3 handshake](/tls-handshake/) is an ephemeral Diffie-Hellman AKE in the SIGMA style: a signature over the transcript and a MAC (Finished) with keys from the handshake secret.
- [IKEv2](/ike-protocol/) uses [SIGMA](/sigma-key-exchange/) to set up IPsec keys.
- The [Noise protocol framework](/noise-protocol-framework/) builds implicitly authenticated AKEs from Diffie-Hellman alone, and WireGuard uses one of them.
- [X3DH](/x3dh/) and the [Signal protocol](/signal-protocol/) use a one-round AKE from static and ephemeral Diffie-Hellman values.
- [Password-authenticated key exchange](/password-authenticated-key-exchange/) is the AKE problem when the long-term secret is a low-entropy password.
- [Kerberos](/kerberos/) and other [key distribution center](/key-distribution-center/) protocols solve a related problem with a trusted server and symmetric keys.

## References
