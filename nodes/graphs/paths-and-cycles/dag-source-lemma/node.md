---
tag: 695XM0
kind: theorem
slug: dag-source-lemma
name: Every DAG has a source node
aliases:
- A DAG has a node with no incoming edges
area: graphs/paths-and-cycles
level: intro
summary: Every finite directed acyclic graph with at least one vertex has a vertex with no incoming edges, the fact that underlies topological ordering.
prereqs: [directed-acyclic-graph, in-degree-and-out-degree, simple-path]
see_also: [topological-ordering-theorem, kahns-algorithm, topological-sort, cycle-detection, dag-longest-path, topological-ordering]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 3.6, Directed acyclic graphs and topological ordering (the statement that a DAG has a node with no incoming edges, and its use to build a topological ordering)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 3, Section 3.3.2, Directed acyclic graphs (every DAG has at least one source and at least one sink)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.3, Linked allocation (topological sorting, Algorithm T, which repeatedly outputs an object with no predecessors)
---

The source lemma says that every finite [directed acyclic graph](/directed-acyclic-graph/) with at least one vertex has a *source*, a vertex with in-degree zero. By symmetry it also has a *sink*, a vertex with out-degree zero. The proof is two lines: follow incoming edges backwards, and since the graph is finite and has no cycle, the walk must stop at a source. The lemma is the induction step of the [topological ordering theorem](/topological-ordering-theorem/) and the loop invariant of [Kahn's algorithm](/kahns-algorithm/).

## Statement

Let $G = (V, E)$ be a directed graph with a finite, nonempty vertex set. Parallel edges are allowed; a [self-loop](/self-loop/) $(v, v)$ is a directed cycle of length 1, so a DAG has none. A *directed cycle* is a closed directed walk $u_1 \to u_2 \to \cdots \to u_k \to u_1$ with $k \ge 1$ and distinct $u_1, \ldots, u_k$. Write $d^-(v)$ for the in-degree of $v$ and $d^+(v)$ for its out-degree.

**Lemma (sources).** If $G$ has no directed cycle, then some $v \in V$ has $d^-(v) = 0$.

**Strong form.** If $G$ has no directed cycle, then for each vertex $x$ there is a source $s$ and a directed path from $s$ to $x$. Dually, for each $x$ there is a sink $t$ and a directed path from $x$ to $t$.

**Characterization.** $G$ has no directed cycle if and only if every nonempty induced subgraph $G[S]$, $\emptyset \ne S \subseteq V$, has a source (a vertex with no incoming edge from $S$).

## In plain words

Think of the edges as rules "do this job before that job". If there are no circular rules, some job has no rule in front of it, and you can start there.

To find it, pick any job and ask which job must come before it. Then ask the same of that job, and so on. You never meet the same job twice, because that would be a circle of rules. There are only so many jobs, so the questions must stop, and they stop at a job with nothing in front of it. The same walk shows that every job can be traced back to such a starting job.

## Proof

**Strong form, hence the lemma.** Let $G$ have no directed cycle and let $x \in V$. Build a sequence $w_0 = x, w_1, w_2, \ldots$: as long as $d^-(w_i) \ge 1$, choose an edge $(w_{i+1}, w_i) \in E$. We claim that the $w_i$ are distinct. Suppose $w_i = w_j$ with $i < j$, and choose such a pair with $j - i$ least. Then $w_j \to w_{j-1} \to \cdots \to w_{i+1} \to w_i = w_j$ is a closed directed walk of length $j - i \ge 1$ whose vertices $w_{i+1}, \ldots, w_j$ are distinct by the choice of the pair, so it is a directed cycle (a self-loop when $j - i = 1$). This contradicts the hypothesis. Since the $w_i$ are distinct and $V$ has $n$ elements, the sequence has at most $n$ terms, so it stops at some $w_k$ with $k \le n - 1$, and it stops only when $d^-(w_k) = 0$. So $s = w_k$ is a source, and $s = w_k \to w_{k-1} \to \cdots \to w_0 = x$ is a directed path from $s$ to $x$. Taking any $x$ proves the lemma, because $V \ne \emptyset$.

**Sinks.** Apply the strong form to the reverse graph, with every edge turned around. It has no directed cycle, its sources are the sinks of $G$, and a path from a source to $x$ in it is a path from $x$ to a sink in $G$.

**Characterization.** If $G$ has no directed cycle, neither has $G[S]$, because each cycle of $G[S]$ is a cycle of $G$. So the lemma applies to $G[S]$ when $S \ne \emptyset$. Conversely, if $G$ has a directed cycle $u_1 \to \cdots \to u_k \to u_1$, let $S = \{u_1, \ldots, u_k\}$. In $G[S]$ each $u_i$ has an incoming edge from $u_{i-1}$ (from $u_k$ when $i = 1$), so $G[S]$ has no source. $\blacksquare$

**A second proof of the lemma.** Let $P = v_0 \to v_1 \to \cdots \to v_k$ be a directed path of $G$ with the largest number of edges; paths have at most $n - 1$ edges, so it exists, and $k = 0$ is allowed. If some edge $(u, v_0)$ existed, then either $u = v_i$ for some $i$, and $v_0 \to \cdots \to v_i \to v_0$ is a cycle, or $u$ is not on $P$, and $u \to v_0 \to \cdots \to v_k$ is a longer path. Both are impossible, so $v_0$ is a source.

## Consequences

- **Topological order.** Remove a source, apply the lemma again to the rest, and repeat. The order of removal is a [topological ordering](/topological-ordering/). This is the proof of "acyclic implies orderable" in the [topological ordering theorem](/topological-ordering-theorem/), and it is [Kahn's algorithm](/kahns-algorithm/), which keeps the in-degrees and a queue of current sources and runs in $\Theta(n + m)$ time.
- **Cycle detection.** Kahn's algorithm stops with vertices left over exactly when the graph has a cycle: by the characterization, the set of left-over vertices induces a subgraph with no source. So the lemma also gives a linear-time [cycle detection](/cycle-detection/) method that does not use depth-first search.
- **Finding a source.** Computing all in-degrees takes $\Theta(n + m)$ time. With lists of incoming edges, the walk of the proof finds a source in at most $n - 1$ steps of $O(1)$ time each, after the lists are built.
- **Dynamic programming on DAGs.** Recurrences over a DAG, such as [longest paths in a DAG](/dag-longest-path/), start at the sources, whose values need no predecessor. The strong form shows that each vertex is reached from some source.
- **Well-founded orders.** A finite strict partial order, seen as a DAG, has a minimal element. This is the lemma for the graph of the order relation.

## Tightness

**Finiteness is needed.** On the vertices $0, 1, 2, \ldots$ with the edges $i + 1 \to i$, there is no cycle, but each vertex $i$ has the incoming edge from $i + 1$. So an infinite DAG need not have a source. The proof breaks exactly where it uses $|V| = n$ to stop the walk.

**The converse of the lemma is false.** The graph $0 \to 1 \to 2 \to 1$ has the source 0, but it has the cycle $1 \to 2 \to 1$. A source in $G$ says nothing about the rest of the graph; only the characterization, with all induced subgraphs, is an equivalence.

**One source is possible.** The path $0 \to 1 \to \cdots \to n - 1$ is a DAG with exactly one source and one sink, so the lemma cannot promise more than one. A graph with no edges has $n$ sources, the most possible.

**A cycle blocks every source.** In a directed cycle on $n \ge 1$ vertices, each vertex has in-degree 1, so there is no source.

## History

The lemma is folklore and appears in each textbook account of topological sorting. Knuth presents topological sorting, with the repeated removal of an object that has no predecessors, as Algorithm T in Section 2.2.3 of the first volume of The Art of Computer Programming. Kleinberg and Tardos state the lemma explicitly as the main step toward a topological ordering, and Dasgupta, Papadimitriou and Vazirani state that each DAG has at least one source and at least one sink.

## References
