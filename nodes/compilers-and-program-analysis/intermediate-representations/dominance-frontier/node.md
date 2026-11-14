---
tag: BRKW75
kind: definition
slug: dominance-frontier
name: Dominance frontier
aliases:
- DF set
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: The nodes where the dominance of a node n ends, that is, nodes with a predecessor dominated by n that are not strictly dominated by n.
prereqs: [dominators-problem, dominator-tree, control-flow-graph]
see_also: [dominance-frontier-computation, static-single-assignment-form, phi-function, ssa-construction-problem, cytron-ssa-construction, control-dependence, post-dominance, pruned-ssa-form]
sources:
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: the definition of the dominance frontier, of DF of a set and of the iterated dominance frontier, the split into DF_local and DF_up, the theorem that the join points of a variable are its iterated dominance frontier, and control dependence as the dominance frontier of the reverse graph
  - paper: doi:10.1145/199448.199464
    title: Vugranam C. Sreedhar and Guang R. Gao, A linear time algorithm for placing phi-nodes, Proceedings of the 22nd ACM Symposium on Principles of Programming Languages (POPL), 1995, pages 62-73
    locator: DJ-graphs, and the iterated dominance frontier computed without the full dominance frontiers
  - url: "https://hdl.handle.net/1911/96345"
    title: Keith D. Cooper, Timothy J. Harvey and Ken Kennedy, A simple, fast dominance algorithm, technical report, Department of Computer Science, Rice University
    locator: the dominance frontier algorithm that walks up the dominator tree from each predecessor of a join node to its immediate dominator
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 19 (Static Single-Assignment Form), the dominance frontier criterion and the computation of DF
  - book: isbn:9783030805142
    title: Fabrice Rastello and Florent Bouchez Tichadou (editors), SSA-based Compiler Design, Springer, 2022
    locator: Chapter 3 (Standard Construction and Destruction Algorithms), join sets and dominance frontiers; Chapter 4 (Advanced Construction Algorithms for SSA), DJ-graphs and merge sets
---

The dominance frontier of a node $x$ in a flow graph is the set of nodes where the dominance of $x$ stops. A node $y$ is in it if $x$ dominates a predecessor of $y$ but does not strictly dominate $y$ itself. So $y$ can be reached from $x$, and also along a path that avoids $x$. If a variable is assigned in $x$, then $y$ is the first place where that value can meet a different value of the same variable. This is why the dominance frontier tells a compiler where to put [phi-functions](/phi-function/) when it builds [static single assignment form](/static-single-assignment-form/). Cytron, Ferrante, Rosen, Wegman and Zadeck defined it in 1991, together with the iterated dominance frontier and a fast way to compute both.

## Definition

### The frontier of one node

Let $G = (N, E, r)$ be a [control flow graph](/control-flow-graph/) with entry $r$, in which every node is reachable from $r$. A node $x$ *dominates* $y$, written $x \operatorname{dom} y$, if every path from $r$ to $y$ passes through $x$. It *strictly dominates* $y$ if also $x \ne y$. The *dominance frontier* of $x$ is

$$DF(x) = \{\, y \in N : \exists\, (p, y) \in E \text{ with } x \operatorname{dom} p \text{ and not } x \operatorname{sdom} y \,\}.$$

The node $x$ itself can be in $DF(x)$. This happens when $x$ dominates a predecessor of $x$, as a loop header does with its latch.

### The frontier of a set, and the iterated frontier

For a set $S$ of nodes, $DF(S) = \bigcup_{x \in S} DF(x)$. The *iterated dominance frontier* $DF^+(S)$ is the limit of

$$DF_1 = DF(S), \qquad DF_{i+1} = DF(S \cup DF_i).$$

The sequence grows and $N$ is finite, so it stops. $DF^+(S)$ is the smallest set $T$ with $DF(S \cup T) \subseteq T$. A worklist computes it: start with the nodes of $S$, and add the frontier of each node taken from the list, putting each new node on the list once.

### The main theorem

Let $S$ be the set of blocks that assign a variable $v$, plus the entry $r$, which holds the initial value. A block $y$ is a *join point* of $S$ if there are two non-empty paths that start at two different nodes of $S$, end at $y$, and have no other node in common. Cytron et al. proved that the join points of $S$ are exactly $DF^+(S)$. So minimal SSA form puts a phi-function for $v$ at each block of $DF^+(S)$, and at no other block. The [SSA construction problem](/ssa-construction-problem/) page proves this.

### Two other ways to write it

**By the dominator tree, bottom up.** Let $\mathrm{idom}(y)$ be the parent of $y$ in the [dominator tree](/dominator-tree/). Cytron et al. split $DF(x)$ into a local part and a part that comes up from the children:

$$DF_{\text{local}}(x) = \{\, y : (x, y) \in E,\ \mathrm{idom}(y) \ne x \,\},$$

$$DF_{\text{up}}(z) = \{\, y \in DF(z) : \mathrm{idom}(y) \ne \mathrm{idom}(z) \,\},$$

$$DF(x) = DF_{\text{local}}(x) \cup \bigcup_{z \,:\, \mathrm{idom}(z) = x} DF_{\text{up}}(z).$$

This gives an algorithm that visits the tree in postorder. See [dominance frontier computation](/dominance-frontier-computation/).

**By the edges.** Every node $d$ that strictly dominates $y$ also dominates every predecessor $p$ of $y$: a path from $r$ to $p$ that avoids $d$, followed by the edge $(p, y)$, would avoid $d$ too. So $\mathrm{idom}(y)$ is an ancestor of $p$ in the dominator tree, and the ancestors of $p$ form a chain. A node $x$ that dominates $p$ is on this chain. It strictly dominates $y$ if and only if it is $\mathrm{idom}(y)$ or above it. So

$$y \in DF(x) \iff \text{some predecessor } p \text{ of } y \text{ has } x \text{ on the tree path from } p \text{ up to } \mathrm{idom}(y), \text{ with } \mathrm{idom}(y) \text{ excluded}.$$

If $y = r$, no node strictly dominates $y$, and the whole path from $p$ up to $r$ counts. The walk of Cooper, Harvey and Kennedy uses this form. A node $y$ with one predecessor $p$ has $\mathrm{idom}(y) = p$, so the path is empty and $y$ is in no frontier. Only join nodes appear in dominance frontiers.

### Size

The sum $\sum_x |DF(x)|$ can be quadratic in the size of the graph. Take $n$ nested repeat-until loops. The nodes are headers $h_1, \ldots, h_n$, latches $l_1, \ldots, l_n$ and an exit $e$, with entry $h_1$. The edges are $h_i \to h_{i+1}$ for $i < n$, $h_n \to l_n$, the back edges $l_i \to h_i$, the loop exits $l_i \to l_{i-1}$ for $i > 1$, and $l_1 \to e$. The graph has $2n + 1$ nodes and $3n$ edges. Its dominator tree is the path $h_1, \ldots, h_n, l_n, l_{n-1}, \ldots, l_1, e$. For each $i$,

$$DF(h_i) = DF(l_i) = \{h_1, \ldots, h_i\},$$

because the back edge $l_j \to h_j$ leaves the region dominated by $h_i$ and $l_i$ for each $j \le i$. The total is $n(n + 1)$, which is $\Theta(N^2)$ for $N$ nodes. If a variable $v_i$ is assigned in $l_i$, then $DF^+(\{h_1, l_i\}) = \{h_1, \ldots, h_i\}$, and minimal SSA form has $n(n+1)/2$ phi-functions for these $n$ variables. Cytron et al. measured the frontiers of real programs and found their total size grew about linearly. Sreedhar and Gao showed that $DF^+(S)$ can be found in time linear in the size of the graph, without computing the frontiers at all.

### The reverse graph

On the reverse graph, with the exit as the entry, dominance becomes [post-dominance](/post-dominance/), and the dominance frontier becomes the *post-dominance frontier*. A block $y$ is [control dependent](/control-dependence/) on $x$ if and only if $x$ is in the post-dominance frontier of $y$. Cytron et al. build the control dependence graph this way.

## Examples and non-examples

### A loop with a branch inside

The program that adds the odd numbers below $n$, from the [control flow graph](/control-flow-graph/) page, has the edges B1 → B2, B2 → B3, B2 → B6, B3 → B4, B3 → B5, B4 → B5 and B5 → B2. The immediate dominators are B1 for B2, B2 for B3 and B6, and B3 for B4 and B5. The frontiers are:

| node | DF |
|---|---|
| B1 | ∅ |
| B2 | {B2} |
| B3 | {B2} |
| B4 | {B5} |
| B5 | {B2} |
| B6 | ∅ |

- $DF(B4) = \{B5\}$: B4 dominates itself, a predecessor of B5, but B5 can be reached through B3 → B5, so B4 does not dominate it.
- $DF(B2) = \{B2\}$: B2 dominates the latch B5, which is a predecessor of B2, and B2 does not strictly dominate itself.
- $DF(B3) = \{B2\}$ and $DF(B5) = \{B2\}$: from the back edge B5 → B2. By the edge form, the walk from B5 up to $\mathrm{idom}(B2) = B1$ passes B5, B3 and B2.

The variable `s` is assigned in B1 and B4. Then $DF(\{B1, B4\}) = \{B5\}$, $DF(\{B1, B4, B5\}) = \{B5, B2\}$, and adding B2 gives nothing new. So $DF^+ = \{B2, B5\}$, and these are the two blocks that get a phi-function for `s` in the SSA form of this program. The variable `i` is assigned in B1 and B5, and $DF^+ = \{B2\}$.

### Three nested repeat-until loops

For $n = 3$ the quadratic family above has the nodes $h_1, h_2, h_3, l_3, l_2, l_1, e$ and

$$DF(h_1) = DF(l_1) = \{h_1\},\quad DF(h_2) = DF(l_2) = \{h_1, h_2\},\quad DF(h_3) = DF(l_3) = \{h_1, h_2, h_3\},\quad DF(e) = \emptyset,$$

12 entries in total for 7 nodes and 9 edges.

### Non-examples

- **A node with one predecessor.** It is in no dominance frontier, since its predecessor is its immediate dominator.
- **A node dominated by $x$.** If $x$ strictly dominates $y$, then $y$ is not in $DF(x)$, even if $y$ is a join node. In the example, B5 is a join node but is not in $DF(B3)$, because B3 dominates B5.
- **The successors of $x$.** $DF(x)$ is not the set of successors of $x$. A successor can be strictly dominated by $x$, and a node far from $x$ can be in $DF(x)$, as $h_1 \in DF(l_3)$ shows.

## Related definitions

- [Dominators problem](/dominators-problem/) and [dominator tree](/dominator-tree/): the relation the frontier is built on.
- [Dominance frontier computation](/dominance-frontier-computation/): the bottom-up algorithm and the walk from the predecessors.
- [Phi-function](/phi-function/), [SSA construction problem](/ssa-construction-problem/) and [Cytron SSA construction](/cytron-ssa-construction/): phi-functions go on the iterated frontier.
- [Pruned SSA form](/pruned-ssa-form/): keeps only the frontier blocks where the variable is live.
- [Post-dominance](/post-dominance/) and [control dependence](/control-dependence/): the frontier on the reverse graph.

## References
