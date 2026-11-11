---
tag: XEFABJ
kind: problem
slug: byzantine-reliable-broadcast
name: Byzantine reliable broadcast
aliases:
- reliable broadcast with Byzantine faults
area: distributed/byzantine-agreement
level: core
summary: One sender's message must reach all honest processes the same, or reach none of them, despite Byzantine faults and an asynchronous network.
prereqs: [asynchronous-model, byzantine-failure-model]
see_also: [bracha-reliable-broadcast, byzantine-broadcast, bracha-asynchronous-agreement, honeybadger-bft, total-order-broadcast, causal-broadcast, fifo-broadcast, digital-signature]
sources:
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luis Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Section 3.10 (Byzantine consistent broadcast, with the authenticated and the signed echo broadcast algorithms) and Section 3.11 (Byzantine reliable broadcast, with the authenticated double-echo broadcast algorithm)
  - paper: doi:10.1016/0890-5401(87)90054-X
    title: Gabriel Bracha, Asynchronous Byzantine agreement protocols, Information and Computation 75(2), 1987
    locator: the broadcast primitive and its properties
  - paper: doi:10.1007/BF01667080
    title: T. K. Srikanth and Sam Toueg, Simulating authenticated broadcasts to derive simple fault-tolerant algorithms, Distributed Computing 2(2), 1987
    locator: the echo broadcast that simulates signed messages
  - paper: doi:10.1145/4221.214134
    title: Gabriel Bracha and Sam Toueg, Asynchronous consensus and broadcast protocols, Journal of the ACM 32(4), 1985
    locator: the bound n > 3t for asynchronous Byzantine protocols
  - paper: "Christian Cachin and Stefano Tessaro, Asynchronous verifiable information dispersal, 24th IEEE Symposium on Reliable Distributed Systems (SRDS), 2005"
    locator: the AVID protocol, reliable broadcast of long messages with erasure codes
---

In Byzantine reliable broadcast, one sender gives a message to $n$ processes, and the honest processes must either all deliver the same message or deliver nothing, even when the sender and up to $t$ other processes are [Byzantine](/byzantine-failure-model/). With an honest sender, every honest process must deliver its message. It is the basic communication primitive of asynchronous Byzantine protocols. Unlike [consensus](/consensus-problem/) it has deterministic solutions in the [asynchronous model](/asynchronous-model/), because it does not ask honest processes to decide when the sender is faulty. The standard algorithm is [Bracha reliable broadcast](/bracha-reliable-broadcast/).

## In plain words

One computer sends a message to a group. If the sender is honest, everyone must get its message. If the sender is a traitor, it may try to tell different members different things. The rule is then: either all honest members get the same message, or none of them gets anything.

A weaker rule, called consistent broadcast, only says that two honest members never get different messages. It allows a traitor to give the message to some honest members and not to others. Reliable broadcast forbids this too: if one honest member gets the message, all honest members get it.

## Definition

There are $n$ processes on reliable, authenticated point-to-point links. The network is asynchronous. At most $t$ processes are Byzantine. A designated process $s$ can *broadcast* a message $m$, and a process *delivers* a message with sender $s$. Byzantine reliable broadcast, in the form of Cachin, Guerraoui and Rodrigues, asks for five properties.

- **Validity.** If an honest sender $s$ broadcasts $m$, every honest process eventually delivers $m$.
- **No duplication.** Every honest process delivers at most one message with sender $s$.
- **Integrity.** If an honest process delivers $m$ with sender $s$, and $s$ is honest, then $s$ broadcast $m$.
- **Consistency.** If honest $p$ delivers $m$ and honest $q$ delivers $m'$, both with sender $s$, then $m = m'$.
- **Totality.** If some honest process delivers a message with sender $s$, every honest process eventually delivers a message with sender $s$.

**Byzantine consistent broadcast** is the same problem without totality: validity, no duplication, integrity and consistency.

With a faulty sender no property asks for a delivery. This is the main difference from [Byzantine broadcast](/byzantine-broadcast/), where every honest process must decide even when the sender is faulty, which needs synchrony or randomization. Here a faulty sender that sends nothing causes no delivery, and no honest process can tell this from a slow sender.

## Variants

- **Consistent broadcast.** Without totality, as above. It is cheaper by one round, and it is enough when a process that did not deliver can later fetch the message from others.
- **Multi-shot broadcast.** Each message carries a sequence number, and the properties hold per pair of sender and sequence number. Each sender can then broadcast many messages, and one instance runs per pair.
- **Verifiable or validated broadcast.** A predicate on messages is fixed, and honest processes deliver only messages that pass it. Asynchronous protocols use it to stop faulty processes from sending values that no honest process could have sent.
- **Information dispersal.** For long messages, each process stores only a fragment, and the message can be rebuilt from enough fragments (AVID, Cachin and Tessaro 2005).
- **Crash faults.** With crash faults only, reliable broadcast is simpler: a process relays a message the first time it gets it. The ordered forms are [FIFO broadcast](/fifo-broadcast/), [causal broadcast](/causal-broadcast/) and [total order broadcast](/total-order-broadcast/).

## Examples

Take $n = 4$, $t = 1$, a faulty sender $p_1$, and the authenticated echo broadcast: a process echoes the first message of the sender, and delivers after echoes from more than $(n + t)/2$ processes, that is 3. The sender sends $m$ to $p_2$ and $p_3$ and nothing to $p_4$. It also sends echo$(m)$, but only to $p_2$.

- $p_2$ gets echo$(m)$ from $p_1$, $p_2$ and $p_3$, and delivers $m$.
- $p_3$ gets echo$(m)$ from $p_2$ and $p_3$ only, and never delivers.
- $p_4$ gets echo$(m)$ from $p_2$ and $p_3$ only, and never delivers.

No two honest processes delivered different messages, so consistency holds. But $p_2$ delivered and $p_3$ did not, so totality fails: this is consistent broadcast and not reliable broadcast. In [Bracha reliable broadcast](/bracha-reliable-broadcast/), $p_2$ also sends a ready message, and the ready round brings $p_3$ and $p_4$ along.

A non-example: if every honest process delivers nothing, all five properties hold when the sender is faulty. A protocol may not do this when the sender is honest, because of validity.

## Known algorithms

| algorithm | problem | assumptions | messages | message delays |
|---|---|---|---|---|
| authenticated echo broadcast (Srikanth and Toueg 1987) | consistent | $n > 3t$, authenticated links | $O(n^2)$ | 2 |
| signed echo broadcast | consistent | $n > 3t$, [digital signatures](/digital-signature/) | $O(n)$ | 3 |
| [Bracha reliable broadcast](/bracha-reliable-broadcast/) (1987), the authenticated double-echo broadcast | reliable | $n > 3t$, authenticated links | $O(n^2)$ | 3 |
| AVID (Cachin and Tessaro 2005) | reliable, with dispersal | $n > 3t$, hash functions, erasure codes | $O(n^2)$ | 3 |

In signed echo broadcast the sender collects $\lceil (n + t + 1)/2 \rceil$ signed echoes and sends the set to all processes, so each honest process sends $O(1)$ messages. The authenticated echo broadcast is the first two rounds of Bracha's algorithm. Bracha's ready round is what adds totality.

## Bounds

- **Resilience.** Bracha and Toueg (1985) show that asynchronous Byzantine protocols of this kind need $n > 3t$ when only authenticated links are available. The algorithms in the table all assume $n > 3t$.
- **Messages.** Bracha's algorithm sends $O(n^2)$ messages with $O(n^2 |m|)$ bits. With hashes the bits fall to $O(n |m| + n^2 \lambda)$ for hash size $\lambda$. With erasure codes each process sends fragments of total size $O(|m|)$, and AVID uses about $O(n |m| + n^2 \lambda \log n)$ bits.
- **Time.** With an honest sender, three message delays for reliable broadcast and two for authenticated echo broadcast. With a faulty sender there is no bound on the time to deliver, and there may be no delivery.

## Reductions

- **Reliable broadcast is weaker than consensus.** It has deterministic asynchronous solutions, and consensus does not, by the [FLP impossibility](/flp-impossibility/). The reason is that a faulty sender may cause no output at all.
- **Total order broadcast needs both.** Reliable broadcast fixes what each sender sent, but not the order of messages from different senders. [Total order broadcast](/total-order-broadcast/) adds an order, and it is equivalent to consensus.
- **Asynchronous agreement on top of it.** [Bracha's agreement protocol](/bracha-asynchronous-agreement/) runs every message of a randomized binary agreement over reliable broadcast. This removes equivocation, so the faulty processes can only send wrong values, which a validation step then filters.

## Applications

- **Asynchronous Byzantine agreement.** [Bracha's protocol](/bracha-asynchronous-agreement/) and its successors.
- **Asynchronous common subset and BFT replication.** In [HoneyBadgerBFT](/honeybadger-bft/) each process broadcasts its batch of transactions by reliable broadcast, and binary agreements then choose which batches to keep.
- **DAG-based protocols.** Protocols such as DAG-Rider (Keidar, Kokoris-Kogias, Naor and Spiegelman 2021) build a graph of blocks, each sent by reliable broadcast, and order it later.
- **Simulating signatures.** Srikanth and Toueg used echo broadcast to give unsigned protocols properties that otherwise need signatures.

## References
