---
title: The sloppy counter is linearizable for the relaxed counter and deadlock-free
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page, with $p$ stripes and threshold $S \ge 1$. Each lock gives mutual exclusion, and each read or write of one count is atomic. The relaxed counter type has state $N$; inc() adds 1, exact() returns $N$, and approximate() may return any $v$ with $N - p(S - 1) \le v \le N$. The counter starts with all local counts 0 and $C.global = N_0$.

**Lemma 1 (who writes what).** Only a thread that holds $C.lock[i]$ writes $C.local[i]$ (lines L2 and L7), and only a thread that holds $C.glock$ writes $C.global$ (line L5). A call that reads $C.local[i]$ holds $C.lock[i]$ (lines L3, L5 and L15).

*Proof.* These are all the accesses of the code to these fields, and each lies between the acquire and the release of the named lock. $\square$

**Linearization points.** An increment on stripe $i$ is *moving* if the value of $C.local[i]$ after its line L2 is at least $S$. By Lemma 1, no other thread changes $C.local[i]$ between lines L2 and L3 of this call, so the test of line L3 succeeds exactly for moving increments. The point of a non-moving increment is its line L2, the point of a moving increment is its line L5, the point of approximate() is line L10, and the point of exact() is line L15. Each point is a step of the call itself, so it lies between the invocation and the response. Let $N$ at each moment be $N_0$ plus the number of increments whose points have passed.

**Lemma 2 (pending amounts).** For each stripe $i$ define $c_i$ at each moment: if the holder of $C.lock[i]$ is a moving increment that has done line L2 but not line L5, then $c_i = C.local[i] - 1$; if it has done line L5 but not line L7, then $c_i = 0$; otherwise $c_i = C.local[i]$. Then at each moment
$$N = C.global + \sum_{i} c_i \quad\text{and}\quad 0 \le c_i \le S - 1 \text{ for each } i.$$

*Proof.* By induction on the steps. At the start $N = N_0 = C.global$, all $c_i = 0$, and $S - 1 \ge 0$. By Lemma 1 only lines L2, L5 and L7 change a count, and only steps of the holder of $C.lock[i]$ change $c_i$. Consider a call on stripe $i$.

- *Line L2 of a non-moving increment.* $c_i = C.local[i]$ before and after, so $c_i$ and $N$ both grow by 1, and $C.global$ does not change. The new $C.local[i]$ is below $S$ because the increment is not moving, so $c_i \le S - 1$.
- *Line L2 of a moving increment.* Before the step, no call on stripe $i$ is inside lines L2 to L7, so $c_i = C.local[i] \le S - 1$. The new value is at least $S$, so the old value was exactly $S - 1$. After the step, $C.local[i] = S$ and $c_i = S - 1$, the same as before. $N$ does not change, because the point is later. So the equation still holds.
- *Line L5 of a moving increment.* $C.global$ grows by $C.local[i] = S$, $c_i$ goes from $S - 1$ to 0, and $N$ grows by 1, because this is the point. The sum $C.global + \sum c_j$ grows by $S - (S - 1) = 1$, the same as $N$.
- *Line L7.* $C.local[i]$ becomes 0, and $c_i$ is 0 before and after.

No other step changes $C.global$, a count, $c_i$ or $N$, and the bounds $0 \le c_i \le S - 1$ hold after each case. $\square$

**Lemma 3 (results).** (a) The value $v$ that approximate() reads at line L10 satisfies $N - p(S - 1) \le v \le N$ at that moment. (b) The value that exact() computes at line L15 is $N$ at that moment.

*Proof.* (a) $v = C.global = N - \sum_i c_i$ by Lemma 2, and $0 \le \sum_i c_i \le p(S - 1)$. (b) An exact read holds every local lock and the global lock at line L15. So no increment is between lines L1 and L8 on any stripe, and every $c_i = C.local[i]$. Lemma 2 gives $C.global + \sum_i C.local[i] = N$. The sum at line L15 is computed while all locks are held, so no count changes during it. $\square$

**Theorem (linearizability).** Each history of the sloppy counter is linearizable with respect to the relaxed counter type.

*Proof.* Take an execution and its history $H$. Complete $H$ by keeping each pending call that has passed its point, with the result of Lemma 3 for a read that has passed line L10 or L15, and removing the other pending calls; a removed call has not changed $N$. Order the kept calls by their points, which are distinct steps. Apply them in this order to the relaxed counter from $N_0$. Each increment adds 1 at its point, which is how $N$ is defined, and each read returns a result allowed in the state $N$ at its point, by Lemma 3. So the sequential history is legal, and each call has the same result as in $H$. If call $a$ returns before call $b$ starts, the point of $a$ is before the point of $b$, so the order keeps the real-time order of $H$. $\square$

**Theorem (deadlock-freedom).** If the locks are deadlock-free, then whenever some call is pending and the threads keep taking steps, some call returns. With starvation-free locks, each call returns.

*Proof.* Number the locks: $C.lock[i]$ gets number $i$ and $C.glock$ gets number $p$. Each call takes its locks in increasing number: an increment takes $i$ and then perhaps $p$; an exact read takes $0, 1, \ldots, p - 1$ and then $p$; an approximate read takes only $p$. Suppose that from some moment on no call returns. A thread that holds no lock and waits for one waits for a thread that holds it. Let $m$ be the largest number of a held lock. Its holder waits, if at all, only for a lock with a number above $m$, which no thread holds, so with a deadlock-free lock it gets that lock. All code between acquires is a bounded number of steps, so this thread finishes its call. This contradicts the assumption. With starvation-free locks, each waiting thread gets its lock after finitely many other critical sections, each of bounded length, so each call returns. $\blacksquare$
