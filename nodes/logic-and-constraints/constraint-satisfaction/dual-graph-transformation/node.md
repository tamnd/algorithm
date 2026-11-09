---
tag: 52WAK0
kind: concept
slug: dual-graph-transformation
name: Dual encoding
aliases:
- dual graph transformation
- hidden variable encoding
- binarization of constraints
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Transforms a CSP with non-binary constraints into an equivalent binary CSP by making each constraint a variable.
prereqs: [constraint-satisfaction-problem, constraint-graph]
see_also: [arc-consistency, tree-structured-csp, tree-decomposition, bucket-elimination, global-constraint, forward-checking, k-consistency, path-consistency]
sources:
  - paper: "Rina Dechter and Judea Pearl, Tree clustering for constraint networks, Artificial Intelligence 38(3), 1989, pages 353 to 366"
    locator: the dual network of a CSP, join trees, and tree clustering, which makes the dual network a tree
  - paper: "Francesca Rossi, Charles Petrie and Vasant Dhar, On the equivalence of constraint satisfaction problems, Proceedings of ECAI 1990, pages 550 to 556"
    locator: the equivalence of non-binary CSPs and their binary encodings, including the hidden variable encoding
  - paper: "Fahiem Bacchus and Peter van Beek, On the conversion between non-binary and binary constraint satisfaction problems, Proceedings of AAAI 1998, pages 311 to 318"
    locator: the dual and hidden variable encodings, and how backtracking and forward checking on them compare with the original problem
  - paper: "Kostas Stergiou and Toby Walsh, Encodings of non-binary constraint satisfaction problems, Proceedings of AAAI 1999, pages 163 to 168"
    locator: arc consistency on the hidden variable encoding equals generalized arc consistency on the original, and on the dual encoding it is strictly stronger
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 9, Tree decomposition methods (dual graphs, join graphs and join trees)
---

The dual encoding turns a [constraint satisfaction problem](/constraint-satisfaction-problem/) with constraints of any arity into a binary one. Each original constraint becomes a *dual variable*, whose values are the tuples that the constraint allows. Two dual variables are linked by a binary constraint when their scopes share original variables, and the constraint says that the two tuples agree on the shared variables. The dual problem has the same solutions as the original, up to a one-to-one map. A related binarization, the *hidden variable encoding*, keeps the original variables and adds one hidden variable per constraint. Both let binary algorithms such as [AC-3](/ac-3/) and the [tree-structured CSP algorithm](/tree-structured-csp/) run on non-binary problems. Dechter and Pearl used the dual network in 1989, and Rossi, Petrie and Dhar (1990) showed the equivalence of these encodings with the original problem.

## In plain words

Some rules talk about three or more unknowns at once. Many methods handle only rules on two unknowns. The dual encoding changes the point of view: treat each rule as a new unknown, whose possible values are the rows of its table of allowed combinations. Two of these new unknowns must agree wherever their rows mention the same original unknown.

Now every rule talks about two of the new unknowns, so the binary methods apply. Picking one row per rule, so that rows agree on shared unknowns, is the same as picking a value for each original unknown that satisfies all the rules. The price is size: a table can have many rows, so the new unknowns can have very large domains.

## The idea

**Notation.** $n$ variables $x_1, \ldots, x_n$ with domains of size at most $d$, and $m$ constraints $C_1, \ldots, C_m$ of arity at most $r$. Each $C_k$ has a scope $S_k$ and an allowed relation $R_k$ of tuples over $S_k$, with $|R_k| \le d^r$. For a tuple $t$ over $S$ and a variable $x \in S$, $t[x]$ is the value of $x$ in $t$. We assume that each variable lies in some scope; a variable in no scope can take any value of its domain and is handled apart.

**The dual encoding.** The dual CSP has one variable $c_k$ for each constraint, with domain $R_k$. For each pair $k \ne l$ with $S_k \cap S_l \ne \emptyset$, it has the binary constraint

$$\{(t, u) \in R_k \times R_l : t[x] = u[x] \text{ for every } x \in S_k \cap S_l\}.$$

Its constraint graph is the *dual graph* of the CSP, described on the [constraint graph](/constraint-graph/) page.

**The hidden variable encoding.** Keep the variables $x_1, \ldots, x_n$ with their domains, and add one hidden variable $h_k$ with domain $R_k$ for each constraint. For each $k$ and each $x \in S_k$, add the binary constraint "$h_k[x] = x$". The constraint graph is the bipartite *incidence graph* of variables and constraints.

> **Proposition (same solutions).** The map $s \mapsto (s|_{S_1}, \ldots, s|_{S_m})$ is a one-to-one correspondence between the solutions of the CSP and those of its dual encoding. The map $s \mapsto (s, s|_{S_1}, \ldots, s|_{S_m})$ is one between the solutions of the CSP and those of the hidden variable encoding.
>
> *Proof.* If $s$ is a solution, each $s|_{S_k}$ lies in $R_k$, and two restrictions agree on shared variables because they come from the same $s$. Conversely, let $(t_1, \ldots, t_m)$ satisfy the dual constraints. For each variable $x$, choose any $k$ with $x \in S_k$ and put $s_x = t_k[x]$. This does not depend on the choice of $k$, because the dual constraint between $c_k$ and $c_l$ forces $t_k[x] = t_l[x]$. Then $s|_{S_k} = t_k \in R_k$ for each $k$, so $s$ is a solution, and the two maps are inverse to each other. The values $s_x$ lie in the domains if the relations $R_k$ use only domain values, which we may assume after [node consistency](/node-consistency/). The hidden variable case is the same, with the constraints $h_k[x] = x$ playing the role of agreement. $\square$

**Size.** The dual encoding has $m$ variables with domains of size up to $d^r$, and up to $m(m-1)/2$ binary constraints, each a relation of up to $d^{2r}$ pairs if stored as a table. Many dual constraints are redundant: for each original variable $x$, the dual constraints that make the tuples agree on $x$ need only form a connected graph among the constraints that contain $x$. Removing the others gives a *join graph*. When the hypergraph of scopes is acyclic, some join graph is a tree, a *join tree*, and the [tree-structured CSP algorithm](/tree-structured-csp/) solves the dual in time polynomial in $\sum_k |R_k|$.

**Consistency on the encodings.** Let generalized arc consistency (GAC) on the original mean that each value of each variable has a supporting tuple in each constraint on it ([arc consistency](/arc-consistency/)).

> **Proposition (hidden variables).** Enforcing arc consistency on the hidden variable encoding deletes from the original domains exactly the values that GAC deletes on the original CSP.
>
> *Proof.* Let $D^\ast$ be the GAC closure of the original, and give each $h_k$ the tuples of $R_k$ whose values all lie in $D^\ast$. These domains are arc consistent: each such tuple has its values as supports, and each $a \in D^\ast_x$ has a supporting tuple in each $C_k \ni x$ with all values in $D^\ast$, by GAC. So the arc consistency closure $E$ of the encoding contains them, and $D^\ast_x \subseteq E_x$. Conversely, the original domains $E_x$ are GAC: a value $a \in E_x$ has, on the arc to $h_k$, a tuple $t \in E_{h_k}$ with $t[x] = a$, and each other value $t[y]$ lies in $E_y$ by arc consistency on the arc from $h_k$ to $y$. So $E_x \subseteq D^\ast_x$. $\square$

On the dual encoding, arc consistency can do more. Stergiou and Walsh (1999) showed that it is strictly stronger than GAC on the original: two tuples must agree on all shared variables at once, not one variable at a time. Bacchus and van Beek (1998) compared backtracking and [forward checking](/forward-checking/) on the two encodings with the same methods on the original problem, and found that none dominates in all cases.

**How the pages relate.** The [constraint graph](/constraint-graph/) page defines the primal, dual and incidence graphs as structures. This page is about the CSPs built on them, and about what propagation does on these CSPs. [Tree decompositions](/tree-decomposition/) and [bucket elimination](/bucket-elimination/) cluster variables until the dual of the clustered problem is a tree.

## Examples

**A small problem.** Five Boolean variables with $C_1$: $x_1 + x_2 + x_3 = 1$, $C_2$: $x_3 + x_4 + x_5 = 1$, and $C_3$: $x_1 \ne x_5$.

- *Dual encoding.* $c_1$ has the domain $\{100, 010, 001\}$ over $(x_1, x_2, x_3)$, $c_2$ has $\{100, 010, 001\}$ over $(x_3, x_4, x_5)$, and $c_3$ has $\{01, 10\}$ over $(x_1, x_5)$. The dual constraints say that $c_1$ and $c_2$ agree on $x_3$, $c_1$ and $c_3$ on $x_1$, and $c_2$ and $c_3$ on $x_5$. The dual graph is a triangle.
- *Hidden variable encoding.* The five $x_i$ and three hidden variables, joined by $3 + 3 + 2 = 8$ binary constraints, one for each pair of a constraint and a variable of its scope.
- *Solutions.* $x_3 = 1$ forces $x_1 = x_5 = 0$, which breaks $C_3$. So $x_3 = 0$, and the solutions are $(1, 0, 0, 1, 0)$ and $(0, 1, 0, 0, 1)$. In the dual these are $(c_1, c_2, c_3) = (100, 010, 10)$ and $(010, 001, 01)$.

**Dual arc consistency is stronger.** Take $x, y, z, w \in \{0, 1\}$ with the ternary constraints $C_1(x, y, z)$: $y = z$, and $C_2(y, z, w)$: $y \ne z$. On the original problem, GAC deletes nothing: $y = 0$ has the support $z = 0$ in $C_1$ and $z = 1$ in $C_2$, and so on for each value. In the dual, the tuples of $c_1$ have $y = z$ and those of $c_2$ have $y \ne z$, so no pair agrees on $(y, z)$, and arc consistency empties both domains. The problem has no solution.

**An acyclic problem.** A crossword puzzle has one constraint per word slot, whose allowed tuples are the dictionary words of that length. Its dual graph links two slots that cross. If the crossing pattern forms a tree, so does the dual graph, and the tree algorithm solves the puzzle without search.

## Where it is used

- **Using binary algorithms.** Theory and early algorithms for CSPs were written for binary constraints. The encodings show that this loses no generality, at a cost in size.
- **Tree clustering.** Join-tree clustering (Dechter and Pearl 1989) groups variables into clusters until the dual graph of the clusters is a tree, then solves it with the [tree-structured CSP algorithm](/tree-structured-csp/); this is the basis of [tree decomposition](/tree-decomposition/) methods.
- **Comparing propagation.** The encodings give a way to compare consistencies for non-binary constraints: arc consistency on the hidden encoding is GAC, and on the dual encoding it is stronger.
- **Databases.** A conjunctive query is a CSP whose constraints are database relations, and the dual graph of an acyclic query is the join tree used by Yannakakis's algorithm to evaluate it in polynomial time.
- **Solvers.** Modern solvers keep non-binary and [global constraints](/global-constraint/) as they are, with their own filtering, and use the encodings mainly for analysis and for special cases.

## References
