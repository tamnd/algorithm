---
title: The TTAS lock with backoff gives mutual exclusion and deadlock freedom, and spin then block is 2-competitive
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes. The memory is sequentially consistent, so every run is one sequence of atomic steps. The lock word $L$ is a test-and-set bit, false at the start. $\mathrm{TAS}(L)$ sets $L$ to true and returns the old value in one step. We use the lines L1 to L7 of the page. A critical section is finite: a process in it leaves after a finite number of its own steps. A run is fair if every process that is not in its remainder section takes infinitely many steps.

Call a process a *holder* from its TAS at L4 that returns false until its write at L7. A process leaves its entry section only through such a TAS, so every process in its critical section is a holder.

**Lemma 1 (invariant).** At every time, $L$ is true if and only if there is a holder, and there is at most one holder.

*Proof.* By induction on the steps of the run. At the start $L$ is false and there is no holder. Only L4 and L7 change $L$ or the set of holders. A TAS at L4 that returns false happens only when $L$ is false, so by induction there is no holder; after it, $L$ is true and its caller is the only holder. A TAS that returns true leaves $L$ true and the holders unchanged. A write at L7 is made by a holder, which is the only holder by induction; after it, $L$ is false and there is no holder. Reads, backoff steps and the other lines change neither. $\square$

**Lemma 2 (mutual exclusion).** At any time at most one process is in its critical section.

*Proof.* Every process in its critical section is a holder, and by Lemma 1 there is at most one holder. $\square$

**Lemma 3 (deadlock freedom).** In a fair run, if some process is in its entry section at time $t$, then some process enters its critical section after $t$.

*Proof.* Assume that no process enters after $t$. Then no process becomes a holder after $t$. A holder at time $t$, if there is one, leaves its critical section after a finite number of its steps and runs L7. So from some time $t_1 \ge t$ on there is no holder, and by Lemma 1 $L$ is false from $t_1$ on. Take a process $p$ that is in its entry section after $t_1$. Each backoff of L5 is finite, since $delay \le MAX$. The loop of L3 ends at the first read after $t_1$, because $L$ is false. So $p$ reaches L4, and its TAS returns false, since $L$ is false. Then $p$ enters, which contradicts the assumption. $\square$

**Lemma 4 (no starvation freedom).** There is a fair run with two processes in which process 0 stays in its entry section forever.

*Proof.* Let $MIN = MAX = 1$, so that the coin of L5 is always 0 and the backoff is empty. Let process 1 win the first TAS. Then repeat this cycle forever: process 0 runs L3 (it reads true and stays in the loop) or, if it is at L4, runs a TAS that returns true; then process 1 runs L7, starts a new entry section, reads false at L3 and wins its TAS at L4. In every cycle $L$ is true when process 0 takes its step. Both processes take infinitely many steps, so the run is fair, and process 0 never enters. The test file finds this cycle in the state graph for two processes that run forever. $\square$

**Lemma 5 (remote references).** In the CC model, while $L$ does not change, a waiter in the loop of L3 makes at most one remote reference. A passage has no bound on its remote references, in the CC or the DSM model.

*Proof.* In the CC model a read misses only if the line of $L$ was written by another process since the last access of the reader. While $L$ does not change, the first read of L3 brings the line into the cache, and the later reads hit. For the second claim, take the run of Lemma 4. Process 1 writes $L$ in every cycle, so the next access of process 0 misses, and process 0 makes at least one remote reference in each cycle while it stays in one passage. In the DSM model $L$ lives in one memory module, and the process that does not own that module makes a remote reference at each read of L3. $\square$

**Lemma 6 (spin then block).** Let the lock become free $w \ge 0$ time units after a waiter arrives, let spinning cost 1 per unit of time, and let blocking cost $C > 0$. The rule "spin for up to $C$ units, then block" costs $A(w) = w$ if $w \le C$ and $A(w) = 2C$ otherwise. The optimal offline cost is $\mathrm{OPT}(w) = \min(w, C)$. Then $A(w) \le 2\,\mathrm{OPT}(w)$ for every $w$, and for every deterministic threshold there is a $w$ at which the ratio is at least 2.

*Proof.* A waiter either blocks at some time $s \le w$ and pays $s + C \ge C$, or spins until $w$ and pays $w$. So no strategy pays less than $\min(w, C)$, and the waiter that knows $w$ pays exactly that. If $w \le C$, then $A(w) = w = \mathrm{OPT}(w)$. If $w > C$, then $A(w) = C + C = 2C = 2\,\mathrm{OPT}(w)$. So the ratio is at most 2, and it equals 2 for every $w > C$.

For the lower bound, let a deterministic rule block after spinning $x$ units, with $0 \le x < \infty$. The adversary frees the lock just after the block, at $w = x + \epsilon$ with $\epsilon > 0$ small. The rule pays $x + C$. If $x < C$, take $\epsilon \le C - x$; then $\mathrm{OPT}(w) = x + \epsilon$, and $(x + C)/(x + \epsilon)$ tends to $(x + C)/x \ge 2$ as $\epsilon \to 0$ (for $x = 0$ the ratio is $C/\epsilon$, which is unbounded). If $x \ge C$, then $\mathrm{OPT}(w) = C$ and $(x + C)/C \ge 2$. A rule that never blocks pays $w$ against $C$, and $w/C$ is unbounded. So no deterministic rule has a ratio below 2. The test file checks the upper bound on a grid of values of $w$ and $C$, with the worst ratio exactly 2, and the lower bound for a grid of thresholds. $\square$

Lemmas 2 and 3 show that TTAS-BO solves the mutual exclusion problem with deadlock freedom. Lemma 4 shows that it is not starvation free. Lemma 5 gives the remote reference costs on the page, and Lemma 6 gives the competitive ratio of spin then block. $\blacksquare$
