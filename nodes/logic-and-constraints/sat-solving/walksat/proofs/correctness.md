---
title: WalkSAT returns only models, stops after a bounded number of flips, keeps its counts correct, and each freebie move increases the number of true clauses
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $F$ is a CNF formula over $x_1, \ldots, x_n$ in which no clause repeats a literal or contains a literal and its negation. The implementation removes repeated literals and tautological clauses first; this does not change the models. A formula with an empty clause has no model, and the implementation answers "no model found" at once.

**Data.** For the current assignment $x$, the implementation keeps, for each clause $C_j$, the number $t_j$ of true literals of $C_j$, and the list $L$ of the indices $j$ with $t_j = 0$, with the position of each such $j$ in $L$. For a variable $v$, $\mathrm{break}(v)$ is the number of clauses that are true under $x$ and false under $x$ with $v$ flipped.

**Lemma 1 (the counts stay correct).** After the set-up of line L2 and after each flip of line L9, $t_j$ is the number of true literals of $C_j$ for each $j$, and $L$ holds exactly the indices of the false clauses.

*Proof.* Line L2 computes $t_j$ directly and puts each $j$ with $t_j = 0$ in $L$. Suppose the claim holds before a flip of $v$. A clause without $v$ keeps its literals and its count. A clause $C_j$ with $v$ has exactly one literal $\ell$ on $v$. If $\ell$ becomes true, $t_j$ grows by 1; if $t_j$ was 0, the clause was in $L$ and is now true, and the implementation removes it from $L$ by moving the last entry of $L$ into its place and updating the position of that entry. If $\ell$ becomes false, $t_j$ drops by 1; if it drops to 0, the clause is now false, and the implementation appends it to $L$. No other clause changes its value. So the claim holds after the flip. $\square$

**Lemma 2 (the break count).** $\mathrm{break}(v)$ is the number of clauses $C_j$ with $t_j = 1$ whose true literal is on $v$.

*Proof.* Flipping $v$ changes only the literal of $v$ in each clause. A true clause becomes false exactly when its only true literal turns false, that is, when $t_j = 1$ and that literal is on $v$. A clause with $t_j \ge 2$ keeps a true literal on another variable. $\square$

The method `break_count` counts exactly these clauses, using the counts of Lemma 1.

**Lemma 3 (freebie moves).** Let $C$ be a false clause and let $v$ be a variable of $C$ with $\mathrm{break}(v) = 0$. Flipping $v$ increases the number of true clauses by at least one.

*Proof.* Since $C$ is false, the literal of $v$ in $C$ is false, and the flip makes it true, so $C$ becomes true. By $\mathrm{break}(v) = 0$, no true clause becomes false. $\square$

**Theorem.**
1. If WalkSAT returns an assignment, it is a model of $F$.
2. WalkSAT stops after at most MAX-TRIES $\times$ MAX-FLIPS flips.
3. Each flip makes the chosen clause $C$ true, and the variable flipped is in $C$.

*Proof.* (1) Line L4 returns $x$ only when $L$ is empty, and by Lemma 1 this means that no clause is false. (2) The loop of line L1 runs at most MAX-TRIES times, and each try makes at most MAX-FLIPS flips, since the check of line L4 comes before each flip and the try ends when the flip budget is used. (3) Line L5 takes an index from $L$, so by Lemma 1 the clause $C$ is false and all its literals are false. Lines L6, L7 and L8 each return a variable of $C$, and flipping it makes its literal in $C$ true. $\blacksquare$

**Relation to Schöning's walk.** If the freebie rule of line L6 is removed and the noise is $p = 1$, each flip picks a uniformly random literal of a random false clause. This is the step of [Schöning's algorithm](/schoning-algorithm/), whose analysis shows that for any fixed model $x^*$ each flip moves toward $x^*$ with probability at least $1/k$. With the freebie rule and the greedy rule of line L8 this coupling argument no longer applies, because the greedy choice can be the one variable of $C$ that agrees with $x^*$.

**What is not claimed.** WalkSAT is incomplete. If $F$ has no model, it reports "no model found" after all tries, which is not a proof. If $F$ has a model, no general bound on the probability of finding it is proved for the SKC rule with noise $p < 1$. Its success on random and structured formulas is measured by experiment.
