---
title: Correctness and properties of approval voting
proves: [correctness]
status: full
---

Let $A = \{0, \ldots, m - 1\}$ with $m \ge 1$ and let $(S_1, \ldots, S_n)$ be an approval profile, with $S_i \subseteq A$. Write $F(a) = \{ i : a \in S_i \}$ for the voters who approve $a$, $s(a) = |F(a)|$ for the approval score, $W = \{ a : s(a) = \max_b s(b) \}$ for the approval correspondence, and $f = \min W$ for the resolute rule.

**Claim 1 (correctness).** APPROVAL returns $f$.

*Proof.* Invariant of the outer loop of line L2: after the first $k$ ballots, $s[a] = |\{ i \le k : a \in S_i \}|$ for every $a$. For $k = 0$ this is line L1. The pass for ballot $k + 1$ runs lines L3 and L4 once for each member of $S_{k+1}$, since a set has no repeated members, so it adds 1 to $s[a]$ exactly when $a \in S_{k+1}$. That keeps the invariant. After $n$ passes, $s[a] = s(a)$. Line L5 computes the maximum of the finite nonempty list, line L6 builds $W \ne \emptyset$, and line L7 returns $\min W = f$.

**Claim 2 (anonymity and neutrality).** Permuting the voters leaves $W$ and $f$ unchanged. If every ballot is renamed by a permutation $\pi$ of $A$, then $W$ becomes $\pi(W)$.

*Proof.* $s(a)$ counts ballots and does not depend on their order. Under the renaming, $\pi(a)$ is in the renamed ballot $i$ exactly when $a \in S_i$, so the new score of $\pi(a)$ is $s(a)$, and the maximizers are renamed by $\pi$.

**Claim 3 (Pareto).** If $F(b) \subsetneq F(a)$, then $b \notin W$.

*Proof.* $s(b) = |F(b)| < |F(a)| = s(a) \le \max s$.

**Claim 4 (monotonicity).** If $w = f$ and $w \notin S_i$, then for the profile with $S_i$ replaced by $S_i \cup \{w\}$ the winner is still $w$.

*Proof.* The score of $w$ goes up by 1 and no other score changes. Before the change, $s(w) \ge s(c)$ for every $c$ and $s(w) > s(c)$ for every $c < w$. Both inequalities stay true and the first becomes strict, so $w$ is the unique maximizer.

**Claim 5 (consistency).** For approval profiles $P_1$ and $P_2$ of disjoint groups, if $W(P_1) \cap W(P_2) \ne \emptyset$, then $W(P_1 + P_2) = W(P_1) \cap W(P_2)$.

*Proof.* The scores add, $s_{P_1 + P_2} = s_{P_1} + s_{P_2}$. Each joined score is at most $\max s_{P_1} + \max s_{P_2}$, with equality exactly for the members of $W(P_1) \cap W(P_2)$. That set is not empty, so the bound is the joined maximum and its maximizers are this set.

**Claim 6 (dominance of the sincere ballot for dichotomous preferences).** Let a voter have a set $G \subseteq A$ of good candidates and only care whether the winner is in $G$. Fix the ballots of the other voters. If the voter casts $S$ and the winner $f_S$ is in $G$, then with the ballot $G$ the winner $f_G$ is in $G$ too.

*Proof.* Let $t$ be the scores of the other voters alone. With ballot $T$ the score of $a$ is $t(a) + [a \in T]$. Order the candidates by the key $(\text{score}, -\text{index})$; the winner is the unique candidate with the largest key. Suppose $f_G = x \notin G$. Then the key of $x$ with ballot $G$ is larger than the key of every $g \in G$. Change the ballot from $G$ to any $S$. The score of each $g \in G$ does not go up, since $g \in G$ already gave it the point, and the score of $x$ does not go down, since $x \notin G$ had no point from the voter. So the key of $x$ is still larger than the key of every $g \in G$, and the winner $f_S$ is not in $G$. By contraposition, $f_S \in G$ implies $f_G \in G$.

So the ballot $G$ is a dominant strategy for this voter. It is also sincere, since it approves exactly the good candidates.

**Claim 7 (plurality ballots).** If $|S_i| = 1$ for every $i$, the winner is the plurality winner of any profile of rankings whose tops are the approved candidates.

*Proof.* Then $s(a)$ is the number of voters whose single approved candidate, the top of their ranking, is $a$. This is the plurality score, and both rules break ties by the smallest index.

**Claim 8 (time).** APPROVAL runs in $O(n + m + L)$ time with $L = \sum_i |S_i|$, and in $O(m)$ extra space.

*Proof.* Line L1 costs $O(m)$. The outer loop does $n$ iterations, and the inner loop does $|S_i|$ unit-cost updates in iteration $i$, so the loops cost $O(n + L)$. Lines L5 to L7 scan $m$ counters. Only the counters and $W$ are stored. $\blacksquare$
