---
title: The top-to-random shuffle has a strong uniform time and a cutoff at n ln n
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The deck has $n \ge 2$ cards; position 0 is the top. The calls of RANDOM are independent and uniform on $\{0, \ldots, n-1\}$. Let $X_t$ be the deck after $t$ moves, $P^t$ its law from a fixed start, and $\pi$ the uniform law on the $n!$ orders. The distance is $\|P^t - \pi\|_{TV} = \max_A (\pi(A) - P^t(A))$ over sets $A$ of orders.

**Termination.** The loop of line L1 makes exactly $t$ iterations, each with one removal, one call of RANDOM and one insertion. For the exact version, which stops at the time $T$ below, we show that $T$ is finite with probability 1 and $E[T] = n H_n$.

**Uniform is stationary.** One move picks $p$ and applies a fixed permutation $\rho_p$ of the positions. If $X_t$ is uniform, then for each $p$ the deck $\rho_p(X_t)$ is uniform, because $\rho_p$ is a bijection of the orders. A mixture of uniform laws is uniform.

## The strong uniform time

Let $b$ be the card at the bottom at time 0. Let $T$ be the first move in which the card taken from the top in line L2 is $b$. $T$ is a stopping time: whether $T = s$ depends only on the first $s$ moves.

**Lemma 1.** For $t \ge 0$, let $S_t$ be the set of cards below $b$ after move $t$, and let $U_t$ be the part of the deck from the top down to $b$, with $b$. On the event $\{T > t\}$, given $U_0, \ldots, U_t$ and $S_0, \ldots, S_t$, the order of the cards of $S_t$ is uniform on the $|S_t|!$ orders of $S_t$.

*Proof.* By induction on $t$. At $t = 0$, $S_0$ is empty. Assume the claim at $t$, and let move $t + 1$ happen with $T > t + 1$, so the top card $x$ is not $b$. After $x$ is removed, $b$ has $k = |S_t|$ cards below it, so $b$ is at position $n - 2 - k$ of the remaining $n - 1$ cards. Of the $n$ places for $x$, the $n - 1 - k$ places $0, \ldots, n - 2 - k$ are above $b$, and the $k + 1$ places $n - 1 - k, \ldots, n - 1$ are below $b$.

- If $p$ is above $b$, then $S_{t+1} = S_t$ and the order below $b$ does not change. The value of $p$ is independent of that order, so the order stays uniform given the new history.
- If $p$ is below $b$, then $S_{t+1} = S_t \cup \{x\}$, and given this event, $x$ goes to a uniform one of the $k + 1$ gaps in the order of $S_t$. A uniform order of $k$ cards and an independent uniform gap give a uniform order of the $k + 1$ cards, because the map (order, gap) to new order is a bijection from $k! \cdot (k+1)$ pairs onto the $(k+1)!$ orders.

In both cases the new $U_{t+1}$ and $S_{t+1}$ are functions of $U_t$, $S_t$ and $p$ only, not of the order below $b$. So the claim holds at $t + 1$. ∎

**Lemma 2.** For each $s \ge 1$, given $T = s$, the deck $X_s$ is uniform. For each $t$ and each order $\sigma$, $\Pr[X_t = \sigma, T \le t] = \Pr[T \le t] / n!$.

*Proof.* The event $\{T = s\}$ says that $b$ is on top after move $s - 1$ and $T > s - 1$. This is a function of $U_{s-1}$. Then $S_{s-1}$ holds all the other $n - 1$ cards, and by Lemma 1 their order is uniform given $\{T = s\}$. Move $s$ inserts $b$ at a uniform place among $n$, independent of that order. As in Lemma 1, a uniform order of $n - 1$ cards and a uniform gap give a uniform order of $n$ cards, so $X_s$ is uniform given $T = s$. The moves after $s$ use new random values, and uniform is stationary, so $X_t$ is uniform given $T = s$ for each $t \ge s$. Sum over $s \le t$:
$$\Pr[X_t = \sigma, T \le t] = \sum_{s \le t} \Pr[T = s] \cdot \frac{1}{n!} = \frac{\Pr[T \le t]}{n!}. \qquad ∎$$

A stopping time with this property is a [strong uniform time](/strong-uniform-time/). So the exact version, which returns $X_T$, outputs a uniform deck.

**The law of $T$.** While $b$ has $k$ cards below it and $b$ is not on top, a move puts the top card below $b$ with probability $(k + 1)/n$, independent of the past. $b$ reaches the top when $k = n - 1$, and then the next move is move $T$. So
$$T = G_1 + G_2 + \cdots + G_n,$$
where $G_i$ is the time spent while $k = i - 1$ for $i \le n - 1$, geometric with success probability $i / n$, and $G_n = 1$ is the move that takes $b$ from the top, which is geometric with success probability 1. The $G_i$ are independent. Hence $T$ is finite with probability 1 and
$$E[T] = \sum_{i=1}^{n} \frac{n}{i} = n H_n.$$
This is the law of the [coupon collector](/coupon-collector-problem/) time with $n$ coupons: when $i$ kinds are still missing, a draw is new with probability $i / n$.

## The upper bound

**Lemma 3.** For every strong uniform time $T$, $\|P^t - \pi\|_{TV} \le \Pr[T > t]$.

*Proof.* For each set $A$ of orders, by Lemma 2,
$$P^t(A) \ge \Pr[X_t \in A, T \le t] = \Pr[T \le t] \, \pi(A).$$
So $\pi(A) - P^t(A) \le \pi(A) (1 - \Pr[T \le t]) \le \Pr[T > t]$. Take the maximum over $A$. ∎

**Theorem 1.** For $c \ge 0$ and $t \ge n \ln n + cn$, $d(t) \le e^{-c}$.

*Proof.* The start deck is arbitrary in all the above, so $d(t) \le \Pr[T > t]$ by Lemma 3. Use the coupon collector form of $T$: draw coupons uniformly from $n$ kinds, and $T$ is the number of draws until all kinds are held. $T > t$ means that some kind is missing after $t$ draws. By the [union bound](/union-bound/),
$$\Pr[T > t] \le n \left(1 - \frac{1}{n}\right)^t \le n e^{-t/n} \le n e^{-\ln n - c} = e^{-c}. \qquad ∎$$

## The lower bound

**Theorem 2.** Let $c > 0$ with $j = \lfloor e^{c/2} \rfloor \ge 2$, and let $0 \le t \le n \ln n - cn$ with $j \le n$. Then
$$d(t) \ge 1 - \frac{1}{j!} - \frac{4}{(j - 1) c^2}.$$

*Proof.* Let $A_j$ be the set of orders in which the $j$ cards that started at the bottom are in their first relative order. Then $\pi(A_j) = 1/j!$, since in a uniform deck the relative order of $j$ fixed cards is uniform.

Let $y$ be the highest of these $j$ cards at the start; it has $j - 1$ cards below it. No card of the $j$ is moved before $y$ is on top: a card is moved only from the top, and $y$ is above the other $j - 1$ until it is moved. Insertions of other cards between them do not change their relative order. Let $T_j$ be the number of moves until $y$ is on top. If $T_j \ge t$, then the deck after $t$ moves is in $A_j$.

The argument for the law of $T$ applies to $y$: while $y$ has $k$ cards below it, a move puts the top card below $y$ with probability $(k + 1)/n$. So $T_j = G_j + G_{j+1} + \cdots + G_{n-1}$ with independent $G_i$ geometric with success probability $i / n$. Then
$$E[T_j] = n \sum_{i=j}^{n-1} \frac{1}{i} \ge n \int_j^n \frac{dx}{x} = n \ln n - n \ln j \ge n \ln n - \frac{cn}{2},$$
because $\ln j \le c/2$. And
$$\operatorname{Var}[T_j] = \sum_{i=j}^{n-1} \frac{1 - i/n}{(i/n)^2} \le n^2 \sum_{i=j}^{\infty} \frac{1}{i^2} \le \frac{n^2}{j - 1}.$$
With $t \le n \ln n - cn$ we have $E[T_j] - t \ge cn/2$. By [Chebyshev's inequality](/chebyshev-inequality/),
$$\Pr[T_j < t] \le \Pr\left[|T_j - E[T_j]| \ge \frac{cn}{2}\right] \le \frac{n^2/(j-1)}{c^2 n^2 / 4} = \frac{4}{(j - 1) c^2}.$$
So $P^t(A_j) \ge 1 - 4/((j-1)c^2)$, and
$$d(t) \ge P^t(A_j) - \pi(A_j) \ge 1 - \frac{4}{(j - 1) c^2} - \frac{1}{j!}. \qquad ∎$$

**Cutoff.** Theorem 1 gives $d(n \ln n + cn) \le e^{-c}$, and Theorem 2 gives $d(n \ln n - cn) \ge 1 - \varepsilon(c)$ with $\varepsilon(c) \to 0$ as $c \to \infty$, for all $n$ with $n \ge e^{c/2}$. So for each $\varepsilon \in (0, 1)$, $t_{mix}(\varepsilon) = n \ln n + O_\varepsilon(n)$, and $t_{mix}(\varepsilon) / (n \ln n) \to 1$. This is the cutoff at $n \ln n$ with a window of order $n$.

## Never uniform at a fixed time

For $n \ge 3$, each probability $P^t(\sigma)$ is an integer multiple of $n^{-t}$. If $P^t(\sigma) = 1/n!$ for all $\sigma$, then $n^t / n!$ is an integer. But $n - 1 \ge 2$ divides $n!$, and $n - 1$ has a prime factor that does not divide $n$, since $\gcd(n - 1, n) = 1$. So $n!$ does not divide $n^t$, and $d(t) > 0$ for all $t$. This is why the exact version stops at a random time, and why a bound on $d(t)$, not exactness, is the right claim for a fixed $t$.
