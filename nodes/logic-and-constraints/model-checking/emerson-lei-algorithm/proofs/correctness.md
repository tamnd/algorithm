---
title: The Emerson-Lei algorithm computes the meaning of the formula within the stated number of evaluations
proves: [correctness]
status: full
---

Let $M = (S, I, R, L)$ be a finite Kripke structure with $n = |S|$, and let $\varphi$ be a closed formula in positive normal form in which each variable is bound once. For a bound variable $X$, let $\sigma_X X.\, \alpha_X$ be its fixed-point subformula. The variables *around* $X$ are those whose fixed-point subformula contains $\sigma_X X.\, \alpha_X$ as a proper subformula; since $\varphi$ is closed and each variable is bound once, every free variable of $\sigma_X X.\, \alpha_X$ is around $X$. A variable is *inside* $X$ if it is bound in $\alpha_X$. The *opposite* variables of $X$ are the variables inside $X$ whose sign differs from $\sigma_X$.

For the current values $V$, write $f_X(T) = [\![\alpha_X]\!]_{V[X \mapsto T]}$. This function depends only on the values of the variables around $X$. In positive normal form, $[\![\alpha]\!]_\rho$ is monotone in each $\rho(Z)$, so $f_X$ is monotone, and $f_X$ grows (pointwise) when the values of the variables around $X$ grow.

**Definition.** $V$ is *sound for $X$* if

- $\sigma_X = \mu$: $V[X] \subseteq f_X(V[X])$ and $V[X] \subseteq \mu f_X$;
- $\sigma_X = \nu$: $f_X(V[X]) \subseteq V[X]$ and $\nu f_X \subseteq V[X]$.

$V$ is *sound* if it is sound for every bound variable. We treat lines L10 to L12 as one *step*.

**Lemma 1 (start values).** If $V[X] = \mathrm{START}(X)$, then $V$ is sound for $X$, whatever the other values are.

*Proof.* For $\mu$, $\emptyset$ is below every set. For $\nu$, $S$ is above every set. $\square$

**Lemma 2 (moves in the right direction).** Let $V$ be sound for $X$, and let $V'$ agree with $V$ on $X$ and on the variables inside $X$. If $\sigma_X = \mu$ and $V'[W] \supseteq V[W]$ for each variable $W$ around $X$, then $V'$ is sound for $X$. Dually, if $\sigma_X = \nu$ and $V'[W] \subseteq V[W]$ for each $W$ around $X$, then $V'$ is sound for $X$.

*Proof.* Let $f$ and $f'$ be $f_X$ under $V$ and $V'$; then $f(T) \subseteq f'(T)$ for every $T$. With $v = V[X]$: $v \subseteq f(v) \subseteq f'(v)$. Also $f(\mu f') \subseteq f'(\mu f') = \mu f'$, so $\mu f'$ is a pre-fixed point of $f$, and $\mu f \subseteq \mu f'$ by the [Knaster-Tarski theorem](/knaster-tarski-theorem/). Hence $v \subseteq \mu f \subseteq \mu f'$. The $\nu$ case is the dual. $\square$

**Lemma 3 (a step keeps soundness).** Suppose $V$ is sound, the loop of $X$ is running, and line L8 has just computed $N = f_X(V[X])$ with $N \ne V[X]$. After lines L10 to L12, the values are sound again. Moreover, if $\sigma_X = \mu$, then every value that the step changes grows, and if $\sigma_X = \nu$, every value that it changes shrinks.

*Proof.* Take $\sigma_X = \mu$; the other case is dual. Let $v = V[X]$. By soundness $v \subseteq f_X(v) = N$, so $X$ grows. The step changes $X$ and resets the opposite variables of $X$, which are $\nu$ variables, to $S$; so every change is growth. The step does not change any variable around $X$, so $f_X$ is the same function before and after. Now check each variable $Y$.

- $Y = X$. The new value is $N = f_X(v)$. From $v \subseteq N$ and monotonicity, $N = f_X(v) \subseteq f_X(N)$. From $v \subseteq \mu f_X$, $N = f_X(v) \subseteq f_X(\mu f_X) = \mu f_X$.
- $Y$ not inside $X$ and $Y \ne X$. Then $X$ and the variables inside $X$ are not around $Y$: if $X$ were around $Y$, then $Y$ would be inside $X$. So $f_Y$ and $V[Y]$ are unchanged.
- $Y$ inside $X$ with $\sigma_Y = \nu$. Then $Y$ is reset, and Lemma 1 applies.
- $Y$ inside $X$ with $\sigma_Y = \mu$. $V[Y]$ is unchanged, and so are the values of the variables inside $Y$, since those are inside $X$ and are either unchanged or reset; but a reset variable inside $Y$ is not around $Y$ and so does not matter for Lemma 2. The variables around $Y$ that change are $X$ and some reset $\nu$ variables, and all of them grow. By Lemma 2, $V$ stays sound for $Y$. $\square$

**Lemma 4 (evaluation).** Suppose $V$ is sound when EVAL$(\psi)$ is called, where $\psi$ is a subformula of $\varphi$. Then the call ends, it changes only variables bound in $\psi$, $V$ is sound after each step and at the end, and it returns $[\![\psi]\!]_V$.

*Proof.* By induction on $\psi$. Note first that the free variables of $\psi$ are bound outside $\psi$, so their values do not change during the call, and $[\![\psi]\!]_V$ is well defined throughout.

- Lines L2 and L3 return the definitions and change nothing.
- Line L4 calls EVAL$(\alpha)$ and then EVAL$(\beta)$. By induction the first call returns $[\![\alpha]\!]_V$ and changes only variables bound in $\alpha$. Since each variable is bound once, none of them is free in $\beta$, so the second call returns $[\![\beta]\!]_V$ for the same values of the free variables of $\beta$. Line L5 is the same with one call.
- Line L6, $\psi = \sigma X.\, \alpha$, with $\sigma = \mu$; the case $\nu$ is dual. At the start of each round of the loop, $V$ is sound, by the assumption for the first round and by Lemma 3 for the later ones. In a round, by induction, line L8 returns $N = [\![\alpha]\!]_V = f_X(V[X])$, since the free variables of $\alpha$ are $X$ and variables around $X$. If $N = V[X]$, then $V[X]$ is a fixed point of $f_X$ and $V[X] \subseteq \mu f_X$, so $V[X] = \mu f_X = [\![\psi]\!]_V$, and line L9 returns it. Otherwise $V[X] \subsetneq N$ by soundness, and line L10 makes $V[X]$ strictly larger. The variables around $X$ do not change during the call, so $f_X$ is one fixed function, and $V[X]$ stays below $\mu f_X$. A strictly growing chain of subsets of $S$ has at most $n$ steps, so the loop ends. The call changes only $X$ and variables inside $X$. $\square$

**Theorem.** EMERSON-LEI$(M, \varphi)$ returns $[\![\varphi]\!]$.

*Proof.* After line L13 all values are start values, which are sound by Lemma 1. By Lemma 4, line L14 returns $[\![\varphi]\!]_V$, and since $\varphi$ is closed this is $[\![\varphi]\!]$. $\square$

**Remark (plain nested iteration).** If each entry of a fixed point first sets $V[X] \leftarrow \mathrm{START}(X)$, then $V$ is sound for $X$ at the start of its loop by Lemma 1, and the same proof applies.

**Theorem (cost).** For a bound variable $X$, let $\ell(X)$ be the number of sign blocks on the chain of fixed points from the outermost one down to $X$, so $1 \le \ell(X) \le d$, and let $k_\ell$ be the number of variables with $\ell(X) = \ell$. Then line L8 runs at most $k \prod_{\ell=1}^{d} (1 + k_\ell n) \le k\,(1 + kn)^d$ times.

*Proof.* Let $C(X)$ be the number of times line L10 changes $V[X]$, $R(X)$ the number of times line L12 resets it, and $E(X)$ the number of times line L8 runs for $X$.

*Changes.* Between two resets of $X$, and before the first one, the value of $X$ changes only at line L10, and by the proof of Lemma 4 each such change is strict growth for $\mu$ and strict shrinking for $\nu$, starting from $\mathrm{START}(X)$. So there are at most $n$ changes in each such period, and $C(X) \le n\,(1 + R(X))$.

*Resets.* $X$ is reset exactly once for each change of a variable $W$ such that $X$ is an opposite variable of $W$. Such a $W$ is around $X$ and has the other sign, so between $W$ and $X$ the sign changes at least once, and $\ell(W) < \ell(X)$. With $T_\ell = \sum_{\ell(W) \le \ell} C(W)$ and $T_0 = 0$, this gives $R(X) \le T_{\ell(X) - 1}$.

*Summing.* For a variable with $\ell(X) = \ell$, $C(X) \le n\,(1 + T_{\ell - 1})$. So $T_\ell \le T_{\ell - 1} + k_\ell\, n\, (1 + T_{\ell - 1})$, that is, $1 + T_\ell \le (1 + T_{\ell - 1})(1 + k_\ell n)$. By induction, $1 + T_d \le \prod_{\ell=1}^{d} (1 + k_\ell n)$.

*Evaluations.* Each run of line L8 for $X$ either ends the loop at line L9, which happens once for each entry of $X$, or is followed by a change at line L10. The subformula $\sigma_X X.\, \alpha_X$ is evaluated once for each run of line L8 of the nearest fixed point $P$ around $X$, or once in all if there is none. So $E(X) \le E(P) + C(X)$, and by induction along the chain of fixed points from the outermost one down to $X$, $E(X) \le 1 + \sum_{W} C(W)$ over the variables $W$ on that chain. This is at most $1 + T_d$. Summing over the $k$ variables gives the bound. Finally, $\prod_\ell (1 + k_\ell n) \le (1 + kn)^d$ because each $k_\ell \le k$. $\square$

**Proposition (fair $\mathsf{EG}$).** Let $P \subseteq S$, let $J_1, \ldots, J_r \subseteq S$ with $r \ge 1$, and let $G$ be the set of states from which some path stays in $P$ forever and visits each $J_i$ infinitely often. For $B \subseteq S$, let $\mathsf{E}[P\,\mathsf{U}\,B]$ be the set of states with a finite path $t_0 \ldots t_j$, $j \ge 0$, such that $t_j \in B$ and $t_0, \ldots, t_{j-1} \in P$. Let

$$f(Z) = P \cap \bigcap_{i=1}^{r} \mathit{pre}_\exists\big(\mathsf{E}[P\,\mathsf{U}\,(Z \cap J_i)]\big).$$

Then $f$ is monotone and $\nu f = G$.

*Proof.* Monotonicity is clear, since $\mathsf{E}[P\,\mathsf{U}\,B]$ grows with $B$.

*$G \subseteq \nu f$.* By the Knaster-Tarski theorem it is enough to show $G \subseteq f(G)$. Let $s \in G$, with a path $\pi = s_0 s_1 s_2 \ldots$ from $s = s_0$ that stays in $P$ and visits each $J_i$ infinitely often. Every suffix of $\pi$ is such a path too, so every $s_j$ is in $G$. Now $s \in P$. For each $i$, choose $j \ge 1$ with $s_j \in J_i$. Then $s_1 \ldots s_j$ is a path with $s_1, \ldots, s_{j-1} \in P$ and $s_j \in G \cap J_i$, so $s_1 \in \mathsf{E}[P\,\mathsf{U}\,(G \cap J_i)]$, and $s \in \mathit{pre}_\exists$ of this set. So $s \in f(G)$.

*$\nu f \subseteq G$.* Let $Z = \nu f$, so $Z = f(Z) \subseteq P$. Let $z_0 \in Z$. Since $z_0 \in f(Z)$, there is a path of at least one step from $z_0$ to a state $z_1 \in Z \cap J_1$, whose states before $z_1$ are in $P$. Since $z_1 \in Z$, there is in the same way a path of at least one step from $z_1$ to $z_2 \in Z \cap J_2$, and so on, with the index running through $1, 2, \ldots, r, 1, 2, \ldots$ forever. The concatenation is an infinite path from $z_0$. Its states are in $P$: the inner states of each segment by the choice of the segment, and the end points because $Z \subseteq P$. It visits each $J_i$ once in every $r$ segments, so infinitely often. So $z_0 \in G$. $\blacksquare$

With $r = 0$ the formula would be $\nu Z.\, P$, which is $P$ and not $\mathsf{EG}\,P$; taking $J_1 = S$ gives plain $\mathsf{EG}$. ∎
