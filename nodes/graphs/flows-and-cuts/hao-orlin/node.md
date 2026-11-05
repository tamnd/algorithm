---
tag: X5P88R
kind: algorithm
slug: hao-orlin
name: Hao-Orlin algorithm
aliases:
- Hao-Orlin directed min cut
area: graphs/flows-and-cuts
level: research
summary: Compute the directed global min cut in the time of a single push-relabel run.
solves: [directed-global-min-cut-problem, global-min-cut-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n^2 m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1992
  people: [Jianxiu Hao, James B. Orlin]
  note: Presented at SODA 1992 and published in the Journal of Algorithms in 1994, with an O(nm log(n^2/m)) bound using dynamic trees.
prereqs: [directed-global-min-cut-problem, push-relabel, min-cut-problem]
see_also: [global-min-cut-problem, stoer-wagner, karger-min-cut, edge-connectivity, gomory-hu-tree, max-flow-min-cut-theorem, dinic]
sources:
  - paper: doi:10.1006/jagm.1994.1043
    title: Jianxiu Hao and James B. Orlin, A faster algorithm for finding the minimum cut in a directed graph, Journal of Algorithms 17(3), 424 to 446 (1994)
    locator: the whole paper (dormant sets, the choice of sinks, the proof that each phase ends with a minimum cut, and the running time)
  - paper: doi:10.1006/jcss.1995.1022
    title: Harold N. Gabow, A matroid approach to finding edge connectivity and packing arborescences, Journal of Computer and System Sciences 50(2), 259 to 273 (1995)
    locator: the introduction (comparison with the Hao-Orlin bound for directed edge connectivity)
  - paper: doi:10.1145/48014.61051
    title: Andrew V. Goldberg and Robert E. Tarjan, A new approach to the maximum-flow problem, Journal of the ACM 35(4), 921 to 940 (1988)
    locator: the push-relabel method, valid labelings and the bounds on relabels and pushes that Hao-Orlin extends
---

The Hao-Orlin algorithm computes a [minimum cut of a directed graph](/directed-global-min-cut-problem/): a nonempty proper vertex set $X$ minimizing the capacity of the edges leaving $X$. The plain method needs $2(n - 1)$ maximum flows, one per sink in each direction. Hao and Orlin run a single [push-relabel](/push-relabel/) computation in which the sink changes $n - 1$ times, and each old sink becomes a source; vertices that can no longer reach the sink are set aside in *dormant* sets so that the labels stay valid. Each phase ends with a minimum cut between the current sources and the sink, and the whole run costs about as much as one push-relabel maximum flow. Run once on the graph and once on its reverse, it gives the directed global minimum cut, and on an undirected graph one run suffices.

## In plain words

Pick one start point. Any cut either keeps it inside or outside, so look at both cases: once on the graph as given and once with all edges reversed. In one case, pick a target, push water from the start toward it, and find the cheapest way to separate them. Then add the target to the sources, pick a new target, and keep pushing from where you were instead of starting over. Points from which water can no longer reach the current target are put to sleep in groups, so that they do not confuse the bookkeeping; they wake up when the awake points run out. Each target gives one candidate cut, and the cheapest of all is the answer.

## The problem

**Input.** A directed graph $G = (V, E)$ with $n \ge 2$ vertices and capacities $c(e) \ge 0$, real numbers. Parallel and antiparallel edges are allowed and keep separate residual pairs; antiparallel edges are not merged. Self-loops leave no set and are ignored. An undirected edge is given as two arcs.

**Output.** A set $X$ with $\emptyset \ne X \ne V$ minimizing $c(X, V \setminus X) = \sum \{ c(u, v) : u \in X, v \notin X \}$, and the value.

Fix a vertex $r$. Every such $X$ either contains $r$ or not. The sets containing $r$ are handled by one run of HAO-ORLIN-ROOTED on $G$. A set $X$ without $r$ has $c(X, V \setminus X) = c^{\mathrm{rev}}(V \setminus X, X)$ in the reversed graph, where $V \setminus X$ contains $r$, so a second run on the reversed graph handles them.

## The algorithm

The state is a preflow $f$, the residual capacities $r_f$, excesses $e(v) = $ inflow minus outflow, and labels $d(v)$. The vertices are split into the source set $S$, a list of dormant sets $D_1, \dots, D_k$ in order of creation, and the awake set $W$, which contains the sink $t$. A vertex $v \in W \setminus \{t\}$ is active if $e(v) > 0$, and an arc $(v, w)$ is admissible if $r_f(v, w) > 0$, $w \in W$ and $d(v) = d(w) + 1$.

```pseudo id=main
HAO-ORLIN-ROOTED(G, c, r)
L1  d(r) ← n;  d(v) ← 0 for v ≠ r;  S ← {r};  W ← V ∖ {r};  no dormant sets
L2  push the full capacity of every arc out of r
L3  t ← a vertex of W with the least label
L4  repeat n − 1 times
L5      while some v ∈ W ∖ {t} is active do
L6          if v has an admissible arc x then push min(e(v), r_f(x)) along x
L7          else if v is the only vertex of W with label d(v) then move { w ∈ W : d(w) ≥ d(v) } from W to a new dormant set
L8          else if v has no residual arc into W then move {v} from W to a new dormant set
L9          else d(v) ← 1 + min { d(w) : (v, w) residual, w ∈ W }
L10     record the cut X = V ∖ W and its capacity c(X, W)
L11     move t from W to S;  d(t) ← n
L12     push the full residual capacity of every arc from t to a vertex not in S
L13     if W = ∅ then move the most recent dormant set back into W, if any is left
L14     t ← a vertex of W with the least label
    return the recorded cut of least capacity

HAO-ORLIN(G, c)
L15 run HAO-ORLIN-ROOTED on G and on the reverse of G from vertex 0; complement the second side; return the better cut
```

Lines L5 to L9 are push-relabel restricted to $W$, with two changes. Line L7 is the gap rule: if no other awake vertex has the label of $v$, then no vertex above that label can reach $t$, and those vertices are put to sleep together. Line L8 puts to sleep a vertex that has no residual arc into $W$. Lines L11 and L12 turn the sink into a source, and line L13 wakes the youngest dormant set when the awake vertices run out. Every vertex other than $r$ is the sink exactly once.

## Example

Take the running network $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10 with one more edge $t s$ 15, so that it is strongly connected; this is the example of the [directed global minimum cut](/directed-global-min-cut-problem/) page. The vertices are numbered $s, a, b, c, d, t$ in that order and ties in line L14 go to the lower number.

| run | sinks in order | cut values recorded | best |
|---|---|---|---|
| forward, root $s$ | $a, d, t, b, c$ | 10, 17, 20, 10, 12 | 10, $X = \{s, b, c, d, t\}$ |
| reverse, root $s$ | $a, t, b, c, d$ | 14, 15, 10, 9, 16 | 9, $X = \{s, a, b, d, t\}$ |

In the forward run, line L2 pushes 10 into $a$ and 10 into $c$. The first sink is $a$. The vertex $c$ is active, and as the phase proceeds every awake vertex except $a$ goes to sleep, so the recorded cut is $V \setminus \{a\}$, of capacity $c(s, a) = 10$, the only edge into $a$. In the third phase, with sink $t$, the cut $\{s, a, c, d\}$ has capacity $c(a, b) + c(d, b) + c(d, t) = 4 + 6 + 10 = 20$. The best cut containing $s$ has value 10.

In the reverse run, the fourth phase has sink $c$ and records the reverse-graph cut $\{s, a, b, d, t\}$ of capacity 9, which is the capacity of the edges into $c$'s complement from $c$ in the original graph: $c(c, d) = 9$. Complementing gives $X = \{c\}$ with $c(X, V \setminus X) = 9$, the directed global minimum cut. The rooted value 10 from the forward run alone would be wrong, which shows why both runs are needed.

**Edge cases.** In the running network without the edge $t s$, no edge enters $s$, so $V \setminus \{s\}$ has capacity 0; the reverse run finds it in its first phases. With the arcs $s \to a$ 5 and $t \to a$ 5 only, there is no path from $s$ to $t$ and several cuts of capacity 0 exist, for example $\{a\}$. An edge of capacity 0 never has a residual arc and adds 0 to every cut. In the antiparallel pair $0 \to 1$ of capacity 3 and $1 \to 0$ of capacity 2, the cut $\{0\}$ counts only the 3 and the cut $\{1\}$ only the 2.

## Correctness

The [correctness proof](proofs/correctness.md) keeps four invariants: $f$ is a preflow with $e(v) \ge 0$ outside $S$; no residual arc goes from $S$ or a dormant set to a later dormant set or to $W$; the labels are valid on $W$, so $d(v) \le d(w) + 1$ for each residual arc inside $W$; and $t$ has the least label in $W$. The gap rule keeps the second invariant because only $v$ could have a residual arc down from its label, and it has no admissible arc. At line L10 no vertex of $W$ other than $t$ has excess, all arcs from $X = V \setminus W$ to $W$ are full and those from $W$ to $X$ are empty, so $c(X, W) = e(t)$. Every set $Y$ with $S \subseteq Y$ and $t \notin Y$ has $c(Y, V \setminus Y) \ge e(t)$, so the recorded cut is a minimum cut between $S$ and $t$. For an optimal set $X^*$ containing $r$, the first sink outside $X^*$ comes while all earlier sinks are inside $X^*$, so that phase records a cut of value at most $c(X^*)$.

## Complexity

Hao and Orlin show that the labels stay below $2n$ and that the total number of relabels over all $n - 1$ phases is $O(n^2)$, as in a single push-relabel run. The usual push-relabel counting then gives $O(nm)$ saturating pushes and $O(n^2 m)$ non-saturating pushes in total, so the generic algorithm runs in $O(n^2 m)$ time; with first-in first-out selection it is $O(n^3)$, and with dynamic trees $O(nm \log(n^2/m))$. The Python version also spends $O(m)$ per phase to compute the cut capacity and $O(n)$ per gap or sink change, which is $O(nm + n^2)$ in total, within the bound. The second run doubles the time. The extra space is $\Theta(n + m)$.

## Properties

- **One flow for $n - 1$ sinks.** The work of earlier phases is kept, which is the whole point.
- **Exact and deterministic**, for real capacities.
- **Gives the arc connectivity** of a directed graph with unit capacities, and the edge connectivity of an undirected graph with one run.
- **Each phase gives a minimum cut between $S$ and $t$**, not between $r$ and $t$; that is enough for the global minimum.

## Variants and improvements

- **Undirected graphs.** One run suffices, since $c(X, V \setminus X) = c(V \setminus X, X)$; in practice [Stoer-Wagner](/stoer-wagner/) and [Karger's algorithm](/karger-min-cut/) compete with it, and experiments by Chekuri, Goldberg, Karger, Levine and Stein found Hao-Orlin with heuristics among the fastest.
- **Unit capacities.** Gabow's matroid method finds the arc connectivity $\lambda$ in $O(\lambda m \log(n^2/m))$.
- **Newer methods.** Randomized algorithms since 2021 beat $O(nm)$ on dense or weighted directed graphs; with the almost-linear maximum flow algorithm, $2(n - 1)$ independent flows already cost $n m^{1 + o(1)}$.
- **Rooted cuts.** A single run gives the least cut with $r$ on the source side, the minimum $r$-rooted cut, used for arborescence packing.

## When to use it

Use it for the minimum cut or arc connectivity of a directed graph with arbitrary capacities, when a push-relabel code is at hand. For undirected graphs, Stoer-Wagner is simpler to code. For a cut between two given vertices, run one maximum flow.

## Pitfalls

- **Running only one direction.** On a directed graph the forward run finds only cuts that contain the root; the example above misses the optimum 9 without the reverse run.
- **Letting the sink go to sleep.** The sink must have the least awake label; then neither line L7 nor line L8 can apply to it.
- **Waking the wrong dormant set.** Only the most recent one may be woken, since older ones may have residual arcs into newer ones.
- **Pushing into dormant vertices during a phase.** Admissible arcs must end in $W$; only line L12 pushes into dormant vertices.
- **Merging antiparallel edges** changes the cut values in a directed graph.

## Implementations

The Python version takes the vertex count and a list of directed edges $(u, v, c)$ with capacities of type `int`, `Fraction` or `float`, and returns the value and the sorted source side of a minimum cut. It runs the rooted algorithm from vertex 0 on the graph and on its reverse, keeps active vertices in a first-in first-out queue with current-arc pointers, and offers a callback that reports each phase.

## History

Jianxiu Hao and James Orlin presented the algorithm at SODA 1992, and the journal version appeared in 1994. It answered the question of whether a directed minimum cut needs $2(n - 1)$ separate flows by showing that it costs about one flow.

## References
