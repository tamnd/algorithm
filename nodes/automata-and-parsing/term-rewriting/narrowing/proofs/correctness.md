---
title: Narrowing is sound for every system and complete for convergent systems
proves: [correctness]
status: full
---

We use the pseudocode of the page and the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, $t|_p$ and $t[s]_p$, substitutions $\sigma$ written after the term, so $t\sigma\tau$ means $(t\sigma)\tau$, rules $l \to r$ with $l \notin V$ and $\mathrm{Var}(r) \subseteq \mathrm{Var}(l)$, and $\to_R^*$ for the reflexive transitive closure. The goal $s \approx t$ is kept as the term $e_0 = \mathrm{eq}(s, t)$ for a binary symbol $\mathrm{eq}$ that does not occur in $R$. A **node** is a triple $(e, \sigma, d)$ of a goal $e = \mathrm{eq}(u, v)$, a substitution $\sigma$ on the variables $X = \mathrm{Var}(s) \cup \mathrm{Var}(t)$, and a depth $d$. Line L9 renames each rule apart, with variables that occur nowhere else in the run.

The unifiers that line L4 and line L8 compute are fully applied, so they are **idempotent**: no variable of the domain occurs in the range. An idempotent most general unifier $\tau$ of $u$ and $l$ has this property: for every unifier $\gamma$ of $u$ and $l$, $\tau\gamma = \gamma$. Indeed, $\gamma = \tau\gamma'$ for some $\gamma'$, so $\tau\gamma = \tau\tau\gamma' = \tau\gamma' = \gamma$.

**Theorem.** Let $D$ be the depth bound.

1. **Termination.** The procedure stops.
2. **Soundness.** For every system $R$ and every answer $\alpha$, $s\alpha \to_R^{k_1} w$ and $t\alpha \to_R^{k_2} w$ for a term $w$ with $k_1 + k_2 \le D$.
3. **Completeness.** Let $R$ be terminating and confluent, and let $\theta$ be a substitution on $X$ with $x\theta$ in normal form for every $x \in X$ and $s\theta \leftrightarrow_R^* t\theta$. Let $n$ be the length of an innermost reduction of $\mathrm{eq}(s\theta, t\theta)$ to its normal form. If $D \ge n$, the procedure returns an answer $\alpha$ such that $x\theta = x\alpha\eta$ for all $x \in X$, for one substitution $\eta$.

## Termination

Each node $(e, \sigma, d)$ has at most $|e| \cdot |R|$ children, one per position and rule, and children are created only for $d < D$. By induction on $d$, finitely many nodes of each depth $d \le D$ are created, and none of depth more than $D$. Each node is removed from the queue once, and each removal does a finite amount of work. $\blacksquare$

## Soundness

**Lemma 1.** For every node $(e, \sigma, d)$ in the queue, $e_0\sigma \to_R^d e$.

*Proof.* Induction on $d$. The node of line L1 has $e = e_0$, $\sigma$ the identity and $d = 0$. A child is created at line L9 from $(e, \sigma, d)$, a position $p$ with $e|_p \notin V$, a renamed rule $l \to r$, and $\tau$ with $e|_p\tau = l\tau$. Then $e\tau|_p = l\tau$ is a redex, and $e\tau \to_R e\tau[r\tau]_p = (e[r]_p)\tau$, which is the child goal. By the induction hypothesis $e_0\sigma \to_R^d e$, and rewriting is closed under substitutions, so $e_0\sigma\tau \to_R^d e\tau \to_R (e[r]_p)\tau$. The child substitution is $\sigma\tau$ on $X$. $\blacksquare$

*Proof of soundness.* An answer comes from a node $(\mathrm{eq}(u, v), \sigma, d)$ with $d \le D$ at line L4, where $\mu$ unifies $u$ and $v$, and $\alpha = \sigma\mu$ on $X$. By Lemma 1 and closure under substitutions, $\mathrm{eq}(s\alpha, t\alpha) = e_0\sigma\mu \to_R^d \mathrm{eq}(u\mu, v\mu)$. Since $\mathrm{eq}$ does not occur in $R$, no step is at the root, so each step rewrites inside one argument. With $w = u\mu = v\mu$, $s\alpha \to_R^{k_1} w$ and $t\alpha \to_R^{k_2} w$ with $k_1 + k_2 = d \le D$. Line L4 renames the fresh variables of $\alpha$ bijectively, which keeps this property. $\blacksquare$

Soundness does not use termination or confluence.

## Completeness

A substitution $\eta$ is **normalized on** a set $Y$ of variables if $y\eta$ is a normal form for every $y \in Y$. A subterm of a normal form is a normal form.

**Lemma 2 (lifting).** Let $(e, \sigma, d)$ be a node with $d < D$, and let $\eta$ be a substitution, normalized on $\mathrm{Var}(e)$, with $x\sigma\eta = x\theta$ for all $x \in X$. Let $e\eta \to_R e'$ be an innermost step. Then line L9 creates a child $(e'', \sigma\tau, d + 1)$ and there is a substitution $\eta'$, normalized on $\mathrm{Var}(e'')$, with $x\sigma\tau\eta' = x\theta$ for all $x \in X$ and $e''\eta' = e'$.

*Proof.* The step uses a rule $l \to r$ at a position $p$ of $e\eta$ with $e\eta|_p = l\rho$. It is innermost, so every proper subterm of $l\rho$ is a normal form; since $l$ is not a variable, $x\rho$ is a proper subterm of $l\rho$ for each $x \in \mathrm{Var}(l)$, so $\rho$ is normalized on $\mathrm{Var}(l)$.

The position $p$ is a position of $e$ with $e|_p \notin V$. Otherwise $p$ is at or below an occurrence of a variable $y$ of $e$, and $l\rho$ is a subterm of $y\eta$, which is a normal form, but $l\rho$ is a redex. Also $p$ is not the root, since $\mathrm{eq}$ does not occur in $R$.

At line L9 the procedure tries the position $p$ and the rule $l \to r$, renamed apart. We may assume that $l \to r$ is this renamed copy, with $\rho$ adjusted; its variables occur neither in $e$ nor in the range of $\sigma$ nor in the domain of $\eta$. Let $\gamma = \eta \cup \rho$, which is well defined because the domains are disjoint. Then $e|_p\gamma = e|_p\eta = l\rho = l\gamma$, so $e|_p$ and $l$ unify, line L8 finds the idempotent most general unifier $\tau$, and line L9 creates the child with $e'' = (e[r]_p)\tau$ and substitution $\sigma\tau$. By the property of idempotent most general unifiers, $\tau\gamma = \gamma$. Set $\eta' = \gamma$. Then:

- $e''\eta' = e[r]_p\tau\gamma = e[r]_p\gamma = e\eta[r\rho]_p = e'$.
- For $x \in X$: $x\sigma\tau\eta' = x\sigma\gamma = x\sigma\eta = x\theta$, because the variables of $x\sigma$ are not variables of the rule.
- Let $y \in \mathrm{Var}(e'')$. Then $y$ occurs in $z\tau$ for some $z \in \mathrm{Var}(e[r]_p) \subseteq \mathrm{Var}(e) \cup \mathrm{Var}(l)$. So $y\gamma$ is a subterm of $z\tau\gamma = z\gamma$, which is $z\eta$ or $z\rho$, a normal form. So $y\eta'$ is a normal form. $\blacksquare$

*Proof of completeness.* $R$ is confluent and $s\theta \leftrightarrow_R^* t\theta$, so $s\theta$ and $t\theta$ have the same normal form $w$. Since $\mathrm{eq}$ does not occur in $R$, the normal form of $e_0\theta$ is $\mathrm{eq}(w, w)$, and $R$ is terminating, so an innermost reduction $e_0\theta = f_0 \to_R f_1 \to_R \cdots \to_R f_n = \mathrm{eq}(w, w)$ exists.

We show by induction on $i \le n$: there is a node $(e_i, \sigma_i, i)$ that the procedure creates, and a substitution $\eta_i$ normalized on $\mathrm{Var}(e_i)$, with $x\sigma_i\eta_i = x\theta$ for $x \in X$ and $e_i\eta_i = f_i$. For $i = 0$ take the node of line L1 and $\eta_0 = \theta$, which is normalized on $\mathrm{Var}(e_0) = X$. For the step from $i$ to $i + 1$, the step $f_i \to_R f_{i+1}$ is an innermost step of $e_i\eta_i$, and $i < n \le D$, so Lemma 2 applies.

Every created node is eventually removed at line L3, since the queue is first in, first out and the procedure terminates. When line L4 runs on the node $(e_n, \sigma_n, n)$ with $e_n = \mathrm{eq}(u, v)$, $\eta_n$ unifies $u$ and $v$ because $e_n\eta_n = \mathrm{eq}(w, w)$. So the most general unifier $\mu$ exists and $\mu\eta_n = \eta_n$. The answer is $\alpha = \sigma_n\mu$ on $X$, and for $x \in X$, $x\alpha\eta_n = x\sigma_n\mu\eta_n = x\sigma_n\eta_n = x\theta$. Line L4 renames the fresh variables of $\alpha$ by a bijection $\pi$, which gives the answer $\alpha\pi$ with $x\theta = x\alpha\pi\pi^{-1}\eta_n$; if the same answer was found before, it is already in the list. Take $\eta = \pi^{-1}\eta_n$. $\blacksquare$

## Remarks

**Why normalized solutions.** The theorem covers only solutions $\theta$ whose values are normal forms. For a convergent $R$ this is no loss: replacing each $x\theta$ by its normal form gives a normalized solution that is equal modulo $R$. Without the condition the lifting fails: with $R = \{ f(a) \to b \}$, the goal $x \approx b$ has the solution $x \mapsto f(a)$, and the only answer is $x \mapsto b$, of which $f(a)$ is not an instance.

**Why the innermost reduction.** Lemma 2 needs $\rho$ to be normalized, so that the new $\eta'$ is normalized again. An innermost step gives this for free. The depth needed is the length $n$ of an innermost reduction, so a breadth-first search with $D \ge n$ finds the answer.

**Without termination or confluence.** Soundness holds for every system. Completeness fails without confluence: for $R = \{ a \to b,\ a \to c \}$, the goal $b \approx c$ holds modulo $R$, but $b$ and $c$ are normal forms with no common reduct, and narrowing finds nothing.
