---
tag: ZVT3WS
kind: concept
slug: key-distribution-center
name: Key distribution center
aliases:
- KDC
- trusted key server
area: cryptography/protocols
level: intro
summary: A trusted server that shares one long-term key with each user and makes session keys on request, so n users need n keys, not n(n-1)/2. Kerberos is the main example.
prereqs: [session-key, key-distribution-problem]
see_also: [kerberos, needham-schroeder-protocol, needham-schroeder, otway-rees-protocol, wide-mouthed-frog-protocol, denning-sacco-protocol, public-key-encryption, threshold-cryptography]
sources:
  - paper: doi:10.1145/359657.359659
    title: Roger M. Needham and Michael D. Schroeder, Using encryption for authentication in large networks of computers, Communications of the ACM 21(12), 1978, pages 993 to 999
    locator: the authentication server that shares a secret key with each principal and issues conversation keys; the comparison with the public-key directory
  - url: "https://www.rfc-editor.org/rfc/rfc4120"
    title: Clifford Neuman, Tom Yu, Sam Hartman and Ken Raeburn, RFC 4120, The Kerberos Network Authentication Service (V5), July 2005
    locator: Section 1 (principals, realms, the KDC as authentication server and ticket-granting server), Section 1.2 (cross-realm operation), Section 3 (the message exchanges)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 12, Section 12.3 (key transport with a server); Chapter 13, Section 13.2 (trusted third parties, key distribution and key translation centers)
---

A key distribution center (KDC) is a trusted server that shares one secret long-term key with each user of a network. When user $A$ wants to talk to user $B$, the KDC makes a fresh [session key](/session-key/) $K_{AB}$ and sends it to both, each copy encrypted under the long-term key of its receiver. With $n$ users, the KDC stores $n$ long-term keys, while a network in which each pair shares its own key needs $n(n-1)/2$. The price is trust: the KDC knows every session key that it issues, it can pose as any user, and when it is down no new session can start. Needham and Schroeder described the design in 1978, and [Kerberos](/kerberos/) is the KDC in wide use today.

**Notation.** $A$ and $B$ are users and $S$ is the KDC. $K_{AS}$ is the long-term key that $A$ shares with $S$. $\{m\}_K$ is the authenticated encryption of $m$ under $K$. $N_A$ is a [nonce](/nonce/) of $A$. $n$ is the number of users.

## In plain words

A company has many offices that must send each other locked boxes. If each pair of offices kept its own key, the number of keys would grow very fast, and each new office would need a new key from every other office.

Instead, the company has one trusted key office. Each branch shares one key with the key office and with no one else. When two branches want to talk, they ask the key office. It cuts a new key for that conversation and sends one copy to each branch, each copy locked with that branch's own key.

This is simple and cheap. But the key office now holds the keys to everything. A thief who breaks into it can read all the traffic, and when it closes for the day, no new conversation can start.

## The idea

### Why a center

The [key distribution problem](/key-distribution-problem/) asks how $n$ users get shared keys. With pairwise keys, each pair needs its own secret channel at setup time, so the network needs $n(n-1)/2$ keys, each user stores $n-1$ of them, and a new user needs $n$ new keys. With a KDC, each user needs one secure setup, with the KDC only. The network has $n$ long-term keys, each user stores one, and a new user needs one new key. The KDC makes session keys on demand, so a session key can be short-lived, and a stolen session key exposes only one session.

### The basic flow

A minimal flow with a ticket has three messages:

1. $A \to S$: $A, B, N_A$
2. $S \to A$: $\{K_{AB}, B, N_A, L\}_{K_{AS}}$, $\{K_{AB}, A, L\}_{K_{BS}}$
3. $A \to B$: $\{K_{AB}, A, L\}_{K_{BS}}$

$L$ is a lifetime or expiry time. The second part of message 2 is the *ticket*: $A$ cannot read it, and passes it on to $B$. Each field has a job. $N_A$ in the reply tells $A$ that the reply is fresh and answers this request. The name $B$ in the reply tells $A$ that the key is for $B$ and not for someone that an attacker put in place of $B$. The name $A$ in the ticket tells $B$ who the peer is. The expiry $L$ limits how long a stolen ticket is useful. This flow does not tell $B$ that the ticket is fresh, and it does not show either party that the other holds $K_{AB}$. Real protocols add those steps: the [Needham-Schroeder protocol](/needham-schroeder-protocol/) adds a nonce handshake between $A$ and $B$, and Kerberos adds an authenticator with a timestamp. The [Needham-Schroeder lineage page](/needham-schroeder/) shows how the missing freshness check for $B$ led to the [Denning-Sacco](/denning-sacco-protocol/) attack and to timestamps.

Other server-based protocols move the work around. In the [Otway-Rees protocol](/otway-rees-protocol/), $B$ contacts the server. In the [wide-mouthed frog protocol](/wide-mouthed-frog-protocol/), $A$ makes the key and the server only translates it from $K_{AS}$ to $K_{BS}$. The Handbook of Applied Cryptography calls such a server a key translation center (KTC), as opposed to a KDC, which makes the key itself.

### The cost of trust

The KDC is a single point of trust. It knows each long-term key, so it can pose as any user, and it knows each session key that it made. An attacker who copies the KDC database and has recorded old traffic can open every recorded ticket and read every recorded session. The design gives no forward secrecy against the compromise of the KDC; a session needs a Diffie-Hellman exchange on top for that (Kerberos has optional extensions for this, such as PKINIT with Diffie-Hellman, RFC 4556).

The KDC is also a single point of failure. A user who cannot reach the KDC cannot start a new session, and the KDC must answer each new session in real time. Real deployments run replica KDCs with copies of the database, which adds more places that hold every key. Kerberos reduces the load with a ticket-granting ticket that lets a user get many service tickets with one login.

### A KDC versus a certificate authority

A certificate authority (CA) of a public-key system is also a trusted third party, but its trust is of a different kind. The CA signs a binding of a name to a public key, and it never sees a private key. So a dishonest or broken CA can issue a false certificate and help an active attacker pose as a user, but it cannot read traffic that it did not take part in. The CA can work offline, because users check certificates with the CA's public key without asking it. A KDC is online for each session and can read everything that it keys. Public keys cost more computation and a revocation system, which mattered more in 1978 than today.

### Words from RFC 4120

Kerberos names each user or service a *principal*, and the set of principals that one KDC serves a *realm*. The Kerberos KDC has two parts: the authentication server (AS), which checks the user's long-term key and issues a ticket-granting ticket (TGT), and the ticket-granting server (TGS), which takes the TGT and issues service tickets. A *ticket* is the KDC's sealed statement of a session key, the client name and a validity period, encrypted under the long-term key of the service. An *authenticator* is a fresh message that the client seals under the session key to show that it holds the key now. Two realms can trust each other through a cross-realm key that the two KDCs share; the TGS of the first realm then issues a TGT for the second (RFC 4120 Section 1.2).

## Examples

**Counting keys.** For $n = 1000$ users, pairwise keys need $1000 \cdot 999 / 2 = 499{,}500$ keys and each user stores 999. A KDC needs 1000 keys, one per user, and each user stores one. When user 1001 joins, the pairwise design needs 1000 new keys, delivered to 1000 different users, and the KDC design needs one. The code builds both networks and counts the keys: for $n = 2, 3, 5, 10, 20$ it finds $n$ keys for the KDC and $n(n-1)/2$ for the pairwise network.

**Counting messages.** Pairwise keys need no message to start a session. The toy flow above needs three messages per session, two of which involve the KDC. The [Needham-Schroeder protocol](/needham-schroeder-protocol/) needs five, and Kerberos needs two for the AS exchange once per login, then two for each service ticket and one or two for each service. So the KDC design trades storage and setup for an online server and a few messages per session.

**What a stolen database gives.** In the code, a KDC with five users issues ten tickets, which an observer records. An attacker who later copies the KDC's key table opens all ten tickets and finds all ten session keys. An observer without the table opens none.

**The code.** The Python code builds a KDC network and a pairwise network and counts keys and messages. Its encryption is a study AEAD, encrypt-then-MAC with an HMAC-SHA256 key stream and an HMAC-SHA256 tag; it is not a standard AEAD such as [GCM](/gcm-mode/). The tests check the counts, that both parties get the same fresh session key, that a ticket fails after its expiry, at the wrong receiver or with the wrong sender name, and that a database copy opens recorded tickets. No official test vectors exist for a generic KDC. The code is for study only, is not constant time, and must not protect real data. Use MIT Kerberos, Heimdal or Active Directory for a real KDC.

## Where it is used

- **Kerberos.** [Kerberos](/kerberos/) is the main KDC in use. It is the default authentication of Windows domains (Active Directory), and it is used in many Unix sites and in Hadoop clusters.
- **Older standards.** The ANSI X9.17 standard for banking key management (1985) used key centers with symmetric keys. GSM and UMTS mobile networks use a related design: the home network's authentication center shares one key with each SIM card and gives keys for each session to the network that serves the phone.
- **Inside larger systems.** A cloud key management service that wraps data keys under a master key for many clients has the same trust structure, and so has the same single point of trust.
- **Splitting the trust.** [Threshold cryptography](/threshold-cryptography/) can split the KDC's secrets over several servers, so that no single server can read the session keys.
- **Public-key alternatives.** [Public-key encryption](/public-key-encryption/) with certificates removes the online center at the cost of more computation and a revocation system, as in TLS.

## References
