---
title: The position maps and the orders of the perfect shuffles
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The deck is $A[0 \ldots n-1]$ with $n = 2m$, and positions are 0-based unless we say otherwise.

**Termination.** The loop of line L2 runs $m$ times, and each iteration writes two entries of $B$. Each position of $B$ is written exactly once: iteration $k$ writes positions $2k$ and $2k + 1$. So $B$ is a rearrangement of $A$, and the algorithm stops after $\Theta(n)$ steps.

## Lemma 1: the position maps

**Out-shuffle.** Line L3 puts $A[k]$ at $2k$ and $A[m + k]$ at $2k + 1$, for $0 \le k < m$. So a card at position $p$ moves to
$$\text{out}(p) = \begin{cases} 2p & \text{if } p < m, \\ 2p - (n - 1) & \text{if } p \ge m. \end{cases}$$
For $p \le n - 2$ both values lie in $\{0, \ldots, n-2\}$, so $\text{out}(p) = 2p \bmod (n-1)$. For $p = n - 1$, $\text{out}(p) = 2(n-1) - (n-1) = n - 1$.

**In-shuffle.** Line L4 puts $A[m + k]$ at $2k$ and $A[k]$ at $2k + 1$. So $\text{in}(p) = 2p + 1$ if $p < m$, and $\text{in}(p) = 2p + 1 - (n + 1)$ if $p \ge m$. Both values lie in $\{0, \ldots, n-1\}$, so $\text{in}(p) = (2p + 1) \bmod (n+1)$. With $q = p + 1 \in \{1, \ldots, n\}$, this is $q \mapsto 2q \bmod (n+1)$. $\square$

## Theorem: the orders

**Theorem.** Let $n \ge 2$ be even. After $k$ out-shuffles the deck is in its first order if and only if $2^k \equiv 1 \pmod{n-1}$. After $k$ in-shuffles it is in its first order if and only if $2^k \equiv 1 \pmod{n+1}$.

*Proof.* By Lemma 1 and induction on $k$, $k$ out-shuffles move the card at position $p \le n-2$ to $2^k p \bmod (n-1)$, and keep the last card fixed. If $2^k \equiv 1 \pmod{n-1}$, every card returns. Conversely, if the deck is restored then the card at position 1 returns, so $2^k \equiv 1 \pmod{n-1}$. (For $n = 2$ the modulus is 1, every $k$ works, and the out-shuffle is the identity.) For the in-shuffle, $k$ shuffles send the 1-based position $q$ to $2^k q \bmod (n+1)$, and the same argument with $q = 1$ applies. Since $n \pm 1$ is odd, 2 is invertible modulo $n \pm 1$, so the orders exist and divide $\varphi(n \pm 1)$. $\blacksquare$

**Example.** For $n = 52$: $2^8 = 256 = 5 \cdot 51 + 1$, and $2^k \not\equiv 1 \pmod{51}$ for $k < 8$, so 8 out-shuffles restore the deck. 53 is prime and 2 is a primitive root modulo 53, so 52 in-shuffles are needed.

## Corollary: reversal by in-shuffles

If $2^j \equiv -1 \pmod{n+1}$, then $j$ in-shuffles send $q$ to $-q \bmod (n+1) = n + 1 - q$, which reverses the deck. For $n = 52$, 53 is prime and $\operatorname{ord}_{53}(2) = 52$, so $x = 2^{26}$ satisfies $x^2 \equiv 1$ and $x \not\equiv 1$. Modulo a prime this gives $x \equiv -1$. So 26 in-shuffles reverse 52 cards. For $n = 8$, $2^3 = 8 \equiv -1 \pmod 9$, so 3 in-shuffles reverse 8 cards.

## Out-shuffle as an in-shuffle of the middle

In an out-shuffle the cards at positions 0 and $n - 1$ stay. The other cards are at positions $1, \ldots, n-2$, and $\text{out}(p) = 2p \bmod (n - 1)$. With $p' = p - 1$ on the $n' = n - 2$ middle cards, $\text{out}$ becomes $p' \mapsto 2p' + 1 \bmod (n' + 1)$, which is the in-shuffle of $n'$ cards. So the out-shuffle order for $n$ cards equals the in-shuffle order for $n - 2$ cards.

## Elmsley's rule

**Claim.** Let $0 \le p < n$ and let $p = (b_1 b_2 \cdots b_r)_2$ in binary with $b_1 = 1$ (and $r = 0$ for $p = 0$). Do the shuffles $s_1, \ldots, s_r$, with $s_i$ an in-shuffle if $b_i = 1$ and an out-shuffle if $b_i = 0$. Then the card that was on top ends at position $p$.

*Proof.* Let $x_i = (b_1 \cdots b_i)_2$, the value of the first $i$ bits, with $x_0 = 0$. We show that after $s_1, \ldots, s_i$ the top card is at $x_i$. This is true for $i = 0$. Assume the top card is at $x_{i-1}$. Since $x_{i-1} \le \lfloor p / 2 \rfloor \le (n-1)/2$, and $x_{i-1}$ is an integer, $x_{i-1} \le m - 1 < m$, so the card is in the top half. By Lemma 1, the out-shuffle sends it to $2x_{i-1}$ and the in-shuffle to $2x_{i-1} + 1$. That is $2x_{i-1} + b_i = x_i$. At the end the card is at $x_r = p$. $\square$

## Power-of-two decks

For $n = 2^k$, the out-shuffle map $p \mapsto 2p \bmod (2^k - 1)$ on $\{0, \ldots, 2^k - 2\}$, together with $2^k - 1 \mapsto 2^k - 1$, is the left rotation of the $k$-bit number $p$ by one bit: the top bit $b$ of $p$ leaves as $b \cdot 2^k$, and $2^k \equiv 1$ brings it back as the lowest bit. So $k$ out-shuffles restore the deck, as $\operatorname{ord}_{2^k - 1}(2) = k$ says.
