---
tag: 4Z2N0P
kind: algorithm
slug: network-flow-tracking
name: Network flow data association
aliases:
- min-cost flow tracking
- Zhang-Li-Nevatia tracking
area: computer-vision/visual-tracking
level: advanced
summary: Link detections over a whole video as a min-cost flow, each unit of flow a track from source to sink through detection nodes, solved globally.
solves: [data-association, multi-object-tracking]
model: real-ram
complexity:
  vars: {n: the number of detections, L: the number of allowed links between detections, K: the number of tracks found}
  time: {worst: O(K n (n + L)), average: O(K n (n + L)), best: O(n (n + L))}
  space: {extra: O(n + L)}
properties: {deterministic: true, exact: true, local: false, iterative: true, online: false}
history:
  year: 2008
  people: [Li Zhang, Yuan Li, Ramakant Nevatia]
  note: Zhang, Li and Nevatia wrote the association of all detections of a video as a min-cost flow problem, with a node pair per detection, at CVPR 2008. Pirsiavash, Ramanan and Fowlkes and Berclaz, Fleuret, Türetken and Fua gave faster shortest path solvers in 2011.
prereqs: [min-cost-flow-problem, successive-shortest-path, bellman-ford, tracking-by-detection]
see_also: [multi-object-tracking, data-association, flow-decomposition, flow-integrality-theorem, k-shortest-paths, vertex-disjoint-paths, total-unimodularity, multiple-hypothesis-tracking]
sources:
  - paper: doi:10.1109/CVPR.2008.4587584
    title: Li Zhang, Yuan Li and Ramakant Nevatia, Global data association for multi-object tracking using network flows, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2008, 1 to 8
    locator: the whole paper (the MAP formulation, the flow network with two nodes per detection, and the costs of entry, exit, detection and link)
  - paper: doi:10.1109/CVPR.2011.5995604
    title: Hamed Pirsiavash, Deva Ramanan and Charless C. Fowlkes, Globally-optimal greedy algorithms for tracking a variable number of objects, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2011, 1201 to 1208
    locator: the whole paper (successive shortest paths on the tracking network and a greedy approximation by dynamic programming)
  - paper: doi:10.1109/TPAMI.2011.21
    title: Jérôme Berclaz, François Fleuret, Engin Türetken and Pascal Fua, Multiple object tracking using K-shortest paths optimization, IEEE Transactions on Pattern Analysis and Machine Intelligence 33(9), 2011, 1806 to 1819
    locator: the whole paper (tracking on an occupancy grid as disjoint shortest paths)
---

Network flow data association links all detections of a video into tracks in one global optimization. Each detection becomes an edge of unit capacity in a directed graph with a source and a sink, and each track becomes one unit of flow from the source to the sink through the detections it contains. Costs on the edges say how likely each detection is to be real, how likely a track is to start or end there, and how likely two detections are to be the same object. A min-cost flow then gives the set of disjoint tracks of least total cost, which is the most probable set of tracks under the model. Zhang, Li and Nevatia introduced this formulation in 2008. It solves its model exactly in polynomial time, which is rare in data association, because it scores a track only by pairs of consecutive detections. It is a batch method for [tracking-by-detection](/tracking-by-detection/) when the whole video, or a window of it, is known.

## In plain words

Think of a set of stepping stones laid across a river over several days, where each day adds a row of stones, and some stones are fake. Each person who crosses steps on at most one stone per row, and no two people share a stone. Real stones pay a reward for stepping on them, long jumps cost effort, and entering or leaving the river costs a fee. We want to choose who crosses and by which stones so that the total reward minus the effort and the fees is as large as possible. Network flow finds this best choice for all people at once. It sends people one at a time along the best path, and a later person can push an earlier one onto a different stone if that helps the total.

## The problem

The input is a set of $n$ detections, each with a frame number, a position and a confidence, and the costs of a model:

- $c_i = \ln(\beta_i / (1 - \beta_i))$ for using detection $i$, where $\beta_i$ is the probability that detection $i$ is false, so a confident detection has a negative cost;
- $c_{\text{en}}$ and $c_{\text{ex}}$ for starting and ending a track, the negative logs of the probabilities of entry and exit;
- $c_{ij} = -\ln P_{\text{link}}(j \mid i)$ for detection $j$ following detection $i$ in a track, defined only for allowed links, from an earlier frame to a later one within a small gap.

A set of tracks is a set of disjoint chains of detections along allowed links. Its cost is the sum, over tracks, of the entry and exit costs, the detection costs and the link costs. The output is a set of tracks of least cost. Zhang, Li and Nevatia derive this cost as the negative log of the posterior probability of the set of tracks, under the assumptions that detections are independent given the tracks, that tracks do not overlap, and that a track is a Markov chain of its detections.

The flow network has the source $s$, the sink $t$, and two nodes $u_i$ and $v_i$ per detection, so $V = 2n + 2$. Its edges, all of capacity 1, are $u_i \to v_i$ with cost $c_i$, $s \to u_i$ with cost $c_{\text{en}}$, $v_i \to t$ with cost $c_{\text{ex}}$, and $v_i \to u_j$ with cost $c_{ij}$ for each of the $L$ allowed links, so $E = 3n + L$. The capacity 1 on $u_i \to v_i$ makes each detection belong to at most one track.

## The algorithm

```pseudo id=main
NETWORK-FLOW-TRACKING(the detections, the costs c_i, c_en, c_ex, c_ij)
L1   build the nodes s, t, u_i, v_i and the edges u_i → v_i of cost c_i, all of capacity 1
L2   add s → u_i of cost c_en, v_i → t of cost c_ex, and v_i → u_j of cost c_ij for each allowed link
L3   start with the zero flow
L4   repeat: find a shortest s-t path P in the residual graph, with Bellman-Ford
L5       if there is no path or cost(P) ≥ 0, stop
L6       push one unit of flow along P
L7   decompose the flow into s-t paths; each path is a track
```

This is the [successive shortest path](/successive-shortest-path/) method for the [min-cost flow problem](/min-cost-flow-problem/), with one change: the amount of flow is not given. Each augmentation adds one track, and the method stops when the next track would not lower the cost. The residual graph has edges with negative cost, from the detection edges and from the reverse edges, so the code uses [Bellman-Ford](/bellman-ford/). Line L7 follows the edges with flow from the source. Each path visits the detections of one track in order of time, which is [flow decomposition](/flow-decomposition/).

## Example

**A reroute by hand.** Frame 0 has detections $a$ and $b$, and frame 1 has $c$ and $d$. Every detection costs $-2$, and entry and exit cost 1 each. The allowed links cost $a \to c$: 1.0, $a \to d$: 0.1, $b \to c$: 5.0, and $b \to d$: 0.2. A track of two detections costs $1 - 2 + c_{ij} - 2 + 1 = c_{ij} - 2$.

- The first shortest path is $s, a, d, t$, with cost $-1.9$. A greedy method would keep it and stop there, because $b$ and $c$ alone cost 0 each and $b \to c$ is expensive: total $-1.9$.
- The second shortest path in the residual graph is $s \to u_b \to v_b \to u_d \to v_a \to u_c \to v_c \to t$. It takes $d$ for $b$, goes back along the reverse of the link $a \to d$ at cost $-0.1$, and gives $c$ to $a$. Its cost is $1 - 2 + 0.2 - 0.1 + 1.0 - 2 + 1 = -0.9$.
- The third search finds no path of negative cost, so the method stops with the tracks $(a, c)$ and $(b, d)$ and the total $-1.9 - 0.9 = -2.8$. That is $(1.0 - 2) + (0.2 - 2)$.

**A short sequence.** In the code, three targets move to the right for 10 frames, 4 units apart, with position noise 0.2 and confidences between 0.8 and 0.95. Target 0 is missed in frame 4 and target 2 in frame 6, and three false alarms with confidence between 0.5 and 0.65 appear at random places. The 31 detections and 43 allowed links, with gaps of up to 2 frames, give three augmenting paths with costs $-12.63$, $-12.0$ and $-11.0$, then stop. The three tracks are exactly the three targets, each bridging its missed frame, and the false alarms are left out.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows these facts.

- **Theorem: flows are track sets.** The integral flows of value $k$ correspond to the sets of $k$ disjoint tracks, with the same cost.
- **Theorem: each step is optimal.** After $k$ augmentations, the flow has the least cost among all flows of value $k$, and the residual graph has no cycle of negative cost, so Bellman-Ford is correct at every step.
- **Theorem: convexity.** The least cost $F(k)$ of a flow of value $k$ is convex in $k$, and the cost of the $(k + 1)$-th augmenting path is $F(k + 1) - F(k)$. So the first path of nonnegative cost marks the minimum of $F$ over all $k$, and the returned tracks have the least cost over all track sets.

The optimality is for the model. The model scores a track only by its detections and its consecutive links, so it cannot express long-range terms such as a constant velocity over three detections or an appearance model that changes over the track. Adding such terms breaks the flow structure, and the problem then becomes NP-hard in general, as for [multiple hypothesis tracking](/multiple-hypothesis-tracking/).

## Complexity

The graph has $V = 2n + 2$ nodes and $E = 3n + L$ edges. Each augmentation adds one track, so there are at most $K + 1 \le n + 1$ shortest path searches. Bellman-Ford costs $O(V E) = O(n (n + L))$ per search, so the total is $O(K n (n + L))$ time. The first search can use [shortest paths on a DAG](/dag-shortest-paths/) in $O(n + L)$, since the original graph has no cycles. After it, node potentials make all reduced costs nonnegative, so the later searches can use [Dijkstra's algorithm](/dijkstra/) in $O(E + V \log V)$, for $O(K (L + n \log n))$ in all. The code keeps Bellman-Ford for every search, which is simpler, and needs at least one search, so its best case is $O(n (n + L))$. The space is $O(n + L)$ for the graph. With $L$ links per detection to the few next frames, $L$ grows linearly in $n$, and the method handles thousands of detections.

## Properties

- **Globally optimal for its model.** No other set of tracks has lower cost.
- **Number of tracks found.** The number of tracks is an output, not an input.
- **Batch.** It needs all frames of the window before it can answer. A sliding window gives a delayed online version.
- **Integral.** The min-cost flow has an integral optimum because the constraint matrix of a network is totally unimodular, so no rounding is needed.
- **Pairwise costs only.** Each cost depends on one detection or two consecutive ones.
- **Missed detections.** Links across a gap of a few frames bridge short occlusions.

## Variants and improvements

- **Successive shortest paths with dynamic programming.** Pirsiavash, Ramanan and Fowlkes (2011) showed that the first path can be found by dynamic programming over the frames, and gave a greedy approximation that adds paths without the reverse edges, with non-maximum suppression between rounds.
- **K-shortest paths.** Berclaz, Fleuret, Türetken and Fua (2011) track on a grid of ground locations from a probabilistic occupancy map, and find the disjoint paths with the K-shortest paths method.
- **Other min-cost flow solvers.** [Cost scaling](/cost-scaling/), [push-relabel](/push-relabel/) and the [network simplex](/network-simplex/) method solve the same problem, with or without a fixed amount of flow.
- **Linear programming.** The same model is a [linear program](/min-cost-flow-lp-formulation/) whose optimum is integral, which allows extra linear constraints at the risk of losing integrality.
- **Higher-order costs.** Lifted multicut, quadratic terms and learned costs add terms on three or more detections, at the price of an NP-hard problem solved approximately.
- **Learned link costs.** Later work learns $c_{ij}$ from appearance and motion features, and keeps the flow solver.

## When to use it

Use network flow association for offline tracking, or online with a delay, when detections are reasonably good, and when you want the best set of tracks of a simple model without tuning a search. It is a good fit for people or vehicles seen by a fixed camera, where the number of objects changes and short occlusions are common. For online use with no delay, use a frame-by-frame method such as [GNN](/global-nearest-neighbor-association/). If identity depends on long-range evidence, such as appearance over the whole track, a method with higher-order costs or [MHT](/multiple-hypothesis-tracking/) can model it better.

## Pitfalls

- **Costs with the wrong signs.** If $c_{\text{en}} + c_{\text{ex}} + c_i < 0$ for every detection, each false alarm becomes a track of one detection. The entry and exit costs must outweigh a weak detection.
- **Dijkstra on negative costs.** The detection costs are negative. Use Bellman-Ford or a DAG pass first, then potentials, before Dijkstra.
- **Too many links.** Allowing links across many frames makes $L$ grow quickly. Gate the links by distance and by the gap.
- **One detection for two objects.** Capacity 1 per detection means two objects merged into one detection cannot both use it. One of the tracks then needs a gap link.
- **Fixed amount of flow.** Giving the number of tracks in advance wastes the main advantage. Stop when the path cost becomes nonnegative.
- **Identity switches inside the model.** The optimum of a pairwise model can still swap two close targets if their links have similar costs.

## Implementations

## History

Linear programming and flow formulations of data association appeared in the 2000s, and Jiang, Fels and Little used linear programming for multiple object tracking in 2007. In 2008, Li Zhang, Yuan Li and Ramakant Nevatia wrote the association of all detections as a min-cost flow, with two nodes per detection, derived the costs from a MAP model, and searched over the amount of flow. In 2011, Pirsiavash, Ramanan and Fowlkes showed how to compute the solution with successive shortest paths and dynamic programming, and gave a fast greedy version. In the same year, Berclaz, Fleuret, Türetken and Fua tracked people on an occupancy grid with K-shortest paths. These papers made global optimization a standard part of tracking-by-detection, and later work kept the flow solver and learned the costs.

## References
