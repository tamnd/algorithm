---
tag: H4ZF52
kind: theorem
slug: lifting-lemma
name: Lifting lemma
aliases:
- lifting theorem
- resolution lifting lemma
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: If two clauses have instances with a binary resolvent R', then factors of the clauses have a binary resolvent R of which R' is an instance. It lifts ground refutations to first-order ones.
prereqs: [binary-resolution, factoring, most-general-unifier]
see_also: [robinson-completeness-theorem, binary-resolution, factoring, herbrand-theorem, most-general-unifier, mgu-existence-theorem, standardization-apart, ordered-resolution]
sources:
  - paper: doi:10.1145/321250.321253
    title: John Alan Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965
    locator: the proof of the resolution theorem, in which resolution of ground instances is lifted to resolution of the general clauses by the most general unifier
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 5, The resolution principle (the lifting lemma for instances of clauses, and its use in the completeness proof)
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 2, Leo Bachmair and Harald Ganzinger, Resolution theorem proving (lifting of ground inferences, and the role of stable orderings and selection)
---

The **lifting lemma** says that a [binary resolution](/binary-resolution/) step between instances of two clauses is an instance of a step between the clauses themselves, after [factoring](/factoring/): if $C_1\theta_1$ and $C_2\theta_2$ have a binary resolvent $R'$, then some factors of $C_1$ and $C_2$ have a binary resolvent $R$ with $R' = R\lambda$ for a substitution $\lambda$. It is the reason why resolution needs only [most general unifiers](/most-general-unifier/): every ground step is covered by one general step. It is Step 3 of the proof of the [Robinson completeness theorem](/robinson-completeness-theorem/), which lifts a ground refutation, given by [Herbrand's theorem](/herbrand-theorem/), to a first-order refutation.

## Statement

Clauses are sets of literals. A factor of $C$ is $C\mu$, where $\mu$ is an mgu of a set of at least two literals of $C$ with the same sign; here $C$ also counts as a factor of itself.

**Lemma (lifting, resolution).** Let $C_1$ and $C_2$ be clauses with no common variable, and let $\theta$ be a substitution. Let $L' \in C_1\theta$ and $M' \in C_2\theta$ be literals of opposite sign whose atoms have an mgu $\sigma'$, and let

$$R' = \big((C_1\theta \setminus \{L'\}) \cup (C_2\theta \setminus \{M'\})\big)\sigma'.$$

Then there are factors $F_1$ of $C_1$ and $F_2$ of $C_2$, a binary resolvent $R$ of $F_1$ and $F_2$, and a substitution $\lambda$ with $R\lambda = R'$.

**Lemma (lifting, factoring).** Let $C$ be a clause, $\theta$ a substitution, and $F'$ a factor of $C\theta$. Then $C$ has a factor $F$ with $F\lambda = F'$ for some $\lambda$.

**Two instances with their own substitutions.** If the instances are $C_1\theta_1$ and $C_2\theta_2$, and the second is renamed apart from the first as the rule asks, then one $\theta$ that agrees with $\theta_1$ on the variables of $C_1$ and with the renamed $\theta_2$ on those of $C_2$ gives both, because the variables of $C_1$ and $C_2$ are disjoint. This is where [standardization apart](/standardization-apart/) is used.

**Corollary (lifting derivations).** If a clause $E'$ has a derivation by binary resolution and factoring from instances of clauses of $S$, then some clause $E$ has a derivation from $S$ by the same rules, with the same number of resolution steps, and $E' = E\lambda$. In particular, a refutation of a set of instances lifts to a refutation of $S$.

## In plain words

A prover could fill in the variables of its clauses with concrete terms and then combine the concrete copies. That works, but there are endlessly many ways to fill in. The lemma says that the prover can skip the filling in. Whatever a step on concrete copies produces is a special case of what a step on the general clauses produces, if the general step makes the two combined parts match in the most general way.

Sometimes filling in turns two different parts of one clause into the same part. The general step can do the same by first merging those parts, which is why merging is needed next to combining.

## Proof

We use one fact about unifiers from the [mgu existence theorem](/mgu-existence-theorem/): a unifiable set $E$ has an mgu $\mu$ with $\mathrm{dom}(\mu) \cup \mathrm{vran}(\mu) \subseteq \mathrm{Var}(E)$, and every unifier $\vartheta$ of $E$ satisfies $\vartheta = \mu\vartheta$, so in particular $\vartheta = \mu\vartheta'$ for $\vartheta' = \vartheta$. Composition $\mu\vartheta$ means: apply $\mu$ first. We write $\mathrm{atom}(L)$ for the atom of a literal.

**Resolution.** Let

$$K_1 = \{L \in C_1 : L\theta = L'\}, \qquad K_2 = \{M \in C_2 : M\theta = M'\}.$$

Both are nonempty, since $L' \in C_1\theta$ and $M' \in C_2\theta$, and all literals of $K_1$ have the sign of $L'$. The substitution $\theta$ unifies the atoms of $K_1$. If $|K_1| \ge 2$, let $\mu_1$ be an mgu of $K_1$ as above, with all its variables in $\mathrm{Var}(C_1)$; if $|K_1| = 1$, let $\mu_1$ be the identity. Define $\mu_2$ from $K_2$ in the same way. Let $F_1 = C_1\mu_1$, $F_2 = C_2\mu_2$, and let $L_1$ and $M_2$ be the single literals $K_1\mu_1$ and $K_2\mu_2$. Then $F_1$ and $F_2$ are factors, and they have no common variable, since $\mathrm{Var}(F_i) \subseteq \mathrm{Var}(C_i)$.

*Step 1: $\theta$ factors through $\mu_1$ and $\mu_2$.* On $\mathrm{Var}(C_1)$, $\theta = \mu_1\theta$, and on $\mathrm{Var}(C_2)$, $\theta = \mu_2\theta$. So, with $\mu = \mu_1 \cup \mu_2$, which is a substitution because the domains are disjoint, $C_i\theta = C_i\mu\theta = F_i\theta$ for $i = 1, 2$. In particular $L_1\theta = L'$ and $M_2\theta = M'$.

*Step 2: the side literals.* We claim $(F_1 \setminus \{L_1\})\theta = C_1\theta \setminus \{L'\}$. Every literal of $F_1$ is $L\mu_1$ for some $L \in C_1$. If $L \in K_1$, then $L\mu_1 = L_1$. If $L \notin K_1$, then $L\mu_1\theta = L\theta \ne L'$, so $L\mu_1 \ne L_1$. Hence $F_1 \setminus \{L_1\} = \{L\mu_1 : L \in C_1 \setminus K_1\}$, and its image under $\theta$ is $\{L\theta : L \in C_1, L\theta \ne L'\} = C_1\theta \setminus \{L'\}$. The same holds for $F_2$, $M_2$ and $M'$.

*Step 3: the mgu.* The substitution $\theta\sigma'$ unifies $\mathrm{atom}(L_1)$ and $\mathrm{atom}(M_2)$, since $\mathrm{atom}(L_1)\theta\sigma' = \mathrm{atom}(L')\sigma' = \mathrm{atom}(M')\sigma' = \mathrm{atom}(M_2)\theta\sigma'$. So they have an mgu $\sigma$, and $\theta\sigma' = \sigma\lambda$ for some $\lambda$. The literals $L_1$ and $M_2$ have opposite signs, so

$$R = \big((F_1 \setminus \{L_1\}) \cup (F_2 \setminus \{M_2\})\big)\sigma$$

is a binary resolvent of $F_1$ and $F_2$.

*Step 4: $R\lambda = R'$.* By Step 3 and Step 2,

$$R\lambda = \big((F_1 \setminus \{L_1\}) \cup (F_2 \setminus \{M_2\})\big)\theta\sigma' = \big((C_1\theta \setminus \{L'\}) \cup (C_2\theta \setminus \{M'\})\big)\sigma' = R'. \qquad \square$$

**Factoring.** Let $F' = C\theta\tau'$, where $\tau'$ is an mgu of a set $J'$ of at least two literals of $C\theta$ with the same sign. Let $K = \{L \in C : L\theta \in J'\}$. Different literals of $J'$ have different preimages, so $|K| \ge |J'| \ge 2$, and $\theta\tau'$ unifies $K$, because it maps every element of $K$ to the single literal $J'\tau'$. Let $\mu$ be an mgu of $K$; then $F = C\mu$ is a factor of $C$, and $\theta\tau' = \mu\lambda$ for some $\lambda$. So $F\lambda = C\mu\lambda = C\theta\tau' = F'$. $\square$

**The corollary.** By induction on the derivation of $E'$. An input instance $C\theta$ lifts to $C$. A factor of a lifted clause $E_j' = E_j\lambda_j$ lifts by the factoring lemma, with one factoring step. A resolvent of $E_j' = E_j\lambda_j$ and $E_k' = E_k\lambda_k$ lifts by the resolution lemma, after renaming $E_k$ apart from $E_j$ and joining $\lambda_j$ and $\lambda_k$ into one $\theta$; it costs one resolution step and at most two factoring steps. If $E' = \square$, then $E\lambda = \square$ forces $E = \square$. $\square$

## Consequences

- **Completeness of resolution.** With [Herbrand's theorem](/herbrand-theorem/) and ground completeness, the lemma proves the [Robinson completeness theorem](/robinson-completeness-theorem/).
- **Only most general unifiers.** A prover never needs to try a less general unifier: the resolvent with the mgu covers all of them, by Step 3.
- **Lifting of refinements.** A refinement that is complete on ground clauses stays complete on first-order clauses when its restriction lifts. For [ordered resolution](/ordered-resolution/) the order must be stable under substitution: if $L\theta$ is maximal in $C\theta$, then $L$ is maximal in $C$, since $L \prec L_2$ in $C$ would give $L\theta \prec L_2\theta$. For [set of support](/set-of-support/), a lifted parent comes from the same input or derived clause, so the support condition lifts as well.
- **Example.** Let $C_1 = P(x) \vee P(f(y)) \vee Q(x)$, $C_2 = \lnot P(f(z)) \vee R(z)$ and $\theta = \{x \mapsto f(a), y \mapsto a, z \mapsto a\}$. Then $C_1\theta = P(f(a)) \vee Q(f(a))$, with two literals merged, and $C_2\theta = \lnot P(f(a)) \vee R(a)$, with the ground resolvent $R' = Q(f(a)) \vee R(a)$. The proof takes $K_1 = \{P(x), P(f(y))\}$, $\mu_1 = \{x \mapsto f(y)\}$ and $F_1 = P(f(y)) \vee Q(f(y))$. Resolving $F_1$ with $C_2$ by the mgu $\{z \mapsto y\}$ gives $R = Q(f(y)) \vee R(y)$, and $R' = R\{y \mapsto a\}$.

## Tightness

- **Factors are needed.** Take $C_1 = P(x) \vee P(y)$, $C_2 = \lnot P(u) \vee \lnot P(v)$ and $\theta$ sending all four variables to $a$. The instances are $P(a)$ and $\lnot P(a)$, with the resolvent $\square$. Every binary resolvent of $C_1$ and $C_2$ themselves has two literals, and no instance of a two-literal clause is $\square$. So the lemma is false with "$C_1$ and $C_2$" in place of "factors of $C_1$ and $C_2$".
- **Disjoint variables are needed.** For $C_1 = P(x)$ and $C_2 = \lnot P(f(x))$, the instances $P(f(a))$ and $\lnot P(f(a))$, with $x \mapsto f(a)$ in the first and $x \mapsto a$ in the second, resolve to $\square$. No single $\theta$ gives both, and the clauses without renaming have no resolvent. After renaming the second to $\lnot P(f(x'))$ the lemma applies.
- **The converse fails.** Not every resolvent $R$ of the general clauses has a resolvent of the given instances among its instances: an instance may make the two atoms differ. The lemma only says that the general level loses nothing.
- **Restrictions that do not lift.** If a strategy allows a step on an instance but forbids it on the general clause, the lemma gives no lifted step. For example, an order on literals that is not stable under substitution can make $L\theta$ maximal in $C\theta$ while $L$ is not maximal in $C$; completeness proofs for ordered calculi need stability for this reason.

## History

The lifting argument is the heart of Robinson's 1965 completeness proof: he showed that resolution with most general unifiers on general clauses does at least what resolution does on ground instances. Chang and Lee's textbook states it as a separate lemma in Chapter 5 and uses it to lift the semantic-tree proof of ground completeness. Later completeness proofs for ordered resolution, [hyperresolution](/hyperresolution/) and [superposition](/superposition/), such as those of Bachmair and Ganzinger, first prove completeness for ground clauses and then lift it with variants of this lemma.

## References
