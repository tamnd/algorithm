---
tag: VP75X0
kind: data-structure
slug: motion-graph
name: Motion graph
aliases:
- motion graphs
area: graphics-and-signals/character-animation
level: core
summary: A directed graph whose edges are clips of captured motion and whose nodes are frames where clips can be joined by short blended transitions.
implements: [graph]
model: real-ram
complexity:
  vars: {f: the number of frames in the database, k: the transition window in frames, j: the number of joints, e: the number of edges}
  time: {build: O(f^2 k j), prune: O(f + e), next_edges: O(1)}
  space: {distance_matrix: O(f^2), graph: O(f + e)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2002
  people: [Lucas Kovar, Michael Gleicher, Frederic Pighin]
  note: "Kovar, Gleicher and Pighin named the motion graph at SIGGRAPH 2002. Arikan and Forsyth and Lee and coworkers published graphs of motion capture frames at the same conference."
prereqs: [motion-blending, strongly-connected-components, tarjan-scc]
see_also: [motion-matching, registration-curves, footskate-cleanup, directed-graph, dijkstra, a-star-search, depth-first-search, kabsch-algorithm]
sources:
  - paper: doi:10.1145/566654.566605
    title: "Lucas Kovar, Michael Gleicher and Frederic Pighin, Motion graphs, ACM Transactions on Graphics 21(3) (SIGGRAPH 2002), 473 to 482"
    locator: "the point cloud distance with its closed form 2D alignment, the transitions at local minima below a threshold, the blend of a transition, the pruning to the largest strongly connected component, and the search for graph walks"
  - book: isbn:9780124158429
    title: "Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012"
    locator: the material on motion capture data and its processing
---

A motion graph turns a database of captured motion clips into a structure that can play new motion of any length.
The database has $f$ frames in total.
Two frames $a$ and $b$ are a possible transition when the poses near $a$ look like the poses near $b$: then the character can leave one clip at $a$, play a short [blend](/motion-blending/) of $k$ frames, and continue in the other clip after $b$.
The graph has an edge for every piece of a clip between two such points and an edge for every transition, so every walk in the graph is a valid sequence of motion.
Construction compares every pair of frames, $O(f^2)$ distance evaluations, keeps the pairs that are local minima of the distance and below a threshold, and then removes the dead ends by keeping the largest [strongly connected component](/strongly-connected-components/).
A search over walks then picks the motion that follows a path, reaches a goal, or obeys a user.

## In plain words

You have many short films of a person who walks, turns and stops.
You look for moments where the person in one film stands almost the same way as the person in another film, or in a later part of the same film.
At each such moment you can cut from one film to the other with a short cross fade, and nobody sees the cut.
Write each film as a road and each good cut as a junction between roads.
Then any drive along the roads is a new, longer film made only of good pieces.
Roads that lead to a place with no way out are removed, so the drive never gets stuck.

## The abstract type

A motion graph is a [directed graph](/directed-graph/) $G = (V, E)$ with motion attached to its edges.

- A node is a frame of the database at which motion can branch.
- An edge from $u$ to $v$ carries a sequence of frames. A clip edge plays the original frames from $u$ to $v$. A transition edge plays a blend of the window that starts at $u$ with the window that starts at $b$, and arrives at $v = b + k$.
- Two edges in a row join without a jump, because both play the frame of their common node.

The queries are the successors of a node (which motions can follow) and the frames of an edge.
Every walk of the graph plays as a continuous motion.
After pruning, every node reaches every other node, so a walk can go on as long as needed.

## Representation

The original paper puts the motion on the edges and keeps only the branch points as nodes.
The code below uses the simpler form with one node per frame: an edge from every frame to the next frame of its clip, and one more edge from $a$ to $b + k$ for every transition $(a, b)$.
Both forms have the same walks; the one with branch points only has fewer nodes.

The graph is stored as [adjacency lists](/adjacency-list/) over the frames.
Each transition edge also stores the alignment $(\theta, x_0, z_0)$ that places the second clip on the first one: a rotation by $\theta$ about the vertical axis and a translation $(x_0, z_0)$ in the ground plane.
During playback, the character keeps a current ground frame; each transition multiplies it by the stored alignment.

The frame distance compares point clouds, not joint angles.
For the windows $a, \dots, a + k - 1$ and $b, \dots, b + k - 1$, take the world positions $p_i$ and $q_i$ of all $j$ joints of all $k$ frames, with weights $w_i$, and minimize over the rigid moves $T_{\theta, x_0, z_0}$:

$$D(a, b) = \min_{\theta, x_0, z_0} \sum_i w_i \, |p_i - T_{\theta, x_0, z_0}(q_i)|^2 .$$

This minimum has a closed form.
With the weights summing to 1, the weighted means $\bar x, \bar z$ of the $p_i$ and $\bar x', \bar z'$ of the $q_i$,

$$\theta = \operatorname{atan2}\Big(\sum_i w_i (x_i z'_i - x'_i z_i) - (\bar x \bar z' - \bar x' \bar z),\ \sum_i w_i (x_i x'_i + z_i z'_i) - (\bar x \bar x' + \bar z \bar z')\Big),$$

and the translation moves the rotated mean of the $q_i$ onto the mean of the $p_i$.
The distance ignores the heading and the place of the character on the floor, so a left turn here matches a left turn there.

## Operations

```pseudo id=main
BUILD-MOTION-GRAPH(clips, k, ε, g)                 ▷ window, threshold, minimum gap
L1  for each window start a, for each window start b
L2      D[a, b] ← Σᵢ wᵢ |pᵢ - T(qᵢ)|²            ▷ the windows at a and b, T as below
L3          where θ ← atan2(S, C) and T moves the mean of q onto the mean of p
    for each pair (a, b) with |a - b| ≥ g
L4      if D[a, b] ≥ ε then skip the pair        ▷ ε is a tuning
L5      if D[a, b] ≤ D at its 8 neighbors then add the transition (a, b)
    for each frame u that has a next frame in its clip
L6      add the clip edge u → u + 1
    for each transition (a, b) with b + k in the clip of b
L7      add the transition edge a → b + k        ▷ plays the blend of the two windows
L8  return the largest strongly connected component of the graph
```

Line L8 uses [Tarjan's algorithm](/tarjan-scc/), which finds all components in one depth-first search.
The paper prunes for each set of motion labels (for example "walk" or "run") separately, so that a walk that must stay in one style cannot get stuck.

A transition edge plays the blend of the two windows.
For $p = 0, \dots, k - 1$, frame $p$ of the transition takes the root position by linear interpolation and each joint rotation by [slerp](/spherical-linear-interpolation/), with the weight

$$\alpha(p) = 2\left(\frac{p + 1}{k}\right)^3 - 3\left(\frac{p + 1}{k}\right)^2 + 1$$

on the frame $a + p$ of the first window and $1 - \alpha(p)$ on the frame $b + p$ of the second window, after the alignment.
The weight goes from 1 to 0 with zero slope at both ends.

To make a motion, search the walks of the graph.
The paper scores a walk by how far the root path is from a path that the user draws, and runs a branch and bound search over walks of a fixed length; it plays the first part of the best walk and repeats the search from there.
Shortest path searches such as [Dijkstra's algorithm](/dijkstra/) or [A*](/a-star-search/) fit when the goal is a node or a place.

## Example

The test builds a database from three synthetic walks of 5 joints at 30 frames per second.
Clip 1 has 40 frames, heading 0.
Clip 2 has 40 frames, heading 0.7 rad, at another place and in another phase.
Clip 3 has 20 frames with steps twice as long.
So $f = 100$, frames 0 to 39, 40 to 79 and 80 to 99.

With $k = 5$, $\epsilon = 0.003$ and the gap $g = k$, construction finds 14 transitions.
Among them are $(1, 31)$ and $(31, 1)$: the walk repeats every 30 frames, so frame 31 looks like frame 1.
There are also transitions between clip 1 and clip 2, such as $(5, 40)$, found even though the two clips have different headings and places, because the distance aligns them first.
The steps of clip 3 are too long, so no transition below the threshold joins it to the other clips.

The graph has 109 edges.
Its largest strongly connected component has 57 frames: frames 6 to 35 and 45 to 71.
Clip 3 is removed, and so are the first and last frames of clips 1 and 2, because a walk that enters them can never return.
The pruned graph has 61 edges, and from every kept frame a walk reaches every other kept frame.

These counts are measurements on this database; with another threshold or another window the graph changes.

## Correctness

The proof file shows four facts.
First, the closed form of line L3 gives the global minimum of the weighted squared distance over all rotations about the vertical axis and all ground translations, so $D(a, b)$ is the distance after the best 2D alignment.
Second, the filter of lines L4 and L5 keeps exactly the pairs that are at least $g$ apart, below the threshold, and not larger than any of their neighbors in the distance matrix.
Third, the component of line L8 is closed under paths: a path between two kept frames never leaves the component, every kept frame reaches every other one in the pruned graph, and no strongly connected subgraph is larger.
Fourth, the blend weight is 1 at the start, 0 at the end, and decreasing.

What the proof does not show is that a transition looks good.
The point cloud distance is a visual heuristic, the weights $w_i$ and the threshold $\epsilon$ are tuning, and the paper leaves the threshold to the user.
A transition below the threshold can still slide a foot, so the contacts are cleaned up afterward, for example with [footskate cleanup](/footskate-cleanup/).

## Complexity

Line L2 runs for all $O(f^2)$ pairs of window starts.
Each distance needs the alignment and the sum over $k j$ points, so construction costs $O(f^2 k j)$ time.
The distance matrix needs $O(f^2)$ space, which dominates: 10 minutes at 30 frames per second are $f = 18000$ frames and $3.24 \cdot 10^8$ entries.
Lines L4 to L7 cost $O(f^2)$, and line L8 costs $O(f + e)$.

During playback, the successors of a node are an adjacency list, $O(1)$ to reach.
The search over walks is the expensive part at run time: a search over all walks of $n$ edges with out degree $d$ visits up to $d^n$ walks, and branch and bound only cuts this in practice.

## Variants

- **Branch points only.** Merge chains of nodes with one successor into one edge, as in the paper. The graph gets much smaller.
- **Labels.** Mark clips with labels (walk, run, sneak), prune for each label set, and restrict the search to edges with the wanted labels.
- **Search over the graph.** Arikan and Forsyth (2002) search a graph of frames by random restarts and local changes; Lee and coworkers (2002) cluster the frames into a two layer structure for interactive control. Both papers appeared at the same conference as the motion graph.
- **Precomputed control.** Later work precomputes for every node and every user command which edge to take, for example by value iteration, so that playback needs no search.
- **No graph.** [Motion matching](/motion-matching/) drops the precomputed transitions. It searches the whole database every few frames for the best next frame and blends there, so every frame is a possible transition.
- **Registration.** [Registration curves](/registration-curves/) use the same frame distance with dynamic time warping to align whole clips for blends instead of single transitions.

## When to use it

Use a motion graph when the motion must come from a fixed database, when the character must follow a path or reach goals, and when the design wants every transition to be checked in advance.
It is a good fit for crowds and background characters, where a small graph plays many characters at a low cost.
For a character that responds to a player every frame, the delay until the next branch point is often too long; [motion matching](/motion-matching/) responds faster at the cost of a search every few frames.

## Pitfalls

- **Quadratic memory.** The full distance matrix grows as $f^2$. Store only the local minima below the threshold, computed one row band at a time.
- **Thresholds.** A threshold that is too low gives a graph with few branches and long waits; one that is too high gives visible pops. The value depends on the joint weights and on the type of motion.
- **Dead ends.** Without pruning, a search can enter a clip end and have no way to go on. Prune after every change of the database or the labels.
- **Self transitions.** A frame is always close to its own neighbors. Without the minimum gap $g$, every frame gets transitions to the next few frames, which play nothing new.
- **Drift.** The ground frame of the character changes at every transition. Over a long walk, small alignment errors add up; a path search must use the aligned root positions, not the stored ones.
- **Foot contact.** The blend of a transition mixes two planted feet. Clean up the contacts after the blend.

## Implementations

## History

Lucas Kovar, Michael Gleicher and Frederic Pighin introduced the motion graph at SIGGRAPH 2002, with the point cloud distance, the transitions at local minima, the pruning to strongly connected components, and a branch and bound search for paths.
At the same conference, Okan Arikan and David Forsyth presented a search over a graph of motion frames, and Jehee Lee, Jinxiang Chai, Paul Reitsma, Jessica Hodgins and Nancy Pollard presented interactive control of avatars on a graph of motion capture data.
Video textures by Arno Schödl and coworkers (2000) had used the same idea of jumps between similar frames for video.
Motion graphs became common in games and crowds; [motion matching](/motion-matching/), presented by Simon Clavet in 2016, replaced the precomputed transitions in many game engines.

## References
