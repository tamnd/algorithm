---
title: The safety check is exact, the banker stays safe, and from a safe state all processes can finish
proves: [correctness]
status: full
---

**Model.** There are $n$ processes and $m$ types with $t$ units in all. For vectors, $x \le y$ means $x[r] \le y[r]$ for every $r$. The tables satisfy $\mathit{alloc}[i] \ge 0$, $\mathit{need}[i] = \mathit{max}[i] - \mathit{alloc}[i] \ge 0$, and $\mathit{avail} = t - \sum_i \mathit{alloc}[i] \ge 0$. A process asks only for $\mathit{req} \le \mathit{need}[i]$. A process that holds its full claim finishes in finite time and releases all its units. A process may release units at any time. The allocator runs REQUEST and RELEASE atomically.

For a set $F$ of processes, let $w(F) = \mathit{avail} + \sum_{i \in F} \mathit{alloc}[i]$. A *partial sequence* is a list $a_1, \ldots, a_k$ of distinct processes with $\mathit{need}[a_s] \le w(\{a_1, \ldots, a_{s-1}\})$ for each $s$. A safe sequence is a partial sequence that contains all $n$ processes. A partial sequence is *complete* if no process outside it satisfies $\mathit{need}[j] \le w(\{a_1, \ldots, a_k\})$.

**Lemma 1 (monotonicity).** If $F \subseteq G$ then $w(F) \le w(G)$.

*Proof.* $w(G) - w(F) = \sum_{i \in G \setminus F} \mathit{alloc}[i] \ge 0$. $\square$

**Lemma 2.** All complete partial sequences contain the same set of processes.

*Proof.* Let $A$ and $B$ be complete, with sets $F_A$ and $F_B$. If $F_A \not\subseteq F_B$, let $a_j$ be the first element of $A$ outside $F_B$. Its predecessors in $A$ lie in $F_B$, so by Lemma 1, $\mathit{need}[a_j] \le w(\{a_1, \ldots, a_{j-1}\}) \le w(F_B)$, and $B$ is not complete. So $F_A \subseteq F_B$, and by symmetry the sets are equal. $\square$

**Theorem 1 (the check is exact).** SAFE returns a list if and only if the state is safe, and the list it returns is a safe sequence. Its cost is $O(m n^2)$.

*Proof.* The list $\mathit{order}$ built by lines L1 to L7 is a partial sequence: when line L6 appends $i$, $\mathit{work} = w(\text{the processes appended before})$, and line L5 checked $\mathit{need}[i] \le \mathit{work}$. The loop stops after a pass in which line L5 succeeds for no unfinished process, so the list is complete. If the state is safe, a safe sequence is a complete partial sequence with all $n$ processes, so by Lemma 2 the list of SAFE also has all $n$ processes, line L8 returns it, and it is a safe sequence. If the state is unsafe, no partial sequence has all $n$ processes, so line L8 returns nil. Each pass that does not stop appends a process, so there are at most $n + 1$ passes of $n$ tests of $m$ entries each. $\square$

**Lemma 3 (granting to the head, and the early stop).** Let the state $S$ be safe, let $\mathit{req} \le \mathit{need}[i]$ and $\mathit{req} \le \mathit{avail}$, and let $S'$ be the state after the tentative grant of line L11. If SAFE on $S'$ appends $i$ at some point, then $S'$ is safe. In particular, if $i$ is the first process of a safe sequence of $S$, then $S'$ is safe with the same sequence.

*Proof.* Write $w$ and $w'$ for the pools of $S$ and $S'$. For a set $F$: if $i \in F$, then $w'(F) = w(F)$, since the grant moves $\mathit{req}$ from $\mathit{avail}$ to $\mathit{alloc}[i]$; if $i \notin F$, then $w'(F) = w(F) - \mathit{req}$. Let $a_1, \ldots, a_k$ be the list of SAFE on $S'$ up to and including $a_k = i$. It is a partial sequence of $S$ too: for $a_s \ne i$ the need is the same and $w'(\ldots) \le w(\ldots)$; for $a_k = i$, $\mathit{need}'[i] = \mathit{need}[i] - \mathit{req} \le w(\{a_1, \ldots, a_{k-1}\}) - \mathit{req}$, so $\mathit{need}[i] \le w(\{a_1, \ldots, a_{k-1}\})$. Since $S$ is safe, Lemma 2 says that every complete extension of this partial sequence in $S$ contains all processes; take one. Its remaining processes $j \ne i$ have the same need in $S'$, and every set that contains $i$ has the same pool in $S$ and $S'$. So the extension is a safe sequence of $S'$.

If $i = i_1$ is the head of a safe sequence $i_1, \ldots, i_n$ of $S$, then $\mathit{need}'[i] = \mathit{need}[i] - \mathit{req} \le \mathit{avail} - \mathit{req} = \mathit{avail}'$, and for $k \ge 2$ the sets $\{i_1, \ldots, i_{k-1}\}$ contain $i$, so the same inequalities hold in $S'$. $\square$

**Theorem 2 (every reachable state is safe).** If the system starts with no allocation, every state reached through REQUEST and RELEASE is safe.

*Proof.* At the start, $\mathit{alloc} = 0$ and $\mathit{need}[i] = \mathit{max}[i] \le t = \mathit{avail}$, so every order is a safe sequence. REQUEST either leaves the state unchanged (lines L9, L10 and L13) or keeps a state that SAFE accepted (line L12), which is safe by Theorem 1. For RELEASE$(i, \mathit{rel})$, take a safe sequence $i_1, \ldots, i_n$ of the old state, with $i = i_k$. After the release, $\mathit{avail}$ grows by $\mathit{rel}$, $\mathit{alloc}[i]$ shrinks by $\mathit{rel}$, and $\mathit{need}[i]$ grows by $\mathit{rel}$. For a position $s \le k$ the pool $w(\{i_1, \ldots, i_{s-1}\})$ grows by $\mathit{rel}$, since $i$ is not among the earlier processes; this covers the larger need of $i$ at $s = k$. For $s > k$ the pool is unchanged. So the same sequence is safe. $\square$

**Theorem 3 (from a safe state all processes can finish, and there is no deadlock).** Let $S$ be safe with safe sequence $i_1, \ldots, i_n$.

(a) There is a continuation in which each process, in the order $i_1, \ldots, i_n$, asks for its whole remaining need, the banker grants it, and the process finishes and releases everything.

(b) In $S$, no process is deadlocked: for each waiting process there is a continuation in which the banker grants its request.

(c) In $S$, the processes are not all stuck: either some process is not waiting, or the banker grants the pending request of $i_1$.

*Proof.* (a) By Lemma 3, the banker grants $\mathit{need}[i_1]$ to $i_1$, since $\mathit{need}[i_1] \le \mathit{avail}$ and $i_1$ heads a safe sequence. Then $i_1$ holds its full claim, finishes, and releases all; the new state is safe with the sequence $i_2, \ldots, i_n$ (the release adds $\mathit{alloc}[i_1] + \mathit{need}[i_1]$ to $\mathit{avail}$, so every pool of the old sequence is matched). Induction on $n$ finishes the proof.

(b) Let $j$ wait with a request $\mathit{req} \le \mathit{need}[j]$. Run (a) for the processes before $j$ in the safe sequence. Then $j$ heads a safe sequence of the reached state, its need has not changed, and $\mathit{req} \le \mathit{need}[j] \le \mathit{avail}$, so Lemma 3 says the banker grants it.

(c) If $i_1$ waits, its request $\mathit{req} \le \mathit{need}[i_1] \le \mathit{avail}$ fits, and by Lemma 3 the tentative state is safe, so lines L10 and L12 grant it. $\square$

By Theorems 2 and 3, a system run under the banker never reaches a deadlock. Theorem 3 does not say that every process is eventually served in every run: a process can wait while the banker serves others, and that is a matter of the order of retries.

**Theorem 4 (unsafe does not imply deadlock).** There is an unsafe state from which every run finishes.

*Proof.* One type with $t = 3$; processes $p$ and $q$ with $\mathit{max} = 3$ and $\mathit{alloc} = 1$ each, so $\mathit{avail} = 1$ and $\mathit{need} = 2$ for both. No process satisfies $2 \le 1$, so no safe sequence exists, and the state is unsafe. Let the actual program of $p$ be "release the unit and finish", and that of $q$ be "get one unit, twice, then release all". If $p$ runs first, $q$ finds two free units and finishes. If $q$ runs first, it gets the free unit and then waits; $p$ is not blocked, releases its unit, and $q$ gets it and finishes. No run deadlocks. The test file checks this by exhaustive search, and checks that the same state does deadlock in some run when both processes ask for their full claims. $\square$

$\blacksquare$
