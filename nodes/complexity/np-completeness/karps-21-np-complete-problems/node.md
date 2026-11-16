---
tag: 26XYBK
kind: theorem
slug: karps-21-np-complete-problems
name: Karp's 21 NP-complete problems
aliases:
- Karp's list of NP-complete problems
area: complexity/np-completeness
level: intro
summary: Karp (1972) proved 21 classic combinatorial problems NP-complete, among them clique, Hamilton circuit and knapsack, by a tree of Karp reductions that starts at SAT.
prereqs: [cook-levin-theorem, np-complete, polynomial-time-reduction]
see_also: [karp-21-np-complete, garey-johnson-compendium, 3-sat, clique-problem, vertex-cover, partition-problem, maximum-cut, strong-np-hardness]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (eds.), Complexity of Computer Computations, Plenum Press (1972), 85 to 103
    locator: Definition 5 and Theorem 3 (p. 93), the Main Theorem and the list of 21 problems (pp. 94 to 97), Figure 1 (p. 96), the reductions (pp. 97 to 100), the credits and the automata problems (pp. 100 to 101)
  - paper: doi:10.1007/978-3-540-68279-0_8
    title: Richard M. Karp, Reducibility among combinatorial problems, reprint with an introduction by the author, in M. Junger et al. (eds.), 50 Years of Integer Programming 1958-2008, Springer (2010), 219 to 241
    locator: Introduction by Richard M. Karp, pp. 219 to 220 (the seminar at Knuth's home, the IBM symposium, which Karp recalls as April 1972, the undirected Hamilton circuit reduction by Lawler and Tarjan)
  - paper: doi:10.1145/800157.805047
    title: Stephen A. Cook, The complexity of theorem-proving procedures, Proceedings of the 3rd ACM Symposium on Theory of Computing (1971), 151 to 158
    locator: Theorem 1 (the root of the tree) and the reduction to clauses with at most 3 literals
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Section 3.1 (six basic NP-complete problems, all of them on Karp's list or close variants)
  - paper: "David S. Johnson, A brief history of NP-completeness, 1954-2012, Documenta Mathematica, Extra Volume: Optimization Stories (2012), 359 to 376"
    locator: the sections on Cook, Karp and Levin
---

Karp's 21 NP-complete problems are the problems in the Main Theorem of Richard Karp's 1972 paper "Reducibility among combinatorial problems". Cook had shown in 1971 that [SAT](/sat/) is hard for NP ([Cook-Levin theorem](/cook-levin-theorem/)). Karp showed that 20 well-known problems from graph theory, scheduling, covering and integer programming are just as hard: each is in NP, and SAT reduces to each of them by a chain of [polynomial-time reductions](/polynomial-time-reduction/) (Karp reductions). So all 21 are [NP-complete](/np-complete/), and a polynomial-time algorithm for any one of them would give P = NP. The paper showed that NP-completeness is common, not a curiosity of logic.

## Statement

All reductions on this page are polynomial-time many-one (Karp) reductions, written $\le_m^p$. Numbers are in binary.

**Theorem (Karp 1972, Main Theorem).** Each of the 21 problems below is in NP, and SAT $\le_m^p$ each of them. So each is NP-complete.

The table uses Karp's numbering and his definitions. The last column is the parent in Karp's Figure 1: the problem from which Karp reduced.

| # | Problem | Yes-instance when | Reduced from |
|---|---|---|---|
| 1 | [Satisfiability](/sat/) | the CNF clauses have a common satisfying assignment | root (Cook 1971) |
| 2 | [0-1 integer programming](/binary-integer-programming/) | some $x \in \{0,1\}^n$ has $Cx = d$ | 1 |
| 3 | [Clique](/clique-problem/) | $G$ has $k$ mutually adjacent nodes | 1 |
| 4 | [Set packing](/set-packing/) | the family has $l$ mutually disjoint sets | 3 |
| 5 | [Node cover](/vertex-cover/) | some $l$ or fewer nodes touch every edge | 3 |
| 6 | [Set covering](/set-cover/) | $k$ or fewer sets have the same union as the whole family | 5 |
| 7 | [Feedback node set](/feedback-vertex-set-problem/) | $k$ nodes meet every directed cycle | 5 |
| 8 | [Feedback arc set](/feedback-arc-set-problem/) | $k$ arcs meet every directed cycle | 5 |
| 9 | [Directed Hamilton circuit](/hamiltonian-cycle-problem/) | a directed cycle visits each node exactly once | 5 |
| 10 | [Undirected Hamilton circuit](/hamiltonian-cycle-problem/) | a cycle visits each node exactly once | 9 |
| 11 | [Satisfiability with at most 3 literals per clause](/3-sat/) | as 1, with at most 3 literals per clause | 1 |
| 12 | [Chromatic number](/chromatic-number/) | $G$ has a proper coloring with $k$ colors | 11 |
| 13 | [Clique cover](/clique-cover/) | the nodes are the union of $l$ or fewer cliques | 12 |
| 14 | [Exact cover](/exact-cover/) | some subfamily covers each element exactly once | 12 |
| 15 | [Hitting set](/hitting-set/) | some set $W$ has exactly one element in each $U_i$ | 14 |
| 16 | [Steiner tree](/steiner-tree-problem/) | a subtree of weight at most $k$ contains every node of $R$ | 14 |
| 17 | [3-dimensional matching](/three-dimensional-matching/) | $\lvert T \rvert$ triples of $U \subseteq T \times T \times T$ agree in no coordinate | 14 |
| 18 | [Knapsack](/subset-sum-problem/) | some 0-1 vector has $\sum_j a_j x_j = b$ | 14 |
| 19 | Job sequencing | some order of the jobs has total penalty of late jobs at most $k$ | 18 |
| 20 | [Partition](/partition-problem/) | the numbers split into two parts of equal sum | 18 |
| 21 | [Max cut](/maximum-cut/) | some cut of the weighted graph has weight at least $W$ | 20 |

Some of Karp's definitions differ from the ones used today:

- His knapsack is the subset sum form, with no values and no capacity. The version with values and weights is on the [knapsack decision](/knapsack-decision/) page.
- His hitting set asks for exactly one element in each set, so it is an exact version; the usual hitting set asks for at least one, within a size bound.
- Problem 11 allows clauses of 1, 2 or 3 literals. The form with exactly 3 literals is also NP-complete.
- For feedback node set and feedback arc set the printed property omits the size bound, but the input includes $k$, and the bound $|R| \le k$ is clearly meant.
- Max cut has integer edge weights. Job sequencing has execution times, deadlines and penalties.

## In plain words

Cook found one hard problem: deciding whether a logic formula can be made true. Karp took twenty other problems that people in operations research and graph theory had tried to solve fast for years. For each one he showed how to translate an instance of a problem already known to be hard into an instance of the new problem, quickly and with the same answer. The translations form a tree with satisfiability at the root. So a fast method for any problem in the tree would give a fast method for satisfiability, and then for every problem whose answers are easy to check. Since nobody had found a fast method for any of them, the list was strong evidence that all twenty-one are hard. It also showed people how to prove that a new problem is hard.

## Proof

The full membership checks and five of the twenty reductions are on [the proof page](proofs/main.md). This section gives the plan.

**Membership.** Each problem has a short certificate that a deterministic multitape Turing machine checks in polynomial time: an assignment for 1 and 11, a 0-1 vector for 2, a set of nodes, arcs, edges or sets for 3 to 8 and 13 to 17, an order of the nodes for 9 and 10, a coloring for 12, a subset of the numbers for 18 and 20, an order of the jobs for 19, and one side of the cut for 21.

**Hardness.** SAT is NP-complete by the [Cook-Levin theorem](/cook-levin-theorem/). Each edge of the tree in the table is a Karp reduction from the parent to the child, and Karp reductions compose. So for each problem $\Pi$, the path from SAT to $\Pi$ gives SAT $\le_m^p \Pi$, and every NP language reduces to $\Pi$ through SAT.

**The five reductions proved on the proof page.** Each comes with the map, its cost, both directions and a run of a script.

- SAT to clique: one node per literal occurrence, edges between compatible literals in different clauses, $k$ = number of clauses. On $(x_1 \lor x_2) \land (\lnot x_1 \lor x_2 \lor x_3) \land (\lnot x_2 \lor \lnot x_3)$ the graph has 7 nodes and 12 edges; the formula has 3 satisfying assignments and the graph has 4 cliques of size 3.
- Clique to node cover: take the complement graph and $l = |N| - k$. In the example, the complement has 9 edges and exactly 4 node covers of size 4.
- Exact cover to knapsack: write each set as a number in base $d = r + 1$, so that sums never carry. For the family $\{1,2\}, \{3,4\}, \{2,3\}, \{1\}, \{4\}$ the numbers are $7, 252, 42, 1, 216$ with target $259$, and the two subsets with sum 259 are the two exact covers.
- Knapsack to partition: add the numbers $b + 1$ and $\sum_i a_i + 1 - b$. This needs $b \le \sum_i a_i$; otherwise the map outputs a fixed no-instance.
- Partition to max cut: the complete graph with weights $c_i c_j$. A cut with side sum $\sigma$ has weight $\sigma(C - \sigma)$, where $C = \sum_i c_i$, so the right threshold is $W = \lceil C^2/4 \rceil$.

A script also checked three of these maps against brute force on random instances (seed 1972): no mismatch on 300 formulas for SAT to clique, on 500 instances for knapsack to partition, and on 500 instances for partition to max cut.

## Consequences

- **All or none.** By Karp's Theorem 3, either all complete problems are in P or none is, and the first holds if and only if P = NP. So each of the 21 problems is in P if and only if P = NP, which is open.
- **Complements.** The complement of each problem is [coNP-complete](/co-np-complete/): "this graph has no Hamilton circuit", "these numbers have no partition".
- **Optimization.** The optimization forms, such as the largest clique, the smallest node cover, the chromatic number and the largest cut, are [NP-hard](/np-hard/) under Cook reductions: one call to an optimizer answers the decision question.
- **Integer programming.** Since 0-1 integer programming is NP-complete, integer programming is NP-hard. Linear programming is different: it is [in P](/lp-in-p/).
- **A starting set for new proofs.** A new problem $\Pi$ in NP is NP-complete as soon as one of the 21 reduces to it. Garey and Johnson (Section 3.1) build their method on six basic problems: 3-SAT, 3-dimensional matching, vertex cover, clique, Hamiltonian circuit and partition. All six are on Karp's list, 3-SAT in the form with exactly 3 literals per clause. Their [compendium](/garey-johnson-compendium/) grew from this start.

## Tightness

The theorem does not separate P from NP, and nothing in it can: it proves only that the 21 problems are equally hard. Several small changes to the problems make them easy, which shows where the hardness lies.

- **Clause width.** With at most 2 literals per clause, [2-SAT](/2-sat/) is solvable in linear time. So the bound 3 in problem 11 cannot drop to 2 unless P = NP.
- **Colors.** With $k = 2$, chromatic number asks whether $G$ is bipartite, which breadth-first search decides. With $k = 3$ the problem is already NP-complete ([three-coloring](/three-coloring/)).
- **Dimension.** The 2-dimensional form of problem 17 is perfect [bipartite matching](/bipartite-matching/), which is in P.
- **Size of the numbers.** Knapsack, partition and job sequencing have algorithms that run in time polynomial in the input length and the value of the numbers ([pseudo-polynomial time](/pseudo-polynomial-time/)); for example, dynamic programming decides knapsack in $O(rb)$ steps. So these problems are hard only when the numbers are large, and Karp's reductions produce large numbers: in exact cover to knapsack, the numbers have about $t \log_2(r + 1)$ bits. They are [weakly NP-hard](/weak-np-hardness/) by these reductions. The weights in Karp's map to max cut are products $c_i c_j$ and are large in the same way. By contrast, the weights in his map from exact cover to Steiner tree are set sizes, at most the number of elements, so that reduction works with weights in unary ([strong NP-hardness](/strong-np-hardness/)).

## History

Cook's 1971 paper showed that every set accepted in polynomial time by a nondeterministic machine reduces to the DNF tautologies, and showed the reduction from SAT to clauses with at most 3 literals. Karp wrote in 2010 that it was "immediately apparent" to him that many familiar combinatorial problems "were likely to have the same universal role as satisfiability". He first presented the results at an informal seminar at Donald Knuth's home and then at an IBM symposium at Yorktown Heights, held on 20 to 22 March 1972 (Karp recalled it in 2010 as April); the paper appeared in the proceedings, edited by Miller and Thatcher. Karp used many-one reductions and called the problems "complete" (Definition 5). The term "NP-complete" came later, from Knuth's 1974 poll. Leonid Levin, working independently, published similar results in 1973.

Karp credits several reductions to others (pages 100 to 101). The reduction from SAT to clique is implicit in Cook's work and was also known to Raymond Reiter. Node cover to feedback node set came from the Algorithms Seminar at Cornell. Node cover to feedback arc set was found by Lawler and Karp, and exact cover to 3-dimensional matching by Lawler. Tarjan showed exact cover to directed Hamilton circuit and, independently, Lawler showed node cover to directed Hamilton circuit; Tarjan also gave the step from directed to undirected Hamilton circuit. In the 2010 introduction, Karp says that he failed to prove the undirected case himself.

Karp also listed three problems from automata theory to which every complete problem reduces but which were not known to be in NP: equivalence of regular expressions, equivalence of nondeterministic finite automata, and context-sensitive recognition. He named problems in NP that he could not classify, among them graph isomorphism, nonprimes and linear inequalities. Linear programming is now known to be [in P](/lp-in-p/), and so is primality ([AKS primality test](/aks-primality-test/)). [Graph isomorphism](/graph-isomorphism-problem/) is still not known to be in P or NP-complete.

## References
