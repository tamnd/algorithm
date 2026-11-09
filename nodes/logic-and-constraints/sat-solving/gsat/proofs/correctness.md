---
title: GSAT returns only models, stops after at most MAX-TRIES times MAX-FLIPS flips, and its score is the change in the number of satisfied clauses
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $F$ is a CNF formula over $x_1, \ldots, x_n$ in which no clause repeats a literal or contains a literal and its negation. The implementation removes repeated literals and tautological clauses first; this does not change the models. A formula with an empty clause has no model, and the implementation answers "no model found" at once.

**Definitions.** For an assignment $x$ and a variable $v$, let $x^{(v)}$ be $x$ with $v$ flipped.

- $\mathrm{make}(v)$ is the number of clauses that are false under $x$ and true under $x^{(v)}$.
- $\mathrm{break}(v)$ is the number of clauses that are true under $x$ and false under $x^{(v)}$.
- $\mathrm{score}(v) = \mathrm{make}(v) - \mathrm{break}(v)$.

**Lemma 1.** $\mathrm{score}(v) = \mathrm{sat}(x^{(v)}) - \mathrm{sat}(x)$, where $\mathrm{sat}$ counts the true clauses.

*Proof.* A clause without $v$ has the same value under $x$ and $x^{(v)}$. A clause with $v$ either keeps its value, or changes from false to true (counted in make), or from true to false (counted in break). So the count changes by make minus break. $\square$

**Lemma 2 (how the implementation computes the counts).** Under $x$:

- A clause $C$ is counted in $\mathrm{make}(v)$ if and only if $C$ is false and contains a literal of $v$.
- A clause $C$ is counted in $\mathrm{break}(v)$ if and only if $C$ has exactly one true literal and that literal is on $v$.

*Proof.* If $C$ is false, every literal of $C$ is false. Flipping $v$ makes the literal of $v$ in $C$ true, if there is one, and so makes $C$ true; if $C$ has no literal of $v$, it stays false. If $C$ is true and has two or more true literals, flipping one variable changes at most one literal of $C$, since $C$ has at most one literal of each variable, so $C$ stays true. If $C$ has exactly one true literal $\ell$, flipping the variable of $\ell$ makes $C$ false, and flipping another variable leaves $\ell$ true. $\square$

The function `scores` of the implementation counts exactly these cases, in one pass over the clauses.

**Theorem.**
1. If GSAT returns an assignment, it is a model of $F$.
2. GSAT stops after at most MAX-TRIES $\times$ MAX-FLIPS flips.
3. Each flip of line L7 increases the number of satisfied clauses by the largest amount that one flip can give, which may be zero or negative.

*Proof.* (1) Line L4 returns $x$ only after the check that $x$ satisfies each clause. (2) The loops of lines L1 and L3 are bounded by MAX-TRIES and MAX-FLIPS. (3) Line L6 picks $v$ with the largest score, and by Lemma 1 the score is the change in the number of satisfied clauses. $\blacksquare$

**What is not claimed.** GSAT is incomplete. If $F$ has no model, GSAT never returns an assignment, and it reports "no model found" after all tries, which is not a proof. If $F$ has a model, no bound on the probability of finding it is proved for GSAT in general: the greedy rule can move back and forth on a plateau or around a local maximum of the number of satisfied clauses. The random restarts of line L2 are what makes it leave such regions.
