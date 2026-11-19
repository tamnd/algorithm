---
title: What the endpoints of Rabiner and Sambur guarantee about energy and zero crossings
proves: [correctness]
status: full
---

The thresholds of the algorithm are heuristics, so no proof can show that the output is the word. We prove what the output means in terms of the frame measures $E$ and $Z$. We work in the real RAM with $T \ge 10$ frames, and we use the words of lines L1 to L8.

Call a frame *high* if $E[i] > ITU$ and *active* if $E[i] > ITL$. A *run* is a maximal block of consecutive active frames. A run is *strong* if it holds a high frame.

**Lemma 1 (the thresholds are ordered).** If $IMN > 0$, then $ITL \ge IMN > 0$ and $ITU = 5\,ITL > ITL$. If also $IMX > IMN$, then $ITL > IMN$.

*Proof.* Since $IMN$ is the mean of the first 10 energies and $IMX$ is the maximum of all of them, $IMX \ge IMN$. So $0.03(IMX - IMN) + IMN \ge IMN$, and $4\,IMN > IMN$. Their minimum is at least $IMN$, and strictly above it when $IMX > IMN$. Finally $5\,ITL > ITL$ because $ITL > 0$. $\square$

By Lemma 1, a high frame is active when $IMN > 0$, so every high frame lies in a strong run. If $IMN = 0$ (digital silence), then $ITL = ITU = 0$, a frame is active exactly when it is high, and everything below still holds.

**Lemma 2 (line L4 finds the start of the first strong run).** The forward scan of line L4 returns the first frame of the first strong run, and returns nothing if there is no strong run. Line L5 returns the last frame of the last strong run.

*Proof.* The scan keeps a candidate $c$. At a frame that is not active it clears $c$. At an active frame with no candidate it sets $c$ to that frame, so $c$ is always the first frame of the run that contains the current frame. At a high frame it returns $c$. So the scan returns at the first high frame it meets, with the first frame of its run, and that run is the first strong run, because any earlier strong run would hold an earlier high frame. If there is no high frame, it returns nothing. The backward scan is the same on the reversed sequence, where the first frame of a run is its last frame in time. $\square$

**Theorem 1 (the interval holds every loud frame).** If line L4 returns $N_1$, then line L5 returns some $N_2 \ge N_1$, every high frame $i$ satisfies $N_1 \le i \le N_2$, and lines L6 and L7 only lower $N_1$ and raise $N_2$.

*Proof.* If L4 returns, a strong run exists, so L5 returns too. By Lemma 2, $N_1$ is the start of the first strong run and $N_2$ the end of the last one, so $N_1 \le N_2$, and every high frame lies in some strong run, between the start of the first and the end of the last. Line L6 replaces $N_1$ only by a frame among the 25 before it, and line L7 replaces $N_2$ only by a frame among the 25 after it. $\square$

**Theorem 2 (the ends are word-like).** After line L5, $E[N_1] > ITL$ and $E[N_2] > ITL$, and the frames from $N_1$ to the first high frame, and from the last high frame to $N_2$, are all active. If line L6 changes $N_1$, then $Z[N_1] > IZCT$, $N_1$ was at most 25 frames before the old value, and at least 3 frames in that span have $Z > IZCT$; the same holds for line L7 and $N_2$.

*Proof.* The first part is Lemma 2: $N_1$ and $N_2$ are ends of strong runs, so they are active, and the frames of a run are active. Line L6 moves $N_1$ only when at least 3 of the 25 frames before it have $Z > IZCT$, and then to the earliest of those frames, which has $Z > IZCT$. Line L7 is symmetric. $\square$

**Theorem 3 (gain does not matter).** Let $s'[n] = c\, s[n]$ with $c > 0$. Then the algorithm returns the same result for $s'$ as for $s$.

*Proof.* Each $E'[i] = c\,E[i]$, and the sign of $c\,s[n]$ is the sign of $s[n]$ (with $0$ counted as positive in both), so $Z' = Z$ and $IZCT' = IZCT$. Then $IMN' = c\,IMN$ and $IMX' = c\,IMX$, and since $c > 0$ factors out of the minimum, $ITL' = c\,ITL$ and $ITU' = c\,ITU$. Every comparison $E'[i] > ITL'$ or $E'[i] > ITU'$ has the same answer as for $s$, so lines L4 to L7 make the same choices. $\square$

The tests check the frame measures and the thresholds by hand, Lemma 2 against a direct search over all frames, the rules of lines L6 and L7 with exactly 2 and 3 hits and with $Z$ equal to IZCT, and the full detector on a synthetic word with and without weak fricatives.
