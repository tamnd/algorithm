---
title: Cycle sort sorts the array and writes each misplaced position exactly once
proves: [correctness, termination]
status: full
---

Let $B[0 \ldots n-1]$ be the input in sorted order. Call a position $q$ **final** when $A[q] = B[q]$, where $=$ means that neither item is less than the other. For $0 \le s \le n-1$ let $M_s$ be the multiset $B[s \ldots n-1]$.

**Outer invariant.** At the start of the iteration of line L2 for $s$:

> **(O)** $A[0 \ldots s-1] = B[0 \ldots s-1]$, and the multiset of $A[s \ldots n-1]$ is $M_s$.

It holds for $s = 0$ because $A$ is a permutation of $B$.

**Lemma 1 (POSITION).** Let $c$ be the number of items of $A[s+1 \ldots n-1]$ that are less than $x$, and suppose the multiset of $A[s+1 \ldots n-1]$ plus $x$ is $M_s$. Then POSITION$(A, s, x)$ returns $s + c$, and $B[s+c], \ldots, B[s+c+m-1]$ are the copies of $x$ in $M_s$, where $m \ge 1$ is their number.

*Proof.* Lines L13 to L15 add 1 for each item of $A[s+1 \ldots n-1]$ less than $x$, so they return $s + c$. The items of $M_s$ less than $x$ are all in $A[s+1 \ldots n-1]$, because $x$ is not less than itself, so exactly $c$ items of $M_s$ are less than $x$. In the sorted order $B[s \ldots n-1]$ of $M_s$ they take the places $s, \ldots, s+c-1$, and the $m$ copies of $x$ come next. $\square$

**Inner invariant.** Fix $s$ with (O), and let $x_0 = A[s]$ at line L3. If line L5 continues, then $c = 0$ for $x_0$, so by Lemma 1 $B[s]$ is a copy of $x_0$, and (O) holds for $s + 1$. Otherwise, at each test of line L7 of this cycle:

> **(I)** The multiset of $A[s+1 \ldots n-1]$ plus $x$ is $M_s$; $A[s]$ still holds $x_0$; each final position of $A[s+1 \ldots n-1]$ at the start of the cycle is still final; and $p$ is the value $s + c$ of Lemma 1 for the held $x$.

At the first test, (I) holds by line L4 and because nothing has been written.

**Lemma 2 (one step).** Assume (I) at line L7. Then line L7 stops at a position $q$ in the block $s+c, \ldots, s+c+m-1$ of $x$ with $A[q] \ne x$, and after line L8, position $q$ is final, no final position of $A[s+1 \ldots n-1]$ has lost its item, and the multiset of $A[s+1 \ldots n-1]$ plus the new $x$ is again $M_s$ if $q \ne s$.

*Proof.* First let $c = 0$. Then $x$ is a smallest item of $M_s$, and $x \ne x_0$: if $x_0$ were a copy of $x$, it would also be a smallest item of $M_s$, which would give $c = 0$ for $x_0$, and line L5 would have continued. So line L7 stops at once at $q = s$. Now let $c \ge 1$, so the block lies in $s+1, \ldots, n-1$. The array part $A[s+1 \ldots n-1]$ holds $m - 1$ copies of $x$, because the held item is the $m$-th copy, so some position of the block does not hold $x$, and line L7, which moves right from the first position of the block past copies of $x$ only, stops at the first such position $q$. In both cases $B[q]$ is a copy of $x$ by Lemma 1, so after line L8 places $x$ at $q$, the position $q$ is final. Before the write $A[q] \ne x = B[q]$, so $q$ was not final, and no final item was moved. If $q \ne s$, the write exchanges an item of $A[s+1 \ldots n-1]$ with the held item, which keeps the multiset of the two together. $\square$

**Termination of a cycle.** By Lemma 2, each write at a position $q \ne s$ turns a position of $A[s+1 \ldots n-1]$ that was not final into a final one, and no final position becomes not final. There are $n - 1 - s$ positions there, so after at most $n - 1 - s$ such writes the next write is at $q = s$, and line L10 ends the loop. Between writes, line L11 sets $p$ by Lemma 1, so (I) holds at the next test of line L7.

**End of a cycle.** The last write is at $q = s$, which by Lemma 2 needs $c = 0$, so the held item is a smallest item of $M_s$ and becomes $B[s]$. The stale copy $x_0$ is now the held item and is dropped. Before this write, the array part $A[s+1 \ldots n-1]$ plus the held item was $M_s$, so after it $A[s \ldots n-1]$ is $M_s$, with $A[s] = B[s]$. So (O) holds for $s + 1$.

**Conclusion.** The loop of line L2 ends after $s = n - 2$. By (O) for $s = n - 1$, $A[0 \ldots n-2] = B[0 \ldots n-2]$ and $A[n-1]$ is the one item of $M_{n-1} = \{B[n-1]\}$. So $A = B$, and the array is sorted.

**Writes.** Each write makes a position final that was not final, and no position stops being final, except that $A[s]$ is not final while it holds the stale copy $x_0 \ne B[s]$, and it is written once, at the end of its cycle. A position that is final at the start of the run is never written: a position $q > s$ is written only when it is not final, and a start $s$ that is final makes line L5 continue. So each position is written at most once, exactly the positions that are not final at the start are written, and the return value of line L12 is the number of positions $i$ with $A[i] \ne B[i]$ in the input. Any algorithm that sorts the array must write each of these positions at least once, so the number is the least possible. $\blacksquare$
