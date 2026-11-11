---
title: Graph reduction finds exactly the deadlocked processes, in any order
proves: [correctness]
status: full
---

**Model.** A state has $n$ processes and $m$ reusable resource types with $t(r)$ units each. $\mathit{alloc}[i]$ and $\mathit{req}[i]$ are vectors in $\mathbb{N}^m$, and $\mathit{avail} = t - \sum_i \mathit{alloc}[i] \ge 0$. For vectors, $x \le y$ means $x[r] \le y[r]$ for every $r$. A process $i$ is *blocked* when $\mathit{req}[i] \not\le \mathit{avail}$. The system grants a request only as a whole and only when it fits. A blocked process takes no step: it neither releases units nor changes its request. A process that is not blocked may take any step; in particular, once its request is granted it may release every unit it holds. A process is *deadlocked* in a state $S$ if it is blocked in every state reachable from $S$ (Holt 1972).

**Reduction.** A process $i$ is *reducible* with pool $w$ if $\mathit{req}[i] \le w$; reducing it replaces $w$ by $w + \mathit{alloc}[i]$. A reduction sequence starts with $w = \mathit{avail}$ and reduces distinct processes one at a time. It is *complete* if no remaining process is reducible at its end. Lines L1 to L8 of DETECT build a complete sequence: each pass reduces every process that is reducible when the pass reaches it, and the loop stops after a pass that reduces nothing.

For a set $F$ of processes, write $w(F) = \mathit{avail} + \sum_{i \in F} \mathit{alloc}[i]$. After a sequence that reduced the set $F$, the pool is $w(F)$, whatever the order.

**Lemma 1 (monotonicity).** If $F \subseteq G$, then $w(F) \le w(G)$. So a process that is reducible with pool $w(F)$ is reducible with pool $w(G)$.

*Proof.* $w(G) - w(F) = \sum_{i \in G \setminus F} \mathit{alloc}[i] \ge 0$. If $\mathit{req}[i] \le w(F)$, then $\mathit{req}[i] \le w(G)$. $\square$

**Theorem 1 (the order does not matter).** All complete reduction sequences reduce the same set of processes.

*Proof.* Let $A = (a_1, \ldots, a_k)$ and $B$ be two complete sequences, and let $F_A$ and $F_B$ be the sets they reduce. Suppose $F_A \not\subseteq F_B$, and let $a_j$ be the first process of $A$ that is not in $F_B$. Then $\{a_1, \ldots, a_{j-1}\} \subseteq F_B$, and $a_j$ was reducible with pool $w(\{a_1, \ldots, a_{j-1}\})$. By Lemma 1 it is reducible with pool $w(F_B)$, at the end of $B$. This contradicts the completeness of $B$. So $F_A \subseteq F_B$, and by symmetry $F_B \subseteq F_A$. $\square$

Let $F^*$ be this common set and $L$ the set of the other processes. DETECT returns $L$.

**Theorem 2 (reduction is exact).** A process is deadlocked in the current state if and only if it is in $L$.

*Proof.* First let $i \notin L$, and let $a_1, \ldots, a_k$ be a complete sequence with $i = a_j$. Here is a future in which $i$ is not blocked. For $s = 1, 2, \ldots, j$ in turn: the free units are $w(\{a_1, \ldots, a_{s-1}\})$, which contains $\mathit{req}[a_s]$, so the system grants the request of $a_s$, and then $a_s$ releases all its units, which leaves $w(\{a_1, \ldots, a_s\})$ free. Before its grant, $a_j = i$ is not blocked. So $i$ is not deadlocked. (If $i$ is not blocked at the start, the claim is immediate.)

Now let $i \in L$. Write $w^* = w(F^*)$; then $w^*[r] = t(r) - \sum_{q \in L} \mathit{alloc}[q][r]$. By completeness, every $q \in L$ has a type $r_q$ with $\mathit{req}[q][r_q] > w^*[r_q]$. We prove by induction on the length of a run from the current state that in every reachable state $T$, every $q \in L$ has the same $\mathit{alloc}[q]$ and $\mathit{req}[q]$ as now and is blocked. At the start, the free units of $r_q$ are $\mathit{avail}[r_q] \le w^*[r_q] < \mathit{req}[q][r_q]$, so $q$ is blocked. Suppose the claim holds in $T$. The free units in $T$ are $t$ minus the units held by all processes, which is at most $t$ minus the units held by $L$, that is at most $w^*$. So the request of each $q \in L$ does not fit in $T$, the system does not grant it, and $q$, being blocked, takes no step. The next step therefore leaves $\mathit{alloc}[q]$ and $\mathit{req}[q]$ unchanged for all $q \in L$, and in the new state the free units are again at most $w^*$, so each $q \in L$ is still blocked. Hence $i$ is blocked in every reachable state, and it is deadlocked. $\square$

**Theorem 3 (termination and cost).** DETECT stops after at most $n + 1$ passes of the loop of lines L2 to L7 and takes $O(m n^2)$ time.

*Proof.* Each pass that does not stop sets at least one more entry of $\mathit{finish}$ to true, and there are $n$ entries, so at most $n$ passes make progress and the next one stops. A pass runs line L5 for $n$ processes, each test compares $m$ entries, and line L6 adds $m$ entries; so a pass costs $O(mn)$, and $n + 1$ passes cost $O(m n^2)$. $\square$

**Corollary (single units).** If every type has one unit, the deadlocked processes are the processes from which a cycle of the wait-for graph is reachable. Indeed, with one unit, process $i$ is reducible exactly when every holder of every type it requests has already been reduced, that is, when all its successors in the wait-for graph are gone. A complete reduction is then the removal of vertices with no remaining successor, which removes exactly the vertices that reach no cycle: a vertex on a cycle is never the first of its cycle to be removed, and a vertex that reaches no cycle has finitely many paths, all ending at sinks, so it is removed after its successors.

$\blacksquare$
