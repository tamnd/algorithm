---
tag: 4H44VJ
kind: definition
slug: abstract-reduction-system
name: Abstract reduction system
aliases:
- ARS
area: automata-and-parsing/term-rewriting
level: core
summary: A set with a binary reduction relation, the abstract setting for confluence and termination.
prereqs: [well-founded-relation, transitive-closure, equivalence-relation]
see_also: [normal-form, confluence, local-confluence, joinability, termination, newman-lemma, hindley-rosen-lemma, term-rewriting-system]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 2, Abstract Reduction Systems (Section 2.1, Equivalence and reduction; Section 2.2, Well-founded induction; Section 2.7, Proving confluence)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 1, Abstract reduction systems
  - paper: doi:10.1145/322217.322230
    title: Gérard Huet, Confluent reductions, abstract properties and applications to term rewriting systems, Journal of the ACM 27(4) (1980)
    locator: pp. 797 to 821, Section 2 (the abstract properties of a relation, before terms are introduced)
  - paper: doi:10.2307/1968867
    title: M. H. A. Newman, On theories with a combinatorial definition of "equivalence", Annals of Mathematics 43(2) (1942)
    locator: pp. 223 to 243
---

An **abstract reduction system** (ARS) is a set $A$ together with a binary relation $\to$ on $A$, read as "reduces in one step to". It strips rewriting down to its graph: the elements can be terms, strings, lambda terms, states of a program or numbers, and the properties that matter for evaluation, such as [termination](/termination/), [confluence](/confluence/) and uniqueness of [normal forms](/normal-form/), are stated and proved once at this level. Results such as [Newman's lemma](/newman-lemma/) and the [Hindley-Rosen lemma](/hindley-rosen-lemma/) are theorems about abstract reduction systems that then apply to every concrete rewriting system.

## Definition

An **abstract reduction system** is a pair $(A, \to)$ where $A$ is a set and $\to \subseteq A \times A$. We write $x \to y$ for $(x, y) \in {\to}$ and call $y$ a **one-step reduct** of $x$. From $\to$ we build these relations:

| relation | meaning |
|---|---|
| $\to^0$ | identity: $x \to^0 y$ iff $x = y$ |
| $\to^{n+1}$ | $x \to^{n+1} z$ iff $x \to^n y \to z$ for some $y$ |
| $\to^+ = \bigcup_{n \ge 1} \to^n$ | [transitive closure](/transitive-closure/) |
| $\to^* = \bigcup_{n \ge 0} \to^n$ | reflexive transitive closure: $x$ **reduces to** $y$ |
| $\to^= = {\to} \cup {\to^0}$ | reflexive closure: zero or one step |
| $\leftarrow$ | inverse: $y \leftarrow x$ iff $x \to y$ |
| $\leftrightarrow = {\to} \cup {\leftarrow}$ | symmetric closure |
| $\leftrightarrow^*$ | reflexive, symmetric, transitive closure: **conversion** |
| $x \downarrow y$ | $x \to^* z \leftarrow^* y$ for some $z$: $x$ and $y$ are [joinable](/joinability/) |

The relation $\leftrightarrow^*$ is the least [equivalence relation](/equivalence-relation/) that contains $\to$. A finite sequence $x_0 \to x_1 \to \cdots \to x_n$ is a **reduction** of length $n$, and an infinite sequence $x_0 \to x_1 \to \cdots$ is an **infinite reduction**.

The standard properties of an element $x$ and of the whole relation are these. A relation has a property when each element has it.

- $x$ is a **[normal form](/normal-form/)** if it has no one-step reduct. $\mathrm{NF}$ is the set of normal forms.
- **Weakly normalizing (WN):** $x \to^* y$ for some $y \in \mathrm{NF}$.
- **Terminating, or strongly normalizing (SN):** there is no infinite reduction starting at $x$. The relation is terminating iff its inverse $\leftarrow$ is a [well-founded relation](/well-founded-relation/).
- **[Confluent](/confluence/) (CR):** for all $y_1, y_2$, if $y_1 \leftarrow^* x \to^* y_2$ then $y_1 \downarrow y_2$.
- **Church-Rosser:** for all $x, y$, if $x \leftrightarrow^* y$ then $x \downarrow y$.
- **[Locally confluent](/local-confluence/) (WCR):** for all $y_1, y_2$, if $y_1 \leftarrow x \to y_2$ then $y_1 \downarrow y_2$.
- **Semi-confluent:** for all $y_1, y_2$, if $y_1 \leftarrow x \to^* y_2$ then $y_1 \downarrow y_2$.
- **Unique normal forms (UN):** if $y_1 \leftarrow^* x \to^* y_2$ and $y_1, y_2 \in \mathrm{NF}$, then $y_1 = y_2$.
- **Convergent (complete, canonical):** confluent and terminating.

These properties are related as follows. Each implication holds for every ARS.

1. **SN implies WN.** Follow any reduction from $x$. It is finite, and it can be extended while its last element is not a normal form, so it ends in a normal form.
2. **Church-Rosser iff confluent.** Church-Rosser implies confluence because $y_1 \leftarrow^* x \to^* y_2$ gives $y_1 \leftrightarrow^* y_2$. For the converse, assume confluence and prove by induction on the number $n$ of $\leftrightarrow$ steps in $x \leftrightarrow^n y$ that $x \downarrow y$. For $n = 0$, $x = y$. For $n + 1$, write $x \leftrightarrow^n y' \leftrightarrow y$; by induction $x \to^* z \leftarrow^* y'$. If $y \to y'$, then $y \to^* z$ and $x \downarrow y$ through $z$. If $y' \to y$, then $z \leftarrow^* y' \to y$, and confluence joins $z$ and $y$ at some $w$, so $x \to^* z \to^* w \leftarrow^* y$.
3. **Confluent iff semi-confluent.** One direction is a special case. The other uses the same induction on the length of $x \to^* y_1$.
4. **CR implies UN,** because two joinable normal forms are equal.
5. **WN and UN imply CR.** If $y_1 \leftarrow^* x \to^* y_2$, take normal forms $n_1, n_2$ of $y_1, y_2$. Both are normal forms of $x$, so $n_1 = n_2$ joins $y_1$ and $y_2$.
6. **SN and WCR imply CR.** This is [Newman's lemma](/newman-lemma/). Neither hypothesis can be dropped.
7. **CR implies WCR,** but not the converse, and **SN implies neither.**

In a convergent ARS each $x$ has exactly one normal form $x{\downarrow}$, and $x \leftrightarrow^* y$ iff $x{\downarrow} = y{\downarrow}$. This turns the word problem of the equivalence $\leftrightarrow^*$ into the computation and comparison of two normal forms.

## Examples and non-examples

**Division by primes.** Let $A = \{1, 2, 3, \ldots\}$ and $m \to m/p$ for each prime $p$ that divides $m$. Each step lowers $m$, so the relation terminates. From $12$ there are two steps, $12 \to 6$ and $12 \to 4$, then $6 \to 3$, $6 \to 2$, $4 \to 2$, $3 \to 1$ and $2 \to 1$. Each element reduces to $1$, the only normal form, so the relation is convergent and $m{\downarrow} = 1$ for each $m$. The number of steps from $m$ to $1$ is the number of prime factors of $m$ counted with multiplicity, whichever path is taken.

**Locally confluent but not confluent.** Let $A = \{a, b, c, d\}$ with $b \to a$, $b \to c$, $c \to b$ and $c \to d$. Each one-step divergence joins: $a \leftarrow b \to c$ joins at $a$ since $c \to b \to a$, and $b \leftarrow c \to d$ joins at $d$ since $b \to c \to d$. But $a \leftarrow^* b \to^* d$, and $a$ and $d$ are distinct normal forms, so the relation is not confluent. It is not terminating either ($b \to c \to b \to \cdots$), which is why [Newman's lemma](/newman-lemma/) does not apply.

**Weakly normalizing but not terminating.** On $A = \{a, b\}$ with $a \to a$ and $a \to b$, the element $a$ has the normal form $b$, but $a \to a \to \cdots$ is infinite.

**Terminating but not confluent.** On $\{a, b, c\}$ with $a \to b$ and $a \to c$, every reduction has length at most one, and $a$ has two normal forms.

**An open problem.** On the positive integers, let $n \to n/2$ when $n$ is even and $n \to 3n + 1$ when $n > 1$ is odd. This ARS is deterministic, so it is confluent, and its only normal form is $1$. Whether it terminates is the Collatz conjecture. So a very small ARS can already have a termination question that nobody can answer.

**Concrete systems.** A [term rewriting system](/term-rewriting-system/) $R$ gives the ARS $(T(\Sigma, V), \to_R)$, a [string rewriting system](/string-rewriting-system/) gives an ARS on strings, the [lambda calculus](/lambda-calculus/) with [beta-reduction](/beta-reduction/) is an ARS on lambda terms, and the transition relation of a [Turing machine](/turing-machine/) is a deterministic ARS on configurations.

**Non-example: labelled steps.** An ARS keeps only which steps exist, not why. Two different rules that turn $x$ into $y$ give the same pair $(x, y)$. Results that count steps or compare reductions, such as the parallel moves of [orthogonal systems](/orthogonal-rewrite-system/), need an indexed ARS, a family of relations $(\to_i)_{i \in I}$, or the terms and positions themselves.

**Non-example: a function.** A function $f : A \to A$ is a special ARS in which each element has exactly one reduct. Such an ARS has no normal form at all, so it is never terminating unless $A$ is empty. A partial function, which may be undefined on some elements, gives a deterministic ARS whose normal forms are the elements where it is undefined.

## Related definitions

- [Normal form](/normal-form/), [joinability](/joinability/), [confluence](/confluence/), [local confluence](/local-confluence/), [termination](/termination/) and [weak normalization](/weak-normalization/) are the properties defined above, each with its own page.
- [Newman's lemma](/newman-lemma/) and the [Hindley-Rosen lemma](/hindley-rosen-lemma/) are the two classic theorems about abstract reduction systems.
- A [term rewriting system](/term-rewriting-system/) and a [string rewriting system](/string-rewriting-system/) are the main concrete instances; [equational theories](/equational-theory/) are their conversions $\leftrightarrow^*$.
- A [well-founded relation](/well-founded-relation/) is the inverse of a terminating ARS, and well-founded induction on $\to^+$ is the main proof method for terminating systems.

## References
