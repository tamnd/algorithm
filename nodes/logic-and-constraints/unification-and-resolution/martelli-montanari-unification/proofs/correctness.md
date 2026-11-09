---
title: The Martelli-Montanari rules terminate and give an idempotent most general unifier or a correct failure
proves: [correctness]
status: full
---

We use the notation of the page. $E_0$ is the input set of equations, $P$ is the set of unsolved equations and $S$ is the solved substitution. $\mathcal{U}(P)$ is the set of unifiers of $P$, $\mathrm{Var}(P)$ is the set of variables of $P$, and $\|P\|$ is the total number of symbol occurrences in $P$. A pass of the loop is one execution of lines L3 to L9.

## Invariants

We show that, at the start of each pass:

- **(J1)** For every substitution $\theta$: $\theta \in \mathcal{U}(E_0)$ if and only if $\theta = S\theta$ and $\theta \in \mathcal{U}(P)$.
- **(J2)** $S$ is idempotent, $\mathrm{dom}(S) \cap \mathrm{Var}(P) = \emptyset$, and $\mathrm{dom}(S) \cup \mathrm{vran}(S) \subseteq \mathrm{Var}(E_0)$.

At the start, $S = \varepsilon$ and $P = E_0$, and both hold, since $\theta = \varepsilon\theta$ for each $\theta$.

Let the pass remove the equation $e = (s \doteq t)$, and let $P' = P \setminus \{e\}$, so $\mathcal{U}(P) = \mathcal{U}(P') \cap \mathcal{U}(\{e\})$.

**Delete (L4), $s = t$.** Each $\theta$ unifies $e$, so $\mathcal{U}(P') = \mathcal{U}(P)$. $S$ does not change, and $\mathrm{Var}(P') \subseteq \mathrm{Var}(P)$. Both invariants hold.

**Clash (L5).** $s$ and $t$ are not variables and have different roots or arities. For each $\theta$, $s\theta$ and $t\theta$ have these roots, so $\mathcal{U}(\{e\}) = \emptyset$ and $\mathcal{U}(P) = \emptyset$. By (J1), $\mathcal{U}(E_0) = \emptyset$, and FAIL is correct.

**Decompose (L6), $s = f(s_1, \ldots, s_k)$ and $t = f(t_1, \ldots, t_k)$.** By the homomorphic rule, $\theta$ unifies $e$ if and only if it unifies each $s_i \doteq t_i$. So the new $P$ has the same unifiers and the same variables. Both invariants hold.

**Orient (L7).** Swapping the sides of $e$ changes nothing. After L7, $s$ is a variable $x$ and $t \ne x$.

**Occurs check (L8), $x \in \mathrm{Var}(t)$.** Then $t$ is not a variable and contains $x$ as a proper subterm. For each $\theta$, $|t\theta| > |x\theta|$, so $\mathcal{U}(\{e\}) = \emptyset$, $\mathcal{U}(P) = \emptyset$, and by (J1) $\mathcal{U}(E_0) = \emptyset$. FAIL is correct.

**Eliminate (L9), $x \notin \mathrm{Var}(t)$.** Let $\tau = \{x \mapsto t\}$. The new values are $P_1 = P'\tau$ and $S_1 = S\tau$. By (J2), $x \notin \mathrm{dom}(S)$ and $\mathrm{Var}(t) \cap \mathrm{dom}(S) = \emptyset$, since $x$ and $\mathrm{Var}(t)$ lie in $\mathrm{Var}(P)$.

*(J1) for the new values.* We show that $\theta = S\theta \wedge \theta \in \mathcal{U}(P)$ holds if and only if $\theta = S_1\theta \wedge \theta \in \mathcal{U}(P_1)$.

- Suppose $\theta = S\theta$ and $\theta \in \mathcal{U}(P)$. Then $x\theta = t\theta$, so $\tau\theta = \theta$: both map $x$ to $t\theta = x\theta$ and agree elsewhere. So $S_1\theta = S\tau\theta = S\theta = \theta$. For $(u \doteq v) \in P'$, $(u\tau)\theta = u\theta = v\theta = (v\tau)\theta$, so $\theta \in \mathcal{U}(P_1)$.
- Suppose $\theta = S_1\theta$ and $\theta \in \mathcal{U}(P_1)$. Since $x \notin \mathrm{dom}(S)$, $xS_1 = x\tau = t$, so $x\theta = xS_1\theta = t\theta$. Then $\tau\theta = \theta$ as above, and $S\theta = S\tau\theta = S_1\theta = \theta$. For $(u \doteq v) \in P'$, $u\theta = u\tau\theta = v\tau\theta = v\theta$. With $x\theta = t\theta$, this gives $\theta \in \mathcal{U}(P)$.

With (J1) for the old values, (J1) holds for the new values.

*(J2) for the new values.* $\mathrm{dom}(S_1) = \mathrm{dom}(S) \cup \{x\}$: $xS_1 = t \ne x$, and for $y \in \mathrm{dom}(S)$ the variables of $(yS)\tau$ lie in $\mathrm{vran}(S) \cup \mathrm{Var}(t)$, which is disjoint from $\mathrm{dom}(S)$, so $(yS)\tau \ne y$. Also $\mathrm{vran}(S_1) \subseteq (\mathrm{vran}(S) \setminus \{x\}) \cup \mathrm{Var}(t)$. Each part of $\mathrm{vran}(S_1)$ is disjoint from each part of $\mathrm{dom}(S_1)$: $\mathrm{vran}(S) \cap \mathrm{dom}(S) = \emptyset$ by (J2), $\mathrm{Var}(t) \cap \mathrm{dom}(S) = \emptyset$, and $x \notin \mathrm{Var}(t)$. A substitution whose domain and variable range are disjoint is idempotent, because each $y\sigma$ then contains only variables that $\sigma$ fixes. The variables of $P_1 = P'\tau$ are those of $P'$ other than $x$, together with those of $t$, so $\mathrm{Var}(P_1) \subseteq \mathrm{Var}(P) \setminus \{x\}$, which is disjoint from $\mathrm{dom}(S) \cup \{x\}$. Finally, $x$ and $\mathrm{Var}(t)$ are in $\mathrm{Var}(P)$, and by induction $\mathrm{Var}(P) \subseteq \mathrm{Var}(E_0)$, so $\mathrm{dom}(S_1) \cup \mathrm{vran}(S_1) \subseteq \mathrm{Var}(E_0)$.

## Termination

Use the measure $(|\mathrm{Var}(P)|, \|P\|)$, ordered lexicographically. It is a pair of natural numbers, so it cannot decrease forever.

- Delete: $\mathrm{Var}(P)$ does not grow, and $\|P\|$ drops by $|s| + |t| \ge 2$.
- Decompose: $\mathrm{Var}(P)$ stays the same, and $\|P\|$ drops by 2, the two occurrences of $f$.
- Orient is always followed in the same pass by the occurs check or by eliminate, so it is not a pass of its own.
- Eliminate: $x \in \mathrm{Var}(P)$ and $\mathrm{Var}(P_1) \subseteq \mathrm{Var}(P) \setminus \{x\}$, so $|\mathrm{Var}(P)|$ drops by at least 1.
- Clash and the occurs check stop the algorithm.

So each pass that does not stop decreases the measure, and the loop ends. The number of eliminate passes is at most $|\mathrm{Var}(E_0)|$.

## Result

If the algorithm returns FAIL, at L5 or L8, then $\mathcal{U}(E_0) = \emptyset$, as shown above.

If it returns $S$ at L10, then $P = \emptyset$ and $\mathcal{U}(P)$ holds every substitution, so (J1) reads: $\theta \in \mathcal{U}(E_0)$ if and only if $\theta = S\theta$. By (J2), $S = SS$, so $S \in \mathcal{U}(E_0)$. Each $\theta \in \mathcal{U}(E_0)$ has $\theta = S\theta$, so $S \le \theta$. So $S$ is an idempotent most general unifier of $E_0$, with $\mathrm{dom}(S) \cup \mathrm{vran}(S) \subseteq \mathrm{Var}(E_0)$.

The proof does not use the order in which line L3 removes equations, so every order of rule applications gives a correct result. $\blacksquare$
