---
title: Paramodulation is sound, and the loop without deletion is refutation complete by the theorem of Robinson and Wos
proves: [correctness]
status: sketch
---

We use the pseudocode of the page. An **E-interpretation** is an interpretation in which the predicate $=$ is the identity on the domain. $S$ is E-unsatisfiable when no E-interpretation satisfies it. Let $S_1$ be the set of clauses stored at line L1: $S$, $x = x$, and the functional reflexivity axioms.

**Theorem.**

1. If the loop returns UNSAT, then $S$ is E-unsatisfiable.
2. Suppose that lines L5 and L6 delete nothing, and that there is no limit. If $S$ is E-unsatisfiable, the loop returns UNSAT.

Parts 1 and the reduction in part 2 are proved in full below. Part 2 uses the completeness theorem of Robinson and Wos, which we state and outline but do not prove here. This proof does not cover the deletions at lines L5 and L6.

## Part 1

Every clause of $S_1 \setminus S$ is true in every E-interpretation. A factor and a binary resolvent follow from their parents. For a paramodulant, let $E$ be an E-interpretation that satisfies $C \vee l = r$ and $D$, and let $\theta$ assign elements of the domain to the variables of $(C \vee D[r])\sigma$. Both premises are true under every assignment, so $(C \vee l = r)\sigma$ and $D\sigma$ are true under $\theta$. If a literal of $C\sigma$ is true, the paramodulant is true. Otherwise $l\sigma = r\sigma$ is true, so $l\sigma$ and $r\sigma$ have the same value. Since $u\sigma = l\sigma$, the term $D\sigma$ at the chosen position and the term $D[r]\sigma$ at the same position have the same value, and by induction on the term structure every literal of $D\sigma$ has the same truth value as the matching literal of $D[r]\sigma$. So $D[r]\sigma$ is true. By induction on the order in which clauses are stored, every stored clause is true in every E-model of $S$. If $\square$ is stored, $S$ has no E-model.

## The theorem of Robinson and Wos

**Theorem (Robinson and Wos 1969).** If $S_1$ is E-unsatisfiable and holds $x = x$ and the functional reflexivity axioms for its function symbols, then there is a derivation of $\square$ from $S_1$ by binary resolution, factoring and paramodulation.

*Outline.* By [Herbrand's theorem](/herbrand-theorem/) for equality, some finite set $T$ of ground instances of clauses of $S_1$ is E-unsatisfiable. A ground argument shows that ground resolution and ground paramodulation, with the ground instances $t = t$, derive $\square$ from $T$. The ground steps are then lifted to the clauses of $S_1$, as in the [lifting lemma](/lifting-lemma/). One case does not lift: a ground paramodulation step can replace a term $s$ that lies inside $x\tau$ for a variable $x$, and then no non-variable position of the clause matches. The functional reflexivity axioms handle this case. From $s = t$ and $f(x_1, \ldots, x_n) = f(x_1, \ldots, x_n)$ paramodulation gives $f(\ldots s \ldots) = f(\ldots t \ldots)$, and repeating this builds an equation whose left side matches the term at a non-variable position above $x$. Brand (1975) and Peterson (1983) later gave proofs without the functional reflexivity axioms. See the sources of the page and Chapter 7 of the Handbook of Automated Reasoning.

## Part 2

Assume that lines L5 and L6 delete nothing and that there is no limit. Then every picked clause enters active at line L7 and stays there. Suppose that the loop does not return UNSAT. It cannot return SATURATED, because then every stored clause was picked, and the claim below and the theorem of Robinson and Wos give a stored $\square$, which line L4 would have returned. So it runs forever, and every stored clause is picked at some time, because line L3 takes the oldest untaken clause at every $k$-th pick and only finitely many clauses are older than a given one.

*Claim: every clause in a derivation from $S_1$ is stored, up to a renaming of variables.* By induction on the derivation. The clauses of $S_1$ are stored at line L1. Let $R$ be a factor of $X$, or a resolvent or paramodulant of $X$ and $Y$, where $X$ and $Y$ are stored up to renaming. Both are picked at some time, and let $G$ be the one picked later, or $X$ if $X = Y$. When $G$ is picked, the other one is in active, and after line L7 so is $G$. Line L8 forms every factor of $G$. Line L9 forms every binary resolvent of $G$ and each active clause, and line L10 every paramodulant from $G$ into each active clause and from each active clause into $G$, a clause and a copy of itself included, with the second clause renamed apart. A renaming of the premises gives a renaming of the conclusion, so a variant of $R$ is formed, and line L11 stores it, or the same clause was stored before.

By the claim, the $\square$ of the derivation from the theorem of Robinson and Wos is stored, so it is picked at some time, and line L4 returns UNSAT, a contradiction. $\blacksquare$
