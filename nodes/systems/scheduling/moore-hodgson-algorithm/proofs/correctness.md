---
title: The Moore-Hodgson algorithm keeps a largest on-time set of least total time
proves: [correctness]
status: full
---

Number the jobs $1, \ldots, n$ as in line L1, so that $d_1 \le d_2 \le \cdots \le d_n$, and let $J_k = \{1, \ldots, k\}$. Call a set $S$ of jobs *feasible* if all its jobs are on time when they run back to back from time $0$ in due date order. A feasible set is the on-time part of some schedule, and every schedule with $q$ on-time jobs gives a feasible set of size $q$: its on-time jobs, moved to the front in due date order, stay on time (this is the optimality of the due date order for the maximum lateness). Let $E_k$ be the set of jobs in $H$ after iteration $k$ of the loop, with $E_0 = \emptyset$. Write $p(S) = \sum_{j \in S} p_j$.

**Fact 1.** If $S \subseteq J_k$ is feasible, then $p(S) \le d_k$.

*Proof.* The last job $j$ of $S$ in due date order completes at $p(S)$ and is on time, so $p(S) \le d_j \le d_k$. $\square$

**Domination.** For a finite multiset $A$ of numbers, let $A_{(1)} \le A_{(2)} \le \cdots$ be its elements in increasing order. Say that $A$ *dominates* $B$ if $|B| \le |A|$ and $A_{(i)} \le B_{(i)}$ for $i = 1, \ldots, |B|$. For sets of jobs we apply this to their multisets of processing times. If $A$ dominates $B$, then the sum of the $|B|$ smallest elements of $A$ is at most the sum of $B$.

**Fact 2.** If $A$ dominates $B$, then $A \cup \{x\}$ dominates $B \cup \{x\}$ for any number $x$ (as multisets), and $A \cup \{x\}$ dominates $B$.

*Proof.* For a sorted list $a_{(1)} \le a_{(2)} \le \cdots$ with $a_{(0)} = -\infty$, the $i$-th smallest element of $A \cup \{x\}$ is $\min(a_{(i)}, \max(a_{(i-1)}, x))$, for each $i$ up to $|A| + 1$, with $a_{(|A|+1)} = +\infty$. This expression does not decrease when any $a_{(\cdot)}$ grows. Since $a_{(i)} \le b_{(i)}$ for $i \le |B|$, and $b_{(|B|+1)} = +\infty$ in the same convention, the $i$-th smallest of $A \cup \{x\}$ is at most the $i$-th smallest of $B \cup \{x\}$ for $i \le |B| + 1$, and $|B| + 1 \le |A| + 1$. For the second claim, the $i$-th smallest of $A \cup \{x\}$ is at most $a_{(i)} \le b_{(i)}$. $\square$

**Invariant $I_k$.** (a) $E_k \subseteq J_k$ is feasible, and $p(E_k)$ is the value of $t$ after iteration $k$. (b) $E_k$ dominates every feasible $S \subseteq J_k$.

$I_0$ holds, since $E_0 = J_0 = \emptyset$ and $t = 0$. Assume $I_{k-1}$, let $m = |E_{k-1}|$, and let $A = E_{k-1} \cup \{k\}$. After line L4, $H$ holds $A$ and $t = p(A)$.

**Case 1: line L5 does not fire,** so $p(A) \le d_k$ and $E_k = A$.

(a) The jobs of $E_{k-1}$ are on time in due date order by $I_{k-1}$. Job $k$ has the largest due date so far, so it goes last, and it completes at $p(A) \le d_k$. So $E_k$ is feasible.

(b) Let $S \subseteq J_k$ be feasible. If $k \notin S$, then $S \subseteq J_{k-1}$, $E_{k-1}$ dominates $S$, and by Fact 2 so does $A$. If $k \in S$, then $S - \{k\}$ is feasible (removing a job does not delay the others) and lies in $J_{k-1}$, so $E_{k-1}$ dominates $S - \{k\}$, and by Fact 2 $A$ dominates $S$.

**Case 2: line L5 fires,** so $p(A) > d_k$. Line L6 removes a job $\ell$ with $p_\ell$ largest in $A$, so $E_k = A - \{\ell\}$, $|E_k| = m$, and line L7 sets $t = p(E_k)$. The sorted times of $E_k$ are the first $m$ sorted times of $A$: $E_{k,(i)} = A_{(i)}$ for $i \le m$.

(b) Let $S \subseteq J_k$ be feasible. First, $|S| \le m$. If $k \notin S$, this is $I_{k-1}$. If $k \in S$, as in Case 1 the set $A$ dominates $S$. Suppose $|S| = m + 1 = |A|$. Then $A_{(i)} \le S_{(i)}$ for all $i$, so $p(A) \le p(S) \le d_k$ by Fact 1, against $p(A) > d_k$. So $|S| \le m$. Second, $A$ dominates $S$ in both cases (by Fact 2 when $k \notin S$). So for $i \le |S| \le m$, $E_{k,(i)} = A_{(i)} \le S_{(i)}$, and $E_k$ dominates $S$.

(a) If $\ell = k$, then $E_k = E_{k-1}$, which is feasible. If $\ell \ne k$, then $E_{k-1} \ne \emptyset$. The jobs of $E_{k-1} - \{\ell\}$ keep their relative order, and each starts no later than before, so each is still on time. Job $k$ goes last and completes at $p(A) - p_\ell \le p(E_{k-1})$, since $p_\ell \ge p_k$. The last job $j$ of $E_{k-1}$ in due date order completes at $p(E_{k-1})$ and is on time, so $p(E_{k-1}) \le d_j \le d_k$. So job $k$ is on time and $E_k$ is feasible.

So $I_k$ holds for all $k$.

**Theorem.** The order of line L8 has the least possible number of late jobs. Moreover, the set of its on-time jobs has the least total processing time among all feasible sets of the largest size.

*Proof.* By $I_n$(a), the jobs of $E_n$ are on time when they run first in due date order, so the schedule of line L8 has at most $n - |E_n|$ late jobs. Any schedule with $q$ on-time jobs gives a feasible set $S$ of size $q$, and by $I_n$(b), $q \le |E_n|$. So no schedule has fewer than $n - |E_n|$ late jobs. If $|S| = |E_n|$, domination gives $E_{n,(i)} \le S_{(i)}$ for every $i$, so $p(E_n) \le p(S)$. $\blacksquare$

**Ties.** The proof never uses how ties are broken, neither among equal due dates in line L1 (any such order is a due date order, and Fact 1 and the feasibility test hold for it) nor among equal processing times in line L6.
