---
title: Davis-Putnam elimination preserves satisfiability, terminates after at most n steps, and its record gives a model
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $F$ is a set of clauses over $x_1, \ldots, x_n$, a clause is a set of literals, and no clause holds a literal and its negation. An assignment $\beta$ gives each variable a value, and it satisfies $F$ when each clause of $F$ has a true literal. Let $\mathrm{var}(F)$ be the set of variables that occur in $F$. For a variable $x$, let $P$ be the clauses of $F$ that contain $x$, let $N$ be those that contain $\neg x$, and let

$$R = \{(C \setminus \{x\}) \cup (D \setminus \{\neg x\}) : C \in P,\ D \in N\},$$

without the tautologies. Elimination replaces $F$ by $F' = (F \setminus (P \cup N)) \cup R$.

## Elimination preserves satisfiability

**Lemma 1 (soundness).** Every assignment that satisfies $F$ satisfies $F'$.

*Proof.* The clauses of $F \setminus (P \cup N)$ are in $F$. For a resolvent $E = (C \setminus \{x\}) \cup (D \setminus \{\neg x\})$, an assignment $\beta$ that satisfies $C$ and $D$ makes $x$ true or false. If $x$ is true, $D$ has a true literal other than $\neg x$, and it is in $E$. If $x$ is false, $C$ has a true literal other than $x$, and it is in $E$. $\square$

**Lemma 2 (extension).** Let $\beta$ satisfy $F'$. Set $x$ to false if every clause of $P$ has a true literal other than $x$ under $\beta$, and to true otherwise, and keep $\beta$ on every other variable. The result $\beta'$ satisfies $F$.

*Proof.* The clauses of $F \setminus (P \cup N)$ do not contain $x$, so $\beta'$ satisfies them as $\beta$ does. If $x$ is false under $\beta'$, every clause of $N$ is true through $\neg x$, and every clause of $P$ is true by the choice of the value. Otherwise some $C \in P$ has no true literal other than $x$, so $C \setminus \{x\}$ is false under $\beta$, and $x$ is true, so every clause of $P$ is true. Take any $D \in N$. If the resolvent $E$ of $C$ and $D$ is in $R$, then $\beta$ satisfies $E$, and since $C \setminus \{x\}$ is false, $D \setminus \{\neg x\}$ has a true literal. If $E$ is a tautology, it has a literal $y$ with $\neg y \in E$. Neither $C$ nor $D$ is a tautology, so one of $y$ and $\neg y$ is in $C \setminus \{x\}$ and the other is in $D \setminus \{\neg x\}$. The one in $C \setminus \{x\}$ is false, so the one in $D \setminus \{\neg x\}$ is true. In both cases $D$ is true under $\beta'$. $\square$

**Corollary.** $F$ is satisfiable if and only if $F'$ is satisfiable, and $x \notin \mathrm{var}(F')$.

The same holds for the two other rules. For a unit clause $\{\ell\}$ or a pure literal $\ell$, let $F' = F|\ell$: remove the clauses with $\ell$, and remove $\neg\ell$ from the others. If $\beta$ satisfies $F'$, then $\beta$ with $\ell$ made true satisfies $F$: the clauses with $\ell$ are true, and every other clause contains a clause of $F'$, which does not mention the variable of $\ell$. If $\beta$ satisfies $F$, then $\beta$ with $\ell$ made true satisfies $F'$: for a unit clause, $\beta$ already makes $\ell$ true, and for a pure literal, no clause of $F'$ contains the variable of $\ell$. Again the variable of $\ell$ is not in $\mathrm{var}(F')$.

## Correctness of the procedure

Let $F_0 = F, F_1, F_2, \ldots$ be the formulas after the steps of lines L4, L5 and L9.

**Theorem.** The procedure stops after at most $n$ steps. It returns UNSAT if and only if $F$ is unsatisfiable. When it returns SAT, the reconstruction gives a model of $F$.

*Proof.* Each step removes at least one variable from $\mathrm{var}(F_i)$ and adds none, by the corollary and the remark after it. So there are at most $n$ steps. The loop stops at line L2 or line L3, because a formula with no variable is $\emptyset$ or $\{\emptyset\}$.

By the corollary, all $F_i$ are satisfiable or all are not. If line L2 stops at $F_t$, then $F_t$ holds the empty clause, so $F_t$ and $F$ are unsatisfiable. If line L3 stops at $F_t = \emptyset$, then $F_t$ is satisfiable, and so is $F$.

For the model, the reconstruction starts from the assignment $\beta_t$ that makes every variable false, which satisfies $F_t = \emptyset$. It then goes through the steps in reverse. For step $i$, from $F_{i-1}$ to $F_i$, it changes only the variable of that step: it makes $\ell$ true for a unit or pure step, and it sets $x$ by the rule of Lemma 2 for an elimination. By the remark after the corollary and by Lemma 2, if $\beta_i$ satisfies $F_i$, then the new $\beta_{i-1}$ satisfies $F_{i-1}$. By induction, $\beta_0$ satisfies $F_0 = F$. $\blacksquare$

The value chosen for $x$ at step $i$ reads only variables of $P$ other than $x$. These variables are in $\mathrm{var}(F_{i-1})$, so none of them is the variable of a step before step $i$, which the reverse pass handles after step $i$. So their values do not change after $x$ is set, and the final assignment is $\beta_0$.

## Cost

A formula over $j$ variables with no tautology and no repeated clause has at most $3^j$ clauses, so $|P|, |N| \le 3^{n-1}$, and one elimination builds at most $9^{n-1}$ resolvents of at most $n$ literals each. With at most $n$ steps, the time is $O(n^2\, 9^n)$ and the space is $O(n\, 3^n)$. These bounds are crude, but the growth is real: by [Haken's theorem](/haken-resolution-lower-bound/), every resolution refutation of the pigeonhole formulas has exponential size, and an UNSAT run of the procedure contains a resolution refutation of $F$ (each resolvent is one resolution step, and each unit step is a sequence of resolution steps with the unit clause). $\blacksquare$
