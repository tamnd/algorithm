---
title: After k Grover iterations a measurement gives a marked item with probability sin^2((2k+1) theta)
proves: [correctness]
status: full
---

We use the pseudocode of the page. The search space is $\{0, 1, \ldots, N-1\}$, the set of marked items is $S$ with $|S| = M$ and $1 \le M \le N$, and $\theta \in (0, \pi/2]$ is the angle with $\sin \theta = \sqrt{M/N}$. The oracle is the phase oracle $O|x\rangle = (-1)^{f(x)} |x\rangle$, and $D = 2|s\rangle\langle s| - I$ with $|s\rangle = N^{-1/2} \sum_{x} |x\rangle$. One iteration (lines L4 and L5) applies $G = D\,O$.

**Claim.** Let $|g\rangle = M^{-1/2} \sum_{x \in S} |x\rangle$, and, when $M < N$, let $|b\rangle = (N-M)^{-1/2} \sum_{x \notin S} |x\rangle$. For each $k \ge 0$,

$$G^k |s\rangle = \sin((2k+1)\theta)\, |g\rangle + \cos((2k+1)\theta)\, |b\rangle.$$

So the measurement of line L6 gives a marked item with probability $\sin^2((2k+1)\theta)$. With $k = \lfloor \pi/(4\theta) \rfloor$ from line L1, this probability is at least $1 - M/N$. GROVER-SEARCH never returns an item that is not marked.

*Proof.* **The case $M = N$.** Then $\theta = \pi/2$, $|s\rangle = |g\rangle$ and $k = 0$. The state at line L6 is $|s\rangle$, all items are marked, and $\sin^2(\pi/2) = 1$. The claim holds. From now on, $M < N$, so $0 < \theta < \pi/2$.

**Step 1: the start state.** The vectors $|g\rangle$ and $|b\rangle$ are unit vectors with disjoint supports, so they are orthonormal. We have

$$|s\rangle = \sqrt{M/N}\, |g\rangle + \sqrt{(N-M)/N}\, |b\rangle = \sin\theta\, |g\rangle + \cos\theta\, |b\rangle.$$

**Step 2: the oracle on the plane.** For a real angle $\alpha$, let $|v(\alpha)\rangle = \sin\alpha\, |g\rangle + \cos\alpha\, |b\rangle$. The oracle multiplies each marked basis state by $-1$ and leaves the others, so $O|g\rangle = -|g\rangle$ and $O|b\rangle = |b\rangle$. Hence

$$O|v(\alpha)\rangle = -\sin\alpha\, |g\rangle + \cos\alpha\, |b\rangle = |v(-\alpha)\rangle.$$

**Step 3: the diffusion on the plane.** By Step 1, $|s\rangle = |v(\theta)\rangle$. Then $\langle s | v(\alpha)\rangle = \sin\theta \sin\alpha + \cos\theta \cos\alpha = \cos(\alpha - \theta)$. So

$$D|v(\alpha)\rangle = 2\cos(\alpha - \theta)\, |v(\theta)\rangle - |v(\alpha)\rangle.$$

We compute the two coordinates with $2\cos A \sin B = \sin(A+B) - \sin(A-B)$ and $2 \cos A \cos B = \cos(A+B) + \cos(A-B)$, where $A = \alpha - \theta$ and $B = \theta$. The $|g\rangle$ coordinate is $\sin\alpha - \sin(\alpha - 2\theta) - \sin\alpha = \sin(2\theta - \alpha)$. The $|b\rangle$ coordinate is $\cos\alpha + \cos(\alpha - 2\theta) - \cos\alpha = \cos(2\theta - \alpha)$. Hence $D|v(\alpha)\rangle = |v(2\theta - \alpha)\rangle$.

**Step 4: one iteration is a rotation by $2\theta$.** By Steps 2 and 3, $G|v(\alpha)\rangle = D|v(-\alpha)\rangle = |v(2\theta + \alpha)\rangle$.

**Step 5: induction on $k$.** For $k = 0$, $G^0|s\rangle = |v(\theta)\rangle$ by Step 1. If $G^k|s\rangle = |v((2k+1)\theta)\rangle$, then Step 4 gives $G^{k+1}|s\rangle = |v((2k+1)\theta + 2\theta)\rangle = |v((2k+3)\theta)\rangle$. This proves the formula for the state.

**Step 6: the success probability.** By the [Born rule](/born-rule/), the measurement gives $x$ with probability $|\langle x | G^k s\rangle|^2$. For $x \in S$ this is $\sin^2((2k+1)\theta)/M$, and the sum over the $M$ marked items is $\sin^2((2k+1)\theta)$.

**Step 7: the choice of $k$.** Let $k = \lfloor \pi/(4\theta) \rfloor$. Then $\pi/(4\theta) - 1 < k \le \pi/(4\theta)$, so $\pi/2 - 2\theta < 2k\theta \le \pi/2$, and

$$\frac{\pi}{2} - \theta < (2k+1)\theta \le \frac{\pi}{2} + \theta.$$

On the interval $[\pi/2 - \theta, \pi/2 + \theta]$, which lies in $[0, \pi]$, the function $\sin^2$ is smallest at the two ends, where it equals $\cos^2\theta = 1 - M/N$. So the success probability is at least $1 - M/N$.

**Step 8: no wrong answer.** Line L7 evaluates $f(x)$ and returns $x$ only if $f(x) = 1$. Otherwise line L8 returns FAIL. So each returned item is marked, and FAIL has probability at most $M/N$. $\blacksquare$

**Remark (any $N$).** The proof uses only $D = 2|s\rangle\langle s| - I$ and $O$. When $N$ is not a power of two, take any unitary $A$ with $A|0\rangle = |s\rangle$ and set $D = A(2|0\rangle\langle 0| - I)A^\dagger$. The proof is the same.
