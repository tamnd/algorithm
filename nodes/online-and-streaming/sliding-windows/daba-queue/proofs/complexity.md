---
title: DABA makes at most 1, 4 and 3 operator calls per query, insert and evict, and stores 2n values
proves: [time.worst, space.extra]
status: full
---

We count calls of $\otimes$, including calls with the identity $1$ as an argument. The helpers $\Pi_F, \Pi_L, \Pi_R, \Pi_A, \Pi_B$ read one slot or return $1$ and make no call.

**FIXUP.** FIXUP has no loop and no recursion, and it runs exactly one of three branches. The singleton branch (line L7) and the shift branch (line L11) assign positions only, with no call. The flip (line L9) assigns positions only, and by the correctness proof it is always followed by a shrink. The shrink makes two calls in line L12, for $\Pi_L \otimes \Pi_R \otimes \Pi_A$, and one call in line L14. So FIXUP makes 0 or 3 calls.

**Operations.** QUERY makes exactly one call, in line L1. INSERT makes one call in line L2 and then runs FIXUP, so it makes 1 or 4 calls. EVICT makes no call in line L4 and then runs FIXUP, so it makes 0 or 3 calls.

**Theorem.** In every state, QUERY makes 1 call, INSERT at most 4 calls and EVICT at most 3 calls of $\otimes$. Each operation also does $O(1)$ other steps: a fixed number of position assignments and comparisons, and one push or pop on the deque. With a deque that supports push at the back, pop at the front and access by position in $O(1)$ worst-case time, every operation takes $O(1)$ worst-case time when $\otimes$ takes $O(1)$ time.

*Proof.* The counts are those above. Every line of QUERY, INSERT, EVICT and FIXUP runs at most once per operation, and each line does a constant number of steps. $\square$

**Both bounds are reached.** Start from the empty window. The insert of a makes 1 call and runs the singleton case. The insert of b makes 1 call in line L2; then $F < B$ and $L = B$, so FIXUP flips and shrinks, with 3 more calls, 4 in total. After two more inserts, c and d, the positions relative to $F$ are $F, L, R, A, B, E = 0, 1, 2, 3, 4, 4$, so $L < R$. An evict now finds $F \ne B$ and $L \ne B$ after line L4, and runs a shrink, with 3 calls.

**Space.** Each slot stores two values, $\mathit{val}$ and $\mathit{agg}$, and the six positions are integers. So the structure stores $2n$ values for $n$ items, which is $\Theta(n)$. $\blacksquare$
