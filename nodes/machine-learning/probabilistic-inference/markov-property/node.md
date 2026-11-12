---
tag: 2VPWEJ
kind: definition
slug: markov-property
name: Markov property
aliases:
- Markov properties of a graph
- global Markov property
- local directed Markov property
area: machine-learning/probabilistic-inference
level: intro
summary: "The rules that read conditional independences off a graph: pairwise, local and global for undirected graphs, and the local directed property for DAGs."
prereqs: [conditional-independence, graphical-model]
see_also: [markov-blanket, d-separation, markov-random-field, bayesian-network, gaussian-graphical-model, markov-chain, hidden-markov-model]
sources:
  - book: isbn:9780198522195
    title: Steffen L. Lauritzen, Graphical Models, Oxford University Press, 1996
    locator: "Chapter 3: Section 3.2.1 (the pairwise, local and global Markov properties of an undirected graph, their implications, and their equivalence under the intersection property) and Section 3.2.2 (the directed Markov properties and their equivalence with factorization)"
  - book: isbn:9781558604797
    title: Judea Pearl, Probabilistic Reasoning in Intelligent Systems, Networks of Plausible Inference, Morgan Kaufmann, 1988
    locator: "Chapter 3: Markov networks and Bayesian networks as graphical representations of independence"
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 3 (local independencies of a Bayesian network and factorization) and Chapter 4 (pairwise, local and global independencies of a Markov network)"
  - paper: doi:10.1002/net.3230200503
    title: Steffen L. Lauritzen, A. Philip Dawid, Birgitte N. Larsen and Hanns-Georg Leimer, Independence properties of directed Markov fields, Networks 20(5), 1990, pages 491 to 505
    locator: the directed local, global and factorization properties and their equivalence
---

A Markov property of a graph is a rule that turns missing edges into [conditional independence](/conditional-independence/) statements. It is the bridge between the picture and the numbers in a [graphical model](/graphical-model/). An undirected graph has three standard Markov properties, called pairwise, local and global. They are equivalent for positive distributions but not in general. A [directed acyclic graph](/directed-acyclic-graph/) has a local directed Markov property, which is equivalent to factorization over the graph. This page is about graphs. For the Markov property of a process in time, see [Markov chain](/markov-chain/).

## Definition

Let $V$ be a finite set of random variables $(X_v)_{v \in V}$ with joint distribution $P$. For sets $A, B, S \subseteq V$ write $A \perp B \mid S$ when $X_A$ and $X_B$ are conditionally independent given $X_S$.

**Undirected graphs.** Let $H = (V, E)$ be an undirected graph, $N(v)$ the neighbours of $v$ and $\mathrm{cl}(v) = N(v) \cup \{v\}$. A set $S$ *separates* $A$ from $B$ if every path from $A$ to $B$ meets $S$. The distribution $P$ satisfies

- the **pairwise** Markov property (P) if $u \perp v \mid V \setminus \{u, v\}$ for every pair of non-adjacent vertices $u, v$;
- the **local** Markov property (L) if $v \perp V \setminus \mathrm{cl}(v) \mid N(v)$ for every vertex $v$;
- the **global** Markov property (G) if $A \perp B \mid S$ for all disjoint $A, B, S$ such that $S$ separates $A$ from $B$.

**Implications.** For every $P$,

$$(G) \Rightarrow (L) \Rightarrow (P).$$

The first step holds because $N(v)$ separates $v$ from $V \setminus \mathrm{cl}(v)$. The second holds because a vertex $u$ not adjacent to $v$ lies in $V \setminus \mathrm{cl}(v)$, and the weak union rule moves the rest of $V \setminus \mathrm{cl}(v)$ into the conditioning set.

**Equivalence under positivity.** If $P$ has the intersection property, that is, $A \perp B \mid C \cup D$ and $A \perp C \mid B \cup D$ imply $A \perp B \cup C \mid D$, then (P), (L) and (G) are equivalent (Pearl and Paz 1987; Lauritzen 1996, Chapter 3). Every strictly positive distribution has the intersection property. A positive $P$ that satisfies them also factorizes over the cliques of $H$, by the Hammersley and Clifford theorem; see [Markov random field](/markov-random-field/).

**Directed acyclic graphs.** Let $G$ be a DAG with parents $\mathrm{Pa}(v)$ and non-descendants $\mathrm{nd}(v)$, the vertices other than $v$ that cannot be reached from $v$. The distribution $P$ satisfies

- the **local directed** Markov property (DL) if $v \perp \mathrm{nd}(v) \setminus \mathrm{Pa}(v) \mid \mathrm{Pa}(v)$ for every $v$;
- the **directed factorization** property (DF) if $P(x) = \prod_{v} P(x_v \mid x_{\mathrm{Pa}(v)})$;
- the **global directed** Markov property (DG) if $A \perp B \mid S$ whenever $S$ [d-separates](/d-separation/) $A$ from $B$.

For discrete variables, or more generally whenever $P$ has a density, these three are equivalent, with no positivity condition (Lauritzen, Dawid, Larsen and Leimer 1990; Lauritzen 1996, Section 3.2.2). The step from (DL) to (DF) is short. List the vertices in a [topological order](/topological-sort/). By the chain rule, $P(x) = \prod_v P(x_v \mid x_{\mathrm{pred}(v)})$, where $\mathrm{pred}(v)$ are the vertices before $v$. These are non-descendants of $v$ and include $\mathrm{Pa}(v)$, so (DL) gives $P(x_v \mid x_{\mathrm{pred}(v)}) = P(x_v \mid x_{\mathrm{Pa}(v)})$. The step from (DF) to (DG) is the soundness of d-separation, and (DG) gives (DL) because $\mathrm{Pa}(v)$ d-separates $v$ from its other non-descendants.

## Examples and non-examples

**All three hold.** Let $P$ be a strictly positive [Markov random field](/markov-random-field/) on the path $a - b - c$, for example $P(x) \propto \psi_1(x_a, x_b)\, \psi_2(x_b, x_c)$ with positive tables. The only missing edge gives $a \perp c \mid b$, which is (P), (L) and (G) at the same time.

**Pairwise without local or global.** Let $X = Y = Z$ be one fair coin, copied three times, and let $H$ be the graph with three vertices and no edges. Given the other two variables, each variable is fixed, so every pairwise statement $X \perp Y \mid Z$ holds and (P) is true. But (L) asks for $X \perp \{Y, Z\} \mid \emptyset$, and $X$ is not independent of $Y$. The global property fails for the same reason, because the empty set separates $X$ from $Y$. The distribution is not positive: it puts zero mass on six of the eight outcomes.

**Local without global.** Take the path $U - W - X - Y - Z$. Let $U$ and $Z$ be independent fair coins, and put $W = U$, $Y = Z$ and $X = W \cdot Y$. Each variable is a function of its neighbours ($U = W$, $W = U$, $X = W \cdot Y$, $Y = Z$, $Z = Y$), so given its neighbours it is fixed, and (L) holds. The vertex $X$ separates $U$ from $Z$, but $U$ and $Z$ are dependent given $X = 0$: the pairs $(U, Z)$ are then $(0,0)$, $(0,1)$ and $(1,0)$ with probability $1/3$ each, so $P(U = 1, Z = 1 \mid X = 0) = 0 \ne 1/9$. So (G) fails.

**Directed, with a missing edge.** For the DAG $A \to B \to C$, (DL) says $C \perp A \mid B$, and (DF) says $P(a, b, c) = P(a) P(b \mid a) P(c \mid b)$. A distribution in which $C$ depends on $A$ given $B$ satisfies neither.

**Not a graph property.** The statement that the future of a process is independent of its past given the present is the Markov property of a [Markov chain](/markov-chain/) or of the hidden states of a [hidden Markov model](/hidden-markov-model/). It is the directed local property of the chain graph $X_1 \to X_2 \to \cdots$, but the term usually refers to the process, not to a graph.

## Related definitions

- **Markov blanket.** The local property says that $N(v)$ is a [Markov blanket](/markov-blanket/) of $v$. In a DAG the blanket is the parents, the children and the co-parents.
- **d-separation.** The global directed property is stated with [d-separation](/d-separation/). An equivalent form uses separation in the moralized graph of the smallest ancestral set.
- **Ordered Markov property.** For a DAG with a fixed topological order, $v \perp \mathrm{pred}(v) \setminus \mathrm{Pa}(v) \mid \mathrm{Pa}(v)$. It is also equivalent to (DF).
- **Faithfulness.** $P$ is faithful to a graph if it has no independences beyond those of the global property. Most parameters give faithful distributions.
- **Gaussian case.** For a multivariate normal distribution, the pairwise property is the statement that the precision matrix has a zero at each missing edge. See [Gaussian graphical model](/gaussian-graphical-model/).

## References
