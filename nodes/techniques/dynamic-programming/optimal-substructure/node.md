---
tag: NB2NY6
kind: concept
slug: optimal-substructure
name: Optimal substructure
area: techniques/dynamic-programming
level: intro
summary: An optimal solution to a problem contains optimal solutions to its subproblems.
prereqs: [recursion, cut-and-paste-argument]
see_also: [overlapping-subproblems, independent-subproblems, principle-of-optimality, memoization, tabulation, subproblem-graph, greedy-choice-property, shortest-path-optimal-substructure]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.3, Elements of dynamic programming (the subsection on optimal substructure, with the longest simple path example)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Chapter 6, Sections 6.1 and 6.2 (weighted interval scheduling and the principles of dynamic programming)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 6, Dynamic programming
---

A problem has optimal substructure when an optimal solution of an instance is made of a choice and of optimal solutions of smaller instances of the same problem. It is the property that lets you write the optimum as a [recursion](/recursion/) over subproblems, and it is the first of the two properties that dynamic programming needs; the second is [overlapping subproblems](/overlapping-subproblems/). The usual proof of the property is a [cut-and-paste argument](/cut-and-paste-argument/). A [greedy algorithm](/greedy-algorithm/) also needs it, together with a safe first choice.

## In plain words

Suppose you know the best way to drive from one city to another. Take any town on that route. The part of the route from the start to that town is also the best way to reach that town. If a better way existed, you could use it and get a better full route.

A problem with this property can be solved from the bottom: find the best answers for small pieces, then build the best answer for the whole from them. You do not know in advance which piece the best answer uses. So you try each possible first choice, combine it with the best answer for what is left, and keep the best result.

The property is not free. It fails when the pieces of a solution must avoid each other, or when the score of the whole does not grow with the score of the parts.

## The idea

### The definition

Fix an optimization problem. Each instance $I$ has a set $\mathcal{F}(I)$ of feasible solutions and a cost $c(X)$ for each $X \in \mathcal{F}(I)$. Let $\mathrm{OPT}(I)$ be the least cost (for a maximization problem, read every minimum as a maximum and turn the inequalities around).

A *decomposition* gives, for each instance $I$ that is not a base case, a finite set of choices $C(I)$. A choice $k \in C(I)$ names subinstances $I_1, \ldots, I_m$, each smaller than $I$ in a fixed well-founded order, and a combination rule: from $X_j \in \mathcal{F}(I_j)$ it builds $X = \mathrm{comb}_k(X_1, \ldots, X_m)$ with cost

$$ c(X) = g_k\bigl(c(X_1), \ldots, c(X_m)\bigr), $$

where $g_k$ is non-decreasing in each argument. The usual case is $g_k = w_k + \sum_j c(X_j)$ for a fixed weight $w_k$ of the choice.

The problem has **optimal substructure** with respect to this decomposition when these two conditions hold.

1. **Cover.** Each optimal solution $X^\ast$ of $I$ is $\mathrm{comb}_k(X_1, \ldots, X_m)$ for some choice $k \in C(I)$, and each $X_j$ is an optimal solution of $I_j$.
2. **Closure.** For each $k \in C(I)$ and each tuple of feasible $X_j \in \mathcal{F}(I_j)$, the combination $\mathrm{comb}_k(X_1, \ldots, X_m)$ is feasible for $I$.

The cover condition is the one that textbooks call optimal substructure. The closure condition says that the parts do not interfere. The page on [independent subproblems](/independent-subproblems/) treats it in detail.

### The recurrence

**Claim.** Under the two conditions, for every instance $I$ that is not a base case,

$$ \mathrm{OPT}(I) = \min_{k \in C(I)} g_k\bigl(\mathrm{OPT}(I_1), \ldots, \mathrm{OPT}(I_m)\bigr). $$

**Proof.** First, $\le$. Fix $k \in C(I)$ and pick an optimal $X_j$ for each $I_j$. By closure, $X = \mathrm{comb}_k(X_1, \ldots, X_m)$ is feasible for $I$, so $\mathrm{OPT}(I) \le c(X) = g_k(\mathrm{OPT}(I_1), \ldots, \mathrm{OPT}(I_m))$. This holds for each $k$, so it holds for the minimum. Second, $\ge$. Let $X^\ast$ be optimal for $I$. By cover, $X^\ast = \mathrm{comb}_k(X_1, \ldots, X_m)$ for some $k$, with each $X_j$ optimal for $I_j$. Then $\mathrm{OPT}(I) = c(X^\ast) = g_k(\mathrm{OPT}(I_1), \ldots, \mathrm{OPT}(I_m))$, which is at least the minimum over $k$. ∎

The proof shows what each condition does. Cover gives the lower bound: no solution is cheaper than the best combination. Closure gives the upper bound: each combination is a real solution. A recurrence that you write without checking both can be wrong in either direction.

The cover condition is usually proved by cut and paste. Take an optimal $X^\ast$ and its choice $k$. If some part $X_j$ is not optimal for $I_j$, replace it by a cheaper $Y_j$. By closure the result is feasible. If $g_k$ is strictly increasing in its $j$-th argument, the result is cheaper than $X^\ast$, which is a contradiction. If $g_k$ is only non-decreasing, the argument shows a weaker fact: some optimal solution has optimal parts. That weaker fact is enough for the $\ge$ direction, because the proof needs only one optimal $X^\ast$ with optimal parts.

### How to find the decomposition

CLRS gives a common pattern for discovering the property.

1. Show that a solution consists of a choice, such as the first cut of a rod or the last split of a matrix product.
2. Assume that you know the choice of an optimal solution. You do not yet know how to find it.
3. Find the subproblems that remain after this choice, and describe the space of all such subproblems as simply as you can.
4. Prove by cut and paste that the parts of an optimal solution are optimal for these subproblems.

Keep the space of subproblems small. For rod cutting, "the best value for a rod of length $j$" for $0 \le j \le n$ is enough. For a product $A_1 A_2 \cdots A_n$ of matrices, prefixes are not enough, because the split of a prefix leaves a range in the middle. The subproblems must be all ranges $A_i \cdots A_j$.

### The cost of the resulting algorithm

The two numbers that set the running time are the number of distinct subproblems and the number of choices for each one. With [memoization](/memoization/) or [tabulation](/tabulation/), each subproblem is solved once, so the time is the sum over all subproblems of the number of choices, times the cost of one choice. In terms of the [subproblem graph](/subproblem-graph/), this is the number of vertices plus the number of edges.

| problem | subproblems | choices each | time |
| --- | --- | --- | --- |
| [rod cutting](/rod-cutting-problem/), length $n$ | $n + 1$ | at most $n$ | $\Theta(n^2)$ |
| [matrix-chain multiplication](/matrix-chain-multiplication/), $n$ matrices | $\Theta(n^2)$ ranges | at most $n - 1$ | $\Theta(n^3)$ |
| [longest common subsequence](/longest-common-subsequence/), lengths $m$ and $n$ | $(m+1)(n+1)$ | at most 2 | $\Theta(mn)$ |

## Examples

### Rod cutting

A rod of length $n$ sells in pieces, and a piece of length $i$ has price $p_i$. With the prices $p_1, \ldots, p_{10} = 1, 5, 8, 9, 10, 17, 17, 20, 24, 30$ of CLRS Section 14.1, the best revenue $r_j$ for $j = 0, \ldots, 10$ is $0, 1, 5, 8, 10, 13, 17, 18, 22, 25, 30$. The choice is the length $i$ of the first piece. The rest is a rod of length $j - i$, and any cutting of it can follow any first piece, so closure holds. Cut and paste proves cover: if the rest were cut in a way worth less than $r_{j-i}$, the best cutting of the rest would give more. So

$$ r_j = \max_{1 \le i \le j} \bigl(p_i + r_{j-i}\bigr), \qquad r_0 = 0. $$

For $j = 4$, the best is $10$, with two pieces of length 2. The rest after the first piece is a rod of length 2, and its cutting (one piece of length 2, worth 5) is optimal, since $r_2 = 5$.

### Shortest paths

In a directed graph with no negative cycle, each subpath of a shortest path is a shortest path. A shortest path from $s$ to $v$ is a shortest path from $s$ to some predecessor $u$, followed by the edge $(u, v)$. This gives the recurrence of [Bellman-Ford](/bellman-ford/) and of [shortest paths in a DAG](/dag-shortest-paths/). The page [shortest-path optimal substructure](/shortest-path-optimal-substructure/) has the proof.

### Longest common subsequence

If $Z$ is a longest common subsequence of $X$ and $Y$ and the last items of $X$ and $Y$ are equal, then $Z$ ends with that item, and the rest of $Z$ is a longest common subsequence of the two prefixes. The full statement has three cases and is the [LCS optimal-substructure theorem](/lcs-optimal-substructure/).

### Non-example: longest simple path

Take the complete graph on the three vertices $a$, $b$, $c$, with unit weights. The longest simple path from $a$ to $c$ is $a, b, c$, with 2 edges. Its part from $a$ to $b$ has 1 edge, but the longest simple path from $a$ to $b$ is $a, c, b$, with 2 edges. If you paste $a, c, b$ in front of $b, c$, you get $a, c, b, c$, which repeats $c$ and is not simple. Closure fails: the two parts compete for the same vertices. No polynomial-time algorithm for the [longest path problem](/longest-path-problem/) is known, since it contains the [Hamiltonian path problem](/hamiltonian-path-problem/). In a [directed acyclic graph](/directed-acyclic-graph/) the parts cannot share a vertex, and the [longest path in a DAG](/dag-longest-path/) has optimal substructure.

### Non-example: a cost that is not monotone

Let the cost of a path be its total weight modulo 10, to be minimized. Take the edges $s \to a$ of weight 1, $s \to b$ of weight 2, $b \to a$ of weight 3 and $a \to t$ of weight 5. The path $s, a, t$ costs $6$, and the path $s, b, a, t$ costs $10 \bmod 10 = 0$, so it is the only optimal path. Its prefix $s, b, a$ costs 5, but the best path from $s$ to $a$ is the edge $s \to a$, with cost 1. So no optimal path from $s$ to $t$ has an optimal prefix. The combination "add the weights, then reduce modulo 10" is not non-decreasing in the cost of the prefix, and the cut-and-paste step fails.

### Optimal substructure without a fast algorithm

The property alone does not make a problem easy. In the [traveling salesman problem](/traveling-salesman-problem/), the subproblems "best path that starts at a fixed city, visits exactly the set $S$ and ends at $v$" have optimal substructure. With the start city fixed, there are $(n-1)2^{n-2}$ such pairs $(S, v)$, and the [Held-Karp algorithm](/held-karp-algorithm/) solves them in $O(n^2 2^n)$ time. The number of subproblems, not the property, decides the cost.

## Where it is used

- **Dynamic programming.** Every DP algorithm rests on a recurrence, and the recurrence is correct only when the problem has optimal substructure for the chosen subproblems. [Memoization](/memoization/) and [tabulation](/tabulation/) are two ways to evaluate it.
- **Greedy algorithms.** A greedy proof has two parts: the [greedy-choice property](/greedy-choice-property/) and optimal substructure for the subproblem that is left after the greedy choice.
- **Shortest paths.** [Dijkstra's algorithm](/dijkstra/), [Bellman-Ford](/bellman-ford/) and [Floyd-Warshall](/floyd-warshall/) all rely on the fact that subpaths of shortest paths are shortest.
- **Sequential decisions.** In control theory and in a [Markov decision process](/markov-decision-process/), the same property for policies is the [principle of optimality](/principle-of-optimality/). It gives the [Bellman equation](/bellman-equation/).
- **Design check.** When a first recurrence gives wrong answers, the usual reason is that the chosen subproblems do not have optimal substructure. The fix is to add information to the subproblem, such as the remaining capacity in a [knapsack](/knapsack-problem/) or the set of visited cities in Held-Karp.

## References
