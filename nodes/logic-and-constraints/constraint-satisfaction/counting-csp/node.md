---
tag: 1AKF8D
kind: problem
slug: counting-csp
name: Counting constraint satisfaction problem
aliases:
- '#CSP'
- counting CSP
- weighted counting CSP
area: logic-and-constraints/constraint-satisfaction
level: research
summary: Count the number of satisfying assignments of a constraint problem.
prereqs: [constraint-satisfaction-problem, constraint-language-polymorphisms]
see_also: [csp-dichotomy-theorem, boolean-constraint-satisfaction, schaefer-dichotomy-theorem, approximate-counting, counting-perfect-matchings, bucket-elimination, tree-structured-csp, xor-sat]
sources:
  - paper: doi:10.1145/2528400
    title: Andrei A. Bulatov, The complexity of the counting constraint satisfaction problem, Journal of the ACM 60(5), 2013
    locator: "the dichotomy theorem, every #CSP with a finite template is in FP or #P-complete"
  - paper: doi:10.1137/100811258
    title: Martin Dyer and David Richerby, An effective dichotomy for the counting constraint satisfaction problem, SIAM Journal on Computing 42(3), 2013
    locator: pages 1245 to 1274 (a simpler proof of the dichotomy, the strong balance criterion and its decidability)
  - paper: "Nadia Creignou and Miki Hermann, Complexity of generalized satisfiability counting problems, Information and Computation 125(1), 1996, pages 1 to 12"
    locator: "Boolean #CSP is in FP when every relation is affine and #P-complete otherwise"
  - paper: "Andrei Bulatov and Víctor Dalmau, Towards a dichotomy theorem for the counting constraint satisfaction problem, Information and Computation 205(5), 2007, pages 651 to 678"
    locator: "a Mal'tsev polymorphism is necessary for #CSP in FP, and pp-definable relations can be added without changing the complexity of #CSP"
  - paper: "Martin Dyer and Catherine Greenhill, The complexity of counting graph homomorphisms, Random Structures and Algorithms 17(3-4), 2000, pages 260 to 289"
    locator: the dichotomy for counting H-colourings of graphs
  - paper: doi:10.1137/0208032
    title: Leslie G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8(3), 1979
    locator: pages 410 to 421 (#P-completeness of counting for problems whose decision version is easy, including monotone 2-SAT)
  - paper: "Martin Dyer, Leslie Ann Goldberg and Mark Jerrum, An approximation trichotomy for Boolean #CSP, Journal of Computer and System Sciences 76(3-4), 2010, pages 267 to 277"
    locator: "approximate counting for Boolean #CSP, in FP, equivalent to #BIS, or equivalent to #SAT under approximation-preserving reductions"
  - paper: "Jin-Yi Cai and Xi Chen, Complexity of counting CSP with complex weights, Journal of the ACM 64(3), 2017"
    locator: "the dichotomy for weighted #CSP with complex-valued constraint functions"
---

The counting constraint satisfaction problem, #CSP, asks for the number of solutions of an instance of the [constraint satisfaction problem](/constraint-satisfaction-problem/), not just whether one exists. For a fixed finite constraint language $\Gamma$, #CSP($\Gamma$) is in the class #P. Bulatov (2013) proved that every #CSP($\Gamma$) is either solvable in polynomial time, in FP, or #P-complete, and Dyer and Richerby (2013) gave a simpler proof with a decidable criterion. The easy side is much smaller than for the decision problem: on Boolean domains only the affine languages, systems of XOR equations, are easy to count (Creignou and Hermann 1996), although Horn and 2-SAT are easy to decide.

## In plain words

The ordinary constraint problem asks: can all the rules hold at once? The counting problem asks: in how many ways? Counting is at least as hard as deciding, since a count above zero answers the yes or no question, and often it is much harder. Finding one independent set in a graph is trivial, since the empty set works, but counting all of them is believed to need exponential time.

For a fixed set of rule types, counting is either easy or as hard as counting the solutions of any problem in NP. The easy rule types have a very rigid structure, close to linear equations, that lets one count without listing.

## Definition

Let $D$ be a finite domain and $\Gamma$ a finite set of relations on $D$.

**#CSP($\Gamma$).** *Input:* an instance of CSP($\Gamma$): variables $x_1, \ldots, x_n$ and constraints $R(x_{i_1}, \ldots, x_{i_r})$ with $R \in \Gamma$. *Output:* the number of assignments $s \in D^n$ that satisfy all constraints.

**Weighted #CSP.** Replace relations by functions $F: D^r \to \mathbb{C}$, or to the non-negative rationals. The output is the *partition function*
$$Z = \sum_{s \in D^n} \prod_{\text{constraints } F(x_{i_1}, \ldots, x_{i_r})} F(s_{i_1}, \ldots, s_{i_r}).$$
A relation is the 0-1 valued function, so #CSP is the special case of 0-1 weights.

**Classes.** #P is the class of functions that count the accepting paths of a polynomial-time nondeterministic machine, and FP is the class of functions computable in polynomial time. A function is #P-complete if it is in #P and every #P function reduces to it by polynomial-time Turing reductions. Toda's theorem shows that a #P-complete function makes the whole polynomial hierarchy computable in polynomial time, so #P-complete problems are believed to be much harder than NP-complete ones.

**The dichotomy.** For every finite $\Gamma$, #CSP($\Gamma$) is in FP or #P-complete (Bulatov 2013). The criterion of Dyer and Richerby (2013), *strong balance*, asks that for every relation that is primitive positive definable from $\Gamma$, and every split of its variables into three groups $\bar{x}$, $\bar{y}$, $\bar{z}$, the matrix whose entry at $(\bar{x}, \bar{z})$ is the number of $\bar{y}$ completing the tuple is, after reordering rows and columns, block diagonal with blocks of rank 1. They showed that this property is decidable for a given $\Gamma$.

**A necessary condition.** A *Mal'tsev* operation satisfies $m(x, y, y) = m(y, y, x) = x$. Bulatov and Dalmau (2007) showed that if $\Gamma$ has no Mal'tsev [polymorphism](/constraint-language-polymorphisms/), then #CSP($\Gamma$) is #P-complete. One reason is rectangularity. A binary relation $R$ is *rectangular* if $(a, c), (a, d), (b, c) \in R$ imply $(b, d) \in R$. If $m$ is a Mal'tsev polymorphism of $R$, then applying it to $(b, c)$, $(a, c)$ and $(a, d)$ gives $(m(b, a, a), m(c, c, d)) = (b, d) \in R$. So with a Mal'tsev polymorphism every pp-definable binary relation is rectangular, and the count splits into products over blocks; a non-rectangular pp-definable relation gives a hardness reduction.

**How the pages relate.** The [CSP dichotomy theorem](/csp-dichotomy-theorem/) is about the decision problem; its tractable side, the languages with a weak near-unanimity polymorphism, is much larger than the FP side here. The [Boolean CSP](/boolean-constraint-satisfaction/) page covers the domain $\{0, 1\}$, where the counting criterion is "affine". This page covers counting over any finite domain, the weighted version and approximate counting.

## Variants

- **Boolean domain.** #CSP($\Gamma$) on $\{0, 1\}$ is in FP if every relation of $\Gamma$ is affine and #P-complete otherwise (Creignou and Hermann 1996). This differs from [Schaefer's theorem](/schaefer-dichotomy-theorem/), where Horn, dual Horn, bijunctive, 0-valid and 1-valid languages are also easy.
- **Graph homomorphisms.** For a graph $H$, #$H$-colouring counts the homomorphisms from a given graph to $H$. Dyer and Greenhill (2000) showed it is in FP when each connected component of $H$ is a complete graph with a loop at every vertex or a complete bipartite graph with no loops, and #P-complete otherwise.
- **Weighted.** For non-negative and real weights, and then for complex weights (Cai and Chen 2017), the weighted #CSP also has a dichotomy between FP and #P-hard. Complex weights allow cancellation, and the easy cases then include some that come from quadratic forms over $\mathbb{Z}_4$ and from holographic transformations.
- **Holant problems.** When each variable appears in exactly two constraints, the problem is a Holant problem. Counting perfect matchings is of this kind, and on planar graphs it is in FP by the FKT algorithm, which shows that structural restrictions change the picture.
- **Approximate counting.** For Boolean $\Gamma$, Dyer, Goldberg and Jerrum (2010) showed a trichotomy under approximation-preserving reductions: in FP if affine, otherwise as hard as counting independent sets in bipartite graphs (#BIS) if every relation is a conjunction of unary relations and implications, and otherwise as hard as #SAT.
- **Bounded structure.** Instead of restricting $\Gamma$, restrict the instance: bounded [treewidth](/treewidth/) of the constraint graph makes every #CSP polynomial, with any language.

## Examples

**Graph colourings.** #CSP($\{\ne\}$) on a domain of $k$ values counts proper $k$-colourings. A path on $n$ vertices has $3 \cdot 2^{n-1}$ proper 3-colourings, and a cycle $C_n$ has $2^n + 2(-1)^n$, which is 6 for the triangle and 18 for $C_4$. Counting 3-colourings is #P-complete in general, and for $k = 2$, a connected bipartite graph has exactly 2 colourings and any other connected graph has none, so 2-colourings are easy to count.

**Independent sets.** The relation NAND, $\neg x \vee \neg y$, placed on each edge, makes solutions the independent sets of a graph. The decision problem is trivial, since all 0 works, and NAND is 0-valid, Horn and bijunctive, but not affine. So counting independent sets is #P-complete. A path on 4 vertices has 8 independent sets, a Fibonacci number, which a dynamic program along the path finds; see the tree algorithm below.

**Monotone 2-SAT.** The relation $x \vee y$ gives the same counts as NAND after swapping 0 and 1, so #2-SAT is #P-complete even without negations (Valiant 1979).

**Linear equations.** For $x_0 \oplus x_1 = 1$, $x_1 \oplus x_2 = 1$ and $x_0 \oplus x_2 = 0$, the rank is 2 and the number of solutions is $2^{3 - 2} = 2$, namely $(0, 1, 0)$ and $(1, 0, 1)$. Over $\mathbb{Z}_p$, a consistent system of rank $\rho$ in $n$ variables has $p^{n - \rho}$ solutions.

## Known algorithms

- **Brute force.** Enumerate all $d^n$ assignments and test each, in $O(d^n m r)$ time for $m$ constraints of arity at most $r$.
- **Gaussian elimination.** For affine languages, over $\mathbb{Z}_p$ or a finite field, compute the rank and output $0$ or $p^{n - \rho}$. More generally, the FP side of the dichotomy uses a compact representation of the solution set, a *frame*, which exists for every language with a Mal'tsev polymorphism, and counts through it.
- **Tree-structured instances.** On a constraint graph that is a tree, a pass from the leaves to the root computes for each value the number of solutions of the subtree. The [tree-structured CSP](/tree-structured-csp/) page gives this count in $O(n d^2)$ time.
- **Bucket and variable elimination.** Replacing the join and projection of [bucket elimination](/bucket-elimination/) by product and sum gives the count in $O((m + n) d^{w + 1})$ time for an elimination order of induced width $w$, the same as [variable elimination](/variable-elimination/) in probabilistic models. With a [tree decomposition](/tree-decomposition/) of width $w$ the time is exponential only in $w$.
- **Cutset conditioning.** Summing the tree counts over all assignments of a cycle cutset of size $c$ gives the count in $O(d^c \cdot n d^2)$ time; see [cutset conditioning](/cutset-conditioning/).
- **Approximate counting.** When an exact count is #P-hard, Markov chain Monte Carlo methods can still give a fully polynomial randomized approximation scheme for some problems, such as the number of colourings of a graph of maximum degree $\Delta$ with enough colours; see [approximate counting](/approximate-counting/).
- **Model counters.** Practical #SAT solvers combine DPLL-style search with component decomposition and caching, or compile the formula into a d-DNNF circuit and count on it.

## Bounds

- **Upper.** Every #CSP($\Gamma$) is in #P. On an instance with constraint graph of treewidth $w$ it is solvable in $O^\ast(d^{w + 1})$ time.
- **Lower.** If $\Gamma$ is not strongly balanced, #CSP($\Gamma$) is #P-complete (Bulatov 2013; Dyer and Richerby 2013), so an FP algorithm would collapse the polynomial hierarchy to P by Toda's theorem. #SAT, #3-colouring, #independent sets and #2-SAT are #P-complete.
- **Counting versus deciding.** Every #P-complete problem is NP-hard, but the converse fails: #2-SAT and the count of perfect matchings in a bipartite graph are #P-complete although the decision problems are in P (Valiant 1979).

## Reductions

- **Primitive positive definitions.** For decision, adding a relation that is pp-definable from $\Gamma$ does not change the complexity. Existential quantification does change counts, so for counting the reduction is less direct, but Bulatov and Dalmau (2007) showed that pp-definable relations can still be added without changing the complexity of #CSP($\Gamma$). So the complexity is again a property of the polymorphism clone.
- **Parsimonious reductions.** A reduction that keeps the number of solutions exactly, such as Cook's reduction from a nondeterministic machine to SAT, transfers #P-hardness. Many NP-completeness reductions are parsimonious or can be made so.
- **Interpolation.** Many #P-hardness proofs build instances whose counts are values of a polynomial at several points, then solve a linear system to recover a hard count. Dyer and Greenhill (2000) used this for graph homomorphisms.
- **To probabilistic inference.** The partition function of a weighted #CSP with non-negative weights is the normalizing constant of a Markov random field, so computing marginals by [belief propagation](/belief-propagation/) on trees, or by variable elimination, is a #CSP algorithm.
- **Matchings.** Counting perfect matchings of a bipartite graph is the permanent of its 0-1 matrix, #P-complete by Valiant (1979); see [counting perfect matchings](/counting-perfect-matchings/).

## Applications

- **Statistical physics.** Partition functions of spin systems, such as the Ising and Potts models, are weighted #CSPs on a graph, and the complexity results say when they can be computed exactly.
- **Probabilistic reasoning.** Computing the probability of evidence in a Bayesian network or a Markov random field is a weighted #CSP, solved by elimination or by knowledge compilation.
- **Reliability and verification.** The probability that a system works when parts fail at random, and the number of inputs that make a circuit output 1, are counting problems of this form, solved by model counters.
- **Combinatorics.** Counting colourings, independent sets, matchings and homomorphisms are #CSPs, and their dichotomies explain which closed formulas can exist.

## References
