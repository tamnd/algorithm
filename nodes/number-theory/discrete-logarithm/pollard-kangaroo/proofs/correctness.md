---
title: Correctness of Pollard's kangaroo algorithm
proves: [correctness, termination]
status: full
---

Let $p \ge 2$, $g \in (\mathbb{Z}/p\mathbb{Z})^*$, $h \in \mathbb{Z}/p\mathbb{Z}$ and $0 \le a \le b$. Put $w = b - a$ and $h' = h g^{-a}$, as in line L1. For an integer $y \ge 0$, $g^{a + y} = h$ if and only if $g^y = h'$, so the task is to return $a + z$ for some $z \in [0, w]$ with $g^z = h'$, or NONE if there is no such $z$.

**Lemma 1 (invariants).** In every attempt, the tame kangaroo satisfies $T = g^t$ and the wild kangaroo satisfies $W = h' g^u$, where $t$ and $u$ are their distances.

*Proof.* Line L4 sets $T = g^{\lfloor w/2 \rfloor}$ with $t = \lfloor w/2 \rfloor$ and $W = h'$ with $u = 0$. Line L13 multiplies a kangaroo by $g^{2^j}$ and adds $2^j$ to its distance, which keeps both relations. $\square$

**Lemma 2 (table entries).** Every entry $D[Y] = (\kappa, d)$ was written at line L12 by kangaroo $\kappa$ while it stood at $Y$ with distance $d$.

*Proof.* Line L12 is the only line that writes to $D$, and it writes the current point, kind and distance. Line L5 empties $D$ at the start of each attempt. $\square$

**Soundness of the kangaroo phase.** Suppose line L11 returns $a + z$. Then $0 \le z \le w$ and $g^z = h'$ were checked on that line, so $a + z \in [a, b]$ and $g^{a + z} = h' g^a = h$. (By Lemmas 1 and 2 the check always succeeds when $z \in [0, w]$: the point $Y$ was visited by the tame kangaroo at distance $t$ and by the wild one at distance $u$, so $g^t = Y = h' g^u$ and $g^{t - u} = h'$; the check is kept because it costs one exponentiation and protects against mistakes in the bookkeeping.)

**The certificate.** Suppose line L15 is reached. Baby-step giant-step with bound $n = w + 1$ uses $m = \lceil \sqrt n \rceil$, stores $g^j$ for $0 \le j < m$ with the least such $j$ for each element, and tests $h' g^{-im}$ for $i = 0, 1, \dots, m - 1$. Let $z^*$ be the least integer $z \ge 0$ with $g^z = h'$, if any.

- If $z^* \le w$, then $z^* < m^2$, so $z^* = i^* m + j^*$ with $0 \le i^*, j^* < m$, and the test at $i^*$ hits. Any hit at a round $i$ yields a solution $i m + j \ge 0$, and a hit at $i < i^*$ would give a solution smaller than $i^* m \le z^*$, which is impossible. So the first hit is at $i^*$ and returns $i^* m + T[g^{j^*}] \le z^*$, a solution, hence equal to $z^*$. Line L15 returns $a + z^*$.
- If $z^*$ exists and $z^* > w$, or no $z^*$ exists, then there is no solution in $[0, w]$. Every hit returns a solution $z \ge 0$, so $z \ge z^* > w$, and line L15 returns NONE; with no hit it also returns NONE.

**Correctness.** By the soundness of the kangaroo phase and the certificate, every value returned is in $[a, b]$ and satisfies $g^x = h$, and NONE is returned only by line L15, which does so only when no $z \in [0, w]$ satisfies $g^z = h'$, that is, when no $x \in [a, b]$ satisfies $g^x = h$.

**Termination.** Each attempt runs at most $N_{\max}$ rounds of two jumps, there are $R$ attempts, and baby-step giant-step makes at most $2m + O(\log m)$ group operations. So the algorithm stops after $O(R N_{\max} + \sqrt w)$ group operations, which is $O(\sqrt w)$ for $R$ constant and $N_{\max} = O(\sqrt w)$. $\blacksquare$
