---
tag: R36NJ8
kind: theorem
slug: mgu-existence-theorem
name: Unification theorem
aliases:
- most general unifier theorem
area: logic-and-constraints/unification-and-resolution
level: core
summary: Unifiable terms have a most general unifier, unique up to variable renaming.
prereqs: [unifier, most-general-unifier, substitution]
see_also: [unification-problem, idempotent-substitution, robinson-unification, martelli-montanari-unification, lifting-lemma, robinson-completeness-theorem, equational-unification, plotkin-lgg]
sources:
  - paper: doi:10.1145/321250.321253
    title: J. A. Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965, pages 23 to 41
    locator: the unification algorithm and the unification theorem, which states that the algorithm terminates and returns a most general unifier of each unifiable finite set of expressions
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 4.5, Syntactic unification, and Section 4.6, Unification by transformation (the rule-based proof that a unifiable problem has an idempotent most general unifier)
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 2 (syntactic unification; most general unifiers and their uniqueness up to renaming) and Section 3 (unification types)
  - paper: doi:10.1145/357162.357169
    title: Alberto Martelli and Ugo Montanari, An efficient unification algorithm, ACM Transactions on Programming Languages and Systems 4(2), 1982, pages 258 to 282
    locator: the transformation rules on sets of equations and the proof that they reach a solved form that gives a most general unifier
---

The **unification theorem** says that if a finite set of equations between first-order [terms](/term/) has a [unifier](/unifier/), then it has a [most general unifier](/most-general-unifier/), and this mgu is unique up to a renaming of variables. J. A. Robinson proved it in 1965 together with his [unification algorithm](/robinson-unification/), and it is the reason that [resolution](/robinson-resolution/) can work with one unifier per step instead of all ground instances. The [unification problem](/unification-problem/) page states the computational task; this page states and proves the theorem behind it.

## Statement

Let $\Sigma$ be a signature, $V$ an infinite set of variables, and $E = \{s_1 \doteq t_1, \ldots, s_m \doteq t_m\}$ a finite set of equations between terms of $T(\Sigma, V)$. Notation: $n = |\mathrm{Var}(E)|$, $\sigma, \theta$ are substitutions, $t\sigma$ is the application of $\sigma$ to $t$, $\sigma\theta$ means "first $\sigma$, then $\theta$", and $\sigma \le \theta$ means $\theta = \sigma\lambda$ for some $\lambda$. $\mathcal{U}(E)$ is the set of unifiers of $E$.

**Theorem (Robinson 1965).**

**(a) Existence.** If $\mathcal{U}(E) \ne \emptyset$, then $E$ has a most general unifier $\sigma$: $\sigma \in \mathcal{U}(E)$ and $\sigma \le \theta$ for each $\theta \in \mathcal{U}(E)$. Moreover $\sigma$ can be chosen with

- $\sigma\sigma = \sigma$ ([idempotent](/idempotent-substitution/)),
- $\theta = \sigma\theta$ for each $\theta \in \mathcal{U}(E)$, and
- $\mathrm{dom}(\sigma) \cup \mathrm{vran}(\sigma) \subseteq \mathrm{Var}(E)$.

**(b) Uniqueness up to renaming.** If $\sigma$ and $\sigma'$ are most general unifiers of $E$, then there is a renaming $\rho$ (a bijection of $V$ that moves finitely many variables) with $x\sigma' = x\sigma\rho$ for each $x \in \mathrm{Var}(E)$.

**(c) Effectiveness.** There is an algorithm that, given $E$, decides whether $\mathcal{U}(E) \ne \emptyset$ and, if so, outputs the $\sigma$ of (a).

## In plain words

Take two patterns with blanks. If some filling of the blanks makes them equal, then there is a best filling. The best filling commits to nothing that equality does not force, and every other good filling is the best one with more filled in. Any two best fillings differ only in the names they give to the blanks that stay open. There is also a mechanical way to find the best filling, or to learn that none exists.

The proof follows the way a person solves such a puzzle. Equal outer symbols mean the parts must be equal. Different outer symbols mean failure. A blank that must equal a pattern without that blank gets that pattern everywhere, and then one blank fewer is left. A blank that must equal a larger pattern that holds the blank itself means failure.

## Proof

The full proof is in the proof file below. Here is its plan.

**Existence.** Induction on the pair (number of variables of $E$, total size of $E$) in the lexicographic order. The claim proved is slightly stronger: either $E$ has no unifier, or it has a unifier $\sigma$ with the three properties of (a). Pick an equation $e$ of $E$.

- $e$ is $x \doteq x$: drop it. The size drops.
- $e$ is $f(s_1, \ldots, s_k) \doteq f(t_1, \ldots, t_k)$: replace it by $s_i \doteq t_i$. The unifiers are the same and the size drops by 2.
- $e$ is $f(\ldots) \doteq g(\ldots)$ with $f \ne g$: no unifier.
- $e$ is $x \doteq t$ with $x$ in $t$ and $t \ne x$: no unifier, because $|t\theta| > |x\theta|$ for each $\theta$.
- $e$ is $x \doteq t$ with $x$ not in $t$: let $\tau = \{x \mapsto t\}$. Each unifier $\theta$ of $E$ satisfies $\theta = \tau\theta$, so it unifies $E'' = (E \setminus \{e\})\tau$, which has one variable fewer. If $\mu$ is the substitution of the induction hypothesis for $E''$, then $\sigma = \tau\mu$ works: $\sigma\theta = \tau\mu\theta = \tau\theta = \theta$.

**Uniqueness.** If $\sigma$ and $\sigma'$ are both mgus, then $x\sigma' = x\sigma\lambda$ and $x\sigma = x\sigma'\lambda'$ on the variables $x$ of $E$, so $x\sigma = x\sigma\lambda\lambda'$. Substitution never makes a term smaller, and it keeps the size only if it maps variables to variables. So $\lambda\lambda'$ is the identity on the variables $Y$ of the terms $x\sigma$, and $\lambda$ maps $Y$ one to one onto a set of variables of the same size. Such a map extends to a renaming $\rho$, and $x\sigma' = x\sigma\rho$.

**Effectiveness.** The induction is a terminating recursive procedure. [Robinson's algorithm](/robinson-unification/) and the [Martelli-Montanari rules](/martelli-montanari-unification/) are two ways to run it.

## Consequences

- **The mgu describes all unifiers.** By (a), $\mathcal{U}(E) = \{\sigma\theta : \theta \text{ any substitution}\}$, and with an idempotent $\sigma$, $\theta \in \mathcal{U}(E)$ if and only if $\theta = \sigma\theta$. So a single substitution of size at most exponential in the input stands for an infinite set.
- **Lifting lemma and completeness of resolution.** A resolution step between ground instances $C\theta_1$ and $D\theta_2$ is an instance of the resolution step between $C$ and $D$ with the mgu of the clashing literals. This is the [lifting lemma](/lifting-lemma/), and with [Herbrand's theorem](/herbrand-theorem/) it gives the [completeness of resolution](/robinson-completeness-theorem/). The same argument lifts [SLD resolution](/sld-resolution/), [paramodulation](/paramodulation/) and [superposition](/superposition/).
- **Answer substitutions in logic programming.** Each answer of [SLD resolution](/sld-resolution/) is a most general answer, because each step uses an mgu, so the [answer substitution](/answer-substitution/) is unique up to renaming for a given derivation.
- **Principal types.** Hindley-Milner type inference applies the theorem to equations between type terms, and gets the principal (most general) type of an expression.
- **Unitary type.** In the terms of [equational unification](/equational-unification/), the theorem says that syntactic unification (the empty theory) is **unitary**: each solvable problem has a single most general solution.
- **Dual result.** For generalization, the dual theorem of Plotkin and Reynolds says that any two terms have a least general generalization, unique up to renaming. See the [anti-unification problem](/anti-unification-problem/) and [Plotkin's algorithm](/plotkin-lgg/).

## Tightness

- **Renaming cannot be removed.** $x \doteq y$ has the two mgus $\{x \mapsto y\}$ and $\{y \mapsto x\}$. More generally, $\sigma\rho$ is an mgu for each mgu $\sigma$ and renaming $\rho$, so (b) is the best possible uniqueness.
- **Idempotence is a choice.** Not every mgu is idempotent: $\{x \mapsto y\}\{z \mapsto w,\ w \mapsto z\} = \{x \mapsto y,\ z \mapsto w,\ w \mapsto z\}$ is an mgu of $x \doteq y$ that is not.
- **Equational theories.** The theorem fails once equality is modulo a theory. Under commutativity of $+$, $x + y \doteq a + b$ has the two incomparable unifiers $\{x \mapsto a,\ y \mapsto b\}$ and $\{x \mapsto b,\ y \mapsto a\}$ and no single mgu. Under associativity, $x \cdot a \doteq a \cdot x$ has the unifiers $\{x \mapsto a\}$, $\{x \mapsto a \cdot a\}$, and so on, an infinite minimal set (Plotkin 1972). For idempotent semigroups, some problems have no minimal complete set at all (Baader 1986; Schmidt-Schauß 1986). See [equational unification](/equational-unification/).
- **Higher order.** For function variables, $F(a) \doteq a$ has the two incomparable solutions $F \mapsto \lambda z.\, a$ and $F \mapsto \lambda z.\, z$, and no mgu. See the [higher-order unification problem](/higher-order-unification-problem/).
- **Finite terms.** The occurs case is needed: $x \doteq f(x)$ has no unifier in finite terms. Over infinite rational trees it has the solution $x = f(f(f(\cdots)))$, and the theory is different. See the [occurs check](/occurs-check/).
- **Size.** The idempotent mgu of (a) can have size exponential in the size of $E$. For $f(x_1, \ldots, x_n) \doteq f(g(x_0, x_0), \ldots, g(x_{n-1}, x_{n-1}))$, the input has size $4n + 2$ and $x_n\sigma$ has $2^{n+1} - 1$ symbols. Shared representations ([term DAGs](/term-dag/)) avoid this blow-up.

## History

Herbrand's thesis of 1930 already contains rules for solving equations between terms, close to the transformation rules used in the proof above. Robinson's 1965 paper on resolution introduced the words unifier and most general unifier, gave the first unification algorithm, and proved this theorem as the basis of the lifting argument for resolution. Martelli and Montanari (1982) recast unification as solving a set of equations by transformation rules, which is the form of the proof here, and gave an efficient algorithm. Knight's 1989 survey and the chapter of Baader and Snyder trace these developments.

## References
