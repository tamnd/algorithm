---
tag: X3KF0J
kind: algorithm
slug: denning-sacco-protocol
name: Denning-Sacco protocol
area: cryptography/key-exchange
level: advanced
summary: Two 1981 key distribution protocols. One adds timestamps to the Needham-Schroeder ticket; the other sends a signed session key with certificates, which Abadi and Needham showed flawed.
solves: [key-distribution-problem]
model: word-ram
complexity:
  vars: {l: the total length of the messages in bits}
  time: {worst: Θ(l), average: Θ(l), best: Θ(l)}
  space: {extra: Θ(l)}
properties: {deterministic: false, randomized: true}
history:
  year: 1981
  people: [Dorothy Denning, Giovanni Maria Sacco]
  note: Denning and Sacco proposed both protocols in 1981 to stop the replay attack on Needham-Schroeder; Abadi and Needham published the attack on the public-key one in 1994 and 1996.
prereqs: [needham-schroeder-protocol]
see_also: [kerberos, key-distribution-center, digital-signature, unknown-key-share-attack, otway-rees-protocol, wide-mouthed-frog-protocol, entity-authentication, session-key]
sources:
  - paper: "Dorothy E. Denning and Giovanni Maria Sacco, Timestamps in key distribution protocols, Communications of the ACM 24(8), August 1981, pages 533 to 536"
    locator: the timestamp fix of the shared-key protocol, the public-key protocol, and the bound d1 + d2 on clock skew and network delay
  - paper: "Martín Abadi and Roger Needham, Prudent engineering practice for cryptographic protocols, IEEE Transactions on Software Engineering 22(1), January 1996, pages 6 to 15"
    locator: the attack on the public-key protocol and the principle that a signed message must name the parties it is meant for; earlier as DEC SRC Research Report 125, 1994
  - paper: "John Clark and Jeremy Jacob, A survey of authentication protocol literature, version 1.0, 1997"
    locator: Section 6.3.2 (the shared-key protocol) and Section 6.9 (the public-key protocol and its attack)
  - paper: "Li Gong, A security risk of depending on synchronized clocks, ACM SIGOPS Operating Systems Review 26(1), 1992, pages 49 to 53"
    locator: replays that exploit clocks that are wrong or out of step (pages to check)
---

The Denning-Sacco protocols are two key distribution protocols that Dorothy Denning and Giovanni Maria Sacco proposed in 1981. The first is a shared-key protocol: it fixes the replay attack on the [Needham-Schroeder protocol](/needham-schroeder-protocol/) by putting a timestamp $T$ from the server into the ticket, so that $B$ can tell that the session key is new without a nonce handshake. It needs only three messages, but it needs clocks that agree. The second is a public-key protocol: a server issues certificates, and $A$ sends $B$ a session key that $A$ signs and encrypts for $B$. Abadi and Needham later showed that $B$ can reuse $A$'s signature to pose as $A$ to a third party, because the signed message does not name $B$.

**Notation.** $\{m\}_K$ is $m$ encrypted and integrity-protected under the symmetric key $K$. $K_{AS}$ and $K_{BS}$ are long-term keys shared with the server $S$. $T$ is a timestamp. $\delta_1$ bounds the difference between the clocks of the parties and the server, and $\delta_2$ bounds the network delay. $C_X = \mathrm{Sig}_S(X, pk_X, T)$ is a certificate, $\mathrm{Sig}_A$ is a signature by $A$, and $\{m\}_{pk_B}$ is public-key encryption for $B$.

## In plain words

In the Needham-Schroeder protocol, Bob cannot tell whether a ticket from the server is new or a copy of an old one. Denning and Sacco add the time to the ticket. The server writes the current time next to the new key, and Bob accepts the ticket only if that time is close to his own clock. An old ticket is then useless, even if its key was stolen.

The price is that all computers must keep their clocks close, and a copy of a ticket made a few seconds ago is still accepted unless Bob remembers what he has seen.

## The problem

As for Needham-Schroeder: users who share keys with a [key distribution center](/key-distribution-center/) need fresh session keys for pairs of users. The extra goal is that $B$ gets a guarantee that the key is fresh, so that the compromise of an old key does not let an attacker pose as $A$ later.

## The algorithm

The shared-key protocol. Each line names the party that acts.

```pseudo id=main
DENNING-SACCO-SK(A, B, S)
L1  A → S: A, B
L2  S: K ← fresh key; T ← clock of S; S → A: {B, K, T, {A, K, T}_{K_BS}}_{K_AS}
L3  A: if B is wrong or |clock_A − T| > δ1 + δ2 then fail; A → B: {A, K, T}_{K_BS}
L4  B: if |clock_B − T| > δ1 + δ2 then fail; accept K as shared with A
```

The timestamp $T$ replaces both nonces of Needham-Schroeder. At line L3, $A$ checks the name and the time, so the reply is new and for the right peer. At line L4, $B$ checks that the ticket was made recently; an old ticket fails, even if its key has leaked. There is no key confirmation: $B$ does not learn that $A$ holds $K$ until $K$ is used.

The public-key protocol has the same first message:

1. $A \to S$: $A, B$
2. $S \to A$: $C_A, C_B$
3. $A \to B$: $C_A, C_B, \{\mathrm{Sig}_A(K, T_A)\}_{pk_B}$

$B$ checks the certificates and the signature of $A$ and the time $T_A$, and takes $K$ as a key shared with $A$.

**About the code.** The Python code implements both protocols with integer clocks, the replay within the time window, and Abadi's attack and its fix. The symmetric encryption is a toy encrypt-then-MAC; the signatures and the public-key encryption are modelled symbolically, as in the Dolev-Yao model. It is for study only. It is not constant time, and these protocols must not protect real data. Use Kerberos (MIT Kerberos or Heimdal), which uses timestamps in this way, or TLS 1.3.

## Example

The public-key protocol and Abadi's attack. $B$ is a dishonest user who receives a correct run from $A$ and wants $C$ to believe that $C$ shares a key with $A$.

| step | message | what the receiver concludes |
|---|---|---|
| 1 | $A \to S$: $A, B$ | |
| 2 | $S \to A$: $C_A, C_B$ | $A$ has $B$'s public key |
| 3 | $A \to B$: $C_A, C_B, \{\mathrm{Sig}_A(K, T_A)\}_{pk_B}$ | $B$ shares $K$ with $A$ (true) |
| attack | $B(A) \to C$: $C_A, C_C, \{\mathrm{Sig}_A(K, T_A)\}_{pk_C}$ | $C$ shares $K$ with $A$ (false: $B$ knows $K$) |

$B$ only decrypts the signature and encrypts it again for $C$. The signature is valid and the time $T_A$ is recent, so $C$ accepts. The fix of Abadi and Needham is to sign $(A, B, K, T_A)$: then $C$ sees that the key was meant for $B$.

## Correctness

In an honest run, $A$ receives its own peer name and a recent time at line L3, and $B$ receives $A$, $K$ and the same recent time at line L4. If the clocks differ by at most $\delta_1$ from the server's and the messages take at most $\delta_2$, both checks pass, and both hold the same $K$. The proof is below.

## Complexity

Each party does a constant number of symmetric encryptions or decryptions, so the time is $\Theta(l)$ in the message length $l$. The shared-key protocol has three messages, two fewer than Needham-Schroeder. The cost moves to clock synchronization, which itself needs a secure protocol.

## Properties

- **Freshness for both parties** from the server's timestamp, within the window $\delta_1 + \delta_2$.
- **No key confirmation** and no evidence for $B$ that $A$ is present.
- **Replays within the window** are not stopped by timestamps alone.
- **The public-key protocol** gives $B$ a key signed by $A$, but in its original form it does not say for whom.

## Variants and improvements

- **Kerberos** uses timestamped tickets in this way, with lifetimes, authenticators and a cache of recent authenticators; see [Kerberos](/kerberos/).
- **Nonces in place of clocks.** The 1987 Needham-Schroeder fix and the [Otway-Rees](/otway-rees-protocol/) and [Yahalom](/yahalom-protocol/) protocols give $B$ freshness with nonces.
- **The fixed public-key protocol.** Sign $(A, B, K, T_A)$, as Abadi and Needham suggest; today one would also use an [authenticated key exchange](/authenticated-key-exchange/) with forward secrecy.

## When to use it

Use the ideas, not the protocol. Timestamps make sense where clocks are managed and secured, as in a Kerberos domain, and only with a replay cache. The public-key protocol, even when fixed, has no forward secrecy: use TLS 1.3 or another authenticated Diffie-Hellman exchange.

## Pitfalls

- **Replays within the window.** At line L4, $B$ accepts the same ticket again as long as it is recent. Keep a cache of the tickets seen in the last $\delta_1 + \delta_2$. The tests show the replay.
- **Clocks that drift or can be set.** If an attacker can change $B$'s clock, or the server's clock runs ahead, old or future tickets pass line L4. Gong (1992) described such "suppress-replay" attacks. Secure the time service.
- **The window too wide.** A large $\delta_1 + \delta_2$ makes the protocol usable on slow networks but widens the time for replays.
- **Signatures that do not name the receiver.** In the public-key protocol, $\mathrm{Sig}_A(K, T_A)$ can be forwarded to anyone. This is Abadi's attack, a form of [unknown key-share](/unknown-key-share-attack/).

## Implementations

## History

Denning and Sacco published "Timestamps in key distribution protocols" in Communications of the ACM in 1981, in answer to the replay on the 1978 Needham-Schroeder protocol. Needham and Schroeder replied in 1987 with a fix based on nonces, arguing against the need for synchronized clocks. Kerberos, designed at MIT in the 1980s, adopted timestamps. Abadi and Needham showed the attack on the public-key protocol in a 1994 report, published in IEEE Transactions on Software Engineering in 1996, as an example of the principle that a message must say explicitly what it means and for whom.

## References
