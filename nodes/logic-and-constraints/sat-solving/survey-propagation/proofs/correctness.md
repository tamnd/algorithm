---
title: SP-guided decimation returns only models and stops; the SP update sends full warnings exactly as unit propagation does
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $F$ is a CNF formula over $x_1, \ldots, x_n$. This file proves only that the procedure is sound and that it stops, and one exact fact about the equations. It does not prove that the procedure finds a model of a satisfiable formula: that claim is false in general, and on random formulas its success is measured, not proved.

**Lemma 1 (simplification is sound).** Let $\sigma$ be the partial assignment of the fixed variables after a call of `simplify`, and let $F'$ be the formula it returns. Then every total assignment that extends $\sigma$ and satisfies $F'$ satisfies $F$. If `simplify` returns "empty clause", no total assignment that extends the fixed values given to it satisfies $F$.

*Proof.* `simplify` removes tautologies, which every assignment satisfies, removes the clauses that contain a literal made true by $\sigma$, which every extension of $\sigma$ satisfies, and removes from the other clauses the literals made false by $\sigma$, which no extension of $\sigma$ can use. So a clause of $F$ is either satisfied by $\sigma$, or its reduced form is in $F'$. When it finds a unit clause $(\ell)$ of the reduced formula, it adds the value that makes $\ell$ true to $\sigma$ and repeats; this keeps the same invariant. If a reduced clause is empty, all its literals are false under the fixed values, and no extension satisfies it. $\square$

**Lemma 2 (termination).** The procedure stops after at most $n$ rounds of the loop of line L1. Each round runs at most a fixed number of sweeps, and the final WalkSAT phase runs at most a fixed number of flips.

*Proof.* At the start of a round, $F'$ has at least one clause, and every clause of $F'$ is non-empty and has only free variables. So the set of free variables that occur in $F'$ is not empty, and line L6 fixes at least one of them. After line L7 that variable no longer occurs in $F'$. So the number of free variables that occur in $F'$ drops by at least one per round, and there are at most $n$ rounds. The sweep loop of line L2 and the flip loop of line L9 are bounded by their limits. $\square$

**Theorem 1 (soundness).** If the procedure returns an assignment, it satisfies $F$.

*Proof.* Line L10 checks every clause of the original $F$ before it returns. Lemma 1 also shows why the check passes when WalkSAT succeeds: the returned $x$ extends the fixed values and satisfies the last $F'$. $\blacksquare$

So a wrong decimation step can only cause the answer "failure", never a wrong model. "Failure" proves nothing about $F$.

**The SP update.** For a clause $a$ and a variable $j$ of $a$, let $p_s$ be the product of $1 - \eta_{b \to j}$ over the other clauses $b$ that contain $j$ with the same sign as in $a$, and $p_u$ the same product over the other clauses with the opposite sign. Then

$$\Pi^u_{j \to a} = (1 - p_u)\, p_s, \qquad \Pi^s_{j \to a} = (1 - p_s)\, p_u, \qquad \Pi^0_{j \to a} = p_s\, p_u,$$

and $\eta_{a \to i} = \prod_{j \in a,\, j \ne i} \Pi^u_{j \to a} / (\Pi^u_{j \to a} + \Pi^s_{j \to a} + \Pi^0_{j \to a})$.

**Lemma 3 (full warnings follow unit propagation).** Suppose all surveys are 0 or 1. Then $\eta_{a \to i} = 1$ if and only if, for every other variable $j$ of $a$, some other clause $b$ with $\eta_{b \to j} = 1$ contains $j$ with the sign opposite to its sign in $a$, and no other clause $b'$ with $\eta_{b' \to j} = 1$ contains $j$ with the same sign as in $a$. Otherwise $\eta_{a \to i} = 0$. In particular, a unit clause always has survey 1.

*Proof.* With surveys in $\{0, 1\}$, $p_s$ is 0 if some other same-sign clause sends a warning to $j$, and 1 otherwise, and the same holds for $p_u$ with opposite-sign clauses. If $p_u = 0$ and $p_s = 1$, the ratio for $j$ is $1/1 = 1$. If $p_u = 1$, then $\Pi^u = 0$ and the ratio is 0 (the denominator is $p_s + p_u - p_s p_u \ge 1$). If $p_u = p_s = 0$, all three terms are 0: the variable is warned by both signs, which is a contradiction, and the implementation stops with "failure". The survey $\eta_{a \to i}$ is the product of the ratios of the other variables, which is 1 exactly when every ratio is 1. For a unit clause the product is empty, so it is 1. $\square$

Read with "warned toward value $v$" for "receives a warning from a clause that needs $v$", Lemma 3 says that clause $a$ warns $i$ exactly when all other variables of $a$ are forced to violate $a$. This is unit propagation, so on formulas where only unit propagation matters, the 0 and 1 surveys are a fixed point that reproduces it. The surveys strictly between 0 and 1 are where SP differs from unit propagation; their meaning as probabilities over clusters of models is a prediction of the cavity method of statistical physics, and is not proved in general.

**What is not claimed.** No bound is proved on the number of sweeps that SP needs to converge, and on some formulas it does not converge. No proof shows that decimation guided by SP keeps a satisfiable formula satisfiable. The good results on large random 3-SAT and $k$-SAT formulas near the threshold are measured.
