---
tag: 67D8KM
kind: problem
slug: group-key-agreement-problem
name: Group key agreement problem
aliases:
- conference key agreement
- group key exchange
area: cryptography/key-exchange
level: advanced
summary: A group of n parties with no shared secret agree on one key to which all contribute, and keep it secret from outsiders and from members who leave or have not joined yet.
prereqs: [key-agreement-problem, diffie-hellman]
see_also: [group-diffie-hellman, ingemarsson-tang-wong, burmester-desmedt, tree-based-group-diffie-hellman, broadcast-encryption, key-distribution-problem, authenticated-key-exchange, secure-messaging]
sources:
  - paper: "Ingemar Ingemarsson, Donald T. Tang and Chak-Kuen Wong, A conference key distribution system, IEEE Transactions on Information Theory 28(5), 1982"
    locator: the first group protocol, a ring in which each member raises the value from its neighbor, n - 1 rounds
  - paper: "Mike Burmester and Yvo Desmedt, A secure and efficient conference key distribution system, EUROCRYPT 1994, LNCS 950"
    locator: the two-round protocol with key g^(x1 x2 + x2 x3 + ... + xn x1)
  - paper: doi:10.1145/238168.238182
    title: Michael Steiner, Gene Tsudik and Michael Waidner, Diffie-Hellman key distribution extended to group communication, ACM CCS 1996
    locator: the protocols GDH.1, GDH.2 and GDH.3, their costs, and the definition of the group Diffie-Hellman decision problem
  - paper: "Yongdae Kim, Adrian Perrig and Gene Tsudik, Tree-based group key agreement, ACM Transactions on Information and System Security 7(1), 2004"
    locator: TGDH, membership events (join, leave, merge, partition) with costs O(log n), and the comparison with earlier protocols
  - paper: "Emmanuel Bresson, Olivier Chevassut, David Pointcheval and Jean-Jacques Quisquater, Provably authenticated group Diffie-Hellman key exchange, ACM CCS 2001"
    locator: the first formal security model for authenticated group key exchange and a proof for an authenticated form of GDH.2
  - paper: "Jonathan Katz and Moti Yung, Scalable protocols for authenticated group key exchange, CRYPTO 2003, LNCS 2729"
    locator: the compiler that turns an unauthenticated group protocol into an authenticated one with one more round, and the proof for Burmester-Desmedt in the standard model
  - paper: "Klaus Becker and Uta Wille, Communication complexity of group key distribution, ACM CCS 1998"
    locator: lower bounds on rounds and messages for contributory group key distribution, and the hypercube and octopus protocols
  - url: "https://www.rfc-editor.org/rfc/rfc9420"
    title: Richard Barnes, Benjamin Beurdouche, Raphael Robert, Jon Millican, Emad Omara and Katriel Cohn-Gordon, RFC 9420, The Messaging Layer Security (MLS) Protocol, July 2023
    locator: Section 7 (ratchet tree and TreeKEM), Section 12 (proposals and commits for add, remove and update), Section 16 (security considerations, forward secrecy and post-compromise security)
---

The group key agreement problem asks $n$ parties to end with one common secret key after they exchange messages over a public network, where each member contributes to the key and no single member can choose it. It extends two-party [key agreement](/key-agreement-problem/) to a group, for example a conference call or a group chat. The group can change: when a member joins, it must not learn old keys, and when a member leaves, it must not learn new ones. The first solution was the ring protocol of [Ingemarsson, Tang and Wong](/ingemarsson-tang-wong/) (1982), and the classic ones are based on [Diffie-Hellman](/diffie-hellman/).

**Notation.** $M_1, \ldots, M_n$ are the members, indices taken modulo $n$. Member $M_i$ picks a secret exponent $x_i \in [1, q)$. $G = \langle g \rangle$ is a group of prime order $q$. $K$ is the group key. A round is a step in which every member may send one message at the same time; messages may be point to point or broadcast. Costs are counted in rounds, messages and modular exponentiations ("exps").

## In plain words

Several people want one shared secret, but every message they send can be read by a spy. Two people can do this with Diffie-Hellman. With a group, the question is how to make one key that all members share and that depends on a secret of each member.

There are more goals. No single member should choose the key alone, because a member with a broken random generator could make it weak. When someone leaves the group, it must not be able to read later messages. When someone joins, it must not be able to read earlier messages.

The cost matters too. Some solutions need many rounds of messages, some need many calculations per member, and some need a lot of work each time the group changes.

## Definition

**Syntax.** A group key agreement protocol is a set of efficient probabilistic interactive algorithms, one for each member. On input $1^\lambda$ and the list of members, each member $M_i$ outputs a key $K_i$.

**Correctness.** In an honest run, $K_1 = K_2 = \cdots = K_n$ with probability $1 - \mathrm{negl}(\lambda)$.

**Contributory.** The key is a function of a fresh random input of each member, and no member, or proper subset of members, can force it to a value of its choice. A protocol in which one member picks $K$ and sends it to the others is group key transport, not group key agreement.

**Security against a passive adversary.** Given the transcript, an efficient adversary cannot tell $K$ from a random element of the key space with more than negligible advantage. For the Diffie-Hellman protocols this reduces to a group form of the decisional Diffie-Hellman assumption: the values $g^{\prod_{i \in S} x_i}$ for proper subsets $S$ of $\{1, \ldots, n\}$ do not help to tell $g^{x_1 \cdots x_n}$ from random.

**Security against an active adversary.** The models of Bresson, Chevassut, Pointcheval and Quisquater (2001) and of Katz and Yung (2003) give the adversary oracles that send messages to instances, reveal keys, corrupt long-term keys and test a fresh key, as in [authenticated key exchange](/authenticated-key-exchange/). Forward secrecy asks that a later corruption of long-term keys does not reveal earlier session keys.

**Dynamic groups.** For a group that changes, the protocol also has join and leave operations. Backward secrecy: a member who joins cannot compute earlier group keys. Forward secrecy (in the membership sense): a member who leaves cannot compute later group keys. Key independence asks both: any set of keys gives no information about the others.

## Variants

- **Static or dynamic groups.** A static protocol runs once for a fixed set of members. A dynamic one updates the key on join, leave, merge and partition without a full rerun.
- **Authenticated or unauthenticated.** The classic protocols resist only a passive attacker; the Katz-Yung compiler adds a signature to each message, with fresh nonces, and gives an authenticated protocol at the cost of one more round.
- **Centralized key distribution.** A trusted group controller picks and sends keys, for example with a logical key hierarchy or [broadcast encryption](/broadcast-encryption/). This is not contributory, but a member change costs only $O(\log n)$ encryptions.
- **Asynchronous group messaging.** Members are not online at the same time, as in a group chat. Messaging Layer Security (MLS, RFC 9420) uses a ratchet tree in which each update replaces a path of keys, which gives forward secrecy and post-compromise security in groups of thousands.
- **Password-based group key exchange.** The members share only a password; see [password-authenticated key exchange](/password-authenticated-key-exchange/).

## Examples

**Four members with the Burmester-Desmedt protocol.** With secrets $x_1, \ldots, x_4$, round 1 broadcasts $z_i = g^{x_i}$, round 2 broadcasts $X_i = (z_{i+1}/z_{i-1})^{x_i}$, and each member computes $K = g^{x_1 x_2 + x_2 x_3 + x_3 x_4 + x_4 x_1}$. Every member does 3 exps whatever $n$ is; see [Burmester-Desmedt](/burmester-desmedt/).

**Measured costs.** The code on this page runs four protocols on the same toy group and counts the costs. For $n$ members:

| Protocol | Rounds | Messages | Exps in total | Exps per member | Contributory |
|---|---|---|---|---|---|
| leader sends the key | 2 | $n + 1$ | $3n - 2$ | $n$ for the leader, 2 for others | no |
| [ITW ring](/ingemarsson-tang-wong/) | $n - 1$ | $n(n - 1)$ | $n^2$ | $n$ | yes |
| [GDH.2](/group-diffie-hellman/) | $n$ | $n$ | $(n^2 + 3n)/2 - 1$ | $i + 1$ for $M_i$ with $i < n$, and $n$ for $M_n$ | yes |
| [Burmester-Desmedt](/burmester-desmedt/) | 2 | $2n$ | $3n$ | 3 | yes |

For $n = 10$: the leader protocol uses 28 exps, ITW 100, GDH.2 64 and Burmester-Desmedt 30. Burmester-Desmedt also does $O(n)$ multiplications per member to compute the key, which the meter does not count. The tests check these formulas for $n$ in $\{3, 4, 6, 10\}$, check that all four protocols agree, check that the leader can force any key, and check that a change of any one secret changes the key in the three contributory protocols.

**Non-example.** In the leader protocol, member 1 can set $K = 42$, and the tests confirm that all members then hold 42. The protocol is a correct key transport, but it is not contributory.

The code is for study only, it is not constant time, and it uses a toy 128-bit group with local simulated parties.

## Known algorithms

- [Ingemarsson-Tang-Wong](/ingemarsson-tang-wong/) (1982): a ring, $n - 1$ rounds, key $g^{x_1 \cdots x_n}$.
- [Burmester-Desmedt](/burmester-desmedt/) (1994): 2 rounds, 3 exps per member, $O(n)$ broadcast messages.
- [Group Diffie-Hellman](/group-diffie-hellman/) GDH.1, GDH.2 and GDH.3 (Steiner, Tsudik and Waidner, 1996), and the Cliques toolkit for dynamic groups.
- Hypercube and octopus protocols (Becker and Wille, 1998): pairwise Diffie-Hellman steps in $\log_2 n$ rounds.
- [Tree-based group Diffie-Hellman](/tree-based-group-diffie-hellman/) (Kim, Perrig and Tsudik, 2000): a binary tree of Diffie-Hellman keys, joins and leaves in $O(\log n)$ exps.
- The Katz-Yung compiler (2003): authenticated Burmester-Desmedt with a proof in the standard model.
- TreeKEM in MLS (2023): a ratchet tree with public-key encryption in place of Diffie-Hellman, for asynchronous groups.

## Bounds

- **Rounds.** If each member must receive information that depends on every other secret, and messages carry pairwise combinations, the key needs $\Omega(\log n)$ rounds with two-party steps; with broadcast, Burmester-Desmedt reaches a constant number of rounds (2).
- **Messages and exps.** Becker and Wille (1998) gave lower bounds on the number of messages and rounds for contributory protocols, met by the hypercube and octopus protocols.
- **Membership changes.** A static protocol pays its full cost on each change. Tree-based protocols pay $O(\log n)$ exps for the members on one path; a centralized controller pays $O(\log n)$ encryptions for a logical key hierarchy, which is optimal for that model.
- **Security.** Passive security of the product-key protocols reduces to the group decisional Diffie-Hellman assumption, which Steiner, Tsudik and Waidner showed is implied by the two-party decisional Diffie-Hellman assumption, with a loss that grows with $n$.

## Reductions

- **To two-party key agreement.** For $n = 2$, ITW, GDH.2 and Burmester-Desmedt all become [Diffie-Hellman](/diffie-hellman/): the key is $g^{x_1 x_2}$ (for Burmester-Desmedt, $g^{2 x_1 x_2}$).
- **From two-party key agreement.** A tree of two-party Diffie-Hellman exchanges, in which the key of each subtree becomes the secret exponent of the next level, gives group key agreement in $\lceil \log_2 n \rceil$ levels; this is the idea of TGDH and of the hypercube protocol.
- **From passive to active security.** The Katz-Yung compiler turns any passively secure group protocol into an authenticated one, given a signature scheme and nonces.

## Applications

- Secure group communication in the research toolkits Cliques and Secure Spread, which used GDH and TGDH.
- Ad hoc and sensor networks, in which no member can act as a trusted controller.
- Group messaging: MLS (RFC 9420) for large asynchronous groups. Older designs built a group from pairwise channels, which costs $O(n)$ encryptions for each message.

## References

Ingemarsson, Tang and Wong (1982) and Burmester and Desmedt (1994) give the first protocols. Steiner, Tsudik and Waidner (1996) give GDH and its costs, and Kim, Perrig and Tsudik (2000, 2004) give TGDH. Bresson, Chevassut, Pointcheval and Quisquater (2001) and Katz and Yung (2003) give the security models. RFC 9420 is the current standard for group messaging.
