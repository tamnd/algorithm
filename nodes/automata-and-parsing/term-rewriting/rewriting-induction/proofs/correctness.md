---
title: Rewriting induction is sound for proofs and for disproofs
proves: [correctness]
status: full
---

We use the definitions and the pseudocode of the page. $R$ is a constructor system, sufficiently complete, and $l > r$ for each rule, where $>$ is the lexicographic path ordering: it is well-founded, closed under contexts and substitutions, contains the proper subterm relation, and $l > r$ implies that every variable of $r$ occurs in $l$. An equation $s \doteq t$ is **valid** if $s\sigma \leftrightarrow^*_R t\sigma$ for every ground substitution $\sigma$. Let $H$ be the final set of hypotheses; $H$ only grows during the run, and every rule $l \to r$ added at line L10 satisfies $l > r$ by line L9. So $\to_{R \cup H} \subseteq {>}$, and the normalizations at line L5 stop.

**Lemma 1 (constructor normal forms).** Every ground term $w$ has $w \to_R^* \hat w$ for a ground constructor term $\hat w$.

*Proof.* $\to_R$ terminates, so $w$ has a normal form $\hat w$. If $\hat w$ had a defined symbol, an innermost one would be the root of a ground basic term $f(c_1, \ldots, c_n)$ with constructor terms $c_i$, which is reducible by sufficient completeness. $\square$

**Lemma 2 (followed instances).** Suppose the run returns at line L12. Let $e$ be an equation in $E$ at some time, $\theta$ a ground substitution, and $M$ either a ground term with $M > e\theta$, meaning $M$ is greater than both sides of $e\theta$, or the symbol $\infty$, taken to be above every ground term. Suppose every ground instance $l'\rho \to r'\rho$ of a rule of $H$ with $l'\rho < M$ satisfies $l'\rho \leftrightarrow^*_R r'\rho$. Then $e\theta$ holds modulo $R$.

*Proof.* The run removes $e$ at line L4 at some later time, since $E$ is empty at line L12. Consider what happens to $e = (s \doteq t)$ there. Line L5 turns it into $s' \doteq t'$ by steps of $R \cup H$; applied to $\theta$, each step is a step on a ground term below $M$, since the terms decrease from $s\theta$ or $t\theta$. A step with $R$ is in $\leftrightarrow^*_R$. A step with a rule of $H$ rewrites an instance $l'\rho$ that is a subterm of a term below $M$, so $l'\rho < M$ and the step is in $\leftrightarrow^*_R$ by assumption. So $s\theta \leftrightarrow^*_R s'\theta$ and $t\theta \leftrightarrow^*_R t'\theta$. Line L12 is reached, so the equation is not handled by lines L3, L7 or L9 with a return. Then either $s' = t'$ at line L6, and $e\theta$ holds, or $s' \doteq t'$, possibly swapped, becomes a rule $s' \to t'$ of $H$ at line L10. Its instance has left side $s'\theta < M$, so by assumption $s'\theta \leftrightarrow^*_R t'\theta$, and again $e\theta$ holds. $\square$

**Lemma 3 (hypotheses).** If the run returns at line L12, every rule $l \to r$ of $H$ is valid.

*Proof.* We show $l\sigma \leftrightarrow^*_R r\sigma$ for every rule $l \to r$ of $H$ and every ground $\sigma$, by well-founded induction on the ground term $l\sigma$ with respect to $>$, over all rules and substitutions at once.

If some variable $x$ of $l$ has $x\sigma$ not a constructor term, let $\hat\sigma$ map each variable $y$ to $\widehat{y\sigma}$ from Lemma 1. Then $l\sigma \to_R^+ l\hat\sigma$, so $l\hat\sigma < l\sigma$ and by induction $l\hat\sigma \leftrightarrow^*_R r\hat\sigma$; also $r\sigma \to_R^* r\hat\sigma$. So $l\sigma \leftrightarrow^*_R r\sigma$.

Otherwise $\sigma$ maps the variables of $l$ to ground constructor terms. When $l \to r$ was added, line L10 took the basic subterm $u = l|_p$. Then $u\sigma$ is a ground basic term, so some rule $l_1 \to r_1$ of $R$ has $u\sigma = l_1\rho$ at the root. With $l_1$ renamed apart, $\theta = \sigma \cup \rho$ unifies $u$ and $l_1$, so they have an idempotent mgu $\tau$, and $\theta = \tau\theta$ because every unifier is an instance of an idempotent mgu in this way. Line L11 put $e = (l[r_1]_p\tau \doteq r\tau)$ into $E$. Now $l\sigma \to_R l\sigma[r_1\rho]_p = l[r_1]_p\tau\theta$, and $r\tau\theta = r\sigma$ because the variables of $r$ occur in $l$. Both sides of $e\theta$ are below $M = l\sigma$: the left side by one $R$ step and the right side because $l > r$. By the induction hypothesis every ground instance of a rule of $H$ with left side below $l\sigma$ holds modulo $R$, so Lemma 2 applies and $l[r_1]_p\tau\theta \leftrightarrow^*_R r\sigma$. Hence $l\sigma \leftrightarrow^*_R r\sigma$. $\square$

**Theorem 1 (proved).** If the run returns PROVED, every conjecture of $E_0$ is valid.

*Proof.* Let $e \in E_0$ and $\sigma$ ground. By Lemma 3 every ground instance of a rule of $H$ holds modulo $R$, so Lemma 2 applies with $M = \infty$, and $e\sigma$ holds modulo $R$. $\blacksquare$

**Theorem 2 (disproved).** If $R$ is ground confluent and the run returns DISPROVED, some conjecture of $E_0$ is not valid.

*Proof.* Suppose every conjecture is valid. We show that every equation ever in $E$ and every rule ever in $H$ is valid, by induction on the run. Equations of $E_0$ are valid. Line L5 rewrites with $R$ and with rules of $H$, which are valid by induction, so validity of $s \doteq t$ passes to $s' \doteq t'$ by closure of $\leftrightarrow^*_R$ under ground instances and contexts. Line L10 adds a valid equation as a rule. At line L11, a ground instance of $l[r_1]_p\tau \doteq r\tau$ is reached from the instance of $l \doteq r$ by one $R$ step, so it is valid. So the equation $s \doteq t$ at line L7 is valid, and so is its ground instance $s\theta \doteq t\theta$ that the search found. But $s\theta$ and $t\theta$ are different ground constructor terms, which are $R$-normal forms because every left side has a defined root; in a ground confluent system two different normal forms are not equal modulo $R$. This is a contradiction. $\blacksquare$

**Termination.** Each iteration of line L2 removes an equation and increases the step count, so the loop ends at line L3, L7, L9 or L12 after at most $B$ iterations. Each normalization at line L5 stops because $\to_{R \cup H} \subseteq {>}$ and $>$ is well-founded, and the search at line L7 is finite. $\blacksquare$
