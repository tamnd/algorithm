---
title: Window permutation keeps the functions, never grows the size, terminates, and ends in a local optimum for windows
proves: [correctness]
status: full
---

The store is a shared BDD that is ordered and reduced, with the variables on levels $1, \ldots, n$. The size is the number of nodes that some root reaches, with the sinks. We use these facts.

- **(S) The swap lemma.** A swap of the levels $k$ and $k + 1$, followed by garbage collection, gives an ordered and reduced store for the order with the two variables exchanged, and keeps the ids and the functions of the roots. It is proved in [the proof file of sifting](/bdd-sifting/).
- **(C) Canonicity.** For fixed root functions, the size of the ordered and reduced store depends only on the order ([BDD canonicity](/bdd-canonicity/)).
- **(T) The Steinhaus-Johnson-Trotter sequence.** For $w \ge 2$ it is a list of $w! - 1$ offsets in $\{0, \ldots, w - 2\}$ such that, if one starts from any arrangement of $w$ items and swaps the positions $j$ and $j + 1$ for each offset $j$ in turn, the $w!$ arrangements seen (the start and one after each swap) are all distinct ([Steinhaus-Johnson-Trotter](/steinhaus-johnson-trotter/)).

**Lemma 1 (one window).** Consider one execution of lines L4 to L9 for a window on levels $k$ to $k + w - 1$. Let $\sigma$ be the order at line L4 and $s_0$ the size. Then:

1. the order outside the window is the same as in $\sigma$ at each moment;
2. at line L7, the order of the window runs through all $w!$ orders except the start one, and `best` is the minimum of $s_0$ and the sizes seen so far;
3. after line L8, the window holds `best_window` in this order, and the size is `best` $\le s_0$;
4. if `best` $= s_0$, the order after line L8 is $\sigma$.

*Proof.* (1) Lines L6 and L8 only swap two adjacent levels inside the window, because the offsets are at most $w - 2$, and line L8 only moves window variables up to levels at least $k$.

(2) By (T), the swaps of line L6 visit the $w!$ window orders; the start order is the one at line L4. Line L7 keeps the running minimum with a strict comparison, and `best_window` is a window order at which the size `best` was seen (the start order if no smaller size was seen).

(3) Let $b_1, \ldots, b_w$ be `best_window`. Before the step for $b_i$, the levels $k, \ldots, k + i - 2$ hold $b_1, \ldots, b_{i-1}$, and $b_i$ is on a level of at least $k + i - 1$ inside the window. Moving $b_i$ up by swaps until it reaches level $k + i - 1$ does not touch the levels above $k + i - 1$. So after the last step the window holds $b_1, \ldots, b_w$. With (1), the whole order equals the order at which `best` was seen. By (C), the size is `best`, and `best` $\le s_0$ by (2).

(4) If `best` $= s_0$, then no size was strictly smaller, so `best_window` is the start order of the window, and by (1) and (3) the order is $\sigma$. $\square$

**Theorem.** Let WINDOW-PERMUTATION$(B, w)$ start on an ordered and reduced store of size $s$, with $2 \le w \le n$. Then:

1. it terminates after at most $s$ passes that set `improved`, plus one pass that does not;
2. at the end the store is ordered and reduced, and the roots have the same ids and functions;
3. the final size is at most $s$;
4. the final order $\pi'$ is a local optimum for windows: for each $k$, no order of the variables on levels $k$ to $k + w - 1$ of $\pi'$, with the other levels as in $\pi'$, gives a smaller size.

*Proof.* (2) follows from (S), since the method changes the store only by swaps.

(3) By Lemma 1 (3), the size after each window is at most the size before it. So the size never increases, and the final size is at most $s$.

(1) If a pass sets `improved`, then some window has `best` $<$ `start`, and by Lemma 1 (3) the size goes down by at least 1 in that window; the other windows do not increase it. The size is a positive integer at most $s$, so at most $s - 1$ passes set `improved`. The loop of line L1 stops after the first pass that does not set it.

(4) Consider the last pass. No window set `improved`, so each window had `best` $=$ `start`, and by Lemma 1 (4) each window left the order unchanged. So the order was $\pi'$ during the whole last pass. For each $k$, the window at levels $k$ to $k + w - 1$ visited all its orders on top of $\pi'$ (Lemma 1 (1) and (2)), and none had a size smaller than the size of $\pi'$. $\blacksquare$

**Remark.** Part (4) is the only quality guarantee. It does not bound the ratio to the optimum size, and no polynomial-time method can bound it by a constant unless P = NP (see [NP-completeness of OBDD variable ordering](/variable-ordering-np-hardness/)).
