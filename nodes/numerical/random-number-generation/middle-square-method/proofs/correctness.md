---
title: The middle-square step computes the middle digits, and small values decay to zero
proves: [correctness]
status: full
---

Fix a base $b \ge 2$ and an even number of digits $n \ge 2$, and put $h = n/2$. The state space is $S = \{0, 1, \ldots, b^n - 1\}$ and the step is $f(x) = \lfloor x^2 / b^h \rfloor \bmod b^n$.

**Lemma 1 (the step).** For $x \in S$, write $x^2$ with exactly $2n$ digits in base $b$, with leading zeros: $x^2 = \sum_{j=0}^{2n-1} d_j b^j$. Then lines L1 and L2 return the number with digits $d_{3h-1} \ldots d_h$, the middle $n$ digits.

*Proof.* Since $x \le b^n - 1$, $x^2 < b^{2n}$, so $2n$ digits suffice. Division by $b^h$ with the floor removes the $h$ low digits: $\lfloor x^2 / b^h \rfloor = \sum_{j \ge h} d_j b^{j - h}$. The remainder modulo $b^n$ keeps the $n$ low digits of that number, which are $d_h, \ldots, d_{h+n-1} = d_{3h-1}$. The $h$ digits above them are dropped. $\square$

By induction, the generator returns $x_1 = f(x_0)$, $x_2 = f(x_1)$, and so on, and each value is in $S$. Because $S$ is finite, the sequence is eventually periodic with tail $\mu$ and period $\rho$, and $\mu + \rho \le b^n$ (see the [period](/generator-period/) page).

**Lemma 2 (decay of small values).** If $1 \le x < b^h$, then $f(x) < x$. Hence a sequence that reaches a value below $b^h$ decreases strictly until it reaches 0, in fewer than $b^h$ further steps, and then stays at 0.

*Proof.* For $1 \le x < b^h$ we have $x^2 < x \cdot b^h$, so $\lfloor x^2 / b^h \rfloor \le x^2 / b^h < x$. Also $x^2 < b^{2h} = b^n$, so $\lfloor x^2/b^h \rfloor < b^n$ and the reduction modulo $b^n$ changes nothing. So $f(x) < x$. A strictly decreasing sequence of nonnegative integers that starts below $b^h$ reaches 0 within $b^h - 1$ steps, and $f(0) = 0$. $\square$

**Lemma 3 (other fixed points).** $f(b^h) = b^h$. In base 10 with $n = 4$, $f(x) = x$ also for $x = 2500$, $3792$ and $7600$.

*Proof.* $(b^h)^2 / b^h = b^h < b^n$. For the three numbers, $2500^2 = 6250000$, whose middle four digits of $06250000$ are $2500$; $3792^2 = 14379264$, with middle digits $3792$; $7600^2 = 57760000$, with middle digits $7600$. $\square$

These lemmas explain the main defect: the state can fall into 0 or into a short cycle, and nothing in the method prevents it. No theorem gives a lower bound on the period for any seed; the cycle structure for a given $b$ and $n$ is known only by exhaustive computation. $\blacksquare$
