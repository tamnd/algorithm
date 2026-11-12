---
title: LHD stays within its capacity, counts every lifetime once, and computes the discrete hit density
proves: [correctness]
status: full
---

We use the pseudocode of the page with a capacity of $C \ge 1$ bytes, positive integer sizes, $S \ge 1$ samples, $K \ge 1$ classes, $A \ge 1$ age bins, coarseness $\kappa \ge 1$, interval $I \ge 1$ and decay $0 \le \delta \le 1$. Let $U$ be the number of cached bytes. The invariants are:

- (I1) $U \le C$, and $U$ is the sum of the sizes of the cached objects;
- (I2) every cached object $x$ has $\mathit{last}(x) \le t$ and $\mathit{refs}(x) \ge 1$, so its age bin $\min(\lfloor (t - \mathit{last}(x))/\kappa \rfloor, A - 1)$ and its class $\min(\mathit{refs}(x), K) - 1$ are valid indices;
- (I3) the sum of all new lifetime counts equals the number of hits plus the number of evictions since the last reconfiguration, and the sum of all new hit counts equals the number of hits in that time.

**Lemma 1 (the eviction loop stops).** If $s \le C$ and (I1) holds, the loop on line L6 stops after at most as many passes as there are cached objects, and afterwards $U + s \le C$.

*Proof.* While $U + s > C$ we have $U > C - s \ge 0$, so some object is cached and line L7 draws a sample of at least one object. Line L9 evicts one object of size at least 1, so $U$ falls. After all objects are gone, $U = 0$ and $U + s = s \le C$, so the loop has stopped by then. $\square$

**Theorem.** (I1) to (I3) hold after every request, and a request is a hit if and only if its object was cached before it.

*Proof.* By induction; all hold at the start. Line L1 raises $t$, which keeps $\mathit{last}(x) \le t$. On a hit (lines L3 and L4), the class and age bin are read before the update, so both are valid by (I2), and one hit and one lifetime are counted. Then $\mathit{last}(x) = t$ and $\mathit{refs}(x)$ grows, which keeps (I2). On line L5 nothing is cached. Otherwise Lemma 1 applies; each eviction on line L9 counts one lifetime in a valid bin, by (I2), and lowers $U$ by the size of $v$. Line L10 adds $s$ to $U$, so $U \le C$, and sets $\mathit{last}(x) = t$ and $\mathit{refs}(x) = 1$. Line L12 clears the new counts when it folds them in, so (I3) holds after a reconfiguration too. Line L2 tests membership, which gives the hit rule. $\blacksquare$

**Lemma 2 (the table).** After line L12, let $H$ and $L$ be the histograms of a class. The single pass of lines L13 and L14, going from $a = A - 1$ down to $0$ and keeping running sums
$$
h_a = \sum_{e \ge a} H[e], \qquad \ell_a = \sum_{e \ge a} L[e], \qquad w_a = w_{a+1} + \ell_a \ (w_A = 0),
$$
gives $w_a = \sum_{e \ge a} (e - a + 1)\,L[e]$, so it sets $\mathit{rank}[a] = h_a / w_a$, or 0 when $w_a = 0$.

*Proof.* By induction from $a = A - 1$ down. For $a = A - 1$, $w_a = L[A-1]$, which is the formula. If $w_{a+1} = \sum_{e \ge a+1} (e - a)\,L[e]$, then
$$
w_a = \sum_{e \ge a+1} (e - a)\,L[e] + \sum_{e \ge a} L[e] = \sum_{e \ge a} (e - a + 1)\,L[e]. \qquad \square
$$

**Lemma 3 (a density).** If $w_a > 0$, then $0 \le \mathit{rank}[a] \le 1$.

*Proof.* Every hit is also a lifetime, so the new counts satisfy $\text{new hits}[e] \le \text{new lives}[e]$ for every bin, and folding with the same $\delta$ keeps $H[e] \le L[e]$. Then $h_a = \sum_{e \ge a} H[e] \le \sum_{e \ge a} L[e] \le \sum_{e \ge a} (e - a + 1)\,L[e] = w_a$. $\square$

So $\mathit{rank}[a]$ is the ratio of the expected number of hits to the expected remaining time in bins, both estimated from the lifetimes that reached bin $a$, which is Eq. 6 of the paper on the grid of bins, before dividing by the size.

**Corollary (exact eviction).** If $S$ is at least the number of cached objects, line L7 draws all of them, and line L8 evicts an object of least hit density, the one with the oldest last request on a tie.

**The test file.** It checks the rank table of the worked example, compares the table with a direct computation of the formula after several rounds of random counts and decay, checks the corollary against the global minimum, checks (I1) to (I3) after every request on 25 seeded traces with mixed sizes, checks that an object larger than the capacity is not cached, and checks the learning example with and without a full sample.
