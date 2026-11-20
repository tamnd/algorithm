---
title: The separation oracle of ellipsoid against hope always finds a violated dual constraint, and the profiles it finds support a correlated equilibrium once their cuts are infeasible
proves: [correctness]
status: full
---

The game has players $1, \ldots, n$ with finite strategy sets $S_i$ and utilities $u_i$. The dual vector $y \ge 0$ has one entry $y_i(j, l)$ for each player $i$ and ordered pair $j \ne l$ in $S_i$, and for a pure profile $s$,

$$g(y, s) = \sum_{i=1}^{n} \sum_{l \ne s_i} y_i(s_i, l)\,\big[u_i(s) - u_i(l, s_{-i})\big].$$

This is $(U^\top y)_s$, where $U$ is the matrix of the incentive constraints: a distribution $p$ on profiles is a correlated equilibrium exactly when $(Up)_{(i, j, l)} = \sum_{s : s_i = j} p(s)\,[u_i(s) - u_i(l, s_{-i})] \ge 0$ for every row. This is the definition, so the LP of line L8, with these rows, $\sum_{s \in X} p(s) = 1$ and $p \ge 0$, has as its feasible set exactly the correlated equilibria supported on $X$. In particular, an output of line L9 is a correlated equilibrium.

**Claim 1 (stationary distributions exist).** Let $r(j, l) \ge 0$ for $j \ne l$ in a finite set $S$. There is a distribution $x$ on $S$ with $x(j) \sum_{l \ne j} r(j, l) = \sum_{l \ne j} x(l)\, r(l, j)$ for every $j$.

*Proof.* Consider the directed graph on $S$ with an edge $j \to l$ when $r(j, l) > 0$. Its strongly connected components form an acyclic graph, which has a component $C$ with no edge leaving it. Let $\lambda$ be larger than every total rate $\sum_l r(j, l)$, and let $P(j, l) = r(j, l)/\lambda$ for $j \ne l$ and $P(j, j) = 1 - \sum_l r(j, l)/\lambda$, for $j, l \in C$. Because $C$ is closed, $P$ is a stochastic matrix, and it is irreducible because $C$ is strongly connected. So it has a stationary distribution $\pi$ with $\pi = \pi P$. Written out, $\pi = \pi P$ is $\lambda$ times the balance equations on $C$. Put $x = \pi$ on $C$ and $x = 0$ elsewhere. For $j \in C$, the balance equation holds because no state outside $C$ has positive mass. For $j \notin C$, both sides are 0: the left side because $x(j) = 0$, and the right side because a state $l$ with $x(l) > 0$ is in $C$, and $r(l, j) = 0$ for $l \in C$, $j \notin C$, since no edge leaves $C$. $\square$

The code computes exactly this distribution: it finds a closed class by reachability and solves the balance equations on it.

**Claim 2 (the product has zero expected dual value).** For each player $i$, let $x_i$ be a distribution given by Claim 1 for the rates $r = y_i$, and let $x = x_1 \times \cdots \times x_n$. Then $\mathbb{E}_{s \sim x}\, g(y, s) = 0$.

*Proof.* Fix $i$ and write $v_i(a) = \mathbb{E}_{s_{-i} \sim x_{-i}}\, u_i(a, s_{-i})$. Because $s_i$ is independent of $s_{-i}$ under $x$, the term of player $i$ has expectation

$$\sum_{j} x_i(j) \sum_{l \ne j} y_i(j, l)\,[v_i(j) - v_i(l)] = \sum_{a} v_i(a) \Big[x_i(a) \sum_{l \ne a} y_i(a, l) - \sum_{j \ne a} x_i(j)\, y_i(j, a)\Big],$$

where the second form collects the coefficient of each $v_i(a)$. Every bracket is 0 by Claim 1. Sum over $i$. $\square$

**Claim 3 (the oracle returns a violated constraint).** For every $y \ge 0$, the oracle of line L6 returns a pure profile $s$ with $g(y, s) \ge 0$.

*Proof.* For $0 \le m \le n$ and strategies $a_1, \ldots, a_m$, let $\varphi_m(a_1, \ldots, a_m)$ be the expectation of $g(y, (a_1, \ldots, a_m, s_{m+1}, \ldots, s_n))$ with $s_{m+1}, \ldots, s_n$ drawn independently from $x_{m+1}, \ldots, x_n$. Then $\varphi_0 = 0$ by Claim 2, and $\varphi_{m-1}(a_1, \ldots, a_{m-1}) = \sum_{a} x_m(a)\, \varphi_m(a_1, \ldots, a_{m-1}, a)$, an average. An average is at most the maximum, so the choice of the oracle, $a_m$ that maximizes $\varphi_m(a_1, \ldots, a_{m-1}, a)$, gives $\varphi_m(a_1, \ldots, a_m) \ge \varphi_{m-1}(a_1, \ldots, a_{m-1})$. By induction $g(y, (a_1, \ldots, a_n)) = \varphi_n \ge \varphi_0 = 0$. $\square$

Each $\varphi_m$ is a sum, with coefficients from $y$, of expectations of $u_i$ under product distributions in which the first $m$ players (and possibly player $i$) use point masses. So for a succinct game, the expected utility algorithm computes it.

**Claim 4 (every cut keeps the dual feasible set).** Let $D$ be the set of $z \ge 0$ with $g(z, s) \le -1$ for every profile $s$. Line L4 and line L7 never cut off a point of $D$.

*Proof.* Line L4 keeps the halfspace $z_r \ge 0$, which contains $D$. In line L7, every $z \in D$ has $g(z, s) \le -1 < 0 \le g(y, s)$ by Claim 3, so $z$ is in the kept halfspace $g(z, s) \le g(y, s)$; this uses that $g(\cdot, s)$ is linear. $\square$

**Claim 5 (infeasible cuts give an equilibrium on $X$).** Let $X$ be a set of profiles. If no $z \ge 0$ satisfies $g(z, s) \le -1$ for every $s \in X$, then a correlated equilibrium supported on $X$ exists, and the LP of line L8 is feasible.

*Proof.* The system is $A z \le b$, $z \ge 0$, where $A$ has the rows $(U^\top)_s$ for $s \in X$ and $b$ has all entries $-1$. By Farkas' lemma, in the form for nonnegative variables, this system is infeasible exactly when some $w \ge 0$ (one entry per $s \in X$) has $w^\top A \ge 0$ and $w^\top b < 0$. The second condition says $\sum_s w_s > 0$, and the first says $U w \ge 0$, with $w$ read as a vector on profiles that is 0 outside $X$. Then $p = w / \sum_s w_s$ is a distribution supported on $X$ with $Up \ge 0$, a correlated equilibrium. $\square$

**Claim 6 (existence).** Every finite game has a correlated equilibrium.

*Proof.* By Claim 3, for every $y \ge 0$ some profile $s$ has $g(y, s) \ge 0 > -1$, so the dual system over all profiles has no solution. Apply Claim 5 with $X$ the set of all profiles. $\square$

This is the existence proof of Hart and Schmeidler (1989) in the constructive form that the algorithm uses; Claim 6 shows that the dual $D$ is empty, so the method runs "against hope".

**Termination.** Papadimitriou and Roughgarden (2008), and Jiang and Leyton-Brown (2015) for the oracle with pure profiles, show that with a radius $R$ and a number of steps $N$ that are polynomial in $d$ and in the bit length of the entries of $U$, the cuts collected after $N$ steps form an infeasible system. In outline, the argument is the volume argument of the ellipsoid method: if the cuts of $X$ had a solution, then by the bounds on the bit lengths of the cut coefficients, the solutions of a slightly relaxed system would contain a ball, and every ellipsoid keeps this ball (as in Claim 4), but after $N$ steps the volume of the ellipsoid is smaller than the volume of the ball. This step count is cited and not proved here. Since each step adds at most one profile to $X$, $|X| \le N$, and by Claim 5 the LP of line L8 is then feasible.

**Conclusion.** The oracle always returns a profile whose dual constraint the center violates (Claims 1 to 3), so every cut is valid (Claim 4). Once the collected cuts are infeasible, which happens within a polynomial number of steps, the LP over the collected profiles has a solution (Claim 5), and every solution of that LP is a correlated equilibrium supported on $X$. The code stops at the first $X$ for which the LP is feasible, and it returns only a solution of that exact LP, so every output is an exact correlated equilibrium. $\blacksquare$
