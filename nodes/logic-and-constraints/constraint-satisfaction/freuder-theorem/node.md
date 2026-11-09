---
tag: Q1W800
kind: theorem
slug: freuder-theorem
name: Freuder's theorem
aliases:
- width theorem for CSP
- Freuder's backtrack-free theorem
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: A CSP that is strongly k-consistent and has width less than k can be solved without backtracking.
prereqs: [k-consistency, constraint-graph]
see_also: [tree-structured-csp, arc-consistency, path-consistency, bucket-elimination, cutset-conditioning, degeneracy, treewidth, chronological-backtracking]
sources:
  - paper: doi:10.1145/322290.322292
    title: Eugene C. Freuder, A sufficient condition for backtrack-free search, Journal of the ACM 29(1), 1982
    locator: pages 24 to 32 (width of an ordered constraint graph, the theorem that strong k-consistency with width less than k gives backtrack-free search, and its corollary for trees and arc consistency)
  - paper: "Eugene C. Freuder, Synthesizing constraint expressions, Communications of the ACM 21(11), 1978, pages 958 to 966"
    locator: the definition of k-consistency and strong k-consistency
  - paper: "Rina Dechter and Judea Pearl, Network-based heuristics for constraint-satisfaction problems, Artificial Intelligence 34(1), 1987, pages 1 to 38"
    locator: directional consistency, adaptive consistency and induced width, which turn the theorem into algorithms
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 4, Directional consistency (width, induced width, and backtrack-free search)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, 2020
    locator: Chapter 6, Section 6.5 (the structure of problems, tree-structured CSPs)
---

Freuder's theorem gives a condition under which a [constraint satisfaction problem](/constraint-satisfaction-problem/) can be solved by a search that never backtracks. It joins a property of the values, strong [k-consistency](/k-consistency/), with a property of the shape, the width of the [constraint graph](/constraint-graph/): if the problem is strongly $k$-consistent and the variables have an order of width less than $k$, then assigning the variables in that order never meets a dead end. Its best known case is for trees: a tree-shaped problem that is node and [arc consistent](/arc-consistency/) is solved without backtracking along any order in which each variable comes after its parent. Freuder proved it in 1982.

## Statement

**Notation.** $n$ variables $x_1, \ldots, x_n$, domains of size at most $d$, $e$ edges of the constraint graph, $k$ the consistency level, $w$ the width. Constraints may have any arity. The *constraint graph* $G$ (the primal graph) has the variables as vertices and an edge between two variables that occur together in some constraint. A partial assignment is *consistent* if it satisfies every constraint whose scope lies inside the assigned variables.

**Width (Freuder 1982).** Let $\sigma = (x_{\sigma(1)}, \ldots, x_{\sigma(n)})$ be an order of the vertices. The *width of a vertex* in $\sigma$ is the number of its neighbours that come before it. The *width of $\sigma$* is the largest width of a vertex, and the *width of $G$* is the smallest width of an order.

**Backtrack-free.** A search along $\sigma$ assigns $x_{\sigma(1)}, x_{\sigma(2)}, \ldots$ in turn and gives each variable a value that keeps the assignment consistent. It is *backtrack-free* along $\sigma$ if every consistent assignment of a prefix $x_{\sigma(1)}, \ldots, x_{\sigma(i-1)}$, $i \le n$, has a consistent extension to $x_{\sigma(i)}$. Then the search finds a solution without undoing any choice.

> **Theorem 1 (Freuder 1982).** Let a CSP be strongly $k$-consistent, and let $\sigma$ be an order of its constraint graph of width $w < k$. Then the search along $\sigma$ is backtrack-free. If no domain is empty, the CSP has a solution and the search finds one with no backtracking.

> **Theorem 2 (trees).** Let the constraint graph of a binary CSP be a tree, or a forest, and let the CSP be node consistent and arc consistent with no empty domain. Then the search is backtrack-free along any order in which each variable comes after its parent, for some choice of a root in each tree.

Theorem 2 is Theorem 1 with $k = 2$: a parent-first order of a forest has width at most 1, since the only earlier neighbour of a vertex is its parent, and node plus arc consistency is strong 2-consistency. With [directional arc consistency](/tree-structured-csp/), which needs only one pass from the leaves to the root, the whole method costs $O(n d^2)$ constraint checks. The [tree-structured CSP algorithm](/tree-structured-csp/) page gives that algorithm and its cost proof.

## In plain words

Put the unknowns in a line and fill them in from left to right. When you reach an unknown, only its earlier neighbours can stop it from taking a value. If each unknown has at most $w$ earlier neighbours, and the problem is consistent enough that any fitting choice for $w$ unknowns can always be extended by one more, then every unknown always has a value that fits. You never have to go back.

For a tree, each unknown has only one earlier neighbour, its parent, if you start at the root. Then "every value of the parent has a partner in the child", which is arc consistency, is all you need.

## Proof

*Proof of Theorem 1.* Write $y_i = x_{\sigma(i)}$. Let $1 \le i \le n$ and let $\alpha$ be a consistent assignment to $y_1, \ldots, y_{i-1}$. Let $Y$ be the set of neighbours of $y_i$ among $y_1, \ldots, y_{i-1}$. Then $|Y| = j \le w \le k - 1$.

The restriction $\alpha|_Y$ is consistent, because each constraint whose scope lies inside $Y$ also lies inside $\{y_1, \ldots, y_{i-1}\}$ and is satisfied by $\alpha$. Since $j + 1 \le k$ and the CSP is strongly $k$-consistent, it is $(j + 1)$-consistent. So there is a value $a \in D_{y_i}$ such that $\alpha|_Y$ extended by $y_i = a$ is consistent. (For $j = 0$ this is 1-consistency: $a$ satisfies the unary constraints on $y_i$.)

We show that $\alpha$ extended by $y_i = a$ is consistent. Let $C$ be a constraint whose scope $S$ lies inside $\{y_1, \ldots, y_i\}$. If $y_i \notin S$, then $\alpha$ satisfies $C$. If $y_i \in S$, every other variable of $S$ occurs with $y_i$ in $C$, so it is a neighbour of $y_i$ in $G$, and it comes before $y_i$; so $S \subseteq Y \cup \{y_i\}$, and $C$ is satisfied by the consistent assignment $\alpha|_Y \cup \{y_i = a\}$. So every consistent prefix assignment extends, which is the claim.

If no domain is empty, the empty assignment is a consistent prefix assignment, and $n$ extension steps give a consistent assignment of all variables, which satisfies every constraint and is a solution. $\square$

*Proof of Theorem 2.* Root each tree of the forest at any vertex and let $\sigma$ list each parent before its children, for example in breadth-first order. A root has no earlier neighbour. Any other vertex $v$ has its parent before it, and none of its children, which come after it. It has no other neighbour, since the graph is a forest. So $\sigma$ has width at most 1. A node and arc consistent CSP is strongly 2-consistent: 1-consistency holds because no domain is empty and every value satisfies the unary constraints, and 2-consistency is arc consistency on node consistent domains. Theorem 1 with $k = 2$ and $w \le 1$ gives the result. $\square$

## Consequences

- **Trees in polynomial time.** Arc consistency does not add constraints, so it keeps a tree a tree. Enforcing it and then searching along a parent-first order solves a tree-structured CSP in polynomial time, and the [tree-structured CSP algorithm](/tree-structured-csp/) does it in $O(n d^2)$ checks by making only the arcs from parents to children consistent.
- **Small width.** Any order of minimal width can be found in $O(n + e)$ time by removing a vertex of smallest degree again and again and placing it last; the width of $G$ is its [degeneracy](/degeneracy/). So the width is easy to compute.
- **A sufficient condition, not an algorithm, for $k \ge 3$.** Enforcing strong $k$-consistency with $k \ge 3$ adds constraints on sets of up to $k - 1$ variables, which adds edges to $G$ and can raise the width above $k - 1$. The fix is to make the problem consistent only in the direction of the order, from the last variable to the first. Each variable then gains edges to its earlier neighbours only, and the width becomes the induced width $w^\ast$. This is adaptive consistency, or [bucket elimination](/bucket-elimination/), which costs time exponential in $w^\ast$, and it links the theorem to [treewidth](/treewidth/).
- **Cycles.** [Cutset conditioning](/cutset-conditioning/) removes a set of variables whose deletion leaves a forest, tries each assignment of them, and applies Theorem 2 to what is left.
- **Search heuristics.** Ordering variables to make the width small is a reason to put highly connected variables first in [chronological backtracking](/chronological-backtracking/).

## Tightness

- **Consistency one level lower is not enough.** The triangle $X, Y, Z \in \{0, 1\}$ with $\ne$ on each pair has width 2 and is strongly 2-consistent, since it is arc consistent. It has no solution, so the search must fail after backtracking. Strong 3-consistency, which is the level $w + 1$, detects this.
- **The order matters.** The chain $X = Y$, $Y = Z$ on $\{0, 1\}$ is arc consistent and is a tree. Along the order $X, Z, Y$, which has width 2 because $Y$ has two earlier neighbours, the consistent prefix $X = 0$, $Z = 1$ has no extension to $Y$. Along the parent-first order $Y, X, Z$, every prefix extends.
- **Strong consistency is needed.** Plain $k$-consistency does not imply $(k - 1)$-consistency. With $R_{xy} = R_{xz} = \{(0, 0), (0, 1)\}$ on $\{0, 1\}$, the CSP is 3-consistent, but along the order $x, y, z$ of width 1 the value $x = 1$ is a consistent prefix with no extension to $y$.
- **The condition is not necessary.** A CSP can be backtrack-free along an order of large width, for example when its constraints are all trivial, or when its constraint language is closed under a near-unanimity operation, a case that Jeavons, Cohen and Cooper (1998) treat with no width condition.

## History

Freuder (1978) defined $k$-consistency and gave a way to synthesize a globally consistent network. In 1982 he defined the width of an ordered constraint graph and proved the theorem above, with the case of trees and arc consistency as a corollary. Dechter and Pearl (1987) made the condition into algorithms: directional arc consistency for trees, adaptive consistency with the induced width for general graphs, and the cycle cutset method. Later work tied the width notions to treewidth and to the algebraic theory of the [CSP dichotomy theorem](/csp-dichotomy-theorem/), where bounded width is a property of a constraint language rather than of a graph.

## References
