---
tag: G4SWD3
kind: problem
slug: consensus-problem
name: Consensus problem
aliases:
- distributed consensus
- agreement problem
area: distributed/consensus
level: intro
summary: Processes must agree on one value, with agreement, validity and termination.
prereqs: [crash-failure, synchronous-model, asynchronous-model]
see_also: [consensus-properties, flp-impossibility, floodset, ben-or-consensus, chandra-toueg-consensus, paxos, raft, replicated-state-machine]
sources:
  - paper: doi:10.1145/3149.214121
    title: Michael J. Fischer, Nancy A. Lynch and Michael S. Paterson, Impossibility of distributed consensus with one faulty process, Journal of the ACM 32(2), 1985
    locator: pages 374 to 382 (no deterministic asynchronous protocol solves consensus with one crash)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 5 (coordinated attack), Chapter 6 (agreement with stopping and Byzantine failures in the synchronous model, FloodSet in Section 6.2 and the f + 1 round lower bound in Section 6.7), Chapter 21 (consensus in asynchronous networks, Sections 21.2 to 21.4), Chapter 25 (consensus with partial synchrony)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 5 (fault-tolerant consensus, Section 5.1 synchronous with crashes, Section 5.3 the asynchronous impossibility) and Chapter 14 (randomized consensus)
  - paper: doi:10.1145/42282.42283
    title: Cynthia Dwork, Nancy Lynch and Larry Stockmeyer, Consensus in the presence of partial synchrony, Journal of the ACM 35(2), 1988
    locator: pages 288 to 323 (consensus with partial synchrony, n > 2f for crash failures and n > 3f for Byzantine failures)
  - paper: doi:10.1145/226643.226647
    title: Tushar Deepak Chandra and Sam Toueg, Unreliable failure detectors for reliable distributed systems, Journal of the ACM 43(2), 1996
    locator: pages 225 to 267 (consensus with failure detectors, and the equivalence of consensus and atomic broadcast)
  - paper: doi:10.1145/800221.806707
    title: Michael Ben-Or, Another advantage of free choice, Completely asynchronous agreement protocols, PODC 1983
    locator: pages 27 to 30 (randomized asynchronous consensus)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luis Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 5 (regular and uniform consensus, and algorithms with failure detectors)
---

In the consensus problem, each of $n$ processes starts with an input value, and the processes must all decide the same value, which must be one of the inputs, even though some of them may fail. It is the basic problem of fault-tolerant distributed computing: [state machine replication](/replicated-state-machine/), atomic commit and [total order broadcast](/total-order-broadcast/) all reduce to it. Its solvability depends sharply on the model. It is solvable with any number of crashes in the [synchronous model](/synchronous-model/), impossible for deterministic algorithms with one crash in the [asynchronous model](/asynchronous-model/), and solvable again with randomization, failure detectors or [partial synchrony](/partial-synchrony/).

## In plain words

A group of computers must choose one value together, for example which request to run next. Each computer starts with its own proposal. In the end, every working computer must pick a value, all picks must be the same, and the value must be one that some computer proposed.

This would be easy if no computer ever stopped and messages always arrived on time. The hard part is failure. A computer may stop in the middle of telling the others its value. A message may be slow, and nobody can tell a slow computer from a stopped one.

What can be done depends on what is known about time. With a shared clock and bounded delays, the group can always agree. With no bounds at all, no fixed method can be sure to finish.

## Definition

**Input.** $n$ processes $p_1, \ldots, p_n$, connected by reliable channels. Process $p_i$ has an input $v_i \in V$. At most $f$ processes may fail, in a stated failure model, usually [crash failures](/crash-failure/). A timing model is fixed: synchronous, asynchronous or partially synchronous.

**Output.** Each process may decide a value of $V$, once. An algorithm solves consensus if every execution has these [properties](/consensus-properties/):

- **Agreement.** No two correct processes decide different values. *Uniform agreement* asks this of all processes, also faulty ones.
- **Validity.** If a process decides $v$, then $v$ is the input of some process. A weaker form, unanimity, asks only that if all inputs are $v$, the decision is $v$.
- **Integrity.** Each process decides at most once.
- **Termination.** Every correct process eventually decides.

Agreement, validity and integrity are safety properties and must hold in every execution. Termination is a liveness property. *Binary consensus* is the case $V = \{0, 1\}$.

## Variants

- **Failure model.** Crash failures, omission failures, or [Byzantine failures](/byzantine-failure-model/), where faulty processes may lie. With Byzantine failures, validity talks only about the inputs of correct processes, see [strong validity](/strong-validity/) and [weak validity](/weak-validity/).
- **Uniform consensus.** Uniform agreement instead of agreement.
- **Randomized consensus.** Termination is required only with probability 1.
- **Weaker agreement.** [$k$-set agreement](/k-set-agreement/) allows up to $k$ different decisions, and [approximate agreement](/approximate-agreement/) allows decisions within $\varepsilon$ of each other.
- **Vector agreement.** [Interactive consistency](/interactive-consistency/) asks for agreement on the vector of all inputs.
- **Lossy links.** The [two generals problem](/two-generals-problem/) is consensus between two processes with no crash but with links that may lose messages. It has no solution.
- **Repeated consensus.** A sequence of instances, one per slot of a log, gives [total order broadcast](/total-order-broadcast/) and replication, as in [Multi-Paxos](/multi-paxos/) and [Raft](/raft/).
- **Shared memory.** Processes communicate through shared objects instead of messages. The power of an object type to solve wait-free consensus is its [consensus number](/consensus-number/).

## Examples

- **No failures.** Each process sends its input to all, waits for all $n$ inputs and decides the smallest. This works in every timing model, but blocks for ever if one process crashes.
- **Synchronous, one crash.** With $n = 3$ and inputs 0, 1, 1, suppose $p_1$ crashes in round 1 after sending its value only to $p_2$. After round 1, $p_2$ knows $\{0, 1\}$ and $p_3$ knows $\{1\}$. In round 2, $p_2$ sends 0 to $p_3$, and both decide 0. [FloodSet](/floodset/) runs $f + 1 = 2$ rounds so that one round without a crash is sure to happen.
- **Asynchronous.** If $p_1$ is silent, $p_2$ cannot tell whether $p_1$ crashed or its messages are slow. Waiting for $p_1$ can block for ever; deciding without $p_1$ is dangerous if $p_1$ is alive and has decided otherwise. The [FLP impossibility](/flp-impossibility/) turns this dilemma into a proof.

## Known algorithms

| model | algorithm | resilience | cost |
|---|---|---|---|
| synchronous, crash | [FloodSet](/floodset/) | any $f < n$ | $f + 1$ rounds |
| synchronous, Byzantine | [oral messages](/oral-messages-algorithm/), [phase king](/phase-king-algorithm/) | $n > 3f$ | $f + 1$ rounds, or $O(f)$ rounds with fewer messages |
| synchronous, Byzantine with signatures | [Dolev-Strong](/dolev-strong-algorithm/) | any $f < n$ | $f + 1$ rounds |
| asynchronous, randomized, crash | [Ben-Or](/ben-or-consensus/) | $n > 2f$ | terminates with probability 1 |
| asynchronous, randomized, Byzantine | [Bracha](/bracha-asynchronous-agreement/) | $n > 3f$ | local coins; with a common coin, as in [Rabin](/rabin-randomized-byzantine-agreement/), a constant expected number of rounds |
| asynchronous with $\Diamond\mathcal{S}$, crash | [Chandra-Toueg](/chandra-toueg-consensus/) | $n > 2f$ | deterministic, rotating coordinator |
| partial synchrony, crash | DLS, [Paxos](/paxos/), [Raft](/raft/) | $n > 2f$ | safe always, live after GST |
| partial synchrony, Byzantine | DLS, [PBFT](/pbft/) | $n > 3f$ | safe always, live after GST |

## Bounds

- **Rounds, synchronous, crash.** Every algorithm needs $f + 1$ rounds in the worst case when $n \ge f + 2$, the [consensus round lower bound](/consensus-round-lower-bound/). FloodSet matches it. The same bound holds for Byzantine failures, see the [Byzantine round lower bound](/byzantine-round-lower-bound/).
- **Asynchronous, deterministic.** Impossible with one crash, by the [FLP impossibility](/flp-impossibility/), even for binary inputs and reliable links.
- **Resilience with crashes.** Any $f < n$ in the synchronous model; $n > 2f$ is necessary and sufficient in partial synchrony, for randomized asynchronous algorithms, and with the failure detector $\Diamond\mathcal{S}$. The proof of necessity splits the processes into two groups of at most $f$ that cannot hear each other for a long time.
- **Resilience with Byzantine failures.** $n > 3f$ in all timing models without signatures, the [Byzantine resilience bound](/byzantine-resilience-bound/).
- **Failure detectors.** [$\Omega$](/omega-failure-detector/) is the [weakest failure detector](/weakest-failure-detector-consensus/) for consensus with a majority of correct processes.
- **Randomized, local coins.** Ben-Or's algorithm can take an exponential expected number of rounds when $f = \Theta(n)$. A common coin gives a constant expected number.

## Reductions

- **Consensus and total order broadcast are equivalent** with crash failures in the asynchronous model: a sequence of consensus instances orders messages, and a total order broadcast decides by taking the first value delivered (Chandra and Toueg, 1996).
- **Consensus and atomic commit.** [Atomic commit](/atomic-commit/) is consensus on commit or abort with a different validity condition. [Two-phase commit](/two-phase-commit/) solves it but can block when the coordinator crashes, and [Paxos commit](/paxos-commit/) runs consensus to avoid that.
- **From binary to multi-valued.** Multi-valued consensus reduces to binary consensus, for example by agreeing bit by bit on the input of some process, at extra cost in rounds or messages.
- **Consensus number.** In shared memory, an object solves wait-free consensus for $n$ processes exactly when its [consensus number](/consensus-number/) is at least $n$. [Registers have consensus number one](/registers-have-consensus-number-one/), which is the shared memory form of FLP.

## Applications

- **Replication.** [Replicated state machines](/replicated-state-machine/) run a consensus instance for each command, so that all replicas apply the same commands in the same order. [Paxos](/paxos/), [Raft](/raft/), [Zab](/zab/) and [Viewstamped Replication](/viewstamped-replication/) are the standard protocols.
- **Configuration and coordination.** Leader election, locks, membership and [cluster reconfiguration](/cluster-reconfiguration/) are built on a consensus service.
- **Distributed transactions.** Atomic commit decides whether a transaction commits at all its participants.
- **Blockchains.** [Nakamoto consensus](/nakamoto-consensus/) and Byzantine fault-tolerant protocols agree on a sequence of blocks among parties that may lie.

## References
