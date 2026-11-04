---
title: The combining funnel counter is linearizable, and every call finishes when all threads keep running
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page. SWAP of a cell, CAS and writes of a $loc$ word, reads and writes of a $result$ word, and the FETCH-AND-ADD of the counter are atomic. The fields $sum$ and $kids$ of a record are written only by its owner. The specification is the sequential counter: fetch-and-add$(x)$ returns the current value $c$ and sets it to $c + x$.

Fix a call $\kappa$ of thread $me$. Between its line L1 and its return, $me$ runs no other call, so we speak of the record of $\kappa$.

**Lemma 1 (who changes $loc$).** During $\kappa$, $me.loc$ is written by $me$ only at lines L1, L5, L7 and L9, and by another thread only by the CAS of line L6, which changes it from a layer number $d$ to CAPTURED. Once it is CAPTURED, it stays CAPTURED until $\kappa$ returns.

*Proof.* By inspection. Lines L5 and L9 are CASes that expect a layer number, and line L7 runs only after line L5 succeeded, so $loc$ is SELF just before it, and nobody else changes SELF (line L6 expects a layer number). So none of the writes of $me$ replaces CAPTURED, and other threads only write CAPTURED. $\square$

**Lemma 2 (captures).** Say that $p$ *captures* $\kappa$ when the CAS of line L6 of a call of $p$ on $me.loc$ succeeds during $\kappa$. Then $\kappa$ is captured at most once. If it is captured, it does not reach line L10, and from the capture on, $me.sum$ and $me.kids$ do not change. If it is not captured, it reaches line L10.

*Proof.* Only one CAS can change $loc$ from a layer number to CAPTURED, since it then stays CAPTURED (Lemma 1). After the capture, the next CAS of $me$ at line L5 or line L9 fails, as $loc$ is not a layer number, and $\kappa$ goes to line L11. Changes of $sum$ and $kids$ happen only at line L6 of $me$, which requires a successful CAS at line L5 in the same round, and $loc$ is SELF from that CAS until line L7, so it cannot be captured in between, and no change of $sum$ happens after the capture. A capture can happen only while $loc$ is a layer number, that is, before line L10, since line L9 for $d = D - 1$ sets $loc$ to $D$, and no CAS at line L6 expects $D$. If $\kappa$ is never captured, every CAS of $me$ at lines L5 and L9 succeeds, and it reaches line L10. $\square$

So the captures form a forest: each captured call has one parent, its capturer. A capturer reads the sum of its kid after the capture (line L6), so the value it adds is the final sum of the kid. The forest has no cycle, since a call can capture only while it is not captured, and a captured call no longer captures.

**Lemma 3 (sums and ranges).** For each call $\kappa$ with amount $x$, at the moment it reaches line L10 or is captured, its final sum is $x$ plus the amounts of all calls in its subtree. Its kids, in the order of $kids$, have offsets $b_1 < b_2 < \ldots$ with $b_1 = x$, and $b_{j+1} = b_j + sum(kid_j)$, and $b_j + sum(kid_j) \le sum(\kappa)$.

*Proof.* By induction on the height of the subtree. At line L1 the sum is $x$ and there are no kids. Each successful line L6 appends the kid with offset equal to the current sum, and then adds the final sum of the kid (Lemma 2). So the offsets are the prefix sums of $x$ followed by the sums of the kids, and the final sum is $x$ plus the sums of the kids, each of which, by induction, is the sum of the amounts of its subtree. $\square$

**Definition (ranges).** Give each call a range of counter values. A root, the call that reaches line L10, gets $[v, v + sum)$, where $v$ is the value returned by its FETCH-AND-ADD. A kid at offset $b$ of a call with range starting at $s$ gets the range that starts at $s + b$ and has length equal to its sum. By Lemma 3, the ranges of the kids of a call and the first $x$ values of its own range are disjoint and fill the range of the call.

**Lemma 4 (results).** Each call returns the start of its range.

*Proof.* A root returns $v$ (line L13). A captured call returns the value written into its $result$ by its capturer at line L12, which is $s + b$, where $s$ is the value that the capturer returns, by induction on the depth: the capturer returns the start of its own range. The result word of $\kappa$ is reset at line L1, before $loc$ is set to 0, so before any capture of $\kappa$, and it is written once, by the parent. $\square$

**Theorem (linearizability).** Each history of the funnel is linearizable with respect to the sequential counter.

*Proof.* Each root $\rho$ performs exactly one FETCH-AND-ADD of $sum(\rho)$ at line L10. Every call in the subtree of $\rho$ is pending at that step: it was invoked before it was captured, and it returns only after it reads its result, which is computed from $v$, so after the step. Linearize all calls of the subtree at this step, in increasing order of the start of their ranges. By Lemma 3 these ranges tile $[v, v + sum(\rho))$, each starting where the previous one ends after its own amount, so in this order, the call that starts at $s$ sees the counter at $s$ and adds its own amount $x$, and the next call starts at $s + x$.

Here we must check that the ranges of a subtree, ordered by start, are such that the call with range start $s$ and amount $x$ is followed by the call with start $s + x$. Inside the range of a call with start $s$, the call's own amount takes $[s, s + x)$, and its kids' ranges follow in order, each tiled recursively in the same way. So the order by start lists, for each call, first the call and then its kids' subtrees, each in this order; this is a preorder of the tree, and consecutive starts differ by the amount of the earlier call. So the sequence of calls, replayed on a counter that holds $v$, returns the start of each range, which by Lemma 4 is what each call returned.

The FETCH-AND-ADD steps of different roots are atomic steps on the counter, so they are ordered, and between two of them the counter does not change. Each root's step adds the total amount of its subtree. So the sequence of all linearized calls, root step by root step, is a legal sequential history. The points are inside the calls, so the order respects real time. Pending calls that are in the subtree of a root that has done its step are completed with their results; the others are removed. $\square$

**Theorem (progress).** No call waits for a call that it captured. If every thread keeps taking steps, every call finishes. A call that is never captured finishes within $O(D(w + 1))$ of its own steps, where $w$ is the wait of line L8.

*Proof.* The only waiting is at line L11, for the result from the capturer. A root never waits: it passes each layer in at most a constant number of steps plus $w$, applies line L10, and writes the results of its kids in $|kids|$ steps. A call captured by $p$ waits until $p$ reaches line L12; $p$ was not captured when it captured, so either $p$ is a root or $p$ is captured later by a call of a thread that is still running. Along the chain of capturers, each one was captured after the one before captured it, and the chain ends at a root, which finishes by the above if its thread keeps taking steps; then the results flow down the chain, each step of which is one write. So every call finishes. The funnel is not lock-free: a capturer that stops for ever blocks the calls it captured. $\blacksquare$
