---
tag: AKDA5X
kind: algorithm
slug: chandra-toueg-consensus
name: Chandra-Toueg consensus algorithm
aliases:
- CT consensus
area: distributed/consensus
level: advanced
summary: Rotating-coordinator consensus using an eventually strong failure detector.
solves: [consensus-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of processes, f: the largest number of crashes}
  time: {best: Θ(1)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
prereqs: [failure-detector, consensus-properties]
see_also: [paxos, ben-or-consensus, omega-failure-detector, eventually-perfect-failure-detector, weakest-failure-detector-consensus, flp-impossibility, partial-synchrony, raft]
sources:
  - paper: doi:10.1145/226643.226647
    title: Tushar Deepak Chandra and Sam Toueg, Unreliable failure detectors for reliable distributed systems, Journal of the ACM 43(2), 1996
    locator: pages 225 to 267, Section 6.2 (the rotating coordinator algorithm with a failure detector in diamond-S and a majority of correct processes) and Section 6.3 (n > 2f is necessary with diamond-S)
  - paper: doi:10.1145/234533.234549
    title: Tushar Deepak Chandra, Vassos Hadzilacos and Sam Toueg, The weakest failure detector for solving consensus, Journal of the ACM 43(4), 1996
    locator: pages 685 to 722 (Omega, and so diamond-W, is the weakest failure detector for consensus with a majority of correct processes)
  - paper: doi:10.1145/3149.214121
    title: Michael J. Fischer, Nancy A. Lynch and Michael S. Paterson, Impossibility of distributed consensus with one faulty process, Journal of the ACM 32(2), 1985
    locator: pages 374 to 382 (the impossibility that a failure detector gets around)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 21, Section 21.4 (failure detectors and consensus in asynchronous networks)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luis Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 5 (consensus with failure detectors, and the rotating coordinator)
---

The Chandra-Toueg algorithm (1996) solves [consensus](/consensus-problem/) in the [asynchronous model](/asynchronous-model/) with $f$ [crash failures](/crash-failure/) and $n > 2f$, using a [failure detector](/failure-detector/) of class $\Diamond\mathcal{S}$. Processes go through rounds, and in each round one coordinator, chosen in turn, tries to make a majority adopt its proposal. Safety never depends on the failure detector: a timestamp on each estimate locks a value once it could be decided. The detector is used only for termination, so the algorithm shows how a weak oracle gets around the [FLP impossibility](/flp-impossibility/).

## In plain words

A group of computers must agree on one value. Messages can take any time, some computers may stop, and each computer has a helper that guesses which others have stopped. The guesses can be wrong for a long time.

The computers take turns as leader, one turn per round. In each round, everyone sends its current value to the leader. The leader picks the value that was accepted most recently, and sends it to all. Each computer accepts it, or gives up on the leader if its helper says that the leader has stopped. If more than half accept, the leader announces the decision.

A wrong guess can only waste a round. It can never cause two different decisions. Once the helpers stop doubting one working computer, its next turn as leader ends the run.

## The problem

There are $n$ processes on a complete network of reliable links. Process $p_i$ has an input $v_i$ from any set of values. At most $f$ processes crash, with $n > 2f$, and a crash can stop a process in the middle of a broadcast. Messages take any finite time and there are no clocks. Each process can query a local failure detector module, which outputs a set of processes that it suspects to have crashed. The class $\Diamond\mathcal{S}$ gives two guarantees:

- **Strong completeness.** Eventually, every crashed process is suspected by every correct process for ever.
- **Eventual weak accuracy.** There is a correct process $\ell$ and a time after which no correct process suspects $\ell$.

Before that time the detector can make any number of mistakes, and nobody knows when the time comes. The algorithm must give the [consensus properties](/consensus-properties/): uniform agreement (no two processes decide differently, also when one of them later crashes), validity (each decision is the input of some process), and termination (each correct process decides).

## The algorithm

The code of process $p_i$ is below. Round $r$ has the coordinator $c = (r \bmod n) + 1$ and four phases. Each process keeps an estimate $est$ and a timestamp $ts$, the last round in which it took $est$ from a coordinator. A majority is $\lceil (n+1)/2 \rceil$ processes. The decision is sent by a simple reliable broadcast: a process that gets $(\text{decide}, v)$ for the first time relays it to all others before it decides.

```pseudo id=main
CT-CONSENSUS(i, v_i)                                ▷ the code of p_i; n > 2f
L1  est ← v_i; ts ← 0; r ← 0
L2  while not decided do
L3      r ← r + 1; c ← (r mod n) + 1
L4      send (r, est, ts) to c                         ▷ phase 1
L5      if i = c then                                   ▷ phase 2
L6          wait for ⌈(n+1)/2⌉ estimates (r, e, t)
L7          send (r, the e with the largest t) to all
L8      wait for (r, v) from c or until c is suspected  ▷ phase 3
L9      if (r, v) arrived then est ← v; ts ← r; send (r, ack) to c
L10     else send (r, nack) to c
L11     if i = c then                                   ▷ phase 4
L12         wait for ⌈(n+1)/2⌉ replies (r, ack or nack)
L13         if all are acks then R-broadcast (decide, est)
L14 when R-deliver (decide, v): if not decided then decide v
```

Line L14 runs as a separate task, at any time. A process never suspects itself, so the coordinator always waits for its own proposal at line L8 and acks it. Lines L6 and L12 count messages from different senders.

## Example

Take $n = 3$, $f = 1$ and the inputs $v_1 = 0$, $v_2 = 1$, $v_3 = 0$. A majority is 2. Round 1 has the coordinator $p_2$, round 2 has $p_3$. No process crashes, but the detector of $p_1$ makes one mistake in round 1.

| round | phase | what happens | $(est, ts)$ after the phase |
|---|---|---|---|
| 1 | 1, 2 | $p_2$ gets $(1, 0)$ from itself and $(0, 0)$ from $p_3$; the timestamps tie, and it proposes 1 | $p_1$: $(0, 0)$, $p_2$: $(1, 0)$, $p_3$: $(0, 0)$ |
| 1 | 3 | $p_2$ and $p_3$ get the proposal and ack; $p_1$ wrongly suspects $p_2$ and sends nack | $p_1$: $(0, 0)$, $p_2$: $(1, 1)$, $p_3$: $(1, 1)$ |
| 1 | 4 | $p_2$ uses the replies of $p_1$ (nack) and $p_2$ (ack), so it does not decide | no change |
| 2 | 1, 2 | $p_3$ gets $(0, 0)$ from $p_1$ and $(1, 1)$ from itself; it proposes 1, the estimate with the largest timestamp | no change |
| 2 | 3 | all three get the proposal and ack | all $(1, 2)$ |
| 2 | 4 | $p_3$ gets two acks and R-broadcasts $(\text{decide}, 1)$; all decide 1 | |

The timestamp makes $p_3$ prefer 1 in round 2, although $p_1$ still holds 0. This is the rule that keeps a value safe once a majority has adopted it: if $p_2$ had seen the ack of $p_3$ first in round 1, it would have decided 1, and every later coordinator must then propose 1.

## Correctness

The full proof is below. It has three parts.

- **Locking.** If the coordinator of round $r$ sends $(\text{decide}, v)$, a majority $A$ acked in round $r$ and so holds $(v, r)$. Every later coordinator takes the estimate with the largest timestamp from a majority $B$, which meets $A$. By induction on the round, that timestamp is in $[r, r' - 1]$ and its estimate is $v$. So every later proposal, and so every decision, is $v$. The detector plays no part here, so agreement holds even if it is always wrong.
- **Validity.** Estimates start as inputs and change only to proposals, which are estimates. So every decision is an input.
- **Termination.** No correct process blocks: a coordinator waits for a majority, and the correct processes are a majority because $n > 2f$; a process waiting at line L8 for a crashed coordinator eventually suspects it, by strong completeness. After a time $T$ when all faulty processes have crashed and nobody suspects $\ell$, take the first round above every round reached at $T$ in which $\ell$ is the coordinator. All replies are acks, so $\ell$ decides, and the relay at line L14 reaches every correct process.

The bound $n > 2f$ is necessary with $\Diamond\mathcal{S}$, and even with $\Diamond\mathcal{P}$: Chandra and Toueg show that with $n \le 2f$ two halves of the processes can each suspect the other and decide alone before any mistake is noticed.

## Complexity

The costs are in asynchronous rounds and messages.

- **Rounds, best case.** If the coordinator of round 1 is correct and nobody suspects it, all processes decide in round 1.
- **Rounds after stabilization.** Once the detector has stopped suspecting $\ell$ and all faulty processes have crashed, the run ends at the next round with coordinator $\ell$, so within $n$ rounds of the slowest correct process. There is no bound on the number of rounds before that time, which is unknown.
- **Messages.** Each round sends $n$ estimates, $n$ proposals and $n$ replies, so $O(n)$ messages. The reliable broadcast of the decision costs $O(n^2)$ messages once per run.
- **Local space.** $O(n)$ for the messages of the current round, plus messages of later rounds that arrive early.

The table gives the round of the first decision over 100 seeded runs with $n$ processes, inputs $0, 1, 0, 1, \ldots$, no crash and a simulated $\Diamond\mathcal{S}$ that suspects each other process with probability $0.3$ at each step until step 200 of the simulation. After step 200 it never suspects one correct process chosen at random. The wrong suspicions make most rounds before step 200 fail, so the decision usually comes soon after the detector stabilizes.

| $n$ | mean round of the decision | largest round | mean number of wrong suspicions |
|---|---|---|---|
| 3 | 12.08 | 27 | 20.67 |
| 5 | 19.05 | 22 | 68.87 |
| 7 | 18.28 | 23 | 105.7 |

## Properties

- **Deterministic.** The algorithm uses no random choice. The failure detector is the only extra power.
- **Indulgent.** Agreement and validity hold in every run, whatever the detector outputs. Only termination needs the $\Diamond\mathcal{S}$ properties.
- **Optimal resilience for $\Diamond\mathcal{S}$.** It tolerates $f < n/2$ crashes, and no algorithm with $\Diamond\mathcal{S}$ tolerates more.
- **Multi-valued.** The values can come from any set, not only $\{0, 1\}$.
- **Uniform agreement.** A process that decides and then crashes decided the common value.

## Variants and improvements

- **Leader based version.** With an [$\Omega$ detector](/omega-failure-detector/), which outputs one trusted leader, the rotation is not needed: processes follow the current leader, and a round fails only while leaders differ. This is the structure of [Paxos](/paxos/), and $\Omega$ is equivalent to $\Diamond\mathcal{W}$, the [weakest failure detector for consensus](/weakest-failure-detector-consensus/).
- **Strong detector.** With a detector of class $\mathcal{S}$, which has perpetual weak accuracy, Chandra and Toueg give another algorithm that tolerates any $f < n$ crashes, with a fixed number of asynchronous rounds.
- **Timeouts as the detector.** In the [partial synchrony](/partial-synchrony/) model, heartbeats with growing timeouts build an [eventually perfect detector](/eventually-perfect-failure-detector/), which is stronger than $\Diamond\mathcal{S}$. So the algorithm runs in that model with no oracle.
- **Repeated consensus.** Running one instance per slot of a log gives [total order broadcast](/total-order-broadcast/), and so [state machine replication](/state-machine-replication/).

## When to use it

Use the Chandra-Toueg algorithm to teach consensus with failure detectors, or when a system already has a failure detection service and needs a single agreement with a majority of correct processes. For a long log of decisions, a leader based protocol such as [Multi-Paxos](/multi-paxos/) or [Raft](/raft/) is cheaper, because a stable leader skips the first two phases. For timing free settings with no detector, randomized protocols such as [Ben-Or's](/ben-or-consensus/) are the alternative.

## Pitfalls

- **Taking any estimate in phase 2.** The coordinator must take the estimate with the largest timestamp. If it takes, for example, the smallest value, a value that was decided in an earlier round can be replaced, and agreement breaks.
- **Deciding with a nack among the replies.** The coordinator decides only if all the replies in its majority are acks. A nack means that the sender did not adopt the proposal, so the majority that holds $(v, r)$ is not guaranteed.
- **Halting before the relay.** A process must relay the decision before it decides. If a coordinator decides and crashes in the middle of its broadcast, the relays are the only way the others learn the value.
- **Treating suspicion as a crash.** A suspected coordinator may be alive and may still send its proposal or a decision. The algorithm stays safe because it never acts on a suspicion except to skip a wait.
- **Waiting for all processes.** Lines L6 and L12 wait for a majority, not for $n$ messages. Waiting for all blocks for ever when one process crashes.

## Implementations

## History

Chandra and Toueg presented unreliable failure detectors at PODC 1991, and the journal version appeared in the Journal of the ACM in 1996. It defines eight classes of detectors by completeness and accuracy, and gives consensus algorithms for $\mathcal{S}$ and $\Diamond\mathcal{S}$. In the same year Chandra, Hadzilacos and Toueg proved that $\Diamond\mathcal{W}$ is the weakest failure detector for consensus, so the rotating coordinator algorithm uses the least information that any algorithm can use. Lamport's Paxos, written in 1989 and published in 1998, has the same locking idea with ballots in place of rotating rounds.

## References
