---
tag: H9NYNK
kind: problem
slug: term-matching
name: Term matching
aliases:
- Matching problem
- Term matching algorithm
- matching
- one-way matching algorithm
- one-way unification
- pattern matching
- term matching
area: automata-and-parsing/term-rewriting
level: core
summary: Find a substitution that makes a pattern term equal to a subject term.
model: word-ram
complexity:
  vars: {m: the size of the pattern, n: the size of the subject}
  time: {worst: Θ(m + n)}
prereqs: [term, substitution]
see_also: [unification-problem, tree-pattern-matching, ac-matching, discrimination-tree, hoffmann-odonnell-matching, rewrite-step, term-indexing, e-matching]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 4, Equational problems (matching as a special case of syntactic unification); Chapter 10, Equational unification
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification theory, in Alan Robinson and Andrei Voronkov (editors), Handbook of Automated Reasoning, Volume I, Elsevier, 2001
    locator: Chapter 8 (syntactic matching and unification, and matching modulo equational theories)
  - paper: doi:10.1016/S0747-7171(87)80027-5
    title: Dan Benanav, Deepak Kapur and Paliath Narendran, Complexity of matching problems, Journal of Symbolic Computation 3(1-2) (1987)
    locator: pp. 203 to 216 (matching modulo associativity, commutativity, and both, is NP-complete)
  - paper: doi:10.1145/322290.322295
    title: Christoph M. Hoffmann and Michael J. O'Donnell, Pattern matching in trees, Journal of the ACM 29(1) (1982)
    locator: pp. 68 to 95
---

**Term matching** asks, for a pattern term $s$ and a subject term $t$, for a [substitution](/substitution/) $\sigma$ with $s\sigma = t$. Only the variables of the pattern may be replaced; the variables of the subject act as constants. It is the test that decides whether a [rewrite rule](/rewrite-rule/) applies at a position, so every [rewrite step](/rewrite-step/), every pattern-matching function of a functional language and every demodulation step of a theorem prover solves it. Syntactic matching takes $\Theta(m + n)$ time in the worst case on terms of sizes $m$ and $n$, while matching modulo associativity and commutativity is NP-complete.

## In plain words

A pattern is an expression with some blanks in it, each blank with a name. Matching asks: can you fill the blanks so that the pattern becomes exactly a given expression? A blank that appears twice must be filled the same way both times. The given expression is fixed: if it has blanks of its own, they are treated as ordinary fixed names.

A program tries this by walking down both expressions together. Where the pattern has an operation, the expression must have the same operation, and the walk goes on into the arguments. Where the pattern has a blank, the walk records what is in the expression at that place, or, if the blank already has a value, checks that the two are the same.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, substitutions $\sigma$ applied as $t\sigma$.

**Input.** Two terms $s, t \in T(\Sigma, V)$: the **pattern** $s$ and the **subject** $t$.

**Output.** A substitution $\sigma$ with $\mathrm{dom}(\sigma) \subseteq \mathrm{Var}(s)$ and $s\sigma = t$ (a **matcher**), or the answer that none exists. We say $t$ is an **instance** of $s$, and $s$ **subsumes** $t$, written $s \lesssim t$.

**Uniqueness.** If a matcher exists, it is unique on $\mathrm{Var}(s)$: for each $x \in \mathrm{Var}(s)$ at a position $p$ of $s$, $x\sigma = (s\sigma)|_p = t|_p$. So the decision version and the search version have the same answer, and the matcher, when it exists, is $\{x \mapsto t|_{p_x}\}$ for any choice of positions $p_x$ of $x$ in $s$.

**Existence.** A matcher exists iff (a) every function position $p$ of $s$ is a position of $t$ with $s(p) = t(p)$, and (b) for each variable $x$ and any two positions $p, q$ of $x$ in $s$, $t|_p = t|_q$. *Proof.* If $s\sigma = t$, then $t$ agrees with $s$ on its function positions, which gives (a), and $t|_p = x\sigma = t|_q$, which gives (b). Conversely, under (a) every variable position of $s$ is a position of $t$, and by (b) $\sigma = \{x \mapsto t|_{p_x}\}$ is well defined. Then $s\sigma$ and $t$ have the same symbol at each function position of $s$ and the same subterm at each variable position of $s$, so $s\sigma = t$ by induction on $s$. $\blacksquare$

## Variants

- **Matching systems.** Solve $s_i\sigma = t_i$ for $i = 1, \ldots, k$ with one $\sigma$. This is matching of $f(s_1, \ldots, s_k)$ against $f(t_1, \ldots, t_k)$.
- **Linear patterns.** If no variable occurs twice in $s$, condition (b) is empty, and matching only compares symbols along the pattern; it needs $O(m)$ time and does not read the subject below the variable positions. The patterns of ML and Haskell are linear.
- **Many-to-one matching.** Match a fixed set of patterns, such as the left sides of a [term rewriting system](/term-rewriting-system/), against many subjects. [Discrimination trees](/discrimination-tree/), [substitution trees](/substitution-tree/) and the automata of [Hoffmann-O'Donnell matching](/hoffmann-odonnell-matching/) preprocess the patterns. See [term indexing](/term-indexing/).
- **All positions.** Find every position $p$ of $t$ where $t|_p$ is an instance of $s$: [tree pattern matching](/tree-pattern-matching/).
- **Matching modulo a theory $E$.** Find $\sigma$ with $s\sigma \approx_E t$. A problem can then have several, or infinitely many, independent matchers. For commutativity (C), associativity (A) and both (AC) the decision problem is NP-complete (Benanav, Kapur and Narendran, 1987); see [AC-matching](/ac-matching/). This is the matching used by [rewriting modulo equations](/rewriting-modulo-equations/). [E-matching](/e-matching/) in SMT solvers matches modulo the ground equations of an [e-graph](/e-graph/).
- **Matching on DAGs.** On a [term DAG](/term-dag/) with [hash-consing](/hash-consing/), the equality test of condition (b) is a pointer comparison, and matching takes $O(m)$ time.

## Examples

**A match.** $s = f(x, g(y))$ and $t = f(a, g(h(b)))$. The walk compares $f$ with $f$, binds $x \mapsto a$, compares $g$ with $g$, and binds $y \mapsto h(b)$. So $\sigma = \{x \mapsto a,\ y \mapsto h(b)\}$.

**A non-linear pattern.** $s = f(x, x)$. Against $t = f(g(z), g(z))$, the matcher is $\{x \mapsto g(z)\}$, where $z$ is a variable of the subject that stays as it is. Against $t = f(a, b)$ there is no matcher, since condition (b) fails.

**Matching is not symmetric.** $f(x, a)$ matches $f(b, a)$ with $\{x \mapsto b\}$. But $f(b, a)$ does not match $f(x, a)$: no substitution of the pattern's variables turns $b$ into $x$. The two terms are unifiable, and matching reduces to unification only after the subject's variables are frozen into constants.

**A variable cannot be a function.** $s = f(x, g(x))$ and $t = f(a, h(a))$: the function position 2 has $g$ in $s$ and $h$ in $t$, so condition (a) fails.

**Matching modulo AC.** Let $+$ be associative and commutative, and match $x + y$ against $a + b + c$, with $x, y$ to be bound to non-empty sums. Each matcher splits the multiset $\{a, b, c\}$ into two non-empty parts, one for $x$ and one for $y$. There are $2^3 - 2 = 6$ matchers, for example $\{x \mapsto a, y \mapsto b + c\}$ and $\{x \mapsto b + c, y \mapsto a\}$. A syntactic matcher has at most one solution; this one has six, and the number grows exponentially with the length of the sum.

## Known algorithms

- **Simultaneous walk.** Keep a stack of pairs (pattern subterm, subject subterm), starting with $(s, t)$. For a pair $(f(s_1, \ldots, s_k), u)$, check that $u = f(u_1, \ldots, u_k)$ and push the pairs $(s_i, u_i)$. For a pair $(x, u)$, bind $x \mapsto u$ if $x$ is unbound, else compare the binding with $u$. This is the standard algorithm; [rewrite step](/rewrite-step/) and [innermost reduction](/innermost-reduction/) use it. With an explicit stack it handles terms of any depth.
- **Unification.** Freeze the variables of $t$ into new constants and run a [unification](/unification-problem/) algorithm such as [Robinson's](/robinson-unification/) or [Martelli-Montanari](/martelli-montanari-unification/). This works, but unification needs an occurs check and composition of bindings that matching does not need.
- **Many patterns.** [Hoffmann-O'Donnell matching](/hoffmann-odonnell-matching/) builds a bottom-up tree automaton for a set of linear patterns, and then finds all matches in a subject in $O(n)$ time after preprocessing; [discrimination trees](/discrimination-tree/) and [substitution trees](/substitution-tree/) index sets of patterns.
- **Modulo AC.** Backtracking search over the ways to split each AC argument multiset, as in [AC-matching](/ac-matching/).

## Bounds

**Upper bound.** The simultaneous walk takes $O(m + n)$ time on terms stored as trees, in the [word RAM](/word-ram/). Each function position of $s$ costs $O(1)$ plus its arity. A variable is bound in $O(1)$ by storing a pointer to the subject subterm. Each repeated occurrence of a variable $x$ at position $q$ compares the binding of $x$ with $t|_q$ in $O(|t|_q|)$ time. The positions of variables in $s$ are pairwise parallel, so the subterms $t|_q$ are disjoint parts of $t$, and all comparisons together cost $O(n)$.

**Lower bound.** Every algorithm must read all $m$ symbols of $s$ in the worst case, since a change at any unread function position of $s$ changes the answer. For non-linear patterns it must also read $\Omega(n)$ symbols of $t$: for $s = f(x, x)$ and $t = f(u, u)$, an algorithm that does not read some node of the second $u$ gives the same answer on $f(u, u')$, where $u'$ differs from $u$ only at that node. So syntactic matching takes $\Theta(m + n)$ time in the worst case.

**Modulo theories.** Matching modulo A, C, and AC is NP-complete (Benanav, Kapur and Narendran, 1987). AC-matching of a pattern in which each variable occurs at most once is in polynomial time. Matching modulo an arbitrary equational theory is undecidable, since the [word problem](/word-problem/) of a theory is the special case of a ground pattern.

## Reductions

- **Matching to unification**, in $O(m + n)$ time: replace each variable of $t$ by a new constant and unify. Every unifier then maps only variables of $s$, and is a matcher.
- **Matching to tree pattern matching**: matching at the root is the case $p = \varepsilon$ of finding all occurrences.
- **Ground word problem to matching modulo $E$**: for ground $s$, a matcher exists iff $s \approx_E t$.

## Applications

- **Rewriting.** A rule $l \to r$ applies at $p$ iff $l$ matches $t|_p$; [term rewriting systems](/term-rewriting-system/), [Knuth-Bendix completion](/knuth-bendix-completion/) and functional language interpreters do this at every step.
- **Functional languages.** ML, Haskell and OCaml compile linear patterns into decision trees or automata that test each symbol of the subject at most once.
- **Theorem proving.** Demodulation (simplification by equations), subsumption of clauses and the forward and backward simplification of a saturation prover all ask whether one term is an instance of another, usually through a [term index](/term-indexing/).
- **SMT solvers.** Quantifier instantiation searches for instances of trigger patterns in an [e-graph](/e-graph/) by [e-matching](/e-matching/).

## References
