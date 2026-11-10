---
tag: 7PASGV
kind: theorem
slug: weakest-failure-detector-consensus
name: Weakest failure detector for consensus
aliases:
- Omega is weakest
area: distributed/consensus
level: research
summary: Omega is the weakest failure detector that solves consensus.
prereqs: [omega-failure-detector, chandra-toueg-consensus]
see_also: [failure-detector, eventually-perfect-failure-detector, flp-impossibility, paxos, total-order-broadcast, consensus-problem, partial-synchrony, consensus-number]
sources:
  - paper: doi:10.1145/234533.234549
    title: Tushar Deepak Chandra, Vassos Hadzilacos and Sam Toueg, The weakest failure detector for solving consensus, Journal of the ACM 43(4), 1996
    locator: pages 685 to 722 (the definition of Omega, the extraction of Omega from any failure detector that solves consensus by the DAG of samples and the simulation forest, and the corollary that diamond-W is the weakest failure detector for consensus with a majority of correct processes)
  - paper: doi:10.1145/226643.226647
    title: Tushar Deepak Chandra and Sam Toueg, Unreliable failure detectors for reliable distributed systems, Journal of the ACM 43(2), 1996
    locator: pages 225 to 267 (consensus with diamond-S and n > 2f, which gives the sufficiency part, and the need for a majority with diamond-P)
  - paper: doi:10.1145/1734213.1734216
    title: Carole Delporte-Gallet, Hugues Fauconnier and Rachid Guerraoui, Tight failure detection bounds on atomic object implementations, Journal of the ACM 57(4), 2010
    locator: Article 22 (the quorum detector Sigma is the weakest for registers, and Omega together with Sigma is the weakest for consensus with any number of crashes)
  - paper: "Francis C. Chu, Reducing Ω to ◊W, Information Processing Letters 67(6), 1998"
    locator: the direct reduction from diamond-W to Omega
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luis Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 2 (the eventual leader detector Omega) and Chapter 5 (consensus with Omega)
---

The theorem of Chandra, Hadzilacos and Toueg (1996) says that the leader detector [$\Omega$](/omega-failure-detector/) is the weakest [failure detector](/failure-detector/) with which [consensus](/consensus-problem/) can be solved in the [asynchronous model](/asynchronous-model/) when a majority of processes is correct. Any detector that solves consensus can be used to build $\Omega$, and $\Omega$ is enough to solve consensus. So the eventual agreement on one correct leader is exactly the information about failures that consensus needs, and the [Chandra-Toueg algorithm](/chandra-toueg-consensus/) and [Paxos](/paxos/) use no more than necessary.

## Statement

**Model.** There are $n$ processes in the asynchronous model with reliable links. Up to $f$ processes may crash. A *failure detector* $\mathcal{D}$ maps each failure pattern to a set of allowed histories of outputs, as on the [failure detector](/failure-detector/) page; outputs may be arbitrary values, not only sets of suspects. A detector $\mathcal{D}'$ is *reducible* to $\mathcal{D}$, written $\mathcal{D}' \preceq \mathcal{D}$, if some algorithm that uses $\mathcal{D}$ and messages builds at each process an output that is a valid history of $\mathcal{D}'$ in every run. $\mathcal{D}$ *solves consensus* if some algorithm that uses $\mathcal{D}$ has uniform agreement, validity and termination in every run.

**$\Omega$.** The output of $\Omega$ at each process is a process, and there is a time after which all correct processes output the same correct process for ever.

**Theorem (Chandra, Hadzilacos and Toueg).**

1. *Necessity.* If a failure detector $\mathcal{D}$ solves consensus, then $\Omega \preceq \mathcal{D}$.
2. *Sufficiency.* If $n > 2f$, then $\Omega$ solves consensus.

So for $n > 2f$, $\Omega$ is the weakest failure detector that solves consensus. Since $\Omega$ is equivalent to $\Diamond\mathcal{W}$ and to $\Diamond\mathcal{S}$, these classes are weakest too. CHT state the necessity part for $\Diamond\mathcal{W}$ and prove it by building $\Omega$.

**Without a majority (Delporte-Gallet, Fauconnier and Guerraoui, 2010).** Let $\Sigma$ be the quorum detector: each output is a set of processes, any two outputs, at any processes and times, intersect, and eventually every output has only correct processes. Then for every $f < n$, $\Omega \times \Sigma$ is the weakest failure detector that solves consensus.

## In plain words

Some helpers that guess which computers have stopped are good enough to let a group agree, and some are not. The question is how little a helper can say and still be good enough.

The answer, when more than half the computers keep working, is: the helper only has to name one leader, and from some point on name the same working leader at every working computer. Anything less fails.

The proof shows more. Take any helper at all with which some method lets the group agree. Then the computers can use that helper to produce such a leader. So every helper that works hides a leader inside it.

## Proof

The sufficiency part is the Chandra-Toueg algorithm with $\Diamond\mathcal{S}$, together with the reduction from $\Omega$ to $\Diamond\mathcal{S}$, both proved on their pages. The necessity part is long. What follows is a **sketch** of it, which gives the structure of the argument and the reason why each step works, but not the full detail of CHT.

Fix an algorithm $A$ that solves consensus with $\mathcal{D}$. The task is an algorithm $T$ in which every process uses its module of $\mathcal{D}$ and sends messages, and outputs a leader such that eventually all correct processes output the same correct process.

**Step 1, a DAG of samples.** In $T$, each process $p$ queries its module of $\mathcal{D}$ again and again. Each answer becomes a vertex $[p, d, k]$: the $k$-th query of $p$ returned $d$. Process $p$ adds an edge to the new vertex from every vertex it already knows, and sends its whole graph to all, again and again; on receipt, it takes the union. The graph $G_p$ of each correct process grows for ever, and all correct processes converge to the same infinite limit DAG $G$. A path in $G$ is a sequence of queries, in an order that is consistent with real time, with outputs that $\mathcal{D}$ really gave in this run. Every correct process has infinitely many vertices in $G$, and every crashed process has finitely many.

**Step 2, a simulation forest.** Let $I_0, \ldots, I_n$ be the initial configurations of $A$ in which processes $p_1, \ldots, p_i$ have input 1 and the others have input 0. For each $I_i$, $p$ builds a tree of runs of $A$: a path from the root applies steps of $A$ in which each step of process $q$ takes its failure detector value from the next vertex of $q$ along a path in $G_p$, and delivers some message or none. Each finite path of the tree is a prefix of a run of $A$ that could really happen with $\mathcal{D}$ in the current failure pattern, because the detector values are real outputs, given in an order consistent with time. Process $p$ cannot run $A$ for real here; it only simulates these runs locally.

**Step 3, valence.** Tag each vertex of the forest by the decisions that appear in its subtree: 0-valent, 1-valent or bivalent. Since $A$ terminates in every run with $\mathcal{D}$, every long enough path of the limit forest in which the correct processes take enough steps reaches a decision. Since $A$ has validity, $I_0$ is 0-valent and $I_n$ is 1-valent. So either some root $I_i$ is bivalent, or for some $i$ the root $I_{i-1}$ is 0-valent and $I_i$ is 1-valent. In the second case, $I_{i-1}$ and $I_i$ differ only in the input of $p_i$, and $p_i$ must be correct: in runs where $p_i$ crashes before its first step, the other processes cannot tell the two roots apart and would decide the same value from both.

**Step 4, decision gadgets.** In a bivalent tree, CHT show that there is a *decision gadget*: a vertex with a 0-valent and a 1-valent descendant that differ in the step of one process. A *fork* has two children made by two different steps of the same process $q$. A *hook* has the step of one process $q$ before or after the step of another process, and the two orders lead to different valences. Each gadget has a *deciding process* $q$. The key lemma, as in the proof of [FLP](/flp-impossibility/), is that the deciding process of a gadget in the limit forest is correct. If $q$ crashed, there is a deciding path in which $q$ takes no more steps, and it can be continued from both sides of the gadget, giving one run that has both a 0-decision and a 1-decision, which contradicts agreement.

**Step 5, the output.** Order the gadgets of the limit forest in a fixed way, for example by depth and then by identifiers. Each correct process outputs the deciding process of the first gadget in its current finite forest, or the process $p_i$ of the critical index of step 3. As $G_p$ grows, the valences of the finitely many vertices that come before the first gadget of the limit forest become fixed, so each correct process eventually outputs the same deciding process for ever. By step 4 that process is correct, so the outputs form a history of $\Omega$.

The difficult part that this sketch leaves out is step 5: a finite part of the forest gives only a guess of the valences, and CHT show that the guesses of the correct processes converge for the gadget that matters. $\blacksquare$

## Consequences

- **Minimal information.** The Chandra-Toueg algorithm with $\Diamond\mathcal{S}$, and leader based protocols with $\Omega$, such as [Paxos](/paxos/), use the least information about failures that any consensus algorithm can use when $n > 2f$.
- **What a system must provide.** A system that solves consensus with $n > 2f$ must have enough timing to build $\Omega$. In practice this means some form of eventual timeliness, as in [partial synchrony](/partial-synchrony/). In the pure asynchronous model $\Omega$ cannot be built, and FLP follows again.
- **Problems equivalent to consensus.** [Total order broadcast](/total-order-broadcast/) and state machine replication can be reduced to consensus and back, so $\Omega$ is the weakest detector for them too when $n > 2f$.
- **A method.** The question "what is the weakest failure detector for problem X" became a standard way to measure how much synchrony a problem needs. For atomic registers the answer is $\Sigma$, and for consensus without a majority it is $\Omega \times \Sigma$.
- **The eight classes.** Among the classes of Chandra and Toueg, $\Diamond\mathcal{W}$ and the equivalent $\Diamond\mathcal{S}$ are exactly as strong as needed for consensus with $n > 2f$; $\Diamond\mathcal{P}$, $\mathcal{S}$ and $\mathcal{P}$ are stronger than needed.

## Tightness

The majority condition in the sufficiency part cannot be dropped. With $n \le 2f$, even $\Diamond\mathcal{P}$, which is stronger than $\Omega$, does not solve consensus (Chandra and Toueg, 1996): the processes can split into two groups of at most $f$, each group can wrongly suspect the other for a long time, and each group must then decide alone, possibly on different values. So with $n \le 2f$, $\Omega$ is still necessary but no longer sufficient, and the extra information needed is the quorum detector $\Sigma$. When $n > 2f$, $\Sigma$ can be built with no detector at all, by outputting the set of the first majority of processes that answered, which is why $\Omega$ alone is enough there.

The necessity part is tight in the other direction too: no detector strictly weaker than $\Omega$ solves consensus, since every detector that does gives $\Omega$.

## History

Chandra and Toueg presented unreliable failure detectors at PODC 1991 and showed that $\Diamond\mathcal{W}$ solves consensus with a majority of correct processes. Chandra, Hadzilacos and Toueg presented the weakest failure detector result at PODC 1992, and both papers appeared in the Journal of the ACM in 1996. Their proof that $\Diamond\mathcal{W}$ is weakest goes through $\Omega$; Chu (1998) gave a short direct reduction from $\Diamond\mathcal{W}$ to $\Omega$. Delporte-Gallet, Fauconnier and Guerraoui introduced $\Sigma$ in 2002 and proved in the journal version of 2010 that $\Omega \times \Sigma$ is weakest for consensus with any number of crashes. The DAG and simulation technique of CHT has since been reused for many other weakest detector results.

## References
