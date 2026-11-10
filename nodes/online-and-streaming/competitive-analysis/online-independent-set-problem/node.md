---
tag: AY1D2J
kind: problem
slug: online-independent-set-problem
name: Online independent set problem
aliases:
- online maximum independent set
- online independent set
- online maximum independent set with vertex arrivals
area: online-and-streaming/competitive-analysis
level: research
summary: Vertices arrive one by one with their edges to earlier vertices, and each must be put in an independent set or refused for good. Every online algorithm has ratio Omega(n).
prereqs: [independent-set, online-algorithm, competitive-ratio]
see_also: [online-vertex-cover-problem, online-graph-coloring-problem, maximum-independent-set, greedy-independent-set, secretary-problem, yao-minimax-principle, online-interval-scheduling, advice-model]
sources:
  - paper: doi:10.1016/S0304-3975(01)00411-X
    title: "Magnus M. Halldorsson, Kazuo Iwama, Shuichi Miyazaki and Shiro Taketomi, Online independent sets, Theoretical Computer Science 289(2) (2002), 953-962; conference version in COCOON 2000, LNCS 1858, 202-209"
    locator: the introduction (the bound n - 1 for one solution), the multi-solution model (Theta(n / log n) for polynomially many solutions, Theta(n) for a constant number), and the inheritance model
  - url: https://arxiv.org/abs/1307.3192
    title: "Oliver Gobel, Martin Hoefer, Thomas Kesselheim, Thomas Schleiden and Berthold Vocking, Online independent set beyond the worst-case: secretaries, prophets, and periods, ICALP 2014; arXiv 1307.3192"
    locator: the introduction (the Omega(n) lower bound on interval graphs by nested pairs of intervals and Yao's principle) and the main results (O(rho^2) in the secretary and prophet models)
  - paper: doi:10.4230/LIPIcs.STACS.2015.116
    title: "Joan Boyar, Lene M. Favrholdt, Christian Kudahl and Jesper W. Mikkelsen, Advice complexity for a class of online problems, STACS 2015, LIPIcs 30, 116-129"
    locator: the class AOC, of which independent set with vertex arrivals is a complete member, and its advice bounds
---

Online independent set is the problem of building an [independent set](/independent-set/) of a graph whose vertices arrive one at a time. Each vertex comes with its edges to the earlier vertices, and the algorithm must accept it into the set or refuse it at once, for good. The goal is a large set compared with the [maximum independent set](/maximum-independent-set/) of the whole graph. In this model the problem is very hard. No deterministic algorithm has ratio better than $n - 1$ on graphs with $n$ vertices, and greedy reaches $n - 1$. Randomization does not help much: the ratio stays $\Omega(n)$, even on interval graphs. Research on the problem therefore studies weaker adversaries, such as random arrival order, and stronger algorithms, such as algorithms that keep many candidate sets. In the same arrival order, the refused vertices form a vertex cover, so this problem is the complement of [online vertex cover](/online-vertex-cover-problem/) in the model where each decision is made on arrival.

## In plain words

A club accepts members one at a time. When a person applies, the club learns which of the earlier applicants this person dislikes. The club must accept or refuse at once, and no two members may dislike each other. The club wants many members.

The trouble is that the club cannot see the future. Whoever it accepts, the next applicants can all dislike that person, while they get along with each other. Then the club is stuck with one member, while a club that had refused the first applicant could have taken everyone else. So no fixed rule does well on every list of applicants. Rules do better when the applicants come in a random order, or when the club may keep several lists of members and choose the best list at the end.

## Definition

**Input.** A graph $G = (V, E)$ with $n$ vertices, revealed as a sequence $v_1, v_2, \ldots, v_n$. When $v_t$ arrives, the algorithm learns the edges between $v_t$ and $v_1, \ldots, v_{t-1}$. The value of $n$ is not known in advance.

**Decisions.** At the arrival of $v_t$, the algorithm puts $v_t$ in the set $I$ or refuses it. A decision is final. $I$ must stay independent: $v_t$ may join only if it has no edge to a vertex already in $I$.

**Measure.** $\mathrm{ALG} = \lvert I \rvert$ and $\mathrm{OPT} = \alpha(G)$, the [independence number](/independence-number/) of the whole graph. An algorithm has ratio $\rho$ if $\mathrm{OPT} \le \rho \cdot \mathrm{ALG}$ on each input with $n$ vertices; the ratio is a function of $n$. A randomized algorithm needs $\mathrm{OPT} \le \rho \cdot \mathbb{E}[\mathrm{ALG}]$ against an [oblivious adversary](/oblivious-adversary/), which fixes the input before the algorithm runs.

**Weighted version.** Each vertex has a weight that is revealed at its arrival, and the goal is the total weight of $I$.

## Variants

- **Multi-solution model.** The algorithm keeps $r(n)$ independent sets. Each arriving vertex may be added to any of them that stay independent, and the output is the largest set at the end. With $r(n) = 2^n$ the problem becomes trivial, because the algorithm can keep every subset. Halldorsson, Iwama, Miyazaki and Taketomi (2002) showed that the best ratio is $\Theta(n / \log n)$ when $r(n)$ is a polynomial in $n$, and $\Theta(n)$ when $r(n)$ is a constant.
- **Inheritance model.** As above, but the algorithm may also copy a current set and grow the copies in different ways. With $n^k$ operations per vertex, the same paper gives an upper bound $O(n / (k \log n))$ and a lower bound of order $n / (e^{k+1} \log^3 n)$. The lower bounds of the paper also hold for randomized algorithms against an oblivious adversary.
- **Random order and prophets.** The graph is fixed by the adversary but the vertices arrive in a uniformly random order, as in the [secretary problem](/secretary-problem/), or the weights are drawn from known distributions, as in the [prophet inequality](/prophet-inequality/). Gobel, Hoefer, Kesselheim, Schleiden and Vocking (2014) gave ratio $O(\rho^2)$ in both models for graphs with inductive independence number $\rho$, and an extra factor $O(\log n)$ for weights. Interval graphs have $\rho = 1$, and disk graphs have $\rho$ at most a constant, so the ratio is $O(1)$ for these classes.
- **Advice.** In the [advice model](/advice-model/), the algorithm reads bits written by an oracle that knows the input. Boyar, Favrholdt, Kudahl and Mikkelsen (2015) placed independent set in a class of problems, called AOC, for which they found the number of advice bits needed for each ratio $c$; it is of order $n / c$.
- **Interval and geometric graphs.** When the vertices are intervals that arrive one by one, the problem is a form of [online interval scheduling](/online-interval-scheduling/) without preemption. The worst case stays $\Omega(n)$ (Theorem 3).
- **Bounded degree.** If each vertex has degree at most $\Delta$, greedy has ratio at most $\Delta$ (Theorem 4).

## Examples

**The adversary for greedy.** Greedy accepts each vertex that has no edge to $I$. Vertex $v_1$ arrives and greedy accepts it. Then $v_2, v_3, v_4, v_5$ arrive, each with one edge to $v_1$ and no other edges.

| vertex | edges to earlier vertices | greedy | $I$ after |
|---|---|---|---|
| $v_1$ | none | accept | $\{v_1\}$ |
| $v_2$ | $v_1$ | refuse | $\{v_1\}$ |
| $v_3$ | $v_1$ | refuse | $\{v_1\}$ |
| $v_4$ | $v_1$ | refuse | $\{v_1\}$ |
| $v_5$ | $v_1$ | refuse | $\{v_1\}$ |

The graph is a star. Greedy has 1 vertex and $\{v_2, v_3, v_4, v_5\}$ is independent, so the ratio is $4 = n - 1$. An algorithm that refuses $v_1$ is not safe either: then the adversary can stop after $v_1$, or keep each new vertex adjacent to the vertices that the algorithm accepts (Theorem 1).

**Nested intervals.** The first pair is the intervals $[0, 0.49]$ and $[0.51, 1]$. A coin picks one of them, say the second, and the next pair lies inside it: $[0.52, 0.75]$ and $[0.76, 0.99]$. The construction goes on in this way. An interval that holds the next pair overlaps every later interval. The interval of each pair that was not picked is disjoint from all later intervals. So the optimum takes the free interval of each pair and both intervals of the last pair. With $k$ pairs, $\mathrm{OPT} = k + 1$. An online algorithm does not know which interval of a pair will be picked, so each interval it accepts blocks the rest of the input with probability $1/2$.

## Known algorithms

- **Greedy.** Accept each vertex with no edge to $I$. The result is a maximal independent set of the graph, as in the offline [greedy independent set](/greedy-independent-set/) rule, but in arrival order. Ratio $n - 1$ for $n \ge 2$ (Theorem 2), and $\Delta$ on graphs of maximum degree $\Delta$ (Theorem 4).
- **Many sets at once.** In the multi-solution model with polynomially many sets, Halldorsson et al. give an algorithm with ratio $O(n / \log n)$, and in general $O(n / \log r(n))$ for $r(n)$ sets. The construction is in the cited paper.
- **Sampling algorithms.** For random arrival order, the algorithm of Gobel et al. observes a first part of the input and uses it to decide which later vertices to accept. Its ratio is $O(\rho^2)$ on graphs with inductive independence number $\rho$.

## Bounds

**Theorem 1 (deterministic lower bound).** For each deterministic online algorithm and each $n \ge 2$, there is a graph with $n$ vertices on which the algorithm gets ratio at least $n - 1$, or accepts no vertex while $\mathrm{OPT} \ge 1$.

*Proof.* The adversary gives each new vertex an edge to every vertex that the algorithm has accepted so far, and no other edge. If the algorithm accepts no vertex among $v_1, \ldots, v_n$, the graph has no edges and $\mathrm{ALG} = 0 < n = \mathrm{OPT}$. Otherwise let $v_s$ be the first vertex it accepts. Each later vertex has an edge to $v_s$, so the algorithm can accept no later vertex, and $\mathrm{ALG} = 1$. Every edge of the graph has $v_s$ as an endpoint, because $v_s$ is the only vertex ever accepted. So $V \setminus \{v_s\}$ is independent, and $\mathrm{OPT} \ge n - 1$. $\square$

**Theorem 2 (greedy matches it).** For $n \ge 2$, greedy has $\mathrm{OPT} \le (n - 1) \cdot \mathrm{ALG}$.

*Proof.* Greedy accepts $v_1$, so $\mathrm{ALG} \ge 1$. If $\mathrm{ALG} \ge 2$, then $\mathrm{OPT} \le n \le 2(n - 1) \le (n - 1) \mathrm{ALG}$. If $\mathrm{ALG} = 1$, then $I = \{v_1\}$, and each later vertex was refused, so it has an edge to $v_1$. An independent set that holds $v_1$ is then $\{v_1\}$ alone, and one that does not hold $v_1$ has at most $n - 1$ vertices. So $\mathrm{OPT} \le n - 1$. $\square$

**Theorem 3 (randomized lower bound on interval graphs, Gobel et al. 2014).** For each randomized online algorithm and each even $n$, there is an interval graph with $n$ vertices on which $\mathrm{OPT} \ge (n/4 + 1/2) \cdot \mathbb{E}[\mathrm{ALG}]$. So the ratio is $\Omega(n)$ even for randomized algorithms and even for interval graphs.

*Proof.* By [Yao's principle](/yao-minimax-principle/), it is enough to give a distribution over inputs on which each deterministic algorithm has $\mathbb{E}[\mathrm{ALG}] \le 2$ and $\mathrm{OPT} \ge n/2 + 1$ on every input. Let $k = n/2$. The input is $k$ pairs of disjoint intervals, sent in order, each pair as two vertices. For $t < k$, a fair coin, independent of all else, picks one interval $c_t$ of pair $t$, and pair $t + 1$ is placed strictly inside $c_t$. The other interval $o_t$ of pair $t$ is disjoint from $c_t$ and so from every later interval.

The set $\{o_1, \ldots, o_{k-1}\}$ together with both intervals of pair $k$ is independent, so $\mathrm{OPT} \ge k + 1$. (It is exactly $k + 1$, but the proof needs only the lower bound.)

Now fix a deterministic algorithm. Let $V_t$ be the largest expected number of intervals that it can still accept from pairs $t, \ldots, k$, given that no accepted interval overlaps pair $t$. Then $V_k \le 2$. For $t < k$, the coin for pair $t$ is tossed after the algorithm has decided on both of its intervals, so the decisions do not depend on it. If the algorithm accepts no interval of pair $t$, it gets at most $V_{t+1}$. If it accepts one, that interval is $c_t$ with probability $1/2$, and then it overlaps all later intervals, so the algorithm gets at most $1 + V_{t+1}/2$. If it accepts both, one of them is $c_t$, and it gets exactly 2. By induction $V_{t+1} \le 2$, so each case gives at most 2, and $V_t \le 2$. So $\mathbb{E}[\mathrm{ALG}] \le V_1 \le 2$, and the ratio is at least $(k + 1)/2 = n/4 + 1/2$. $\square$

**Theorem 4 (bounded degree).** If every vertex has degree at most $\Delta \ge 1$, greedy has $\mathrm{OPT} \le \Delta \cdot \mathrm{ALG}$.

*Proof.* Let $O$ be a maximum independent set. Each $u \in O \setminus I$ was refused, so it has a neighbour in $I$; send $u$ to one such neighbour. A vertex $v \in I$ receives at most $\Delta$ vertices. If $v \in O$, it receives none, because $O$ is independent, and it counts once. So each $v \in I$ accounts for at most $\Delta$ vertices of $O$, and $\lvert O \rvert \le \Delta \lvert I \rvert$. $\square$

The star of the examples has $\Delta = n - 1$ and ratio $n - 1$, so Theorem 4 is tight for greedy on stars.

**Offline hardness.** A polynomial-time online algorithm is also an offline algorithm. Offline, maximum independent set is as hard to approximate as [maximum clique](/clique-inapproximability/): no ratio $n^{1 - \varepsilon}$ in polynomial time unless P = NP. Theorems 1 and 3 need no such assumption and hold for algorithms with unlimited time.

| model | upper bound | lower bound |
|---|---|---|
| one set, deterministic | $n - 1$ (Theorem 2) | $n - 1$ (Theorem 1) |
| one set, randomized | $n - 1$ | $n/4 + 1/2$, also on interval graphs (Theorem 3) |
| maximum degree $\Delta$, greedy | $\Delta$ (Theorem 4) | $\Delta$ for greedy (the star) |
| $r(n)$ constant sets | $O(n)$ | $\Omega(n)$ (Halldorsson et al.) |
| polynomially many sets | $O(n / \log n)$ | $\Omega(n / \log n)$ (Halldorsson et al.) |
| random order, inductive independence $\rho$ | $O(\rho^2)$ (Gobel et al.) | not covered here |

## Reductions

- **Complement of online vertex cover.** In the model where each vertex is decided at its arrival, the vertices left out of a cover form an independent set, and the other way round. So a rule for one problem gives a rule for the other. The ratios do not carry over, because $n - \alpha(G)$ and $\alpha(G)$ behave very differently; see [online vertex cover](/online-vertex-cover-problem/).
- **One color class of an online coloring.** An online coloring with $\chi$ colors, run on the same sequence, has a color class with at least $n / \chi$ vertices. But the algorithm does not know in advance which class will be the largest, so this gives an independent set only in the multi-solution model, with one set for each color. See [online graph coloring](/online-graph-coloring-problem/).
- **From interval scheduling.** Intervals that arrive one by one and must be accepted or refused at once are an instance on interval graphs. So Theorem 3 applies to them when the adversary chooses the arrival order. The nested pairs above do not arrive in order of start time.

## Applications

- **Admission control.** Requests that conflict with each other arrive one by one, and each must be accepted or refused at once. Accepted requests may not conflict. Gobel et al. apply their sampling approach to an admission control setting.
- **Wireless transmissions.** Transmitters that interfere with each other can be modelled by a disk graph, which has bounded inductive independence number. So the random order results give a constant ratio for them.
- **A limit case for online packing.** The problem shows that online packing without structure is hopeless in the worst case, and so it explains why online packing results use weights, bounded sizes, random order or several solutions.

## References
