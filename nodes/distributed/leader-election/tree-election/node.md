---
tag: 5X8NA5
kind: algorithm
slug: tree-election
name: Tree election by saturation
aliases:
- Saturation election on trees
area: distributed/leader-election
level: core
summary: Election on an asynchronous tree. Messages flow in from the leaves until two neighbours meet; they know the largest id and send it back out. 3n + k − 4 messages for k starters.
solves: [tree-leader-election]
model: asynchronous-model
complexity:
  vars: {n: the number of processes, k: the number of processes that start on their own, d: the diameter of the tree}
  time: {worst: O(d)}
  messages: {worst: O(n)}
  space: {extra: O(Δ)}
properties: {deterministic: true, recursive: false}
prereqs: [tree, asynchronous-model, convergecast, message-complexity]
see_also: [tree-leader-election, echo-algorithm, convergecast, explicit-leader-election, tree-center, floodmax, distributed-spanning-tree, broadcast-problem]
sources:
  - book: isbn:9780471719977
    title: Nicola Santoro, Design and Analysis of Distributed Algorithms, Wiley, 2007
    locator: Chapter 2 (wake-up and the saturation technique on trees, with its message count) and Chapter 3 (election in trees by saturation)
  - book: isbn:9780521794831
    title: Gerard Tel, Introduction to Distributed Algorithms, second edition, Cambridge University Press, 2000
    locator: Chapter 6 (the tree algorithm, in which two neighbours decide) and Chapter 7 (election with the tree algorithm and a wake-up phase)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 2 (convergecast and broadcast on spanning trees)
---

Tree election by saturation elects a leader on a network that is a [tree](/tree/), in the [asynchronous model](/asynchronous-model/), with $O(n)$ messages. Each process waits until it has heard from all its neighbours but one, then sends the largest identifier it knows to that last neighbour. The messages move in from the leaves, and they meet on exactly one link: its two ends are *saturated*, they both know the largest identifier, and they send it back out to everyone. With $k$ processes that start on their own, the algorithm sends exactly $3n + k - 4$ messages, or $2n - 2$ when all processes start. This page gives the algorithm and its proof; the [tree election problem](/tree-leader-election/) page gives the problem, the lower bound and the other methods.

## In plain words

The people in a group are linked by phone lines, and there are no loops in the lines. Each person has a different number. First, anyone who is awake calls all their contacts to wake them up.

A person with only one contact sends their number to that contact. Any other person waits until all their contacts but one have reported, and then sends the biggest number they have heard of to the last one. In this way the reports move inwards from the edges of the group.

At some point two people who are linked send reports to each other at the same time. Each of them has now heard from everyone, so each knows the biggest number. They pass that number back outwards, and the person who owns it is the leader.

## The problem

The network is a tree with $n \ge 1$ processes and $n - 1$ links. Each process knows its own identifier and its links, but not $n$ and not the shape of the tree. Identifiers are distinct. Channels are reliable and need not be FIFO. Any nonempty set of processes starts on its own, at any times; the others start when the first message reaches them. The goal is [explicit leader election](/explicit-leader-election/): exactly one process becomes the leader, and every process learns its identifier. The algorithm elects the process with the largest identifier.

## The algorithm

Each process $p$ has a set $N(p)$ of neighbours, a value $\mathit{best}$, a set $\mathit{heard}$ of neighbours that have reported, a $\mathit{parent}$ and a state in *asleep*, *awake*, *processing*, *saturated*. Three kinds of messages are used: $\mathrm{WAKE}$, $\langle \mathrm{M}, x \rangle$ to report, and $\langle \mathrm{L}, x \rangle$ to announce.

```pseudo id=main
TREE-ELECTION at process p                ▷ the same code at every process
L1  on start, or on the first message while asleep (from q): state ← awake; best ← id(p); heard ← ∅;
      send WAKE to every neighbour except q
L2    if |N(p)| = 1 then parent ← the neighbour; send ⟨M, best⟩ to parent; state ← processing
L3  on ⟨M, x⟩ from q: best ← max(best, x); heard ← heard ∪ {q}
L4    if state = awake and |N(p) \ heard| = 1 then parent ← the neighbour in N(p) \ heard;
        send ⟨M, best⟩ to parent; state ← processing
L5    else if state = processing then state ← saturated; leader ← best;
        send ⟨L, best⟩ to every neighbour except parent
L6  on ⟨L, x⟩ from q: leader ← x; send ⟨L, x⟩ to every neighbour except q
L7  on any message: a WAKE that reaches an awake process is ignored; status ← leader if leader = id(p), else non-leader
```

A process that is woken by a message runs line L1 and then handles that message. A process with no neighbours, $n = 1$, is saturated at once and is the leader. If every process starts on its own, the $\mathrm{WAKE}$ messages can be left out, and the count drops by $n + k - 2$.

## Example

Take the tree with links $p_0p_1$, $p_1p_2$, $p_1p_3$, $p_3p_4$, $p_3p_5$, $p_5p_6$, $p_6p_7$ and identifiers $4, 9, 2, 5, 7, 1, 3, 6$ for $p_0, \ldots, p_7$. All processes start at time 0, so no $\mathrm{WAKE}$ is sent, and every message takes one time unit.

| time | events |
|---|---|
| 0 | The leaves $p_0, p_2, p_4, p_7$ send $\langle \mathrm{M}, 4 \rangle$, $\langle \mathrm{M}, 2 \rangle$, $\langle \mathrm{M}, 7 \rangle$, $\langle \mathrm{M}, 6 \rangle$. |
| 1 | $p_1$ has heard from $p_0$ and $p_2$ and sends $\langle \mathrm{M}, 9 \rangle$ to $p_3$. $p_3$ has heard from $p_4$ only and waits. $p_6$ sends $\langle \mathrm{M}, 6 \rangle$ to $p_5$. |
| 2 | $p_3$ has heard from $p_4$ and $p_1$ and sends $\langle \mathrm{M}, 9 \rangle$ to $p_5$. $p_5$ has heard from $p_6$ and sends $\langle \mathrm{M}, 6 \rangle$ to $p_3$. |
| 3 | The two reports cross on the link $p_3p_5$. Both ends are saturated with $\mathit{best} = 9$. $p_3$ sends $\langle \mathrm{L}, 9 \rangle$ to $p_1$ and $p_4$, and $p_5$ sends it to $p_6$. |
| 4 | $p_1$ learns that it is the leader and sends $\langle \mathrm{L}, 9 \rangle$ to $p_0$ and $p_2$. $p_6$ sends it to $p_7$. |
| 5 | The last announcements arrive. |

There are 8 reports and 6 announcements, $14 = 2n - 2$ messages. If only $p_0$ starts, 7 $\mathrm{WAKE}$ messages are added, $21 = 3n + 1 - 4$ in all, and with that timing the saturated link is $p_6p_7$. The saturated link depends on the timing; the leader does not.

## Correctness

The [proof of correctness](proofs/correctness/) shows the following.

- **Everyone wakes up.** A process that wakes sends $\mathrm{WAKE}$ to all its other neighbours, and the tree is connected.
- **Every process sends exactly one report.** It sends one at most, because it leaves the state *awake* when it does. If some processes never sent one, take such a process $u$: each neighbour that has not reported to $u$ also has no report from $u$, so it has not sent one either. These processes would form a nonempty part of the tree in which each has at least two neighbours, which a finite tree does not have.
- **Exactly one link carries two reports.** No link carries none: if neither end of a link reported over it, each end heard from the other, which is false. There are $n$ reports and $n - 1$ links. A process becomes saturated exactly when it gets a report from its own parent, that is, over a link that carries two reports. So exactly two processes are saturated, and they are neighbours.
- **The value is right.** A report from $u$ to its parent carries the largest identifier in the part of the tree on $u$'s side of the link. A saturated process has reports from all its neighbours, so its $\mathit{best}$ is the largest identifier of the tree. The announcements carry it to every other process, each of which gets exactly one.

## Complexity

**Messages.** Let $k \ge 1$ be the number of processes that start on their own, before any message reaches them. Each of them sends $\mathrm{WAKE}$ on all its links, and each other process on all links but the one it was woken by, so the number of $\mathrm{WAKE}$ messages is $2(n - 1) - (n - k) = n + k - 2$. There are exactly $n$ reports and $n - 2$ announcements. In total, for $n \ge 2$,

$$\underbrace{(n + k - 2)}_{\text{wake-up}} + \underbrace{n}_{\text{reports}} + \underbrace{(n - 2)}_{\text{announce}} = 3n + k - 4 \le 4n - 4.$$

Without the wake-up phase the count is $2n - 2$. The tests check these numbers exactly on 950 random trees with random sets of starters, in random and in lock-step schedules.

**Time.** With every message taking at most one time unit and the first start at time 0, every process is awake by time $d$, the last report is sent by time $2d$, the saturated pair forms by time $2d + 1$, and the announcements take at most $d$ more units. So the time is at most $3d + 1 = O(d)$.

**Space.** A process stores a value and a set of at most $\deg(p)$ neighbours, where $\Delta$ is the largest degree. Messages carry one identifier.

## Properties

- **Deterministic and asynchronous.** Correct under every schedule, with or without FIFO channels.
- **No knowledge of $n$ is needed**, and the processes need not know which of them start.
- **Explicit.** Every process learns the leader's identifier.
- **The saturated pair is a by-product.** The two saturated processes are a natural pair of coordinators, and the reports could carry any function that can be combined piece by piece, such as a sum or a minimum, not only the maximum.
- **Message optimal up to a constant.** Explicit election on a tree needs at least $n - 1$ messages, as shown on the [problem page](/tree-leader-election/).

## Variants and improvements

- **Elect a saturated process.** The two saturated processes can elect one of themselves, for example the one with the larger identifier, without computing the maximum of the tree.
- **Find the centre.** If the reports carry the height of the subtree instead of an identifier, the saturated pair can compute where the [centre](/tree-center/) of the tree lies and send a message along the path to it. This elects a centre, as the [leaf peeling method](/tree-center-leaf-peeling/) does sequentially.
- **The tree algorithm.** Tel presents the same report phase as a wave algorithm, in which the two processes that decide are neighbours, and uses it for election after a wake-up phase.
- **[Echo](/echo-algorithm/) from one starter.** If exactly one process starts, a wave out and a [convergecast](/convergecast/) back also elect the largest identifier, with $2(n - 1)$ messages plus $n - 1$ to announce.
- **General graphs.** On a graph with cycles, first build a spanning tree, for example with the algorithm of [Gallager, Humblet and Spira](/gallager-humblet-spira/), then run this algorithm on it.

## When to use it

Use it when the network is a tree, or when a [spanning tree](/distributed-spanning-tree/) of the network is already known and any process may start. It needs no knowledge of $n$, uses a linear number of short messages and finishes in time proportional to the diameter. On a ring or a general graph it does not apply directly, because there are cycles.

## Pitfalls

- **Sending to the wrong neighbour.** A process must report to the one neighbour it has not heard from. If it reports earlier, two reports can meet in the middle of a long path before the ends have reported, and the saturated pair does not know the maximum.
- **Forgetting the wake-up.** If only some processes start and a sleeping leaf never wakes, its report is never sent and the algorithm stops with no leader.
- **Treating a woken process as a starter.** A process that a message wakes must not send $\mathrm{WAKE}$ back on that link; otherwise the count grows.
- **Expecting a fixed saturated pair.** The saturated link depends on the timing. Only the elected process, the one with the largest identifier, is fixed.

## Implementations

## History

The idea of collecting information from the leaves of a tree until two neighbours meet is old and appears in many early algorithms for trees, such as the tree algorithm that Tel presents among wave algorithms. Santoro made saturation a named basic technique, used it for election, for finding the centre and for other problems on trees, and counted its messages exactly. This page follows Santoro's form, with a wake-up phase, and elects the largest identifier.

## References
