---
title: The Steinhaus-Johnson-Trotter algorithm visits every permutation once, by adjacent exchanges
proves: [correctness]
status: full
---

A *state* of SJT$(n)$ is the array $A[1 \ldots n]$ together with the directions $d[1 \ldots n]$. The array $pos$ is the inverse of $A$ at all times, because line L1 sets it so and line L8 changes $A$ and $pos$ together. For a state with the value $n$ in $A$, its *reduced state* is the array $A'$ of length $n - 1$ that $A$ gives when $n$ is removed, with the directions $d[1 \ldots n-1]$.

Recall the list $L_n$ from the page: $L_1 = (1)$, and for $n \ge 2$, if $L_{n-1} = (\pi_1, \ldots, \pi_N)$ with $N = (n-1)!$, then $L_n$ is made of $N$ blocks, where block $t$ lists $\pi_t$ with $n$ inserted at positions $n, n-1, \ldots, 1$ when $t$ is odd, and at positions $1, 2, \ldots, n$ when $t$ is even.

**Lemma 1.** Let $n \ge 2$, and let the value $n$ be at position 1 or at position $n$ of $A$. Then a value $m < n$ is mobile in the state if and only if it is mobile in the reduced state.

*Proof.* Let $m$ be at position $p$ of $A$ and $q = p + d[m]$. If $q$ is the position of $n$, then $m$ is not mobile in $A$, because $n > m$. In $A'$, the value $n$ is gone from an end of the array, so $m$ is at that end of $A'$ and points out of it, and $m$ is not mobile in $A'$. Otherwise the position $q$ is inside $A$ if and only if the place next to $m$ in direction $d[m]$ is inside $A'$, and the two places hold the same value, since removing $n$ from an end does not change which values are neighbors. So the two tests agree. $\square$

**Lemma 2.** Let the value $n$ point in direction $d[n]$. Then $n$ is mobile unless it is at position 1 with $d[n] = -1$, or at position $n$ with $d[n] = +1$.

*Proof.* If $q = pos[n] + d[n]$ is inside the array, then $A[q] < n$, because $n$ is the largest value. $\square$

**Theorem.** Let $n \ge 1$, and let SJT$(n - 1)$ visit the states $s_1, \ldots, s_N$ in order, for $n \ge 2$. Then SJT$(n)$ makes exactly $n \cdot N$ visits, in $N$ blocks of $n$ visits each, such that:

1. at each visit of block $t$, the reduced state is $s_t$;
2. in block $t$, the value $n$ is at positions $n, n - 1, \ldots, 1$ when $t$ is odd, and at positions $1, 2, \ldots, n$ when $t$ is even.

So the arrays that SJT$(n)$ visits form the list $L_n$, for all $n \ge 1$.

*Proof.* For $n = 1$, line L1 sets $A = (1)$, line L2 visits it, and line L5 does not test any value, so line L6 returns. The run is $L_1$.

Let $n \ge 2$. We prove by induction on $t$ that block $t$ exists and starts with this condition: the reduced state is $s_t$, and the value $n$ is at position $n$ with $d[n] = -1$ when $t$ is odd, and at position 1 with $d[n] = +1$ when $t$ is even. For $t = 1$, line L1 gives $A = (1, \ldots, n)$ with all directions $-1$. The reduced state is the start state of SJT$(n - 1)$, which is $s_1$, and $n$ is at position $n$ with $d[n] = -1$.

Take block $t$ with $t$ odd. The case of $t$ even is the same with left and right exchanged. The value $n$ starts at position $n$ and points left. While $n$ is at a position $p \ge 2$, Lemma 2 says that $n$ is mobile. It is the largest value, so line L5 stops at $m = n$ at once. Line L8 moves $n$ to position $p - 1$. Line L9 turns no value, as no value is larger than $n$. The other values keep their order and their directions, so the reduced state stays $s_t$. After $n - 1$ such steps, the visits of the block have put $n$ at positions $n, n - 1, \ldots, 1$, and $n$ is at position 1 with $d[n] = -1$. This proves parts 1 and 2 for block $t$.

Now $n$ is at position 1 and points left, so it is not mobile, by Lemma 2. By Lemma 1, the values $m < n$ that are mobile are the ones that are mobile in $s_t$. So line L5 tests $n$ and then finds the same largest mobile value $m$ that SJT$(n-1)$ finds in the state $s_t$, or it finds none when SJT$(n-1)$ finds none.

If it finds none, then $t = N$, because SJT$(n-1)$ stops exactly after its last visit $s_N$. Then SJT$(n)$ returns at line L6, and the run has $n \cdot N$ visits.

If it finds $m$, then $t < N$. The value $m$ is mobile, so its neighbor $u$ in direction $d[m]$ is smaller than $m$, and $u \ne n$. In $A'$ the same value $u$ is next to $m$ in the same direction, as in the proof of Lemma 1. So line L8 makes in $A'$ the same exchange as SJT$(n-1)$ makes, and it does not move $n$, which is at position 1 and is not $u$. Line L9 turns the values $m + 1, \ldots, n - 1$, as SJT$(n-1)$ does, and it also turns $n$. So the reduced state becomes $s_{t+1}$, and $n$ is at position 1 with $d[n] = +1$. This is the start condition of block $t + 1$, which is even. This completes the induction.

By parts 1 and 2, the array at the visits of block $t$ is $\pi_t$, the array of $s_t$, with $n$ inserted at the positions of the definition of $L_n$. So by induction on $n$, the run of SJT$(n)$ is $L_n$. $\blacksquare$

**Corollary 1.** SJT$(n)$ visits each permutation of $[n]$ exactly once, and two consecutive visits differ by the exchange of two adjacent positions.

*Proof.* The list $L_n$ holds each permutation once: removing $n$ from a permutation $\sigma$ of $[n]$ gives the unique $\pi_t$ with $\sigma$ in block $t$, and inside the block the position of $n$ fixes $\sigma$. By induction $L_{n-1}$ holds each permutation of $[n-1]$ once, so $L_n$ holds each permutation of $[n]$ once. Between two visits, line L8 exchanges the values at positions $p$ and $q = p \pm 1$. $\blacksquare$

**Corollary 2.** For $n \ge 2$, the last visit of SJT$(n)$ is $2\,1\,3\,4 \cdots n$, and the value $m$ moves exactly $(m - 1)(m - 1)!$ times, for $2 \le m \le n$.

*Proof.* For $n = 2$, $L_2 = (1\,2,\ 2\,1)$. For $n \ge 3$, the number $N = (n-1)!$ of blocks is even, so the last block lists the last permutation of $L_{n-1}$ with $n$ at positions $1, \ldots, n$, and it ends with $n$ at position $n$. By induction the last permutation of $L_{n-1}$ is $2\,1\,3 \cdots (n-1)$, so the last visit is $2\,1\,3 \cdots n$.

The value $n$ moves $n - 1$ times in each of the $(n-1)!$ blocks. Between blocks, the run makes the moves of SJT$(n-1)$, so a value $m < n$ moves as many times in SJT$(n)$ as in SJT$(n-1)$. By induction on $n$, this number is $(m - 1)(m - 1)!$. $\blacksquare$
