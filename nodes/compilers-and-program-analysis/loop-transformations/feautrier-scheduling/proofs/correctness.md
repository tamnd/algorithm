---
title: Feautrier's greedy algorithm terminates and returns a legal multidimensional schedule
proves: [correctness]
status: full
---

**Setting.** We use the notation of the page. The program is a static control program with integer parameters $N$ in the context $K$. Statement $S$ has depth $d_S$ and a domain $D_S$, a polyhedron that is bounded for each $N$, on which every loop counter is nonnegative. Each edge $e : S \to T$ of the input set $E_0$ has a nonempty polyhedron $P_e$, given by affine constraints $c_{e,i}(\vec{s}, \vec{t}, N) \ge 0$ that include the domains and the context. The edges are the memory-based dependences of the program, split by depth, as on the page: at depth $l$ the constraints contain $s_k = t_k$ for $k < l$ and $t_l - s_l - 1 \ge 0$; at the "same iteration" depth they contain $s_k = t_k$ for all common loops, and $S$ comes before $T$ in the text of the innermost common loop. For an affine form $\theta$ per statement and an edge $e$, write $\Delta_e\theta(\vec{s}, \vec{t}) = \theta_T(\vec{t}) - \theta_S(\vec{s})$.

**Claim.** The algorithm stops after at most $|E_0|$ rounds. The list $\Theta$ it returns satisfies $\Theta_S(\vec{s}) <_{\mathrm{lex}} \Theta_T(\vec{t})$ for every $e \in E_0$, every $N \in K$ and every integer pair $(\vec{s}, \vec{t}) \in P_e$. If some affine $\theta$ with $\theta_S \ge 0$ on every $D_S$ strongly satisfies every edge of $E_0$, the list has one dimension.

### Step 1: the linear constraints say what they should

**Lemma 1 (affine Farkas lemma).** Let $P = \{x : c_i(x) \ge 0,\ i = 1, \dots, m\}$ be a nonempty polyhedron, with affine $c_i$. An affine form $\psi$ is nonnegative on all of $P$ if and only if $\psi \equiv \lambda_0 + \sum_i \lambda_i c_i$ for some $\lambda_0, \dots, \lambda_m \ge 0$.

This is Corollary 7.1h of Schrijver's book. The "if" part is direct: each term is nonnegative on $P$. $\square$

The variables of $P_e$ are $\vec{s}$, $\vec{t}$ and $N$. The identity in Lemma 1 holds for all values of these variables, so it is equivalent to the equality of the coefficients of each variable and of the constants. The coefficients of $\Delta_e\theta - \varepsilon_e$ are linear in the unknown coefficients of $\theta$ and in $\varepsilon_e$, so line L4 adds linear equations in the unknowns $\theta$, $\varepsilon$ and $\lambda$, with $\lambda \ge 0$. By Lemma 1, a vector of unknowns satisfies them if and only if $\Delta_e\theta \ge \varepsilon_e$ on $P_e$. In the same way, the constraints of line L3 hold if and only if $\theta_S \ge 0$ on the polyhedron of $D_S$ and $K$ for each $S$. When both $c$ and $-c$ are constraints, the implementation uses one free multiplier for the pair; this is the same as the difference of two nonnegative ones.

### Step 2: the first linear program returns 0 or 1

Let $E$ be the current set of edges and let $F$ be the set of feasible points of line L4: affine $\theta$ with $\theta_S \ge 0$ on each $D_S$, and $0 \le \varepsilon_e \le 1$ with $\Delta_e\theta \ge \varepsilon_e$ on $P_e$ for $e \in E$.

**Lemma 2.** At every optimal point of line L5, every $\varepsilon_e$ is 0 or 1.

*Proof.* Let $(\theta, \varepsilon)$ be optimal and suppose some $\varepsilon_e$ lies strictly between 0 and 1. Let $\mu$ be the least positive $\varepsilon_e$; then $0 < \mu < 1$. Set $\theta' = \theta / \mu$ and $\varepsilon'_e = 1$ if $\varepsilon_e > 0$ and $\varepsilon'_e = 0$ otherwise. Then $\theta'_S \ge 0$ on $D_S$. For an edge with $\varepsilon_e > 0$, $\Delta_e\theta' = \Delta_e\theta / \mu \ge \varepsilon_e / \mu \ge 1$ on $P_e$. For an edge with $\varepsilon_e = 0$, $\Delta_e\theta' \ge 0$. So $(\theta', \varepsilon') \in F$. Its objective is the number of positive $\varepsilon_e$, which is larger than $\sum_e \varepsilon_e$, because one term is less than 1. This contradicts optimality. $\square$

So the set $G = \{e : \varepsilon_e = 1\}$ of line L5 is a set of edges that one feasible $\theta$ strongly satisfies, while it weakly satisfies all of $E$. By Lemma 2, the optimal value is the largest size of such a set.

### Step 3: the chosen dimension is correct

**Lemma 3.** The dimension appended at line L7 weakly satisfies every edge of $E$, strongly satisfies every edge of $G$, and is nonnegative on every domain.

*Proof.* Line L6 solves the constraints of Step 1 with $\varepsilon_e$ fixed to 1 on $G$ and to 0 on $E \setminus G$. This system is feasible, because the optimum of line L5 satisfies it. Its objective is a weighted sum of absolute values, bounded below by 0, so an optimum exists. By Step 1, its $\theta$ has $\Delta_e\theta \ge 1$ on $P_e$ for $e \in G$, $\Delta_e\theta \ge 0$ for $e \in E$, and $\theta_S \ge 0$ on $D_S$. Line L7 multiplies every $\theta_S$ by the same integer $D \ge 1$. This multiplies each $\Delta_e\theta$ by $D$, so the three properties stay true, and the coefficients become integers. $\square$

### Step 4: every round removes an edge

Let $\Omega_S(\vec{s}) = (\beta^S_0, s_1, \beta^S_1, \dots, s_{d_S}, \beta^S_{d_S})$ be the original schedule vector of $S$, where $\beta^S_k \ge 0$ is the text position at depth $k$. Its components are affine in $\vec{s}$ and nonnegative on $D_S$, because the counters are nonnegative. For an edge $e$ with $c$ common loops, define its *position* $\pi(e)$: if $e$ has depth $l$, then $\pi(e) = 2l$, the place of the counter $s_l$; if $e$ is a "same iteration" edge, then $\pi(e) = 2c + 1$, the place of $\beta_c$. Number the components from 1.

**Lemma 4.** For an edge $e$ and every $(\vec{s}, \vec{t}) \in P_e$, the components $q < \pi(e)$ of $\Omega_S(\vec{s})$ and $\Omega_T(\vec{t})$ are equal, and component $\pi(e)$ of $\Omega_T(\vec{t})$ exceeds that of $\Omega_S(\vec{s})$ by at least 1.

*Proof.* The components before $\pi(e)$ are $\beta_0, s_1, \dots, \beta_{l-1}$ (or up to $s_c$). The text positions $\beta_k$ for $k < c$ are equal, because the two statements share these loops. The counters before depth $l$ are equal by the constraints of $P_e$. At position $2l$, $t_l - s_l \ge 1$ by the constraints. At position $2c + 1$, $\beta^T_c - \beta^S_c \ge 1$, because these are different integers and $S$ comes first. $\square$

**Lemma 5.** If $E$ is not empty, the set $G$ of line L5 is not empty.

*Proof.* Let $p = \min_{e \in E} \pi(e)$, and let $e^\ast$ reach the minimum. Every edge $e \in E$ has $\pi(e) \ge p$, and $p \le \pi(e) \le 2c_e + 1$, so component $p$ belongs to the common prefix of the two statements of $e$, where both vectors have the same kind of entry. Define $\theta_S$ as component $p$ of $\Omega_S$ for every statement that has one, and as $0$ for the others. Then $\theta_S \ge 0$ on $D_S$. By Lemma 4, $\Delta_e\theta = 0$ on $P_e$ if $\pi(e) > p$, and $\Delta_e\theta \ge 1$ on $P_e$ if $\pi(e) = p$. So $\theta$, with $\varepsilon_{e^\ast} = 1$ and the other $\varepsilon_e = 0$, is feasible with objective at least 1. The optimum of line L5 is then at least 1, and by Lemma 2 it is a whole number of edges with $\varepsilon_e = 1$, so $G \ne \emptyset$. $\square$

### Step 5: conclusion

*Termination.* By Lemma 5, line L8 removes at least one edge in each round, so the loop runs at most $|E_0|$ times.

*Legality.* Take $e \in E_0$ and let $r$ be the round that removes it. For each round $q < r$, $e$ was in $E$, so by Lemma 3 the dimension $\theta^q$ weakly satisfies $e$: $\Delta_e\theta^q \ge 0$ on $P_e$. The dimension $\theta^r$ strongly satisfies it: $\Delta_e\theta^r \ge 1$. So for every $(\vec{s}, \vec{t}) \in P_e$, the vector $\Theta_T(\vec{t}) - \Theta_S(\vec{s})$ has nonnegative entries up to place $r$ and a positive entry at place $r$. Its first nonzero entry is at some place $q \le r$ and is positive, so $\Theta_S(\vec{s}) <_{\mathrm{lex}} \Theta_T(\vec{t})$.

*One dimension.* If an affine $\theta$ with $\theta_S \ge 0$ on each $D_S$ strongly satisfies every edge of $E_0$, then $\theta$ with every $\varepsilon_e = 1$ is feasible in the first round, and its objective $|E_0|$ is the largest possible. So $G = E_0$, and the loop stops after one round.

*Completeness of the edges.* Every pair of instances that touch the same element, with at least one write, and with $S(\vec{s})$ before $T(\vec{t})$ in the original order, satisfies the constraints of exactly one depth for the pair of accesses involved, by the definition of the lexicographic order of $\Omega$. So it lies in some $P_e$, and the schedule keeps its order. Instances with equal time vectors are therefore independent, and they may run in any order or in parallel. $\blacksquare$
