---
tag: 8WKNDT
kind: concept
slug: path-consistency
name: Path consistency
aliases:
- 3-consistency
- strong path consistency
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Every consistent assignment to a pair of variables extends to any third variable along each path of the constraint graph.
prereqs: [arc-consistency, constraint-graph]
see_also: [pc-2, k-consistency, ac-3, constraint-propagation, simple-temporal-problem, allens-interval-algebra, singleton-arc-consistency, freuder-theorem]
sources:
  - paper: doi:10.1016/0020-0255(74)90008-5
    title: Ugo Montanari, Networks of constraints, fundamental properties and applications to picture processing, Information Sciences 7, 1974
    locator: pages 95 to 132 (path consistency of networks of binary relations, composition and intersection, and the reduction to paths of length 2)
  - paper: doi:10.1016/0004-3702(77)90007-8
    title: Alan K. Mackworth, Consistency in networks of relations, Artificial Intelligence 8(1), 1977
    locator: pages 99 to 118 (path consistency and the algorithms PC-1 and PC-2)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 3, Consistency-enforcing algorithms (path consistency and 3-consistency), and Chapter 12, Temporal constraint networks
  - paper: "Peter Jeavons, David Cohen and Martin C. Cooper, Constraints, consistency and closure, Artificial Intelligence 101(1-2), 1998, pages 251 to 265"
    locator: constraints closed under a near-unanimity operation of arity k+1 are solved by strong (k+1)-consistency; for a majority operation this is strong path consistency
  - paper: "Rina Dechter, Itay Meiri and Judea Pearl, Temporal constraint networks, Artificial Intelligence 49(1-3), 1991, pages 61 to 95"
    locator: the simple temporal problem, where path consistency is the Floyd-Warshall algorithm and decides consistency
  - paper: "Bernhard Nebel and Hans-Jürgen Bürckert, Reasoning about temporal relations, a maximal tractable subclass of Allen's interval algebra, Journal of the ACM 42(1), 1995, pages 43 to 66"
    locator: path consistency decides the ORD-Horn subclass of Allen's interval algebra
---

Path consistency is a property of a binary [constraint satisfaction problem](/constraint-satisfaction-problem/): for every two variables and every pair of values that their constraint allows, every third variable has a value that is compatible with both. It is the same as 3-consistency in the sense of [k-consistency](/k-consistency/), and, with [arc consistency](/arc-consistency/), strong path consistency. Montanari (1974) introduced it, and Mackworth (1977) gave the algorithms PC-1 and [PC-2](/pc-2/). Unlike arc consistency, it deletes pairs of values and can add new constraints, and it decides some problems that arc consistency cannot, such as 2-SAT and the [simple temporal problem](/simple-temporal-problem/).

## In plain words

Arc consistency looks at one rule at a time. Path consistency looks at three unknowns at a time. Suppose two unknowns may take the values "red" and "blue" together. Path consistency asks: is there a value for a third unknown that fits with both? If not, that pair is impossible, and we delete it from the list of allowed pairs, even when the two unknowns had no rule between them before.

Repeating this until nothing changes gives tighter rules. It can show that a problem has no solution when arc consistency cannot, for example two colours on a triangle. It costs more, and it fills in rules between unknowns that were not linked, so the problem loses its simple shape.

## The idea

**Notation.** A binary CSP has variables $x_1, \ldots, x_n$, domains $D_i$ with $|D_i| \le d$, and binary constraints. We complete the network: for each pair $i \ne j$, $R_{ij} \subseteq D_i \times D_j$ is the intersection of the constraints on $x_i$ and $x_j$, or $D_i \times D_j$ if there is none, and $R_{ji}$ is its converse. Here $k$ is the third variable of a triple and the consistency level 3.

**Definition.** The pair $(i, j)$ is *path consistent relative to* $k \notin \{i, j\}$ if for every $(a, b) \in R_{ij}$ there is $c \in D_k$ with $(a, c) \in R_{ik}$ and $(c, b) \in R_{kj}$. The network is *path consistent* if every pair is path consistent relative to every third variable, and *strongly path consistent* if it is also arc consistent. In relation algebra, path consistency says $R_{ij} \subseteq R_{ik} \circ R_{kj}$ for all distinct $i, j, k$, where $\circ$ is composition, and enforcing it repeats

$$R_{ij} \leftarrow R_{ij} \cap (R_{ik} \circ R_{kj})$$

until no relation changes.

**Equal to 3-consistency.** An assignment $x_i = a$, $x_j = b$ is consistent when $a \in D_i$, $b \in D_j$ and $(a, b) \in R_{ij}$. It extends to $x_k$ when some $c \in D_k$ satisfies both $R_{ik}$ and $R_{kj}$. So 3-consistency for a binary CSP is exactly path consistency, and strong 3-consistency is strong path consistency.

**Paths of any length.** Montanari's original definition asks the condition along every path $i = v_0, v_1, \ldots, v_p = j$ of the complete graph: each $(a, b) \in R_{ij}$ has values $c_t \in D_{v_t}$, with $c_0 = a$ and $c_p = b$, such that $(c_{t-1}, c_t) \in R_{v_{t-1} v_t}$ for each $t$.

> **Theorem (Montanari 1974).** In a complete binary network, path consistency for all paths of length 2 implies it for all paths.
>
> *Proof.* By induction on the length $p$. The case $p = 1$ is the pair itself, and $p = 2$ is the hypothesis. Let $p \ge 3$ and $(a, b) \in R_{v_0 v_p}$. Path consistency of $(v_0, v_p)$ relative to $v_{p-1}$ gives $c \in D_{v_{p-1}}$ with $(a, c) \in R_{v_0 v_{p-1}}$ and $(c, b) \in R_{v_{p-1} v_p}$. The network is complete, so $R_{v_0 v_{p-1}}$ exists, and the induction hypothesis for the path $v_0, \ldots, v_{p-1}$ of length $p - 1$ gives values $c_1, \ldots, c_{p-2}$ that link $a$ to $c$. Adding $c_{p-1} = c$ and $c_p = b$ gives the path. $\square$

This is why completing the network matters: in an incomplete graph, length 2 is not enough.

**A unique closure.** The union of two path consistent networks inside the same complete network is path consistent: a witness for a pair of one network is a witness in the union. So each network has a largest path consistent sub-network, its *path consistency closure*, and it contains all pairs of values that occur in solutions. [PC-2](/pc-2/) computes it in $O(n^3 d^5)$ time, and its proof page shows how to add arc consistency at the end to get the strong closure. In a path consistent network with at least 3 variables, each value occurs in every relation of its variable or in none.

**What it decides.** Strong path consistency with no empty relation or domain does not imply a solution in general. It does for:

- *Binary Boolean constraints* (2-SAT). Each binary relation on $\{0, 1\}$ is closed under the majority operation, so the theorem of Jeavons, Cohen and Cooper (1998) on near-unanimity operations applies. Arc consistency alone does not decide 2-SAT: the triangle with two colours below is a 2-SAT instance, since $x \ne y$ is $(x \vee y) \wedge (\neg x \vee \neg y)$, and it is arc consistent and unsatisfiable.
- *Majority-closed constraints* in general, by the same theorem.
- *The simple temporal problem*, with constraints $a \le x_j - x_i \le b$. Composition adds intervals and intersection takes the tighter bounds, so path consistency is the Floyd-Warshall algorithm, and the network is consistent exactly when no negative cycle appears (Dechter, Meiri and Pearl 1991).
- *The ORD-Horn subclass of [Allen's interval algebra](/allens-interval-algebra/)*, where path consistency decides consistency (Nebel and Bürckert 1995).

**How the pages relate.** This page defines the property. [PC-2](/pc-2/) is an algorithm that enforces it, as [AC-3](/ac-3/) enforces arc consistency. [k-consistency](/k-consistency/) generalizes it to sets of $k - 1$ variables, and [singleton arc consistency](/singleton-arc-consistency/) is a different strengthening of arc consistency that deletes values only, never pairs.

## Examples

**The triangle with two colours.** $X, Y, Z \in \{0, 1\}$ with $\ne$ on each pair is arc consistent. The pair $(X, Y) = (0, 1)$ needs $Z \ne 0$ and $Z \ne 1$, which is impossible, and so does $(1, 0)$. Path consistency empties $R_{XY}$ and proves that there is no solution.

**A derived equality.** On the 4-cycle $x_0 x_1 x_2 x_3$ with domain $\{0, 1\}$ and $\ne$ on its edges, the pair $x_0, x_2$ has no constraint, so $R_{02}$ starts full. The pairs $(0, 1)$ and $(1, 0)$ have no common $\ne$-partner in $x_1$, so path consistency derives $x_0 = x_2$, and in the same way $x_1 = x_3$. The [PC-2](/pc-2/) page traces this run.

**Path consistent with no solution.** Four variables with domain $\{0, 1, 2\}$ and $\ne$ on all pairs (3-colouring the complete graph $K_4$) are path consistent: any two different colours leave a third colour for each other variable. No solution exists. Strong 4-consistency would detect this.

**Temporal constraints.** $10 \le x_2 - x_1 \le 20$, $5 \le x_3 - x_2 \le 15$ and $x_3 - x_1 \le 18$. Composition through $x_2$ gives $15 \le x_3 - x_1 \le 35$, and intersection with $(-\infty, 18]$ gives $15 \le x_3 - x_1 \le 18$. Running the other triples tightens $x_2 - x_1$ to $[10, 13]$ and $x_3 - x_2$ to $[5, 8]$.

**A non-example.** A network in which only some pairs have constraints and each existing triangle passes the test is not yet path consistent: the definition is over the completed network, and a pair with no constraint can still lose pairs of values.

## Where it is used

- **Temporal and spatial reasoning.** Path consistency, also called algebraic closure, is the main inference step for the [simple temporal problem](/simple-temporal-problem/), [Allen's interval algebra](/allens-interval-algebra/) and region calculi.
- **Tractable classes.** It decides binary Boolean CSPs and other majority-closed languages, which are classes of the [CSP dichotomy theorem](/csp-dichotomy-theorem/) of bounded width.
- **Backtrack-free search.** With an order of width at most 2, strong path consistency gives backtrack-free search by [Freuder's theorem](/freuder-theorem/), when no domain is empty.
- **Preprocessing of small dense problems.** For a few dozen variables, it can remove many pairs before a search, at the price of a complete graph.
- **A step in the hierarchy.** It is the level $k = 3$ of [k-consistency](/k-consistency/), between [arc consistency](/arc-consistency/) and higher levels; in practice solvers often prefer [singleton arc consistency](/singleton-arc-consistency/), which keeps the graph sparse.

## References
