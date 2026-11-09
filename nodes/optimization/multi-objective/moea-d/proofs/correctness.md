---
title: MOEA/D replacements never make a subproblem worse at the current reference point, a child replaces every neighbour it weakly dominates, and the external population is the front of all points evaluated
proves: [correctness]
status: full
---

All objectives are minimized, $p$ is the number of objectives, $N$ is the number of subproblems and of solutions, and line numbers refer to the `pseudo id=main` block of the MOEA/D page. For a weight vector $\lambda \ge 0$ and a point $z$, $g(x \mid \lambda, z) = \max_m \lambda_m \lvert f_m(x) - z_m \rvert$. We write $a \preceq b$ when $a$ weakly dominates $b$. MOEA/D is a heuristic; the statements below are about its update rules, not about reaching the Pareto front of a problem.

## The reference point

**Lemma 1.** After line L2 and after each run of line L6, $z_m$ is the smallest value of $f_m$ over all points evaluated so far. So $z \le f(x)$ in each coordinate for each evaluated $x$, and $g(x \mid \lambda, z) = \max_m \lambda_m (f_m(x) - z_m)$.

*Proof.* Line L2 sets $z$ to the minimum over the first population, and line L6 lowers $z_m$ to $f_m(y)$ when the new point $y$ is better. The second claim follows because $f_m(x) - z_m \ge 0$. $\square$

## Replacement

**Lemma 2.** Line L8 replaces $x^j$ by $y$ only when $g(y \mid \lambda^j, z) \le g(x^j \mid \lambda^j, z)$ for the current $z$. The number of solutions stays $N$.

*Proof.* This is the test of line L8, and each replacement puts one solution in place of one. $\square$

The value of a subproblem can still grow between generations, because $z$ moves: $g(x \mid \lambda, z)$ grows when $z_m$ falls in an objective with $\lambda_m > 0$ that attains the maximum.

**Theorem 3.** If $f(y) \preceq f(x^j)$ for some $j \in B(i)$, then line L8 replaces $x^j$ by $y$. In particular, if $f(y)$ dominates $f(x^j)$, the child replaces $x^j$.

*Proof.* By Lemma 1, after line L6 we have $z \le f(y) \le f(x^j)$. With $\lambda^j \ge 0$, each term satisfies $\lambda^j_m (f_m(y) - z_m) \le \lambda^j_m (f_m(x^j) - z_m)$, so the maxima satisfy $g(y \mid \lambda^j, z) \le g(x^j \mid \lambda^j, z)$, and line L8 replaces. $\square$

The converse fails: a child can replace a solution that it does not dominate, and it can replace several neighbours in one step. The example of the MOEA/D page has a child that replaces two of three neighbours, so two subproblems then hold the same solution.

## The external population

**Theorem 4.** After each run of line L9, $E$ is exactly the set of non-dominated images of all points evaluated so far, with no repeated image.

*Proof.* By induction. Line L2 builds $E$ by the same update from the first population. Let $E$ be the non-dominated images of the set $S$ evaluated before $y$, one copy each. If some $e \in E$ has $e \preceq f(y)$, line L9 leaves $E$ as it is: every image that $f(y)$ dominates is dominated by $e$, and $f(y)$ is either dominated or equal to $e$, so the non-dominated images of $S \cup \{f(y)\}$ are those of $S$. Otherwise no point of $S$ dominates $f(y)$: if $s \in S$ did, a non-dominated image $w \preceq s$ of $S$ would be in $E$ and would dominate $f(y)$. So $f(y)$ is non-dominated in $S \cup \{f(y)\}$, and the other non-dominated images are the members of $E$ that $f(y)$ does not dominate. Line L9 removes the others and adds $f(y)$. $\square$

Zhang and Li add $f(y)$ when no image of $E$ dominates it; with weak dominance in the test, as here, equal images are not repeated.

## The neighbourhoods

**Lemma 5.** Each $B(i)$ has $T$ distinct indices, contains $i$, and no index outside $B(i)$ has a weight vector strictly nearer to $\lambda^i$ than all of $B(i)$.

*Proof.* Line L1 sorts the indices by the distance of their weight vectors to $\lambda^i$, with $i$ first among those at distance $0$, and takes the first $T$. $\square$

## The weight vectors

**Lemma 6.** For $h \ge 1$, the vectors $\lambda \in \mathbb{R}^p$ with $\lambda_m \ge 0$, $\sum_m \lambda_m = 1$ and each $h \lambda_m$ an integer number $\binom{h + p - 1}{p - 1}$.

*Proof.* Multiply by $h$: these are the tuples of $p$ nonnegative integers with sum $h$, counted by placing $p - 1$ bars among $h + p - 1$ places. $\square$
