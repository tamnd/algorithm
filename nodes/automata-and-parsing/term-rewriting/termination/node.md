---
tag: ES2AGT
kind: definition
slug: termination
name: Termination
aliases:
- strong normalization
- SN
area: automata-and-parsing/term-rewriting
level: core
summary: Every reduction sequence from every term is finite.
prereqs: [term-rewriting-system, well-founded-relation]
see_also: [weak-normalization, well-founded-reduction-ordering, undecidability-of-termination, termination-decision-problem, newman-lemma, polynomial-interpretation, dependency-pairs, normal-form]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 2.2 and 2.3 (well-founded induction and termination of abstract reduction systems); Chapter 5, Termination (5.2, reduction orders)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 6, Termination
  - paper: doi:10.1016/0020-0190(87)90122-0
    title: Yoshihito Toyama, Counterexamples to termination for the direct sum of term rewriting systems, Information Processing Letters 25(3) (1987)
    locator: pp. 141 to 143
---

A [term rewriting system](/term-rewriting-system/) is **terminating**, or **strongly normalizing**, if no term has an infinite sequence of [rewrite steps](/rewrite-step/). Then every way of computing stops, and every term has a [normal form](/normal-form/). Termination is the property that makes [Newman's lemma](/newman-lemma/) and the [critical pair lemma](/critical-pair-lemma/) decide confluence, and that [completion](/knuth-bendix-completion/) must keep at each step. It is undecidable in general, and it is proved with a [reduction ordering](/well-founded-reduction-ordering/) or a related method.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure; $\to_R^+$ is the transitive closure.

A term $t$ is **terminating** (strongly normalizing, $\mathrm{SN}(t)$) if there is no infinite sequence $t = t_0 \to_R t_1 \to_R t_2 \to_R \cdots$. The system $R$ is **terminating** if every term in $T(\Sigma, V)$ is terminating. Equivalent forms:

1. $\to_R$ has no infinite chain, that is, the inverse relation ${}_R\!\leftarrow$ is [well-founded](/well-founded-relation/).
2. $\to_R^+$ is a well-founded strict order (read from left to right as "greater").
3. **Well-founded induction** holds: if a property $P$ of terms satisfies "$P(u)$ for all $u$ with $t \to_R u$ implies $P(t)$", then $P$ holds for all terms. This is **noetherian induction**, the main proof tool for terminating systems.

For a finite system the **derivation height** $\mathrm{dh}(t) = \max\{ n \mid t \to_R^n u \text{ for some } u \}$ is finite for each terminating term. *Proof.* Each term has at most $|t| \cdot |R|$ one-step reducts, so the tree of all reductions from $t$ is finitely branching. It has no infinite path, so by König's lemma it is finite, and its height is $\mathrm{dh}(t)$. The **derivational complexity** $\mathrm{dc}_R(n) = \max\{ \mathrm{dh}(t) \mid |t| \le n \}$ measures how long computations can be.

**Termination and orders.** $R$ is terminating iff there is a [reduction ordering](/well-founded-reduction-ordering/) $>$, a well-founded strict order closed under contexts and substitutions, with $l > r$ for each rule $l \to r \in R$. *Proof.* If such an order exists and $s \to_R t$ with $s|_p = l\sigma$, then $l\sigma > r\sigma$ by closure under substitutions and $s = s[l\sigma]_p > s[r\sigma]_p = t$ by closure under contexts, so an infinite chain of steps would be an infinite descending chain in $>$. Conversely, if $R$ terminates, then $\to_R^+$ is transitive, irreflexive (a cycle $t \to_R^+ t$ gives an infinite chain), well-founded, and closed under contexts and substitutions because $\to_R$ is; it contains each rule. $\blacksquare$ This turns termination proofs into the search for an order: [polynomial interpretations](/polynomial-interpretation/), the [recursive path ordering](/recursive-path-ordering/), the [lexicographic path ordering](/lexicographic-path-ordering/), the [Knuth-Bendix ordering](/knuth-bendix-ordering/), [matrix interpretations](/matrix-interpretation/), and the [dependency pair](/dependency-pairs/) framework, which needs weaker orders.

**Related properties.** $R$ is [weakly normalizing](/weak-normalization/) if each term has some reduction to a normal form; termination implies it, and the converse fails. $R$ is **simply terminating** if a simplification ordering (a reduction ordering that contains the [subterm](/subterm/) relation) orients its rules. $R$ is **non-looping** if no term reduces to a term that contains an instance of itself; a loop $t \to_R^+ C[t\sigma]$ is the usual witness of non-termination.

**Decidability.** Termination of finite term rewriting systems is undecidable; see [undecidability of termination](/undecidability-of-termination/) and [deciding termination](/termination-decision-problem/). It is decidable for some classes, for example for finite ground systems.

## Examples and non-examples

**Sorting letters.** The rule $b(a(x)) \to a(b(x))$, the string rule $ba \to ab$, terminates: each step lowers the number of pairs ($b$ before $a$) by exactly one. From $b^n a^n$ every reduction has exactly $n^2$ steps, so $\mathrm{dh}(b^n a^n) = n^2$ and the derivational complexity is quadratic.

**Arithmetic.** The rules $0 + y \to y$, $s(x) + y \to s(x + y)$, $x \times 0 \to 0$, $x \times s(y) \to (x \times y) + x$ terminate. The [lexicographic path ordering](/lexicographic-path-ordering/) with $\times > + > s$ orients them: for example $x \times s(y) > (x \times y) + x$ because $\times > +$, $x \times s(y) > x \times y$ by the lexicographic comparison $s(y) > y$, and $x$ is a subterm.

**Terminating, but not simply terminating.** $f(f(x)) \to f(g(f(x)))$ terminates: each step lowers by one the number of nodes labelled $f$ whose parent is labelled $f$. Still, its left side is embedded in its right side (delete $g$), so no simplification ordering orients it. From $f^5(a)$ exactly 16 terms are reachable, and from $f^7(a)$ exactly 64.

**Weakly normalizing, not terminating.** $R = \{a \to a,\ a \to b\}$: the term $a$ has the normal form $b$, but also the infinite reduction $a \to a \to \cdots$.

**Non-examples.**

- $f(x) \to f(f(x))$ does not terminate: $f(a) \to f(f(a)) \to \cdots$.
- Combinatory logic, $S\,x\,y\,z \to x\,z\,(y\,z)$ and $K\,x\,y \to x$, does not terminate: $S\,I\,I\,(S\,I\,I)$ with $I = S\,K\,K$ reduces to itself.
- **Termination is not modular** (Toyama, 1987). $R_1 = \{f(0, 1, x) \to f(x, x, x)\}$ and $R_2 = \{g(x, y) \to x,\ g(x, y) \to y\}$ terminate, and they share no symbol, but their union has the cycle $f(0, 1, g(0, 1)) \to f(g(0, 1), g(0, 1), g(0, 1)) \to f(0, g(0, 1), g(0, 1)) \to f(0, 1, g(0, 1))$. So proofs of termination for parts of a system do not combine by union in general.
- The empty system terminates trivially, and $R = \{a \to a\}$ does not, though it is [confluent](/confluence/).

## Related definitions

- [Weak normalization](/weak-normalization/): some reduction stops.
- [Normal form](/normal-form/): the terms where reductions stop.
- [Reduction ordering](/well-founded-reduction-ordering/): the orders that prove termination.
- [Newman's lemma](/newman-lemma/): termination and local confluence give confluence.
- [Undecidability of termination](/undecidability-of-termination/): no algorithm decides the property.
- [Termination proof](/termination-proof/): the same idea for loops and recursive programs, with a variant function.
- [Size-change termination](/size-change-termination/): a termination method for programs with recursive calls.

## References
