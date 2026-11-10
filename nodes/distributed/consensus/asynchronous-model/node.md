---
tag: B2TQHC
kind: model
slug: asynchronous-model
name: Asynchronous message-passing model
aliases:
- asynchronous system
area: distributed/consensus
level: core
summary: No bounds on message delay or relative process speed.
prereqs: [synchronous-model]
see_also: [flp-impossibility, partial-synchrony, crash-failure, failure-detector, ben-or-consensus, synchronizer, k-set-agreement, approximate-agreement]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 8 (the I/O automaton model, fairness and the time measure with upper bounds), Chapter 14 (the asynchronous network model), Chapter 21 (asynchronous network computing with process failures, the impossibility in Section 21.2, randomization in Section 21.3 and failure detectors in Section 21.4)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 2, Section 2.1 (formal models of asynchronous message passing systems, admissible executions and time complexity), Chapter 5, Section 5.3 (the impossibility of consensus in asynchronous systems)
  - paper: doi:10.1145/3149.214121
    title: Michael J. Fischer, Nancy A. Lynch and Michael S. Paterson, Impossibility of distributed consensus with one faulty process, Journal of the ACM 32(2), 1985
    locator: pages 374 to 382 (the model of configurations, steps and admissible runs, and the impossibility)
  - paper: doi:10.1145/226643.226647
    title: Tushar Deepak Chandra and Sam Toueg, Unreliable failure detectors for reliable distributed systems, Journal of the ACM 43(2), 1996
    locator: pages 225 to 267 (the asynchronous model extended with failure detectors)
---

The asynchronous message-passing model has no timing assumptions at all: a message can take any finite time to arrive, and a process can take any finite time between two steps. Algorithms cannot use clocks or timeouts, so they must be correct for every interleaving of steps that the adversary chooses. A crashed process cannot be told apart from a slow one, and so deterministic [consensus](/consensus-problem/) is impossible here with even one crash, by the [FLP impossibility](/flp-impossibility/).

## The machine

**Network.** There are $n$ processes, usually on a complete graph of point to point channels. Each process knows $n$ and its own identifier.

**Processes and channels.** In Lynch's formalism (Chapter 8), each process and each channel is an I/O automaton. A process has states, start states, and steps of three kinds: *receive* a message, *send* a message, and *internal* steps. A channel from $i$ to $j$ is a reliable queue: every message that $i$ sends to $j$ is eventually delivered to $j$, exactly once. Some presentations use FIFO channels and some use a multiset of messages in transit, as in Fischer, Lynch and Paterson; for consensus the difference does not matter.

**Executions.** An execution is a sequence of steps of processes and channels, interleaved in any order. An execution is *fair*, or *admissible*, if every process that does not fail takes infinitely many steps, and every message sent to a process that does not fail is eventually delivered. No bound is placed on the number of steps of other processes between two steps of one process, or on the time a message stays in transit. The processes have no clocks.

**The configuration view.** Fischer, Lynch and Paterson use an equivalent form. A configuration is the states of all processes and the multiset of messages in transit. A step of process $p$ takes one message for $p$ from the buffer, or the null message, changes the state of $p$ and adds finitely many messages to the buffer. The adversary chooses the next step.

**Failures.** At most $f$ processes may fail.

- **[Crash failures](/crash-failure/).** A process stops and takes no further steps. A process that crashes during a broadcast may have sent some of the messages and not others.
- **Byzantine failures.** A faulty process may send arbitrary messages.

**Extensions.** The model is often extended with an oracle: a [failure detector](/failure-detector/) module at each process, or local coin flips for [randomized algorithms](/randomized-algorithm/). The timing remains asynchronous.

## What it counts

- **Messages.** The number of messages sent, and the number of bits, in the worst execution, see [message complexity](/message-complexity/).
- **Time.** Time cannot be measured by the algorithm, but it can be measured for analysis. Lynch's time measure assumes an upper bound $\ell$ on the time between two steps of a process and $d$ on message delay, unknown to the processes, and states the time as a function of $\ell$ and $d$. An equivalent view counts *asynchronous rounds*: a time unit is the longest message delay in the execution, normalized to 1.
- **Termination.** For problems like consensus, the main question is whether every admissible execution terminates, not how fast. Randomized algorithms are measured by expected rounds against a stated adversary.

## Relation to other models

- **Synchronous model.** The [synchronous model](/synchronous-model/) is a special case in which the adversary must deliver every message within one round. Results that hold here hold there, and impossibility results there carry over here.
- **Synchronizers.** Without failures, a [synchronizer](/synchronizer/) lets a synchronous algorithm run on an asynchronous network, so the two models are equal in what they can compute. With crashes they are not: the synchronizer would wait for ever for a crashed process.
- **Partial synchrony.** The [partial synchrony](/partial-synchrony/) model adds timing bounds that hold only eventually, or that are unknown. Algorithms for it are often written in the asynchronous model plus a failure detector.
- **Shared memory.** With $n > 2f$ crash failures, atomic read and write registers can be emulated over asynchronous message passing, by the algorithm of Attiya, Bar-Noy and Dolev, so results for asynchronous shared memory with registers carry over.

## Known results in the model

**Why a crash looks like a delay.** Let $q$ crash at the start of an execution $\alpha$, and let $\beta$ be the same execution in which $q$ is correct but all its messages are delayed until after time $t$. Up to time $t$, every other process sees exactly the same steps in $\alpha$ and in $\beta$. Since $t$ can be as large as the adversary likes, no process can ever be sure that $q$ has crashed. Every impossibility result below uses this fact.

**Consensus.**

- **Deterministic, with one crash: impossible.** The [FLP impossibility](/flp-impossibility/) shows that no deterministic algorithm solves consensus if one process may crash, even with reliable channels.
- **With no failures: easy.** Each process sends its input to all and waits for all $n$ values.
- **Randomized: possible with $n > 2f$.** [Ben-Or's algorithm](/ben-or-consensus/) decides with probability 1. With $n \le 2f$, no algorithm, randomized or not, solves consensus: two halves of the processes can each decide alone while the messages between them are slow.
- **With failure detectors.** With a detector in $\Diamond\mathcal{S}$ and $n > 2f$, the [Chandra-Toueg algorithm](/chandra-toueg-consensus/) solves consensus, and [$\Omega$](/omega-failure-detector/) is the [weakest failure detector](/weakest-failure-detector-consensus/) for it.
- **Byzantine, randomized: possible with $n > 3f$**, by [Bracha's algorithm](/bracha-asynchronous-agreement/).

**Weaker problems that are solvable.**

- **Reliable broadcast** with any $f < n$ crashes: relay each new message to all before delivering it.
- **[Approximate agreement](/approximate-agreement/)** with $n > 2f$ crashes: processes get values within $\varepsilon$ of each other.
- **Atomic registers** with $n > 2f$ crashes, as above.

**Weaker problems that are still impossible.** [$k$-set agreement](/k-set-agreement/), where at most $k$ different values may be decided, is impossible deterministically when $f \ge k$ (Borowsky and Gafni, Herlihy and Shavit, Saks and Zaharoglou, 1993). Consensus is the case $k = 1$.

## References
