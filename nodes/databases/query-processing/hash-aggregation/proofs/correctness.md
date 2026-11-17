---
title: Hash aggregation outputs each group once with its correct aggregates
proves: [correctness]
status: full
---

We assume that MERGE is associative and commutative, and that $\text{state}(X \uplus Y) = \text{MERGE}(\text{state}(X), \text{state}(Y))$ for non-empty multisets $X$ and $Y$, where $\text{state}(\{\!\{v\}\!\}) = \text{INIT}(v)$. For a multiset $P$ of records and a key $k$, write $P_k$ for the records of $P$ with key $k$, and $\sigma(P_k)$ for the MERGE of their states, in any order. By the assumptions, $\sigma(P_k)$ does not depend on the order.

**Lemma (one pass).** Run lines L4 to L8 on a multiset $P$ with $m \ge 1$. Let $K$ be the set of keys of $P$ and $K_T$ the set of keys in $T$ after line L8. Then:
1. For each $k \in K_T$, $T[k] = \sigma(P_k)$.
2. For each $k \in K \setminus K_T$, all records of $P_k$ are in the same list $Q[h_\ell(k) \bmod F]$, and no list holds a record of a key of $K_T$.
3. If some record is spilled, then $|K_T| = m$.

*Proof.* No line removes a key from $T$, and line L7 adds a key only when $|T| < m$. Fix $k \in K$ and its first record $r_1$ in the scan.

If line L7 puts $k$ into $T$ at $r_1$, then at each later record $r$ of $k$, the test of line L6 is true, and line L6 merges the state of $r$ into $T[k]$. No record of $k$ is spilled. After the pass, $T[k]$ is the MERGE of the states of all records of $P_k$, which is $\sigma(P_k)$. This shows 1 for $k$, and the second part of 2.

If $k$ is not put into $T$ at $r_1$, then $k \notin T$ and $|T| \ge m$ at that time, so $|T| = m$. From then on line L7 never runs its assignment, so $T$ keeps the same $m$ keys, and $k$ never enters $T$. Each record of $k$, including $r_1$, fails both tests and goes to line L8, to the list $Q[h_\ell(k) \bmod F]$, which depends only on $k$ and $\ell$. This shows 2 for $k$. The same argument shows 3: a spill happens only when $|T| = m$, and $T$ does not shrink. $\square$

**Lemma (progress).** Each list $Q[i]$ pushed at line L11 has at most $|K| - m$ distinct keys.

*Proof.* A list is pushed only if it is not empty, so some record was spilled, and by part 3 $|K_T| = m$. By part 2, the keys of $Q[i]$ are in $K \setminus K_T$, which has $|K| - m$ keys. $\square$

**Theorem.** HASH-AGGREGATE stops, and outputs each key $k$ of the input exactly once, with $\text{FINAL}(\sigma(R_k))$, where $R_k$ is the set of level-0 records of key $k$.

*Proof.* Termination: assign to a stack entry $(P, \ell)$ the number of distinct keys of $P$. By the progress lemma, each entry that a pass pushes has a value at least $m \ge 1$ less than the popped entry. A pass pushes at most $F$ entries. So the tree of entries has depth at most $\lceil d/m \rceil$ and at most $F^{\lceil d/m \rceil}$ nodes, and the loop of line L2 ends.

Invariant of line L2: for each input key $k$, exactly one of the following holds. (a) $k$ was output once, with $\text{FINAL}(\sigma(R_k))$, and no record of $k$ is on the stack. (b) $k$ was not output, and the records of $k$ on the stack all lie in one entry $(P, \ell)$, with $\sigma(P_k) = \sigma(R_k)$.

At the start, the stack holds all level-0 records in one entry, and nothing was output, so (b) holds for each key. Assume the invariant before a pass that pops $(P, \ell)$. A key with no record in $P$ is not changed by the pass. For a key $k$ of $P$, (b) holds, so all its stack records were in $P$ and $\sigma(P_k) = \sigma(R_k)$. If $k \in K_T$, part 1 gives $T[k] = \sigma(P_k) = \sigma(R_k)$, line L9 outputs $\text{FINAL}(\sigma(R_k))$ once, and by part 2 no record of $k$ is pushed, so (a) holds. If $k \notin K_T$, part 2 puts all of $P_k$, with the same states, into one list, which line L11 pushes as one entry $(Q[i], \ell + 1)$, so (b) holds with $\sigma(Q[i]_k) = \sigma(P_k) = \sigma(R_k)$.

At the end the stack is empty. Each input key has at least one record, so (b) is false for it, and (a) holds. $\blacksquare$

**Remark.** The output does not depend on the hash functions $h_\ell$. They only decide how the spilled keys are split, which changes the cost and not the answer.
