---
tag: 00SN4E
kind: algorithm
slug: yahalom-protocol
name: Yahalom protocol
area: cryptography/key-exchange
level: advanced
summary: A four-message key distribution protocol in which B's nonce travels only under encryption and returns to B under the new key. A standard case study for BAN logic and Paulson's inductive method.
solves: [key-distribution-problem]
model: word-ram
complexity:
  vars: {l: the total length of the messages in bits}
  time: {worst: Θ(l), average: Θ(l), best: Θ(l)}
  space: {extra: Θ(l)}
properties: {deterministic: false, randomized: true}
history:
  year: 1989
  people: [Raphael Yahalom, Michael Burrows, Martín Abadi, Roger Needham, Lawrence C. Paulson]
  note: The protocol is due to Yahalom and was first published in the 1989 BAN logic report of Burrows, Abadi and Needham; Paulson proved its secrecy properties in 2001.
prereqs: [needham-schroeder-protocol]
see_also: [key-distribution-center, otway-rees-protocol, denning-sacco-protocol, wide-mouthed-frog-protocol, kerberos, entity-authentication, session-key, key-distribution-problem]
sources:
  - paper: "Michael Burrows, Martín Abadi and Roger Needham, A logic of authentication, DEC SRC Research Report 39, February 1989; also ACM Transactions on Computer Systems 8(1), 1990, pages 18 to 36"
    locator: the protocol, attributed to Yahalom, its BAN analysis, and a modified version (sections to check)
  - paper: "Lawrence C. Paulson, Relations between secrets: two formal analyses of the Yahalom protocol, Journal of Computer Security 9(3), 2001, pages 197 to 216"
    locator: the proof in Isabelle by the inductive method that the session key and B's nonce stay secret, and the dependence of the nonce's secrecy on the key
  - paper: "John Clark and Jeremy Jacob, A survey of authentication protocol literature, version 1.0, 1997"
    locator: Section 6.3.6 (the protocol) and the following sections on its variants
---

The Yahalom protocol is a key distribution protocol with a trusted server $S$ that shares a long-term key with each user. It has four messages: $A$ sends a nonce to $B$; $B$ sends both nonces to $S$ under its own key; $S$ sends $A$ the new session key $K$ with both nonces, plus a ticket for $B$; and $A$ forwards the ticket together with $B$'s nonce encrypted under $K$. The special feature is that $B$'s nonce $N_B$ never travels in clear, and comes back to $B$ only under $K$. This gives $B$ both freshness and evidence that $A$ holds $K$, but only as long as $N_B$ stays secret. The protocol was first published in the 1989 BAN logic paper of Burrows, Abadi and Needham, and Paulson's 2001 analysis of the "relations between secrets" in it is a classic of formal verification.

**Notation.** $\{m\}_K$ is $m$ encrypted and integrity-protected under the symmetric key $K$. $K_{AS}$ and $K_{BS}$ are long-term keys shared with $S$. $N_A$ and $N_B$ are nonces, and $K$ is the new session key.

## In plain words

Alice wants a key for talking to Bob, and each of them shares a secret key with a trusted server. Alice sends Bob her name and a random number. Bob adds his own random number, locks both numbers for the server, and sends them on.

The server makes a key and sends Alice one locked box with the key and both random numbers, and a second box, a ticket for Bob with the key and Alice's name. Alice checks her number, then gives Bob the ticket and Bob's number locked with the new key. Only someone with the new key could do that, and only someone who saw the server's answer knows Bob's number, so Bob knows the key is new and that Alice has it.

## The problem

The [key distribution problem](/key-distribution-problem/) with a [key distribution center](/key-distribution-center/): fresh session keys for pairs of users without clocks, with freshness and key confirmation for $B$.

## The algorithm

Each line names the party that acts.

```pseudo id=main
YAHALOM(A, B, S)
L1  A: N_A ← fresh; A → B: A, N_A
L2  B: N_B ← fresh; B → S: B, {A, N_A, N_B}_{K_BS}
L3  S: decrypt; K ← fresh key; S → A: {B, K, N_A, N_B}_{K_AS}, {A, K}_{K_BS}
L4  A: decrypt the first part; if B or N_A is wrong then fail; accept K with B
        A → B: {A, K}_{K_BS}, {N_B}_K
L5  B: decrypt the ticket, get A and K; if {N_B}_K does not give its own N_B then fail; accept K with A
```

At line L4, $A$ sees its own nonce with the name $B$ under $K_{AS}$, so $K$ is fresh and meant for $B$. At line L5, the ticket tells $B$ that $S$ made $K$ for $A$, but the ticket carries nothing fresh. Freshness for $B$ comes from $N_B$: $B$ sent it only under $K_{BS}$, and $S$ passed it on only under $K_{AS}$, so a party that returns it under $K$ took part in this run and knows $K$.

**About the code.** The Python code implements the protocol and tests it against a replay of an old ticket with a known old key, which fails here because the attacker does not know the new $N_B$. The encryption is a toy encrypt-then-MAC. It is for study only. It is not constant time, and this protocol must not protect real data. Use Kerberos (MIT Kerberos or Heimdal) or TLS 1.3.

## Example

The replay of an old ticket. The attacker $E$ recorded an old ticket $\{A, K'\}_{K_{BS}}$ and later learned $K'$. Compare with [Needham-Schroeder](/needham-schroeder-protocol/), where the same knowledge is enough.

| step | Needham-Schroeder | Yahalom |
|---|---|---|
| attacker sends | the old ticket $\{K', A\}_{K_{BS}}$ | $A, N$ as message 1, then the old ticket $\{A, K'\}_{K_{BS}}$ |
| $B$ makes | a challenge $\{N_B\}_{K'}$, sent to the attacker | $N_B$, sent only inside $\{A, N, N_B\}_{K_{BS}}$ |
| attacker must give | $\{N_B - 1\}_{K'}$: easy, it decrypts the challenge | $\{N_B\}_{K'}$: it does not know $N_B$ |
| result | $B$ accepts $K'$ with $A$ | $B$ rejects |

## Correctness

In an honest run, $A$ finds $B$ and $N_A$ under $K_{AS}$ at line L4, and $B$ finds the ticket for $A$ and its own $N_B$ under the key in the ticket at line L5, so both accept the same $K$. The proof is below.

The security argument is subtle. Paulson proved in Isabelle, with his inductive method, that $K$ stays secret and that $N_B$ stays secret as long as $K$ does. His title, "relations between secrets", refers to this dependence: the guarantee for $B$ rests on the secrecy of $N_B$, which rests on the secrecy of a key that $B$ has not yet checked.

## Complexity

Each party does a constant number of symmetric encryptions or decryptions, so the time is $\Theta(l)$ in the message length $l$. There are four messages, and the server keeps no state between runs.

## Properties

- **Freshness for both parties** from their own nonces, without clocks.
- **Key confirmation for $B$**, from $\{N_B\}_K$ at line L5.
- **No key confirmation for $A$**: $A$ accepts at line L4 before $B$ has the key.
- **Secrecy of $N_B$** depends on the secrecy of $K$; if $K$ leaks, $\{N_B\}_K$ gives $N_B$ away. The tests show this.

## Variants and improvements

- **The BAN modified version.** Burrows, Abadi and Needham proposed a changed protocol with $N_B$ in clear and inside the ticket; later papers showed weaknesses in it (details to check).
- **Otway-Rees and Needham-Schroeder** are the related designs; see [Otway-Rees](/otway-rees-protocol/) and [Needham-Schroeder](/needham-schroeder-protocol/).
- **Kerberos** uses timestamps in place of $B$'s nonce; see [Kerberos](/kerberos/).

## When to use it

Do not use the protocol in new systems. Study it as an example of a protocol whose security rests on secret nonces, and as a test case for formal methods. Use Kerberos in a server-based setting, or an [authenticated key exchange](/authenticated-key-exchange/) with public keys.

## Pitfalls

- **Sending $N_B$ in clear at line L2.** Then an attacker with an old ticket and its key can answer $B$'s check at line L5, as in the Denning-Sacco attack on Needham-Schroeder. $N_B$ must stay secret.
- **Reusing nonces as keys or as public values.** $N_B$ protects $B$ only while it is secret; using it elsewhere, or after $K$ leaks, breaks the guarantee.
- **No confirmation for $A$.** $A$ accepts at line L4 even if message 4 never arrives. Add a confirmation from $B$ if $A$ needs it.
- **Unauthenticated encryption.** With a malleable cipher, parts of the ciphertexts at lines L3 and L4 can be changed. Use authenticated encryption.

## Implementations

## History

Raphael Yahalom designed the protocol, and Burrows, Abadi and Needham published it in their 1989 report "A logic of authentication" (journal version in ACM Transactions on Computer Systems, 1990), where they analysed it with BAN logic and suggested a modified version. The protocol became a standard example for protocol logics and model checkers. Paulson's 2001 paper in the Journal of Computer Security gave machine-checked proofs of its secrecy properties and made explicit the relation between the secrecy of the key and of $B$'s nonce.

## References
