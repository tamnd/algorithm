---
tag: N1M60Z
kind: problem
slug: unification-problem
name: Unification problem
aliases:
- first-order unification
- term unification
area: logic-and-constraints/unification-and-resolution
level: core
summary: Given terms or equations, decide whether a unifier exists and compute a most general unifier.
model: word-ram
complexity:
  vars: {N: the total size of the input terms}
  time: {decide: O(N), mgu as a DAG: O(N)}
  space: {extra: O(N)}
prereqs: [unifier, most-general-unifier, term]
see_also: [mgu-existence-theorem, robinson-unification, martelli-montanari-unification, paterson-wegman-unification, occurs-check, term-matching, equational-unification, anti-unification-problem]
sources:
  - paper: doi:10.1145/321250.321253
    title: J. A. Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965, pages 23 to 41
    locator: the unification algorithm and the unification theorem
  - paper: doi:10.1145/357162.357169
    title: Alberto Martelli and Ugo Montanari, An efficient unification algorithm, ACM Transactions on Programming Languages and Systems 4(2), 1982, pages 258 to 282
    locator: the formulation of unification as solving a set of equations by transformations, and the efficient algorithm
  - paper: "M. S. Paterson and M. N. Wegman, Linear unification, Journal of Computer and System Sciences 16(2), 1978, pages 158 to 167"
    locator: the linear-time algorithm on term DAGs
  - paper: doi:10.1145/62029.62030
    title: "Kevin Knight, Unification: a multidisciplinary survey, ACM Computing Surveys 21(1), 1989"
    locator: the sections on the history of unification algorithms, their complexity, and the parallel complexity of unification
  - paper: "Cynthia Dwork, Paris C. Kanellakis and John C. Mitchell, On the sequential nature of unification, Journal of Logic Programming 1(1), 1984, pages 35 to 50"
    locator: the proof that unification is complete for P under log-space reductions
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 2 (syntactic unification, its algorithms and complexity)
---

The **unification problem** asks, for two first-order [terms](/term/) $s$ and $t$ (or a finite set of equations), whether some [substitution](/substitution/) makes them identical, and if so, to compute a [most general unifier](/most-general-unifier/). It is the basic operation of resolution theorem proving, of Prolog and of type inference. The [unification theorem](/mgu-existence-theorem/) says that the answer, when it exists, is one mgu, unique up to renaming. [Robinson's algorithm](/robinson-unification/) of 1965 solves it, the [Paterson-Wegman algorithm](/paterson-wegman-unification/) solves it in linear time, and the [Martelli-Montanari algorithm](/martelli-montanari-unification/) solves it in almost linear time with a simpler structure.

## In plain words

You have two patterns built from fixed symbols and blanks. Can you fill the blanks so that the two patterns become exactly the same? A blank can be filled with any pattern, but the same blank must get the same filling everywhere it appears.

Sometimes the answer is no. Two different fixed symbols at the same place can never match. A blank also cannot be filled with a pattern that holds itself, because the result would grow forever. When the answer is yes, the problem asks for the filling that commits to the least. Every other filling is that filling plus more choices. This one filling exists whenever any filling exists, and a computer can find it in time proportional to the size of the patterns.

## Definition

Fix a signature $\Sigma$ of function symbols with arities and an infinite set $V$ of variables. $T(\Sigma, V)$ is the set of terms. Notation: $n$ is the number of distinct variables, $m$ the number of equations, $N$ the total number of symbol occurrences in the input, $\sigma, \theta$ are substitutions and $t\sigma$ is the application of $\sigma$ to $t$.

**Input.** A finite set of equations $E = \{s_1 \doteq t_1, \ldots, s_m \doteq t_m\}$ over $T(\Sigma, V)$.

**Decision version.** Is there a substitution $\sigma$ with $s_i\sigma = t_i\sigma$ for each $i$, where $=$ is syntactic identity? Such a $\sigma$ is a [unifier](/unifier/).

**Search version.** If $E$ is unifiable, output a most general unifier $\sigma$: a unifier with $\sigma \le \theta$ for every unifier $\theta$, where $\sigma \le \theta$ means $\theta = \sigma\lambda$ for some $\lambda$. Otherwise output "not unifiable".

**Output form.** The output can be an explicit map $\{x_1 \mapsto t_1, \ldots, x_k \mapsto t_k\}$ in [idempotent](/idempotent-substitution/) form, a triangular form (a composition of single bindings), or bindings on a [term DAG](/term-dag/). The choice matters: the explicit map can be exponentially larger than the input, while the other two forms have size $O(N)$.

The single equation $s \doteq t$ and the set $E$ are the same problem: with a new symbol $h$ of arity $m$, $E$ has the same unifiers as $h(s_1, \ldots, s_m) \doteq h(t_1, \ldots, t_m)$.

## Variants

- **Matching.** Only one side may be instantiated: find $\sigma$ with $s\sigma = t$. See [term matching](/term-matching/). It is easier: no [occurs check](/occurs-check/) is needed, and it is in [NC](/nc/).
- **Unification without the occurs check, or over rational trees.** If $x \doteq f(x)$ is allowed to have a solution, the solutions are infinite regular (rational) trees. Prolog II used this model, and many Prolog systems omit the occurs check for speed. The problem is then an equivalence closure on a graph, solved by union-find in almost linear time.
- **Unification of term DAGs.** The input is a DAG with shared subterms, and the size $N$ counts DAG nodes. The [Paterson-Wegman](/paterson-wegman-unification/) and union-find algorithms work directly on this input.
- **Equational unification.** Equality is modulo a theory $E$, such as associativity and commutativity. One mgu may not exist, and the problem may be undecidable. See [equational unification](/equational-unification/) and [AC unification](/ac-unification-problem/).
- **Higher-order unification.** Variables may stand for functions, and equality is modulo $\beta\eta$. See the [higher-order unification problem](/higher-order-unification-problem/); it is undecidable already at second order. [Pattern unification](/pattern-unification-problem/) is a decidable fragment with mgus.
- **Nominal unification.** Terms have binders and names, and equality is modulo $\alpha$-renaming. See the [nominal unification problem](/nominal-unification-problem/).
- **Semi-unification.** Solve inequalities $s \le t$, meaning $t\sigma$ is an instance of $s\sigma$. See the [semi-unification problem](/semi-unification-problem/); it is undecidable.
- **Anti-unification.** The dual problem: find the most specific term of which both inputs are instances. See the [anti-unification problem](/anti-unification-problem/).

## Examples

Below $a, b$ are constants, $f, g, h$ are function symbols and $x, y, z, x_i$ are variables.

| input | answer | reason |
|---|---|---|
| $f(x, g(y), y) \doteq f(g(z), w, a)$ | $\{x \mapsto g(z),\ w \mapsto g(a),\ y \mapsto a\}$ | unifiable |
| $f(x_1, h(x_1), x_2) \doteq f(g(x_3), x_4, x_3)$ | $\{x_1 \mapsto g(x_3),\ x_4 \mapsto h(g(x_3)),\ x_2 \mapsto x_3\}$ | unifiable |
| $f(x, y) \doteq f(y, x)$ | $\{x \mapsto y\}$ | unifiable, one variable stays free |
| $f(x, a) \doteq g(y, a)$ | not unifiable | clash of $f$ and $g$ |
| $f(x, x) \doteq f(a, b)$ | not unifiable | $x$ would need two values |
| $x \doteq f(x)$ | not unifiable | occurs check |
| $f(x, y) \doteq f(g(y), g(x))$ | not unifiable | occurs check through two steps: $x = g(g(x))$ |

**An mgu of exponential size.** Let $s = f(x_1, \ldots, x_n)$ and $t = f(g(x_0, x_0), g(x_1, x_1), \ldots, g(x_{n-1}, x_{n-1}))$. The input has size $4n + 2$. The mgu maps $x_i$ to the complete binary tree of $g$ nodes of height $i$, so $s\sigma$ has $2^{n+2} - n - 3$ nodes. With shared subterms, $s\sigma$ has only $n + 2$ DAG nodes. [Robinson's algorithm](/robinson-unification/) on trees spends exponential time on this input, and a DAG-based algorithm spends linear time.

## Known algorithms

| algorithm | year | time | notes |
|---|---|---|---|
| [Robinson](/robinson-unification/) | 1965 | exponential on trees | disagreement pairs; explicit idempotent mgu |
| Robinson with shared terms (Corbin and Bidoit) | 1983 | $O(N^2)$ | the same algorithm on DAGs |
| Huet, union-find | 1976 | $O(N\,\alpha(N))$ | works over rational trees; a final acyclicity test gives finite-tree unification |
| [Paterson and Wegman](/paterson-wegman-unification/) | 1978 | $O(N)$ | term DAG; checks the occurs condition during the search |
| [Martelli and Montanari](/martelli-montanari-unification/) | 1982 | almost linear | transformation rules on sets of equations and multiequations |

The transformation rules of Martelli and Montanari (delete, decompose, clash, orient, occurs check, eliminate) are the standard textbook form. They also define the problem in its clearest form: unification is the solving of a set of equations until it is in solved form.

## Bounds

- **Upper bound.** $O(N)$ time and space on a RAM, for the decision and for an mgu given as DAG bindings (Paterson and Wegman). This is optimal, since the input has to be read.
- **Output size.** An mgu written as an explicit map can need $\Omega(2^{N/4})$ symbols, as the example above shows. So no algorithm can output the explicit map in polynomial time in the worst case, and linear bounds always refer to a shared representation.
- **Parallel complexity.** Unification is complete for P under log-space reductions (Dwork, Kanellakis and Mitchell, 1984), with a reduction from the [monotone circuit value problem](/circuit-value-problem/). So it is not in [NC](/nc/) unless $\mathrm{NC} = \mathrm{P}$. Term matching is in NC (Dwork, Kanellakis and Stockmeyer, 1988).
- **Without the occurs check.** Over rational trees the problem is an equivalence closure; with union-find it takes $O(N\,\alpha(N))$, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/).

## Reductions

- **Sets of equations to one equation.** Pair all left sides under a new symbol $h$ and all right sides under $h$, as in the definition.
- **To a closure on a graph.** Build one [term DAG](/term-dag/) for both sides and merge the two roots. The finest equivalence on nodes that contains the merged pair and is closed downward (if two function nodes are merged, their $i$-th children are merged) is computed with a [disjoint-set forest](/disjoint-set-forest/). $E$ is unifiable if and only if no class holds two different function symbols and the graph of classes has no cycle. This is the dual of [congruence closure](/congruence-closure/), which closes upward from children to parents. The same merge-and-propagate loop decides the equivalence of finite automata in the [Hopcroft-Karp algorithm](/hopcroft-karp-equivalence/).
- **Cycle test.** The occurs condition becomes "the quotient graph is acyclic", which a [topological sort](/topological-sort/) or [cycle detection](/cycle-detection/) checks in linear time.
- **From the circuit value problem.** The P-hardness proof encodes the gates of a monotone circuit as equations, so that unification forces the variable of the output gate to a term that shows the circuit value.

## Applications

- **Resolution theorem proving.** [Binary resolution](/binary-resolution/), [factoring](/factoring/), [paramodulation](/paramodulation/) and [superposition](/superposition/) apply the mgu of literals or terms. Provers call unification millions of times and use [term indexing](/term-indexing/) to filter candidates.
- **Logic programming.** Each step of [SLD resolution](/sld-resolution/) unifies a goal with a clause head after [standardization apart](/standardization-apart/). The [Warren abstract machine](/warren-abstract-machine/) compiles clause heads to unification instructions.
- **Type inference.** Hindley-Milner type inference in ML and Haskell generates equations between type terms and solves them by unification; the occurs check rejects infinite types.
- **Term rewriting.** Critical pairs in [Knuth-Bendix completion](/knuth-bendix-completion/) come from mgus of overlapping left sides.

## References
