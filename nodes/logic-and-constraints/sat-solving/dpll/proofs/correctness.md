---
title: DPLL returns a model exactly when the formula is satisfiable, and it makes at most 2^(n+1) - 1 calls
proves: [correctness, termination]
status: full
---

We use the recursive pseudocode of the page. The implementation runs the same calls in the same order, with an explicit stack of pending second branches. $F$ is a set of clauses, a clause is a set of literals, and no clause holds a literal and its negation (the implementation drops such clauses at the start, since they are true under every assignment). For a literal $\ell$, the formula $F|\ell$ is $F$ with every clause that contains $\ell$ removed and with $\neg\ell$ removed from every other clause. Let $\mathrm{var}(F)$ be the set of variables that occur in $F$. An assignment $\beta$ is a set of literals with no complementary pair, and $\beta$ satisfies $F$ when each clause of $F$ has a literal in $\beta$.

## Four facts about simplification

**Lemma 1.** Let $\ell$ be a literal and let $\beta$ be an assignment with $\ell \in \beta$. Then $\beta$ satisfies $F$ if and only if $\beta$ satisfies $F|\ell$. Also $\mathrm{var}(F|\ell) \subseteq \mathrm{var}(F) \setminus \{\mathrm{var}(\ell)\}$.

*Proof.* A clause with $\ell$ is satisfied by $\beta$ and is removed. For a clause $C$ without $\ell$, the literal $\neg\ell$ is false under $\beta$, so $\beta$ satisfies $C$ if and only if it satisfies $C \setminus \{\neg\ell\}$. The variable of $\ell$ is gone from every clause that is kept. $\square$

**Lemma 2 (unit clause).** If $\{\ell\} \in F$, then $F$ is satisfiable if and only if $F|\ell$ is satisfiable.

*Proof.* Every model of $F$ contains $\ell$, so by Lemma 1 it satisfies $F|\ell$. Conversely, let $\beta$ satisfy $F|\ell$. The variable of $\ell$ is not in $\mathrm{var}(F|\ell)$, so $\beta' = (\beta \setminus \{\neg\ell\}) \cup \{\ell\}$ also satisfies $F|\ell$, and by Lemma 1 it satisfies $F$. $\square$

**Lemma 3 (pure literal).** If $\ell$ occurs in $F$ and $\neg\ell$ does not, then $F$ is satisfiable if and only if $F|\ell$ is satisfiable.

*Proof.* If $\beta$ satisfies $F|\ell$, then $\beta'$ as in Lemma 2 satisfies $F$. Conversely, let $\beta$ satisfy $F$ and let $\beta' = (\beta \setminus \{\neg\ell\}) \cup \{\ell\}$. A clause with $\ell$ is satisfied by $\beta'$. A clause without $\ell$ also has no $\neg\ell$, because $\ell$ is pure, so its literals have the same values under $\beta$ and $\beta'$, and it is still satisfied. So $\beta'$ satisfies $F$, and by Lemma 1 it satisfies $F|\ell$. $\square$

**Lemma 4 (split).** For each literal $\ell$, $F$ is satisfiable if and only if $F|\ell$ or $F|\neg\ell$ is satisfiable.

*Proof.* A model of $F$ contains $\ell$ or $\neg\ell$, and Lemma 1 applies. Conversely, a model of $F|\ell$ or of $F|\neg\ell$ gives a model of $F$ as in the proof of Lemma 2. $\square$

## Correctness

**Theorem.** Let $F$ be a formula and $\alpha$ an assignment with no variable in $\mathrm{var}(F)$. If $F$ is satisfiable, DPLL$(F, \alpha)$ returns SAT and an assignment $\beta \supseteq \alpha$ that satisfies $F$. Otherwise it returns UNSAT.

*Proof.* By induction on $|\mathrm{var}(F)|$. The loops of lines L1 to L5 keep three facts: $\alpha$ is an assignment, no variable of $\alpha$ occurs in $F$, and the current $F$ is satisfiable if and only if the input $F$ is (Lemmas 2 and 3). Also, an assignment that contains the current $\alpha$ and satisfies the current $F$ satisfies the input $F$, by Lemma 1 applied step by step. The literal $\ell$ added at each step is free, because its variable occurs in $F$, so $\alpha \cup \{\ell\}$ is an assignment. Each step removes the variable of $\ell$ from $F$ (Lemma 1), so each loop runs at most $|\mathrm{var}(F)|$ times.

- **Line L3.** If the current $F$ has the empty clause, it is unsatisfiable, so the input $F$ is too, and UNSAT is correct.
- **Line L6.** If the current $F$ is empty, the current $\alpha$ satisfies it, so $\alpha$ satisfies the input $F$, and it contains the input $\alpha$.
- **Lines L7 to L9.** Otherwise $F$ is nonempty and has no empty clause, so $\ell$ exists, and $F|\ell$ and $F|\neg\ell$ have fewer variables than $F$. By induction, the call of line L8 returns a model of $F|\ell$ that contains $\alpha \cup \{\ell\}$ when $F|\ell$ is satisfiable, and this is a model of $F$ by Lemma 1. If $F|\ell$ is unsatisfiable, line L9 returns what the call on $F|\neg\ell$ returns, and by induction and Lemma 4 this is correct for $F$.

The base case $\mathrm{var}(F) = \emptyset$ means $F = \emptyset$ or $F = \{\emptyset\}$, and lines L3 and L6 handle it. $\blacksquare$

The top call is DPLL$(F, \emptyset)$. A variable of $x_1, \ldots, x_n$ that is not in the returned $\beta$ can take either value, and the implementation sets it to false.

## Termination and the number of calls

Each call makes at most two calls, on formulas with fewer variables. So the calls form a binary tree of depth at most $|\mathrm{var}(F)| \le n$, with at most $2^{n+1} - 1$ nodes. Each call does at most $n$ steps of lines L1 to L5, and each step builds $F|\ell$ in $O(|F|)$ time, so the total time is $O(2^n \cdot n \cdot |F|)$. $\blacksquare$
