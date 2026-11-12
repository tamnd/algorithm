---
title: The Chou-Fasman procedure computes the labels its rules define, in O(n^2) time
proves: [correctness]
status: full
---

We use the names and line numbers of the pseudocode on the page. The sequence has $n$ residues, $P(r)$ is the propensity of residue $r$ for the state at hand (times 100), and a nucleus window has width $w \ge 4$. Write $W(t) = P(t) + P(t+1) + P(t+2) + P(t+3)$ for the sum of the four residues that start at $t$, for $0 \le t \le n - 4$.

**Specification.** For a nucleus that starts at $s_0$, its segment is $[s, e)$ with

- $s$ the smallest integer with $0 \le s \le s_0$ such that $W(t) \ge 400$ for every $t$ with $s \le t < s_0$;
- $e$ the largest integer with $s_0 + w \le e \le n$ such that $W(u - 3) \ge 400$ for every $u$ with $s_0 + w \le u < e$.

In words: the segment grows to the left one residue at a time while the four residues that start at the new left end have a sum of at least 400, and it grows to the right while the four residues that end at the new right end have a sum of at least 400. A segment is accepted for its state when its mean propensity for that state is above the accept threshold and its sum for that state is larger than its sum for the other state. A residue gets H when it is in an accepted helix segment and in no accepted strand segment, E in the opposite case, and C when it is in neither. When it is in both, its maximal run of such residues gets H if the sum of $P_\alpha$ over the run is larger than the sum of $P_\beta$, else E.

**Lemma 1 (EXTEND).** EXTEND$(P, s_0, s_0 + w)$ stops and returns the segment of the specification.

*Proof.* The loop of line L6 lowers $s$ by exactly 1 in each step and runs only while $s > 0$, so it stops after at most $s_0$ steps. Before each test of line L6, $W(t) \ge 400$ holds for each $t$ with $s \le t < s_0$. At the start $s = s_0$ and there is no such $t$. A step runs only when $W(s - 1) \ge 400$, and it changes $s$ to $s - 1$, which adds exactly the index $t = s - 1$; so the invariant stays true. When the loop stops, $s = 0$ or $W(s - 1) < 400$. Any start smaller than $s$ would need $t = s - 1$ to exist and to have $W(s - 1) \ge 400$, so no smaller start meets the specification, and $s$ is the smallest one. Every window that the loop reads lies inside the sequence: $t + 3 \le s_0 + 2 < s_0 + w \le n$.

The loop of line L7 is the mirror image. It raises $e$ by exactly 1 in each step and runs only while $e < n$, so it stops after at most $n - s_0 - w$ steps. Before each test, $W(u - 3) \ge 400$ for each $u$ with $s_0 + w \le u < e$, by the same argument. When it stops, $e = n$ or $W(e - 3) < 400$, so no larger end meets the specification. The window start $u - 3 \ge s_0 + w - 3 \ge s_0 + 1$ is valid because $w \ge 4$. $\square$

**Lemma 2 (SEGMENTS).** SEGMENTS returns exactly the accepted segments of one state.

*Proof.* Line L2 visits the start of each window of width $w$ that has at least $k$ residues with propensity above the former threshold $f$, which is the definition of a nucleus. For each nucleus, line L3 computes its segment by Lemma 1. Line L4 tests $\sum P > a \cdot (e - s)$. This is the test $\frac{1}{e - s}\sum P > a$ of the mean, multiplied by the positive length $e - s$, so the two tests agree. Line L4 also tests the sum against the sum for the other state. All values are integers, so no rounding can change a decision. $\square$

**Theorem.** CHOU-FASMAN returns the labels of the specification.

*Proof.* By Lemma 2, after lines L11 and L12 the flag $h[r]$ is true exactly when residue $r$ is in an accepted helix segment, and $b[r]$ is true exactly when it is in an accepted strand segment. Line L13 gives each residue with one flag its state and each residue with no flag C.

Lines L14 to L19 scan the residues from left to right. The scan reaches each index either by a step of 1 from the index before it (line L19, taken only when that index has at most one flag) or by a jump to $t$ (line L18), and $t$ is $n$ or an index with at most one flag. So when the scan is at an index $r$ with both flags, $r = 0$ or $r - 1$ has at most one flag. The inner loop of line L17 then advances $t$ while both flags are true, so $[r, t)$ is a maximal run of residues with both flags. Line L18 gives the whole run the label of the specification, and the scan goes on at $t$. Each residue with both flags lies in exactly one maximal run, and the scan meets each run once, so each such residue gets the right label. Lines L14 to L19 change no other label. $\blacksquare$

**Cost.** Let $w$ be fixed. Line L2 costs $O(nw)$ for all windows. There are at most $n$ nuclei. By Lemma 1, EXTEND does at most $n$ steps for one nucleus, at $O(1)$ each, and the sums of line L4 cost $O(n)$. So SEGMENTS costs $O(n^2)$ in the worst case, the flags of lines L11 and L12 cost $O(n^2)$, and the scan of lines L14 to L19 costs $O(n)$, because each index is visited once by $r$ or by $t$. The bound is tight for this procedure: for $n \ge 6$ alanines (helix propensity 142), every window of width 6 is a nucleus and every segment is $[0, n)$, so the work is $\Theta(n^2)$.
