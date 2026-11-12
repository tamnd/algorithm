---
tag: DE85PH
kind: concept
slug: working-set-model
name: Working set model
aliases:
- Denning working set
- working set
- working set policy
area: systems/caching-policies
level: intro
summary: "Denning's working set W(t, tau) is the set of pages used in the last tau references. It measures the locality of a program and explains thrashing; it is not itself a replacement rule."
prereqs: [locality-of-reference]
see_also: [lru, page-fault, demand-paging, reuse-distance, cache-hit-ratio, clock, inclusion-property, multilevel-caching]
sources:
  - paper: doi:10.1145/363095.363141
    title: "Peter J. Denning, The working set model for program behavior, Communications of the ACM 11(5) (1968), 323-333"
    locator: the definition of W(t, tau), the working set size, the relation to the interreference distribution, and the use of working sets for memory allocation and against thrashing
  - paper: doi:10.1145/361268.361281
    title: "Peter J. Denning and Stuart C. Schwartz, Properties of the working-set model, Communications of the ACM 15(3) (1972), 191-198"
    locator: the mean working set size s(tau), its concavity, and the relation of its slope to the missing-page rate
  - paper: doi:10.1145/1070838.1070856
    title: "Peter J. Denning, The locality principle, Communications of the ACM 48(7) (2005), 19-24"
    locator: the history of the working set, thrashing, and the phase and transition view of program behavior
  - url: "https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys-policy.pdf"
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces, Chapter 22, Beyond Physical Memory, Policies
    locator: Section 22.12, Thrashing, which uses the working set to decide which processes to run
---

The working set model, introduced by Peter Denning in 1968, describes the memory demand of a program by the set of pages it used recently. For a time $t$, counted in references of the program, and a window $\tau$, the working set $W(t, \tau)$ is the set of distinct pages referenced in the last $\tau$ references, those at times $t - \tau + 1, \ldots, t$. Its size $\omega(t, \tau) = |W(t, \tau)|$ estimates how much memory the program needs now. The working set is a model of program behavior. The *working set policy*, which keeps exactly $W(t, \tau)$ in memory, is one use of it, and it differs from a fixed-size replacement policy such as [LRU](/lru/) because the memory it gives a program grows and shrinks.

## In plain words

Look back over the last few hundred steps of a program and write down each page it touched. That list is its working set. If the program is in a loop over a small table, the list is short. If it moves on to a new task, the list changes, and for a short time it grows.

The idea gives the operating system a rule of thumb. A program runs well when its whole working set is in memory. If the system runs so many programs that their working sets do not fit together, each program keeps losing the pages it needs, and the machine spends its time moving pages instead of doing work. This is called thrashing. The fix is to run fewer programs at once, so that each one has room for its working set.

## The idea

**Definition.** Let $r_1 r_2 \cdots r_n$ be the page references of one process, and let $\tau \ge 1$. Then

$$W(t, \tau) = \{ r_s : t - \tau < s \le t \}, \qquad \omega(t, \tau) = |W(t, \tau)|.$$

For $t < \tau$ the window starts at $s = 1$. Two facts follow at once from the definition. First, $W(t, \tau) \subseteq W(t, \tau + 1)$, so a larger window gives a larger set. Second, $\omega(t, \tau) \le \min(\tau, t)$.

**The working set policy.** Before reference $t$, keep in memory exactly $W(t - 1, \tau)$. Reference $t$ is a fault exactly when $r_t \notin W(t - 1, \tau)$, that is, when its *backward reuse time*, the time since the previous reference to $r_t$, is larger than $\tau$, or when $r_t$ is new. A page leaves memory when $\tau$ references pass without a use of it, not when another page needs its frame. So the policy decides the size of the memory of each process as well as its contents.

**Compared with LRU.** LRU with $k$ frames hits a reference exactly when its [reuse distance](/reuse-distance/), the number of distinct other pages since the previous use, is less than $k$. The working set policy hits a reference exactly when its reuse time is at most $\tau$. Both keep the most recently used pages; LRU fixes the number of pages, and the working set fixes the age. On a phase with few distinct pages the working set shrinks and frees memory for other processes, which LRU with a fixed $k$ cannot do.

**Size and fault rate.** Let $s(\tau)$ be the mean of $\omega(t, \tau)$ over $t$, and let $m(\tau)$ be the fault rate of the working set policy. Denning and Schwartz showed for long stationary traces that $s(\tau + 1) - s(\tau)$ tends to $m(\tau)$, so $s$ is a concave increasing function of $\tau$ whose slope is the fault rate. A finite form of this is exact: for a trace of length $n$,

$$\sum_{t=1}^{n} \bigl(\omega(t, \tau + 1) - \omega(t, \tau)\bigr) = \#\{ s \le n - \tau : \text{the next reference to } r_s \text{ is more than } \tau \text{ steps after } s, \text{ or there is none} \}.$$

The reason is that a page $r_s$ is in $W(t, \tau + 1)$ but not in $W(t, \tau)$ exactly when its last reference up to $t$ is at time $s = t - \tau$.

**Thrashing and load control.** If the sum of the working set sizes of the running processes is larger than the main memory, each process faults often, and the processor waits for the disk most of the time. The working set principle says: run a process only if its working set fits in the memory that is free, and otherwise suspend a process. This keeps the system out of thrashing.

## Examples

Take the trace $a\,b\,c\,a\,b\,d\,e\,e\,e\,f\,a$ with $n = 11$ and $\tau = 4$.

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $r_t$ | $a$ | $b$ | $c$ | $a$ | $b$ | $d$ | $e$ | $e$ | $e$ | $f$ | $a$ |
| $W(t, 4)$ | $a$ | $ab$ | $abc$ | $abc$ | $abc$ | $abcd$ | $abde$ | $bde$ | $de$ | $ef$ | $aef$ |
| fault | F | F | F | | | F | F | | | F | F |

The sizes are $1, 2, 3, 3, 3, 4, 4, 3, 2, 2, 3$, with mean $30/11 \approx 2.7$, and the policy has 7 faults. During the three references to $e$, the working set falls to 2 pages, which LRU with 4 frames would not give back. The last reference to $a$ is a fault because $a$ was last used 7 steps earlier, more than $\tau$.

For other windows on the same trace:

| $\tau$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| faults | 9 | 9 | 7 | 7 |
| mean size $s(\tau)$ | $11/11$ | $19/11$ | $26/11$ | $30/11$ |

The differences of the sums of sizes are $11, 8, 7, 4$, and they agree with the count in the identity above. A larger window costs memory and saves faults, and the gain stops at the point where the window is longer than the reuse times of the loop.

A non-example: a program that scans a huge array once has a working set of $\tau$ pages for each $\tau$, and the policy faults on each new page whatever the window. The working set then does not describe a locality, because there is none.

## Where it is used

- **Load control in operating systems.** The working set principle decides how many processes to keep in memory. VMS and Windows NT keep a working set for each process, with limits, and trim it when free memory is short.
- **Approximations.** Exact working sets need a time stamp per reference. Practical systems sample reference bits at intervals, as in WSClock, a working set variant of [CLOCK](/clock/), or adjust the memory of a process by its fault rate, as in the page fault frequency rule.
- **Measuring locality.** The curves $s(\tau)$ and $m(\tau)$ summarize a trace, much like the [miss ratio curve](/miss-ratio-curve/) does for LRU.
- **Elsewhere.** The idea of a working set appears for processor caches, for database buffer pools and for the hot data of key-value stores, wherever one asks how much data a program is using now.

## References
