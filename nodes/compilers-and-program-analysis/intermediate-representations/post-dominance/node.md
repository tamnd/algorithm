---
tag: FWJCCP
kind: definition
slug: post-dominance
name: Post-dominance
aliases:
- postdominator
- post-dominator tree
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: Block p post-dominates block v if every path from v to the exit passes through p; the immediate post-dominators form a tree rooted at the exit.
prereqs: [control-flow-graph, dominators-problem, transpose-graph]
see_also: [dominator-tree, cooper-harvey-kennedy-dominance, control-dependence, program-dependence-graph, dominance-frontier, aggressive-dead-code-elimination, lengauer-tarjan-algorithm, graph-reachability]
sources:
  - paper: doi:10.1145/24039.24041
    title: Jeanne Ferrante, Karl J. Ottenstein and Joe D. Warren, The program dependence graph and its use in optimization, ACM Transactions on Programming Languages and Systems 9(3), 1987, pages 319-349
    locator: the definitions of post-dominance, of the post-dominator tree and of control dependence on a control flow graph with a unique exit
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: the section on the control dependence graph, which computes control dependences as dominance frontiers of the reverse control flow graph
  - book: isbn:1558603204
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: Chapter 7 (Control-Flow Analysis), dominators and postdominators
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 9 (Data-Flow Analysis), dominance; the reverse control flow graph and reverse dominance frontiers in the treatment of dead code elimination
---

Post-dominance is dominance with the arrows turned around. In a [control flow graph](/control-flow-graph/) with one exit, a block $p$ post-dominates a block $v$ if every path from $v$ to the exit passes through $p$. So once control reaches $v$, it must later reach $p$, if the run ends normally. The closest such block is the immediate post-dominator, and these form the post-dominator tree, rooted at the exit. Post-dominance is the [dominators problem](/dominators-problem/) on the [transpose graph](/transpose-graph/), so the same algorithms compute it. Its main use is [control dependence](/control-dependence/): which branch decides whether a block runs.

## Definition

Let $G = (N, E, r)$ be a control flow graph with a designated *exit* node $x$, and assume for now that every node has a path to $x$. If the procedure has several returning blocks, $x$ is a new node with an edge from each of them; nodes that cannot reach any return are treated below.

- $p$ **post-dominates** $v$, written $p \;\mathrm{pdom}\; v$, if every path from $v$ to $x$ contains $p$. Every node post-dominates itself, and $x$ post-dominates every node.
- $p$ **strictly post-dominates** $v$ if $p \;\mathrm{pdom}\; v$ and $p \ne v$.
- The **immediate post-dominator** $\mathrm{ipdom}(v)$ of $v \ne x$ is the strict post-dominator of $v$ that every other strict post-dominator of $v$ post-dominates.

Let $G^T$ be the transpose of $G$: the same nodes, every edge $(a, b)$ turned into $(b, a)$, and $x$ as the start node. A path from $v$ to $x$ in $G$ is, read backward, a path from $x$ to $v$ in $G^T$. So

$$p \;\mathrm{pdom}\; v \text{ in } G \iff p \text{ dominates } v \text{ in } G^T \text{ with start } x.$$

Every fact about dominance carries over through this one line. Post-dominance is reflexive, antisymmetric and transitive on the nodes that reach $x$; the strict post-dominators of $v$ are totally ordered by post-dominance; $\mathrm{ipdom}(v)$ exists and is unique for $v \ne x$; and the edges $\mathrm{ipdom}(v) \to v$ form a tree rooted at $x$, the **post-dominator tree**, in which the post-dominators of $v$ are exactly the ancestors of $v$. The proofs are those of the [dominator tree](/dominator-tree/), applied to $G^T$.

### Computing it

Run any dominator algorithm on $G^T$ from $x$: the [Cooper-Harvey-Kennedy](/cooper-harvey-kennedy-dominance/) iteration, which needs a reverse postorder of $G^T$ (not of $G$), or the [Lengauer-Tarjan algorithm](/lengauer-tarjan-algorithm/). The cost is the same as for dominators on a graph with the same $n$ and $m$.

### Nodes that cannot reach the exit

A procedure with a loop that never exits, such as an event loop, has nodes with no path to $x$. For them the definition says that every $p$ post-dominates them, which is useless, and they are not reachable from $x$ in $G^T$. Compilers fix this in one of three ways: add a fake edge to $x$ from some node of each such loop (so every node reaches $x$), treat those nodes as having no post-dominator, or use a weaker notion for non-terminating programs. The choice changes the post-dominator tree and the control dependences, so tools differ here. This is the main place where post-dominance is not a plain mirror of dominance: in a CFG every node is reachable from $r$ after cleanup, but not every node can reach $x$.

### Control dependence

Ferrante, Ottenstein and Warren (1987) define: $Y$ is **control dependent** on $X$ if there is a path from $X$ to $Y$ on which $Y$ post-dominates every node after $X$, and $Y$ does not strictly post-dominate $X$. An equivalent form: $Y$ is control dependent on $X$ if $X$ has an edge to a successor $S$ with $Y \;\mathrm{pdom}\; S$, and $Y$ does not strictly post-dominate $X$. In words, one edge out of $X$ forces control to reach $Y$, and another edge out of $X$ can avoid it. Cytron et al. (1991) show that the nodes on which $Y$ is control dependent are the [dominance frontier](/dominance-frontier/) of $Y$ in $G^T$, the *reverse dominance frontier*.

## Examples and non-examples

### A loop with a branch inside

Take the toy IR program that adds the odd numbers below $n$, with blocks B1 to B6 and the edges

$$B1 \to B2,\; B2 \to B3,\; B2 \to B6,\; B3 \to B4,\; B3 \to B5,\; B4 \to B5,\; B5 \to B2.$$

B6 holds `ret s`, so it is the exit. Computed by the definition (delete $p$ and test whether $v$ still reaches B6):

| $v$ | post-dominators of $v$ | $\mathrm{ipdom}(v)$ |
|---|---|---|
| B1 | B1, B2, B6 | B2 |
| B2 | B2, B6 | B6 |
| B3 | B3, B5, B2, B6 | B5 |
| B4 | B4, B5, B2, B6 | B5 |
| B5 | B5, B2, B6 | B2 |
| B6 | B6 | none |

The post-dominator tree has the edges $B6 \to B2$, $B2 \to B1$, $B2 \to B5$, $B5 \to B3$, $B5 \to B4$. Compare the dominator tree of the same graph, which has $B1 \to B2$, $B2 \to B3$, $B2 \to B6$, $B3 \to B4$, $B3 \to B5$. B3 dominates B5 but B5 post-dominates B3: the branch in B3 and its join point in B5 swap roles.

The control dependences, by the edge form of the definition: B4 is control dependent on B3 (the edge $B3 \to B4$ reaches it, the edge $B3 \to B5$ avoids it). B2, B3 and B5 are control dependent on B2, because the edge $B2 \to B3$ leads to them and the edge $B2 \to B6$ leaves the loop. B1 and B6 are control dependent on nothing: they run on every run that ends. In a [program dependence graph](/program-dependence-graph/) these are the control edges.

### A diamond

For `B0: br a B1 B2`, `B1: jump B3`, `B2: jump B3`, `B3: ret x`, the post-dominators of B0 are B0 and B3, so $\mathrm{ipdom}(B0) = B3$, the join point of the branch. This is why the classic stack-based scheme for GPU branches, which runs the two sides one after the other for different threads, joins the threads again at the immediate post-dominator of the branch: it is the first block that every thread must reach.

### Several returns

If B4 holds `ret 1` and B5 holds `ret 0`, the graph has two exits and no node post-dominates both. With a virtual exit $x$ and the edges $B4 \to x$, $B5 \to x$, the immediate post-dominator of B4 and of B5 is $x$.

### Non-examples

- "B5 runs after B3" is not post-dominance when B5 can be avoided. In the graph $B3 \to B4$, $B3 \to B5$, $B4 \to x$, $B5 \to x$, B5 does not post-dominate B3.
- Post-dominance is not dominance read in the other direction on the same nodes. B2 dominates B6 above, and B6 post-dominates B2, but B3 dominates B4 while B4 does not post-dominate B3.
- On a node in an infinite loop, without a fake exit edge, post-dominance is not defined in a useful way, as explained above.

### Pitfalls

- **Wrong order for the iteration.** The iterative algorithm on $G^T$ needs a reverse postorder of a depth-first search of $G^T$ from $x$. The reverse of a postorder of $G$ is not that order.
- **Forgetting the virtual exit.** With several returns, a dominator algorithm on $G^T$ has no single start node. Add $x$ first.
- **Silently dropping non-terminating code.** Nodes that cannot reach $x$ are not visited by a search of $G^T$. If an optimization such as [aggressive dead code elimination](/aggressive-dead-code-elimination/) then treats them as dead, it can delete an infinite loop, which changes the behavior of the program.

## Related definitions

- [Dominators problem](/dominators-problem/) and [dominator tree](/dominator-tree/): the forward relation and its tree.
- [Transpose graph](/transpose-graph/): post-dominance is dominance on it.
- [Control dependence](/control-dependence/) and [program dependence graph](/program-dependence-graph/): built from post-dominance.
- [Dominance frontier](/dominance-frontier/): computed on $G^T$, it gives control dependence.
- [Cooper-Harvey-Kennedy dominance](/cooper-harvey-kennedy-dominance/) and [Lengauer-Tarjan algorithm](/lengauer-tarjan-algorithm/): algorithms that compute post-dominators when run on $G^T$.

## References
