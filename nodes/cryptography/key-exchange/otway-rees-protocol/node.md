---
tag: GDNTC9
kind: algorithm
slug: otway-rees-protocol
name: Otway-Rees protocol
area: cryptography/key-exchange
level: advanced
summary: A four-message key distribution protocol in which B forwards A's request to the server with its own, so both nonces reach the server. Known for a type flaw attack.
solves: [key-distribution-problem]
model: word-ram
complexity:
  vars: {l: the total length of the messages in bits}
  time: {worst: Θ(l), average: Θ(l), best: Θ(l)}
  space: {extra: Θ(l)}
properties: {deterministic: false, randomized: true}
history:
  year: 1987
  people: [Dave Otway, Owen Rees]
  note: Otway and Rees published the protocol in 1987 as an efficient and timely alternative to Needham-Schroeder; the type flaw attack on it is a standard example in the literature.
prereqs: [needham-schroeder-protocol]
see_also: [key-distribution-center, yahalom-protocol, denning-sacco-protocol, wide-mouthed-frog-protocol, kerberos, entity-authentication, session-key, key-distribution-problem]
sources:
  - paper: "Dave Otway and Owen Rees, Efficient and timely mutual authentication, ACM SIGOPS Operating Systems Review 21(1), January 1987, pages 8 to 10"
    locator: the protocol
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Protocol 12.29 (Otway-Rees) and Section 12.9.1 (Attack 4, misplaced trust in the server)
  - paper: "John Clark and Jeremy Jacob, A survey of authentication protocol literature, version 1.0, 1997"
    locator: Section 6.3.3 (the protocol and the type flaw attack in which A takes M, A, B as the key)
  - paper: "Michael Burrows, Martín Abadi and Roger Needham, A logic of authentication, DEC SRC Research Report 39, February 1989"
    locator: the BAN analysis of the protocol (section to check)
---

The Otway-Rees protocol is a key distribution protocol with a trusted server $S$ that shares a long-term key with each user. It was published by Dave Otway and Owen Rees in 1987. Unlike [Needham-Schroeder](/needham-schroeder-protocol/), where $A$ asks the server alone, here $A$ sends its encrypted request to $B$, and $B$ adds its own encrypted request and passes both to $S$. So the server sees a nonce from each party, and each party gets a fresh session key from a reply that answers its own nonce, in four messages and without clocks. The protocol is best known for a type flaw: without type information in the plaintexts, an attacker can send $A$'s own request back to it, and $A$ takes public values as the key.

**Notation.** $\{m\}_K$ is $m$ encrypted and integrity-protected under the symmetric key $K$. $K_{AS}$ and $K_{BS}$ are long-term keys shared with $S$. $M$ is a run identifier, $N_A$ and $N_B$ are nonces, and $K$ is the new session key.

## In plain words

Alice wants a key for talking to Bob, and each of them shares a secret key with a trusted server. Alice writes a request with a random number and a run number, locks it for the server, and gives it to Bob. Bob adds his own locked request with his own random number and sends both to the server.

The server checks that both requests name the same run and the same two people. It makes a new key and returns two locked answers, one for each, each with the owner's random number and the key. Bob keeps his answer and passes Alice hers. Each checks that the random number is the one they chose.

## The problem

The [key distribution problem](/key-distribution-problem/) with a [key distribution center](/key-distribution-center/): fresh session keys for pairs of users, with freshness for both parties and no need for synchronized clocks.

## The algorithm

Each line names the party that acts.

```pseudo id=main
OTWAY-REES(A, B, S)
L1  A: M, N_A ← fresh; A → B: M, A, B, {N_A, M, A, B}_{K_AS}
L2  B: N_B ← fresh; B → S: M, A, B, {N_A, M, A, B}_{K_AS}, {N_B, M, A, B}_{K_BS}
L3  S: decrypt both; if M, A, B in either differ from the clear values then fail
        K ← fresh key; S → B: M, {N_A, K}_{K_AS}, {N_B, K}_{K_BS}
L4  B: if N_B is wrong then fail; accept K with A; B → A: M, {N_A, K}_{K_AS}
L5  A: if N_A is wrong then fail; accept K with B
```

At line L3, the server knows from the two encrypted parts that $A$ and $B$ both asked for a key for the same run $M$ with each other. At lines L4 and L5, each party sees its own nonce next to $K$, under the key it shares with $S$, so $K$ is fresh and made by $S$ for this run. Neither party learns at the end that the other holds $K$: there is no key confirmation.

**About the code.** The Python code implements the protocol in two forms. With `typed=False` the plaintexts are plain concatenations and a party takes "the bytes after the nonce" as the key; with `typed=True` each field has a type tag. The encryption is a toy encrypt-then-MAC. It is for study only. It is not constant time, and this protocol must not protect real data. Use Kerberos (MIT Kerberos or Heimdal) or TLS 1.3.

## Example

The type flaw attack. Run identifiers are 16 bytes, names 8 bytes and keys 32 bytes, so $M, A, B$ together have the length of a key. $E(B)$ means the attacker posing as $B$.

| step | message | what happens |
|---|---|---|
| 1 | $A \to E(B)$: $M, A, B, \{N_A, M, A, B\}_{K_{AS}}$ | $E$ stops the message |
| 4 | $E(B) \to A$: $M, \{N_A, M, A, B\}_{K_{AS}}$ | the encrypted part of message 1, sent back as message 4 |
| L5 | $A$ decrypts and reads $\{N_A, K\}$ with $K = M \mid A \mid B$ | $N_A$ is right, so $A$ accepts |
| result | $A$ believes it shares $K = M \mid A \mid B$ with $B$ | every part of $K$ was sent in clear |

## Correctness

In an honest run, the server finds the same $M$, $A$ and $B$ in both encrypted parts at line L3, $B$ finds $N_B$ in its part at line L4, and $A$ finds $N_A$ at line L5, so both accept the same $K$. The proof is below.

The protocol is secure only if the parties can tell apart the plaintexts of different messages. That condition is what the type flaw attack breaks.

## Complexity

Each party does a constant number of symmetric encryptions or decryptions, so the time is $\Theta(l)$ in the message length $l$. The protocol has four messages; the server keeps no state between runs.

## Properties

- **Freshness for both parties** from their own nonces, without clocks.
- **No key confirmation**: neither party knows at the end that the other has $K$.
- **The server checks agreement** on the run, $A$ and $B$ before it makes a key.
- **No forward secrecy**: an attacker who records a run and later learns $K_{AS}$ or $K_{BS}$ gets $K$.

## Variants and improvements

- **Typed or tagged messages.** Give each field a type tag, or each message a unique label, so that $\{N_A, M, A, B\}_{K_{AS}}$ can never be read as $\{N_A, K\}_{K_{AS}}$. The tests show that this stops the attack.
- **Names in the reply.** A common change puts the peer's name into the server's reply parts, for example $\{N_A, B, K\}_{K_{AS}}$, so that each party can check for whom the key was made.
- **Kerberos and Yahalom** are the related designs most used in teaching; see [Yahalom](/yahalom-protocol/).

## When to use it

Do not use the protocol in new systems. Study it as an example of a type flaw and of the role of explicit message formats. Use Kerberos in a server-based setting, or an [authenticated key exchange](/authenticated-key-exchange/) with public keys.

## Pitfalls

- **The type flaw at line L5.** If $A$ cannot tell a key from the triple $M, A, B$, it accepts its own request, reflected, as the server's reply. The tests run this attack. Tag every field, or give every message a unique label inside the encryption.
- **Misplaced trust in the server.** The Handbook of Applied Cryptography (Section 12.9.1) lists an attack on this protocol of the kind "misplaced trust in the server": the parties trust that the server checked more than it did. Make every check that the security argument needs explicit at line L3.
- **No confirmation.** $A$ may accept $K$ at line L5 even if $B$ never got a key, for example if the attacker blocks message 4 or answers it as in the attack. Add a confirmation step before relying on $K$.
- **Unauthenticated encryption.** With a malleable cipher, parts of the ciphertexts at lines L1 and L2 can be cut and joined. Use authenticated encryption.

## Implementations

## History

Otway and Rees published the protocol in ACM SIGOPS Operating Systems Review in January 1987. Burrows, Abadi and Needham analysed it with BAN logic in 1989. Several authors described attacks in the early 1990s; the best known is the type flaw attack in which $A$ accepts the public values $M, A, B$ as its key. Clark and Jacob's 1997 survey gives this attack without attribution, and its origin is not clear to this page. The protocol became a standard test case for tools that analyse protocols, such as the inductive method of Paulson and model checkers.

## References
