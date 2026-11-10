---
tag: B9K8H1
kind: model
slug: synchronous-model
name: Synchronous message-passing model
aliases:
- synchronous system
- lock-step model
area: distributed/consensus
level: core
summary: Processes proceed in rounds with known bounds on message delay.
prereqs: []
see_also: [asynchronous-model, partial-synchrony, crash-failure, floodset, consensus-round-lower-bound, synchronizer, local-model, round-complexity]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 2 (the synchronous network model, its failures and its complexity measures), Chapter 5 (coordinated attack), Chapter 6 (agreement with stopping and Byzantine failures, FloodSet in Section 6.2 and the f + 1 round lower bound in Section 6.7)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 2, Section 2.1 (formal models of synchronous and asynchronous message passing systems), Chapter 5, Section 5.1 (consensus in synchronous systems)
  - paper: doi:10.1016/0020-0190(82)90033-3
    title: Michael J. Fischer and Nancy A. Lynch, A lower bound for the time to assure interactive consistency, Information Processing Letters 14(4), 1982
    locator: pages 183 to 186 (f + 1 rounds are needed for agreement with f faults)
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine generals problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: pages 382 to 401 (agreement with Byzantine faults needs n > 3f without signatures)
---

The synchronous message-passing model is the model in which processes run in lock step: computation is a sequence of rounds, and every message sent in a round arrives before the next round begins. It is the strongest of the usual timing models, and it is the model of the [LOCAL](/local-model/) and [CONGEST](/congest-model/) models of distributed graph algorithms and of the classic agreement algorithms. In it, a missing message is a sure sign of a failure, which is exactly what the [asynchronous model](/asynchronous-model/) lacks.

## The machine

**Network.** There is a directed graph $G = (V, E)$ with $n$ vertices. Each vertex is a process, and each edge $(i, j)$ is a channel from $i$ to $j$. For consensus, $G$ is usually the complete graph. The processes know $n$, and each process knows its own identifier.

**Processes.** Following Lynch (Chapter 2), process $i$ is a state machine with a set of states, a set of start states, a *message generation* function $\mathit{msgs}_i$ and a *state transition* function $\mathit{trans}_i$. The function $\mathit{msgs}_i$ maps the current state and an out-neighbour $j$ to the message for $j$, or to *null* for no message. The function $\mathit{trans}_i$ maps the current state and the vector of messages received from the in-neighbours to the next state.

**Rounds.** All processes start in a start state. Each round has two steps.

1. Every process applies $\mathit{msgs}_i$ to its state and puts the messages on its outgoing channels.
2. Every process applies $\mathit{trans}_i$ to its state and to the messages on its incoming channels, and the channels become empty.

Every message sent in round $r$ is received in round $r$. The execution is fully determined by the start states, unless the algorithm is randomized or faults occur.

**A real system that gives rounds.** Rounds can be built if there are known bounds: every message arrives within $\Delta$, every process takes a step at least every $\Phi$ time units of its local clock, and clocks are close enough. Each process then waits a fixed time per round, long enough for every message of the round to arrive.

**Failures.** The model is used with several failure types.

- **Stopping or [crash failures](/crash-failure/).** A process may stop at any point. In the round of its crash, it may send its messages to any subset of its out-neighbours, so a crash can fall in the middle of a broadcast. After that it sends nothing.
- **Byzantine failures.** A faulty process may send any messages at all, see the [Byzantine failure model](/byzantine-failure-model/).
- **Link failures.** A channel may lose messages, as in the [two generals problem](/two-generals-problem/).

At most $f$ processes are faulty, and $f$ is known.

## What it counts

- **Time** is the number of rounds until all non-faulty processes have produced their outputs, see [round complexity](/round-complexity/). For agreement the usual measure is the worst case over all inputs and all failure patterns with at most $f$ faults.
- **Communication** is the number of non-null messages sent, see [message complexity](/message-complexity/), and sometimes the total number of bits.
- **Local computation** is free. Only rounds and messages are counted.

Early stopping algorithms also count rounds as a function of the number $t \le f$ of crashes that actually happen.

## Relation to other models

- **Asynchronous model.** Every synchronous execution is also an execution that the asynchronous model allows, so an algorithm that is correct in the asynchronous model is correct here. The converse fails: algorithms here use the absence of a message as information.
- **Synchronizers.** With no failures, a [synchronizer](/synchronizer/) simulates synchronous rounds on an asynchronous network at some cost in messages and time. With crashes this is impossible, because a process cannot tell whether a missing message is late or will never come; this is the content of the [FLP impossibility](/flp-impossibility/).
- **Partial synchrony.** In the [partial synchrony](/partial-synchrony/) model, rounds work only after an unknown time GST, or with unknown bounds. Algorithms there must also be safe when rounds fail.
- **LOCAL and CONGEST.** These graph models are the synchronous model with no failures, with unbounded messages (LOCAL) or messages of $O(\log n)$ bits (CONGEST).

## Known results in the model

**Crash failures, any $f < n$.** [Consensus](/consensus-problem/) is solvable for every $f < n$. [FloodSet](/floodset/) runs $f + 1$ rounds: each process sends every value it has seen to all, and decides on the minimum after round $f + 1$. Some round among the $f + 1$ has no crash, and after that round all processes that are still alive have the same set. The bound is tight: every algorithm needs $f + 1$ rounds in the worst case when $n \ge f + 2$, the [consensus round lower bound](/consensus-round-lower-bound/) of Fischer and Lynch (1982) and Dolev and Strong (1983). Early stopping algorithms decide in $\min(f + 1, t + 2)$ rounds when only $t$ crashes happen.

**Byzantine failures.** Without signatures, agreement is solvable exactly when $n > 3f$ ([Byzantine resilience bound](/byzantine-resilience-bound/)), in $f + 1$ rounds by the [oral messages algorithm](/oral-messages-algorithm/) with exponential messages, or with polynomial messages by the [phase king algorithm](/phase-king-algorithm/) in $O(f)$ rounds, which needs $n > 4f$ in its simplest form. With signatures, the [Dolev-Strong algorithm](/dolev-strong-algorithm/) tolerates any $f < n$ in $f + 1$ rounds. The $f + 1$ lower bound also holds for Byzantine faults, see the [Byzantine round lower bound](/byzantine-round-lower-bound/).

**Lossy links.** With links that may lose any message, even two processes with no crash cannot agree on a common action: the [two generals problem](/two-generals-problem/) has no solution, and randomization only makes the error probability small.

**Summary of crash resilience across models.** For consensus with crash failures:

| model | crashes tolerated | page |
|---|---|---|
| synchronous | any $f < n$ | this page |
| [partial synchrony](/partial-synchrony/) | $n > 2f$ | partial synchrony |
| [asynchronous](/asynchronous-model/), deterministic | none ($f \ge 1$ is impossible) | [FLP](/flp-impossibility/) |
| asynchronous, randomized | $n > 2f$ | [Ben-Or](/ben-or-consensus/) |

## References
