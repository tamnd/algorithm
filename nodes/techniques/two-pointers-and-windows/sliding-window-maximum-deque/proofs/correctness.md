---
title: The monotonic deque reports the maximum of every window of length k
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode of the page, with $1 \le k \le n$. For $0 \le r \le n - 1$ let $W_r = \{\max(0, r-k+1), \ldots, r\}$. An index $i \in W_r$ is a *leader* of $W_r$ if $A[i] > A[j]$ for every $j$ with $i < j \le r$. Let $\Lambda_r$ be the list of the leaders of $W_r$ in increasing order of index.

**Lemma 1.** The values of $\Lambda_r$ strictly decrease, $r$ is the last element of $\Lambda_r$, and the first element of $\Lambda_r$ is an index $i$ with $A[i] = \max_{j \in W_r} A[j]$.

*Proof.* If $i < i'$ are both leaders, then $A[i] > A[i']$ because $i < i' \le r$. The index $r$ is a leader, because there is no $j$ with $r < j \le r$. Let $m$ be the largest index in $W_r$ with $A[m] = \max_{W_r} A$. Each $j$ with $m < j \le r$ has $A[j] < A[m]$, by the choice of $m$, so $m$ is a leader. A leader $i < m$ would need $A[i] > A[m]$, which is not possible. So $m$ is the first leader. $\blacksquare$

**Lemma 2.** For $r \ge 1$, the leaders of $W_r$ are: the leaders $i$ of $W_{r-1}$ with $i \ge r - k + 1$ and $A[i] > A[r]$, and the index $r$.

*Proof.* Take $i \in W_r$ with $i < r$. Then $i \in W_{r-1}$ and $i \ge r - k + 1$. The condition "$A[i] > A[j]$ for all $i < j \le r$" is the condition for $W_{r-1}$ together with $A[i] > A[r]$. $\blacksquare$

**Claim.** After line L5 of step $r$, $D$ equals $\Lambda_r$ from front to back. So line L6 appends $\max_{W_r} A$ for each $r \ge k - 1$, and the output is $M[l] = \max(A[l \ldots l+k-1])$ for $l = 0, \ldots, n - k$.

*Proof.* By induction on $r$.

*Step $r = 0$.* $D$ is empty after line L1. Line L3 does nothing, line L4 gives $D = (0)$, and line L5 tests $0 \le -k$, which is false. $\Lambda_0 = (0)$.

*Step $r \ge 1$.* By induction, $D = \Lambda_{r-1}$ before line L3. Its values strictly decrease by Lemma 1. Line L3 pops from the back while the back value is at most $A[r]$. Because the values decrease from front to back, the popped indices are exactly the indices of $\Lambda_{r-1}$ with value at most $A[r]$, and the kept ones are those with value greater than $A[r]$. Line L4 appends $r$. Now $D$ holds the leaders $i$ of $W_{r-1}$ with $A[i] > A[r]$, then $r$. All indices of $\Lambda_{r-1}$ are at least $r - k$, since they are in $W_{r-1}$. The only one that can be less than $r - k + 1$ is $r - k$ itself, and if it is in $D$, it is at the front because the indices increase. Line L5 removes it exactly in this case. ($r - k$ is never equal to $r$, so line L5 never removes the index just pushed.) By Lemma 2, $D = \Lambda_r$.

*Output.* By Lemma 1 the front of $\Lambda_r$ has the maximum value of $W_r$. For $r \ge k - 1$, $W_r = \{r - k + 1, \ldots, r\}$ is the window that starts at $l = r - k + 1$. So line L6 appends $M[l]$, for $l = 0, 1, \ldots, n - k$ in order. $\blacksquare$

**Why the popped indices lose nothing.** An index $j$ popped by line L3 at step $r$ has $A[j] \le A[r]$ and $j < r$. Each window $W_{r'}$ with $r' \ge r$ that contains $j$ also contains $r$, because windows are intervals. So $A[j]$ is never the strict maximum of a later window, and if it ties the maximum, $A[r]$ has the same value. The proof above makes this exact through Lemma 2.

**Termination and cost.** The for loop runs $n$ times. Each index enters $D$ once, in line L4, and leaves at most once, so the total number of pops in lines L3 and L5 is at most $n$, and the while loop of line L3 runs at most $n$ times with a pop in total. Each step ends the while loop with at most one comparison that is false. So the total number of comparisons of values in line L3 is at most $2n - 2$: there are at most $n - 1$ pops at the back, since the index $n - 1$ is never popped at the back, and at most $n - 1$ false tests, since step 0 makes none. The time is $\Theta(n)$. At each moment $D \subseteq W_r$, so $|D| \le k$. $\blacksquare$
