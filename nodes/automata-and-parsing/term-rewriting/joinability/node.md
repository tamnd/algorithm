---
tag: AP77KC
kind: definition
slug: joinability
name: Joinability
aliases:
- joinable terms
area: automata-and-parsing/term-rewriting
level: core
summary: Two terms are joinable if they reduce to a common term.
prereqs: [abstract-reduction-system]
see_also: [confluence, local-confluence, critical-pair, critical-pair-lemma, normal-form, newman-lemma]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.1 (the relation of joinability and the Church-Rosser property); Chapter 6, Section 6.2, Critical pairs
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 1, Abstract reduction systems (the common reduct relation); Chapter 2, Section on critical pairs
  - paper: doi:10.1145/322217.322230
    title: Gérard Huet, Confluent reductions, abstract properties and applications to term rewriting systems, Journal of the ACM 27(4) (1980)
    locator: pp. 797 to 821 (joinability of critical pairs and the critical pair lemma)
---

Two elements of an [abstract reduction system](/abstract-reduction-system/) are **joinable** when each of them reduces, in zero or more steps, to one common element. Joinability is the local check behind [confluence](/confluence/): a system is confluent when all pairs that come from one element are joinable, and the [critical pair lemma](/critical-pair-lemma/) says that for a term rewriting system it is enough to check the joinability of finitely many [critical pairs](/critical-pair/). In a terminating system the check is mechanical, since each element has only finitely many reducts.

## Definition

Let $(A, \to)$ be an abstract reduction system. The notation is that of the term rewriting pages: $\to^*$ is the reflexive transitive closure of $\to$, $\leftarrow^*$ its inverse, and $\leftrightarrow^*$ the least equivalence relation that contains $\to$.

Elements $x, y \in A$ are **joinable**, written $x \downarrow y$, if

$$\exists z \in A:\quad x \to^* z \ \text{ and } \ y \to^* z.$$

The element $z$ is a **common reduct**. For a term rewriting system $R$ on $T(\Sigma, V)$, terms $s$ and $t$ are joinable when $s \downarrow_R t$ for the relation $\to_R$. A pair $\langle s, t \rangle$ is **joinable** if $s \downarrow t$, and a set of pairs is joinable if each pair in it is.

Basic facts, each proved from the definition:

1. **$\downarrow$ is reflexive and symmetric**, with $z = x$ for $x \downarrow x$ and the same $z$ for both orders.
2. **${\downarrow} \subseteq {\leftrightarrow^*}$,** because $x \to^* z \leftarrow^* y$ is a conversion.
3. **$\downarrow$ is transitive if and only if $\to$ is confluent.** If $\to$ is confluent, it is Church-Rosser, so $x \leftrightarrow^* y$ implies $x \downarrow y$, so ${\downarrow} = {\leftrightarrow^*}$, which is transitive. Conversely, if $\downarrow$ is transitive and $y_1 \leftarrow^* x \to^* y_2$, then $y_1 \downarrow x$ (common reduct $y_1$) and $x \downarrow y_2$ (common reduct $y_2$), so $y_1 \downarrow y_2$.
4. **In a convergent system,** $x \downarrow y$ iff $x{\downarrow} = y{\downarrow}$, where $x{\downarrow}$ is the unique [normal form](/normal-form/) of $x$. If $x \to^* z \leftarrow^* y$, the normal form of $z$ is a normal form of both. Conversely, the common normal form is a common reduct.
5. **Two distinct normal forms are never joinable,** because a normal form reduces only to itself.

**Deciding joinability.** If $\to$ is terminating and finitely branching (each element has finitely many one-step reducts, which holds for a finite term rewriting system), then by König's lemma the set $\{z : x \to^* z\}$ is finite, and $x \downarrow y$ is decided by computing the two reduct sets and testing them for a common element. If $\to$ is convergent, it is enough to compute and compare two normal forms. Without termination, joinability is only semi-decidable for a finite term rewriting system: enumerating the reducts of $x$ and $y$ in breadth-first order finds a common reduct when one exists, and runs forever otherwise. It is undecidable in general, because $x \downarrow h$ for a normal form $h$ is the same as $x \to^* h$, and reachability in a [string rewriting system](/string-rewriting-system/) is undecidable.

**Variants.** $x$ and $y$ are **strongly joinable** if $x \to^= z \leftarrow^* y$ and $x \to^* z' \leftarrow^= y$ for some $z, z'$, where $\to^=$ means zero or one step; Huet used this in his lemma for linear systems. In rewriting modulo a set of equations $E$, $x$ and $y$ are joinable modulo $E$ if $x \to^* z_1$, $y \to^* z_2$ and $z_1$ and $z_2$ are equal modulo $E$.

## Examples and non-examples

**One step against two.** Let $R = \{f(x) \to g(x, x),\ a \to b\}$. The term $f(a)$ has two one-step reducts:

$$f(b) \leftarrow f(a) \to g(a, a).$$

They are joinable: $f(b) \to g(b, b)$ and $g(a, a) \to g(b, a) \to g(b, b)$, so the common reduct $g(b, b)$ is reached in one step on one side and two steps on the other. The rule copies the argument $x$, so one step inside $a$ becomes two steps after the copy. The full reduct set of $f(a)$ is $\{f(a), g(a,a), f(b), g(a,b), g(b,a), g(b,b)\}$.

**A critical pair that joins.** Let $R = \{f(g(x)) \to g(f(x)),\ f(a) \to a,\ g(a) \to a\}$. The term $f(g(a))$ can be rewritten at the root by the first rule and inside, at position $1$, by the third rule:

$$g(f(a)) \leftarrow f(g(a)) \to f(a).$$

Both sides reduce to $a$: $g(f(a)) \to g(a) \to a$ and $f(a) \to a$. So this critical pair is joinable.

**A pair that does not join.** Let $R = \{f(a) \to b,\ a \to c\}$. Then $b \leftarrow f(a) \to f(c)$, and both $b$ and $f(c)$ are normal forms. They are distinct, so they are not joinable, and $R$ is not confluent. Adding the rule $f(c) \to b$ makes the pair joinable, which is the step that [Knuth-Bendix completion](/knuth-bendix-completion/) takes.

**Not transitive.** In the system $b \leftarrow a \to c$ with three constants, $b \downarrow a$ and $a \downarrow c$ hold, but $b \downarrow c$ fails. This is fact 3 above for a system that is not confluent.

**The empty system.** If $R = \emptyset$, each term reduces only to itself, so $s \downarrow t$ iff $s = t$.

**Non-example: a conversion is not a join.** In $\{b \to a,\ b \to c\}$, the conversion $a \leftarrow b \to c$ shows $a \leftrightarrow^* c$, but $a$ and $c$ are distinct normal forms, so they are not joinable. Joinability asks for a common reduct below, not a common ancestor above.

## Related definitions

- [Confluence](/confluence/) is joinability of all pairs $y_1 \leftarrow^* x \to^* y_2$, and [local confluence](/local-confluence/) is joinability of all pairs $y_1 \leftarrow x \to y_2$.
- A [critical pair](/critical-pair/) is a pair from an overlap of two rules; the [critical pair lemma](/critical-pair-lemma/) says that a term rewriting system is locally confluent iff all its critical pairs are joinable.
- [Newman's lemma](/newman-lemma/) turns local confluence into confluence for terminating systems, so for a finite terminating system confluence is decided by joining the critical pairs.
- [Normal forms](/normal-form/) are joinable only when they are equal, which is why joinability gives uniqueness of normal forms.

## References
