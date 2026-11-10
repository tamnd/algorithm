---
tag: SAHXW6
kind: problem
slug: tcp-acknowledgment-problem
name: TCP acknowledgment problem
aliases:
- TCP ack problem
- dynamic TCP acknowledgment
- acknowledgment delay problem
area: online-and-streaming/competitive-analysis
level: advanced
summary: Choose when to acknowledge packets so that the number of acknowledgments plus the total delay is small. Greedy is 2-competitive and optimal among deterministic rules.
prereqs: [competitive-ratio, online-algorithm, offline-optimum]
see_also: [ski-rental-problem, randomized-online-algorithm, oblivious-adversary, online-primal-dual, break-even-strategy, nagle-algorithm, tcp-reno, bahncard-problem]
sources:
  - paper: doi:10.1145/375827.375843
    title: "Daniel R. Dooly, Sally A. Goldman and Stephen D. Scott, On-line analysis of the TCP acknowledgment delay problem, Journal of the ACM 48(2) (2001), 243-273"
    locator: the model, the 2-competitive greedy algorithm and the matching deterministic lower bound, and the offline dynamic programs; first in STOC 1998 as TCP dynamic acknowledgment delay, theory and practice
  - paper: "Anna R. Karlin, Claire Kenyon and Dana Randall, Dynamic TCP acknowledgement and other stories about e/(e-1), Proceedings of the 33rd ACM Symposium on Theory of Computing (STOC), 2001, 502-509"
    locator: the randomized e/(e-1)-competitive algorithm for the oblivious adversary, by a reduction to a family of ski rental problems; journal version in Algorithmica 36(3) (2003), 209-224
  - paper: "Susanne Albers and Helge Bals, Dynamic TCP acknowledgment: penalizing long delays, Proceedings of the 14th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2003, 47-55"
    locator: the variant with the maximum delay in place of the sum, with the optimal deterministic ratio pi^2/6
  - paper: doi:10.1561/0400000024
    title: "Niv Buchbinder and Joseph (Seffi) Naor, The design of competitive online algorithms via a primal-dual approach, Foundations and Trends in Theoretical Computer Science 3(2-3) (2009), 93-263"
    locator: the chapter on the TCP acknowledgment problem, which derives the e/(e-1) bound by the online primal-dual method
---

The TCP acknowledgment problem asks when a receiver should send acknowledgments for packets that arrive over time, when one acknowledgment covers every packet that is still waiting. Each acknowledgment has a fixed cost, and each packet costs the time it waits, so the receiver trades the number of acknowledgments against the delay. Dooly, Goldman and Scott (1998) showed that acknowledging when the waiting cost reaches the acknowledgment cost is 2-competitive, and that no deterministic online algorithm does better. Karlin, Kenyon and Randall (2001) gave a randomized algorithm with ratio $e/(e-1) \approx 1.582$ against an [oblivious adversary](/oblivious-adversary/).

## In plain words

Data packets come to a computer one at a time, at times nobody knows in advance. For each packet the computer must send a short message back to say that the packet came. One message can confirm all the packets that are waiting, but each message costs something to send, so it is good to send few of them. Each packet also costs something for each moment that it waits, so it is bad to wait long.

The computer must decide when to send each message without knowing when the next packet will come. A simple rule works well: send a message as soon as the waiting cost of the packets in hand is equal to the cost of one message. This rule never pays more than twice the best possible cost, and no rule that decides without seeing the future can always do better.

## Definition

Packets arrive at times $0 \le a_1 \le a_2 \le \cdots \le a_n$. A *schedule* is a finite set of acknowledgment times $t_1 < t_2 < \cdots < t_k$. An acknowledgment at time $t$ covers every packet that arrived at or before $t$ and was not covered before. Packet $i$ is covered at $c_i = \min\{t_j : t_j \ge a_i\}$, and every packet must be covered. The cost of the schedule is

$$\mathrm{cost} = k + \sum_{i=1}^{n} (c_i - a_i),$$

the number of acknowledgments plus the total latency. The cost of one acknowledgment is scaled to $1$; a cost $\alpha$ is the same problem with time scaled by $\alpha$.

An *online algorithm* learns $a_i$ at time $a_i$, does not know $n$ or the future arrivals, and must decide at each moment whether to acknowledge. The input is $\sigma = (a_1, \ldots, a_n)$. An algorithm is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for every $\sigma$, where $\mathrm{OPT}(\sigma)$ is the cost of the best schedule chosen with full knowledge of $\sigma$ (the [offline optimum](/offline-optimum/)). For a [randomized online algorithm](/randomized-online-algorithm/), $\mathrm{ALG}(\sigma)$ is the expected cost and the adversary is oblivious: it fixes $\sigma$ in advance.

## Variants

- **Maximum delay.** The cost is the number of acknowledgments plus the largest latency of a packet in each batch, summed over the batches. Albers and Bals (2003) show that the best deterministic ratio is $\pi^2/6 \approx 1.645$.
- **Bounded number of acknowledgments.** The algorithm has a budget of acknowledgments and minimizes the total or maximum latency. DGS treat versions with such limits.
- **Joint replenishment.** Several item types share an ordering cost and each type has its own extra cost per order. The TCP problem is the case of one type. Buchbinder, Kimbrel, Levi, Makarychev and Sviridenko (2008) give a 3-competitive algorithm for the online version.
- **Aggregation on trees.** Messages travel up a tree and each edge has its own cost. The TCP problem is the case of a tree with one edge.

## Examples

Let the arrivals be $\sigma = (0, 0.2, 0.5, 1.6, 1.7, 3.0)$.

**The greedy rule.** It acknowledges as soon as the latency of the pending packets reaches $1$.

| batch | packets | latency builds up | acknowledgment at | batch cost |
|---|---|---|---|---|
| 1 | 0, 0.2, 0.5 | $0.2$ by time $0.2$, $0.8$ by time $0.5$, then 3 packets add $0.2$ in time $1/15$ | $17/30 \approx 0.567$ | $1 + 1 = 2$ |
| 2 | 1.6, 1.7 | $0.1$ by time $1.7$, then 2 packets add $0.9$ in $0.45$ | $2.15$ | $2$ |
| 3 | 3.0 | one packet adds $1$ in time $1$ | $4.0$ | $2$ |

The greedy cost is $6$.

**The optimum.** Acknowledge at $0.5$, at $1.7$ and at $3.0$. The latencies are $0.5 + 0.3 + 0 = 0.8$, then $0.1 + 0$, then $0$, so $\mathrm{OPT}(\sigma) = 3 + 0.9 = 3.9$. The ratio is $6/3.9 \approx 1.54$.

**A non-example.** Acknowledging each packet at once costs $n$, and waiting until the end costs at least $\sum_i (a_n - a_i)$. Neither is competitive: the first loses on a burst of $n$ packets at one time, where $\mathrm{OPT} = 1$, and the second on packets far apart.

## Known algorithms

- **Greedy, or balance.** Acknowledge as soon as the total latency of the pending packets reaches the acknowledgment cost. It is 2-competitive with $b = 0$, and this is optimal for deterministic algorithms (DGS 1998). It is a [break-even strategy](/break-even-strategy/), like the deterministic rule for [ski rental](/ski-rental-problem/).
- **Randomized algorithm of Karlin, Kenyon and Randall.** It acknowledges at a random time drawn from a density that grows like $e^z$, chosen as in randomized ski rental. Its expected cost is at most $\frac{e}{e-1} \mathrm{OPT}(\sigma)$ against an oblivious adversary. Buchbinder and Naor derive the same bound with the [online primal-dual](/online-primal-dual/) method.
- **Offline dynamic program.** An optimal schedule acknowledges only at arrival times, since moving an acknowledgment back to the last arrival it covers lowers the latency and changes nothing else. So $\mathrm{OPT}$ splits the sorted packets into contiguous batches, each acknowledged at the arrival of its last packet:

$$F(0) = 0, \qquad F(i) = \min_{0 \le j < i} \Bigl( F(j) + 1 + \sum_{m=j+1}^{i} (a_i - a_m) \Bigr),$$

and $\mathrm{OPT} = F(n)$. With prefix sums this takes $O(n^2)$ time. In the example, $F$ gives $3.9$.

## Bounds

**Theorem 1 (the greedy rule is 2-competitive).** For every arrival sequence $\sigma$, $\mathrm{GREEDY}(\sigma) \le 2\,\mathrm{OPT}(\sigma)$.

*Proof.* Let greedy send $k$ acknowledgments. Batch $j$ consists of the packets covered by the $j$-th acknowledgment; let $s_j$ be the arrival time of its first packet and $t_j$ the time of the acknowledgment.

1. Greedy acknowledges exactly when the latency of the batch reaches $1$, so each batch costs $1 + 1 = 2$, and $\mathrm{GREEDY}(\sigma) = 2k$.
2. A packet that arrives after $t_j$ belongs to a later batch, so $s_{j+1} > t_j$, and the intervals $I_j = [s_j, t_j)$ are pairwise disjoint.
3. Fix an optimal schedule and a batch $j$. If the schedule has an acknowledgment in $I_j$, charge $1$ of its acknowledgment cost to batch $j$. Each acknowledgment lies in at most one interval, so it is charged at most once.
4. If the schedule has no acknowledgment in $I_j$, every packet of batch $j$ arrives at or after $s_j$ and stays pending in the optimal schedule until time $t_j$ at least. So its latency there is at least its latency $t_j - a_i$ under greedy, and the optimal latency of batch $j$ is at least $1$. Charge this latency to batch $j$; different batches have different packets.
5. Each batch gets a charge of at least $1$ from disjoint parts of the optimal cost, so $\mathrm{OPT}(\sigma) \ge k = \mathrm{GREEDY}(\sigma)/2$. $\square$

**Theorem 2 (no deterministic algorithm beats 2).** For every deterministic online algorithm $A$ and every constants $c < 2$ and $b$, some $\sigma$ has $A(\sigma) > c \cdot \mathrm{OPT}(\sigma) + b$.

*Proof.* Fix $n$, even, and let $\delta = 1/n^2$. The adversary sends packet 1 at time $0$. Each time $A$ acknowledges, the adversary sends the next packet $\delta$ later, until it has sent $n$ packets. (If $A$ never acknowledges some packet, its cost is infinite.) So each batch of $A$ holds one packet. Let $d_i$ be the latency of packet $i$ under $A$; then $A(\sigma) = n + \sum_i d_i$ and $a_{i+1} - a_i = d_i + \delta$.

Consider two offline schedules. Schedule $P$ acknowledges the pairs $\{1, 2\}, \{3, 4\}, \ldots$, each at the arrival of its second packet, so it costs $n/2 + \sum_{i \text{ odd}} (d_i + \delta)$. Schedule $Q$ acknowledges $\{1\}$, then the pairs $\{2, 3\}, \ldots, \{n-2, n-1\}$, then $\{n\}$, so it costs $n/2 + 1 + \sum_{i \text{ even}, i < n} (d_i + \delta)$. Adding,

$$P + Q \le n + 1 + \sum_i d_i + n\delta \le A(\sigma) + 2,$$

so $\mathrm{OPT}(\sigma) \le \min(P, Q) \le (A(\sigma) + 2)/2$. If $A(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ held for all such $\sigma$, then $A(\sigma)(1 - c/2) \le c + b$. Since $A(\sigma) \ge n$ and $n$ is arbitrary, this fails for large $n$ when $c < 2$. $\square$

**Randomized bounds.** Karlin, Kenyon and Randall (2001) give an algorithm with expected cost at most $\frac{e}{e-1}\mathrm{OPT}(\sigma)$ against an oblivious adversary. No randomized algorithm does better against an oblivious adversary; this matching lower bound is due to Seiden (2000).

## Reductions

- **From ski rental.** With one batch in view, the receiver must choose between paying latency as it goes, like renting, and paying the acknowledgment cost, like buying, while the end of the batch is unknown. Karlin, Kenyon and Randall cut the problem into a family of such [ski rental](/ski-rental-problem/) decisions, and the randomized ski rental ratio $e/(e-1)$ carries over.
- **To an online covering linear program.** Each packet and each time after its arrival form a covering constraint, with variables for acknowledgments and for latency. The [online primal-dual](/online-primal-dual/) method raises these variables at a rate that keeps the dual within a factor $e/(e-1)$.
- **To joint replenishment.** The TCP problem is the joint replenishment problem with one item type, so lower bounds for the TCP problem hold for joint replenishment.

## Applications

- **Delayed acknowledgments in TCP.** TCP receivers delay acknowledgments to send fewer of them and to piggyback them on data. Common stacks use a fixed timer, often 200 ms, or acknowledge every second segment. DGS study adaptive rules of this kind against a fixed timer. The related [Nagle algorithm](/nagle-algorithm/) batches outgoing small segments for the same reason.
- **Batching in general.** Any service that can group requests at a fixed cost per group, such as message aggregation in sensor networks, write batching in storage systems and order batching in supply chains, has the same tradeoff between the cost of a batch and the delay of waiting.

## References
