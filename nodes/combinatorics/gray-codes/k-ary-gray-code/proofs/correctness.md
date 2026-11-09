---
title: Algorithm H visits the reflected mixed-radix Gray code in order
proves: [correctness]
status: full
---

Fix radices $m_0, \ldots, m_{n-1}$, each at least 2, and let $N = m_0 \cdots m_{n-1}$ and $P_j = m_0 \cdots m_{j-1}$, so $P_0 = 1$ and $P_n = N$. Each $r$ with $0 \le r < N$ has unique mixed-radix digits $b_j(r)$, $0 \le b_j(r) < m_j$, with $r = \sum_j b_j(r) P_j$. Let $H_j(r) = \lfloor r / P_{j+1} \rfloor$, the number formed by the digits above $j$. Digit $j$ of $r$ is *full* when $b_j(r) = m_j - 1$. Let $t_j(r)$ be the largest $t \ge 0$ such that digits $j, \ldots, j + t - 1$ of $r$ are all full, with $t_n(r) = 0$.

The reflected code is $G(r) = (a_{n-1}, \ldots, a_0)$ with $a_j = b_j(r)$ if $H_j(r)$ is even and $a_j = m_j - 1 - b_j(r)$ if $H_j(r)$ is odd.

**Lemma 1 (Gray step).** Let $1 \le r < N$ and let $i = t_0(r - 1)$. Then $i < n$, and $G(r)$ differs from $G(r-1)$ only in digit $i$, where it is larger by 1 if $H_i(r-1)$ is even and smaller by 1 if it is odd. Also $H_i(r) = H_i(r - 1)$.

*Proof.* If $i = n$ then all digits of $r - 1$ are full, so $r - 1 = N - 1$, which contradicts $r < N$. So digit $i$ of $r - 1$ is not full. Adding 1 to $r - 1$ turns digits $0, \ldots, i - 1$ from $m_j - 1$ into 0, adds 1 to digit $i$, and leaves the digits above $i$ unchanged.

- For $j < i$: $r - 1 \equiv P_{j+1} - 1 \pmod{P_{j+1}}$, since its digits $0$ to $j$ are full. So $P_{j+1}$ divides $r$ and $H_j(r) = H_j(r-1) + 1$. Let $h = H_j(r-1)$. If $h$ is even, $a_j(r-1) = b_j(r-1) = m_j - 1$ and, since $h + 1$ is odd, $a_j(r) = m_j - 1 - 0 = m_j - 1$. If $h$ is odd, $a_j(r-1) = m_j - 1 - (m_j - 1) = 0$ and $a_j(r) = 0$. Either way digit $j$ of the code does not change.
- For $j = i$: the residue of $r - 1$ modulo $P_{i+1}$ is $b_i(r-1) P_i + P_i - 1$, and that of $r$ is $(b_i(r-1) + 1) P_i \le (m_i - 1) P_i < P_{i+1}$. So no carry passes digit $i$, and $H_i(r) = H_i(r-1)$. Since $b_i$ grows by 1, $a_i$ grows by 1 if $H_i$ is even and shrinks by 1 if it is odd.
- For $j > i$: $b_j$ and $H_j$ are the same for $r - 1$ and $r$, so $a_j$ is the same. $\square$

**Lemma 2 (one-to-one).** $G$ is one-to-one on $[0, N)$.

*Proof.* From $G(r)$ we recover $r$ from the top. $H_{n-1}(r) = 0$, so $b_{n-1} = a_{n-1}$. Once $b_{n-1}, \ldots, b_{j+1}$ are known, $H_j(r) = \sum_{i > j} b_i P_i / P_{j+1}$ is known, and $b_j$ is $a_j$ or $m_j - 1 - a_j$ by its parity. So $G(r)$ determines all digits of $r$. $\square$

**Invariant $I(r)$.** At the $r$-th arrival at line L4, counting from 0:

1. $a = G(r)$;
2. for $0 \le j \le n$: $f_j = j + t_j(r)$ if $j = 0$ or digit $j - 1$ of $r$ is not full, and $f_j = j$ otherwise;
3. for $0 \le j < n$: $o_j = (-1)^{H_j(r)}$ if digit $j$ of $r$ is not full, and $o_j = -(-1)^{H_j(r)}$ if it is full.

As in the binary proof, we call the first case of item 2 the *head* case.

**Lemma 3 (base).** $I(0)$ holds.

*Proof.* Line L1 sets $a = 0 = G(0)$, $f_j = j$ and $o_j = +1$, and line L2 sets $f_n = n$. All digits of 0 are 0, which is not full since $m_j \ge 2$. So every $t_j(0) = 0$, every $j$ is in the head case, and every $H_j(0) = 0$, which asks for $f_j = j$ and $o_j = +1$. $\square$

**Lemma 4 (step).** Let $0 \le r < N - 1$ and assume $I(r)$. Then the pass from line L5 does not return, and $I(r+1)$ holds at the next arrival at line L4.

*Proof.* Let $i = t_0(r)$. By item 2 with $j = 0$, line L5 reads $j = f_0 = i$. By Lemma 1 applied to $r + 1$, $i < n$, so line L6 does not return. Digit $i$ of $r$ is not full, so item 3 gives $o_i = (-1)^{H_i(r)}$, and line L7 changes $a_i$ by $+1$ if $H_i(r)$ is even and by $-1$ if it is odd. By Lemma 1 this turns $G(r)$ into $G(r+1)$, which proves item 1.

*When does line L8 succeed?* Digit $i$ of $r + 1$ is $b_i(r) + 1 \ge 1$. If $H_i$ is even then $a_i = b_i(r+1)$, which is never 0 here and is $m_i - 1$ exactly when digit $i$ of $r + 1$ is full. If $H_i$ is odd then $a_i = m_i - 1 - b_i(r+1)$, which is never $m_i - 1$ here and is 0 exactly when digit $i$ of $r + 1$ is full. So line L8 succeeds if and only if digit $i$ of $r + 1$ is full. Call this event $E$.

*Item 3.* Only $o_i$ can change.
- For $j < i$: digit $j$ of $r$ is full, digit $j$ of $r + 1$ is 0 and not full, and $H_j(r+1) = H_j(r) + 1$ by the proof of Lemma 1. The rule asks for $o_j = (-1)^{H_j(r) + 1} = -(-1)^{H_j(r)}$, which is the old value.
- For $j = i$: $H_i$ is unchanged. Without $E$, digit $i$ stays not full and $o_i$ stays $(-1)^{H_i}$. With $E$, digit $i$ becomes full and line L9 turns $o_i$ into $-(-1)^{H_i}$.
- For $j > i$: nothing changes.

*Item 2.* Line L5 sets $f_0 \leftarrow 0$. With $E$, line L10 then sets $f_i \leftarrow f_{i+1}$ and $f_{i+1} \leftarrow i + 1$, using the old $f_{i+1}$. Digits $0$ to $i - 1$ of $r + 1$ are 0, so not full.
- $j = 0$ when $i \ge 1$, or $j = 0 = i$ without $E$: $f_0 = 0$. Digit 0 of $r + 1$ is not full, so $t_0(r+1) = 0$, as required.
- $1 \le j \le i - 1$: digit $j - 1$ of $r$ is full, so the old $f_j = j$, and it does not change. In $r + 1$, digit $j - 1$ is not full and digit $j$ is not full, so the rule asks for $j + 0 = j$.
- $j = i \ge 1$ without $E$: digit $i - 1$ of $r$ is full, so the old $f_i = i$, unchanged. In $r + 1$, digit $i - 1$ is 0 and digit $i$ is not full, so the rule asks for $i$.
- $j = i + 1$ without $E$: $f_{i+1}$ does not change. Digit $i$ is not full in $r$ and in $r + 1$, so both are head cases, and $t_{i+1}$ depends only on digits $i + 1$ and higher, which agree. The value is the same.
- $j = i$ with $E$: the new $f_i$ is the old $f_{i+1}$. Digit $i$ of $r$ is not full, so $i + 1$ was a head case and the old $f_{i+1} = i + 1 + t_{i+1}(r)$. In $r + 1$, $i$ is a head case ($i = 0$, or digit $i - 1$ is 0), digit $i$ is full, and the digits above agree, so $t_i(r+1) = 1 + t_{i+1}(r)$. The rule asks for $i + t_i(r+1) = i + 1 + t_{i+1}(r)$.
- $j = i + 1$ with $E$: line L10 sets $f_{i+1} = i + 1$. Digit $i$ of $r + 1$ is full, so this is not a head case, and the rule asks for $i + 1$. This includes $i + 1 = n$.
- $j \ge i + 2$: $f_j$ does not change, digit $j - 1$ and all digits from $j$ up agree in $r$ and $r + 1$, so the rule gives the same value. $\square$

**Lemma 5 (stop).** If $I(N - 1)$ holds, the pass returns at line L6.

*Proof.* All digits of $N - 1$ are full, so $t_0(N - 1) = n$ and line L5 reads $j = f_0 = n$. $\square$

**Theorem.** REFLECTED-MIXED-RADIX visits exactly $N$ arrays, the $r$-th of which is $G(r)$. Each array with $0 \le a_j < m_j$ is visited once, two consecutive arrays differ in one digit by $\pm 1$, and each pass after line L2 does a bounded number of operations.

*Proof.* Lemma 3 and induction with Lemma 4 give $I(r)$ at the $r$-th arrival at line L4 for $0 \le r \le N - 1$, with no return before the arrival for $r = N - 1$, and Lemma 5 stops the loop there. So the visits are $G(0), \ldots, G(N-1)$. By Lemma 2 they are $N$ distinct arrays, which are all the arrays in the range, and by Lemma 1 consecutive ones differ in one digit by $\pm 1$. Lines L4 to L10 contain no loop. For $n = 0$, $N = 1$ and Lemma 5 applies at once: the empty array is visited once. $\blacksquare$
