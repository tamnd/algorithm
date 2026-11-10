---
tag: DFYQ3T
kind: theorem
slug: anonymous-ring-impossibility
name: Angluin's impossibility theorem for anonymous rings
aliases:
- Anonymous ring impossibility
- Impossibility of election with identical processes
area: distributed/leader-election
level: advanced
summary: No deterministic algorithm elects a leader on a ring of n ≥ 2 identical processes, even if n is known. The proof shows that all processes stay in the same state.
prereqs: [anonymous-network, ring-network, synchronous-model, asynchronous-model]
see_also: [anonymous-leader-election, itai-rodeh, ring-leader-election, port-numbering, las-vegas-algorithm, chang-roberts, ring-election-lower-bound]
sources:
  - paper: doi:10.1145/800141.804655
    title: Dana Angluin, Local and global properties in networks of processors, Proceedings of the 12th ACM Symposium on Theory of Computing, 1980
    locator: pages 82 to 93 (no election in networks of identical processes that have a symmetric covering)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 3, Section 3.2 (Theorem 3.1, impossibility for identical processes on a synchronous ring, proved by induction on rounds)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 3, Section 3.2 (there is no nonuniform anonymous leader election algorithm for synchronous rings, and hence none for asynchronous rings)
  - paper: doi:10.1016/0890-5401(90)90004-2
    title: Alon Itai and Michael Rodeh, Symmetry breaking in distributed networks, Information and Computation 88(1), 1990
    locator: pages 60 to 87 (randomized election on anonymous rings as the way round the theorem)
---

On a [ring](/ring-network/) of $n \ge 2$ processes that are all the same, with no identifiers, no deterministic algorithm can elect a leader. This holds even when every process knows $n$, and in both the [synchronous](/synchronous-model/) and the [asynchronous](/asynchronous-model/) model. The reason is symmetry: all processes start in the same state and see the same things, so they stay in the same state for ever, and if one of them becomes the leader, all of them do. The result goes back to Angluin's 1980 paper on [anonymous networks](/anonymous-network/).

## Statement

**Theorem.** Let $n \ge 2$, and let $A$ be a deterministic algorithm for a ring of $n$ processes in which all processes have the same state machine and the same initial state; $A$ may depend on $n$. Then:

1. In the synchronous model on an oriented ring, after every round of the run of $A$ all processes are in the same state. So $A$ does not solve leader election: either no process ever becomes the leader, or all $n$ processes become leaders in the same round.
2. In the asynchronous model, unidirectional or bidirectional, with FIFO channels or not, $A$ does not solve leader election either.

The ring of part 1 is oriented: for each $i$, the right port of $p_i$ leads to $p_{i+1}$. On a non-oriented ring the algorithm must work for every labelling of the ports, so it must also work for the oriented one, and the theorem applies. A unidirectional ring is a special case in which the left messages are always empty.

## In plain words

Picture people in a circle who all look the same, all follow exactly the same instructions, and have no names. Each one can tell their left hand from their right hand, and so can everyone else, in the same way.

At the start they are all in the same position. In each step each person does the same thing, so each person gets the same thing from their left neighbour and the same thing from their right neighbour. So after the step they are still all alike.

This never changes. If the instructions ever say "now you are the leader", they say it to everyone at once. So a set of instructions that picks exactly one leader does not exist. Coins, names, or something else that differs between people is needed.

## Proof

Let the processes be $p_0, \ldots, p_{n-1}$, indices modulo $n$. A deterministic process is given by a set of states, an initial state $s_0$, a message function $\mathit{msg}(s) = (\ell, r)$ that gives the message sent to the left and to the right in state $s$ (or nothing), and a transition function $\delta(s, a, b)$ that gives the next state after receiving $a$ on the left port and $b$ on the right port. A status *leader* is a property of the state.

**Part 1, the synchronous ring.** In round $k$ of the run, every process computes its two messages from its state, all messages are delivered, and every process applies $\delta$. Let $s_i^{(k)}$ be the state of $p_i$ after $k$ rounds.

*Claim.* For every $k \ge 0$, $s_0^{(k)} = s_1^{(k)} = \cdots = s_{n-1}^{(k)}$.

*Induction on $k$.* For $k = 0$ every process is in $s_0$, because the processes have the same initial state; this holds even if $s_0$ depends on $n$, because $n$ is the same for all.

Suppose all processes are in the same state $s$ after round $k - 1$. In round $k$ each $p_i$ sends $\mathit{msg}(s) = (\ell, r)$: $\ell$ on its left port and $r$ on its right port. Because the ring is oriented, the left port of $p_i$ is joined to the right port of $p_{i-1}$, so $p_i$ receives on its left port the right message of $p_{i-1}$, which is $r$. In the same way $p_i$ receives $\ell$ on its right port. So every process applies $\delta(s, r, \ell)$, and every process has the same state after round $k$. This proves the claim.

Now suppose $A$ solves leader election. Then in the synchronous run some process $p_j$ is in a leader state after some round $k$. By the claim every process is in the same state after round $k$, so all $n \ge 2$ processes are leaders. This breaks the uniqueness condition. If no process ever becomes the leader, the election condition is broken. Either way $A$ does not solve the problem. $\square$

**Part 2, the asynchronous ring.** An algorithm for the asynchronous model must work in every fair run. It is enough to give one fair run in which all processes stay in the same state. The idea is that the synchronous run of Part 1 can be carried out as an asynchronous run. Here is the run, in phases.

- In phase 0, each process sends its initial messages.
- In phase $k \ge 1$, the processes take steps one after another, $p_0$ first, then $p_1$, and so on. When $p_i$ takes its step, it receives the messages that were in its input channels at the start of the phase, and then sends its new messages. A message sent in phase $k$ is delivered in phase $k + 1$, even if its receiver takes its step later in phase $k$.

Every message is delivered one phase after it is sent, and every process takes a step in every phase, so the run is fair. It also respects FIFO, because each channel delivers its messages in the order they were sent.

*Claim.* At the start of each phase $k \ge 1$ all processes are in the same state, each left input channel holds the same sequence of messages, and each right input channel holds the same sequence of messages.

*Induction on $k$.* For $k = 1$ all processes are in $s_0$, and every left channel holds the right message of $s_0$, and every right channel holds the left message of $s_0$. Suppose the claim holds at the start of phase $k$, with common state $s$ and common channel contents. In phase $k$ each process, whenever its turn comes, starts in $s$ and receives the same messages on the same ports, since the messages sent earlier in the same phase are not delivered until phase $k + 1$. So each process goes through the same sequence of states and sends the same sequence of messages on each port. At the start of phase $k + 1$ the processes are therefore in the same state, and by orientation each left channel holds the right messages of a neighbour, which are the same for all. This proves the claim.

In this run, after each step of $p_{n-1}$ in a phase, all processes are in the same state. If any process were the leader at some point, then by the end of the same phase all processes would be leaders; if none ever is, the run elects nobody. In either case $A$ does not solve leader election in the asynchronous model. Leaders in this model are permanent, so being a leader at the end of the phase is enough. The same run is a valid run of a unidirectional ring, with no left messages, and of a non-oriented ring with the oriented labelling. $\blacksquare$

The two parts show why the synchronous case is enough: an asynchronous algorithm would also have to be correct on the particular run that copies the synchronous one, and there it fails. The tests run random deterministic programs on rings of size 1 to 8 and check that all states are equal after every round of both schedules, and that a [Chang-Roberts](/chang-roberts/) style program with equal identifiers declares all $n$ processes leaders in round $n$.

## Consequences

- **Identifiers or randomness are needed.** Election on rings needs something that breaks the symmetry: distinct identifiers, as in the [ring election problem](/ring-leader-election/), or random choices, as in the [Itai-Rodeh algorithm](/itai-rodeh/).
- **Other networks.** The same induction works on any [anonymous network](/anonymous-network/) with a port-preserving automorphism that moves the process that would be the leader. If every process is moved by some such automorphism, deterministic election is impossible. Yamashita and Kameda give the exact condition in terms of views.
- **Other tasks.** Any task whose output must differ between two processes that a symmetry maps to each other is impossible in the same way. For example, an oriented anonymous ring cannot deterministically compute a proper colouring with two colours of its processes, or choose a maximal independent set.
- **No help from knowledge.** Knowing $n$, or even the whole ring, does not help, because the argument does not depend on what the processes know.

## Tightness

- **One process.** For $n = 1$ the only process can elect itself, so $n \ge 2$ is needed.
- **Randomization.** With coin flips and known $n$, the [Itai-Rodeh algorithm](/itai-rodeh/) elects a leader with probability 1 and is always correct when it ends. With coin flips and unknown $n$, no algorithm both ends for sure and is always correct; see [leader election in anonymous networks](/anonymous-leader-election/).
- **Asymmetric port labels.** On a non-oriented ring the port labels of a given ring may break the symmetry; for example, a ring of size 3 in which exactly one process has its ports swapped. The theorem only says that no algorithm works for every labelling, and in particular for the oriented one.
- **Inputs.** If even one process has a different input, the symmetry is broken and election becomes possible.

## History

Angluin proved the impossibility in 1980, in a more general form that uses coverings of networks: if one network covers another, a run on the smaller one lifts to the larger, and processes over the same process behave alike. The ring case with the induction on rounds is Theorem 3.1 in Lynch's 1996 book and is in Chapter 3 of Attiya and Welch, who also derive the asynchronous case from the synchronous one. Itai and Rodeh studied in 1981 how randomization gets round the result.

## References
