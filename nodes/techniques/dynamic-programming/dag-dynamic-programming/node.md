---
tag: 2GCN5E
kind: technique
slug: dag-dynamic-programming
name: Dynamic programming on DAGs
aliases:
- Dynamic programming in DAGs
area: techniques/dynamic-programming
level: core
summary: Solves recursive problems on directed acyclic graphs by computing values in reverse topological order, so each subproblem is solved after its dependencies.
prereqs: [directed-acyclic-graph, topological-sort, optimal-substructure]
see_also: [dp-on-dag, subproblem-graph, longest-increasing-subsequence, edit-distance, coin-change-problem, rod-cutting-problem, tabulation, memoization]
sources:
  - book: isbn:9780073523408
    title: Dasgupta, Papadimitriou and Vazirani, Algorithms
    locator: Chapter 6, Sections 6.1 (shortest paths in dags, revisited), 6.2 (longest increasing subsequences), 6.3 (edit distance) and 6.4 (knapsack)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.1 (rod cutting and its subproblem graph) and Section 14.3 (elements of dynamic programming)
  - book: isbn:9780321295354
    title: Kleinberg and Tardos, Algorithm Design
    locator: Section 6.2 (principles of dynamic programming) and Section 6.6 (sequence alignment)
---

Dynamic programming on DAGs is a way to design a dynamic program: you define the states of a problem as the vertices of an implicit [directed acyclic graph](/directed-acyclic-graph/), with an edge for each step from one state to the next, so that the answer becomes a shortest path, a longest path or a path count in that graph. The values are then computed so that each state comes after all the states it depends on, which is a reverse [topological order](/topological-sort/) of the dependency edges. Dasgupta, Papadimitriou and Vazirani base their Chapter 6 on this view. This page is about building the graph from a problem that is not a graph problem; the pass over a graph that is given as input is [dynamic programming on directed acyclic graphs](/dp-on-dag/).

## In plain words

Many problems ask for the best sequence of choices: which coins to give, which pieces to cut, which letters to change. Write down the situation after some of the choices. Call it a state. A choice moves you from one state to a new state, and it has a cost or a gain.

Draw each state as a dot and each choice as an arrow. If the arrows can never lead back to a state you already left, the drawing has no loops. The best sequence of choices is now the best route from the start dot to the goal dot. To find it, compute the best route to each dot, in an order where each dot comes after all dots that point to it. That order exists because there are no loops.

## When it applies

Look for these signals.

- The solution is a sequence of decisions, and after each decision a small amount of information (the state) is enough to describe what is left.
- The cost or the gain of the whole sequence is a sum, a maximum or a product of the costs of the decisions.
- A measure, such as a length, an index or an amount, moves in one direction with each decision. This measure is a potential $\varphi$ with $\varphi(u) < \varphi(v)$ for each edge $u \to v$, and it proves that the graph has no cycle.
- The number of different states is small, polynomial in the input size or in a numeric parameter of it.

## The template

The holes are the set of states $S$, the start state $s$ and the goal states, the list $\mathrm{in}(v)$ of edges into each state with their weights, the potential $\varphi$, and the operations $\oplus$ and $\otimes$ of the [path pass](/dp-on-dag/).

```pseudo id=main
DAG-DESIGN(instance)
L1  S ← the states of the instance                  ▷ hole: what a state records
L2  for each state v, in(v) ← the edges (u, v, w)     ▷ hole: the last decision before v
L3  check that φ(u) < φ(v) for each edge (u, v)       ▷ hole: the potential; it proves there is no cycle
L4  for each state v in increasing order of φ do
L5      if v = s then L[v] ← 1
L6      else L[v] ← ⊕ over (u, v, w) in in(v) of L[u] ⊗ w   ▷ empty ⊕ is 0
L7  return ⊕ over the goal states g of L[g]
```

Line L1 is where the design happens. A state must hold all the information that the future decisions need, and nothing more. Line L2 lists, for each state, the possible last decisions. Line L3 is a proof, not code: if each edge raises $\varphi$, the order of line L4 is topological, and line L6 reads only values that are final. Lines L4 to L7 are the pass of [dynamic programming on directed acyclic graphs](/dp-on-dag/), and its correctness proof carries over.

**The direction of the edges.** In this page an edge $u \to v$ means "a decision leads from $u$ to $v$", and $L[v]$ is computed from its predecessors in increasing topological order. CLRS draws the [subproblem graph](/subproblem-graph/) the other way: an edge from a subproblem to each smaller subproblem that it needs. In that picture the same evaluation order is a *reverse* topological order. Both say the same thing: compute a state after every state it depends on.

**The cost.** The time is the number of edges times the cost of one $\otimes$ and one $\oplus$, plus the number of states. The space is the number of states, for the values $L$. If a state also stores the edge that gave its value, a [traceback](/traceback/) along these edges recovers the decisions.

## Classic examples

### Longest increasing subsequence

Given $a_1, \ldots, a_n$, find the longest subsequence whose values strictly increase. The states are the positions $1, \ldots, n$, and there is an edge $i \to j$ when $i < j$ and $a_i < a_j$. An increasing subsequence is a path, and the potential is the index. With $L(j)$ the length of the longest path that ends at $j$,
$$ L(j) = 1 + \max\{\, L(i) : i < j,\ a_i < a_j \,\}, $$
with the maximum of an empty set taken as 0. The answer is $\max_j L(j)$. For $a = (5, 2, 8, 6, 3, 6, 9, 7)$, the example of DPV Section 6.2, the values are $L = (1, 1, 2, 2, 2, 3, 4, 4)$, and a longest subsequence is $2, 3, 6, 9$. The graph has up to $n(n-1)/2$ edges, so this takes $O(n^2)$ time. See [longest increasing subsequence](/longest-increasing-subsequence/) for the $O(n \log n)$ method.

### Edit distance

For strings $x$ of length $m$ and $y$ of length $n$, the states are the pairs $(i, j)$ with $0 \le i \le m$ and $0 \le j \le n$, meaning "the prefixes $x[1..i]$ and $y[1..j]$ are aligned". The edges go from $(i-1, j)$ (delete $x_i$, cost 1), from $(i, j-1)$ (insert $y_j$, cost 1) and from $(i-1, j-1)$ (keep or substitute, cost 0 if $x_i = y_j$ and 1 otherwise). The potential is $i + j$. The [edit distance](/edit-distance/) is the shortest path from $(0, 0)$ to $(m, n)$ in this grid DAG, which has $(m+1)(n+1)$ vertices and fewer than $3(m+1)(n+1)$ edges, so it takes $O(mn)$ time. For SNOWY and SUNNY the distance is 3. The same graph with other weights is the [alignment graph](/alignment-graph/) of [Needleman-Wunsch](/needleman-wunsch/).

### Coin change

To pay the amount $A$ with the fewest coins of the values $d_1, \ldots, d_k$, take the states $0, 1, \ldots, A$ and an edge $x - d_i \to x$ of weight 1 for each coin with $d_i \le x$. The potential is the amount, and it rises by at least 1 on each edge when all coin values are positive. The least number of coins is the shortest path from 0 to $A$, in $O(kA)$ time. For the values $\{1, 3, 4\}$ and $A = 6$, the shortest path is $0 \to 3 \to 6$, two coins, while the greedy choice $4 + 1 + 1$ uses three. See the [coin change problem](/coin-change-problem/).

### Rod cutting

To cut a rod of length $n$ into pieces with prices $p_1, \ldots, p_n$, take the states $0, 1, \ldots, n$ (the length already cut off) and an edge $j - i \to j$ of weight $p_i$ for each piece length $i \le j$. The best revenue is the longest path from 0 to $n$. With the CLRS prices $p = (1, 5, 8, 9, 10, 17, 17, 20, 24, 30)$, the best revenue for $n = 4$ is 10, from two pieces of length 2. The graph has $n + 1$ vertices and $n(n+1)/2$ edges, so this takes $\Theta(n^2)$ time. See the [rod cutting problem](/rod-cutting-problem/).

### Knapsack and the size of a state

For the [0/1 knapsack](/knapsack-problem/), the remaining capacity alone is not a good state, since it does not say which items are still free. The state $(i, c)$, "the first $i$ items are decided and the capacity $c$ is used", is enough. It has an edge from $(i-1, c)$ (skip item $i$, gain 0) and from $(i-1, c - w_i)$ (take it, gain $v_i$). The graph has $(n+1)(W+1)$ vertices, which is [pseudo-polynomial](/pseudo-polynomial-time/). For the [unbounded knapsack](/unbounded-knapsack/) the capacity alone is enough, because each item stays available.

## Variations

- **Recursive form.** Compute $L[v]$ by a recursive call on each predecessor, with a table of the values already known. This is [memoization](/memoization/). It visits only the states that the goal needs, and it needs no explicit order, but it uses a stack as deep as the longest path.
- **Iterative form.** Lines L4 to L6 are [tabulation](/tabulation/). The order is often a few nested loops: increasing $j$ for subsequences, row by row for a grid.
- **Hypergraphs.** In [matrix-chain multiplication](/matrix-chain-multiplication/) and other [interval](/interval-dp/) problems, the value of a state combines *two* other states, the two halves of a split. The dependencies still form a DAG, and the evaluation order is the same, but the best solution is a tree in a hypergraph, not a path in a graph.
- **Trees as input.** In [tree dynamic programming](/tree-dynamic-programming/), the states are the vertices of a given tree, and a postorder is a topological order of the child-to-parent edges.
- **States as subsets.** In [bitmask dynamic programming](/bitmask-dp/), such as the [Held-Karp algorithm](/held-karp-algorithm/), a state holds a set, and the potential is the size of the set. The number of states is exponential, but much smaller than the number of orders.

## Pitfalls

- **A state that forgets.** If two different situations share a state but have different futures, the values are wrong. The knapsack state without the item index lets an item be taken twice.
- **A hidden cycle.** If some edge does not raise the potential, the graph can have a cycle, and the pass reads a value before it is final. A coin of value 0 gives the edge $x \to x$. An edit model that allows a move back gives a cycle in the grid.
- **Too many states.** The method is fast only when the state space is small. A state that holds a whole set or a whole sequence makes the graph exponential.
- **Reversed edges.** Mixing the "decision" direction and the "depends on" direction gives a loop that reads values that are not yet computed. Write down which direction the edges go, and check the order against line L3.
- **Not a path problem.** If the value of a state depends on two or more other states at once, as in interval problems, a path pass over a graph is not the right model, and a path traceback gives only one branch of the solution.

## Exercises

1. For $a = (3, 1, 4, 1, 5, 9, 2, 6)$, draw the DAG of the increasing-subsequence method and compute $L$ for each position.
2. Model the problem "the number of ways to climb $n$ stairs with steps of 1 or 2" as a path count on a DAG. Give the states, the edges, the potential and the answer for $n = 10$.
   <details><summary>Hint</summary>The states are the stair numbers $0, \ldots, n$, and the count at $n$ is a Fibonacci number.</details>
3. Show that the edit-distance graph has exactly $(m+1)(n+1)$ vertices and $3mn + m + n$ edges.
4. In the coin graph, use the path count in place of the shortest path. Show that it counts the ordered sequences of coins that pay $A$, not the multisets of coins. Compute both numbers for the values $\{1, 3, 4\}$ and $A = 6$, and change the states so that the path count gives the number of multisets.
5. Give the states and the edges of a DAG for the [weighted interval scheduling](/weighted-interval-scheduling/) problem, and state the potential.
6. Prove that a potential $\varphi$ with $\varphi(u) < \varphi(v)$ for each edge exists if and only if the graph has no cycle.

## References
