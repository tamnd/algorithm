---
title: The finite state projection bound and its convergence
proves: [correctness]
status: full
---

Let the reachable states of a network be countable, ordered in some way, and let $A$ be the generator of the chemical master equation $\dot P = A P$: $A_{xx} = -a_0(x)$, $A_{yx} = \sum_{j : x + \nu_j = y} a_j(x)$ for $y \ne x$, and all other entries 0. So $A_{yx} \ge 0$ for $y \ne x$, and each column sums to 0. Assume that the jump process $X$ with these rates does not explode on $[0, t]$, so that $P(\cdot, s)$ is a probability vector for $s \le t$ and solves the master equation.

For a finite set $J$ of states, let $A_J$ be the submatrix of $A$ on the rows and columns in $J$, and let $p_J(s) = e^{A_J s} P_J(0)$, where $P_J(0)$ is the start distribution restricted to $J$.

**Lemma 1 ($e^{A_J s} \ge 0$).** Every entry of $e^{A_J s}$ is $\ge 0$ for $s \ge 0$.

*Proof.* Let $q = \max_{x \in J} a_0(x)$. Then $B = A_J + q I$ has entries $\ge 0$: off the diagonal they are those of $A$, and on the diagonal $q - a_0(x) \ge 0$. Since $qI$ commutes with $A_J$, $e^{A_J s} = e^{-qs} e^{Bs} = e^{-qs} \sum_{k \ge 0} (s B)^k / k!$, a sum of matrices with entries $\ge 0$. $\square$

**Theorem 1 (Munsky and Khammash 2006).** For every $x \in J$, $0 \le p_J(x, t) \le P(x, t)$, and

$$\sum_{x \in J} |P(x, t) - p_J(x, t)| + \sum_{x \notin J} P(x, t) = 1 - \sum_{x \in J} p_J(x, t).$$

So if $\sum_{x \in J} p_J(x, t) \ge 1 - \varepsilon$, the L1 error of $p_J$ (set to 0 outside $J$) is at most $\varepsilon$.

*Proof.* Split the states into $J$ and its complement $J'$. The rows of the master equation for the states in $J$ read

$$\dot P_J = A_J P_J + A_{J J'} P_{J'},$$

where $A_{JJ'}$ holds the rates from states outside $J$ into $J$. Its entries are $\ge 0$, and so are those of $P_{J'}$. Let $f(s) = A_{JJ'} P_{J'}(s) \ge 0$. By variation of constants,

$$P_J(t) = e^{A_J t} P_J(0) + \int_0^t e^{A_J (t - s)} f(s)\, ds.$$

By Lemma 1 the integrand has entries $\ge 0$, so $P_J(t) \ge e^{A_J t} P_J(0) = p_J(t)$ in every entry, and $p_J(t) \ge 0$ by Lemma 1 again. Then each term $|P(x, t) - p_J(x, t)|$ for $x \in J$ equals $P(x, t) - p_J(x, t)$, and the left side of the identity is $\sum_x P(x, t) - \sum_{x \in J} p_J(x, t) = 1 - \sum_{x \in J} p_J(x, t)$. $\square$

There is also a probabilistic reading: $p_J(x, t)$ is the probability that $X(t) = x$ and that $X$ stayed in $J$ during all of $[0, t]$. Mass that leaves $J$ is lost, even if the process could come back.

**Lemma 2 (larger sets give larger values).** If $J \subseteq K$, then $p_J(x, t) \le p_K(x, t)$ for $x \in J$.

*Proof.* Apply the proof of Theorem 1 with $K$ in place of the full space: the rows of $\dot p_K = A_K p_K$ for the states in $J$ are $\dot p_{K, J} = A_J p_{K, J} + A_{J, K \setminus J}\, p_{K, K \setminus J}$, with a forcing term $\ge 0$, so $p_{K, J}(t) \ge e^{A_J t} p_{K, J}(0) = p_J(t)$. $\square$

So the lost mass $1 - \sum_{x \in J} p_J(x, t)$ can only go down when $J$ grows.

**Theorem 2 (the loop stops).** Start the loop with $J_0 \ni x_0$ and the start law $\delta_{x_0}$, and let line L6 add every state that one reaction with a positive propensity reaches from $J$. For every $\varepsilon > 0$, the loop stops after finitely many rounds.

*Proof.* After $N$ rounds, $J_N$ contains every state that $X$ can reach from $x_0$ with at most $N$ reactions. On the event that $X$ makes at most $N$ jumps in $[0, t]$, the path stays in $J_N$. By the probabilistic reading above, $\sum_{x \in J_N} p_{J_N}(x, t) \ge \Pr(\text{at most } N \text{ jumps in } [0, t])$. Since $X$ does not explode, this probability tends to 1 as $N \to \infty$, so the lost mass drops below $\varepsilon$ for some finite $N$. $\square$

**Lemma 3 (uniformization in the code).** Let $q \ge \max_{x \in J} a_0(x)$, $q > 0$, and $Q = I + A_J / q$. Then $e^{A_J t} = \sum_{k \ge 0} e^{-qt} \frac{(qt)^k}{k!} Q^k$, every term has entries $\ge 0$, and cutting the series after any number of terms gives a vector $\le p_J(t)$ in every entry.

*Proof.* $Q = B / q$ with $B$ as in Lemma 1, and $e^{A_J t} = e^{-qt} e^{qt Q}$. The terms are $\ge 0$ because $Q \ge 0$ and $P_J(0) \ge 0$, so a partial sum is below the full sum. The code splits $t$ into pieces of length $\delta$ with $q \delta \le 10$ and uses $e^{A_J t} = (e^{A_J \delta})^{t / \delta}$. Each cut series gives a vector below the exact one, and applying the nonnegative matrix $e^{A_J \delta}$ to a smaller vector gives a smaller vector, so the computed result is still below $p_J(t)$. $\square$

So the mass that the code reports as lost, $1 - \sum p$, is at least the true lost mass of Theorem 1, and the bound of Theorem 1 still holds for the computed vector (up to rounding in floating point).
