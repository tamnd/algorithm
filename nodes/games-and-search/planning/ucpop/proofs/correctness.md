---
title: UCPOP is sound, terminates, is complete within its bound, and with iterative deepening returns a plan with the fewest steps
proves: [correctness]
status: full
---

We use the definitions and the pseudocode of the page. A literal $\ell$ holds in a state $x$ if $\ell = f$ and $f \in x$, or $\ell = \neg f$ and $f \notin x$. Effect $e$ *makes* $\ell$ if it adds $f$ when $\ell = f$, and deletes $f$ when $\ell = \neg f$; START makes every literal that holds in $I$. We assume, as the page does:

**(C)** If two effects of an action can fire together, no fact is added by one and deleted by the other.

So when an action applies in $x$ and a fired effect makes $\ell$, then $\ell$ holds in the next state: no other fired effect makes $\neg \ell$. And if $\ell$ holds in $x$, it fails in the next state only if some fired effect makes $\neg \ell$.

**Lemma 1 (soundness).** Let $P$ be complete: acyclic, with no open goal and no threat. Then for every linearization $L$, the actions of $L$ form a solution.

*Proof.* Let $L = (u_0, u_1, \ldots, u_{m+1})$ with $u_0 = $ START and $u_{m+1} = $ FINISH, and let $x_t$ be the state after the actions $u_1, \ldots, u_t$, with $x_0 = I$. We prove by strong induction on $t$ that every goal $(\ell, u_{t+1})$ holds in $x_t$. The goals of $u_{t+1}$ include its precondition, so this shows that every action applies, and for FINISH that $G$ holds at the end.

Take a goal $(\ell, u_{t+1})$. It is not open, so there is a link $u_r \xrightarrow{e,\ell} u_{t+1}$ with $r \le t$, because the link orders its ends. If $r = 0$, $\ell$ holds in $I = x_0$. If $r \ge 1$, the goals of $u_r$ include its precondition and $\mathit{cond}(e)$, which hold in $x_{r-1}$ by the induction hypothesis; so $u_r$ applies, $e$ fires, and by (C) $\ell$ holds in $x_r$. Now let $r < v \le t$. The step $u_v$ lies between the ends of the link in $L$, so the orderings allow it there: neither $u_v \prec u_r$ nor $u_{t+1} \prec u_v$. Suppose an effect $e'$ of $u_v$ makes $\neg \ell$. Since $P$ has no threat, some goal $(\neg c, u_v)$ with $c \in \mathit{cond}(e')$ exists, and by the induction hypothesis $\neg c$ holds in $x_{v-1}$, so $e'$ does not fire. So no effect that fires at $u_{r+1}, \ldots, u_t$ makes $\neg \ell$, and $\ell$ holds in $x_t$. $\square$

**Lemma 2 (termination).** For a fixed $n$, REFINE visits finitely many partial plans.

*Proof.* Each refinement does one of four things. It adds a new step, at most $n$ times on a branch. It adds a link into an open goal, which closes that goal for good, since links and goals are never removed. It adds a new ordering pair to the closure: a threat exists only if neither $k \prec i$ nor $j \prec k$ holds. Or it adds a goal $(\neg c, k)$ that is new, since a threat exists only while no such goal is present. With at most $n + 2$ steps there are at most $2 |F| (n + 2)$ goals, as many links, and $(n + 2)^2$ ordering pairs. So every branch is finite, every node has finitely many children, and by König's lemma the tree is finite. $\square$

**Lemma 3 (completeness).** Let $\sigma = (a_1, \ldots, a_m)$ with $m \le n$ be a solution over the actions given to REFINE. Then REFINE with the bound $n$ returns a complete plan.

*Proof.* Let $x_0 = I$ and let $x_t$ be the state after $a_1, \ldots, a_t$. Say that effect $e$ *fires at* position $t \ge 1$ if $e$ is an effect of $a_t$ whose condition holds in $x_{t-1}$, and that START fires at position $0$ and makes every literal of $x_0$. For a literal $\ell$ that holds in $x_{p-1}$, let $\lambda(\ell, p)$ be the last position $q < p$ at which some fired effect makes $\ell$. It exists: if no position $q \ge 1$ qualifies, then $\ell$ held in $x_0$, since nothing made it true later, and $q = 0$. Also no effect that fires strictly between $q$ and $p$ makes $\neg \ell$: by (C) $\ell$ holds in $x_q$, and if a later fired effect made it false, nothing made it true again before $p$.

Put START at position $0$, FINISH at $m + 1$. Call $P$ *faithful* if there is a one-to-one map $\phi$ from its steps to positions such that $\phi(\text{START}) = 0$, $\phi(\text{FINISH}) = m + 1$, every other step $s$ is a copy of $a_{\phi(s)}$; $i \prec j$ implies $\phi(i) < \phi(j)$; every goal $(\ell, j)$ holds in $x_{\phi(j) - 1}$, with $x_m$ for FINISH; and every link $i \xrightarrow{e,\ell} j$ has $\phi(i) = \lambda(\ell, \phi(j))$ and $e$ firing at $\phi(i)$.

The first plan is faithful, since $\sigma$ reaches $G$. Let $P$ be faithful with a flaw. We show that every flaw has a resolver that gives a faithful child. Then whatever line L8 chooses, a faithful child exists; following such children gives a finite path by Lemma 2, which ends in a faithful plan with no flaw, returned by line L7, unless the depth-first search returns another complete plan first.

*Open goal $(\ell, j)$.* The goal holds in $x_{\phi(j) - 1}$, so $q = \lambda(\ell, \phi(j))$ exists and some effect $e$ firing at $q$ makes $\ell$. If $q = \phi(i)$ for a step $i$, then $j \prec i$ is false, and line L13 offers the link $i \xrightarrow{e,\ell} j$. Its ordering $i \prec j$ agrees with $\phi$. Its new goals $(c, i)$ for $c \in \mathit{cond}(e)$ hold in $x_{q - 1}$ because $e$ fires at $q$. If no step has position $q$, then $q \ge 1$ and $P$ has fewer than $m \le n$ action steps, so line L14 offers a new copy of $a_q$ linked by $e$. Map it to $q$. Its precondition goals hold in $x_{q-1}$ because $\sigma$ is executable, and the condition goals hold as before.

*Threat $(k, e', i \xrightarrow{e,\ell} j)$.* Since $\phi$ is one to one, $\phi(k) \notin \{\phi(i), \phi(j)\}$. If $\phi(k) < \phi(i)$, demotion agrees with $\phi$; if $\phi(k) > \phi(j)$, promotion does; line L10 keeps both, because orderings that agree with $\phi$ are acyclic. Otherwise $\phi(i) < \phi(k) < \phi(j)$. As $\phi(i) = \lambda(\ell, \phi(j))$, no effect that fires strictly between makes $\neg \ell$, and $e'$ makes $\neg \ell$, so $e'$ does not fire at $\phi(k)$. The action $a_{\phi(k)}$ applies in $x_{\phi(k) - 1}$, so some $c \in \mathit{cond}(e')$ fails there; that is, $\neg c$ holds in $x_{\phi(k) - 1}$. Line L11 offers the goal $(\neg c, k)$, and the child is faithful. $\square$

**Lemma 4 (the step bound and the cut test).** If a solution exists, one with at most $2^{|F|} - 1$ actions exists. If a round with bound $n$ ends with $\mathit{cut} = \mathit{false}$, every round with a larger bound visits the same plans and fails.

*Proof.* A shortest solution visits no state twice, and there are $2^{|F|}$ states. The bound appears only in line L14; if line L15 never ran, at every open goal the round met, either $P$ had fewer than $n$ steps or no effect makes $\ell$, and in both cases line L14 gives the same set under a larger bound. By induction from the root the rounds make the same choices. The implementation drops actions whose precondition contains both $f$ and $\neg f$; they never apply, so no solution uses them. $\square$

**Theorem.** UCPOP returns a complete plan whose every linearization is a solution, with as few steps as a shortest solution, if a solution exists, and it returns failure otherwise.

*Proof.* By Lemma 1 every returned plan is correct. If a solution exists, let $L^*$ be the length of a shortest one; $L^* \le 2^{|F|} - 1$ by Lemma 4. A round $n < L^*$ fails, since its plan would give a solution with fewer actions by Lemma 1, and it does not stop at line L5, since by Lemma 4 that would make the round $L^*$ fail, against Lemma 3. So the round $L^*$ is reached and, by Lemma 3, returns a plan of at most $L^*$ steps, hence of exactly $L^*$. If no solution exists, no round returns a plan, and the loop ends at line L5 or L6 after finitely many rounds by Lemma 2. $\square$
