---
tag: 2BCNZB
kind: algorithm
slug: gallager-humblet-spira
name: Gallager-Humblet-Spira algorithm
aliases:
- GHS algorithm
- GHS
area: distributed/distributed-graph-algorithms
level: advanced
summary: The first distributed MST algorithm. Fragments with levels merge along their minimum outgoing edges; at most 5n log2 n + 2m messages and O(n log n) time in the asynchronous model.
solves: [distributed-mst]
model: asynchronous-model
complexity:
  vars: {n: the number of nodes, m: the number of edges}
  time: {worst: O(n log n)}
  messages: {worst: O(m + n log n)}
  space: {extra: O(Δ)}
properties: {deterministic: true, recursive: false}
history:
  year: 1983
  people: [Robert G. Gallager, Pierre A. Humblet, Philip M. Spira]
  note: Published in ACM TOPLAS in 1983 after a 1979 MIT report. The authors received the Dijkstra Prize in 2004 for it.
prereqs: [minimum-spanning-tree, cut-property, boruvka, asynchronous-model, message-complexity]
see_also: [distributed-mst, peleg-rubinovich-lower-bound, awerbuch-leader-election, complete-network-leader-election, distributed-spanning-tree, convergecast, synchronizer, kruskal]
sources:
  - paper: doi:10.1145/357195.357200
    title: Robert G. Gallager, Pierre A. Humblet and Philip M. Spira, A distributed algorithm for minimum-weight spanning trees, ACM Transactions on Programming Languages and Systems 5(1), 1983
    locator: pages 66 to 77 (Section 3 the algorithm and the deadlock argument, Section 4 the message count 5N log2 N + 2E, Section 5 the timing analysis, the appendix with responses (1) to (12))
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Section 4.4 (SynchGHS, the synchronous version) and Section 15.5 (the asynchronous GHS algorithm and its analysis)
  - paper: "Gopal Pandurangan, Peter Robinson and Michele Scquizzato, The distributed minimum spanning tree problem, Bulletin of the EATCS 125, 2018"
    locator: Section 4.1 (an overview of GHS as a distributed Borůvka) and Table 1 (later algorithms)
---

The Gallager-Humblet-Spira algorithm, or GHS, computes the [minimum spanning tree](/minimum-spanning-tree/) of a network in the [asynchronous model](/asynchronous-model/). Each node knows only the weights of its own edges, and at the end each node knows which of its edges are in the tree. Like [Borůvka's algorithm](/boruvka/), it grows fragments of the tree and merges them along minimum outgoing edges, but it gives each fragment a *level* so that merges need no global clock. It sends at most $5n \log_2 n + 2m$ messages of $O(\log n)$ bits, and it was the first distributed algorithm for the [distributed MST problem](/distributed-mst/).

## In plain words

Each computer in a network knows only the cables at its own ports and the price of each cable. The goal is to keep the cheapest set of cables that still connects everyone.

At first, each computer is a group of its own. A group looks for its cheapest cable to an outside computer, and it joins with the group at the other end. A known fact about these trees says that this cable is always safe to keep.

There is no common clock, so each group has a rank. Two groups of the same rank that pick the same cable join, and the rank goes up by one. A group of lower rank joins a group of higher rank at once. A question from a group of higher rank waits until the other group catches up. Ranks grow slowly, so each computer takes part in few searches.

## The problem

The network is a connected undirected graph $G = (V, E)$ with $n = |V| \ge 2$ nodes and $m = |E|$ edges. Each edge $e$ has a weight $w(e)$, and the weights are distinct, so the MST $T$ is unique ([MST uniqueness](/mst-uniqueness/)). The paper makes weights distinct by appending the identifiers of the endpoints, which costs $2m$ extra messages if the nodes do not know their neighbours' identifiers.

The model: a node knows the weights of its incident edges and nothing else. It does not need to know $n$, and it needs no identifier. Channels are reliable and FIFO: messages on one edge in one direction arrive in the order they were sent, after a finite but unbounded delay. Any nonempty set of nodes wakes up on its own, and a sleeping node wakes up when the first message arrives. There are no failures. The output: each node marks each incident edge as in $T$ (Branch) or not (Rejected).

Notation on this page: $n$ nodes, $m$ edges, $D$ the hop diameter, $\Delta$ the maximum degree.

## The algorithm

A *fragment* is a subtree of $T$. Each fragment has a level $L \ge 0$ and a name, the weight of its *core* edge. A single node is a fragment of level 0. The *minimum outgoing edge* (MOE) of a fragment is its lightest edge to a node outside it. By the [cut property](/cut-property/), the MOE of a fragment is in $T$. Fragments combine by two rules:

- **Merge.** If fragments $F$ and $F'$ both have level $L$ and the same MOE $e$, they form a fragment of level $L + 1$ whose core is $e$.
- **Absorb.** If the MOE of $F$ leads to $F'$ and $\mathrm{level}(F) < \mathrm{level}(F')$, then $F$ joins $F'$ at once and takes its level and name.

In any other case, the fragment waits. A node keeps its state $SN \in \{$Sleeping, Find, Found$\}$, a state $SE[j] \in \{$Basic, Branch, Rejected$\}$ for each edge $j$, the level $LN$ and name $FN$ of its fragment as far as it knows them, and the variables of the search: in-branch (the edge toward the core), best-edge, best-wt, test-edge and find-count (the number of reports it still waits for). The code below is the appendix of the paper. "Defer" puts the message back at the end of the node's input queue, to be served again after the node's state changes.

```pseudo id=main
WAKEUP()                                        ▷ spontaneous, or on the first message
L1  m ← the adjacent edge of minimum weight
L2  SE[m] ← Branch; LN ← 0; SN ← Found; find-count ← 0
L3  send Connect(0) on m
on Connect(L) on edge j:
L4  if SN = Sleeping then WAKEUP()
L5  if L < LN then SE[j] ← Branch                 ▷ absorb the lower fragment
L6      send Initiate(LN, FN, SN) on j; if SN = Find then find-count ← find-count + 1
L7  else if SE[j] = Basic then defer the message  ▷ same level, j is not our MOE yet
L8  else send Initiate(LN + 1, w(j), Find) on j    ▷ merge: j is the new core
on Initiate(L, F, S) on edge j:
L9  LN ← L; FN ← F; SN ← S; in-branch ← j; best-edge ← nil; best-wt ← ∞
L10 for each i ≠ j with SE[i] = Branch: send Initiate(L, F, S) on i; if S = Find then find-count ← find-count + 1
L11 if S = Find then TEST()
TEST()
L12 if some adjacent edge is Basic then test-edge ← the lightest Basic edge
L13     send Test(LN, FN) on test-edge
L14 else test-edge ← nil; REPORT()
on Test(L, F) on edge j:
L15 if SN = Sleeping then WAKEUP()
    if L > LN then defer the message             ▷ cannot answer yet
L16 else if F ≠ FN then send Accept on j          ▷ j is outgoing
L17 else if SE[j] = Basic then SE[j] ← Rejected   ▷ same fragment
L18     if test-edge ≠ j then send Reject on j
L19     else TEST()
on Accept on edge j:
L20 test-edge ← nil; if w(j) < best-wt then best-edge ← j; best-wt ← w(j)
L21 REPORT()
on Reject on edge j:
L22 if SE[j] = Basic then SE[j] ← Rejected
L23 TEST()
REPORT()
L24 if find-count = 0 and test-edge = nil then SN ← Found
L25     send Report(best-wt) on in-branch
on Report(w) on edge j:
L26 if j ≠ in-branch then
L27     find-count ← find-count − 1; if w < best-wt then best-wt ← w; best-edge ← j
L28     REPORT()
L29 else if SN = Find then defer the message
L30 else if w > best-wt then CHANGE-ROOT()       ▷ the MOE is on this side of the core
L31 else if w = best-wt = ∞ then halt            ▷ no outgoing edge: the tree is done
CHANGE-ROOT()
L32 if SE[best-edge] = Branch then
L33     send Change-root on best-edge           ▷ walk toward the MOE
L34 else send Connect(LN) on best-edge
L35     SE[best-edge] ← Branch
on Change-root:
L36 CHANGE-ROOT()
```

**One search.** When a fragment of level $L$ is formed, the two ends of the core send Initiate$(L, F, \text{Find})$ through the fragment (line L10). Each node then tests its Basic edges in order of weight (lines L12 and L13). A Test is answered with Accept if the other end has a different name (line L16), and with Reject if it has the same name (lines L17 and L18). A node stops at its first Accept, because the edges are tested in increasing order. Reports flow back to the core (lines L24 to L28): each node reports the lightest outgoing edge in its subtree. The two core nodes exchange Reports over the core. The side with the lighter edge sends Change-root along the path to the MOE (line L30), and the node at the MOE sends Connect over it (line L34).

**Why Tests wait.** A node of a lower level may belong to a fragment whose name is out of date, because the Initiate of its new fragment has not reached it yet. So the answer is deferred until the receiver's level is at least the level of the test (line L15). After that, equal names mean the same fragment.

**Why Connects wait.** A Connect of the same level waits until the receiving fragment has chosen its own MOE (line L7). If it chooses the same edge, the edge is Branch on both sides, and line L8 makes it the core of a level $L + 1$ fragment. If it chooses another edge, it will connect elsewhere and its level will rise, and then the waiting Connect is an absorb.

## Example

The graph has 6 nodes and 8 edges: $01{:}3$, $12{:}1$, $23{:}6$, $34{:}2$, $45{:}5$, $05{:}4$, $14{:}7$, $25{:}8$ (endpoints and weight). All nodes wake at time 0, and each message takes exactly 1 time unit.

| time | event | fragments (level, name) |
|---|---|---|
| 0 | each node sends Connect(0) on its lightest edge: 0 on 3, 1 and 2 on 1, 3 and 4 on 2, 5 on 4 | six fragments of level 0 |
| 1 to 2 | $\{1, 2\}$ and $\{3, 4\}$ each chose the same edge: they merge over the cores 1 and 2 | $\{1,2\}$ (1, 1), $\{3,4\}$ (1, 2) |
| 2 | node 1 now has level 1 > 0: the waiting Connect of node 0 is an absorb | $\{0,1,2\}$ (1, 1) |
| 3 | node 0 absorbs node 5 in the same way | $\{0,1,2,5\}$ (1, 1), $\{3,4\}$ (1, 2) |
| 3 to 8 | Tests and Reports: the MOE of both fragments is the edge $45$ of weight 5. A Test from node 4 to node 5 waits until node 5 has level 1. | unchanged |
| 9 to 11 | Change-root goes $1 \to 0 \to 5$, and nodes 5 and 4 send Connect(1) on edge 45 | merge over the core 5 |
| 11 to 19 | the last search finds no outgoing edge; Report(∞) reaches both core nodes 4 and 5, which halt | $V$ (2, 5) |

The tree is $\{12, 34, 01, 05, 45\}$ with weights $\{1, 2, 3, 4, 5\}$, the same as [Kruskal's algorithm](/kruskal/). The run sends 54 messages: 8 Connect, 12 Initiate, 12 Test, 3 Reject, 5 Accept, 12 Report and 2 Change-root. The bound is $5 \cdot 6 \log_2 6 + 2 \cdot 8 \approx 93.5$. The run ends at time 19, under the time bound $5 n \log_2 n \approx 77.5$.

## Correctness

Three facts give correctness. The full proof is in [the proof page](proofs/correctness/).

1. **Every Branch edge is in $T$.** An edge becomes Branch only as the MOE of some fragment (lines L2, L5, L35). So by the cut property it is in $T$, if the search finds the true MOE.
2. **The search finds the true MOE.** The key invariant: a node's known level is at most the level of its fragment, and if the two levels are equal, the known name is the true name. A Test of level $L$ is answered only by a node with known level at least $L$, so Accept means a different fragment and Reject means the same fragment. A fragment absorbed after the search reported cannot hold a lighter outgoing edge.
3. **No deadlock.** Take a fragment of the lowest level whose MOE is the lightest among the MOEs of the fragments of that level. None of its Tests waits, and its Connect causes an absorb or a merge. So some fragment always makes progress.

A fragment of level $L$ has at least $2^L$ nodes, by induction: a merge joins two fragments of level $L - 1$. So levels never exceed $\log_2 n$, and the run ends with one fragment, which spans $G$. Its search finds no outgoing edge, and the two core nodes halt.

## Complexity

**Messages.** The count is from Section 4 of the paper.

- An edge is rejected at most once, and each rejection costs at most two messages (a Test and a Reject, or two crossing Tests). That gives at most $2m$ messages.
- At each level other than 0 and the last, a node receives at most one Initiate and one Accept, and it sends at most one Test that is accepted, one Report, and one Change-root or Connect. That is at most 5 messages per node per level, and there are at most $\log_2 n - 1$ such levels.
- At level 0 a node receives at most one Initiate and sends one Connect. At the last level it sends at most one Report. That is fewer than $5n$ messages.

The total is at most $5n(\log_2 n - 1) + 5n + 2m = 5n \log_2 n + 2m$. Each message has a type, at most one edge weight and one level, so it has $O(\log n)$ bits when the weights are polynomial in $n$. The algorithm thus runs in the [CONGEST model](/congest-model/). The bound $O(m + n \log n)$ matches the $\Omega(m)$ lower bound (each edge must carry a message when $n$ is unknown) up to the $n \log n$ term, which is needed in some networks.

**Time.** Assume that each message takes at most one time unit and that local work is free. If all nodes wake at time 0, the paper shows by induction on the level that all nodes reach level $\ell$ by time $5\ell n - 3n$, so the run ends by time $5n \log_2 n$. That is $O(n \log n)$, and some graphs need $\Theta(n \log n)$ time. If only one node wakes, Figure 2 of the paper is a graph that needs $n(n-1)$ sequential messages. So wake all nodes first: a [flooding](/flooding/) wake-up costs at most $n - 1$ time units and $2m$ messages.

**Space.** A node keeps a constant number of variables plus one state for each incident edge, so $O(\Delta)$ words.

## Properties

- **Asynchronous and event driven.** No clock, no round numbers, no knowledge of $n$ or of the identifiers.
- **Needs FIFO channels.** The proof uses FIFO order on each edge. For example, a node's Report must not overtake the Initiate that it answers.
- **Deterministic.** The tree is unique, so every schedule gives the same output. The message count and the time depend on the schedule.
- **Termination is known only at the core.** The two final core nodes halt. To tell all nodes, the core broadcasts over the tree, at a cost of $n - 1$ more messages.
- **Elects a leader.** One of the final core nodes, say the one with the larger identifier, is a leader. This is how GHS solves [leader election](/complete-network-leader-election/) in a general network with $O(m + n \log n)$ messages.

## Variants and improvements

- **SynchGHS.** In the synchronous model, all fragments search at the same time in phases of $O(n)$ rounds, with no levels: a distributed [Borůvka](/boruvka/). The [distributed MST](/distributed-mst/) page gives this version in CONGEST, in $O(n \log n)$ rounds.
- **Equal weights without the $2m$ extra messages.** The paper sketches a variant that names fragments by node identifiers and cancels some Connects.
- **Faster time.** Chin and Ting reached $O(n \log \log n)$ time, Gafni $O(n \log^* n)$ and Awerbuch $O(n)$ in 1987, all with $O(m + n \log n)$ messages. Awerbuch keeps the levels but makes a large fragment stop a small one from slowing it down. See [distributed MST](/distributed-mst/) for the table of later results, which reach $\tilde{O}(D + \sqrt{n})$ rounds.
- **Leader election.** [Awerbuch's election](/awerbuch-leader-election/) uses the same fragment and level scheme.

## When to use it

Use GHS when messages are expensive and there is no common clock: it is message optimal up to the $n \log n$ term and needs no [synchronizer](/synchronizer/). Use it also to build a spanning tree and elect a leader at the same time. When time matters and the diameter $D$ is small, GHS is slow: it can take $\Theta(n \log n)$ time even when $D = O(1)$. Then use a $\tilde{O}(D + \sqrt{n})$ algorithm from [distributed MST](/distributed-mst/), which is optimal up to polylog factors by the [Peleg-Rubinovich lower bound](/peleg-rubinovich-lower-bound/).

## Pitfalls

- **Answering a Test too early.** If line L15 is dropped and a node of lower level answers at once, it can send Accept to a node of its own new fragment, because it does not yet know the new name. Then a fragment connects to itself and makes a cycle.
- **Dropping the wait on Connect.** If line L7 always sends Initiate$(LN+1, \ldots)$, two fragments of level $L$ can merge although they chose different edges. Then a level $L + 1$ fragment need not have $2^{L+1}$ nodes, and the message bound fails.
- **Flushing messages only after a successful step.** In an implementation, a deferred Connect or Test can still wake the node (lines L4 and L15). The Connect of WAKEUP must be sent even though the first message waits, or the run deadlocks.
- **Non-FIFO channels.** With reordering, a Report can reach the core before an Initiate that should have raised the find-count, and the core reports too early.
- **Equal weights.** With equal weights, two fragments can choose different edges of the same weight and form a cycle. Break ties by the endpoint identifiers.

## Implementations

## History

Gallager, Humblet and Spira wrote the algorithm at MIT in 1979 and published it in 1983. It answered a question of Spira (1977) and Dalal (1977) on the communication cost of a distributed MST. The level idea and the bound $5n \log_2 n + 2m$ are from the paper, which also gives the deadlock argument as an outline and reports tests of a FORTRAN version. Lynch gives an asynchronous proof in her book (Section 15.5). The algorithm received the Dijkstra Prize in 2004. Its time bound was improved by Chin and Ting, by Gafni, and by Awerbuch (1987, $O(n)$), and the round-optimal line of work starts with Garay, Kutten and Peleg in 1993.

## References
