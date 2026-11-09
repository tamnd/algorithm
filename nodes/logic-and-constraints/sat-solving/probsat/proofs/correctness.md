---
title: probSAT returns only models, stops after a bounded number of flips, picks variables with the stated distribution, and without restarts finds a model of a satisfiable formula with probability 1
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $F$ is a CNF formula over $x_1, \ldots, x_n$ in which no clause repeats a literal or contains a literal and its negation, and $k$ is the largest clause size. The implementation removes repeated literals and tautological clauses first; this does not change the models. A formula with an empty clause has no model, and the implementation answers "no model found" at once.

The weight function is $f(b) = (\varepsilon + b)^{-c_b}$ with $\varepsilon > 0$ and $c_b \ge 0$ (the polynomial form), or $f(b) = c_b^{-b}$ with $c_b \ge 1$ (the exponential form). In both forms $f(b) > 0$ for every $b \ge 0$ and $f$ is non-increasing. It is strictly decreasing for $c_b > 0$ in the polynomial form and for $c_b > 1$ in the exponential form, and constant otherwise.

**Lemma 1 (the counts stay correct).** After the set-up of line L2 and after each flip of line L8, the number of true literals kept for each clause is correct, and the list of false clauses holds exactly the clauses that are false. The break count computed for $v$ is the number of clauses whose only true literal is on $v$, which is the number of true clauses that become false when $v$ is flipped.

*Proof.* The data structure and the update are the same as in [WalkSAT](/walksat/), and the proof of that page applies word for word: a flip of $v$ changes the true-literal count only of the clauses that contain $v$, by $+1$ or $-1$, and a clause enters or leaves the false list exactly when its count passes through 0. A true clause becomes false under the flip of $v$ exactly when its only true literal is on $v$. $\square$

**Lemma 2 (the distribution).** Let $C$ be the false clause of line L5, with variables $v_1, \ldots, v_r$. Line L7 flips $v_i$ with probability $f(\mathrm{break}(v_i)) / \sum_{j} f(\mathrm{break}(v_j))$. If $f$ is strictly decreasing, a variable with a smaller break count has a strictly larger probability, and variables with equal break counts have equal probabilities.

*Proof.* Line L6 computes $w_i = f(\mathrm{break}(v_i))$, which is correct by Lemma 1. All $w_i$ are positive, so the sum is positive and the quotients form a probability distribution, which line L7 samples. The second claim follows because the denominator is the same for all $i$. $\square$

**Theorem 1.**
1. If probSAT returns an assignment, it is a model of $F$.
2. probSAT stops after at most MAX-TRIES $\times$ MAX-FLIPS flips.
3. Each flip makes the chosen clause true.

*Proof.* (1) Line L4 returns $x$ only when the false list is empty, and by Lemma 1 no clause is then false. (2) Each try makes at most MAX-FLIPS flips, since the check of line L4 comes before each flip and the try ends when the budget is used, and there are at most MAX-TRIES tries. (3) The chosen clause is false, so all its literals are false, and the flipped variable is one of its variables, whose literal in $C$ becomes true. $\blacksquare$

**Theorem 2 (completeness in the limit).** Let $F$ be satisfiable, and let $q = f(B) / (k \, f(0))$, where $B$ is the largest number of clauses that contain one variable. Then a single try of probSAT with $tn$ flips misses every model with probability at most $(1 - q^n)^t$. So with unbounded MAX-FLIPS a single try finds a model with probability 1.

*Proof.* Fix a model $x^*$. Suppose the current $x$ is not a model, and let $C$ be the chosen false clause. Since $x^*$ satisfies $C$ and $x$ does not, some variable $v$ of $C$ has $x_v \ne x^*_v$. Every break count lies between 0 and $B$, and $f$ is non-increasing, so the weight of $v$ is at least $f(B)$, and the sum of the at most $k$ weights is at most $k f(0)$. So line L7 flips $v$ with probability at least $q$, and this flip lowers the Hamming distance from $x$ to $x^*$ by one. The distance is at most $n$, so from any state, the next $n$ flips reach a model with probability at least $q^n$; the walk may also stop earlier at some other model, which is fine. The flips of disjoint blocks of $n$ steps use fresh random choices, so the probability that $t$ blocks all fail is at most $(1 - q^n)^t$, which tends to 0 as $t$ grows. $\blacksquare$

The bound of Theorem 2 is very weak: $q^n$ is exponentially small. It only shows that probSAT cannot be trapped forever, a property that Hoos called probabilistic approximate completeness. It is not a running time bound.

**The case $c_b = 0$.** Then $f$ is constant and line L7 picks a uniformly random variable of $C$. This is the step of [Schöning's algorithm](/schoning-algorithm/), and the analysis of that page applies: with $q = 1/k$ toward a fixed model, one try of $3n$ flips from a random start succeeds with probability at least about $(k/(2(k-1)))^n$, up to a polynomial factor.

**What is not claimed.** probSAT is incomplete. If $F$ has no model, it reports "no model found" after all tries, which is not a proof. For $c_b > 0$, no bound on the expected number of flips better than the one of Theorem 2 is proved in general. The good speed of the tuned values is measured.
