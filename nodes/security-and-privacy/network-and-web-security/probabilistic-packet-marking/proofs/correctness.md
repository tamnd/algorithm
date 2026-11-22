---
title: Correctness of probabilistic packet marking (edge sampling)
proves: [correctness]
status: full
---

**Setting.** The path is $R_1, \ldots, R_d$ with $R_d$ next to the victim $v$, and we write $R_{d+1} = v$. The path is fixed, and no router on it is compromised. The attacker chooses the initial mark $w_0 = (s_0, e_0, k_0)$ of every packet with $0 \le k_0 \le 31$, and may choose it as a function of everything except the draws of the routers on the path. Each router runs MARK of the main page with a fresh uniform draw, independent of all other draws. We assume $d \le 31$, so the saturated distance field never hides a path length.

**Lemma 1 (the mark at the victim).** Fix one packet. Let $J$ be the position of the last router on the path that marks it, if any. If $J = i$, the mark at $v$ is $(R_i, \text{nil}, 0)$ when $i = d$ and $(R_i, R_{i+1}, d - i)$ when $i < d$. If no router marks, the mark at $v$ has distance $\min(k_0 + d, 31) \ge d$.

*Proof.* After a router marks (line L3), the mark is $(R_i, \text{nil}, 0)$. The routers $R_{i+1}, \ldots, R_d$ do not mark, by the choice of $i$. Each of them runs lines L4 to L6. By induction on $t = 0, \ldots, d - i$, after the router $R_{i+t}$ the distance is $t$, and for $t \ge 1$ the end field is $R_{i+1}$: at $t = 1$ the distance before $R_{i+1}$ is 0, so line L5 writes $R_{i+1}$; for $t \ge 2$ the distance before $R_{i+t}$ is $t - 1 \ge 1$, so line L5 does not run and the end field stays $R_{i+1}$. Since $t \le d \le 31$, the minimum in line L6 equals $t$. For $t = d - i$ this gives the claim. If no router marks, each of the $d$ routers runs line L6 once, and the distance is $\min(k_0 + d, 31)$, which is at least $d$ because $k_0 \ge 0$ and $d \le 31$. $\square$

**Lemma 2 (the probabilities).** For $j = 1, \ldots, d$, the mark at $v$ yields the edge $f_j = (R_{d-j+1}, R_{d-j+2}, j - 1)$ (after line L9 turns $(R_d, \text{nil}, 0)$ into $(R_d, v, 0)$) with probability $q_j = p(1-p)^{j-1}$, and these events are independent across packets.

*Proof.* By Lemma 1 the edge $f_j$ arrives exactly when the router $R_{d-j+1}$ marks and the $j - 1$ routers after it do not. These are independent events of probabilities $p$ and $1 - p$, so the probability is $p(1-p)^{j-1}$. Different packets use independent draws. The attacker's choice of $w_0$ does not change this event, because line L3 discards $w_0$. $\square$

**Lemma 3 (forged edges sit beyond the suffix).** Every edge in $E$ (after lines L8 to L10) is either some $f_j$ or has distance at least $d$.

*Proof.* By Lemma 1, a mark at $v$ either comes from a router on the path, and then gives some $f_j$, or no router marked it, and then its distance is at least $d$. $\square$

**Theorem 1 (reconstruction).** If $E$ contains every $f_j$, then RECONSTRUCT keeps every $f_j$, every other kept edge has distance at least $d$, and every maximal chain of kept edges ends with $(R_1, \ldots, R_d, v)$ or contains it as a suffix.

*Proof.* Line L11 keeps the edges level by level: at level $k = 0$ the edges $(x, v, 0)$, at level $k \ge 1$ the edges $(x, y, k)$ whose end $y$ is the start of a kept edge at level $k - 1$. By induction on $k = 0, \ldots, d - 1$, the edge $f_{k+1}$ is kept: $f_1 = (R_d, v, 0)$ is kept at level 0, and $f_{k+1} = (R_{d-k}, R_{d-k+1}, k)$ ends at $R_{d-k+1}$, the start of the kept $f_k$. By Lemma 3, every kept edge other than the $f_j$ has distance at least $d$. A chain toward $v$ visits kept edges with distances $0, 1, 2, \ldots$ in order, and the edges at distances $0, \ldots, d - 1$ that end at the start of the previous edge are the $f_j$ only, by Lemma 3. So the last $d$ edges of every chain of length at least $d$ are $f_d, \ldots, f_1$, which spell $(R_1, \ldots, R_d, v)$. $\square$

The algorithm is therefore a robust solution of approximate traceback against this attacker: a forged mark can add edges only at distance $d$ or more, before $R_1$.

**Theorem 2 (expected number of packets).** Let $X$ be the number of packets until every $f_j$ has arrived. Then

$$
E[X] = \sum_{\emptyset \ne S \subseteq \{1, \ldots, d\}} \frac{(-1)^{|S|+1}}{\sum_{j \in S} q_j} \le \frac{H_d}{p(1-p)^{d-1}} ,
$$

where $H_d = 1 + 1/2 + \cdots + 1/d$.

*Proof of the equality.* Let $T_j$ be the index of the first packet that yields $f_j$, so $X = \max_j T_j$. For $n \ge 0$, $\Pr[X > n] = \Pr[\bigcup_j \{T_j > n\}]$. For a nonempty set $S$, the event $\bigcap_{j \in S} \{T_j > n\}$ says that none of the first $n$ packets yields an edge of $S$. The edges $f_j$ are disjoint outcomes of one packet, so a packet yields an edge of $S$ with probability $Q_S = \sum_{j \in S} q_j$, and the event has probability $(1 - Q_S)^n$. By inclusion and exclusion,

$$
\Pr[X > n] = \sum_{\emptyset \ne S} (-1)^{|S|+1} (1 - Q_S)^n .
$$

Summing over $n \ge 0$ with $E[X] = \sum_{n \ge 0} \Pr[X > n]$ and $\sum_{n \ge 0} (1 - Q_S)^n = 1 / Q_S$ (valid since $0 < Q_S \le 1$; the sums are finite, so the order of summation can be changed) gives the equality.

*Proof of the bound.* Let $q = \min_j q_j = p(1-p)^{d-1}$. Split the time into phases: phase $i$, for $i = 0, \ldots, d - 1$, starts when exactly $i$ distinct edges of the path have arrived and ends when one more arrives. During phase $i$, $d - i$ edges are missing, and each packet yields one of them with probability $\sum_{j \text{ missing}} q_j \ge (d - i) q$, independently of earlier packets. So the length of phase $i$ is a geometric random variable with success probability at least $(d - i) q$, and its mean is at most $1 / ((d - i) q)$. By linearity of expectation,

$$
E[X] \le \sum_{i=0}^{d-1} \frac{1}{(d - i) q} = \frac{H_d}{q} = \frac{H_d}{p(1-p)^{d-1}} .
$$

$\square$

**Remark (the printed estimate).** Savage et al. state $E[X] < \ln(d)/(p(1-p)^{d-1})$. Since $H_d > \ln d$, this does not follow from the argument above, and it is false in general: for $d = 2$ and $p = 1/25$ the equality of Theorem 2 gives $E[X] \approx 38.29$, while $\ln(2)/(p(1-p)) \approx 18.05$. For $d = 10$ and $p = 1/25$ the exact value is about 89.57 and the estimate is about 83.12. The bound with $H_d$ gives about 105.73 there. $\blacksquare$
