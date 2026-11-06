---
tag: 5TVZ6C
kind: data-structure
slug: graph-structured-stack
name: Graph-structured stack
aliases:
- GSS
area: automata-and-parsing/context-free-parsing
level: advanced
summary: Shared-stack representation of all parallel LR parser states in generalized LR parsing.
model: word-ram
complexity:
  vars: {N: the number of nodes, E: the number of edges, W: the number of partial paths that one pop visits}
  time: {node: O(1), push: O(1), pop: O(W + 1)}
  space: {extra: O(N + E)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [stack, directed-acyclic-graph, lr-parsing]
see_also: [glr-parsing, gll-parsing, shared-packed-parse-forest, persistent-stack, parent-pointer-tree, pushdown-automaton, lr-item, hash-consing]
sources:
  - paper: url:https://aclanthology.org/J87-1004/
    title: Masaru Tomita, An efficient augmented-context-free parsing algorithm, Computational Linguistics 13(1-2) (1987)
    locator: pp. 31 to 46 (the graph-structured stack, its splitting and combining of stack tops, and local ambiguity packing)
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 11.1, Generalized LR Parsing (11.1.1, p. 382; 11.1.2 Necessary Optimizations, p. 383; 11.1.3 Hidden Left Recursion and Loops, p. 387)
  - paper: doi:10.1007/978-3-662-21545-6_18
    title: Bernard Lang, Deterministic techniques for efficient non-deterministic parsers, Automata, Languages and Programming (ICALP 1974), LNCS 14
    locator: pp. 255 to 269
  - paper: doi:10.1145/1146809.1146810
    title: Elizabeth Scott and Adrian Johnstone, Right nulled GLR parsers, ACM Transactions on Programming Languages and Systems 28(4) (2006)
    locator: pp. 577 to 618
  - paper: doi:10.1016/j.entcs.2010.08.041
    title: Elizabeth Scott and Adrian Johnstone, GLL parsing, Electronic Notes in Theoretical Computer Science 253(7) (2010)
    locator: pp. 177 to 189
---

A graph-structured stack (GSS) stores many [stacks](/stack/) of a parser as one directed graph, so that stacks with a common top or a common bottom part share one copy of it. Each node is a stack cell, identified by a parser state and the number of input symbols read when the cell was pushed, and each edge points from a cell to the cell directly below it. Every path from a node down to the root is one stack. It is the central data structure of [GLR parsing](/glr-parsing/), where it keeps the number of cells polynomial in the input length although the number of stacks can grow exponentially.

## In plain words

A parser for an ambiguous grammar must sometimes follow several choices at once. Each choice needs its own stack, and copying stacks is expensive. Most of the stacks are the same at the bottom, and many of them also end with the same top. A graph-structured stack keeps each different cell only once. A cell points down to all the cells that can be below it. To read one stack, start at a top cell and follow the pointers down to the bottom. When two branches of the parser come back to the same state after reading the same input, their tops become one cell, and from then on the parser does the work for both branches only once.

## The abstract type

We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol, $n$ the input length, and the grammar size $|G| = \sum_{A \to \alpha} (|\alpha| + 1)$.

A **cell** is a pair $(s, j)$ of a state $s$ and a **level** $j \ge 0$, the number of input symbols read when the cell was pushed. A **stack** is a sequence of cells $c_0 c_1 \cdots c_k$, read from the bottom $c_0$ to the top $c_k$, where $c_0$ is the root cell $(q_0, 0)$ and the levels do not decrease from bottom to top. Each step $c_{i-1} c_i$ also has a label, for example the parse tree of the grammar symbol that the cell $c_i$ stands for. The structure holds a set $\mathcal{S}$ of stacks with these operations:

- `new(q0)`: $\mathcal{S} = \{(q_0, 0)\}$, one stack with only the root cell.
- `push(s, j, x)`: put the cell $(s, j)$ on every stack of $\mathcal{S}$ whose top is the cell $x$, with $\mathrm{level}(x) \le j$. Return the node of $(s, j)$, and tell whether the node and the edge are new.
- `pop(u, m, e)`: for every stack whose top is $u$, remove the top $m$ cells, and return the new top and the labels of the removed steps. If $e$ is an edge, keep only the stacks that contain the step $e$.
- `tops(j)`: the cells of level $j$ that are tops of stacks.

The set $\mathcal{S}$ is always **closed under splicing**: if two stacks $\sigma = \sigma_1 c \sigma_2$ and $\tau = \tau_1 c \tau_2$ contain the same cell $c$, then $\tau_1 c \sigma_2$ is also in $\mathcal{S}$. This is the property that makes sharing possible. A parser state is a function of the input read and the stack, so a branch that reaches the cell $c$ continues in the same way, whatever lies below $c$. A push therefore adds the new cell to every stack with top $x$, including the stacks that the push itself creates when $x$ lies above the new cell, and then closes the set under splicing.

## Representation

The structure is a directed graph. There is one node for each cell, and a hash table maps the key $(s, j)$ to the node, so that a cell is never stored twice. Each node $v$ has a table $\mathrm{OUT}[v]$ that maps each node $x$ directly below $v$ to the label of the edge $v \to x$. A list for each level gives the nodes of that level in the order they were made. The root is the node of $(q_0, 0)$.

The stacks of $\mathcal{S}$ are exactly the paths that start at a node, follow edges and end at the root, read in reverse. A node with several outgoing edges is a cell with several cells below it, where the stacks split. A node with several incoming edges is a cell with several cells on top of it.

**Invariants.**

1. The keys are unique: no two nodes have the same pair $(s, j)$.
2. No edge goes up a level: for every edge $v \to x$, $\mathrm{level}(x) \le \mathrm{level}(v)$.
3. Every node has a path to the root.

Edges inside one level are possible, and they can form cycles. In GLR parsing they come from reductions by empty productions. For the grammar $S \to A S \mid b$, $A \to \varepsilon$, the state $q_1$ reached from $q_0$ on $A$ satisfies $\mathrm{GOTO}(q_1, A) = q_1$, so the reduction $A \to \varepsilon$ on the node $(q_1, 0)$ adds the edge $(q_1, 0) \to (q_1, 0)$. So the graph is acyclic only between levels, and $\mathcal{S}$ can be infinite. Every operation below works on paths of bounded length and is correct with cycles.

## Operations

```pseudo id=main
PUSH(G, s, j, x, t)                   ▷ put the cell (s, j) on every stack with top x, edge label t
L1  require LEVEL(x) ≤ j
L2  (v, created) ← NODE(G, s, j)
L3  new ← ADD-EDGE(G, v, x, t)
L4  return (v, created, new)

NODE(G, s, j)
L5  if INDEX has no key (s, j) then make a node v with OUT[v] ← ∅, set INDEX[(s, j)] ← v, append v to the list of level j, and return (v, true)
L6  return (INDEX[(s, j)], false)

ADD-EDGE(G, v, x, t)                  ▷ LEVEL(x) ≤ LEVEL(v)
L7  if x ∈ OUT[v] then return false   ▷ the edge exists; keep its first label
L8  OUT[v][x] ← t; return true

POP(G, u, m, e)                       ▷ e = y₀ → x₀ is an edge, or none
L9  R ← ∅; floor ← LEVEL(y₀) if e ≠ none else 0; T ← [(u, 0, e = none, ())]
L10 while T ≠ ∅ do
L11     remove the last entry (y, d, used, labels) from T
L12     if d = m then (if used then add (y, labels in reverse) to R); continue
L13     if not used and LEVEL(y) < floor then continue   ▷ e is out of reach from y
L14     for each edge y → x with label t do append (x, d + 1, used or (y → x) = e, labels + t) to T
L15 return R
```

PUSH is the only operation that changes the graph. It finds or makes the node of the new cell, and adds the edge to $x$ if it is not there. When the edge is already there, the label stays. A parser that needs all labels, for example all parse trees, keeps a set of labels on each edge, which is a node of a [shared packed parse forest](/shared-packed-parse-forest/).

POP lists the paths of $m$ edges that start at $u$, one at a time, with an explicit stack $T$ instead of recursion. A path is a walk: with a cycle inside a level, it can use the same edge more than once. Each path gives one end node and one sequence of labels, bottom first. The same end node can come from different paths with different labels. In a parser, this is a local ambiguity: two ways to read the same part of the input as the same symbol.

The argument $e$ serves the parser that adds an edge $v \to x$ to an existing node $v$ after some reductions have already popped through $v$. The paths that use the new edge are new stacks, and only these must be reduced again. Line L13 cuts a branch of the search as soon as it can no longer reach $e$: the path has not used $e$, and it is below the level of $e$, where by invariant 2 no edge leads back up.

## Example

Take the grammar $S \to S S \mid a$, the input $a a a$, and the LR(0) states $q_0, \ldots, q_3$ of the [GLR parsing](/glr-parsing/) page: $q_1 = \mathrm{GOTO}(q_0, S)$, $q_2 = \mathrm{GOTO}(q, a)$ for every state $q$ with an item $S \to \bullet a$, and $q_3 = \mathrm{GOTO}(q_1, S) = \mathrm{GOTO}(q_3, S)$. After the parser reads the whole input, the GSS has 9 nodes and 11 edges. The label of each edge is the grammar symbol of the upper cell.

| Node | Edges to (label) |
|---|---|
| $(q_0, 0)$ | none, the root |
| $(q_2, 1)$ | $(q_0, 0)$ ($a$) |
| $(q_1, 1)$ | $(q_0, 0)$ ($S$) |
| $(q_2, 2)$ | $(q_1, 1)$ ($a$) |
| $(q_3, 2)$ | $(q_1, 1)$ ($S$) |
| $(q_1, 2)$ | $(q_0, 0)$ ($S$) |
| $(q_2, 3)$ | $(q_3, 2)$ ($a$), $(q_1, 2)$ ($a$) |
| $(q_3, 3)$ | $(q_1, 2)$ ($S$), $(q_3, 2)$ ($S$), $(q_1, 1)$ ($S$) |
| $(q_1, 3)$ | $(q_0, 0)$ ($S$) |

The node $(q_2, 3)$ is the top of two stacks, $(q_0,0)\,(q_1,1)\,(q_3,2)\,(q_2,3)$ and $(q_0,0)\,(q_1,2)\,(q_2,3)$. The parser shifted the last $a$ once for both of them, because their tops after the shift are the same cell. The node $(q_3, 3)$ is the top of three stacks:

$$(q_0,0)\,(q_1,1)\,(q_3,2)\,(q_3,3), \qquad (q_0,0)\,(q_1,1)\,(q_3,3), \qquad (q_0,0)\,(q_1,2)\,(q_3,3).$$

The call $\mathrm{POP}((q_3, 3), 2, \text{none})$ for the reduction $S \to S S$ returns three paths. Two of them end at the root: the path through $(q_1, 2)$, where the first $S$ covers $a a$, and the path through $(q_1, 1)$, where the second $S$ covers $a a$. These are the parses $(a a)\, a$ and $a\, (a a)$, and both give the same new edge $(q_1, 3) \to (q_0, 0)$: the GSS stores the ambiguity once. The third path, $(q_3, 3) \to (q_3, 2) \to (q_1, 1)$, ends at $(q_1, 1)$. With $e = (q_3, 3) \to (q_3, 2)$, POP returns only this third path.

## Correctness

Let $\mathrm{Paths}(G)$ be the set of paths from a node to the root, read from the root up. The claim is that, if the graph is changed only by PUSH, then after every operation the invariants hold and $\mathrm{Paths}(G) = \mathcal{S}$, the abstract set of stacks.

PUSH keeps invariant 1 because NODE looks the key up before it makes a node, invariant 2 because of line L1, and invariant 3 because the new or old node $v$ gets an edge to $x$, which has a path to the root. For the set of stacks, $\mathrm{Paths}(G)$ is closed under splicing, because a path from $\tau_1$ up to $c$ joined with a path from $c$ up through $\sigma_2$ is a path. It contains the old stacks and $\sigma v$ for each of its own paths $\sigma$ that end at $x$. So it contains the new $\mathcal{S}$, the least such set. Conversely, take a path that uses the new edge, and split it at its last use, as $\alpha\, v\, \beta$ with $\alpha$ ending at $x$. By induction on the number of uses, $\alpha \in \mathcal{S}$, so $\alpha v \in \mathcal{S}$. If $\beta$ is not empty, $v$ is an old node, and by invariant 3 it has an old path $\rho$ to the root. Then $\rho \beta$ is an old stack, and splicing it with $\alpha v$ at $v$ gives $\alpha v \beta$.

POP searches the tree of all walks of at most $m$ edges from $u$, and visits each walk once. Line L13 removes a walk only when it has not used $e$ and stands at a level below the source of $e$. By invariant 2, every extension of the walk stays at that level or lower, so it never uses $e$. So POP returns exactly the walks of $m$ edges from $u$ that use $e$, or all of them when $e$ is none. Removing the top $m$ cells of the stacks with top $u$ leaves exactly the stacks whose top is the end of such a walk. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **NODE, ADD-EDGE and PUSH.** $O(1)$ expected time, with hash tables for the keys and for the out-edges of each node. With a table indexed by the state for each level, NODE takes $O(1)$ time in the worst case.
- **POP.** $O(W + 1)$ time, where $W$ is the number of partial walks that the search visits, plus the time to build the label sequences. Without $e$, $W$ is at most the number of walks of at most $m$ edges from $u$. A node has at most $N$ out-edges, so $W \le 1 + N + \cdots + N^m$. In a GLR parser for a fixed grammar, $m$ is at most the length $p$ of the longest right side, so one pop takes $O(n^p)$ time.
- **tops(j).** $O(1)$ time per node returned.
- **Space.** $O(N + E)$ words. In a GLR parser, each level has at most one node for each state, so $N \le |Q|\,(n + 1)$ for the set $Q$ of LR(0) states, and $E \le N^2$. For a fixed grammar, the GSS has $O(n)$ nodes and $O(n^2)$ edges, while the number of stacks it represents can grow exponentially with $n$ for an ambiguous grammar, or be infinite if there are cycles.

## Variants

- **Symbol nodes.** Some descriptions, among them Tomita's, put a separate node for the grammar symbol on each edge, between two state nodes. That node holds the parse forest of the symbol. This is the same as a label on the edge.
- **Tree of stacks.** If equal tops are never merged, the graph is a tree of cells with pointers to the parent, a [parent-pointer tree](/parent-pointer-tree/), also used for [persistent stacks](/persistent-stack/). Each branch then repeats the work of the others, and the size can grow exponentially.
- **Reductions from the new edge.** Right nulled GLR (RNGLR) parsers of Scott and Johnstone start the extra reductions directly at the new edge, and use reductions that skip a nullable end of the right side. This removes the need to search for paths through an edge.
- **Binarized paths.** Binary right nulled GLR (BRNGLR) adds nodes so that each reduction pops at most two edges at a time. This bounds the pop time and gives $O(n^3)$ parsing for every grammar.
- **GLL parsing.** [GLL parsing](/gll-parsing/) uses a GSS for the return stack of a recursive descent parser. A node is a pair of a grammar position and an input position, and a set of finished pops lets edges that come later reuse the results.

## When to use it

Use a GSS when you run many copies of one stack machine on the same input in lockstep, and their stacks often meet in the same state at the same input position: [GLR parsing](/glr-parsing/), GLL parsing, and the simulation of a nondeterministic [pushdown automaton](/pushdown-automaton/). The merging of equal tops is what makes the number of cells polynomial. If the copies never meet, a tree of stacks is simpler. If you need only one stack, use an ordinary [stack](/stack/).

## Pitfalls

- **Merging tops of different levels.** Two tops can share a node only if they have the same state and the same level. Cells with the same state after different amounts of input stand for different parts of the input, and merging them mixes up the parses.
- **Missing the stacks of a new edge.** A reduction that ran before an edge was added to its top node does not see the stacks through that edge. Tomita's original algorithm has this fault on some grammars with empty productions. The parser must run the reductions again on the paths that use the new edge, which is what the argument $e$ of POP is for.
- **Assuming a DAG.** With empty productions, edges inside one level can form cycles, as in the example with $S \to A S \mid b$. A search that follows edges until it reaches the root never ends. POP must stop at $m$ edges.
- **Duplicate edges for an ambiguity.** POP can return the same end node more than once. The parser must add the resulting edge once, and pack the different labels into it, or the GSS and the work grow with the number of parses.
- **Recursion depth.** A GSS for an input of length $n$ can have paths of length $n$. Search with an explicit stack, as POP does.

## Implementations

## History

Lang described in 1974 how to simulate a nondeterministic pushdown parser by dynamic programming over shared stack configurations. Tomita introduced the graph-structured stack for GLR parsing of natural language in the mid-1980s, in a 1986 book and in a 1987 journal paper, with the merging of equal tops and the packing of local ambiguities. Later work fixed the treatment of empty productions, among others Nozohoor-Farshi in 1991 and Scott and Johnstone with right nulled GLR in 2006, and Scott and Johnstone used the GSS again for GLL parsing in 2010.

## References
