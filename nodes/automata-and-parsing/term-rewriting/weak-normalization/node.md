---
tag: F7C8F6
kind: definition
slug: weak-normalization
name: Weak normalization
aliases:
- weak normalisation
- WN
area: automata-and-parsing/term-rewriting
level: core
summary: Every term has at least one reduction sequence ending in a normal form.
prereqs: [normal-form, termination]
see_also: [termination, reduction-strategy, outermost-reduction, innermost-reduction, confluence, newman-lemma, combinatory-logic, lambda-calculus]
sources:
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 1, Abstract reduction systems (normalization properties); Chapter 4, Orthogonality (non-erasing systems); Chapter 9, Strategies
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 2, Abstract reduction systems (normal forms, normalizing and terminating relations)
---

A rewrite system is **weakly normalizing** if every term has at least one reduction to a [normal form](/normal-form/). Some way of computing stops, though others may run forever. It is weaker than [termination](/termination/), which asks that every way stops, and it is the property a [normalizing strategy](/reduction-strategy/) needs in order to find normal forms.

## Definition

We use the notation of the term rewriting pages: terms $T(\Sigma, V)$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure. The definitions apply to any [abstract reduction system](/abstract-reduction-system/).

A term $t$ is **weakly normalizing**, $\mathrm{WN}(t)$, if there is a normal form $u$ with $t \to_R^* u$. A system $R$ is **weakly normalizing** if every term is.

**Termination implies weak normalization.** If every reduction from $t$ is finite, follow any reduction until no step applies; it ends in a normal form. The converse fails, already for one term: in $\{a \to a,\ a \to b\}$, $a \to b$ reaches a normal form, and $a \to a \to \cdots$ does not stop.

**Finding the normal form.** If $R$ is finite and $t$ is weakly normalizing, a normal form of $t$ can be computed by breadth-first search over the reduction graph of $t$: each term has finitely many one-step reducts, so each level of the search is finite, and some normal form lies at a finite depth. This is a semi-decision procedure for $\mathrm{WN}(t)$. A strategy that follows one reduction at a time may fail where the search succeeds, because it may pick the infinite reduction.

**Unique normal forms.** If $R$ is weakly normalizing and [confluent](/confluence/), every term $t$ has exactly one normal form $\mathrm{nf}(t)$, and $s \leftrightarrow_R^* t$ iff $\mathrm{nf}(s) = \mathrm{nf}(t)$. *Proof.* Two normal forms $u_1, u_2$ of $t$ have a common reduct by confluence, and a normal form reduces only to itself, so $u_1 = u_2$. If $s \leftrightarrow_R^* t$, confluence gives a common reduct of $s$ and $t$ (the Church-Rosser property), and its normal form is a normal form of both. $\blacksquare$ Unlike [Newman's lemma](/newman-lemma/), this needs confluence, not only local confluence.

**Local confluence is not enough.** In $\{b \to a,\ b \to c,\ c \to b,\ c \to d\}$ every term is weakly normalizing and every local peak is joinable ($a \leftarrow b \to c$ joins at $a$ via $c \to b \to a$, and $b \leftarrow c \to d$ joins at $d$ via $b \to c \to d$), but $b$ has the two normal forms $a$ and $d$. So Newman's lemma needs termination, and weak normalization does not replace it.

**Orthogonal systems.** For an [orthogonal](/orthogonal-rewrite-system/) system that is **non-erasing** (each variable of a left side also occurs in the right side), a weakly normalizing term is terminating. Erasing rules break this: they can discard a subterm with an infinite reduction.

**Undecidability.** Whether a given term is weakly normalizing is undecidable: a deterministic string rewriting system that simulates a Turing machine has at most one step from each word, so the encoding of an input configuration reaches a normal form iff the machine halts. See [the halting problem](/halting-problem/) and [undecidability of termination](/undecidability-of-termination/).

## Examples and non-examples

**Erasing an infinite computation.** In [combinatory logic](/combinatory-logic/) with $K\,x\,y \to x$ and $S\,x\,y\,z \to x\,z\,(y\,z)$, let $\Omega = S\,I\,I\,(S\,I\,I)$ with $I = S\,K\,K$; $\Omega$ reduces to itself and has no normal form. The term $K\,a\,\Omega$ is weakly normalizing: one step at the root gives the normal form $a$. It is not terminating: steps inside $\Omega$ can go on forever. [Innermost reduction](/innermost-reduction/) loops on it; [outermost reduction](/outermost-reduction/) finds $a$.

**The untyped and the typed lambda calculus.** In the untyped [lambda calculus](/lambda-calculus/), $(\lambda x.\, x\,x)(\lambda x.\, x\,x)$ has no normal form, so beta reduction is not weakly normalizing. The simply typed lambda calculus is terminating, so it is also weakly normalizing.

**Arithmetic.** The rules $0 + y \to y$, $s(x) + y \to s(x + y)$ terminate, so they are weakly normalizing; the normal form of a ground term is a numeral.

**Non-examples.**

- $\{f(x) \to f(f(x))\}$: no term that contains $f$ has a normal form, since each such term is a redex and every reduct contains $f$ again.
- $\{a \to b,\ b \to a\}$: neither $a$ nor $b$ has a normal form.
- [Combinatory logic](/combinatory-logic/) as a whole: $\Omega$ has no normal form, so the system is not weakly normalizing, though many of its terms are.

## Related definitions

- [Termination](/termination/): every reduction stops; the strong form of the property.
- [Normal form](/normal-form/): the end point of a normalizing reduction.
- [Reduction strategy](/reduction-strategy/): a strategy is normalizing if it reaches the normal form of every weakly normalizing term.
- [Outermost reduction](/outermost-reduction/) and [innermost reduction](/innermost-reduction/): the first is normalizing for important classes of systems, the second is not.
- [Confluence](/confluence/): with weak normalization it gives unique normal forms.
- [Newman's lemma](/newman-lemma/): needs termination; the four-element example above shows why.

## References
