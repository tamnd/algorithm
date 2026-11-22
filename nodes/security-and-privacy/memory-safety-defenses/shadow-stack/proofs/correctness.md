---
title: A protected shadow stack accepts exactly the returns to the matching call site
proves: [correctness, invariant, termination]
status: full
---

**The model.** A run of the protected program is a finite sequence of events $e_1, e_2, \ldots, e_n$. Each event is one of: CALL$(a)$, which saves the return address $a$; RET, which reads a value $r$ from the normal stack and returns to it; WRITE, which changes an entry of the normal stack; and RESTORE$(d)$, a non-local exit to a frame saved at depth $d$. The instrumentation runs PUSH$(S, a)$ at each CALL$(a)$, CHECK-RETURN$(S, r)$ at each RET with the value $r$ that the RET read, and RESTORE$(S, d)$ at each RESTORE$(d)$.

**Assumptions.** (A1) Only lines L1 to L10 write the array $S$ and the index $t$; no WRITE event changes them. (A2) The instrumentation runs at every call, every return and every non-local exit of the run, and nowhere else. (A3) The capacity is at least the largest number of pending calls in the run, and every RESTORE$(d)$ has $d$ at most the current number of pending calls. These are the assumptions that a real shadow stack must make true, by hardware protection of its pages, by the compiler, and by the runtime library.

**The intended stack.** Define a sequence $P_k$ of return addresses after the first $k$ events, from the CALL, RET and RESTORE events alone: $P_0$ is empty; CALL$(a)$ appends $a$; RET removes the last entry; RESTORE$(d)$ keeps the first $d$ entries; WRITE leaves $P$ as it is. For calls and returns that nest, the last entry of $P_{k-1}$ at a RET event $e_k$ is the return address of the CALL event that matches $e_k$, the latest CALL before $e_k$ that has not yet been matched by a RET or cut off by a RESTORE. This is the same matching as for [balanced parentheses](/balanced-parentheses/).

**Invariant (I).** After the first $k$ events, if no fault was raised, then $t = |P_k|$ and $S[i] = P_k[i]$ for $0 \le i < t$.

*Proof of (I), by induction on $k$.*

Base, $k = 0$. Line L1 sets $t = 0$, and $P_0$ is empty. There is no index $i$ to check.

Step. Assume (I) after $k - 1$ events, with no fault. Look at the event $e_k$.

- WRITE. By (A1) neither $S$ nor $t$ changes, and $P_k = P_{k-1}$, so (I) still holds. This is the one place where the protection of the shadow stack is used.
- CALL$(a)$. By (A3) and the hypothesis, $t = |P_{k-1}| <$ capacity, so line L2 does not fault. Line L3 writes $S[t] \leftarrow a$ and line L4 sets $t \leftarrow t + 1$. The entries $S[0], \ldots, S[t-1]$ of the old $t$ do not change. So $S$ holds $P_{k-1}$ followed by $a$, which is $P_k$, and the new $t$ is $|P_k|$.
- RET, with value $r$. Suppose that no fault is raised. Then $t > 0$ by line L5, line L6 sets $t \leftarrow t - 1$, and no entry of $S$ is written. So $S[0], \ldots, S[t-1]$ for the new $t$ are the first $|P_{k-1}| - 1$ entries of $P_{k-1}$, which is $P_k$.
- RESTORE$(d)$. By (A3), $d \le |P_{k-1}| = t$, so line L9 does not fault, and line L10 sets $t \leftarrow d$. No entry is written, so $S[0], \ldots, S[d-1]$ are the first $d$ entries of $P_{k-1}$, which is $P_k$.

In each case (I) holds after $k$ events. $\square$

**Theorem.** Under (A1), (A2) and (A3), at a RET event $e_k$ that reads the value $r$ from the normal stack, CHECK-RETURN raises a fault if and only if $r$ differs from the return address of the matching call, the last entry of $P_{k-1}$. If it raises no fault, it returns $r$, so the return goes to the matching call site. CHECK-RETURN never faults with "empty" on a run whose returns all have a matching call.

*Proof.* By (I) after $k - 1$ events, $t = |P_{k-1}|$ and $S[t - 1]$ is the last entry of $P_{k-1}$. A RET with a matching call has $|P_{k-1}| \ge 1$, so line L5 does not fault. Line L6 sets $t$ to $|P_{k-1}| - 1$, so line L7 compares $r$ with the old $S[t-1]$, the last entry of $P_{k-1}$. It faults exactly when the two differ. If they agree, line L8 returns $r$, which equals the return address of the matching call. $\square$

**Corollary (no false alarm, no missed overwrite).** If no WRITE event changes a saved return address before it is used, the normal stack and the intended stack agree at each RET, so no fault is raised. If WRITE events leave a different value in the saved return address of a pending call when its matching RET reads it, that RET faults. If an earlier RESTORE cut the frame off, the changed value is never used as a return target. In both cases, no RET of the run goes to an address other than the return address of its matching call.

**What the theorem does not say.** It is a statement about returns only. It says nothing about indirect calls and jumps (the forward edges), and nothing about data that a WRITE changes other than saved return addresses. If (A1) fails, for example when the shadow stack is only hidden at a secret address and the attacker can find it, the invariant can break, and so can the theorem.

**Termination and cost.** Each operation runs a fixed number of lines, with no loop, so each one ends after $O(1)$ steps in the [word RAM](/word-ram/) model. A run of $n$ events takes $O(n)$ steps in total. $\blacksquare$
