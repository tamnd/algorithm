---
title: Gnome sort sorts the array and stops after n + 2d steps
proves: [correctness, termination]
status: full
---

Let $d_0$ be the number of inversions of the input. Each change of $A$ is the exchange of line L6, so $A$ always holds a permutation of the input.

**Invariant.** At each test of line L2, $0 \le i \le n$, and $A[0 \ldots i-1]$ is sorted.

*Initialization.* $i = 0$, and the empty prefix is sorted.

*A step forward (line L4).* If $i = 0$, the new prefix is $A[0 \ldots 0]$, which is sorted. If $i > 0$, the test found $A[i-1] \le A[i]$. The prefix $A[0 \ldots i-1]$ is sorted and its last item is at most $A[i]$, so $A[0 \ldots i]$ is sorted. The step happens only when $i < n$, so the new $i$ is at most $n$.

*A step back (lines L6 and L7).* This needs $i > 0$. The exchange changes only $A[i-1]$ and $A[i]$. The new prefix is $A[0 \ldots i-2]$, which was a part of the sorted prefix $A[0 \ldots i-1]$ and is not changed by the exchange. So it is sorted, and the new $i$ is at least 0.

**Correctness.** The loop stops only when $i \ge n$, and with $i \le n$ this means $i = n$. By the invariant, $A[0 \ldots n-1]$ is sorted.

**Termination.** A step back exchanges $A[i-1]$ and $A[i]$ with $A[i-1] > A[i]$. This pair is an inversion before the exchange and not after it, and no other pair changes its order, because the two items are neighbours. So each step back lowers the number of inversions by exactly 1, and a step forward does not change it. The number of inversions is never negative, so there are at most $d_0$ steps back. Between two steps back, and after the last one, the steps forward raise $i$, which is at most $n$, so there are at most $n$ of them in a row. So the loop makes finitely many steps.

**The number of steps.** When the loop stops, $A$ is sorted and has no inversions, so there were exactly $d_0$ steps back. Each step changes $i$ by $+1$ or $-1$, from 0 to $n$, so there were $n + d_0$ steps forward, and $n + 2d_0$ steps in total. $\blacksquare$
