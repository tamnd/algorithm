---
tag: YB4A74
kind: algorithm
slug: auction-algorithm
name: Auction algorithm
aliases:
- Bertsekas auction algorithm
area: graphs/matching
level: advanced
summary: Solves the assignment problem by simulating bidding among persons for objects with epsilon-scaled prices.
solves: [assignment-problem]
model: word-ram
complexity:
  vars: {n: the number of persons and of objects, C: the largest difference between two benefits}
  time: {worst: O(n^3 C + n^2)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 1979
  people: [Dimitri Bertsekas]
  note: Bertsekas proposed the auction algorithm in a 1979 MIT report on distributed assignment, and with Eckstein added epsilon-scaling, which makes it polynomial, in 1988.
prereqs: [assignment-problem]
see_also: [hungarian-algorithm, complementary-slackness, lp-duality, cost-scaling, push-relabel, min-cost-flow-problem, gale-shapley, bottleneck-matching]
sources:
  - paper: doi:10.1007/BF02186476
    title: Dimitri P. Bertsekas, The auction algorithm, a distributed relaxation method for the assignment problem, Annals of Operations Research 14, 105 to 123 (1988)
    locator: the whole paper (the bidding phase, epsilon-complementary slackness and the scaling analysis)
  - book: isbn:9781886529021
    title: Dimitri P. Bertsekas, Network Optimization, Continuous and Discrete Models, Athena Scientific (1998)
    locator: Chapter 7, Auction algorithms (Section 7.1, the auction algorithm for the assignment problem)
  - book: isbn:9780898716634
    title: Rainer Burkard, Mauro Dell'Amico and Silvano Martello, Assignment Problems, SIAM (2009)
    locator: Chapter 4, Linear sum assignment problem (the section on auction algorithms)
---

The auction algorithm solves the [assignment problem](/assignment-problem/) by running an auction. Each object has a price; an unassigned person bids for the object that gives the best value, benefit minus price, and raises its price by the gap to the second best value plus a small step $\varepsilon$. The previous owner is outbid and bids again later. Prices only go up, and when every person holds an object, the assignment is within $n\varepsilon$ of optimal. With integer benefits and $\varepsilon < 1/n$ it is optimal. The graph is bipartite and weighted: persons on one side, objects on the other, a benefit on each pair. The algorithm was designed by Dimitri Bertsekas for parallel and distributed machines.

## In plain words

Picture a room of buyers and a set of houses, one house per buyer. Each buyer values each house differently, and every house has a price that starts at zero. A buyer without a house looks at what each house is worth to them minus its price, picks the best deal, and raises that house's price by exactly as much as keeps it the best deal, plus one small coin. Whoever held the house before is pushed out and goes shopping again.

Prices only rise, so popular houses get expensive and buyers spread out to the houses they really prefer. The small coin makes sure prices keep moving, so the auction cannot go on forever. When everyone has a house, no buyer could do better by more than one coin. If the values are whole numbers and the coin is small enough, the result is the best possible assignment.

## The problem

The input is an $n \times n$ benefit matrix $A = (a_{ij})$: person $i$ values object $j$ at $a_{ij}$, an integer, or a pair is forbidden. The output is a permutation $\sigma$, person $i$ getting object $\sigma(i)$, that maximizes $\sum_i a_{i\sigma(i)}$, or the answer that no permutation avoids the forbidden pairs. Minimum cost is the same problem with $a_{ij} = -c_{ij}$. This is the [assignment problem](/assignment-problem/), the weighted [perfect matching](/perfect-matching/) problem in the complete [bipartite graph](/bipartite-graph/) $K_{n,n}$ or in a subgraph of it. For $n = 0$ the empty assignment, of value 0, is the answer.

**Prices and $\varepsilon$-complementary slackness.** With a price $p_j$ on each object, the *value* of object $j$ to person $i$ is $a_{ij} - p_j$. A partial assignment satisfies $\varepsilon$-complementary slackness ($\varepsilon$-CS) if every assigned person $i$, holding $j$, has

$$a_{ij} - p_j \ge \max_k \, (a_{ik} - p_k) - \varepsilon.$$

With $\varepsilon = 0$ this is [complementary slackness](/complementary-slackness/) for the [linear programming dual](/lp-duality/) of the assignment problem, whose variables are the prices $p_j$ and the profits $\pi_i = \max_k (a_{ik} - p_k)$.

**Assumptions.** Benefits are integers, as on most inputs; rational benefits can be scaled to integers. The implementation multiplies every benefit by $n + 1$ and uses $\varepsilon = 1$, which is the same as $\varepsilon = 1/(n + 1)$ on the original scale.

## The algorithm

The version below is the Gauss-Seidel auction: one person bids at a time. Write $a'_{ij}$ for the scaled benefits.

```pseudo id=main
AUCTION(A)
L1  p[j] ← 0 for every object j;  every person and every object is unassigned
L2  a'[i][j] ← (n + 1) · a[i][j], with forbidden pairs set to a very low benefit
L3  Q ← a queue of all persons
L4  while Q is not empty do i ← DEQUEUE(Q)
L5      j* ← an object maximizing a'[i][j] − p[j];  v ← a'[i][j*] − p[j*]
L6      w ← max over j ≠ j* of a'[i][j] − p[j], or w ← v if n = 1
L7      p[j*] ← p[j*] + (v − w) + 1
L8      if j* has an owner k then unassign k;  ENQUEUE(Q, k)
L9      assign j* to i
L10 return the assignment, or "infeasible" if it uses a forbidden pair
```

Line L5 finds the best object for the bidder, and line L6 the second best value. Line L7 is the bid: it raises the price of $j^*$ until the value of $j^*$ to the bidder is $w - 1$, exactly $\varepsilon = 1$ below the second best value, so the bidder holds $j^*$ within $\varepsilon$ of its best choice. The increment $v - w + 1$ is at least 1, so every bid moves a price. Lines L8 and L9 hand the object to the bidder and send the outbid person back to the queue. The queue always holds exactly the unassigned persons.

A forbidden pair gets the benefit $\ell - n(h - \ell) - 1$, where $\ell$ and $h$ are the smallest and largest allowed benefits. An assignment that uses such a pair is worse than every assignment that does not, so line L10 reports infeasibility exactly when no permutation avoids the forbidden pairs, as when [Hall's condition](/hall-theorem/) fails.

## Example

Take $n = 3$ and

$$A = \begin{pmatrix} 10 & 5 & 8 \\ 9 & 2 & 3 \\ 7 & 6 & 4 \end{pmatrix}, \qquad A' = 4A = \begin{pmatrix} 40 & 20 & 32 \\ 36 & 8 & 12 \\ 28 & 24 & 16 \end{pmatrix}.$$

All prices start at 0, and persons 1, 2, 3 bid in this order.

| bid | bidder | values $a'_{ij} - p_j$ | $j^*$, $v$, $w$ | new price | outbid | prices after |
|---|---|---|---|---|---|---|
| 1 | 1 | 40, 20, 32 | 1, 40, 32 | $p_1 = 9$ | none | 9, 0, 0 |
| 2 | 2 | 27, 8, 12 | 1, 27, 12 | $p_1 = 25$ | 1 | 25, 0, 0 |
| 3 | 3 | 3, 24, 16 | 2, 24, 16 | $p_2 = 9$ | none | 25, 9, 0 |
| 4 | 1 | 15, 11, 32 | 3, 32, 15 | $p_3 = 18$ | none | 25, 9, 18 |

Person 2 wants object 1 badly, since its other objects are worth little, and outbids person 1 by a wide margin. Person 1 moves to object 3. The result is $\sigma = (3, 1, 2)$ with benefit $8 + 9 + 6 = 23$, the optimum of the six permutations. On the original scale the prices are $p = (6.25, 2.25, 4.5)$ and the profits $\pi_i = \max_j (a_{ij} - p_j)$ are $3.75, 2.75, 3.75$, so the dual value $\sum_j p_j + \sum_i \pi_i = 23.25$ is within $n\varepsilon = 0.75$ of 23, which certifies optimality for integers.

**No perfect matching.** With $A = \begin{pmatrix} 5 & \times \\ 7 & \times \end{pmatrix}$, where $\times$ marks a forbidden pair, both persons want only object 1. The auction ends with a forbidden pair in the assignment, and line L10 reports that no feasible assignment exists.

**Edge cases.** With $n = 0$ the queue is empty and the empty assignment is returned with no bid. With $n = 1$, line L6 sets $w = v$, so the single bid raises the price by 1. When all benefits are equal, every bid raises a price by exactly 1, and each person gets the first free object it sees.

## Correctness

The invariant is $\varepsilon$-CS, with $\varepsilon = 1$ on the scaled benefits. After a bid by $i$ for $j^*$, the value of $j^*$ to $i$ is $w - 1$, and every other object is worth at most $w$ to $i$, so $i$ satisfies 1-CS. Other assigned persons keep their objects and prices, while other prices only rise, so their condition still holds. The auction stops: while some object has never received a bid, its price is 0, which bounds every price by about $(n + 1)C$, and every bid raises a price by at least 1. Once every object has received a bid, every object has an owner, so every person is assigned and the queue is empty. At the end, 1-CS bounds the gap to any other assignment by $n$ on the scaled benefits, which is $n/(n + 1) < 1$ on the original scale, so for integers the assignment is optimal. The full proof is in the proof files below.

## Complexity

The model is the [word RAM](/word-ram/).

- **Bids.** Let $C$ be the largest difference between two benefits. While some object $j_0$ has received no bid, a bid by $i$ for $j$ sets $p_j = a'_{ij} - w + 1 \le a'_{ij} - a'_{ij_0} + 1 \le (n + 1)C + 1$. Each object gets at most $(n + 1)C + 1$ bids before the last object gets its first one, which ends the auction. So there are at most $n((n + 1)C + 2)$ bids, $O(n^2 C + n)$.
- **One bid** scans a row of $A'$ in $O(n)$ time.
- **Total.** $O(n^3 C + n^2)$ time, pseudo-polynomial, and $\Theta(n^2)$ space for the scaled matrix. Forbidden pairs raise $C$ to about $(n + 1)C$.
- **With $\varepsilon$-scaling**, below, the bound becomes polynomial, $O(n m \log(nC))$ for $m$ allowed pairs, by Bertsekas and Eckstein.

The full argument is in the complexity proof below.

## Properties

- **Exact for integers.** With $\varepsilon < 1/n$ and integer benefits the result is optimal; with a larger $\varepsilon$ it is within $n\varepsilon$ of optimal.
- **Dual certificate.** The final prices $p_j$ and profits $\pi_i = \max_k (a_{ik} - p_k)$ form a dual solution whose value exceeds the assignment by at most $n\varepsilon$.
- **Monotone prices.** Prices never fall, and once an object is assigned it stays assigned, to some person.
- **Order-dependent.** The final assignment and prices depend on the order of bids, but the value does not when the result is optimal.
- **Local and parallel.** A bid reads one row and the prices; many persons can compute bids at once, and an object accepts the highest bid. This Jacobi form suits parallel and distributed machines.
- **Sensitive to the gap.** The number of bids grows with $C/\varepsilon$, and inputs where several persons compete for the same few objects with close values show the pseudo-polynomial bound; these are the price wars.

## Variants and improvements

- **$\varepsilon$-scaling.** Run the auction with a large $\varepsilon$, then divide $\varepsilon$ by a constant such as 4 or 7 and run again from the current prices, until $\varepsilon < 1/n$. Each stage starts with prices that are almost right, so it needs few bids; Bertsekas and Eckstein proved $O(n m \log(nC))$ time.
- **Jacobi auction.** All unassigned persons bid at the same time against the same prices, and each object takes the highest bid; the parallel version.
- **Forward and reverse auction.** Objects also bid for persons by lowering their prices; alternating the two directions reduces price wars, and handles asymmetric problems with more objects than persons.
- **Min-cost flow.** The same idea, prices and $\varepsilon$-CS, gives auction algorithms for transportation and [min-cost flow](/min-cost-flow-problem/) problems; Goldberg's [cost-scaling](/cost-scaling/) method is a close relative, and the bid is a [push-relabel](/push-relabel/) step on the assignment network.
- **Shortest paths.** Bertsekas also gave an auction algorithm for single-pair shortest paths.
- **Economics.** Demange, Gale and Sotomayor's exact ascending auction finds Walrasian prices for unit-demand buyers; the auction algorithm is its numerical cousin, much as [Gale-Shapley](/gale-shapley/) is the stable-matching counterpart.

## When to use it

Use the auction algorithm for large sparse or parallel assignment problems, where its local bids beat the global searches of the [Hungarian algorithm](/hungarian-algorithm/), and inside min-cost flow solvers. With $\varepsilon$-scaling it is competitive with the best codes on many sparse benchmarks. For small dense problems, or when a strongly polynomial bound is needed, the Hungarian algorithm in $O(n^3)$ time is simpler and does not depend on the size of the benefits. Without scaling, the auction is a good teaching example of dual prices, but price wars make it slow on hard inputs.

## Pitfalls

- **$\varepsilon$ too large.** With $\varepsilon \ge 1/n$ on integer benefits, the result can be suboptimal by up to $n\varepsilon$. Scale the benefits by $n + 1$, as here, or run until $\varepsilon < 1/n$.
- **Zero increment.** Without the $+\varepsilon$ in line L7, a bid can leave the price unchanged when the two best values tie, and two persons can swap the same object forever.
- **Infeasible problems.** With forbidden pairs and no perfect matching, the plain auction never stops: prices of the contested objects rise without bound. Use the big-benefit trick, as here, or check feasibility first with [Hopcroft-Karp](/hopcroft-karp/).
- **Floating point.** Real-valued benefits with a tiny $\varepsilon$ lose precision as prices grow; scale to integers and use $\varepsilon = 1$.
- **Unbalanced problems.** With more objects than persons, the plain auction is optimal only if unassigned objects keep their initial prices; otherwise use a reverse auction phase or add dummy persons.
- **Second best with one object.** For $n = 1$ there is no second object, and line L6 must set $w = v$.

## Implementations

The Python version takes a square matrix of integers, with `None` for a forbidden pair, and returns the assignment, its value, the final prices on the scaled benefits, and the number of bids, or `None` for the assignment when no feasible one exists. An optional callback reports each bid. It scales by $n + 1$, uses $\varepsilon = 1$ and a queue of unassigned persons, without $\varepsilon$-scaling, so its time is pseudo-polynomial.

## History

Dimitri Bertsekas introduced the auction algorithm in a 1979 MIT report on a distributed algorithm for the assignment problem, and gave a full account in 1988 in the Annals of Operations Research. Bertsekas and Jonathan Eckstein added $\varepsilon$-scaling in 1988 and proved a polynomial bound. The idea of prices that rise under bids goes back to economic models of markets, and Demange, Gale and Sotomayor described an exact auction for assignment markets in 1986. Bertsekas later extended the method to transportation, min-cost flow and shortest path problems, and studied its parallel versions.

## References
