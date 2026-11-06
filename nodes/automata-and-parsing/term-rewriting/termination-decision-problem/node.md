---
tag: DRTVYF
kind: problem
slug: termination-decision-problem
name: Deciding termination
aliases:
- termination problem
- uniform termination problem
- strong normalization problem
area: automata-and-parsing/term-rewriting
level: advanced
summary: Decide whether a given term rewriting system terminates; undecidable in general.
prereqs: [termination, undecidability-of-termination]
see_also: [confluence-decision-problem, dependency-pairs, recursive-path-ordering, lexicographic-path-ordering, polynomial-interpretation, matrix-interpretation, size-change-termination, knuth-bendix-ordering]
sources:
  - paper: doi:10.1016/S0747-7171(87)80022-6
    title: Nachum Dershowitz, Termination of rewriting, Journal of Symbolic Computation 3(1 and 2) (1987)
    locator: pp. 69 to 115 (survey of termination methods, undecidability, and decidable cases such as ground systems)
  - paper: doi:10.1007/978-3-642-04027-6_20
    title: Jörg Endrullis, Herman Geuvers and Hans Zantema, Degrees of undecidability in term rewriting, Computer Science Logic (CSL 2009), Lecture Notes in Computer Science 5771
    locator: pp. 255 to 270 (strong normalization of one term is Σ^0_1-complete, uniform termination is Π^0_2-complete)
  - paper: doi:10.1016/0304-3975(92)90022-8
    title: Max Dauchet, Simulation of Turing machines by a regular rewrite rule, Theoretical Computer Science 103(2) (1992)
    locator: pp. 409 to 420
  - paper: doi:10.1016/0020-0190(87)90122-0
    title: Yoshihito Toyama, Counterexamples to termination for the direct sum of term rewriting systems, Information Processing Letters 25(3) (1987)
    locator: pp. 141 to 143
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 5, Termination (Section 5.1 undecidability, Sections 5.2 to 5.4 reduction orders)
---

The **termination problem** asks whether a given finite [term rewriting system](/term-rewriting-system/) is [terminating](/termination/): whether every term has only finite reductions. The problem is [undecidable](/undecidability-of-termination/), and even worse than the halting problem: uniform termination is $\Pi^0_2$-complete, so neither it nor its complement is semi-decidable. In practice it is attacked by searching for termination proofs, with reduction orders, interpretations and the dependency pair method, and by searching for loops to show non-termination; both searches can fail, so every tool may answer "don't know".

## In plain words

You are given a set of rewriting rules and want to know whether simplification with them always stops, no matter which expression you start from and which rule you apply where.

No program answers this correctly for every set of rules. What programs can do is look for a reason. To show that the rules always stop, find a measure of expressions that every rule makes smaller and that cannot shrink forever. To show that they can run forever, find an expression that comes back, inside a bigger one, after some steps. If neither search succeeds, the question stays open.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure.

**Input.** A finite term rewriting system $R$ over a finite signature $\Sigma$.

**Question.** Is $R$ terminating, that is, is there no infinite reduction $t_0 \to_R t_1 \to_R t_2 \to_R \cdots$ from any term $t_0 \in T(\Sigma, V)$?

If $\Sigma$ has a constant, the question can be asked for ground terms only, since rewriting is closed under substitution: an infinite reduction from $t$ gives one from every ground instance of $t$.

## Variants

- **Termination of one term.** Given $R$ and $t$, is $t$ terminating? Since $R$ is finitely branching, this holds iff the reduction tree of $t$ is finite, by König's lemma.
- **Innermost termination.** Only innermost reductions are considered, as in eager evaluation. It is implied by termination, and for some classes, such as non-overlapping systems, it is equivalent to it.
- **Termination under a strategy or modulo a theory.** Termination of outermost or context-sensitive reduction, or of rewriting modulo AC.
- **Restricted classes.** Ground systems, string rewriting systems, systems with one rule, left-linear or orthogonal systems.
- **Weak normalization.** Does every term have some normal form? See [weak normalization](/weak-normalization/).
- **Bounded termination.** Does every reduction have length at most $n$, for a given $n$? This is decidable by search, and the derivation length as a function of term size measures the complexity of $R$.

## Examples

**Terminating, by a path order.** The rules $A(0, y) \to s(y)$, $A(s(x), 0) \to A(x, s(0))$, $A(s(x), s(y)) \to A(x, A(s(x), y))$ for the Ackermann function terminate. The [recursive path ordering](/recursive-path-ordering/) with lexicographic status for $A$ and $A > s$ orients all three rules; a program checked this. No polynomial interpretation proves it, since the derivation lengths grow faster than any primitive recursive function.

**Terminating, but not simply terminating.** $f(f(x)) \to f(g(f(x)))$ terminates, but the term $f(f(x))$ is embedded in $f(g(f(x)))$, so no simplification order, and hence no path order, can orient the rule; see [termination](/termination/). The [dependency pair](/dependency-pairs/) method proves it.

**Not terminating, by a loop.** $f(a, b, x) \to f(x, x, x)$ terminates alone, and $g(x, y) \to x$, $g(x, y) \to y$ terminate alone, but their union does not (Toyama, 1987):
$$f(a, b, g(a, b)) \to f(g(a, b), g(a, b), g(a, b)) \to f(a, g(a, b), g(a, b)) \to f(a, b, g(a, b)).$$
A program confirmed the cycle; the term has 27 reducts. So termination is not modular: it is not preserved by the union of systems over disjoint signatures.

**Single terms versus all terms.** In $\{f(a) \to f(b),\ b \to a\}$ every term without $f$ terminates, but $f(a) \to f(b) \to f(a)$ loops.

## Known algorithms

All are sound and incomplete: an answer is correct when given, but the search can fail.

- **Reduction orders.** Find a [well-founded reduction ordering](/well-founded-reduction-ordering/) that contains $R$: the [lexicographic path ordering](/lexicographic-path-ordering/) and [recursive path ordering](/recursive-path-ordering/), whose precedence search is NP-complete but small in practice; the [Knuth-Bendix ordering](/knuth-bendix-ordering/); [polynomial interpretations](/polynomial-interpretation/) and [matrix interpretations](/matrix-interpretation/), found with SAT or SMT solvers.
- **Dependency pairs.** The [dependency pair](/dependency-pairs/) method reduces termination to the absence of infinite chains of calls, splits the problem along the strongly connected components of a dependency graph, and solves each part with weaker orders. It is the core of modern termination tools.
- **Size-change termination.** [Size-change termination](/size-change-termination/) checks that every infinite call sequence would have an infinitely decreasing value, by a closure computation on size-change graphs.
- **Proving non-termination.** Search for a loop: a term $t$ with $t \to^+ C[t\sigma]$. Then $t$ has an infinite reduction. Toyama's example is a loop with $C$ empty and $\sigma$ the identity.
- **Decision procedures for classes.** For ground systems, termination is decidable (Huet and Lankford, 1978, as surveyed by Dershowitz, 1987).

## Bounds

- **Undecidable.** Both termination of one term and uniform termination are undecidable; see [undecidability of termination](/undecidability-of-termination/).
- **Arithmetical level.** Termination of one term is $\Sigma^0_1$-complete: a terminating term has a finite reduction tree, which a search finds. Uniform termination is $\Pi^0_2$-complete (Endrullis, Geuvers and Zantema, 2009).
- **Restricted classes stay undecidable.** Termination is undecidable for systems with one left-linear, non-overlapping rule (Dauchet, 1992), and for string rewriting systems.
- **Proof search for one method.** Whether $R$ is contained in some lexicographic path ordering is decidable and NP-complete; see [recursive path ordering](/recursive-path-ordering/). Whether a polynomial interpretation with integer coefficients exists is undecidable in general, by Hilbert's tenth problem; see [polynomial interpretation](/polynomial-interpretation/).

## Reductions

- **Halting problem to termination of one term.** A deterministic Turing machine is simulated by a string rewriting system, so a start configuration terminates iff the machine halts.
- **Post correspondence problem to uniform termination.** An instance $P$ maps to a system $R_P$ that loops iff $P$ has a solution; see [undecidability of termination](/undecidability-of-termination/).
- **Confluence through termination.** By Newman's lemma, for terminating systems confluence reduces to joinability of critical pairs, so termination proofs are the first step of most confluence checks; see the [confluence decision problem](/confluence-decision-problem/).

## Applications

- Program verification: termination of functional and logic programs is proved by translating them into rewrite systems and running a termination prover.
- [Knuth-Bendix completion](/knuth-bendix-completion/) needs a reduction order to orient each new rule, and the choice of order decides whether completion succeeds.
- Theorem provers and proof assistants check that recursive definitions terminate before they accept them as functions.
- Equational reasoning: a terminating and confluent system decides its [word problem](/word-problem/) by normal forms.

## References
