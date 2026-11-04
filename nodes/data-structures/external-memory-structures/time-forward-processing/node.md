---
tag: 2A0G6A
kind: technique
slug: time-forward-processing
name: Time-forward processing
aliases:
- time-forward processing with an external priority queue
area: data-structures/external-memory-structures
level: advanced
summary: Evaluates DAG-structured computations in external memory by sending values forward in time through a priority queue.
prereqs: [external-memory-priority-queue, directed-acyclic-graph, topological-sort]
see_also: [buffer-tree, maximal-independent-set, dag-shortest-paths, list-ranking, euler-tour-technique, boolean-circuit, graph-coloring, external-merge-sort]
sources:
  - paper: "Yi-Jen Chiang, Michael T. Goodrich, Edward F. Grove, Roberto Tamassia, Darren E. Vengroff and Jeffrey Scott Vitter, External-memory graph algorithms, Proceedings of the 6th ACM-SIAM Symposium on Discrete Algorithms (1995)"
    locator: pp. 139 to 149, the section on time-forward processing and its uses for circuit evaluation, list ranking and independent sets
  - paper: "Lars Arge, The buffer tree: a technique for designing batched external data structures, Algorithmica 37(1) (2003)"
    locator: pp. 1 to 24, the external priority queue and its use for time-forward processing
  - book: isbn:9781601981066
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4) (2008)
    locator: Chapter 9 (external graph algorithms, time-forward processing) and Section 11.4 (the priority queue)
---

Time-forward processing is a way to evaluate a computation on a [directed acyclic graph](/directed-acyclic-graph/) in the [external memory model](/external-memory-model/) when the graph is far larger than memory. Each vertex computes a value from the values of its in-neighbors. The vertices are visited in [topological order](/topological-sort/), which is treated as time. When a vertex has its value, it does not write it to the in-neighbor lists of its successors, which are scattered over the disk, but sends it *forward in time*: it inserts a message into an [external memory priority queue](/external-memory-priority-queue/), with the time of the receiving vertex as the priority. When the receiver comes up, its messages are at the front of the queue. With $V$ vertices and $E$ edges this costs $O(\mathrm{Sort}(V + E))$ I/Os, which is $O\big(\frac{V+E}{B}\log_{M/B}\frac{V+E}{B}\big)$, instead of up to one I/O per edge. Chiang and others named the technique in 1995, and Arge's priority queue made it work for all values of the parameters.

## In plain words

Think of a long line of workers, each with a number. Each worker needs notes from some earlier workers and passes notes to some later workers. If each note were carried by hand to its receiver, someone would run up and down the line all day.

Instead, there is one shared mailbox that always gives out the note with the smallest receiver number first. Each worker posts their notes in it and walks on. When worker 57 comes up, all notes for worker 57 are at the front. They take them, do the work, and post new notes for later workers. The mailbox does all the sorting of notes in big batches, which is cheap on disk.

## When it applies

- The computation is on a DAG, and the value of each vertex depends only on its label and on values sent along its in-edges.
- A topological order of the vertices is known, and the vertices are stored in that order, each with its label and its out-edges. If the order is known but the data is not stored that way, one [sort](/external-merge-sort/) puts it in place.
- Each message has $O(1)$ words, or its total size is counted in the bound.
- The order is a real topological order: every edge goes from an earlier vertex to a later one.

Finding the topological order itself is often the hard part. Depth-first search is not known to be I/O-efficient on general graphs, so time-forward processing is used where the order comes from the problem: the order of vertex numbers, the order of a sweep line, the order of time in a simulation, or the levels of a circuit.

## The template

The holes are the label of each vertex, the function `f` that combines the received values, and the message sent on each out-edge. The vertices are numbered $1, \ldots, V$ in topological order.

```pseudo id=main
TIME-FORWARD(G)                         ▷ G: vertices 1..V in topological order, each with its label and out-edges
L1  Q ← an empty external memory priority queue
L2  for v ← 1 to V do                    ▷ a scan of the vertex file
L3      I ← empty list
L4      while Q is not empty and the minimum priority in Q equals v do
L5          (v, x) ← DELETE-MIN(Q); append x to I
L6      value(v) ← f(label(v), I)       ▷ hole: the local computation
L7      for each out-edge (v, w) do       ▷ stored next to v in the file
L8          INSERT(Q, (w, message(v, w))) with priority w
L9      write value(v) to the output file
```

**Why it is correct.** By induction on $v$: when the loop reaches $v$, every in-neighbor $u$ of $v$ has $u < v$, so it was handled earlier and has inserted its message for $v$. No message for $v$ has been removed before, because line L4 only removes messages with priority equal to the current vertex, and every earlier vertex is smaller than $v$. Every message still in $Q$ has priority at least $v$, since each one was sent to a later vertex. So the messages for $v$ are exactly the ones with the minimum priority $v$, and lines L4 and L5 get all of them. Line L6 then computes the value of $v$ from the right inputs.

**Cost.** The scan of the vertex file and its out-edges costs $O((V+E)/B)$ I/Os. There are $E$ inserts and $E$ delete-mins, plus one `find-min` per vertex for the test of line L4. With the priority queue of [Arge](/buffer-tree/), each costs $O\big(\frac{1}{B}\log_{M/B}\frac{E}{B}\big)$ amortized, so the total is $O(\mathrm{Sort}(V+E))$. The memory holds only $O(1)$ values at a time besides the queue. On graphs from list and tree problems, $E = O(V)$, and the cost is $O(\mathrm{Sort}(V))$, which is optimal for many of them by the [permuting](/permuting-problem/) lower bound.

## Classic examples

**Evaluating a circuit.** Take a Boolean circuit, a DAG whose sources are inputs and whose other vertices are gates; see [Boolean circuit](/boolean-circuit/). The vertices are numbered by levels: 1 is the input 1, 2 is the input 0, 3 is the input 1, then $4 = \text{AND}(1, 2)$, $5 = \text{OR}(2, 3)$ and $6 = \text{OR}(4, 5)$. The run:

| $v$ | messages taken | value | messages sent | queue after |
|---|---|---|---|---|
| 1 | none | 1 | $(4, 1)$ | $(4,1)$ |
| 2 | none | 0 | $(4, 0), (5, 0)$ | $(4,1), (4,0), (5,0)$ |
| 3 | none | 1 | $(5, 1)$ | $(4,1), (4,0), (5,0), (5,1)$ |
| 4 | 1, 0 | 0 | $(6, 0)$ | $(5,0), (5,1), (6,0)$ |
| 5 | 0, 1 | 1 | $(6, 1)$ | $(6,0), (6,1)$ |
| 6 | 0, 1 | 1 | none | empty |

The output is 1. The queue held at most 4 messages, which is the largest number of edges crossing the boundary between processed and unprocessed vertices. Chiang and others showed that this evaluates any circuit of size $N$, given in topological order, in $O(\mathrm{Sort}(N))$ I/Os.

**Greedy maximal independent set.** Number the vertices of an undirected graph and orient each edge from the smaller to the larger end, which gives a DAG. Vertex $v$ joins the set if no smaller neighbor joined. Each vertex sends "I joined" or "I did not join" to its larger neighbors. This computes the lexicographically first [maximal independent set](/maximal-independent-set/) in $O(\mathrm{Sort}(V+E))$ I/Os, a step in external [list ranking](/list-ranking/) and in graph contraction.

**Greedy coloring.** The same orientation, with each vertex sending its color, lets each vertex take the smallest color not used by a smaller neighbor. This gives a coloring with at most $\Delta + 1$ colors, where $\Delta$ is the maximum degree; see [graph coloring](/graph-coloring/).

**Paths in a DAG.** For [single-source shortest or longest paths in a DAG](/dag-shortest-paths/), vertex $v$ sends $d(v) + w(v, u)$ to each successor $u$, and $f$ takes the minimum or the maximum.

**Trees.** In a rooted tree stored in preorder, each node sends its depth plus one to its children, which are later in preorder: this computes all depths. In postorder the edges go from children to parents, and the same loop evaluates an [expression tree](/expression-tree/) or computes subtree sizes. Together with the [Euler tour technique](/euler-tour-technique/) this gives most tree computations in $O(\mathrm{Sort}(N))$ I/Os.

## Variations

- **Backward in time.** To compute values that depend on successors, run the loop from $V$ down to 1 with a max-priority queue, or with priorities $V + 1 - w$.
- **Sweep lines.** In external computational geometry, the time is the position of a sweep line, and a priority queue holds events that are sent to a later position, such as the end of a segment. This is the same pattern, with the vertex file replaced by the sorted event file.
- **Chiang's original method.** Chiang and others first gave a divide-and-conquer method that needs no general priority queue, but needs a mild condition relating $N$, $M$ and $B$. Arge's [buffer tree](/buffer-tree/) priority queue removed the condition.
- **Cache-oblivious.** With a cache-oblivious priority queue, such as the funnel heap of Brodal and Fagerberg, the technique runs in $O(\mathrm{Sort}(V+E))$ memory transfers without knowing $M$ and $B$, under the tall-cache assumption.
- **Messages of many kinds.** Several computations can share one pass by tagging messages, as long as all use the same order.

## Pitfalls

- **The wrong priority.** The priority of a message is the topological number of the receiver, not of the sender and not an arbitrary vertex id. If ids are not topological numbers, first relabel the vertices and the edges by sorting.
- **An order that is not topological.** If one edge goes backward, its message arrives after the receiver was processed and stays in the queue forever, and the result is silently wrong. Check that the queue is empty at the end.
- **Edges stored with the wrong end.** Each vertex must find its out-edges next to itself in the file, so the edge file must be sorted by the source's topological number. Edges sorted by target need one sort first.
- **Large messages.** If a vertex sends a large value, the bound grows with the total size of all messages. Send only what the receiver needs.
- **Topological sort is not free.** The technique assumes the order. For a general DAG given without one, no I/O-efficient algorithm is known that finds it in $O(\mathrm{Sort}(V+E))$ I/Os.

## Exercises

1. Run the template on the circuit of the example with the inputs changed to 0, 1, 0, and write the queue after each vertex.
2. Show that the largest size of the queue is the largest number of edges $(u, w)$ with $u \le v < w$, over all $v$.
3. Give a time-forward algorithm that computes, for each vertex of a DAG in topological order, the number of paths from vertex 1 to it, and state its I/O cost.
4. Explain how to compute the depth of every node of a rooted tree stored as an unordered edge list, with sorting and one time-forward pass, assuming the preorder numbers are known.
5. Show that the greedy maximal independent set computed by time-forward processing is maximal and independent, and that it is the same set as the sequential greedy algorithm in vertex order produces.

## References
