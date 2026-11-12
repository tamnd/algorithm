---
title: CFS keeps every virtual runtime within one virtual slice of the minimum, so each task stays within one slice of its weighted share
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. First fix a set $R$ of $n$ CPU-bound tasks that are all runnable from time 0 with virtual runtime 0 and do not finish in the interval we study. Let $W = \sum_{k \in R} w_k$, $P = \max(\mathit{latency}, n \cdot \mathit{min\_gran})$, and $\mathit{slice}_k = P w_k / W$. Let $\mathit{cpu}_k$ be the real CPU time of task $k$ so far, and $m = \min_k \mathit{vr}_k$.

**Lemma 1 (equal virtual steps).** Each pass of lines L5 to L11 adds $V = P \cdot 1024 / W$ to the virtual runtime of the task $j$ that runs, and $\mathit{vr}_k = \mathit{cpu}_k \cdot 1024 / w_k$ for every $k$.

*Proof.* No task finishes, so $n$ and $W$ at lines L6 and L7 are those of $R$, and $\delta = \mathit{slice}_j = P w_j / W$ at line L8. Line L9 adds $\delta \cdot 1024 / w_j = P \cdot 1024 / W = V$. Since $\mathit{vr}_k$ starts at 0 and line L9 is the only change while no task wakes, $\mathit{vr}_k = \mathit{cpu}_k \cdot 1024 / w_k$. $\square$

**Lemma 2 (the virtual runtime invariant).** At the end of each pass, $m \le \mathit{vr}_k \le m + V$ for every $k \in R$.

*Proof.* At time 0 all virtual runtimes are 0, which is $m$. Assume the claim before a pass. Line L5 takes the task $j$ with the smallest key, so $\mathit{vr}_j = m$. By Lemma 1 it ends with $\mathit{vr}_j = m + V$. The new minimum $m'$ is at least $m$, since only $\mathit{vr}_j$ changed, and it went up. So $\mathit{vr}_j = m + V \le m' + V$, and for $k \ne j$, $\mathit{vr}_k \le m + V \le m' + V$. $\square$

This is the same argument as the pass invariant of stride scheduling, with every stride replaced by the real time scaled by $1024 / w$.

**Theorem 1 (lag bound).** At the end of each pass, with elapsed time $t$, every task $k \in R$ has $|\mathit{cpu}_k - t\, w_k / W| \le \mathit{slice}_k$.

*Proof.* The CPU is never idle, so $t = \sum_i \mathit{cpu}_i = \sum_i \mathit{vr}_i\, w_i / 1024$ by Lemma 1. By Lemma 2, $m W / 1024 \le t \le (m + V) W / 1024$, and $m w_k / 1024 \le \mathit{cpu}_k \le (m + V) w_k / 1024$. So

$$\mathit{cpu}_k - t \frac{w_k}{W} \le \frac{(m + V) w_k}{1024} - \frac{m w_k}{1024} = \frac{V w_k}{1024} = \mathit{slice}_k,$$

and in the same way $\mathit{cpu}_k - t\, w_k / W \ge -V w_k / 1024 = -\mathit{slice}_k$. $\square$

**Corollary (exact periods).** Whenever all virtual runtimes are equal, Lemma 1 gives $\mathit{cpu}_k / \mathit{cpu}_i = w_k / w_i$ for all $i$ and $k$, so the CPU times are exactly in the ratio of the weights. In the example with weights 1024 and 2048, this happens at the end of each period of 48 ms, and B has had exactly twice the CPU of A.

**Lemma 3 (placement).** Now let tasks arrive, sleep and wake. At all times every task in $Q$, and the task that runs, has $\mathit{vr} \ge \mathit{min\_vr}$, and $\mathit{min\_vr}$ never falls.

*Proof.* Line L10 sets $\mathit{min\_vr}$ to the maximum of its old value and another value, so it never falls. Line L3 sets the virtual runtime of a task that enters to at least $\mathit{min\_vr}$. Line L9 only raises virtual runtimes. At line L10, the new value is either the old $\mathit{min\_vr}$, which is at most every runnable virtual runtime by induction, or the smallest runnable virtual runtime, which by definition is at most each of them. $\square$

So a task that wakes after a long sleep enters at the smallest virtual runtime of the runnable tasks (or above it), and it does not keep the CPU to make up for the time it slept.

**Termination.** Let all bursts and sleeps be positive. Each pass of lines L5 to L11 either ends a burst or runs a full slice of length at least $\mathit{latency} \cdot w_{\min} / W_{\max} > 0$, where $w_{\min}$ is the smallest weight and $W_{\max}$ the sum of all weights. So each burst ends after finitely many passes. A pass of line L4 moves $t$ to the next arrival or wake, which is one of finitely many events. Each task has finitely many bursts, so the loop of line L2 ends. $\blacksquare$
