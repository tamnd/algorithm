---
title: Pass the buck never frees a node that a guard still traps, frees each node once, and keeps at most n (R + G) + G retired nodes unfreed
proves: [correctness]
status: full
---

**Setting.** There are $n$ asynchronous processes on a sequentially consistent shared memory with atomic reads, writes and compare-and-swap on a pair (value, version). There are $G = n K$ guards; guard $g$ has a word $POST[g]$ and a word $HNDOFF[g] = (val, ver)$. We use the lines L1 to L11 of the page. A value is **escaping** from the call of LIBERATE that it is passed to until a call of LIBERATE returns it. A guard $g$ **traps** a value $v$ at time $t$ if $POST[g] = v$ at every time from some time before $v$ was last passed to LIBERATE up to $t$. The client follows three rules.

1. **Post, then check.** A process accesses a node $x$ only if, after it wrote $x$ to one of its guards at L1, it read the source again and saw $x$, and $x$ was reachable from a root at that read. It does not change that guard until it is done with $x$. The stack reads from the root; the dequeue reads the head again before it uses $head.next$.
2. **Retire after unlink.** A node is given to LIBERATE once per allocation, after the step that removed the last link to it, and it is not linked again before it is freed.
3. **Free only what LIBERATE returns.** A process frees exactly the values of the set that its LIBERATE returns.

Each successful CAS on $HNDOFF[g]$ adds 1 to the version, so a CAS with the expected pair $h$ succeeds only if no other CAS on $HNDOFF[g]$ succeeded since the read that returned $h$.

**Lemma 1 (single location).** Each escaping value is in exactly one place: the set $S$ of one running LIBERATE, or one word $HNDOFF[g]$. Every value in such a place is escaping.

*Proof.* A value enters a set when it is passed in, and by rule 2 it is not escaping then. A successful CAS at L6 replaces the pair $h$ that is in $HNDOFF[g]$, so it moves $v$ from $S$ into the word and the old value $h.val$ from the word into $S$ (L7), in one step. A successful CAS at L10 moves $h.val$ from the word into $S$. A return at L11 ends the escape of every value in $S$. No step copies a value. $\square$

**Lemma 2 (picked-up values are free of guard g).** If LIBERATE adds a value $w$ to $S$ at L7 or L10 while it works on guard $g$, then $g$ does not trap $w$ at that time.

*Proof.* Let $h$ be the pair that the successful CAS replaced, read at time $t_h$. LIBERATE read $POST[g] = v$ at L4 or L8 at a time $t_p$ after $t_h$ and before the CAS. No CAS on $HNDOFF[g]$ succeeded between $t_h$ and the CAS, so $w = h.val$ was in $HNDOFF[g]$ at $t_p$, and $w$ was escaping then. At L10, $w \ne v$ by the test at L9. At L7, $v$ is in $S$ and $w$ is in $HNDOFF[g]$, so $w \ne v$ by Lemma 1. So $g$ did not post $w$ at $t_p$, which is after $w$ was passed to LIBERATE, and so $g$ cannot trap $w$ after $t_p$. $\square$

**Lemma 3 (giving up is safe).** If LIBERATE leaves the loop at L5 to L8 for the value $v$ without a successful CAS, then $g$ does not trap $v$ at that time.

*Proof.* If it leaves at L8, $POST[g] \ne v$ at that read, so $g$ does not trap $v$ after it. The other exits need failed CAS steps. Let the process be $p$, its first read of $HNDOFF[g]$ be at time $A$, and its CAS steps fail at times $B < D < F$, with rereads at $C$ (after $B$) and $E$ (after $D$). A failed CAS at $D$ means that some CAS on $HNDOFF[g]$ succeeded at a time $H$ between $C$ and $D$, and another one succeeded at a time $G'$ between $A$ and $B$.

Suppose some successful CAS at L6 by a process $q$ happens at a time after $G'$ and at or before the exit. That CAS used a pair that $q$ read after the last success before it, so after $G'$, and between that read and its CAS, $q$ read $POST[g] = v_q$ with $v_q$ in its set. By Lemma 1, $v_q \ne v$, because $v$ is in the set of $p$ all along. That read of $POST[g]$ is after $G' > A$, so after $v$ was passed to LIBERATE, and $g$ did not post $v$ then. So $g$ does not trap $v$ at the exit.

It remains to show that such a CAS exists. If $p$ leaves at the test after L8 with $attempts = 2$ and a non-nil value at $E$: if the CAS at $H$ is at L6, we are done; if it is at L10, it stored nil, and a non-nil value at $E$ means that a later CAS stored it, which is a CAS at L6. If $p$ leaves with $attempts = 3$ after the failure at $F$: if no CAS at L6 succeeded in $(G', E]$, then the CAS at $H$ was at L10 and stored nil, so the word holds nil at $E$, and some CAS succeeded between $E$ and $F$. The first of these acts on a nil value, and L10 never acts on nil, so it is at L6. $\square$

**Lemma 4 (invariant).** When a LIBERATE has finished guards $0, \ldots, i - 1$, no value in its $S$ is trapped by any of these guards. No value in $HNDOFF[g]$ is trapped by any guard below $g$.

*Proof.* By induction over the steps. A value that is passed in enters before any guard is done. A value can only stop being trapped, never start, while it is escaping, because a trap needs a post from before the value was passed in. At guard $g$, LIBERATE reads $v = POST[g]$ at L4. A value $u \ne v$ of $S$ is not trapped by $g$, because a trapped value is in $POST[g]$ at all times. If $v \in S$, then either the CAS at L6 moves $v$ out of $S$ into $HNDOFF[g]$, where it is not trapped by guards below $g$ by the induction, or Lemma 3 shows that $g$ does not trap $v$. A value added at L7 or L10 comes from $HNDOFF[g]$, so it is not trapped by guards below $g$ by the induction, and not by $g$ by Lemma 2. $\square$

**Theorem 1 (safety).** No process accesses a node after it is freed.

*Proof.* Let $q$ access $x$ by rule 1, with the post of $x$ in guard $g$ at time $t_1$ and the check read at time $t_2 > t_1$, at which $x$ was reachable. By rule 2, $x$ was not escaping at $t_2$, so it was passed to LIBERATE after $t_2$ and after $t_1$. The guard $g$ keeps $x$ until $q$ is done with it, so $g$ traps $x$ during all that time. By Lemma 4, applied after the last guard, LIBERATE returns no trapped value, so $x$ is returned, and freed by rule 3, only after $q$ is done with it. $\square$

**Theorem 2 (no double free).** Each incarnation of a node is freed at most once.

*Proof.* By Lemma 1, an escaping value is in one set or one word, so only one LIBERATE returns it, and by rules 2 and 3 it is freed once. $\square$

**Theorem 3 (bound).** Let each process call LIBERATE when its set reaches $R$ values. At every time, at most $n (R + G) + G$ retired nodes are unfreed, even if any processes stop.

*Proof.* By Lemma 1, every unfreed retired node is in a set or in a handoff word. There are $G$ handoff words. A process that is not in LIBERATE has fewer than $R$ values. A LIBERATE starts with $R$ values; a CAS at L6 removes one value and adds at most one; a CAS at L10 adds one, at most once per guard. So a set never holds more than $R + G$ values. $\square$

**Theorem 4 (cost).** PostGuard at L1 is one write; with the check read, a protected read is lock free, as in hazard pointers. LIBERATE is wait free: for each guard it does at most three CAS steps at L6 or one at L10, and a constant number of reads, so it takes $O(G)$ steps plus the set operations. A LIBERATE that starts with $R$ values returns at least $R - G$ of them, since each guard keeps at most one, so with $R \ge 2 G$ the cost is $O(1)$ steps per freed node. $\square$

Theorems 1 to 4 give the correctness of the method. $\blacksquare$
