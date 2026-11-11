---
tag: NQ3YET
kind: problem
slug: byzantine-broadcast
name: Byzantine broadcast
aliases:
- Byzantine broadcast problem
- sender-based Byzantine agreement
- Byzantine generals problem
area: distributed/byzantine-agreement
level: core
summary: A designated sender sends one value, and all correct processes must output the same value, which is the sender's value whenever the sender is correct.
prereqs: [byzantine-failure-model, consensus-problem]
see_also: [interactive-consistency, oral-messages-algorithm, signed-messages-algorithm, dolev-strong-algorithm, byzantine-resilience-bound, authenticated-resilience-bound, byzantine-reliable-broadcast, phase-king-algorithm]
sources:
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine Generals Problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: Section 1 (the problem with conditions IC1 and IC2, page 383), Section 2 (impossibility for n <= 3m), Sections 3 and 4 (algorithms OM(m) and SM(m))
  - paper: doi:10.1145/322186.322188
    title: Marshall Pease, Robert Shostak and Leslie Lamport, Reaching Agreement in the Presence of Faults, Journal of the ACM 27(2), 1980
    locator: pages 228 to 234 (interactive consistency, of which broadcast is one entry)
  - paper: doi:10.1137/0212045
    title: Danny Dolev and H. Raymond Strong, Authenticated algorithms for Byzantine agreement, SIAM Journal on Computing 12(4), 1983
    locator: pages 656 to 666 (Byzantine agreement as broadcast from one sender, with signatures, in t + 1 phases)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 6, Sections 6.3 to 6.5 (Byzantine agreement in synchronous networks, the bound on processes and the connectivity bound)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 5, Section 5.2 (consensus with Byzantine failures in synchronous systems)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 3 (Byzantine consistent and reliable broadcast) and Chapter 5 (Byzantine consensus)
---

In Byzantine broadcast, one designated process, the sender, has a value, and every correct process must output a value. All correct processes must output the same value, and if the sender is correct, that value must be the sender's value. Some processes, perhaps the sender, are [Byzantine](/byzantine-failure-model/) and may lie in any way. Lamport, Shostak and Pease stated it in 1982 as the Byzantine generals problem, with a commanding general and his lieutenants. It is the basic primitive from which [interactive consistency](/interactive-consistency/) and Byzantine consensus are built, and it is the problem that the classic bounds of $n > 3t$ processes and $t + 1$ rounds were first proved for.

## In plain words

A general sends one order to his officers by messenger. Some of the officers are traitors, and the general may be a traitor too. The loyal officers must all act on the same order. If the general is loyal, that order must be the one he gave.

The difficulty is that a traitor general can send different orders to different officers, and a traitor officer can lie about what he was told. So an officer cannot simply act on the order he received. The loyal officers must talk among themselves until they agree, and the talk must be designed so that the traitors cannot split them.

## Definition

**Model.** There are $n$ processes on a network of reliable links, usually complete, in the [synchronous model](/synchronous-model/). One process $s$ is the *sender*. At most $t$ processes are Byzantine, and the others are *correct*. Messages are either oral, as in the [oral messages model](/oral-messages-model/), or signed, as in the [signed messages model](/signed-messages-model/).

**Problem.** The sender has an input $v$ from a set of values $V$. Each correct process must output a value in $V$ such that:

- **termination:** every correct process outputs a value;
- **agreement:** all correct processes output the same value;
- **validity:** if the sender is correct, every correct process outputs $v$.

In the words of Lamport, Shostak and Pease, with the commander as sender and the lieutenants as the other processes:

- **IC1.** All loyal lieutenants obey the same order.
- **IC2.** If the commanding general is loyal, then every loyal lieutenant obeys the order he sends.

IC1 is agreement and IC2 is validity. Termination is implicit in the 1982 paper, since the algorithms run for a fixed number of rounds. When the sender is faulty, validity asks nothing, so the correct processes may agree on any value, including a default such as RETREAT. A correct sender can output $v$ at once, so most formulations only constrain the other processes.

## Variants

- **[Interactive consistency](/interactive-consistency/).** Every process is a sender. The correct processes must agree on a vector of $n$ values whose entry for each correct process is its input.
- **Consensus.** Every process has an input, and the correct processes agree on one value. With [strong validity](/strong-validity/), if all correct processes have the same input, that is the decision. With [weak validity](/weak-validity/), only failure-free runs are constrained.
- **Reliable broadcast.** In the [asynchronous model](/asynchronous-model/) broadcast with termination is impossible, because a correct process cannot tell a silent sender from a slow one. [Byzantine reliable broadcast](/byzantine-reliable-broadcast/) weakens termination: if the sender is correct, all correct processes deliver, and if one correct process delivers, all do. [Bracha's algorithm](/bracha-reliable-broadcast/) solves it for $n > 3t$.
- **General networks.** On a network graph that is not complete, messages travel over paths with faulty relays, and the graph must have [vertex connectivity](/vertex-connectivity/) at least $2t + 1$.
- **Multivalued and binary.** The value set $V$ may be $\{0, 1\}$ or larger. For $n > 3t$, Turpin and Coan (1984) reduce multivalued agreement to binary agreement with two extra rounds.

## Examples

**One traitor among four, oral messages.** Let $n = 4$ and $t = 1$, with sender $s$ and processes $p_1, p_2, p_3$. Suppose $s$ is a traitor and sends 1, 1, 0. With [OM(1)](/oral-messages-algorithm/), each $p_i$ relays what it got to the other two, and takes the majority of the three values it now has. All three have the multiset $\{1, 1, 0\}$, so all output 1. Agreement holds, and validity asks nothing. If instead $p_3$ is the traitor and $s$ sends 1 to all, $p_1$ sees $\{1, 1, x\}$ and $p_2$ sees $\{1, 1, y\}$ for any lies $x$ and $y$, and both output 1.

**Three processes are not enough.** With $n = 3$ and $t = 1$, no algorithm works without signatures, by the [Byzantine resilience bound](/byzantine-resilience-bound/). A process that hears 1 from the sender and "the sender told me 0" from the third process cannot tell which of the two is lying.

**From broadcast to a vector.** The implementation runs $n$ instances of the [Dolev-Strong algorithm](/dolev-strong-algorithm/) in parallel, one per sender, and checks interactive consistency for $n = 3, 4, 5$ with $t = n - 2$, every set of at most $t$ faulty processes, and three attack strategies. All instances end after $t + 1$ rounds.

## Known algorithms

| Algorithm | Model | Faults | Rounds | Messages sent |
| --- | --- | --- | --- | --- |
| [OM(m)](/oral-messages-algorithm/), Lamport, Shostak and Pease 1982 | oral | $n > 3t$ | $t + 1$ | $O(n^{t+1})$ |
| [SM(m)](/signed-messages-algorithm/), Lamport, Shostak and Pease 1982 | signed | any $t < n$ | $t + 1$ | $O(n^2 d)$ for $d$ signed values |
| [Dolev-Strong](/dolev-strong-algorithm/), 1983 | signed | any $t < n$ | $t + 1$ | $O(n^2)$ |
| [Phase king](/phase-king-algorithm/), Berman, Garay and Perry 1989 | oral | $n > 3t$ | $O(t)$ | $O(n^2 t)$ |
| Garay and Moses 1998 | oral | $n > 3t$ | $t + 1$ | polynomial |

The phase king and [phase queen](/phase-queen-algorithm/) algorithms solve consensus, and they give broadcast by the reduction below. Randomized algorithms, such as those of [Rabin](/rabin-randomized-byzantine-agreement/) and [Feldman and Micali](/feldman-micali-byzantine-agreement/), solve consensus in an expected constant number of rounds for $n > 3t$.

## Bounds

- **Processes, oral messages.** For $3 \le n \le 3t$, broadcast is impossible. So $n \ge 3t + 1$ is necessary and enough. See the [Byzantine resilience bound](/byzantine-resilience-bound/).
- **Processes, signed messages.** Broadcast is solvable for any $t < n$. See the [authenticated resilience bound](/authenticated-resilience-bound/).
- **Rounds.** Every deterministic algorithm needs $t + 1$ rounds in some run when $t \le n - 2$, with or without signatures. See the [Byzantine round lower bound](/byzantine-round-lower-bound/).
- **Messages.** Every deterministic algorithm sends $\Omega(n + t^2)$ messages from correct processes in some run, and $\Omega(nt)$ signatures if it uses signatures. See the [Dolev-Reischuk lower bound](/dolev-reischuk-lower-bound/).
- **Connectivity.** On a general graph, vertex connectivity at least $2t + 1$ is needed, together with $n > 3t$ without signatures.

## Reductions

The three classic problems reduce to each other, but the conditions on $n$ differ. Each reduction below keeps the model, oral or signed.

1. **Broadcast to interactive consistency, for any $n$ and $t$.** Run $n$ broadcasts in parallel, with process $q$ as the sender of instance $q$. The vector of outputs satisfies interactive consistency. The rounds are the same.
2. **Interactive consistency to broadcast, for any $n$ and $t$.** Run interactive consistency with the sender's value as its input, and output entry $s$ of the vector.
3. **Interactive consistency to consensus with strong validity, for $n > 2t$.** Decide the strict majority of the vector, or a default if there is none. If all correct processes have input $v$, at least $n - t > n/2$ entries are $v$. For $n \le 2t$ no algorithm at all achieves strong validity.
4. **Broadcast to consensus with weak validity, for any $n$ and $t$.** Decide the output of the broadcast from process $p_0$, with its input as the value.
5. **Consensus with strong validity to broadcast, for any $n$ and $t$ where consensus is solvable.** In one extra round, the sender sends its value to everyone. Then all processes run consensus with the value they received as input, and a default if they received nothing. If the sender is correct, all correct processes have input $v$, and strong validity gives $v$.

So with oral messages and $n > 3t$, all three problems are equivalent. With signatures, broadcast and interactive consistency are solvable for every $t < n$, but consensus with strong validity only for $n > 2t$. The implementation checks reductions 1, 2, 3 and 5. For $n = 4$, $t = 2$, inputs $(0, 0, 1, 1)$ and processes 0 and 1 faulty but acting correctly, reduction 3 decides 0 at processes 2 and 3, although both have input 1. It also runs one case that separates the two validity conditions: with $n = 4$, $t = 1$, process 0 faulty with input 1 and all correct inputs 0, reduction 4 decides 1 and reduction 3 decides 0.

## Applications

- **Replicated control computers.** The problem came from the SIFT aircraft control computer, in which replicated processors had to agree on sensor readings even if a processor was faulty. Each reading is broadcast by its source.
- **Byzantine state machine replication.** [Byzantine fault tolerance](/byzantine-fault-tolerance/) systems order client requests with repeated consensus or broadcast. Synchronous designs use Dolev-Strong style broadcast, and [PBFT](/pbft/) and its successors use a leader that acts as a sender.
- **Secure multiparty computation.** Many protocols assume a broadcast channel, and Byzantine broadcast with signatures implements it for any number of corrupted parties.
- **Blockchains.** A block proposer acts as the sender of a broadcast, and validators must agree on its block or on none.

## References
