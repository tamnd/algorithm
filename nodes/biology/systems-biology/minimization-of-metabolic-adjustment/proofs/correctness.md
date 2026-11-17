---
title: The active set enumeration returns the unique MOMA flux vector
proves: [correctness]
status: full
---

Fix an $n \times m$ matrix $S$, a wild-type vector $w \in \mathbb{Q}^m$, and mutant bounds $lb_j \le ub_j$ (entries may be infinite). Let $P = \{v : S v = 0, \; lb \le v \le ub\}$ and consider

$$\text{(MOMA)} \qquad \min_{v \in P} \; q(v) = \tfrac{1}{2} \|v - w\|^2 .$$

The factor $\frac{1}{2}$ does not change the minimizer. The claim is that the code returns the unique minimizer of (MOMA) if $P$ is not empty, and None if $P$ is empty.

**Lemma 1 (a unique minimizer).** If $P$ is not empty, (MOMA) has exactly one minimizer $v^*$.

*Proof.* $P$ is closed and convex. Pick $p \in P$. The set $P \cap \{v : \|v - w\| \le \|p - w\|\}$ is closed, bounded and not empty, so the continuous function $q$ has a minimizer on it, and this point minimizes $q$ on all of $P$. If $u \ne u'$ were two minimizers with value $q^*$, the midpoint $\frac{1}{2}(u + u')$ is in $P$, and $\|\frac{1}{2}(u + u') - w\|^2 = \frac{1}{2}\|u - w\|^2 + \frac{1}{2}\|u' - w\|^2 - \frac{1}{4}\|u - u'\|^2 < 2 q^*$, so its value is below $q^*$, a contradiction. $\square$

For a vector $v$ and multipliers $\lambda \in \mathbb{R}^n$, write $g = v - w + S^{\mathsf T} \lambda$. Say that $v$ is a KKT point if $v \in P$ and some $\lambda$ gives, for every $j$ with $lb_j < ub_j$: $g_j = 0$ if $lb_j < v_j < ub_j$, $g_j \ge 0$ if $v_j = lb_j$, and $g_j \le 0$ if $v_j = ub_j$. (For $lb_j = ub_j$ there is no condition on $g_j$.)

**Lemma 2 (KKT is necessary and sufficient).** A vector $v$ is the minimizer of (MOMA) if and only if it is a KKT point.

*Proof.* Sufficiency. Let $v$ be a KKT point with $\lambda$, and let $u \in P$. By convexity of $q$, $q(u) \ge q(v) + (v - w)^{\mathsf T}(u - v)$. Since $S u = S v = 0$, $(v - w)^{\mathsf T}(u - v) = g^{\mathsf T}(u - v)$. Each term $g_j (u_j - v_j)$ is non-negative: it is 0 if $g_j = 0$ or $lb_j = ub_j$ (then $u_j = v_j$); if $v_j = lb_j$ and $g_j \ge 0$, then $u_j - v_j \ge 0$; if $v_j = ub_j$ and $g_j \le 0$, then $u_j - v_j \le 0$. So $q(u) \ge q(v)$.

Necessity. Let $v = v^*$ be the minimizer. For every $u \in P$ and $\theta \in (0, 1]$, $v + \theta(u - v) \in P$, so $q(v + \theta (u - v)) \ge q(v)$, and letting $\theta \to 0$ gives $(v - w)^{\mathsf T} h \ge 0$ for every $h$ in the cone of feasible directions $D = \{h : S h = 0, \; h_j \ge 0 \text{ if } v_j = lb_j, \; h_j \le 0 \text{ if } v_j = ub_j, \; h_j = 0 \text{ if } lb_j = ub_j\}$. (Every $h \in D$ is a feasible direction: for small $\theta > 0$, $v + \theta h$ stays inside the bounds that are not tight.) So the linear program $\min \{(v - w)^{\mathsf T} h : h \in D\}$ has the optimum 0 at $h = 0$. By [LP duality](/lp-duality/) (Farkas' lemma), its dual is feasible: there are $\lambda$ and $\alpha_j \ge 0$ for the tight lower bounds, $\beta_j \ge 0$ for the tight upper bounds, and free $\gamma_j$ for the fixed reactions, with $v - w = -S^{\mathsf T} \lambda + \alpha - \beta + \gamma$, where each of $\alpha, \beta, \gamma$ is 0 outside its index set. Then $g = \alpha - \beta + \gamma$, which has the signs of the KKT conditions. $\square$

The code tries states: a state gives each reaction one of LOW, UP or FREE, where LOW needs a finite $lb_j$, UP a finite $ub_j$, and a fixed reaction ($lb_j = ub_j$) gets only LOW. Let $F$ be the free set of a state. Line L2 sets $v_j$ to its bound for $j \notin F$, line L3 sets $r = -\sum_{j \notin F} S_{\cdot j} v_j$, and line L4 solves

$$\begin{pmatrix} I & S_F^{\mathsf T} \\ S_F & 0 \end{pmatrix} \begin{pmatrix} x \\ \mu \end{pmatrix} = \begin{pmatrix} w_F \\ r \end{pmatrix} .$$

**Lemma 3 (the x part is unique).** If this system has a solution, all its solutions have the same $x$.

*Proof.* Let $(x, \mu)$ and $(x', \mu')$ be two solutions. Then $x - x' = -S_F^{\mathsf T}(\mu - \mu')$ is in the row space of $S_F$, and $S_F(x - x') = 0$, so it is in the null space of $S_F$. These two spaces are orthogonal, so $x - x' = 0$. $\square$

**Lemma 4 (soundness).** If the code returns $v$ at line L7, then $v$ is a KKT point, so $v = v^*$.

*Proof.* $S v = S_F x + \sum_{j \notin F} S_{\cdot j} v_j = r - r = 0$. The bounds hold for $j \notin F$ by line L2 and for $j \in F$ by the test of line L5, so $v \in P$. Line L6 accepts only if an LP in $\lambda$ is feasible, with the rows $g_j = 0$ for $j \in F$, $g_j \ge 0$ for LOW, $g_j \le 0$ for UP, and none for fixed reactions. A free reaction with $v_j$ at a bound has $g_j = 0$, which satisfies its condition. A LOW reaction has $v_j = lb_j$ and $g_j \ge 0$, and an UP reaction has $v_j = ub_j$ and $g_j \le 0$. So $v$ is a KKT point, and by Lemma 2 it is the minimizer, which is unique by Lemma 1. The LP of line L6 is decided correctly by solve_lp (Lemma 1 of the proof on the flux variability analysis page). $\square$

**Lemma 5 (completeness).** If $P$ is not empty, the code returns a vector.

*Proof.* Let $v^*$ be the minimizer, with KKT multipliers $\lambda^*$, $\alpha^*$, $\beta^*$, $\gamma^*$ from Lemma 2. Define the state $\sigma$: LOW for a fixed reaction; else LOW if $\alpha^*_j > 0$; else UP if $\beta^*_j > 0$; else FREE. ($\alpha^*_j > 0$ and $\beta^*_j > 0$ cannot both hold for $lb_j < ub_j$, since $v^*_j$ cannot be at both bounds.) This state is in the list. For it, line L2 sets each non-free $v_j$ to $v^*_j$, so $r = S_F v^*_F$. For $j \in F$, $g^*_j = 0$, that is, $v^*_j - w_j + (S_F^{\mathsf T} \lambda^*)_j = 0$. So $(x, \mu) = (v^*_F, \lambda^*)$ solves the system of line L4, and by Lemma 3 solve_linear returns a solution with $x = v^*_F$. Then $v = v^* \in P$ passes line L5, and $\lambda^*$ is a feasible point of the LP of line L6. So if the loop reaches $\sigma$, it returns there, and if it returns earlier, it returns a vector too. $\square$

**Theorem.** moma returns the unique minimizer of (MOMA) if $P$ is not empty, and None if $P$ is empty.

*Proof.* If $P$ is not empty, Lemma 5 says that the code returns some $v$, and Lemma 4 says that $v = v^*$. If $P$ is empty, every vector that passes lines L5 and L6 would be in $P$ by the proof of Lemma 4, so none passes and the code returns None at line L8. The order of the states (most free reactions first) changes only the running time. $\square$

**Remark (cost).** The number of states is at most $3^m$, and each needs one linear system of size $|F| + n$ and one small LP. This is meant for toy networks and for checking a QP solver. On genome-scale networks, (MOMA) is solved by a convex quadratic programming solver, which needs no enumeration.
