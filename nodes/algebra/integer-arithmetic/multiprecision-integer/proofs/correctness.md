---
title: The operations on multiprecision integers are exact and keep the representation normalized
proves: [correctness]
status: full
---

We write $\beta = 2^w$, and for a list of limbs $a$ we write $\operatorname{mag}(a) = \sum_{i=0}^{|a|-1} a_i \beta^i$. A pair $(s, a)$ is *normalized* when it meets (N): $a_{|a|-1} \ne 0$ if $|a| > 0$, and $s = +$ if $|a| = 0$. A list $c$ with $c_{|c|-1} \ne 0$ or $|c| = 0$ is a *normalized list*.

**Fact 1 (length and size).** If $a$ is a normalized list with $|a| = k \ge 1$, then $\beta^{k-1} \le \operatorname{mag}(a) \le \beta^k - 1$. *Proof.* The top term is at least $\beta^{k-1}$ and the other terms are nonnegative. Each limb is at most $\beta - 1$, so $\operatorname{mag}(a) \le (\beta - 1)\sum_{i<k} \beta^i = \beta^k - 1$. $\square$

**Lemma 1 (CMP-MAG).** For normalized lists $a$ and $b$, CMP-MAG$(a, b)$ returns the sign of $\operatorname{mag}(a) - \operatorname{mag}(b)$.

*Proof.* If $|a| > |b|$, then $|a| \ge 1$ and, by Fact 1, $\operatorname{mag}(a) \ge \beta^{|a|-1} \ge \beta^{|b|} > \operatorname{mag}(b)$; the empty list $b$ has magnitude $0 < \operatorname{mag}(a)$ too. So line C1 is right, and the case $|a| < |b|$ is symmetric. Let $|a| = |b| = k$. If $a = b$, the loop of lines C2 and C3 finds no difference and line C4 returns 0. Otherwise let $i$ be the largest index with $a_i \ne b_i$; the loop finds this $i$ first, because it runs down from $k - 1$. Say $a_i > b_i$, so $a_i - b_i \ge 1$. Then

$$\operatorname{mag}(a) - \operatorname{mag}(b) = (a_i - b_i)\beta^i + \sum_{j<i} (a_j - b_j)\beta^j \ge \beta^i - (\beta - 1)\sum_{j<i}\beta^j = \beta^i - (\beta^i - 1) = 1 ,$$

and line C3 returns 1. The case $a_i < b_i$ is symmetric. $\square$

**Lemma 2 (ADD-MAG).** For lists $a$ and $b$ of limbs with $m = |a| \ge |b| = n$, ADD-MAG returns a list $c$ of limbs with $\operatorname{mag}(c) = \operatorname{mag}(a) + \operatorname{mag}(b)$. If $a$ is a normalized list, so is $c$.

*Proof.* Write $b_i = 0$ for $i \ge n$. We prove the invariant

> **(A)** at the start of step $i$ of the loop of line L8, $c_0, \ldots, c_{i-1}$ are limbs, $\text{carry} \in \{0, 1\}$, and $\sum_{j<i} c_j \beta^j + \text{carry} \cdot \beta^i = \sum_{j<i} (a_j + b_j)\beta^j$.

*Initialization.* For $i = 0$, line L7 sets carry to 0, and both sides are 0.

*Maintenance.* In step $i$, line L9 sets $t = a_i + b_i + \text{carry}$, so $0 \le t \le 2(\beta - 1) + 1 = 2\beta - 1$. Line L10 writes $t = c_i + \text{carry}' \beta$ with $\text{carry}' \in \{0, 1\}$ and $0 \le c_i < \beta$: if $t \ge \beta$ then $c_i = t - \beta \le \beta - 1$, else $c_i = t$. Then

$$\sum_{j \le i} c_j \beta^j + \text{carry}' \beta^{i+1} = \sum_{j<i} c_j\beta^j + t \beta^i = \sum_{j<i} c_j\beta^j + \text{carry}\cdot\beta^i + (a_i + b_i)\beta^i ,$$

which by (A) is $\sum_{j \le i} (a_j + b_j) \beta^j$. So (A) holds for $i + 1$.

*Termination.* The loop runs $m$ times. At its end, (A) for $i = m$ says $\sum_{j<m} c_j\beta^j + \text{carry}\cdot \beta^m = \operatorname{mag}(a) + \operatorname{mag}(b)$. Line L11 appends the limb 1 exactly when carry is 1, so $\operatorname{mag}(c) = \operatorname{mag}(a) + \operatorname{mag}(b)$.

*Normalized.* If carry is 1, the top limb of $c$ is 1. If carry is 0 and $m \ge 1$, then $\operatorname{mag}(c) \ge \operatorname{mag}(a) \ge \beta^{m-1}$ by Fact 1, while $\sum_{j < m-1} c_j \beta^j \le \beta^{m-1} - 1$; so $c_{m-1} \ne 0$. If $m = 0$, then $c$ is empty. $\square$

**Lemma 3 (SUB-MAG).** For lists $a$ and $b$ of limbs with $m = |a| \ge |b| = n$ and $\operatorname{mag}(a) \ge \operatorname{mag}(b)$, SUB-MAG returns a normalized list $c$ with $\operatorname{mag}(c) = \operatorname{mag}(a) - \operatorname{mag}(b)$.

*Proof.* Again let $b_i = 0$ for $i \ge n$. The invariant of the loop of line L14 is

> **(S)** at the start of step $i$, $c_0, \ldots, c_{i-1}$ are limbs, $\text{borrow} \in \{0, 1\}$, and $\sum_{j<i} c_j\beta^j - \text{borrow}\cdot\beta^i = \sum_{j<i}(a_j - b_j)\beta^j$.

*Initialization.* Line L13 sets borrow to 0; both sides are 0 for $i = 0$.

*Maintenance.* Line L15 gives $t = a_i - b_i - \text{borrow}$, so $-\beta \le t \le \beta - 1$. Line L16 writes $t = c_i - \text{borrow}'\beta$ with $\text{borrow}' \in \{0, 1\}$ and $0 \le c_i < \beta$: if $t < 0$ then $c_i = t + \beta \in [0, \beta - 1]$, else $c_i = t$. The same computation as in Lemma 2, with $-\text{borrow}$ in place of carry, gives (S) for $i + 1$.

*Termination.* After $m$ steps, $\operatorname{mag}(c) - \text{borrow}\cdot\beta^m = \operatorname{mag}(a) - \operatorname{mag}(b) \ge 0$. Since $\operatorname{mag}(c) \le \beta^m - 1 < \beta^m$, the borrow must be 0, and $\operatorname{mag}(c) = \operatorname{mag}(a) - \operatorname{mag}(b)$. Line L17 removes only zero limbs at the top, which do not change $\operatorname{mag}(c)$, and it stops with an empty list or a nonzero top limb, so $c$ is normalized. $\square$

**Theorem (ADD).** For normalized pairs $x = (s, a)$ and $y = (t, b)$, ADD$(x, y)$ returns a normalized pair with the value $\operatorname{val}(x) + \operatorname{val}(y)$.

*Proof.* Write $\sigma(+) = 1$ and $\sigma(-) = -1$, so $\operatorname{val}(x) = \sigma(s)\operatorname{mag}(a)$. ADD-MAG and SUB-MAG are called with the longer list first: ADD-MAG swaps its arguments when needed, and SUB-MAG is called only after CMP-MAG has shown that its first argument has the larger or equal magnitude, which by Fact 1 for normalized lists means at least as many limbs.

*Case $s = t$.* Line L2 returns $(s, c)$ with $\operatorname{mag}(c) = \operatorname{mag}(a) + \operatorname{mag}(b)$ by Lemma 2, so the value is $\sigma(s)(\operatorname{mag}(a) + \operatorname{mag}(b)) = \operatorname{val}(x) + \operatorname{val}(y)$. The longer of $a$ and $b$ is a normalized list, so $c$ is a normalized list by Lemma 2. If $c$ is empty, then $a$ and $b$ are both empty, so $s = t = +$ by (N) for $x$, and the pair is normalized.

*Case $s \ne t$.* Then $\operatorname{val}(x) + \operatorname{val}(y) = \sigma(s)(\operatorname{mag}(a) - \operatorname{mag}(b))$. By Lemma 1, line L3 gets the sign $c$ of $\operatorname{mag}(a) - \operatorname{mag}(b)$. If $c = 0$, the sum is 0, and line L4 returns $(+, [\,])$, which is normalized and has the value 0. If $c > 0$, line L5 returns $(s, d)$ with $\operatorname{mag}(d) = \operatorname{mag}(a) - \operatorname{mag}(b) > 0$ by Lemma 3; $d$ is a normalized list and is not empty, so the pair is normalized, and its value is $\sigma(s)(\operatorname{mag}(a) - \operatorname{mag}(b))$, the sum. If $c < 0$, line L6 returns $(t, d)$ with $\operatorname{mag}(d) = \operatorname{mag}(b) - \operatorname{mag}(a) > 0$, and $\sigma(t)(\operatorname{mag}(b) - \operatorname{mag}(a)) = \sigma(s)(\operatorname{mag}(a) - \operatorname{mag}(b))$ since $\sigma(t) = -\sigma(s)$. $\square$

**Subtraction and negation.** Negation maps $(s, a)$ to $(\bar s, a)$ for $a$ nonempty and keeps $(+, [\,])$; the result is normalized and has the value $-\operatorname{val}(x)$. Then SUB$(x, y)$ = ADD$(x, -y)$ is correct by the theorem.

**Lemma 4 (MUL).** For normalized pairs, MUL returns a normalized pair with the value $\operatorname{val}(x)\operatorname{val}(y)$.

*Proof.* If $m = 0$ or $n = 0$ the product is 0, and line M1 returns $(+, [\,])$. Otherwise the [schoolbook multiplication](/schoolbook-multiplication/) proof shows that after lines M2 to M7 the list $c$ of $m + n$ limbs has $\operatorname{mag}(c) = \operatorname{mag}(a)\operatorname{mag}(b)$. By Fact 1, $\operatorname{mag}(a)\operatorname{mag}(b) \ge \beta^{m-1}\beta^{n-1} = \beta^{m+n-2}$, so the limbs $c_{m+n-2}$ and $c_{m+n-1}$ are not both zero: if both were zero, $\operatorname{mag}(c) \le \beta^{m+n-2} - 1$. Hence removing one zero top limb at line M8 leaves a normalized nonempty list. The sign is $+$ exactly when the signs agree, and $\sigma(s)\sigma(t)$ is the sign of the product. $\square$

**Lemma 5 (DIV-LIMB).** For a normalized pair $(s, a)$ and a limb $0 < d < \beta$, DIV-LIMB returns a normalized pair $(s', q)$ and an $r$ with $\operatorname{mag}(a) = \operatorname{mag}(q)\, d + r$ and $0 \le r < d$.

*Proof.* Let $k = |a|$ and $P_i = \sum_{j \ge i} a_j \beta^{j-i}$, the number formed by the limbs $a_{k-1}, \ldots, a_i$; so $P_k = 0$, $P_i = P_{i+1}\beta + a_i$ and $P_0 = \operatorname{mag}(a)$. The invariant before the step with index $i$ (from $k - 1$ down) is $P_{i+1} = \sum_{j > i} q_j \beta^{j-i-1} \cdot d + r$ with $0 \le r < d$. It holds at the start with $r = 0$ and no digits. In the step, $u = r\beta + a_i$ satisfies $0 \le u \le (d - 1)\beta + \beta - 1 < d\beta$, so $q_i = \lfloor u/d \rfloor < \beta$ is a limb, and $u = q_i d + r'$ with $0 \le r' < d$. Then $P_i = P_{i+1}\beta + a_i = \big(\sum_{j>i} q_j \beta^{j-i}\big) d + u = \big(\sum_{j \ge i} q_j\beta^{j-i}\big) d + r'$, the invariant for $i - 1$. After the step with $i = 0$ this is the claim. Line D4 removes the zero top limbs and sets the sign to $+$ for an empty quotient, so the pair is normalized. $\blacksquare$
