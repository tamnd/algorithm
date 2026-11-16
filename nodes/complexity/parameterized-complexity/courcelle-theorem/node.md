---
tag: 1RQ806
kind: theorem
slug: courcelle-theorem
name: Courcelle's theorem
aliases:
- MSO on bounded treewidth
area: complexity/parameterized-complexity
level: advanced
summary: "A graph property written in MSO2 logic is decidable in time f(|phi|, t) n on graphs with a tree decomposition of width t. The function f is a non-elementary tower."
prereqs: [treewidth, tree-decomposition, dp-on-tree-decompositions, fixed-parameter-tractable]
see_also: [meta-theorems, grid-minor-theorem, minor-testing, treewidth-computation, graph-minor-theorem, nice-tree-decomposition, regular-language, three-coloring]
sources:
  - paper: doi:10.1016/0890-5401(90)90043-H
    title: "Bruno Courcelle, The monadic second-order logic of graphs I: recognizable sets of finite graphs, Information and Computation 85(1), 12-75 (1990)"
    locator: the main result, MSO2 properties are recognizable on graphs of bounded treewidth and decidable in linear time when a tree decomposition is given
  - paper: doi:10.1016/0196-6774(91)90006-K
    title: "Stefan Arnborg, Jens Lagergren and Detlef Seese, Easy problems for tree-decomposable graphs, Journal of Algorithms 12(2), 308-340 (1991)"
    locator: the extension to optimization and counting problems over MSO-definable sets
  - book: isbn:9783319212746
    title: "Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015"
    locator: "Section 7.4, Treewidth and monadic second-order logic (7.4.1 the logic, 7.4.2 the statement, the optimization form and the remark on the non-elementary f), and the bibliographic notes of Chapter 7"
  - paper: doi:10.1016/j.apal.2004.01.007
    title: "Markus Frick and Martin Grohe, The complexity of first-order and monadic second-order logic revisited, Annals of Pure and Applied Logic 130(1-3), 3-31 (2004)"
    locator: the lower bound, no f(k) p(n) algorithm with elementary f for MSO on finite words unless P = NP
  - paper: doi:10.1137/S0097539793251219
    title: "Hans L. Bodlaender, A linear-time algorithm for finding tree-decompositions of small treewidth, SIAM Journal on Computing 25(6), 1305-1317 (1996)"
    locator: the main theorem, a tree decomposition of width t in time linear in n for every fixed t
---

Courcelle's theorem says that every graph property that can be written as a sentence of monadic second-order logic can be decided in linear time on graphs of bounded [treewidth](/treewidth/). The parameter is the treewidth $t$ together with the length of the sentence. The running time is $f(\lVert\varphi\rVert, t) \cdot n$, so the problem is [fixed-parameter tractable](/fixed-parameter-tractable/) in this combined parameter, but $f$ is a tower of exponentials and cannot be made elementary unless $\mathsf{P} = \mathsf{NP}$. The proof is given here as a sketch with its sources.

## Statement

A graph $G = (V, E)$ is seen as a logical structure. **MSO2** is the logic with four sorts of variables: single vertices, single edges, sets of vertices and sets of edges. The atomic formulas are equality, membership ($v \in X$, $e \in F$), the incidence relation $\mathrm{inc}(v, e)$ ("$v$ is an end of $e$") and the adjacency relation $\mathrm{adj}(u, v)$. Formulas are built with $\neg, \wedge, \vee, \rightarrow$ and with $\exists$ and $\forall$ over all four sorts. **MSO1** is the part of MSO2 that has no edge variables and no edge-set variables. The length $\lVert\varphi\rVert$ of a formula is the number of symbols in it.

**Theorem (Courcelle 1990).** There is an algorithm that takes an MSO2 sentence $\varphi$, a graph $G$ with $n$ vertices, and a [tree decomposition](/tree-decomposition/) of $G$ of width $t$, and decides whether $G \models \varphi$ in time $f(\lVert\varphi\rVert, t) \cdot n$, for a computable function $f$.

**Optimization form (Arnborg, Lagergren and Seese 1991).** Let $\varphi(X)$ be an MSO2 formula with one free set variable $X$. Within the same form of time bound, the algorithm can find a set $X$ of minimum size (or maximum size) such that $G \models \varphi(X)$, or report that there is none.

The model is a RAM with unit-cost operations on numbers of $O(\log n)$ bits. The form here is the one in Cygan et al., Section 7.4.2. The tree decomposition is part of the input. If it is not given, Bodlaender's algorithm finds one of width $t$ in time linear in $n$ for every fixed $t$ (see [treewidth computation](/treewidth-computation/)), so the whole procedure stays linear in $n$ for a fixed sentence and a fixed $t$.

Some properties and their sentences, from Cygan et al., Section 7.4:

- 3-colorability (MSO1): $\exists X_1 \exists X_2 \exists X_3 \, [\forall v \, (v \in X_1 \vee v \in X_2 \vee v \in X_3) \wedge \forall u \forall v \, (\mathrm{adj}(u, v) \rightarrow \bigwedge_{i=1}^{3} \neg(u \in X_i \wedge v \in X_i))]$.
- Vertex cover (the formula for the optimization form): $\mathrm{vcover}(X) = \forall e \, \exists x \, (x \in X \wedge \mathrm{inc}(x, e))$.
- Hamiltonicity needs MSO2: there is an edge set $F$ such that every vertex is incident to exactly two edges of $F$, and $F$ is connected. Connectivity is written as "no proper nonempty subset of the vertices is closed under the edges of $F$".

## In plain words

Many hard graph questions become easy when the graph is built like a thin tree. You cut the graph along small vertex sets and solve it from the leaves of the tree up. Courcelle's theorem says that this always works for every question you can write in a certain formal language. That language can say "there is a set of vertices such that..." and "for every edge...". At each small cut, only a fixed number of different summaries of the part below can occur. The algorithm keeps one of these summaries per cut, so the time grows only linearly with the size of the graph. The cost is hidden in the fixed part. The number of summaries can grow like a tower of powers of two in the length of the question, and in general this cannot be avoided.

## Proof

The proof is a sketch. It follows the route by types and dynamic programming. The full proof is in Courcelle (1990). A different full proof translates the sentence into a finite tree automaton.

### Setup: boundaried graphs

Fix a rooted [nice tree decomposition](/nice-tree-decomposition/) of width $t$ with $O(t n)$ nodes. For a node $x$ with bag $B_x$, let $G_x$ be the subgraph induced on the vertices in the bags of the subtree of $x$, with the edges introduced below $x$. The pair $(G_x, B_x)$ is a graph with a boundary of at most $t + 1$ labeled vertices. A node is of one of four kinds: leaf, introduce vertex, forget vertex, or join. Each kind builds $(G_x, B_x)$ from the graphs of its children by one of a fixed, finite set of operations. A join glues two boundaried graphs along their common boundary.

### Step 1: types

Let $q$ be the quantifier rank of $\varphi$ (the largest nesting depth of quantifiers). The *$q$-type* of a boundaried graph is the set of all MSO2 formulas of quantifier rank at most $q$ that hold in it, with the boundary vertices as constants. Up to logical equivalence there are only finitely many such formulas for fixed $q$ and $t$. So the number of $q$-types is bounded by a function $N(q, t)$. This function is a tower of exponentials whose height grows with $q$.

### Step 2: the composition lemma

The $q$-type of the result of each operation depends only on the $q$-types of its inputs. For a join, this is the Feferman-Vaught style composition lemma for gluing along a boundary. Its proof uses Ehrenfeucht-Fraïssé games of length $q$: a winning strategy on each part combines into a winning strategy on the glued graph. This step is left out here.

### Step 3: the dynamic program

By Step 2, each operation is a finite table from types to types. The algorithm computes these tables from $\varphi$ and $t$ before it reads $G$. It then visits the nodes of the tree decomposition from the leaves to the root and stores one type per node. Each node costs one table lookup, so this phase takes $O(t n)$ lookups. At the root the boundary is empty, and the type of $G$ says whether $\varphi$ is in it. The time to build the tables is the function $f$. How to compute these tables is left out here. It is where the non-elementary cost comes from.

For the optimization form, each node stores, for each type of $(G_x, B_x, X \cap V(G_x))$, the least size of a partial set that has that type. The tables then combine sizes by addition at a join.

### Worked example

Take 3-colorability on the 3 by 3 grid. In row-major order, the grid has a path decomposition whose bags are windows of 4 consecutive vertices, so its width is 3 (the treewidth of the 3 by 3 grid is 3). A problem-specific version of Step 3 keeps, for each window, the colors of the last 3 vertices and the number of partial colorings that end in them. That is at most $3^3 = 27$ states. A run of this table method counts 246 proper 3-colorings of the 3 by 3 grid, the same number as a brute-force count, and at most 18 of the 27 states are live at one time. On the 4 by 4 grid (width 4, at most 81 states), it counts 7812 colorings with at most 36 live states. The generic algorithm of the theorem uses types of the sentence instead of colors, and it has many more states.

## Consequences

- Every property in MSO2 is decidable in linear time on each class of graphs of bounded treewidth. This includes 3-colorability, [Hamiltonian cycle](/hamiltonian-cycle-problem/), and, for each fixed $H$, "$H$ is a [minor](/graph-minor/) of $G$". The last one gives a linear test for every [minor-closed](/graph-minor-theorem/) property on graphs of bounded treewidth.
- With the optimization form, [vertex cover](/vertex-cover/), [dominating set](/dominating-set/) and independent set are solvable in time $f(t) \cdot n$ on graphs of treewidth $t$.
- Courcelle's theorem is the bounded-treewidth half of many win/win arguments. If the treewidth is large, the [grid minor theorem](/grid-minor-theorem/) gives a large grid, and the grid gives the answer. If the treewidth is small, Courcelle's theorem gives the answer. See [bidimensionality theory](/bidimensionality-theory/) and the [irrelevant vertex technique](/irrelevant-vertex-technique/).
- The theorem is the first example of an [algorithmic meta-theorem](/meta-theorems/): a single result that gives an algorithm for a whole class of problems defined by logic.

## Tightness

- **The function $f$ is not elementary, and this is needed.** Frick and Grohe (2004) proved that model checking of MSO on finite words has no algorithm in time $f(\lVert\varphi\rVert) \cdot p(n)$ with $f$ elementary and $p$ a polynomial, unless $\mathsf{P} = \mathsf{NP}$. A word is a path with labels, and a path has treewidth 1. So no version of Courcelle's theorem can have an elementary $f$ unless $\mathsf{P} = \mathsf{NP}$. Cygan et al. note that the height of the tower grows linearly with the number of quantifier alternations.
- **The constants are not practical.** The theorem shows that a problem is FPT in the treewidth. It does not give a usable algorithm. Practical solvers write a [dynamic program on the tree decomposition](/dp-on-tree-decompositions/) for each problem, with a known small number of states, as in the worked example.
- **Bounded treewidth is needed.** 3-colorability is an MSO1 property, and it is [NP-complete](/np-complete/) on [planar graphs](/planar-graph/). So the theorem does not extend to all graphs, or to planar graphs, unless $\mathsf{P} = \mathsf{NP}$.
- **MSO1 and MSO2 differ.** Courcelle, Makowsky and Rotics extended the theorem to graphs of bounded cliquewidth, but only for MSO1. Edge-set quantifiers, which Hamiltonicity needs, are not covered there.
- **Optimization needs set sizes, not general arithmetic.** The optimization form minimizes or maximizes the size (or a linear weight) of one set. It does not allow arbitrary counting conditions inside the formula.

## History

MSO on words and on trees was linked to finite automata by Büchi (1960) and by Thatcher and Wright (1968): a set of words or trees is definable in MSO if and only if it is a [regular language](/regular-language/) of words or trees. Courcelle (1990) carried this to graphs of bounded treewidth, through the algebra of graphs with boundaries. Arnborg, Lagergren and Seese (1991) gave the optimization and counting forms, and Borie, Parker and Tovey gave a similar framework at about the same time. Bodlaender (1996) made the tree decomposition computable in linear time for fixed width, which removed the need to give it as input. Frick and Grohe (2004) showed that the tower in $f$ cannot be avoided. Courcelle, Makowsky and Rotics extended the MSO1 case to cliquewidth.

## References
