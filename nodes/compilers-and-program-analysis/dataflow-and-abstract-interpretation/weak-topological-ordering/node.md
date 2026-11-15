---
tag: X5B201
kind: algorithm
slug: weak-topological-ordering
name: Weak topological ordering
aliases:
- Bourdoncle iteration strategy
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: Orders the nodes of a flow graph as nested components with heads, giving the points where to widen and a good order of iteration.
model: word-ram
complexity:
  vars: {n: the number of vertices reachable from the root, m: the number of edges between them, k: the largest number of components that contain one vertex}
  time: {worst: O((k + 1)(n + m)), average: O((k + 1)(n + m)), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true}
history:
  year: 1993
  people: [François Bourdoncle]
  note: Bourdoncle defined weak topological orderings, built them with a recursive form of Tarjan's strongly connected components algorithm, and proved that widening at the component heads is enough.
prereqs: [tarjan-scc, widening-operator, control-flow-graph]
see_also: [strongly-connected-components, topological-sort, depth-first-orders, loop-nesting-forest, reducible-flow-graph, worklist-dataflow-algorithm, narrowing-operator, abstract-interpretation]
sources:
  - paper: doi:10.1007/BFb0039704
    title: "François Bourdoncle, Efficient chaotic iteration strategies with widenings, Formal Methods in Programming and Their Applications (FMPA 1993), LNCS 735, pages 128 to 141"
    locator: the definition of hierarchical and weak topological orderings, the algorithm built on Tarjan's algorithm, the iterative and recursive iteration strategies, and the result that the heads of the components are an admissible set of widening points
  - paper: doi:10.1137/0201010
    title: "Robert Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 1972, pages 146 to 160"
    locator: the depth-first numbering and the low values that find the strongly connected components, which the visit procedure reuses
  - paper: doi:10.1145/512950.512973
    title: "Patrick Cousot and Radhia Cousot, Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints, POPL 1977, pages 238 to 252"
    locator: the upward iteration with widening, applied at a set of points that cuts every loop of the program
---

A weak topological ordering (WTO) of a directed graph is a total order of its vertices with nested parentheses, such as `entry (outer init (inner body) next) exit`. Each parenthesized group is a strongly connected part of the graph, and its first vertex is its *head*. Bourdoncle's algorithm builds a WTO in $O((k + 1)(n + m))$ time, where $k$ is the nesting depth, by applying [Tarjan's SCC algorithm](/tarjan-scc/) again inside each component. An abstract interpreter then iterates the equations in this order, stabilizes each inner component before the outer one, and applies the [widening](/widening-operator/) only at the heads. Every cycle of the graph passes through a head, so this is enough to make the iteration stop.

## In plain words

An analyzer computes a value at each block of a program, and it must recompute the blocks of a loop until nothing changes. Two questions come up. In which order should it visit the blocks? And where must it widen, so that a loop with an unknown trip count does not keep it busy forever?

A WTO answers both. It lists the blocks so that, outside loops, every block comes after the blocks that feed it. A loop is written as a group in parentheses, with its entry block first. The analyzer runs through a group again and again until the entry block of the group stops changing. It widens only at the first block of each group. Inner loops are groups inside groups, and the analyzer settles an inner loop before it goes on with the outer one.

## The problem

The input is a directed graph $G = (V, E)$, given by the successor lists $\mathit{succ}(v)$, and a root $r$. In program analysis $G$ is a [control flow graph](/control-flow-graph/) and $r$ is its entry block. Let $V_r$ be the set of vertices reachable from $r$.

A *hierarchical ordering* of $V_r$ is a sequence of the vertices of $V_r$, each once, with matched parentheses, where every opening parenthesis is followed at once by a vertex, the *head* of that component. For a vertex $c$, $\omega(c)$ is the set of heads of the components that contain $c$; a head belongs to its own component. Write $u \prec v$ when $u$ comes before $v$ in the sequence. The ordering is a **weak topological ordering** when every edge $u \to v$ with $u \in V_r$ satisfies

$$ \bigl(u \prec v \ \text{ and } \ v \notin \omega(u)\bigr) \quad \text{or} \quad \bigl(v \preceq u \ \text{ and } \ v \in \omega(u)\bigr). $$

So an edge either goes forward, and does not enter a component through its head from inside, or it goes backward, to the head of a component that contains its source. A topological order of a graph without cycles is a WTO with no parentheses.

The second task is to solve equations $x_v = F_v(x)$, one for each vertex, over an [abstract domain](/abstract-domain/) with a widening $\nabla$, and to return values with $F_v(x) \sqsubseteq x_v$ at every vertex.

## The algorithm

WTO uses a counter $\mathit{num}$, a stack $S$ and a depth-first number $\mathit{DFN}[v]$, which is 0 for a vertex not yet visited, a positive number for a vertex on the stack, and $+\infty$ for a vertex that is already placed. A partition $P$ is a list of elements; an element is a vertex or a component $(h, C)$, whose body $C$ is a partition. ITERATE is the recursive iteration strategy; every value $x[v]$ is $\bot$ at the start.

```pseudo id=main
WTO(G, r)
L1  for each v in V do DFN[v] ← 0
L2  num ← 0, S ← empty stack, P ← empty list
L3  VISIT(r, P)
L4  return P

VISIT(v, P)                                ▷ returns the least DFN reached from v
L5  push v on S, num ← num + 1, DFN[v] ← num
L6  head ← DFN[v], loop ← false
L7  for each w in succ(v) do
L8      if DFN[w] = 0 then min ← VISIT(w, P) else min ← DFN[w]
L9      if min ≤ head then head ← min, loop ← true
L10 if head = DFN[v] then                  ▷ v is the root of a strongly connected part
L11     DFN[v] ← +∞, e ← pop S
L12     if loop then
L13         while e ≠ v do DFN[e] ← 0, e ← pop S
L14         add COMPONENT(v) to the front of P
L15     else add v to the front of P
L16 return head

COMPONENT(v)
L17 C ← empty list
L18 for each w in succ(v) do
L19     if DFN[w] = 0 then VISIT(w, C)
L20 return (v, C)

ITERATE(P)
L21 for each element e of P, in order do
L22     if e is a vertex v then x[v] ← F_v(x)
L23     else let (h, C) = e
L24         x[h] ← x[h] ∇ F_h(x)
L25         repeat
L26             ITERATE(C)
L27             t ← F_h(x)
L28             if t ⊑ x[h] then leave the repeat loop
L29             x[h] ← x[h] ∇ t
```

**VISIT** is Tarjan's algorithm with one change. Line L9 computes the least depth-first number that $v$ reaches, as Tarjan's low value does, and also records in $\mathit{loop}$ whether $v$ reaches a vertex numbered at most $v$ itself, that is, whether $v$ lies on a cycle of its part. A vertex placed earlier has $\mathit{DFN} = +\infty$, so it never lowers $\mathit{head}$. When line L10 finds the root $v$ of a strongly connected part, either the part is $v$ alone with no self-loop (line L15), or line L13 takes the other vertices off the stack and marks them unvisited again. Line L14 then calls COMPONENT, which runs the same search on the part without $v$: $v$ now has $\mathit{DFN} = +\infty$, so every edge back to it is ignored, and the search splits the rest into smaller parts. Each finished element goes to the front of the list, so the elements come out in a topological order of the parts, as in Tarjan's algorithm.

**ITERATE** walks the WTO. A vertex outside every component is computed once (line L22). A component is computed again and again: the head is widened (lines L24 and L29), then the body is stabilized by a recursive call (line L26), and the loop ends when the head no longer grows (line L28). Only the head is tested. Only the heads are widened.

## Example

The program has two nested loops. Its parameter is `n`; here $n = 3$.

```
entry:
  i = 0
  jump outer
outer:
  t = i < 3
  br t init exit
init:
  j = 0
  jump inner
inner:
  u = j < i
  br u body next
body:
  j = j + 1
  jump inner
next:
  i = i + 1
  jump outer
exit:
  ret i
```

The edges are entry $\to$ outer, outer $\to$ init, outer $\to$ exit, init $\to$ inner, inner $\to$ body, inner $\to$ next, body $\to$ inner and next $\to$ outer, with the successors in this order. The table lists the calls of VISIT in the order in which they finish.

| call | DFN | returns | what happens |
|---|---|---|---|
| VISIT(body) | 5 | 4 | sees inner with DFN 4, so it is not a root |
| VISIT(next) | 6 | 2 | sees outer with DFN 2 |
| VISIT(inner) | 4 | 2 | loop is true, but 2 < 4, so it is not a root |
| VISIT(init) | 3 | 2 | not a root |
| VISIT(exit) | 7 | 7 | a root with no loop: $P$ = [exit] |
| VISIT(outer) | 2 | 2 | a root with a loop: pop next, body, inner, init and set their DFN to 0; call COMPONENT(outer) |
| inside: VISIT(next) | 11 | 11 | outer has DFN $+\infty$; a root with no loop: $C$ = [next] |
| inside: VISIT(body) | 12 | 12 | called by COMPONENT(inner); inner has DFN $+\infty$: $C'$ = [body] |
| inside: VISIT(inner) | 9 | 9 | a root with a loop: $C$ = [(inner body), next] |
| inside: VISIT(init) | 8 | 8 | a root with no loop: $C$ = [init, (inner body), next] |
| VISIT(entry) | 1 | 1 | a root with no loop |

The result is `entry (outer init (inner body) next) exit`. The heads are `outer` and `inner`; $\omega(\mathit{body}) = \{\mathit{outer}, \mathit{inner}\}$. The back edges body $\to$ inner and next $\to$ outer each go to a head that contains their source.

Now ITERATE runs an [interval](/interval-domain/) analysis on this WTO. The value of a block is the state at its start; `j` has no value before `init`, so it is $\top$ there. The guard `j < i` on the edge to `body` refines `j` below the upper bound of `i` and `i` above the lower bound of `j`.

| step | vertex | line | $i$ | $j$ | note |
|---|---|---|---|---|---|
| 1 | entry | L22 | $\top$ | $\top$ | |
| 2 | outer | L24 | $[0, 0]$ | $\top$ | $\bot \nabla [0, 0]$ |
| 3 | init | L22 | $[0, 0]$ | $\top$ | |
| 4 | inner | L24 | $[0, 0]$ | $[0, 0]$ | |
| 5 | body | L22 | $\bot$ | $\bot$ | the guard $j < i$ fails |
| 6 | inner | L28 | $[0, 0]$ | $[0, 0]$ | stable: leave the inner loop |
| 7 | next | L22 | $[0, 0]$ | $[0, 0]$ | |
| 8 | outer | L29 | $[0, +\infty]$ | $\top$ | $F$ gives $i \in [0, 1]$; widen |
| 9 | init | L22 | $[0, 2]$ | $\top$ | |
| 10 | inner | L24 | $[0, +\infty]$ | $[0, 0]$ | $F$ gives $i \in [0, 2]$; the widening with the old $[0, 0]$ jumps |
| 11 | body | L22 | $[1, +\infty]$ | $[0, 0]$ | |
| 12 | inner | L29 | $[0, +\infty]$ | $[0, +\infty]$ | $F$ gives $j \in [0, 1]$; widen |
| 13 | body | L22 | $[1, +\infty]$ | $[0, +\infty]$ | |
| 14 | inner | L28 | | | stable: leave the inner loop |
| 15 | next | L22 | $[0, +\infty]$ | $[0, +\infty]$ | |
| 16 | outer | L28 | | | stable: leave the outer loop |
| 17 | exit | L22 | $[3, +\infty]$ | $\top$ | |

The run makes 17 evaluations of some $F_v$, with widening at two vertices only. The order of the evaluations is entry, outer, then init, inner, body, inner, next, outer, then the same pass with one more round of the inner loop, and last exit. Step 10 shows a weakness discussed under Pitfalls. Inside the inner loop `i` is at most 2, but the old value $[0, 0]$ of the inner head makes the widening jump to $+\infty$. A [narrowing](/narrowing-operator/) pass does not repair this, because the cycle inner $\to$ body $\to$ inner keeps the bound $+\infty$ alive. The restart variant below keeps $i \in [0, 2]$ at `inner`, and a narrowing pass after it gives $i \in [3, 3]$ at exit.

## Correctness

There are three claims; the full proofs are in the proof file.

1. **WTO builds a weak topological ordering of $V_r$.** VISIT finds the strongly connected parts of the graph as Tarjan's algorithm does, and it lists them in a topological order, because each part goes to the front of the list when it is finished. A part with a cycle becomes a component whose head is the first vertex of the part that the search reached, and whose body is, by induction on the number of vertices, a WTO of the part without its head. The edge condition follows by cases: an edge between two parts goes forward; an edge to the head of a part goes backward to a head that contains its source; any other edge inside a part is an edge of the smaller graph.
2. **Every cycle passes through a head.** Take a cycle and its last vertex $u$ in the order. The next vertex $v$ on the cycle has $v \preceq u$, so the edge condition puts $v$ in $\omega(u)$: $v$ is a head. So the vertices without the heads form a graph with no cycle, and the heads are enough as widening points.
3. **ITERATE stops with $F_v(x) \sqsubseteq x[v]$ at every vertex**, if each $F_v$ is monotone and $\nabla$ is a widening. Every assignment makes a value larger or keeps it, so the inputs of each head form an increasing chain over the whole run, and the widening makes the number of strict changes at each head finite. When the outer loop of a component ends, its head passes the test of line L28, and the edge condition shows that no value it depends on changes later. With sound $F_v$, the [abstract domain](/abstract-domain/) claim then gives a sound result.

## Complexity

**Building the WTO.** A unit step is one look at an edge or one push or pop. VISIT$(v)$ looks at each successor of $v$ once. A vertex $v$ is visited once at the top level, and once more by COMPONENT of each component that contains $v$ and has a head other than $v$. COMPONENT$(v)$ looks at the successors of $v$ once more. So the successor list of $v$ is read exactly $1 + |\omega(v)|$ times, and the total time is

$$ \sum_{v \in V_r} \bigl(1 + |\omega(v)|\bigr)\bigl(1 + \mathit{outdeg}(v)\bigr) \le (k + 1)(n + m). $$

With no cycle, $k = 0$ and the time is $\Theta(n + m)$. In the worst case $k = n - 1$: on the chain $0 \rightleftarrows 1 \rightleftarrows \cdots \rightleftarrows n-1$ the WTO is $(0\ (1\ (2 \cdots (n-2\ n-1) \cdots)))$, vertex $i$ is read $i + 2$ times for $i \le n - 2$, and the total is $\Theta(n^2)$, which is $\Theta(n(n + m))$ for this graph. The stack, the DFN array and the output take $\Theta(n)$ space.

**Iterating.** ITERATE evaluates $F_v$ once per assignment and once per stop test. The number of passes over a component depends on the domain and the widening, not on the graph alone. With the interval widening on $v$ names, a head can change at most $2v + 1$ times over the whole run, and each change starts at most one more pass over its body.

## Properties

- **Deterministic.** The WTO depends on the root and on the order of the successor lists. Another order can give other heads.
- **Not the fewest heads.** Finding the fewest vertices that cut every cycle is the feedback vertex set problem, which is NP-hard. On the graph $0 \to 1$, $1 \rightleftarrows 2$, $2 \rightleftarrows 3$ the WTO is $0\ (1\ (2\ 3))$ with heads 1 and 2, but vertex 2 alone cuts both cycles.
- **Heads on reducible graphs.** On a [reducible flow graph](/reducible-flow-graph/) each head is a loop header: the head is the entry of its part, so it dominates the part, and the edge into it from inside the part is a back edge. The components then follow the loops of a [loop nesting forest](/loop-nesting-forest/).
- **Irreducible graphs work too.** A cycle with two entries, such as $0 \to 1$, $0 \to 2$, $1 \rightleftarrows 2$, gives `0 (1 2)`. The edge $0 \to 2$ enters the component at a vertex that is not the head; it is a forward edge, and the iteration stays correct.
- **Order of the dataflow pages.** The same WTO serves an analysis in the dual order of Kildall that the [worklist algorithm](/worklist-dataflow-algorithm/) uses; only the join, the stop test and the direction of the widening are turned around.

## Variants and improvements

- **The iterative strategy.** Bourdoncle also gives a strategy that runs through the whole component of the outermost head, in the flattened order, until that head is stable, without stabilizing inner components first. It is simpler, but the recursive strategy usually needs fewer evaluations, and it lets the analyzer test only the head.
- **Restart an inner loop on entry.** Replace line L24 by $x[h] \leftarrow F_h(x)$, so that each new pass of an outer loop starts the inner head from its new entry value. In the example, step 10 then keeps $i \in [0, 2]$, and `body` gets $i \in [1, 2]$ and $j \in [0, 1]$. Values can then go down, so the termination proof above no longer applies; the iteration still stops if the widening makes every widened sequence stop, increasing or not, which the interval widening does.
- **A narrowing pass.** After ITERATE, run it again with $\Delta$ in place of $\nabla$ at lines L24 and L29, and with the test of line L28 replaced by "no change".
- **A worklist on top of the WTO.** Use the WTO order as the priority of a worklist, and put a vertex back only when an input changed. This skips blocks whose inputs did not change.
- **Plain topological order.** On a graph without cycles the WTO is a [topological sort](/topological-sort/). It is the reverse postorder of the [depth-first search](/depth-first-orders/) from the root, because each vertex goes to the front of the list when its visit ends.

## When to use it

Use a WTO in an abstract interpreter over a domain of infinite height, such as [intervals](/interval-domain/), [octagons](/octagon-domain/) or [polyhedra](/polyhedra-domain/), where the widening points and the order of iteration decide both termination and precision. It also suits a [worklist](/worklist-dataflow-algorithm/) dataflow solver on a lattice of finite height, but there a reverse postorder is simpler and almost as fast. Widening at every block also stops, but it loses much more precision; widening at the targets of the back edges of a depth-first search also cuts every cycle, but it gives no order in which to stabilize nested loops.

## Pitfalls

- **A strict test in line L9.** With `min < head` in place of `min ≤ head`, the flag $\mathit{loop}$ stays false at the root of every part, because every cycle through the root returns exactly $\mathit{DFN}[v]$. Then no loop gets a component. ITERATE passes over each loop once, and the result is not a post-fixed point, so it is unsound. Line L9 must use $\le$.
- **No reset in line L13.** If the vertices taken off the stack keep their old DFN, COMPONENT in line L14 sees them as visited and returns an empty body, and the loop body is lost. Line L13 must set their DFN to 0.
- **Widening at every vertex in line L22.** Writing $x[v] \leftarrow x[v] \nabla F_v(x)$ for every vertex still stops, but it loses bounds that a guard has just set. In the example, `init` has $i \in [0, 0]$ after the first pass, and in the second pass $F$ gives $[0, 2]$, so the widening sets $i \in [0, +\infty]$ and the guard `i < 3` is lost. Line L22 must assign, and only lines L24 and L29 widen.
- **Widening on re-entry in line L24.** The old value of an inner head comes from the last pass of the outer loop. Widening with it can jump over a bound that the outer loop has just changed, as in step 10 of the example. Use the restart variant with a widening that stops on every sequence, or recover the bound with narrowing.
- **Deep recursion.** VISIT can recurse $n$ levels deep, and ITERATE $k$ levels deep. The Python code keeps its own stack.

## Implementations

## History

Cousot and Cousot (1977) showed that an upward iteration with widening stops when the widening is applied at a set of points that cuts every loop. François Bourdoncle (1993) asked which points and which order to use. He defined hierarchical and weak topological orderings, built them by applying Tarjan's 1972 algorithm for strongly connected components again inside each part, and gave the iterative and recursive strategies. He proved that the heads of a WTO are an admissible set of widening points and that, in the recursive strategy, stability of a component can be detected at its head alone. The method is the standard iteration order of abstract interpreters for imperative programs.

## References
