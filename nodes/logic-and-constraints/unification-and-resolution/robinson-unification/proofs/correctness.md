---
title: Robinson's algorithm terminates and returns an idempotent most general unifier or correct failure
proves: [correctness]
status: full
---

We use the notation of the page. $s$ and $t$ are the input terms, $X = \mathrm{Var}(s) \cup \mathrm{Var}(t)$ and $n = |X|$. $\sigma_k$ is the value of $\sigma$ after $k$ executions of line L7, so $\sigma_0 = \varepsilon$, and $s_k = s\sigma_k$, $t_k = t\sigma_k$. A unifier of $s$ and $t$ is a $\theta$ with $s\theta = t\theta$.

## The disagreement pair

Positions are sequences of argument numbers, and $u|_p$ is the subterm of $u$ at position $p$. If $s' \ne t'$, read the two terms together in preorder. The first disagreement pair is $(s'|_p, t'|_p)$ for the first position $p$ (in preorder) that is a position of both terms where the two subterms differ and either one of them is a variable, or their root symbols differ, or their arities differ. Above $p$ the two terms have the same symbols, so $p$ exists when $s' \ne t'$.

**Lemma 1.** If $\theta$ unifies $s'$ and $t'$, and $p$ is a position of both, then $(s'|_p)\theta = (t'|_p)\theta$.

*Proof.* Substitution keeps the positions of a term: $p$ is a position of $s'\theta$ and $(s'\theta)|_p = (s'|_p)\theta$. The same holds for $t'$. As $s'\theta = t'\theta$, the two subterms at $p$ are equal. $\square$

## Invariants

We show by induction on $k$ that, while the loop runs:

- **(I1)** $\sigma_k$ is idempotent, and $\mathrm{dom}(\sigma_k) \cup \mathrm{vran}(\sigma_k) \subseteq X$.
- **(I2)** Each unifier $\theta$ of $s$ and $t$ satisfies $\theta = \sigma_k\theta$.
- **(I3)** $\mathrm{Var}(s_k) \cup \mathrm{Var}(t_k) \subseteq X \setminus \mathrm{dom}(\sigma_k)$, and $|\mathrm{dom}(\sigma_k)| = k$.

For $k = 0$ all three hold with $\sigma_0 = \varepsilon$.

**A consequence of (I2).** If $\theta$ unifies $s$ and $t$, then $s_k\theta = s\sigma_k\theta = s\theta = t\theta = t\sigma_k\theta = t_k\theta$. So each unifier of $s, t$ unifies $s_k, t_k$, and if $s_k, t_k$ have no unifier, neither have $s, t$.

**Line L4.** Here $u = s_k|_p$ and $v = t_k|_p$ are both non-variables with different root symbols or arities. For each $\theta$, $u\theta$ and $v\theta$ have these different roots, so $u\theta \ne v\theta$. By Lemma 1, $s_k$ and $t_k$ have no unifier, and by the consequence of (I2), neither have $s$ and $t$. So FAIL is correct.

**Line L6.** Here $x$ is a variable, $x \ne r$ (the pair differs), and $x \in \mathrm{Var}(r)$. Then $r$ is not a variable, and $x$ is a proper subterm of $r$. For each $\theta$, $x\theta$ is a proper subterm of $r\theta$, so $|r\theta| > |x\theta|$. By Lemma 1, $s_k, t_k$ have no unifier, and neither have $s, t$. So FAIL is correct.

**Line L7.** Here $x \notin \mathrm{Var}(r)$. Let $\tau = \{x \mapsto r\}$, so $\sigma_{k+1} = \sigma_k\tau$, $s_{k+1} = s_k\tau$ and $t_{k+1} = t_k\tau$. Both $x$ and $\mathrm{Var}(r)$ are inside $\mathrm{Var}(s_k) \cup \mathrm{Var}(t_k)$, which by (I3) is disjoint from $\mathrm{dom}(\sigma_k)$.

*(I2) for $k + 1$.* Let $\theta$ unify $s$ and $t$. It unifies $s_k, t_k$, so by Lemma 1, $x\theta = r\theta$. Then $x\tau\theta = r\theta = x\theta$, and $y\tau\theta = y\theta$ for $y \ne x$, so $\tau\theta = \theta$. Hence $\sigma_{k+1}\theta = \sigma_k\tau\theta = \sigma_k\theta = \theta$.

*(I1) for $k + 1$.* Since $x \notin \mathrm{dom}(\sigma_k)$, $x\sigma_{k+1} = x\tau = r$, and for $y \in \mathrm{dom}(\sigma_k)$, $y\sigma_{k+1} = (y\sigma_k)\tau$. So

$$\mathrm{dom}(\sigma_{k+1}) = \mathrm{dom}(\sigma_k) \cup \{x\}, \qquad \mathrm{vran}(\sigma_{k+1}) \subseteq (\mathrm{vran}(\sigma_k) \setminus \{x\}) \cup \mathrm{Var}(r).$$

For the domain: $x\sigma_{k+1} = r \ne x$, and for $y \in \mathrm{dom}(\sigma_k)$ the variables of $(y\sigma_k)\tau$ lie in $\mathrm{vran}(\sigma_k) \cup \mathrm{Var}(r)$, which is disjoint from $\mathrm{dom}(\sigma_k)$, so $(y\sigma_k)\tau \ne y$. The four intersections are empty: $\mathrm{vran}(\sigma_k) \cap \mathrm{dom}(\sigma_k) = \emptyset$ by (I1), $(\mathrm{vran}(\sigma_k) \setminus \{x\}) \cap \{x\} = \emptyset$, $\mathrm{Var}(r) \cap \mathrm{dom}(\sigma_k) = \emptyset$ by (I3), and $x \notin \mathrm{Var}(r)$. So $\mathrm{dom}(\sigma_{k+1}) \cap \mathrm{vran}(\sigma_{k+1}) = \emptyset$, which means that $\sigma_{k+1}$ is idempotent. (If $\mathrm{dom} \cap \mathrm{vran} = \emptyset$, each $y\sigma$ has only variables that $\sigma$ fixes, so $y\sigma\sigma = y\sigma$.) Both sets are inside $X$, because $x$ and $\mathrm{Var}(r)$ are inside $\mathrm{Var}(s_k) \cup \mathrm{Var}(t_k) \subseteq X$.

*(I3) for $k + 1$.* The variables of $s_k\tau$ and $t_k\tau$ are those of $s_k, t_k$ other than $x$, plus those of $r$, which are already variables of $s_k, t_k$. So $\mathrm{Var}(s_{k+1}) \cup \mathrm{Var}(t_{k+1}) \subseteq (\mathrm{Var}(s_k) \cup \mathrm{Var}(t_k)) \setminus \{x\} \subseteq X \setminus \mathrm{dom}(\sigma_{k+1})$. As $x \notin \mathrm{dom}(\sigma_k)$, $|\mathrm{dom}(\sigma_{k+1})| = k + 1$.

## Termination

Each pass of the loop returns at L4 or L6, or executes L7. By (I1) and (I3), $\mathrm{dom}(\sigma_k)$ is a subset of $X$ with $k$ elements, so $k \le n$. So line L7 runs at most $n$ times, and the loop stops after at most $n + 1$ passes.

## Result

If the algorithm returns FAIL, at L4 or L6, then $s$ and $t$ have no unifier, as shown above.

If it returns $\sigma = \sigma_k$ at L8, then $s\sigma = s_k = t_k = t\sigma$, so $\sigma$ is a unifier. By (I2), each unifier $\theta$ satisfies $\theta = \sigma\theta$, so $\sigma \le \theta$. So $\sigma$ is a most general unifier. By (I1) it is idempotent, and its domain and variable range lie in $X$.

Finally, if $s$ and $t$ are unifiable, the algorithm cannot return FAIL, since FAIL is returned only when no unifier exists. As it terminates, it returns a most general unifier. $\blacksquare$
