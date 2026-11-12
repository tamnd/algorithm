---
title: EASY backfilling never delays the head past its shadow time, and conservative backfilling never delays any job past its first reservation
proves: [correctness, termination]
status: full
---

The machine has $P$ processors. Job $j$ has size $p_j \le P$, estimate $e_j$ and real run time $r_j$, and it holds its processors during $[s_j, s_j + \min(r_j, e_j))$. So a job that starts at $s_j$ releases its processors at or before its *estimated end* $s_j + e_j$. The scheduler runs at every arrival and every real end.

For a set $X$ of running jobs and a time $\tau \ge t$, let $F_X(\tau) = P - \sum \{ p_k : k \in X,\ s_k + e_k > \tau \}$ be the number of processors that are free at $\tau$ by the estimates. It does not fall as $\tau$ grows.

**Lemma 1 (capacity).** At every time, the running jobs hold at most $P$ processors.

*Proof.* Lines L1 and L8 (and the start rule of each policy) start a job only if its size is at most the number of idle processors at that moment. Processors are released only by real ends. $\square$

## EASY

**Lemma 2 (one pass).** Let a pass at time $t$ find the head $h$ blocked, with the running set $X$ and the shadow time $S$ of line L5. Let $X'$ be the running set at the end of the pass. Then $F_{X'}(S) \ge p_h$.

*Proof.* By line L5, $S$ is the first estimated end at which $\mathit{free} + \sum\{p_k : k \in X, s_k + e_k \le S\} \ge p_h$, which is $F_X(S) \ge p_h$; and line L6 sets $\mathit{extra} = F_X(S) - p_h \ge 0$. A job $j$ that line L9 starts with $t + e_j \le S$ does not count in $F(S)$. A job with $t + e_j > S$ counts in $F(S)$ with size $p_j \le \mathit{extra}$, and line L9 lowers $\mathit{extra}$ by $p_j$. So $\mathit{extra} = F_{X'}(S) - p_h$ stays at least 0 during the pass. $\square$

**Lemma 3 (the shadow never moves later).** Let $h$ be the head at two passes, at times $t < t'$, with no start of $h$ between them, and with shadow times $S$ and $S'$. Then $S' \le S$.

*Proof.* Between the end of the pass at $t$ and the pass at $t'$, jobs only end: a job starts only in a pass. Removing jobs from $X$ does not lower $F_X(\tau)$ for any $\tau$. So by Lemma 2, $F_{X}(S) \ge p_h$ for the running set $X$ at the start of the pass at $t'$. If $S \ge t'$, then line L5 at $t'$ finds an estimated end $S' \le S$ with $F \ge p_h$, because $F_X$ only changes at estimated ends of jobs in $X$. If $S < t'$, then every job of $X$ with estimated end at most $S$ has ended, so $F_X(t') \ge F_X(S) \ge p_h$, and $h$ fits at $t'$ and starts at line L1, against the assumption. $\square$

**Theorem 1 (EASY protects the head).** Let $h$ become the head at time $t_0$ and not fit, and let $S_0$ be its shadow time then. Then $s_h \le S_0$.

*Proof.* By Lemma 3, every later pass while $h$ is the head computes a shadow time of at most $S_0$, and by Lemma 2 the jobs that run after each pass leave $F(S_0) \ge p_h$. Each job $k$ that is running and has estimated end at most $S_0$ ends at a real time at most $S_0$, and each real end is a pass. At the last of these ends, or at $t_0$ if there is none, the jobs still running are the ones with estimated end after $S_0$, so at least $p_h$ processors are idle, and line L1 starts $h$. That time is at most $S_0$. $\square$

## Conservative

Here a *reservation* is a pair (start time, the interval $[s, s + e_j)$ of $p_j$ processors). The schedule at time $t$ is the set of running jobs (held up to their estimated ends) and the reservations of the queued jobs. Call it *feasible* if at every future time the total size of the running jobs and reserved jobs that overlap that time is at most $P$.

**Lemma 4 (feasibility).** After every event, the schedule is feasible, and every queued job has a reservation at or after the current time.

*Proof.* A new job gets the earliest start at which it fits beside all running jobs and reservations, so feasibility holds; such a start exists because after the last estimated end everything is free. A real end only removes load, so it keeps feasibility. In a compression, each job is removed and put back at its earliest fit beside all others, which keeps feasibility. A job starts only when its reservation equals the current time, and its interval is then the same interval as its reservation, so feasibility holds after it starts as well. $\square$

**Lemma 5 (compression never moves a job later).** In a compression, process the queued jobs in order of their old reservation times $\sigma_1 \le \sigma_2 \le \cdots$. Then each job gets a new reservation at most its old one.

*Proof.* By induction on the order. When job $j$ is processed, the jobs before it in the order had $\sigma_k \le \sigma_j$ and have moved to $\sigma'_k \le \sigma_k$. The part of $[\sigma'_k, \sigma'_k + e_k)$ that lies at or after $\sigma_j$ is $[\sigma_j, \sigma'_k + e_k)$, which is inside the old part $[\sigma_j, \sigma_k + e_k)$. So at every time at or after $\sigma_j$, the moved jobs use no more processors than before. Running jobs only ended, and jobs after $j$ in the order have not moved. So the old interval $[\sigma_j, \sigma_j + e_j)$ still fits, and the earliest fit is at most $\sigma_j$. $\square$

**Theorem 2 (conservative protects every job).** Each job starts no later than the reservation it gets at its arrival.

*Proof.* The reservation of a job changes only in a compression, and by Lemma 5 it never moves later. By Lemma 4 it is never before the current time. A reservation equals an estimated end or the time of an event. If it is the estimated end of a job that ends early, that end is an event, and a compression recomputes the reservation then. Otherwise the scheduler runs at that time, and step 3 starts the job. So the job starts exactly at its final reservation, which is at most its first one. $\square$

**Termination.** Every job starts in finite time: under conservative backfilling at its finite reservation (Theorem 2), and under EASY because each job becomes the head after the finitely many jobs that arrived before it have started, and then starts by its shadow time (Theorem 1). Each started job ends within its estimate. There are at most $2n$ events, so the simulation ends. $\blacksquare$
