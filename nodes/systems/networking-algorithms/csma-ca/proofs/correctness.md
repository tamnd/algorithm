---
title: Acknowledged frames are delivered, RTS/CTS protects data in a single collision domain, and the Bianchi fixed point is unique
proves: [correctness]
status: full
---

**Setting.** Time is cut into slots. Nodes form a graph: a frame of node $u$ reaches exactly the neighbors of $u$. A node $r$ *receives* a frame of $u$ if $r$ is a neighbor of $u$, $r$ does not send during the frame, and no other neighbor of $r$ sends during any slot of the frame. A receiver sends an ACK, SIFS after it receives a data frame addressed to it, and only then. A node that receives a frame addressed to another node sets its NAV to the end time carried in that frame, and it does not start an RTS or a data frame while the NAV is in the future.

**Claim 1 (no false success).** If the sender of a data frame $F$ gets the ACK for $F$ (line L7), then the receiver received $F$.

*Proof.* The ACK is sent only by the receiver of $F$, and only SIFS after it received $F$; the sender accepts only the ACK that arrives within its timeout, which ends at the end of that ACK. $\square$

The converse fails: the receiver may get $F$ while the ACK is lost. Then the sender repeats $F$, and the receiver discards the copy by its sequence number. So DCF delivers each frame at most once to the upper layer, and at least once unless the retry limit is reached.

**Claim 2 (RTS/CTS in one collision domain).** Suppose every node hears every other node. Then with RTS/CTS, no data frame is lost.

*Proof.* A sender sends its data frame only after it received a CTS, which the receiver sends only after it received the RTS. Let the RTS of $A$ occupy slots $[s, s + R)$. Since the RTS was received, no other node sent during $[s, s + R)$. Since every node hears $A$ and no node other than $A$ sent during the RTS, every node other than $A$ received the RTS, and every node other than the receiver set its NAV to the end of the whole exchange (RTS, CTS, data and ACK with the SIFS gaps). Until then, no such node starts an RTS or a data frame. The only frames that such a node can still start in that time are SIFS responses (a CTS or an ACK) to frames it received. No response to an earlier frame is pending: a response starts SIFS after the frame it answers, and $A$ started its RTS only after DIFS of idle medium, with DIFS longer than SIFS, so any such response would have made the medium busy. And no node receives a new frame addressed to it during the exchange, because the only frames sent are those of $A$ and its receiver, which are addressed to each other. So during the data frame only $A$ sends, and the receiver receives it. $\square$

The claim needs the single collision domain. With hidden terminals a node may miss the CTS, for example because it was sending at that time, and then it may later send during the data frame; this is why RTS/CTS lowers but does not remove data losses in the hidden terminal test.

**Claim 3 (Bianchi's send probability).** Assume, as Bianchi does, that a station is always saturated and that each of its sends collides with the same probability $p$, independently of everything else. Let the window of backoff stage $i$ be $W_i = 2^{\min(i, m)} W$, with the counter drawn uniformly from $\{0, \dots, W_i - 1\}$, and count time in backoff steps: a step is an idle slot or a whole busy period, and a counter goes down by one per step. Then the long-run fraction of steps in which the station sends is

$$\tau(p) = \frac{2}{1 + W + p W \sum_{k=0}^{m-1} (2p)^k}.$$

*Proof.* Use the renewal reward theorem with one cycle per frame. The attempts of one frame end at the first success, so their number $A$ has $\Pr(A > k) = p^k$ and $\mathbb{E}[A] = 1 / (1 - p)$. The $(k+1)$-th attempt uses stage $\min(k, m)$, and it takes the counter value plus one steps: the counter runs down to zero and the send takes one more step. The expected length of a cycle is therefore

$$\sum_{k \ge 0} p^k \, \frac{W_{\min(k,m)} + 1}{2} = \frac{1}{2(1-p)} + \frac{W}{2} \left( \sum_{k=0}^{m-1} (2p)^k + \frac{(2p)^m}{1 - p} \right).$$

The station sends $\mathbb{E}[A]$ times per cycle, so $\tau = \mathbb{E}[A] / \mathbb{E}[\text{cycle}]$, which is $2 / \big(1 + W (1 - p) \sum_{k<m} (2p)^k + W (2p)^m\big)$. Since $(1 - 2p) \sum_{k<m} (2p)^k = 1 - (2p)^m$, the denominator equals $1 + W + p W \sum_{k<m} (2p)^k$. $\square$

At $p \ne 1/2$ this is Bianchi's form $\tau = 2(1-2p) / \big((1-2p)(W+1) + pW(1 - (2p)^m)\big)$; the sum form has no removable singularity at $p = 1/2$.

**Claim 4 (the fixed point is unique).** For $n \ge 2$ stations the system $\tau = \tau(p)$, $p = 1 - (1 - \tau)^{n-1}$ has exactly one solution with $p \in [0, 1]$, and bisection on $p$ finds it.

*Proof.* Let $g(p) = 1 - (1 - \tau(p))^{n-1} - p$. The function $\tau(p)$ is continuous and strictly decreasing on $[0, 1]$, because its denominator is a polynomial in $p$ with positive coefficients; its values lie in $(0, 1]$ because the denominator is at least $1 + W \ge 2$. So $1 - (1 - \tau(p))^{n-1}$ is continuous and nonincreasing in $p$, and $g$ is continuous and strictly decreasing. Also $g(0) = 1 - (1 - 2/(W+1))^{n-1} > 0$ and $g(1) = -(1 - \tau(1))^{n-1} \le 0$, with $g(1) < 0$ since $\tau(1) < 1$. So $g$ has exactly one root, and each bisection step keeps it inside the interval. $\square$

The model is an approximation: the constant and independent collision probability is an assumption, not a theorem. The slot-level simulation of the implementation does not make this assumption, and for $n = 5, 10, 20$ it agrees with the model within three percent on $\tau$ and $p$ and within $0.01$ on the throughput.
