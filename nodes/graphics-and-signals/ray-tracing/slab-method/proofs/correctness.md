---
title: The slab method returns the part of the ray inside the box
proves: [correctness]
status: full
---

We work in exact arithmetic on $\mathbb{R} \cup \{-\infty, +\infty\}$ with the IEEE 754 rules: $1/(+0) = +\infty$, $1/(-0) = -\infty$, $x \cdot (\pm\infty) = \pm\infty$ for $x > 0$, $x \cdot (\pm\infty) = \mp\infty$ for $x < 0$, $0 \cdot (\pm\infty) = $ NaN, and each comparison with NaN is false. We take $\rho = 1$. The preconditions are those of the problem: $lo_a \le hi_a$ are finite, $d \ne 0$, $t_0^{in}$ is finite, $t_1^{in} \le +\infty$, and neither is NaN.

For each axis $a$ let $S_a = \{t \in \mathbb{R} : lo_a \le o_a + t\,d_a \le hi_a\}$. Then $\{t \in \mathbb{R} : r(t) \in B\} = S_0 \cap S_1 \cap S_2$, so the goal is $I = [t_0^{in}, t_1^{in}] \cap S_0 \cap S_1 \cap S_2$. For $x, y \in \mathbb{R} \cup \{\pm\infty, \text{NaN}\}$ write $[x, y]_\mathbb{R} = \{t \in \mathbb{R} : x \le t \le y\}$, where a NaN lower end is read as $-\infty$ and a NaN upper end as $+\infty$.

**Lemma 1 (one slab).** For the values $tn$ and $tf$ of lines L3 and L4 at axis $a$, $[tn, tf]_\mathbb{R} = S_a$.

*Proof.* If $d_a > 0$, then $inv_a = 1/d_a > 0$, line L2 sets $n = lo_a$ and $f = hi_a$, and $lo_a \le o_a + t d_a \le hi_a$ is equivalent to $(lo_a - o_a)/d_a \le t \le (hi_a - o_a)/d_a$, which is $tn \le t \le tf$. If $d_a < 0$, then $inv_a < 0$, line L2 sets $n = hi_a$ and $f = lo_a$, and dividing by the negative $d_a$ reverses both inequalities, which gives $(hi_a - o_a)/d_a \le t \le (lo_a - o_a)/d_a$, again $tn \le t \le tf$. Both values are finite in these two cases.

If $d_a = 0$, then $o_a + t d_a = o_a$ for all $t$, so $S_a = \mathbb{R}$ if $lo_a \le o_a \le hi_a$ and $S_a = \emptyset$ otherwise. Let $s \in \{+1, -1\}$ be the sign of the zero, so $inv_a = s\infty$. For $s = +1$, $tn = (lo_a - o_a)\infty$ and $tf = (hi_a - o_a)\infty$. For $s = -1$, $tn = (hi_a - o_a)(-\infty)$ and $tf = (lo_a - o_a)(-\infty)$. We check the six positions of $o_a$:

| position of $o_a$ | $S_a$ | $(tn, tf)$ for $s = +1$ | $(tn, tf)$ for $s = -1$ |
|---|---|---|---|
| $o_a < lo_a$ | $\emptyset$ | $(+\infty, +\infty)$ | $(-\infty, -\infty)$ |
| $lo_a < o_a < hi_a$ | $\mathbb{R}$ | $(-\infty, +\infty)$ | $(-\infty, +\infty)$ |
| $o_a > hi_a$ | $\emptyset$ | $(-\infty, -\infty)$ | $(+\infty, +\infty)$ |
| $o_a = lo_a < hi_a$ | $\mathbb{R}$ | $(\text{NaN}, +\infty)$ | $(-\infty, \text{NaN})$ |
| $lo_a < hi_a = o_a$ | $\mathbb{R}$ | $(-\infty, \text{NaN})$ | $(\text{NaN}, +\infty)$ |
| $lo_a = o_a = hi_a$ | $\mathbb{R}$ | $(\text{NaN}, \text{NaN})$ | $(\text{NaN}, \text{NaN})$ |

In each row, $[tn, tf]_\mathbb{R}$ is the set in the second column: no real $t$ satisfies $+\infty \le t$ or $t \le -\infty$, and the other rows put no bound on $t$. $\square$

**Lemma 2 (one pass).** Lines L5 and L6 never produce a NaN, and after them $[t_0, t_1]_\mathbb{R}$ equals the old $[t_0, t_1]_\mathbb{R} \cap S_a$.

*Proof.* MAX$(x, y)$ is $x$ if $x > y$ and $y$ otherwise. If $tn$ is NaN, the comparison is false and the result is the old $t_0$, which is not NaN by induction, and $\{t : t \ge \text{NaN}\}$ is read as $\mathbb{R}$. If $tn$ is not NaN, the result is $\max(tn, t_0)$, and $\{t : t \ge \max(tn, t_0)\} = \{t : t \ge tn\} \cap \{t : t \ge t_0\}$. The same argument with MIN applies to line L6 and the upper ends. Intersecting the two half lines with Lemma 1 gives the claim. $\square$

**Theorem.** SLAB-TEST returns MISS if $I = \emptyset$. Otherwise it returns $(t_0, t_1)$ with $t_0, t_1$ real and $I = [t_0, t_1]$.

*Proof.* Let $A$ be the set of axes after which line L7 did not return. By Lemma 2 and induction on the passes, the invariant $[t_0, t_1]_\mathbb{R} = [t_0^{in}, t_1^{in}] \cap \bigcap_{a \in A} S_a$ holds after each pass, and at the start with $A = \emptyset$.

If line L7 returns MISS at axis $a$, then $t_0 > t_1$, so $[t_0, t_1]_\mathbb{R} = \emptyset$, and $I$ is a subset of it by the invariant. So $I = \emptyset$ and the answer is right.

Suppose the loop ends and line L8 runs. By the invariant with $A = \{0, 1, 2\}$, $[t_0, t_1]_\mathbb{R} = I$. Since $t_0$ only grows from the finite $t_0^{in}$, $t_0 > -\infty$. Since $d \ne 0$, some axis $b$ has $d_b \ne 0$, its $tf$ is finite, and from that pass on $t_1 \le tf < +\infty$. Line L7 did not fire at the last pass, so $t_0 \le t_1 < +\infty$. So both ends are real, $t_0 \le t_1$, and $I = [t_0, t_1]$ is not empty.

It remains to show that MISS is returned whenever $I = \emptyset$. If the loop ends, $I$ is not empty by the last paragraph. So when $I = \emptyset$ the loop cannot end, and the only other exit is MISS at line L7. $\blacksquare$

**Remark on the first argument rule.** The proof uses that MAX and MIN return the old running value when the slab value is NaN. With the arguments swapped, a NaN $tn$ would become $t_0$, the invariant would break, and since $t_0 > t_1$ is false for $t_0 = $ NaN, line L7 could not return MISS on a later axis.
