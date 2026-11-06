---
title: Correctness of Brent's variant of Pollard's rho
proves: [correctness, termination]
status: full
---

Let $N \ge 2$, $0 \le s < N$, $m \ge 1$, $f(x) = (x^2 + c) \bmod N$, $x_0 = s$ and $x_{i+1} = f(x_i)$. Let $\mu \ge 0$ and $\lambda \ge 1$ be the tail and cycle lengths of the sequence $(x_i)$: $x_0, \dots, x_{\mu+\lambda-1}$ are distinct, and $x_{i+\lambda} = x_i$ for $i \ge \mu$. They exist because the sequence takes values in a set of $N$ elements (as in the proof for [Pollard's rho](/pollard-rho/)). Then for $j > i \ge \mu$, $x_j = x_i$ if and only if $\lambda \mid j - i$.

**Lemma 1 (the indices).** At the start of the block with length $r$ (the first is $r = 1$, then $r$ doubles), $y = x_{2r-2}$. In that block, line L3 sets $x = x_{2r-2}$, and the comparisons of line L7 are $|x - x_j|$ for $j = 3r - 1, 3r, \dots$ in order, up to $4r - 2$ if the block is not cut short. If the block runs to the end, $y = x_{4r - 2} = x_{2(2r) - 2}$ at its end.

*Proof.* For $r = 1$, line L1 gives $y = x_0$. Suppose $y = x_{2r-2}$ at the start of a block. Line L3 saves $x = x_{2r-2}$ and applies $f$ $r$ times, so $y = x_{3r-2}$. The loop of lines L5 to L8 applies $f$ once before each comparison, so the comparisons use $x_{3r-1}, x_{3r}, \dots$, and the batches together contain $r - k$ steps at most, $r$ in all, ending at $x_{4r-2}$. Since $4r - 2 = 2(2r) - 2$, the claim holds for the next block. $\square$

**Lemma 2 (the product).** At each gcd of line L8, $q \equiv \prod |x - x_j| \pmod N$, the product over all comparisons made so far (in all blocks, each with the saved value of its own block).

*Proof.* $q$ starts at $1$ and each comparison multiplies it by the new difference modulo $N$. $\square$

**Termination of the main loop.** Let $r^*$ be the least power of two with $r^* \ge \max(\lambda, \mu, 2)$. Suppose the loop reaches the block with $r = r^*$. Its saved index is $2r - 2 \ge r \ge \mu$. Its comparison indices $j$ run over $3r - 1, \dots, 4r - 2$, so $j - (2r - 2)$ runs over the $r$ consecutive integers $r + 1, \dots, 2r$; since $r \ge \lambda$, one of them is a multiple of $\lambda$. For that $j$, $x_j = x_{2r-2}$, the difference is $0$, and by Lemma 2 $q \equiv 0 \pmod N$ at the next gcd, which gives $g = \gcd(0, N) = N \ne 1$. So the loop of line L2 ends at the latest in this block, after $O(r^*) = O(N)$ evaluations of $f$. All inner loops are finite.

**The backtrack.** Suppose that after the main loop $g = N$. Consider the last batch, the one whose gcd gave $N$, and let $t_1, \dots, t_\ell$ ($\ell \le m$) be its differences. The previous gcd (or the start, with $q = 1$) gave $1$, so the product $q'$ before this batch is coprime to $N$. Let $p$ be any prime factor of $N$. Since $p \mid N = \gcd(q, N)$ and $q \equiv q' t_1 \cdots t_\ell \pmod N$, $p$ divides $q' t_1 \cdots t_\ell$, and $p \nmid q'$, so $p \mid t_i$ for some $i$. Line L6 saved $y_s = y$ at the start of this batch, and $x$ is unchanged, so the loop of line L11 recomputes $|x - y_s|$ equal to $t_1, t_2, \dots$ in order. At the first $i$ with $\gcd(t_i, N) > 1$, which exists by the argument above and has $i \le \ell \le m$, the loop stops.

**Correctness.** The algorithm returns $g$ only when $g > 1$, either from the main loop (where $g \ne 1$) or from line L11 (where $g > 1$). In both cases $g$ is a gcd with $N$, so $g$ is a divisor of $N$ with $g > 1$. If some prime $p \mid N$ divides a difference before every prime power part of $N$ does, the gcd at that batch, or the backtrack, returns a proper divisor of $N$ that is a multiple of $p$. $\blacksquare$
