---
title: The farthest-reach greedy finds a smallest cover
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The family is $I[1], \ldots, I[n]$ with $I[j] = \langle l_j, r_j \rangle$, and the target has $s < t$. All sets have one type. Define the prefix of length up to $x \ge s$:

$$ P(x) = [s, x) \text{ for closed and half-open intervals}, \qquad P(x) = (s, x) \text{ for open intervals}. $$

So $P(s) = \emptyset$. For a set $S$ of intervals let $U(S) = \bigcup_{j \in S} I[j]$ and $\rho(S) = \sup \{ x \ge s : P(x) \subseteq U(S) \}$. Since $P(\rho) = \bigcup_{x < \rho} P(x)$, the supremum is attained: $P(\rho(S)) \subseteq U(S)$.

**Covering the target.** For half-open and open intervals the target is $P(t)$. For closed intervals the target is $[s, t]$, and $[s, t] \subseteq U(S)$ if and only if $P(t) = [s, t) \subseteq U(S)$, because $U(S)$ is a finite union of closed sets, hence closed, and $t$ is a limit of points of $[s, t)$. So in all cases, $S$ covers the target if and only if $\rho(S) \ge t$.

**The test.** Call an interval *available at $x$* when $l \le x$, except for open intervals with $x > s$, where it means $l < x$. Line L5 reads exactly the unread intervals available at $reach$.

**Lemma 1 (extension).** Let $s \le x$ and let $S$ be a set with $\rho(S) > x$. Then some $J \in S$ is available at $x$ and has $r_J > x$.

*Proof.* The points of the open interval $(x, \rho(S))$ lie in $P(\rho(S)) \subseteq U(S)$. Let $m$ be the least left end among the intervals of $S$ with left end greater than $x$, or $m = \rho(S)$ if there is none, and let $y$ be a point with $x < y < \min(m, \rho(S))$. Then $y$ lies in some $J \in S$, with $l_J \le x$ by the choice of $y$, and $r_J \ge y > x$. If the intervals are not open, or if $x = s$, then $J$ is available at $x$. If they are open and $x > s$, then $x \in P(\rho(S))$, so $x$ lies in some $J' = (l', r') \in S$, which has $l' < x < r'$; take $J'$. $\square$

**Lemma 2 (the chosen prefix).** After $j$ choices, $P(reach_j) \subseteq U(C_j)$, where $C_j$ is the set of chosen intervals and $reach_j$ the value of $reach$.

*Proof.* By induction on $j$; for $j = 0$, $P(s) = \emptyset$. At step $j$ the choice $J = I[best]$ is available at $reach_{j-1}$ and has $r_J = reach_j > reach_{j-1}$. For closed and half-open intervals $l_J \le reach_{j-1}$, so $J \supseteq [reach_{j-1}, reach_j)$, and $P(reach_j) = P(reach_{j-1}) \cup [reach_{j-1}, reach_j)$. For open intervals with $j = 1$, $l_J \le s$, so $J \supseteq (s, reach_1)$. For open intervals with $j \ge 2$, $l_J < reach_{j-1}$, so $J \supseteq [reach_{j-1}, reach_j)$, and again the union of $P(reach_{j-1})$ and this set is $P(reach_j)$. $\square$

**Lemma 3 (what line L5 sees).** At step $j$, the value $far$ after line L6 is the largest right end among all intervals available at $reach_{j-1}$, if this is more than $reach_{j-1}$.

*Proof.* Line L1 sorts by left end, and availability at $x$ only depends on $l$, so the unread available intervals form a contiguous run starting at $i$, which line L5 reads. An interval read at an earlier step $j' < j$ has right end at most $far = reach_{j'} \le reach_{j-1}$. So the earlier reads cannot beat $reach_{j-1}$, and line L6 sees every other available interval. $\square$

**Lemma 4 (stays ahead).** If the greedy makes at least $j$ choices, then $reach_j \ge \rho(S)$ for every set $S$ of at most $j$ intervals.

*Proof.* By induction on $j$. For $j = 0$, $S = \emptyset$ and $\rho(\emptyset) = s = reach_0$. Let $j \ge 1$, $|S| \le j$, and $x = \rho(S)$. If $x \le reach_{j-1}$, then $x < reach_j$. Otherwise $x > reach_{j-1} \ge s$. The points of $P(x)$ just left of $x$ lie in $U(S)$, and $S$ is finite, so some $J \in S$ contains points arbitrarily close to $x$ from the left; then $l_J < x \le r_J$. Let $S' = S \setminus \{J\}$, with $|S'| \le j - 1$.

*Closed and half-open intervals.* Each point of $P(x)$ less than $l_J$ is not in $J$, so it lies in $U(S')$. If $l_J > s$, then $P(l_J) \subseteq U(S')$, so $\rho(S') \ge l_J$, and by induction $reach_{j-1} \ge l_J$. If $l_J \le s$, then $l_J \le reach_{j-1}$ directly. So $J$ is available at $reach_{j-1}$.

*Open intervals.* If $l_J \le s$, then $J$ is available at $reach_{j-1}$, since either $j = 1$ and the test is $l \le s$, or $j \ge 2$ and $reach_{j-1} > s \ge l_J$. If $l_J > s$, then the points of $(s, l_J]$ are not in $J$ and lie in $P(x)$, so $(s, l_J] \subseteq U(S')$. The set $U(S')$ is open, so it also contains $(s, l_J + \varepsilon)$ for some $\varepsilon > 0$, and $\rho(S') > l_J$. By induction $reach_{j-1} > l_J$, so $J$ is available.

In both cases $r_J \ge x > reach_{j-1}$, so by Lemma 3 the greedy's $far$ at step $j$ is at least $r_J$, and $reach_j \ge x$. $\square$

**Termination.** Each step of the outer loop either returns at line L7 or chooses an interval with $r > reach$ and sets $reach$ to that right end, so $reach$ strictly increases. The chosen interval was read in this step and $i$ moved past it, so no interval is chosen twice, and there are at most $n$ steps. The inner loop moves $i$ forward, at most $n$ times in total.

**Correctness.** *If the greedy returns $C$*, it stopped because $reach \ge t$, so $\rho(C) \ge reach \ge t$ by Lemma 2, and $C$ covers the target. *If a cover exists*, let $S^*$ be a smallest one, with $k$ intervals. While $reach_{j} < t \le \rho(S^*)$, Lemma 1 with $x = reach_j$ gives an interval of $S^*$ available at $reach_j$ with right end above $reach_j$; it has not been read in an earlier step, by the argument of Lemma 3, so line L6 sets $best$, and line L7 does not fail. By Lemma 4, if the greedy makes $k$ choices then $reach_k \ge \rho(S^*) \ge t$, and the loop stops. So the greedy returns a cover with at most $k$ intervals, which is optimal. *If no cover exists*, the greedy cannot return a list, since every returned list is a cover, so it returns "no cover" at line L7, by termination. $\blacksquare$
