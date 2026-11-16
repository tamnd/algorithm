---
tag: 5W5X6B
kind: problem
slug: clique-problem
name: Clique problem
aliases:
- maximum clique decision
area: complexity/reductions-catalogue
level: core
summary: Decide whether a graph has k pairwise adjacent vertices. NP-complete by Karp's reduction from SAT; independent set and vertex cover are the same problem on the complement graph.
prereqs: [np-complete, 3-sat, polynomial-time-reduction, clique]
see_also: [maximum-clique, clique-decision, independent-set, vertex-cover, parameterized-clique, clique-inapproximability, karps-21-np-complete-problems, gadget-reduction]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103
    locator: Section 4, problem 3 (CLIQUE), the reduction SATISFIABILITY to CLIQUE, and the reductions from CLIQUE to SET PACKING and NODE COVER
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage, 2013
    locator: Section 7.4, Theorem 7.32 (3SAT is polynomial time reducible to CLIQUE)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 3.1.3 (VERTEX COVER and CLIQUE) and Appendix A1.2, problem GT19 (Clique)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 34.5.1 (the clique problem) and Section 34.5.2 (the vertex-cover problem)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms, McGraw-Hill, 2006
    locator: Section 8.3 (3SAT to INDEPENDENT SET, and INDEPENDENT SET to VERTEX COVER and to CLIQUE)
  - paper: doi:10.4086/toc.2007.v003a006
    title: David Zuckerman, Linear degree extractors and the inapproximability of max clique and chromatic number, Theory of Computing 3, 2007
    locator: the main theorem (no n^(1-e)-approximation for max clique unless P = NP)
  - paper: "Jaroslav Nešetřil and Svatopluk Poljak, On the complexity of the subgraph problem, Commentationes Mathematicae Universitatis Carolinae 26(2), 1985"
    locator: the reduction of k-clique detection to triangle detection and fast matrix multiplication
---

The clique problem asks whether a graph has $k$ vertices that are all adjacent to each other. It is one of [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/): Karp (1972) reduced [SAT](/sat/) to it, and the same reduction from [3-SAT](/3-sat/) is the textbook first example of a reduction between two unlike problems. On the complement graph a clique is an [independent set](/independent-set/), and the vertices outside an independent set form a [vertex cover](/vertex-cover/), so these three problems are one problem in three forms. This page is the decision problem and its NP-completeness. The optimization form, with its algorithms, is [maximum clique](/maximum-clique/).

## In plain words

At a party, a clique is a group of guests in which every guest knows every other guest. The question is whether the party has such a group of a given size.

Checking a proposed group is easy: look at each pair once. Finding a group is another matter. The number of possible groups grows very fast with the size of the party, and no method is known that avoids this growth in the worst case.

The reason is that the clique question can express logic puzzles. For each clause of a formula, put one guest for each of its literals. Two guests know each other when they come from different clauses and do not contradict each other. A group with one guest from every clause is then a consistent choice of one true literal per clause, which is exactly a satisfying assignment.

## Definition

**Instance.** A graph $G = (V, E)$ and a positive integer $k \le \lvert V \rvert$.

**Question.** Is there a set $C \subseteq V$ with $\lvert C \rvert = k$ such that $\{u, v\} \in E$ for every two distinct $u, v \in C$?

**Encoding.** The graph is given as an adjacency list or an adjacency matrix, and $k$ in binary. Since $k \le \lvert V \rvert$, the encoding of $k$ does not change the input length by more than a logarithmic term. The certificate is the set $C$. With an adjacency matrix, the verifier checks the $\binom{k}{2}$ pairs in $O(k^2)$ lookups, so the problem is in NP. Classes are defined on the [multitape Turing machine](/multitape-turing-machine/), and the verifier runs in polynomial time there too.

**Complexity.** The problem is [NP-complete](/np-complete/) under Karp (polynomial-time many-one) reductions. Karp (1972) reduced SAT to it; Garey and Johnson (Section 3.1.3) and Sipser (Theorem 7.32) reduce 3-SAT to it. It is in P if and only if P = NP, which is open.

## Variants

- **Optimization.** Find the largest clique; its size is the clique number $\omega(G)$. See [maximum clique](/maximum-clique/). One call to an algorithm for the optimization form answers the decision question, and binary search over $k$ with the decision form gives $\omega(G)$.
- **Independent set.** Is there a set of $k$ vertices with no edge between any two? $C$ is a clique of $G$ if and only if $C$ is an independent set of the complement graph $\bar G$, which has an edge exactly where $G$ has none.
- **Vertex cover.** Is there a set of at most $\ell$ vertices that touches every edge? $S$ is an independent set of a graph if and only if $V \setminus S$ is a vertex cover of that graph. So $G$ has a $k$-clique if and only if $\bar G$ has a vertex cover of size $\lvert V \rvert - k$.
- **Fixed $k$.** For each fixed $k$ the problem is in P: test all $\binom{n}{k}$ sets, where $n = \lvert V \rvert$. With $k$ as a parameter it is W[1]-complete; see [parameterized clique](/parameterized-clique/) and [clique W[1]-completeness](/clique-w1-completeness/).
- **Restricted graphs.** A planar graph has no clique on 5 vertices, because $K_5$ is not planar, so on [planar graphs](/planar-graph/) the problem is in P by testing all sets of at most 4 vertices. In the same way, a graph with maximum degree $d$ has no clique larger than $d + 1$.

## Examples

**The reduction from 3-SAT on a small formula.** Take
$$\varphi = (x_1 \lor x_2 \lor \lnot x_3) \land (\lnot x_1 \lor x_2 \lor x_3) \land (\lnot x_1 \lor \lnot x_2 \lor \lnot x_3).$$
The graph has one vertex for each of the 9 literal occurrences, written as the literal and its clause number, and an edge between two occurrences when they are in different clauses and are not a variable and its negation. A script built the graph and counted: it has 9 vertices and 21 edges, and $k = 3$.

- **Forward.** The assignment $x_1 = 0, x_2 = 1, x_3 = 0$ satisfies $\varphi$. Pick a true literal in each clause: $x_2$ in clause 1, $x_2$ in clause 2 and $\lnot x_3$ in clause 3. These three occurrences are pairwise adjacent, since they are in different clauses and no two contradict each other. So they form a 3-clique.
- **Backward.** The script also found the 3-clique $\{(x_1, 1), (x_3, 2), (\lnot x_2, 3)\}$. Making its literals true gives $x_1 = 1, x_2 = 0, x_3 = 1$, and this assignment satisfies all three clauses.
- **Counts.** $\varphi$ has 5 satisfying assignments, and the graph has 12 cliques of size 3. The numbers differ because a clique fixes only the chosen literals, and one assignment can make several literals true in the same clause. The reduction is not [parsimonious](/parsimonious-reduction/).

**The complement.** The complement of this 9-vertex graph has $36 - 21 = 15$ edges. Its independent sets of size 3 are the 12 cliques above, and their complements are its vertex covers of size 6.

**A random check.** The same script compared the answer of the reduction with brute force: on 300 random 3-CNF formulas with 3 to 5 variables, and on 60 dense formulas built so that 20 of them are unsatisfiable, the graph had a $k$-clique exactly when the formula was satisfiable.

## Known algorithms

- **Brute force.** $O(n^k k^2)$ time on a [word RAM](/word-ram/) with an adjacency matrix, by testing all sets of size $k$. This is polynomial for each fixed $k$ and exponential when $k$ grows with $n$.
- **Fast matrix multiplication for fixed $k$ (Nešetřil and Poljak 1985).** Reduce $k$-clique to triangle detection in a graph with about $n^{k/3}$ vertices, then use matrix multiplication; the time is about $n^{\omega k / 3}$, where $\omega$ is the matrix multiplication exponent. See [parameterized clique](/parameterized-clique/).
- **Exact search for the largest clique.** Branch and bound and the [Bron-Kerbosch](/bron-kerbosch/) enumeration of maximal cliques are the practical methods; exponential-time bounds come from algorithms for [maximum independent set](/maximum-independent-set/) on the complement. See [maximum clique](/maximum-clique/).

## Bounds

- **NP-completeness.** No polynomial-time algorithm exists unless P = NP.
- **Approximation.** For every $\varepsilon > 0$, no polynomial-time algorithm approximates $\omega(G)$ within a factor $n^{1 - \varepsilon}$ unless P = NP (Zuckerman 2007). See [clique inapproximability](/clique-inapproximability/).
- **Parameterized.** With parameter $k$, the problem is W[1]-complete, so it has no algorithm with time $f(k) n^{O(1)}$ unless FPT = W[1]; see [clique W[1]-completeness](/clique-w1-completeness/).
- **Complement.** The complement problem, "$G$ has no clique of size $k$", is [coNP-complete](/co-np-complete/).

## Reductions

**From 3-SAT (Karp reduction).** Let $\varphi = C_1 \land \cdots \land C_m$ with each clause a set of at most 3 literals.

- *Map.* The vertices are the pairs $(\sigma, i)$ with $\sigma$ a literal in $C_i$. Two vertices $(\sigma, i)$ and $(\delta, j)$ are adjacent if and only if $i \ne j$ and $\sigma \ne \lnot \delta$. Set $k = m$. This is Karp's map for SAT, restricted to 3-CNF.
- *Cost.* The graph has at most $3m$ vertices and fewer than $\binom{3m}{2}$ edges. Each pair of vertices is tested once, so $f$ runs in $O(m^2)$ time, polynomial in the length of $\varphi$.
- *If $\varphi$ is satisfiable, then the graph has an $m$-clique.* Fix a satisfying assignment. Choose one true literal $\sigma_i$ in each clause $C_i$. The $m$ vertices $(\sigma_i, i)$ are in different clauses, and no two of them are a literal and its negation, because both are true. So every two are adjacent.
- *If the graph has an $m$-clique, then $\varphi$ is satisfiable.* Let $Q$ be any $m$-clique. Vertices in the same clause are never adjacent, so $Q$ has at most one vertex per clause, and since $\lvert Q \rvert = m$ it has exactly one, say $(\sigma_i, i)$. No two of the $\sigma_i$ are complementary, since their vertices are adjacent. So the assignment that makes each $\sigma_i$ true is well defined; give the other variables any value. It makes a literal true in every clause.

Together with membership in NP and the NP-completeness of 3-SAT ([Cook-Levin theorem](/cook-levin-theorem/)), this proves that the clique problem is NP-complete.

**To independent set and vertex cover (Karp reductions).** Map $(G, k)$ to $(\bar G, k)$ for independent set and to $(\bar G, \lvert V \rvert - k)$ for vertex cover. Building $\bar G$ takes $O(n^2)$ time. Both directions follow from the two equivalences under Variants. Karp's tree uses the second map for NODE COVER. The reductions also go back the same way, so the three problems are equally hard.

**To set packing (Karp reduction).** For each vertex $i$, let $S_i$ be the set of non-edges $\{i, j\}$ at $i$. Two sets $S_i$ and $S_j$ can share only the pair $\{i, j\}$, so they are disjoint if and only if $\{i, j\}$ is an edge. So $k$ pairwise disjoint sets exist if and only if $G$ has a $k$-clique. See [Karp's reduction tree](/karp-21-np-complete/).

**Gadget view.** The reduction from 3-SAT is a [gadget reduction](/gadget-reduction/): each clause becomes a group of vertices with no edges inside it, and the edges between groups join the literals that can be true together.

## Applications

- **A source of hardness.** Clique, independent set and vertex cover are the usual starting points for NP-hardness proofs of graph problems, and clique is the base problem of the W hierarchy in [parameterized complexity](/parameterized-clique/).
- **Network analysis.** Groups of pairwise connected nodes in social, biological and communication networks are cliques; finding them uses the algorithms on [maximum clique](/maximum-clique/).
- **Hardness of approximation.** The inapproximability of clique is the start of many other inapproximability results, such as those for [graph coloring](/graph-coloring/).

## References
