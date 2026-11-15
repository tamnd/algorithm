---
title: QSIM is sound but not complete
proves: [correctness, soundness, incompleteness, termination]
status: full
---

This proof follows Kuipers (Artificial Intelligence 29(3), 1986): Section 2 for the qualitative description of a function, Appendix A for the transitions of Table 1, Appendix B for the constraints, and Section 5 for Theorem 5.2 (soundness) and Theorem 5.3 (spurious behaviors). It checks that each step of the implementation keeps what Kuipers's argument needs.

## Setting

A *reasonable function* $f : [a, b] \to \overline{\mathbb{R}}$ is continuous, continuously differentiable on $(a, b)$, has finitely many critical points in each bounded interval, and has one-sided limits of $f'$ at $a$ and $b$ (Kuipers, Definition 2.1). Each variable $f$ has a quantity space: a finite ordered list of landmark values that contains $0$, $-\infty$ and $+\infty$. The *qualitative state* of $f$ at a time $t$ is the pair $(q, d)$, where $q$ is the landmark $f(t)$ if $f(t)$ is a landmark, and else the open interval between two adjacent landmarks that contains $f(t)$, and $d$ is inc, std or dec as $f'(t)$ is positive, zero or negative. The *distinguished time points* of a system are the times where some variable reaches a landmark or has a critical point; between two adjacent distinguished time points every qualitative state is constant (Kuipers, Section 2). A *solution* is a tuple of reasonable functions that satisfies the constraints at every time. Its *qualitative behavior* is the alternating sequence of the qualitative states of the system at the distinguished time points and on the open intervals between them.

## Lemma 1 (Table 1 lists every successor of one function)

Let $f$ be reasonable, let $t_i < t_{i+1}$ be adjacent distinguished time points, and let $f$ stay finite. If $f$ has state $(q, d)$ at $t_i$, its state on $(t_i, t_{i+1})$ is one of the P transitions of Table 1 for $(q, d)$. If $f$ has state $(q, d)$ on $(t_i, t_{i+1})$, its state at $t_{i+1}$ is one of the I transitions of Table 1 for $(q, d)$, where a value strictly inside the interval is a new landmark (I8 and I9).

*Proof.* This is Kuipers, Propositions A.1, A.2, A.4 and A.5. For the point to interval step: if $f(t_i) = l_j$ and $f'(t_i) > 0$, then $f$ increases just after $t_i$, so it lies in $(l_j, l_{j+1})$ and is increasing on the interval (P4); the case $f'(t_i) < 0$ is P6. If $f'(t_i) = 0$, then on the next interval $f$ is constant (P1), or increasing (P2), or decreasing (P3), since $f'$ has no zero inside the interval. If $f(t_i)$ is inside an interval, $f$ stays in it on the open interval after $t_i$ and keeps the sign of $f'$ there (P5 and P7; a zero derivative is P1 on a landmark only, since a constant value inside an interval is not a landmark). For the interval to point step: an increasing $f$ in $(l_j, l_{j+1})$ reaches at $t_{i+1}$ either $l_{j+1}$, with derivative zero (I2) or positive (I3), or stays inside the interval, with positive derivative (I4) or with derivative zero at a new critical value (I8), which becomes a landmark. The decreasing cases I5, I6, I7 and I9 are symmetric, and a constant $f$ stays constant (I1). $\square$

The function `transitions` returns exactly these lists, and the test `test_table1_counts` checks their sizes. It then removes the moves whose value is $-\infty$ or $+\infty$ (a No Divergence restriction; Kuipers discusses divergence to infinity in Appendix A). This removes nothing for a solution whose values stay finite.

## Lemma 2 (the constraint test accepts every real tuple)

Let a solution be at a time $t$, and let the arguments of a constraint have the states $(q_k, d_k)$ there. Then `constraint_ok` accepts these states, with the corresponding values recorded so far.

*Proof.* For each kind, the test is a consequence of the real relation.

- **DERIV(f, g)**, $g = f'$: the sign of $f'(t)$ is the sign of $g(t)$, that is, the direction of $f$ equals the sign of the value of $g$ against the landmark 0. This is the test `ds[0] == s(1, "0")` (Kuipers, Definition 3.4).
- **CONSTANT(f)**: $f' = 0$, so the direction is std.
- **M+(f, g)**, $f = H(g)$ with $H$ continuously differentiable and $H' > 0$: $f' = H'(g) g'$ has the sign of $g'$, so the directions are equal. For a pair $(p, q)$ of corresponding values, $H(q) = p$, and $f - p = H(g) - H(q)$ has the sign of $g - q$ because $H$ is strictly increasing (Kuipers, Definition 3.5 and Proposition B.6 to B.8). M- and MINUS are the same with the signs reversed.
- **ADD(f, g, h)**, $f + g = h$: $f' + g' = h'$, and for corresponding values $(p, q, r)$ with $p + q = r$ we have $(f - p) + (g - q) = h - r$ (Kuipers, Proposition B.3). Two reals with signs $a$ and $b$ have a sum whose sign is $a$ if $a = b$ or $b = 0$, is $b$ if $a = 0$, and is any sign if $a = -b \ne 0$. The function `_add_ok` accepts exactly these triples, so it accepts the true signs.

A new landmark lies strictly inside the interval of its placeholder, and `_as_interval` tests it as that interval. Its sign against every old landmark is then the true sign. Corresponding values are added only when all arguments are at landmarks (`initial_state` and line L8), and then they are true values of the solution, so later tests use only true facts. $\square$

## Lemma 3 (Waltz filtering and the search lose no global interpretation)

Call a choice of one candidate per variable a *global interpretation* if, for each constraint, the tuple of its arguments is accepted by line L5. Then lines L6 and L7 return exactly the global interpretations.

*Proof.* Let $I$ be a global interpretation. Its tuple for a constraint $c$ is in the set of $c$ after line L5. Line L6 removes a tuple from the set of $c$ only when some other constraint $c'$ shares a variable $v$ with $c$ and no tuple of $c'$ has the same candidate for $v$. The tuple of $I$ for $c'$ has the same candidate for $v$ as the tuple of $I$ for $c$, so by induction over the removals no tuple of $I$ is ever removed. Line L7 is a depth-first search over all choices; it rejects a partial choice only when a constraint with all its arguments chosen has a tuple outside its set. It therefore returns every choice whose tuples are all in the filtered sets, which includes every global interpretation, and every returned choice is a global interpretation since the filtered sets are subsets of the sets of line L5. A variable that appears in no constraint is free and is kept by the search. The test `test_waltz_and_search_lose_nothing` compares the result with a brute-force product on 500 states. $\square$

## Lemma 4 (the global filters)

Line L9 (No Change) removes a successor of an interval state in which every variable takes I1, I4 or I7. Such a successor has the same values and directions as the interval state, so it is not a new distinguished time point; the solution is still described by the interval state and the other successors (Kuipers, Section 4.8). Line L10 (Cycle) stops a branch when a time-point state repeats an earlier one on the same branch, and records it; the continuation of the solution is described by the earlier part of the branch. Line L11 (Quiescence) stops a branch at a time point where every variable is std. In the models used here every variable is a state variable or a function of the state variables, so all directions std means that the state is an equilibrium of the differential equation, and by uniqueness of solutions it stays there. $\square$

## Theorem (soundness)

Let a solution of the differential equation stay finite, start in the initial state, and match the constraints. Then its qualitative behavior, cut after `max_states` states, is a prefix of one of the behaviors that `qsim` returns, after each new landmark is replaced by the old interval that contains it.

*Proof.* By induction on the number of states. The initial state is the root (line L1). Suppose the first $k$ states of the behavior of the solution are the path of a state $S$ in the tree. By Lemma 1 the next state of each variable is among the candidates of line L4. By Lemma 2 each constraint accepts the tuple of the true next states, so these tuples survive line L5. By Lemma 3 the true next state is among the successors of line L7, and line L8 builds it, with a new landmark for each I8 or I9 move. By Lemma 4 the filters of lines L9 to L11 either keep it, or stop the branch at a point after which the behavior is already described. So the first $k + 1$ states are a path in the tree, or the behavior is described by a branch that was stopped and recorded. $\square$

This is Theorem 5.2 of Kuipers (1986). The tests check it on numeric solutions: 40 runs of the ball thrown upward and 20 runs of a damped spring, with the Euler method, where the sign changes of each sampled trajectory give its qualitative behavior.

## Theorem (incompleteness)

QSIM can return behaviors that no solution has. This is Theorem 5.3 of Kuipers (1986), proved with the frictionless spring $X'' = -H(X)$, with $H$ in $M_0^+$: the energy $\int_0^X H(y)\,dy + V^2/2$ is constant on every solution, so when $X$ returns to 0 the speed must be the starting speed $v_0$. The constraints DERIV(X, V), DERIV(V, A) and M-(A, X) do not express this, and QSIM gives three behaviors from $X = 0$, $V = v_0$: a cycle that comes back to $(0, v_0)$, one that reaches $X = 0$ with a new speed landmark different from $v_0$, and one that reaches $V = v_0$ again while $X$ is not 0. The test `test_spring_three_branches_and_spurious` finds these three branches and checks that two of them break the energy law, so they are spurious.

## Termination

Each call of `successors` is finite: at most four candidates per variable, a finite set of tuples per constraint, a filtering loop that only removes tuples, and a finite search. The main loop only pushes a state with depth below `max_states`, and every state has finitely many successors, so the tree is finite and the loop stops. Without the bound the tree can be infinite, since each I8 or I9 move creates a new landmark. $\blacksquare$
