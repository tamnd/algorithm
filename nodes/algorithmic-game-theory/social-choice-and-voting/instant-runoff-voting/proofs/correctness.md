---
title: Correctness and properties of instant-runoff voting
proves: [correctness]
status: full
---

Let $A = \{0, \ldots, m - 1\}$ with $m \ge 1$, and let $P = (r_1, \ldots, r_n)$ be ballots, each a sequence of distinct candidates, best first. For $C \subseteq A$, ballot $i$ counts for the first entry of $r_i$ that is in $C$, if there is one. Let $t_C(a)$ be the number of ballots that count for $a$ and $T_C = \sum_{a \in C} t_C(a)$.

The direct rule starts with $C = A$ and repeats: if some $a \in C$ has $2 t_C(a) > T_C$, or $C = \{a\}$, return $a$; else remove from $C$ the element $x$ with the smallest $t_C(x)$, the largest index among ties. Call the sequence of sets it visits $C_0 = A \supsetneq C_1 \supsetneq \cdots$.

**Claim 1 (invariant).** At the start of the $k$-th pass of line L4, the set $C$ of the method is $C_k$, and for every $a \in C$, $pile[a]$ is the set of ballots that count for $a$ with respect to $C$. For every ballot $i$ on $pile[a]$, $r_i[ptr[i]] = a$, and every entry of $r_i$ before position $ptr[i]$ is outside $C$.

*Proof.* By induction on $k$. For $k = 0$, $C = A$, every nonempty ballot counts for its first entry, and line L2 puts it on that pile with $ptr[i] = 1$. Empty ballots count for nobody and are on no pile.

Assume the claim at pass $k$ and that the method does not return. Then $|pile[a]| = t_{C_k}(a)$, so line L7 picks the same $x$ as the direct rule, and line L8 makes $C = C_k \setminus \{x\} = C_{k+1}$. Take a ballot $i$. If it counted for some $a \ne x$, all its entries before $a$ are outside $C_k$, hence outside $C_{k+1}$, and $a \in C_{k+1}$, so it still counts for $a$; the method does not touch it. If it counted for $x$, it is on $pile[x]$, and line L10 moves $ptr[i]$ to the first later entry in $C_{k+1}$; all entries before it are outside $C_{k+1}$ (the ones before $x$ by the hypothesis, $x$ itself, and the skipped ones by line L10). So the ballot now counts for $r_i[ptr[i]]$, and line L11 puts it on that pile, or it is exhausted and counts for nobody. If it counted for nobody, it still counts for nobody. Clearing $pile[x]$ completes the step.

**Claim 2 (correctness).** The method returns the winner of the direct rule.

*Proof.* By Claim 1, in each pass line L4 computes $T = T_{C_k}$ and line L5 tests the same condition as the direct rule. If it holds, both return the same $a$. Otherwise both remove the same $x$. Each pass removes one candidate, so after at most $m - 1$ passes $|C| = 1$ and the method returns.

**Claim 3 (early stop).** If $2 t_C(a) > T_C$ for some $a \in C$, then eliminating until one candidate is left, by the same elimination rule, also elects $a$.

*Proof.* While $a$ is in $C$ and $|C| \ge 2$, every $b \in C \setminus \{a\}$ has $t_C(b) \le T_C - t_C(a) < t_C(a)$, so $a$ is not the candidate of smallest count and is not removed. Removing another candidate does not decrease $t_C(a)$, since a ballot that counts for $a$ still counts for $a$, and it does not increase $T_C$, since a ballot can only become exhausted. So the condition $2 t_C(a) > T_C$ holds in every later round, and $a$ is the last candidate left.

**Claim 4 (majority criterion).** If more than $n/2$ ballots have $a$ first, the rule returns $a$ in round 1.

*Proof.* $t_A(a) > n/2 \ge T_A/2$, and no other candidate can also have more than half.

**Claim 5 (Condorcet loser criterion).** Assume full rankings. If $\ell$ loses to every other candidate in pairs, that is $n_P(\ell, b) < n_P(b, \ell)$ for all $b \ne \ell$, where $n_P(x, y)$ is the number of voters who rank $x$ above $y$, then the rule does not return $\ell$ (for $m \ge 2$).

*Proof.* With full rankings no ballot is exhausted, so $T_C = n$. If the rule returns $\ell$ at a round with $|C| \ge 3$ or by a strict majority, then $t_C(\ell) > n/2$; every ballot that counts for $\ell$ ranks $\ell$ above every other member of $C$, so for any $b \in C \setminus \{\ell\}$, $n_P(\ell, b) > n/2$, a contradiction. Otherwise $\ell$ can only be returned when $C = \{\ell\}$, so the rule must pass through a round with $C = \{\ell, b\}$ for some $b$. In that round each ballot counts for the one of $\ell, b$ that it ranks higher, so $t_C(\ell) = n_P(\ell, b) < n_P(b, \ell) = t_C(b)$. The two counts add up to $n$, so $b$ has a strict majority and is returned. In no case is $\ell$ returned.

**Claim 6 (Pareto).** Assume full rankings and $n \ge 1$. If every voter ranks $a$ above $b$, the rule does not return $b$.

*Proof.* While $a \in C$, no ballot counts for $b$, because $a$ comes before $b$ on every ballot. Suppose $a$ is removed in some round while $b$ is in $C$. Then $t_C(a) \le t_C(b) = 0$, so $a$ had no ballots and its removal moves none: $t(b)$ stays 0. From then on, as long as $b$ is in $C$, the smallest count in $C$ is 0, so every removed candidate has count 0 and moves no ballots, and $t(b)$ stays 0. Since $T_C = n \ge 1$, some candidate in $C$ has a positive count, so $b$ never has a majority, and $C = \{b\}$ would need all candidates with ballots to be removed, which never happens while $b$, with count 0, is still in. Hence $b$ is removed before the end, and it is not returned.

**Claim 7 (anonymity).** The winner does not depend on the order of the ballots.

*Proof.* Every quantity that the direct rule uses, $t_C$ and $T_C$, counts ballots and does not depend on their order.

**Claim 8 (two candidates).** If $m = 2$ and the ballots are full rankings, the rule returns 0 exactly when $2 n_P(0, 1) \ge n$.

*Proof.* In round 1, $t(0) = n_P(0, 1)$ and $t(1) = n - t(0)$. If $2 t(0) > n$ the rule returns 0, and if $2 t(1) > n$ it returns 1. If $t(0) = t(1)$, neither has a majority, the tie rule removes 1, and the rule returns 0.

**Claim 9 (time).** The method runs in $O(L + m^2)$ time with $L = \sum_i |r_i|$, plus $O(n + m)$ for the setup, and in $O(n + m)$ extra space.

*Proof.* Lines L1 and L2 take $O(n + m)$ time. Each round removes one candidate, so there are at most $m$ rounds, and lines L4 to L8 cost $O(m)$ per round. In lines L9 to L11 each unit of work moves a pointer forward by one entry, and the pointer of ballot $i$ never passes the end of $r_i$, so the total over all rounds is $O(n + L)$. A ballot is on at most one pile at a time, so the piles use $O(n + m)$ space, and the pointers use $O(n)$. $\blacksquare$
