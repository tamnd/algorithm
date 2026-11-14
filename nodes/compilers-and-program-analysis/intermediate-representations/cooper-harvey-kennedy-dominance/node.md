---
tag: 0T0R8F
kind: algorithm
slug: cooper-harvey-kennedy-dominance
name: Cooper-Harvey-Kennedy dominance algorithm
aliases:
- simple fast dominance algorithm
- iterative dominator algorithm
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: Computes immediate dominators by iterating over the nodes in reverse postorder and intersecting paths in the partial dominator tree.
solves: [dominators-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, d: the largest number of retreating edges on a simple path from the root (for the depth-first order of line L1)}
  time: {worst: O((d + 2) n (n + m)), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [dominators-problem, depth-first-orders, control-flow-graph]
see_also: [dominator-tree, lengauer-tarjan-algorithm, post-dominance, dominance-frontier-computation, reducible-flow-graph, kam-ullman-iteration-bound, lowest-common-ancestor, static-single-assignment-form]
sources:
  - url: "https://hdl.handle.net/1911/96345"
    title: Keith D. Cooper, Timothy J. Harvey and Ken Kennedy, A simple, fast dominance algorithm, technical report, Department of Computer Science, Rice University
    locator: the iterative algorithm with the doms array and the intersect routine (Figure 3), the pass bound taken from Kam and Ullman, the timing study against Lengauer-Tarjan, and the dominance frontier algorithm built on the same tree
  - paper: "Loukas Georgiadis, Robert E. Tarjan and Renato F. Werneck, Finding dominators in practice, Journal of Graph Algorithms and Applications 10(1) (2006), 69-94"
    locator: the iterative algorithm of Cooper, Harvey and Kennedy among the implementations compared, its O(mn^2) worst-case bound, and the graph families on which it is slow
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 9.6.1 (dominators, found as a data-flow problem by iteration over sets) and Section 9.6.2 (depth-first ordering)
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 9 (Data-Flow Analysis), dominance, the iterative computation and the dominator tree
  - book: isbn:1558603204
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 7 (Control-Flow Analysis), the computation of dominators and immediate dominators
---

The Cooper-Harvey-Kennedy algorithm solves the [dominators problem](/dominators-problem/) on a flow graph, usually a [control flow graph](/control-flow-graph/). It keeps one number per node, the current guess of its immediate dominator, so the guesses form a tree. In each pass it visits the nodes in reverse postorder and sets the guess of a node to the nearest common ancestor, in that tree, of its predecessors. Two fingers that climb the tree by postorder numbers find this ancestor. It repeats passes until one pass changes nothing. On a [reducible flow graph](/reducible-flow-graph/) this takes at most two passes. The name "iterative dominator algorithm" also covers older methods, such as the iteration over sets of dominators in the style of Allen and Cocke; this page is the version of Cooper, Harvey and Kennedy (2001) with the intersect step.

## In plain words

Every block of a program has guards: blocks that each run must pass through before it gets there. The nearest guard is the immediate dominator. The algorithm keeps one guess per block, a pointer to its nearest guard, so the guesses form a tree. It visits the blocks so that a block usually comes after the blocks that lead into it. For each block, it finds where the paths up the tree from the blocks that lead into it meet. Two fingers climb the tree, always moving the deeper one, until they touch. The meeting point is the new guess. A loop can make a guess wrong at first, so the algorithm sweeps again until a sweep changes nothing. On most real programs, two sweeps are enough.

## The problem

The input is a directed graph $G$ with vertices $0, \ldots, n - 1$ and $m$ edges, given as a list of pairs $(a, b)$ meaning $a \to b$, and a start vertex $r$. Self-loops and parallel edges are allowed. A vertex $x$ *dominates* $v$ if every path from $r$ to $v$ contains $x$; $D(v)$ is the set of dominators of $v$. The immediate dominator $\mathrm{idom}(v)$ of $v \ne r$ is the strict dominator of $v$ that every other strict dominator of $v$ dominates. The output is $\mathrm{idom}(v)$ for every vertex $v \ne r$ that $r$ reaches, and nothing (here $-1$) for $r$ and for the unreachable vertices.

The algorithm numbers the reachable vertices in postorder of a depth-first search from $r$, so $po(r)$ is the largest number, and visits them in *reverse postorder*, from the largest number down. An edge $(u, v)$ is *retreating* if $po(v) \ge po(u)$, that is, if $v$ does not come after $u$ in the visit order. Every other edge goes forward in that order.

## The algorithm

The array $doms$ holds the guesses. A vertex is *defined* once it has a guess. Following $doms$ from a defined vertex $y$ gives a path $y, doms[y], doms[doms[y]], \ldots$ that ends at $r$; call its vertices the *chain* of $y$. The proof file shows that $doms[y]$ always has a larger postorder number than $y$, so the defined vertices form a tree rooted at $r$, and the chain of $y$ is the set of its ancestors in this tree. The intended result is that the chain of $y$ is exactly $D(y)$.

```pseudo id=main
CHK-DOMINATORS(G, r)
L1  number the vertices that r reaches in postorder of a DFS from r: po[v]
L2  for all vertices b do doms[b] <- Undefined
L3  doms[r] <- r
L4  changed <- true
L5  while changed do
L6      changed <- false
L7      for each vertex b != r that r reaches, in reverse postorder do
L8          new_idom <- the first predecessor p of b with doms[p] != Undefined
L9          for each other predecessor p of b do
L10             if doms[p] != Undefined then new_idom <- INTERSECT(p, new_idom)
L11         if doms[b] != new_idom then
L12             doms[b] <- new_idom; changed <- true
L13 return doms

INTERSECT(b1, b2)
L14 finger1 <- b1; finger2 <- b2
L15 while finger1 != finger2 do
L16     while po[finger1] < po[finger2] do finger1 <- doms[finger1]
L17     while po[finger2] < po[finger1] do finger2 <- doms[finger2]
L18 return finger1
```

Line L8 always finds a predecessor: the parent of $b$ in the DFS tree comes before $b$ in reverse postorder, so it is defined. INTERSECT walks the two fingers up the tree of guesses. The finger with the smaller postorder number is the deeper one in that tree, and it moves up until it is no longer below the other. When they meet, they are at the nearest common ancestor of $b_1$ and $b_2$, whose chain is the intersection of the two chains. So lines L8 to L10 compute the vertex whose chain is the intersection of the chains of all defined predecessors, and line L12 makes the chain of $b$ equal to $\{b\}$ plus that intersection. This is the classic set equation $D(b) = \{b\} \cup \bigcap_{p} D(p)$, with each set stored as a path in one tree instead of as a bit vector.

In the implementation, line L1 is an iterative DFS, the predecessors with $doms[p] = $ Undefined are filtered out before line L8, and the vertices that $r$ does not reach never get a postorder number and stay Undefined. The function `cfg_idom` runs the algorithm on the blocks of a toy IR program and returns a map from each block to its immediate dominator.

## Example

Take the flow graph with vertices $r, a, b, c, d, e$, start $r$, and the edges

$$r \to a,\; r \to b,\; a \to c,\; b \to d,\; b \to e,\; c \to d,\; d \to c,\; d \to e,\; e \to d.$$

The cycle $c \to d \to c$ can be entered at $c$ (from $a$) and at $d$ (from $b$), so no vertex of the cycle dominates the other, and the graph is not reducible. Every vertex other than $r$ has $\mathrm{idom} = r$: $c$ is reached by $r, a, c$ and by $r, b, d, c$, and $d$ by $r, b, d$ and by $r, a, c, d$.

With successors tried in the order listed, the DFS from $r$ goes $r, a, c, d, e$, backs up, and then visits $b$. The postorder is $e, d, c, a, b, r$ with $po = 0, \ldots, 5$, and the reverse postorder is $r, b, a, c, d, e$. The retreating edges are $d \to c$ and $e \to d$.

| pass | vertex | defined predecessors | INTERSECT steps | $doms$ |
|---|---|---|---|---|
| 1 | $b$ | $r$ | none | $r$ |
| 1 | $a$ | $r$ | none | $r$ |
| 1 | $c$ | $a$ ($d$ is not yet defined) | none | $a$ |
| 1 | $d$ | $b, c$ | $c \to a \to r$, then $b \to r$ | $r$ |
| 1 | $e$ | $b, d$ | $d \to r$, then $b \to r$ | $r$ |
| 2 | $c$ | $a, d$ | $d \to r$, then $a \to r$ | $r$ (changed) |
| 3 | all | | | no change |

After pass 1, the guess for $c$ is wrong: when $c$ was visited, its predecessor $d$ had no guess yet, because the edge $d \to c$ is retreating. Pass 2 sees $d$ and moves $c$ up to $r$. Pass 3 changes nothing, so the algorithm stops after 3 passes with $\mathrm{idom}(v) = r$ for all $v \ne r$. Here the largest number of retreating edges on a simple path from $r$ is $d = 2$, on the path $r, b, e, d, c$, and the proved bound is $d + 2 = 4$ passes.

On the reducible control flow graph of the odd-sum program on the [control flow graph](/control-flow-graph/) page, with edges $B1 \to B2$, $B2 \to B3$, $B2 \to B6$, $B3 \to B4$, $B3 \to B5$, $B4 \to B5$, $B5 \to B2$, pass 1 already gives the answer $B2 \mapsto B1$, $B3 \mapsto B2$, $B6 \mapsto B2$, $B4 \mapsto B3$, $B5 \mapsto B3$, and pass 2 confirms it. On the 9-vertex example of the [Lengauer-Tarjan algorithm](/lengauer-tarjan-algorithm/), which is not reducible, the algorithm also stops after 2 passes, with the same $idom = [-, 0, 1, 2, 2, 4, 2, 3, 7]$.

## Correctness

The full proof is in the proof file. Its steps:

1. **The guesses form a tree.** When $b$ gets a guess, the guess is on the chain of the DFS parent of $b$, so it is a proper DFS ancestor of $b$ with a larger postorder number. Hence every chain climbs strictly in postorder and ends at $r$, and a new guess for $b$ is never inside the subtree of $b$.
2. **INTERSECT.** A finger never passes the nearest common ancestor $c$ of $b_1$ and $b_2$: a finger at $c$ has a postorder number at least that of the other finger, so it does not move. Each move raises a postorder number, so the loops stop, and they stop at $c$.
3. **Soundness.** At all times $D(y) \subseteq chain(y)$ for every defined $y$. A strict dominator of $b$ dominates every predecessor of $b$, and a change at $b$ also keeps the property for the vertices below $b$ in the tree, because they are DFS descendants of $b$.
4. **Fixed point.** When a pass changes nothing, $chain(b) = \{b\} \cup \bigcap_p chain(p)$ for all $b \ne r$. Walking along a path from $r$ that avoids a vertex $x$ shows that $x$ is in no chain on the path, so $chain(y) \subseteq D(y)$. With step 3, $chain(y) = D(y)$, and then $doms[y] = \mathrm{idom}(y)$.
5. **Termination.** The chains are always subsets of the sets of the plain set iteration run in the same order, and after pass $k$ those sets are inside the vertex set of every path from $r$ with at most $k - 1$ retreating edges. So after pass $d + 1$ every chain equals $D$, and pass $d + 2$ changes nothing.

## Complexity

**Proved.** Line L1 takes $\Theta(n + m)$ time. In one pass, each vertex is visited once and each edge causes at most one call of INTERSECT; each finger move raises a postorder number along one chain, so a call costs at most the sum of two chain lengths, at most $2n$. A pass costs $O(n + m n)$. The number of passes is at most $d + 2$, where $d$ is the largest number of retreating edges on a simple path from $r$ for the DFS of line L1. It is at most the loop connectedness of [Kam and Ullman](/kam-ullman-iteration-bound/), which counts retreating edges on all cycle-free paths, not only on those from $r$. Since $d \le n - 1$, the total is $O((d + 2)\, n (n + m))$, which is $O(n^2 (n + m))$ in the worst case. On a reducible graph every retreating edge $(t, h)$ is a back edge, so $h$ comes before $t$ on any path from $r$ to $t$, and a simple path from $r$ cannot use the edge. So $d = 0$, there are at most 2 passes, and the time is $O(n (n + m))$. Georgiadis, Tarjan and Werneck give graph families on which the iterative algorithm is slow. The extra space is $\Theta(n + m)$ for the predecessor lists and $\Theta(n)$ for $po$ and $doms$.

**Stated in the paper, not proved here.** The technical report quotes a bound of $d(G) + 3$ passes from the work of Kam and Ullman. The proof file proves $d + 2$ for this version, counting the final pass that changes nothing.

**Measured, not proved.** Cooper, Harvey and Kennedy timed their code against Lengauer-Tarjan on a 300 MHz Sun Ultra 10, on the control flow graphs of 169 Fortran routines (the largest with 744 blocks). Their algorithm was about 2.5 times faster on average. On random graphs with 30,000 nodes the two were about equal, and on a straight-line graph with 30,000 nodes theirs took about 0.04 s against about 0.4 s. In a seeded experiment for this page, over 20,000 random digraphs with 1 to 8 vertices and up to $3n$ edges, the largest pass count was 5, the count never exceeded $d + 2$, and it reached $d + 2$ on some graphs; no reducible graph needed more than 2 passes.

| graph | passes | time per pass |
|---|---|---|
| reducible | at most 2 | $O(n + m \cdot h)$, $h$ the height of the dominator tree |
| general | at most $d + 2$ | $O(n + m \cdot n)$ |
| a tree, a path, a star | 2 | $\Theta(n + m)$ |

## Properties

- **Deterministic.** The DFS order depends on the order of the successor lists. The number of passes depends on that order; the result does not.
- **Non-recursive.** The DFS of line L1 uses an explicit stack, and INTERSECT is two loops, so long paths do not overflow the call stack.
- **The tree is the output.** The $doms$ array is the [dominator tree](/dominator-tree/) as a parent array; no separate sets are kept.
- **Offline.** The whole graph is needed. After an edge change, the old $doms$ is not in general a valid starting point.
- **Guesses are never too high.** A guess can be too deep, as for $c$ in the example, but the chain of every vertex always contains all its dominators. On a reducible graph each guess is final as soon as it is first set.

## Variants and improvements

- **Iteration over sets.** The older iterative method keeps the set $D(v)$ for each vertex, as a bit vector, and repeats $D(b) \leftarrow \{b\} \cup \bigcap_p D(p)$ until no set changes. Its passes obey the same bound, but it costs $\Theta(n)$ bits per vertex and $\Theta(n)$ word operations per edge per pass. The dragon book presents dominators this way.
- **Post-dominators.** Run the algorithm on the reverse graph from the exit, with a reverse postorder of the reverse graph, to get [post-dominance](/post-dominance/).
- **Dominance frontiers.** The same report gives a short algorithm for [dominance frontiers](/dominance-frontier-computation/) that walks up the $doms$ tree from the predecessors of each join point, used to place phi-functions in [static single assignment form](/static-single-assignment-form/).
- **Semidominators plus nearest common ancestors.** A hybrid computes the semidominators of the [Lengauer-Tarjan algorithm](/lengauer-tarjan-algorithm/) and then finds each immediate dominator with one nearest common ancestor step in the partly built tree, in one pass and without iteration. Georgiadis, Tarjan and Werneck study it under the name SNCA.
- **Lengauer-Tarjan.** Near-linear in the worst case, with more code. Use it when the graphs are large or adversarial.

## When to use it

Use it for the control flow graphs of single procedures. They are small, and most of them are reducible, so the algorithm runs at most two passes over a graph of a few hundred blocks, and its short code is easy to get right. The same code also gives post-dominators and, with a few more lines, dominance frontiers. For very large graphs or for graphs built to be hard, such as heap graphs or generated code with deep irreducible nesting, prefer a near-linear algorithm such as Lengauer-Tarjan.

## Pitfalls

- **Comparing the wrong numbers.** INTERSECT must compare postorder numbers of the same DFS that gives the visit order. Comparing vertex labels or preorder numbers can make a finger skip the meeting point and climb past $r$.
- **Visiting in another order.** The proof needs every vertex to be visited after its DFS parent in pass 1, so that line L8 finds a defined predecessor whose chain is made of DFS ancestors. Reverse postorder does this. Plain vertex order does not.
- **Forgetting $doms[r] = r$.** Without line L3 the root is Undefined, line L8 finds nothing for the children of $r$, and INTERSECT has no stopping point.
- **Unreachable predecessors.** A predecessor that $r$ does not reach has no postorder number and stays Undefined; it must be skipped, not used in INTERSECT.
- **Post-dominators with the forward order.** On the reverse graph, the reverse postorder must come from a DFS of the reverse graph from the exit. The reverse of a forward postorder is not that order, and the pass bound fails.
- **Stopping after a fixed number of passes.** On a reducible graph pass 1 already gives the answer, but on an irreducible graph it can be wrong, as for $c$ in the example. Keep the test on `changed` unless the graph is known to be reducible.

## Implementations

## History

Prosser introduced dominators in 1959, and Lowry and Medlock used them in 1969 for loop optimization in the FORTRAN H compiler. Allen's 1970 paper on control flow analysis and the 1972 IBM report of Allen and Cocke (RC 3923) treated dominators with the other flow graph facts; Purdom and Moore gave another early method. Computing $D(v)$ by iteration over sets became the textbook method, and Kam and Ullman (1976) bounded the number of passes of such iterations by the loop connectedness. Lengauer and Tarjan (1979) gave the near-linear algorithm. Cooper, Harvey and Kennedy, in a Rice University report of 2001, kept the iteration but stored all the sets in one tree and intersected them with the two-finger walk; their timing study made the case that this simple algorithm is fast on real control flow graphs. Georgiadis, Tarjan and Werneck (2006) compared it with several versions of Lengauer-Tarjan on many graph families.

## References
