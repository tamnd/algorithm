---
tag: 0Y15BJ
kind: problem
slug: ofdma-resource-allocation
name: OFDMA resource allocation
aliases:
- subcarrier and power allocation
area: communications/link-adaptation-and-resource-allocation
level: advanced
summary: Assign subcarriers, bits and powers to the users of an OFDMA system to meet their rates with least power or most utility.
prereqs: [orthogonal-frequency-division-multiple-access, water-filling-power-allocation]
see_also: [orthogonal-frequency-division-multiple-access, water-filling-power-allocation, bit-loading, hughes-hartogs-algorithm, multiuser-diversity, max-rate-scheduling, proportional-fair-scheduling, lagrangian-duality]
sources:
  - paper: doi:10.1109/49.793310
    title: "Cheong Yui Wong, Roger S. Cheng, Khaled Ben Letaief and Ross D. Murch, Multiuser OFDM with adaptive subcarrier, bit, and power allocation, IEEE Journal on Selected Areas in Communications 17(10), 1999, pages 1747 to 1758"
    locator: "the margin-adaptive problem of least total power under per-user bit targets, its relaxation with time-shared subcarriers, and the iterative subcarrier allocation that follows from it"
  - paper: doi:10.1109/JSAC.2002.807348
    title: "Jiho Jang and Kwang Bok Lee, Transmit power adaptation for multiuser OFDM systems, IEEE Journal on Selected Areas in Communications 21(2), 2003, pages 171 to 178"
    locator: "the proof that, for the sum rate under a total power limit, each subcarrier goes to the user with the best gain and the power is water-filled over the subcarriers"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Chapter 6 (multiuser capacity and opportunistic communication), on the uplink and downlink of fading channels with many users"
---

OFDMA resource allocation is the problem of sharing the subcarriers and the power of an [OFDMA](/orthogonal-frequency-division-multiple-access/) system among its users. Each subcarrier goes to one user, and each subcarrier then gets a power and a number of bits. The channel of each user changes across the band, so each subcarrier is strong for some users and weak for others, and the assignment decides how much the system gets from these differences. With a total power limit and the sum rate as the goal, the answer is simple: give each subcarrier to the user with the best gain, then apply [water-filling](/water-filling-power-allocation/) over the subcarriers. With a rate target for each user, the problem becomes a mixed integer program: the assignment is a discrete choice, and the power on each user's subcarriers follows from it. Wong, Cheng, Letaief and Murch (1999) relaxed the integer choice to time sharing, which makes the problem convex, and most practical methods round or search near that relaxation.

## In plain words

A wide channel is cut into many narrow pieces, and several users share them. Each user hears some pieces well and others badly, and the good pieces are different for each user. The base station decides which user gets which piece, and how much power to put on each piece. If it only wants the most total data, it gives each piece to the user who hears it best and puts more power where the channel is good. But then a user who is far away may get almost nothing. If every user must get a fixed amount of data, the station must sometimes give a piece to a user who is not the best one for it, so that each user gets enough. Finding the best way to do this is a hard choice when there are many pieces and many users.

## Definition

**Input.** $K$ users, $N$ subcarriers, gains $g_{k,n} > 0$ (the SNR of user $k$ on subcarrier $n$ per unit power, including the noise), and a power limit $\bar P$ or rate targets $r_k$.

**Variables.** An assignment $a_{k,n} \in \{0, 1\}$ with $\sum_k a_{k,n} \le 1$ for every $n$, and powers $p_{k,n} \ge 0$ with $p_{k,n} = 0$ when $a_{k,n} = 0$. The rate of user $k$ is

$$R_k = \sum_{n} a_{k,n} \log_2(1 + g_{k,n}\, p_{k,n}) \quad \text{bits per OFDM symbol.}$$

With a finite set of modulations, $\log_2(1 + g p)$ is replaced by the integer number of bits that the power supports at the target error rate, as in [bit loading](/bit-loading/).

**Two standard forms.**

- **Margin adaptive.** Minimize $\sum_{k,n} p_{k,n}$ subject to $R_k \ge r_k$ for every $k$.
- **Rate adaptive.** Maximize a utility of the rates, such as $\sum_k R_k$, $\sum_k w_k R_k$ or $\min_k R_k$, subject to $\sum_{k,n} p_{k,n} \le \bar P$.

**Output.** The assignment and the powers.

## Variants

- **Weighted sum rate.** Weights $w_k$ from a scheduler, for example the inverse average rates of [proportional fair scheduling](/proportional-fair-scheduling/), turn each time slot into a weighted sum rate problem.
- **Max-min rate.** Maximize $\min_k R_k$, or the rates in fixed proportions $R_1 : R_2 : \cdots : R_K$, under the power limit.
- **Resource blocks.** Real systems assign groups of adjacent subcarriers over several symbols, and often require equal power across the band or one modulation per user; this lowers the number of choices but adds constraints.
- **Uplink.** Each user has its own power limit, so the constraint $\sum_{n} p_{k,n} \le \bar p_k$ replaces the total limit.
- **Multicell.** When neighboring cells reuse the subcarriers, each rate depends on the powers in the other cells, and the problem has the interference of [weighted sum rate maximization](/weighted-sum-rate-maximization/) on each subcarrier.
- **Discrete rates.** With integer bits and a finite set of modulations, each user's power for a given set of subcarriers is found by greedy bit loading, as in the [Hughes-Hartogs algorithm](/hughes-hartogs-algorithm/).

## Examples

Two users and four subcarriers, with gains

| | $n = 1$ | $n = 2$ | $n = 3$ | $n = 4$ |
|---|---|---|---|---|
| user 1 | 10 | 8 | 6 | 1 |
| user 2 | 9 | 2 | 5 | 4 |

**Sum rate with $\bar P = 4$.** User 1 has the best gain on subcarriers 1, 2 and 3, and user 2 on subcarrier 4. Water-filling over the gains $(10, 8, 6, 4)$ gives the level $\mu = 1.1604$, powers $(1.0604, 1.0354, 0.9938, 0.9104)$, and a sum rate of $11.765$ bits per symbol. A search over all $2^4 = 16$ assignments confirms that this is the best; the next best gives $11.627$. But user 1 gets $9.551$ bits and user 2 only $2.215$.

**Least power for the rates $(4, 4)$.** The assignment of the sum rate example needs $4.324$ in total: user 1 water-fills $4$ bits over gains $(10, 8, 6)$ with $0.574$, but user 2 must send $4$ bits on subcarrier 4 alone, which costs $(2^4 - 1)/4 = 3.75$. The best of the 16 assignments gives subcarriers 2 and 3 to user 1 and subcarriers 1 and 4 to user 2. User 2 is not the best user on subcarrier 1 ($9$ against $10$), but the small loss there gives it a second good subcarrier for its rate. The powers are $0.863$ and $0.972$, a total of $1.835$, less than half of the first assignment. With the targets $(3, 5)$ the best total is $2.001$, with only subcarrier 2 for user 1.

**Max-min rate with $\bar P = 4$.** The same assignment, subcarriers 2 and 3 to user 1 and 1 and 4 to user 2, gives both users $5.806$ bits. The total, $11.612$, is only $1.3\%$ below the largest sum rate, while the smaller rate rises from $2.215$ to $5.806$.

## Known algorithms

- **Best user and water-filling (sum rate).** Jang and Lee (2003) show that, for the sum rate under a total power limit, each subcarrier goes to the user with the largest $g_{k,n}$, and the power is water-filled over the $N$ resulting gains. The cost is $O(KN + N \log N)$. The result is the frequency form of [max-rate scheduling](/max-rate-scheduling/), and the gain it gets from many users is [multiuser diversity](/multiuser-diversity/).
- **Time-sharing relaxation.** Wong, Cheng, Letaief and Murch (1999) let user $k$ use a fraction $\rho_{k,n} \in [0, 1]$ of subcarrier $n$, with $\sum_k \rho_{k,n} \le 1$. The power $\rho_{k,n} (2^{c_{k,n} / \rho_{k,n}} - 1) / g_{k,n}$ for $c_{k,n}$ bits is a perspective of a convex function, so the relaxed problem is convex. Its solution gives a lower bound on the least power and a starting assignment, which is then rounded.
- **Lagrange dual methods.** Put a multiplier $\lambda_k$ on each rate constraint. For fixed multipliers, the [dual problem](/lagrangian-duality/) splits over the subcarriers: each subcarrier goes to the user with the best value of a one-line function of $g_{k,n}$ and $\lambda_k$, and its power is a water-filling formula. The multipliers are then updated by subgradient steps or bisection. The cost per iteration is $O(KN)$. When the number of subcarriers is large, the duality gap of these problems is small, and the dual solution is close to optimal (Yu and Lui, 2006).
- **Greedy heuristics.** Assign subcarriers one at a time, each to the user that is furthest below its target or that gains the most from it, then load bits by greedy bit loading. Rhee and Cioffi (2000) proposed this for max-min rate with equal power per subcarrier, and Shen, Andrews and Evans (2005) for rates in fixed proportions.
- **Exact search.** For small $K$ and $N$, a search over the $K^N$ assignments with water-filling for each, or branch and bound on the mixed integer program, gives the global optimum.

## Bounds

- **Sum rate.** The best-user rule with water-filling is optimal, so the sum rate problem is solved in polynomial time for any $K$ and $N$.
- **Time sharing.** The relaxed problem is convex and its optimum is a lower bound on the least total power, and an upper bound on any rate utility of the integer problem. When the time-shared solution gives each subcarrier to one user, it is also optimal for the integer problem.
- **Hardness.** With interference between cells, the choice of an interference-free set of subcarriers for each link is NP-hard in general (Hayashi and Luo, 2009). For a single cell with rate targets, exact integer methods take time exponential in $N$ in the worst case, and the methods in common use are dual or greedy.
- **Cost of fairness.** In the example, fairness costs little: the rate targets move only one subcarrier away from its best user, and the sum rate falls by $1.3\%$. With very unequal path losses the loss is larger, because the weak user needs many subcarriers on which another user is much stronger.

## Reductions

- **To water-filling.** For a fixed assignment, the least power for user $k$ to reach $r_k$ over its subcarriers is a water-filling with the level set by the rate, and the largest rate under a power budget is ordinary water-filling.
- **To an assignment problem.** If each user gets a fixed number of subcarriers and the power per subcarrier is fixed, the choice of subcarriers is an [assignment problem](/assignment-problem/) on a bipartite graph, solved by the [Hungarian algorithm](/hungarian-algorithm/).
- **From weighted sum rate.** Each time slot of a scheduler with weights is a weighted sum rate OFDMA problem: each subcarrier goes to the user with the largest $w_k \log_2(1 + g_{k,n} p_{k,n})$ at the water level of that user.
- **To a knapsack-like choice.** With discrete rates, giving bits to users under a power budget has the structure of the [knapsack problem](/knapsack-problem/); greedy loading is optimal for one user because the power cost of each extra bit grows.

## Applications

- **Cellular downlink and uplink.** LTE and 5G NR base stations assign resource blocks to users in each slot from the users' channel reports and their weights.
- **Wi-Fi 6 and later.** IEEE 802.11ax splits the channel into resource units that the access point assigns to several stations at once.
- **Digital subscriber lines and cable.** Shared multicarrier links allocate tones among users with the same water-filling tools.
- **Scheduling studies.** The best-user rule over subcarriers is the standard model of opportunistic scheduling across frequency, used to measure multiuser diversity.

## References
