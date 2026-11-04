---
title: FKS-SEARCH answers membership correctly, and FKS-BUILD ends with probability 1
proves: [correctness, termination]
status: full
---

Let $S \subseteq \{0, \ldots, p - 1\}$ be a set of $n$ distinct keys, with $p$ prime. We write $n_j = |S_j|$ for the size of bucket $j$ after the loop of lines L2 to L5.

**Lemma 1 (the stored table).** When FKS-BUILD returns, for each $j$ with $n_j > 0$, the array $T_j$ holds exactly the keys of $S_j$, and each $x \in S_j$ is in the slot $T_j[h_j(x)]$. For each $j$ with $n_j = 0$, $m_j = 0$.

*Proof.* Fix $j$. Line L7 sets $m_j = n_j^2$, so $m_j = 0$ exactly when $n_j = 0$. If $n_j > 0$, the loop of lines L9 and L10 ends only with a function $h_j$ that gives distinct slots to distinct keys of $S_j$. Line L11 writes each $x \in S_j$ to $T_j[h_j(x)]$. Two keys of $S_j$ never write the same slot, so no write is lost, and after line L11 the slots of $T_j$ that are not NIL hold exactly the $n_j$ keys of $S_j$. No later step changes $T_j$. $\square$

**Theorem 1 (search).** After FKS-BUILD$(S)$, FKS-SEARCH$(x)$ returns true if $x \in S$ and false if $x \notin S$, for each $x \in \{0, \ldots, p - 1\}$.

*Proof.* Let $j = h(x)$, the value of line L12.

Case $x \in S$. By line L4, $x \in S_j$, so $n_j \ge 1$ and $m_j \ge 1$, and line L13 does not return. By Lemma 1, $T_j[h_j(x)] = x$, so line L14 returns true.

Case $x \notin S$. If $m_j = 0$, line L13 returns false. Else, by Lemma 1, the slot $T_j[h_j(x)]$ holds NIL or a key of $S_j \subseteq S$. Neither is equal to $x$, since $x \notin S$. So line L14 returns false. $\square$

**Theorem 2 (termination).** FKS-BUILD ends with probability 1, and the expected number of trials of each loop is less than 2.

*Proof.* The complexity proof shows that one trial of lines L3 to L5 meets the test of line L5 with probability $q > 1/2$, and that, for each $j$ with $n_j > 0$, one trial of lines L9 and L10 meets the test of line L10 with probability $q_j > 1/2$. The trials of one loop use independent random choices, so the probability that the first $t$ trials all fail is $(1 - q)^t < 2^{-t}$, which tends to 0. So each loop ends with probability 1, and the number of its trials has a geometric distribution with mean $1/q < 2$ (or $1/q_j < 2$). There are $m + 1$ loops, a finite number, so the build ends with probability 1. $\blacksquare$
