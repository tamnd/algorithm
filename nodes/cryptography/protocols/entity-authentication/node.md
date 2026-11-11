---
tag: 99PD0N
kind: problem
slug: entity-authentication
name: Entity authentication
aliases:
- mutual authentication
- entity authentication problem
area: cryptography/protocols
level: intro
summary: Let a verifier become sure, during a run of a protocol, that a named party is present and taking part now, so that an attacker who watched earlier runs cannot pose as it.
prereqs: [message-authentication-code, digital-signature, nonce]
see_also: [challenge-response-authentication, schnorr-identification-protocol, feige-fiat-shamir-identification, authenticated-key-exchange, kerberos, needham-schroeder, tls-handshake, zero-knowledge-proof]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 10 (identification and entity authentication), Section 10.1 (objectives, the properties of identification protocols), Sections 10.2 to 10.4 (passwords, challenge-response, zero-knowledge), Section 10.5 (attacks)
  - paper: doi:10.1007/3-540-48329-2_21
    title: Mihir Bellare and Phillip Rogaway, Entity authentication and key distribution, CRYPTO 1993, LNCS 773, pages 232 to 249
    locator: the model with oracles for each session, matching conversations, and the definition of a secure mutual authentication protocol
  - paper: "ISO/IEC 9798, Information technology, Security techniques, Entity authentication, Parts 1 to 6"
    locator: Part 1 (general model), Part 2 (symmetric encipherment), Part 3 (digital signatures), Part 4 (cryptographic check functions), Part 5 (zero-knowledge techniques), Part 6 (manual data transfer)
  - paper: "Gavin Lowe, A hierarchy of authentication specifications, 10th IEEE Computer Security Foundations Workshop (CSFW 1997), pages 31 to 43"
    locator: aliveness, weak agreement, non-injective agreement and injective agreement
  - paper: "David Basin, Cas Cremers and Simon Meier, Provably repairing the ISO/IEC 9798 standard for entity authentication, Journal of Computer Security 21(6), 2013"
    locator: attacks found by machine on several mechanisms of the standard, and the repaired versions
  - paper: "Michel Abdalla, Jee Hea An, Mihir Bellare and Chanathip Namprempre, From identification to signatures via the Fiat-Shamir transform, EUROCRYPT 2002, LNCS 2332, pages 418 to 433"
    locator: the conditions under which a secure identification scheme gives a secure signature scheme
---

Entity authentication, also called identification, is the problem of letting one party, the verifier, become sure of the identity of another party, the claimant, and sure that the claimant is taking part in the protocol right now. It differs from message authentication in its time: a [MAC](/message-authentication-code/) or a [signature](/digital-signature/) on a message says who made the message at some time, while entity authentication says who is present in this run. This page states the problem. The main technique that solves it is [challenge-response authentication](/challenge-response-authentication/), and the formal model is the one of Bellare and Rogaway (1993), with matching conversations.

## In plain words

When you phone your bank, the bank wants to know two things: that the caller is you, and that you are on the line now, not a recording of an old call. The first is about who. The second is about when.

Entity authentication asks for both. A protocol solves it if an honest person who runs it is always accepted, and an impostor is almost never accepted, even if the impostor has listened to many earlier runs, can start runs of their own, and can mix messages from several runs at the same time. A version in which both sides check each other is called mutual authentication.

## Definition

**Parties and runs.** There is a set of parties, each with long-term secrets (shared keys, private keys or passwords) and public information. A *session* is one run of the protocol at one party. The adversary controls the network: it can deliver, change, drop, reorder and make messages, and it can start any number of sessions at any party.

**HAC objectives (Section 10.1.1).** For a claimant $A$ and a verifier $B$, an identification protocol must give:

1. *Completeness.* If $A$ and $B$ are honest and the messages arrive unchanged, $B$ accepts $A$.
2. *No transfer.* $B$ cannot use a run with $A$ to pose as $A$ to a third party $C$.
3. *No impersonation.* For each party $C \ne A$, the chance that $C$ makes $B$ accept the identity $A$ is negligible.
4. Items 2 and 3 stay true when the adversary has seen a polynomial number of earlier runs, may have taken part in them, and may run several sessions at the same time.

**The Bellare-Rogaway definition.** Each session is an oracle $\Pi^s_{i,j}$: party $i$ in its session $s$, which thinks it talks to party $j$. Its *conversation* is the ordered list of the messages that it sent and received, with times. Two sessions $\Pi^s_{i,j}$ and $\Pi^t_{j,i}$ have *matching conversations* when each message that one of them sent was received by the other in the same order, except possibly the last message, which the other may not have received yet. A mutual authentication protocol is *secure* when:

1. if two sessions have matching conversations, both accept; and
2. for each polynomial time adversary, the probability of the event *No-Matching* is negligible in $\lambda$, where No-Matching means that some session $\Pi^s_{i,j}$, with $i$ and $j$ uncorrupted, accepts although no session $\Pi^t_{j,i}$ has a conversation that matches it.

So the adversary may pass messages on, but it cannot make a party accept unless the named partner really took part in a run with the same messages. A unilateral version asks the second condition only for the verifier.

**Lowe's hierarchy.** For a responder $B$ that completes a run that it thinks is with $A$, Lowe (1997) lists guarantees of rising strength. *Aliveness*: $A$ has run the protocol at some time. *Weak agreement*: $A$ has run the protocol with $B$. *Non-injective agreement*: $A$ has run it with $B$ as its partner and they agree on the data values. *Injective agreement*: in addition, each run of $B$ matches a distinct run of $A$, so that replays fail. Matching conversations imply injective agreement on the whole transcript.

## Variants

- **Unilateral or mutual.** Only $B$ checks $A$, or both check each other. TLS on the web is unilateral by default; [Kerberos](/kerberos/) gives mutual authentication when the client asks for it.
- **Weak, strong and zero-knowledge.** HAC classes protocols by the claimant's secret and how much the protocol shows of it: passwords and PINs, which a verifier or an eavesdropper sees (Section 10.2); [challenge-response](/challenge-response-authentication/) with keys (Section 10.3); and [zero-knowledge](/zero-knowledge-proof/) protocols, which show nothing about the key (Section 10.4), such as the [Schnorr](/schnorr-identification-protocol/) and [Feige-Fiat-Shamir](/feige-fiat-shamir-identification/) protocols.
- **With a trusted third party.** In the [Needham-Schroeder](/needham-schroeder/) family and in Kerberos, a [key distribution center](/key-distribution-center/) vouches for the parties.
- **Together with a key.** [Authenticated key exchange](/authenticated-key-exchange/) asks for entity authentication and a shared session key at the same time. Bellare and Rogaway define both in one model. A protocol that authenticates the parties but sends data without a key bound to the run leaves the later data open to a man in the middle.
- **Password-based.** The claimant has only a low-entropy password, and the goal is to limit an attacker to one guess per run (see [password-authenticated key exchange](/password-authenticated-key-exchange/)).

## Examples

**A password over the network fails.** $A \to B$: $(A, pw)$. Completeness holds, but an eavesdropper replays the message and is accepted, so objective 4 fails. Sending $h(pw)$ instead does not help: the hash is the new password.

**A nonce and a MAC succeeds.** $B \to A$: $r_B$; $A \to B$: $\mathrm{MAC}_K(r_B \,\|\, B)$. If the MAC is EUF-CMA secure and $r_B$ has $n$ random bits, an impostor is accepted with probability at most the MAC advantage plus $q^2/2^{n+1}$ over $q$ sessions (proved on the [challenge-response](/challenge-response-authentication/) page).

**The same with no identity fails.** With the answer $\mathrm{MAC}_K(r_B)$ and a key shared in both directions, the reflection attack makes $B$ answer its own challenge in a second session. $B$ accepts in session 1 with no matching session at $A$, which is the event No-Matching.

**Aliveness without agreement.** In Lowe's attack on the Needham-Schroeder public-key protocol (see [the protocol page](/needham-schroeder-protocol/)), $B$ finishes a run that it thinks is with $A$. $A$ is alive and did run the protocol, but with the intruder as its partner. Aliveness holds and weak agreement fails. The [Needham-Schroeder lineage](/needham-schroeder/) page finds this attack with a small model checker.

**A standard with flaws.** Basin, Cremers and Meier (2013) analysed the mechanisms of ISO/IEC 9798 with a protocol verifier and found attacks on several of them, among them reflection and role mix-up attacks, and gave repaired versions that the ISO committee adopted.

## Known algorithms

- [Challenge-response authentication](/challenge-response-authentication/) with MACs, signatures or public-key encryption (ISO/IEC 9798-2, -3 and -4), and the one-pass HOTP and TOTP.
- Zero-knowledge identification: the [Schnorr identification protocol](/schnorr-identification-protocol/), [Feige-Fiat-Shamir identification](/feige-fiat-shamir-identification/), and [sigma protocols](/sigma-protocol/) in general.
- Third-party protocols: the [Needham-Schroeder protocols](/needham-schroeder-protocol/), the [Otway-Rees protocol](/otway-rees-protocol/), the [Yahalom protocol](/yahalom-protocol/) and [Kerberos](/kerberos/).
- Authentication with a key: the [station-to-station protocol](/station-to-station-protocol/), [SIGMA](/sigma-key-exchange/) and the [TLS 1.3 handshake](/tls-handshake/).

## Bounds

**Guessing.** If the verifier's decision depends on an answer of $\ell$ bits that the impostor cannot predict better than at random, one attempt succeeds with probability $2^{-\ell}$, so $v$ attempts succeed with probability at most $v \cdot 2^{-\ell}$ by the union bound. This is the reason for the bound $s v / 10^{d}$ of HOTP and for limits on the number of attempts.

**One message needs state.** *Claim.* A protocol in which the claimant sends one message and the verifier keeps no state between runs cannot stop replay. *Proof.* The verifier's decision is a function of its long-term keys, its clock and the message. If it keeps no state and the decision does not depend on a clock, then the message that it accepted in one run it accepts again in the next. So a one-pass protocol needs a clock (a timestamp and a window), a counter, or a cache of seen messages. $\square$

**Mutual authentication with nonces needs three messages.** *Claim.* If each party's freshness comes only from its own random challenge, mutual authentication needs at least three messages. *Proof.* Each party must receive an answer that depends on its own challenge, so the answer to $A$'s challenge is sent after $A$'s challenge, and the answer to $B$'s challenge after $B$'s challenge. Suppose there are only two messages. If one party sends both, the other party sends nothing and cannot be authenticated. Otherwise the first is sent by $X$ and the second by $Y$. Then $X$ sends nothing after it receives anything, so no message depends on $Y$'s challenge, and $Y$ cannot authenticate $X$. So two messages are not enough. The three-pass protocols of ISO/IEC 9798 reach this bound: $B \to A: r_B$; $A \to B: r_A, \mathrm{MAC}_K(r_A, r_B, B)$; $B \to A: \mathrm{MAC}_K(r_B, r_A, A)$. $\square$ With timestamps, two messages are enough for mutual authentication, as in the one-pass mechanisms of ISO/IEC 9798 used in both directions.

## Reductions

- **From a MAC or a signature.** An EUF-CMA secure MAC or signature scheme gives a secure unilateral protocol by challenge-response, with a loss of the term $q^2/2^{n+1}$ for nonce collisions. With identities in the signed data, it gives mutual authentication in the Bellare-Rogaway model.
- **From identification to signatures.** The Fiat-Shamir transform turns a public-coin identification protocol into a signature scheme in the [random oracle model](/random-oracle-model/). Abdalla, An, Bellare and Namprempre (2002) show that security against passive impersonation of the identification scheme, with the right form of the challenge, gives EUF-CMA security of the signature.
- **Into key exchange.** An entity authentication protocol does not give a key. A key exchange with explicit authentication, such as SIGMA, solves both problems together; a key exchange with only implicit authentication becomes explicit with [key confirmation](/key-confirmation/).

## Applications

Logins to computers and services, second factors (HOTP, TOTP, FIDO keys), smart cards and car keys, the network authentication of [Kerberos](/kerberos/), the server and client authentication of the [TLS handshake](/tls-handshake/), and each [authenticated key exchange](/authenticated-key-exchange/). The problem also sets the goals that protocol analysis tools check, for example in the [Needham-Schroeder lineage](/needham-schroeder/).

## References
