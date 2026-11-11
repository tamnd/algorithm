---
tag: NNA88Z
kind: theorem
slug: byzantine-resilience-bound
name: Byzantine resilience bound
aliases:
- n >= 3t+1 bound
- 3f+1 bound
- one-third resilience bound
area: distributed/byzantine-agreement
level: core
summary: "Without signatures, Byzantine broadcast and consensus are impossible when n <= 3t (for n >= 3). A general network also needs vertex connectivity at least 2t + 1."
prereqs: [byzantine-broadcast, oral-messages-model, strong-validity]
see_also: [authenticated-resilience-bound, oral-messages-algorithm, byzantine-round-lower-bound, byzantine-quorum-system, phase-king-algorithm, approximate-agreement, k-vertex-connected-graph, adversary-argument]
sources:
  - paper: doi:10.1145/322186.322188
    title: Marshall Pease, Robert Shostak and Leslie Lamport, Reaching Agreement in the Presence of Faults, Journal of the ACM 27(2), 1980
    locator: pages 228 to 234 (interactive consistency is solvable for, and only for, n >= 3m + 1, the first rigorous proof)
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine Generals Problem, ACM Transactions on Programming Languages and Systems 4(3), 1982
    locator: Section 2 (impossibility for three generals and the reduction from 3m Albanian generals, pages 384 to 387)
  - paper: doi:10.1007/BF01843568
    title: Michael J. Fischer, Nancy A. Lynch and Michael Merritt, Easy impossibility proofs for distributed consensus problems, Distributed Computing 1(1), 1986
    locator: pages 26 to 39 (the hexagon scenario argument for n >= 3t + 1 and connectivity at least 2t + 1, also for weak agreement, firing squad, approximate agreement and clock synchronization)
  - paper: doi:10.1016/0196-6774(82)90004-9
    title: Danny Dolev, The Byzantine generals strike again, Journal of Algorithms 3(1), 1982
    locator: pages 14 to 30 (agreement in general graphs needs n > 3t and connectivity greater than 2t, and both are enough)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 6, Section 6.4 (lower bound on the number of processes, by the hexagon argument) and Section 6.5 (connectivity in general graphs)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 5, Section 5.2 (the ratio of faulty processes for Byzantine failures)
---

Without signatures, Byzantine agreement is impossible unless fewer than one third of the processes are faulty. In the synchronous [oral messages model](/oral-messages-model/) on a complete network, no algorithm solves [Byzantine broadcast](/byzantine-broadcast/) with $t$ faults when $3 \le n \le 3t$, and no algorithm solves consensus with [strong validity](/strong-validity/) when $2 \le n \le 3t$. On a general network, the [vertex connectivity](/vertex-connectivity/) must also be at least $2t + 1$. Pease, Shostak and Lamport proved the bound in 1980, and the hexagon proof on this page is the scenario argument of Fischer, Lynch and Merritt (1986).

## Statement

**Model.** There are $n$ processes on a complete network of reliable links in the [synchronous model](/synchronous-model/). Messages are oral: a receiver knows the sender of each message on a link, but a process cannot prove to a third process what it received. Up to $t$ processes are [Byzantine](/byzantine-failure-model/): they can send any messages, different ones to different processes, and they act together. The adversary is static. The algorithm may be deterministic or randomized, but it must be correct in every run.

**Theorem.**

1. *(Broadcast.)* If $3 \le n \le 3t$, no algorithm solves Byzantine broadcast with at most $t$ faults: in some run, either two correct processes output different values, or the sender is correct and a correct process outputs a value other than the sender's input. This is the bound "$n \ge 3m + 1$" of PSL and LSP, with $m = t$.
2. *(Consensus.)* If $1 \le t$ and $2 \le n \le 3t$, no algorithm solves binary consensus with agreement, strong validity and termination with at most $t$ faults.
3. *(Connectivity, cited.)* On a network graph $G$ with $n > 3t$, Byzantine broadcast and consensus are solvable with $t$ faults if and only if $G$ has vertex connectivity at least $2t + 1$.

Parts 1 and 2 are proved on this page in full. Part 3 is due to Dolev (1982), and its proof by the same scenario method is in Fischer, Lynch and Merritt. Only a sketch is given here.

**Notation.** LSP write $m$ for the number of traitors. This page uses $t$, as the other pages of this area do.

## In plain words

Three generals, one of them a traitor, cannot agree by messenger. Suppose a general hears "attack" from the commander and "the commander told me retreat" from the third general. Either the commander or the third general is lying, and the two cases look the same to this general. Any rule it uses can be fooled.

The proof makes this exact. It joins two copies of the three generals in a ring of six. In the ring nobody lies, but each pair of neighbors sees just what it would see in some real run with one traitor. The rules of agreement then force answers around the ring that cannot all hold.

With more generals, split them into three groups of at most a third each, and the same trick works. So a third or more traitors is always too many.

## Proof

The full proof is below. This section gives its structure.

**Indistinguishability.** A process decides as a function of its *view*: its input, its coins and the messages it received in each round, with the name of the sender of each. Two runs in which a process has the same view give it the same decision. Oral messages give the faulty processes their full power: a faulty process can send to $q$ any message that some correct process could send to $q$ in some run.

**The hexagon for consensus, $n = 3$, $t = 1$.** Assume an algorithm $P$ for processes $A$, $B$, $C$. Build a ring of six copies, $A_0, B_0, C_0, A_1, B_1, C_1$ in this order, with input 0 at the copies with index 0 and input 1 at those with index 1. Each copy runs the code of its process, and each ring neighbor stands in for the other process of that name. For example, $A_0$ talks to $B_0$ as $B$ and to $C_1$ as $C$. The ring is not a run of $P$, but each copy has a well defined view.

- *Run $\alpha$:* $B$ and $C$ are correct with input 0. $A$ is faulty: it sends to $B$ what $A_0$ sends to $B_0$ in the ring, and to $C$ what $A_1$ sends to $C_0$. By induction on rounds, $B$ and $C$ have the views of $B_0$ and $C_0$. Strong validity forces 0, so $C_0$ decides 0.
- *Run $\beta$:* $A$ and $B$ are correct with input 1, and $C$ is faulty in the same way. They have the views of $A_1$ and $B_1$, so $A_1$ decides 1.
- *Run $\gamma$:* $C$ has input 0, $A$ has input 1, and $B$ is faulty. $C$ and $A$ have the views of $C_0$ and $A_1$, so $C$ decides 0 and $A$ decides 1. Agreement fails.

The implementation builds the ring for four small protocols and replays each of the three runs. It checks that each correct process has the same view as its copy in the ring. For "exchange inputs and take the majority", the copies with index 0 decide 0 and those with index 1 decide 1. The three runs give $\{B: 0, C: 0\}$, $\{A: 1, B: 1\}$ and $\{C: 0, A: 1\}$, so run $\gamma$ breaks agreement. For two rounds of flooding with the minimum rule, which is correct for one crash, run $\beta$ gives $\{A: 0, B: 0\}$ although both inputs are 1, so validity fails. "Decide your own input" breaks agreement in run $\gamma$. Each protocol fails in at least one run, as the proof says it must.

**The hexagon for broadcast, $n = 3$, $t = 1$.** Let $A$ be the sender. Use the same ring, with $A_0$ holding input 0 and $A_1$ holding input 1. In run $X$, $A$ and $B$ are correct with $A$'s input 0, and $C$ is faulty: $B$ has the view of $B_0$ and must output 0 by validity. In run $Y$, $B$ and $C$ are correct and the sender $A$ is faulty: by agreement $B_0$ and $C_0$ output the same value, so $C_0$ outputs 0. In run $Z$, $C$ and $A$ are correct with input 1, and $B$ is faulty: $C$ has the view of $C_0$ and outputs 0, but validity asks for 1.

**From $n \le 3t$ to $n = 3$.** This is the reduction of LSP, Section 2, with "Albanian" generals. Split the $n$ processes into three nonempty groups of at most $t$ each, which is possible when $3 \le n \le 3t$. Each of three processes simulates one group: it runs all their code, delivers messages inside the group itself, and sends messages between groups on its links. A faulty simulator makes at most $t$ simulated processes faulty. A correct one outputs the output of the first process of its group. So an algorithm for $n$ processes and $t$ faults gives one for 3 processes and 1 fault, which does not exist. For broadcast, the sender's group is simulated by the sender. For consensus each simulated process gets the input of its simulator, and strong validity carries over.

**Consensus with $n \le 2$.** For $n = 2$ and $t = 1$, let $A$ have input 0 and $B$ input 1, both correct. $A$ cannot tell this run from one where $B$ is faulty but follows the code. In that run, strong validity forces $A$ to decide 0. In the same way $B$ decides 1. For $n = 1$ the one process decides its own input, so consensus is trivial there.

## Consequences

- **The bound of OM(m) is exact.** The [oral messages algorithm](/oral-messages-algorithm/) works for $n > 3t$, so $n \ge 3t + 1$ is necessary and enough for Byzantine broadcast with oral messages in the synchronous model. The implementation of OM(m) builds the hexagon attack on it for $n = 3m$, with $m = 1$ and $m = 2$.
- **Quorums of size $2t + 1$.** Since $n \ge 3t + 1$, any two sets of $n - t$ processes share at least $t + 1$ processes, so at least one correct one. This is the root of [Byzantine quorum systems](/byzantine-quorum-system/) and of the $3f + 1$ replicas of [PBFT](/pbft/) and other [BFT](/byzantine-fault-tolerance/) protocols.
- **The same bound in weaker timing.** An algorithm for the asynchronous or partially synchronous model also works in the synchronous model. So $n \ge 3t + 1$ is needed there too, for every Byzantine protocol without signatures, and in partial synchrony also with signatures (Dwork, Lynch and Stockmeyer, 1988).
- **Other problems.** Fischer, Lynch and Merritt use the same method to show the bound for weak agreement, the firing squad problem, [approximate agreement](/approximate-agreement/) and clock synchronization. LSP show in Section 2 that approximate agreement on a time of attack is as hard as exact agreement.
- **Signatures change it for broadcast only.** With unforgeable signatures, broadcast works for any $t < n$, but consensus with strong validity still needs $n > 2t$. See the [authenticated resilience bound](/authenticated-resilience-bound/).

## Tightness

Both parts are tight. OM(m) solves broadcast for $n = 3t + 1$, and the consensus algorithm that broadcasts every input with OM(t) and decides the majority of the resulting vector solves consensus with strong validity for $n \ge 3t + 1$. For broadcast, $n \le 2$ is trivial: with $n = 2$, the receiver outputs what the sender sends, which is correct whenever the sender is. At $n = 3t + 1$ the cost can also be small: the algorithm of Garay and Moses (1998) needs only $t + 1$ rounds and polynomial communication.

On a general graph the bound has two parts: $n \ge 3t + 1$ and vertex connectivity at least $2t + 1$. A [$(2t + 1)$-connected graph](/k-vertex-connected-graph/) has $2t + 1$ disjoint paths between any two vertices by [Menger's theorem](/menger-theorem/), so a value sent on all of them arrives on a majority of correct paths. With connectivity $2t$, a cut of $2t$ vertices splits the graph, and a ring of copies built around the cut gives the contradiction, see Fischer, Lynch and Merritt.

## History

Pease, Shostak and Lamport (1980) proved that interactive consistency needs $n \ge 3m + 1$ processes without authentication, as part of the SIFT project. The 1982 paper by Lamport, Shostak and Pease gave the informal three-generals argument, with a pointer to the 1980 paper for the rigorous proof, and the reduction from $3m$ "Albanian" generals. Dolev (1982) added the connectivity condition. Fischer, Lynch and Merritt (1986) gave the short hexagon proofs, which became the standard method for such bounds in the textbooks of Lynch and of Attiya and Welch.

## References
