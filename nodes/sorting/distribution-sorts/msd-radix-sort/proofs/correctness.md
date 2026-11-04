---
title: MSD radix sort sorts strings in lexicographic order and is stable
proves: [correctness, stability, termination]
status: full
---

Strings are over $\{0, \ldots, R-1\}$, and $c(s, d) = s[d] + 1$ for $d < |s|$ and $c(s, d) = 0$ otherwise. Write $s[0 \ldots d-1]$ for the prefix of length $d$ (all of $s$ when $d \ge |s|$).

**Fact 1.** Let $s$ and $t$ have the same prefix of length $d$, and let $|s| \ge d$ and $|t| \ge d$. If $c(s, d) < c(t, d)$, then $s < t$ in lexicographic order. If $c(s, d) = c(t, d) = 0$, then $s = t$.

*Proof.* If $c(s, d) = 0 < c(t, d)$, then $|s| = d < |t|$ and $s$ is a proper prefix of $t$, so $s < t$. If $0 < c(s, d) < c(t, d)$, then $s[d] < t[d]$ and $d$ is the first index where they differ. If both are 0, both have length $d$ and the same prefix of length $d$, so they are equal. $\square$

We call a task $(lo, hi, d)$ *valid* if the strings of $A[lo \ldots hi-1]$ all have length at least $d$ and the same prefix of length $d$. We call the array *good* for a set of tasks on $S$ if:

> **(G1)** the ranges of the tasks are disjoint;
> **(G2)** each task is valid;
> **(G3)** for indices $i < j$ that are not in the same task, $A[i] \le A[j]$ in lexicographic order, and if $A[i] = A[j]$ then the item at $i$ came first in the input; and the multiset of $A$ is the input;
> **(G4)** inside each task, equal strings are in input order.

**Initialization.** The single task $(0, n, 0)$ is valid, since each string has the empty prefix. (G1), (G3) and (G4) hold, because there is one task and nothing has moved.

**Maintenance.** Pop a task $(lo, hi, d)$. If $hi - lo \le 1$, drop it. One index forms its own range, so (G3) now covers it with the indices of the other tasks: those are already in order with it by (G3) before the pop, since they were not in the same task. Otherwise, lines L5 to L8 stably sort the range by $c(\cdot, d)$, and lines L9 and L10 push one task for each bucket $r \ge 1$.

- The new ranges are inside $[lo, hi)$ and disjoint, so (G1) holds.
- A string in bucket $r \ge 1$ has length more than $d$ and the old common prefix plus the character $r - 1$. So each new task is valid, and (G2) holds.
- For (G3), take two indices of the old range that are not in the same new task. If they are in different buckets, the one in the lower bucket comes first after the stable sort, and Fact 1 says that its string is less. If both are in bucket 0, the strings are equal by Fact 1, and the stable sort keeps them in the order they had, which is input order by (G4). Pairs with one index outside $[lo, hi)$ keep their old relation, because the range holds the same strings as before.
- (G4) holds in each new task, because the stable sort keeps the order of equal strings.

**Termination.** Let $L = \max_s |s|$. Each pushed task has depth $d + 1$ and holds strings of length at least $d + 1$, so each task on the stack has depth at most $L$. Give a task $(lo, hi, d)$ the weight $(hi - lo)(L + 1 - d)$, which is at least $hi - lo$, and let $W$ be the total weight of the tasks on $S$. When a task with $m = hi - lo \ge 2$ strings is popped, its children have sizes that add up to at most $m$, each with the factor $L - d$, so $W$ drops by at least $m(L + 1 - d) - m(L - d) = m \ge 2$. When a task with at most one string is popped, $W$ does not grow. So at most $W_0/2 = n(L+1)/2$ pops handle a task with two or more strings. Each of them pushes at most $R$ tasks, so the number of pops is at most $1 + R\,n(L+1)/2$, and the loop ends.

**Result.** When $S$ is empty, (G3) holds for all pairs of indices. So $A$ is in lexicographic order, it holds the input strings, and equal strings are in input order. $\blacksquare$
