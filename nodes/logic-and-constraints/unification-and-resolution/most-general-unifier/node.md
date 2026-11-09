---
tag: 3ZC33M
kind: concept
slug: most-general-unifier
name: Most general unifier
aliases:
- mgu
- principal unifier
area: logic-and-constraints/unification-and-resolution
level: core
summary: A unifier of which every other unifier is an instance; unique up to variable renaming.
prereqs: [unifier, substitution]
see_also: [mgu-existence-theorem, unification-problem, idempotent-substitution, robinson-unification, martelli-montanari-unification, binary-resolution, equational-unification, plotkin-lgg]
sources:
  - paper: doi:10.1145/321250.321253
    title: J. A. Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965, pages 23 to 41
    locator: the definition of a most general unifier and the unification theorem
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 4.5, Syntactic unification (most general unifiers and their uniqueness up to renaming)
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 2 (syntactic unification) and Section 3 (complete sets of unifiers and unification types)
---

A **most general unifier** (mgu) of a [unification problem](/unification-problem/) is a [unifier](/unifier/) $\sigma$ such that every other unifier $\theta$ is an instance of it: $\theta = \sigma\lambda$ for some [substitution](/substitution/) $\lambda$. It makes the terms equal while it commits to as little as possible. The [unification theorem](/mgu-existence-theorem/) says that each unifiable problem has one, and that it is unique up to a renaming of variables. So the mgu is a finite description of the infinite set of all unifiers.

## In plain words

Two patterns with blanks can often be made equal in many ways. One way fills a blank with a specific value that nothing forces. Another way fills only what the two patterns force and leaves the rest open. The second way is the most general one. Every other solution is that solution plus some extra choices.

So one answer stands for all answers. A theorem prover or a Prolog system needs only this one answer, and it can add the extra choices later, when another step forces them. Two most general answers differ only in the names of their blanks, so the answer is unique in practice. For plain syntactic equality the best answer always exists. When symbols obey laws such as commutativity, one best answer can be too few, and a set of answers takes its place.

## The idea

Notation, as in the rest of this area: $n$ is the number of variables, $m$ the number of equations, $\sigma, \theta$ are substitutions, $t\sigma$ is the application of $\sigma$ to $t$, and $\sigma\theta$ means "first $\sigma$, then $\theta$".

**The instance order.** $\sigma \le \theta$ ($\sigma$ is more general than $\theta$) when $\theta = \sigma\lambda$ for some $\lambda$. This is a preorder. Two substitutions with $\sigma \le \theta$ and $\theta \le \sigma$ are **equivalent**, and they differ by a renaming of variables.

**Definition.** Let $E$ be a set of equations and $\mathcal{U}(E)$ its set of unifiers. A unifier $\sigma \in \mathcal{U}(E)$ is a **most general unifier** of $E$ when $\sigma \le \theta$ for each $\theta \in \mathcal{U}(E)$. So an mgu is a least element of $\mathcal{U}(E)$ in the preorder $\le$.

Since $\mathcal{U}(E)$ is closed under instances (if $\sigma$ unifies $E$, so does $\sigma\lambda$), an mgu $\sigma$ gives the whole set:

$$\mathcal{U}(E) = \{\, \sigma\lambda : \lambda \text{ a substitution} \,\}.$$

**Order on a set of variables.** Many texts compare substitutions only on the variables of the problem. For a set $X$ of variables, $\sigma \le_X \theta$ when $x\theta = x\sigma\lambda$ for each $x \in X$, for some $\lambda$. With $X = \mathrm{Var}(E)$, this weaker order lets an mgu use new variables. The difference shows in the example $x \doteq y$ below.

**Facts.** The [unification theorem](/mgu-existence-theorem/) proves these facts for syntactic unification in the free term algebra.

1. **Existence.** If $E$ is unifiable, it has an mgu $\sigma$. It can be chosen [idempotent](/idempotent-substitution/), with $\mathrm{dom}(\sigma) \cup \mathrm{vran}(\sigma) \subseteq \mathrm{Var}(E)$.
2. **Uniqueness up to renaming.** If $\sigma$ and $\sigma'$ are mgus of $E$, there is a renaming $\rho$ with $x\sigma' = x\sigma\rho$ for each $x \in \mathrm{Var}(E)$.
3. **Fixed point test.** If $\sigma$ is an idempotent mgu, then $\theta \in \mathcal{U}(E)$ if and only if $\theta = \sigma\theta$.

**Computation.** [Robinson's algorithm](/robinson-unification/) computes an mgu, or reports failure, but its output written as one map can be exponential in the input size. The [Martelli-Montanari algorithm](/martelli-montanari-unification/) and the union-find method are almost linear, and the [Paterson-Wegman algorithm](/paterson-wegman-unification/) is linear. The last two represent the mgu as a [term DAG](/term-dag/) or in triangular form, because the mgu written out as trees can have size exponential in the input.

**Beyond syntactic unification.** In [equational unification](/equational-unification/), terms are equal modulo a theory, and one mgu may not exist. For example, under commutativity of $+$, the problem $x + y \doteq a + b$ has the two incomparable unifiers $\{x \mapsto a,\ y \mapsto b\}$ and $\{x \mapsto b,\ y \mapsto a\}$. The mgu is then replaced by a minimal complete set of unifiers. A theory where the mgu always exists is called **unitary**, and syntactic unification is the main example.

**The dual notion.** The least general generalization of the [anti-unification problem](/anti-unification-problem/) is the dual object: the most specific term that has both inputs as instances. [Plotkin's algorithm](/plotkin-lgg/) computes it.

## Examples

Below $a, b$ are constants, $f, g, h$ are function symbols and $x, y, z, x_i$ are variables.

**One equation, two mgus that differ by a renaming.** For $f(x_1, h(x_1), x_2) \doteq f(g(x_3), x_4, x_3)$, Robinson's algorithm gives

$$\sigma = \{x_1 \mapsto g(x_3),\ x_4 \mapsto h(g(x_3)),\ x_2 \mapsto x_3\},$$

and the Paterson-Wegman algorithm, which chooses the other variable of the class $\{x_2, x_3\}$, gives

$$\sigma' = \{x_1 \mapsto g(x_2),\ x_4 \mapsto h(g(x_2)),\ x_3 \mapsto x_2\}.$$

With the renaming $\rho = \{x_2 \mapsto x_3,\ x_3 \mapsto x_2\}$, $\sigma\rho = \sigma'$. Both sides become $f(g(x_3), h(g(x_3)), x_3)$ under $\sigma$.

**A unifier that is not most general.** For the same problem, $\theta = \{x_1 \mapsto g(a),\ x_4 \mapsto h(g(a)),\ x_2 \mapsto a,\ x_3 \mapsto a\}$ is a unifier, and $\theta = \sigma\{x_3 \mapsto a\}$. It is not most general: $\theta$ is ground on the variables of the problem, so no instance of $\theta$ gives back $\sigma$.

**Equivalent mgus.** For $x \doteq y$, both $\{x \mapsto y\}$ and $\{y \mapsto x\}$ are mgus, and $\{x \mapsto y\}\{y \mapsto x\} = \{y \mapsto x\}$. The unifier $\{x \mapsto z,\ y \mapsto z\}$ with a new variable $z$ is an mgu in the order $\le_{\{x, y\}}$, but not in the order $\le$ on all variables. It is not more general than $\{x \mapsto y\}$, because each instance of it maps $z$ to the same term as $x$, while $\{x \mapsto y\}$ maps $z$ to $z$ and $x$ to $y$.

**An mgu with large output.** For $f(x_1, \ldots, x_n) \doteq f(g(x_0, x_0), \ldots, g(x_{n-1}, x_{n-1}))$, the mgu maps $x_n$ to a complete binary tree of $g$ nodes with $2^{n+1} - 1$ nodes. As a DAG with shared subterms, the same mgu has $n + 1$ nodes.

**No mgu because no unifier.** $f(x, x) \doteq f(a, b)$ and $x \doteq f(x)$ have no unifier, so they have no mgu.

## Where it is used

- **Resolution.** [Binary resolution](/binary-resolution/) and [factoring](/factoring/) use an mgu of the complementary literals. The [lifting lemma](/lifting-lemma/) needs the mgu: it shows that each ground resolution step is an instance of a step with the mgu, so a prover can work with the mgu only and stay complete.
- **Logic programming.** Each step of [SLD resolution](/sld-resolution/) unifies the goal with a clause head by an mgu. The [answer substitution](/answer-substitution/) is the composition of these mgus. The [Warren abstract machine](/warren-abstract-machine/) compiles this unification.
- **Rewriting and completion.** Critical pairs in [Knuth-Bendix completion](/knuth-bendix-completion/) and [superposition](/superposition/) are built from the mgu of a rule's left side and a subterm of another rule.
- **Type inference.** Hindley-Milner type inference solves type equations with unification, and the most general type of an expression is the mgu applied to its type variables.
- **Term indexing.** [Term indexes](/term-indexing/) retrieve the stored terms that unify with a query, and the prover then computes the mgu for each candidate.

## References
