---
title: LSD radix sort sorts the items and is stable
proves: [correctness, stability, termination]
status: full
---

Let $b \ge 2$ and let each key be an integer $x \ge 0$. Write $x_t = \lfloor x / b^t \rfloor \bmod b$ for the digit $t$ of $x$, and $x^{(t)} = x \bmod b^{t}$ for the value of its lowest $t$ digits. Then $x^{(t+1)} = x_t b^t + x^{(t)}$ with $0 \le x^{(t)} < b^t$. We use one fact about this split.

**Fact.** For keys $x, y$ and $t \ge 0$: $x^{(t+1)} < y^{(t+1)}$ if and only if $x_t < y_t$, or $x_t = y_t$ and $x^{(t)} < y^{(t)}$.

*Proof.* If $x_t < y_t$, then $x^{(t+1)} \le x_t b^t + b^t - 1 < (x_t + 1) b^t \le y_t b^t \le y^{(t+1)}$. If $x_t = y_t$, the two values differ by $x^{(t)} - y^{(t)}$. If $x_t > y_t$, the first case with $x$ and $y$ swapped gives $y^{(t+1)} < x^{(t+1)}$. $\square$

**Termination.** Let $m$ be the largest key (0 for an empty array). The variable $p$ starts at 1 and is multiplied by $b \ge 2$ in each pass, so after $t + 1$ passes $p = b^{t+1} \ge 2^{t+1}$. The test of line L6 is true as soon as $b^{t+1} > m$. So the loop runs for $d$ passes, where $d = 1$ if $m < b$ and otherwise $d$ is the least integer with $b^d > m$. In each case $b^d > m$, and pass $t$ (for $t = 0, \ldots, d-1$) runs with $p = b^t$, so line L4 sorts by the digit $x_t$.

**Claim.** After pass $t$, the array is sorted by $\mathrm{key}^{(t+1)}$, and items with equal $\mathrm{key}^{(t+1)}$ are in their input order.

*Proof by induction on $t$.* We say that the array before pass 0 is "after pass $-1$", and it is sorted by $\mathrm{key}^{(0)} = 0$ with all items in input order, so the claim holds for $t = -1$.

Assume the claim after pass $t - 1$, for some $t \ge 0$. Pass $t$ is a stable sort by digit $t$. Take two items $u$ and $v$ with keys $x$ and $y$, where $u$ is in front of $v$ after pass $t$. We show that $x^{(t+1)} \le y^{(t+1)}$, and that $u$ came first in the input if $x^{(t+1)} = y^{(t+1)}$.

1. If $x_t \ne y_t$: the sort by digit $t$ put $u$ first, so $x_t < y_t$, and the Fact gives $x^{(t+1)} < y^{(t+1)}$.
2. If $x_t = y_t$: the sort is stable, so $u$ was also in front of $v$ after pass $t - 1$. By the induction hypothesis $x^{(t)} \le y^{(t)}$, and so $x^{(t+1)} \le y^{(t+1)}$ by the Fact. If $x^{(t+1)} = y^{(t+1)}$, then $x^{(t)} = y^{(t)}$, and the induction hypothesis says that $u$ came first in the input.

Both cases give the claim after pass $t$. $\square$

**Theorem.** RADIX-SORT returns the items of $A$ in non-decreasing order of key, and items with equal keys are in their input order.

*Proof.* Each pass is a counting sort, which returns a permutation of its input, so the result holds the items of $A$. After the last pass $t = d - 1$, the Claim says that the array is sorted by $\mathrm{key}^{(d)}$, stably. Each key is at most $m < b^d$, so $\mathrm{key}^{(d)} = \mathrm{key}$. $\blacksquare$
