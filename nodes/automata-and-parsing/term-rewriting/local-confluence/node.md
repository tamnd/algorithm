---
tag: PGSZTS
kind: definition
slug: local-confluence
name: Local confluence
aliases:
- weak confluence
area: automata-and-parsing/term-rewriting
level: core
summary: Any one-step divergence from a term can be joined by reductions.
prereqs: [abstract-reduction-system, joinability]
see_also: [confluence, newman-lemma, critical-pair, critical-pair-lemma, knuth-bendix-completion, termination]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.7, Proving confluence (local confluence and Newman's lemma); Chapter 6, Section 6.2, Critical pairs
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 1, Abstract reduction systems (weak Church-Rosser property and the counterexamples to its sufficiency)
  - paper: doi:10.2307/1968867
    title: M. H. A. Newman, On theories with a combinatorial definition of "equivalence", Annals of Mathematics 43(2) (1942)
    locator: pp. 223 to 243
  - paper: doi:10.1145/322217.322230
    title: Gérard Huet, Confluent reductions, abstract properties and applications to term rewriting systems, Journal of the ACM 27(4) (1980)
    locator: pp. 797 to 821 (the short proof of Newman's lemma by well-founded induction)
---

A relation is **locally confluent** when every pair of one-step reducts of an element is [joinable](/joinability/): if $x$ rewrites in one step to $y_1$ and in one step to $y_2$, then $y_1$ and $y_2$ have a common reduct. It is the one-step, local version of [confluence](/confluence/). Local confluence alone does not give confluence, but for a terminating relation it does, by [Newman's lemma](/newman-lemma/), and for a term rewriting system it can be checked on finitely many [critical pairs](/critical-pair/). These two facts together are the basis of the Knuth-Bendix confluence test and of [completion](/knuth-bendix-completion/).

## Definition

Let $(A, \to)$ be an [abstract reduction system](/abstract-reduction-system/), with $\to^*$ the reflexive transitive closure of $\to$. The relation $\to$ is **locally confluent** (also **weakly confluent**, or **weak Church-Rosser**, WCR) if

$$\forall x, y_1, y_2 \in A:\quad y_1 \leftarrow x \to y_2 \ \implies\ \exists z:\ y_1 \to^* z \leftarrow^* y_2.$$

A triple $y_1 \leftarrow x \to y_2$ is a **local peak**; local confluence says that each local peak has a valley. The valley may be long on either side. A term rewriting system $R$ is locally confluent when $\to_R$ is.

**For term rewriting systems.** In a peak $t[r_1\sigma_1]_p \leftarrow t \to t[r_2\sigma_2]_q$ of a term rewriting system, there are three cases for the positions $p$ and $q$, sequences of positive integers.

- **Disjoint positions** ($p$ and $q$ are not prefixes of each other). The two steps commute: doing the other step on each side gives the same term in one step each.
- **Variable overlap** ($q = p.q'$ and $q'$ lies at or below a variable position of the first left-hand side $l_1$). The inner step happens inside the part that $\sigma_1$ substitutes for a variable $x$. On one side, rewrite each copy of that subterm, once for each occurrence of $x$ in $r_1$; on the other side, rewrite the copies of $x$ in $l_1$ that are left, then apply the first rule. The peak is joinable, for any rules.
- **Critical overlap** ($q = p.q'$ with $q'$ a non-variable position of $l_1$). Then the peak is an instance of a [critical pair](/critical-pair/).

The [critical pair lemma](/critical-pair-lemma/) turns this case analysis into a theorem: $R$ is locally confluent if and only if all critical pairs of $R$ are joinable. A finite $R$ has finitely many critical pairs. If $R$ is also terminating, joinability of each pair is decidable, so local confluence of a finite terminating system is decidable.

**Local confluence and confluence.**

- Confluence implies local confluence: a one-step peak is a special peak.
- Local confluence does not imply confluence (the examples below).
- Local confluence and termination together imply confluence: this is [Newman's lemma](/newman-lemma/).
- Local confluence and weak normalization do not imply confluence, as the second example below shows.

## Examples and non-examples

**Local peaks of a copying rule.** Let $R = \{f(x) \to g(x, x),\ a \to b\}$. The only peak from $f(a)$ with steps at overlapping positions is $f(b) \leftarrow f(a) \to g(a, a)$, a variable overlap. It joins at $g(b, b)$, in one step on the left and two steps on the right. $R$ has no critical pairs, so it is locally confluent, and it terminates, so it is confluent.

**A local peak that does not join.** With $R = \{f(a) \to b,\ a \to c\}$, the peak $b \leftarrow f(a) \to f(c)$ ends in two distinct normal forms. This is the critical pair $\langle b, f(c) \rangle$ of the two rules, and $R$ is not locally confluent.

**Locally confluent, not confluent, with a cycle.** Let $A = \{a, b, c, d\}$ with $b \to a$, $b \to c$, $c \to b$, $c \to d$. The two local peaks are $a \leftarrow b \to c$, joined at $a$ by $c \to b \to a$, and $b \leftarrow c \to d$, joined at $d$ by $b \to c \to d$. But $a \leftarrow b \to c \to d$, and $a$ and $d$ are different normal forms. This four-element system is the standard counterexample, often credited to Hindley.

**Locally confluent and weakly normalizing, not confluent.** The same system is weakly normalizing: $a$ and $d$ are normal forms, $b \to a$ and $c \to d$. So weak normalization is not enough for Newman's lemma; it needs the absence of every infinite reduction.

**Locally confluent, not confluent, with no cycle.** Let $A = \{a_0, a_1, a_2, \ldots\} \cup \{b, c\}$ with $a_i \to a_{i+1}$ for each $i$, $a_i \to b$ for even $i$ and $a_i \to c$ for odd $i$. For even $i$, the peak $b \leftarrow a_i \to a_{i+1}$ joins at $b$ through $a_{i+1} \to a_{i+2} \to b$; for odd $i$, the peak $c \leftarrow a_i \to a_{i+1}$ joins at $c$ in the same way. So the relation is locally confluent and has no cycle. But $b \leftarrow a_0 \to a_1 \to c$, with $b \ne c$ normal forms. Here the infinite reduction $a_0 \to a_1 \to \cdots$ breaks confluence, and it is again the missing termination that Newman's lemma needs.

**The empty system** is locally confluent, since it has no peaks.

## Related definitions

- [Confluence](/confluence/) closes all peaks $y_1 \leftarrow^* x \to^* y_2$; local confluence closes only the one-step peaks.
- [Newman's lemma](/newman-lemma/): termination and local confluence imply confluence.
- [Critical pairs](/critical-pair/) and the [critical pair lemma](/critical-pair-lemma/) reduce local confluence of a term rewriting system to finitely many joinability checks.
- [Knuth-Bendix completion](/knuth-bendix-completion/) repairs a failure of local confluence by turning a non-joinable critical pair into a new rule.
- [Termination](/termination/) is the extra hypothesis that turns local confluence into confluence.

## References
