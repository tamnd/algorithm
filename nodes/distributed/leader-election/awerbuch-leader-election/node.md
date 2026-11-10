---
tag: ESZB9E
kind: algorithm
slug: awerbuch-leader-election
name: Awerbuch's election algorithm
aliases:
- Awerbuch's time-optimal election
- Election by minimum spanning tree
area: distributed/leader-election
level: advanced
summary: Election on any network by GHS-style fragment merging into a minimum spanning tree. O(m + n log n) messages; Awerbuch's changes to the merging cut the time from O(n log n) to O(n).
model: asynchronous-model
complexity:
  vars: {n: the number of processes, m: the number of links, Δ: the largest degree}
  time: {worst: O(n)}
  messages: {worst: O(m + n log n)}
  space: {extra: O(Δ)}
properties: {deterministic: true, recursive: false}
history:
  year: 1987
  people: [Baruch Awerbuch]
  note: Spanning tree, counting and election in general asynchronous networks with O(m + n log n) messages and O(n) time.
prereqs: [gallager-humblet-spira, minimum-spanning-tree, tree-election, message-complexity]
see_also: [gallager-humblet-spira, distributed-mst, distributed-spanning-tree, tree-leader-election, complete-network-leader-election, korach-kutten-moran, synchronizer, explicit-leader-election]
sources:
  - paper: doi:10.1145/28395.28421
    title: Baruch Awerbuch, Optimal distributed algorithms for minimum weight spanning tree, counting, leader election, and related problems, Proceedings of the 19th ACM Symposium on Theory of Computing (STOC), 1987
    locator: pages 230 to 240 (the algorithm with O(m + n log n) messages and O(n) time, and its use for counting and election)
  - paper: doi:10.1145/357195.357200
    title: Robert G. Gallager, Pierre A. Humblet and Philip M. Spira, A distributed algorithm for minimum-weight spanning trees, ACM Transactions on Programming Languages and Systems 5(1), 1983
    locator: pages 66 to 77 (fragments, levels, the test and reject rule, and the bound of 5n log n + 2m messages)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Section 4.4 (the synchronous form in phases) and Section 15.5 (the asynchronous GHS algorithm and its use for election)
---

Awerbuch's algorithm elects a leader on an arbitrary connected network in the [asynchronous model](/asynchronous-model/), with $O(m + n \log n)$ messages and $O(n)$ time, where $n$ is the number of processes and $m$ the number of links. It builds a [minimum spanning tree](/minimum-spanning-tree/) by merging fragments, as in the algorithm of [Gallager, Humblet and Spira](/gallager-humblet-spira/), and the process at the core of the last fragment is the leader. GHS already has the same message bound but takes $O(n \log n)$ time; Awerbuch changed the way fragments grow and wait for each other, which brings the time down to $O(n)$. This page gives the fragment-merging structure in full, in a form with global phases, with a proof of its message bound, and it describes Awerbuch's changes for the time as a sketch.

## In plain words

Every person in a network starts as a small team of one. In each round, every team looks for the cheapest link that leads out of the team, and it joins the team at the other end. Teams at least double in size each round, so after a few rounds there is only one team.

To find its cheapest outgoing link, a person tries their links from the cheapest up. If a link leads into their own team, they mark it as useless and never try it again. This is the trick that keeps the number of messages small.

When only one team is left, its head is the leader. Awerbuch's version also makes sure that no team waits too long for a slow neighbour, so the whole job ends in time that grows only in proportion to the number of people.

## The problem

The network is a connected graph with $n$ processes and $m$ links. Each process has a distinct identifier and knows its own links, but not the shape of the network. Channels are reliable. The goal is [explicit election](/explicit-leader-election/): exactly one process becomes the leader and every process learns its identifier.

To make election a spanning tree problem, give the link $\{u, v\}$ the weight $(\min(\mathrm{id}(u), \mathrm{id}(v)), \max(\mathrm{id}(u), \mathrm{id}(v)))$, compared in lexicographic order. All weights are distinct, so the minimum spanning tree is unique. The two ends of a link learn its weight when they exchange identifiers over it at the start, which costs $2m$ messages.

## The algorithm

A *fragment* is a set of processes joined by tree links, with one process as its *root*. The name of a fragment is the identifier of its root. In the form on this page, all fragments work in the same phase; the asynchronous algorithms replace global phases with fragment levels.

```pseudo id=main
FRAGMENT-ELECTION                                  ▷ the structure that GHS and Awerbuch share
L1  every process sends HELLO⟨id⟩ on all its links; it is a fragment of size 1 and its own root
L2  phase: the root sends INITIATE⟨name⟩ down the fragment tree
L3  each process tests its links that are not tree links and not rejected, in increasing weight:
      TEST⟨name⟩; the other end answers REJECT if it has the same name (both ends reject the link for good),
      else ACCEPT; the process stops at the first ACCEPT
L4  REPORT the smallest accepted weight up the tree; the root takes the minimum outgoing link (MOL)
L5  if there is no outgoing link then the root is the leader; it sends LEADER⟨id⟩ down the tree; stop
L6  the root sends CHANGE along the tree path to the end of its MOL, which sends CONNECT over it
L7  fragments joined by CONNECT links merge; on the link chosen from both sides, the end with the
      larger identifier is the new root; next phase
```

The leader is the root of the last fragment. It is the end with the larger identifier of the last link chosen from both sides, which need not be the largest identifier in the network.

## Example

Take 6 processes $p_0, \ldots, p_5$ with identifiers $4, 9, 2, 7, 5, 1$ and links $p_0p_1, p_0p_2, p_1p_2, p_1p_3, p_2p_4, p_3p_4, p_3p_5, p_4p_5$. The weights are $(4, 9), (2, 4), (2, 9), (7, 9), (2, 5), (5, 7), (1, 7), (1, 5)$.

| phase | what happens |
|---|---|
| 1 | Six fragments of size 1. Each process tests its lightest link and gets ACCEPT: $p_0$ and $p_2$ choose $p_0p_2$, $p_1$ chooses $p_1p_2$, $p_3$ chooses $p_3p_5$, $p_4$ and $p_5$ choose $p_4p_5$. The links $p_0p_2$ and $p_4p_5$ are chosen from both sides. Two fragments form: $\{p_0, p_1, p_2\}$ with root $p_0$, and $\{p_3, p_4, p_5\}$ with root $p_4$. |
| 2 | $p_0$ tests $p_0p_1$ and gets REJECT. $p_3$ tests $p_3p_4$, gets REJECT, then tests $p_1p_3$ and gets ACCEPT. $p_1$, $p_2$, $p_4$ get ACCEPT at once. Both fragments choose $p_2p_4$, weight $(2, 5)$. $p_0$ sends one CHANGE to $p_2$. The new root is $p_4$, since $5 > 2$. |
| 3 | One fragment. $p_1$ tests $p_1p_3$ and gets REJECT. No outgoing link is left, so $p_4$ is the leader and tells everyone. |

The tree is $p_0p_2, p_1p_2, p_2p_4, p_3p_5, p_4p_5$, the minimum spanning tree. The run sends 16 HELLO, 9 INITIATE, 13 TEST, 10 ACCEPT, 3 REJECT, 9 REPORT, 1 CHANGE, 8 CONNECT and 5 LEADER messages, 74 in all. The leader $p_4$ has identifier 5, not 9.

## Correctness

The [proof of correctness](proofs/correctness/) shows the following for the form with phases.

- **Fragments are parts of the minimum spanning tree.** The minimum outgoing link of a fragment belongs to the minimum spanning tree, by the cut property, so merging along such links keeps every fragment a subtree of it.
- **Each merged group has one root.** If $F$ fragments merge into one, they are joined by $F - 1$ links, and each of the $F$ fragments chose one of them, so exactly one link is chosen from both sides. Its end with the larger identifier is the only new root.
- **Rejecting is safe.** A link that joins two processes of the same fragment stays inside one fragment for ever, because fragments only grow. So it never needs to be tested again.
- **The end.** Every fragment that has an outgoing link merges with at least one other, so the number of fragments at least halves in each phase. When one fragment is left, its root finds no outgoing link and is the only leader.

## Complexity

**Messages.** There are at most $\lfloor \log_2 n \rfloor + 1$ phases, because the number of fragments halves. In a phase with $F$ fragments, the INITIATE, REPORT and CHANGE messages use each tree link at most once each, at most $n - F$ messages for each kind; each process has at most one accepted test, at most $2n$ messages; and there are $F$ CONNECT messages. So a phase sends at most $5n$ messages, besides the rejected tests. Each link is rejected at most once from each end, over the whole run, which costs at most $4m$ messages. With the $2m$ HELLO messages and the announcement, the total is at most

$$5n\left(\lfloor \log_2 n \rfloor + 1\right) + 6m + (n - 1) = O(m + n \log n).$$

This is the bound of GHS, up to the constant, and Awerbuch's algorithm keeps it.

**Time.** In the form with phases, a phase takes $O(n)$ time: the broadcasts and the convergecast go along paths of at most $n - 1$ links, and a process tests at most $n - 1$ links one after the other. So the time is $O(n \log n)$, the same as for GHS. Awerbuch's algorithm takes $O(n)$ time; see the sketch below.

**Space.** A process stores the state of each of its links (tree, rejected or not yet known), its fragment name, its parent and the best weight reported to it, so $O(\deg(v)) \subseteq O(\Delta)$ words, where $\Delta$ is the largest degree.

## Properties

- **Deterministic and works on every connected network.**
- **No knowledge of $n$ or $m$ is needed** by GHS; Awerbuch's algorithm first counts the processes, so it does not need $n$ either.
- **Explicit.** Every process learns the leader, and the minimum spanning tree is a by-product, with the leader as its root.
- **Optimal.** The paper calls the algorithm optimal in both measures. The $n \log n$ term and the $O(n)$ time cannot be improved in the worst case over networks with $n$ processes, because rings already need $\Omega(n \log n)$ messages and $\Omega(n)$ time; see the [ring election lower bound](/ring-election-lower-bound/). The $m$ term is needed by a separate argument for networks in which processes do not know their neighbours.

## Variants and improvements

**Awerbuch's changes for $O(n)$ time (sketch).** This outline follows the structure of the paper, but it leaves out the details and the proofs. In GHS, a fragment of level $L$ has at least $2^L$ processes, but it can have many more, and a large fragment can be held up by many small fragments of low level, which must catch up first. Over all levels this gives $O(n \log n)$ time. Awerbuch's algorithm works in three stages.

1. **Counting.** The processes first build a spanning tree and count themselves, so that every process knows $n$, within the same bounds on messages and time.
2. **Fragments up to size $n / \log n$.** GHS runs with an extra procedure that updates the level of a fragment when it grows, so that the level of a fragment matches its size. Then a fragment is never held up for long by fragments of much lower level, and this stage takes $O(n)$ time.
3. **The large fragments.** When fragments have at least $n / \log n$ processes, there are at most $\log n$ of them. In this stage, the paper adds a procedure that bounds, in terms of $2^L$, how far a fragment of level $L$ lets its tests go before it waits. This keeps each level to $O(2^L)$ time, and the sum over all levels is $O(n)$.

With the count $n$ known, the leader can be the root of the final tree, as in GHS.

- **[Gallager, Humblet and Spira](/gallager-humblet-spira/).** The base algorithm, with $5n \log_2 n + 2m$ messages and $O(n \log n)$ time. It was the first algorithm for a [distributed minimum spanning tree](/distributed-mst/) and gives election directly.
- **Election on a tree.** If a [spanning tree](/distributed-spanning-tree/) is known, [tree election](/tree-election/) uses only $O(n)$ more messages.
- **Complete networks.** On $K_n$, $m = \Theta(n^2)$, and the special algorithms of [Korach, Kutten and Moran](/korach-kutten-moran/) and [Afek and Gafni](/afek-gafni/) need only $O(n \log n)$ messages.
- **Later time bounds.** Later work on the distributed minimum spanning tree improved the time to depend on the diameter of the network rather than on $n$, with more messages in some cases.

## When to use it

Use it when the network is arbitrary and both the number of messages and the time matter, and when a minimum spanning tree is useful as well, for example for later broadcasts. On a ring or a complete network, the special algorithms for those networks are simpler. When only a spanning tree is needed and time matters more than messages, a [breadth-first search tree](/breadth-first-search-distributed/) from a known root is simpler.

## Pitfalls

- **Equal weights.** The fragments are parts of one minimum spanning tree only if all weights are distinct. Use identifiers to break ties, as this page does.
- **Testing a link twice.** A link that was rejected must be marked at both ends; otherwise the $4m$ term turns into $O(m \log n)$.
- **Answering a test too early.** In the asynchronous algorithm, a process of a lower level cannot know whether a test comes from its own fragment and must delay the answer until its level is high enough. The form with phases avoids this by finishing each INITIATE before tests start.
- **Mixing up the leader.** The leader is the final root, not the process with the largest identifier.

## Implementations

## History

Gallager, Humblet and Spira published their minimum spanning tree algorithm in 1983, with $O(m + n \log n)$ messages and $O(n \log n)$ time, and noted that it elects a leader. Other algorithms in the following years improved the time with the same number of messages. Baruch Awerbuch presented an algorithm at STOC in 1987 that reaches $O(n)$ time, with the same message bound, and used it for counting and for leader election.

## References
