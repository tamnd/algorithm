---
tag: 1ADEFK
kind: theorem
slug: flp-impossibility
name: FLP impossibility theorem
aliases:
- Fischer-Lynch-Paterson impossibility
area: distributed/consensus
level: core
summary: No deterministic asynchronous consensus protocol tolerates even one crash failure.
prereqs: [consensus-properties, asynchronous-model, crash-failure]
see_also: [consensus-round-lower-bound, ben-or-consensus, partial-synchrony, failure-detector, chandra-toueg-consensus, consensus-number, k-set-agreement, paxos]
sources:
  - paper: doi:10.1145/3149.214121
    title: Michael J. Fischer, Nancy A. Lynch and Michael S. Paterson, Impossibility of distributed consensus with one faulty process, Journal of the ACM 32(2), 1985
    locator: pages 374 to 382; Section 2 (the model), Section 3 (Lemmas 1, 2 and 3 and Theorem 1), Section 4 (a protocol for initially dead processes)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 12 (the impossibility for asynchronous shared memory) and Chapter 21, Section 21.2 (the impossibility for asynchronous networks)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 5, Section 5.3 (impossibility in asynchronous systems)
  - paper: doi:10.1145/226643.226647
    title: Tushar Deepak Chandra and Sam Toueg, Unreliable failure detectors for reliable distributed systems, Journal of the ACM 43(2), 1996
    locator: pages 225 to 267 (consensus with failure detectors, a way around the theorem)
  - paper: doi:10.1145/42282.42283
    title: Cynthia Dwork, Nancy Lynch and Larry Stockmeyer, Consensus in the presence of partial synchrony, Journal of the ACM 35(2), 1988
    locator: pages 288 to 323 (consensus under partial synchrony, a way around the theorem)
  - paper: doi:10.1145/800221.806707
    title: Michael Ben-Or, Another advantage of free choice, Completely asynchronous agreement protocols, PODC 1983
    locator: pages 27 to 30 (randomized consensus, a way around the theorem)
---

The FLP theorem of Fischer, Lynch and Paterson (1985) says that in the [asynchronous model](/asynchronous-model/), no deterministic protocol solves [consensus](/consensus-problem/) if even one process may [crash](/crash-failure/). The links are reliable, and only the delays are unbounded, but that is enough: the adversary can always choose a next step that keeps the outcome open. The theorem does not rule out [randomized](/ben-or-consensus/) protocols, protocols with [failure detectors](/failure-detector/), or protocols for [partial synchrony](/partial-synchrony/), and these are the ways in which real systems reach consensus.

## Statement

**Model.** There are $n \ge 2$ processes. Each process is a deterministic state machine with a one-bit input and a write-once output in $\{b, 0, 1\}$, where $b$ means undecided. Processes talk through a message buffer. A *step* of process $p$ takes one message for $p$ out of the buffer, or the null message $\varnothing$, then changes the state of $p$ and sends finitely many messages. A step is an *event* $e = (p, m)$. Any order of events is allowed, and a message can stay in the buffer for any finite time. There are no clocks.

**Correctness.** A protocol is *partially correct* if no reachable configuration has two different decision values ([agreement](/consensus-properties/)), and each value 0 and 1 is the decision of some reachable configuration (a weak validity, which rules out the protocol that always decides 0). A run is *admissible* if at most one process takes only finitely many steps (it is *faulty*), and each message sent to a nonfaulty process is received in the end. A protocol is *totally correct in spite of one fault* if it is partially correct and in each admissible run *some* process decides.

**Theorem 1 (Fischer, Lynch and Paterson).** No consensus protocol is totally correct in spite of one fault.

Each part of the definition is weak: one crash only, reliable links, no Byzantine behavior, and only one process must decide. So the theorem also holds for each stronger form of the [consensus properties](/consensus-properties/), for any number $f \ge 1$ of crashes, and for multi-valued consensus.

## In plain words

Some computers must agree on one bit. Messages always arrive, but they can take any time, and there are no clocks. One computer may stop. Then a slow computer and a stopped one look the same: a computer cannot wait for everyone, because it may wait for ever.

The proof shows that the adversary, who picks the order of messages, can keep the outcome open for ever. At the start, there is a setting of inputs where both outcomes are still possible. From such an open state, whatever message is next in line, the adversary can deliver it at a moment where the outcome stays open. Doing this again and again gives a run where every computer keeps working and every message arrives, but nobody ever decides.

## Proof

The full proof, with every step, is below. This section gives the three lemmas and the main argument. Assume a protocol $P$ that is totally correct in spite of one fault.

**Valence.** For a configuration $C$, let $V(C)$ be the set of decision values of configurations reachable from $C$. $C$ is *bivalent* if $V(C) = \{0, 1\}$, and *0-valent* or *1-valent* if $V(C)$ is $\{0\}$ or $\{1\}$. Total correctness makes $V(C)$ nonempty. A configuration in which some process has decided $v$ is $v$-valent, because outputs are write-once and partial correctness forbids a second value. So in a bivalent configuration no process has decided.

**Lemma 1 (commutativity).** If schedules $\sigma_1$ and $\sigma_2$ are applicable to $C$ and no process takes steps in both, then $\sigma_1(\sigma_2(C)) = \sigma_2(\sigma_1(C))$.

*Proof sketch.* A step of $p$ reads and changes only the state of $p$, removes only a message for $p$, and adds messages to the buffer. So neither schedule changes what the other one sees, and the final buffer is the same multiset in both orders. $\square$

**Lemma 2 (a bivalent start).** $P$ has a bivalent initial configuration.

*Proof.* If not, validity gives a 0-valent and a 1-valent initial configuration. Change the inputs one at a time from one to the other: some 0-valent $C_0$ and 1-valent $C_1$ differ only in the input of one process $p$. Take an admissible run from $C_0$ in which $p$ takes no step. It decides, say $v$, after a finite schedule $\sigma$. The same $\sigma$ runs from $C_1$, and every process other than $p$ goes through the same states, so it decides $v$ from $C_1$ too. Then $v = 0$ and $v = 1$, a contradiction. $\square$

**Lemma 3 (a step that keeps bivalence).** Let $C$ be bivalent and let $e = (p, m)$ be applicable to $C$. Let $\mathcal{C}$ be the configurations reachable from $C$ without the event $e$, and $\mathcal{D} = e(\mathcal{C})$. Then $\mathcal{D}$ contains a bivalent configuration.

*Proof.* Assume that all of $\mathcal{D}$ is univalent. $e$ stays applicable in $\mathcal{C}$, because only $e$ can remove $m$. Since $C$ is bivalent, $\mathcal{D}$ holds a 0-valent and a 1-valent configuration. Walk in $\mathcal{C}$ from $C$ to a configuration where the valence of $e(\cdot)$ is the other one: two neighbours $C_0$ and $C_1 = e'(C_0)$ in $\mathcal{C}$, with $e' = (p', m')$, give a 0-valent $D_0 = e(C_0)$ and a 1-valent $D_1 = e(C_1)$.

- If $p' \ne p$, Lemma 1 gives $D_1 = e'(D_0)$. A configuration reachable from a 0-valent one cannot be 1-valent.
- If $p' = p$, take a deciding run from $C_0$ in which $p$ takes no step, with schedule $\sigma$ and end $A = \sigma(C_0)$. By Lemma 1, $e(A) = \sigma(D_0)$ is 0-valent and $e(e'(A)) = \sigma(D_1)$ is 1-valent. Both are reachable from $A$, so $A$ is bivalent. But a process has decided in $A$, so $A$ is univalent.

Both cases are contradictions. $\square$

**The theorem.** Build a run in stages. Keep the processes in a queue, and in each stage let $p$ be the head of the queue and $m$ the oldest message for $p$, or $\varnothing$. Start from the bivalent configuration of Lemma 2. In each stage, Lemma 3 gives a schedule that ends with the event $(p, m)$ and leads to a bivalent configuration. Then move $p$ to the back of the queue. Each process takes infinitely many steps and each message is received, so the run is admissible, with no faulty process at all. Every stage ends bivalent, so nobody ever decides. This contradicts total correctness. $\blacksquare$

**What a program can and cannot show.** The theorem is about every protocol, and a program can only explore one protocol on a small $n$. For $n = 3$ and binary inputs, a search over all schedules with at most one crash gives these results:

- *Protocol A* waits for $n - 1$ values, its own included, and decides the majority, with ties to 0. With inputs $(1, 1, 0)$, the message of $p_1$ reaches $p_2$ and $p_3$ first. Then $p_2$ sees $\{1, 1\}$ and decides 1, and $p_3$ sees $\{0, 1\}$ and decides 0. No crash is needed. The initial configuration $(1, 1, 0)$ is bivalent.
- *Protocol B* waits for all $n$ values and decides the majority. It never disagrees, and it decides in every run without a crash. All its initial configurations are univalent, so by the argument of Lemma 2 one silent process must block it. With inputs $(1, 1, 0)$, $p_1$ and $p_2$ exchange values, then $p_3$ crashes before it sends anything, and $p_1$ and $p_2$ wait for ever.
- *Protocol C* lets $p_1$ decide its own input, and the others wait for the value of $p_1$. A crash of $p_1$ blocks it, also when $p_1$ crashes in the middle of its broadcast, after it has sent to $p_2$ but before it sends to $p_3$.

In the blocked runs, the same steps without the crash form the start of a run with no fault, in which the message of the "crashed" process is only slow. The processes that wait are in the same states in both runs. This is the reason why a timeout cannot help.

## Consequences

The theorem rules out deterministic protocols that are always safe and always live in the asynchronous model. Each way around it gives up one assumption.

- **Randomization.** [Ben-Or's algorithm](/ben-or-consensus/) (1983) uses coin flips. It is always safe, and it terminates with probability 1 when $n > 2f$. The adversary can still delay it, but only on a set of runs of probability 0.
- **Partial synchrony.** Dwork, Lynch and Stockmeyer (1988) show that consensus is solvable with $n > 2f$ crashes if the timing bounds hold after an unknown time, the model of [partial synchrony](/partial-synchrony/). The protocols are always safe, and they decide after the system becomes stable.
- **Failure detectors.** Chandra and Toueg (1996) add an oracle that suspects processes. With the [eventually strong detector](/failure-detector/) $\Diamond\mathcal{S}$ and $n > 2f$, the [Chandra-Toueg algorithm](/chandra-toueg-consensus/) solves consensus. The [weakest such detector](/weakest-failure-detector-consensus/) is [Ω](/omega-failure-detector/).
- **Safety always, liveness when lucky.** [Paxos](/paxos/) and [Raft](/raft/) never break agreement, and they decide when the network behaves well for long enough. FLP says that no protocol can also guarantee termination in every admissible run.
- **Weaker problems.** [Approximate agreement](/approximate-agreement/) is solvable in the asynchronous model with crashes, and [$k$-set agreement](/k-set-agreement/) is solvable when $k > f$. Set agreement with $k \le f$ is impossible, by a topological proof that extends FLP.
- **Shared memory.** The same kind of argument shows that read and write registers cannot solve wait-free consensus for two processes, so [registers have consensus number one](/registers-have-consensus-number-one/). Herlihy's [consensus numbers](/consensus-number/) rank shared objects by this power.
- **No timeout fixes it.** The proof uses only the fact that a crashed process and a slow process look the same. Any detector built from local clocks in an asynchronous system makes mistakes, and a protocol must be safe in spite of them.

## Tightness

- **Zero faults.** With no crash, consensus is easy in the asynchronous model: each process sends its input to all, waits for all $n$ inputs, and decides by a fixed rule. Protocol B above does this. So one crash is the exact threshold.
- **Initially dead processes.** FLP also give a protocol, in Section 4 of the paper, that solves consensus when a majority of the processes are correct and the faulty processes are dead from the start, taking no step at all. So the problem is a crash *during* the run.
- **Synchrony.** In the [synchronous model](/synchronous-model/), [FloodSet](/floodset/) solves consensus with any $f < n$ crashes in $f + 1$ rounds, and the [round lower bound](/consensus-round-lower-bound/) shows that this is exact. The same bivalence method gives the round bound there.

## History

Fischer, Lynch and Paterson presented the result at the ACM Symposium on Principles of Database Systems in 1983, motivated by the transaction commit problem, and published the journal version in 1985. It got the first PODC Influential Paper Award, now the Dijkstra Prize, in 2001. Ben-Or showed in 1983 that randomization gets around it. Dolev, Dwork and Stockmeyer (1987) mapped which mixes of synchrony make consensus possible, and Dwork, Lynch and Stockmeyer (1988) introduced partial synchrony. Loui and Abu-Amara (1987) proved the shared memory form, and Herlihy (1991) built the hierarchy of consensus numbers on it. Chandra and Toueg (1996) introduced failure detectors, and Chandra, Hadzilacos and Toueg (1996) showed that Ω is the weakest one for consensus. Aguilera and Toueg (1999) used the same bivalence method to give a short proof of the synchronous round lower bound.

## References
