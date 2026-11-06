---
tag: P767NM
kind: definition
slug: orthogonal-rewrite-system
name: Orthogonal rewrite system
aliases:
- orthogonal TRS
area: automata-and-parsing/term-rewriting
level: advanced
summary: A left-linear system with no critical pairs.
prereqs: [linearity, critical-pair, term-rewriting-system]
see_also: [orthogonal-confluence-theorem, outermost-reduction, innermost-reduction, combinatory-logic, confluence, critical-pair-lemma, parallel-rewriting, graph-reduction]
sources:
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 4, Orthogonality (definitions, confluence, weak orthogonality, and normalization results)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 6, Confluence (orthogonal systems and their confluence by parallel reduction)
  - paper: doi:10.1145/321738.321750
    title: Barry K. Rosen, Tree-manipulating systems and Church-Rosser theorems, Journal of the ACM 20(1) (1973)
    locator: pp. 160 to 187 (confluence of non-overlapping left-linear rule schemes)
  - paper: "Gérard Huet and Jean-Jacques Lévy, Computations in orthogonal rewriting systems, I and II, in J.-L. Lassez and G. Plotkin (editors), Computational Logic, Essays in Honor of Alan Robinson, MIT Press, 1991"
    locator: pp. 395 to 443 (needed redexes and normalizing strategies)
---

An **orthogonal rewrite system** is a [term rewriting system](/term-rewriting-system/) whose rules are [left-linear](/linearity/) and do not overlap: no left side can be unified with a non-variable subterm of another left side, or with a proper non-variable subterm of itself. In such a system, contracting one redex never destroys another one; it only copies, moves or erases it. This makes orthogonal systems [confluent](/confluence/) without any termination assumption, by the [orthogonal confluence theorem](/orthogonal-confluence-theorem/), and gives them a theory of strategies with normalizing ones. Functional programs defined by non-overlapping pattern matching, [combinatory logic](/combinatory-logic/) and, in a higher-order form, the [lambda calculus](/lambda-calculus/) are orthogonal.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, $\mathrm{Pos}_\Sigma(l)$ the non-variable positions of $l$, $t|_p$ and $t[s]_p$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$.

Let $R$ be a term rewriting system. Two rules $l_1 \to r_1$ and $l_2 \to r_2$, renamed to share no variable, **overlap** at $p \in \mathrm{Pos}_\Sigma(l_1)$ if $l_1|_p$ and $l_2$ are unifiable, except in the case where they are the same rule and $p = \varepsilon$. Each overlap gives a [critical pair](/critical-pair/).

- $R$ is **non-overlapping** (or non-ambiguous) if no two of its rules overlap, that is, $R$ has no critical pairs.
- $R$ is **orthogonal** if it is left-linear and non-overlapping.
- $R$ is **weakly orthogonal** if it is left-linear and every critical pair $\langle s, t \rangle$ is trivial, $s = t$.

For a finite $R$, each property is decidable: check the left sides for repeated variables, and run syntactic [unification](/robinson-unification/) on each pair of a left side and a non-variable subterm of a left side.

**Redexes do not interfere.** Let $R$ be orthogonal and let $t$ contain two redexes at positions $p$ and $q$. If they are disjoint, contracting one leaves the other unchanged. If $q$ is below $p$, then $q$ lies below a variable position of the left side $l$ matched at $p$, since otherwise the two left sides would overlap. Contracting the redex at $q$ changes only the value of that variable, and since $l$ is linear, the redex at $p$ survives with a new substitution. Contracting the redex at $p$ instead leaves zero or more copies of the redex at $q$, one for each occurrence of the variable in the right side; these copies are its **residuals**. Contracting all residuals on one side and the other redex on the other side closes the peak. This is the content of the parallel moves lemma, behind the [orthogonal confluence theorem](/orthogonal-confluence-theorem/).

## Examples and non-examples

**Peano arithmetic.** The rules $\mathit{add}(0, y) \to y$, $\mathit{add}(s(x), y) \to s(\mathit{add}(x, y))$, $\mathit{mul}(0, y) \to 0$, $\mathit{mul}(s(x), y) \to \mathit{add}(\mathit{mul}(x, y), y)$ are left-linear. The left sides of the two $\mathit{add}$ rules have $0$ and $s(x)$ at the same position, which do not unify, and no left side has a defined symbol below the root. So the system is orthogonal.

**Constructor systems.** If $\Sigma$ splits into defined symbols and constructors, and every left side is $f(p_1, \ldots, p_n)$ with $f$ defined and linear patterns $p_i$ made of constructors and variables, then overlaps can only happen at the root. Such a system is orthogonal iff no two left sides unify. This is the shape of a functional program with non-overlapping pattern matching.

**Combinatory logic.** With a binary application symbol, $K\,x\,y \to x$ and $S\,x\,y\,z \to x\,z\,(y\,z)$ are left-linear and do not overlap, so [combinatory logic](/combinatory-logic/) is orthogonal, and hence confluent, although it does not terminate.

**Infinite reductions are allowed.** $\{ \mathit{from}(x) \to \mathit{cons}(x, \mathit{from}(s(x))) \}$ is orthogonal and not terminating. Every term still has at most one normal form.

**Weakly orthogonal, not orthogonal.** Parallel or, $\mathit{por}(\mathit{true}, x) \to \mathit{true}$ and $\mathit{por}(x, \mathit{true}) \to \mathit{true}$, overlap at the root on $\mathit{por}(\mathit{true}, \mathit{true})$, with the trivial critical pair $\langle \mathit{true}, \mathit{true} \rangle$. Weakly orthogonal systems are confluent too.

**Non-example: overlapping rules.** $f(g(x)) \to a$ and $g(b) \to c$ overlap at position $1$ on $f(g(b))$, with the critical pair $\langle f(c), a \rangle$; both are normal forms, so the system is not confluent.

**Non-example: not left-linear.** Huet's system $f(x, x) \to a$, $f(x, g(x)) \to b$, $c \to g(c)$ is non-overlapping but not left-linear, and $f(c, c)$ has the two normal forms $a$ and $b$. Both conditions of orthogonality are needed.

**Non-example: a rule overlapping itself.** $f(f(x)) \to g(x)$ is left-linear, but it overlaps itself at position $1$, on $f(f(f(x)))$. So it is not orthogonal, and its critical pair $\langle f(g(x)), g(f(x)) \rangle$ is not joinable.

## Related definitions

- The [orthogonal confluence theorem](/orthogonal-confluence-theorem/): every orthogonal system, and every weakly orthogonal system, is confluent. So each term has at most one normal form.
- **Normalizing strategies.** In an orthogonal system, parallel-outermost reduction reaches the normal form of every term that has one, and leftmost-outermost reduction does so when the system is also left-normal ([outermost reduction](/outermost-reduction/)). Every term that is not in normal form has a **needed** redex, one whose residuals every reduction to normal form must contract, and contracting needed redexes is normalizing (Huet and Lévy).
- **Innermost reduction.** In a non-overlapping system, distinct innermost redexes are disjoint, so all maximal [innermost](/innermost-reduction/) reductions of a term have the same length.
- **Non-erasing systems.** If an orthogonal system is non-erasing, every variable of each left side occurring in the right side, then a term that has a normal form has no infinite reduction: weak and strong normalization coincide term by term.
- **Implementation.** [Graph reduction](/graph-reduction/) implements orthogonal systems with sharing, and [parallel rewriting](/parallel-rewriting/) contracts sets of non-interfering redexes at once.

## References
