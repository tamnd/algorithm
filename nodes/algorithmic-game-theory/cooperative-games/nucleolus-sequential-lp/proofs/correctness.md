---
title: The sequential LP returns the nucleolus after at most n - 1 rounds
proves: [correctness]
status: full
---

Let $(N, v)$ be a TU game with players $N = \{1, \ldots, n\}$ and $v(\emptyset) = 0$. For a payoff vector $x \in \mathbb{R}^n$ write $x(S) = \sum_{i \in S} x_i$ and $e(S, x) = v(S) - x(S)$. Let $\mathcal{P}$ be the set of coalitions $S$ with $\emptyset \ne S \ne N$, and $m = |\mathcal{P}| = 2^n - 2$. The base set $X_0$ is the set of imputations, $\{x : x(N) = v(N),\ x_i \ge v(\{i\})\}$, or, in the prenucleolus mode, the set of preimputations $\{x : x(N) = v(N)\}$. For a set $\mathcal{F} \subseteq \mathcal{P}$ let $\theta_{\mathcal{F}}(x)$ be the vector of the numbers $e(S, x)$, $S \in \mathcal{F}$, sorted in nonincreasing order, and $\theta = \theta_{\mathcal{P}}$. The nucleolus $\nu$ is the point of $X_0$ with the lexicographically smallest $\theta$. Line L1 stops when $v(N) < \sum_i v(\{i\})$, because then there is no imputation. From now on $X_0 \ne \emptyset$. If $n = 1$, then $X_0 = \{v(N)\}$, $\mathcal{P} = \emptyset$, the rank test of line L3 fails at once, and line L10 returns $v(N)$. So let $n \ge 2$.

**Lemma 1 (the nucleolus exists and is unique; Schmeidler 1969).** The minimum of $\theta$ over $X_0$ exists and is attained at exactly one point.

*Proof.* Existence. Fix $x^0 \in X_0$ and let $K = \{x \in X_0 : \theta_1(x) \le \theta_1(x^0)\}$, where $\theta_1(x) = \max_{S \in \mathcal{P}} e(S, x)$. A point of $X_0$ outside $K$ is worse than $x^0$, so it suffices to minimize over $K$. On $K$, $e(\{i\}, x) \le \theta_1(x^0)$ gives $x_i \ge v(\{i\}) - \theta_1(x^0)$, and with $x(N) = v(N)$ this bounds every $x_i$ from above too. So $K$ is compact and nonempty. The $k$-th entry $\theta_k(x)$ is the $k$-th largest of $m$ continuous functions, so it is continuous. Let $K_0 = K$ and let $K_k$ be the set of minimizers of $\theta_k$ on $K_{k-1}$. Each $K_k$ is nonempty and compact, and $K_m$ is the set of lexicographic minimizers.

Uniqueness. Let $x \ne y$ both be minimizers, so $\theta(x) = \theta(y) = a$, and let $z = (x + y)/2 \in X_0$. Then $e(S, z) = (e(S, x) + e(S, y))/2$ for every $S$. List $\mathcal{P}$ as $S_1, \ldots, S_m$ with $e(S_j, z)$ nonincreasing. Any $k$ excesses at $x$ sum to at most $a_1 + \cdots + a_k$, and the same holds at $y$, so

$$\sum_{j \le k} \theta_j(z) = \tfrac12 \sum_{j \le k} e(S_j, x) + \tfrac12 \sum_{j \le k} e(S_j, y) \le \sum_{j \le k} a_j \quad \text{for every } k.$$

If $\theta(z) \ne a$, let $k$ be the first index with $\theta_k(z) \ne a_k$. The partial sums up to $k - 1$ are equal, so $\theta_k(z) < a_k$ and $z$ is lexicographically better than $x$, which is impossible. So $\theta(z) = a$, every inequality above is an equation, and so $\sum_{j \le k} e(S_j, x) = \sum_{j \le k} a_j$ for every $k$. Subtracting consecutive equations gives $e(S_k, x) = a_k$ for every $k$, and in the same way $e(S_k, y) = a_k$. So $x$ and $y$ have the same excess at every coalition in $\mathcal{P}$, in particular at every singleton, and $x = y$. $\square$

**Lemma 2 (common entries do not change the order).** Let $a, b$ be vectors of the same length and $c$ a third vector. Write $a \sqcup c$ for the concatenation. Then $\mathrm{sort}(a \sqcup c) \le_{\mathrm{lex}} \mathrm{sort}(b \sqcup c)$ if and only if $\mathrm{sort}(a) \le_{\mathrm{lex}} \mathrm{sort}(b)$, where sort means nonincreasing order.

*Proof.* For a vector $u$ let $C_u(\beta)$ be the number of entries $\ge \beta$. Let $\alpha = \mathrm{sort}(a)$ and $\gamma = \mathrm{sort}(b)$ differ first at position $k$, with $\alpha_k < \gamma_k$. For $\beta > \gamma_k$ the entries at positions $k$ and later are below $\beta$ in both vectors, and the entries before $k$ are equal, so $C_a(\beta) = C_b(\beta)$. At $\beta = \gamma_k$ we get $C_b(\gamma_k) \ge k$ and $C_a(\gamma_k) = k - 1$. So sorted vectors compare as follows: $\mathrm{sort}(a) <_{\mathrm{lex}} \mathrm{sort}(b)$ exactly when $C_a < C_b$ at the largest $\beta$ where $C_a$ and $C_b$ differ, and the sorted vectors are equal exactly when $C_a = C_b$. Since $C_{a \sqcup c} = C_a + C_c$ and $C_{b \sqcup c} = C_b + C_c$, the two differences are the same function, and the comparison does not change. $\square$

**The state.** At the start of each round the code holds three disjoint sets that cover $\mathcal{P}$: the fixed pairs $E$ (a coalition $S$ with its level $t_S$), the free set $\mathcal{F}$ and the dropped set $D$. Let $B$ be the span of $\mathbf{1}_N$ and the indicators $\mathbf{1}_S$, $S \in E$, and

$$X = \{x \in X_0 : e(S, x) = t_S \text{ for every } (S, t_S) \in E\}.$$

**Invariant.** At the start of each round:
1. $\nu \in X$;
2. every $S \in D$ has $\mathbf{1}_S \in B$, and no $S \in \mathcal{F}$ has $\mathbf{1}_S \in B$;
3. $\nu$ minimizes $\theta_{\mathcal{F}}$ over $X$.

A consequence of part 2: for $S \in E \cup D$ the excess $e(S, \cdot)$ is constant on $X$. For $S \in E$ this is the definition of $X$. For $S \in D$, write $\mathbf{1}_S = \lambda \mathbf{1}_N + \sum_{T \in E} \mu_T \mathbf{1}_T$; then $x(S) = \lambda v(N) + \sum_T \mu_T (v(T) - t_T)$ is the same for all $x \in X$.

*Start.* Line L2 sets $E = D = \emptyset$, $\mathcal{F} = \mathcal{P}$ and $X = X_0$. Part 1 holds by Lemma 1. For part 2, $B$ is the line of $\mathbf{1}_N$, and the indicator of a proper coalition has entries 0 and 1 and is not a multiple of $\mathbf{1}_N$. Part 3 is the definition of $\nu$.

**One round.** Let the invariant hold and let $\mathrm{rank}\,B < n$ (line L3).

*The free set is not empty.* The singleton indicators span $\mathbb{R}^n$, so some $\{i\}$ has $\mathbf{1}_{\{i\}} \notin B$. It is not in $E$ or $D$, whose indicators are in $B$, so it is in $\mathcal{F}$.

*The LP of line L4 has an optimum.* It minimizes $t$ over the pairs $(x, t)$ with $x \in X$ and $e(S, x) \le t$ for $S \in \mathcal{F}$. It is feasible, because $X$ contains $\nu$. If it were unbounded, there would be a direction $d$ with $d(N) = 0$, $d(T) = 0$ for $T \in E$ and $d(S) > 0$ for every $S \in \mathcal{F}$ (in the imputation mode $X$ is bounded, so this case does not arise there). By the consequence above, $d(S) = 0$ for $S \in D$. Take any $i$. The coalitions $\{i\}$ and $N \setminus \{i\}$ are both in $\mathcal{P}$, and $d(\{i\}) + d(N \setminus \{i\}) = d(N) = 0$. Neither value is negative, so both are 0, and $d_i = 0$. So $d = 0$, which contradicts $d(S) > 0$ on the nonempty $\mathcal{F}$. So the LP has an optimal value $t^*$, and

$$t^* = \min_{x \in X} \max_{S \in \mathcal{F}} e(S, x).$$

Let $X' = \{x \in X : e(S, x) \le t^* \text{ for all } S \in \mathcal{F}\}$, the set of optimal $x$. It is convex. The first entry of $\theta_{\mathcal{F}}(x)$ is $\max_{S \in \mathcal{F}} e(S, x)$, and $\nu$ minimizes $\theta_{\mathcal{F}}$ on $X$ (part 3), so it minimizes the first entry too: $\nu \in X'$.

*Lines L5 to L7 move exactly the set $M = \{S \in \mathcal{F} : e(S, x) = t^* \text{ for every } x \in X'\}$.* If the dual value of the row of $S$ is not zero, complementary slackness says that the row is tight at every optimal primal solution, because it holds between every primal optimum and every dual optimum; so $S \in M$. Otherwise line L6 maximizes $x(S)$ over $X'$. This LP is bounded: the complement $N \setminus S$ is in $\mathcal{P}$, and on $X'$ either its excess is at most $t^*$ (if it is free) or constant (if it is in $E \cup D$), so $x(S) = v(N) - x(N \setminus S)$ is bounded above. On $X'$ we have $e(S, x) \le t^*$, that is, $x(S) \ge v(S) - t^*$. So the maximum of $x(S)$ equals $v(S) - t^*$ exactly when $x(S) = v(S) - t^*$ on all of $X'$, that is, when $S \in M$. So line L7 moves $S$ if and only if $S \in M$.

*$M$ is not empty.* Suppose it is. Then for each $S \in \mathcal{F}$ there is $x^S \in X'$ with $e(S, x^S) < t^*$. Let $\bar x$ be the average of the points $x^S$. It is in $X'$ by convexity. For each $S \in \mathcal{F}$, $e(S, \bar x)$ is the average of the numbers $e(S, x^T)$, which are all $\le t^*$, and one of them, $e(S, x^S)$, is $< t^*$. So $e(S, \bar x) < t^*$ for every $S$ in the finite set $\mathcal{F}$, and $\max_{S \in \mathcal{F}} e(S, \bar x) < t^*$. This contradicts the definition of $t^*$.

*The rank grows.* Every $S \in M$ is in $\mathcal{F}$, so $\mathbf{1}_S \notin B$ by part 2. Adding the pairs $(S, t^*)$, $S \in M$, to $E$ therefore raises the rank of $B$ by at least 1.

*Lines L8 and L9* move to $D$ every remaining free coalition whose indicator is in the new span $B'$. Let $E'$, $\mathcal{F}'$, $D'$ and $X''$ be the new state, so $X'' = \{x \in X : e(S, x) = t^* \text{ for } S \in M\}$. We check the invariant.

Part 1: $\nu \in X'$, and every $S \in M$ has excess $t^*$ on $X'$, so $\nu \in X''$.

Part 2 holds by the construction of lines L8 and L9, since the old members of $D$ had indicators in $B \subseteq B'$.

Part 3. Take $y \in X''$. We show $\theta_{\mathcal{F}'}(\nu) \le_{\mathrm{lex}} \theta_{\mathcal{F}'}(y)$. Note that $X' \subseteq X''$, and that $\nu \in X'$ gives $e(S, \nu) \le t^*$ for all $S \in \mathcal{F}$.

- If $y \notin X'$, some $S \in \mathcal{F}$ has $e(S, y) > t^*$. This $S$ is not in $M$, where the excess is $t^*$ on $X''$. It is not in $D' \setminus D$ either, because there the excess is constant on $X''$ and so equals $e(S, \nu) \le t^*$. So $S \in \mathcal{F}'$, and the first entry of $\theta_{\mathcal{F}'}(y)$ is $> t^*$, while every entry of $\theta_{\mathcal{F}'}(\nu)$ is $\le t^*$. So $\nu$ is strictly better.
- If $y \in X'$, split $\mathcal{F} = M \cup (D' \setminus D) \cup \mathcal{F}'$. On $X''$ the excesses on $M$ are all $t^*$ and those on $D' \setminus D$ are constant, so $\nu$ and $y$ have the same entries there. Part 3 for the old state gives $\theta_{\mathcal{F}}(\nu) \le_{\mathrm{lex}} \theta_{\mathcal{F}}(y)$, since $y \in X' \subseteq X$. By Lemma 2 we may delete the common entries, which gives $\theta_{\mathcal{F}'}(\nu) \le_{\mathrm{lex}} \theta_{\mathcal{F}'}(y)$.

So the invariant holds at the start of the next round.

**Theorem.** The algorithm stops after at most $n - 1$ rounds and line L10 returns $\nu$.

*Proof.* The rank of $B$ starts at 1, grows by at least 1 in each round and never exceeds $n$, so line L3 ends the loop after at most $n - 1$ rounds. At the end $\mathrm{rank}\,B = n$, so the system $x(N) = v(N)$, $x(S) = v(S) - t_S$ for $(S, t_S) \in E$ has at most one solution. Every point of $X$ solves it, and $\nu \in X$ by part 1. So the system has exactly one solution, $\nu$, and line L10 returns it. In the imputation mode the bounds $x_i \ge v(\{i\})$ are not part of this system, but they hold at $\nu$ because $\nu \in X_0$. $\square$

**Remarks.**
- The levels $t^*$ do not increase from one round to the next. At the end of a round every free excess at $\nu$ is at most $t^*$, and $\nu$ is feasible for the next LP.
- The code writes the LP in the form of the shared simplex code, where every variable is nonnegative. In the imputation mode it uses $x_i = v(\{i\}) + y_i$ with $y_i \ge 0$, and in the prenucleolus mode $x_i = p_i - q_i$ with $p_i, q_i \ge 0$. The level is $t = t^+ - t^-$. All numbers are fractions, so the tests $t^* = $ value and dual $\ne 0$ are exact.
- The tests in `impl/python/test_nucleolus_sequential_lp.py` check the result against a brute force over a fine grid of imputations for 3 and 4 players, against Kohlberg's criterion for the prenucleolus (every set of coalitions with excess at least a given level is balanced), against the Talmud values, and the bound of $n - 1$ rounds.
