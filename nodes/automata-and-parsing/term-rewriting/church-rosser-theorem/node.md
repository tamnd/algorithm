---
tag: 4E73DY
kind: theorem
slug: church-rosser-theorem
name: Church-Rosser theorem
aliases:
- Church-Rosser property of beta-reduction
area: automata-and-parsing/term-rewriting
level: core
summary: Beta-reduction in the lambda calculus is confluent.
prereqs: [beta-reduction, confluence, lambda-calculus]
see_also: [orthogonal-confluence-theorem, newman-lemma, hindley-rosen-lemma, normal-form, combinatory-logic, standardization-theorem]
sources:
  - paper: "Alonzo Church and J. Barkley Rosser, Some properties of conversion, Transactions of the American Mathematical Society 39(3) (1936)"
    locator: pp. 472 to 482 (the original proof, for the lambda-I calculus and for beta-delta reduction)
  - book: isbn:9780444875082
    title: Henk P. Barendregt, The Lambda Calculus, Its Syntax and Semantics, revised edition, North-Holland, 1984
    locator: Chapter 3, Reduction (the Church-Rosser theorem for beta by the method of Tait and Martin-Löf, and its consequences); Chapter 2 (the substitution lemma)
  - paper: doi:10.1006/inco.1995.1057
    title: Masako Takahashi, Parallel reductions in lambda-calculus, Information and Computation 118(1) (1995)
    locator: pp. 120 to 127 (the proof through the complete development M*)
  - book: isbn:9780521898850
    title: J. Roger Hindley and Jonathan P. Seldin, Lambda-Calculus and Combinators, an Introduction, Cambridge University Press, 2008
    locator: Appendix A2, Confluence proofs
---

The **Church-Rosser theorem** states that [beta-reduction](/beta-reduction/) in the untyped [lambda calculus](/lambda-calculus/) is [confluent](/confluence/): if a term reduces to two terms, they reduce to a common term. As a result, a lambda term has at most one [normal form](/normal-form/), two terms are beta-equal exactly when they have a common reduct, and the calculus is consistent, since distinct normal forms such as $\lambda x.\, \lambda y.\, x$ and $\lambda x.\, \lambda y.\, y$ are not equal. The proof cannot go through [Newman's lemma](/newman-lemma/), because beta-reduction does not terminate; it goes through parallel reduction instead.

## Statement

Let $\Lambda$ be the set of lambda terms modulo $\alpha$-conversion, $\to_\beta$ one-step beta-reduction (a redex $(\lambda x.\, M)\,N$ contracted to $M[x := N]$ at any position, also under $\lambda$), $\twoheadrightarrow_\beta$ its reflexive transitive closure and $=_\beta$ beta-conversion.

**Theorem (Church and Rosser, 1936).** For all $M, M_1, M_2 \in \Lambda$,

$$M \twoheadrightarrow_\beta M_1 \ \text{ and } \ M \twoheadrightarrow_\beta M_2 \implies \exists N:\ M_1 \twoheadrightarrow_\beta N \ \text{ and } \ M_2 \twoheadrightarrow_\beta N.$$

Equivalently (Church-Rosser property): $M =_\beta M'$ implies that $M$ and $M'$ have a common reduct.

**Corollaries.**

1. If $M$ has a beta-normal form, it is unique up to $\alpha$-conversion.
2. If $N$ is a normal form and $M =_\beta N$, then $M \twoheadrightarrow_\beta N$.
3. Two distinct normal forms are not beta-equal, so $=_\beta$ does not identify all terms: the lambda calculus is consistent.

The same holds for $\beta\eta$-reduction.

## In plain words

A lambda term can have several places where a function is applied to an argument, and each can be evaluated first. The theorem says that this choice never matters for the final answer. If two people evaluate the same expression in different orders and stop at different points, both can continue and reach the same expression.

The difficulty is that one evaluation step can copy an argument many times or throw it away. So one step on one side may need many steps on the other side to catch up, and evaluation might go on forever. The proof uses a bigger kind of step that evaluates any chosen set of places at once. For this bigger step, two different choices can always be repaired in exactly one more bigger step each, and that settles the matter.

## Proof

The full proof is in [the proof by parallel reduction](proofs/main.md). Its structure:

1. **Parallel reduction.** Define $M \Rightarrow M'$ to contract any set of the redexes present in $M$ simultaneously: $x \Rightarrow x$; it is compatible with $\lambda$ and application; and $M \Rightarrow M'$, $N \Rightarrow N'$ give $(\lambda x.\, M)\,N \Rightarrow M'[x := N']$.
2. **Sandwich.** ${\to_\beta} \subseteq {\Rightarrow} \subseteq {\twoheadrightarrow_\beta}$, so $\Rightarrow^* = \twoheadrightarrow_\beta$.
3. **Substitution.** $M \Rightarrow M'$ and $N \Rightarrow N'$ imply $M[x := N] \Rightarrow M'[x := N']$, by induction on $M \Rightarrow M'$ with the syntactic substitution lemma.
4. **Triangle.** Let $M^*$ contract all redexes of $M$, from the inside: $((\lambda x.\, P)\,Q)^* = P^*[x := Q^*]$, and $M^*$ commutes with the other constructors. Then $M \Rightarrow M'$ implies $M' \Rightarrow M^*$, by induction on $M \Rightarrow M'$ with step 3.
5. **Diamond.** So any two parallel steps from $M$ meet at $M^*$ in one parallel step each, and by tiling a grid of such diamonds, $\Rightarrow^*$ has the diamond property. By step 2 this is confluence of $\to_\beta$. $\blacksquare$

**Why plain beta-steps do not have the diamond property.** Let $I = \lambda z.\, z$, $\Delta = \lambda x.\, x\,x$ and $M = \Delta\,(I\,y)$. Then $M \to_\beta (I\,y)\,(I\,y)$ and $M \to_\beta \Delta\,y \to_\beta y\,y$. From $(I\,y)\,(I\,y)$ two steps are needed to reach $y\,y$, while $\Delta\,y$ reaches it in one. So one step on each side does not close the peak; one parallel step on each side does, since $(I\,y)\,(I\,y) \Rightarrow y\,y$ and $\Delta\,y \Rightarrow y\,y$.

## Consequences

- **Unique results.** A functional program written as a lambda term has at most one result, whatever the evaluation order. This justifies [outermost reduction](/outermost-reduction/), call-by-value and lazy evaluation as different ways to find the same normal form.
- **Consistency.** $=_\beta$ is a non-trivial equational theory, so the lambda calculus is a consistent system.
- **Deciding equality of normalizing terms.** If $M$ and $N$ both have normal forms, then $M =_\beta N$ iff their normal forms are $\alpha$-equal, which a normalizing strategy computes.
- **Orthogonal systems.** The same parallel-reduction argument proves the [orthogonal confluence theorem](/orthogonal-confluence-theorem/) for first-order term rewriting, and it shows confluence of [combinatory logic](/combinatory-logic/).
- **Unions of relations.** With the [Hindley-Rosen lemma](/hindley-rosen-lemma/), confluence of $\beta$ and of $\eta$, and their commutation, give confluence of $\beta\eta$.

## Tightness

- **Termination is not available.** $\Omega = (\lambda x.\, x\,x)(\lambda x.\, x\,x) \to_\beta \Omega$, so beta-reduction is not terminating, and [Newman's lemma](/newman-lemma/) cannot turn local confluence into confluence here.
- **Normal forms need not be reached.** Confluence does not say that every reduction from a normalizing term reaches its normal form: $(\lambda x.\, \lambda y.\, y)\,\Omega$ reduces to $\lambda y.\, y$ in one step, and also to itself forever. Reaching it needs a good strategy, which is the content of the [standardization theorem](/standardization-theorem/).
- **Extensions can break it.** Adding rules to the lambda calculus can destroy confluence. Klop showed that the lambda calculus extended with surjective pairing, a pairing constant with projections and the rule that rebuilds a pair from its two projections, is not confluent, although each part is.

## History

Church and Rosser proved the theorem in 1936, for a version of the calculus that did not allow discarding arguments, and their proof was a long analysis of residuals of redexes. W. Tait and P. Martin-Löf found the method of parallel reduction around 1971, which Barendregt's book presents and which is the standard proof today. Masako Takahashi in 1995 simplified it further with the complete development $M^*$, which turns the diamond into a triangle. Huet and others carried the method over to first-order term rewriting systems, where it proves confluence of orthogonal systems.

## References
