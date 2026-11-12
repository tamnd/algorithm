---
title: Truncated binary exponential backoff ends every frame in bounded time and separates two stations fast
proves: [correctness]
status: full
---

**Model.** Time is divided into slots. A transmission takes one slot; if two or more stations transmit in the same slot, all of them collide and know it at the end of the slot. A station with a frame transmits it (line L2). After the $n$-th collision of the frame, line L6 draws $k$ uniformly from $\{0, 1, \ldots, 2^{\min(n,10)} - 1\}$, independently of everything else, and line L7 tries again $k$ slots later, in slot $\mathit{now} + 1 + k$. At the 16th collision, line L5 drops the frame.

**Claim 1 (every frame ends in bounded time).** Each frame is sent or dropped within at most $16 + 7151 = 7167$ slots after its first attempt.

*Proof.* Line L4 counts the collisions of the frame, and line L5 drops it at $n = 16$, so it has at most 16 attempts. Between attempt $n$ and attempt $n + 1$ the station waits at most $2^{\min(n,10)} - 1$ slots. Summed over $n = 1, \ldots, 15$, this is $(2 + 4 + \cdots + 512) + 6 \cdot 1024 - 15 = 1022 + 6144 - 15 = 7151$ slots, plus one slot for each of the 16 attempts. $\square$

So no frame is held forever, whatever the other stations do. The price is that a frame can be lost: the upper layer must then recover it, for example with TCP.

**Claim 2 (two stations).** Let two stations each have one frame and collide in slot 0, and let no other station transmit. After the $c$-th collision, they collide again with probability $2^{-\min(c,10)}$, independently of the past. The expected number of collisions is

$$E = \sum_{c=1}^{16} \prod_{j=1}^{c-1} 2^{-\min(j,10)} = 1 + \tfrac12 + \tfrac18 + \tfrac1{64} + \tfrac1{1024} + \cdots \approx 1.6416.$$

*Proof.* After their $c$-th collision both stations have the same count $c$, and both draw from a window of $W = 2^{\min(c,10)}$ values. If the draws $k_1 \ne k_2$, the station with the smaller draw transmits alone in its slot and succeeds; the other station then transmits alone too. If $k_1 = k_2$, they collide again, with the count $c + 1$. The draws are independent and uniform, so $\Pr[k_1 = k_2] = \sum_{x} W^{-2} = 1/W$. The number of collisions is at least $c$ with probability $\prod_{j=1}^{c-1} 2^{-\min(j,10)}$, and it is at most 16 by line L5. The expectation of a variable with values in $\{1, \ldots, 16\}$ is the sum of these tail probabilities. $\square$

**Claim 3 (more stations).** If $s \ge 2$ stations collide with the same count $c$ and draw from a window of $W \ge s$ values, the probability that the smallest draw is shared, so that no station succeeds in the next busy slot, is at most $\binom{s}{2}/W$.

*Proof.* The smallest draw is shared only if some pair of stations draws the same value. Each pair does so with probability $1/W$, and the union bound over the $\binom{s}{2}$ pairs gives the claim. $\square$

So after about $\log_2 s^2$ collisions, the windows are large enough that the stations separate with a constant probability at each step. $\blacksquare$
