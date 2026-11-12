---
title: Slotted ALOHA delivers each frame intact, and its throughput is at most 1/e
proves: [correctness]
status: full
---

The model is the one of the page. Time is cut into slots of one frame time. At the start of a slot, each station decides to send or not. At the end of the slot, every station learns whether the slot was idle (no sender), a success (one sender) or a collision (two or more senders). A frame that overlaps another frame in time is lost, and a frame that overlaps no other frame is received.

## 1. Safety: a success slot carries one intact frame

All frames start at a slot boundary and last exactly one slot, so two frames overlap in time if and only if they are sent in the same slot. In a success slot exactly one station sends, so its frame overlaps no other frame and is received. In a collision slot every frame overlaps another one and is lost, and line L6 keeps each of them in its queue. So no frame is lost for good, and no frame is reported as delivered when it was lost. $\square$

## 2. Throughput with a fixed send probability

**Claim.** Let $n \ge 1$ stations each have a frame and send it in a slot with probability $p \in [0, 1]$, independently. The probability that the slot is a success is

$$S_n(p) = n p (1 - p)^{n-1}.$$

*Proof.* The slot is a success when exactly one station sends. Station $i$ is the only sender with probability $p (1-p)^{n-1}$, by independence. These $n$ events are disjoint, so their probabilities add. $\square$

**Claim.** For $n \ge 2$, $S_n$ has its unique maximum on $[0, 1]$ at $p = 1/n$, and $S_n(1/n) = (1 - 1/n)^{n-1}$. For $n = 1$ the maximum is $S_1(1) = 1$.

*Proof.* For $n = 1$, $S_1(p) = p$. For $n \ge 2$,

$$S_n'(p) = n (1-p)^{n-2} \bigl((1 - p) - (n-1) p\bigr) = n (1-p)^{n-2} (1 - n p).$$

On $(0, 1)$ the factor $n(1-p)^{n-2}$ is positive, so $S_n'$ is positive for $p < 1/n$ and negative for $p > 1/n$. $S_n(0) = S_n(1) = 0$. So the unique maximum is at $p = 1/n$, with the value $n \cdot \frac1n (1 - \frac1n)^{n-1}$. $\square$

**Claim.** $b_n = (1 - 1/n)^{n-1}$ decreases strictly for $n \ge 2$ and tends to $1/e$. So $b_n > 1/e$ for all $n$.

*Proof.* Put $m = n - 1 \ge 1$. Then $b_n = \bigl(\frac{m}{m+1}\bigr)^m = 1 / a_m$ with $a_m = (1 + 1/m)^m$. It is enough to show that $a_m$ increases strictly to $e$. Apply the inequality of arithmetic and geometric means to the $m + 1$ positive numbers $1 + 1/m$ (taken $m$ times) and $1$. They are not all equal, so the inequality is strict:

$$a_m = \Bigl(1 + \frac1m\Bigr)^m \cdot 1 < \Bigl(\frac{m (1 + 1/m) + 1}{m + 1}\Bigr)^{m+1} = \Bigl(1 + \frac{1}{m+1}\Bigr)^{m+1} = a_{m+1}.$$

The limit $a_m \to e$ is the definition of $e$, or follows from $m \ln(1 + 1/m) = 1 - \frac{1}{2m} + O(m^{-2})$. Since $a_m$ increases to $e$, $b_n = 1/a_{n-1}$ decreases to $1/e$ and stays above it. $\square$

So with $n$ stations that know $n$, the best fixed probability gives a success in a fraction $b_n$ of the slots in the long run, by the strong law of large numbers applied to the independent slots. No choice of a common $p$ does better, and for large $n$ the best fraction is close to $1/e \approx 0.3679$.

## 3. The Poisson model and pure ALOHA

Abramson and Roberts analyze a different model: an infinite population, in which the total number of frames sent in a slot (new frames and repeats together) is a Poisson random variable with mean $G$. This is an approximation of the real protocol; it holds when many stations each send rarely and repeats are spread out at random.

**Slotted.** The slot is a success when exactly one frame is sent, with probability $G e^{-G}$. So $S(G) = G e^{-G}$, and $S'(G) = (1 - G) e^{-G}$ is positive for $G < 1$ and negative for $G > 1$. The maximum is $S(1) = 1/e$.

**Pure (unslotted) ALOHA.** Frame starts form a Poisson process of rate $G$ per frame time, and a frame lasts one frame time. A frame that starts at time $t$ overlaps another frame if and only if some other frame starts in the open interval $(t - 1, t + 1)$, of length $2$. By the independent increments of the Poisson process, the probability of no other start there is $e^{-2G}$. So $S(G) = G e^{-2G}$, with $S'(G) = (1 - 2G) e^{-2G}$, and the maximum is $S(1/2) = 1/(2e) \approx 0.1839$. Slots cut the period in which another start causes a collision from two frame times to one, and this doubles the best throughput.

## 4. Each frame is delivered with probability 1

In the saturated model of Section 2 with $0 < p < 1$, a given station is the only sender of a slot with probability $q = p (1-p)^{n-1} > 0$, independently from slot to slot. So the number of slots until its frame gets through is geometric with parameter $q$: it is finite with probability 1, and its mean is $1/q$. At $p = 1/n$ the mean is $n / b_n$, which is less than $e n$ by Section 2. $\square$

## 5. Fixed repeat probability: the drift becomes positive

Take the infinite-population model in which new frames arrive as a Poisson stream of $\lambda > 0$ frames per slot and are sent in their first slot, and each of the $b$ backlogged frames is sent again with a fixed probability $q_r \in (0, 1)$. Given a backlog of $b$, a slot is a success with probability

$$P_{\mathrm{succ}}(b) = e^{-\lambda} \bigl(\lambda (1 - q_r)^b + b q_r (1 - q_r)^{b-1}\bigr),$$

since either one new frame and no backlogged frame is sent, or no new frame and one backlogged frame. Each term tends to $0$ as $b \to \infty$, because $b x^b \to 0$ for $0 \le x < 1$. The backlog grows by the number of new frames and falls by one at each success, so its expected change in a slot is $\lambda - P_{\mathrm{succ}}(b)$, which is positive for all large $b$. Above that level the backlog drifts up, and fewer and fewer slots succeed. This is the instability of plain slotted ALOHA. A rule that lowers the send probability as the backlog grows, such as the pseudo-Bayesian rule of Rivest, keeps the success rate near $1/e$ at every backlog. $\square$
