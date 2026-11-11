---
tag: 1FPAEV
kind: algorithm
slug: dining-cryptographers
name: Dining cryptographers protocol
aliases:
- DC-net
- dining cryptographers problem
- dining cryptographers network
area: cryptography/protocols
level: advanced
summary: Anonymous broadcast in which neighbors in a key graph share random keys and everyone announces the XOR of their keys, the sender adding its message; the XOR of all announcements is the message.
solves: [anonymous-communication]
model: word-ram
complexity:
  vars: {n: the number of parties, E: the number of edges of the key graph, l: the length of a message in machine words}
  time: {worst: O((n + E) l), average: O((n + E) l), best: O((n + E) l)}
  space: {extra: O(E l)}
properties: {deterministic: false, randomized: true}
history:
  year: 1988
  people: [David Chaum]
  note: Chaum published the protocol in the first issue of the Journal of Cryptology in 1988; Waidner and Pfitzmann added traps against jamming in 1989.
prereqs: [one-time-pad]
see_also: [anonymous-communication, mix-network, perfect-secrecy, secret-sharing, secure-multiparty-computation, breadth-first-search, ring-signature, threshold-cryptography]
sources:
  - paper: doi:10.1007/BF00206326
    title: David Chaum, The dining cryptographers problem, unconditional sender and recipient untraceability, Journal of Cryptology 1(1), 1988, pages 65 to 75
    locator: the dinner story with three cryptographers, the generalization to a key graph, the theorem that the sender is hidden among the parties of a connected honest component, collisions, reservation and the use of a pseudorandom generator for long keys
  - paper: "Michael Waidner and Birgit Pfitzmann, The dining cryptographers in the disco, unconditional sender and recipient untraceability with computationally secure serviceability, Eurocrypt 1989, LNCS 434, page 690"
    locator: traps that let honest parties find a jammer without losing anonymity in the rounds that are not traps
  - paper: doi:10.1145/1866307.1866346
    title: Henry Corrigan-Gibbs and Bryan Ford, Dissent, accountable anonymous group messaging, ACM CCS 2010, pages 340 to 350
    locator: a verifiable shuffle that assigns each member a slot, followed by DC-net style bulk transfer, with a blame phase that names a member who disrupts
  - paper: "Sharad Goel, Mark Robson, Milo Polte and Emin Gün Sirer, Herbivore, a scalable and efficient protocol for anonymous communication, Cornell University technical report, 2003"
    locator: small DC-net cliques inside a large overlay, so that the cost depends on the clique size, not on the number of users
  - paper: "Philippe Golle and Ari Juels, Dining cryptographers revisited, Eurocrypt 2004, LNCS 3027, pages 456 to 473"
    locator: non-interactive DC-nets in which a jammer is detected with high probability, based on bilinear maps
---

The dining cryptographers protocol lets one member of a group broadcast a message so that every member learns the message but nobody, not even a coalition of the other members with unlimited computing power, learns who sent it. Pairs of members share secret random keys, and each member announces the XOR of its keys, the sender also XORing in the message. Each key is in exactly two announcements, so the XOR of all announcements is the message, and the keys hide whose announcement carried it. David Chaum published the protocol in 1988; a network that runs it is called a DC-net.

**Notation.** There are $n$ parties, the vertices of a key graph $\Gamma = (V, E)$. For each edge $e = \{i, j\}$, parties $i$ and $j$ share a key $k_e$ of $\ell$ bits. $\oplus$ is the bitwise XOR. Party $i$ announces $A_i$, and $M = \bigoplus_i A_i$ is the output of the round. A coalition $C$ is a set of dishonest parties, and $H = V \setminus C$ the honest ones; $\Gamma_H$ is the subgraph of edges between honest parties.

## In plain words

Three cryptographers finish dinner and learn that the bill is paid. Either one of them paid, or their employer did. They want to know which, without finding out who among them paid.

Each pair flips a coin behind a menu, so that each cryptographer sees the two coins she shares with her neighbors. Each then says whether her two coins are the same or different, but the one who paid says the opposite. If the number of "different" answers is odd, one of them paid; if it is even, the employer did.

Each coin is counted by two people, so the coins cancel, and only the lie of the payer is left. To a cryptographer who did not pay, the other two answers look like fair coin flips, whichever of them paid.

## The problem

A group of $n$ parties wants an anonymous broadcast channel: in each round, a party may publish a message, and everyone learns the message, but nobody can tell which honest party sent it, beyond the fact that it came from the group. The anonymity should hold against any coalition $C$ of other parties, without a trusted server and without a computational assumption. This is sender anonymity, a part of [anonymous communication](/anonymous-communication/). Receiver anonymity follows, because every party receives every message.

## The algorithm

```pseudo id=main
DC-ROUND(Γ = (V, E), sender s, message m of ℓ bits)
L1  for each edge e = {i, j} of Γ: i and j share a fresh uniform key k_e of ℓ bits
L2  each party i: A_i ← XOR of k_e over the edges e at i
L3  the sender s: A_s ← A_s ⊕ m
L4  each party i broadcasts A_i
L5  each party computes M ← A_1 ⊕ A_2 ⊕ … ⊕ A_n
L6  if M = 0, nobody sent; else M is the message, or the XOR of several messages if senders collided
```

**Why the message comes out.** Each key $k_e$ with $e = \{i, j\}$ is XORed into $A_i$ and into $A_j$ and into no other announcement (line L2), and $k_e \oplus k_e = 0$. So all keys cancel in line L5, and only $m$ is left.

**Why the sender is hidden.** Look at the announcements from the view of a coalition $C$, which knows the keys on its own edges. Each honest announcement still includes the keys on edges between honest parties. If the honest subgraph $\Gamma_H$ is connected, these keys make the vector of honest announcements uniform among all vectors with the right XOR, and that set is the same whichever honest party sent. This is Chaum's theorem: the sender is hidden among all honest parties of its connected component of $\Gamma_H$, against any adversary, as with the [one-time pad](/one-time-pad/). If $\Gamma_H$ falls apart, the coalition learns the component of the sender. The complete graph is the safest key graph, because the honest parties stay connected whatever $C$ is; a ring is cheap but is cut by two dishonest parties.

**Keys.** The keys must be fresh in each round, so a DC-net with perfect anonymity needs a lot of shared randomness: $\ell$ bits per edge per round. In practice, each pair shares a short secret, for example from a Diffie-Hellman exchange, and expands it with a pseudorandom generator; the anonymity then holds only against a bounded adversary, as Chaum already noted.

**Collisions and reservation.** If two parties send in the same round, $M$ is the XOR of their messages and both are lost. Chaum proposed a reservation phase: parties first run a DC-net round on a vector of slots, each setting a bit in a random slot, and then send in the slots that they reserved alone. Two parties that pick the same slot cancel each other in that bit and both try again.

**Jamming.** A dishonest party can XOR random bits into its announcement. The round then gives garbage, and since the jammer's announcement looks as random as an honest one, nobody can tell from the round who did it. One jammer can stop the whole group. Waidner and Pfitzmann (Eurocrypt 1989) added traps, rounds that the parties later open to find a cheater, and later systems add accountability.

**Herbivore and Dissent.** Herbivore (Goel, Robson, Polte and Sirer, 2003) made DC-nets scale by splitting users into small cliques, in which each user runs a DC-net with a few dozen others, inside a large overlay network. The cost depends on the size of the clique, not on the number of users, and so does the anonymity set. Dissent (Corrigan-Gibbs and Ford, CCS 2010) added accountability: members first run a verifiable shuffle, as in a [mix network](/mix-network/), to give each member a slot with a pseudonymous key, without telling who owns which slot. Then they send in their slots with DC-net rounds. If a member disrupts a slot, its owner can start a blame phase that names the disruptor without exposing honest senders. Later versions of Dissent use a small set of servers, so each client shares keys only with the servers, and scale to thousands of clients.

**About the code.** The Python code is for study only. It is not constant time and has no defense against jamming; for real anonymous group messaging, use a maintained system with accountability, such as one built on Dissent. It runs one DC-net round on any key graph, with fresh keys from the system random source, and it can enumerate every value of every key for small graphs with 1-bit messages, so the tests check anonymity exactly rather than by sampling. DC-nets have no official test vectors.

## Example

Alice, Bob and Carol sit at a triangle. The coins are $k_{AB} = 1$, $k_{BC} = 0$ and $k_{AC} = 1$, and Bob paid, so he sends $m = 1$.

| Step | Line | Alice | Bob | Carol |
|---|---|---|---|---|
| 1 | L1 | sees $k_{AB} = 1$, $k_{AC} = 1$ | sees $k_{AB} = 1$, $k_{BC} = 0$ | sees $k_{BC} = 0$, $k_{AC} = 1$ |
| 2 | L2 | $1 \oplus 1 = 0$ | $1 \oplus 0 = 1$ | $0 \oplus 1 = 1$ |
| 3 | L3 | | $1 \oplus m = 0$ | |
| 4 | L4 | announces $0$ | announces $0$ | announces $1$ |
| 5 | L5 | $M = 0 \oplus 0 \oplus 1 = 1$ | $M = 1$ | $M = 1$ |

So one of them paid. Alice sees her two coins and the announcements $0$ from Bob and $1$ from Carol. Had Carol paid instead, with $k_{BC} = 1$, Bob would announce $1 \oplus 1 = 0$ and Carol $1 \oplus 1 \oplus 1 = 1$: the same view. For each value of $k_{BC}$ that makes one story fit, there is one value that makes the other fit, so Alice cannot tell.

The tests of the code check these claims exhaustively. On the triangle, the distribution of Alice's views over all eight coin values is the same whether Bob or Carol paid. On a ring of six parties with two dishonest parties at opposite positions, the honest parties fall into two parts, and the coalition learns for sure which part holds the sender, but not who in that part; with one more key across the ring, the honest parties are connected and all four look the same. On a path with a dishonest party in the middle, the sender is exposed. A party that XORs junk into its announcement turns the output into garbage, and the sender's view is the same whichever of the other parties did it.

## Correctness

By the cancellation argument above, the output of line L5 is the XOR of all messages sent in the round, so one sender gives $M = m$ and no sender gives $M = 0$. For anonymity, the keys on honest edges make the map from these keys to the vector of honest key sums a linear map whose image is the set of vectors with XOR zero, when $\Gamma_H$ is connected; a spanning tree shows that every such vector is reached. So the honest announcements are uniform on a set that depends on the messages only through their XOR, and the coalition's view does not depend on which honest party sent. The proof page gives the full proofs, the converse for a disconnected $\Gamma_H$, and the statement that a jammer is not detected.

## Complexity

In each round, party $i$ XORs $\deg(i)$ keys of $\ell$ bits, so all parties together do $O(E \ell)$ bit operations, or $O(E l)$ word operations, plus $O(n l)$ to XOR the $n$ announcements. Each party broadcasts $\ell$ bits, so the round sends $n \ell$ bits, or $n^2 \ell$ bits if each announcement is sent to each party without a broadcast medium. With a complete key graph, $E = n(n-1)/2$, so each round costs $\Theta(n^2 \ell)$ in key material, and every party pays for every message, even when it has nothing to send. Each party stores its keys, $O(E l)$ words in total. This cost, linear in the group size for each party and each message bit, is what limits DC-nets to small groups or to designs with servers.

## Properties

- **Information-theoretic sender anonymity.** With fresh uniform keys, the sender is hidden among the honest parties of its component of $\Gamma_H$, against any adversary.
- **Receiver anonymity.** Everyone receives every message, so a receiver who decrypts a message addressed to it is not singled out.
- **Unobservability.** Everyone sends in every round, so an observer cannot even tell whether a party sent.
- **No trusted party.** No server needs to be honest; the anonymity depends only on the key graph.
- **Fragile.** One party can jam every round without being detected by the basic protocol, and collisions waste rounds.

## Variants and improvements

- **Computational keys.** Short shared seeds expanded with a pseudorandom generator, which trade perfect anonymity for practical key sizes.
- **Key graphs.** A complete graph resists any coalition that leaves at least two honest parties; sparser graphs cost less but need assumptions about which parties can collude.
- **Superposed sending.** Chaum's DC-nets work over any abelian group, not only bits; sending in a larger group, such as integers modulo a prime, lets the output count how many parties sent and helps resolve collisions.
- **Traps and accountability.** Waidner and Pfitzmann's traps (1989), Golle and Juels's DC-nets with pairings that detect jammers (Eurocrypt 2004), and Dissent's shuffle and blame phases.
- **Servers.** Dissent in its later form, Riposte (Corrigan-Gibbs, Boneh and Mazières, IEEE S&P 2015) and similar systems let clients share keys only with a few servers, at least one of which must be honest, which cuts the cost for clients.
- **Herbivore.** Small DC-net cliques in a large network.

## When to use it

Use a DC-net when a small group needs anonymity for a broadcast that holds even against an adversary with unlimited computing power and against any coalition of members, and when every member is online in every round, for example for a whistleblowing channel among a fixed set of peers. When the group is large, use a design with servers, such as Dissent or Riposte, or a [mix network](/mix-network/), which costs less per message. For anonymity on the web, use onion routing.

## Pitfalls

- **Reused keys.** A key used in two rounds is no longer a one-time pad: the XOR of two announcements of one party cancels the key and exposes the XOR of the messages it sent. Use fresh keys, or a pseudorandom generator with a new counter in each round.
- **Weak key graphs.** A sparse key graph is cut by a few dishonest parties, and then the coalition learns which side holds the sender. Check that the honest parties stay connected for the coalitions you must resist, as breadth-first search does in the code.
- **Jamming.** Without traps or a blame phase, one dishonest member can stop all communication and stay hidden.
- **Timing and participation.** If parties announce at different times or skip rounds, the pattern of who takes part reveals information; all parties must announce in every round.
- **Collisions.** Without a reservation phase, two senders destroy each other's messages, and repeated attempts can reveal who keeps trying.

## Implementations

## History

David Chaum published the dining cryptographers protocol, with the theorem for general key graphs, in the first issue of the Journal of Cryptology in 1988. Waidner and Pfitzmann showed in 1989 how to find jammers with traps. Herbivore (2003) made the protocol scale with small cliques, and Golle and Juels (2004) gave DC-nets that detect cheaters non-interactively. Dissent (2010) combined a verifiable shuffle with DC-net rounds to give accountable anonymity, and later work, including Riposte (2015), moved the key sharing to a few servers to support large groups.

## References
