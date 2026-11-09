---
tag: 2742H6
kind: technique
slug: skolemization
name: Skolemization
aliases:
- Skolem functions
- Skolem normal form
- Skolem form
area: logic-and-constraints/unification-and-resolution
level: core
summary: Replace each existential quantifier by a new function of the universal variables around it. The result is satisfiable exactly when the input is, but it is not equivalent to it.
prereqs: [prenex-normal-form, term]
see_also: [clausal-normal-form, herbrand-theorem, herbrand-universe, first-order-theorem-proving, robinson-resolution, quantifier-instantiation]
sources:
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 4, Section 4.2, Skolem standard forms (the construction from a prenex form and Theorem 4.1, which says that the standard form is unsatisfiable exactly when the formula is)
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 6, Andreas Nonnengart and Christoph Weidenbach, Computing small clause normal forms (Skolemization, the choice of Skolem arguments, and miniscoping)
  - paper: "Thoralf Skolem, Logisch-kombinatorische Untersuchungen über die Erfüllbarkeit oder Beweisbarkeit mathematischer Sätze nebst einem Theoreme über dichte Mengen, Skrifter utgit av Videnskapsselskapet i Kristiania, 1920"
    locator: the normal form for satisfiability, in which existential quantifiers are replaced by functions, used for the proof of the Löwenheim-Skolem theorem
---

Skolemization removes the existential quantifiers of a first-order formula. Each subformula $\exists y \, G$ that lies in the scope of the universal variables $x_1, \ldots, x_n$ is replaced by $G[f(x_1, \ldots, x_n)/y]$, where $f$ is a new function symbol, a **Skolem function**. The result has only universal quantifiers, so a prover can drop them and work with free variables. It is **satisfiable exactly when the input is**, which is all that a [refutation](/refutation/) prover needs, but it is **not equivalent** to the input. Skolemization is the step between [prenex normal form](/prenex-normal-form/) and [clausal normal form](/clausal-normal-form/).

## In plain words

"For every person there is a mother" says that a mother exists, but it does not name her. Skolemization gives the unknown a name that depends on what it may depend on: "the mother of this person", written as a new function.

The new sentence says more than the old one: it claims that a specific way to pick the mother exists. So the two sentences are not the same. But if the old sentence can be true in some world, we can always choose such a way to pick, so the new sentence can be true too. And if the new sentence is true, the old one is true. For a prover that only asks "can these sentences all be true together?", the answer stays the same.

## When it applies

- **The question is satisfiability.** To prove $\Gamma \models \varphi$, a prover shows that $\Gamma \cup \{\lnot \varphi\}$ has no model. Skolemize this set, not $\varphi$ itself.
- **The formula is in negation normal form.** Negations must sit on atoms, so that each $\exists$ really is existential. An $\exists$ under a $\lnot$, or on the left of $\to$, is a universal in disguise.
- **The signature can grow.** Each Skolem symbol must be new. This is never a problem in first-order logic, but it matters in settings with a fixed signature, such as a theory with a fixed set of function symbols.

## The template

```pseudo id=main
SKOLEMIZE(F)
L1  F ← the negation normal form of F, with bound variables renamed apart
L2  for each subformula ∃y G of F, from the outside in
L3      z₁, …, zₙ ← the argument variables of ∃y G          ▷ hole: which variables
L4      f ← a function symbol of arity n not used so far      ▷ hole: fresh symbol
L5      replace ∃y G by G[f(z₁, …, zₙ)/y]
L6  delete the ∀ quantifiers; all variables are now universal  ▷ hole: output form
L7  return F
```

**The holes.**

- *The argument variables (L3).* The classic choice, from a prenex form, is all universal variables to the left of $\exists y$. A smaller sound choice is the universal variables in whose scope $\exists y \, G$ lies and that are free in $\exists y \, G$. Fewer arguments give smaller terms and more unifications that succeed.
- *The fresh symbol (L4).* It must not occur in the formula or in any other part of the problem. The proof below needs this.
- *The output form (L6).* A prover goes on to [clausal normal form](/clausal-normal-form/). A [Herbrand](/herbrand-theorem/) style procedure goes on to ground instances over the [Herbrand universe](/herbrand-universe/).

**Theorem (Skolem).** Let $F$ be a closed formula in negation normal form, let $\exists y \, G$ be an occurrence of a subformula of $F$ whose free variables other than $y$ are among $z_1, \ldots, z_n$, and let $f$ be an $n$-ary function symbol that does not occur in $F$. Let $F'$ be $F$ with this occurrence replaced by $G[f(z_1, \ldots, z_n)/y]$. Then:

1. $F' \models F$: every model of $F'$ is a model of $F$.
2. Every model $M$ of $F$ has an expansion $M'$, which adds an interpretation of $f$ and changes nothing else, that is a model of $F'$.

So $F$ and $F'$ are equisatisfiable, and by induction on the number of $\exists$, so are $F$ and its full Skolem form.

*Proof.* We use the substitution lemma: the truth value of $G[t/y]$ under an assignment $\beta$ is the truth value of $G$ under $\beta[y \mapsto t^\beta]$, where $t^\beta$ is the value of $t$.

(1) For every structure that interprets $f$ and every assignment $\beta$, if $G[f(\vec z)/y]$ is true, then $G$ is true under $\beta[y \mapsto f(\vec z)^\beta]$, so $\exists y \, G$ is true. In negation normal form every subformula occurrence is positive: the only connectives above it are $\wedge$, $\vee$, $\forall$ and $\exists$, and each of them is monotone, so replacing a subformula by a weaker one cannot turn a true formula false. Induction on the context of the occurrence gives that $F'$ true implies $F$ true, in every structure.

(2) Let $M$ have domain $D$. For each $\vec d \in D^n$, let $W(\vec d)$ be the set of $e \in D$ such that $G$ is true in $M$ when $\vec z \mapsto \vec d$ and $y \mapsto e$. Define $f^{M'}(\vec d)$ as an element of $W(\vec d)$ if this set is not empty, and as any element of $D$ otherwise. (For an infinite $D$ this uses the axiom of choice; for a countable $D$, take the first element in a fixed enumeration.) Then, under every assignment, $\exists y \, G$ and $G[f(\vec z)/y]$ have the same truth value in $M'$: if some $e$ works, $f^{M'}(\vec d)$ is such an $e$; if none works, both are false. Replacing a subformula by one with the same truth value under all assignments keeps the truth value of $F$, so $F'$ and $F$ have the same truth value in $M'$. Since $f$ does not occur in $F$, the truth value of $F$ in $M'$ is its truth value in $M$, which is true. $\square$

**Skolemization is not equivalence.** Take $F = \forall x \exists y \, R(x, y)$ and its Skolem form $F' = \forall x \, R(x, f(x))$. In the domain $\{0, 1\}$ with $R = \{(0, 1), (1, 0)\}$ and $f$ the identity, $F$ is true and $F'$ is false, because $R(0, 0)$ is false. So $F \not\models F'$. Part 2 of the theorem says only that **some** interpretation of $f$, here $f(0) = 1$ and $f(1) = 0$, makes $F'$ true. The smallest case is $\exists x \, P(x)$ and $P(c)$: with domain $\{0, 1\}$, $P = \{1\}$ and $c = 0$, the first is true and the second is false.

**Example.** The negation of the drinker formula $\exists x (D(x) \to \forall y \, D(y))$ is $\forall x (D(x) \wedge \exists y \, \lnot D(y))$ in negation normal form. The $\exists y$ lies in the scope of $\forall x$, but $x$ is not free in $\exists y \, \lnot D(y)$. The classic choice gives $D(x) \wedge \lnot D(f(x))$. The smaller choice gives $D(x) \wedge \lnot D(c)$. Both are unsatisfiable, but the second gives a ground unit clause, and the refutation is one step: resolve $D(x)$ with $\lnot D(c)$.

## Classic examples

- [Clausal normal form](/clausal-normal-form/): every resolution and superposition prover Skolemizes the negated goal and the axioms before it makes clauses.
- [Herbrand's theorem](/herbrand-theorem/): it is stated for universal formulas, and Skolemization brings every formula to that shape. The [Herbrand universe](/herbrand-universe/) is built from the Skolem symbols and the other function symbols.
- [Robinson's resolution](/robinson-resolution/) and [superposition](/superposition/): the Skolem terms become ordinary terms that [unification](/most-general-unifier/) can match.
- [Quantifier instantiation](/quantifier-instantiation/) in SMT solvers: an existential quantifier in a positive position is Skolemized to a fresh constant once, and universal ones are instantiated.
- The Löwenheim-Skolem theorem: Skolem used his functions to show that a satisfiable countable set of first-order sentences has a countable model.

## Variations

- **Herbrandization.** The dual, for validity: replace each universal quantifier, in a formula whose validity is in question, by a function of the existential variables before it. The result is valid exactly when the input is. It is the same as Skolemizing the negation and negating again.
- **Inner and outer Skolemization.** Outer Skolemization uses all universal variables in scope, as in the prenex route. Inner Skolemization uses only those free in the subformula, as in the drinker example. Both are sound by the theorem, since it only needs the free variables among the arguments.
- **Miniscoping first.** Push quantifiers inward before Skolemization, as in [prenex normal form](/prenex-normal-form/) in reverse. The arguments then become fewer, often zero.
- **Definitional forms.** When a large subformula would be copied by the clausal form, name it with a new predicate first, then Skolemize. See [clausal normal form](/clausal-normal-form/).

## Pitfalls

- **An existential under a negation.** Skolemizing $\lnot \exists x \, P(x)$ as $\lnot P(c)$ is wrong: the formula says that no $x$ has $P$, which is $\forall x \lnot P(x)$. With the extra fact $P(a)$, the set $\{\lnot \exists x \, P(x), P(a)\}$ is unsatisfiable, but $\{\lnot P(c), P(a)\}$ is satisfiable, so the prover misses the refutation. Compute the negation normal form first, as line L1 does.
- **Skolemizing the goal instead of its negation.** To prove $\exists x \, P(x)$ from $P(a)$, negate first: $\forall x \lnot P(x)$ has no existential, and $\{P(a), \lnot P(x)\}$ is refuted at once. Skolemizing the goal to $P(c)$ and then negating it gives $\lnot P(c)$, and $\{P(a), \lnot P(c)\}$ is satisfiable, so a true theorem is not proved.
- **A symbol that is not new.** $\exists x \, P(x) \wedge \exists x \lnot P(x)$ is satisfiable, but with one constant $c$ for both quantifiers it becomes $P(c) \wedge \lnot P(c)$, which is not. The same happens with a constant of the input: $\exists x \lnot P(x) \wedge P(a)$ with $x \mapsto a$. Line L4 must take a symbol that is not used anywhere.
- **Too few arguments.** $\forall x \exists y \, R(x, y) \wedge \forall x \lnot R(x, x)$ is satisfiable, with $R = \{(0, 1), (1, 0)\}$. If the Skolem term for $y$ drops the argument $x$, the result $\forall x \, R(x, c) \wedge \forall x \lnot R(x, x)$ gives $R(c, c)$ and $\lnot R(c, c)$, so it is unsatisfiable. An argument may be dropped only when the variable is not free in the subformula.
- **Expecting equivalence.** A Skolem form must not be used where equivalence is needed, for example to simplify a formula that will be negated later, or to answer "is this formula valid?" without negating first.

## Exercises

1. Skolemize $\forall x \exists y \forall z \exists w \, R(x, y, z, w)$ with the classic choice. *Answer:* $\forall x \forall z \, R(x, f(x), z, g(x, z))$.
2. Show that $\exists y \forall x \, R(x, y)$ Skolemizes to $\forall x \, R(x, c)$, and that this form implies the Skolem form $\forall x \, R(x, f(x))$ of $\forall x \exists y \, R(x, y)$ under $f(x) = c$.
3. Give a satisfiable formula whose Skolem form has no finite model, although the formula has an infinite model, or show that no such formula exists. *Hint:* part 2 of the theorem keeps the domain.
4. Prove that the Herbrandization of a formula $F$ is valid exactly when $F$ is valid, from the theorem applied to $\lnot F$.
5. In the drinker example, show that the classic Skolem form $\{D(x), \lnot D(f(x))\}$ has a resolution refutation with the unifier $x \mapsto f(x')$ after renaming apart.

## References
