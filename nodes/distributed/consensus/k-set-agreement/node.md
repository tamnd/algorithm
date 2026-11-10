---
tag: 16H2HE
kind: problem
slug: k-set-agreement
name: k-set agreement problem
aliases:
- set agreement
area: distributed/consensus
level: advanced
summary: Each process decides one of the input values, and at most k different values are decided. Consensus is the case k = 1. With f crashes it is solvable asynchronously exactly when f < k.
prereqs: [consensus-problem, asynchronous-model, synchronous-model, crash-failure]
see_also: [consensus-problem, flp-impossibility, floodset, consensus-round-lower-bound, approximate-agreement, consensus-number, wait-freedom, atomic-snapshot]
sources:
  - paper: doi:10.1006/inco.1993.1043
    title: Soma Chaudhuri, More choices allow more faults, set consensus problems in totally asynchronous systems, Information and Computation 105(1), 1993, pages 132 to 158
    locator: the definition of k-set agreement, the algorithm for f < k, and the conjecture that the problem is not solvable for f ≥ k
  - paper: doi:10.1145/167088.167119
    title: Elizabeth Borowsky and Eli Gafni, Generalized FLP impossibility result for t-resilient asynchronous computations, Proceedings of the 25th ACM Symposium on Theory of Computing (STOC), 1993, pages 91 to 100
    locator: the impossibility of k-set agreement with k failures, and the simulation (BG simulation) that carries a wait-free result to the t-resilient case
  - paper: doi:10.1145/331524.331529
    title: Maurice Herlihy and Nir Shavit, The topological structure of asynchronous computability, Journal of the ACM 46(6), 1999, pages 858 to 923
    locator: the asynchronous computability theorem and the wait-free impossibility of k-set agreement among k + 1 processes
  - paper: doi:10.1137/S0097539796307698
    title: Michael Saks and Fotios Zaharoglou, Wait-free k-set agreement is impossible, the topology of public knowledge, SIAM Journal on Computing 29(5), 2000, pages 1449 to 1483
    locator: the wait-free impossibility of k-set agreement
  - paper: doi:10.1145/355483.355489
    title: Soma Chaudhuri, Maurice Herlihy, Nancy A. Lynch and Mark R. Tuttle, Tight bounds for k-set agreement, Journal of the ACM 47(5), 2000, pages 912 to 943
    locator: the lower bound of floor(f/k) + 1 rounds in the synchronous model with crash failures, and the matching algorithm
  - book: isbn:9780124045781
    title: Maurice Herlihy, Dmitry Kozlov and Sergio Rajsbaum, Distributed Computing Through Combinatorial Topology, Morgan Kaufmann, 2013
    locator: the chapters on set agreement, Sperner's lemma, and the synchronous lower bound
---

The k-set agreement problem asks $n$ processes, each with an input value, to decide values so that every decision is some process's input and at most $k$ different values are decided. For $k = 1$ it is the [consensus problem](/consensus-problem/); a larger $k$ allows more disagreement and, in return, tolerates more crashes. Chaudhuri (1993) defined it and solved it in the [asynchronous model](/asynchronous-model/) whenever fewer than $k$ processes can crash. Three groups proved in 1993 that it cannot be solved when $k$ or more can crash, which extends the [FLP impossibility](/flp-impossibility/) result from $k = 1$ to every $k$.

## In plain words

A group of friends must choose where to eat. Full agreement on one place is hard when some friends stop answering their phones. So the rule is weaker: the group may split, but into at most $k$ places, and each place must be one that somebody suggested.

A simple method works when fewer than $k$ friends can go silent. Everyone sends a suggestion to everyone. Each friend waits for suggestions from all but the silent ones and picks the first place in alphabetical order. Each friend misses only a few suggestions, so everyone picks from the first few places of the list.

When $k$ or more friends can go silent, no method at all works, however clever.

## Definition

There are $n$ processes. Each process $p_i$ starts with an input $v_i$ from a set $V$ with more than $k$ elements. Up to $f$ processes can crash. A protocol solves **k-set agreement** if every run has these properties:

- **Termination.** Every correct process eventually decides.
- **Validity.** Every decided value is the input of some process.
- **k-agreement.** The set of values decided by all processes, correct or not, has at most $k$ elements.

For $k = 1$ this is consensus. For $k \ge n$ it is trivial: each process decides its own input. **Set agreement** often means the case $k = n - 1$, the weakest nontrivial case for $n$ processes.

## Variants

- **Strong validity.** Every decided value is the input of a correct process. This matters with crash failures only in some lower bound proofs, and it is the natural form with Byzantine failures, where a faulty process can claim any input.
- **Shared memory.** Processes communicate through read and write registers instead of messages. The wait-free form ($f = n - 1$) is the standard setting of the topological results.
- **Synchronous rounds.** With [synchronous](/synchronous-model/) rounds the problem is always solvable, and the question is how many rounds it takes.
- **Byzantine set agreement.** Faulty processes may lie; the bounds on $n$ grow.
- **Approximate agreement.** Instead of few values, the decisions must be close: see [approximate agreement](/approximate-agreement/).

## Examples

Take $n = 5$, $f = 2$ and $k = 3$, with inputs $4, 7, 1, 9, 3$. In the algorithm below each process waits for $n - f = 3$ values, its own included, and decides the smallest.

| process | input | values it hears first | decision |
|---|---|---|---|
| $p_1$ | 4 | 4, 7, 9 | 4 |
| $p_2$ | 7 | 7, 9, 3 | 3 |
| $p_3$ | 1 | 1, 4, 7 | 1 |
| $p_4$ | 9 | 9, 7, 4 | 4 |
| $p_5$ | 3 | 3, 9, 7 | 3 |

The decisions are $\{1, 3, 4\}$: three values, which $k = 3$ allows. These are the three smallest inputs, as the proof below predicts. With $k = 2$ this run breaks 2-agreement, which shows why the algorithm needs $f < k$.

**Non-example.** Every process decides its own input: validity holds, but there can be $n$ values, so it solves $k$-set agreement only for $k \ge n$.

## Known algorithms

**Asynchronous, $f < k$ (Chaudhuri, 1993).** Channels are reliable, and $f < n$.

```pseudo id=main
MIN OF THE FIRST n − f VALUES, at process p
L1  send v_p to all processes
L2  wait until values from n − f distinct processes have arrived (its own value counts)
L3  decide the smallest value received
FLOODMIN, synchronous, at process p                      ▷ x ← v_p
L4  for rounds 1 to ⌊f/k⌋ + 1: send x to all; x ← min(x, all values received this round)
L5  decide x
```

**Theorem 1.** If $f < k$, lines L1 to L3 solve k-set agreement in the asynchronous model with up to $f$ crashes. More exactly, every decision is at most the $(f+1)$-th smallest input.

*Proof.* Termination: at least $n - f$ processes are correct, and each sends its value to all in line L1, so every correct process gets $n - f$ values in line L2. Validity: a process decides a value that it received, and only inputs are sent. For k-agreement, list the processes by input, from smallest to largest, with ties broken by id, and let $S$ be the first $f + 1$ processes of this list. A process that decides has values from $n - f$ processes, so it misses at most $f$ processes, and at least one process of $S$ is among those it heard. Its decision is at most the input of that process, hence at most $u$, the largest input in $S$. Every decision is also an input. So every decision is in the set of inputs that are at most $u$, and every such input is the input of some process in $S$ (an input smaller than $u$ comes before position $f + 1$ in the list, and an input equal to $u$ is $u$). That set has at most $f + 1 \le k$ values. $\square$

The bound is tight for this algorithm: with $f = k$ it can decide $k + 1$ values, as the example above shows for $f = 2$, $k = 2$.

**Synchronous, FloodMin.** Lines L4 and L5 run $\lfloor f/k \rfloor + 1$ rounds.

**Theorem 2.** FloodMin solves k-set agreement in the synchronous model with up to $f$ crashes, where a process can crash in the middle of sending a round's messages.

*Proof.* Validity holds because only inputs travel. Termination is by the fixed round count. Call the value $x$ of a process its estimate. Two facts:

1. *The number of distinct estimates among live processes never grows.* Every estimate at the end of a round is the estimate of some process at its start, and only processes that were live then send. So the set of estimates after a round is a subset of the set before it.
2. *Some round has at most $k - 1$ crashes.* There are $\lfloor f/k \rfloor + 1$ rounds. If each had $k$ or more crashes, there would be at least $k(\lfloor f/k \rfloor + 1) > f$ crashes.

Take a round $r$ with at most $k - 1$ crashes. Let $m$ be the smallest estimate among the processes that are live at its start and do not crash in it. These processes send to all, so every process that ends round $r$ gets $m$, and its new estimate is either $m$ or a smaller value that came from one of the at most $k - 1$ processes that crashed in round $r$. So after round $r$ there are at most $k$ distinct estimates, and by fact 1 there are still at most $k$ at the end. $\square$

## Bounds

- **Asynchronous, solvable when $f < k$.** Theorem 1. Chaudhuri conjectured that it is not solvable when $f \ge k$, and proved this for a restricted class of protocols.
- **Asynchronous, impossible when $f \ge k$.** No deterministic protocol solves k-set agreement if $k$ processes can crash, in message passing or in shared memory with read and write registers. Borowsky and Gafni (1993), Herlihy and Shavit (1999, first announced in 1993) and Saks and Zaharoglou (2000, first announced in 1993) proved the wait-free case, $k + 1$ processes with up to $k$ crashes, independently. The proofs use topology: the possible views form a subdivided simplex, and Sperner's lemma gives a run in which $k + 1$ values are decided. The BG simulation of Borowsky and Gafni carries the wait-free result to any $n$ and $f \ge k$. This page cites these results and does not prove them.
- **Synchronous rounds.** With crash failures, $\lfloor f/k \rfloor + 1$ rounds are necessary and sufficient (Chaudhuri, Herlihy, Lynch and Tuttle, 2000); the lower bound needs enough processes, $n \ge f + k + 1$. For $k = 1$ this is the $f + 1$ bound of the [consensus round lower bound](/consensus-round-lower-bound/), and FloodMin with $k = 1$ is [FloodSet](/floodset/). The tests show a run with $n = 5$, $f = 2$, $k = 2$ in which one round, $\lfloor f/k \rfloor$, gives 3 values.

So, in the asynchronous model with crash failures, k-set agreement is solvable if and only if $f < k$.

## Reductions

- **From consensus.** Any consensus protocol solves k-set agreement for every $k \ge 1$, since one value is at most $k$ values. So k-set agreement is no harder than consensus.
- **From $k$-set to $k'$-set, for $k' \ge k$.** Trivial, in the same way.
- **To $k$ groups of consensus.** Split the processes into $k$ groups and run consensus in each group; at most $k$ values are decided. This shows that k-set agreement among $n$ processes is solvable when consensus is solvable inside each group, for example with fewer than half of each group crashing and a [failure detector](/failure-detector/).
- **BG simulation.** $k + 1$ processes can simulate a protocol of $n$ processes that tolerates $k$ crashes, using [atomic snapshots](/atomic-snapshot/) and agreement on each simulated step. So a $k$-resilient protocol for $n$ processes would give a [wait-free](/wait-freedom/) protocol for $k + 1$ processes, which does not exist.

## Applications

- **Computability theory.** k-set agreement is the standard task for showing what [wait-free](/wait-freedom/) shared memory cannot do. The topological method that proved it impossible became the general tool for asynchronous computability.
- **Hierarchies of objects.** An object that solves k-set agreement among some number of processes is weaker than consensus, and such objects measure the power of synchronization primitives between registers and [consensus numbers](/consensus-number/) above 1.
- **Weaker coordination.** Some tasks need only a few leaders or a few choices, for example choosing at most $k$ coordinators or at most $k$ versions of a value; then k-set agreement is enough and tolerates more crashes than consensus.

## References
