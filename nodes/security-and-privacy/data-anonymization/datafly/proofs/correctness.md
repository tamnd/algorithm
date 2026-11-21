---
title: Datafly stops and releases a k-anonymous table
proves: [correctness]
status: full
---

The table $T$ has $n$ rows and $d$ quasi-identifier attributes. Attribute $a$ has a hierarchy with levels $0, 1, \ldots, h_a$, and level $h_a$ maps every value of $a$ to one value. Let $h = \sum_a h_a$, and let $k \ge 1$. We write $T_v$ for $T$ generalized by the vector $v$. Line L4 computes $s$, the set of rows of $T_v$ whose combination of values occurs fewer than $k$ times in $T_v$.

**Lemma 1.** If line L5 does not stop the loop, then line L6 picks an attribute $a$ with $v_a < h_a$.

*Proof.* Assume that each attribute has one distinct value in $T_v$. Then all the $n$ rows of $T_v$ are equal. If $n \ge k$, no row is in a group of fewer than $k$ rows, so $|s| = 0$. If $n < k$, all rows are in $s$, so $|s| = n < k$. In both cases $|s| \le k$, and line L5 stops the loop. So if the loop goes on, some attribute has at least 2 distinct values in $T_v$, and line L6 picks an attribute $a$ with the most distinct values, so with at least 2. Level $h_a$ gives one value, so $v_a < h_a$. $\square$

**Theorem.** DATAFLY stops after at most $h + 1$ rounds of the loop of line L2. It returns $(v, s)$ with $0 \le v_a \le h_a$ for each $a$ and $|s| \le k$, and the table $T_v$ without the rows of $s$ is k-anonymous.

*Proof.* Line L1 sets $v = (0, \ldots, 0)$. By Lemma 1, each round that does not stop raises one level $v_a$ by one with $v_a < h_a$ before the step (line L7). So $0 \le v_a \le h_a$ stays true, and the height $\sum_a v_a$ goes up by one in each such round. The height is at most $h$, so at most $h$ rounds go on, and the next round stops. This gives at most $h + 1$ rounds.

The loop stops only at line L5, so $|s| \le k$ at line L8. Let $R$ be the rows of $T_v$ that are not in $s$. Each row of $R$ has a combination of values that occurs at least $k$ times in $T_v$. All the rows with this combination are outside $s$, because $s$ holds a row exactly when its combination occurs fewer than $k$ times. So each combination of $R$ occurs at least $k$ times in $R$, and $R$ is k-anonymous. $\blacksquare$

**Remark.** The theorem says nothing about the quality of $v$. The page gives a table where Datafly returns a vector of height 2 while a vector of height 1 also has at most $k$ rows to suppress. Datafly is a heuristic for the choice of $v$, and only the k-anonymity of the release is a theorem.
