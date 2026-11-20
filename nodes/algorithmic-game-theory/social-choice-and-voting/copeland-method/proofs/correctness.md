---
title: Correctness and properties of Copeland's method
proves: [correctness]
status: full
---

Let $A = \{0, \ldots, m - 1\}$ with $m \ge 1$, and let $P = (r_1, \ldots, r_n)$ be a profile of rankings, each best first. Write $n_P(a, b)$ for the number of voters who rank $a$ above $b$. Candidate $a$ beats $b$ when $n_P(a, b) > n_P(b, a)$. Let $w_P(a)$ and $l_P(a)$ be the numbers of candidates that $a$ beats and that beat $a$, and let $t_P(a) = m - 1 - w_P(a) - l_P(a)$ be the number of ties of $a$. The Copeland score is $s_P(a) = w_P(a) - l_P(a)$, the correspondence is $W(P) = \{ a : s_P(a) = \max_b s_P(b) \}$, and the resolute rule is $f(P) = \min W(P)$. For $0 \le \alpha \le 1$, the Copeland$^\alpha$ score is $c^\alpha_P(a) = w_P(a) + \alpha\, t_P(a)$.

**Claim 1 (correctness).** COPELAND returns $f(P)$.

*Proof.* Line L1: a ballot $r$ ranks $a$ above $b$ exactly when $a$ comes before $b$ in $r$, so adding 1 to $N[a][b]$ for each such ordered pair of each ballot gives $N[a][b] = n_P(a, b)$. Loop of lines L3 to L5, invariant: after the pairs $\{a, b\}$ in a set $F$ have been processed, $s[x]$ equals the number of pairs in $F$ that $x$ wins minus the number of pairs in $F$ that $x$ loses. It holds for $F = \emptyset$ by line L2. Processing the pair $\{a, b\}$ changes only $s[a]$ and $s[b]$. If $a$ beats $b$, line L4 adds 1 to $s[a]$ and subtracts 1 from $s[b]$, which matches one more win of $a$ and one more loss of $b$. If $b$ beats $a$, line L5 does the reverse. If the pair is a tie, neither test holds and neither count changes. When every pair has been processed, $s[a] = w_P(a) - l_P(a) = s_P(a)$. Line L6 builds $W(P)$, which is nonempty since a maximum over the finite nonempty set $A$ is attained, and line L7 returns $\min W(P) = f(P)$.

**Claim 2 (Copeland$^{1/2}$).** $s_P(a) = 2 c^{1/2}_P(a) - (m - 1)$ for every $a$, so the Copeland score and the Copeland$^{1/2}$ score order the candidates in the same way.

*Proof.* $2 c^{1/2}_P(a) - (m - 1) = 2 w_P(a) + t_P(a) - w_P(a) - l_P(a) - t_P(a) = w_P(a) - l_P(a)$.

**Claim 3 (anonymity and neutrality).** $W$ does not change when the voters are reordered. For a permutation $\pi$ of $A$ and the renamed profile $\pi P$, $W(\pi P) = \pi(W(P))$.

*Proof.* $n_P(a, b)$ counts ballots with a property of the ballot alone, so it does not depend on their order. In $\pi P$, a voter ranks $\pi(a)$ above $\pi(b)$ exactly when the voter ranks $a$ above $b$ in $P$, so $n_{\pi P}(\pi(a), \pi(b)) = n_P(a, b)$. So $\pi(a)$ beats $\pi(b)$ in $\pi P$ exactly when $a$ beats $b$ in $P$, and $s_{\pi P}(\pi(a)) = s_P(a)$. The two score vectors have the same maximum, and $\pi(a)$ attains it in $\pi P$ exactly when $a$ attains it in $P$. The resolute rule is not neutral for $m \ge 2$: with the two ballots $(0, 1, 2, \ldots, m - 1)$ and $(1, 0, 2, \ldots, m - 1)$, candidates 0 and 1 tie with each other and have the same results against all others, the swap $\pi$ of 0 and 1 maps the profile to itself up to the order of the voters, and $f$ returns 0 on both, while $\pi(0) = 1$.

**Claim 4 (Condorcet consistency).** If $c$ is a Condorcet winner, then $W(P) = \{c\}$.

*Proof.* $c$ beats all $m - 1$ others, so $s_P(c) = m - 1$. Every $b \ne c$ loses to $c$, so $l_P(b) \ge 1$ and $w_P(b) \le m - 2$, which gives $s_P(b) \le m - 3 < s_P(c)$.

**Claim 5 (Smith consistency).** Let $S$ be the Smith set, the smallest nonempty set of candidates each of whom beats every candidate outside it. For every $0 \le \alpha \le 1$, every $a \in S$ and every $b \notin S$, $c^\alpha_P(a) > c^\alpha_P(b)$ and $s_P(a) > s_P(b)$. So $W(P) \subseteq S$.

*Proof.* Let $k = |S|$. The candidate $a$ beats all $m - k$ candidates outside $S$, so $c^\alpha_P(a) \ge m - k$. The candidate $b$ loses to each of the $k$ members of $S$, so it can gain points only from the other $m - k - 1$ candidates outside $S$, at most 1 point from each, and $c^\alpha_P(b) \le m - k - 1$. The claim for $s_P$ follows by Claim 2 with $\alpha = 1/2$. The set $S$ is not empty, so every $b \notin S$ has a lower score than some member of $S$, and $b \notin W(P)$.

**Claim 6 (Pareto).** If every voter ranks $a$ above $b$ and $n \ge 1$, then $s_P(a) > s_P(b)$, so $b \notin W(P)$.

*Proof.* $n_P(a, b) = n > 0 = n_P(b, a)$, so $a$ beats $b$. For any third candidate $x$, every voter who ranks $b$ above $x$ ranks $a$ above $x$ too, so $n_P(a, x) \ge n_P(b, x)$ and $n_P(x, a) \le n_P(x, b)$. So the result of $a$ against $x$ is at least as good as the result of $b$ against $x$, in the order loss, tie, win. The contribution of $x$ to $s_P(a)$ is at least its contribution to $s_P(b)$. The pair $\{a, b\}$ contributes $+1$ to $s_P(a)$ and $-1$ to $s_P(b)$. Adding up gives $s_P(a) \ge s_P(b) + 2$.

**Claim 7 (monotonicity).** Let $w \in W(P)$, and let $Q$ be $P$ with one ballot changed by moving $w$ up one place, passing the candidate $x$, with all other relative orders kept. Then $w \in W(Q)$ and $W(Q) \subseteq W(P)$. So $f(P) = w$ implies $f(Q) = w$.

*Proof.* Only the counts of the pair $\{w, x\}$ change: $n_Q(w, x) = n_P(w, x) + 1$ and $n_Q(x, w) = n_P(x, w) - 1$. So the result of $w$ against $x$ moves up or stays (loss to tie or win, tie to win), and nothing else changes for $w$. This gives $s_Q(w) \ge s_P(w)$. For $x$ the result against $w$ moves down or stays, so $s_Q(x) \le s_P(x)$, and every other score is the same. So $s_Q(w) \ge s_P(w) \ge s_P(y) \ge s_Q(y)$ for each $y$, and $w \in W(Q)$. If $y \in W(Q)$ with $y \ne w$, then $s_P(y) \ge s_Q(y) \ge s_Q(w) \ge s_P(w) = \max s_P$, so $y \in W(P)$. If $w$ is the smallest element of $W(P)$, it is then also the smallest element of $W(Q)$. Every raise of $w$ that keeps the other relative orders is a chain of such moves.

**Claim 8 (ties with four candidates).** If $n$ is odd, $m = 4$ and there is no Condorcet winner, then $|W(P)| \ge 2$.

*Proof.* With $n$ odd there are no tied pairs, so $s_P(a) = 2 w_P(a) - 3$ and the wins add up to the 6 pairs. No candidate has 3 wins. Four numbers in $\{0, 1, 2\}$ with sum 6 have at least two entries equal to 2: with at most one entry equal to 2 the sum is at most $2 + 1 + 1 + 1 = 5$. So at least two candidates have the top score.

**Claim 9 (time).** COPELAND runs in $O(n m^2)$ time and $O(m^2)$ extra space.

*Proof.* Line L1 touches each of the $m(m - 1)/2$ ordered pairs of each of the $n$ ballots once, in $O(1)$ time each, after $O(m^2)$ time to clear the matrix. Lines L3 to L5 do $O(1)$ work for each of the $m(m - 1)/2$ pairs. Lines L6 and L7 scan $m$ scores. The matrix has $m^2$ entries, and the scores and $W$ take $O(m)$ space. $\blacksquare$
