---
title: Fiduccia-Mattheyses keeps the balance, maintains exact gains with the critical net rules, lowers the cut in every applied pass, and runs a pass in linear time
proves: [correctness, termination, local optimality, gain update, running time]
status: full
---

Let $H$ have vertices $V = \{0, \ldots, n-1\}$ and a list of nets, each a non-empty set of vertices. Let $P = \sum_e |e|$ be the number of pins and $p_{\max}$ the largest number of nets at one vertex. A partition is a map $\mathrm{side} : V \to \{0, 1\}$, and its cut is the number of nets with pins on both sides. For a net $e$ and a side $s$, let $N_s(e)$ be the number of pins of $e$ on side $s$. For a vertex $v$ on side $s$, let
$$ \mathrm{FS}(v) = |\{e \ni v : N_s(e) = 1\}|, \qquad \mathrm{TE}(v) = |\{e \ni v : N_{1-s}(e) = 0\}|, \qquad g(v) = \mathrm{FS}(v) - \mathrm{TE}(v). $$
A partition is *balanced* if the number of vertices on side 0 lies in $[lo, hi]$.

**Lemma 1 (gain).** Moving a single vertex $v$ to the other side lowers the cut by exactly $g(v)$.

*Proof.* Only nets that contain $v$ can change status. Let $v$ be on side $s$, $t = 1 - s$, and let $e \ni v$. There are four cases.

- $N_s(e) = 1$ and $N_t(e) \ge 1$: $e$ is cut before and not cut after. It adds 1 to $\mathrm{FS}(v)$ and 0 to $\mathrm{TE}(v)$, so 1 to $g(v)$.
- $N_s(e) \ge 2$ and $N_t(e) = 0$: $e$ is not cut before and cut after. It adds $-1$ to $g(v)$.
- $N_s(e) = 1$ and $N_t(e) = 0$, so $e = \{v\}$: never cut. It adds $1 - 1 = 0$.
- $N_s(e) \ge 2$ and $N_t(e) \ge 1$: cut before and after. It adds 0.

In each case the contribution of $e$ to $g(v)$ equals the decrease of the cut caused by $e$. $\square$

**Lemma 2 (critical net rules).** Let a vertex $v$ move from side $s$ to side $t = 1 - s$, and let $F = N_s(e)$ and $T = N_t(e)$ be the counts of a net $e \ni v$ before the move. For every other vertex $u \in e$, the contribution of $e$ to $g(u)$ changes by
$$ [T = 0] + [F = 2] \ \text{ if } u \text{ is on side } s, \qquad -[T = 1] - [F = 1] \ \text{ if } u \text{ is on side } t. $$
Line L6 applies exactly these changes to the free vertices.

*Proof.* The contribution of $e$ to $g(u)$, for $u$ on side $r$, is $[N_r(e) = 1] - [N_{1-r}(e) = 0]$. After the move the counts are $F - 1$ on side $s$ and $T + 1$ on side $t$.

If $u$ is on side $s$, then $F \ge 2$, since $u$ and $v$ are both on $s$. The contribution is $0 - [T = 0]$ before and $[F - 1 = 1] - 0$ after. The change is $[F = 2] + [T = 0]$.

If $u$ is on side $t$, then $T \ge 1$ and $F \ge 1$. The contribution is $[T = 1] - 0$ before and $0 - [F - 1 = 0]$ after. The change is $-[T = 1] - [F = 1]$.

Now compare with line L6. Before updating the counts it checks $T$. If $T = 0$, all other pins are on side $s$, and it adds 1 to every free one: this is the term $[T = 0]$. If $T = 1$, the single pin on side $t$ must lose 1, the term $-[T = 1]$. The code does this when no pin on side $t$ is locked; otherwise that single pin is locked, its gain is not used again in this pass, and nothing needs to be done. After updating the counts to $F' = F - 1$ and $T' = T + 1$, it checks $F'$. If $F' = 0$, all other pins are on side $t$, and it subtracts 1 from every free one: the term $-[F = 1]$. If $F' = 1$, the single remaining pin on side $s$ gains 1, the term $[F = 2]$, and again the code skips this only when that pin is locked. Every free $u$ receives the change of each net it shares with $v$, and nets without $v$ do not change, so all free gains stay exact. $\square$

**Lemma 3 (selection).** At each step of line L4, the moved vertex $v$ has the largest gain among the free vertices whose move keeps the partition balanced.

*Proof.* With unit vertex weights, a move from side $s$ keeps the balance if and only if the count of side 0 after the move lies in $[lo, hi]$, which depends only on $s$. Every free vertex $u$ is stored in bucket $g(u)$ of its side, and by Lemma 2 these gains are exact. The pointer $\mathrm{top}[s]$ is never below the highest non-empty bucket of side $s$: it is set at line L2 to the highest bucket, and each time a gain grows, the pointer is raised to the new bucket if needed. Line L4 lowers it past empty buckets, so it stops at the highest non-empty bucket. So line L4 compares the largest gain of each allowed side and takes the larger. $\square$

**Lemma 4 (one pass).** Let a pass start from a balanced partition with cut $C$ and record moves $v_1, \ldots, v_m$ with gains $g_1, \ldots, g_m$. The partition obtained by applying the moves $v_1, \ldots, v_k$ is the tentative partition after step $k$. It is balanced, and its cut is $C - G_k$ with $G_k = g_1 + \cdots + g_k$.

*Proof.* Each vertex is locked when it moves, so it moves at most once in a pass, and the tentative partition after $k$ steps is the start with $v_1, \ldots, v_k$ moved. Each step keeps the balance by the rule of line L3. By Lemma 2 the recorded $g_j$ is the exact gain in the tentative partition before step $j$, and by Lemma 1 the cut drops by $g_j$. Induction on $k$ gives the claim. $\square$

**Lemma 5 (time per pass).** One pass takes $O(n + P)$ time.

*Proof.* Line L2 computes the counts, the gains and the buckets in $O(n + P + p_{\max})$ time, and $p_{\max} \le P$. Each step of the inner loop does $O(1)$ work outside the scans of line L6 and the pointer moves of line L4. Each net $e$ starts a scan of its pins, in $O(|e|)$ time, in at most 8 steps per pass, as follows. Fix the direction $s \to t$ of the move.

- The scan for $T = 0$ leaves a locked pin on side $t$. Locked pins stay, so $N_t(e) \ge 1$ for the rest of the pass.
- The scan for $T = 1$ with no locked pin on side $t$ also leaves a locked pin on side $t$, so its condition is false for the rest of the pass.
- The scan for $F' = 0$ leaves $N_s(e) = 0$. After that, no pin can move from $s$ to $t$ until a pin moves into $s$, and that pin is locked on $s$, so $N_s(e) \ge 1$ for the rest of the pass.
- The scan for $F' = 1$ with no locked pin on side $s$ leaves $N_s(e) = 1$. To reach $F' = 1$ again in this direction, $N_s(e)$ must first grow, which puts a locked pin on side $s$.

So each of the 4 scans occurs at most once per direction, and the scans cost $O(P)$ in total. Each scan step changes one gain by $\pm 1$ in $O(1)$ time. A gain increase raises a pointer by at most 1, so the pointers rise by at most $O(P)$ in total, and they fall at most as often as they rise, plus $2 p_{\max} + 1$. Lines L8 to L10 take $O(n)$. $\square$

**Theorem.** Let the algorithm start from a balanced partition.

1. Every partition it holds, tentative or real, is balanced.
2. Each execution of line L10 lowers the cut by $G_{k^*} > 0$.
3. It terminates after at most $C + 1$ passes, where $C$ is the cut of the start, and so in $O((C + 1)(n + P))$ time.
4. In the output partition no single move that keeps the balance lowers the cut.

*Proof.* Part 1 and part 2 follow from Lemma 4 and the test of line L9. The cut is a non-negative integer, so at most $C$ passes change the partition, and one more pass ends the loop; Lemma 5 gives the time. For part 4, the last pass starts from the output and has $G_k \le 0$ for all $k$. If it made no move, no move keeps the balance and there is nothing to show. Otherwise, by Lemma 3 its first move has the largest gain among all vertices whose move keeps the balance, since all vertices are free at that point, and this gain is $G_1 \le 0$. By Lemma 1 no such move lowers the cut. $\blacksquare$
