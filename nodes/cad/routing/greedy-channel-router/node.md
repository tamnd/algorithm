---
tag: N38E4M
kind: algorithm
slug: greedy-channel-router
name: Greedy channel router
aliases:
- Rivest-Fiduccia router
area: cad/routing
level: core
summary: Rivest and Fiduccia's router that scans the channel column by column and greedily joins, splits and jogs nets, and always completes by extending past the end.
solves: [channel-routing-problem]
model: word-ram
complexity:
  vars: {n: the number of columns, E: the number of extension columns, T: the number of tracks used, N: the number of nets}
  time: {worst: O((n + E) T^2)}
  space: {extra: Θ(T + N)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1982
  people: [Ronald L. Rivest, Charles M. Fiduccia]
  note: Rivest and Fiduccia presented the greedy channel router at the 19th Design Automation Conference in 1982. It routes one column at a time and adds columns past the right end when nets are still split.
prereqs: [channel-routing-problem, channel-density]
see_also: [left-edge-algorithm, dogleg-channel-routing, yoshimura-kuh-algorithm, vertical-constraint-graph, switchbox-routing, greedy-algorithm, channel-routing-np-completeness, detailed-routing]
sources:
  - paper: "R. L. Rivest and C. M. Fiduccia, A greedy channel router, Proceedings of the 19th Design Automation Conference, 418 to 424, 1982"
    locator: the steps of the router in each column, its parameters and its results on benchmark channels (general locator)
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 6, Detailed Routing, the section on channel routing (the greedy channel router; general locator)
  - book: isbn:9780792383932
    title: Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, third edition, Kluwer, 1999
    locator: the chapter on detailed routing, the part on channel routing (the greedy channel router and its steps; general locator)
  - paper: "W. K. Luk, A greedy switch-box router, Integration, the VLSI Journal 3(2), 129 to 149, 1985"
    locator: the extension of the column scan to pins on all four sides (general locator)
---

The greedy channel router solves the [channel routing problem](/channel-routing-problem/) by a scan from left to right, one column at a time. Unlike the [left-edge algorithm](/left-edge-algorithm/), it does not assign whole nets to tracks. It keeps, for each track, the net that runs on it at the current column, and in each column it makes a few local moves: it brings the pins of the column onto tracks, joins the tracks of nets that are split over several tracks, moves nets toward the side of their next pin, and frees the tracks of nets that are done. A net may change track in any column where the vertical layer is free. If nets are still split after the last column, the router goes on in extra columns past the right end. So it always finishes, also when the [vertical constraint graph](/vertical-constraint-graph/) has a cycle. The number of tracks is a measured result, not a proved one.

## In plain words

Walk along the corridor from one end to the other, one step at a time. At each step, you hold the ropes that are already laid in their lanes.

When a door on the north or south wall comes up, bring its rope into the nearest lane that is free or already holds a rope of that color. If a color sits in two lanes, join the two lanes with a short rope across the corridor as soon as the way is clear, and free one lane. If a rope must reach a door on the south wall soon, move it to a lane near the south wall when you can.

When a color has no doors left, free its lane. If at the end of the corridor some color still sits in two lanes, keep walking past the end until they are joined.

## The problem

The input is a channel with columns $1, \ldots, n$ and a top and a bottom pin in each column, as on the page on the [channel routing problem](/channel-routing-problem/). The model is the reserved two-layer model with jogs in any column: trunks run on tracks on layer H, and vertical wires on layer V, and a net may use vertical wires in any column, not only at its pins. Wires may also go on to the right of column $n$, in *extension columns* that hold no pins.

The output is a legal routing, with its number of tracks $T$ and its number of extension columns $E$. The goal is a small $T$ with $E = 0$, but the router puts completion first.

## The algorithm

```pseudo id=main
GREEDY-CHANNEL(top, bot)
L1  make d empty tracks, where d is the channel density;  c ← 1
L2  while c ≤ n or some track holds a net do
L3      bring in the pins of column c: each goes to the nearest track, from its own edge, that is empty or holds its net; if the two branches would meet, the shorter one stays and the other pin gets a new track at the edge of its side
L4      join split nets: add vertical jogs in column c between tracks of the same net, shortest first, where layer V is free; in each joined set keep the track on the side of the next pin and free the others
L5      move nets: each net on one track jogs toward the side of its next pin, to the farthest empty track it can reach in column c
L6      free the track of each net that is on one track and has no pin to the right of c
L7      c ← c + 1
L8  remove the tracks that hold no trunk and number the rest from the top
L9  return the tracks, the wires and E, the number of columns past n
```

The order of the steps follows Rivest and Fiduccia. Line L3 makes the connections that column $c$ forces. Line L4 frees tracks, which is the main way to keep the width small. Line L5 gets nets ready for the next pins, so that line L3 will find a track for them in a later column. A track freed in column $c$ is not given to another net in the same column, because the trunk of the old net still holds column $c$ on it.

The original router has one more step, which moves the tracks of a split net closer together when they cannot be joined yet, and it inserts the new track of line L3 by its own rule. This page leaves the first out and puts a new track at the edge of the side of its pin. The version stays legal and complete, as the proof shows.

## Example

Take the channel

| column | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- |
| top | 1 | 2 | 1 | 3 | 0 | 0 |
| bottom | 2 | 0 | 0 | 1 | 3 | 3 |

with density 2. Line L1 makes tracks 1 and 2.

| column | what happens | track 1 | track 2 |
| --- | --- | --- | --- |
| 1 | net 1 enters on track 1, net 2 on track 2; neither can move, because the branches fill the column | 1 | 2 |
| 2 | net 2 enters on track 2, with a branch past track 1; net 2 is done, track 2 is freed | 1 | 2 (freed) |
| 3 | net 1 enters on track 1; its next pin is at the bottom, so it jogs down to the empty track 2, and track 1 is freed | 1 (freed) | 1 |
| 4 | net 3 enters on track 1, net 1 enters on track 2; net 1 is done and is freed | 3 | 1 (freed) |
| 5 | net 3 enters on track 2 from the bottom, so it is split; a jog joins tracks 1 and 2, and track 1 is freed, since the next pin is at the bottom | 3 (freed) | 3 |
| 6 | net 3 enters on track 2 and is done | | 3 (freed) |

The routing uses 2 tracks, the density, and no extension column. Net 1 changes track in column 3 and net 3 in column 5. Without doglegs, this channel needs 3 tracks, because its vertical constraint graph has the path $3 \to 1 \to 2$.

**A cycle.** Take top pins $1, 2$ and bottom pins $2, 1$, with density 2. In column 1, net 1 enters on track 1 and net 2 on track 2. In column 2, the top pin of net 2 finds its track 2, and the bottom pin of net 1 finds track 1, so the two branches would cross. Both are equally long, so the top pin keeps track 2, and net 1 gets a new track 3 at the bottom. Net 2 is done and frees track 2. Net 1 is now on tracks 1 and 3, and the branch of net 2 blocks the jog in column 2. In the extension column 3, the jog from track 1 to track 3 is free, and net 1 is joined. The result has 3 tracks and 1 extension column. The page on [channel density](/channel-density/) shows that 2 tracks are not enough for this channel in this model.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Legal wires.** A track holds at most one net at a time, and a track is never given to a new net in the column where it was freed. Every vertical wire in a column is placed only where layer V is free, except the two pin branches, whose conflict line L3 resolves. So no point of a layer holds two nets.
- **Connected nets.** Every part of the wire of a net is joined to one of the tracks that the net holds. A net is freed only when it holds one track and has no pin to the right, so its wire is then one connected piece.
- **Completion.** In an extension column there are no pins, so the shortest jog of a split net is always free, and each extension column frees at least one track. The scan stops after at most as many extension columns as there are tracks.
- **Density bound.** The router starts with $d$ tracks and every routing in this model needs at least $d$, so $T \ge d$.

## Complexity

- **Time.** With an array that marks the rows of the current column used on layer V, each step of a column takes $O(T)$ per net and $O(T^2)$ in all, and the next pin of each net comes from a table built in $O(n)$ time. So the total time is $O((n + E) T^2)$. Line L3 adds at most two tracks per column, so $T \le d + 2n$, and the completion argument gives $E \le T$.
- **Space.** $\Theta(T + N)$ for the state of the current column and the next pins, besides the output wires.

## Properties

- **What is proved.** Every result is a legal routing of all nets, possibly with extension columns, and it has at least $d$ tracks.
- **What is only measured.** The number of tracks. Rivest and Fiduccia reported results close to the density on the benchmark channels of the time. On 1000 random channels of 20 columns and 10 nets, this version used $d$ tracks in 578, $d + 1$ in 332, $d + 2$ in 72, and more in 18. It needed extension columns in 272, and 447 of the channels had a cyclic constraint graph. On the acyclic ones, it beat left-edge in 123 and lost in 102. These are tests on random cases, not bounds.
- **Jogs anywhere.** It handles cycles of the constraint graph without any special step, because a net can change track in any free column.
- **Local.** Each decision depends only on the current column and the next pins. The router never goes back, so an early choice can cost tracks later.
- **Vias.** Every jog adds two vias. The router does not try to keep the number of vias small.

## Variants and improvements

- **Range reduction.** Rivest and Fiduccia also move the tracks of a split net closer together when they cannot be joined yet. This makes a later join more likely.
- **Parameters.** The original router has parameters, among them the starting number of tracks and a minimum length for a jog. Trying several values and keeping the best result is common.
- **Starting width.** If the router needs extension columns, run it again with more starting tracks. More tracks often remove the need for extension columns.
- **Switchboxes.** Luk in 1985 extended the column scan to pins on the left and right sides, for [switchbox routing](/switchbox-routing/).
- **Doglegs at pins only.** If jogs are allowed only at pin columns, the problem is the one of [dogleg channel routing](/dogleg-channel-routing/).

## When to use it

- When the vertical constraint graph has cycles, and routers without doglegs fail.
- When a router that always completes is needed, and extension columns or extra tracks are acceptable.
- On long channels, since the scan is linear in the number of columns.

When the channel has no vertical constraints, use the [left-edge algorithm](/left-edge-algorithm/), which is optimal. When the number of tracks matters most, also try the [Yoshimura-Kuh algorithm](/yoshimura-kuh-algorithm/).

## Pitfalls

- **Reusing a track in the column where it was freed.** The old trunk holds column $c$ on that track. A new net there would touch it.
- **Forgetting the branch of a pin.** The branch of a top pin passes over every track above its own on layer V. A jog in the same column must avoid those rows.
- **Expecting the density.** The router starts with $d$ tracks, but it can add tracks and extension columns. Report both numbers.
- **Extension columns that are not allowed.** If the channel has no room past its end, a result with $E > 0$ is not a solution. Rerun with more tracks.

## Implementations

## History

Ronald L. Rivest and Charles M. Fiduccia presented the greedy channel router at the 19th Design Automation Conference in 1982. It differed from the routers before it, which assigned whole nets or pieces of nets to tracks, in that it routed one column at a time with jogs anywhere. It became one of the most used channel routers, and Luk extended it to switchboxes in 1985. Szymanski's proof of 1985 that the fewest tracks with doglegs is NP-hard to find explained why such heuristics are the practical choice.

## References
