---
title: What the feasibility pump guarantees
proves: [correctness]
status: full
---

**Statement.** Let $P = \{x \ge 0 : A x \le b,\ x_j \le 1\ (j \in I)\}$ and let $S = \{x \in P : x_j \in \{0,1\}\ (j \in I)\}$ be the feasible set of the 0-1 program. Then FEASIBILITY-PUMP stops after at most $N + 1$ linear programs, and:

1. each point it returns lies in $S$;
2. it returns INFEASIBLE only if $S$ is empty;
3. if, at line L5, the vector $\tilde{x}$ equals $z_I$ for some $z \in S$, then line L6 returns a point of $S$ in the same iteration;
4. if iteration $k - 1$ ends with the rounding move of line L9 and iteration $k$ reaches line L5, then $\Delta(x^*_k, \tilde{x}_k) \le \Delta(x^*_{k-1}, \tilde{x}_{k-1})$, where $x^*_k$ and $\tilde{x}_k$ are the points of line L5 in iteration $k$.

**Lemma 1.** For $x \in P$ and $\tilde{x} \in \{0,1\}^I$, $\Delta(x, \tilde{x}) = \sum_{j \in I} |x_j - \tilde{x}_j| \ge 0$, and $\Delta(x, \tilde{x}) = 0$ if and only if $x_j = \tilde{x}_j$ for all $j \in I$.

*Proof.* For $j \in I$ we have $0 \le x_j \le 1$. If $\tilde{x}_j = 0$ then $|x_j - \tilde{x}_j| = x_j$, and if $\tilde{x}_j = 1$ then $|x_j - \tilde{x}_j| = 1 - x_j$. Summing gives the formula. A sum of nonnegative terms is 0 exactly when each term is 0. $\square$

**Lemma 2.** Line L5 is well defined: when $P$ is not empty, the linear program $\min\{\Delta(x, \tilde{x}) : x \in P\}$ has an optimal solution.

*Proof.* The objective is a linear function of $x$ plus a constant, and by Lemma 1 it is bounded below by 0 on $P$. A linear program that is feasible and bounded has an optimal solution, and the simplex method finds one. $P$ is not empty at line L5, because line L1 returned otherwise. $\square$

**Lemma 3.** For a fixed $x \in P$, the rounding $[x]$ minimizes $\Delta(x, \tilde{x})$ over $\tilde{x} \in \{0,1\}^I$.

*Proof.* By Lemma 1 the distance is a sum of one term for each $j \in I$, and the term for $j$ depends only on $\tilde{x}_j$. The term is $x_j$ for $\tilde{x}_j = 0$ and $1 - x_j$ for $\tilde{x}_j = 1$. The rounding chooses $\tilde{x}_j = 1$ exactly when $x_j \ge 1/2$, that is, when $1 - x_j \le x_j$. So each term is at its minimum, and so is the sum. $\square$

**Proof of the statement.**

*Termination.* Line L1 solves one linear program. Each pass through the loop increases $k$ by exactly 1 at line L5 and solves one linear program, and the loop runs only while $k < N$. So there are at most $N$ passes and at most $N + 1$ linear programs. Lines L7 to L10 do a finite amount of work.

*Part 1.* A point is returned only at line L2 or line L6, and only when it is integer. It comes from line L1 or line L5, so it lies in $P$. A point of $P$ that is integer lies in $S$ by the definition of $S$.

*Part 2.* INFEASIBLE is returned only at line L1, when $P$ is empty. Since $S \subseteq P$, the set $S$ is empty too.

*Part 3.* Let $z \in S$ with $z_I = \tilde{x}$. Then $z \in P$ and $\Delta(z, \tilde{x}) = 0$ by Lemma 1. By Lemma 1 the optimal value of line L5 is at least 0, so it is exactly 0, and the point $x^*$ of line L5 has $\Delta(x^*, \tilde{x}) = 0$. By Lemma 1, $x^*_j = \tilde{x}_j \in \{0,1\}$ for each $j \in I$. So $x^*$ is integer, and line L6 returns it. By Part 1 it lies in $S$.

*Part 4.* A rounding move in iteration $k - 1$ sets $\tilde{x}_k = [x^*_{k-1}]$. By Lemma 3, $\Delta(x^*_{k-1}, \tilde{x}_k) \le \Delta(x^*_{k-1}, \tilde{x}_{k-1})$. The point $x^*_{k-1}$ lies in $P$, and $x^*_k$ minimizes $\Delta(\cdot, \tilde{x}_k)$ over $P$, so $\Delta(x^*_k, \tilde{x}_k) \le \Delta(x^*_{k-1}, \tilde{x}_k)$. Together these give the claim. $\blacksquare$

**What is not claimed.** The statement gives no bound on the number of iterations that the pump needs to find a point of $S$, and FAIL does not imply that $S$ is empty. Part 3 says only that the pump stops once its 0-1 vector agrees with a feasible point; it does not say that this ever happens. Deciding whether $S$ is empty is NP-complete, so no polynomial time method of this kind can give such a guarantee unless P = NP.
