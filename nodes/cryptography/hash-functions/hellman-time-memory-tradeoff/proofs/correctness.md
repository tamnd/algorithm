---
title: Hellman inversion is always right and succeeds on every covered target
proves: [correctness]
status: full
---

Let $f : X \to Y$, and for each table $i$ let $R_i : Y \to X$ and $g_i = R_i \circ f$. After HELLMAN-PRECOMPUTE, table $T_i$ maps end points to start points. For a pair $(SP, EP)$ stored in $T_i$, the *stored chain* is $SP = c_0, c_1, \ldots, c_t = EP$ with $c_{j+1} = g_i(c_j)$. A target $y$ is *covered* if some table $i$ has a stored chain with $f(c_j) = y$ for some $0 \le j \le t - 1$.

**Lemma 1 (stored pairs).** For each key $EP$ of $T_i$, $g_i^t(T_i[EP]) = EP$.

*Proof.* Line L5 stores $T_i[EP] = SP$ only with $EP = g_i^t(SP)$ from line L4, and never overwrites a key. $\square$

**Lemma 2 (soundness).** If HELLMAN-INVERT($y$) returns $x$, then $f(x) = y$.

*Proof.* The only return of a value is at line L9, right after the test $f(x) = y$. $\square$

**Lemma 3 (the online walk).** In table $i$, at the test of line L9 with counter $s$, $z = g_i^s(R_i(y))$.

*Proof.* Line L7 sets $z = R_i(y) = g_i^0(R_i(y))$. Each run of line L10 applies $g_i$ once and is followed by the next value of $s$. $\square$

**Lemma 4 (completeness on covered targets).** If $y$ is covered by the stored chain $(SP, EP)$ of table $i$ at position $j \le t - 1$, then HELLMAN-INVERT($y$) returns a value, at the latest in table $i$ at $s = t - 1 - j$.

*Proof.* Suppose the algorithm has not returned before it reaches table $i$ with $s = t - 1 - j$. Since $f(c_j) = y$, we have $R_i(y) = g_i(c_j) = c_{j+1}$. By Lemma 3, $z = g_i^{t-1-j}(c_{j+1}) = c_t = EP$, which is a key of $T_i$. So line L9 sets $x = g_i^{t-1-s}(T_i[EP]) = g_i^{j}(SP) = c_j$, and $f(c_j) = y$, so it returns. A false alarm at an earlier step, where $f(x) \ne y$, does not stop the loops, so this step is reached unless an earlier step returns. By Lemma 2, any earlier return is also a correct preimage. $\square$

**Lemma 5 (cost).** HELLMAN-INVERT makes at most $\ell t$ lookups and at most $\ell(t - 1) + a \cdot t$ calls of $f$, where $a$ is the number of end point matches at line L9.

*Proof.* Each table runs the loop of line L8 at most $t$ times, with one lookup and at most one call of $f$ at line L10. Each match at line L9 makes $t - 1 - s$ calls of $f$ to rebuild the chain and one call for the check, so at most $t$. $\square$

**Theorem.** HELLMAN-INVERT never returns a wrong answer. It returns a preimage of $y$ for every covered target $y$, and for some targets that are not covered by the definition above when another preimage lies on a stored chain. It makes $O(\ell t + a t)$ calls of $f$.

*Proof.* Lemma 2 gives soundness, Lemma 4 completeness on covered targets, and Lemma 5 the cost. $\blacksquare$

**Remark (coverage).** The probability that a random $x$ lies on a stored chain of one table is what Hellman bounds: if the first $i - 1$ chains hold at most $(i - 1)t$ distinct points, then point $j$ of chain $i$ is new with probability at least $(1 - it/N)^{j+1}$, when $f$ and $R_i$ act as random functions, since a repeat at any of the $j + 1$ points from the start makes the rest of the chain old. Summing over $i$ and $j$ and dividing by $N$ gives the bound on the page.
