---
title: The PPM reconstruction is exact for cubics away from limiting, gives monotone parabolas inside the range of the neighbors, and PPM for linear advection is conservative and TVD for Courant numbers up to 1
proves: [correctness]
status: full
---

**Setting.** The cell averages $a_j$ live on cells of width $h$. Lines L2 to L4 of the page compute the slopes

$$\delta a_j = \begin{cases}\mathrm{sgn}(\Delta_{j+1/2})\min\big(\tfrac12|a_{j+1} - a_{j-1}|, 2|\Delta_{j-1/2}|, 2|\Delta_{j+1/2}|\big) & \text{if } \Delta_{j-1/2}\Delta_{j+1/2} > 0,\\ 0 & \text{otherwise,}\end{cases}$$

with $\Delta_{j+1/2} = a_{j+1} - a_j$, the face values $a_{j+1/2} = \frac12(a_j + a_{j+1}) - \frac16(\delta a_{j+1} - \delta a_j)$, and then, in each cell, $a_L = a_{j-1/2}$ and $a_R = a_{j+1/2}$ changed by three tests:

1. if $(a_R - a_j)(a_j - a_L) \le 0$, set $a_L = a_R = a_j$;
2. else if $d\,m > d^2/6$, set $a_L = 3a_j - 2a_R$;
3. else if $d\,m < -d^2/6$, set $a_R = 3a_j - 2a_L$;

where $d = a_R - a_L$ and $m = a_j - \frac12(a_L + a_R)$. The parabola in cell $j$, with $\xi \in [0, 1]$ across the cell, is

$$P_j(\xi) = a_L + \xi\big(d + a_6(1 - \xi)\big), \qquad a_6 = 6m.$$

**Lemma 1 (mean and fourth order face values).** $\int_0^1 P_j = a_j$. If no slope is limited, that is $\delta a_j = \frac12(a_{j+1} - a_{j-1})$ for all $j$, then $a_{j+1/2} = \frac7{12}(a_j + a_{j+1}) - \frac1{12}(a_{j-1} + a_{j+2})$, and this is exact when the $a_j$ are the averages of a cubic.

*Proof.* $\int_0^1 \xi\,d\xi = \frac12$ and $\int_0^1 \xi(1 - \xi)\,d\xi = \frac16$, so the integral is $a_L + \frac d2 + m = a_j$. Inserting the central slopes gives the second formula. For the third claim, let $V$ be the primitive of the cubic, so $h a_k = V(x_{k+1/2}) - V(x_{k-1/2})$. The formula is a linear combination of the values of $V$ at five faces, and its value at the face equals $V'(x_{j+1/2})$ for $V = 1, x, \dots, x^4$ by direct computation, so it is exact for $V$ of degree 4. $\square$

The test checks the cubic case exactly in `Fraction` arithmetic on the averages of $x^3 + x$, where no slope is limited.

**Lemma 2 (face values lie between neighbors).** $a_{j+1/2}$ lies between $a_j$ and $a_{j+1}$.

*Proof.* If $\Delta_{j+1/2} = 0$, both slopes are 0, because each has a factor $\Delta_{j+1/2}$ in its sign test, and $a_{j+1/2} = a_j$. Let $\Delta = \Delta_{j+1/2} > 0$ (the other sign is the mirror image). Both $\delta a_j$ and $\delta a_{j+1}$ are zero or have the sign of $\Delta$, and both are at most $2\Delta$. So $\frac16(\delta a_{j+1} - \delta a_j) \in [-\frac13\Delta, \frac13\Delta]$ and $a_{j+1/2} \in [a_j + \frac16\Delta, a_j + \frac56\Delta]$. $\square$

**Lemma 3 (the tests give monotone parabolas).** After the three tests, $P_j$ is monotone on $[0, 1]$, $a_j$ lies between $a_L$ and $a_R$, and $a_L$ and $a_R$ lie between the values they had before the tests and $a_j$.

*Proof.* $P'_j(\xi) = d + a_6(1 - 2\xi)$ is linear, so $P_j$ is monotone on $[0, 1]$ if and only if $P'_j(0) = d + a_6$ and $P'_j(1) = d - a_6$ do not have strict opposite signs, which holds when $|a_6| \le |d|$, that is $|m| \le |d|/6$. Test 1 gives a constant. If test 1 does not apply, $a_j$ is strictly between $a_L$ and $a_R$, so $d \ne 0$. If tests 2 and 3 do not apply, $|d\,m| \le d^2/6$, so $|m| \le |d|/6$. In test 2, the new values $a'_L = 3a_j - 2a_R$, $d' = 3(a_R - a_j)$ and $m' = \frac12(a_R - a_j)$ give $d'm' = d'^2/6$, so $|m'| = |d'|/6$ and $P_j$ is monotone. Also $a'_L$ is on the same side of $a_j$ as $a_L$, since $a_j - a'_L = 2(a_R - a_j)$ has the sign of $a_j - a_L$, and $a'_L$ lies between $a_L$ and $a_j$, because $d\,m > d^2/6$ is the same as $a'_L - a_L$ having the sign of $d$. Test 3 is the mirror image. $\square$

**Corollary.** Every value of $P_j$ lies between the smallest and the largest of $a_{j-1}, a_j, a_{j+1}$. The test `test_parabolas_are_monotone_and_bounded` checks this at 17 points in every cell for random data.

**Lemma 4 (the reconstruction keeps the total variation).** On a periodic grid, let $p$ be the function equal to $P_j$ on cell $j$. Then $TV(p) = \sum_j |a_{j+1} - a_j|$.

*Proof.* Write $a_{R,j}$ and $a_{L,j+1}$ for the values on the two sides of the face $j + 1/2$ after the tests. Suppose $a_j \le a_{j+1}$. By Lemma 2 the face value $a_{j+1/2}$ is in $[a_j, a_{j+1}]$. The tests in cell $j$ move $a_{R,j}$ from $a_{j+1/2}$ toward $a_j$ (Lemma 3, or test 1), and the tests in cell $j + 1$ move $a_{L,j+1}$ from $a_{j+1/2}$ toward $a_{j+1}$. So $a_j \le a_{R,j} \le a_{j+1/2} \le a_{L,j+1} \le a_{j+1}$. The case $a_j > a_{j+1}$ is the mirror image. In each cell, $P_j$ is monotone from $a_{L,j}$ to $a_{R,j}$ and passes through the level $a_j$, which lies between them. So the function $p$, read from left to right, visits $a_j, a_{R,j}, a_{L,j+1}, a_{j+1}$ monotonically between every two neighbor averages, and its variation between the levels $a_j$ and $a_{j+1}$ is exactly $|a_{j+1} - a_j|$. Summing over $j$ gives the claim. $\square$

**Theorem 1 (PPM for linear advection).** For $u_t + cu_x = 0$ with $c > 0$, $\nu = c\Delta t/h \in [0, 1]$ and line L5, the step of line L6 sets $a_j^{n+1}$ to the average over cell $j$ of $p$ moved right by $\nu h$. On a periodic grid the step is conservative, $TV(a^{n+1}) \le TV(a^n)$, and every new value lies between the smallest and the largest old value. At $\nu = 1$ the step is the exact shift $a_j^{n+1} = a_{j-1}^n$.

*Proof.* The value of line L5 is $\frac1\nu\int_{1-\nu}^1 P_j$, by direct integration of the parabola; the test compares it with Simpson's rule, which is exact for parabolas, in `Fraction` arithmetic. Since $\nu \le 1$, the part of $p$ that crosses the face $j + 1/2$ in the step comes only from cell $j$, so line L6 computes the average over cell $j$ of the moved function exactly. The fluxes telescope, so the sum is kept. For the total variation, let $q$ be the moved function. Then

$$\sum_j |a^{n+1}_{j+1} - a^{n+1}_j| = \sum_j \Big|\frac1h\int_0^h \big(q(x_{j+1/2} + s) - q(x_{j-1/2} + s)\big)\,ds\Big| \le \frac1h\int_0^h \sum_j |q(x_{j+1/2} + s) - q(x_{j-1/2} + s)|\,ds \le TV(q),$$

and $TV(q) = TV(p) = TV(a^n)$ by Lemma 4. The bounds follow from the Corollary, because each new value is an average of values of $p$. At $\nu = 1$ the flux is $\int_0^1 P_j = a_j$ by Lemma 1, so $a_j^{n+1} = a_j - (a_j - a_{j-1})$. $\square$

The tests check Theorem 1 on a square wave at $\nu = 0.3, 0.5, 0.9, 1$ and on 100 random data sets, and check conservation exactly in `Fraction` arithmetic.

**What is not proved here.** The order of accuracy is measured, not proved: on a sine wave for advection the $L^1$ orders are 2.27, 2.43 and 2.38, above 2 because the face values are fourth order, and below 3 because test 1 flattens the parabolas at extrema. For the Euler equations the page uses the reconstruction in a method of lines with the HLL flux and SSP RK3, without the characteristic tracing, contact steepening and flattening of the full gas dynamics scheme. No TVD or positivity property is proved for that case.
