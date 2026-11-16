---
tag: TPB4FR
kind: definition
slug: polynomial-time-reduction
name: Polynomial-time reduction
aliases:
- Karp reduction
- Polynomial-time many-one reduction
- polynomial many-one reduction
- polynomial reduction
- polynomial-time many-one reduction
area: complexity/reductions-catalogue
level: intro
summary: A polynomial-time computable map f with x in A if and only if f(x) in B. It is the Karp reduction that defines NP-hardness and NP-completeness.
prereqs: [decision-problem, polynomial-time]
see_also: [turing-reduction, levin-reduction, parsimonious-reduction, transitivity-of-reductions, many-one-reducibility, np-completeness-proof, reduction, np-hard]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: "Richard M. Karp, Reducibility among combinatorial problems, in R. E. Miller and J. W. Thatcher (eds.), Complexity of Computer Computations, Plenum Press, 1972, 85-103"
    locator: the definition of polynomial-time reducibility (a many-one reduction) and the reductions from satisfiability
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 2.5, Polynomial Transformations and NP-Completeness (pp. 34-38)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, 3rd edition, Cengage Learning, 2013
    locator: Section 7.4, NP-completeness (polynomial time reducibility)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Section 2.2, Reducibility and NP-completeness
  - paper: doi:10.1016/0304-3975(75)90016-X
    title: "Richard E. Ladner, Nancy A. Lynch and Alan L. Selman, A comparison of polynomial time reducibilities, Theoretical Computer Science 1(2) (1975), 103-123"
    locator: the definitions of many-one, truth-table and Turing reducibility in polynomial time and the separations between them
---

A polynomial-time reduction (Karp reduction) from a [decision problem](/decision-problem/) $A$ to a decision problem $B$ is a function $f$, computable in [polynomial time](/polynomial-time/), such that every instance $x$ is a yes-instance of $A$ exactly when $f(x)$ is a yes-instance of $B$. It is written $A \le_m^p B$, where $m$ stands for "many-one" and $p$ for "polynomial time". It is the reduction used to define [NP-hard](/np-hard/) and [NP-complete](/np-complete/) problems: if $A \le_m^p B$ and $B$ is in [P](/p/), then $A$ is in P. The general idea of a reduction, with its many uses in algorithm design, is on [reduction](/reduction/); this page gives the exact definition and its properties.

## Definition

Fix the alphabet $\{0,1\}$ and a fixed, polynomial-time encoding of instances as strings, with numbers in binary. A decision problem is then a language $A \subseteq \{0,1\}^*$, the set of encodings of yes-instances. Time is measured on a deterministic [multitape Turing machine](/multitape-turing-machine/). The class of polynomial-time computable functions does not change if a single-tape machine or a [random-access machine](/ram-turing-equivalence/) is used instead, because these models simulate each other with polynomial overhead ([multitape simulation theorem](/multitape-simulation-theorem/)).

**Definition (Karp 1972).** Let $A, B \subseteq \{0,1\}^*$. A *polynomial-time reduction* from $A$ to $B$ is a function $f : \{0,1\}^* \to \{0,1\}^*$ such that

1. some deterministic Turing machine computes $f(x)$ from $x$ in at most $p(|x|)$ steps, for a polynomial $p$, and
2. for every $x \in \{0,1\}^*$: $\quad x \in A \iff f(x) \in B$.

We write $A \le_m^p B$ when such an $f$ exists, and $A \equiv_m^p B$ when $A \le_m^p B$ and $B \le_m^p A$.

Four details of the definition matter in proofs.

- **Both directions.** Condition 2 is an equivalence. It says that yes-instances go to yes-instances ($x \in A \Rightarrow f(x) \in B$) and that no-instances go to no-instances, which is the same as $f(x) \in B \Rightarrow x \in A$.
- **Every string.** $f$ is defined on all strings, also on strings that encode no instance. In practice the reduction checks the syntax first and maps a malformed string to a fixed no-instance of $B$.
- **The output is short.** A machine writes at most one output symbol in each step, so $|f(x)| \le p(|x|)$. This bound is what makes reductions compose ([transitivity of reductions](/transitivity-of-reductions/)).
- **One question, answer copied.** Seen as an algorithm for $A$ that uses a solver for $B$, the reduction asks the solver exactly one question, $f(x)$, and returns the answer without change. A [Cook reduction](/turing-reduction/) may ask many questions and combine the answers.

**Basic properties.** For all languages $A$, $B$ and $C$:

- $\le_m^p$ is reflexive (take $f(x) = x$) and transitive (compose the two maps; the proof is on [transitivity of reductions](/transitivity-of-reductions/)). So it is a preorder, and $\equiv_m^p$ is an equivalence relation.
- $A \le_m^p B$ if and only if $\bar A \le_m^p \bar B$, where the bar is the complement in $\{0,1\}^*$. The same $f$ works, because condition 2 is an equivalence.
- If $A \le_m^p B$ and $B \in$ P, then $A \in$ P. If $B$ is decided in time $q(m)$, then $A$ is decided in time $p(n) + q(p(n))$.
- If $A \le_m^p B$ and $B \in$ [NP](/np/), then $A \in$ NP: a [certificate](/certificate/) for $f(x) \in B$ is a certificate for $x \in A$, and the verifier first computes $f(x)$. In the same way, [coNP](/co-np/) is closed under $\le_m^p$.

## Examples and non-examples

### Independent set and vertex cover

An *independent set* of a graph $G = (V, E)$ is a set $S \subseteq V$ with no edge inside $S$; a *vertex cover* is a set $C \subseteq V$ that meets every edge. For every $S \subseteq V$, $S$ is independent if and only if $V \setminus S$ is a vertex cover: an edge with both ends in $S$ is exactly an edge that $V \setminus S$ misses. So the map

$$f(G, k) = (G, |V| - k)$$

is a polynomial-time reduction from INDEPENDENT SET ("does $G$ have an independent set of size $k$?") to [VERTEX COVER](/vertex-cover/) ("does $G$ have a vertex cover of size $|V| - k$?"), and the same map, read the other way, reduces VERTEX COVER to INDEPENDENT SET. The problems are $\equiv_m^p$-equivalent. In the same way, $(G, k) \mapsto (\bar G, k)$ reduces [CLIQUE](/clique-problem/) to INDEPENDENT SET, where $\bar G$ is the complement graph.

### 3-SAT to independent set, with numbers

A [3-SAT](/3-sat/) formula $\varphi$ with $m$ clauses maps to a pair $(G_\varphi, m)$. The graph $G_\varphi$ has one vertex for each occurrence of a literal, an edge between the three vertices of each clause (a triangle), and an edge between each pair of vertices whose literals are $x_i$ and $\neg x_i$. An independent set has at most one vertex in each triangle, so size $m$ means one vertex in every clause, and the conflict edges forbid picking both $x_i$ and $\neg x_i$.

For

$$\varphi = (x_1 \lor x_2 \lor \neg x_3) \land (\neg x_1 \lor x_2 \lor x_3) \land (\neg x_1 \lor \neg x_2 \lor \neg x_3),$$

the graph has $9$ vertices and $15$ edges: $9$ triangle edges and $6$ conflict edges. The question is whether it has an independent set of size $3$.

- *Yes to yes.* The assignment $x_1 = 1, x_2 = 1, x_3 = 0$ satisfies $\varphi$. Pick a true literal in each clause: $x_1$ in the first, $x_2$ in the second, $\neg x_3$ in the third. These three vertices are in different triangles and no two of them are opposite literals, so they form an independent set of size $3$.
- *Yes back to yes.* Take any independent set of size $3$, for example the vertices of $x_2$ (first clause), $x_3$ (second clause) and $\neg x_1$ (third clause). Set each picked literal to true; this is consistent, since no conflict edge is inside the set. Set the other variables to $0$. The result $x_1 = 0, x_2 = 1, x_3 = 1$ makes one literal of each clause true, so it satisfies $\varphi$.

The map takes $O(m^2)$ time, since it compares each pair of the $3m$ literal occurrences. For this $\varphi$, both sides are yes-instances. On all $164$ formulas with $1$ to $3$ clauses, each clause with three different variables among $x_1, x_2, x_3$, the two answers agree. The general proof is the two arguments above with an arbitrary assignment and an arbitrary independent set.

### Non-examples

- **A map that is correct but slow.** Let $f(\varphi)$ be a fixed satisfiable formula when $\varphi$ is satisfiable and a fixed unsatisfiable formula otherwise. Condition 2 holds for SAT to SAT, but $f$ needs a SAT solver. No polynomial-time algorithm for $f$ is known, so $f$ is not a polynomial-time reduction unless P = NP.
- **A map with a large output.** Converting a CNF formula into an equivalent DNF formula preserves satisfiability, and DNF satisfiability is in P. But the DNF of $(x_1 \lor y_1) \land \cdots \land (x_n \lor y_n)$ has $2^n$ terms, so the map is not polynomial and proves nothing about SAT.
- **A map that keeps only yes-instances.** Map a graph $G$ to itself and ask whether $G$ is connected. Every graph with a [Hamiltonian cycle](/hamiltonian-cycle-problem/) is connected, so yes goes to yes. But a connected tree with $3$ vertices has no Hamiltonian cycle, so a no-instance goes to a yes-instance. The map fails condition 2.
- **Numbers written in unary.** [PARTITION](/partition-problem/) has a dynamic programming algorithm that is polynomial in the sum of its numbers. The map that rewrites each number $a_i$ in unary writes $a_i$ symbols, which is exponential in its $\lceil \log_2 (a_i + 1) \rceil$ bits. So this map is not a polynomial-time reduction, and the algorithm does not put PARTITION in P.
- **Flipping the answer.** $\overline{\mathrm{SAT}}$ (the unsatisfiable formulas, together with the malformed strings) Cook-reduces to SAT with one question and a negated answer. A Karp reduction cannot negate: $\overline{\mathrm{SAT}} \le_m^p \mathrm{SAT}$ holds if and only if NP = coNP. The proof is on [reduction](/reduction/).
- **A trivial reduction inside P.** If $A \in$ P and $B$ has a yes-instance $y_1$ and a no-instance $y_0$, then $A \le_m^p B$ by $f(x) = y_1$ if $x \in A$ and $f(x) = y_0$ otherwise. So every problem in P reduces to every non-trivial problem, and Karp reductions cannot compare problems inside P. Completeness for P and for [NL](/nondeterministic-logspace/) uses [logspace](/logspace/) reductions instead.

## Related definitions

- **[Cook reduction](/turing-reduction/)** ($A \le_T^p B$): a polynomial-time [oracle machine](/oracle-turing-machine/) that may ask many questions to $B$. Every Karp reduction is a Cook reduction with one question. Ladner, Lynch and Selman (1975) showed that the two differ on some sets in exponential time. Cook (1971) used this form for SAT; Karp (1972) used many-one reductions for his list of problems.
- **Truth-table reduction**: a Cook reduction whose questions are fixed before any answer is known (non-adaptive).
- **Logspace reduction** ($A \le_m^{\log} B$): the same as $\le_m^p$, but $f$ is computed by a machine with a read-only input, a write-only output and $O(\log n)$ work space. Every logspace reduction is a Karp reduction, since such a machine has at most polynomially many configurations.
- **[Levin reduction](/levin-reduction/)**: a Karp reduction between search problems, together with polynomial-time maps that carry solutions in both directions.
- **[Parsimonious reduction](/parsimonious-reduction/)**: a Karp reduction that keeps the number of solutions. The 3-SAT example above is not parsimonious: $\varphi$ has $5$ satisfying assignments, but $G_\varphi$ has $12$ independent sets of size $3$.
- **[Many-one reducibility](/many-one-reducibility/)** in computability theory: the same definition with "computable" in place of "polynomial-time computable".
- **[Parameterized reduction](/parameterized-reduction/)**, **[fine-grained reduction](/fine-grained-reduction/)** and the [approximation-preserving reductions](/approximation-preserving-reduction/) keep a parameter, an exact running time or the quality of approximate solutions.
- **[NP-hard](/np-hard/)** and **[NP-complete](/np-complete/)** are defined with $\le_m^p$ unless a page says otherwise. The recipe for a proof is on [NP-completeness proof](/np-completeness-proof/).

## References
