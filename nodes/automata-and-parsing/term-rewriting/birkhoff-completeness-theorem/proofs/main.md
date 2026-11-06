---
title: Proof of Birkhoff's completeness theorem with the term model
proves: [statement]
status: full
---

Fix a signature $\Sigma$, a set of variables $V$ and a set $E$ of equations between terms of $T(\Sigma, V)$. Algebras have non-empty carriers. For a $\Sigma$-algebra $\mathcal{A}$ with carrier $A$ and an assignment $\alpha : V \to A$, the value $[\![t]\!]_\alpha$ of a term is defined by $[\![x]\!]_\alpha = \alpha(x)$ and $[\![f(t_1, \ldots, t_n)]\!]_\alpha = f^{\mathcal{A}}([\![t_1]\!]_\alpha, \ldots, [\![t_n]\!]_\alpha)$. $\mathcal{A}$ satisfies $s \approx t$ if $[\![s]\!]_\alpha = [\![t]\!]_\alpha$ for every $\alpha$, and $E \models s \approx t$ means that every algebra that satisfies all equations of $E$ satisfies $s \approx t$. The relation $\approx_E$ is the least relation that contains $E$ and is closed under reflexivity, symmetry, transitivity, congruence and substitution; see [equational theory](/equational-theory/), where it is also shown that $\approx_E$ is the conversion $\leftrightarrow_E^*$.

**Theorem.** $E \models s \approx t$ iff $s \approx_E t$.

## Substitution lemma

**Lemma 1.** For every algebra, assignment $\alpha$, substitution $\sigma$ and term $t$: $[\![t\sigma]\!]_\alpha = [\![t]\!]_{\beta}$, where $\beta(x) = [\![x\sigma]\!]_\alpha$.

*Proof.* Induction on $t$. For a variable $x$, both sides are $[\![x\sigma]\!]_\alpha$. For $t = f(t_1, \ldots, t_n)$, $[\![t\sigma]\!]_\alpha = f^{\mathcal{A}}([\![t_1\sigma]\!]_\alpha, \ldots) = f^{\mathcal{A}}([\![t_1]\!]_\beta, \ldots) = [\![t]\!]_\beta$ by the induction hypothesis. $\blacksquare$

## Soundness

**Lemma 2.** If $s \approx_E t$, then $E \models s \approx t$.

*Proof.* Let $\mathcal{A}$ satisfy $E$. We show by induction on a derivation of $s \approx_E t$ that $\mathcal{A}$ satisfies $s \approx t$. Equations of $E$ hold by assumption. Reflexivity, symmetry and transitivity hold because equality of values is an equivalence relation, for each fixed $\alpha$. For congruence, if $[\![s_i]\!]_\alpha = [\![t_i]\!]_\alpha$ for all $i$, then applying $f^{\mathcal{A}}$ to both lists gives equal values. For substitution, assume $\mathcal{A}$ satisfies $s \approx t$, and let $\alpha$ be an assignment. With $\beta(x) = [\![x\sigma]\!]_\alpha$, Lemma 1 gives $[\![s\sigma]\!]_\alpha = [\![s]\!]_\beta = [\![t]\!]_\beta = [\![t\sigma]\!]_\alpha$. $\blacksquare$

## Completeness

Write $\sim$ for $\approx_E$ and $[t]$ for the class of $t$ in $T(\Sigma, V)/{\sim}$.

**The term model.** Let $\mathcal{Q}$ have carrier $T(\Sigma, V)/{\sim}$ and operations $f^{\mathcal{Q}}([t_1], \ldots, [t_n]) = [f(t_1, \ldots, t_n)]$. This is well-defined: if $t_i \sim t_i'$ for all $i$, then $f(t_1, \ldots, t_n) \sim f(t_1', \ldots, t_n')$ by congruence. The carrier is not empty when $V$ is not empty or $\Sigma$ has a constant; we assume one of these, which holds whenever $s$ and $t$ exist.

**Lemma 3.** Let $\alpha$ be an assignment into $\mathcal{Q}$ and let $\sigma$ be a substitution with $[x\sigma] = \alpha(x)$ for every variable $x$ of a term $t$. Then $[\![t]\!]_\alpha = [t\sigma]$.

*Proof.* Induction on $t$. For a variable $x$, $[\![x]\!]_\alpha = \alpha(x) = [x\sigma]$. For $t = f(t_1, \ldots, t_n)$, $[\![t]\!]_\alpha = f^{\mathcal{Q}}([t_1\sigma], \ldots, [t_n\sigma]) = [f(t_1\sigma, \ldots, t_n\sigma)] = [t\sigma]$. $\blacksquare$

**Lemma 4.** $\mathcal{Q}$ satisfies every equation of $E$.

*Proof.* Let $l \approx r \in E$ and let $\alpha$ be an assignment into $\mathcal{Q}$. Pick a representative $x\sigma \in \alpha(x)$ for each of the finitely many variables of $l$ and $r$, and $x\sigma = x$ elsewhere. By Lemma 3, $[\![l]\!]_\alpha = [l\sigma]$ and $[\![r]\!]_\alpha = [r\sigma]$. Since $l \sim r$, the substitution rule gives $l\sigma \sim r\sigma$, so the two values are equal. $\blacksquare$

**Lemma 5.** If $E \models s \approx t$, then $s \approx_E t$.

*Proof.* By Lemma 4, $\mathcal{Q}$ is a model of $E$, so it satisfies $s \approx t$. Take the assignment $\alpha(x) = [x]$ and the identity substitution, which satisfies the condition of Lemma 3. Then $[s] = [\![s]\!]_\alpha = [\![t]\!]_\alpha = [t]$, that is, $s \sim t$. $\blacksquare$

Lemmas 2 and 5 prove the theorem. $\blacksquare$

**Remarks.** The proof shows more: $\mathcal{Q}$ alone decides all consequences of $E$, since $E \models s \approx t$ iff $\mathcal{Q}$ satisfies $s \approx t$ under the assignment $x \mapsto [x]$. $\mathcal{Q}$ is the free algebra of the class of models of $E$ over the generators $V$. The substitution rule was used in Lemma 4 to make $\mathcal{Q}$ a model of $E$; a relation closed only under the first four rules gives a quotient in which the equations of $E$ may fail for some assignments. In many-sorted equational logic, where a sort may have no elements, transitivity through a middle term with a variable of an empty sort is unsound, so there the rules must record the variables in use.
