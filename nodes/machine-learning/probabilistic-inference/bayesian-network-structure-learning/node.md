---
tag: RJFQX2
kind: problem
slug: bayesian-network-structure-learning
name: Bayesian network structure learning
aliases:
- learning the DAG of a Bayesian network
- Bayesian network structure search
area: machine-learning/probabilistic-inference
level: advanced
summary: "Find the DAG of a Bayesian network from data, by maximizing a score such as BIC or BDeu or by independence tests. NP-hard in general; exact DP over subsets works for small n."
prereqs: [bayesian-network, d-separation, maximum-likelihood-estimation]
see_also: [chow-liu-algorithm, markov-blanket, hill-climbing, bitmask-dp, np-complete, structural-causal-model, conditional-independence, edmonds-arborescence]
sources:
  - paper: doi:10.1007/BF00994016
    title: David Heckerman, Dan Geiger and David M. Chickering, Learning Bayesian networks, the combination of knowledge and statistical data, Machine Learning 20, 1995, pages 197 to 243
    locator: the BDe score and its uniform case BDeu, likelihood equivalence and score equivalence, and search methods including branchings
  - paper: "David M. Chickering, Learning Bayesian networks is NP-complete, in Doug Fisher and Hans-J. Lenz (editors), Learning from Data, Artificial Intelligence and Statistics V, Lecture Notes in Statistics 112, Springer, 1996, pages 121 to 130"
    title: Chickering 1996
    locator: NP-completeness of deciding whether some network with at most K parents per node, K at least 2, reaches a given BDe score
  - paper: "David M. Chickering, David Heckerman and Christopher Meek, Large-sample learning of Bayesian networks is NP-hard, Journal of Machine Learning Research 5, 2004, pages 1287 to 1330"
    title: Chickering, Heckerman and Meek 2004
    locator: hardness remains even with an independence oracle for a distribution that a sparse DAG represents perfectly
  - paper: doi:10.1177/089443939100900106
    title: Peter Spirtes and Clark Glymour, An algorithm for fast recovery of sparse causal graphs, Social Science Computer Review 9(1), 1991, pages 62 to 72
    locator: the PC algorithm, which removes edges by conditional independence tests on growing conditioning sets and then orients v-structures
  - paper: "Tomi Silander and Petri Myllymäki, A simple approach for finding the globally optimal Bayesian network structure, Proceedings of the 22nd Conference on Uncertainty in Artificial Intelligence (UAI 2006), pages 445 to 452"
    title: Silander and Myllymäki 2006
    locator: the exact algorithm in five steps, local scores, best parent sets, best sinks, the order and the network, over all subsets of the variables
  - paper: "Thomas Verma and Judea Pearl, Equivalence and synthesis of causal models, Proceedings of the 6th Conference on Uncertainty in Artificial Intelligence (UAI 1990)"
    title: Verma and Pearl 1990
    locator: two DAGs are Markov equivalent if and only if they have the same skeleton and the same v-structures
  - paper: "David M. Chickering, Optimal structure identification with greedy search, Journal of Machine Learning Research 3, 2002, pages 507 to 554"
    title: Chickering 2002
    locator: greedy equivalence search over Markov equivalence classes and its large-sample optimality
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 18 (structure learning in Bayesian networks): constraint-based and score-based learning, BIC and Bayesian scores, search"
---

Bayesian network structure learning is the problem of finding the directed acyclic graph of a [Bayesian network](/bayesian-network/) from data. There are two main approaches. Score-based methods give each DAG a score, such as BIC or the Bayesian score BDeu, and search for the DAG with the best score. Constraint-based methods, such as the PC algorithm, run [conditional independence](/conditional-independence/) tests and build a graph whose [d-separations](/d-separation/) match them. The number of DAGs grows like $2^{\Theta(n^2)}$, the score version is NP-hard even when each node has at most two parents (Chickering 1996), and data can only identify a DAG up to Markov equivalence. Trees are easy, by the [Chow-Liu algorithm](/chow-liu-algorithm/), and for up to about 30 variables an exact dynamic program over subsets finds the best DAG.

## In plain words

You have a table of observations of several variables and want to draw arrows that show which variables directly influence which others. One way is to give each possible drawing a grade: how well it explains the data, minus a charge for each extra link. Then you look for the drawing with the best grade. Another way is to test, for pairs of variables, whether they still move together once you hold other variables fixed, and to keep a link only if no such test explains the pair away. Both ways face the same limits. The number of drawings explodes as the variables grow. And some drawings explain every possible data set equally well, so the data cannot choose between them.

## Definition

**Data and model.** The input is a data set $D$ of $s$ samples of $n$ discrete variables $X_1, \dots, X_n$, where $X_v$ has $r_v$ states. Here $n$ counts variables, the nodes of the graph, and $s$ counts samples. A candidate is a DAG $G$ on the $n$ variables. With the parent set $\mathrm{Pa}(v)$ of each node, $G$ has $\dim(G) = \sum_v q_v (r_v - 1)$ free parameters, where $q_v = \prod_{u \in \mathrm{Pa}(v)} r_u$ is the number of parent configurations.

**Score-based version.** A score is *decomposable* if $\mathrm{score}(G, D) = \sum_v \mathrm{local}(v, \mathrm{Pa}(v))$, where each local term depends only on the counts $N_{vjk}$ of samples with $X_v = k$ and parent configuration $j$. The two standard ones are:

- **BIC** (Schwarz 1978): the log-likelihood at the maximum likelihood tables minus $\frac{\log s}{2} \dim(G)$, with local term $\sum_{j, k} N_{vjk} \log \frac{N_{vjk}}{N_{vj}} - \frac{\log s}{2} q_v (r_v - 1)$.
- **BDeu** (Heckerman, Geiger and Chickering 1995): the log marginal likelihood under Dirichlet priors with equivalent sample size $\alpha$ spread evenly, with local term
$$\sum_{j} \Big[\log \frac{\Gamma(\alpha / q_v)}{\Gamma(\alpha / q_v + N_{vj})} + \sum_k \log \frac{\Gamma(\alpha / (q_v r_v) + N_{vjk})}{\Gamma(\alpha / (q_v r_v))}\Big].$$

The *structure learning problem* asks for a DAG that maximizes the score, often with at most $K$ parents per node. Its decision version asks, for given $D$, $K$ and $t$, whether some DAG with in-degree at most $K$ has score at least $t$.

**Markov equivalence.** Two DAGs are *Markov equivalent* if they have the same d-separations. Verma and Pearl (1990) proved that this holds exactly when they have the same skeleton and the same v-structures, that is, the same triples $a \to c \leftarrow b$ with $a$ and $b$ not adjacent. BIC and BDeu are *score equivalent*: they give the same score to equivalent DAGs. So the real output is an equivalence class, often drawn as a partially directed graph (CPDAG) in which the edges that differ inside the class have no direction.

**Constraint-based version.** Given an oracle, or a statistical test, for statements $X_u \perp X_v \mid X_S$, find the equivalence class of a DAG whose d-separations are exactly the independences. This assumes that the data come from a distribution *faithful* to some DAG.

## Variants

- **Known order.** If a topological order is given, each node picks its best parent set among its predecessors on its own. This is the K2 setting of Cooper and Herskovits (1992).
- **Trees and branchings.** With at most one parent per node, the problem is polynomial: a maximum spanning tree under mutual information for likelihood ([Chow-Liu](/chow-liu-algorithm/)), or a maximum branching by [Edmonds' algorithm](/edmonds-arborescence/) for other decomposable scores.
- **Bounded in-degree.** At most $K$ parents per node; NP-hard for every $K \ge 2$.
- **Bayesian model averaging.** Instead of one DAG, compute posterior probabilities of features such as edges, summing over all DAGs or all orders.
- **Gaussian and mixed data.** Linear Gaussian networks use the BGe score or BIC with partial correlation tests.
- **Causal discovery.** With latent variables the FCI algorithm returns a partial ancestral graph; with interventional data, more edges can be oriented. See [structural causal model](/structural-causal-model/).
- **Local structure.** Find the [Markov blanket](/markov-blanket/) of a single target variable, for feature selection, without learning the whole graph.

## Examples

**Explaining away in data.** Let $A$ and $B$ be independent fair coins and $C = A \lor B$, copied correctly in 90 percent of the samples and flipped in the others. Take $s = 400$ samples with exactly the expected counts, 90 or 10 of each pattern for each of the 4 values of $(A, B)$. The BIC scores of some DAGs are:

| DAG | BIC |
|---|---|
| no edges | $-807.85$ |
| $A \to C$ | $-770.15$ |
| $A \to C \to B$ | $-732.44$ |
| $A \to C \leftarrow B$ | $-702.53$ |
| $A \to B$, $A \to C$, $B \to C$ | $-705.52$ |

The v-structure wins. The complete DAG fits the data as well, because $A$ and $B$ are exactly independent in these counts, but it pays $\frac{\log 400}{2} \approx 3.00$ for one more parameter. The exact search over all 25 DAGs on three nodes returns $A \to C \leftarrow B$. BDeu with $\alpha = 1$ gives the same answer, $-703.91$ against $-707.46$ for the complete DAG.

**Equivalent DAGs.** The DAGs $A \to B \to C$, $A \leftarrow B \leftarrow C$ and $A \leftarrow B \to C$ have the same skeleton and no v-structure, so they are Markov equivalent and get the same score from any score equivalent score. The DAG $A \to B \leftarrow C$ has a v-structure and is alone in its class. On three nodes the 25 DAGs fall into 11 classes, and on four nodes the 543 DAGs fall into 185 classes.

**Counting DAGs.** By Robinson's recurrence $a_n = \sum_{k=1}^{n} (-1)^{k+1} \binom{n}{k} 2^{k(n-k)} a_{n-k}$, there are $1, 3, 25, 543, 29281$ DAGs on $1, \dots, 5$ labelled nodes, and more than $10^{18}$ on $10$ nodes. Searching them one by one is hopeless beyond about six nodes.

## Known algorithms

| algorithm | approach | guarantee | cost |
|---|---|---|---|
| [Chow-Liu](/chow-liu-algorithm/) (1968) | maximum spanning tree | best tree | $O(n^2 s)$ |
| K2 (Cooper and Herskovits 1992) | greedy parents for a fixed order | heuristic | polynomial |
| PC (Spirtes and Glymour 1991) | independence tests | correct class if faithful and tests correct | polynomial for bounded degree |
| [Hill climbing](/hill-climbing/) | add, delete or reverse one edge | local optimum | per step $O(n^2)$ moves |
| GES (Chickering 2002) | greedy over equivalence classes | best class in the large-sample limit | exponential in the worst case |
| Silander and Myllymäki (2006) | [dynamic programming over subsets](/bitmask-dp/) | exact optimum | $O(n^2 2^n)$ time after the local scores |

**Exact dynamic programming.** Silander and Myllymäki (2006) use three facts. Every DAG has a sink, a node with no children. If $v$ is a sink of the best DAG on a set $W$, then $v$ takes the best parent set inside $W \setminus \{v\}$, and the rest is the best DAG on $W \setminus \{v\}$. And a decomposable score lets the parts be added. So:

1. Compute $\mathrm{local}(v, C)$ for all $v$ and all $C \subseteq V \setminus \{v\}$: $n 2^{n-1}$ local scores.
2. Compute $\mathrm{bps}(v, C) = \max\big(\mathrm{local}(v, C), \max_{c \in C} \mathrm{bps}(v, C \setminus \{c\})\big)$, the best parent set inside $C$.
3. Compute $\mathrm{best}(W) = \max_{v \in W} \big[\mathrm{best}(W \setminus \{v\}) + \mathrm{bps}(v, W \setminus \{v\})\big]$ with $\mathrm{best}(\emptyset) = 0$, and record the best sink of each $W$.
4. Peel the best sinks off $V$ one by one to get an order, and give each node its best parent set among the nodes before it.

Steps 2 and 3 take $O(n^2 2^n)$ time and $O(n 2^n)$ memory, and step 1 costs $O(n 2^n)$ score evaluations, each a pass over the data. The tests of this page compare it with brute force over all 543 DAGs on four nodes, with BIC and BDeu, and over all 29281 DAGs on five nodes.

**The PC algorithm.** Start with the complete undirected graph. For $k = 0, 1, 2, \dots$, remove the edge $u - v$ if some set $S$ of $k$ current neighbours of $u$ gives $X_u \perp X_v \mid X_S$, and remember $S$. Then orient $u \to w \leftarrow v$ for each non-adjacent pair $u, v$ with a common neighbour $w$ not in their remembered set, and propagate orientations with fixed rules. Under faithfulness and correct tests, the output is the CPDAG of the true DAG.

## Bounds

- **Search space.** The number of DAGs is $2^{\Theta(n^2)}$, and the number of equivalence classes is about a constant fraction of it, so even equivalence classes do not make exhaustive search feasible.
- **NP-hardness.** Chickering (1996) showed that the decision version with the BDe score is NP-complete for every bound $K \ge 2$ on the number of parents. Chickering, Heckerman and Meek (2004) showed that it stays NP-hard even with infinite data, that is, with a perfect independence oracle for a distribution that a sparse DAG represents exactly, for small fixed in-degree bounds.
- **Trees.** With $K = 1$ the problem is polynomial, by a maximum spanning tree or a maximum branching.
- **Exact algorithms.** The best known exact algorithms for the general problem take time $2^n$ times a polynomial, like the dynamic program above.

## Reductions

- **To parent set selection.** With a fixed order, the problem splits into $n$ independent choices of a best parent set among the predecessors.
- **To shortest paths.** The dynamic program is a shortest path problem in the lattice of subsets of $V$, from $\emptyset$ to $V$, with the edge $W \to W \cup \{v\}$ costing $-\mathrm{bps}(v, W)$. Heuristic search such as A* uses this view to skip most subsets.
- **To integer programming.** Each node chooses one parent set from a list, under cluster constraints that forbid cycles. Integer linear programming solvers handle networks with dozens of nodes this way.
- **From hard problems.** Chickering's NP-hardness proof reduces a feedback arc set problem to structure learning: the data are built so that a high score needs an acyclic orientation of a given graph with few reversed arcs.

## Applications

- **Causal discovery.** Under faithfulness and no hidden confounders, the equivalence class found from data contains the true causal DAG, and some edge directions are identified.
- **Biology.** Gene regulatory and protein signalling networks are learned from expression data, often with model averaging over structures.
- **Density estimation and classification.** A learned network gives a compact joint distribution, and tree-augmented naive Bayes builds on the Chow-Liu tree.
- **Feature selection.** The [Markov blanket](/markov-blanket/) of the class variable, found by local structure learning, is a minimal set of relevant features.

## References
