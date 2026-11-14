---
tag: SJ43AX
kind: algorithm
slug: dogleg-channel-routing
name: Dogleg channel routing
aliases:
- Deutsch dogleg router
area: cad/routing
level: core
summary: Deutsch's router that splits each multi-pin net at its pins into pieces that may take different tracks, which breaks some constraint cycles and can use fewer tracks.
solves: [channel-routing-problem]
model: word-ram
complexity:
  vars: {P: the number of pieces of nets, n: the number of columns, T: the number of tracks used}
  time: {worst: O(n + P log P + T (P + n))}
  space: {extra: Θ(P + n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1976
  people: [D. N. Deutsch]
  note: Deutsch presented the dogleg channel router at the 13th Design Automation Conference in 1976, together with a large test channel that became the standard benchmark of the field.
prereqs: [left-edge-algorithm]
see_also: [vertical-constraint-graph, channel-density, greedy-channel-router, yoshimura-kuh-algorithm, channel-routing-np-completeness, channel-routing-problem, switchbox-routing]
sources:
  - paper: "D. N. Deutsch, A dogleg channel router, Proceedings of the 13th Design Automation Conference, 425 to 433, 1976"
    locator: the cut of nets into pieces at their pin columns, the constraint graph of the pieces and the large test channel (general locator)
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 6, Detailed Routing, the section on channel routing (doglegs and the dogleg left-edge algorithm; general locator)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on detailed routing, the part on channel routing (the dogleg router; general locator)
  - paper: doi:10.1109/TCAD.1985.1270096
    title: Thomas G. Szymanski, Dogleg channel routing is NP-complete, IEEE Transactions on Computer-Aided Design 4(1), 31 to 41, 1985
    locator: the hardness of the fewest tracks when nets may dogleg
---

Dogleg channel routing extends the [left-edge algorithm](/left-edge-algorithm/) by letting a net change track. A *dogleg* is a jog of a net from one track to another in one column, with a short vertical wire. Deutsch's router allows doglegs only at the pin columns of the net. It cuts each net with pins in $k$ columns into $k - 1$ pieces, one between each two pin columns that follow each other, and treats each piece as a net of its own. The constraint graph is built on the pieces, and the pieces are placed with the left-edge scan. A cycle in the [vertical constraint graph](/vertical-constraint-graph/) of the nets can vanish in the graph of the pieces, and a long constraint path can split, so the channel can need fewer tracks. The method is a heuristic: it does not break every cycle, and it can also use more tracks than the left-edge algorithm.

## In plain words

In the left-edge method, each net is one long stick that must stay in one lane. Here, a net that has pins in many places is cut at its pins into short sticks. The short sticks of one net still touch at the pins, where a short wire across the corridor joins them, so each can sit in a different lane.

Short sticks fit into gaps that a long stick cannot use. They can also get around a rule that would force one net both above and below another, as long as the two demands come from different parts of the net.

Then the short sticks are packed into lanes with the left-edge method, the same as before.

## The problem

The input is a channel as on the page on the [channel routing problem](/channel-routing-problem/), in the reserved two-layer model with doglegs allowed at pin columns. For a net with pin columns $c_0 < c_1 < \cdots < c_{k-1}$, the pieces are $p_i = [c_i, c_{i+1}]$ for $0 \le i \le k - 2$. A net with pins in two columns has one piece.

The output is a track $t(p)$ for each piece, such that:

- two pieces of different nets on the same track have disjoint intervals;
- if column $c$ has net $a$ on top and net $b \ne a$ at the bottom, every piece of $a$ that holds $c$ is on a higher track than every piece of $b$ that holds $c$.

The wires follow: a trunk of each piece on its track on layer H, and in each pin column of a net, one branch on layer V from the pin past all the tracks of the pieces of that net that meet there. Where two pieces of a net on different tracks meet, the branch is the dogleg. The goal is a small number of tracks $T$.

## The algorithm

```pseudo id=main
DOGLEG(channel)
L1  cut each net into pieces at its pin columns; sort the pieces by left end, ties by net and index
L2  build the constraint graph G_p of the pieces;  t ← 0;  U ← all pieces, in this order
L3  while U is not empty do
L4      t ← t + 1;  last ← none;  lastnet ← none
L5      for each piece p of net x in U, in order do
L6          if (last is none or l_p > last or (l_p = last and x = lastnet)) and every parent of p in G_p has a track < t then
L7              t(p) ← t;  last ← r_p;  lastnet ← x
L8      remove from U the pieces placed on track t
L9      if no piece was placed on track t then return "cycle"
L10 return the tracks t(p)
```

The graph $G_p$ on line L2 has an edge $p \to q$ when some column $c$ has net $a$ on top and net $b \ne a$ at the bottom, $p$ is a piece of $a$ that holds $c$, and $q$ is a piece of $b$ that holds $c$. A pin column of a net is held by two of its pieces when it is an inner pin column, and both get the edge, because the dogleg wire in that column runs past both of their tracks.

Lines L3 to L9 are the scan of the left-edge algorithm. The only change is on line L6: a piece may start in the column where the last piece on the track ends, if both belong to the same net. Then the two pieces form one straight trunk.

## Example

Take the channel

| column | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- |
| top | 1 | 2 | 1 | 3 | 0 | 0 |
| bottom | 2 | 0 | 0 | 1 | 3 | 3 |

The nets have the intervals $I_1 = [1, 4]$, $I_2 = [1, 2]$ and $I_3 = [4, 6]$, and the density is 2. The vertical constraint graph of the nets is the path $3 \to 1 \to 2$, from columns 4 and 1. So without doglegs, nets 3, 1 and 2 need three different tracks in this order, and every routing without doglegs uses 3 tracks.

Line L1 cuts net 1 at column 3 into $(1, 0) = [1, 3]$ and $(1, 1) = [3, 4]$, and net 3 at column 5 into $(3, 0) = [4, 5]$ and $(3, 1) = [5, 6]$. Net 2 stays one piece $(2, 0) = [1, 2]$. The graph of the pieces has two edges: $(1, 0) \to (2, 0)$ from column 1, and $(3, 0) \to (1, 1)$ from column 4. The path is broken, because the two edges at net 1 now end at different pieces.

The order is $(1, 0), (2, 0), (1, 1), (3, 0), (3, 1)$.

| track | scan | placed |
| --- | --- | --- |
| 1 | $(1, 0)$ placed, last = 3; $(2, 0)$ blocked (parent on this track); $(1, 1)$ blocked (parent $(3, 0)$ not placed); $(3, 0)$ placed, last = 5; $(3, 1)$ starts at 5 and is of the same net, placed | $(1, 0), (3, 0), (3, 1)$ |
| 2 | $(2, 0)$ placed, last = 2; $(1, 1)$ placed | $(2, 0), (1, 1)$ |

The result has 2 tracks, which is the density. Net 1 runs on track 1 from column 1 to column 3, jogs down to track 2 in column 3, and goes on to column 4. In column 3 the dogleg runs from the top pin to track 2, and no other net has a pin there. In column 4 net 3 comes down to track 1 and net 1 comes up to track 2, so they do not meet.

**A cycle that doglegs break.** Take top pins $1, 1, 2$ and bottom pins $2, 0, 1$. The nets give $1 \to 2$ from column 1 and $2 \to 1$ from column 3, a cycle, so left-edge fails. Net 1 has pins in columns 1, 2 and 3, and its pieces are $[1, 2]$ and $[2, 3]$. The graph of the pieces is the path $(1, 0) \to (2, 0) \to (1, 1)$, and the scan routes the channel in 3 tracks.

**A cycle that doglegs do not break.** Take top pins $1, 2$ and bottom pins $2, 1$. Each net has pins in two columns only, so it is one piece, and the cycle stays. The method returns "cycle".

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Legal routing.** Pieces on one track are disjoint, except that pieces of one net may touch at a shared end. Every edge of $G_p$ is kept, so in every column the branch of the top net ends above the branch of the bottom net. Each net is connected through its pin columns.
- **Termination and cycles.** As for left-edge, each pass places a piece when $G_p$ is acyclic, and a pass that places nothing happens exactly when $G_p$ has a cycle.
- **The same as left-edge on two-pin nets.** If every net has pins in two columns, each net is one piece, $G_p$ is the vertical constraint graph, and the result is that of the [left-edge algorithm](/left-edge-algorithm/).
- **Density bound.** The result never uses fewer than $d$ tracks, since the bound of the page on [channel density](/channel-density/) holds with doglegs.

## Complexity

- **Time.** A net with pins in $k$ columns gives $k - 1$ pieces, so $P$ is less than the number of pins. A column is held by at most two pieces of each net, so each column gives at most 4 edges of $G_p$, and $G_p$ has $O(n)$ edges. Building the pieces and $G_p$ in one sweep over the columns takes $O(n + P)$ time. Sorting takes $O(P \log P)$, and each pass of the scan takes $O(P + n)$. The total is $O(n + P \log P + T(P + n))$.
- **Space.** $\Theta(P + n)$ for the pieces, the graph and the tracks.

## Properties

- **What is proved.** The result is a legal routing with doglegs at pin columns, it is reported as "cycle" exactly when $G_p$ has a cycle, and it has at least $d$ tracks.
- **Not always better.** Take top pins $1, 2, 1, 2$ and bottom pins $0, 0, 0, 1$. Left-edge puts net 2 on track 1 and net 1 on track 2. The dogleg scan puts the first piece of net 1 on track 1, and then its second piece must go below net 2, so it uses 3 tracks.
- **What is only measured.** On 1000 random channels of 12 columns and 7 nets with an acyclic constraint graph, the dogleg scan used fewer tracks than the optimum without doglegs in 27, as many in 744, and more in 229. Against the left-edge algorithm, it was better in 58 and worse in 128. On a sample of small random channels whose constraint graph has a cycle, it routed about one third. These are tests on random cases, not bounds.
- **Why it can lose.** A dogleg holds its pin column on layer V across the tracks of both pieces. This adds constraints in that column, and a piece placed early on a high track can force the next piece of the same net lower.
- **Deterministic.** The order of line L1 fixes the result.

## Variants and improvements

- **Doglegs in any column.** Allow a net to change track wherever the column is free on layer V. The [greedy channel router](/greedy-channel-router/) works in this model.
- **Fewer cuts.** Cut a net only at the pin columns where a cut breaks a cycle or shortens a long path of the constraint graph, so that fewer vias are made.
- **Merging pieces.** The [Yoshimura-Kuh algorithm](/yoshimura-kuh-algorithm/) has a form with pieces at pin columns, where it merges pieces before the scan.
- **Both directions.** Fill tracks from the top and from the bottom, and keep the better result.

## When to use it

- When the constraint graph of the nets has a cycle or a long path, and the nets have pins in three or more columns.
- When vias are cheap, since every dogleg adds vias.

When the nets have only two pins each, the method is plain left-edge, and the [greedy channel router](/greedy-channel-router/) is the better choice for cycles.

## Pitfalls

- **Cutting at the wrong columns.** The cuts must be at the pin columns of the net. A cut between pin columns needs a free column on layer V there, which is a different model.
- **Missing edges at the dogleg column.** At an inner pin column, both pieces of the net hold the column, and both must get the edges of that column. With only one of them, the dogleg wire can cross the branch of the other net.
- **Pieces of one net on one track.** Two pieces of one net that share a column may lie on the same track. Treating them as different nets wastes tracks.
- **Expecting fewer tracks.** The dogleg form is not always better than left-edge. Run both and keep the better result.

## Implementations

## History

D. N. Deutsch presented the dogleg channel router at the 13th Design Automation Conference in 1976. The paper also gave a channel with density 19 that later papers call Deutsch's difficult example, and that served for years as the standard test of channel routers. In 1983 Burstein and Pelavin reported that their hierarchical router routed it in 19 tracks, and that the routers known to them needed 20 or more. Szymanski showed in 1985 that the fewest tracks with doglegs is NP-hard to find, so a fast exact dogleg router is not to be expected.

## References
