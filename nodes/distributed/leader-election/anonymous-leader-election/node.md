---
tag: XNGCEW
kind: problem
slug: anonymous-leader-election
name: Leader election in anonymous networks
aliases:
- Anonymous ring election
- Anonymous leader election
area: distributed/leader-election
level: advanced
summary: Leader election among identical processes. It is impossible deterministically on symmetric networks; with coins it is solvable for sure when n is known, and only with some error when n is unknown.
prereqs: [anonymous-network, anonymous-ring-impossibility, ring-leader-election, las-vegas-algorithm]
see_also: [itai-rodeh, anonymous-ring-impossibility, ring-leader-election, chang-roberts, las-vegas-algorithm, fair-coin-flipping, explicit-leader-election, ring-network]
sources:
  - paper: doi:10.1145/800141.804655
    title: Dana Angluin, Local and global properties in networks of processors, Proceedings of the 12th ACM Symposium on Theory of Computing, 1980
    locator: pages 82 to 93 (no deterministic election in symmetric networks of identical processes)
  - paper: doi:10.1109/SFCS.1981.41
    title: Alon Itai and Michael Rodeh, Symmetry breaking in distributive networks, Proceedings of the 22nd IEEE Symposium on Foundations of Computer Science, 1981
    locator: pages 150 to 158 (randomized election on anonymous rings)
  - paper: doi:10.1016/0890-5401(90)90004-2
    title: Alon Itai and Michael Rodeh, Symmetry breaking in distributed networks, Information and Computation 88(1), 1990
    locator: pages 60 to 87 (Lemma 3.1 on verification and restart, Section 3.4 on asynchronous rings, Theorems 4.1 and 4.2 on rings of unknown size)
  - paper: doi:10.1109/71.481599
    title: Masafumi Yamashita and Tsunehiko Kameda, Computing on anonymous networks, part I, characterizing the solvable cases, IEEE Transactions on Parallel and Distributed Systems 7(1), 1996
    locator: pages 69 to 89 (deterministic election on anonymous networks and views)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 3, Section 3.2 (anonymous rings) and Chapter 14, Section 14.1 (randomized leader election in rings)
---

Leader election in anonymous networks asks identical processes, with no identifiers, to choose exactly one leader. On a symmetric network such as a ring, no deterministic algorithm can do this, by [Angluin's theorem](/anonymous-ring-impossibility/). Random choices are the standard way out. When the processes know the size $n$ of the network, a [Las Vegas algorithm](/las-vegas-algorithm/) such as [Itai-Rodeh](/itai-rodeh/) elects a leader with probability 1 and is never wrong. When $n$ is not known, Itai and Rodeh showed that no algorithm in which the processes stop can be correct in every run: some error, or a run that never visibly ends, must be accepted.

## In plain words

A group of people who look exactly alike and follow the same instructions must pick one leader. They have no names. If they all see the same things, nothing in the instructions can make one of them different, so they cannot pick a leader by rules alone.

If each person can toss a coin, the coins can come out differently, and that breaks the tie. When everyone knows how many people there are, they can check that exactly one person won, and try again if not. So in the end they always succeed, though how long it takes depends on luck.

If nobody knows how many people there are, a check can be fooled: a bigger circle can look just like a smaller one. Then the group must accept a small chance of a wrong result.

## Definition

The network is an [anonymous network](/anonymous-network/): a connected graph with $n$ processes and a port numbering, in which all processes run the same algorithm from the same initial state. In the randomized version each process has its own source of independent random bits. Each process has an output $\mathit{status} \in \{\text{unknown}, \text{leader}, \text{non-leader}\}$, written at most once.

An algorithm solves **anonymous leader election** on a class of networks with one of the following guarantees, for every network in the class and every schedule of the adversary:

- **Deterministic.** Every run elects exactly one leader.
- **Las Vegas.** In every run at most one process becomes the leader, and with probability 1 exactly one does. Processes that stop must have the right output.
- **Monte Carlo.** Every run ends, and with probability at least $1 - \varepsilon$ exactly one process is the leader.

The scheduler of an asynchronous network does not see the coins in advance. A run is *process terminating* if each process enters a final state and knows that it has; it is *message terminating* if only the absence of messages at the end shows that the run is over.

## Variants

- **Knowledge.** Processes know $n$ exactly, know a bound $N \ge n$, know $n$ up to a factor, or know nothing.
- **Topology.** Unidirectional or bidirectional rings, oriented or not; general graphs; complete graphs.
- **Timing.** [Synchronous](/synchronous-model/) or [asynchronous](/asynchronous-model/), and FIFO or not.
- **Termination.** Process termination or message termination.
- **Explicit.** In the [explicit form](/explicit-leader-election/) every process also learns something that names the leader, such as its distance from the leader.

## Examples

- **An oriented ring, deterministic.** No algorithm, for any $n \ge 2$, because all processes stay in the same state.
- **A star, deterministic.** The centre is the only process of its degree, so it can elect itself at once.
- **A ring of 4, randomized, $n$ known.** Each process draws a value in $\{1, 2, 3, 4\}$, and if the largest value is not unique the processes that hold it draw again. The worked run on the [Itai-Rodeh page](/itai-rodeh/) needs two rounds and 16 messages.
- **A ring of unknown size.** A ring of size $2N$ can be split into two halves that each behave like a ring of size $N$, so any algorithm that stops and claims one leader on the ring of size $N$ can stop with two leaders on the ring of size $2N$.

## Known algorithms

| algorithm | network | knowledge | guarantee | cost |
|---|---|---|---|---|
| [Itai-Rodeh](/itai-rodeh/) (random values, hop counter, dirty bit) | asynchronous unidirectional ring, FIFO | $n$ | Las Vegas | $O(n \log n)$ expected messages |
| Itai-Rodeh 1990, coin flips then verification | asynchronous ring | $n$ | Las Vegas | $O(n \log n)$ expected bits |
| Itai-Rodeh, synchronous | synchronous ring | $n$ | Las Vegas | at most $2.442\,n$ expected bits, $O(n)$ time |
| Itai-Rodeh, size known up to a factor below 2 | asynchronous ring | $N \le n \le 2N - 1$ | Las Vegas | $O(n \log n)$ expected bits |
| Monte Carlo versions | rings and graphs | none | correct with high probability | depends on the error |
| Deterministic, by views | any graph with all views different | $n$ or the graph | deterministic | depends on the graph |

## Bounds

- **Deterministic impossibility.** On every network with a port-preserving automorphism that moves each process, in particular an oriented ring with $n \ge 2$, no deterministic algorithm solves the problem, even with $n$ known ([Angluin 1980](/anonymous-ring-impossibility/)).
- **Las Vegas with $n$ known.** Possible on rings with $O(n \log n)$ expected messages or bits in the asynchronous case (Itai and Rodeh). The [Itai-Rodeh page](/itai-rodeh/) proves the bound $\mathbb{E}[M] \le (1 - 1/n)^{-n} n (H_n + 1)$ for the form with random values.
- **No certain termination with $n$ unknown.** Itai and Rodeh prove that a processor terminating algorithm that is always correct on a ring of size $N$ cannot be always correct on a ring of size $2N$ (their Theorem 4.1), and that no processor terminating asynchronous algorithm computes the size of the ring with probability $\alpha > 0$ on all rings (their Theorem 4.2). So with $n$ unknown, no algorithm both ends for certain and is always correct. One must accept an error probability, or message termination only.
- **Size known up to a factor.** If each process knows an $N$ with $N \le n \le 2N - 1$, a verification message that travels $2N - 1$ hops passes a second candidate whenever there is one, and Las Vegas election is again possible. Theorem 4.1 shows that this range cannot be widened to include both $N$ and $2N$.
- **Messages with identifiers.** For comparison, the [ring election lower bound](/ring-election-lower-bound/) gives $\Omega(n \log n)$ messages for deterministic algorithms on rings with identifiers.

## Reductions

- **To identifiers.** Election with $n$ known reduces to drawing random identifiers from a large range and running a deterministic algorithm such as [Chang-Roberts](/chang-roberts/), plus a check that the largest identifier is unique. The check uses the known $n$, as in Lemma 3.1 of Itai and Rodeh: a candidate sends a counter round the ring and restarts the election if it meets another candidate.
- **From size.** On a ring with a leader, the size can be found with $n$ messages: the leader sends a counter round the ring. So once a leader exists, the problem of computing $n$ is easy, and the hardness for unknown $n$ is really the hardness of checking that the leader is unique.
- **To symmetry breaking tasks.** Many tasks, such as choosing a maximal independent set or a colouring, need the same kind of symmetry breaking and use the same coin flipping tools, such as [fair coin flipping](/fair-coin-flipping/) in other settings.

## Applications

- **Systems without unique names**, such as some sensor networks or networks of very small devices, where giving each process a unique identifier is costly.
- **Privacy.** Processes may choose not to reveal stable identifiers.
- **Theory.** The problem shows how much knowledge of the network matters: with $n$ known it is solvable, with $n$ unknown it is not fully solvable.

## References
