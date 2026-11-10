---
title: The two-stacks queue makes O(1) amortized operator calls per operation, and one evict can make n calls
proves: [time.amortized, time.worst, space.extra]
status: full
---

We count calls of $\otimes$. Let $c_j$ be the number of calls made by the $j$-th operation, and let $|B|_j$ be the size of the back stack after it, with $|B|_0 = 0$.

**Per-operation counts.** INSERT makes exactly one call, in line L2. QUERY makes exactly one call, in line L12; line L11 reads a stored value. EVICT makes calls only in line L7, once per iteration of the loop, and the loop runs only when $F$ is empty and then runs exactly $|B|$ times, as shown in the correctness proof. So an EVICT makes $|B|$ calls if $F$ is empty and 0 calls if not.

**Potential.** Let $\Phi_j = |B|_j$. Then $\Phi_0 = 0$ and $\Phi_j \ge 0$ for all $j$. The amortized cost of operation $j$ is $\hat c_j = c_j + \Phi_j - \Phi_{j-1}$.

- INSERT: $c_j = 1$ and line L1 adds one item to $B$, so $\hat c_j = 1 + 1 = 2$.
- QUERY: $c_j = 1$ and $B$ does not change, so $\hat c_j = 1$.
- EVICT without a flip: $c_j = 0$ and $B$ does not change, so $\hat c_j = 0$.
- EVICT with a flip of $k = |B|_{j-1}$ items: $c_j = k$, and after the loop $B$ is empty, so $\hat c_j = k + 0 - k = 0$.

**Theorem 1.** Any sequence of $I$ inserts, $Q$ queries and any number of evicts, started from the empty structure, makes at most $2I + Q$ calls of $\otimes$. So each operation makes $O(1)$ calls amortized.

*Proof.* Summing the definition of $\hat c_j$ over the $N$ operations gives $\sum_j c_j = \sum_j \hat c_j - \Phi_N + \Phi_0 \le \sum_j \hat c_j$, since $\Phi_N \ge 0 = \Phi_0$. By the table, $\sum_j \hat c_j = 2I + Q$. $\square$

**Stack operations.** Count each push and each pop as one step as well. INSERT does one push, an evict without a flip does one pop, and an evict that flips $k$ items does $k$ pops, $k$ pushes and one more pop. With $\Phi = 3|B|$ and calls plus stack steps as the cost, INSERT costs $2 + 3 = 5$ amortized, an evict without a flip costs 1, and an evict with a flip costs $3k + 1 - 3k = 1$. So the total work, in calls and stack steps, is at most $5I + E + Q$ for $E$ evicts.

**Theorem 2.** For every $n \ge 1$ there is a sequence of operations in which one EVICT makes $n$ calls of $\otimes$, with $n$ items in the window just before it.

*Proof.* Start empty and insert $n$ items. No evict has run, so $F$ is empty and $B$ holds the $n$ items. The next EVICT finds $F$ empty in line L3, and its loop runs $n$ times, with one call in each run of line L7. $\square$

**Space.** In a state with $f$ items in $F$, the structure stores $2f$ values in $F$, $n - f$ values in $B$ and the value $a_B$, so $n + f + 1 \le 2n + 1$ values. For $n \ge 1$ it stores at least $n$ values, so the space is $\Theta(n)$. $\blacksquare$
