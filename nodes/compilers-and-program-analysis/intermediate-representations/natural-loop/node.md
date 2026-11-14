---
tag: DSAB3F
kind: definition
slug: natural-loop
name: Natural loop
aliases:
- back edge loop
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: For a back edge n to h where h dominates n, the set of nodes that reach n without passing through h, with h as the single header.
prereqs: [control-flow-graph, dominators-problem]
see_also: [reducible-flow-graph, loop-nesting-forest, cooper-harvey-kennedy-dominance, dominator-tree, loop-invariant-code-motion, induction-variable-analysis, strongly-connected-components, depth-first-orders]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 9.6.4 (back edges and reducibility) and Section 9.6.6 (natural loops, with the algorithm that builds the natural loop of a back edge by a backward search from its tail)
  - book: isbn:1558603204
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 7 (Control-Flow Analysis), back edges, natural loops and their nesting
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 18 (Loop Optimizations), the section on loops, with dominators, back edges, natural loops, nested loops and the loop-nest tree
  - paper: doi:10.1145/390013.808479
    title: Frances E. Allen, Control flow analysis, Proceedings of a Symposium on Compiler Optimization, SIGPLAN Notices 5(7), 1970
    locator: dominance and intervals, the single-entry regions of a flow graph that hold its loops
---

A natural loop is the loop that a compiler sees in a [control flow graph](/control-flow-graph/). It comes from a *back edge* $t \to h$, an edge whose target $h$ dominates its source $t$. The loop is $h$ together with every block that can reach $t$ without passing through $h$. Then $h$, the *header*, is the only way into the loop, and it dominates every block of the loop. Single entry is what loop optimizations need: there is one place before the loop to put hoisted code, the *preheader*, and every run that enters the loop starts at the same block. A backward search from $t$ that stops at $h$ finds the loop in time proportional to its size.

## Definition

Let $G = (N, E, r)$ be a control flow graph in which every node is reachable from the entry $r$. A node $d$ *dominates* $v$ if every path from $r$ to $v$ contains $d$ ([dominators problem](/dominators-problem/)).

- An edge $(t, h)$ is a **back edge** if $h$ dominates $t$. A self-loop $(h, h)$ is a back edge.
- The **natural loop** of the back edge $(t, h)$ is
$$L(t, h) = \{h\} \cup \{\, v \in N : \text{there is a path from } v \text{ to } t \text{ that does not contain } h \,\}.$$
- $h$ is the **header** of the loop and $t$ is a **latch**. The *body* is $L(t, h)$. An edge $(u, w)$ with $u \in L$ and $w \notin L$ is an **exit edge**.
- When several back edges share the header $h$, compilers usually treat the union of their natural loops as one loop with header $h$. It has the same properties as below.

A back edge in this sense is the target of the arrow being a dominator. A *retreating edge* of a depth-first search, an edge to an ancestor in the DFS tree, need not be a back edge; the graphs in which every retreating edge is a back edge are the [reducible flow graphs](/reducible-flow-graph/).

### Building the loop

```
NATURAL-LOOP(G, t, h)          (t, h) is a back edge
1  loop <- {h}; stack <- empty
2  if t != h then add t to loop; push t
3  while stack is not empty do
4      pop v
5      for each predecessor p of v do
6          if p is not in loop then add p to loop; push p
7  return loop
```

**Claim 1.** NATURAL-LOOP returns $L(t, h)$, and it runs in time proportional to the number of nodes of the loop plus the number of edges that end in a node of the loop other than $h$.

*Proof.* Every node is pushed at most once, because it is added to $loop$ when it is pushed and never removed, and $h$ is in $loop$ from line 1, so it is never pushed. Each popped node scans its predecessor list once, which gives the time bound.

*Every node in the result is in $L(t, h)$.* For each pushed node $v$ we show that a path from $v$ to $t$ avoids $h$. For $v = t$ the path of length 0 does, since $t \ne h$ when $t$ is pushed. A node $p$ is pushed in line 6 as a predecessor of a popped node $v$; $v$ was pushed, so $v \ne h$ and $v$ reaches $t$ without $h$, and $p \ne h$ because $h$ is in $loop$. So the path $p, v, \ldots, t$ avoids $h$.

*Every node of $L(t, h)$ is in the result.* $h$ is added in line 1. Let $v \ne h$ have a path $v = v_0, v_1, \ldots, v_k = t$ that avoids $h$; we use induction on $k$. If $k = 0$, then $v = t \ne h$ is added in line 2. Otherwise $v_1$ has a shorter path to $t$ that avoids $h$, so $v_1$ is added, and since $v_1 \ne h$ it was pushed, so it is popped later, and line 6 adds its predecessor $v$ if it is not already there. $\square$

The search never passes $h$, so it stays inside the loop even if the header has many predecessors outside.

### Properties

**Claim 2.** Let $L = L(t, h)$.

1. $h$ dominates every node of $L$.
2. Every edge from a node outside $L$ to a node of $L$ ends at $h$. So $h$ is the only entry.
3. $L$ is strongly connected: every node of $L$ reaches every other one by a path inside $L$.

*Proof.* (1) Let $v \in L$, $v \ne h$, with a path from $v$ to $t$ that avoids $h$. If a path from $r$ to $v$ avoided $h$, then together they would give a path from $r$ to $t$ that avoids $h$, but $h$ dominates $t$.

(2) Let $(u, w)$ be an edge with $w \in L$ and $w \ne h$. Then $w$ has a path to $t$ that avoids $h$. If $u \ne h$, then $u$, $w$, and that path form a path from $u$ to $t$ that avoids $h$, so $u \in L$. If $u = h$, then $u \in L$ too. So an edge from outside ends at $h$.

(3) From $v \in L$, a path to $t$ that avoids $h$ stays in $L$, since each node on it reaches $t$ without $h$; then the edge $(t, h)$ leads to $h$. From $h$ to $v \in L$: take a path from $r$ to $v$; by (1) it contains $h$; take the part after the last $h$. Each node $w$ on that part reaches $v$ without $h$, and $v$ reaches $t$ without $h$ (or $v = h$, and the part is just $h$), so $w \in L$. $\square$

**Claim 3 (nesting).** Two natural loops with different headers are either disjoint or one is a proper subset of the other.

*Proof.* Let $L_1 = L(t_1, h_1)$ and $L_2 = L(t_2, h_2)$ with $h_1 \ne h_2$ share a node $v$. By Claim 2, $h_1$ and $h_2$ both dominate $v$. The dominators of a node lie on one path of the [dominator tree](/dominator-tree/), so one of them dominates the other; say $h_2$ strictly dominates $h_1$. Then $h_2 \notin L_1$, since every node of $L_1$ is dominated by $h_1$, and $h_1$ does not dominate $h_2$. In particular $v \ne h_2$, so $v$ has a path to $t_2$ that avoids $h_2$. By the proof of Claim 2 (3), there is a path from $h_1$ to $v$ inside $L_1$, so it avoids $h_2$. Joined, they show that $h_1$ reaches $t_2$ without $h_2$, so $h_1 \in L_2$. Now every $u \in L_1$ reaches $t_1$ inside $L_1$, then $h_1$ by the back edge, then $t_2$ as just shown, all without $h_2$. So $u \in L_2$, and $L_1 \subseteq L_2$. The inclusion is proper because $h_2 \in L_2 \setminus L_1$. $\square$

After the loops with the same header are merged, Claim 3 makes the natural loops a forest under inclusion, the [loop nesting forest](/loop-nesting-forest/) of a reducible graph. The innermost loop that contains a block gives its *loop depth*.

## Examples and non-examples

### A loop with a branch inside

The odd-sum program of the [control flow graph](/control-flow-graph/) page has the edges $B1 \to B2$, $B2 \to B3$, $B2 \to B6$, $B3 \to B4$, $B3 \to B5$, $B4 \to B5$, $B5 \to B2$. B2 dominates B5, so $B5 \to B2$ is a back edge. The backward search from B5 adds B3 and B4, then from B3 it finds B2, which is already in the loop, and stops. The natural loop is $\{B2, B3, B4, B5\}$ with header B2 and the exit edge $B2 \to B6$.

### Nested loops

```
B0:
  i = 0
  s = 0
  jump B1
B1:
  t = i < n
  br t B2 B6
B2:
  j = 0
  jump B3
B3:
  u = j < i
  br u B4 B5
B4:
  s = s + j
  j = j + 1
  jump B3
B5:
  i = i + 1
  jump B1
B6:
  ret s
```

The edges are $B0 \to B1$, $B1 \to B2$, $B1 \to B6$, $B2 \to B3$, $B3 \to B4$, $B3 \to B5$, $B4 \to B3$, $B5 \to B1$. Computed by the definition, the back edges are $B4 \to B3$ and $B5 \to B1$. Their natural loops are $\{B3, B4\}$ and $\{B1, B2, B3, B4, B5\}$, and the first lies inside the second, as Claim 3 says. B4 has loop depth 2, B2 and B5 have depth 1, and B0 and B6 have depth 0. The program adds $j$ over all $0 \le j < i < n$; the toy interpreter returns 4 for $n = 4$ and 10 for $n = 5$.

### Two latches, one header

```
B0:
  i = 0
  s = 0
  jump B1
B1:
  t = i < n
  br t B2 B5
B2:
  i = i + 1
  r = i % 3
  br r B3 B1
B3:
  s = s + i
  jump B1
B5:
  ret s
```

This is a loop with a `continue`: B2 jumps back to B1 when $i$ is a multiple of 3, and B3 jumps back after adding $i$. Both $B2 \to B1$ and $B3 \to B1$ are back edges. Their natural loops are $\{B1, B2\}$ and $\{B1, B2, B3\}$, which share the header, so Claim 3 does not apply; a compiler merges them into one loop $\{B1, B2, B3\}$. On $n = 4$ the run returns $1 + 2 + 4 = 7$.

### Non-examples

- **A cycle with two entries.** In the graph $r \to a$, $r \to b$, $a \to c$, $b \to d$, $c \to d$, $d \to c$, the cycle $c, d$ is entered at $c$ from $a$ and at $d$ from $b$. Neither $c$ nor $d$ dominates the other, so neither $c \to d$ nor $d \to c$ is a back edge, and the cycle is not a natural loop. Such graphs are not reducible; a [loop nesting forest](/loop-nesting-forest/) still describes the cycle, with two entries.
- **A retreating edge that is not a back edge.** In the same graph, a DFS that visits $a$ first has $d \to c$ as a retreating edge, an edge to a DFS ancestor. It is not a back edge, because $c$ does not dominate $d$.
- **A strongly connected component.** The [strongly connected components](/strongly-connected-components/) of a CFG are the maximal sets of blocks that all reach each other. One component can hold several natural loops, nested or with a shared header, and the component $\{c, d\}$ above holds none.

### Pitfalls

- **Searching forward from the header.** The blocks that $h$ reaches are not the loop: they include the code after the loop. The search must go backward from the latch and stop at $h$.
- **Not stopping at the header.** If the search continues through $h$, it runs into the code before the loop and, through the entry, into the whole procedure.
- **Unreachable blocks.** An unreachable block that jumps into the loop would be added by the backward search. Delete unreachable blocks first, as the definition assumes.
- **Treating every retreating edge as a loop.** On an irreducible graph some retreating edges have no natural loop; an optimization that needs a single header must check dominance, or first make the graph reducible by node splitting.
- **Loops with the same header.** The natural loops of two back edges to $h$ overlap without nesting. Merge them, or a loop pass may see the same header twice.

## Related definitions

- [Dominators problem](/dominators-problem/), [dominator tree](/dominator-tree/) and [Cooper-Harvey-Kennedy dominance](/cooper-harvey-kennedy-dominance/): the dominance needed to find back edges.
- [Reducible flow graph](/reducible-flow-graph/): every cycle has a back edge, so the natural loops cover all loops.
- [Loop nesting forest](/loop-nesting-forest/): the loops arranged by inclusion, also for irreducible graphs.
- [Depth-first orders](/depth-first-orders/): retreating edges, the candidates for back edges.
- [Loop-invariant code motion](/loop-invariant-code-motion/) and [induction variable analysis](/induction-variable-analysis/): optimizations that work on natural loops and use the preheader.

## References
