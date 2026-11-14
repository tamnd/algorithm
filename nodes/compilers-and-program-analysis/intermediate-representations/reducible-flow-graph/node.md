---
tag: 2BH0BE
kind: definition
slug: reducible-flow-graph
name: Reducible flow graph
aliases:
- reducible control flow graph
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: A flow graph whose retreating edges are all back edges to dominators, so every loop has one entry, as in structured programs.
prereqs: [control-flow-graph, dominators-problem, depth-first-orders, natural-loop]
see_also: [t1-t2-reduction, loop-nesting-forest, cooper-harvey-kennedy-dominance, elimination-dataflow-methods, kam-ullman-iteration-bound, dfs-forest, strongly-connected-components, directed-acyclic-graph]
sources:
  - paper: "Matthew S. Hecht and Jeffrey D. Ullman, Flow graph reducibility, SIAM Journal on Computing 1(2) (1972), 188-202"
    locator: the transformations T1 and T2, the definition of reducibility as reduction to one node, and the uniqueness of the limit graph
  - paper: doi:10.1145/321832.321835
    title: Matthew S. Hecht and Jeffrey D. Ullman, Characterizations of reducible flow graphs, Journal of the ACM 21(3), 1974
    locator: the equivalent forms of reducibility, among them the forbidden (*) subgraph and the uniqueness of the acyclic graph of forward edges
  - paper: doi:10.1016/S0022-0000(74)80049-8
    title: Robert Endre Tarjan, Testing flow graph reducibility, Journal of Computer and System Sciences 9(3), 1974, pages 355-365
    locator: the almost-linear test for reducibility with depth-first search and disjoint set union
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 9.6.3 (edges in a depth-first spanning tree), Section 9.6.4 (back edges and reducibility), Section 9.6.5 (depth of a flow graph) and Section 9.7 (region-based analysis)
---

A reducible flow graph is a [control flow graph](/control-flow-graph/) whose loops all have a single entry. Formally, call an edge $t \to h$ a back edge if $h$ dominates $t$; the graph is reducible if removing its back edges leaves no cycle. Then every cycle is part of a [natural loop](/natural-loop/), the loops nest, and a depth-first search classifies the edges the same way whatever order it uses. Programs written with `if`, `while`, `for`, `break` and `continue` give reducible graphs; a `goto` into the middle of a loop can give an irreducible one. Many compiler algorithms are simpler or faster on reducible graphs, and some only work on them.

## Definition

Let $G = (N, E, r)$ be a flow graph in which every node is reachable from $r$. An edge $(t, h)$ is a **back edge** if $h$ dominates $t$ ([dominators problem](/dominators-problem/)); let $B$ be the set of back edges. $G$ is **reducible** if the graph $(N, E \setminus B)$ is acyclic. Otherwise it is **irreducible**.

For a depth-first search from $r$ with postorder numbers $po$, an edge $(u, v)$ is **retreating** if $po(v) \ge po(u)$. These are the edges to an ancestor in the [DFS forest](/dfs-forest/), self-loops included; every other edge, tree, forward or cross, goes to a smaller $po$.

### Equivalent forms

**Claim.** The following are equivalent.

1. $G$ is reducible: $G$ without its back edges is acyclic.
2. Every cycle of $G$ contains a back edge.
3. Every simple cycle of $G$ has a node that dominates all nodes of the cycle.
4. For every depth-first search from $r$, the retreating edges are exactly the back edges.
5. For some depth-first search from $r$, every retreating edge is a back edge.

*Proof.* (1) ⇔ (2): a cycle avoids $B$ exactly when it is a cycle of $(N, E \setminus B)$.

(2) ⇒ (3): a simple cycle contains a back edge $(t, h)$. For a node $v$ of the cycle, the part of the cycle from $v$ to $t$ does not contain $h$, which appears once, right after $t$. So $v$ is in the natural loop of $(t, h)$, and $h$ dominates $v$.

(3) ⇒ (2): if $h$ on a simple cycle dominates all its nodes, then the edge $(t, h)$ of the cycle that enters $h$ is a back edge. Every cycle contains a simple cycle, so it contains a back edge.

*Back edges are retreating, for every DFS.* If $h$ dominates $t$, then $h$ lies on the tree path from $r$ to $t$, whose nodes are the DFS ancestors of $t$, so $(t, h)$ goes to an ancestor.

(1) ⇒ (4): let $(u, v)$ be retreating, so $v$ is a DFS ancestor of $u$. A tree edge $(x, y)$ is never a back edge, because the tree path from $r$ to $x$ does not contain its descendant $y$. If $(u, v)$ were not a back edge, the tree path from $v$ to $u$ and the edge $(u, v)$ would be a cycle without back edges. So retreating edges are back edges, and with the previous paragraph the two sets are equal.

(4) ⇒ (5) is clear. (5) ⇒ (1): the back edges include all retreating edges of that search, so every edge of $E \setminus B$ goes to a smaller $po$, and no cycle can do that. $\square$

So on a reducible graph the edge classes do not depend on the order of the search: the back edges, the retreating edges and the acyclic graph $(N, E \setminus B)$ are the same for every DFS. On an irreducible graph the set of retreating edges can change with the order.

### Other characterizations

- **T1 and T2.** Hecht and Ullman (1972) defined reducibility by two transformations: T1 deletes a self-loop, and T2 merges a node with a single predecessor into that predecessor. $G$ is reducible if and only if T1 and T2 reduce it to a single node. The proof is on the page of the [T1-T2 reduction](/t1-t2-reduction/).
- **Forbidden subgraph.** Hecht and Ullman (1974) showed that $G$ is irreducible if and only if it contains a $(*)$ subgraph: nodes $a$, $b$, $c$, where $b \ne c$ and $a$ may be $r$, with paths $r \to a$, $a \to b$, $a \to c$, $b \to c$ and $c \to b$ that share no nodes except their ends. It is a cycle through $b$ and $c$ that can be entered at both. This page uses the result and does not prove it.
- **Intervals.** Allen and Cocke's interval analysis partitions the graph into single-entry regions and collapses each region to a node. $G$ is reducible exactly when repeating this ends in one node.
- **Testing.** The T1-T2 rules give a simple quadratic test. Tarjan (1974) tests reducibility in almost linear time with a depth-first search and disjoint set union.

### What reducibility gives

- **Loops.** Every cycle lies in a natural loop, natural loops are disjoint or nested, and the [loop nesting forest](/loop-nesting-forest/) is unique.
- **Fast iteration.** The *depth* of a flow graph, for a DFS, is the largest number of retreating edges on a cycle-free path. Round-robin iteration in reverse postorder of the common bit-vector data-flow problems takes at most depth plus 2 passes ([Kam-Ullman bound](/kam-ullman-iteration-bound/)). On a reducible graph, a simple path that starts at $r$ has no retreating edge at all: such an edge $(t, h)$ is a back edge, so $h$ comes before $t$ on the path, and the edge would repeat $h$. This is why the [Cooper-Harvey-Kennedy](/cooper-harvey-kennedy-dominance/) dominator algorithm needs at most 2 passes.
- **Elimination methods.** Interval and T1-T2 [elimination methods](/elimination-dataflow-methods/) solve data-flow problems by collapsing the graph, which needs it to collapse to one node.
- **Structured code.** Decompilers that rebuild source code with loops and no `goto` have an easier job on reducible graphs, since each loop has one header.

## Examples and non-examples

### Reducible

The odd-sum program of the [control flow graph](/control-flow-graph/) page has one retreating edge, $B5 \to B2$, and B2 dominates B5, so the graph is reducible. Removing $B5 \to B2$ leaves the acyclic graph $B1 \to B2 \to B3 \to \{B4, B5\}$, $B4 \to B5$, $B2 \to B6$. The nested and two-latch examples of the [natural loop](/natural-loop/) page are reducible too: each loop is entered only at its header.

Every graph without cycles is reducible, since $B$ is empty and nothing needs to be removed.

### The smallest irreducible graph

```
r:
  br p A B
A:
  x = x + 1
  br q B C
B:
  x = x * 2
  br q A C
C:
  ret x
```

The cycle $A \to B \to A$ can be entered at $A$ and at $B$ from $r$. Neither dominates the other, so neither $A \to B$ nor $B \to A$ is a back edge, $B$ is empty, and the cycle remains: the graph is irreducible. It is the $(*)$ subgraph with $a = r$, $b = A$, $c = B$. A DFS that visits $A$ first makes $B \to A$ retreating; one that visits $B$ first makes $A \to B$ retreating. T1 and T2 get stuck: there is no self-loop, $r$ has no predecessor, and $A$, $B$ and $C$ have two each.

### Irreducible code in C

```c
switch (n % 4) {
case 0: do { *to = *from++;
case 3:      *to = *from++;
case 2:      *to = *from++;
case 1:      *to = *from++;
           } while (--count > 0);
}
```

This is Duff's device. The `switch` jumps into the middle of the `do` loop, so the loop has four entries and the CFG is irreducible. A `goto` into a loop body does the same, and so does some generated code.

### Non-examples

- "Every loop has a header" is not a test by itself: an irreducible graph can contain natural loops as well. Reducibility asks that *every* cycle has one entry.
- Reducibility is not about the source language alone. A compiler transformation such as jump threading can turn a reducible graph into an irreducible one, so analyses should not assume it without checking.

### Pitfalls

- **Testing with one DFS the wrong way.** Finding retreating edges with one DFS and checking that each one's target dominates its source is a correct test (form 5). Checking only that the retreating edges form loops, without the dominance test, is not.
- **Assuming reducibility.** Code that collapses natural loops or uses interval analysis must detect irreducible regions and handle them, by node splitting or by a loop nesting forest that allows several entries. Node splitting copies code and can make the graph much larger.
- **Unreachable nodes.** Dominance is defined only for reachable nodes. Delete unreachable nodes before the test.

## Related definitions

- [Natural loop](/natural-loop/): the loop of a back edge, the building block of loops in a reducible graph.
- [T1-T2 reduction](/t1-t2-reduction/): the transformations that define reducibility and test it.
- [Loop nesting forest](/loop-nesting-forest/): the loop structure, unique on reducible graphs and defined also for irreducible ones.
- [Depth-first orders](/depth-first-orders/) and [DFS forest](/dfs-forest/): retreating edges and the order of iterative analyses.
- [Cooper-Harvey-Kennedy dominance](/cooper-harvey-kennedy-dominance/): dominators in at most two passes on a reducible graph.
- [Elimination data-flow methods](/elimination-dataflow-methods/): analyses that collapse a reducible graph.

## References
