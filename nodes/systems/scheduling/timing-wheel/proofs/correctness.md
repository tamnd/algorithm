---
title: Every timer of a hashed or hierarchical timing wheel expires exactly at its expiry tick
proves: [correctness, termination]
status: full
---

Time is an integer $\mathit{now} \ge 0$. A running timer has an expiry $e = \mathit{now}_0 + j$, where $\mathit{now}_0$ is the time of its START-TIMER and $j \ge 1$. We must show that each running timer is reported by PER-TICK-BOOKKEEPING exactly at the tick at which $\mathit{now}$ becomes $e$, and at no other tick, and that a stopped timer is never reported.

## Hashed wheel

**Invariant H.** Between operations, every running timer with expiry $e$ satisfies $e > \mathit{now}$, it is in bucket $e \bmod N$, and its count is $\mathit{rounds} = \lfloor (e - \mathit{now} - 1)/N \rfloor$.

*Proof.* By induction on the operations.

- START-TIMER (lines L1 to L3) puts the new timer in bucket $e \bmod N$ with the count $\lfloor (j - 1)/N \rfloor = \lfloor (e - \mathit{now} - 1)/N \rfloor$, and $e > \mathit{now}$ as $j \ge 1$. Other timers do not change.
- STOP-TIMER (line L4) only removes a timer.
- PER-TICK-BOOKKEEPING changes $\mathit{now}$ to $\mathit{now}' = \mathit{now} + 1$ and visits the bucket $\mathit{now}' \bmod N$. Take a running timer with expiry $e > \mathit{now}$, and let $q = e - \mathit{now} - 1 \ge 0$, so the new count must be $\lfloor (q - 1)/N \rfloor$ if the timer does not expire.
  - If $e \not\equiv \mathit{now}' \pmod N$, the timer is not in the visited bucket. Then $q \not\equiv 0 \pmod N$, so $\lfloor (q - 1)/N \rfloor = \lfloor q/N \rfloor$, and the old count is still right.
  - If $e \equiv \mathit{now}' \pmod N$, the timer is in the visited bucket, and $q$ is a multiple of $N$, say $q = cN$, with old count $c$. If $c = 0$, then $e = \mathit{now}'$, and line L7 removes the timer and reports it. If $c \ge 1$, then $e > \mathit{now}'$, and line L8 sets the count to $c - 1 = \lfloor (cN - 1)/N \rfloor$, which is right. $\square$

**Theorem 1.** In the hashed wheel, a timer is reported at the tick $\mathit{now}' = e$ and at no other tick. A stopped timer is never reported.

*Proof.* By Invariant H, at each tick the timer is either outside the visited bucket, or in it with count $c = (e - \mathit{now}' )/N$. Line L7 reports it only if $c = 0$, which means $e = \mathit{now}'$. Since $e > \mathit{now}$ before every tick and $\mathit{now}$ grows by 1 per tick, the tick $\mathit{now}' = e$ comes, and then the timer is in the visited bucket (as $e \equiv \mathit{now}'$) with count 0, so it is reported. STOP-TIMER removes the timer from its bucket, so later ticks do not see it. $\square$

The simple wheel is the case $N > j$ for every interval $j$; then every count is $\lfloor (j-1)/N \rfloor = 0$.

## Hierarchical wheel

Write $\mathrm{digit}_k(x) = \lfloor x / N^k \rfloor \bmod N$ and $\mathrm{high}(x) = \lfloor x / N^L \rfloor$. For $e \ne \mathit{now}$, let $\mathrm{top}(e)$ be the largest $k < L$ with $\mathrm{digit}_k(e) \ne \mathrm{digit}_k(\mathit{now})$, when $\mathrm{high}(e) = \mathrm{high}(\mathit{now})$.

**Invariant W.** Between operations, every running timer with expiry $e$ satisfies $e > \mathit{now}$, and it is in the overflow list if $\mathrm{high}(e) \ne \mathrm{high}(\mathit{now})$, and else in bucket $\mathrm{digit}_k(e)$ of wheel $k = \mathrm{top}(e)$.

*Proof.* START-TIMER places the timer by this rule, and STOP-TIMER only removes. Consider a tick from $\mathit{now}$ to $\mathit{now}' = \mathit{now} + 1$. Let $J$ be the largest $k \le L$ such that $N^k$ divides $\mathit{now}'$. Then the digits $0, \ldots, J - 1$ of $\mathit{now}$ are all $N - 1$ and become 0, the digit $J$ (or $\mathrm{high}$, if $J = L$) grows by 1, and the higher digits do not change.

- A timer on a wheel $k > J$ still has its highest differing digit at $k$, because the digits at and above $k$ of $\mathit{now}$ do not change. It stays right.
- A timer on a wheel $k < J$ cannot exist before the tick, if $J \ge 1$: such a timer agrees with $\mathit{now}$ above digit $k$ and has $e > \mathit{now}$, so $\mathrm{digit}_k(e) > \mathrm{digit}_k(\mathit{now}) = N - 1$, which is impossible. If $J = 0$, there is no wheel below $J$.
- A timer on wheel $J$ (or in the overflow list, if $J = L$) agreed with $\mathit{now}$ above $J$ and had a larger digit $J$. After the tick, its digit $J$ either still differs from that of $\mathit{now}'$, and it stays right, or it equals it, and then the timer is exactly in the bucket $\mathrm{digit}_J(\mathit{now}')$ of wheel $J$ (or in the overflow list with $\mathrm{high}(e) = \mathrm{high}(\mathit{now}')$).

The tick cascades the overflow list if $J = L$, and then the buckets $\mathrm{digit}_k(\mathit{now}')$ of the wheels $k = L - 1, \ldots, 1$ for which $N^k$ divides $\mathit{now}'$, which are the wheels $k \le J$, from the top down. Cascading re-places each timer by the rule, relative to $\mathit{now}'$. A timer that moves from wheel $J$ lands on a lower wheel in a bucket that is cascaded later in the same tick if its digit there equals that of $\mathit{now}'$, which is 0; so after the cascades, every timer with $e > \mathit{now}'$ is placed by the rule. A timer with $e = \mathit{now}'$ is placed in bucket $\mathrm{digit}_0(\mathit{now}')$ of wheel 0 (no digit differs), and the tick reports and removes all timers of that bucket. $\square$

**Theorem 2.** In the hierarchical wheel, a timer is reported exactly at the tick $\mathit{now}' = e$, and a stopped timer is never reported.

*Proof.* The tick reports the bucket $\mathrm{digit}_0(\mathit{now}')$ of wheel 0. By Invariant W (applied after the cascades), a timer in that bucket with $e > \mathit{now}'$ would differ from $\mathit{now}'$ only in digit 0, but have the same digit 0, which is impossible; so every reported timer has $e = \mathit{now}'$. Conversely, at the tick $\mathit{now}' = e$, the proof of Invariant W shows that the timer is in that bucket. $\square$

**Moves.** Each cascade puts a timer on a strictly lower wheel, or moves it from the overflow list to a wheel. If $j < N^L$, then $\mathrm{high}(e) \le \mathrm{high}(\mathit{now}_0) + 1$, so the timer leaves the overflow list at most once, and it moves at most $L$ times in total.

**Termination.** START-TIMER and STOP-TIMER do a constant amount of work, or $O(L)$ for the placement on the hierarchical wheel. A tick scans one bucket of wheel 0 and at most $L$ cascaded buckets, each a finite list, and it does not add entries to a bucket that it is scanning: re-placed timers go to lower wheels, and a timer started during expiry processing has $e > \mathit{now}'$. So every operation ends. $\blacksquare$
