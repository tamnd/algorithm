---
tag: M0J1CY
kind: theorem
slug: newman-lemma
name: Newman's lemma
aliases:
- diamond lemma
area: automata-and-parsing/term-rewriting
level: core
summary: A terminating system is confluent if it is locally confluent.
prereqs: [abstract-reduction-system, local-confluence, confluence, well-founded-relation]
see_also: [critical-pair-lemma, knuth-bendix-completion, termination, hindley-rosen-lemma, joinability, normal-form]
sources:
  - paper: doi:10.2307/1968867
    title: M. H. A. Newman, On theories with a combinatorial definition of "equivalence", Annals of Mathematics 43(2) (1942)
    locator: pp. 223 to 243 (the original statement and proof)
  - paper: doi:10.1145/322217.322230
    title: Gérard Huet, Confluent reductions, abstract properties and applications to term rewriting systems, Journal of the ACM 27(4) (1980)
    locator: pp. 797 to 821, Section 2 (the proof by well-founded induction)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.7, Proving confluence
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 1, Abstract reduction systems (Newman's lemma and several of its proofs)
---

**Newman's lemma** says that a terminating reduction relation is [confluent](/confluence/) as soon as it is [locally confluent](/local-confluence/). Confluence is a statement about reductions of any length, and local confluence only about single steps, so the lemma lets one check finitely many small diagrams instead of infinitely many large ones. For term rewriting systems, combined with the [critical pair lemma](/critical-pair-lemma/), it gives the Knuth-Bendix test: a finite terminating system is confluent if and only if all its [critical pairs](/critical-pair/) are [joinable](/joinability/).

## Statement

Let $(A, \to)$ be an [abstract reduction system](/abstract-reduction-system/), with $\to^*$ the reflexive transitive closure and $\to^+$ the transitive closure of $\to$.

**Theorem (Newman, 1942).** If $\to$ is terminating, that is, there is no infinite sequence $x_0 \to x_1 \to x_2 \to \cdots$, and $\to$ is locally confluent, that is,

$$y_1 \leftarrow x \to y_2 \implies \exists z:\ y_1 \to^* z \leftarrow^* y_2,$$

then $\to$ is confluent:

$$y_1 \leftarrow^* x \to^* y_2 \implies \exists z:\ y_1 \to^* z \leftarrow^* y_2.$$

So a terminating and locally confluent relation is convergent, and each element $x$ has exactly one [normal form](/normal-form/) $x{\downarrow}$.

## In plain words

Think of the elements as positions in a game where each move goes "down", and no player can move down forever. Suppose that whenever two different single moves start at one position, the two results can always be brought back together by more moves. The lemma says that then any two long sequences of moves from one position can also be brought back together.

The proof works from the bottom up. Positions near the bottom, with few moves left, are handled first. For a higher position, the two long sequences start with two single moves, which can be joined by the assumption. What is left are smaller problems that start lower down, and they are already solved. Without the guarantee that moves cannot go on forever, the bottom does not exist, and the argument has nothing to stand on.

## Proof

Because $\to$ is terminating, the relation $\succ$ defined by $x \succ y$ iff $x \to^+ y$ is well-founded: an infinite descending chain $x_0 \succ x_1 \succ \cdots$ would give an infinite reduction by joining the nonempty reductions $x_i \to^+ x_{i+1}$. So we may use well-founded induction on $\succ$ (see [well-founded relation](/well-founded-relation/)).

Let $P(x)$ be the property "$x$ is confluent", that is, for all $y_1, y_2$, $y_1 \leftarrow^* x \to^* y_2$ implies $y_1 \downarrow y_2$. We prove $P(x)$ for all $x$, assuming as induction hypothesis that $P(y)$ holds for every $y$ with $x \to^+ y$.

Take $y_1 \leftarrow^* x \to^* y_2$.

1. **One side is empty.** If $x = y_1$, then $y_1 \to^* y_2$, and $z = y_2$ joins them. The case $x = y_2$ is the same.
2. **Both sides are nonempty.** Then $x \to x_1 \to^* y_1$ and $x \to x_2 \to^* y_2$ for some $x_1, x_2$.
3. **Close the local peak.** By local confluence applied to $x_1 \leftarrow x \to x_2$, there is $u$ with $x_1 \to^* u$ and $x_2 \to^* u$.
4. **Use the hypothesis at $x_1$.** Since $x \to^+ x_1$, $P(x_1)$ holds. From $y_1 \leftarrow^* x_1 \to^* u$ we get $v$ with $y_1 \to^* v$ and $u \to^* v$.
5. **Use the hypothesis at $x_2$.** Since $x \to^+ x_2$, $P(x_2)$ holds. Now $x_2 \to^* u \to^* v$ and $x_2 \to^* y_2$, so $v \leftarrow^* x_2 \to^* y_2$, and we get $w$ with $v \to^* w$ and $y_2 \to^* w$.
6. **Combine.** $y_1 \to^* v \to^* w$ and $y_2 \to^* w$, so $y_1 \downarrow y_2$ with common reduct $w$.

Thus $P(x)$ holds. By well-founded induction, $P(x)$ holds for each $x \in A$, so $\to$ is confluent. $\blacksquare$

The proof uses the induction hypothesis at two elements, $x_1$ and $x_2$, both one step below $x$. It never needs the hypothesis at $x$ itself, which is why termination, and not only weak normalization, is the right condition.

## Consequences

- **The Knuth-Bendix confluence test.** By the [critical pair lemma](/critical-pair-lemma/), a term rewriting system is locally confluent iff all its critical pairs are joinable. With Newman's lemma, a terminating finite system is confluent iff each of its finitely many critical pairs reduces to a common term, and since normal forms are computable, iff the two sides of each critical pair have the same normal form. This makes [confluence decidable](/confluence-decision-problem/) for finite terminating systems.
- **Completion.** [Knuth-Bendix completion](/knuth-bendix-completion/) keeps the system terminating with a reduction ordering and adds rules until all critical pairs are joinable. Newman's lemma then shows that the result is convergent, so it decides the [equational theory](/equational-theory/) of the input equations by comparing normal forms.
- **Unique normal forms.** A terminating and locally confluent system has the unique normal form property, so any [normal form computation](/normal-form-computation/) strategy, for example [innermost reduction](/innermost-reduction/), returns the same result.
- **Gröbner bases.** Buchberger's criterion for Gröbner bases, that all S-polynomials reduce to zero, is an instance of the same idea: polynomial reduction modulo a set of polynomials terminates, and local confluence is checked on finitely many overlaps.

## Tightness

Neither hypothesis can be dropped, and termination cannot be weakened to weak normalization.

- **Without local confluence.** $a \to b$ and $a \to c$ terminate, but $b$ and $c$ are distinct normal forms.
- **Without termination.** On $\{a, b, c, d\}$ let $b \to a$, $b \to c$, $c \to b$, $c \to d$. The local peaks $a \leftarrow b \to c$ and $b \leftarrow c \to d$ join at $a$ and at $d$, so the relation is locally confluent. It is even weakly normalizing. But $a \leftarrow^* b \to^* d$ with $a \ne d$ normal forms. An acyclic example also exists: $a_i \to a_{i+1}$ for all $i \ge 0$, $a_i \to b$ for even $i$ and $a_i \to c$ for odd $i$.
- **The converse fails.** Confluence does not imply termination: $a \to a$ is confluent. So the lemma gives a sufficient condition for confluence, and the [Church-Rosser theorem](/church-rosser-theorem/) and the [orthogonal confluence theorem](/orthogonal-confluence-theorem/) cover the many non-terminating confluent systems.

## History

Max Newman proved the lemma in 1942, in a paper on theories whose equivalence is generated by single reduction steps. His proof was complicated. Gérard Huet gave the short proof by well-founded induction, the one above, in his 1980 paper on confluent reductions, and this is the proof found in the textbooks. The same paper made the link between Newman's lemma, critical pairs and completion explicit.

## References
