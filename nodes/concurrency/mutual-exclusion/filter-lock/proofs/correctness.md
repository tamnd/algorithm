---
title: The filter lock gives mutual exclusion and starvation freedom, but no bound on bypass
proves: [correctness]
status: full
---

We use the pseudocode of the page, with processes $0, \ldots, n-1$, $n \ge 2$, and levels $1, \ldots, n-1$. The registers are atomic, and the memory is sequentially consistent, so a run is one sequence of steps. A process stays in the critical section for a finite time, and a process that is not in its remainder section takes another step eventually.

**Terms.** A *passage* of process $i$ starts with its first step of the entry section and ends with its write of L8. Process $i$ *passes level* $\ell$ when it leaves the loop L4 to L7 of level $\ell$. At a time $t$, process $i$ is *above* $\ell$ if it has passed level $\ell$ in its current passage and has not yet written L8. To simplify the induction, every process in a passage is above $0$. A process in the critical section is above $n - 1$. During a passage, $level[i]$ only grows, and it becomes $0$ again only at L8. So if process $i$ has written $level[i] \leftarrow \ell$ in its current passage, then $level[i] \ge \ell$ until the end of the passage.

**Lemma 1.** For $0 \le \ell \le n - 1$, at any time at most $n - \ell$ processes are above $\ell$.

*Proof.* By induction on $\ell$. For $\ell = 0$ there are only $n$ processes. Let $\ell \ge 1$, and assume the claim for $\ell - 1$. Suppose that at time $T$ a set $S$ of $n - \ell + 1 \ge 2$ processes is above $\ell$. Each $B \in S$ wrote $level[B] \leftarrow \ell$ and then $victim[\ell] \leftarrow B$ at a time $w_B$ in its current passage, before $T$. Let $w$ be the last write of $victim[\ell]$ before $T$, by a process $C$. From $w$ to $T$, $victim[\ell] = C$.

First we show this fact: *process $C$ does not pass level $\ell$ between $w$ and $T$*. Assume it does. The write $w$ is the write of L3 of level $\ell$ in a passage of $C$, and in that passage $C$ reads $victim[\ell]$ only after $w$, and gets $C$. So $C$ passes by its other exit: a full scan in L6, after $w$, in which every read of $level[k]$ returns a value smaller than $\ell$. Take $B \in S$ with $B \ne C$; it exists because $|S| \ge 2$. Since $w$ is the last write of $victim[\ell]$ and $B \ne C$, $w_B < w$. So $B$ wrote $level[B] \leftarrow \ell$ before $w$, and $level[B] \ge \ell$ from then until $T$. The read of $level[B]$ in the scan of $C$ comes after $w$ and before $T$, so it returns at least $\ell$. This is a contradiction, and the fact holds.

Now there are two cases.

- *$C \in S$.* Then $C$ wrote $victim[\ell]$ in its current passage, at $w_C \le w$, and it does not write $victim[\ell]$ twice in one passage, so $w_C = w$. Process $C$ is above $\ell$ at $T$, so it passed level $\ell$ after $w$ and before $T$. This contradicts the fact.
- *$C \notin S$.* The passage of $C$ that contains $w$ cannot have ended before $T$, because a passage that ends passes every level, and by the fact $C$ did not pass level $\ell$ after $w$. So at $T$, process $C$ is still in that passage, it has not passed level $\ell$, and it has passed level $\ell - 1$ (or $\ell = 1$). So $C$ is above $\ell - 1$ but not above $\ell$. Then the $n - \ell + 2$ processes of $S \cup \{C\}$ are all above $\ell - 1$, which contradicts the claim for $\ell - 1$.

Both cases are impossible, so at most $n - \ell$ processes are above $\ell$. $\square$

**Theorem 1 (mutual exclusion).** At most one process is in the critical section at any time.

*Proof.* A process in the critical section is above $n - 1$, and by Lemma 1 at most $n - (n - 1) = 1$ process is above $n - 1$. $\square$

**Lemma 2.** Assume that every run is fair. For each level $\ell$, a process that writes $victim[\ell]$ at L3 later finishes its passage.

*Proof.* By induction on $\ell$ downward, from $\ell = n - 1$ to $\ell = 1$. Assume the claim for all levels larger than $\ell$; for $\ell = n - 1$ there are none. If a process passes level $\ell$, then it finishes its passage: if $\ell < n - 1$ it writes $level$ and $victim[\ell + 1]$ at once, since L2 and L3 have no waiting, and the claim for $\ell + 1$ applies; if $\ell = n - 1$ it enters the critical section, stays there for a finite time, and then writes L8.

So assume that process $i$ writes $victim[\ell]$ at time $w_i$ and then never passes level $\ell$. It keeps taking steps in the loop L4 to L7.

(a) *No process writes $victim[\ell]$ after $w_i$.* Otherwise, after that write $victim[\ell] \ne i$ forever, because only $i$ writes the value $i$. The next read of L5 by $i$ returns a value other than $i$, and $i$ passes level $\ell$.

(b) *There is a time $T_1$ after which $level[j] < \ell$ for every $j \ne i$.* Look at a process $j \ne i$ at time $w_i$.
- If $j$ is above $\ell$, it finishes its passage, by the first paragraph.
- If $j$ waits in the loop of level $\ell$, it wrote $victim[\ell]$ before $w_i$, so now $victim[\ell] \ne j$ forever, and $j$ passes level $\ell$ at its next read of L5. Then it finishes its passage.
- If $j$ has written $level[j] \leftarrow \ell$ but not yet $victim[\ell]$, it writes $victim[\ell]$ at its next step, after $w_i$. This contradicts (a), so there is no such $j$.
- Otherwise $level[j] < \ell$.

After $j$ finishes its passage, or if $level[j] < \ell$ already, $level[j]$ can become $\ell$ or more only by a write of L2 at level $\ell$, and that write is followed at once by a write of $victim[\ell]$, which (a) does not allow. So from some time on, $level[j] < \ell$ forever. Let $T_1$ be the latest of these times over all $j \ne i$.

After $T_1$, process $i$ starts a new turn of its loop: it reads $victim[\ell] = i$ at L5 and then reads $level[k] < \ell$ for every $k \ne i$ in L6, so it passes level $\ell$ at L7. This is a contradiction. $\square$

**Theorem 2 (starvation freedom).** In a fair run, every process that starts its entry section enters the critical section.

*Proof.* The process writes $level[i] \leftarrow 1$ and $victim[1] \leftarrow i$ without waiting, so by Lemma 2 it finishes its passage, and a passage goes through the critical section. $\square$

Deadlock freedom follows from Theorem 2.

**Theorem 3 (no bound on bypass for $n \ge 3$).** For every $m$ there is a run in which process $0$ has finished its doorway (L2 and L3 of level 1), and the other processes enter the critical section $m$ times before process $0$ enters. In the same run, process $1$ starts its doorway after process $0$ finishes its doorway and enters first, so the lock is not first come, first served.

*Proof.* Processes $3, \ldots, n-1$ stay in their remainder sections, with $level = 0$. Process $0$ writes $level[0] \leftarrow 1$ and $victim[1] \leftarrow 0$, and then takes no step until the end of the construction. Process $1$ writes $level[1] \leftarrow 1$ and $victim[1] \leftarrow 1$. Let $a = 1$ and $b = 2$, and repeat $m$ times:

1. Process $b$ writes $level[b] \leftarrow 1$ and $victim[1] \leftarrow b$ and stops at level 1.
2. Process $a$ reads $victim[1] = b \ne a$ and passes level 1. At each level $\ell \ge 2$ it writes $level[a] \leftarrow \ell$ and $victim[\ell] \leftarrow a$, reads $victim[\ell] = a$, and reads all $level[k] < \ell$, because process $0$ and process $b$ have level 1 and all others have level 0. So it passes every level and enters the critical section. Then it writes $level[a] \leftarrow 0$.
3. Exchange $a$ and $b$.

Each repetition is one entry of process 1 or process 2, and process 0 does not enter. The run is finite, so it can be continued fairly: after it, $victim[1] \ne 0$, and process 0 enters when it runs, as Theorem 2 says. For $n = 2$ the lock is Peterson's algorithm, which has bypass 1. $\blacksquare$
