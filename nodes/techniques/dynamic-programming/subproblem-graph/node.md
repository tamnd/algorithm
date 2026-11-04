---
tag: MJP44N
kind: concept
slug: subproblem-graph
name: Subproblem graph
area: techniques/dynamic-programming
level: core
summary: A directed graph with a vertex for each subproblem and an edge to each subproblem it depends on, used to analyze dynamic programming.
prereqs: [directed-acyclic-graph, overlapping-subproblems, recursion]
see_also: [dp-on-dag, dag-dynamic-programming, memoization, tabulation, rod-cutting-problem, topological-sort, depth-first-search, recursion-tree-method]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.1, the subsection on subproblem graphs (rod cutting), and Section 14.3 (elements of dynamic programming, overlapping subproblems)
  - book: isbn:9780073523408
    title: Dasgupta, Papadimitriou and Vazirani, Algorithms
    locator: Chapter 6, Sections 6.1 and 6.2 (the dag behind a dynamic program)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Section 6.4 (memoization and dynamic programming; the dependency graph, memoized recursion as depth-first search, dynamic programming in dags)
---

The subproblem graph of a dynamic program is a directed graph with one vertex for each distinct subproblem and an edge from a subproblem $x$ to a subproblem $y$ when the computation of $x$ uses the solution of $y$ directly. CLRS Section 14.1 uses it to analyze dynamic programs: the running time is about the number of vertices plus the number of edges, the bottom-up order is a reverse [topological sort](/topological-sort/) of the graph, and the top-down [memoized](/memoization/) recursion is a [depth-first search](/depth-first-search/) of it. The graph is a tool to measure and order a dynamic program. To design one by a path search in a graph of states, see [dynamic programming on DAGs](/dag-dynamic-programming/); to run one on a graph that is the input, see [dynamic programming on directed acyclic graphs](/dp-on-dag/).

## In plain words

A recursive program calls itself on smaller cases. Often it calls the same smaller case many times from different places. Draw each different case one time, as a dot. Draw an arrow from a case to each smaller case that it asks for. This drawing is the subproblem graph.

The drawing tells you three things. The number of dots and arrows tells you how much work a program does if it solves each case only once. Since each arrow points to a smaller case, there are no loops, so you can list the cases from small to large, and that list is the order of a table-filling program. A recursive program that saves its answers walks the drawing like a maze, and it never enters a dot twice.

## The idea

**Definition.** Let a recurrence define a value $V(x)$ for each subproblem $x$ in terms of the values $V(y_1), \ldots, V(y_k)$ of other subproblems. The subproblem graph $G = (S, E)$ has the vertex set $S$, the subproblems reachable from the original problem, and the edge set $E = \{(x, y) : V(x) \text{ uses } V(y)\}$. The base cases are the vertices with no leaving edge.

**The graph is acyclic.** If the recursion stops on each input, then there is no cycle. A cycle $x \to \cdots \to x$ would make the computation of $V(x)$ need $V(x)$ itself, and the plain recursion would not stop. In practice one proves it with a measure, such as a length or an index, that drops along each edge.

**The running time.** Suppose that, apart from the recursive values, solving $x$ takes time proportional to its out-degree $\deg^+(x)$, plus a constant. When each subproblem is solved one time, the total time is
$$ \sum_{x \in S} \Theta\bigl(1 + \deg^+(x)\bigr) = \Theta(|S| + |E|). $$
This is the statement of CLRS Section 14.1: the time is linear in the number of vertices and edges. When the work at $x$ is larger, for example a split point that costs more than a constant, sum the real work of each vertex instead.

**The bottom-up order.** A bottom-up program, also called [tabulation](/tabulation/), must solve $y$ before $x$ for each edge $(x, y)$. So its order is a topological sort of the graph with all edges reversed, which is a reverse topological sort of $G$. CLRS names it this way. A loop "for $j = 0$ to $n$" is such an order when each edge goes from a larger index to a smaller one.

**The top-down order.** A memoized recursion starts at the original problem. At $x$, it calls each $y$ with $(x, y) \in E$, and it returns at once when $y$ is already solved. This is a depth-first search of $G$ from the original problem, and each vertex finishes after all its successors. So the finishing order of the search is the same kind of order as the bottom-up one, a reverse topological order. It visits only the vertices reachable from the start, and its stack depth is the length of the longest path in $G$.

**The naive recursion.** A recursion without a table calls $y$ once for each *path* from the start to $y$. Its recursion tree is the unfolding of $G$ into a tree, and its size is the number of paths from the start. This number is exponential when many vertices have in-degree 2 or more, which is the formal content of [overlapping subproblems](/overlapping-subproblems/).

## Examples

### Rod cutting with n = 4

In [rod cutting](/rod-cutting-problem/), the revenue $r_j$ for a rod of length $j$ is $\max_{1 \le i \le j}(p_i + r_{j-i})$ with $r_0 = 0$. The subproblems are the lengths $0, 1, 2, 3, 4$, and there is an edge $j \to j - i$ for each $i = 1, \ldots, j$, so $j$ has out-degree $j$:

| vertex | 4 | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|
| edges to | 3, 2, 1, 0 | 2, 1, 0 | 1, 0 | 0 | none |

The graph has 5 vertices and $4 + 3 + 2 + 1 = 10$ edges. In general it has $n + 1$ vertices and $n(n+1)/2$ edges, so the bottom-up and the memoized program take $\Theta(n^2)$ time. The bottom-up program solves $0, 1, 2, 3, 4$ in this order, which is a reverse topological order.

The naive recursion makes one call for each path from $n$. The number of paths from $n$ to $j < n$ is $2^{n-j-1}$, because such a path is a choice of which of the $n - j - 1$ lengths strictly between $j$ and $n$ it visits. With the one empty path at $n$, the total is $1 + \sum_{j=0}^{n-1} 2^{n-j-1} = 2^n$. For $n = 4$ the naive recursion makes 16 calls, and for $n = 10$ it makes 1024, against 11 vertices and 55 edges.

### Fibonacci numbers

For $F_n = F_{n-1} + F_{n-2}$, the graph has the vertices $0, \ldots, n$, and each vertex $j \ge 2$ has two edges, to $j - 1$ and $j - 2$. It has $n + 1$ vertices and $2(n - 1)$ edges, so the table method takes $\Theta(n)$ additions. The naive recursion makes $C(n) = 1 + C(n-1) + C(n-2)$ calls with $C(0) = C(1) = 1$, and induction gives $C(n) = 2F_{n+1} - 1$. For $n = 20$ that is 21891 calls for 21 distinct subproblems. See [Fibonacci numbers](/fibonacci-numbers/).

### Longest common subsequence

For the [longest common subsequence](/longest-common-subsequence/) of strings of lengths $m$ and $n$, the vertices are the prefix pairs $(i, j)$, $(m+1)(n+1)$ in all. A vertex with $x_i = y_j$ has one edge, to $(i-1, j-1)$, and the other inner vertices have two, to $(i-1, j)$ and $(i, j-1)$. So $|E| \le 2mn$ and the time is $\Theta(mn)$.

### Matrix-chain multiplication

For [matrix-chain multiplication](/matrix-chain-multiplication/) of $n$ matrices, the vertices are the ranges $(i, j)$ with $1 \le i \le j \le n$, $n(n+1)/2$ in all. The range $(i, j)$ with $j > i$ has $j - i$ split points and two edges for each, so
$$ |E| = \sum_{\ell = 1}^{n-1} (n - \ell) \cdot 2\ell = \frac{n^3 - n}{3}, $$
which is 70 for $n = 6$. The time is $\Theta(n^3)$. Here each vertex combines two successors at a time, so the graph is really a hypergraph, but the count of the work is the same.

### A sparse graph

For the [0/1 knapsack](/knapsack-problem/) with the state (items left, capacity left), the full table has $(n+1)(W+1)$ cells. The subproblem graph contains only the states that the start can reach. With $n$ items and a huge capacity $W$, at most $2^i$ states are reachable at depth $i$, so the memoized program can do much less work than the table when $W$ is much larger than $2^n$. The graph, not the table, measures the work of the top-down method.

## Where it is used

- **Running time of a dynamic program.** Count the vertices and the work at each vertex. This is the standard way to get $\Theta(n^2)$ for rod cutting, $\Theta(mn)$ for edit distance and $\Theta(n^3)$ for matrix chains.
- **Choosing the loop order.** A bottom-up program needs a reverse topological order. When the graph is a grid or a triangle of ranges, the order is a pair of nested loops, and the graph shows which direction each loop must run.
- **Space reduction.** When every edge from row $i$ goes to rows $i - 1$ to $i - k$, only $k + 1$ rows are needed at one time. This is [rolling-array space reduction](/rolling-array-space-reduction/).
- **Explaining overlapping subproblems.** The gap between the number of paths and the number of vertices is the gap between the naive recursion and dynamic programming.
- **Parallel evaluation.** The vertices at the same distance from the base cases can be computed at the same time. The longest path of the graph bounds the number of parallel rounds, as for a [computation DAG](/computation-dag/).
- **Shortest and longest paths.** When the value at a vertex is the best over its edges of a successor value plus an edge cost, the dynamic program *is* a path computation in the subproblem graph. See [dynamic programming on DAGs](/dag-dynamic-programming/).

## References
