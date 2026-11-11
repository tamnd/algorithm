---
title: In uABS, D inverts C, the decoder returns the message, and the state grows by at most the ideal length plus a constant
proves: [correctness, termination, length]
status: full
---

Notation. The probability of a 1 is $p$ with $0 < p < 1$, and $q = 1 - p$. For a state $y \in \mathbb{N} = \{0, 1, 2, \ldots\}$ let $s(y) = \lceil (y+1) p \rceil - \lceil y p \rceil$, the symbol of $y$ (line L3). For $y \in \mathbb{N}$ let $N_1(y) = \lceil y p \rceil$ and $N_0(y) = y - \lceil y p \rceil = \lfloor y q \rfloor$. The second form of $N_0$ holds because $y - \lceil yp \rceil = \lfloor y - yp \rfloor$.

**Lemma 1 (counting).** $s(y) \in \{0, 1\}$, and $N_b(y)$ is the number of states $z < y$ with $s(z) = b$, for $b \in \{0, 1\}$.

*Proof.* For a real $a$ and $0 < p < 1$, $\lceil a + p \rceil - \lceil a \rceil \in \{0, 1\}$, so $s(y) \in \{0, 1\}$. The sum $\sum_{z < y} s(z)$ telescopes to $\lceil yp \rceil - \lceil 0 \rceil = N_1(y)$, which counts the states with symbol 1. The other $y - N_1(y) = N_0(y)$ states below $y$ have symbol 0. $\square$

So $D(y) = (s(y), N_{s(y)}(y))$ of lines L3 to L5 gives the symbol of $y$ and the rank of $y$ among the states with the same symbol, counted from 0.

**Lemma 2 (C finds the state of a given rank).** For each $x \in \mathbb{N}$ and $s \in \{0, 1\}$, the state $y = C(s, x)$ of lines L1 and L2 has $s(y) = s$ and $N_s(y) = x$.

*Proof.* Take $s = 1$ and $y = \lfloor x/p \rfloor$. Then $y \le x/p$, so $yp \le x$ and $\lceil yp \rceil \le x$. Also $y > x/p - 1$, so $(y+1) p > x$, and since $x$ is an integer, $\lceil (y+1) p \rceil \ge x + 1$. The difference of the two ceilings is at most 1 by Lemma 1, so $\lceil yp \rceil = x$ and $\lceil (y+1)p \rceil = x + 1$. That is $N_1(y) = x$ and $s(y) = 1$.

Take $s = 0$ and $y = \lceil (x+1)/q \rceil - 1$. Then $y + 1 \ge (x+1)/q$, so $\lfloor (y+1) q \rfloor \ge x + 1$. Also $y < (x+1)/q$, so $yq < x + 1$ and $\lfloor yq \rfloor \le x$. Now $N_0(y+1) - N_0(y) = 1 - s(y) \le 1$, so $\lfloor yq \rfloor = x$ and $\lfloor (y+1) q \rfloor = x + 1$. That is $N_0(y) = x$ and $s(y) = 0$. $\square$

**Theorem 1 (D inverts C).** $D(C(s, x)) = (s, x)$ for each $s$ and $x$. Each symbol has infinitely many states, and $D$ is a bijection from $\mathbb{N}$ onto $\{0, 1\} \times \mathbb{N}$ with inverse $C$.

*Proof.* The first claim is Lemma 2 with the reading of $D$ after Lemma 1. Since $N_1(y) = \lceil yp \rceil$ and $N_0(y) = \lfloor yq \rfloor$ grow without bound, each symbol has infinitely many states, so the rank of a state among the states of its symbol takes each value in $\mathbb{N}$ exactly once. So $D$ is a bijection, and $C$ is its inverse by the first claim. $\square$

**Theorem 2 (correctness).** For each message $s_1 \ldots s_n$ and each start state $x_0$, DECODE applied to the output of ENCODE returns $s_1 \ldots s_n$, and its last state is $x_0$.

*Proof.* Let $y_n = x_0$ and $y_{i-1} = C(s_i, y_i)$ for $i = n, n-1, \ldots, 1$. Lines L6 to L8 compute these states in this order and return $y_0$. DECODE computes $D(y_0) = (s_1, y_1)$ by Theorem 1, then $D(y_1) = (s_2, y_2)$, and so on. After $n$ steps it has output $s_1, \ldots, s_n$ and holds $y_n = x_0$, which line L10 checks. $\square$

**Theorem 3 (length).** Let $p_1 = p$, $p_0 = q$, and let $X$ be the output of ENCODE. Then
$$\lg(X + 1) \le \lg(x_0 + 1) + \sum_{i=1}^{n} \lg \frac{1}{p_{s_i}} + \frac{q}{p \,(x_0 + 1) \ln 2}.$$

*Proof.* Let $t = x + 1$ before a step and $t' = y + 1$ after it, with $y = C(s, x)$. If $s = 1$, Lemma 2 gives $\lceil (y+1) p \rceil = x + 1$, so $(y+1)p \le x + 1$ and $t' \le t/p$. Also $y = \lfloor x/p \rfloor \ge x$, so $t' \ge t$. If $s = 0$, then $y < (x+1)/q$ and $y$ is an integer, so $y \le \lceil (x+1)/q \rceil - 1 < (x+1)/q$, and $t' < t/q + 1 = (t/q)(1 + q/t)$. Also $y + 1 \ge (x+1)/q$, so $t' \ge t/q$. Taking logarithms and $\lg(1 + z) \le z / \ln 2$,
$$\lg t' \le \lg t + \lg \frac{1}{p_s} + [s = 0]\, \frac{q}{t \ln 2}.$$
The value of $t$ never goes down, and each step with $s = 0$ multiplies it by at least $1/q$. So before the $j$-th step with $s = 0$, $t \ge (x_0 + 1) q^{-(j-1)}$, and the extra terms sum to at most $\frac{q}{(x_0 + 1) \ln 2} \sum_{j \ge 1} q^{j-1} = \frac{q}{p (x_0 + 1) \ln 2}$. Adding the steps gives the bound. $\square$

The output written in binary has $\lfloor \lg X \rfloor + 1 \le \lg(X + 1) + 1$ bits.

**Termination.** ENCODE and DECODE make $n$ steps each. Each step is a constant number of operations on integers and fractions. $\blacksquare$
