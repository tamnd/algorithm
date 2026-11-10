---
title: Lin-Kernighan steps give tours, the search stops, and with full lists the result is 2-optimal
proves: [correctness]
status: full
---

The costs $d$ on the city set $V$, with $|V| = n \ge 4$, are symmetric and non-negative. $T$ is the current tour. A search removes one tour edge $\{t_1, y_0\}$, which leaves a Hamiltonian path $P_0$ from $t_1$ to the free end $y_0$, with the start gain $G_0 = d(t_1, y_0)$. A step on a path $P$ from $t_1$ to the free end $y$, with partial gain $G$, picks a candidate $z$ that is not $y$ and not the path neighbor of $y$. Let $w$ be the city after $z$ on $P$, on the side of $y$. The step adds $\{y, z\}$, removes $\{z, w\}$ and reverses the part of $P$ from $w$ to $y$. The new path $P'$ goes from $t_1$ to $z$, then from $y$ back to $w$, so $w$ is the new free end and $G' = G - d(y, z) + d(z, w)$. Closing $P'$ adds the edge $\{w, t_1\}$ and gives the gain $G' - d(w, t_1)$. A step is allowed only if $G - d(y, z) > 0$ (the gain criterion), $\{y, z\}$ was not removed before, and $\{z, w\}$ was not added before. The implementation uses $\varepsilon = 10^{-12}$ in place of 0 in each test.

**Lemma 1 (steps give paths, and the gains are exact).** Each $P'$ is a Hamiltonian path from $t_1$ to $w$ with $c(P') = c(T) - G'$. Closing it gives a tour of cost $c(T) - (G' - d(w, t_1))$.

*Proof.* By induction on the steps. At the start, $c(P_0) = c(T) - d(t_1, y_0) = c(T) - G_0$. In a step, $P$ is $t_1, \ldots, z, w, \ldots, y$. Removing $\{z, w\}$ cuts it into the piece $t_1, \ldots, z$ and the piece $w, \ldots, y$. Adding $\{z, y\}$ joins the end $z$ of the first piece to the end $y$ of the second, so $P' = t_1, \ldots, z, y, \ldots, w$ visits each city once. Its cost is $c(P) + d(y, z) - d(z, w) = c(T) - G + d(y, z) - d(z, w) = c(T) - G'$. The cities $w$ and $t_1$ are the two ends of $P'$, and $w \ne t_1$ because $z$ comes before $w$. So adding $\{w, t_1\}$ closes $P'$ into a tour of cost $c(P') + d(w, t_1)$. $\square$

**Lemma 2 (the depth is less than $n$).** Every removed edge is an edge of $T$, and no edge of $T$ is removed twice in one search. So a search makes at most $n - 1$ steps on one branch.

*Proof.* The edges of a path $P$ in the search are edges of $T$ and added edges. The step removes $\{z, w\}$, an edge of $P$, and the rule forbids $\{z, w\}$ to be an added edge. So $\{z, w\}$ is an edge of $T$. Once removed, it is not on later paths of the branch, since the rule forbids adding it again. The first removed edge is $\{t_1, y_0\}$, so a branch removes at most $n$ distinct edges of $T$ and makes at most $n - 1$ steps. $\square$

**Lemma 3 (each search stops, and its answer is correct).** A call of the search stops, and it returns either nothing or a tour whose cost is $c(T)$ minus the returned gain, which is positive.

*Proof.* By Lemma 2 each branch has depth less than $n$ (and the code also stops at a fixed depth), and each step has finitely many choices, so the search tree is finite. A tour is recorded only when its closing gain is above $\varepsilon$, and by Lemma 1 its cost is $c(T)$ minus that gain. $\square$

**Theorem 1 (termination).** The outer loop stops at a tour on which no search, from any start city $t_1$ and either of its two tour edges, finds a gain.

*Proof.* Each accepted search makes the tour strictly shorter by Lemma 3. There are finitely many tours, so only finitely many searches are accepted. Between two accepted searches the loop runs at most $2n$ searches, each finite. The loop ends only after $2n$ searches in a row return nothing, which is the claim. $\square$

**Theorem 2 (full lists give 2-optimal tours).** Suppose each candidate list holds all other cities and the search tries every allowed choice at depth 0. Then the returned tour is 2-optimal.

*Proof.* Let $T$ be the returned tour, and suppose a 2-opt move gains on it. Write the tour as $a, b, \ldots, c, e, \ldots$, with $b$ after $a$ and $e$ after $c$, where the move removes $\{a, b\}$ and $\{c, e\}$ and adds $\{a, c\}$ and $\{b, e\}$, with gain

$$g = d(a, b) + d(c, e) - d(a, c) - d(b, e) > 0.$$

The two edges do not touch, so the four cities are distinct. Look at two searches.

1. *Start $t_1 = a$, removing $\{a, b\}$.* The path is $a, \ldots, e, c, \ldots, b$ (the tour walked backward from $a$), with free end $b$ and $G_0 = d(a, b)$. The choice $z = e$ is allowed, since $e$ is not $b$ and not the path neighbor of $b$, which is the tour successor of $b$. Its $w$ is $c$. The first partial gain is $g_1 = d(a, b) - d(b, e)$. Closing adds $\{c, a\}$, so the closing gain is $d(a, b) - d(b, e) + d(c, e) - d(c, a) = g$.
2. *Start $t_1 = e$, removing $\{c, e\}$.* By the same argument with the tour walked forward from $e$, the path is $e, \ldots, a, b, \ldots, c$, with free end $c$. The choice $z = a$ is allowed, its $w$ is $b$, the first partial gain is $g_2 = d(c, e) - d(c, a)$, and the closing gain is again $g$.

Now $g_1 + g_2 = g > 0$, so $g_1 > 0$ or $g_2 > 0$. In that search the step passes the gain criterion, and no edge is tabu at depth 0. Since every allowed choice is tried at depth 0, the step is tried and the closed tour with gain $g > 0$ is recorded. So that search returns a tour, which contradicts Theorem 1. Hence no 2-opt move gains on $T$. $\square$

**Corollary.** Under the conditions of Theorem 2 and for metric costs, the returned tour has cost at most $2\sqrt{2} \sum_{i=1}^{n} 1/\sqrt{i} \cdot \text{OPT} < 4\sqrt{2}\,\sqrt{n} \cdot \text{OPT}$.

*Proof.* The bound of the [2-opt](/two-opt/) page holds for every 2-optimal tour, and its proof uses nothing else. $\blacksquare$

**Remarks.**

- With the usual short candidate lists (here the 8 nearest cities) and narrow breadth, Theorem 2 does not apply, and no worst-case ratio is proved for the tours. The quality claims on the page for that setting are measured.
- The page claims no polynomial bound on the number of improvements. The test file checks Lemma 1 through the traced example, checks Theorem 1 by running every search on the result, and checks Theorem 2 and the corollary against brute force for $n \le 8$.
