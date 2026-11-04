---
title: Correctness and step bound of the shortcut inverse
proves: [correctness]
status: full
---

Fix $i$, let $C = (c_0, c_1, \ldots, c_{L-1})$ be its cycle with $c_{k+1} = \pi(c_k)$, indices mod $L$, and let $i = c_a$. The answer is $\pi^{-1}(i) = c_{a-1}$.

**Lemma 1 (the walk stays on the cycle).** Every value of $j$ is an element of $C$: initially $j = i$, a forward step moves from $c_k$ to $c_{k+1}$, and a shortcut moves from a marked $c_{qt}$ to $c_{(q-1)t}$ (or, for $q = 0$, to the last mark $c_{Qt}$ with $Q = \lceil L / t \rceil - 1$), both on $C$.

**Lemma 2 (stopping).** The loop stops exactly when $\Pi[j] = i$, that is, when $j = c_{a-1}$, since $\pi$ is injective. So if it stops, it returns $\pi^{-1}(i)$.

**Short cycles ($L \le t$).** No element of $C$ is marked, so the walk takes forward steps only: $c_a, c_{a+1}, \ldots$, and reaches $c_{a-1} = c_{a + L - 1}$ after $L - 1$ steps, with $L \le t$ reads of $\Pi$.

**Long cycles ($L > t$).** The marks are $c_0, c_t, \ldots, c_{Qt}$, so between two consecutive marks along the cycle there are at most $t - 1$ unmarked elements: the gaps are $t$, except the last, from $c_{Qt}$ around to $c_0$, which is $L - Qt \le t$ because $Q$ is the largest integer with $Qt < L$.

*Phase 1.* The walk goes forward from $c_a$ until it either stops at $c_{a-1}$ or sits at a marked element $c_b$, with $b$ the first index at or after $a$ (cyclically) that is marked. This takes at most $t$ steps, since $c_b$ is within $t - 1$ positions of $c_a$. If the predecessor $c_{a-1}$ is met first, the loop stops (Lemma 2).

*Phase 2.* At $c_b$ the walk takes the shortcut to the previous mark $c_{b'}$. By the choice of $b$, no element strictly between $c_a$ and $c_b$ is marked, so the previous mark $c_{b'}$ is at or before $c_{a-1}$, cyclically: either $b = a$ and $c_{b'}$ is the mark before $c_a$, or $b \ne a$ and $c_{b'}$ is before $c_a$ because $c_a$ itself is unmarked. Its distance to $c_{a-1}$ is less than the gap $b - b' \le t$.

*Phase 3.* From $c_{b'}$, forward steps reach $c_{a-1}$ after at most $t - 1$ steps, without passing $c_a$, and the loop stops there. A mark met in this phase is passed by a forward step, because `jumped` is set.

In total, the walk reads $\Pi$ at most $t$ times in phase 1, once after the jump, and at most $t - 1$ more times in phase 3, plus the initial read: at most $2t + 1$ reads, so INVERSE takes $O(t)$ time and always terminates.

**Space.** Each long cycle of length $L$ has $Q + 1 = \lceil L / t \rceil \le L/t + 1$ marks and there are at most $n / (t + 1)$ long cycles, so $|S| \le n/t + n/(t+1)$. $\blacksquare$
