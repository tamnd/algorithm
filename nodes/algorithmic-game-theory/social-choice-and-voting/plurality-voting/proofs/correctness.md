---
title: Correctness and properties of plurality voting
proves: [correctness]
status: full
---

Let $A = \{0, \ldots, m - 1\}$ with $m \ge 1$, and let $P = (r_1, \ldots, r_n)$ be a profile of rankings, each best first. Write $s_P(a) = |\{ i : r_i[1] = a \}|$ for the plurality score and $W(P) = \{ a : s_P(a) = \max_b s_P(b) \}$ for the plurality correspondence. The resolute rule is $f(P) = \min W(P)$.

**Claim 1 (correctness).** PLURALITY returns $f(P)$.

*Proof.* Invariant of the loop of lines L2 and L3: after the first $k$ ballots, $s[a] = |\{ i \le k : r_i[1] = a \}|$ for every $a$. For $k = 0$ this is line L1. If it holds for $k$, the pass for ballot $k + 1$ adds 1 to $s[r_{k+1}[1]]$ and to no other counter, and the set on the right gains the index $k + 1$ for $a = r_{k+1}[1]$ only, so it holds for $k + 1$. After $n$ passes, $s[a] = s_P(a)$. Line L4 sets $best = \max_a s_P(a)$, line L5 builds $W(P)$, which is nonempty because a maximum is attained on the finite nonempty set $A$, and line L6 returns $\min W(P) = f(P)$.

**Claim 2 (anonymity).** For every permutation $\sigma$ of the voters, $W(r_{\sigma(1)}, \ldots, r_{\sigma(n)}) = W(P)$, and so $f$ is the same on both profiles.

*Proof.* $s_P(a)$ counts a set of ballots with a property that depends only on the ballot, so it does not depend on the order of the voters.

**Claim 3 (neutrality of the correspondence).** For a permutation $\pi$ of $A$, let $\pi P$ be the profile in which every ranking has each $a$ replaced by $\pi(a)$. Then $W(\pi P) = \pi(W(P))$.

*Proof.* The top of the renamed ballot $\pi r_i$ is $\pi(r_i[1])$, so $s_{\pi P}(\pi(a)) = s_P(a)$ for every $a$. The two score vectors have the same maximum, and $\pi(a)$ attains it in $\pi P$ exactly when $a$ attains it in $P$.

The resolute rule is not neutral when $m \ge 2$: for the profile $P = ((0, 1, \ldots), (1, 0, \ldots))$ and $\pi$ the swap of 0 and 1, $\pi P$ has the same two ballots in the other order, so $f(\pi P) = 0 \ne 1 = \pi(f(P))$.

**Claim 4 (Pareto).** If $n \ge 1$ and every voter ranks $a$ above $b$, then $b \notin W(P)$.

*Proof.* No ballot has $b$ on top, so $s_P(b) = 0$. The scores add up to $n \ge 1$, so some candidate has a positive score, and $\max_c s_P(c) > 0 = s_P(b)$.

**Claim 5 (monotonicity).** Let $w \in W(P)$, and let $Q$ be $P$ with one ballot $r_i$ changed by moving $w$ up one place and keeping the order of all other candidates. Then $w \in W(Q)$, and if $w = f(P)$ then $w = f(Q)$.

*Proof.* If $w$ is not in second place in $r_i$, the top of $r_i$ does not change, and $s_Q = s_P$. If $w$ is in second place, the old top $t$ loses one first place and $w$ gains one: $s_Q(w) = s_P(w) + 1$, $s_Q(t) = s_P(t) - 1$, and every other score is the same. In both cases $s_Q(w) \ge s_Q(c)$ for every $c$, because $s_Q(w) \ge s_P(w) \ge s_P(c) \ge s_Q(c)$. So $w \in W(Q)$. Moreover $W(Q) \subseteq W(P)$: a candidate $c \ne w$ in $W(Q)$ has $s_P(c) \ge s_Q(c) = s_Q(w) \ge s_P(w) = \max s_P$. So if $w$ is the smallest element of $W(P)$, it is also the smallest element of $W(Q)$. Any raise of $w$ that keeps the order of the other candidates is a chain of such one-place moves, so the claim holds for it too.

**Claim 6 (consistency).** Let $P_1$ and $P_2$ be profiles of disjoint groups of voters, and let $P_1 + P_2$ be the joined profile. If $W(P_1) \cap W(P_2) \ne \emptyset$, then $W(P_1 + P_2) = W(P_1) \cap W(P_2)$.

*Proof.* The scores add: $s_{P_1 + P_2} = s_{P_1} + s_{P_2}$. Let $M_j = \max s_{P_j}$. Every candidate has a joined score at most $M_1 + M_2$, and a candidate attains this bound exactly when it attains $M_1$ in $P_1$ and $M_2$ in $P_2$, that is, when it is in $W(P_1) \cap W(P_2)$. That set is nonempty, so $M_1 + M_2$ is the maximum of the joined scores and $W(P_1 + P_2) = W(P_1) \cap W(P_2)$.

**Claim 7 (two candidates).** If $m = 2$, then $f(P) = 0$ exactly when $2 s_P(0) \ge n$; that is, $f$ is majority rule with ties to candidate 0, and $f$ elects the Condorcet winner whenever there is one.

*Proof.* With two candidates the top of a ballot is the candidate preferred to the other one, so $s_P(0) = n_P(0, 1)$ and $s_P(1) = n_P(1, 0) = n - s_P(0)$. Candidate 0 is in $W(P)$ exactly when $s_P(0) \ge n - s_P(0)$, and then $f(P) = 0$; otherwise $W(P) = \{1\}$. A Condorcet winner has more than $n/2$ of these pairwise votes, so it is the unique maximizer.

**Claim 8 (time).** PLURALITY runs in $O(n + m)$ time and $O(m)$ extra space.

*Proof.* Line L1 writes $m$ counters. Each of the $n$ passes of the loop reads one entry and updates one counter in $O(1)$ time. Lines L4, L5 and L6 each scan at most $m$ values. Only the $m$ counters and the set $W$, of size at most $m$, are stored. $\blacksquare$
