---
title: The CUBIC window function starts at the reduced window, returns to W_max at time K, and is concave then convex, and the Reno-friendly increase matches the Reno rate
proves: [correctness]
status: full
---

**The setting.** Constants $C > 0$ and $0 < \beta < 1$ (RFC 9438 uses $C = 0.4$ and $\beta = 0.7$). At a congestion event (line L7 to line L9) the sender records $W_{\max} > 0$, sets $\text{cwnd}_{\text{epoch}} = \beta\, \text{cwnd} \le W_{\max}$, and starts a new epoch at time $t = 0$ with

$$K = \sqrt[3]{\frac{W_{\max} - \text{cwnd}_{\text{epoch}}}{C}}, \qquad W_{\text{cubic}}(t) = C (t - K)^3 + W_{\max}.$$

**Lemma 1 (end points).** $W_{\text{cubic}}(0) = \text{cwnd}_{\text{epoch}}$ and $W_{\text{cubic}}(K) = W_{\max}$. Without fast convergence, $W_{\max}$ is the window at the loss, so $\text{cwnd}_{\text{epoch}} = \beta W_{\max}$ and $K = \sqrt[3]{W_{\max}(1 - \beta)/C}$.

*Proof.* $W_{\text{cubic}}(0) = -C K^3 + W_{\max} = -(W_{\max} - \text{cwnd}_{\text{epoch}}) + W_{\max}$. The second equality is immediate. For the last, put $\text{cwnd}_{\text{epoch}} = \beta W_{\max}$ in the formula for $K$. $\square$

**Lemma 2 (shape).** $W_{\text{cubic}}$ is nondecreasing on $[0, \infty)$, strictly increasing except at $t = K$, strictly concave on $[0, K)$ and strictly convex on $(K, \infty)$. Its slope at $t = K$ is 0.

*Proof.* $W'_{\text{cubic}}(t) = 3C(t - K)^2 \ge 0$ with equality only at $t = K$. $W''_{\text{cubic}}(t) = 6C(t - K)$ is negative for $t < K$ and positive for $t > K$. $\square$

So the window grows fast just after the reduction, slows down near the last window that had a loss (the plateau at $W_{\max}$), and grows faster again after it. The growth depends on the time $t$ since the loss, not on the number of round trips.

**Lemma 3 (the step per ACK is bounded).** Lines L2, L3 and L6 change cwnd by $(\text{target} - \text{cwnd})/\text{cwnd}$ per acknowledged segment, with $\text{cwnd} \le \text{target} \le 1.5\,\text{cwnd}$. So each ACK adds between $0$ and $0.5$ segments, and one round trip of cwnd ACKs adds at most about one half of the window.

*Proof.* Line L3 clamps the target to $[\text{cwnd}, 1.5\,\text{cwnd}]$, so $0 \le (\text{target} - \text{cwnd})/\text{cwnd} \le 0.5$. $\square$

**Theorem 1 (the Reno-friendly increase).** Consider an AIMD sawtooth that grows by $\alpha$ segments per round trip and multiplies the window by $\beta$ at each loss, with one loss per cycle, as in the model of Mathis et al. Its rate $B$ in segments per round trip and its loss rate $p$ satisfy

$$B^2 p = \frac{\alpha (1 + \beta)}{2(1 - \beta)}.$$

So $\alpha = 3(1 - \beta)/(1 + \beta)$ gives the same rate as Reno ($\alpha = 1$, $\beta = 1/2$) at every loss rate. For $\beta = 0.7$ this is $\alpha = 0.9/1.7 \approx 0.529$.

*Proof.* Let the window go from $\beta w$ up to $w$. The cycle has $(1 - \beta) w/\alpha$ round trips, and the mean window is $(1 + \beta) w/2$, so the cycle sends $N = (1 + \beta)(1 - \beta) w^2 / (2\alpha)$ segments, with one loss: $p = 1/N$. The rate is $B = (1 + \beta) w/2$. Then

$$B^2 p = \frac{(1 + \beta)^2 w^2}{4} \cdot \frac{2\alpha}{(1 + \beta)(1 - \beta) w^2} = \frac{\alpha (1 + \beta)}{2 (1 - \beta)}.$$

For Reno this is $1 \cdot 1.5 / 1 = 3/2$. Setting $\alpha (1 + \beta)/(2(1 - \beta)) = 3/2$ gives $\alpha = 3(1 - \beta)/(1 + \beta)$. $\blacksquare$

Line L4 grows $W_{\text{est}}$ by this $\alpha$ per round trip, and line L5 uses $W_{\text{est}}$ when it is above $W_{\text{cubic}}$. So where the Reno-friendly estimate is the larger of the two, CUBIC follows it and gets about the rate of Reno at the same loss rate. Once $W_{\text{est}}$ reaches the window before the loss, line L4 uses $\alpha = 1$, as RFC 9438 asks.

**Theorem 2 (the rate in the cubic region).** Consider the periodic model in which each epoch ends with one loss at time $K$, when the window is back at $W_{\max}$, and $\text{cwnd}_{\text{epoch}} = \beta W_{\max}$. With a round trip of $\text{RTT}$ seconds and the window following $W_{\text{cubic}}$, the mean window is

$$\bar{W} = \left(\frac{C(3 + \beta)}{4(1 - \beta)}\right)^{1/4} \left(\frac{\text{RTT}}{p}\right)^{3/4} \text{ segments}.$$

*Proof.* The epoch lasts $K$ seconds, which is $K/\text{RTT}$ round trips, and sends

$$N = \frac{1}{\text{RTT}} \int_0^K W_{\text{cubic}}(t)\, dt = \frac{1}{\text{RTT}} \left( W_{\max} K - \frac{C K^4}{4} \right)$$

segments, since $\int_0^K (t - K)^3\, dt = -K^4/4$. By Lemma 1, $W_{\max} = C K^3/(1 - \beta)$, so

$$N = \frac{C K^4}{\text{RTT}} \left(\frac{1}{1 - \beta} - \frac{1}{4}\right) = \frac{C K^4 (3 + \beta)}{4 (1 - \beta)\, \text{RTT}}.$$

One segment is lost per epoch, so $p = 1/N$ and $K^4 = 4(1 - \beta)\,\text{RTT} / (C (3 + \beta) p)$. The mean window is $\bar W = N / (K/\text{RTT}) = C K^3 (3 + \beta)/(4(1 - \beta))$. Put in $K^3 = (K^4)^{3/4}$:

$$\bar W = \frac{C(3 + \beta)}{4(1 - \beta)} \left(\frac{4(1 - \beta)\,\text{RTT}}{C(3 + \beta)\,p}\right)^{3/4} = \left(\frac{C(3 + \beta)}{4(1 - \beta)}\right)^{1/4} \left(\frac{\text{RTT}}{p}\right)^{3/4}. \qquad \blacksquare$$

For $C = 0.4$ and $\beta = 0.7$ the constant is $(1.48/1.2)^{1/4} \approx 1.054$. The rate $\bar W/\text{RTT}$ is proportional to $\text{RTT}^{-1/4}$, while the Reno rate is proportional to $\text{RTT}^{-1}$.
