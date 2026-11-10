---
tag: PKPK26
kind: problem
slug: ring-leader-election
name: Leader election in a ring
aliases:
- Ring election
- Election on a ring
area: distributed/leader-election
level: intro
summary: Make exactly one process of a ring the leader. With distinct ids it costs Θ(n log n) messages for comparison-based algorithms; without ids no deterministic algorithm exists.
prereqs: [ring-network, asynchronous-model, synchronous-model, message-complexity]
see_also: [chang-roberts, hirschberg-sinclair, peterson-leader-election, franklin, ring-election-lower-bound, explicit-leader-election, anonymous-leader-election, complete-network-leader-election]
sources:
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 3 (leader election in a synchronous ring, Sections 3.1 to 3.7) and Chapter 15, Section 15.1 (leader election in an asynchronous ring)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 3 (the leader election problem, anonymous rings, asynchronous rings and synchronous rings)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 7 (election algorithms, Section 7.2 on rings)
  - paper: doi:10.1145/7531.7919
    title: Greg N. Frederickson and Nancy A. Lynch, Electing a leader in a synchronous ring, Journal of the ACM 34(1), 1987
    locator: pages 98 to 115 (the O(n) algorithm with integer identifiers and the comparison lower bound)
  - paper: doi:10.1145/1634.1889
    title: Jan Pachl, Ephraim Korach and Doron Rotem, Lower bounds for distributed maximum-finding algorithms, Journal of the ACM 31(4), 1984
    locator: pages 905 to 918 (average and worst case lower bounds on rings)
---

Leader election in a ring is the problem of making exactly one process of a [ring network](/ring-network/) the leader. With distinct identifiers it is solvable, and the best comparison-based algorithms send $\Theta(n \log n)$ messages, which is optimal by the [ring election lower bound](/ring-election-lower-bound/). Without identifiers no deterministic algorithm solves it, by [Angluin's theorem](/anonymous-ring-impossibility/). It is the standard first problem of distributed algorithms, because it is the simplest task that needs the processes to break their symmetry.

## In plain words

A group of computers is linked in a circle. Each can talk only to its two neighbours. They must choose one of them as the boss, and each must know the outcome: "I am the boss" or "I am not". Nobody is in charge at the start, so the choice must come from the computers talking to each other.

If each computer has a different name, they can choose the one with the largest name. The question is how many messages this costs. Sending every name all the way round works but costs a lot. Clever methods let only the strong candidates send far, and they need far fewer messages. If the computers have no names and all run the same program, they cannot choose at all, because nothing makes one of them different from the others.

## Definition

A ring of $n \ge 1$ processes runs the same algorithm at each process, except for an identifier $\mathrm{id}_i$ given as input. The identifiers are distinct elements of a totally ordered set $U$. Each process has a variable $\mathit{status}$ with values *unknown*, *leader* and *non-leader*, and the value *unknown* at the start. An algorithm solves **leader election** if in every admissible run, that is, every run in which each process takes steps and each message is delivered:

- **Uniqueness.** At no time do two processes have status *leader*, and a status that leaves *unknown* never changes again.
- **Election.** Eventually exactly one process has status *leader*.

The **full form** used by Attiya and Welch adds that every other process eventually has status *non-leader*. The **explicit form** also asks that every process learns $\mathrm{id}_\ell$ of the leader $\ell$; this is [explicit leader election](/explicit-leader-election/). A run may also have to *terminate*: each process eventually stops, and no message is left in transit.

The cost of an algorithm is its [message complexity](/message-complexity/), the largest number of messages over all runs on rings of size $n$, and its time: rounds in the synchronous model, or time units in the asynchronous model when each message takes at most one unit.

## Variants

- **Maximum finding.** The leader must be the process with the largest identifier. Most algorithms below solve this form. Pachl, Korach and Rotem call it distributed maximum finding.
- **Unidirectional or bidirectional, oriented or not.** The [ring network](/ring-network/) page lists these choices. An algorithm for unidirectional rings runs on oriented bidirectional rings.
- **Uniform or non-uniform.** In a uniform algorithm the processes do not know $n$.
- **Synchronous or asynchronous.** In the [synchronous model](/synchronous-model/) an algorithm can learn from the absence of a message, and this changes the bounds (see below).
- **Comparison based or not.** A comparison-based algorithm uses identifiers only by comparing them. A non-comparison algorithm may compute with them, for example wait a number of rounds that depends on the value.
- **Anonymous rings.** All processes are identical. This is the [anonymous leader election](/anonymous-leader-election/) problem, which needs randomization.

## Examples

- **Size 1.** The only process must become the leader. In the [Chang-Roberts algorithm](/chang-roberts/) its identifier goes round a ring of one link and returns at once.
- **Size 5.** Identifiers $3, 7, 1, 5, 2$ on a unidirectional ring. A maximum-finding algorithm must make the process with identifier 7 the leader and the other four processes *non-leader*. Chang-Roberts sends 11 election messages and 5 announcement messages here.
- **Not a solution.** Each process becomes leader if its identifier is larger than the identifiers of both neighbours. On the ring $3, 7, 1, 5, 2$ both 7 and 5 are local maxima, so two processes become leader. One round of local comparison does not solve the problem; the winners of such rounds must compete again, as in [Franklin's algorithm](/franklin/).

## Known algorithms

The message counts are worst cases for $n$ processes with all processes starting, with $\lg = \log_2$. The counts with an announcement include $n$ messages for it. Time is for the asynchronous model when each message takes at most one time unit.

| algorithm | ring | messages, worst case | time |
|---|---|---|---|
| Le Lann (1977) | unidirectional | $n^2$ | $O(n)$ |
| [Chang-Roberts](/chang-roberts/) (1979) | unidirectional | $n(n+1)/2 + n$; average $n H_n + n$ | $O(n)$ |
| [Hirschberg-Sinclair](/hirschberg-sinclair/) (1980) | bidirectional | at most $8n \lceil \lg n \rceil + 8n$ | $O(n)$ |
| [Franklin](/franklin/) (1982) | bidirectional, FIFO | at most $2n \lfloor \lg n \rfloor + 2n$ | $O(n \log n)$ |
| [Peterson](/peterson-leader-election/) (1982) | unidirectional, FIFO | at most $2n \lfloor \lg n \rfloor + n$ | $O(n \log n)$ |
| [Dolev-Klawe-Rodeh](/dolev-klawe-rodeh/) (1982) | unidirectional, FIFO | at most $2n \lfloor \lg n \rfloor + 2n$ | $O(n \log n)$ |
| TimeSlice (Lynch) | synchronous, $n$ known, positive integer identifiers | $n$ | $n \cdot \mathrm{id}_{\min}$ rounds |
| [Itai-Rodeh](/itai-rodeh/) (1981) | anonymous, unidirectional, $n$ known | $O(n \log n)$ expected | finite with probability 1 |

The time bounds $O(n \log n)$ for Franklin, Peterson and Dolev-Klawe-Rodeh are the simple bound of $O(n)$ time units for each of $O(\log n)$ phases. Peterson and Dolev, Klawe and Rodeh also give refined unidirectional versions with about $1.44\, n \lg n$ and $1.36\, n \lg n$ messages.

## Bounds

- **Upper bound.** $O(n \log n)$ messages and $O(n)$ time, on bidirectional rings by Hirschberg and Sinclair, and $O(n \log n)$ messages on unidirectional rings by Peterson and by Dolev, Klawe and Rodeh.
- **Lower bound, asynchronous.** Every algorithm for asynchronous bidirectional rings in which $n$ is unknown sends $\Omega(n \log n)$ messages in some run. Burns proved this in 1980, and Attiya and Welch give it in Section 3.3.3. See the [ring election lower bound](/ring-election-lower-bound/).
- **Lower bound, average.** On unidirectional rings every algorithm sends at least $n H_n$ messages on average over random orders of the identifiers (Pachl, Korach and Rotem). Chang-Roberts meets this bound exactly.
- **Lower bound, synchronous.** Every comparison-based algorithm on synchronous rings sends $\Omega(n \log n)$ messages in some run (Frederickson and Lynch). The same holds for any algorithm whose number of rounds is bounded by a function of $n$ alone, if the identifier set is large enough.
- **Synchronous with integer identifiers.** If identifiers are positive integers and the algorithm may compute with them, $n$ messages are enough when $n$ is known (TimeSlice) and $O(n)$ when it is not (Lynch's VariableSpeeds). The number of rounds then grows with the smallest identifier, without a bound in terms of $n$.
- **No identifiers.** No deterministic algorithm exists (Angluin). With random choices and known $n$, a [Las Vegas](/las-vegas-algorithm/) algorithm exists; with unknown $n$ no algorithm can be sure to terminate correctly.

## Reductions

- **Explicit from implicit.** After a leader is known, it sends its identifier once round the ring: $n$ more messages give the explicit form.
- **Maximum finding and election.** A maximum-finding algorithm is an election algorithm. In the other direction, a leader finds the maximum with one more trip round the ring, $n$ messages, in which each process replaces the carried value by the larger of it and its own identifier.
- **Election gives structure.** A leader can count $n$, orient a non-oriented ring, or compute any function of the inputs with $O(n)$ further messages, by one trip round the ring. So the $\Omega(n \log n)$ bound is the cost of breaking symmetry, not of the later computation.
- **Other topologies.** The same problem on a [complete network](/complete-network-leader-election/), on a [tree](/tree-leader-election/) and on a general graph has its own bounds: $\Theta(n \log n)$, $\Theta(n)$ and $O(m + n \log n)$ messages ([Awerbuch](/awerbuch-leader-election/), after [Gallager, Humblet and Spira](/gallager-humblet-spira/)).

## Applications

- **Recovering a ring.** In a token ring network a process must recreate a lost token, and an election makes sure that only one process does it.
- **Choosing a coordinator.** Many algorithms assume one initiator, for example a [convergecast](/convergecast/), a snapshot or [termination detection](/termination-detection/). An election chooses it.
- **Leader-based consensus.** [Paxos](/paxos/) and [Raft](/raft/) run with a leader, but they elect it under crashes and timing faults, with timeouts or an [Omega failure detector](/omega-failure-detector/), not with the failure-free algorithms of this page.

## References
