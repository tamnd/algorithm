---
title: The digit-by-digit method returns the integer square root and its remainder
proves: [correctness, termination]
status: full
---

Let $\beta \ge 2$ and $A = \sum_{i=0}^{2n-1} a_i \beta^i$ with $0 \le a_i < \beta$. For $0 \le j \le n$ let $P_j = \lfloor A / \beta^{2(n-j)} \rfloor$, the number formed by the top $2j$ digits. Then $P_0 = 0$, $P_n = A$, and

$$P_{j+1} = P_j \beta^2 + g_j, \qquad g_j = a_{2k+1} \beta + a_{2k}, \quad k = n - 1 - j, \qquad 0 \le g_j \le \beta^2 - 1 .$$

For an integer $P \ge 0$, the integer $q \ge 0$ satisfies $q = \lfloor \sqrt P \rfloor$ if and only if $q^2 \le P < (q + 1)^2$, that is, if and only if $0 \le P - q^2 \le 2q$.

**Invariant.** After $j$ passes of the loop of line L2, $q = \lfloor \sqrt{P_j} \rfloor$ and $r = P_j - q^2$, so $0 \le r \le 2q$.

*Initialization.* Line L1 sets $q = r = 0$, and $\lfloor \sqrt{P_0} \rfloor = 0$, $P_0 - 0 = 0$.

*Maintenance.* Assume the invariant after $j$ passes, with values $q$ and $r$. Line L3 sets $\rho = r \beta^2 + g_j = P_{j+1} - q^2 \beta^2$.

*Step 1: the new root lies in a range of $\beta$ values.* Let $Q' = \lfloor \sqrt{P_{j+1}} \rfloor$. First, $(q\beta)^2 = q^2 \beta^2 \le P_j \beta^2 \le P_{j+1}$, so $Q' \ge q\beta$. Second, $P_j \le (q+1)^2 - 1$ by the invariant, so

$$P_{j+1} \le ((q+1)^2 - 1)\beta^2 + \beta^2 - 1 = (q+1)^2 \beta^2 - 1 < ((q+1)\beta)^2,$$

and $Q' < (q+1)\beta$. Hence $Q' = q\beta + x^*$ for a unique $x^* \in \{0, \ldots, \beta - 1\}$.

*Step 2: line L4 finds $x^*$.* For each $x \in \{0, \ldots, \beta - 1\}$,

$$(q\beta + x)^2 = q^2 \beta^2 + (2q\beta + x)\, x,$$

so $(q\beta + x)^2 \le P_{j+1}$ holds if and only if $(2q\beta + x)\, x \le \rho$. The left side $(2q\beta + x)x$ increases with $x$, so the set of digits $x$ that satisfy the test is an initial segment $\{0, \ldots, x_{\max}\}$, which contains 0. Its largest element is the largest $x$ with $(q\beta + x)^2 \le P_{j+1}$. By Step 1 this is $x^*$: $(q\beta + x^*)^2 = Q'^2 \le P_{j+1}$, and for $x^* < x \le \beta - 1$, $q\beta + x > Q'$ gives $(q\beta + x)^2 > P_{j+1}$. So line L4 sets $x = x^*$. (The binary search of the implementation keeps $lo \le x^* \le hi$, since the test holds at $lo$ and the set is an initial segment, so it ends with $lo = hi = x^*$.)

*Step 3: the new values.* Line L6 sets $q' = q\beta + x^* = Q'$, and line L5 sets

$$r' = \rho - (2q\beta + x^*)\, x^* = P_{j+1} - q^2\beta^2 - (2q\beta + x^*)\, x^* = P_{j+1} - Q'^2 .$$

So the invariant holds after $j + 1$ passes, and $0 \le r' \le 2q'$ follows from $Q' = \lfloor \sqrt{P_{j+1}} \rfloor$.

*Termination.* The loop of line L2 runs $n$ times, and line L4 examines at most $\beta$ candidates.

**Theorem.** DIGIT-SQRT returns $q = \lfloor \sqrt A \rfloor$ and $r = A - q^2$, with $0 \le r \le 2q$. The digits appended in line L6 are the $n$ base $\beta$ digits of $q$, most significant first.

*Proof.* After $n$ passes the invariant gives $q = \lfloor \sqrt{P_n} \rfloor = \lfloor \sqrt A \rfloor$ and $r = A - q^2$. Each pass replaces $q$ by $q\beta + x$ with $0 \le x < \beta$, so the values $x$ in order are the digits of $q$, and $q < \beta^n$ because $A < \beta^{2n}$. $\blacksquare$
