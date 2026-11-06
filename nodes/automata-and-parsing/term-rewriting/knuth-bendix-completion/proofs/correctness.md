---
title: Completion is sound, and a success result is a convergent system for the input equations
proves: [correctness]
status: full
---

We use the pseudocode of the page and the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, $t|_p$ and $t[s]_p$, substitutions $\sigma$, rules $l \to r$, and $\to^*$ for the reflexive transitive closure. For a set $E$ of equations, $\leftrightarrow_E$ is one replacement step with an equation of $E$ in either direction, and $\leftrightarrow_E^*$ its reflexive transitive closure. We treat a set $R$ of rules as a set of equations when we write $\leftrightarrow_{E \cup R}^*$. $E_0$ is the input set, $B$ the step bound and $>$ the order.

**Assumption.** $>$ is a reduction order: a strict order on $T(\Sigma, V)$ that is well-founded and closed under contexts ($s > t$ implies $u[s]_p > u[t]_p$) and under substitutions ($s > t$ implies $s\sigma > t\sigma$). The [lexicographic path ordering](/lexicographic-path-ordering/) and the [Knuth-Bendix ordering](/knuth-bendix-ordering/) are reduction orders.

**Theorem.** The procedure stops after at most $B$ executions of line L5. If it returns $\mathrm{SUCCESS}(R)$, then $R$ is terminating and confluent, and $\leftrightarrow_R^* = \leftrightarrow_{E_0}^*$. If it returns $\mathrm{FAIL}(s \approx t)$, then $s \ne t$, $s \leftrightarrow_{E_0}^* t$, and neither $s > t$ nor $t > s$. If it returns $\mathrm{GIVE\text{-}UP}(R)$, then $R$ is terminating and $\leftrightarrow_R^* \subseteq \leftrightarrow_{E_0}^*$.

## Invariants

We show that the following two statements hold each time line L2 starts an iteration, and also when the procedure returns.

- **(I1)** Every rule $g \to d$ in $R$ satisfies $g > d$.
- **(I2)** $\leftrightarrow_{E \cup R}^* = \leftrightarrow_{E_0}^*$.

After line L1, $R = \emptyset$ and $E = E_0$, so both hold. We check that each line keeps them. Write $E, R$ for the sets before the line and $E', R'$ for the sets after it.

**Two facts about conversions.** (F1) If $E \cup R$ and $E' \cup R'$ are such that each equation of one set is a consequence $u \leftrightarrow^* v$ of the other set, then the two conversions are equal: a step with $u \approx v$ inside a context $w[\cdot]_p$ under a substitution $\sigma$ is replaced by the conversion $u \leftrightarrow^* v$ in the same context and under the same substitution, and conversions are closed under contexts and substitutions. (F2) If $u \to_R^* u'$, then $u \leftrightarrow_R^* u'$.

**Line L3.** It adds to $E$ critical pairs $\langle u, v \rangle$ of $R$. Each of them comes from a term $l_1\sigma$ with $l_1\sigma \to_R u$ and $l_1\sigma \to_R v$, so $u \leftrightarrow_R^* v$, and (I2) holds by (F1). $R$ does not change.

**Line L5.** It replaces $s \approx t$ by $s{\downarrow} \approx t{\downarrow}$, where $s{\downarrow}$ and $t{\downarrow}$ are normal forms reached with $R$. The new equation is a consequence of $\{s \approx t\} \cup R$ by $s{\downarrow} \leftrightarrow_R^* s \leftrightarrow t \leftrightarrow_R^* t{\downarrow}$, and the old one is a consequence of $\{s{\downarrow} \approx t{\downarrow}\} \cup R$ in the same way. By (F1), (I2) holds. The normal forms exist because $R$ terminates, which follows from (I1): a rewrite step $w[g\sigma]_p \to w[d\sigma]_p$ goes down in $>$ by the closure properties, and $>$ is well-founded.

**Line L6.** It removes an equation $s \approx s$, which is a consequence of the empty set.

**Line L7.** It moves $s \approx t$ from $E$ to $R$ as $s \to t$ or $t \to s$, chosen so that the left side is the greater one. The set $E \cup R$ is the same as a set of equations, so (I2) holds, and the new rule satisfies (I1). If neither side is greater, the procedure returns; we treat this case below.

**Line L8.** It moves rules $g \to d$ from $R$ to $E$ as $g \approx d$. Again $E \cup R$ does not change as a set of equations, and (I1) holds for the remaining rules.

**Line L9.** It replaces a rule $g \to d$ by $g \to d'$, where $d \to_{S}^* d'$ for the set $S = (R \setminus \{g \to d\}) \cup \{\rho\}$. All rules of $S$ satisfy (I1), by the previous lines and because earlier executions of this line keep (I1), as we now show. Each rewrite step with $S$ goes down in $>$, so $d > d'$ or $d = d'$; with $g > d$ and transitivity, $g > d'$. For (I2): $g \approx d'$ is a consequence of $\{g \approx d\} \cup S$, by $g \leftrightarrow d \to_S^* d'$, and $g \approx d$ is a consequence of $\{g \approx d'\} \cup S$, by $g \leftrightarrow d' \leftarrow_S^* d$. The rules of $S$ stay in the system, so (F1) applies.

**Line L10.** It adds $\rho$ to $R$, which it already contains as an equation after line L7, and adds critical pairs to $E$, which are consequences of $R$ as for line L3.

Line L4 changes neither set. So (I1) and (I2) hold at every iteration and at each return.

## A rule never has a variable left side or a new variable on the right

These two facts follow from (I1) alone, and they make every rule of $R$ a proper rewrite rule. Let $g > d$.

- **$g$ is not a variable.** Suppose $g = x$. If $x$ occurs in $d$, then $d = C[x]$ for a context $C$ that is not empty, because $x \ne d$ by irreflexivity. With $\sigma = \{x \mapsto d\}$ and closure under substitutions and contexts we get $x > C[x] > C[C[x]] > \cdots$, an infinite descending chain, which contradicts well-foundedness. If $x$ does not occur in $d$, then with $\sigma = \{x \mapsto d\}$ we get $d = x\sigma > d\sigma = d$, which contradicts irreflexivity.
- **$\mathrm{Var}(d) \subseteq \mathrm{Var}(g)$.** Suppose $y$ occurs in $d$ but not in $g$. Then $d = C[y]$ for a context $C$. With $\sigma = \{y \mapsto g\}$ we get $g = g\sigma > d\sigma = C\sigma[g]$, where $C\sigma$ is $C$ with $\sigma$ applied. If $C$ is empty this is $g > g$; otherwise closure under contexts gives $g > C\sigma[g] > C\sigma[C\sigma[g]] > \cdots$. Both contradict the assumptions on $>$.

## Termination of the procedure

Line L4 counts the iterations that reach it, and returns when the count exceeds $B$. Each iteration that does not reach line L4 returns at line L3. Each other line runs a finite number of times per iteration: line L5 normalizes with a terminating $R$, and lines L8 to L10 loop over the finite set $R$, whose critical pairs are finite in number because each left side has finitely many positions and a most general unifier is unique up to renaming. So the procedure stops.

## The three results

**Success.** The procedure returns $\mathrm{SUCCESS}(R)$ only at line L3, when $E$ is empty and every critical pair $\langle u, v \rangle$ of $R$ satisfies $u{\downarrow}_R = v{\downarrow}_R$, with the normal forms computed by line L3. So every critical pair of $R$ is joinable. By the [critical pair lemma](/critical-pair-lemma/), $R$ is locally confluent. By (I1), $R$ is terminating, as shown for line L5. By [Newman's lemma](/newman-lemma/), $R$ is confluent. By (I2) with $E = \emptyset$, $\leftrightarrow_R^* = \leftrightarrow_{E_0}^*$.

**Fail.** The procedure returns $\mathrm{FAIL}(s \approx t)$ only at line L7, after line L6 found $s \ne t$, and when neither $s > t$ nor $t > s$. The equation $s \approx t$ was in $E$, so $s \leftrightarrow_{E \cup R}^* t$, and by (I2), $s \leftrightarrow_{E_0}^* t$.

**Give up.** The procedure returns $\mathrm{GIVE\text{-}UP}(R)$ only at line L4. By (I1), $R$ is terminating, and by (I2), every rule of $R$ is a consequence of $E_0$, so $\leftrightarrow_R^* \subseteq \leftrightarrow_{E_0}^*$. $\blacksquare$

## Remarks

**Why line L3 checks all critical pairs.** Line L10 adds the critical pairs of each new rule, and line L5 later deletes those that become joinable. But line L8 may remove a rule after its critical pairs were computed, and line L9 may change a right side, so a critical pair that was joinable earlier is not obviously joinable for the final $R$. Line L3 recomputes all critical pairs of the final $R$, so the success case needs no argument about the history of the run. A run that never needs line L3 to add a pair pays only the cost of the check.

**Consequence for the word problem.** On success, by the [Birkhoff completeness theorem](/birkhoff-completeness-theorem/), $E_0 \models s \approx t$ iff $s \leftrightarrow_{E_0}^* t$ iff $s{\downarrow}_R = t{\downarrow}_R$; the last equivalence holds because $R$ is confluent and terminating. So the result decides the word problem of $E_0$.

**What the theorem does not say.** It does not say that a convergent system for $E_0$ does not exist when the procedure fails or gives up. A different order, or a different choice of equation at line L5, may succeed. The bound $B$ only cuts off runs that do not stop by themselves.
