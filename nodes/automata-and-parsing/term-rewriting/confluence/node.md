---
tag: 4XYTRE
kind: definition
slug: confluence
name: Confluence
aliases:
- Church-Rosser property
area: automata-and-parsing/term-rewriting
level: core
summary: Any two reducts of a term can be rewritten to a common term.
prereqs: [abstract-reduction-system, joinability]
see_also: [local-confluence, newman-lemma, critical-pair-lemma, church-rosser-theorem, orthogonal-confluence-theorem, hindley-rosen-lemma, confluence-decision-problem, normal-form]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.1 (confluence and the Church-Rosser property) and Section 2.7, Proving confluence; Chapter 6, Confluence
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 1, Abstract reduction systems; Chapter 4, Orthogonality
  - paper: doi:10.1145/322217.322230
    title: Gérard Huet, Confluent reductions, abstract properties and applications to term rewriting systems, Journal of the ACM 27(4) (1980)
    locator: pp. 797 to 821 (the abstract confluence results and the counterexample of a non-left-linear system without critical pairs)
  - paper: "Alonzo Church and J. Barkley Rosser, Some properties of conversion, Transactions of the American Mathematical Society 39(3) (1936)"
    locator: pp. 472 to 482
---

A reduction relation is **confluent** when any two results that one element can reach can be brought back together: whenever $x$ reduces to $y_1$ and to $y_2$, some $z$ is reachable from both. Confluence means that the order in which steps are taken does not change what can still be reached, so each element has at most one [normal form](/normal-form/), and a program defined by rewrite rules has one result no matter which reducible part an evaluator picks first. It is equivalent to the Church-Rosser property, named after the 1936 proof that [beta-reduction](/beta-reduction/) of the lambda calculus has it.

## Definition

Let $(A, \to)$ be an [abstract reduction system](/abstract-reduction-system/), with $\to^*$ its reflexive transitive closure and $\leftrightarrow^*$ the least equivalence relation containing $\to$. Write $y_1 \downarrow y_2$ when $y_1$ and $y_2$ are [joinable](/joinability/), that is, $y_1 \to^* z \leftarrow^* y_2$ for some $z$.

- An element $x$ is **confluent** if for all $y_1, y_2 \in A$: $y_1 \leftarrow^* x \to^* y_2$ implies $y_1 \downarrow y_2$.
- The relation $\to$ is **confluent** if each $x \in A$ is confluent.
- $\to$ is **Church-Rosser** if $x \leftrightarrow^* y$ implies $x \downarrow y$ for all $x, y$.
- $\to$ has the **diamond property** if $y_1 \leftarrow x \to y_2$ implies $y_1 \to z \leftarrow y_2$ for some $z$, with exactly one step on each side.

As a picture, confluence closes every "peak" $y_1 \leftarrow^* x \to^* y_2$ by a "valley" $y_1 \to^* z \leftarrow^* y_2$. A term rewriting system $R$ is confluent when the relation $\to_R$ on $T(\Sigma, V)$ is.

**Equivalent forms.** For each ARS the following are equivalent. The proofs are on the page of [abstract reduction systems](/abstract-reduction-system/) and use induction on the length of a reduction or a conversion.

1. $\to$ is confluent.
2. $\to$ is Church-Rosser.
3. $\to$ is semi-confluent: $y_1 \leftarrow x \to^* y_2$ implies $y_1 \downarrow y_2$.
4. $\to^*$ has the diamond property.
5. The joinability relation $\downarrow$ is transitive.

**Two consequences.** If $\to$ is confluent, then each element has at most one normal form, and two elements are equivalent under $\leftrightarrow^*$ exactly when they are joinable. If in addition $\to$ terminates, then $x \leftrightarrow^* y$ iff the normal forms $x{\downarrow}$ and $y{\downarrow}$ are equal.

**A sufficient condition through a second relation.** If ${\to} \subseteq {\Rightarrow} \subseteq {\to^*}$ and $\Rightarrow$ has the diamond property, then $\to$ is confluent. Indeed $\Rightarrow^* = \to^*$, and the diamond property of $\Rightarrow$ passes to $\Rightarrow^*$ by tiling a grid of diamonds. This is how the [Church-Rosser theorem](/church-rosser-theorem/) and the [orthogonal confluence theorem](/orthogonal-confluence-theorem/) are proved, with $\Rightarrow$ the parallel reduction.

**Weaker and stronger notions.**

- [Local confluence](/local-confluence/) (weak Church-Rosser) closes only one-step peaks $y_1 \leftarrow x \to y_2$. It is strictly weaker, and [Newman's lemma](/newman-lemma/) says it is enough for terminating systems.
- **Strong confluence** (Huet): $y_1 \leftarrow x \to y_2$ implies $y_1 \to^= z \leftarrow^* y_2$, with at most one step on the left. It implies confluence without termination.
- **Ground confluence:** confluence on the ground terms $T(\Sigma)$ only. It is weaker than confluence, and it is what [inductive theorem proving](/inductive-theorem-proving/) needs.

## Examples and non-examples

**Deterministic systems.** If each element has at most one one-step reduct, the relation is confluent: two reductions from $x$ are prefixes of one path, so the shorter ends at an element that reduces to the end of the longer.

**Unary addition.** The system $\mathit{add}(0, y) \to y$, $\mathit{add}(s(x), y) \to s(\mathit{add}(x, y))$ is confluent. Its two left-hand sides do not overlap and have no repeated variable, so it is an [orthogonal system](/orthogonal-rewrite-system/), and orthogonal systems are confluent by the [orthogonal confluence theorem](/orthogonal-confluence-theorem/).

**The lambda calculus.** [Beta-reduction](/beta-reduction/) is confluent by the [Church-Rosser theorem](/church-rosser-theorem/), although it does not terminate: $(\lambda x.\, x\,x)(\lambda x.\, x\,x)$ reduces only to itself.

**Combinatory logic.** The rules $S\,x\,y\,z \to x\,z\,(y\,z)$ and $K\,x\,y \to x$ of [combinatory logic](/combinatory-logic/) form an orthogonal system, so it is confluent.

**Non-example: two rules for one term.** $\{f(x, y) \to x,\ f(x, y) \to y\}$ terminates, and $f(a, b)$ has the two normal forms $a$ and $b$, so it is not confluent.

**Non-example: locally confluent but not confluent.** On $\{a, b, c, d\}$ with $b \to a$, $b \to c$, $c \to b$, $c \to d$, each one-step peak is joinable, but $a \leftarrow^* b \to^* d$ with $a \ne d$ both normal forms. The cycle between $b$ and $c$ is what breaks the step from local to global.

**Non-example: no critical pairs, still not confluent.** Huet gave the system

$$f(x, x) \to a, \qquad f(x, g(x)) \to b, \qquad c \to g(c).$$

The left-hand sides $f(x, x)$ and $f(x', g(x'))$ do not unify, since $x = g(x)$ fails the occurs check, so the system has no [critical pairs](/critical-pair/). Yet $f(c, c) \to a$, and $f(c, c) \to f(c, g(c)) \to b$, and $a$ and $b$ are distinct normal forms. The first rule is not left-linear, and the system does not terminate. So neither "no critical pairs" alone nor "no critical pairs and non-terminating" gives confluence; left-linearity is needed, as in the orthogonal theorem, or termination, as in the [critical pair lemma](/critical-pair-lemma/) with Newman's lemma.

**Non-example: confluence is not ground confluence.** With $\Sigma = \{a, f\}$ and the rules $f(x) \to a$ and $f(x) \to x$, the term $f(y)$ has the two normal forms $a$ and $y$, so the system is not confluent. But each ground term is $f^k(a)$, which reduces to $a$ by either rule, so the system is ground confluent.

**The empty system** is confluent, since each element reduces only to itself.

## Related definitions

- [Joinability](/joinability/) is the relation $\downarrow$ used above, and [local confluence](/local-confluence/) is the one-step version.
- [Newman's lemma](/newman-lemma/): terminating and locally confluent implies confluent. The [critical pair lemma](/critical-pair-lemma/) makes local confluence checkable, which gives the Knuth-Bendix test for terminating systems.
- The [Church-Rosser theorem](/church-rosser-theorem/) (lambda calculus), the [orthogonal confluence theorem](/orthogonal-confluence-theorem/) (left-linear systems without critical pairs) and the [Hindley-Rosen lemma](/hindley-rosen-lemma/) (unions of commuting relations) prove confluence without termination.
- [Deciding confluence](/confluence-decision-problem/) is undecidable for finite term rewriting systems in general, decidable for terminating ones and for ground ones.
- [Knuth-Bendix completion](/knuth-bendix-completion/) adds rules to a terminating system until it is confluent.

## References
