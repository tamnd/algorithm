---
tag: HV09R2
kind: concept
slug: meta-theorems
name: Meta-theorems
aliases:
- meta-kernelization
- algorithmic meta-theorems
area: complexity/parameterized-complexity
level: research
summary: "One theorem gives an algorithm or a kernel for every problem in a logic on a graph class: MSO on bounded treewidth, first-order logic on nowhere dense classes, linear kernels on bounded genus."
prereqs: [courcelle-theorem, kernel, fixed-parameter-tractable]
see_also: [courcelle-theorem, bidimensionality-theory, grid-minor-theorem, irrelevant-vertex-technique, parameterized-dominating-set, kernelization, w-hierarchy, minor-testing]
sources:
  - paper: doi:10.1016/0890-5401(90)90043-H
    title: "Bruno Courcelle, The monadic second-order logic of graphs I: recognizable sets of finite graphs, Information and Computation 85(1), 12-75 (1990)"
    locator: the main result, MSO2 model checking in linear time on graphs of bounded treewidth
  - paper: doi:10.1145/504794.504798
    title: "Markus Frick and Martin Grohe, Deciding first-order properties of locally tree-decomposable structures, Journal of the ACM 48(6), 1184-1206 (2001)"
    locator: first-order model checking on classes of locally bounded treewidth, including planar graphs in linear time
  - paper: doi:10.1145/3051095
    title: "Martin Grohe, Stephan Kreutzer and Sebastian Siebertz, Deciding first-order properties of nowhere dense graphs, Journal of the ACM 64(3), article 17 (2017)"
    locator: "the main theorem, first-order model checking is FPT on every nowhere dense class (conference version STOC 2014)"
  - paper: doi:10.1145/2973749
    title: "Hans L. Bodlaender, Fedor V. Fomin, Daniel Lokshtanov, Eelko Penninkx, Saket Saurabh and Dimitrios M. Thilikos, (Meta) Kernelization, Journal of the ACM 63(5), article 44 (2016)"
    locator: "protrusion decompositions and the linear kernels on graphs of bounded genus (conference version FOCS 2009)"
  - paper: doi:10.1016/j.apal.2004.01.007
    title: "Markus Frick and Martin Grohe, The complexity of first-order and monadic second-order logic revisited, Annals of Pure and Applied Logic 130(1-3), 3-31 (2004)"
    locator: the non-elementary lower bounds for MSO on words and for first-order logic on trees
  - book: isbn:9783319212746
    title: "Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015"
    locator: "Section 7.4 (Courcelle's theorem) and the bibliographic notes of Chapter 7 (cliquewidth, Frick and Grohe, related frameworks)"
---

An algorithmic meta-theorem is a single result that gives an efficient algorithm, or a kernel, for every problem in a whole family. The family is usually defined by a logic, and the result holds on a class of graphs with some structure. The standard example is [Courcelle's theorem](/courcelle-theorem/): every MSO2 property is decidable in linear time on graphs of bounded [treewidth](/treewidth/). This page is about the family of such results; the individual theorems and techniques have their own pages.

## In plain words

Instead of writing a clever algorithm for each problem, you write the problem as a short sentence in a formal language. A meta-theorem then says: on this kind of graph, every question that you can write in this language can be answered fast. Richer languages can say more, but they need graphs with more structure. A language that can talk about sets of vertices needs graphs that look like thin trees. A simpler language that can only talk about single vertices works on much larger kinds of sparse graphs. The price is always a huge hidden factor that depends on the length of the sentence. So a meta-theorem tells you that a fast algorithm exists, and then people look for a practical one.

## The idea

A meta-theorem has three parts.

- **A logic.** First-order logic (FO) quantifies over vertices only. MSO1 also quantifies over sets of vertices. MSO2 also quantifies over sets of edges. Counting MSO (CMSO) adds predicates for set sizes modulo a number. More quantifiers make more problems expressible.
- **A graph class.** Examples, from narrow to wide: bounded treewidth, bounded cliquewidth, bounded degree, planar graphs, graphs of bounded local treewidth, graphs that exclude a fixed minor, classes of bounded expansion, and nowhere dense classes. A wider class has less structure to work with.
- **A result.** Model checking in time $f(\lVert\varphi\rVert, \text{class}) \cdot n^{c}$, which is FPT with the length of the formula as the parameter. Or a kernel of linear size for every problem with some extra property. Or a subexponential algorithm.

The parameter is the length $\lVert\varphi\rVert$ of the formula, often together with a structural parameter such as the treewidth $t$. A problem with a solution size $k$ fits this form when its sentence has length bounded by a function of $k$. For example, "there is a dominating set of size $k$" is the FO sentence

$$\exists x_1 \dots \exists x_k \, \forall y \, \bigvee_{i=1}^{k} \big(y = x_i \vee \mathrm{adj}(y, x_i)\big),$$

of length $O(k)$. So an FPT result for FO model checking on a class gives an FPT algorithm for $k$-dominating set on that class.

The main trade-off is between the logic and the class. MSO can express 3-colorability, which is NP-complete on planar graphs, so MSO model checking cannot be FPT on planar graphs unless $\mathsf{P} = \mathsf{NP}$. FO cannot express 3-colorability, and FO model checking is FPT on planar graphs. On all graphs, FO model checking is not FPT unless $\mathsf{FPT} = \mathsf{W}[2]$, because dominating set is W[2]-complete (see the [W-hierarchy](/w-hierarchy/)).

## Examples

| logic | graph class | result | source |
|---|---|---|---|
| MSO2 | bounded treewidth | decision and optimization in time $f(\lVert\varphi\rVert, t) \cdot n$ | Courcelle 1990; Arnborg, Lagergren and Seese 1991 |
| MSO1 | bounded cliquewidth | linear time, given a decomposition | Courcelle, Makowsky and Rotics |
| FO | planar graphs, and classes of bounded local treewidth | linear time on planar graphs | Frick and Grohe 2001 |
| FO | nowhere dense classes | FPT, time $f(\lVert\varphi\rVert, \varepsilon) \cdot n^{1+\varepsilon}$ for every $\varepsilon > 0$ | Grohe, Kreutzer and Siebertz 2017 |
| problems with finite integer index and a compactness condition (CMSO-based) | bounded genus | linear kernels | Bodlaender, Fomin, Lokshtanov, Penninkx, Saurabh and Thilikos 2016 |
| minor- or contraction-bidimensional problems | planar and H-minor-free graphs | time $2^{O(\sqrt{k})} \cdot n^{O(1)}$ | see [bidimensionality theory](/bidimensionality-theory/) |

A small example of the FO sentence above. By exhaustive search, the domination number is 3 for the 3 by 3 grid, 3 for the Petersen graph and 4 for the 4 by 4 grid. So the sentence with $k = 3$ is true on the first two graphs and false on the 4 by 4 grid. The grids are planar, so the result of Frick and Grohe decides this sentence in linear time on all planar graphs, with a constant that depends on $k$.

Each row has a known cost. The function $f$ in Courcelle's theorem must be non-elementary unless $\mathsf{P} = \mathsf{NP}$, already on words, and Frick and Grohe (2004) prove non-elementary lower bounds for FO on trees as well. So the constants of these theorems are not a weakness of the proofs only.

The kernel row works by *protrusion replacement*. A protrusion is a part of the graph of bounded treewidth with a small boundary. Bodlaender et al. show that on graphs of bounded genus, a yes-instance has a decomposition into $O(k)$ protrusions and a small core. When the problem has finite integer index, each large protrusion can be replaced by a small one with the same behavior at its boundary, so the kernel has $O(k)$ vertices.

## Where it is used

- **Quick classification.** To show that a problem is FPT on a graph class, write it in the right logic. Then search for a direct algorithm with a small constant. Many problem-specific dynamic programs on tree decompositions started this way.
- **Minor-closed properties.** For each fixed $H$, "$H$ is a minor of $G$" is MSO2, so [minor testing](/minor-testing/) is linear on bounded treewidth. With the [graph minor theorem](/graph-minor-theorem/) and the [grid minor theorem](/grid-minor-theorem/), this gives tests for many minor-closed properties.
- **Win/win algorithms.** Meta-theorems handle the small-treewidth case in arguments that use the [irrelevant vertex technique](/irrelevant-vertex-technique/) or bidimensionality.
- **Kernels.** Meta-kernelization gives linear [kernels](/kernelization/) on sparse graph classes for many problems at once, such as dominating set and feedback vertex set on planar graphs.
- **Databases.** Model checking is query evaluation. The results say which query languages can be evaluated fast on which databases, with the query length as the parameter.

## References
