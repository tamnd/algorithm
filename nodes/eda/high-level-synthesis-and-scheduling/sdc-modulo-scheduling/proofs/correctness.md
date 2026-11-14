---
title: Correctness of SDC-based modulo scheduling
proves: [correctness]
status: full
---

We use the notation of the page. A loop body has operations $V$ with latency $\ell(v) \ge 0$ and type $k(v)$, and edges $(u, v)$ with distance $\mathrm{dist}(u, v) \ge 0$. Every cycle of edges has a total distance of at least 1. A limited type $k$ has $a_k \ge 1$ pipelined units. For an integer $II \ge 1$, a modulo schedule is a vector $s \in \mathbb{Z}_{\ge 0}^V$ with

- (D) $s_v - s_u \ge \ell(u) - II \cdot \mathrm{dist}(u, v)$ for each edge $(u, v)$;
- (M) for each limited type $k$ and each $r \in \{0, \ldots, II - 1\}$, at most $a_k$ operations $v$ of type $k$ have $s_v \bmod II = r$.

Let $C_{II}$ be the rows (D). A fixing step adds the two rows $s_v \ge t$ and $s_v \le t$. All rows are difference constraints or bounds on one variable, as on the [SDC scheduling](/sdc-scheduling/) page.

## Facts used from SDC scheduling

The proof of the SDC page gives these facts for a finite system $S$ of rows $s_v - s_u \ge w$ with integer $w$, lower bounds $s_v \ge \lambda_v$ and upper bounds $s_v \le \mu_v$, all integers.

- **(F1)** $S$ has a real solution exactly when it has an integer solution, since its matrix is totally unimodular and its data are integers.
- **(F2)** If $S$ has a solution, it has a least one, componentwise, and it is integral. The longest path computation from the lower bounds finds it, and $S$ is feasible exactly when that computation ends with no positive cycle and the result meets every upper bound. This is the test that `least_solution` makes.

## Lemma 1 (lower bounds)

Every modulo schedule for $II$ has $II \ge \mathrm{ResMII}$ and $II \ge \mathrm{RecMII}$.

*Proof.* Fix a limited type $k$ with $n_k$ operations. By (M), each of the $II$ residues holds at most $a_k$ of them, and every operation has one residue, so $n_k \le a_k \cdot II$, which gives $II \ge \lceil n_k / a_k \rceil$. Now fix a cycle $c$ of edges. Add the rows (D) of its edges. Each start appears once with a plus sign and once with a minus sign, so the left sides add to 0, and
$$0 \ge \sum_{(u, v) \in c} \ell(u) - II \cdot \sum_{(u, v) \in c} \mathrm{dist}(u, v).$$
The total distance $D_c$ is at least 1, so $II \ge \sum \ell(u) / D_c$, and as $II$ is an integer, $II \ge \lceil \sum \ell(u) / D_c \rceil$. $\square$

## Lemma 2 (the rows of L3 are feasible)

If $II \ge \mathrm{RecMII}$, then $C_{II}$ with $s \ge 0$ has a solution, so line L4 succeeds. If $II < \mathrm{RecMII}$, then $C_{II}$ has none.

*Proof.* Read $C_{II}$ as a graph with an arc $u \to v$ of weight $w = \ell(u) - II \cdot \mathrm{dist}(u, v)$. A cycle $c$ has weight $\sum \ell(u) - II \cdot D_c$, which is at most 0 exactly when $II \ge \sum \ell(u) / D_c$. So all cycles have weight at most 0 exactly when $II \ge \mathrm{RecMII}$. With no positive cycle, the longest path from a source joined to every node with weight 0 gives a solution with $s \ge 0$. With a positive cycle, the sum argument of Lemma 1 shows that no solution exists. $\square$

So the least $II$ with no positive cycle, which the implementation finds by trying $II = 1, 2, \ldots$, is $\mathrm{RecMII}$. Since a cycle weight only falls when $II$ grows, a binary search also works.

## Lemma 3 (the feasible starts of one operation form an interval)

Let $S$ be a feasible system of the form in (F2), and let $v$ be an operation. Let $T = \{t \in \mathbb{Z} : S \text{ with } s_v = t \text{ is feasible}\}$. Then $T$ is a set of consecutive integers, and its least element is $lo(v)$, the value of $v$ in the least solution of $S$.

*Proof.* The real solutions of $S$ form a convex set $P$. Its image under $s \mapsto s_v$ is a convex subset of $\mathbb{R}$, an interval $J$. Take an integer $t \in J$. Then $S$ with the two rows $s_v \ge t$ and $s_v \le t$ has a real solution, and these rows are bounds of the form in (F1), so it has an integer solution. Hence $T = J \cap \mathbb{Z}$, a set of consecutive integers. Let $x$ be the least solution of $S$. Then $x_v \in T$, and every solution $y$ has $y_v \ge x_v$, so no $t < x_v$ is in $T$. $\square$

## Theorem 1 (the candidates of L8 cover every residue that can work)

When line L7 handles $v$ with the current system $S$, write $lo = lo(v)$. If some $t \in T$ has a free unit of type $k(v)$ in slot $t \bmod II$, then line L8 reaches such a $t$ and line L11 fixes $v$.

*Proof.* Let $t^* \in T$ have a free slot. By Lemma 3, $T$ is a set of consecutive integers that starts at $lo$, so it holds every integer from $lo$ to $t^*$. Let $t' = lo + ((t^* - lo) \bmod II)$. Then $lo \le t' \le t^*$, so $t' \in T$, and $t' \equiv t^* \pmod{II}$, so $t'$ has the same free slot. Also $t' \le lo + II - 1$, so line L8 tries $t'$ unless an earlier candidate is fixed first. Each candidate that L8 tries passes L9 only with a free slot, and passes L10 exactly when it lies in $T$, by (F2). So the scan fixes the first candidate in $lo, \ldots, lo + II - 1$ that is in $T$ and has a free slot, and $t'$ is such a candidate. $\square$

So an operation fails on line L12 only when no feasible start of it, under the earlier choices, has a free slot. The failure comes from the earlier choices, not from a missed candidate.

## Theorem 2 (valid output)

If the algorithm returns $(II, s)$, then $s$ is a modulo schedule for $II$.

*Proof.* We keep this invariant: the current system $S$, which is $C_{II}$ with $s \ge 0$ and the rows added on line L11, is feasible, and the table holds, for each limited type $k$ and residue $r$, the number of fixed operations of type $k$ with residue $r$, which is at most $a_k$.

At the start, $S$ is feasible by Lemma 2, since $II \ge \mathrm{RecMII}$ on line L1 and $II$ only grows, and the table is empty. On line L11, the system with $s_v = t$ added was found feasible on line L10, and the slot of $t$ had fewer than $a_k$ entries on line L9, so after one more entry it holds at most $a_k$. Every limited operation is fixed once, since line L6 lists each of them once.

On line L14 every limited operation is fixed, and $S$ is feasible, so its least solution $s$ exists by (F2). It meets (D), since $C_{II} \subseteq S$, and $s \ge 0$. Each limited $v$ has $s_v$ equal to its fixed value $t_v$, so the operations of type $k$ with residue $r$ are exactly the fixed ones that the table counts, and (M) holds. Operations of unlimited types have no slot limit. $\square$

## Theorem 3 (the exact search)

For fixed $II$, the function `exact_schedule` returns a modulo schedule exactly when one exists.

*Proof.* Each $s \in \mathbb{Z}_{\ge 0}^V$ is written in one way as $s_v = r_v + II \cdot q_v$ with $r_v \in \{0, \ldots, II - 1\}$ and $q_v \in \mathbb{Z}_{\ge 0}$. Condition (M) depends only on $r$, and `_residues` lists exactly the vectors $r$ that meet (M), since it skips a value of $r_v$ only when its slot is already full. For fixed $r$, a row of (D) with weight $w$ reads $r_v + II q_v - r_u - II q_u \ge w$, that is, $q_v - q_u \ge (w - r_v + r_u)/II$. As $q_v - q_u$ is an integer, this holds exactly when $q_v - q_u \ge \lceil (w - r_v + r_u)/II \rceil$. These rows are difference constraints with integer weights, and with $q \ge 0$ they have an integer solution exactly when the longest path computation succeeds, by (F2). So for each $r$ the search finds a $q$ exactly when some schedule has residues $r$, and it returns $s = r + II \cdot q$, which meets (D) and (M). If it finds none for every $r$, no schedule exists. $\square$

Then `exact_min_ii` returns the least $II$ in its range with a schedule, since it tries $II$ upward from $\max(\mathrm{ResMII}, \mathrm{RecMII})$, and Lemma 1 shows that no smaller $II$ has one.

## What is not claimed

- The heuristic $II$ is not always the least. The accumulator example on the page returns 4 where 3 is possible.
- We do not prove that the outer loop ends with a schedule for some $II$. The implementation stops at a cap and returns `None`. In the tests it never reached the cap.
- The measured counts on the page, 2 losses in 150 random loops and the optimum at $\max(\mathrm{ResMII}, \mathrm{RecMII})$ on all 150, are observations on small loops, not bounds.
- The order of line L6 and the scan of line L8 are a simplified form of Zhang and Liu's method. The theorems above concern this form.
