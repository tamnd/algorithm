---
title: Existence and uniqueness up to renaming of most general unifiers
proves: [statement]
status: full
---

We use the notation of the page. $E$ is a finite set of equations $s \doteq t$ between terms of $T(\Sigma, V)$, $\mathrm{Var}(E)$ is the set of its variables, $|t|$ is the number of symbol occurrences of $t$, and $\|E\| = \sum_{(s \doteq t) \in E} (|s| + |t|)$. Substitutions are applied in postfix form, $\sigma\theta$ means "first $\sigma$, then $\theta$", and $\mathcal{U}(E)$ is the set of unifiers of $E$.

## Two facts about substitutions

**Fact 1 (size).** For each term $u$ and substitution $\lambda$, $|u\lambda| \ge |u|$. Equality holds if and only if $y\lambda$ is a variable for each $y \in \mathrm{Var}(u)$.

*Proof.* $|u\lambda| = |u| + \sum_{p} (|y_p\lambda| - 1)$, where the sum runs over the variable positions $p$ of $u$ and $y_p$ is the variable at $p$. Each summand is at least $0$, and it is $0$ exactly when $y_p\lambda$ is a variable. $\square$

**Fact 2 (occurs).** If $x \in \mathrm{Var}(t)$ and $t \ne x$, then $x \doteq t$ has no unifier.

*Proof.* Then $t$ is not a variable, so $x$ occurs in $t$ at a position of depth at least $1$. For each $\theta$, $t\theta$ contains $x\theta$ as a proper subterm, so $|t\theta| > |x\theta|$ and $x\theta \ne t\theta$. $\square$

## Part (a): existence of an idempotent mgu

We prove the following claim by induction on the pair $(|\mathrm{Var}(E)|, \|E\|)$ in the lexicographic order, which is well-founded on pairs of natural numbers.

**Claim.** Either $\mathcal{U}(E) = \emptyset$, or there is a $\sigma \in \mathcal{U}(E)$ such that

1. $\theta = \sigma\theta$ for each $\theta \in \mathcal{U}(E)$,
2. $\sigma\sigma = \sigma$, and
3. $\mathrm{dom}(\sigma) \cup \mathrm{vran}(\sigma) \subseteq \mathrm{Var}(E)$.

Property 1 gives $\sigma \le \theta$ (take $\lambda = \theta$), so such a $\sigma$ is an idempotent mgu.

**Case 0: $E = \emptyset$.** Each substitution unifies $E$. Take $\sigma = \varepsilon$. Then $\theta = \varepsilon\theta$, $\varepsilon\varepsilon = \varepsilon$, and the domain is empty.

Otherwise pick an equation $e \in E$ and let $E' = E \setminus \{e\}$. Each equation is in exactly one of the cases below.

**Case 1: $e$ is $x \doteq x$ for a variable $x$.** Each substitution unifies $e$, so $\mathcal{U}(E) = \mathcal{U}(E')$. Here $\mathrm{Var}(E') \subseteq \mathrm{Var}(E)$ and $\|E'\| < \|E\|$, so the induction hypothesis applies to $E'$. Its answer is an answer for $E$, and property 3 holds because $\mathrm{Var}(E') \subseteq \mathrm{Var}(E)$.

**Case 2: $e$ is $f(s_1, \ldots, s_k) \doteq f(t_1, \ldots, t_k)$ with the same symbol $f$ ($k \ge 0$).** By the homomorphic rule, $f(s_1, \ldots, s_k)\theta = f(t_1, \ldots, t_k)\theta$ if and only if $s_i\theta = t_i\theta$ for each $i$. So $E_2 = E' \cup \{s_1 \doteq t_1, \ldots, s_k \doteq t_k\}$ has $\mathcal{U}(E_2) = \mathcal{U}(E)$, $\mathrm{Var}(E_2) = \mathrm{Var}(E)$ and $\|E_2\| = \|E\| - 2$. The induction hypothesis for $E_2$ gives the answer for $E$.

**Case 3: $e$ is $f(\ldots) \doteq g(\ldots)$ with $f \ne g$.** For each $\theta$, the two sides of $e\theta$ have the roots $f$ and $g$, so $\mathcal{U}(E) = \emptyset$.

**Case 4: $e$ is $x \doteq t$ or $t \doteq x$, with $x$ a variable and $t \ne x$.** Both forms have the same unifiers, so we treat them together.

*Case 4a: $x \in \mathrm{Var}(t)$.* By Fact 2, $e$ has no unifier, so $\mathcal{U}(E) = \emptyset$.

*Case 4b: $x \notin \mathrm{Var}(t)$.* Let $\tau = \{x \mapsto t\}$ and $E'' = E'\tau = \{u\tau \doteq v\tau : (u \doteq v) \in E'\}$.

Each variable of $E''$ is a variable of $E'$ other than $x$, or a variable of $t$. So $\mathrm{Var}(E'') \subseteq \mathrm{Var}(E) \setminus \{x\}$, and since $x \in \mathrm{Var}(E)$, $|\mathrm{Var}(E'')| < |\mathrm{Var}(E)|$. The induction hypothesis applies to $E''$.

*Step 1: each $\theta \in \mathcal{U}(E)$ satisfies $\theta = \tau\theta$ and $\theta \in \mathcal{U}(E'')$.* Since $\theta$ unifies $e$, $x\tau\theta = t\theta = x\theta$, and for $y \ne x$, $y\tau\theta = y\theta$. So $\tau\theta = \theta$. For $(u \doteq v) \in E'$, $(u\tau)\theta = u\theta = v\theta = (v\tau)\theta$.

*Step 2: if $\mathcal{U}(E'') = \emptyset$, then $\mathcal{U}(E) = \emptyset$.* This is the contrapositive of Step 1.

*Step 3: otherwise let $\mu$ be the substitution that the induction hypothesis gives for $E''$, and let $\sigma = \tau\mu$.* Note that $x \notin \mathrm{dom}(\mu) \cup \mathrm{vran}(\mu)$, because both sets are inside $\mathrm{Var}(E'')$, which does not contain $x$. So $\mu$ maps $x$ to $x$, and no term $w\mu$ contains $x$ unless $w$ does.

- *$\sigma$ unifies $E$.* $x\sigma = t\mu$, and $t\sigma = (t\tau)\mu = t\mu$ because $x \notin \mathrm{Var}(t)$. For $(u \doteq v) \in E'$, $u\sigma = (u\tau)\mu = (v\tau)\mu = v\sigma$, because $\mu$ unifies $E''$.
- *Property 1.* Let $\theta \in \mathcal{U}(E)$. By Step 1, $\theta = \tau\theta$ and $\theta \in \mathcal{U}(E'')$. By property 1 for $\mu$, $\theta = \mu\theta$. So $\sigma\theta = \tau\mu\theta = \tau\theta = \theta$.
- *Property 2.* For a variable $y \ne x$: $y\tau = y$, and $y\mu$ does not contain $x$, so $y\sigma\sigma = (y\mu)\tau\mu = (y\mu)\mu = y\mu = y\sigma$, using $\mu\mu = \mu$. For $x$: $t$ does not contain $x$, so $t\mu$ does not contain $x$, and $x\sigma\sigma = (t\mu)\tau\mu = (t\mu)\mu = t\mu = x\sigma$.
- *Property 3.* $\mathrm{dom}(\sigma) \subseteq \{x\} \cup \mathrm{dom}(\mu) \subseteq \mathrm{Var}(E)$. For $y \in \mathrm{dom}(\sigma)$, the variables of $y\sigma$ are in $\mathrm{Var}(t\mu)$ or $\mathrm{Var}(y\mu)$, and both are inside $\mathrm{Var}(t) \cup \mathrm{Var}(E'') \cup \{y\} \subseteq \mathrm{Var}(E)$.

**The cases are exhaustive.** If neither side of $e$ is a variable, Case 2 or Case 3 applies. If a side is a variable $x$, Case 1 applies when both sides are $x$, and Case 4 applies otherwise. This completes the induction and proves (a). $\square$

The induction is a recursive procedure: it decides unifiability and computes $\sigma$. Cases 1 to 4 are the delete, decompose, clash, occurs-check and eliminate rules of the [Martelli-Montanari algorithm](/martelli-montanari-unification/).

## Part (b): uniqueness up to renaming

Let $X = \mathrm{Var}(E)$, and let $\sigma$ and $\sigma'$ be mgus of $E$. Then $\sigma \le \sigma'$ and $\sigma' \le \sigma$, so there are $\lambda$ and $\lambda'$ with

$$x\sigma' = x\sigma\lambda \quad \text{and} \quad x\sigma = x\sigma'\lambda' \qquad \text{for each } x \in X.$$

(These equations are all that the proof uses, so it also holds for the weaker order $\le_X$ that compares substitutions on $X$ only.)

Then $x\sigma = x\sigma\lambda\lambda'$ for each $x \in X$. Let $Y = \bigcup_{x \in X} \mathrm{Var}(x\sigma)$, a finite set.

*$\lambda\lambda'$ is the identity on $Y$.* Fix $x \in X$ and let $u = x\sigma$. Since $u\lambda\lambda' = u$, Fact 1 says that $\lambda\lambda'$ maps each variable of $u$ to a variable. So $u\lambda\lambda'$ is $u$ with each variable $y$ replaced by the variable $y\lambda\lambda'$ at the same positions. As the result is $u$, $y\lambda\lambda' = y$ for each $y \in \mathrm{Var}(u)$.

*$\lambda$ maps $Y$ injectively to variables.* For $y \in Y$, $y\lambda\lambda' = y$ is a variable, so $y\lambda$ is a variable: if $y\lambda$ were not a variable, then $y\lambda\lambda'$ would not be one either. If $y_1\lambda = y_2\lambda$, then $y_1 = y_1\lambda\lambda' = y_2\lambda\lambda' = y_2$.

*Extend to a renaming.* Let $Y' = \{y\lambda : y \in Y\}$. Then $|Y'| = |Y|$, so $|Y' \setminus Y| = |Y| - |Y \cap Y'| = |Y \setminus Y'|$. Define $\rho$ by $y\rho = y\lambda$ for $y \in Y$, by any bijection from $Y' \setminus Y$ onto $Y \setminus Y'$ on $Y' \setminus Y$, and by $z\rho = z$ for $z \notin Y \cup Y'$. Then $\rho$ maps $Y$ onto $Y'$ and $Y' \setminus Y$ onto $Y \setminus Y'$, so it is a bijection of $Y \cup Y'$ and of $V$, and it moves only finitely many variables. So $\rho$ is a renaming.

*Conclusion.* For $x \in X$, all variables of $x\sigma$ are in $Y$, where $\rho$ and $\lambda$ agree. So $x\sigma' = x\sigma\lambda = x\sigma\rho$. $\square$

Conversely, if $\sigma$ is an mgu and $\rho$ is a renaming, then $\sigma\rho$ unifies $E$, and $\sigma = (\sigma\rho)\rho^{-1}$ gives $\sigma\rho \le \sigma \le \theta$ for each unifier $\theta$. So $\sigma\rho$ is also an mgu, and the renaming in (b) cannot be removed. $\blacksquare$
