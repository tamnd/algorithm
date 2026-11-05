---
tag: WDGRCA
kind: concept
slug: sorting-barrier
name: Sorting barrier for SSSP
aliases:
- Dijkstra sorting barrier
area: graphs/shortest-paths
level: advanced
summary: The long-standing bound that comparison-based Dijkstra-style methods need roughly sorting time, which later work beat for directed graphs.
prereqs: [dijkstra, single-source-shortest-paths, comparison-sort-lower-bound, fibonacci-heap]
see_also: [breaking-sorting-barrier-sssp, thorup-undirected-sssp, dijkstra, comparison-sort-lower-bound, fibonacci-heap, integer-sorting, comparison-model, dag-shortest-paths]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.3, Dijkstra's algorithm (the O(V lg V + E) bound with Fibonacci heaps) and Section 8.1, Lower bounds for sorting
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 596 to 615 (1987)
    locator: the O(m + n log n) bound for Dijkstra and the remark that it is optimal for algorithms that visit vertices in order of distance
  - paper: doi:10.1145/316542.316548
    title: Mikkel Thorup, Undirected single-source shortest paths with positive integer weights in linear time, Journal of the ACM 46(3), 362 to 394 (1999)
    locator: the introduction (the sorting bottleneck of Dijkstra) and the component hierarchy that avoids it
  - paper: "Seth Pettie and Vijaya Ramachandran, A shortest path algorithm for real-weighted undirected graphs, SIAM Journal on Computing 34(6), 1398 to 1431 (2005)"
    locator: the comparison-addition model and the undirected bound below sorting time
  - paper: "Mikkel Thorup, Equivalence between priority queues and sorting, Journal of the ACM 54(6), article 28 (2007)"
    locator: the reduction from priority queues to sorting and its use for Dijkstra with integer weights
  - paper: "Bernhard Haeupler, Richard Hladik, Vaclav Rozhon, Robert E. Tarjan and Jakub Tetek, Universal optimality of Dijkstra via beyond-worst-case heaps, Proceedings of the 65th IEEE Symposium on Foundations of Computer Science (FOCS), 2024"
    locator: the problem of ordering the vertices by distance and the universal optimality of Dijkstra for it
  - url: https://arxiv.org/abs/2504.17033
    title: Ran Duan, Jiayi Mao, Xiao Mao, Xinkai Shu and Longhui Yin, Breaking the sorting barrier for directed single-source shortest paths (STOC 2025)
    locator: the introduction (the sorting barrier) and the main theorem, O(m log^(2/3) n) time in the comparison-addition model
---

Dijkstra's algorithm finds the vertices in nondecreasing order of distance from the source, so it sorts the distances as a side effect. The *sorting barrier* is the bound this places on it: in the comparison model, any algorithm that outputs the vertices in that order needs $\Omega(n \log n)$ comparisons, so Dijkstra with a [Fibonacci heap](/fibonacci-heap/), $O(m + n \log n)$, is optimal among such algorithms. But the [single-source shortest paths](/single-source-shortest-paths/) problem asks only for the distances, not for their order. Thorup (1999) beat the barrier for undirected graphs with integer weights, Pettie and Ramachandran for undirected graphs with real weights, and Duan, Mao, Mao, Shu and Yin (2025) for directed graphs with real weights, in $O(m \log^{2/3} n)$ time.

## In plain words

Dijkstra's method finds the closest place first, then the next closest, and so on. So at the end it has put all places in order of distance. Putting $n$ numbers in order by comparing them takes about $n \log n$ steps, so Dijkstra cannot be faster than that.

But the question was only "how far is each place?", not "which place is closer than which?". A method that does not finish places one by one in order is not held back by the cost of sorting. For many years no such method was known for general one-way maps. One was found in 2025.

## The idea

**The models.** The barrier is a statement about the *comparison-addition model*: weights are real numbers, and an algorithm may only add them and compare sums. In the [word RAM](/word-ram/) with integer weights, other operations are allowed, and the bounds differ.

**Weight assumptions.** The barrier concerns nonnegative real weights, the setting of Dijkstra. Integer weights are the setting of the word-RAM results. With negative weights the best algorithms are much slower than sorting time anyway, and a [negative cycle](/negative-cycle/) makes the distances undefined, so the barrier plays no role there. Unreachable vertices have distance $+\infty$ and need no place in the order.

**Why Dijkstra sorts.** Take numbers $x_1, \ldots, x_n \ge 0$ and build the star with arcs $s \to v_i$ of weight $x_i$. Dijkstra extracts $v_i$ in nondecreasing order of $x_i$, so it sorts. Sorting needs $\Omega(n \log n)$ comparisons in the worst case (see the [comparison sort lower bound](/comparison-sort-lower-bound/)), so every algorithm that visits the vertices in order of distance needs $\Omega(m + n \log n)$ time, counting $\Omega(m)$ to read the input. Fibonacci heaps reach this bound.

**Why this is not a lower bound for the problem.** On the star, the distances are just the weights $x_i$; an algorithm can output them in $O(n)$ time without comparing any two. The order is extra information. So the $\Omega(n \log n)$ argument says nothing about algorithms that compute distances in some other order. For the problem itself, the only known lower bound is the trivial $\Omega(m + n)$.

**How the barrier was broken.**

- *Undirected graphs, integer weights.* Thorup's [algorithm](/thorup-undirected-sssp/) builds a component hierarchy from a minimum spanning tree and visits vertices in an order that is only roughly sorted by distance, using buckets. It takes $O(m)$ time on the word RAM.
- *Undirected graphs, real weights.* Pettie and Ramachandran extend the hierarchy approach to the comparison-addition model, with $O(m \alpha(m, n) + \min(n \log n, n \log \log r))$ time, where $r$ is the ratio of the largest to the smallest weight.
- *Directed graphs, real weights.* Duan, Mao, Mao, Shu and Yin combine Dijkstra with Bellman-Ford. They work on a frontier of vertices with uncertain distances, run a few Bellman-Ford steps to find a small set of *pivots* whose shortest-path subtrees are large, and recurse on distance ranges, so that only about $n / \log^{\Omega(1)} n$ vertices ever pass through a priority queue. The result is $O(m \log^{2/3} n)$ deterministic time, below $O(m + n \log n)$ when $m = o(n \log^{1/3} n)$. This is the [breaking the sorting barrier](/breaking-sorting-barrier-sssp/) algorithm.

**Integer weights.** On the word RAM, integers can be sorted in $o(n \log n)$ time, so the barrier is lower. Thorup showed that priority queues are as fast as [integer sorting](/integer-sorting/), which gives Dijkstra in $O(m + n \log \log n)$ time for directed graphs with integer weights. Whether directed integer SSSP can be solved in $O(m)$ time is open.

**Dijkstra is still optimal for its own task.** If the output must be the vertices in order of distance, Haeupler, Hladik, Rozhon, Tarjan and Tetek show that Dijkstra with a suitable heap is *universally optimal*: on every fixed graph, its time is within a constant factor of the best possible for the worst weights on that graph.

## Examples

**The star sorts.** Take arcs $s \to a$ (3), $s \to b$ (1) and $s \to c$ (2). Dijkstra extracts $s, b, c, a$, that is the order $1, 2, 3$ of the weights. The distances $\delta(s, a) = 3$, $\delta(s, b) = 1$ and $\delta(s, c) = 2$ are read off the arcs with no comparison at all.

**A graph where order is free.** In a DAG, [DAG shortest paths](/dag-shortest-paths/) relaxes arcs in topological order and takes $O(n + m)$ time with any real weights, negative ones included. It never sorts the distances, which shows again that sorting is not part of the problem.

**BFS.** With all weights equal to 1, breadth-first search computes distances in $O(n + m)$ time. Its queue is sorted by distance, but the keys take only $n$ different values in order, so no comparison sorting is needed. Buckets, as in [Dial's algorithm](/dial-algorithm/), extend this to small integer weights.

**An unreachable vertex and a negative cycle.** Add a vertex $d$ with no incoming arc to the star: its distance is $+\infty$ and it is never extracted. Add arcs $a \to e$ (1) and $e \to a$ ($-2$): the cycle has weight $-1$, Dijkstra's answer is wrong, and the question of sorting time does not arise because no algorithm in this setting applies.

## Where it is used

- **As the target of new algorithms.** The bound $O(m + n \log n)$ was the best for directed SSSP with real weights from 1984 to 2025, and the 2025 result is stated as breaking it.
- **As a lower bound for ordered output.** Problems that need vertices in order of distance, such as listing the $k$ nearest vertices in order, inherit the $\Omega(n \log n)$ bound.
- **In the design of priority queues.** The equivalence of priority queues and sorting, and the bucket queues and [radix heaps](/radix-heap/) for integer weights, come from the wish to make Dijkstra run in sorting time or less.
- **In route planning.** Fast practical methods such as [contraction hierarchies](/contraction-hierarchies/) and [hub labeling](/hub-labeling/) avoid the barrier in another way: they preprocess the graph so that each query explores only a small part of it.

## References
