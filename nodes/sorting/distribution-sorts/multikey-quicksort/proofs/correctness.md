---
title: Multikey quicksort sorts strings in lexicographic order
proves: [correctness, termination]
status: full
---

Let $c(s, d) = s[d]$ for $d < |s|$ and $c(s, d) = -1$ otherwise, where $-1$ is less than every character.

**Fact 1.** Let $s$ and $t$ agree on their first $d$ characters, with $|s| \ge d$ and $|t| \ge d$. If $c(s, d) < c(t, d)$, then $s < t$. If $c(s, d) = c(t, d) = -1$, then $s = t$. If $c(s, d) = c(t, d) \ne -1$, then $s$ and $t$ agree on their first $d + 1$ characters.

*Proof.* If $c(s, d) = -1 < c(t, d)$, then $s$ has length $d$ and is a proper prefix of $t$, so $s < t$. If $-1 < c(s, d) < c(t, d)$, then $d$ is the first index where they differ, and $s[d] < t[d]$. The other two cases follow from the definition of $c$. $\square$

A task $(lo, hi, d)$ is *valid* if all strings of $A[lo \ldots hi - 1]$ have length at least $d$ and agree on their first $d$ characters. Call the state *good* if:

> **(G1)** the ranges of the tasks on $S$ are disjoint, and each task is valid;
> **(G2)** for indices $i < j$ that are not in the same task, $A[i] \le A[j]$;
> **(G3)** $A$ holds the input strings as a multiset.

**Initialization.** The task $(0, n, 0)$ is valid, and there is one task, so (G1) to (G3) hold.

**Maintenance.** Pop $(lo, hi, d)$. If $hi - lo \le 1$, the task is dropped. Its range has at most one index, which was already in a different task from every other index, so (G2) already covers all its pairs. Otherwise, line L6 permutes the range, so (G3) holds, and it creates three ranges $[lo, lt)$, $[lt, gt)$ and $[gt, hi)$ with $c(\cdot, d) < v$, $= v$ and $> v$.

- The two outer ranges hold strings of the old task, so they are valid at depth $d$.
- If $v \ne -1$, the strings of the middle range agree on $d + 1$ characters by Fact 1 and have length at least $d + 1$, so the task $(lt, gt, d + 1)$ is valid. If $v = -1$, the middle range is not pushed.
- The new ranges are disjoint and inside $[lo, hi)$, so (G1) holds.
- For (G2), take $i < j$ in $[lo, hi)$ that are not in the same new task. If they are in different ranges, then $c(A[i], d) < c(A[j], d)$, and $A[i] < A[j]$ by Fact 1. If both are in the middle range and $v = -1$, then $A[i] = A[j]$ by Fact 1. A pair with one index outside $[lo, hi)$ keeps its relation from before, because the range holds the same strings: the order between $A[j]$ outside the range and every string of the range was the same for all strings of the range, by (G2) before the pop.

**Termination.** Let $L$ be the largest length of a string. A valid task has strings of length at least $d$, so $d \le L$ for each task with at least one string. Give a task $(lo, hi, d)$ the weight $(hi - lo)(L + 2 - d) \ge 0$, and let $W$ be the total weight of the tasks on $S$. Pop a task with $m = hi - lo \ge 2$ strings, and let $m_<$, $m_=$ and $m_>$ be the sizes of its three ranges, with $m_= \ge 1$ because the pivot string is in the middle range. The children have the total weight at most $(m_< + m_>)(L + 2 - d) + m_=(L + 1 - d) = m(L + 2 - d) - m_=$, so $W$ drops by at least 1. A pop of a task with at most one string does not increase $W$. So at most $W_0 = n(L + 2)$ pops handle a task with two or more strings. Each of them pushes at most three tasks, so there are at most $1 + 3n(L + 2)$ pops, and the loop ends.

**Result.** When $S$ is empty, (G2) holds for all pairs $i < j$, so $A$ is sorted, and by (G3) it holds the input strings. $\blacksquare$
