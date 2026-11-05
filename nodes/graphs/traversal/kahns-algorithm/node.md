---
tag: JVCQ4E
kind: algorithm
slug: kahns-algorithm
name: Kahn's algorithm
aliases:
- Kahn's topological sort
- topological sort by in-degree
area: graphs/traversal
level: intro
summary: Repeatedly removes vertices of in-degree zero; vertices left over reveal a cycle.
solves: [topological-ordering, cycle-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [topological-ordering, queue, in-degree-and-out-degree]
see_also: [topological-sort, topological-ordering-theorem, directed-acyclic-graph, priority-queue, dag-shortest-paths, critical-path, incremental-topological-ordering, cycle-detection]
sources:
  - paper: doi:10.1145/368996.369025
    title: Arthur B. Kahn, Topological sorting of large networks, Communications of the ACM 5(11), 558 to 562 (1962)
    locator: the whole paper
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.3, Linked allocation (Algorithm T, topological sort, with a count of predecessors and a list of successors for each object)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 3.6, Directed acyclic graphs and topological ordering (the algorithm that deletes a node with no incoming edges, and its O(m + n) implementation)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.4, Topological sort (the exercise on topological sort by repeatedly removing vertices of in-degree 0)
---

Kahn's algorithm finds a [topological ordering](/topological-ordering/) of a [directed graph](/directed-graph/) by removing, again and again, a vertex that no remaining edge enters. It keeps the current [in-degree](/in-degree-and-out-degree/) of each vertex and a [queue](/queue/) of the vertices whose in-degree is zero. Each vertex taken from the queue goes to the output, and the in-degrees of its successors go down by one. If all vertices are output, the output is a topological ordering. If some are left, they all lie on or behind a directed cycle, so the graph has no topological ordering. The algorithm runs in $\Theta(n + m)$ time, uses no recursion, and produces the ordering from the front.

## In plain words

You have jobs with rules "this job before that job". Count, for each job, how many rules say that some other job must come before it.

A job with count zero can be done now. Do it, and cross out its rules. Each job that was waiting for it now has one less job to wait for. When the count of a job drops to zero, it is ready too.

Keep doing ready jobs until there are none. If all jobs are done, the order in which you did them keeps every rule. If some jobs are never ready, they wait for each other in a loop, and no valid order exists.

## The problem

Given a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges in [adjacency lists](/adjacency-list/), return a list of all vertices in which each edge $(u, v)$ has $u$ before $v$, or report that $G$ has a directed cycle.

## The algorithm

The array $\mathrm{in}[v]$ holds the number of edges into $v$ from vertices that are not yet output. The queue $Q$ holds the vertices with $\mathrm{in}[v] = 0$ that are not yet output.

```pseudo id=main
KAHN(G)
L1  for each vertex u ∈ V do in[u] ← 0
L2  for each vertex u ∈ V do for each v ∈ Adj[u] do in[v] ← in[v] + 1
L3  Q ← empty queue, L ← empty list
L4  for each vertex u ∈ V do if in[u] = 0 then ENQUEUE(Q, u)
L5  while Q is not empty do
L6      u ← DEQUEUE(Q), append u to L
L7      for each v ∈ Adj[u] do
L8          in[v] ← in[v] − 1
L9          if in[v] = 0 then ENQUEUE(Q, v)
L10 if |L| < |V| then report "G has a cycle"
L11 return L
```

Lines L1 and L2 compute the in-degrees. Lines L5 to L9 output a vertex of in-degree zero and remove its outgoing edges. The queue can be replaced by a [stack](/stack/), a set or any other container: the proof uses only that each vertex put in it is taken out later. The choice changes which of the topological orderings comes out.

A parallel edge $(u, v)$ that appears twice in $\mathrm{Adj}[u]$ adds 2 to $\mathrm{in}[v]$ and is removed twice, so multigraphs need no special case. A self-loop $(u, u)$ keeps $\mathrm{in}[u] \ge 1$ until $u$ is output, so $u$ is never output, as it should be.

## Example

Take the acyclic graph with vertices 0 to 6 and these lists.

| $u$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $\mathrm{Adj}[u]$ | 1, 3, 2 | 2 | none | 2, 4 | none | 4, 6 | none |
| $\mathrm{in}[u]$ after line L2 | 0 | 1 | 3 | 1 | 2 | 0 | 1 |

Line L4 puts 0 and 5 in the queue.

| step | dequeue | changes of $\mathrm{in}$ | enqueued | $Q$ after the step | $L$ after the step |
|---|---|---|---|---|---|
| 1 | 0 | $\mathrm{in}[1] = 0$, $\mathrm{in}[3] = 0$, $\mathrm{in}[2] = 2$ | 1, 3 | 5, 1, 3 | 0 |
| 2 | 5 | $\mathrm{in}[4] = 1$, $\mathrm{in}[6] = 0$ | 6 | 1, 3, 6 | 0, 5 |
| 3 | 1 | $\mathrm{in}[2] = 1$ | none | 3, 6 | 0, 5, 1 |
| 4 | 3 | $\mathrm{in}[2] = 0$, $\mathrm{in}[4] = 0$ | 2, 4 | 6, 2, 4 | 0, 5, 1, 3 |
| 5 | 6 | none | none | 2, 4 | 0, 5, 1, 3, 6 |
| 6 | 2 | none | none | 4 | 0, 5, 1, 3, 6, 2 |
| 7 | 4 | none | none | empty | 0, 5, 1, 3, 6, 2, 4 |

All 7 vertices are output, so $0, 5, 1, 3, 6, 2, 4$ is a topological ordering. The [DFS topological sort](/topological-sort/) on the same lists gives $5, 6, 0, 3, 4, 1, 2$, another valid ordering.

**With a cycle.** Add the edge $2 \to 0$. Now $\mathrm{in}[0] = 1$, and only 5 starts in the queue. Step 1 outputs 5 and enqueues 6, step 2 outputs 6, and the queue is empty. Line L10 finds $|L| = 2 < 7$ and reports a cycle. The vertices $0, 1, 2, 3, 4$ remain, each with $\mathrm{in}[v] \ge 1$. Walking backwards along edges inside this set from 4 gives $4, 3, 0, 2, 1, 0$, which repeats 0 and shows the cycle $0, 1, 2$.

## Correctness

The invariant is that $\mathrm{in}[v]$ is the number of edges into $v$ from vertices not in $L$. So a vertex enters the queue only when all its predecessors are in $L$, and then it comes after them in $L$. If all vertices are output, every edge goes forward. If a vertex is never output, its in-degree stays positive, so it has a predecessor that is also never output; following predecessors among these vertices must repeat one, which gives a cycle. Conversely, no vertex of a cycle is ever output, because the first one would need its predecessor on the cycle to be output before it. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model.

- **Lines L1 and L2.** $\Theta(n)$ for the array and $\Theta(n + m)$ for the scan of all lists.
- **Line L4.** $\Theta(n)$.
- **Lines L5 to L9.** Each vertex is enqueued at most one time, since $\mathrm{in}[v]$ only decreases and is tested for zero right after each decrease, and the vertices with $\mathrm{in}[v] = 0$ at line L4 have no incoming edge and are never decreased. So the loop runs at most $n$ times, and the inner loop scans each list at most one time, which is $O(m)$ in total, with $O(1)$ per queue operation.

So the time is $\Theta(n + m)$ on every input, because line L2 always reads all lists. The extra space is $\Theta(n)$ for the counts, the queue and the output.

## Properties

- **Deterministic.** With a FIFO queue and the order $0, 1, \ldots, n - 1$ in line L4, the output is fixed. Another container or order can give another valid ordering.
- **Not recursive.** No call stack, so no overflow on long paths.
- **Online output.** The output is produced from the front, one vertex at a time. A consumer can start on the first vertices before the algorithm ends.
- **Layers.** If the vertices are taken in rounds, where round $r$ takes all vertices that have in-degree zero after round $r - 1$, then the round of a vertex is the number of vertices on a longest path that ends at it. The number of rounds is the number of vertices on a longest path of $G$.

## Variants and improvements

- **Lexicographically smallest ordering.** Use a min-[priority queue](/priority-queue/) in place of the queue. Each step takes the smallest vertex that can come next, which gives the lexicographically smallest topological ordering in $O(m + n \log n)$ time with a [binary heap](/binary-heap/).
- **Return the cycle.** If vertices remain, start at one of them and step to any predecessor that also remains. Within $n + 1$ steps a vertex repeats, and the steps between the two visits, read backwards, form a cycle. This needs the lists of predecessors, which one pass over the edges builds.
- **Algorithm T.** Knuth's version keeps, for each object, a count of predecessors and a linked list of successors, and it links the queue through the count fields that have become zero, so it needs no separate queue array.
- **Parallel rounds.** Process all vertices of in-degree zero together in each round. The number of rounds is the number of vertices on a longest path, so the method is fast in parallel when the longest path is short.
- **Scheduling.** With durations on the vertices, the same order computes the earliest start times of a project, the [critical path](/critical-path/) method.

## When to use it

Use Kahn's algorithm when recursion is unwanted, when the output should be produced from the front, when the next vertex should be chosen by a rule (smallest number, highest priority, earliest deadline), or when the edges are already given as in-degree counts and successor lists, as in build systems and task schedulers. Use the [DFS topological sort](/topological-sort/) when the graph is given only as a successor function, so that the in-degrees are not known in advance, or when a DFS runs anyway.

## Pitfalls

- **No final check.** Without line L10, a graph with a cycle gives a short list without a warning. Compare the length of the output with $n$.
- **Wrong initial queue.** All vertices of in-degree zero must enter the queue at line L4, including isolated vertices. Starting from one source only can miss vertices.
- **Counting edges without multiplicity.** If parallel edges are counted once in line L2 but decreased twice in line L8, a count goes negative or reaches zero too early. Count and decrease in the same way.
- **Enqueue on a nonzero test.** Line L9 must test for zero right after the decrease. Testing $\mathrm{in}[v] \le 0$ or testing before the decrease can enqueue a vertex twice or too early.

## Implementations

## History

Arthur Kahn published the method in 1962, in a paper on the topological sorting of large networks. Knuth gives it as Algorithm T in the first volume of The Art of Computer Programming, as an example of linked allocation with a count of predecessors for each object. Kleinberg and Tardos present it as the proof that every directed acyclic graph has a topological ordering, followed by its $O(m + n)$ implementation.

## References
