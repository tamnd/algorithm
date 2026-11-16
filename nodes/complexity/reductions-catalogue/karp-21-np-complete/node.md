---
tag: DZ6KGJ
kind: theorem
slug: karp-21-np-complete
name: Karp's reduction tree
area: complexity/reductions-catalogue
level: core
summary: The 20 reductions of Karp's 1972 tree from SAT to his other 20 problems, with full proofs of the 15 not proved on the list page and a corrected Steiner tree step.
prereqs: [karps-21-np-complete-problems, polynomial-time-reduction, transitivity-of-reductions]
see_also: [cook-levin-theorem, gadget-reduction, clique-problem, three-coloring, hamiltonian-cycle-np-completeness, zero-one-equations, knapsack-decision, garey-johnson-compendium]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103
    locator: Section 4, the list of problems (pages 94 and 95), Figure 1 (page 96), the reductions (pages 97 to 100) and the credits for some of them (pages 100 and 101)
  - paper: doi:10.1007/978-3-540-68279-0_8
    title: Richard M. Karp, Reducibility among combinatorial problems, reprinted in 50 Years of Integer Programming 1958 to 2008, Springer, 2010
    locator: the reprint of the 1972 paper, with the same Figure 1 and reductions
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Chapter 3 (the six basic NP-complete problems) and the appendix entries for Karp's problems
---

Karp's reduction tree is the diagram, Figure 1 of Karp (1972), that connects his 21 NP-complete problems. Its root is [SAT](/sat/), which Cook (1971) proved NP-complete, and each of its 20 edges is a polynomial-time many-one reduction from a parent problem to a child. By the [transitivity of reductions](/transitivity-of-reductions/), every problem in the tree is then NP-hard, and each is in NP. The page [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/) states the list, proves membership in NP and proves five edges. This page proves the other fifteen. One edge, exact cover to Steiner tree, does not work as printed; it is replaced here by a reduction from exact cover by 3-sets.

## Statement

All reductions are Karp (polynomial-time many-one) reductions, and numbers are in binary. The problems and their numbers are those of [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/). The tree has these edges, with each child below its parent:

- 1 SAT
  - 2 0-1 integer programming
  - 3 Clique
    - 4 Set packing
    - 5 Node cover
      - 6 Set covering
      - 7 Feedback node set
      - 8 Feedback arc set
      - 9 Directed Hamilton circuit
        - 10 Undirected Hamilton circuit
  - 11 SAT with at most 3 literals per clause
    - 12 Chromatic number
      - 13 Clique cover
      - 14 Exact cover
        - 15 Hitting set
        - 16 Steiner tree
        - 17 3-dimensional matching
        - 18 Knapsack
          - 19 Job sequencing
          - 20 Partition
            - 21 Max cut

**Theorem (Karp 1972).** For each edge from $A$ to $B$ in the tree, $A \le_m^p B$. The edge from 14 to 16 holds through 17: exact cover reduces to 3-dimensional matching, which reduces to exact cover by 3-sets, which reduces to Steiner tree. Since SAT is NP-complete and each problem is in NP, all 21 problems are NP-complete.

## In plain words

Karp took one problem known to be hard, satisfiability, and showed how to rewrite it as each of twenty other problems, often through a chain. Each rewriting is a recipe that turns any question of the first kind into a question of the second kind with the same answer, and it runs quickly.

If any problem in the tree had a fast method, the chain of recipes above it would give a fast method for satisfiability, and then for every problem whose answers can be checked quickly. So all 21 problems are equally hard in this sense. This page checks each recipe of the tree in both directions, except the five that the list page checks.

## Proof

The edges 1 to 3, 3 to 5, 14 to 18, 18 to 20 and 20 to 21 are proved on [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/). For each other edge, we give the map and prove both directions. Each map writes an object of size polynomial in its input, by a direct loop over the parts of the input, so each runs in polynomial time; we state the size where it is not obvious.

**1 to 2: SAT to 0-1 integer programming.** Let the clauses be $C_1, \ldots, C_p$ over $x_1, \ldots, x_n$, with no variable twice in one clause. Karp sets $c_{ij} = 1$ if $x_j \in C_i$, $c_{ij} = -1$ if $\lnot x_j \in C_i$ and $c_{ij} = 0$ otherwise, and $b_i = 1 - (\text{number of negated literals in } C_i)$, and asks for $x \in \{0, 1\}^n$ with $\sum_j c_{ij} x_j \ge b_i$. For any $x$, $\sum_j c_{ij} x_j + (\text{number of negated literals in } C_i)$ is the number of true literals of $C_i$, so the inequality says that $C_i$ has a true literal. Karp's problem 2 is stated as $Cx = d$. For that form, add to row $i$ new 0-1 variables $s_{i,1}, \ldots, s_{i, \lvert C_i \rvert - 1}$ with coefficient $-1$ and ask for equality with $b_i$. *Forward:* for a satisfying assignment with $t_i \ge 1$ true literals in $C_i$, set $t_i - 1$ of the $s_{i, \cdot}$ to 1. *Backward:* from any 0-1 solution, row $i$ says that $C_i$ has $1 + \sum_r s_{i,r} \ge 1$ true literals.

**1 to 11: SAT to SAT with at most 3 literals per clause.** Replace a clause $(\sigma_1 \lor \cdots \lor \sigma_m)$ with $m > 3$ by the clauses $(\sigma_1 \lor \sigma_2 \lor u)$, $(\sigma_3 \lor \cdots \lor \sigma_m \lor \lnot u)$ and $(\lnot \sigma_i \lor u)$ for $3 \le i \le m$, with a new variable $u$, and repeat on the second clause until all clauses are short. The new clauses say that $u$ is true if and only if one of $\sigma_3, \ldots, \sigma_m$ is true. *Forward:* extend a satisfying assignment by this value of $u$; then $(\sigma_1 \lor \sigma_2 \lor u)$ holds since the old clause held. *Backward:* in any satisfying assignment, $u$ equals $\sigma_3 \lor \cdots \lor \sigma_m$, so $(\sigma_1 \lor \sigma_2 \lor u)$ is the old clause. A clause of length $m$ gives $O(m^2)$ literals in total, which is polynomial.

**3 to 4: Clique to set packing.** For each node $i$ of $G$, let $S_i$ be the set of non-edges $\{i, j\}$ with $j \ne i$; ask for $k$ pairwise disjoint sets. Two sets $S_i$ and $S_j$ can share only $\{i, j\}$, so they are disjoint if and only if $\{i, j\}$ is an edge. So $k$ disjoint sets are exactly a $k$-clique, in both directions. See [clique problem](/clique-problem/).

**5 to 6: Node cover to set covering.** For each node $j$, let $S_j$ be the set of edges at $j$, and keep the bound $l$. A set $R$ of nodes covers all edges if and only if $\bigcup_{j \in R} S_j$ is the set of all edges, which is the union of the whole family. Isolated nodes give empty sets and change nothing.

**5 to 7: Node cover to feedback node set.** Replace each edge $\{u, v\}$ by the two arcs $(u, v)$ and $(v, u)$, and keep $l$. *Forward:* if $R$ covers every edge, removing $R$ leaves no arcs, so no cycles. *Backward:* if $R$ meets every directed cycle, it meets each 2-cycle $u \to v \to u$, so it contains $u$ or $v$ for every edge.

**5 to 8: Node cover to feedback arc set.** Make nodes $\langle u, 0 \rangle$ and $\langle u, 1 \rangle$ for each node $u$, the arc $\langle u, 0 \rangle \to \langle u, 1 \rangle$, and for each edge $\{u, v\}$ the arcs $\langle u, 1 \rangle \to \langle v, 0 \rangle$ and $\langle v, 1 \rangle \to \langle u, 0 \rangle$; keep $l$. *Forward:* for a cover $R$, remove the arcs $\langle u, 0 \rangle \to \langle u, 1 \rangle$ with $u \in R$. A directed cycle alternates between inner arcs and edge arcs, so it passes the inner arcs of two adjacent nodes $u$ and $v$, and one of them is removed. *Backward:* take any feedback arc set $F$ with $\lvert F \rvert \le l$. Replace each arc $\langle u, 1 \rangle \to \langle v, 0 \rangle$ of $F$ by $\langle v, 0 \rangle \to \langle v, 1 \rangle$; every cycle through the old arc uses the new one next, so the result is still a feedback arc set and is not larger. Now $F$ has only inner arcs; let $R$ be their nodes. For each edge $\{u, v\}$, the cycle $\langle u, 0 \rangle \langle u, 1 \rangle \langle v, 0 \rangle \langle v, 1 \rangle$ must lose an arc, so $u \in R$ or $v \in R$.

**5 to 9: Node cover to directed Hamilton circuit (Karp credits Lawler).** Remove isolated nodes and replace $l$ by $\min(l, \text{number of nodes left})$, as on [Hamiltonian cycle NP-completeness](/hamiltonian-cycle-np-completeness/). Make selector nodes $a_1, \ldots, a_l$ and, for each node $u$ and each edge $e$ at $u$, nodes $\langle u, e, 0 \rangle$ and $\langle u, e, 1 \rangle$. The arcs are $\langle u, e, 0 \rangle \to \langle u, e, 1 \rangle$; for $e = \{u, v\}$, both arcs between $\langle u, e, \alpha \rangle$ and $\langle v, e, \alpha \rangle$ for $\alpha = 0, 1$; for the edges $e_1, \ldots, e_d$ at $u$ in a fixed order, $\langle u, e_i, 1 \rangle \to \langle u, e_{i+1}, 0 \rangle$; and $\langle u, e_d, 1 \rangle \to a_f$ and $a_f \to \langle u, e_1, 0 \rangle$ for all $f$.

*Gadget fact.* In a Hamilton circuit, a walk that enters the four nodes of $e = \{u, v\}$ at $\langle u, e, 0 \rangle$ from outside leaves them at $\langle u, e, 1 \rangle$: either directly, or by $\langle u, e, 0 \rangle \to \langle v, e, 0 \rangle \to \langle v, e, 1 \rangle \to \langle u, e, 1 \rangle$. Indeed, if it goes to $\langle v, e, 0 \rangle$, the out-neighbors of that node are $\langle v, e, 1 \rangle$ and $\langle u, e, 0 \rangle$, which is already used, so it goes on to $\langle v, e, 1 \rangle$. The in-neighbors of $\langle u, e, 1 \rangle$ are $\langle u, e, 0 \rangle$, which already has its successor, and $\langle v, e, 1 \rangle$, so the walk goes from $\langle v, e, 1 \rangle$ to $\langle u, e, 1 \rangle$. If it goes to $\langle u, e, 1 \rangle$ directly, then $\langle v, e, 0 \rangle$ must be entered from the chain of $v$ and goes on to $\langle v, e, 1 \rangle$. *Forward:* for a cover $\{c_1, \ldots, c_l\}$, run from $a_f$ through the chain of $c_f$, taking the detour through $\langle v, e, \cdot \rangle$ exactly when $v$ is not in the cover, and go on to $a_{f+1}$. *Backward:* by the gadget fact, the path between two selectors follows the chain of one node, so the $l$ paths belong to $l$ nodes, and every gadget, being visited, is on the chain of one of its two ends. These nodes form a cover.

**9 to 10: Directed to undirected Hamilton circuit (Karp credits Tarjan).** Replace each node $u$ by a path $u_0 - u_1 - u_2$ and each arc $(u, v)$ by the edge $u_2 - v_0$. *Forward:* a directed circuit $u, v, \ldots$ becomes $u_0, u_1, u_2, v_0, v_1, v_2, \ldots$. *Backward:* in any Hamilton circuit, $u_1$ has degree 2, so the circuit contains $u_0 - u_1 - u_2$. Walk the circuit in the direction in which some $u$ is crossed as $u_0, u_1, u_2$. After $u_2$ comes some $v_0$ with $(u, v)$ an arc, then $v_1, v_2$, and so on. So every path is crossed from 0 to 2, and the order of the paths is a directed Hamilton circuit.

**11 to 12: SAT with at most 3 literals to chromatic number.** Let the variables be $x_1, \ldots, x_m$ and the clauses $D_1, \ldots, D_r$; add unused variables if needed so that $m \ge 4$. Make nodes $x_i$, $\bar x_i$, $v_i$ for $1 \le i \le m$ and $D_f$ for $1 \le f \le r$, with the edges $x_i - \bar x_i$; $v_i - v_j$ for $i \ne j$; $v_i - x_j$ and $v_i - \bar x_j$ for $i \ne j$; and $x_i - D_f$ (or $\bar x_i - D_f$) when that literal is not in $D_f$. Ask for a coloring with $k = m + 1$ colors. *Forward:* give $v_i$ color $i$, the true literal of variable $i$ color $i$, the false one color $m + 1$, and $D_f$ the color $i$ of a true literal of $D_f$. The only other node with color $i$ next to $D_f$ could be that literal, which is in $D_f$, so no edge joins them. *Backward:* take any $(m+1)$-coloring. The $v_i$ form a clique, so they use $m$ colors; call the color of $v_i$ color $i$ and the last color $\ast$. Each literal node of variable $i$ is adjacent to all $v_j$ with $j \ne i$, so it has color $i$ or $\ast$, and the two literals of $x_i$ differ. Call a literal true if it has color $i$. A clause $D_f$ has at most 3 literals and $m \ge 4$, so some variable $j$ has neither literal in $D_f$; $D_f$ is adjacent to both, one of which has color $\ast$, so $D_f$ has some color $i \le m$. The literal of variable $i$ with color $i$ is not adjacent to $D_f$, so it is in $D_f$, and it is true.

**12 to 13: Chromatic number to clique cover.** Map $(G, k)$ to the complement $\bar G$ with $l = k$. A color class of $G$ is an independent set of $G$, which is a clique of $\bar G$, so $k$ colors are exactly $k$ cliques that cover the nodes of $\bar G$.

**12 to 14: Chromatic number to exact cover.** The elements are the nodes $u$, the edges $e$, and the triples $(u, e, f)$ for each edge $e$, each end $u$ of $e$ and each color $1 \le f \le k$. The sets are, for each node $u$ and color $f$, the set $\{u\} \cup \{(u, e, f) : e \ni u\}$; and for each edge $e = \{u, v\}$ and colors $f \ne g$, the set $\{e\} \cup \{(u, e, f') : f' \ne f\} \cup \{(v, e, g') : g' \ne g\}$. *Forward:* for a proper coloring $c$, take the node sets for $(u, c(u))$ and the edge sets for $(c(u), c(v))$; each element $(u, e, f')$ is covered by the node set if $f' = c(u)$ and by the edge set otherwise. *Backward:* in any exact cover, each node $u$ is in one node set, which defines $c(u)$, and each edge $e$ is in one edge set, with colors $f \ne g$. The element $(u, e, c(u))$ is in the node set, so the edge set must avoid it, which forces $f = c(u)$, and likewise $g = c(v)$. So $c(u) \ne c(v)$ for every edge.

**14 to 15: Exact cover to hitting set.** Karp's hitting set asks for a set $W$ with exactly one element in each given set. For each element $u$, let $U_u$ be the set of indices $j$ with $u \in S_j$. A set $W$ of indices meets each $U_u$ in exactly one index if and only if the sets $S_j$, $j \in W$, contain each element exactly once.

**14 to 16: Exact cover to Steiner tree, corrected.** Karp's map makes a node $n_0$, a node per set $S_j$ and a node per element, with the edge $n_0 - S_j$ of weight $\lvert S_j \rvert$ and the edges $S_j - u$ of weight 0 for $u \in S_j$, the required nodes $n_0$ and all elements, and the bound $k = \lvert \bigcup_j S_j \rvert$. This map is not correct, because a tree can pass from one set node to another through an element node at no cost. Take $S_1 = \{1, 2\}$ and $S_2 = \{2, 3\}$. They have no exact cover, but the tree $n_0 - S_1$, $S_1 - 1$, $S_1 - 2$, $2 - S_2$, $S_2 - 3$ has weight $2 \le k = 3$. A script found that the printed map gave the wrong answer on 53 of 200 random families.

A correct reduction starts from *exact cover by 3-sets* (X3C): sets of size 3 over $3q$ elements. X3C contains 3-dimensional matching (forget which coordinate an element comes from), and edge 14 to 17 below reduces exact cover to 3-dimensional matching, so X3C is NP-complete. Map an X3C instance to the same graph with every edge of weight 1, the same required nodes, and $k = 4q$. *Forward:* an exact cover by $q$ sets gives the tree with the $q$ edges $n_0 - S_j$ and the $3q$ edges from these sets to their elements, of weight $4q$. *Backward:* take any tree of weight at most $4q$ that contains $n_0$ and all elements, and let $s$ be its number of set nodes. It has $1 + 3q + s$ nodes, so $3q + s \le 4q$ edges, and $s \le q$. Each element node is adjacent only to set nodes, and each set has 3 elements, so the set nodes in the tree contain all $3q$ elements only if $s \ge q$. So $s = q$, and $q$ sets of size 3 that contain $3q$ elements are disjoint: an exact cover.

**14 to 17: Exact cover to 3-dimensional matching (Karp credits Lawler).** Let $T = \{(u, S_j) : u \in S_j\}$. If some element is in no set, output a fixed no-instance. Fix, for each element $u$, one pair $\alpha(u) = (u, S_j) \in T$, and let $\pi$ be the permutation of $T$ that cycles through the pairs of each set $S_j$. The triples are $(\alpha(u), (u, S_j), (u, S_j))$ for every pair $(u, S_j)$ (type 1), and $(\beta, \sigma, \pi(\sigma))$ for every $\beta \in T$ that is not an $\alpha(u)$ and every $\sigma \in T$ (type 2). We ask for $\lvert T \rvert$ triples that agree in no coordinate. *Backward:* in any such matching, the first coordinates are all of $T$; the triple with first coordinate $\alpha(u)$ is of type 1 and picks a pair $(u, S_j)$. Let $A$ be the second coordinates of the type 1 triples. The third coordinates are $A$ and $\pi(T \setminus A)$, and they are all of $T$, so $\pi(T \setminus A) = T \setminus A$. So $A$ is a union of cycles of $\pi$, that is, all pairs of the sets in some family $\mathcal{C}$. $A$ has exactly one pair per element, so each element is in exactly one set of $\mathcal{C}$. *Forward:* for an exact cover $\mathcal{C}$, take the type 1 triples for the pairs of the sets in $\mathcal{C}$, and match the $\beta$'s that are not an $\alpha(u)$ one to one with the pairs $\sigma$ of the sets not in $\mathcal{C}$, using $(\beta, \sigma, \pi(\sigma))$. If there are $n$ elements, both groups have $\lvert T \rvert - n$ members, so the matching exists, and $\pi$ maps the pairs of sets outside $\mathcal{C}$ onto themselves.

**18 to 19: Knapsack to job sequencing.** Karp's knapsack asks for a subset of $a_1, \ldots, a_r$ with sum $b$. Make $r$ jobs with execution time $a_j$, deadline $b$ and penalty $a_j$, and set $k = \sum_j a_j - b$. All deadlines are equal, so in any order the jobs that finish on time form a prefix with total time at most $b$, and the penalty is $\sum_j a_j$ minus that total. *Forward:* run a subset with sum $b$ first; the penalty is $\sum_j a_j - b$. *Backward:* if the penalty is at most $\sum_j a_j - b$, the on-time jobs have total time at least $b$ and at most $b$, so they form a subset with sum $b$.

Together with the five edges on [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/), membership in NP and the [Cook-Levin theorem](/cook-levin-theorem/), this proves the theorem. $\blacksquare$

**Checks by script.** A script built each of the fifteen maps above on random small instances and compared the answers with brute force. The numbers of yes-instances and no-instances were: SAT to 0-1 IP 152 and 48; SAT to 3-SAT 272 and 20; clique to set packing 86 and 114; node cover to set covering 142 and 31; to feedback node set 168 and 32; to feedback arc set 135 and 15; to directed Hamilton circuit 86 and 9; directed to undirected Hamilton circuit 42 and 258; 3-SAT to chromatic number 62 and 58; chromatic number to clique cover 104 and 46; to exact cover 66 and 54; exact cover to hitting set 138 and 62; X3C to Steiner tree 85 and 65; exact cover to 3DM 128 and 72; knapsack to sequencing 93 and 107. All answers agreed.

## Consequences

- **Many NP-complete problems at once.** Each edge adds a problem, and later work added thousands more by reductions from these; see [Garey and Johnson's compendium](/garey-johnson-compendium/).
- **Hardness of optimization.** The optimization versions of clique, node cover, set covering, chromatic number, Steiner tree, knapsack and max cut are NP-hard, so they have no polynomial-time algorithms unless P = NP.
- **Strong and weak hardness.** Edges 14 to 18, 18 to 19 and 18 to 20 make numbers with many digits, so they give only weak NP-hardness. The other edges make no large numbers, so chromatic number, Steiner tree with unit weights and the graph problems are strongly NP-complete; see [strong NP-hardness](/strong-np-hardness/).

## Tightness

- **Printed details.** Two details of the printed paper need care. For chromatic number, Karp prints the bound as $r + 1$, where $r$ is the number of clauses, but the proof needs $m + 1$, where $m$ is the number of variables. A script built the graph for the unsatisfiable formula with all 8 clauses on $x_1, x_2, x_3$, with $m = 4$: it is not 5-colorable, but it is 9-colorable, so the bound $r + 1 = 9$ gives a wrong answer. Also, the printed Steiner tree map fails, as shown above.
- **Weaker problems.** Some neighbors of Karp's problems are in P: 2-SAT, 2-colorability, Euler circuits and matching in bipartite graphs. The tree uses 3 literals per clause and 3 colors because 2 is not enough.

## History

Cook (1971) proved SAT NP-complete under Turing reductions and reduced it to clique and to 3-SAT. Karp (1972) introduced polynomial-time many-one reductions in this sense and proved 21 problems NP-complete with the tree above; he credits some reductions to Lawler and Tarjan, among others. Garey and Johnson (1979) rebuilt the tree around six basic problems (3-SAT, 3-dimensional matching, vertex cover, clique, Hamiltonian circuit and partition), with reductions that start from 3-SAT and 3-dimensional matching, and their proofs are the ones most textbooks use.

## References
