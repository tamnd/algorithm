---
tag: 00XN3N
kind: problem
slug: assembly-line-scheduling
name: Assembly-line scheduling
aliases:
- two-line assembly scheduling
area: techniques/dynamic-programming
level: intro
summary: Choose which station line to use at each stage to minimise the total time through a factory.
prereqs: [optimal-substructure, dag-shortest-paths]
see_also: [dp-on-dag, dag-dynamic-programming, viterbi-algorithm, trellis, traceback, rolling-array-space-reduction, principle-of-optimality, subproblem-graph]
sources:
  - book: isbn:9780262032933
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, second edition
    locator: Section 15.1 (assembly-line scheduling), Figures 15.1 and 15.2
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 14 (dynamic programming) and Section 22.2 (single-source shortest paths in directed acyclic graphs)
  - book: isbn:9780073523408
    title: Dasgupta, Papadimitriou and Vazirani, Algorithms
    locator: Section 6.1 (shortest paths in dags, revisited)
---

Assembly-line scheduling is the problem of routing one product through a factory with two parallel lines of $n$ stations each, choosing at each stage the line whose station to use, so that the total of assembly times and transfer times is least. It has $2^n$ routes, but the least time to reach each station depends only on the least times to reach the two stations of the stage before, so a dynamic program finds the best route in $\Theta(n)$ time. The problem is a [shortest path in a DAG](/dag-shortest-paths/) with two vertices per stage. It opened the dynamic programming chapter of the second edition of CLRS and was dropped from later editions.

## In plain words

A car goes through a factory with two lines. Each line does the same work in the same order, stage by stage, but the stations of the two lines are not equally fast. At each stage the car can stay on its line for free, or cross to the other line, which takes some time. Getting onto a line and leaving it also take time.

You want the fastest way through. Trying all routes doubles the work with each stage. But the fastest way to reach a given station passes through the fastest way to reach one of the two stations just before it. So you work stage by stage and keep only two numbers: the best time to finish the current stage on line one, and on line two. At the end you take the better one and follow the stored choices back.

## Definition

**Input.** For lines $i \in \{1, 2\}$ and stations $j \in \{1, \ldots, n\}$, with all values non-negative:

- $a_{i,j}$, the time at station $S_{i,j}$, the $j$-th station of line $i$;
- $e_i$, the time to enter line $i$, and $x_i$, the time to leave it after $S_{i,n}$;
- $t_{i,j}$ for $1 \le j \le n - 1$, the time to transfer from line $i$ after station $S_{i,j}$ to the other line. Staying on the same line costs nothing.

**Routes.** A route is a sequence $(\ell_1, \ldots, \ell_n) \in \{1, 2\}^n$: at stage $j$ the product uses station $S_{\ell_j, j}$. Its time is
$$T(\ell) = e_{\ell_1} + \sum_{j=1}^{n} a_{\ell_j, j} + \sum_{\substack{1 \le j < n \\ \ell_{j+1} \ne \ell_j}} t_{\ell_j, j} + x_{\ell_n}.$$

**Output.** The least time $f^* = \min_\ell T(\ell)$ and a route that achieves it.

**The recurrence.** Let $f_i[j]$ be the least time from the start through station $S_{i,j}$, and write $\bar\imath$ for the other line. Then
$$f_i[1] = e_i + a_{i,1}, \qquad f_i[j] = \min\bigl( f_i[j-1] + a_{i,j},\; f_{\bar\imath}[j-1] + t_{\bar\imath, j-1} + a_{i,j} \bigr) \text{ for } 2 \le j \le n,$$
and $f^* = \min\bigl(f_1[n] + x_1,\, f_2[n] + x_2\bigr)$.

*Proof.* A route that reaches $S_{i,j}$ with $j \ge 2$ came from $S_{i,j-1}$ or from $S_{\bar\imath, j-1}$. Its time up to $S_{i,j}$ is the time of its prefix up to that station, plus $a_{i,j}$, plus $t_{\bar\imath, j-1}$ in the second case. The prefix costs at least $f_i[j-1]$ or $f_{\bar\imath}[j-1]$, so $f_i[j]$ is at least the minimum. For each of the two cases, a fastest prefix followed by the move to $S_{i,j}$ is a valid route with exactly that time, so $f_i[j]$ is at most the minimum. The case $j = 1$ and the exit are the same argument with one predecessor. ∎

The choice $l_i[j] \in \{1, 2\}$, the line of the predecessor that achieves $f_i[j]$, is stored for the [traceback](/traceback/).

## Variants

- **More lines.** With $k$ lines and a transfer time $t_{i,i',j}$ for each pair, the recurrence takes a minimum over $k$ predecessors: $\Theta(k^2 n)$ time.
- **Time-dependent transfer costs.** Any transfer time that depends only on the two stations it joins fits the same recurrence.
- **Maximum or other semirings.** Replace min and $+$ by max and $+$ for the most profitable route, or by sum and product to count routes or add probabilities, as in the forward algorithm of [hidden Markov models](/hidden-markov-model/).
- **Value only.** If only $f^*$ is needed, keep two numbers per stage and drop the table, as in [rolling-array space reduction](/rolling-array-space-reduction/).

## Examples

**The CLRS instance.** Six stations, with $e = (2, 4)$, $x = (3, 2)$,

| | $j=1$ | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $a_{1,j}$ | 7 | 9 | 3 | 4 | 8 | 4 |
| $a_{2,j}$ | 8 | 5 | 6 | 4 | 5 | 7 |
| $t_{1,j}$ | 2 | 3 | 1 | 3 | 4 | |
| $t_{2,j}$ | 2 | 1 | 2 | 2 | 1 | |

The DP gives

| | $j=1$ | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $f_1[j]$ | 9 | 18 | 20 | 24 | 32 | 35 |
| $f_2[j]$ | 12 | 16 | 22 | 25 | 30 | 37 |
| $l_1[j]$ | | 1 | 2 | 1 | 1 | 2 |
| $l_2[j]$ | | 1 | 2 | 1 | 2 | 2 |

For example, $f_2[2] = \min(12 + 5,\ 9 + 2 + 5) = 16$, through line 1. At the exit, $f^* = \min(35 + 3,\ 37 + 2) = 38$ on line 1. Following the stored lines back from $S_{1,6}$ gives the route $(1, 2, 1, 2, 2, 1)$:
$2 + 7 + 2 + 5 + 1 + 3 + 1 + 4 + 5 + 1 + 4 + 3 = 38$.
Staying on line 1 the whole time costs 40, and staying on line 2 costs 41. A search over all $2^6 = 64$ routes gives the same optimum, 38.

## Known algorithms

- **Brute force.** Evaluate all $2^n$ routes: $\Theta(n 2^n)$ time.
- **The DP (CLRS 2nd edition, FASTEST-WAY).** Compute $f_1[j]$ and $f_2[j]$ for $j = 1, \ldots, n$, then trace back. $\Theta(n)$ time, $\Theta(n)$ space for the choices, and $O(1)$ space for the value alone.
- **Generic DAG shortest paths.** Run [DAG shortest paths](/dag-shortest-paths/) on the graph below. The time is $\Theta(V + E) = \Theta(n)$, the same as the special-purpose DP; the DP is this algorithm with the topological order written in.

## Bounds

- **Upper bound.** $\Theta(n)$ time for $k = 2$ lines, and $O(k^2 n)$ for $k$ lines with pairwise transfers.
- **Lower bound.** $\Omega(n)$: every $a_{i,j}$ can change the answer, so an algorithm must read the whole input. So the DP is optimal up to a constant factor.

## Reductions

- **To shortest path in a DAG.** Make a source $s$, a sink $z$ and a vertex for each station. Give each vertex $S_{i,j}$ the weight $a_{i,j}$, or move it onto the edges that enter it. Add the edges $s \to S_{i,1}$ of weight $e_i + a_{i,1}$, the edges $S_{i,j-1} \to S_{i,j}$ of weight $a_{i,j}$, the edges $S_{\bar\imath,j-1} \to S_{i,j}$ of weight $t_{\bar\imath,j-1} + a_{i,j}$, and the edges $S_{i,n} \to z$ of weight $x_i$. The graph has $2n + 2$ vertices and $4n$ edges, and every edge goes from a stage to the next one, so it is acyclic and the stage order is a topological order. Routes are exactly the paths from $s$ to $z$, with the same cost. This is the general pattern of [DP on a DAG](/dp-on-dag/): the subproblems are vertices and the recurrence relaxes the edges in topological order.
- **To a trellis.** The graph is a [trellis](/trellis/) with two states per stage. The [Viterbi algorithm](/viterbi-algorithm/) solves the same min-sum problem on a trellis with many states.

## Applications

- **Multi-stage choices with a switching cost.** Picking one of a few modes, machines or servers at each step of a fixed sequence of jobs, when changing mode costs time, has this exact form.
- **Decoding.** Finding the most likely state sequence of a two-state hidden Markov model is the same problem with log-probabilities as weights.
- **Teaching.** CLRS used it, in the second edition, as the first example of the four steps of dynamic programming: describe an optimal solution, write the recurrence, compute the values, and build a solution from the stored choices. It also shows the [principle of optimality](/principle-of-optimality/) on a problem where the subproblem graph is easy to draw.

## References
