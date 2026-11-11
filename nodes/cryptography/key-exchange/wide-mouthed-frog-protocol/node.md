---
tag: CYAP9N
kind: algorithm
slug: wide-mouthed-frog-protocol
name: Wide-mouthed frog protocol
aliases:
- wide-mouth frog
area: cryptography/key-exchange
level: advanced
summary: A two-message protocol in which A makes a session key and a server passes it to B with timestamps. Because both messages have the same form, a replay can keep an old key looking fresh.
solves: [key-distribution-problem]
model: word-ram
complexity:
  vars: {l: the total length of the messages in bits}
  time: {worst: Θ(l), average: Θ(l), best: Θ(l)}
  space: {extra: Θ(l)}
properties: {deterministic: false, randomized: true}
history:
  year: 1989
  people: [Michael Burrows, Martín Abadi, Roger Needham]
  note: Burrows, Abadi and Needham gave the protocol in their 1989 BAN logic report as an example of a very simple key distribution protocol.
prereqs: [key-distribution-center]
see_also: [denning-sacco-protocol, needham-schroeder-protocol, otway-rees-protocol, yahalom-protocol, kerberos, session-key, entity-authentication, key-transport-problem]
sources:
  - paper: "Michael Burrows, Martín Abadi and Roger Needham, A logic of authentication, DEC SRC Research Report 39, February 1989; also ACM Transactions on Computer Systems 8(1), 1990, pages 18 to 36"
    locator: the protocol and its BAN analysis (section to check)
  - paper: "John Clark and Jeremy Jacob, A survey of authentication protocol literature, version 1.0, 1997"
    locator: Section 6.3.5 (the protocol, the replay within the window, and the attack that keeps the timestamp fresh, described as found independently by several authors)
  - paper: "Ross Anderson and Roger Needham, Programming Satan's computer, in Computer Science Today, LNCS 1000, Springer, 1995"
    locator: the attack that bounces the server's message back to it (pages to check)
---

The wide-mouthed frog protocol is a key distribution protocol with only two messages. $A$ makes a session key $K$ and sends it, with a timestamp and $B$'s name, to the server $S$ under the key they share. $S$ checks the timestamp and sends $K$ on to $B$, with its own timestamp and $A$'s name, under the key it shares with $B$. Burrows, Abadi and Needham gave it in their 1989 BAN logic paper as a minimal design. It is now a standard example of what can go wrong: because the two messages have the same form, an attacker can send $S$'s message back to $S$ as a new request and get a new timestamp on the same key, again and again, so an old key keeps looking fresh.

**Notation.** $\{m\}_K$ is $m$ encrypted and integrity-protected under the symmetric key $K$. $K_{AS}$ and $K_{BS}$ are long-term keys shared with $S$. $T_A$ and $T_S$ are timestamps from the clocks of $A$ and $S$, and $\Delta$ is the accepted age of a message (clock skew plus delay).

## In plain words

Alice wants to send Bob a new key, and each of them shares a secret key with a server. Alice makes the key herself. She locks it with the time and Bob's name and sends it to the server. The server checks the time, then locks the key again for Bob, with the current time and Alice's name. Bob checks the time and takes the key.

The danger is that the message to Bob looks just like a message to the server. An attacker can send it back to the server as if Bob were sending a key to Alice, and get a new message with a new time. By doing this again and again, the attacker can keep an old key looking new.

## The problem

The [key distribution problem](/key-distribution-problem/) with a [key distribution center](/key-distribution-center/), in its smallest form: $A$ chooses the key, and the server only passes it on, as [key transport](/key-transport-problem/) through a trusted relay. The goal is that $B$ gets a fresh key from $A$ with two messages and no state at the server.

## The algorithm

Each line names the party that acts.

```pseudo id=main
WIDE-MOUTHED-FROG(A, B, S)
L1  A: K ← fresh key; T_A ← clock of A; A → S: A, {T_A, B, K}_{K_AS}
L2  S: decrypt with K_AS; if |clock − T_A| > Δ then fail; S → B: {T_S, A, K}_{K_BS}
L3  B: if |clock − T_S| > Δ then fail; accept K as shared with A
```

At line L2 the server uses the name in clear to choose $K_{AS}$, and learns from the timestamp that the request is recent. At line L3, $B$ learns that $S$ passed on a key from $A$ recently. Nothing tells $B$ how old the key itself is: the timestamp $T_S$ says when $S$ forwarded the key, not when $A$ made it.

**About the code.** The Python code implements the protocol with integer clocks, the attack that keeps a key alive, and a fix with message labels. The encryption is a toy encrypt-then-MAC. It is for study only. It is not constant time, and this protocol must not protect real data. Use Kerberos (MIT Kerberos or Heimdal) or TLS 1.3.

## Example

The attack, with $\Delta = 30$ seconds. $A$ sends a key $K$ at time 1000. The attacker $E$ records message 2 and bounces each new message 2 back to $S$ every 20 seconds, each time as a message 1 from its recipient.

| time | message | effect |
|---|---|---|
| 1000 | $A \to S$: $A, \{1000, B, K\}_{K_{AS}}$ | honest request |
| 1001 | $S \to B$: $\{1001, A, K\}_{K_{BS}}$ | $B$ accepts $K$ |
| 1021 | $E(B) \to S$: $B, \{1001, A, K\}_{K_{BS}}$ | $S$ reads: $B$ sends key $K$ for $A$, time 1001 is recent |
| 1021 | $S \to A$: $\{1021, B, K\}_{K_{AS}}$ | taken by $E$ |
| 1041 | $E(A) \to S$: $A, \{1021, B, K\}_{K_{AS}}$ | $S$ reads: $A$ sends key $K$ for $B$, time 1021 is recent |
| ... | the same, every 20 seconds | |
| 87401 | $E \to B$: $\{87401, A, K\}_{K_{BS}}$ | one day later, $B$ accepts the old $K$ again |

If $K$ has leaked in the meantime, $E$ can now talk to $B$ as $A$. The tests run this attack.

## Correctness

In an honest run within the time bounds, $S$ decrypts $A$'s request and finds a recent $T_A$ at line L2, and $B$ decrypts the forwarded message and finds a recent $T_S$ at line L3, so $B$ accepts the $K$ that $A$ made, with peer $A$. The proof is below.

## Complexity

Each party does one symmetric encryption or decryption, so the time is $\Theta(l)$ in the message length $l$. There are two messages, and the server keeps no state.

## Properties

- **Freshness of the forwarding**, not of the key: $B$ learns that $S$ handled $K$ recently.
- **Trust in $A$** to make good keys: $S$ only passes the key on.
- **No key confirmation** and no evidence for $A$ that $B$ got the key.
- **Replays within $\Delta$** are accepted unless $S$ and $B$ remember recent messages.

## Variants and improvements

- **Message labels.** Put a different label inside each encrypted message (or a different structure, as in the BAN analysis), so that a message 2 is never read as a message 1. The tests show that this stops the attack.
- **Replay caches** at $S$ and $B$ stop replays within the window.
- **The original timestamp.** Let $S$ forward $T_A$ in place of a new time, so that the age of the key is visible to $B$.
- **Denning-Sacco and Kerberos** let the server make the key; see the [Denning-Sacco protocol](/denning-sacco-protocol/) and [Kerberos](/kerberos/).

## When to use it

Do not use the protocol. Study it as an example of the danger of symmetric message formats and of timestamps that do not say what they are about. Use Kerberos in a server-based setting, or an [authenticated key exchange](/authenticated-key-exchange/) with public keys.

## Pitfalls

- **Messages with the same form.** At line L2, $S$ cannot tell a message 2 for $B$ from a message 1 from $B$, because both are $\{T, \text{name}, K\}$ under $B$'s key. This is what the attack uses.
- **A new timestamp on an old key.** Line L2 puts the server's current time on a key of unknown age, so line L3 checks the wrong thing.
- **Replays within the window.** Without a cache, $B$ accepts the same message 2 several times within $\Delta$ at line L3.
- **Clocks.** As with all timestamp protocols, an attacker who can change a clock can make old messages pass.

## Implementations

## History

Burrows, Abadi and Needham described the protocol in their 1989 report "A logic of authentication" and its 1990 journal version, as an example of a protocol that BAN logic handles with simple assumptions. Attacks were found by several authors in the 1990s; Anderson and Needham's 1995 paper "Programming Satan's computer" describes the attack that bounces the server's message back to it, and Clark and Jacob's 1997 survey lists it with the replay within the window.

## References
