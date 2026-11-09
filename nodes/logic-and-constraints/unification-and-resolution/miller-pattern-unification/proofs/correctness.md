---
title: Pattern unification returns a most general unifier or fails correctly
proves: [correctness]
status: full
---

All terms are simply typed, $\beta$-normal and $\eta$-long. A substitution maps free variables to terms of the same type that have no free bound variables, and $\delta(t)$ is the normal form of the instance. Two normal η-long terms are equal up to $\beta\eta$ exactly when they are equal up to α. We write $\delta' \circ \rho$ for "first $\rho$, then $\delta'$". $V_0$ is the set of free variables of the input $E_0$. A *renaming* is a map from bound variables to bound variables that is one to one.

**Lemma 1 (rigid heads stay).** If $h$ is a constant or a bound variable, then $\delta(\lambda \bar x.\, h(t_1, \ldots, t_m)) = \lambda \bar x.\, h(\delta(t_1), \ldots, \delta(t_m))$. So $\delta$ unifies $\lambda \bar x.\, a(\bar s) \doteq \lambda \bar x.\, b(\bar t)$ if and only if $a = b$ and $\delta$ unifies each $\lambda \bar x.\, s_i \doteq \lambda \bar x.\, t_i$.

*Proof.* A substitution does not touch $h$, and normalization works inside the arguments only. $\square$

**Lemma 2 (application to distinct variables).** Let $r$ be a normal term whose free bound variables are among $w_1, \ldots, w_n$, and let $y_1, \ldots, y_n$ be distinct bound variables that are not bound inside $r$. Then $(\lambda \bar w.\, r)(\bar y)$ normalizes to $r[\bar y / \bar w]$, which is $r$ with the names changed by a renaming. In particular it has the same shape and size as $r$, and it contains $y_i$ free exactly when $r$ contains $w_i$ free.

*Proof.* Substituting a variable (in η-long form) for a variable creates no new redex in a normal η-long term: an η-long variable $\lambda \bar z.\, y(\bar z)$ applied to arguments $\bar u$ reduces to $y(\bar u)$. So the result is $r$ with each $w_i$ replaced by $y_i$. The $y_i$ are distinct, so the map is one to one. $\square$

**Lemma 3 (closure).** If $\rho$ is a binding made in lines L5, L7, L11 or L17, and $t$ is a pattern, then $\rho(t)$ is a pattern.

*Proof.* In lines L5, L7 and L17 the value is $\lambda \bar w.\, H(\bar u)$ with $\bar u$ a sub-list of the distinct $\bar w$. An instance of $F(\bar y)$ becomes $H$ applied to a sub-list of $\bar y$, which is a list of distinct bound variables. In line L11 the value is $\lambda \bar y.\, t$ with $t$ a pattern. By Lemma 2, an instance $F(\bar z)$ becomes a renaming of $t$, and a renaming maps distinct bound variables to distinct bound variables. $\square$

So each pair the algorithm sees is a pair of patterns. We now show that each step is most general. Let $p$ be the pair of line L3, after $\theta$, under the binders $\bar x$.

**Lemma 4 (flex-flex, same head).** Let $p$ be $F(\bar y) \doteq F(\bar z)$ and $\rho = \{F \mapsto \lambda \bar w.\, H(w_i : y_i = z_i)\}$. Then $\rho$ unifies $p$, and each unifier $\delta$ of $p$ equals $\delta' \circ \rho$ on all variables but $H$, for some $\delta'$.

*Proof.* Both sides of $\rho(p)$ are $H(y_i : y_i = z_i)$. Let $\delta(F) = \lambda \bar w.\, r$. By Lemma 2, $\delta$ unifies $p$ if and only if $r[\bar y / \bar w] = r[\bar z / \bar w]$. Both are renamings of $r$, so they are equal exactly when each free occurrence of a $w_i$ in $r$ gets the same name on both sides, that is, when $r$ has no free $w_i$ with $y_i \ne z_i$. Let $\bar u$ list the $w_i$ with $y_i = z_i$, and set $\delta'(H) = \lambda \bar u.\, r$ and $\delta' = \delta$ on all other variables. Then $\delta'(\rho(F)) = \lambda \bar w.\, r = \delta(F)$. $\square$

**Lemma 5 (flex-flex, different heads).** Let $p$ be $F(\bar y) \doteq G(\bar z)$ with $F \ne G$, let $\bar v$ list the variables in both $\bar y$ and $\bar z$, and let $\rho = \{F \mapsto \lambda \bar y.\, H(\bar v), G \mapsto \lambda \bar z.\, H(\bar v)\}$. Then $\rho$ unifies $p$, and each unifier $\delta$ of $p$ equals $\delta' \circ \rho$ on all variables but $H$.

*Proof.* Both sides of $\rho(p)$ are $H(\bar v)$. Let $\delta$ unify $p$ and let $m$ be the common normal form of both sides. By Lemma 2, the free bound variables of $m$ are in $\bar y$ (left side) and in $\bar z$ (right side), so they are in $\bar v$. Set $\delta'(H) = \lambda \bar v.\, m$. Then $\delta'(\rho(F)) = \lambda \bar y.\, m$. Since $\delta(F)$ applied to $\bar y$ is $m$, Lemma 2 gives $\delta(F) = \lambda \bar y.\, m$ up to α. The same holds for $G$. $\square$

**Lemma 6 (occurs check).** Let $p$ be $F(\bar y) \doteq t$ with $t$ rigid, and let $F$ occur in $t$. Then $p$ has no unifier.

*Proof.* In a pattern, a free variable has only bound variables as arguments. So the occurrence $F(\bar z)$ in $t$ lies under rigid heads only. By Lemma 1, $\delta(t)$ keeps these heads and contains $\delta(F(\bar z))$ as a proper subterm, up to binders. By Lemma 2, $\delta(F(\bar y))$ and $\delta(F(\bar z))$ are renamings of the same term, so they have the same size. Hence $\delta(t)$ is strictly larger than $\delta(F(\bar y))$, and they are not equal. $\square$

**Lemma 7 (pruning and flex-rigid).** Let $p$ be $F(\bar y) \doteq t$, with $t$ rigid and $F$ not in $t$. If PRUNE$(t, \bar y)$ fails, $p$ has no unifier. Otherwise let $\rho$ be all bindings of lines L17 and L11 in this step. Then $\rho$ unifies $p$, and each unifier $\delta$ of $p$ equals $\delta' \circ \rho$ on all variables but the new ones.

*Proof.* Let $\delta$ unify $p$. By Lemma 2, $\delta(F(\bar y))$ has no free bound variable outside $\bar y$, so neither has $\delta(t)$.

Line L19: PRUNE fails at a rigid bound variable $b$ that is not in $\bar y$ and not bound inside $t$. All heads above it are rigid, so by Lemma 1, $b$ occurs free in $\delta(t)$, which is a contradiction. So no unifier exists.

Line L17: take an occurrence $G(\bar w)$ in $t$ under the local binders $\bar z$, and let $\delta(G) = \lambda \bar w'.\, r$. All heads above it are rigid, so by Lemmas 1 and 2 a renaming of $r$ is a subterm of $\delta(t)$, where $w'_i$ becomes $w_i$. If $r$ had a free $w'_i$ with $w_i \notin \bar y \cup \bar z$, then $\delta(t)$ would have the free variable $w_i$, which is not in $\bar y$. So $r$ uses only the places in $\bar u$, and as in Lemma 4, $\delta(G) = \delta'(\lambda \bar w.\, H(\bar u))$ with $\delta'(H) = \lambda \bar u.\, r$.

Line L11: let $t'$ be the result of PRUNE, so $\delta(t) = \delta'(t')$ by the previous step. By Lemma 2 the term $\delta(F)$ applied to $\bar y$ is a renaming of its body, and it equals $\delta(t)$. So $\delta(F) = \lambda \bar y.\, \delta(t) = \delta'(\lambda \bar y.\, t')$. This shows $\delta = \delta' \circ \rho$. Finally $\rho(F(\bar y)) = t'[\bar y/\bar y] = t' = \rho(t)$, since $F$ does not occur in $t'$, so $\rho$ unifies $p$. $\square$

**Invariant.** Let $E$ be the pairs that are left and $\theta$ the current substitution. Then:

> **(S)** For each substitution $\sigma$ that unifies $\theta(E)$, the substitution $\sigma \circ \theta$ unifies $E_0$.
>
> **(C)** For each unifier $\delta$ of $E_0$ there is a $\delta_1$ that unifies $\theta(E)$, with $\delta = \delta_1 \circ \theta$ on $V_0$.

Both hold at the start, with $\theta$ the identity. A rigid-rigid step keeps both by Lemma 1. Consider a step that makes the bindings $\rho$ for the pair $p$, so that $E$ becomes $E' = E \setminus \{p\}$ and $\theta$ becomes $\rho \circ \theta$.

For (S): let $\sigma$ unify $\rho(\theta(E'))$. Then $\sigma \circ \rho$ unifies $\theta(E')$, and it unifies $p$ because $\rho$ does. So $\sigma \circ \rho$ unifies $\theta(E)$, and by the old (S), $\sigma \circ \rho \circ \theta$ unifies $E_0$.

For (C): let $\delta$ unify $E_0$, and take $\delta_1$ from the old (C). Since $\delta_1$ unifies $p$, Lemmas 4, 5 and 7 give $\delta_1 = \delta_2 \circ \rho$ on all old variables. So $\delta_2$ unifies $\rho(\theta(E'))$, and $\delta = \delta_1 \circ \theta = \delta_2 \circ \rho \circ \theta$ on $V_0$.

**Termination.** Let $N$ be the number of free variables that occur in $\theta(E)$ and let $S$ be the total size of $\theta(E)$. A rigid-rigid step keeps $N$ and lowers $S$. A flex-flex step with different heads replaces two variables by one. A flex-rigid step removes $F$ for good, because $F$ is not in the value $\lambda \bar y.\, t'$, and each prune replaces one variable by one new variable. A flex-flex step with the same head keeps $N$, removes the pair, and makes no other term larger, because $H$ takes fewer arguments than $F$. So $(N, S)$ goes down in the lexicographic order at each step.

**Theorem.** PATTERN-UNIFY$(E_0)$ stops. If it returns $\theta$, then $\theta$ is a most general unifier of $E_0$. If it fails, $E_0$ has no unifier.

*Proof.* At the end $E$ is empty. (S) with $\sigma$ the identity shows that $\theta$ unifies $E_0$. (C) shows that each unifier $\delta$ is $\delta_1 \circ \theta$ on $V_0$. If the algorithm fails at a pair $p$, then $p$ has no unifier by Lemma 1, Lemma 6 or Lemma 7. A unifier $\delta$ of $E_0$ would give, by (C), a $\delta_1$ that unifies $\theta(E)$, and so $p$. Hence $E_0$ has no unifier. $\blacksquare$

The tests check this theorem against brute force: for each small problem they list all closed terms up to three head symbols for each variable, keep the ground unifiers, and check that the algorithm finds a unifier exactly when one exists and that each ground unifier is an instance of the result.
