---
tag: MQ0AC7
kind: algorithm
slug: yoshimura-kuh-algorithm
name: Yoshimura-Kuh algorithm
aliases:
- net merging channel router
area: cad/routing
level: advanced
summary: Channel routing that merges nets onto common tracks zone by zone, choosing merges that keep the longest path of the vertical constraint graph short, then runs left-edge.
solves: [channel-routing-problem]
model: word-ram
complexity:
  vars: {N: the number of nets, n: the number of columns}
  time: {worst: O(n N^2 (N + n))}
  space: {extra: Θ(N + n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1982
  people: [Takeshi Yoshimura, Ernest S. Kuh]
  note: Yoshimura and Kuh published the merging of nets on the zone representation of a channel in the first issue of the IEEE Transactions on Computer-Aided Design in 1982.
prereqs: [left-edge-algorithm, vertical-constraint-graph]
see_also: [channel-density, dogleg-channel-routing, greedy-channel-router, dag-longest-path, bipartite-matching, channel-routing-problem, channel-routing-np-completeness, interval-partitioning]
sources:
  - paper: "T. Yoshimura and E. S. Kuh, Efficient algorithms for channel routing, IEEE Transactions on Computer-Aided Design 1(1), 25 to 35, 1982"
    locator: the zone representation, the merging of nets that keeps the longest path of the vertical constraint graph short, and the form with bipartite matching (general locator)
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 6, Detailed Routing, the section on channel routing (zones and the vertical constraint graph; general locator)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on detailed routing, the part on channel routing (the Yoshimura-Kuh router and the merging of nets; general locator)
---

The Yoshimura-Kuh algorithm is a channel router without doglegs that decides first which nets share a track and only then which track each group gets. In the [left-edge algorithm](/left-edge-algorithm/), the nets that share a track are picked greedily from the left, and a poor pick can make a chain of vertical constraints longer than needed. Yoshimura and Kuh cut the channel into *zones*, the maximal sets of nets that cross one column, and scan the zones from left to right. At each boundary between zones, a net that has ended may be merged with a net that starts after it, if no path of the [vertical constraint graph](/vertical-constraint-graph/) joins them. Merged nets become one node of the graph and will share a track. Among the possible merges, the algorithm takes the one that keeps the longest path through the new node shortest. The groups then get their tracks by the left-edge rule.

## In plain words

Some nets must lie above others, and these rules form chains. A chain of five nets needs five lanes, however short the nets are. So the danger is that the lanes fill up in a way that makes the chains long.

Walk along the channel. Each time some nets end and new nets begin, pair an ending net with a starting net, so that the two will later share one lane. Do not pair two nets that a chain of rules puts one above the other, since they can never share a lane. Among the pairs that are allowed, take the pair that makes the longest chain through it as short as possible.

When the walk is over, place the pairs and groups into lanes as the left-edge method does.

## The problem

The input is a channel as on the page on the [channel routing problem](/channel-routing-problem/), with nets $x$, closed intervals $[l_x, r_x]$, and the vertical constraint graph $G_v$. The model is the reserved two-layer model without doglegs. The output is a track $t(x)$ for each net, with disjoint intervals on each track and $t(a) < t(b)$ for each edge $a \to b$ of $G_v$, or the answer that $G_v$ has a cycle. The goal is a small number of tracks $T$.

**Zones.** Let $S(c)$ be the set of nets that cross column $c$. A set $S(c)$ that is not contained in any other $S(c')$ is *maximal*. The zones $Z_1, Z_2, \ldots, Z_m$ are the different maximal sets, in the order of the columns where they occur. Each net lies in a run of consecutive zones, from its first zone to its last zone. The largest zone has $d$ nets, the [channel density](/channel-density/).

## The algorithm

```pseudo id=main
YOSHIMURA-KUH(channel)
L1  build G_v; if G_v has a cycle then return "cycle"
L2  compute the zones Z_1, ..., Z_m; each group is one net
L3  L ← ∅
L4  for i ← 1 to m - 1 do
L5      add to L the groups whose last zone is Z_i
L6      R ← the groups whose first zone is Z_{i+1}
L7      while some a in L and b in R have no path between them in G_v do
L8          take such a pair with the least cost max(u(a), u(b)) + max(d(a), d(b)) - 1, ties by label
L9          merge b into a in G_v; remove a from L and b from R
L10 assign tracks to the groups with the left-edge scan on G_v, a group spanning its nets
L11 return the track of each net, the track of its group
```

Here $u(v)$ is the number of nodes on a longest path of $G_v$ that ends at $v$, and $d(v)$ the number on a longest path that starts at $v$, both counted with $v$. After the merge of $a$ and $b$, the longest path through the new node has exactly the cost of line L8, so the rule picks the merge that keeps the paths through it shortest. Both numbers come from a [longest path](/dag-longest-path/) computation on the acyclic graph.

A merged group stays out of $L$ until its new last zone is reached, and then line L5 adds it again, so a group can take more nets at later boundaries. The groups in $R$ are always single nets, because a group made by a merge starts in an earlier zone.

## Example

Take the channel

| column | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| top | 5 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| bottom | 2 | 2 | 4 | 5 | 3 | 3 | 1 | 4 |

with $I_5 = [1, 4]$, $I_2 = [1, 2]$, $I_4 = [3, 8]$, $I_1 = [4, 7]$, $I_3 = [5, 6]$ and $d = 3$. The graph $G_v$ is the path $1 \to 5 \to 2$, and net 3 and net 4 have no edges. The [left-edge algorithm](/left-edge-algorithm/) uses 4 tracks here, because it puts net 4 alone on track 1.

The zones are $Z_1 = \{2, 5\}$ (columns 1 and 2), $Z_2 = \{1, 4, 5\}$ (column 4) and $Z_3 = \{1, 3, 4\}$ (columns 5 and 6). The path numbers are $u = 1, 3, 1, 1, 2$ and $d = 3, 1, 1, 1, 2$ for nets 1, 2, 3, 4, 5.

- **Boundary 1.** $L = \{2\}$, $R = \{1, 4\}$. Net 1 reaches net 2, so the pair $(2, 1)$ is out. The pair $(2, 4)$ costs $\max(3, 1) + \max(1, 1) - 1 = 3$. Merge: nets 2 and 4 form one group.
- **Boundary 2.** $L = \{5\}$, $R = \{3\}$. The pair $(5, 3)$ costs $\max(2, 1) + \max(2, 1) - 1 = 3$. Merge: nets 5 and 3 form one group.

The groups are $\{1\}$, $\{5, 3\}$ with span $[1, 6]$, and $\{2, 4\}$ with span $[1, 8]$, and the graph of the groups is the path $\{1\} \to \{5, 3\} \to \{2, 4\}$. The left-edge scan puts net 1 on track 1, nets 5 and 3 on track 2, and nets 2 and 4 on track 3. That is 3 tracks, which is optimal, since the density is 3.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Merged nets are disjoint.** When a net $a$ with last zone at most $Z_i$ is merged with a net $b$ with first zone $Z_{i+1}$, the interval of $a$ ends before the interval of $b$ starts. So all nets of a group fit on one track.
- **No cycles.** A merge of two nodes with no path between them keeps $G_v$ acyclic. So the scan of line L10 places every group.
- **Legal routing.** Groups on a track have disjoint spans, and every edge of $G_v$ between nets becomes an edge between their groups, which the scan keeps.
- **Cycles are reported.** If $G_v$ has a cycle, no routing without doglegs exists, and line L1 says so.

## Complexity

- **Time.** The zones come from one sweep over the columns, keeping only the sets $S(c)$ that are maximal, in $O(n + N^2)$ time with sets of nets. In this version, each try of line L7 recomputes $u$ and $d$ in $O(N + n)$ and tests each pair by a search in $O(N + n)$. There are at most $N$ merges and $m - 1 < n$ boundaries, and each try looks at fewer than $N^2$ pairs, so the time is $O(n N^2 (N + n))$. A reachability matrix updated after each merge makes the test of a pair $O(1)$.
- **Space.** $\Theta(N + n)$ for the graph, the zones as runs of indices, and the groups.

## Properties

- **What is proved.** The result is a legal routing without doglegs whenever $G_v$ is acyclic. It has at least $\max(d, k)$ tracks, where $k$ is the number of nets on a longest path of $G_v$.
- **What is only measured.** The track count. On 1000 random channels of 12 columns and 7 nets with an acyclic $G_v$, this version matched the optimum without doglegs in 980 and used more tracks in 20. It used fewer tracks than left-edge in 133 and more in 11. These are tests on small random cases, not bounds.
- **Not always better than left-edge.** The merges are greedy, one boundary at a time, and a merge that is cheap now can block a better one later.
- **No doglegs.** On a cyclic $G_v$ it fails, like left-edge. The form with doglegs below works on pieces of nets.

## Variants and improvements

- **Merging by matching.** Yoshimura and Kuh also give a form in which the merges at each boundary come from a [bipartite matching](/bipartite-matching/) between $L$ and $R$, with weights that favor pairs on long paths. It looks at all pairs of a boundary at once.
- **Doglegs at pin columns.** Cut the nets into pieces at their pin columns, as in [dogleg channel routing](/dogleg-channel-routing/), and merge the pieces. This can break cycles of $G_v$.
- **Looking ahead.** Cost functions that also count the nets still to come, so that a merge does not use up a net that a later boundary needs.

## When to use it

- When $G_v$ is acyclic and has long paths, so that left-edge wastes tracks.
- When doglegs are not wanted, for example to keep the number of vias small.

When $G_v$ has a cycle, use [dogleg channel routing](/dogleg-channel-routing/) or the [greedy channel router](/greedy-channel-router/). When $G_v$ has no edges, the [left-edge algorithm](/left-edge-algorithm/) is already optimal.

## Pitfalls

- **Merging nets joined by a path.** Two nets with a path between them in $G_v$ need different tracks. Merging them makes a cycle, and the scan fails.
- **Zones that are not maximal.** A set $S(c)$ inside another one is not a zone. Keeping it gives extra boundaries and wrong first and last zones.
- **Stale path numbers.** $u$ and $d$ change after every merge, because the merged node has the edges of both nets. Recompute them, or update them, before the next choice.
- **Spans of groups.** The span of a group is from the left end of its first net to the right end of its last net. The scan of line L10 must use these spans, not the intervals of single nets, or two groups can overlap on a track.

## Implementations

## History

Takeshi Yoshimura and Ernest S. Kuh published the method in 1982, in the first issue of the IEEE Transactions on Computer-Aided Design. They took the vertical constraint graph and the zone representation of the channel as the main objects, and merged nets to keep the longest path of the graph short, since that path bounds the tracks from below when there are no doglegs. Their paper gave a merge rule based on path lengths and a second one based on bipartite matching, and a form with pieces of nets. Szymanski showed in 1985 that the general problem with doglegs is NP-complete, and LaPaugh had shown the same in 1980 for the problem without doglegs, so such heuristics remained the practical approach.

## References
