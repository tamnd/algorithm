---
tag: W1Y0N8
kind: concept
slug: idempotent-substitution
name: Idempotent substitution
aliases:
- idempotent unifier
area: logic-and-constraints/unification-and-resolution
level: core
summary: A substitution with sigma sigma = sigma, which holds exactly when no variable of its domain occurs in its range; each unifiable problem has an idempotent most general unifier.
prereqs: [substitution, unifier]
see_also: [most-general-unifier, mgu-existence-theorem, robinson-unification, martelli-montanari-unification, paterson-wegman-unification, term-dag, answer-substitution]
sources:
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 2 (idempotent substitutions and idempotent most general unifiers)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 4.5, Syntactic unification, and Section 4.6, Unification by transformation (solved forms give idempotent most general unifiers)
  - book: "Jean-Louis Lassez, Michael J. Maher and Kim Marriott, Unification revisited, in J. Minker (editor), Foundations of Deductive Databases and Logic Programming, Morgan Kaufmann, 1988"
    locator: the sections on idempotent substitutions and on the characterization theta = sigma theta of the unifiers of an idempotent most general unifier sigma
---

An **idempotent substitution** is a [substitution](/substitution/) $\sigma$ with $\sigma\sigma = \sigma$: applying it a second time changes nothing. This holds exactly when no variable that $\sigma$ replaces occurs in the terms that it puts in. Every unifiable problem has an idempotent [most general unifier](/most-general-unifier/), and the standard algorithms ([Robinson](/robinson-unification/), [Martelli-Montanari](/martelli-montanari-unification/)) return one. For an idempotent most general unifier $\sigma$, a substitution $\theta$ is a [unifier](/unifier/) if and only if $\theta = \sigma\theta$.

## In plain words

A substitution is a list of replacements: put this term in place of that variable. Suppose a replacement puts in a term that still holds a variable which the list itself also replaces. Then one pass leaves work undone, and a second pass changes the result again. An idempotent substitution has no such leftover: the variables it replaces never appear in what it puts in. One pass is final.

This is the normal form that unification algorithms give. It is easy to read, because each replaced variable has its final value. It also gives a simple test: a substitution is a solution of the same equations exactly when doing the idempotent answer first, and then the other substitution, changes nothing.

## The idea

We use the notation of the [substitution](/substitution/) page: $\mathrm{dom}(\sigma) = \{x : x\sigma \ne x\}$, $\mathrm{vran}(\sigma) = \bigcup_{x \in \mathrm{dom}(\sigma)} \mathrm{Var}(x\sigma)$, composition $\sigma\theta$ means "first $\sigma$, then $\theta$", and $\sigma \le \theta$ means $\theta = \sigma\lambda$ for some $\lambda$.

**Definition.** $\sigma$ is **idempotent** if $\sigma\sigma = \sigma$, that is, $(x\sigma)\sigma = x\sigma$ for each variable $x$.

**Lemma 1.** $\sigma$ is idempotent if and only if $\mathrm{dom}(\sigma) \cap \mathrm{vran}(\sigma) = \emptyset$.

*Proof.* Suppose the intersection is empty. If $x \notin \mathrm{dom}(\sigma)$, then $x\sigma\sigma = x\sigma = x$. If $x \in \mathrm{dom}(\sigma)$, each variable of $x\sigma$ is outside $\mathrm{dom}(\sigma)$, so $\sigma$ fixes each of them and $(x\sigma)\sigma = x\sigma$.

Conversely, suppose $y \in \mathrm{dom}(\sigma)$ occurs in $x\sigma$ for some $x \in \mathrm{dom}(\sigma)$. Applying $\sigma$ to a term never decreases its size, and it keeps the size only if it maps each variable of the term to a variable. If $y\sigma$ is not a variable, then $|x\sigma\sigma| > |x\sigma|$. If $y\sigma$ is a variable $y' \ne y$, then $x\sigma\sigma$ has $y'$ at each position where $x\sigma$ has $y$. In both cases $x\sigma\sigma \ne x\sigma$. $\square$

**Lemma 2.** If $\sigma$ is idempotent, then $\sigma \le \theta$ if and only if $\theta = \sigma\theta$.

*Proof.* If $\theta = \sigma\theta$, take $\lambda = \theta$. If $\theta = \sigma\lambda$, then $\sigma\theta = \sigma\sigma\lambda = \sigma\lambda = \theta$. $\square$

**Corollary.** Let $\sigma$ be an idempotent most general unifier of a problem $E$. Then a substitution $\theta$ is a unifier of $E$ if and only if $\theta = \sigma\theta$.

*Proof.* A unifier $\theta$ satisfies $\sigma \le \theta$, so $\theta = \sigma\theta$ by Lemma 2. Conversely, if $\theta = \sigma\theta$, then for each equation $s \doteq t$ of $E$, $s\theta = (s\sigma)\theta = (t\sigma)\theta = t\theta$. $\square$

So the set of unifiers of $E$ is exactly the set of fixed points of the map $\theta \mapsto \sigma\theta$. Lassez, Maher and Marriott use this as the definition of a most general unifier in their survey.

**Existence.** By the [unification theorem](/mgu-existence-theorem/), each unifiable problem $E$ has an idempotent most general unifier $\sigma$ with $\mathrm{dom}(\sigma) \cup \mathrm{vran}(\sigma) \subseteq \mathrm{Var}(E)$. Not every most general unifier is idempotent. If $\sigma$ is a most general unifier and $\rho$ is a renaming, $\sigma\rho$ is also one, and it is often not idempotent.

**Size.** Idempotence has a cost. A solved, idempotent form writes the final value of each variable in full, so it can be exponentially larger than a triangular form $\{x_1 \mapsto t_1\} \cdots \{x_k \mapsto t_k\}$ or a [term DAG](/term-dag/). The [Paterson-Wegman algorithm](/paterson-wegman-unification/) keeps the triangular form to stay linear.

## Examples

**Idempotent.** $\sigma = \{x \mapsto f(y, a),\ z \mapsto y\}$. Here $\mathrm{dom}(\sigma) = \{x, z\}$ and $\mathrm{vran}(\sigma) = \{y\}$, so $\sigma$ is idempotent. The identity $\varepsilon$ and each ground substitution (no variables in the range) are idempotent.

**Not idempotent, with a cycle.** $\{x \mapsto f(x)\}$: $x\sigma\sigma = f(f(x)) \ne f(x)$. No power of it is idempotent.

**Not idempotent, but equivalent to an idempotent one.** $\sigma = \{x \mapsto f(y),\ y \mapsto z\}$ has $y$ in both sets: $x\sigma\sigma = f(z) \ne f(y)$. Here $\sigma\sigma = \{x \mapsto f(z),\ y \mapsto z\}$ is idempotent.

**A renaming breaks idempotence.** For $E = \{x \doteq y\}$, $\sigma = \{x \mapsto y\}$ is an idempotent most general unifier. With the renaming $\rho = \{z \mapsto w,\ w \mapsto z\}$, $\sigma\rho = \{x \mapsto y,\ z \mapsto w,\ w \mapsto z\}$ is still a most general unifier of $E$, since $(\sigma\rho)\rho = \sigma$, but $z$ is in its domain and in its range.

**Composition does not keep idempotence.** $\sigma = \{x \mapsto f(y)\}$ and $\theta = \{y \mapsto g(x)\}$ are idempotent, but $\sigma\theta = \{x \mapsto f(g(x)),\ y \mapsto g(x)\}$ is not: $x$ is in its domain and in its range.

**The test $\theta = \sigma\theta$.** Take $E = \{f(x, g(y)) \doteq f(g(z), x)\}$ with idempotent most general unifier $\sigma = \{x \mapsto g(y),\ z \mapsto y\}$. For $\theta = \{x \mapsto g(a),\ y \mapsto a,\ z \mapsto a\}$, $\sigma\theta$ maps $x$ to $g(y)\theta = g(a)$, $z$ to $y\theta = a$ and $y$ to $a$, so $\sigma\theta = \theta$ and $\theta$ is a unifier. For $\theta' = \{x \mapsto g(a),\ z \mapsto b\}$, $z\sigma\theta' = y \ne b$, so $\theta'$ is not a unifier, and indeed $x\theta' = g(a)$ but $g(z)\theta' = g(b)$.

## Where it is used

- [Robinson's algorithm](/robinson-unification/) and the [Martelli-Montanari rules](/martelli-montanari-unification/) keep the substitution built so far idempotent, and return an idempotent most general unifier. Their correctness proofs use the invariant $\theta = \sigma\theta$ for each unifier $\theta$.
- The proof of the [unification theorem](/mgu-existence-theorem/) builds the idempotent most general unifier by induction, and uses Lemma 2 at each step.
- In [SLD resolution](/sld-resolution/), the [answer substitution](/answer-substitution/) of a query is the composition of the most general unifiers of the steps, restricted to the variables of the query.
- Solved forms in constraint logic programming and in type inference are idempotent substitutions written as sets of equations $x_i \doteq t_i$.

## References
