---
tag: RG20X2
kind: technique
slug: reductions-for-algorithms
name: Reductions for algorithms
area: techniques/reductions-and-transforms
level: core
summary: Solves a new problem by transforming its instances into instances of a problem that already has a known algorithm.
prereqs: [reduction, max-flow-problem, strongly-connected-components]
see_also: [reduction-to-sorting, reduction-to-linear-programming, longest-to-shortest-paths-reduction, bipartite-matching, 2-sat, transform-and-conquer, optimization-to-decision-reduction, vertex-splitting]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Chapter 24, Maximum flow (the section on maximum bipartite matching); Chapter 22, Single-source shortest paths (shortest paths in directed acyclic graphs)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 7.5, A first application, the bipartite matching problem; Section 8.1, Polynomial-time reductions
  - paper: doi:10.1016/0020-0190(79)90002-4
    title: "Bengt Aspvall, Michael F. Plass and Robert Endre Tarjan, A linear-time algorithm for testing the truth of certain quantified boolean formulas, Information Processing Letters 8(3) (1979), 121-123"
    locator: the implication graph of a 2-CNF formula and the test by strongly connected components
  - book: isbn:9780132316811
    title: Anany Levitin, Introduction to the Design and Analysis of Algorithms, third edition, Pearson, 2012
    locator: Chapter 6, Transform-and-Conquer (the section on problem reduction)
  - paper: doi:10.1145/321694.321699
    title: "Jack Edmonds and Richard M. Karp, Theoretical improvements in algorithmic efficiency for network flow problems, Journal of the ACM 19(2) (1972), 248-264"
    locator: the shortest augmenting path rule and its bound on the number of augmentations
---

A reduction for algorithms solves a new problem $A$ by turning each instance into an instance of a problem $B$ that already has a good algorithm, running that algorithm, and turning its answer into an answer for $A$. It is the forward use of a [reduction](/reduction/): the goal is an upper bound, an algorithm, and not a hardness result. The running time is the time of the transform, plus the time of the algorithm for $B$ on the transformed size, plus the time to recover the answer. Typical targets are [sorting](/reduction-to-sorting/), shortest paths, [maximum flow](/max-flow-problem/), [strongly connected components](/strongly-connected-components/) and [linear programming](/reduction-to-linear-programming/).

## In plain words

When a new problem comes up, first ask whether it is an old problem in disguise. Often a small change of view shows it: draw a graph from the input, sort a copy of it, flip the sign of the weights, or add a start and an end node. Then a tested algorithm for the old problem does the hard work, and you write only the code that translates in and out.

The price of the translation counts. A translation that makes the input much larger, or that is slower than the old algorithm, can give a result that is correct but slow. A translation must also meet every condition of the old algorithm, for example "no negative weights" or "the graph has no cycles".

## When it applies

- The input can be read as a graph, and the question is about paths, cuts, pairings or reachability.
- The question asks to choose pairs, or to assign items to slots, with each item used at most once. This points to matching or flow.
- The question involves order, duplicates or neighbours in value. This points to sorting.
- The question asks for a maximum where a known algorithm finds a minimum, or the reverse. A sign change may convert one to the other.
- The constraints have two variables each and are "if this, then that". This points to an implication graph.

## The template

```pseudo id=main
SOLVE-A(x)                         ▷ x an instance of A of size n
L1  y ← TRANSFORM(x)                 ▷ time t_T(n); |y| ≤ s(n)
L2  z ← SOLVE-B(y)                   ▷ known algorithm, time T_B(|y|)
L3  w ← RECOVER(x, y, z)             ▷ time t_R(n)
L4  return w
```

The holes are TRANSFORM, the choice of $B$ with its algorithm, and RECOVER. Three facts must be shown: TRANSFORM produces a valid instance of $B$ that meets every precondition of the chosen algorithm; RECOVER maps every correct answer for $y$ to a correct answer for $x$; and the costs below.

**Cost rule.** Let $T_B$ be non-decreasing. Then the worst-case time of SOLVE-A on inputs of size $n$ is

$$T_A(n) \ \le\ t_T(n) + T_B(s(n)) + t_R(n).$$

*Proof.* On an input of size $n$, line L1 takes at most $t_T(n)$ steps and gives $|y| \le s(n)$. Line L2 takes $T_B(|y|) \le T_B(s(n))$ steps, since $T_B$ is non-decreasing. Line L3 takes at most $t_R(n)$ steps. Add the three bounds. $\square$

If SOLVE-A calls the algorithm for $B$ several times, on instances $y_1, \ldots, y_k$, the middle term becomes $\sum_{i=1}^{k} T_B(|y_i|)$, and $t_T$ and $t_R$ count all the work outside the calls. A reduction gives a faster algorithm for $A$ only when the sum is smaller than the time of the best direct method.

## Classic examples

The examples go from simple to hard. Each gives the transform, the proof of correctness and the cost.

### Element distinctness and mode to sorting

Sort the $n$ items, then scan neighbours: equal items are next to each other in sorted order. [Element distinctness](/element-distinctness/) and [mode finding](/mode-finding/) then take $O(n \log n) + O(n)$ comparisons. The details are on [presorting](/presorting/), and [reduction to sorting](/reduction-to-sorting/) gives reductions that sort derived keys.

### Longest path in a DAG to shortest path by negation

Given a directed acyclic graph with weights $w$, set $w'(e) = -w(e)$. For each path $P$, $w'(P) = -w(P)$, so a path is longest under $w$ if and only if it is shortest under $w'$. A DAG has no cycles, so it has no negative cycles under $w'$, and [shortest paths in a DAG](/dag-shortest-paths/) by [topological sort](/topological-sort/) work with negative weights. The time is $O(V + E)$ for the transform and $O(V + E)$ for the solver. See [longest-to-shortest-paths reduction](/longest-to-shortest-paths-reduction/) and [DAG longest path](/dag-longest-path/). The transform needs both conditions: it fails with [Dijkstra's algorithm](/dijkstra/), which needs non-negative weights, and it fails on a graph with cycles, where the [longest simple path problem](/longest-path-problem/) is NP-hard.

### Longest increasing subsequence to longest common subsequence

Let $a$ be a sequence and let $b$ be the distinct values of $a$ in increasing order. Claim: the length of a longest strictly increasing subsequence of $a$ equals the length of a [longest common subsequence](/longest-common-subsequence/) of $a$ and $b$.

*Proof.* A common subsequence of $a$ and $b$ is a subsequence of $b$, so it is strictly increasing, and it is a subsequence of $a$. Conversely, a strictly increasing subsequence of $a$ has distinct values in increasing order, all of them values of $a$, so it is a subsequence of $b$ as well. The two sets of sequences are equal, so their maximum lengths are equal. $\square$

For $a = (3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5)$, $b = (1, 2, 3, 4, 5, 6, 9)$, and the LCS has length $4$, for example $(3, 4, 5, 9)$. The cost is $O(n \log n)$ to build $b$ and $O(n^2)$ for the dynamic program of LCS, so $O(n^2)$ in total. This reduction is correct but slower than the direct $O(n \log n)$ method of [longest increasing subsequence](/longest-increasing-subsequence/) by [patience sorting](/patience-sorting/). It shows that a reduction proves an upper bound, not the best one.

### Bipartite matching to maximum flow

Let $G = (L \cup R, E)$ be a [bipartite graph](/bipartite-graph/). Build a flow network $N$: a source $s$, a sink $t$, an arc $s \to u$ of capacity $1$ for each $u \in L$, an arc $u \to v$ of capacity $1$ for each edge $\{u, v\} \in E$ with $u \in L$, and an arc $v \to t$ of capacity $1$ for each $v \in R$. Claim: the size of a [maximum matching](/bipartite-matching/) of $G$ equals the value of a maximum flow in $N$, and an integral maximum flow gives a maximum matching.

*Proof.* A matching $M$ gives a flow of value $|M|$: send one unit along $s \to u \to v \to t$ for each edge $\{u, v\} \in M$. No arc gets more than one unit, since the edges of $M$ share no endpoint. Conversely, all capacities are integers, so the [Ford-Fulkerson method](/ford-fulkerson/) returns an integral maximum flow $f$ ([flow integrality theorem](/flow-integrality-theorem/)). Each $u \in L$ receives at most one unit, from $s$, so at most one arc out of $u$ carries flow. Each $v \in R$ sends at most one unit, to $t$, so at most one arc into $v$ carries flow. The arcs $u \to v$ with $f(u, v) = 1$ form a matching, and its size equals the flow across the cut $(\{s\} \cup L, R \cup \{t\})$, which is $|f|$. $\square$

*Cost.* $N$ has $|L| + |R| + 2$ vertices and $|E| + |L| + |R|$ arcs. Each augmentation of Ford-Fulkerson finds a path in $O(V + E)$ time and raises the value by $1$, and the value is at most $\min(|L|, |R|)$. So the time is $O(\min(|L|, |R|) \cdot (V + E)) = O(VE)$ for a graph without isolated vertices. RECOVER reads the matching in $O(E)$ time. The [Hopcroft-Karp algorithm](/hopcroft-karp/) finds a maximum bipartite matching in $O(E \sqrt{V})$ time.

*Worked example.* Let $L = \{a_1, a_2, a_3\}$, $R = \{b_1, b_2, b_3\}$ and $E = \{a_1 b_1, a_1 b_2, a_2 b_1, a_3 b_2, a_3 b_3\}$. The network has $8$ vertices and $11$ arcs. Breadth-first search for augmenting paths, with neighbours taken in name order, finds:

| Step | Augmenting path | Flow value |
|---|---|---|
| 1 | $s, a_1, b_1, t$ | 1 |
| 2 | $s, a_3, b_2, t$ | 2 |
| 3 | $s, a_2, b_1, a_1, b_2, a_3, b_3, t$ | 3 |

Path 3 uses the residual arcs $b_1 \to a_1$ and $b_2 \to a_3$: it moves $a_1$ from $b_1$ to $b_2$ and $a_3$ from $b_2$ to $b_3$, and frees $b_1$ for $a_2$. After step 3 the residual network has no path from $s$ to $t$. The arcs from $L$ to $R$ with flow $1$ are $a_1 b_2$, $a_2 b_1$, $a_3 b_3$, a perfect matching of size $3$. The total work is $3$ searches on a network with $8$ vertices and $11$ arcs, plus one pass over the $5$ edges to recover the matching. Greedy matching in name order takes $a_1 b_1$, finds $b_1$ taken for $a_2$, takes $a_3 b_2$, and stops with $2$ pairs. The residual arcs of the flow network undo such early choices.

### 2-SAT to strongly connected components

Let $\varphi$ be a [2-SAT](/2-sat/) formula with $n$ variables and $m$ clauses. The [implication graph](/implication-graph/) has a vertex for each of the $2n$ literals and, for each clause $(a \vee b)$, the arcs $\neg a \to b$ and $\neg b \to a$, so $2m$ arcs. Each arc $\ell \to \ell'$ means "if $\ell$ is true, then $\ell'$ must be true". Claim (Aspvall, Plass and Tarjan, 1979): $\varphi$ is satisfiable if and only if no variable $x$ has $x$ and $\neg x$ in the same strongly connected component.

*Proof.* If $x$ and $\neg x$ are in the same component, there are paths $x \leadsto \neg x$ and $\neg x \leadsto x$. A satisfying assignment makes true the head of each arc whose tail is true, so along a path from a true literal all literals are true. If $x$ is true, then $\neg x$ is true; if $\neg x$ is true, then $x$ is true. Both are impossible, so $\varphi$ is unsatisfiable.

For the converse, fix a topological order $\prec$ of the components (the condensation is acyclic), and write $C(\ell)$ for the component of $\ell$. Make $\ell$ true when $C(\neg \ell) \prec C(\ell)$. This is well defined, since $C(x) \ne C(\neg x)$, and it gives exactly one of $x$, $\neg x$ the value true. Suppose a clause $(a \vee b)$ has $a$ and $b$ both false, that is $C(a) \prec C(\neg a)$ and $C(b) \prec C(\neg b)$. The arc $\neg a \to b$ gives $C(\neg a) \preceq C(b)$, and the arc $\neg b \to a$ gives $C(\neg b) \preceq C(a)$. Then $C(a) \prec C(\neg a) \preceq C(b) \prec C(\neg b) \preceq C(a)$, which is impossible. So every clause is true. $\square$

*Cost.* The graph is built in $O(n + m)$ time, [Tarjan's algorithm](/tarjan-scc/) finds the components in $O(n + m)$ time, and the test and the assignment take $O(n)$. The total is $O(n + m)$.

*Example.* For $(x_1 \vee x_2) \wedge (\neg x_1 \vee x_3) \wedge (\neg x_2 \vee \neg x_3) \wedge (\neg x_1 \vee \neg x_2)$ the eight arcs form two components, $\{x_1, x_3, \neg x_2\}$ and $\{\neg x_1, \neg x_3, x_2\}$, with no arc between them. Either order is topological. Putting the first component later gives $x_1 = 1, x_2 = 0, x_3 = 1$, and the other order gives $x_1 = 0, x_2 = 1, x_3 = 0$. These are the only two satisfying assignments of the formula. Adding the clauses $(\neg x_1 \vee \neg x_3)$ and $(x_1 \vee \neg x_2)$ merges all six literals into one component, so the larger formula is unsatisfiable.

## Variations

- **Several calls.** [Binary search on the answer](/binary-search-on-answer/) and the [optimization-to-decision reduction](/optimization-to-decision-reduction/) call a decision algorithm $O(\log W)$ times, where $W$ is the range of the answer. The cost rule then has the sum of the calls in the middle term.
- **Changing the graph.** [Vertex splitting](/vertex-splitting/) turns vertex capacities into arc capacities, and the [bipartite double cover](/bipartite-double-cover/) turns a question about a general graph into one about a bipartite graph. [Path cover by bipartite matching](/path-cover-by-bipartite-matching/) reduces a covering problem on a DAG to matching.
- **Reduction to a general solver.** Linear programming, integer programming and SAT solvers accept many problems. The page [reduction to linear programming](/reduction-to-linear-programming/) treats the first case and its integrality issues.
- **Transform and conquer.** Presorting and change of representation are reductions inside one problem. See [transform and conquer](/transform-and-conquer/) and [presorting](/presorting/).
- **Chains.** Reductions compose: if $A$ reduces to $B$ and $B$ to $C$, the costs add with the sizes passed along, $t_T^{A \to B}(n) + t_T^{B \to C}(s(n))$ and so on.

## Pitfalls

- **The reduction is slower than a direct method.** LIS through LCS takes $O(n^2)$ time, while a direct algorithm takes $O(n \log n)$. Compare the total with the best known direct bound.
- **The size grows.** The time of the solver depends on $|y|$. A transform that builds a complete graph on $n$ items gives $\Theta(n^2)$ arcs even when the input has $n$ numbers.
- **A precondition of the solver fails.** Negated weights break Dijkstra's algorithm. Negation on a graph with cycles can create negative cycles. Check every assumption of the chosen algorithm on the transformed instance.
- **The answer is not integral.** The matching reduction needs an integral maximum flow. Ford-Fulkerson with integer capacities gives one; a general flow or LP solver may return a fractional optimum of the same value, and RECOVER must then convert it.
- **The recovery step is missing.** Many reductions give the right value but need extra work to return the object: the matching is read from the arcs with flow, the assignment of 2-SAT from the order of the components.
- **Only one direction of correctness.** RECOVER must be correct for every correct answer of $B$, not only for the one that a particular solver returns.

## Exercises

1. Reduce the problem "find the maximum number of arc-disjoint paths from $s$ to $t$ in a directed graph" to maximum flow, and prove the claim with the flow integrality theorem.
2. Reduce the problem of [vertex-disjoint](/vertex-splitting/) paths to the problem of arc-disjoint paths, and give the size of the new graph.
3. Give a reduction from "longest non-decreasing subsequence" to LCS. What must change in the sequence $b$?
4. Reduce the problem of finding a path with the largest product of positive weights in a DAG to a shortest path problem.
5. In the 2-SAT example, list the eight arcs of the implication graph and check that the two components have no arc between them.
6. A transform takes $O(n \log n)$ time and builds an instance of size $2n$ for a problem solved in $O(m^{1.5})$ time. Give the total time, and say which term dominates.

## References
