---
title: Knuth's algorithm gives mutual exclusion, deadlock freedom and starvation freedom
proves: [correctness]
status: full
---

We use the pseudocode of the page, with processes $0, \ldots, n - 1$ and all arithmetic on process numbers mod $n$. At the start $control[x] = 0$ for all $x$ and $k$ is some process number. The registers are atomic and the memory is sequentially consistent; each access in the pseudocode is one step. A process stays in the critical section for a finite time, and a process that is not in its remainder section takes another step eventually.

A *round* of process $x$ is one pass through the loop, from L2 to the next L2 or to L9. Phase 1 is L3 to L5, and phase 2 is L6 to L8. Only process $x$ writes $control[x]$. Note these facts about the code:

- (F1) $control[x] = 0$ while $x$ is in its remainder section, and $control[x] \in \{1, 2\}$ from its first write at L2 until L12.
- (F2) Process $x$ enters only at the end of a round in which it wrote $control[x] \leftarrow 2$ at L6 and then read $control[y] \ne 2$ for every $y \ne x$. After that write it does not write $control[x]$ again until L12.
- (F3) The register $k$ is written only at L10, with the number of the process that enters, and at L11, with the number of the process that leaves, minus 1. While a process is in the critical section, $k$ is its number.

(F3) holds because a process writes L10 just before it enters and L11 just after it leaves, and by Theorem 1 no other process enters or leaves in between.

**Theorem 1 (mutual exclusion).** At most one process is in the critical section at any time.

*Proof.* Suppose that processes $x \ne y$ are both in the critical section at time $\tau$. Let $w_x$ and $w_y$ be their writes of 2 at L6 in the rounds in which they entered, and say $w_x$ comes before $w_y$. By (F2), $control[x] = 2$ from $w_x$ until $x$ leaves, which is after $\tau$. Process $y$ reads $control[x]$ at L8 after $w_y$ and before $\tau$, so it reads 2 and does not enter in that round. This contradicts (F2). $\square$

(The proof of (F3) uses Theorem 1 only for writes at L10 and L11 made after entries, and Theorem 1 does not use (F3), so there is no circle.)

## Distance to a waiting process

Fix a process $i$. For a process number $x$, let $d(x) = (x - i) \bmod n$, a number from 0 to $n - 1$; so $d(i) = 0$, and $d(x - 1) = d(x) - 1$ when $x \ne i$.

**Lemma 1 (the scan).** Suppose that process $j \ne i$ reads $k = y$ at L3 and then passes phase 1 without going back to L3. If $d(j) > d(y)$, then $j$ read $control[i] = 0$ in that scan.

*Proof.* The scan reads $control$ of $y, y - 1, y - 2, \ldots$ and stops when it comes to $j$. Along this order, $d$ goes down by 1 at each step, from $d(y)$, until it comes to $i$, where $d = 0$. If $d(j) > d(y)$, the scan does not meet $j$ before it meets $i$, so it reads $control[i]$. The scan passes only if each value it reads is 0. $\square$

So, if $i$ has finished its doorway (the first write at L2) and has not left, then a process $j \ne i$ that passes phase 1 with a scan that started after that write has $d(j) \le d(y)$, where $y$ is the value it read at L3.

## Deadlock freedom

**Theorem 2 (deadlock freedom).** In a fair run, if some process is in its entry section, then some process enters later.

*Proof.* Suppose not. Choose $t_0$ so that after $t_0$ no process enters, no process is in its critical or exit section, and the set $P$ of processes in the entry section does not change. Then $P \ne \emptyset$, each process of $P$ goes around the loop forever, $k$ is a constant $y$ (by (F3)), $control[x] = 0$ for $x \notin P$, and $control[x] \in \{1, 2\}$ for $x \in P$ (by (F1)).

Let $i$ be the process of $P$ that comes first in the order $y, y - 1, y - 2, \ldots$. Each scan of $i$ after $t_0$ reads the $control$ of processes before $i$ in this order, which are not in $P$, so it reads only zeros and passes. Each scan of a process $j \in P$, $j \ne i$, that starts after $t_0$ meets $i$ before $j$ and reads $control[i] \ne 0$, so it fails. So after its current round, each such $j$ never reaches L6 again, and it writes $control[j] \leftarrow 1$ at L2 at the start of its next round. From some time on, $control[j] = 1$ for all $j \ne i$ in $P$, and $control[x] = 0$ for $x \notin P$. The next round of $i$ passes phase 1, writes 2, reads no other 2 in phase 2, and enters. This is a contradiction. $\square$

## Starvation freedom

**Theorem 3 (starvation freedom).** In a fair run, every process that starts its entry section enters the critical section.

*Proof.* Suppose that process $i$ starts its entry section and never enters. Let $\tau_0$ be the time of its first write at L2. From then on $control[i] \ne 0$ by (F1). Since $i$ is always in its entry section, Theorem 2, used again and again, shows that other processes enter infinitely often.

For a process $j \ne i$ in its entry section or in its critical section, let $y_j$ be the value of $k$ that $j$ read at its last read of L3 in the current passage, if it has made one. Each process has at most one passage in progress at $\tau_0$, and these passages end in finite time or stay in the entry section; let $\tau_1 \ge \tau_0$ be a time after which every $y_j$ comes from a read after $\tau_0$, and after which no process enters with a scan that started before $\tau_0$. (A process that stays in its entry section reads L3 again in each round, so such a time exists.) After $\tau_1$, define

$$D = \max\big(d(k),\ \max_j d(y_j)\big),$$

with the inner maximum over the processes $j \ne i$ that have a value $y_j$.

*Claim A: after $\tau_1$, $D$ never increases.* A read of $k$ at L3 sets $y_j$ to the current $k$, so $d(y_j) \le D$. A write $k \leftarrow j$ at L10 comes after a scan that started after $\tau_0$ and passed, so by Lemma 1, $d(j) \le d(y_j) \le D$. A write $k \leftarrow j - 1$ at L11 has $d(j - 1) = d(j) - 1$, and $d(j) \le D$ because $k = j$ just before it, by (F3). When a passage ends, its value $y_j$ goes away. No other step changes $k$ or a $y_j$.

*Claim B: if $D \le m$ from some time $t \ge \tau_1$ on, and $m \ge 1$, then $D \le m - 1$ from some later time on.* Let $x = i + m$, the only process with $d(x) = m$.

1. No process $j$ with $d(j) > m$ enters after $t$, by Lemma 1 and $d(y_j) \le m$; and such a $j$ is not in the critical section at $t$, since then $k = j$ by (F3) and $d(k) \le m$.
2. So after $t$, the value $x$ is written to $k$ only by $x$ itself at L10: the only other write of the value $x$ is $k \leftarrow (x + 1) - 1$ by process $x + 1$ at L11, and $x + 1$ is either $i$, which never enters, or has $d(x + 1) = m + 1$.
3. Process $x$ enters at most once after $t$. If it enters twice, then for the second entry it read $k = x$ at L3, since $d(x) = m \le d(y_x) \le m$ forces $y_x = x$. That read comes after the first exit of $x$, which wrote $k \leftarrow x - 1 \ne x$, and before its own next write at L10. By item 2 no step in between writes $x$ to $k$. This is a contradiction.
4. So from some time on, $x$ is in neither its critical section nor its exit section, and never writes $k$ again. From the next time on that $k \ne x$, $k$ stays $\ne x$ by item 2; such a time comes, because by (F3) $k = x$ only while $x$ is in its critical section, or until the next write of $k$, and other processes enter infinitely often.
5. After that, no read of L3 gets $x$. A process $j$ with $y_j = x$ either leaves the critical section in finite time, or, in a fair run, reads L3 again in finite time, since each round of the loop does. So all the values $y_j = x$ go away.

Then no term of $D$ is equal to $m$, so $D \le m - 1$. This proves Claim B.

By Claims A and B, from some time on $D = 0$, that is, $k = i$ and $y_j = i$ for every $j$ that has a value. But a process $j \ne i$ that enters after $\tau_1$ has $1 \le d(j) \le d(y_j) \le D = 0$, by Lemma 1. So no process other than $i$ enters from then on, and this contradicts the fact that other processes enter infinitely often. $\square$

Deadlock freedom also follows from Theorem 3.

**Not proved here: the bound on waiting.** Knuth showed that a waiting process can be passed only a bounded number of times; the bound usually quoted for his algorithm is $2^{n - 1} - 1$ entries of others after the doorway, and de Bruijn's change lowers it to $n(n - 1)/2$. We do not prove these bounds here. The test file checks by exhaustive search that the largest number of entries of others between the doorway of a process and its own entry is exactly $2^{n - 1} - 1$ for $n = 2$ (1 entry) and $n = 3$ (3 entries). $\blacksquare$
