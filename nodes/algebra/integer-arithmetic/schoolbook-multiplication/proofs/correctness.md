---
title: Schoolbook multiplication computes the exact product in m + n limbs
proves: [correctness, termination]
status: full
---

Let $\beta = 2^w$, let $a = [a_0, \ldots, a_{m-1}]$ and $b = [b_0, \ldots, b_{n-1}]$ be arrays of limbs ($0 \le a_i, b_j \le \beta - 1$), and let $A = \sum_i a_i \beta^i$ and $B = \sum_j b_j \beta^j$. For an array $c$ of $m + n$ entries write $V(c) = \sum_{k=0}^{m+n-1} c_k \beta^k$, and $A_i = \sum_{i' < i} a_{i'}\beta^{i'}$, so $A_0 = 0$ and $A_m = A$.

**Theorem.** SCHOOLBOOK-MUL$(a, b)$ terminates and returns an array $c$ of $m + n$ limbs, each in $[0, \beta - 1]$, with $V(c) = AB$.

*Proof.* Both loops have fixed bounds, so the procedure terminates after $mn$ runs of the inner body. We prove an invariant of the outer loop.

> **(O)** Before row $i$ (that is, before line L3 with this $i$), each $c_k$ is a limb, $c_k = 0$ for each $k \ge i + n$, and $V(c) = A_i \cdot B$.

*Initialization.* Line L1 sets all $c_k = 0$, so $V(c) = 0 = A_0 B$, and every $c_k$ is 0.

*Maintenance.* Fix $i$ with $0 \le i < m$ and assume (O). Let $c^{(0)}$ be the array before row $i$. For the inner loop we prove:

> **(I)** Before step $j$ of the inner loop ($0 \le j \le n$), $0 \le \text{carry} \le \beta - 1$, the entries $c_{i}, \ldots, c_{i+j-1}$ are limbs, the other entries are those of $c^{(0)}$, and
> $$\sum_{k=i}^{i+j-1} c_k \beta^{k} + \text{carry}\cdot\beta^{i+j} = \sum_{k=i}^{i+j-1} c^{(0)}_k \beta^k + a_i \Big(\sum_{j' < j} b_{j'} \beta^{j'}\Big) \beta^i .$$

For $j = 0$, line L3 sets carry to 0 and both sides are 0. In step $j$, line L5 forms $t = c^{(0)}_{i+j} + a_i b_j + \text{carry}$; the entry $c_{i+j}$ is still the old one by (I). All three terms are nonnegative, and $t \le (\beta - 1) + (\beta - 1)^2 + (\beta - 1) = \beta^2 - 1$. Lines L6 and L7 write $t = c_{i+j} + \text{carry}' \beta$ with $c_{i+j} = t \bmod \beta \in [0, \beta - 1]$ and $\text{carry}' = \lfloor t / \beta \rfloor \le \lfloor (\beta^2 - 1)/\beta \rfloor = \beta - 1$. So

$$c_{i+j}\beta^{i+j} + \text{carry}'\beta^{i+j+1} = t\,\beta^{i+j} = c^{(0)}_{i+j}\beta^{i+j} + \text{carry}\cdot\beta^{i+j} + a_i b_j \beta^{i+j} .$$

Adding this to (I) for $j$ gives (I) for $j + 1$.

After the inner loop, (I) with $j = n$ holds. Line L8 stores carry in $c_{i+n}$. By (O), $c^{(0)}_{i+n} = 0$, so this store adds $\text{carry}\cdot\beta^{i+n}$ to $V(c)$ and replaces nothing. Hence, with (I) for $j = n$, the new array satisfies

$$V(c) = V(c^{(0)}) + a_i B \beta^i = A_i B + a_i \beta^i B = A_{i+1} B .$$

Each entry is a limb: the entries $c_i, \ldots, c_{i+n-1}$ by (I), $c_{i+n} = \text{carry} \le \beta - 1$, and the others are unchanged. The entries with index $k \ge i + 1 + n$ were not written in row $i$, so they are still 0. Thus (O) holds for $i + 1$.

*Termination.* For $i = m$, (O) gives $V(c) = A_m B = AB$, with every entry a limb. Line L9 returns this array, of $m + n$ limbs. $\blacksquare$

**Remark (no row writes a fresh position twice).** The maintenance step uses $c^{(0)}_{i+n} = 0$. This is the second part of (O): row $i' < i$ writes only positions $i', \ldots, i' + n$, all below $i + n$.

**Remark (signs).** For signed inputs, $AB = \operatorname{sign}(A)\operatorname{sign}(B)\,|A|\,|B|$, so multiplying the magnitudes with this procedure and setting the sign by the product of the signs is correct; a zero product is given the sign $+$.
