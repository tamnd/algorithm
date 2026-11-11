---
title: The bakery algorithm gives mutual exclusion, FCFS order and starvation freedom, with safe registers
proves: [correctness]
status: full
---

We follow Lamport's proof (1974) and use the pseudocode of the page, with processes $0, \ldots, n-1$. Pairs are compared in lexicographic order: $(a, b) < (c, d)$ if $a < c$, or $a = c$ and $b < d$.

**Memory model.** Each register has one writer: only process $i$ writes $choosing[i]$ and $number[i]$. A read or a write takes an interval of time, and the writes of one process do not overlap. The registers are *safe*: a read that overlaps no write of the register returns the value of the last write before it, and a read that overlaps a write may return any value of the register's type. Atomic registers are a special case. A process stays in the critical section for a finite time, and a process that is not in its remainder section takes another step eventually.

**Terms.** The *doorway* of process $k$ is L1 to L4. Process $k$ is *in the bakery* from the end of its write of L4 until the end of its write of L8. While $k$ is in the bakery, its *ticket* $N_k \ge 1$ is the value that it wrote at L3 in its last doorway, and $number[k] = N_k$ with no write of $number[k]$ in progress. The critical section is inside the bakery.

**Lemma 1.** Suppose that process $i$ is in the bakery during the whole of the read of $number[i]$ that process $k$ makes at L2 in some doorway. Then the ticket that $k$ chooses in that doorway is larger than $N_i$.

*Proof.* The read overlaps no write of $number[i]$, because $i$ writes $number[i]$ only at L3 and L8, and it is in the bakery the whole time, after its L3 and before its L8. So the read returns $N_i$, and $k$ chooses at least $N_i + 1$. $\square$

**Lemma 2.** If process $i$ is in the critical section and process $k \ne i$ is in the bakery, then $(N_i, i) < (N_k, k)$.

*Proof.* Look at the last doorway of $k$. In it, $k$ writes $choosing[k] \leftarrow true$ at L1 (a write that ends at time $e_1$), reads at L2, writes $number[k] \leftarrow N_k$ at L3, and writes $choosing[k] \leftarrow false$ at L4 (a write that starts at time $s_4$). From $e_1$ to $s_4$, $choosing[k] = true$ and no write of it is in progress. Now look at the entry section of $i$ that led to the critical section. For $j = k$ it made a last read of $choosing[k]$ at L6, during $[a, b]$, that returned false, and after that a last read of $number[k]$ at L7, during $[c, d]$ with $c > b$, that let it go on. A read inside $(e_1, s_4)$ would return true, so $a < e_1$ or $b > s_4$.

- *Case $a < e_1$.* Process $i$ has been in the bakery since before $a$, because L6 comes after L4, and it is still in the bakery now. The reads of $k$ at L2 begin after $e_1 > a$, and end before now. So $i$ is in the bakery during the whole read of $number[i]$ by $k$, and Lemma 1 gives $N_k > N_i$.
- *Case $b > s_4$.* The write of L3 by $k$ ended before $s_4 < b < c$. After it, $k$ writes $number[k]$ again only at L8, and $k$ is still in the bakery now, after $d$. So the read $[c, d]$ overlaps no write and returns $N_k \ge 1$. Since $i$ went on, $number[k] = 0$ is false, so $(N_k, k) > (N_i, i)$.

In both cases $(N_i, i) < (N_k, k)$, since $N_k > N_i$ implies it. $\square$

**Theorem 1 (mutual exclusion).** At most one process is in the critical section at any time.

*Proof.* If $i \ne k$ are both in the critical section, both are in the bakery, and Lemma 2 gives $(N_i, i) < (N_k, k)$ and $(N_k, k) < (N_i, i)$. $\square$

**Theorem 2 (first come, first served).** If process $i$ finishes its doorway before process $k$ starts its doorway, then $k$ does not enter the critical section before $i$ does.

*Proof.* Assume that $k$ enters at a time $t$ while $i$ is still waiting. Then $i$ has been in the bakery from before the start of the doorway of $k$ until $t$, so by Lemma 1, $N_k > N_i$. By Lemma 2, with $k$ in the critical section and $i$ in the bakery, $(N_k, k) < (N_i, i)$, so $N_k \le N_i$. This is a contradiction. $\square$

**Corollary (bypass).** While process $i$ is in the bakery and waits, each other process enters the critical section at most once. So at most $n - 1$ entries of other processes come between the end of the doorway of $i$ and its entry.

*Proof.* After its first such entry, a process $k$ leaves and starts a new doorway after $i$ finished its doorway, and by Theorem 2 it cannot enter again before $i$. $\square$

**Theorem 3 (deadlock freedom).** If some process is in its entry section, then some process enters the critical section later.

*Proof.* Assume that from some time on, no process enters, while some process is in its entry section. The doorway has no waiting, and the critical section and the exit section are finite. So from some time $T$ on, each process is either in its remainder section forever, or in the bakery forever, waiting in L5 to L7 with a fixed ticket, $choosing$ false, and no write in progress. At least one process waits. Let $i$ be the waiting process with the smallest pair $(N_i, i)$. After $T$, its reads overlap no write. For each $j \ne i$, it reads $choosing[j] = false$ at L6, and at L7 it reads $number[j] = 0$ (if $j$ is in its remainder section) or $N_j$ with $(N_j, j) > (N_i, i)$. So $i$ passes every $j$ and enters. This is a contradiction. $\square$

**Theorem 4 (starvation freedom).** Each process that starts its entry section enters the critical section.

*Proof.* Process $i$ finishes its doorway, since it has no waiting. If $i$ then waited forever, the other processes would enter at most $n - 1$ times in all, by the corollary. After the last of these entries, no process enters, but $i$ is in its entry section, which contradicts Theorem 3. $\square$

**Why the safe registers do no harm.** The proofs never use the value of a read that overlaps a write. A read of $number[j]$ at L2 that overlaps a write can make the ticket of $k$ too large, which is harmless. A read of $choosing[j]$ at L6 that overlaps a write can return false too early; the case analysis of Lemma 2 covers it, because such a read starts before $e_1$ or ends after $s_4$. A read of $number[j]$ at L7 that overlaps a write is not the last read before an entry in the cases that the proofs need, because the last read of Lemma 2 overlaps no write. $\blacksquare$
