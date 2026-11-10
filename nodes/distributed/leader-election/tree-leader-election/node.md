---
tag: 8SHSZ4
kind: problem
slug: tree-leader-election
name: Leader election in trees
aliases:
- Election on tree networks
area: distributed/leader-election
level: core
summary: Choose one leader in a network whose links form a tree. Without cycles, Θ(n) messages and Θ(d) time are enough and needed; saturation is the standard method.
prereqs: [tree, ring-leader-election, asynchronous-model, message-complexity]
see_also: [tree-election, explicit-leader-election, ring-leader-election, complete-network-leader-election, echo-algorithm, tree-center, distributed-spanning-tree, floodmax]
sources:
  - book: isbn:9780471719977
    title: Nicola Santoro, Design and Analysis of Distributed Algorithms, Wiley, 2007
    locator: Chapter 2 (saturation on trees) and Chapter 3 (election in trees, with the message count of election by saturation)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 7 (election with the tree algorithm, after a wake-up phase)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 4 (election in general synchronous networks by flooding) and Chapter 15 (election and spanning trees in asynchronous networks)
---

Leader election in trees asks the processes of a network whose links form a [tree](/tree/) to choose exactly one leader. Because a tree has no cycle, information can be collected from the leaves inwards with one message per link, and the problem is much cheaper than on a [ring](/ring-leader-election/) or a [complete network](/complete-network-leader-election/): $\Theta(n)$ messages are both enough and needed, in the asynchronous model and with any set of starting processes. The standard method is [election by saturation](/tree-election/), which sends $3n + k - 4$ messages when $k$ processes start on their own. This page is the problem view, with the lower bound; the saturation page gives the algorithm in full with its proof.

## In plain words

A group of people are linked by phone lines, with no loops, and they must agree on one leader. On a ring, messages have to go round and round, and that costs a lot. On a tree it is easier: the people at the edges report inwards, each person passes on the best number they have heard of, and the reports meet somewhere in the middle. Then the result is sent back outwards. Every line is used only a few times.

At the same time, nothing much cheaper is possible. Each person who is not the leader must hear at least one message, or they cannot know who the leader is.

## Definition

The network is a tree $T$ with $n \ge 1$ processes and $n - 1$ links. Each process has a distinct identifier and knows its own links; it need not know $n$ or the shape of $T$. Channels are reliable. A nonempty set of processes starts on its own, at times chosen by an adversary, and the others start when a message reaches them. Each process has an output $\mathit{status} \in \{\text{unknown}, \text{leader}, \text{non-leader}\}$ that it writes at most once.

An algorithm solves **leader election on trees** if in every run exactly one process ends with *leader* and all others with *non-leader*. In the [explicit form](/explicit-leader-election/) every process also outputs the leader's identifier.

## Variants

- **Timing.** [Asynchronous](/asynchronous-model/), FIFO or not, or [synchronous](/synchronous-model/) rounds.
- **Starters.** All processes start, or any nonempty set does; in the second case a wake-up phase is needed.
- **Which leader.** Any process, the largest identifier, or a centre of the tree.
- **Implicit or explicit.** Only the leader knows, or all processes learn the leader.
- **Anonymous trees.** If processes have no identifiers, the [anonymous version](/anonymous-leader-election/) depends on symmetry: a tree with a single [centre](/tree-center/) can elect it, while a tree with two centres and a symmetry that swaps them cannot elect a leader by a deterministic algorithm.

## Examples

- **Two processes.** Each sends its identifier to the other, and the larger one is the leader: 2 messages, $2n - 2$.
- **A path of $n$ processes.** With all processes starting, reports move in from both ends and meet on one link. The two ends of that link announce the result back to the ends of the path.
- **A star.** Every leaf reports to the centre. The centre is saturated together with the leaf whose report came last, because the centre reports to that leaf. All other leaves get the announcement from the centre.
- **A worked run.** The [saturation page](/tree-election/) traces a tree of 8 processes with 14 messages when all start, and 21 when one starts.

## Known algorithms

| algorithm | model | starters | messages | time |
|---|---|---|---|---|
| [Election by saturation](/tree-election/) | asynchronous | any | $3n + k - 4$ for $k$ starters | $O(d)$ |
| Saturation without wake-up | asynchronous | all | $2n - 2$ | $O(d)$ |
| [Echo](/echo-algorithm/) with a maximum, then broadcast | asynchronous | one | $3(n - 1)$ | $O(d)$ |
| Centre finding by saturation | asynchronous | any | $O(n)$ | $O(d)$ |
| [FloodMax](/floodmax/) | synchronous, $d$ known | all | $2(n - 1)\,d$ | $d$ rounds |

Here $d$ is the diameter of the tree. FloodMax works on every graph and is shown only for comparison; on a tree it wastes messages.

## Bounds

- **Upper bound.** Saturation elects the largest identifier with $3n + k - 4 \le 4n - 4$ messages and $O(d)$ time in every run, for any set of $k$ starters, and with $2n - 2$ messages when all start. The [proof](/tree-election/proofs/correctness/) counts every message exactly.
- **Lower bound for the explicit form: $n - 1$ messages.** In every run, each process other than the leader receives at least one message. *Proof.* Suppose a process $q$ that is not the leader receives no message in a run $\rho$. Then $q$ started on its own, and its only step is its start step, in which it writes the leader's identifier $L \ne \mathrm{id}(q)$. That step depends only on $\mathrm{id}(q)$ and the links of $q$. Change the leader's identifier to a value that is not used in the tree, and let $q$ start first. It takes the same start step and outputs $L$, which is not the identifier of any process, so the algorithm is wrong. $\square$ So the saturation method is optimal up to a factor of at most 4, and of 2 when all processes start.
- **Time.** In the explicit form, the process farthest from the leader is at distance at least $d/2$ and must receive a chain of messages that starts at the leader, so the time is $\Omega(d)$ when each message takes one time unit.
- **Contrast with cycles.** On rings and complete networks, election needs $\Omega(n \log n)$ messages; see the [ring election lower bound](/ring-election-lower-bound/). The cycles let messages go round, but also force the algorithm to break symmetry between many candidates.

## Reductions

- **From general graphs.** Election on any connected graph reduces to building a [spanning tree](/distributed-spanning-tree/) and running tree election on it, at a cost of $O(n)$ extra messages. If the spanning tree is built by [Gallager, Humblet and Spira](/gallager-humblet-spira/), the total is $O(m + n \log n)$ messages, which is the bound of [Awerbuch's algorithm](/awerbuch-leader-election/) for general networks.
- **To aggregation.** The report phase computes any value that can be combined from parts, such as the maximum, the sum or the size $n$, and the announcement phase spreads it. Election is the case of the maximum.
- **To the centre.** Finding the [centre of a tree](/tree-center/) uses the same report phase with heights instead of identifiers.

## Applications

- **Networks that are trees**, such as some sensor and hierarchical networks, where a coordinator must be chosen.
- **The last step of election in general networks**, after a spanning tree is built.
- **Choosing a root** for [convergecast](/convergecast/) and broadcast on a tree, or a process to start a protocol.

## References
