---
title: Binary exponentiation returns x^e mod m
proves: [correctness, termination, multiplications.worst]
status: full
---

**Claim.** Let $x$ be an integer, $e_0 \ge 0$ an integer and $m \ge 1$ an integer. BINARY-EXP$(x, e_0, m)$ stops after $\lfloor \lg e_0 \rfloor + 1$ passes of the loop when $e_0 \ge 1$, and after none when $e_0 = 0$. It returns the integer $r$ with $0 \le r < m$ and $r \equiv x^{e_0} \pmod m$. It makes $\lfloor \lg e_0 \rfloor$ squarings and $\nu(e_0)$ multiplications into $r$, where $\nu(e_0)$ is the number of digits $1$ in the binary form of $e_0$.

**Setup.** We use the rules of [congruences](/congruence/): if $a \equiv a'$ and $c \equiv c' \pmod m$, then $ac \equiv a'c' \pmod m$, and $a \bmod m \equiv a$ with $0 \le a \bmod m < m$. Write $r_j, b_j, e_j$ for the values of $r, b, e$ at the start of pass $j + 1$ (so $r_0 = 1 \bmod m$, $b_0 = x \bmod m$, and $e_0$ is the input).

**Invariant.** At the start of each pass, and at the exit of the loop:

> **(I)** $r \cdot b^{e} \equiv x^{e_0} \pmod m$, and $0 \le r < m$ and $0 \le b < m$.

**Step 1: initialization.** After lines L1 and L2, $r = 1 \bmod m \equiv 1$ and $b = x \bmod m \equiv x$, so $r b^{e_0} \equiv 1 \cdot x^{e_0}$. Both values are results of a reduction modulo $m$, so they lie in $0$ to $m - 1$. This covers $m = 1$, where $r = b = 0$; then each integer is congruent to $0$ and (I) holds trivially.

**Step 2: maintenance.** Assume (I) at the start of a pass, with $e \ge 1$. Write $e = 2q + d$ with $q = \lfloor e/2 \rfloor$ and $d = e \bmod 2 \in \{0, 1\}$. Then $b^{e} = b^{d} \cdot (b^2)^{q}$.

- Line L4 sets $r' = r b \bmod m$ if $d = 1$ and leaves $r' = r$ if $d = 0$. In both cases $r' \equiv r b^{d}$ and $0 \le r' < m$.
- Line L5 sets $e' = q$.
- If $q \ge 1$, line L6 sets $b' = b^2 \bmod m \equiv b^2$, with $0 \le b' < m$. Then $r' b'^{e'} \equiv r b^{d} (b^2)^{q} = r b^{e} \equiv x^{e_0}$.
- If $q = 0$, line L6 leaves $b' = b$. Then $b'^{e'} = 1 = (b^2)^0$, so again $r' b'^{e'} = r' \equiv r b^{d} = r b^{d} (b^2)^{q} = r b^{e} \equiv x^{e_0}$.

So (I) holds at the start of the next pass.

**Step 3: termination.** In each pass $e' = \lfloor e/2 \rfloor$. For $e \ge 1$ with $L$ binary digits, $\lfloor e/2 \rfloor$ has $L - 1$ binary digits (and is $0$ when $L = 1$). So the number of binary digits drops by exactly $1$ in each pass, and the loop stops after exactly $L = \lfloor \lg e_0 \rfloor + 1$ passes when $e_0 \ge 1$. When $e_0 = 0$, the test of line L3 fails at once.

**Step 4: the result.** At exit $e = 0$, so (I) gives $r = r \cdot b^0 \equiv x^{e_0} \pmod m$ with $0 \le r < m$. This $r$ is unique, because two integers in $0$ to $m - 1$ that are congruent modulo $m$ are equal. Line L7 returns it.

**Step 5: the count of multiplications.** In pass $j + 1$ (for $j = 0, 1, \ldots, L - 1$), the value of $e$ is $\lfloor e_0 / 2^j \rfloor$, and its lowest digit is digit $j$ of $e_0$. Line L4 multiplies exactly when this digit is $1$, so it runs $\nu(e_0)$ times in total. Line L6 squares exactly when the new $e$ is non-zero, that is in each pass except the last, so it runs $L - 1 = \lfloor \lg e_0 \rfloor$ times. $\blacksquare$

**The count is at most $2 \lfloor \lg e_0 \rfloor + 1$.** Since $\nu(e_0) \le L = \lfloor \lg e_0 \rfloor + 1$, the total $\lfloor \lg e_0 \rfloor + \nu(e_0)$ is at most $2 \lfloor \lg e_0 \rfloor + 1$, with equality exactly when all $L$ digits are $1$, that is $e_0 = 2^L - 1$.
