---
tag: 9NTM5E
kind: algorithm
slug: needham-schroeder-protocol
name: Needham-Schroeder protocols and their attacks
area: cryptography/key-exchange
level: advanced
summary: The 1978 shared-key and public-key protocols of Needham and Schroeder, step by step, with the Denning-Sacco replay on the first, Lowe's attack on the second, and the fixes.
solves: [key-distribution-problem]
model: word-ram
complexity:
  vars: {l: the total length of the messages in bits}
  time: {worst: Θ(l), average: Θ(l), best: Θ(l)}
  space: {extra: Θ(l)}
properties: {deterministic: false, randomized: true}
history:
  year: 1978
  people: [Roger Needham, Michael Schroeder, Dorothy Denning, Giovanni Maria Sacco, Gavin Lowe]
  note: Needham and Schroeder published both protocols in 1978; Denning and Sacco found the replay in 1981, and Lowe found the attack on the public-key protocol in 1995.
prereqs: [key-distribution-center]
see_also: [needham-schroeder, kerberos, denning-sacco-protocol, otway-rees-protocol, yahalom-protocol, wide-mouthed-frog-protocol, entity-authentication, challenge-response-authentication]
sources:
  - paper: "Roger M. Needham and Michael D. Schroeder, Using encryption for authentication in large networks of computers, Communications of the ACM 21(12), December 1978, pages 993 to 999"
    locator: the shared-key protocol with an authentication server and the public-key protocol
  - paper: "Dorothy E. Denning and Giovanni Maria Sacco, Timestamps in key distribution protocols, Communications of the ACM 24(8), August 1981, pages 533 to 536"
    locator: the replay of an old ticket with a compromised session key, and the fix with timestamps
  - paper: "Gavin Lowe, An attack on the Needham-Schroeder public-key authentication protocol, Information Processing Letters 56(3), 1995"
    locator: the attack in which an intruder uses a run with the initiator to pose as the initiator (pages to check)
  - paper: "Gavin Lowe, Breaking and fixing the Needham-Schroeder public-key protocol using FDR, TACAS 1996, LNCS 1055, Springer, 1996, pages 147 to 166"
    locator: the attack found by model checking with FDR and the fixed protocol with the responder's name in message 2
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Protocol 12.26 (shared-key protocol) and Protocol 12.38 (public-key protocol)
  - paper: "John Clark and Jeremy Jacob, A survey of authentication protocol literature, version 1.0, 1997"
    locator: Section 6.3.1 (the shared-key protocol and the Denning-Sacco attack) and the section on the public-key protocol and Lowe's attack (section number to check)
---

The Needham-Schroeder protocols are the two key distribution protocols that Roger Needham and Michael Schroeder published in 1978. In the shared-key protocol (NSSK), a trusted server $S$ that shares a long-term key with each user makes a session key $K$ for $A$ and $B$, sends it to $A$ with a "ticket" for $B$, and the two finish with a nonce handshake. In the public-key protocol (NSPK), $A$ and $B$ exchange nonces encrypted under each other's public keys. Both became classic examples of protocol flaws: in 1981 Denning and Sacco showed that an attacker with an old session key can replay an old ticket to $B$, and in 1995 Lowe showed that NSPK lets an attacker pose as $A$ to $B$. This page gives both protocols as algorithms, with the attacks and fixes. The page [Needham-Schroeder protocol](/needham-schroeder/) covers the protocol in practice and its place in network authentication; [Kerberos](/kerberos/) is its best-known descendant.

**Notation.** $\{m\}_K$ is $m$ encrypted (and integrity-protected) under the symmetric key $K$; $\{m\}_{pk_B}$ is $m$ encrypted under $B$'s public key. $K_{AS}$ and $K_{BS}$ are the long-term keys that $A$ and $B$ share with $S$. $N_A$ and $N_B$ are nonces, fresh random numbers used once.

## In plain words

Alice wants to talk to Bob, and each of them shares a secret key with a trusted server, but not with each other. Alice asks the server for a key. The server makes a new key and sends it to Alice in a box that only Alice can open. Inside it is a second box, the ticket, that only Bob can open; it holds the same key and Alice's name. Alice gives the ticket to Bob. Bob then checks that Alice really has the key, by sending her a random number to change.

The flaw is that Bob cannot tell if the ticket is new. If an old key is ever stolen, the thief can replay the old ticket and Bob will accept the old key again.

## The problem

Users who share keys only with a [key distribution center](/key-distribution-center/) need fresh session keys for each pair of users, with [entity authentication](/entity-authentication/) of each party to the other. This is the [key distribution problem](/key-distribution-problem/). The public-key protocol solves mutual authentication when each party has the other's public key.

## The algorithm

The shared-key protocol has five messages. Each line names the party that acts.

```pseudo id=main
NEEDHAM-SCHROEDER-SK(A, B, S)
L1  A → S: A, B, N_A
L2  S: K ← fresh key; S → A: {N_A, B, K, {K, A}_{K_BS}}_{K_AS}
L3  A: decrypt; if N_A or B is wrong then fail; A → B: {K, A}_{K_BS}
L4  B: decrypt, get K and A; N_B ← fresh nonce; B → A: {N_B}_K
L5  A: decrypt; A → B: {N_B − 1}_K
L6  B: if the value is not N_B − 1 then fail; accept K as shared with A
```

At line L3, the nonce $N_A$ shows $A$ that the reply is fresh and answers its own request, and the name $B$ shows that $S$ made the key for the right peer. The ticket $\{K, A\}_{K_{BS}}$ tells $B$ that $S$ made $K$ for a session with $A$. Lines L4 to L6 are a [challenge-response](/challenge-response-authentication/) step: the answer $N_B - 1$ (not $N_B$, which an attacker could copy back) shows $B$ that someone with $K$ is present now.

The public-key protocol (core part, with the public keys already known) has three messages:

1. $A \to B$: $\{N_A, A\}_{pk_B}$
2. $B \to A$: $\{N_A, N_B\}_{pk_A}$
3. $A \to B$: $\{N_B\}_{pk_B}$

Each party accepts when its own nonce comes back, and the two nonces were meant to be a shared secret.

**About the code.** The Python code implements both protocols, the Denning-Sacco replay, Lowe's attack and the two fixes, with local simulated parties. The symmetric encryption is a toy encrypt-then-MAC; the public-key encryption is modelled symbolically (a box addressed to a name opens only for that name), as in the Dolev-Yao model, because the attacks do not depend on the cipher. It is for study only. It is not constant time, and these protocols must not protect real data. Use Kerberos (MIT Kerberos or Heimdal) or TLS 1.3.

## Example

An honest run of the shared-key protocol, and Lowe's attack on the public-key protocol. In the attack, $A$ starts a normal run with the dishonest user $E$, and $E(A)$ means $E$ posing as $A$.

| step | honest NSSK run | Lowe's attack on NSPK |
|---|---|---|
| 1 | $A \to S$: $A, B, N_A$ | $A \to E$: $\{N_A, A\}_{pk_E}$ |
| 2 | $S \to A$: $\{N_A, B, K, \{K, A\}_{K_{BS}}\}_{K_{AS}}$ | $E(A) \to B$: $\{N_A, A\}_{pk_B}$ |
| 3 | $A \to B$: $\{K, A\}_{K_{BS}}$ | $B \to E(A)$: $\{N_A, N_B\}_{pk_A}$, forwarded to $A$ |
| 4 | $B \to A$: $\{N_B\}_K$ | $A \to E$: $\{N_B\}_{pk_E}$ |
| 5 | $A \to B$: $\{N_B - 1\}_K$ | $E(A) \to B$: $\{N_B\}_{pk_B}$ |
| result | $B$ accepts $K$ with $A$ | $B$ accepts $A$ as peer; $E$ knows $N_A$ and $N_B$ |

## Correctness

In an honest run, $A$ gets back its own nonce and the name $B$ at line L3, $B$ gets $K$ and $A$ from the ticket at line L4, and $A$ returns $N_B - 1$, so $B$ accepts at line L6, and both hold the same $K$. The proof is below.

Correctness does not mean security. The protocol assumes that old session keys stay secret forever. The Denning-Sacco attack breaks it when one old key leaks, and Lowe's attack shows that NSPK does not give $B$ the guarantee it seems to give.

## Complexity

Each party does a constant number of encryptions and decryptions, linear in the message length $l$, so the time is $\Theta(l)$ for symmetric ciphers. The shared-key protocol has five messages and the public-key core three (seven with the requests for public keys from the server). The server keeps no session state.

## Properties

- **Freshness for $A$** from its nonce $N_A$ at line L3.
- **No freshness for $B$** of the key: the ticket at line L4 carries nothing that $B$ knows to be new.
- **Key confirmation** in both directions, from lines L4 to L6.
- **NSPK authenticates $A$ to $B$ only weakly.** After Lowe's fix it gives mutual authentication and secret nonces in the symbolic model.

## Variants and improvements

- **Denning-Sacco timestamps.** Put a timestamp in the ticket; see the [Denning-Sacco protocol](/denning-sacco-protocol/).
- **The 1987 fix.** Needham and Schroeder ("Authentication revisited", 1987) let $B$ first give $A$ a nonce, sent under $K_{BS}$, that $S$ puts into the ticket. The code uses a simplified form in which $B$'s nonce goes in clear.
- **Kerberos** adds timestamps, lifetimes and a ticket-granting server; see [Kerberos](/kerberos/).
- **Needham-Schroeder-Lowe (NSL).** Message 2 becomes $\{N_A, N_B, B\}_{pk_A}$, and $A$ checks the name.
- **Otway-Rees and Yahalom** give both parties nonces in the request; see [Otway-Rees](/otway-rees-protocol/) and [Yahalom](/yahalom-protocol/).

## When to use it

Do not use either protocol as written. Study them as the first examples of the design and analysis of key distribution protocols. In practice use Kerberos for a server-based setting and TLS 1.3 or another authenticated key exchange with public keys.

## Pitfalls

- **Replay of an old ticket.** At line L4, $B$ accepts any ticket under $K_{BS}$. An attacker who has recorded the old ticket $\{K', A\}_{K_{BS}}$ and has learned the old key $K'$ sends the ticket to $B$, decrypts $\{N_B\}_{K'}$, and sends back $\{N_B - 1\}_{K'}$ at line L5. $B$ then believes it shares $K'$ with $A$. The tests run this attack.
- **The name in message 2 of NSPK.** Without $B$'s name in $\{N_A, N_B\}_{pk_A}$, $A$ cannot tell that the reply comes from a run with $B$ and not with the $E$ it meant to talk to. Lowe found this with the FDR model checker 17 years after publication.
- **Unauthenticated encryption.** The 1978 paper assumed that encryption also protects integrity. With a malleable cipher, the parts of the messages at lines L2 and L3 can be cut and changed.
- **Nonces as keys.** Using $N_A$ and $N_B$ of NSPK as key material is unsafe, because the attack gives both to $E$.

## Implementations

## History

Needham and Schroeder published the two protocols in Communications of the ACM in 1978, in one of the first papers on authentication in networks. Denning and Sacco showed the replay in 1981 and proposed timestamps. Needham and Schroeder replied with a nonce-based fix in 1987. The shared-key protocol became the basis of Kerberos at MIT in the 1980s. Burrows, Abadi and Needham analysed both protocols with BAN logic in 1989. In 1995 Lowe found the attack on the public-key protocol, and in 1996 he showed how to find it with the FDR model checker, which made the protocol a standard test case for formal methods.

## References
