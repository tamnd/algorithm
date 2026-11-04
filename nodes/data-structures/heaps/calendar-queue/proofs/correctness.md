---
title: The calendar queue returns an event of smallest time
proves: [correctness, termination]
status: full
---

Let $\mathrm{vb}(t) = \lfloor t/w \rfloor$ for the current width $w$. Since $t \mapsto t/w$ is non-decreasing for $w > 0$, and so is the floor, $\mathrm{vb}$ is non-decreasing: $t \le t'$ implies $\mathrm{vb}(t) \le \mathrm{vb}(t')$, and so $\mathrm{vb}(t) < \mathrm{vb}(t')$ implies $t < t'$. Events are compared by the pair (time, arrival number), and $\mathrm{vb}$ depends on the time only.

**Invariants.** Between operations, with $n$ events in the queue:

> **(B)** each event with time $t$ is in the bucket $B[\mathrm{vb}(t) \bmod N]$, exactly once, and each bucket is sorted by (time, arrival);
>
> **(V)** if $n \ge 1$, then $\mathrm{vb}(t) \ge V$ for each event in the queue.

Both hold for the empty queue.

**Lemma 1.** Let (B) and (V) hold with $n \ge 1$. If $B[V \bmod N]$ is not empty and its first event $x$ has $\mathrm{vb}(x) = V$, then $x$ is a smallest event of the queue. Else no event has the virtual bucket $V$, and (V) holds with $V + 1$.

*Proof.* Let $y$ be any event. If $\mathrm{vb}(y) > V = \mathrm{vb}(x)$, then $y$ has a larger time than $x$. Else $\mathrm{vb}(y) = V$ by (V), so $y$ is in the same bucket $B[V \bmod N]$ by (B), and $x$ comes first in that sorted bucket, so $x \le y$. For the second part: if some event $y$ had $\mathrm{vb}(y) = V$, the bucket would not be empty, and its first event $x$ would satisfy $V \le \mathrm{vb}(x) \le \mathrm{vb}(y) = V$, since $x \le y$ in the bucket and $\mathrm{vb}$ is non-decreasing. So all events have $\mathrm{vb} \ge V + 1$. $\square$

**INSERT.** Line L2 puts the event into the bucket of (B) at its sorted place, so (B) holds. If the queue was empty, line L3 sets $V = \mathrm{vb}(t)$ and (V) holds for the one event. Else (V) held for the old events, and line L3 lowers $V$ if needed, so it holds for the new one too, and lowering $V$ keeps it for the old ones.

**EXTRACT-MIN.** Let $n \ge 1$. By Lemma 1, each iteration of the loop of lines L6 to L10 either finds a smallest event, removes it, and returns it, or moves $V$ up by one and keeps (V). The loop runs at most $N$ times. If it finds no event, line L11 compares the first events of all buckets; by (B), the first event of each bucket is its smallest, so the result is a smallest event of the queue. Line L12 sets $V = \mathrm{vb}(t)$ for this smallest $t$; every event has a time at least $t$, so $\mathrm{vb} \ge V$, and (V) holds. Removing the first event of a bucket keeps (B), and removing any event keeps (V).

**RESIZE.** It takes all events out, picks a new width $w' > 0$ and a new $N'$, puts each event into $B[\mathrm{vb}'(t) \bmod N']$ and sorts each bucket, so (B) holds for the new $\mathrm{vb}'$. It sets $V$ to the least $\mathrm{vb}'(t)$, so (V) holds. Lemma 1 holds for any width, so the next operations are correct.

**Theorem.** Each operation stops, after at most $N$ iterations of the scan plus one direct search and one resize. Each EXTRACT-MIN on a non-empty queue returns a smallest event, and events with equal times leave in the order of arrival.

*Proof.* Termination is the bound on the loop. The answer is a smallest pair (time, arrival) by Lemma 1 and the analysis of the direct search, which gives the second claim. $\blacksquare$
