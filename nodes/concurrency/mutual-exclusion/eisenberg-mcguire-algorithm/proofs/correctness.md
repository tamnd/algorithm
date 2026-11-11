---
title: The Eisenberg-McGuire algorithm gives mutual exclusion, deadlock freedom and a bypass of at most n - 1
proves: [correctness]
status: full
---

We use the pseudocode of the page, with processes $0, \ldots, n - 1$ and all arithmetic on process numbers mod $n$. At the start every flag is IDLE and $turn$ is some process number. The registers are atomic and the memory is sequentially consistent; each access in the pseudocode is one step. A process stays in the critical section for a finite time, and a process that is not in its remainder section takes another step eventually.

A *round* of process $x$ is one pass through the loop, from L2 to the next L2 or to the exit of the loop. We say that $x$ *enters* at its write at L11; the critical section follows at once. Only process $x$ writes $flag[x]$. Note these facts about the code:

- (F1) $flag[x] = \text{IDLE}$ while $x$ is in its remainder section, and $flag[x] \ne \text{IDLE}$ from its first write at L2 until its write at L15.
- (F2) Process $x$ enters only at the end of a round in which it wrote ACTIVE at L6, then read $flag[y] \ne \text{ACTIVE}$ for each $y \ne x$, then read $turn = t$ at L9 with $t = x$ or, at L10, $flag[t] = \text{IDLE}$.
- (F3) After the write at L6 of the round in which $x$ enters, $x$ does not write $flag[x]$ until L15. So $flag[x] = \text{ACTIVE}$ during that time.
- (F4) The register $turn$ is written only at L11 (an entry) and at L14 (in an exit).

For an entry $e$ of a process, let $a(e)$ be the time of its write at L6 in the entering round and $f(e)$ the time of its write at L15 in the exit after $e$. By (F3), the flag of the process is ACTIVE from $a(e)$ to $f(e)$.

## Mutual exclusion

**Lemma 1.** Let $e$ be an entry of process $q$ and $e'$ a later entry of a process $j \ne q$. Let $r$ be the time at which $j$ reads $flag[q]$ at L8 in the round that ends with $e'$. Then $f(e) < r$. In particular, $q$ has finished its exit before $j$ enters.

*Proof.* We have $a(e') < r < e'$. There are three cases.

- $r < a(e)$. Process $q$ reads $flag[j]$ in its entering round at a time $r_q$ with $a(e) < r_q < e$. Then $a(e') < r < a(e) < r_q < e < e' < f(e')$, so $flag[j] = \text{ACTIVE}$ at $r_q$ by (F3), and $q$ does not enter in that round. This contradicts (F2).
- $a(e) < r < f(e)$. Then $flag[q] = \text{ACTIVE}$ at $r$ by (F3), and $j$ does not enter in that round. This contradicts (F2).
- $f(e) < r$. This is the claim. $\square$

**Theorem 1 (mutual exclusion).** At any time, at most one process is in its critical section or its exit section.

*Proof.* Suppose that $q \ne j$ are both in the critical or exit section at time $\tau$, after entries $e$ and $e'$, and that $e$ comes before $e'$. By Lemma 1, $q$ finished its exit before $e' \le \tau$. This is a contradiction. If $q = j$ there is nothing to prove. $\square$

**Lemma 2 (turn).** After an entry $e$ of process $j$, $turn = j$ until the write of $j$ at L14 in the exit that follows. If that write sets $turn \leftarrow z$, then $turn = z$ until the next entry of any process.

*Proof.* By (F4), only entries and exits write $turn$. Between $e$ and the next entry, only $j$ is in its critical or exit section, by Theorem 1, and $j$ writes $turn$ once in its exit. $\square$

## Bounded bypass

Fix a process $i$, and let $\tau_0$ be the time of its first write at L2 in some passage. For a process number $x$, let $d(x) = (i - x) \bmod n$, the number of steps forward from $x$ to $i$. So $d(i) = 0$, and $d(x + 1) = d(x) - 1$ when $x \ne i$.

**Theorem 2 (bypass at most $n - 1$).** Between $\tau_0$ and the next entry of $i$, other processes enter at most $n - 1$ times.

*Proof.* Let $e_1, e_2, \ldots$ be the entries of processes other than $i$ after $\tau_0$ and before the next entry of $i$, in time order, and let $p_k$ be the process of $e_k$. We show that $d(p_{k + 1}) < d(p_k)$ for each $k$. Since $1 \le d(p_k) \le n - 1$, this gives at most $n - 1$ entries.

Let $j = p_k$ and $m = p_{k + 1}$. In its exit after $e_k$, process $j$ reads $turn = j$ at L12 (Lemma 2). It then reads $flag[j + 1], flag[j + 2], \ldots$ and stops at the first $z$ whose flag it reads as not IDLE. By (F1), $flag[i] \ne \text{IDLE}$ during the whole exit, since $i$ has passed $\tau_0$ and has not entered. So the scan stops at $i$ or before it: $d(z) \le d(j + 1) = d(j) - 1$. Then $j$ writes $turn \leftarrow z$ at L14.

Now look at the round of $m$ that ends with $e_{k + 1}$. Its read of $turn$ at L9 comes after the write $turn \leftarrow z$ of $j$. If $m = j$, this holds because the round comes after the exit in the program of $j$. If $m \ne j$, Lemma 1 (with $q = j$) shows that $m$ reads $flag[j]$ at L8 after $f(e_k)$, and L9 comes after L8. By Lemma 2, $m$ reads $turn = z$. By (F2), $z = m$ or $m$ reads $flag[z] = \text{IDLE}$ at L10.

Suppose $z \ne m$. The flag of $z$ was not IDLE when $j$ read it in its exit. By (F1) it becomes IDLE only at L15 of $z$, and $z$ can be at L15 only in an exit after an entry. Between the read of $j$ and $e_{k + 1}$, only $j$ is in its critical or exit section (Theorem 1 and the choice of $e_{k + 1}$ as the next entry). So $flag[z] \ne \text{IDLE}$ when $m$ reads it, and $m$ does not enter in that round. This is a contradiction. So $m = z$, and $d(m) = d(z) < d(j)$. $\square$

If the scan of $j$ stops at $z = i$, the argument shows that the next entry after $e_k$ is an entry of $i$.

## Deadlock freedom and starvation freedom

The exit section is wait free: the flag of the exiting process is ACTIVE during the scan at L13, so the scan stops after at most $n$ reads.

**Theorem 3 (deadlock freedom).** In a fair run, if some process is in its entry section, then some process enters later.

*Proof.* Suppose not. Since exits are wait free, there is a time $t_1$ after which no process enters, no process is in its critical or exit section, and the set $P$ of processes in their entry sections is constant and not empty. By (F4), $turn$ is a constant $y$ after $t_1$. By (F1), $flag[x] = \text{IDLE}$ for $x \notin P$ and $flag[x] \ne \text{IDLE}$ for $x \in P$.

Let $i$ be the process of $P$ that comes first in the order $y, y + 1, y + 2, \ldots$. Take $j \in P$ with $j \ne i$. A round of $j$ that does not enter ends at L8 or L10 and starts a new round, and each new round reads $turn = y$ at L3. A scan of $j$ that starts from $y$ meets $i$ before $j$, reads $flag[i] \ne \text{IDLE}$, reads $turn = y$ again, and so on forever. So from some time $t_2$ on, every $j \in P \setminus \{i\}$ stays in phase 1 forever, with $flag[j] = \text{WAITING}$ from the write at L2 of its last round.

Process $i$ also starts new rounds, since it does not enter. Consider a round of $i$ that starts after $t_2$. It reads $turn = y$ and scans $y, \ldots, i - 1$, which are not in $P$, so it reads only IDLE and passes phase 1. In phase 2 no other flag is ACTIVE. At L9 it reads $t = y$, and either $y = i$ or $y \notin P$, so $flag[y] = \text{IDLE}$. So $i$ enters. This is a contradiction. $\square$

**Theorem 4 (starvation freedom).** In a fair run, every process that starts its entry section enters the critical section.

*Proof.* Suppose that $i$ starts its entry section and never enters. By Theorem 3, used again and again, other processes enter infinitely often after $\tau_0$. This contradicts Theorem 2. $\blacksquare$
