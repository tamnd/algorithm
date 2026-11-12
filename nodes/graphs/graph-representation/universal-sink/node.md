---
tag: SXFMZV
kind: problem
slug: universal-sink
name: Universal sink
area: graphs/graph-representation
level: intro
summary: Decide whether a directed graph has a vertex with an edge from every other vertex and no outgoing edges, using its adjacency matrix in linear time.
prereqs: [adjacency-matrix, directed-graph, in-degree-and-out-degree]
see_also: [adjacency-matrix, in-degree-and-out-degree, adjacency-query, adversary-argument, lower-bound, vertex, decision-tree-model, adjacency-list]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1 (Representations of graphs), Exercise 20.1-6, the universal sink in O(V) time from the adjacency matrix
  - book: isbn:9780201120370
    title: Udi Manber, Introduction to Algorithms, A Creative Approach, Addison-Wesley, 1989
    locator: Section 5.5, the celebrity problem and its solution by elimination with at most 3(n - 1) questions
---

The universal sink problem asks whether a [directed graph](/directed-graph/), given by its [adjacency matrix](/adjacency-matrix/), has a [vertex](/vertex/) that every other vertex points to and that points to no vertex. Such a vertex has in-degree $n - 1$ and out-degree 0. The question looks as if it needs the whole matrix, $n^2$ entries, but it can be answered by reading fewer than $3n$ of them. It is CLRS Exercise 20.1-6, and in the form of the *celebrity problem* (a person whom everyone knows and who knows no one) it is a standard example of design by elimination: each probe of the matrix rules out one candidate.

## In plain words

At a party, a celebrity is someone everyone knows but who knows no one. You may ask any guest "do you know that person?". You want to find the celebrity, or learn that there is none, with few questions.

Ask guest A whether they know guest B. If yes, A is not the celebrity, since a celebrity knows no one. If no, B is not the celebrity, since everyone knows a celebrity. Either way one guest is out. After one fewer question than there are guests, only one guest is left. Then check that one guest with a few more questions. The total is less than three questions per guest.

## Definition

**Input.** A directed graph $G = (V, E)$ with $V = \{0, \ldots, n - 1\}$, $n \ge 1$, $E \subseteq V \times V$, given as its adjacency matrix $A$: $A[i, j] = 1$ if $(i, j) \in E$ and 0 otherwise. The diagonal (self-loops) is ignored.

**Universal sink.** A vertex $s$ is a universal sink if

$$A[i, s] = 1 \text{ for every } i \ne s \qquad \text{and} \qquad A[s, j] = 0 \text{ for every } j \ne s,$$

that is, $d^-(s) = n - 1$ and $d^+(s) = 0$, not counting a loop. In the matrix, column $s$ is all ones and row $s$ is all zeros, off the diagonal.

**Output.** The universal sink $s$, or "none".

**Cost measure.** The number of probes, reads of one entry $A[i, j]$, and the time on the [word RAM](/word-ram/), where a probe costs $O(1)$.

**At most one.** If $s \ne t$ were both universal sinks, then $A[t, s] = 1$ because $s$ is a universal sink, and $A[t, s] = 0$ because $t$ is one. So a graph has at most one universal sink, and the output is well defined.

## Variants

- **Celebrity problem.** "$i$ knows $j$" is the edge $(i, j)$. A celebrity is a universal sink. The query "does $i$ know $j$?" is a probe.
- **Universal source.** A vertex with out-degree $n - 1$ and in-degree 0. It is a universal sink of the [transpose](/transpose-graph/), so the same method works with the roles of rows and columns swapped.
- **Adjacency lists.** With [adjacency lists](/adjacency-list/), compute all in-degrees in one pass and check the out-degrees from the list lengths: $\Theta(n + m)$ time. A sink has $d^-(s) = n - 1$, so if one exists then $m \ge n - 1$ and this bound is never below $\Theta(n)$.
- **Sink, not universal.** A vertex with out-degree 0 only. From a matrix this needs $\Theta(n^2)$ probes in the worst case, since every row may have its single 1 in the last place probed.

## Examples

Let $n = 4$ and

$$A = \begin{pmatrix} 0 & 1 & 1 & 0 \\ 0 & 0 & 1 & 1 \\ 0 & 0 & 0 & 0 \\ 1 & 0 & 1 & 0 \end{pmatrix}.$$

**Elimination.** Start with the candidate $c = 0$. Probe $A[0, 1] = 1$: vertex 0 has an out-edge, so it is out, and $c = 1$. Probe $A[1, 2] = 1$: 1 is out, $c = 2$. Probe $A[2, 3] = 0$: vertex 3 lacks the in-edge from 2, so 3 is out, and $c$ stays 2. That is $n - 1 = 3$ probes.

**Check.** Row 2 off the diagonal: $A[2, 0] = A[2, 1] = A[2, 3] = 0$. Column 2 off the diagonal: $A[0, 2] = A[1, 2] = A[3, 2] = 1$. So vertex 2 is the universal sink. The check used 6 probes, but $A[1, 2]$ and $A[2, 3]$ were already read, so 4 new probes suffice, and the total is 7 out of the 12 entries off the diagonal.

**No sink.** Change $A[2, 0]$ to 1. Elimination still ends at $c = 2$, since it never read $A[2, 0]$, and then the check finds $A[2, 0] = 1$. The answer is "none".

## Known algorithms

**Elimination and check.** Let $c = 0$. For $j = 1, \ldots, n - 1$: if $A[c, j] = 1$, set $c = j$. Then test row $c$ and column $c$ off the diagonal, and return $c$ if row $c$ is all zeros and column $c$ is all ones; otherwise return "none".

*Correctness.* The loop keeps this invariant: after step $j$, no vertex in $\{0, \ldots, j\} \setminus \{c\}$ is a universal sink. At step $j$, if $A[c, j] = 1$, then $c$ has an out-edge and is not a sink, and $j$ becomes the candidate. If $A[c, j] = 0$, then $j$ lacks the in-edge from $c$ and is not a sink. Either way one of $c$ and $j$ is ruled out, and the other is the candidate. At the end, every vertex except $c$ is ruled out, so $c$ is the only possible universal sink, and the check decides it.

*Cost.* $n - 1$ probes in the loop and $2(n - 1)$ in the check, so at most $3(n - 1)$ probes and $\Theta(n)$ time, with $O(1)$ extra space. Entries already read in the loop need not be read again in the check, which saves a few probes.

## Bounds

**Upper bound.** $3(n - 1)$ probes and $O(n)$ time, as above. This is a factor of about $n/3$ below the $n(n - 1)$ entries off the diagonal.

**Lower bound for a "yes" answer.** If an algorithm answers "$s$ is the universal sink", it must have probed all $2(n - 1)$ entries in row $s$ and column $s$ off the diagonal. *Proof by adversary.* Suppose $A[i, s]$ was not probed, for some $i \ne s$. Then the graph with $A[i, s] = 0$ and all probed entries the same is consistent with every answer the algorithm saw, and in it $s$ is not a universal sink. So the algorithm is wrong on one of the two graphs. The same holds for an unprobed $A[s, j]$. Hence every correct algorithm uses at least $2(n - 1)$ probes on a graph with a universal sink, and the problem needs $\Theta(n)$ probes.

**Why not all the matrix.** Many graph properties of a matrix need all $\binom{n}{2}$ or $n(n-1)$ entries in the worst case; such properties are called evasive. The universal sink is a standard example of a property that is not evasive. See [lower bound](/lower-bound/) and [adversary argument](/adversary-argument/).

## Reductions

- **Celebrity.** The celebrity problem is the same problem with "knows" as the edge relation.
- **Universal source.** A universal source of $G$ is a universal sink of $G^T$; read $A[j, i]$ in place of $A[i, j]$.
- **To degrees.** The universal sink is the vertex with $d^-(v) = n - 1$ and $d^+(v) = 0$, so computing all [in- and out-degrees](/in-degree-and-out-degree/) solves the problem, at a cost of $\Theta(n^2)$ from a matrix and $\Theta(n + m)$ from lists.

## Applications

- **A teaching example.** It shows that the cost of a problem on an adjacency matrix is not always $\Theta(n^2)$, and that a lower bound must be proved with an adversary rather than assumed.
- **Elimination tournaments.** The same pattern, one comparison rules out one candidate, finds a maximum in $n - 1$ comparisons and a majority candidate in the Boyer-Moore vote.

## References
