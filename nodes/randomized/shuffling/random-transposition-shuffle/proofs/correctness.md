---
title: Random transpositions converge to uniform, Broder's time is strong uniform, and (1/2) n ln n moves are needed
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, with $n \ge 2$ cards. The calls of RANDOM are independent and uniform on $\{0, \ldots, n-1\}$. Let $X_t$ be the deck after $t$ moves, $P^t$ its law, and $\pi$ the uniform law on the $n!$ orders. The distance is $d(t) = \|P^t - \pi\|_{TV} = \max_A (\pi(A) - P^t(A))$.

The upper bound $d(\frac12 n \ln n + cn) \le a e^{-2c}$ of Diaconis and Shahshahani needs the representation theory of the symmetric group, and it is only cited here. Everything else on the page is proved below.

**Termination.** The loop of line L1 makes exactly $t$ iterations of $\Theta(1)$ work. For Broder's exact version we show below that the stopping time $T$ is finite with probability 1 and has mean $\frac{2n^2}{n+1} H_n$.

## Stationarity and convergence

A move picks $(L, R)$ with probability $1/n^2$ and applies the permutation of positions $\tau_{L,R}$, a transposition or the identity. Each $\tau_{L,R}$ is a bijection of the orders, so if $X_t$ is uniform then $X_{t+1}$ is uniform. The transpositions generate the symmetric group, so every order can be reached from every other: the chain is irreducible. The identity move has probability $1/n > 0$, so the chain is aperiodic. By the convergence theorem for finite chains, $d(t) \to 0$.

**Never exactly uniform for $n \ge 3$.** Each $P^t(\sigma)$ is a sum of terms $n^{-2t}$, so it is an integer multiple of $n^{-2t}$. If $P^t(\sigma) = 1/n!$, then $n^{2t}/n!$ is an integer. The number $n - 1 \ge 2$ divides $n!$ and is coprime to $n$, so it has a prime factor that does not divide $n^{2t}$. So $d(t) > 0$ for every $t$.

**Distinct pairs are periodic.** If $L \ne R$ is forced, each move is a transposition, an odd permutation. After $t$ moves the deck has the parity of $t$. The set $A$ of orders with the other parity has $\pi(A) = \frac12$ and $P^t(A) = 0$, so $d(t) \ge \frac12$ for all $t$.

## Broder's strong uniform time

At each move, let $c_R$ be the card at position $R$ and $c_L$ the card at position $L$ before the swap. Mark $c_R$ if $c_R$ is not marked and ($c_L$ is marked or $L = R$). Then do the swap. Let $M_t$ be the set of marked cards after move $t$, $Q_t$ the set of positions that hold them, and $f_t : M_t \to Q_t$ the map from each marked card to its position. Let $\mathcal H_t$ be the history $(M_s, Q_s)_{s \le t}$.

**Lemma 1.** Given $\mathcal H_t$, the map $f_t$ is uniform on the $|M_t|!$ bijections from $M_t$ to $Q_t$.

*Proof.* By induction on $t$. At $t = 0$ nothing is marked. Assume the claim at $t$, with $k = |M_t|$. Which case happens at move $t + 1$ depends only on $L$, $R$ and $Q_t$, since a position holds a marked card exactly when it is in $Q_t$. So the case is independent of $f_t$ given $\mathcal H_t$.

- *Both $L$ and $R$ in $Q_t$.* No new mark. $f_{t+1} = \tau_{L,R} \circ f_t$, where $\tau_{L,R}$ swaps the two positions. Composing with a fixed bijection maps the uniform law on bijections $M_t \to Q_t$ to itself, and $Q_{t+1} = Q_t$.
- *Neither in $Q_t$, and $L \ne R$.* No new mark, and no marked card moves: $f_{t+1} = f_t$.
- *$L \in Q_t$ and $R \notin Q_t$.* This is a new mark; see the last case.
- *$R \in Q_t$ and $L \notin Q_t$.* No new mark, since $c_R$ is marked. The marked card at $R$ moves to $L$: $f_{t+1} = \tau_{L,R} \circ f_t$, a fixed relabeling of the positions from $Q_t$ to $Q_{t+1} = Q_t - \{R\} \cup \{L\}$. A uniform bijection stays uniform.
- *A new mark: $R \notin Q_t$, and $L \in Q_t$ or $L = R$.* Let $c = c_R$. Given $R$ and the event that a mark happens, $L$ is uniform on the $k + 1$ positions $Q_t \cup \{R\}$, because each of them has probability $1/n$. After the swap, $c$ is at $L$, and if $L \ne R$ the marked card that was at $L$ is at $R$. So $Q_{t+1} = Q_t \cup \{R\}$, $M_{t+1} = M_t \cup \{c\}$, and $f_{t+1} = \tau_{L,R} \circ (f_t \cup \{c \mapsto R\})$. The map $(f_t, L) \mapsto f_{t+1}$ is a bijection from the $k! \,(k+1)$ pairs onto the $(k+1)!$ bijections $M_{t+1} \to Q_{t+1}$: from $f_{t+1}$ we read $L = f_{t+1}(c)$, and then $f_t = \tau_{L,R} \circ f_{t+1}$ on $M_t$. A uniform $f_t$ and an independent uniform $L$ give a uniform $f_{t+1}$.

In every case the new history is a function of $\mathcal H_t$, $L$ and $R$ that does not use $f_t$, so the claim holds at $t + 1$. ∎

**Theorem 1.** Let $T$ be the first move after which all $n$ cards are marked. Then $T$ is a strong uniform time: for each $t$ and each order $\sigma$, $\Pr[X_t = \sigma, T \le t] = \Pr[T \le t]/n!$.

*Proof.* The event $\{T = s\}$ is a function of $\mathcal H_s$. On it, $M_s$ is all cards and $Q_s$ all positions, so by Lemma 1 the deck $X_s = f_s$ is uniform given $T = s$. The later moves use new random values and keep the uniform law, so $X_t$ is uniform given $T = s$ for $t \ge s$. Summing over $s \le t$ gives the claim. ∎

**The law of $T$.** With $k$ cards marked, a move marks a card when $R$ is one of the $n - k$ unmarked positions and $L$ is one of the $k + 1$ positions in $Q_t \cup \{R\}$; the probability is $p_k = (n-k)(k+1)/n^2$, whatever the past. So $T$ is a sum of independent geometric times with these success probabilities, $T$ is finite with probability 1, and
$$E[T] = \sum_{k=0}^{n-1} \frac{n^2}{(n-k)(k+1)} = \frac{n^2}{n+1} \sum_{k=0}^{n-1} \left( \frac{1}{k+1} + \frac{1}{n-k} \right) = \frac{2n^2}{n+1} H_n,$$
using $\frac{1}{(n-k)(k+1)} = \frac{1}{n+1} \left( \frac{1}{k+1} + \frac{1}{n-k} \right)$.

**Corollary.** $d(t) \le \Pr[T > t]$ (the bound of the [strong uniform time](/strong-uniform-time/) page). By [Markov's inequality](/markov-inequality/), $\Pr[T > 4 E[T]] \le \frac14$, so $d(t) \le \frac14$ for $t \ge \frac{8 n^2}{n+1} H_n$. This is $O(n \log n)$ but with a worse constant than the sharp $\frac12 n \ln n$.

## The lower bound

**Theorem 2.** For $c > 0$ and $t \le \frac{n-1}{2} \ln n - c(n-1)$,
$$d(t) \ge 1 - 6 e^{-2c}.$$

*Proof.* Call a position *untouched* at time $t$ if it was neither $L$ nor $R$ in moves $1$ to $t$. An untouched position holds its first card, so it is a fixed point of the deck. Let $N$ be the number of untouched positions and $F$ the number of fixed points; then $F \ge N$.

Let $I_i$ be the indicator that position $i$ is untouched. A move avoids $i$ with probability $(1 - 1/n)^2$, so $E[I_i] = (1 - 1/n)^{2t}$, and
$$\mu = E[N] = n \left(1 - \frac1n\right)^{2t} \ge n e^{-2t/(n-1)} \ge n e^{-\ln n + 2c} = e^{2c},$$
using $\ln(1 - x) \ge -x/(1-x)$ with $x = 1/n$. For $i \ne j$, a move avoids both with probability $(1 - 2/n)^2 \le (1 - 1/n)^4$, so $E[I_i I_j] \le E[I_i] E[I_j]$ and the covariances are at most 0. Hence $\operatorname{Var}[N] \le \sum_i \operatorname{Var}[I_i] \le \mu$.

Let $A$ be the set of orders with at least $\mu / 2$ fixed points. By [Chebyshev's inequality](/chebyshev-inequality/),
$$P^t(A) \ge \Pr[N \ge \mu/2] \ge 1 - \Pr[|N - \mu| \ge \mu/2] \ge 1 - \frac{4 \operatorname{Var}[N]}{\mu^2} \ge 1 - \frac{4}{\mu}.$$
A uniform order has on average one fixed point (each position is fixed with probability $1/n$), so by Markov's inequality $\pi(A) \le 2/\mu$. Then
$$d(t) \ge P^t(A) - \pi(A) \ge 1 - \frac{6}{\mu} \ge 1 - 6 e^{-2c}. \qquad ∎$$

**Cutoff.** Theorem 2 and the theorem of Diaconis and Shahshahani give, for each fixed $\varepsilon \in (0, 1)$, $t_{mix}(\varepsilon) = \frac12 n \ln n + O_\varepsilon(n)$.

## The cycle-type chain used for the tables

The step law gives the same weight to all transpositions, a set closed under conjugation. Then $P^t(\gamma \sigma \gamma^{-1}) = P^t(\sigma)$ for all $\gamma$, by induction on $t$, so $P^t$ is constant on each cycle type $\lambda$. Hence
$$d(t) = \frac12 \sum_\lambda \left| P^t(\text{type } \lambda) - \pi(\text{type } \lambda) \right|, \qquad \pi(\text{type } \lambda) = \prod_a \frac{1}{a^{m_a} m_a!},$$
where $m_a$ is the number of cycles of length $a$. The type evolves as a Markov chain. Composing with a transposition $(x\,y)$ splits a cycle when $x$ and $y$ are in the same cycle and merges two cycles otherwise. For a cycle of length $a$ and each $s \in \{1, \ldots, a-1\}$, exactly $a$ ordered pairs $(L, R)$ in it split it into cycles of lengths $s$ and $a - s$ (for each $L$, one $R$ at distance $s$ along the cycle). Two cycles of lengths $a$ and $b$ are merged by $2ab$ ordered pairs. The $n$ pairs with $L = R$ keep the type. These counts add up to $n^2$. The tests check that this chain gives the same distances as brute force over all orders for $n \le 5$.
