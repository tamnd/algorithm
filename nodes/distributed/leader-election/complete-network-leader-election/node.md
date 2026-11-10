---
tag: EE9300
kind: problem
slug: complete-network-leader-election
name: Leader election in complete networks
aliases:
- Election in complete graphs
- Election in fully connected networks
area: distributed/leader-election
level: advanced
summary: Elect one leader when every pair of processes is linked. Asynchronous algorithms need Θ(n log n) messages; capture algorithms reach this in O(n) time, or O(log n) synchronous rounds.
prereqs: [complete-graph, ring-leader-election, asynchronous-model, message-complexity]
see_also: [korach-kutten-moran, afek-gafni, bully-algorithm, ring-leader-election, tree-leader-election, awerbuch-leader-election, ring-election-lower-bound, explicit-leader-election]
sources:
  - paper: doi:10.1016/0304-3975(89)90103-5
    title: Ephraim Korach, Shlomo Moran and Shmuel Zaks, Optimal lower bounds for some distributed algorithms for a complete network of processors, Theoretical Computer Science 64(1), 1989
    locator: pages 125 to 132 (the lower bound of Ω(n log n) messages for election in asynchronous complete networks)
  - paper: doi:10.1137/0220023
    title: Yehuda Afek and Eli Gafni, Time and message bounds for election in synchronous and asynchronous complete networks, SIAM Journal on Computing 20(2), 1991
    locator: pages 376 to 394 (O(n log n) messages with O(log n) synchronous time and O(n) asynchronous time)
  - paper: doi:10.1145/77606.77610
    title: Ephraim Korach, Shay Kutten and Shlomo Moran, A modular technique for the design of efficient distributed leader finding algorithms, ACM Transactions on Programming Languages and Systems 12(1), 1990
    locator: pages 84 to 101 (election from traversal, with the O(n log n) instance for complete networks)
  - book: isbn:9780471719977
    title: Nicola Santoro, Design and Analysis of Distributed Algorithms, Wiley, 2007
    locator: Chapter 3 (election in complete networks)
---

Leader election in complete networks asks $n$ processes, each of them linked to every other one, to choose exactly one leader. Each process can reach every other process in one hop, so a leader can be found in one round by sending every identifier to everybody, but that costs $n(n - 1)$ messages. The interesting question is how few messages are enough. In the [asynchronous model](/asynchronous-model/), $\Theta(n \log n)$ messages are needed and enough: Korach, Moran and Zaks proved the lower bound, and capture algorithms such as those of [Korach, Kutten and Moran](/korach-kutten-moran/) and [Afek and Gafni](/afek-gafni/) meet it. Afek and Gafni also showed that the time can be $O(n)$ in the asynchronous model and $O(\log n)$ rounds in the synchronous model with the same number of messages.

## In plain words

Everyone in a room can talk directly to everyone else, and the group must pick one leader. The easy way is for everybody to tell their number to everybody, and the biggest number wins. That works at once, but the number of messages grows with the square of the group size.

A cheaper way is for candidates to collect supporters. A candidate asks people one by one, or in growing groups, to join its team. When two candidates want the same person, the stronger one wins, and the other drops out. Only a few candidates get far, so the total number of messages grows only a little faster than the size of the group. It cannot be made smaller than that.

## Definition

The network is the [complete graph](/complete-graph/) $K_n$ on $n \ge 1$ processes. Each process has a distinct identifier and $n - 1$ links to the others. A process knows its links, and so knows $n$, but it does not know which identifier is at the other end of a link. In the basic model there is no *sense of direction*: the links carry no global labels. Channels are reliable. A nonempty set of processes, chosen by an adversary, starts on its own, and the others start when a message reaches them. Each process has an output $\mathit{status} \in \{\text{unknown}, \text{leader}, \text{non-leader}\}$ that it writes at most once.

An algorithm solves **leader election in complete networks** if in every run exactly one process ends with *leader* and all others with *non-leader*. In the [explicit form](/explicit-leader-election/), every process also learns the leader's identifier, which the leader can tell everyone with $n - 1$ more messages.

## Variants

- **Timing.** [Asynchronous](/asynchronous-model/), or [synchronous](/synchronous-model/) rounds with a common start.
- **Sense of direction.** If the links of each process are labelled in a way that is consistent across the network, for example by the distance along a fixed Hamiltonian cycle, a process can use the structure, and fewer messages are enough.
- **How identifiers are used.** Comparison algorithms only compare identifiers. Synchronous algorithms that use the values of identifiers to count time, such as the TimeSlice idea, can use fewer messages at the cost of time that depends on the identifiers.
- **Failures.** If processes can crash, the [bully algorithm](/bully-algorithm/) and its relatives elect the largest identifier among those alive, with failure detection by timeouts.
- **Anonymous processes.** Without identifiers, a deterministic algorithm cannot break the symmetry of a complete network; see [anonymous leader election](/anonymous-leader-election/).

## Examples

- **Two processes.** Each sends its identifier to the other, and the larger wins: 2 messages.
- **All-to-all.** Every process sends its identifier on all its links, and the largest wins: $n(n - 1)$ messages and one time unit. For $n = 1000$ that is 999,000 messages.
- **Capture.** In the [Afek-Gafni](/afek-gafni/) synchronous form, candidates ask $1, 2, 4, \ldots$ others in successive phases. The page traces a run on 8 processes with 48 messages before the announcement, in 12 rounds. For $n = 1000$ its bound is $4n \lceil \log_2 n \rceil = 40{,}000$ messages, well below the all-to-all count.
- **One starter.** If only one process starts, it can capture the others one by one with $2(n - 1)$ messages, because nobody competes with it. The hard case is many starters.

## Known algorithms

| algorithm | model | messages | time |
|---|---|---|---|
| All-to-all | any | $n(n - 1)$ | $O(1)$ |
| [Bully algorithm](/bully-algorithm/) | synchronous, crashes | $O(n^2)$ | a few timeout periods |
| Korach, Moran and Zaks | asynchronous | $O(n \log n)$ | not studied here |
| [Korach, Kutten and Moran](/korach-kutten-moran/) | asynchronous | $O(n \log n)$ | $O(n \log n)$ for the form on its page |
| [Afek and Gafni](/afek-gafni/), synchronous | synchronous | $O(n \log n)$ | $O(\log n)$ |
| [Afek and Gafni](/afek-gafni/), asynchronous | asynchronous | $O(n \log n)$ | $O(n)$ |
| TimeSlice idea | synchronous, integer identifiers | $n - 1$ | $u_{\min}$ rounds |
| [Awerbuch](/awerbuch-leader-election/) on $K_n$ | asynchronous | $O(n^2)$, since $m = \Theta(n^2)$ | $O(n)$ |

The TimeSlice line: the process with identifier $u$ waits until round $u$, and if it has heard nothing by then, it sends its identifier to all others and is the leader. The process with the smallest identifier $u_{\min}$ is elected with $n - 1$ messages, but the time can be huge.

## Bounds

- **Lower bound, asynchronous.** Every asynchronous election algorithm on $K_n$, in the basic model without sense of direction, has runs with $\Omega(n \log n)$ messages. This is the theorem of Korach, Moran and Zaks. Its proof is an adversary argument: the adversary controls which process is at the other end of a link that has not been used yet, and the order in which messages arrive, and it uses this to force many candidates to grow before one of them can win. The same bound holds for rings; see the [ring election lower bound](/ring-election-lower-bound/).
- **Upper bound.** $O(n \log n)$ messages, by the capture algorithms above; the complete-network form on the [Korach-Kutten-Moran page](/korach-kutten-moran/) has a full proof of at most $4 n H_n$ messages, where $H_n$ is the $n$-th [harmonic number](/harmonic-series/).
- **Time.** In the asynchronous model, Afek and Gafni elect in $O(n)$ time with $O(n \log n)$ messages; in the synchronous model, in $O(\log n)$ rounds. They also prove lower bounds on how time and messages trade against each other.
- **Easy lower bound for the explicit form.** Every process other than the leader must receive a message, so $n - 1$ messages are needed. In the synchronous model with integer identifiers, the TimeSlice idea meets this bound, which shows that the $\Omega(n \log n)$ bound needs asynchrony, comparison of identifiers or a bound on the time.
- **Sense of direction.** With a consistent labelling of the links, $O(n)$ messages are enough. Loui, Matsushita and West gave such an algorithm.

## Reductions

- **To a spanning star.** Once a leader is known, it can tell every process, and the links to the leader form a [spanning tree](/distributed-spanning-tree/) of depth 1, with $n - 1$ more messages. Conversely, a spanning tree that one process knows to be the root gives a leader.
- **From general networks.** Algorithms for arbitrary graphs, such as [Gallager, Humblet and Spira](/gallager-humblet-spira/) or [Awerbuch](/awerbuch-leader-election/), work on $K_n$, but with $m = n(n - 1)/2$ links their $O(m + n \log n)$ bound is $O(n^2)$, worse than the capture algorithms.
- **To rings, with sense of direction.** If the links are labelled along a Hamiltonian cycle, the processes can run any [ring election](/ring-leader-election/) on that cycle, with $O(n \log n)$ messages, and use the other links for short cuts.
- **From traversal.** The [Korach-Kutten-Moran](/korach-kutten-moran/) technique turns a serial traversal of cost $f(n)$ into an election of cost $O((f(n) + n) \log n)$. On $K_n$, $f(n) = O(n)$.

## Applications

- **Clusters with a full mesh.** In a small cluster in which every server can reach every other one, a coordinator, a lock manager or a primary copy must be chosen.
- **Recovery after a failure.** When a coordinator fails, the remaining processes elect a new one; the [bully algorithm](/bully-algorithm/) and the [invitation algorithm](/invitation-algorithm/) are designed for this setting.
- **A model for overlay networks.** Many algorithms on overlays and on the congested clique assume that every process can send to every other one, and the bounds here show what election costs there.

## References
