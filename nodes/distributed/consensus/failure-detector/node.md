---
tag: KVH786
kind: concept
slug: failure-detector
name: Failure detector
aliases:
- unreliable failure detector
area: distributed/consensus
level: advanced
summary: Oracle that gives processes possibly inaccurate suspicion of crashed peers.
prereqs: [flp-impossibility, crash-failure]
see_also: [eventually-perfect-failure-detector, omega-failure-detector, weakest-failure-detector-consensus, chandra-toueg-consensus, partial-synchrony, failure-detection, phi-accrual-failure-detector, swim]
sources:
  - paper: doi:10.1145/226643.226647
    title: Tushar Deepak Chandra and Sam Toueg, Unreliable failure detectors for reliable distributed systems, Journal of the ACM 43(2), 1996
    locator: pages 225 to 267 (failure patterns and histories, completeness and accuracy, the eight classes, reducibility, the reduction from weak to strong completeness, and consensus with S and diamond-S)
  - paper: doi:10.1145/234533.234549
    title: Tushar Deepak Chandra, Vassos Hadzilacos and Sam Toueg, The weakest failure detector for solving consensus, Journal of the ACM 43(4), 1996
    locator: pages 685 to 722 (failure detectors that output values other than sets, the detector Omega, and the weakest detector for consensus)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luis Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 2 (process abstractions, the perfect, eventually perfect and leader election detectors, and their implementations with timeouts)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 21, Section 21.4 (failure detectors in asynchronous networks)
---

A failure detector is a module at each process that outputs a list of processes it suspects to have crashed. Chandra and Toueg (1996) introduced *unreliable* failure detectors, which may suspect a live process or miss a crashed one, and classified them by two abstract properties, completeness and accuracy, instead of by timeouts. A failure detector adds just enough information to the [asynchronous model](/asynchronous-model/) to get around the [FLP impossibility](/flp-impossibility/), and it separates the timing assumptions of a system from the algorithms that run on it.

## In plain words

In a network with no timing guarantees, a computer cannot tell whether a silent peer has stopped or is only slow. A failure detector is a helper on each computer that gives its best guess: a list of the peers it thinks have stopped.

The guess can be wrong. The helper may name a working peer, and it may be late to name a stopped one. What matters is what the helper promises in the long run, for example that a stopped peer is named for ever from some point on, or that at least one working peer is no longer named from some point on.

Algorithms are written against these promises. Whoever builds the helper, with heartbeats and timeouts, must make sure that the promises hold.

## The idea

### Failure patterns and histories

There are $n$ processes, and time is a global clock that the processes cannot read. A *failure pattern* $F$ gives, for each time $t$, the set $F(t)$ of processes that have crashed by $t$. A process is *correct* if it never crashes. A failure detector history $H$ gives the output $H(p, t)$ of the module of process $p$ at time $t$, a set of suspected processes. A *failure detector* $\mathcal{D}$ maps each failure pattern $F$ to a set $\mathcal{D}(F)$ of allowed histories. A run with $\mathcal{D}$ uses one failure pattern $F$ and one history from $\mathcal{D}(F)$, and a process sees $H(p, t)$ when it queries its module at time $t$.

The definition is in terms of what the output may be, not how it is computed. This is why a detector is called an oracle.

### Completeness and accuracy

Completeness says that crashed processes are eventually suspected.

- **Strong completeness.** Eventually every crashed process is permanently suspected by every correct process.
- **Weak completeness.** Eventually every crashed process is permanently suspected by some correct process.

Accuracy limits the mistakes.

- **Strong accuracy.** No process is suspected before it crashes.
- **Weak accuracy.** Some correct process is never suspected.
- **Eventual strong accuracy.** There is a time after which no correct process is suspected by any correct process.
- **Eventual weak accuracy.** There is a time after which some correct process is never suspected by any correct process.

Completeness alone is trivial: a module that suspects everyone has it. Accuracy alone is trivial too: a module that suspects nobody has it. Each class combines one of each.

### The eight classes

| | strong accuracy | weak accuracy | eventual strong accuracy | eventual weak accuracy |
|---|---|---|---|---|
| strong completeness | perfect $\mathcal{P}$ | strong $\mathcal{S}$ | [eventually perfect](/eventually-perfect-failure-detector/) $\Diamond\mathcal{P}$ | eventually strong $\Diamond\mathcal{S}$ |
| weak completeness | $\mathcal{Q}$ | weak $\mathcal{W}$ | $\Diamond\mathcal{Q}$ | eventually weak $\Diamond\mathcal{W}$ |

A detector $\mathcal{D}'$ is *reducible* to $\mathcal{D}$ if some algorithm, using $\mathcal{D}$ and messages, builds at each process an output that is a valid history of $\mathcal{D}'$. Then $\mathcal{D}$ is at least as strong as $\mathcal{D}'$, and any problem solvable with $\mathcal{D}'$ is solvable with $\mathcal{D}$. Two detectors are *equivalent* if each is reducible to the other.

### From weak to strong completeness

Chandra and Toueg give a reduction that keeps the accuracy and makes the completeness strong. Each process $q$ forever queries its module, gets the set $\mathit{suspects}_q$ and sends it to all. A process $p$ keeps an output set, empty at the start, and runs this when it gets $\mathit{suspects}_q$ from $q$:

$$\mathit{output}_p \leftarrow (\mathit{output}_p \cup \mathit{suspects}_q) \setminus \{q\}.$$

*Strong completeness.* Let $c$ crash. By weak completeness, some correct $q$ suspects $c$ from some time on, and so it sends sets that contain $c$ for ever. Process $c$ sends finitely many messages, and all of them arrive at some time. After that, no message removes $c$ from any $\mathit{output}_p$, and each correct $p$ adds $c$ when the next set from $q$ arrives. So $c$ is in the output of every correct process for ever.

*Accuracy is kept.* A process $s$ enters $\mathit{output}_p$ only when some module suspected $s$. So with strong accuracy, $s$ enters only after it crashed, and with weak accuracy the correct process that no module suspects never enters. For the eventual forms, let a correct process $\ell$ be unsuspected by every module from a time $t_0$ on. The sets sent before $t_0$ are finitely many and all arrive. After that, the next message from $\ell$ to $p$ removes $\ell$ from $\mathit{output}_p$, and no later set adds it again. The same argument applies to every correct $\ell$ for eventual strong accuracy.

So $\mathcal{P} \cong \mathcal{Q}$, $\mathcal{S} \cong \mathcal{W}$, $\Diamond\mathcal{P} \cong \Diamond\mathcal{Q}$ and $\Diamond\mathcal{S} \cong \Diamond\mathcal{W}$: the converse direction holds because strong completeness implies weak completeness. Only four classes are really different.

### What the classes solve

- **$\mathcal{S}$.** Consensus with any number $f < n$ of crashes.
- **$\Diamond\mathcal{S}$.** Consensus with $n > 2f$, by the [Chandra-Toueg algorithm](/chandra-toueg-consensus/). No algorithm with $\Diamond\mathcal{S}$, or even with $\Diamond\mathcal{P}$, tolerates $n \le 2f$.
- **$\Diamond\mathcal{W}$.** It is the [weakest failure detector for consensus](/weakest-failure-detector-consensus/) with $n > 2f$ (Chandra, Hadzilacos and Toueg, 1996). It is equivalent to the leader detector [$\Omega$](/omega-failure-detector/).

None of the eight classes can be built in the pure asynchronous model, since each of them lets consensus be solved there. A system that implements one must have some timing property. In the synchronous model, timeouts with the known bounds give $\mathcal{P}$. In the [partial synchrony](/partial-synchrony/) model, timeouts that grow after each mistake give $\Diamond\mathcal{P}$.

## Examples

- **Heartbeats with timeouts.** Each process sends a heartbeat at a fixed rate and suspects a peer whose heartbeat is late. With known bounds on message delay and on process speed, a fixed timeout is never wrong, so this is $\mathcal{P}$. With unknown bounds, a timeout that grows after each mistake gives $\Diamond\mathcal{P}$, as proved on the [eventually perfect failure detector](/eventually-perfect-failure-detector/) page.
- **A leader oracle.** $\Omega$ outputs one trusted process instead of a set of suspects. Chandra, Hadzilacos and Toueg allow such outputs, and $\Omega$ is equivalent to $\Diamond\mathcal{W}$.
- **Non-example: suspect everybody.** This module has strong completeness and no accuracy, so it is in none of the eight classes. With it, the Chandra-Toueg algorithm stays safe but may never decide.
- **Non-example: a fixed timeout in an asynchronous system.** If message delays have no bound, a fixed timeout can suspect the same correct process again and again, so it gives no eventual accuracy.

## Where it is used

- **Consensus and replication.** The [Chandra-Toueg algorithm](/chandra-toueg-consensus/) and leader based protocols such as [Paxos](/paxos/) and [Raft](/raft/) are safe in the asynchronous model and use a detector, often in the form of a leader with timeouts, only for liveness. [Total order broadcast](/total-order-broadcast/) is equivalent to consensus, so it needs the same detectors.
- **Proofs of what can be solved.** The question "what is the weakest failure detector for problem X" measures how much timing information X needs. For consensus with a majority of correct processes the answer is $\Omega$.
- **Practical monitoring.** Systems monitor their members with heartbeat schemes such as the [phi accrual detector](/phi-accrual-failure-detector/), [SWIM](/swim/) and other forms of [failure detection](/failure-detection/) by gossip. They choose a point in the trade off between fast detection of crashes and few false suspicions.

## References
