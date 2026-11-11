---
title: The integer arithmetic decoder returns the message, and the code has at most the ideal length plus 2 bits plus a small loss per symbol
proves: [correctness, termination, length]
status: full
---

Notation. The registers have $b$ bits, $Q = 2^{b-2}$, $H = 2Q$. Each symbol $x_i$ has the counts $c_{lo} < c_{hi} \le T_i$ from the model, with $f_i = c_{hi} - c_{lo}$ and $p_i = f_i / T_i$, and the model guarantees $T_i \le T_{\max} \le Q$. A *step* of the loop of lines L7 to L12 is one pass that does not exit: an E1 step (line L8), an E2 step (line L9) or an E3 step (line L10). The state interval is $[low, high + 1)$, scaled to $[low/2^b, (high+1)/2^b) \subseteq [0, 1)$. We write $C$ for a real number in $[0, 1)$ that we read as a binary fraction $0.c_1 c_2 c_3 \ldots$, and $u$ for the string of bits that EMIT has written so far.

**Lemma 1 (the registers stay sound).** At line L4, $low < high$ and $r = high - low + 1 > Q$. After lines L5 and L6, $low \le high$.

*Proof.* At the start $r = 2^b$. The loop of line L7 exits only when none of the three tests holds, so $low < H \le high$, and $low < Q$ or $high \ge 3Q$. In both cases $high - low + 1 > Q$. Each step maps $low$ and $high$ by $y \mapsto 2(y - a)$ and $y \mapsto 2(y - a) + 1$ with $a \in \{0, Q, H\}$, and the test before it shows that the interval lies in $[a, a + H)$, so the new values stay in $[0, 2^b)$. For lines L5 and L6, the new width is the integer $\lfloor r c_{hi} / T \rfloor - \lfloor r c_{lo} / T \rfloor$, and it is greater than $r f / T - 1 \ge r / T - 1 > Q / T_{\max} - 1 \ge 0$. An integer greater than 0 is at least 1. $\square$

**Lemma 2 (the coordinate map).** Let $m$ be the number of pending bits. At each time, the encoder state represents the map
$$\varphi(C) = 2^m\bigl(2^{|u|} C - u\bigr) - \tfrac{2^m - 1}{2},$$
where $u$ is read as an integer. That is, the state interval in the coordinates of the original unit interval is $\varphi^{-1}\bigl([low/2^b, (high + 1)/2^b)\bigr)$.

*Proof.* At the start $u$ is empty and $m = 0$, so $\varphi(C) = C$. An E3 step changes coordinates by $y \mapsto 2y - \tfrac12$ and adds 1 to $m$: $2\varphi(C) - \tfrac12 = 2^{m+1}(2^{|u|}C - u) - \tfrac{2^{m+1} - 1}{2}$, which is the formula for $m + 1$. An E1 step changes coordinates by $y \mapsto 2y$ and appends $0\,1^m$ to $u$: $2\varphi(C) = 2^{|u| + m + 1} C - (2^{m+1} u + 2^m - 1)$, and $2^{m+1} u + 2^m - 1$ is the integer of the string $u\,0\,1^m$. An E2 step changes coordinates by $y \mapsto 2y - 1$ and appends $1\,0^m$: $2\varphi(C) - 1 = 2^{|u|+m+1} C - (2^{m+1} u + 2^m)$, which is the integer of $u\,1\,0^m$. In all three cases $m$ is 0 after an E1 or E2 step. $\square$

**Lemma 3 (nesting).** Let $I_0 \supseteq I_1 \supseteq \cdots$ be the state intervals in original coordinates, taken after each symbol. Then they are nested, and the width of $I_i$ is $\prod_{j \le i} w_j$ where $w_j = r'_j / r_j$ is the ratio of the new width to the old width at symbol $j$.

*Proof.* Lines L5 and L6 replace $[low, high + 1)$ by a subinterval, and the steps only change coordinates. By Lemma 2 a change of coordinates does not move the interval in original coordinates. A step doubles the width in scaled coordinates and doubles the scale, so the width in original coordinates changes only at lines L5 and L6, by the factor $w_j$. $\square$

**Lemma 4 (the end).** Let $w$ be the full output. Every $C$ whose binary expansion begins with $w$ lies in the last interval $I_n$.

*Proof.* At line L14 the state is after the loop, so by Lemma 1, $low < Q$ and $high \ge H$, or $low < H$ and $high \ge 3Q$. In the first case line L15 writes $0$ and $m + 1$ ones. By the algebra of Lemma 2 (one E3 change and then one E1 change), this appends exactly the bits that make $2^{|w|} C - w \in [0, 1)$ equivalent to $\varphi(C) \in [Q/2^b, H/2^b)$. The interval $[Q, H)$ is inside $[low, high + 1)$. The second case is the same with $[H, 3Q)$. A number $C$ begins with $w$ exactly when $2^{|w|} C - w \in [0, 1)$. $\square$

**Theorem 1 (correctness).** For each message $x_1 \ldots x_n$ and each adaptive model that the encoder and decoder update in the same way, DECODE returns $x_1 \ldots x_n$. This holds whatever bits follow the code, in particular for the zero padding.

*Proof.* Let $C$ be the code followed by any bits. By Lemma 4 and Lemma 3, $C \in I_i$ for each $i$. We show by induction on $i$ that before the decoder handles symbol $i + 1$, it has the same $low$, $high$ and model as the encoder, and $value = \lfloor 2^b \varphi_i(C) \rfloor$, where $\varphi_i$ is the encoder map at that time. For $i = 0$, line L17 reads the first $b$ bits, so $value = \lfloor 2^b C \rfloor$. In the step, $C \in I_i$ gives $low \le value \le high$. Let $v = value - low$, so $0 \le v < r$. For an integer $c$, $\lfloor r c / T \rfloor \le v$ holds if and only if $r c < (v + 1) T$, that is $r c \le (v+1) T - 1$, that is $c \le t$ with $t$ as in line L20. So $low + \lfloor r c_{lo}/T \rfloor \le value$ if and only if $c_{lo} \le t$, and $value \le low + \lfloor r c_{hi}/T \rfloor - 1$ if and only if $t < c_{hi}$. The symbol $x_{i+1}$ has $value$ in its subinterval, because $C \in I_{i+1}$. So line L21 finds exactly $x_{i+1}$, since the subintervals of the symbols do not overlap. Line L22 makes the same $low$ and $high$ as lines L5 and L6. The loop of line L23 tests only $low$ and $high$, so it does the same steps as the encoder. A step maps $y \mapsto 2y - a$ with $2^b a$ an integer, and $\lfloor 2^b (2y - a) \rfloor = 2 \lfloor 2^b y \rfloor - 2^b a + d$, where $d$ is the first bit of the fraction of $2^b y$. With $y = \varphi(C)$, the fraction of $2^b \varphi(C)$ is the fraction of $2^{b + k} C$ for the number $k$ of steps so far, and its first bit is the next unread bit of $C$. This is line L24. Line L25 updates the model with the same symbol. $\square$

**Theorem 2 (length).** The number of output bits is
$$L \le \sum_{i=1}^{n} \lg \frac{1}{p_i} + 2 + n \lg \frac{1}{1 - T_{\max}/Q}.$$

*Proof.* Each step adds exactly one bit to the output: an E1 or E2 step writes one bit and the pending bits, which earlier E3 steps added to $m$, and line L15 writes $m + 1$ bits after line L14 adds one. So $L = S + 2$, where $S$ is the number of steps. At symbol $j$, the new width is $r'_j > r_j f_j / T_j - 1 = (r_j f_j/T_j)(1 - T_j/(r_j f_j)) \ge (r_j f_j / T_j)(1 - T_{\max}/Q)$, by Lemma 1. So $w_j \ge p_j (1 - T_{\max}/Q)$. By Lemma 3 the width of $I_n$ in original coordinates is $\prod_j w_j$. In scaled coordinates this width is multiplied by $2^S$ and it is at most 1. So $2^S \prod_j w_j \le 1$, and $S \le \sum_j \lg(1/w_j) \le \sum_j \lg(1/p_j) + n \lg(1/(1 - T_{\max}/Q))$. $\square$

**Termination.** Each pass of the loop of line L7 that does not exit doubles $high - low + 1$, and Lemma 1 keeps this width at most $2^b$. The width is at least 1 at the start of the loop, so the loop makes at most $b$ steps for each symbol. The outer loops run $n$ times. $\blacksquare$
