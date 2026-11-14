---
tag: NN5MVW
kind: algorithm
slug: left-edge-algorithm
name: Left-edge algorithm
aliases:
- Hashimoto-Stevens algorithm
area: cad/routing
level: core
summary: Hashimoto and Stevens's channel router that sorts intervals by left end and fills each track greedily, which meets the density bound without vertical constraints.
solves: [channel-routing-problem]
model: word-ram
complexity:
  vars: {N: the number of nets, n: the number of columns, T: the number of tracks used}
  time: {worst: O(n + N log N + T (N + n))}
  space: {extra: Θ(N + n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1971
  people: [A. Hashimoto, J. Stevens]
  note: Hashimoto and Stevens gave the assignment of intervals to tracks in order of their left ends at the 8th Design Automation Workshop in 1971, for the wiring of large apertures between cells.
prereqs: [channel-routing-problem, channel-density, vertical-constraint-graph, interval-partitioning]
see_also: [interval-partitioning-greedy, interval-coloring-depth-theorem, dogleg-channel-routing, yoshimura-kuh-algorithm, greedy-channel-router, channel-routing-np-completeness, topological-sort, switchbox-routing]
sources:
  - paper: "A. Hashimoto and J. Stevens, Wire routing by optimizing channel assignment within large apertures, Proceedings of the 8th Design Automation Workshop, 155 to 169, 1971"
    locator: the assignment of trunks to tracks in order of their left ends (general locator)
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 6, Detailed Routing, the section on channel routing (the left-edge algorithm with vertical constraints; general locator)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on detailed routing, the part on channel routing (the basic and the constrained left-edge algorithm; general locator)
  - paper: "T. Yoshimura and E. S. Kuh, Efficient algorithms for channel routing, IEEE Transactions on Computer-Aided Design 1(1), 25 to 35, 1982"
    locator: the left-edge assignment as the last step after the merging of nets, and channels where it needs more tracks than the optimum (general locator)
---

The left-edge algorithm is the first channel router. It solves the [channel routing problem](/channel-routing-problem/) without doglegs: each net gets one trunk on one track. It fills the tracks one at a time from the top. On each track it runs through the nets in the order of their left ends, and it puts a net on the track when the net does not overlap the last net there and all the nets that must lie above it, by the [vertical constraint graph](/vertical-constraint-graph/), are already on higher tracks. When the channel has no vertical constraints, this is the greedy method for [interval partitioning](/interval-partitioning/), and it uses exactly $d$ tracks, the [channel density](/channel-density/), which is optimal. With vertical constraints it is a heuristic: it can use more tracks than needed, and it stops when the constraint graph has a cycle.

## In plain words

Think of the nets as sticks of different lengths laid along a ruler. Each lane of the channel can hold sticks that do not touch. Sort the sticks by where they start.

Fill the first lane: take the first stick, then the next stick that starts after it ends, and so on to the end of the ruler. Then fill the second lane with the sticks that are left in the same way, and go on until no stick is left.

Some sticks must lie in a lane above some others, because their pins face each other across the channel. A stick may go into the current lane only when all sticks that must be above it are already in higher lanes. If a whole lane stays empty, the rules contradict each other, and the method gives up.

## The problem

The input is a channel with columns $1, \ldots, n$ and a top and a bottom pin in each column, as on the page on the [channel routing problem](/channel-routing-problem/). Each net $x$ has the interval $[l_x, r_x]$ of columns from its first to its last pin. The vertical constraint graph $G_v$ has an edge $a \to b$ when some column has $a$ on top and $b$ at the bottom.

The output is a track $t(x) \in \{1, \ldots, T\}$ for each net, with track 1 at the top, such that:

- two nets on the same track have disjoint intervals;
- every edge $a \to b$ of $G_v$ has $t(a) < t(b)$.

From the tracks, the wires follow: a trunk of $x$ on track $t(x)$ from column $l_x$ to column $r_x$ on layer H, and a branch on layer V from each pin to the trunk. The goal is a small $T$.

## The algorithm

```pseudo id=main
LEFT-EDGE(nets x with intervals [l_x, r_x], constraint graph G_v)
L1  sort the nets by left end l_x, with ties broken by label
L2  t ← 0;  U ← all nets, in this order
L3  while U is not empty do
L4      t ← t + 1;  last ← none
L5      for each net x in U, in order do
L6          if (last is none or l_x > last) and every parent of x in G_v has a track < t then
L7              t(x) ← t;  last ← r_x
L8      remove from U the nets placed on track t
L9      if no net was placed on track t then return "cycle"
L10 return the tracks t(x)
```

Line L6 holds both rules. The test $l_x > \mathit{last}$ keeps the nets on a track disjoint. The intervals are closed, so a net that starts in the column where the last one ends must wait. The test on the parents keeps the vertical constraints. A parent that is not yet placed, or that is placed on the current track, blocks $x$ for this track.

## Example

Take the channel

| column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| top | 1 | 0 | 3 | 1 | 0 | 4 | 6 | 4 | 0 | 5 |
| bottom | 3 | 6 | 0 | 2 | 2 | 0 | 3 | 6 | 5 | 2 |

The intervals are $I_1 = [1, 4]$, $I_2 = [4, 10]$, $I_3 = [1, 7]$, $I_4 = [6, 8]$, $I_5 = [9, 10]$ and $I_6 = [2, 8]$. The local densities are 2, 3, 3, 4, 3, 4, 4, 3, 2, 2, so $d = 4$. The constraint graph has the edges $1 \to 2$, $1 \to 3$, $4 \to 6$, $5 \to 2$ and $6 \to 3$. Line L1 gives the order 1, 3, 6, 2, 4, 5.

| track | scan | placed |
| --- | --- | --- |
| 1 | 1 placed, last = 4; 3 blocked (parent 1 is on this track); 6 blocked (parent 4 not placed); 2 overlaps; 4 placed, last = 8; 5 placed | 1, 4, 5 |
| 2 | 3 blocked (parent 6 not placed); 6 placed, last = 8; 2 overlaps | 6 |
| 3 | 3 placed, last = 7; 2 overlaps | 3 |
| 4 | 2 placed | 2 |

The result uses 4 tracks, which is $d$, so it is optimal. The vertical constraints matter here. Without them, the same scan puts net 3 on track 2 and net 6 on track 3. Column 7 has net 6 on top and net 3 at the bottom, so the branch of 6 would come down to track 3 through the point where the branch of 3 leaves track 2, and the routing would be illegal.

**A channel where left-edge is not optimal.** Take

| column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| top | 5 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| bottom | 2 | 2 | 4 | 5 | 3 | 3 | 1 | 4 |

with $I_5 = [1, 4]$, $I_2 = [1, 2]$, $I_4 = [3, 8]$, $I_1 = [4, 7]$, $I_3 = [5, 6]$, edges $1 \to 5$ and $5 \to 2$, and $d = 3$. Left-edge puts net 4 on track 1, since it is the first net in order with no parent, and then nothing else fits there. It goes on with net 1 on track 2, nets 5 and 3 on track 3, and net 2 on track 4. That is 4 tracks. Three tracks are enough: net 1 on track 1, nets 5 and 3 on track 2, nets 2 and 4 on track 3. The greedy choice of net 4 for the top track is the mistake, because net 4 has no constraint and could go lower. The [Yoshimura-Kuh algorithm](/yoshimura-kuh-algorithm/) finds the 3-track routing.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Legal tracks.** On each track, the nets are placed in order of their left ends, and each starts after the right end of the one before, so their intervals are disjoint. Every net is placed only when its parents are on higher tracks, so every edge $a \to b$ has $t(a) < t(b)$.
- **Termination when $G_v$ is acyclic.** Some unplaced net has all its parents placed. The first such net in the order is placed on the next track, so each pass places at least one net, and the algorithm stops after at most $N$ passes.
- **Cycles are reported.** A net on a cycle is never placed, because one of its parents on the cycle is never placed before it. So when $G_v$ has a cycle, a pass places nothing and line L9 reports it. When $G_v$ is acyclic, line L9 never fires.
- **Density without vertical constraints.** If $G_v$ has no edges, a net on track $k$ was rejected on tracks $1, \ldots, k - 1$, each time because of a net on that track that holds its left end. So $k$ nets cross the column $l_x$, and $k \le d$. The [interval coloring depth theorem](/interval-coloring-depth-theorem/) gives the matching lower bound.

## Complexity

- **Time.** The intervals and the edges of $G_v$ come from one pass over the columns, in $O(n)$ time. Sorting takes $O(N \log N)$. Each pass of lines L5 to L8 looks at each unplaced net once and at each of its parents, in $O(N + n)$ time, since $G_v$ has at most $n$ edges. With $T$ passes, the total is $O(n + N \log N + T(N + n))$. In the worst case $T = N$ and this is quadratic.
- **No vertical constraints.** The track-by-track scan is not needed then. The one-pass form of [interval partitioning](/interval-partitioning-greedy/), which keeps the free tracks in a heap, gives a routing with $d$ tracks in $O(n + N \log N)$ time.
- **Space.** $\Theta(N + n)$ for the intervals, the graph and the tracks.

## Properties

- **What is proved.** Every result is a legal routing without doglegs. With no vertical constraints, it uses $d$ tracks, which is optimal. A cycle of $G_v$ is always reported.
- **What is only measured.** With vertical constraints, the track count is a heuristic result. On 1000 random channels of 12 columns and 7 nets with an acyclic $G_v$, left-edge matched the optimum without doglegs in 858 and used more tracks in 142. That is a test on small random cases, not a bound.
- **No doglegs.** It never splits a net, so a channel with a cyclic $G_v$ is out of its reach. [Dogleg channel routing](/dogleg-channel-routing/) extends it to pieces of nets.
- **Deterministic.** The order of line L1 and the fixed tie rule fix the result.
- **Track order.** Filling from the top is a choice. Filling from the bottom with the constraints reversed is the same method, and routers often try both and keep the better result.

## Variants and improvements

- **Basic left-edge.** Without vertical constraints, assign each net in order of left ends to any track whose last net ends before it. This is the greedy rule of [interval partitioning](/interval-partitioning-greedy/), and it gives $d$ tracks.
- **Constrained left-edge.** The form on this page, with the parent test of line L6.
- **Dogleg left-edge.** Split each net at its pin columns and apply the same scan to the pieces. This is [dogleg channel routing](/dogleg-channel-routing/).
- **Merging first.** The [Yoshimura-Kuh algorithm](/yoshimura-kuh-algorithm/) first merges nets into groups that share a track, chosen to keep the longest path of $G_v$ short, and then runs left-edge on the groups.
- **Both directions.** Fill tracks from the top and from the bottom at the same time, and pick at each step the side where the next net fits better.

## When to use it

- When a channel has no vertical constraints, for example when all pins are on one side, or each column has only one pin. Then the result is optimal.
- As a fast first try, or as the last step of a router that has already fixed the groups of nets on each track.
- To teach channel routing, since each step can be traced by hand.

When the constraint graph has a cycle, use [dogleg channel routing](/dogleg-channel-routing/) or the [greedy channel router](/greedy-channel-router/). When the track count matters, compare with the [Yoshimura-Kuh algorithm](/yoshimura-kuh-algorithm/).

## Pitfalls

- **Half-open intervals.** A net that starts in the column where another ends cannot share its track, because both need the point of that track in that column. The test must be $l_x > \mathit{last}$, not $l_x \ge \mathit{last}$.
- **Parents on the current track.** A parent placed earlier in the same pass is on track $t$, not above it. The test must be $t(p) < t$, or the two branches meet.
- **Assuming the density bound is met.** With vertical constraints, $d$ is only a lower bound, and the longest path of $G_v$ can be larger. Report the result against $\max(d, k_{\max})$, the larger of the two bounds.
- **Nets in one column.** A net with all pins in one column has no trunk. Leave it out, or it blocks a track for nothing.
- **Unbounded loop.** Without the check of line L9, a cyclic channel makes the algorithm open new tracks forever.

## Implementations

## History

A. Hashimoto and J. Stevens presented the method at the 8th Design Automation Workshop in 1971, the meeting that later became the Design Automation Conference. They treated the wiring between rows of cells as the assignment of intervals to tracks. The rule of taking the intervals in order of left ends gave the method its name. The same greedy rule appears in scheduling and in the coloring of interval graphs, where it is optimal. Channel routers of the 1970s added the vertical constraints in the form given here. Deutsch in 1976 applied the scan to pieces of nets to get around cycles, and Yoshimura and Kuh in 1982 merged nets before the scan to need fewer tracks.

## References
