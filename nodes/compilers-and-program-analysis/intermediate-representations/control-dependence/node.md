---
tag: 10RK1C
kind: definition
slug: control-dependence
name: Control dependence
aliases:
- control dependence graph
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: Node n is control dependent on branch b if one edge out of b forces n to run and another can skip it, found from post-dominance frontiers.
prereqs: [control-flow-graph, post-dominance, dominance-frontier]
see_also: [program-dependence-graph, dominator-tree, dominance-frontier-computation, aggressive-dead-code-elimination, program-slicing, static-single-information-form, data-dependence, transpose-graph]
sources:
  - paper: doi:10.1145/24039.24041
    title: Jeanne Ferrante, Karl J. Ottenstein and Joe D. Warren, The program dependence graph and its use in optimization, ACM Transactions on Programming Languages and Systems 9(3), 1987, pages 319-349
    locator: the definition of control dependence by paths and post-dominance, and its computation from the post-dominator tree
  - paper: doi:10.1145/115372.115320
    title: Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4), 1991, pages 451-490
    locator: the section on the control dependence graph, which proves that control dependences are the dominance frontiers of the reverse control flow graph
  - paper: doi:10.1109/32.58784
    title: Andy Podgurski and Lori A. Clarke, A formal model of program dependences and its implications for software testing, debugging, and maintenance, IEEE Transactions on Software Engineering 16(9), 1990, pages 965-979
    locator: strong and weak control dependence
  - paper: doi:10.1145/256167.256217
    title: Keshav Pingali and Gianfranco Bilardi, Optimal control dependence computation and the Roman chariots problem, ACM Transactions on Programming Languages and Systems 19(3), 1997, pages 462-491
    locator: the augmented post-dominator tree, which answers control dependence queries in time proportional to the size of the answer after linear preprocessing
  - paper: doi:10.1145/231379.231435
    title: Gianfranco Bilardi and Keshav Pingali, A framework for generalized control dependence, PLDI 1996, pages 291-300
    locator: control dependence relative to a family of path sets, which covers the strong and weak forms
  - book: isbn:1558603204
    title: Steven S. Muchnick, Advanced Compiler Design and Implementation, Morgan Kaufmann, 1997
    locator: the chapter on dependence analysis and dependence graphs, control dependence and program dependence graphs
---

Control dependence says which branch decides whether a node of a [control flow graph](/control-flow-graph/) runs. Node $Y$ is control dependent on node $X$ if one edge out of $X$ makes $Y$ certain to run and another edge out of $X$ can skip $Y$. Ferrante, Ottenstein and Warren (1987) defined it through [post-dominance](/post-dominance/), and Cytron et al. (1991) showed that the nodes that control $Y$ are the [dominance frontier](/dominance-frontier/) of $Y$ in the reverse graph. The relation, drawn as a graph with an edge from $X$ to each node that depends on it, is the *control dependence graph*. Together with [data dependence](/data-dependence/) it makes the [program dependence graph](/program-dependence-graph/), and it drives [aggressive dead code elimination](/aggressive-dead-code-elimination/) and [program slicing](/program-slicing/).

## Definition

Let $G = (N, E)$ be a control flow graph with an entry node and one exit node $x$, in which every node reaches $x$. Add a node START with an edge to the entry and an edge to $x$. The second edge is not a real control transfer: it says that the procedure may not run at all, and it makes the nodes that run on every run depend on START, so that every node except START has a parent in the control dependence graph. Post-dominance is taken in this augmented graph, written $p \;\mathrm{pdom}\; v$, with $\mathrm{ipdom}(v)$ the immediate post-dominator.

**Path form** (Ferrante, Ottenstein and Warren). $Y$ is **control dependent** on $X$ if

1. there is a path $X \to v_1 \to \dots \to v_k = Y$ with $k \ge 1$ on which $Y \;\mathrm{pdom}\; v_i$ for every $i$, and
2. $Y$ does not strictly post-dominate $X$.

**Edge form.** $Y$ is control dependent on $X$ **through the edge** $X \to S$ if $Y \;\mathrm{pdom}\; S$ and $Y$ does not strictly post-dominate $X$. The successor $S$ is the *label* of the dependence: it records which way the branch at $X$ must go for $Y$ to run. A two-way branch with a true edge and a false edge gives labels T and F.

**Reverse dominance frontier.** Let $G^T$ be the [transpose](/transpose-graph/) of the augmented graph, with $x$ as its start. The post-dominators in $G$ are the dominators in $G^T$, so the [dominance frontier](/dominance-frontier/) of $Y$ in $G^T$ is

$$\mathrm{RDF}(Y) = \{X : Y \;\mathrm{pdom}\; S \text{ for some successor } S \text{ of } X, \text{ and } Y \text{ does not strictly post-dominate } X\}.$$

The three forms define the same relation.

**Theorem** (Cytron et al. 1991). For all nodes $X$ and $Y$: $Y$ is control dependent on $X$ by the path form, iff it is by the edge form through some successor of $X$, iff $X \in \mathrm{RDF}(Y)$.

*Proof.* The edge form and the formula for $\mathrm{RDF}(Y)$ are the same text, because the predecessors of $X$ in $G^T$ are the successors of $X$ in $G$, and "dominates in $G^T$" is "post-dominates in $G$". It is left to show that the path form and the edge form agree. Condition 2 is the same in both. If a path as in condition 1 exists, its first node after $X$ is a successor $S = v_1$, and $Y \;\mathrm{pdom}\; v_1$, so the edge form holds. Conversely, let $Y \;\mathrm{pdom}\; S$ for a successor $S$ of $X$. Take any path from $S$ to $x$. It contains $Y$, so cut it at the first occurrence of $Y$: $S = v_1, \dots, v_k = Y$. Suppose some $v_i$ with $i < k$ were not post-dominated by $Y$. Then some path from $v_i$ to $x$ avoids $Y$, and the prefix $v_1, \dots, v_i$ also avoids $Y$, so their join is a path from $S$ to $x$ that avoids $Y$, which contradicts $Y \;\mathrm{pdom}\; S$. So $X, v_1, \dots, v_k$ is a path as in condition 1. $\square$

### Computing it from the post-dominator tree

The edge form gives a direct algorithm. Build the post-dominator tree, for example with the [Cooper-Harvey-Kennedy](/cooper-harvey-kennedy-dominance/) iteration on $G^T$. Then:

```
for each edge a -> b of the augmented CFG:
    if b != ipdom(a):
        runner = b
        while runner != ipdom(a):
            record: runner is control dependent on a, label b
            runner = ipdom(runner)
```

**Why the walk is correct.** Fix an edge $a \to b$. By the edge form, the nodes that depend on $a$ through it are the post-dominators of $b$ that are not strict post-dominators of $a$. In the post-dominator tree, the post-dominators of $b$ are the ancestors of $b$ (with $b$ itself), and the strict post-dominators of $a$ are $\mathrm{ipdom}(a)$ and its ancestors. Now $\mathrm{ipdom}(a)$ post-dominates $b$: a path from $b$ to $x$, with the edge $a \to b$ in front, is a path from $a$ to $x$, so it holds $\mathrm{ipdom}(a)$, and $\mathrm{ipdom}(a) \ne a$, so $\mathrm{ipdom}(a)$ lies on the part after $a$. So $\mathrm{ipdom}(a)$ is an ancestor of $b$, and the wanted set is the tree path from $b$ up to $\mathrm{ipdom}(a)$ with $\mathrm{ipdom}(a)$ left out. That is what the walk visits. If $b = \mathrm{ipdom}(a)$ the set is empty, and these are the only edges that give nothing: if $b$ strictly post-dominates $a$, then $b$ is $\mathrm{ipdom}(a)$ or above it, and also below it, so $b = \mathrm{ipdom}(a)$.

**Cost.** The post-dominator tree costs what dominators cost on a graph with $n$ nodes and $m$ edges. Each step of the walk records one new triple, so the walks cost $O(m + c)$, where $c$ is the number of (node, branch, label) triples in the answer. The answer itself can have $\Theta(n^2)$ pairs with only $O(n)$ edges, as the chain example below shows. Pingali and Bilardi (1997) avoid building it: their augmented post-dominator tree takes $O(m)$ time and space to build and answers "which nodes depend on this edge", "which edges does this node depend on" and "which nodes have the same dependences" in time proportional to the size of the answer.

### Properties

- **Self-dependence.** A node can be control dependent on itself. This happens exactly when $X$ has a successor $S$ with $X \;\mathrm{pdom}\; S$, that is, when $X$ is a loop test and one edge stays in the loop.
- **Only branches control.** If $X$ has one successor $S$, then $S = \mathrm{ipdom}(X)$, so no node depends on $X$.
- **The parents of a node.** The nodes that $Y$ depends on are $\mathrm{RDF}(Y)$, so they can also be found with the [dominance frontier computation](/dominance-frontier-computation/) run on $G^T$, one node at a time.
- **Regions.** Two nodes with the same set of (branch, label) pairs run under the same conditions. Ferrante, Ottenstein and Warren group such nodes under one region node in the program dependence graph.

## Examples and non-examples

### The odd-sum loop

The toy IR program that adds the odd numbers below $n$ has blocks B1 to B6, where B2 is the loop test `br t1 B3 B6`, B3 is the parity test `br t2 B4 B5`, B4 adds, B5 increments and jumps back to B2, and B6 returns. After START and EXIT are added, the post-dominator tree has the edges $\mathrm{ipdom}(B1) = B2$, $\mathrm{ipdom}(B2) = B6$, $\mathrm{ipdom}(B3) = \mathrm{ipdom}(B4) = B5$, $\mathrm{ipdom}(B5) = B2$, $\mathrm{ipdom}(B6) = \mathrm{EXIT}$ and $\mathrm{ipdom}(\mathrm{START}) = \mathrm{EXIT}$.

Of the ten edges, seven end at the immediate post-dominator of their source and give nothing: $\mathrm{START} \to \mathrm{EXIT}$, $B1 \to B2$, $B2 \to B6$, $B3 \to B5$, $B4 \to B5$, $B5 \to B2$ and $B6 \to \mathrm{EXIT}$. The other three walk:

| edge | stop at | walk visits | dependences recorded |
|---|---|---|---|
| $\mathrm{START} \to B1$ | EXIT | B1, B2, B6 | B1, B2, B6 on START |
| $B2 \to B3$ | B6 | B3, B5, B2 | B3, B5, B2 on B2, label B3 |
| $B3 \to B4$ | B5 | B4 | B4 on B3, label B4 |

So B1, B2 and B6 run on every run, B3 and B5 run once per trip of the loop, B2 depends on itself because it is the loop test, and B4 runs only when the parity test takes its true edge. The [post-dominance](/post-dominance/) page derives the same block dependences from the edge form by hand.

### A diamond

For `B0: br a B1 B2`, `B1: x = 1; jump B3`, `B2: x = 2; jump B3`, `B3: ret x`, the dependences are B0 and B3 on START, B1 on B0 with label B1, and B2 on B0 with label B2. The join block B3 depends on nothing inside the procedure, because both edges of B0 reach it.

### A chain with back edges

Take blocks $v_1, \dots, v_k$ with the edges $v_i \to v_{i+1}$, an edge $v_k \to x$, and an edge $v_i \to v_1$ from every $v_i$. Every path to $x$ passes through all of $v_1, \dots, v_k$ in order, so $\mathrm{ipdom}(v_i) = v_{i+1}$. The edge $v_i \to v_1$ walks $v_1, v_2, \dots, v_i$, so $v_j$ depends on $v_i$ for every $j \le i$. That is $k(k+1)/2$ dependences from $2k$ edges, which is why an explicit control dependence graph can be quadratic in the size of the CFG.

### Non-examples

- **Both edges reach the node.** In the odd-sum loop, B5 is not control dependent on B3: B5 post-dominates both successors of B3, and it strictly post-dominates B3 itself.
- **One edge goes straight to the node.** B6 is not control dependent on B2, even though the edge $B2 \to B6$ reaches it at once. B6 strictly post-dominates B2, since leaving the loop is the only way to return, so condition 2 fails.
- **Reachability is not dependence.** B4 is reachable from B2, but it is not control dependent on B2: B4 does not post-dominate B3, the only node after B2 on any path to B4.
- **Code after an infinite loop.** If a loop may never stop, the code after it runs only if the loop stops. The standard (strong) definition ignores this: the node after a loop post-dominates the loop test, so it does not depend on it. A loop with no exit at all leaves nodes that cannot reach $x$, and the definition does not apply until a fake exit edge is added, as discussed under [post-dominance](/post-dominance/).

## Related definitions

- **Weak control dependence.** Podgurski and Clarke (1990) call the definition above *strong* control dependence, and define a *weak* form that also makes the code after a loop depend on the loop test, because the loop might not terminate. Analyses that must keep non-termination, such as some slicers, use the weak form.
- **Generalized control dependence.** Bilardi and Pingali (1996) give one framework, parameterized by a set of paths, from which the strong and weak forms both follow.
- [Post-dominance](/post-dominance/) and the [dominator tree](/dominator-tree/): the relation is read off the post-dominator tree.
- [Dominance frontier](/dominance-frontier/): control dependence is the dominance frontier of the reverse graph.
- [Data dependence](/data-dependence/): the other kind of edge in a [program dependence graph](/program-dependence-graph/).
- [Static single information form](/static-single-information-form/): it renames variables at the branch points that control dependence names.

## References

- Jeanne Ferrante, Karl J. Ottenstein and Joe D. Warren. The program dependence graph and its use in optimization. ACM TOPLAS 9(3), 1987, pages 319-349. The path definition and the walk over the post-dominator tree.
- Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck. Efficiently computing static single assignment form and the control dependence graph. ACM TOPLAS 13(4), 1991, pages 451-490. Control dependence as reverse dominance frontiers.
- Andy Podgurski and Lori A. Clarke. A formal model of program dependences and its implications for software testing, debugging, and maintenance. IEEE TSE 16(9), 1990, pages 965-979. Strong and weak control dependence.
- Keshav Pingali and Gianfranco Bilardi. Optimal control dependence computation and the Roman chariots problem. ACM TOPLAS 19(3), 1997, pages 462-491.
- Gianfranco Bilardi and Keshav Pingali. A framework for generalized control dependence. PLDI 1996, pages 291-300.
- Steven S. Muchnick. Advanced Compiler Design and Implementation. Morgan Kaufmann, 1997. The chapter on dependence analysis and dependence graphs.
