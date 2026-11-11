---
tag: 9Y7P6X
kind: algorithm
slug: bracha-reliable-broadcast
name: Bracha reliable broadcast
aliases:
- Bracha broadcast
- echo-ready broadcast
- authenticated double-echo broadcast
area: distributed/byzantine-agreement
level: advanced
summary: Asynchronous Byzantine reliable broadcast with echo and ready rounds, n > 3t, O(n^2) messages and three message delays, without signatures.
solves: [byzantine-reliable-broadcast]
model: asynchronous-model
complexity:
  vars: {n: the number of processes, t: the largest number of Byzantine processes, d: the largest message delay in the run}
  time: {worst: 3d}
  messages: {worst: n + 2n^2}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
prereqs: [asynchronous-model, byzantine-failure-model, byzantine-reliable-broadcast]
see_also: [byzantine-reliable-broadcast, bracha-asynchronous-agreement, honeybadger-bft, byzantine-quorum-system, quorum-intersection, byzantine-broadcast, total-order-broadcast]
sources:
  - paper: doi:10.1016/0890-5401(87)90054-X
    title: Gabriel Bracha, Asynchronous Byzantine agreement protocols, Information and Computation 75(2), 1987
    locator: the broadcast primitive (the initial, echo and ready messages) and its lemmas
  - paper: doi:10.1145/4221.214134
    title: Gabriel Bracha and Sam Toueg, Asynchronous consensus and broadcast protocols, Journal of the ACM 32(4), 1985
    locator: the asynchronous model and the bound n > 3t for asynchronous Byzantine protocols
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luis Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Section 3.11, Byzantine reliable broadcast (the authenticated double-echo broadcast algorithm)
  - paper: doi:10.1007/BF01667080
    title: T. K. Srikanth and Sam Toueg, Simulating authenticated broadcasts to derive simple fault-tolerant algorithms, Distributed Computing 2(2), 1987
    locator: the echo broadcast that the first round of Bracha's primitive extends
---

Bracha reliable broadcast lets one sender give a message to $n$ processes in an [asynchronous](/asynchronous-model/) network so that all honest processes deliver the same message, or none of them delivers anything, even when the sender and up to $t < n/3$ other processes are [Byzantine](/byzantine-failure-model/). It uses no signatures. The sender sends its message, every process echoes the first message it gets from the sender, and then the processes exchange ready messages. It sends $O(n^2)$ messages and, with an honest sender, it delivers after three message delays. Gabriel Bracha gave it in 1987 as the base of his [asynchronous agreement protocol](/bracha-asynchronous-agreement/). The problem it solves, with its five properties, is on the [Byzantine reliable broadcast](/byzantine-reliable-broadcast/) page.

## In plain words

One computer, the sender, wants to give a message to a group. The sender may be a traitor that gives different messages to different members, and some members may lie too.

Each member first repeats to everyone the message it got from the sender. When a member hears the same message repeated by a large part of the group, it says "ready" for that message. A member also says "ready" when enough other members already said it, because at least one of them is honest. A member accepts the message when it hears "ready" from a large part of the group.

Two large parts of the group always share an honest member, so two members cannot accept different messages. If one honest member accepts, enough honest members said "ready" to make all others say it and accept too.

## The problem

There are $n$ processes with reliable, authenticated point-to-point links. The network is asynchronous: a message between honest processes always arrives, but after any finite delay, and the adversary picks the order. At most $t$ processes are Byzantine, and $n > 3t$. One process $s$ is the sender. The algorithm must give validity, no duplication, integrity, consistency and totality, as defined on the [Byzantine reliable broadcast](/byzantine-reliable-broadcast/) page. In short: with an honest sender all honest processes deliver its message; honest processes never deliver different messages; and if one honest process delivers, all do.

## The algorithm

The code of process $p_i$ is below. Each line is a rule that fires when its condition becomes true. A *broadcast* sends one message to each of the $n$ processes. Counts are over different senders, and messages that claim to come from $s$ are accepted only on the link from $s$.

```pseudo id=main
BRACHA-RBC(i, s, m)                                       ▷ n > 3t; s is the sender
L1  if i = s then broadcast initial(m)
L2  on the first initial(v) from s: broadcast echo(v)
L3  on echo(v) from more than (n + t)/2 senders, if no ready sent yet: broadcast ready(v)
L4  on ready(v) from t + 1 senders, if no ready sent yet: broadcast ready(v)
L5  on ready(v) from 2t + 1 senders, if nothing delivered yet: deliver v
```

The three thresholds have three jobs. More than $(n + t)/2$ echoes is a quorum that any other such quorum meets in an honest process, so all honest readys from line L3 are for one value. $t + 1$ readys contain an honest one, so line L4 only repeats a value that an honest process chose; it is the amplification step that gives totality. $2t + 1$ readys contain $t + 1$ honest ones, which is enough to make every other honest process pass line L4.

## Example

Take $n = 4$, $t = 1$, and a Byzantine sender $p_1$. The thresholds are 3 echoes (more than $2.5$), 2 readys for line L4 and 3 readys for line L5. The sender sends initial(a) to $p_2$ and $p_3$ and initial(b) to $p_4$. In every later step $p_1$ also sends echo(a) and ready(a) to $p_2$ and $p_3$, and echo(b) and ready(b) to $p_4$. The scheduler delivers messages in the order they were sent.

| step | event | effect |
|---|---|---|
| 1 | $p_2$, $p_3$ get initial(a); $p_4$ gets initial(b) | $p_2$, $p_3$ broadcast echo(a); $p_4$ broadcasts echo(b) |
| 2 | $p_2$ and $p_3$ each have echo(a) from $p_1$, $p_2$, $p_3$ | each broadcasts ready(a) by line L3 |
| 3 | $p_2$ and $p_3$ each have ready(a) from $p_1$, $p_2$, $p_3$ | each delivers a |
| 4 | $p_4$ has echo(a) from 2 and echo(b) from 2, no quorum; ready(a) from $p_2$, $p_3$ | $p_4$ broadcasts ready(a) by line L4 |
| 5 | $p_4$ has ready(a) from $p_2$, $p_3$, $p_4$ | $p_4$ delivers a |

The sender tried to split the group, but $p_4$ is pulled to a by the two honest readys. All three honest processes deliver a. They send 24 messages: 12 echoes and 12 readys.

## Correctness

The full proof is below. It has three steps.

- **One ready value.** Two sets of more than $(n + t)/2$ echoes share more than $t$ processes, so an honest one, which echoes only once. So all readys from line L3 carry one value $v^*$. A ready from line L4 copies an earlier honest ready, so by induction it also carries $v^*$.
- **Consistency and totality.** A delivery needs $2t + 1$ readys, so $t + 1$ honest readys for $v^*$. These $t + 1$ honest readys reach every honest process, which then sends ready$(v^*)$ by line L4. So all $n - t \ge 2t + 1$ honest processes send it, and all deliver $v^*$.
- **Validity.** With an honest sender, the $n - t$ honest echoes are more than $(n + t)/2$ exactly when $n > 3t$, so every honest process sends ready for the message of $s$ and delivers it.

Consistency does not use $n > 3t$. Validity and totality do.

## Complexity

- **Messages.** The sender sends $n$ initial messages, and each honest process sends at most $n$ echoes and $n$ readys. So the honest processes send at most $n + 2n^2$ messages, exactly $n + 2n^2$ when all are honest.
- **Bits.** Each echo and ready carries the message, so $O(n^2 |m|)$ bits. Sending a hash in the echoes and readys gives $O(n |m| + n^2 \lambda)$ bits for hash size $\lambda$, at the cost of a step to fetch the message.
- **Time.** With an honest sender, three message delays: initial, echo and ready. With a faulty sender there is no bound, because the sender may never send; this is allowed, since the properties then only ask for all or nothing.
- **Space.** Each process keeps counters per value and the sets of senders, $O(n)$ per broadcast.

## Properties

- **Deterministic and signature free.** Only authenticated links are needed.
- **Optimal resilience.** $n > 3t$ is necessary for Byzantine reliable broadcast in asynchrony without signatures.
- **Asynchronous.** It uses no clocks and no timeouts, so the [FLP impossibility](/flp-impossibility/) does not apply: reliable broadcast is not consensus, because a faulty sender may cause no delivery at all.
- **No termination with a faulty sender.** An honest process cannot know that nothing will be delivered.

## Variants and improvements

- **Echo on echoes.** In Bracha's paper a process also sends echo$(v)$ when it gets more than $(n + t)/2$ echo$(v)$ or $t + 1$ ready$(v)$ before the initial message. The properties above do not need this rule.
- **Consistent broadcast.** Without the ready round the result is the authenticated echo broadcast of Srikanth and Toueg, which gives consistency but not totality. See the comparison on the [Byzantine reliable broadcast](/byzantine-reliable-broadcast/) page.
- **Erasure codes.** For long messages, the sender sends to each process one fragment of a [Reed-Solomon](/reed-solomon-code/) encoding, and the echoes carry fragments and a [Merkle](/merkle-tree/) root. This is asynchronous verifiable information dispersal (AVID, Cachin and Tessaro 2005), with about $O(n |m| + n^2 \lambda \log n)$ bits. [HoneyBadgerBFT](/honeybadger-bft/) uses it.
- **Signatures.** With signatures, a process can collect $2t + 1$ signed echoes into a certificate and forward it, which trades messages for computation.

## When to use it

Use Bracha reliable broadcast as a building block in asynchronous Byzantine protocols, where a process must make sure that all others see the same message from it, or nothing. [Bracha's agreement protocol](/bracha-asynchronous-agreement/) runs every step over it, and the asynchronous common subset of [HoneyBadgerBFT](/honeybadger-bft/) runs one instance per process. It is not enough to order many messages from many senders; that is [total order broadcast](/total-order-broadcast/), which needs consensus.

## Pitfalls

- **Counting messages instead of senders.** A faulty process that sends echo(a) twice counts once.
- **Echoing more than once.** An honest process must echo only the first initial message from $s$. If it echoes both values of an equivocating sender, Lemma 1 of the proof breaks.
- **Waiting for the echo quorum only.** Without line L4 a process that saw a split of echoes never sends ready, and totality fails.
- **Expecting termination with a faulty sender.** Code that waits for a delivery from every sender blocks forever on a silent one.
- **Lowering the echo threshold.** With "at least $(n + t)/2$" or "a majority" in place of "more than $(n + t)/2$", two echo quorums can miss each other on honest processes, and consistency fails. A threshold of $n - t$ is safe, and it equals the strict one when $n = 3t + 1$.

## Implementations

## History

Srikanth and Toueg (1987) used an echo round to simulate signed messages without signatures. Bracha and Toueg (1985) set the asynchronous Byzantine model and showed that $n > 3t$ is needed. Bracha (1987) added the ready round, which gives totality, and used the primitive to run each step of a randomized agreement protocol. Cachin, Guerraoui and Rodrigues (2011) call it authenticated double-echo broadcast. Cachin and Tessaro (2005) made it efficient for long messages with erasure codes.

## References
