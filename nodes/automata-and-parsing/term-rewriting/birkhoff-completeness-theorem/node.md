---
tag: J4A5S3
kind: theorem
slug: birkhoff-completeness-theorem
name: Birkhoff completeness theorem
aliases:
- Birkhoff's theorem
- completeness of equational logic
area: automata-and-parsing/term-rewriting
level: advanced
summary: An equation follows semantically from a set of equations iff it is derivable equationally.
prereqs: [equational-theory, term, substitution]
see_also: [word-problem, knuth-bendix-completion, term-rewriting-system, inductive-theorem-proving, congruence-closure, term-algebra, undecidability-of-word-problem]
sources:
  - paper: doi:10.1017/S0305004100013463
    title: Garrett Birkhoff, On the structure of abstract algebras, Proceedings of the Cambridge Philosophical Society 31(4) (1935)
    locator: pp. 433 to 454 (the rules of equational deduction, their completeness, and the characterization of equational classes)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 3, Universal Algebra (soundness and completeness of equational logic, proved with the quotient term algebra, and the equality of derivability with the conversion of E)
  - book: isbn:9780387905785
    title: Stanley Burris and H. P. Sankappanavar, A Course in Universal Algebra, Graduate Texts in Mathematics 78, Springer, 1981
    locator: Chapter II, Section 14, Equational logic and fully invariant congruences (Birkhoff's completeness theorem)
---

The **Birkhoff completeness theorem** says that an equation is true in every algebra that satisfies a set $E$ of equations exactly when it can be derived from $E$ by the five rules of equational logic: reflexivity, symmetry, transitivity, congruence and substitution. Since derivability is the same as conversion by the rules of $E$ used in both directions, the theorem turns a question about all algebras into a question about rewriting terms. This is what makes [term rewriting systems](/term-rewriting-system/) and [Knuth-Bendix completion](/knuth-bendix-completion/) decision procedures for semantic questions, and what makes the [word problem](/word-problem/) of an [equational theory](/equational-theory/) a syntactic problem.

## Statement

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, $t|_p$ and $t[s]_p$, substitutions $\sigma$, rules $l \to r$, and $\to^*$ for reflexive transitive closures. $\approx_E$ is derivability in equational logic from $E$ and $\leftrightarrow_E^*$ is the conversion relation of $E$, the least equivalence that contains all replacement steps $u[l\sigma]_p \leftrightarrow u[r\sigma]_p$ for $l \approx r \in E$.

A $\Sigma$-algebra $\mathcal{A}$ is a non-empty set $A$ with a function $f^{\mathcal{A}} : A^n \to A$ for each $n$-ary $f \in \Sigma$. It **satisfies** $s \approx t$ if $s$ and $t$ have the same value under every assignment of elements of $A$ to the variables. Write $E \models s \approx t$ if every algebra that satisfies all equations of $E$ satisfies $s \approx t$.

**Theorem (Birkhoff, 1935).** For every set $E$ of equations and all terms $s, t \in T(\Sigma, V)$:

$$E \models s \approx t \iff s \approx_E t \iff s \leftrightarrow_E^* t.$$

The second equivalence is purely syntactic and is proved on the [equational theory](/equational-theory/) page. The first is soundness ($\Leftarrow$) and completeness ($\Rightarrow$) of equational logic.

## In plain words

There are two ways to say that an equation follows from some rules about operations. The first: it is true in every structure where the rules are true, whatever the elements and whatever the operations do. The second: one can get from one side to the other by replacing equals by equals, using the rules and filling in the variables in any way. The theorem says that both ways give the same equations. So to check the first, which talks about infinitely many structures, it is enough to search for a chain of replacements, and to show that an equation does not follow, it is enough to find one structure where it fails.

## Proof

The full proof is in [the proof with the term model](proofs/main.md). Its structure:

1. **Substitution lemma.** The value of $t\sigma$ under an assignment $\alpha$ is the value of $t$ under the assignment $x \mapsto$ value of $x\sigma$ under $\alpha$. By induction on $t$.
2. **Soundness.** Each rule of equational logic preserves truth in a fixed model of $E$; for substitution this is step 1. So $s \approx_E t$ implies $E \models s \approx t$.
3. **Term model.** Because $\approx_E$ is a congruence, the quotient $\mathcal{Q} = T(\Sigma, V)/{\approx_E}$ is an algebra with $f^{\mathcal{Q}}([t_1], \ldots, [t_n]) = [f(t_1, \ldots, t_n)]$. Under an assignment that picks the class of $x\sigma$ for each $x$, a term $t$ has the value $[t\sigma]$.
4. **$\mathcal{Q}$ is a model of $E$.** For $l \approx r$ in $E$ and any assignment, the values are $[l\sigma]$ and $[r\sigma]$, which are equal because $\approx_E$ is closed under substitution.
5. **Completeness.** If $E \models s \approx t$, then $\mathcal{Q}$ satisfies $s \approx t$; under the assignment $x \mapsto [x]$ this says $[s] = [t]$, that is, $s \approx_E t$. $\blacksquare$

## Consequences

- **Rewriting decides semantic questions.** If $E$ has an equivalent convergent [term rewriting system](/term-rewriting-system/) $R$, then $E \models s \approx t$ iff $s$ and $t$ have the same normal form under $R$. For example, an equation holds in all groups iff both sides have the same normal form under the ten rules that [Knuth-Bendix completion](/knuth-bendix-completion/) produces from the three group axioms.
- **Semi-decidability.** For a recursively enumerable $E$, the set of consequences $\{ s \approx t : E \models s \approx t \}$ is recursively enumerable: enumerate derivations, or conversions. It need not be decidable: there are finite $E$ with an undecidable [word problem](/word-problem/) ([undecidability of the word problem](/undecidability-of-word-problem/)).
- **Compactness.** A derivation uses finitely many equations of $E$, so $E \models s \approx t$ implies $E_0 \models s \approx t$ for a finite $E_0 \subseteq E$.
- **Counter-models.** To show $E \not\models s \approx t$, exhibit one model of $E$ in which $s \approx t$ fails; by the theorem, $s \approx t$ is then not derivable. The theorem says that a counter-model always exists when there is no derivation, namely the term model.
- **Free algebras and varieties.** The term model is the free algebra over $V$ in the class of models of $E$. Birkhoff's second theorem in the same paper, the HSP theorem, characterizes the classes of algebras definable by equations as those closed under homomorphic images, subalgebras and products.
- **Ground equations.** For a finite set of ground equations, the consequences between ground terms are decided by [congruence closure](/congruence-closure/).

## Tightness

- **Truth in one model is weaker.** An equation can hold in the intended model and still not follow from $E$. With $E = \{ x + 0 \approx x,\ x + s(y) \approx s(x + y) \}$, the equation $0 + x \approx x$ holds for all natural numbers, but it is not a consequence of $E$. A counter-model is the set $\{0, 1\}$ with $s$ the identity, $x + 0 = x$ and $x + 1 = 0$: both equations of $E$ hold, and $0 + 1 = 0 \ne 1$. Such equations, true in the initial model $T(\Sigma)/{\approx_E}$ of ground terms, are inductive theorems, the subject of [inductive theorem proving](/inductive-theorem-proving/).
- **All five rules are needed.** Without the substitution rule, $f(x) \approx b$ does not give $f(a) \approx b$, although every model of $f(x) \approx b$ satisfies $f(a) \approx b$. Without congruence, $a \approx b$ does not give $f(a) \approx f(b)$.
- **Only equations.** The theorem is about universally quantified equations. For implications, such as cancellation $x \cdot y \approx x \cdot z \Rightarrow y \approx z$, the matching completeness result is for Horn clauses and needs other rules.
- **Empty sorts.** For many-sorted algebras whose sorts may be empty, the five rules are not sound as stated: transitivity through a term with a variable of an empty sort can derive an equation that fails. The rules must then record the variables in use.

## History

Garrett Birkhoff stated the rules of equational deduction and proved their completeness in 1935, in the same paper as his characterization of equational classes, now called varieties, by closure under homomorphic images, subalgebras and products. The theorem became the semantic basis of term rewriting when Knuth and Bendix in 1970 used rewriting to decide word problems in universal algebra. Goguen and Meseguer later gave the corrected rules for many-sorted equational logic with possibly empty sorts.

## References
