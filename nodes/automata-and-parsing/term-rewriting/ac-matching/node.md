---
tag: HX6A58
kind: problem
slug: ac-matching
name: Associative-commutative matching
aliases:
- AC matching
area: automata-and-parsing/term-rewriting
level: advanced
summary: Term matching where the function symbols are associative and commutative.
prereqs: [term-matching, rewriting-modulo-equations, equational-theory]
see_also: [ac-unification-problem, bipartite-matching, np-complete, knuth-bendix-completion, discrimination-tree, equational-unification, stickel-ac-unification]
sources:
  - paper: doi:10.1016/S0747-7171(87)80027-5
    title: Dan Benanav, Deepak Kapur and Paliath Narendran, Complexity of matching problems, Journal of Symbolic Computation 3(1-2) (1987)
    locator: pp. 203 to 216 (AC matching, associative matching and commutative matching are NP-complete)
  - paper: doi:10.1093/comjnl/38.5.381
    title: Steven M. Eker, Associative-commutative matching via bipartite graph matching, The Computer Journal 38(5) (1995)
    locator: pp. 381 to 399 (a hierarchy of bipartite graph matching problems that encodes the solutions of subproblems, then a search over them)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 10, Equational unification (unification and matching modulo associativity and commutativity)
---

**Associative-commutative matching**, or AC matching, is [term matching](/term-matching/) when some function symbols are associative and commutative, such as $+$ and $\cdot$ on numbers or union on sets. Given a pattern $p$ and a subject $t$, the task is to find the substitutions $\sigma$ with $p\sigma = t$ modulo the laws $x + (y + z) = (x + y) + z$ and $x + y = y + x$. It is the inner step of [rewriting modulo equations](/rewriting-modulo-equations/) and of completion modulo AC. Unlike syntactic matching, which is linear, it is NP-complete, and a pattern can have exponentially many matchers; for linear patterns it is solvable in polynomial time by [bipartite matching](/bipartite-matching/).

## In plain words

Suppose $+$ is an operation where neither grouping nor order matters, so $a + (b + c)$ and $c + (a + b)$ are the same thing: a bag of parts. A pattern such as $f(x) + y$ asks: can the bag be split into one part of the form $f(\ldots)$ and some other parts? Usually there are many ways to split a bag, and the search must try them. When a pattern uses the same variable twice, such as $x + x + y$, the choices must also agree, and that is what makes the problem hard in general.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, substitutions $\sigma$, rules $l \to r$, and $\to^*$ for reflexive transitive closures. A subset $\Sigma_{AC} \subseteq \Sigma$ of binary symbols is declared associative and commutative. $AC$ is the set of equations $f(x, f(y, z)) \approx f(f(x, y), z)$ and $f(x, y) \approx f(y, x)$ for each $f \in \Sigma_{AC}$, and $=_{AC}$ is its [equational theory](/equational-theory/). We write $f$ in infix as $+$ when there is one.

**Input.** A pattern $p \in T(\Sigma, V)$ and a subject $t$, usually ground.

**Question.** Is there a substitution $\sigma$ with $p\sigma =_{AC} t$? The search version asks for one matcher, and the enumeration version for a complete set: a set of matchers such that every matcher agrees, modulo $AC$ on the variables of $p$, with one of them. A finite complete set always exists, because each $x\sigma$ can be chosen among the finitely many parts of $t$.

**Flattened form.** Every term has a flattened form, in which nested occurrences of an AC symbol are merged into one node with a multiset of arguments, $a + (b + c) \mapsto {+}\{a, b, c\}$, and no argument of an $f$-node has the root $f$. Two terms are $=_{AC}$ iff their flattened forms are equal, with arguments compared as multisets. Sorting the arguments by a fixed total order makes the flattened form canonical, so $=_{AC}$ is decidable in polynomial time.

## Variants

- **Commutative matching and associative matching.** Only one of the two laws holds. Both are also NP-complete (Benanav, Kapur and Narendran).
- **ACU matching.** The symbol also has a unit $0$ with $x + 0 = x$, so a variable may take the empty part. This removes the requirement that each part be nonempty.
- **ACI matching.** Also idempotent, $x + x = x$, as for set union. Set matching is a special case, and it is NP-complete as well (Kapur and Narendran).
- **Linear patterns.** No variable occurs twice in $p$. This case is in polynomial time (see below).
- **Many-to-one matching.** Match one subject against many patterns at once, as rewriting with many rules does. Indexes such as [discrimination trees](/discrimination-tree/) are extended to AC symbols for this.
- **AC unification.** Both terms have variables. This is the [AC unification problem](/ac-unification-problem/), solved by [Stickel's algorithm](/stickel-ac-unification/) with Diophantine equations; matching is the special case of a ground right side.

## Examples

Let $+$ be AC and let $a, b, c, d$ be distinct constants.

| pattern | subject | matchers |
|---|---|---|
| $x + y$ | $a + b + c$ | 6: $x$ takes a nonempty proper part, $y$ the rest |
| $f(x) + x$ | $f(a) + a$ | 1: $x \mapsto a$ |
| $f(x) + x$ | $f(a + b) + a + b$ | 1: $x \mapsto a + b$ |
| $f(x) + x$ | $f(a) + b$ | none |
| $x + x + y$ | $a + a + b + b + c$ | 3: $x \mapsto a$, $x \mapsto b$, or $x \mapsto a + b$ with $y \mapsto c$ |
| $x + x$ | $a + a + b + b$ | 1: $x \mapsto a + b$ |
| $f(x) + g(y) + z$ | $f(a) + f(b) + g(c) + d$ | 2: $x \mapsto a$ or $x \mapsto b$, with $y \mapsto c$ |

The first line shows the blow-up: $x + y$ against a sum of $n$ distinct constants has $2^n - 2$ matchers, one for each nonempty proper subset that $x$ takes. In the third line, $x$ binds to a sum, which a syntactic matcher cannot produce. In the sixth line, the repeated variable forces both parts to be equal multisets.

## Known algorithms

- **Backtracking over flattened terms.** Flatten $p$ and $t$. At a node $f$ of $\Sigma_{AC}$, match the non-variable arguments of $p$ one at a time against distinct arguments of $t$ with the same root, recursively, and backtrack on failure; then split the remaining arguments of $t$ among the variable arguments of $p$, each part nonempty, consistent with bindings already made. This is the classic method of the first AC rewriting systems. It is exponential in the worst case, as it must be unless P = NP.
- **Bipartite graph matching.** Eker (1995) builds, for each AC node of the pattern, a bipartite graph between pattern arguments and subject arguments that they can match, and records the solutions of the subproblems in a hierarchy of such graphs. A search over this structure then finds complete matchers. Many patterns are rejected early because the graph has no matching that covers the pattern side. The Maude system uses this method.
- **Linear patterns in polynomial time.** If $p$ is linear, the following decides matchability. For a variable, answer yes. For $p = g(p_1, \ldots, p_n)$ with $g \notin \Sigma_{AC}$, require $t = g(t_1, \ldots, t_n)$ and solve each pair $(p_i, t_i)$. For a flattened $p = f\{q_1, \ldots, q_k, x_1, \ldots, x_v\}$ with non-variable $q_i$ and variables $x_j$, require $t = f\{t_1, \ldots, t_n\}$, build the bipartite graph with an edge $q_i\, t_j$ when $q_i$ matches $t_j$, and answer yes iff it has a matching that covers all $q_i$, and $n - k \ge v$ when $v \ge 1$, or $n = k$ when $v = 0$.

*Proof.* Each $q_i$ is not a variable and its root is not $f$, so $q_i\sigma$ is one argument of the flattened $t$, and distinct $q_i$ take distinct argument occurrences; the variables $x_j$ take the remaining $n - k$ occurrences in $v$ nonempty parts. So a matcher gives a covering matching and the count condition. Conversely, take a covering matching and a matcher of each matched pair, and split the $n - k$ remaining arguments into $v$ nonempty parts. Because $p$ is linear, these matchers bind disjoint sets of variables, so their union is a substitution, and it matches $p$ to $t$. Any covering matching works, since the number $n - k$ of remaining arguments does not depend on it. $\blacksquare$

With memoization over pairs of a pattern node and a subject node, and a polynomial bipartite matching algorithm such as [Hopcroft-Karp](/hopcroft-karp/), the whole test runs in polynomial time.

## Bounds

**In NP.** If $p\sigma =_{AC} t$, then for every variable $x$ of $p$, the flattened $x\sigma$ is a part of the flattened $t$: either a subterm of it, or an $f$-node built from a sub-multiset of the arguments of an $f$-node of $t$. So it has size at most $|t|$. A certificate is such a $\sigma$, and the check $p\sigma =_{AC} t$ compares canonical flattened forms in polynomial time.

**NP-hard.** Benanav, Kapur and Narendran (1985, journal version 1987) proved that AC matching is NP-complete, with uninterpreted symbols allowed next to AC symbols, and that commutative matching and associative matching are NP-complete as well. Later work showed that the problem stays NP-complete in very restricted forms: even when the pattern is one AC symbol applied to variables, some of them repeated, and the subject is the same symbol applied to constants. The hardness comes from repeated variables, as the polynomial algorithm for linear patterns shows.

**Number of matchers.** A minimal complete set of matchers can have exponential size, as the example $x + y$ with $2^n - 2$ matchers shows, so enumerating all of them takes exponential time in the worst case, whatever the algorithm.

## Reductions

- **To bipartite matching.** Linear AC matching reduces to a sequence of [bipartite matching](/bipartite-matching/) problems, one per AC node pair, as above.
- **From AC unification.** AC matching is AC unification with a ground side, so every AC unification algorithm also solves matching, but less efficiently than a dedicated matcher.
- **From NP-complete problems.** The hardness proofs encode a combinatorial problem in the repeated variables of an AC pattern, and the result transfers to commutative and associative matching.

## Applications

- **Rewriting modulo AC.** Systems such as Maude and the OBJ family rewrite modulo associativity and commutativity, and each rewrite step calls AC matching on the left sides of the rules. AC matching is the dominant cost of such a step.
- **Completion modulo AC.** [Knuth-Bendix completion](/knuth-bendix-completion/) cannot orient commutativity. Peterson and Stickel built AC into matching and unification so that completion works for theories with AC operators, such as abelian groups and commutative rings.
- **Computer algebra and pattern-based programming.** Pattern matchers for algebraic expressions treat $+$ and $\times$ as associative and commutative. Mathematica's attributes Flat and Orderless declare these laws for a symbol, and the Python library MatchPy implements many-to-one AC matching.
- **Theorem proving.** Equational provers with AC symbols use AC matching for simplification, and AC unification for inference.

## References
