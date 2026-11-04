---
title: American flag sort sorts strings in lexicographic order
proves: [correctness, termination]
status: full
---

Let $c(s, d) = s[d] + 1$ for $d < |s|$ and $c(s, d) = 0$ otherwise. A task $(lo, hi, d)$ is *valid* if the strings of $A[lo \ldots hi - 1]$ have length at least $d$ and agree on their first $d$ characters.

**Fact 1.** Let $s$ and $t$ agree on their first $d$ characters, with $|s|, |t| \ge d$. If $c(s, d) < c(t, d)$ then $s < t$. If $c(s, d) = c(t, d) = 0$ then $s = t$. If $c(s, d) = c(t, d) \ge 1$ then they agree on $d + 1$ characters. (This is Fact 1 of [MSD radix sort](/msd-radix-sort/), with the same proof.)

**Lemma (one step).** Let a task $(lo, hi, d)$ with $m = hi - lo \ge 2$ be popped. After lines L5 to L11, the range $A[lo \ldots hi - 1]$ is a permutation of its old content, and for each $r$ the block $A[start[r] \ldots end[r] - 1]$ holds exactly the strings with $c(\cdot, d) = r$.

*Proof.* The blocks are disjoint and cover $[lo, hi)$, in the order of $r$, because $start[r + 1] = start[r] + C[r] = end[r]$ and $end[R] = hi$. We show that the following holds before and after each execution of lines L9 to L11:

> **(P1)** for each $b$, $start[b] \le next[b] \le end[b]$, and $A[start[b] \ldots next[b] - 1]$ holds strings of bucket $b$;
> **(P2)** for each $b$, the number of strings of bucket $b$ at positions outside $[start[b], next[b])$ is $end[b] - next[b]$, and these positions are all in blocks $b'$ at positions in $[next[b'], end[b'])$;
> **(P3)** the range is a permutation of its old content.

At the start $next[b] = start[b]$, so (P1) holds; there are $C[b] = end[b] - start[b]$ strings of bucket $b$, so (P2) holds; and (P3) holds.

In the scan of bucket $r$, let $i = next[r] < end[r]$ and $b = c(A[i], d)$. If $b = r$, line L10 extends block $r$ by a string of bucket $r$, and (P1) to (P3) still hold. If $b \ne r$, the string at $i$ is an unplaced string of bucket $b$, so by (P2) $end[b] - next[b] \ge 1$ and $next[b] < end[b]$. Line L11 swaps it into position $next[b]$ and then increases $next[b]$. Block $b$ grows by a string of bucket $b$, so (P1) holds for $b$; the string that moved to $i$ was at an unplaced position, and $i$ is still unplaced in block $r$, so (P1) holds for $r$ and (P2) holds for every bucket. A swap keeps (P3).

Each execution of lines L9 to L11 increases $\sum_b next[b]$ by 1, and this sum is at most $\sum_b end[b]$, so the loops end, after at most $m$ executions. When the scan of bucket $r$ ends, $next[r] = end[r]$, and $next[r]$ never decreases. So at the end $next[b] = end[b]$ for all $b$, and by (P1) each block holds only strings of its bucket. $\square$

**Correctness.** Call the state *good* if the tasks on $S$ have disjoint ranges and are valid, every pair of indices $i < j$ that are not in the same task has $A[i] \le A[j]$, and $A$ holds the input strings. The first task $(0, n, 0)$ makes the state good. When a task with at most one string is popped, nothing changes and the state stays good. When a task with $m \ge 2$ strings is popped, the lemma gives blocks in the order of $c(\cdot, d)$.

- Two strings in different blocks are in order by Fact 1.
- Two strings in block 0 are equal by Fact 1.
- Each block $r \ge 1$ with at least two strings becomes a task, valid at $d + 1$ by Fact 1. A block with one string has no partner.
- Pairs with one index outside $[lo, hi)$ keep their relation, because the range holds the same strings as before.

So the state stays good.

**Termination.** Let $L$ be the largest length of a string. A valid task with at least one string has $d \le L$. Give a task the weight $(hi - lo)(L + 1 - d)$, as in the proof for MSD radix sort. A pop of a task with $m \ge 2$ strings replaces its weight $m(L + 1 - d)$ by children of total weight at most $m(L - d)$, so the total weight drops by at least $m \ge 2$, and other pops do not increase it. So the number of pops of tasks with two or more strings is at most $n(L + 1)/2$. Line L12 pushes only tasks with at least two strings, so every pop after the first is of such a task, and the loop ends.

**Result.** When $S$ is empty, every pair $i < j$ has $A[i] \le A[j]$, and $A$ holds the input strings, so $A$ is sorted. $\blacksquare$
