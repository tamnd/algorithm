---
tag: A0QXGV
kind: theorem
slug: cremer-mclean-theorem
name: Cremer-McLean theorem
aliases:
- full surplus extraction
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: "With finitely many correlated types, a seller can take the whole expected surplus: by a BIC, interim IR auction under convex independence, and a DSIC one under full rank."
prereqs: [bayesian-incentive-compatibility, individual-rationality, vickrey-auction, farkas-lemma]
see_also: [myerson-optimal-auction, myerson-satterthwaite-theorem, agv-mechanism, revenue-equivalence-theorem, common-value-auction, linkage-principle, separating-hyperplane-theorem, automated-mechanism-design]
sources:
  - paper: doi:10.2307/1913096
    title: "Jacques Cremer and Richard P. McLean, Full extraction of the surplus in Bayesian and dominant strategy auctions, Econometrica 56(6) (1988), 1247-1257"
    locator: the full extraction results for finite type spaces, in Bayes-Nash equilibrium under convex independence of the beliefs and in dominant strategies under the full rank condition
  - paper: doi:10.2307/1911240
    title: "Jacques Cremer and Richard P. McLean, Optimal selling strategies under uncertainty for a discriminating monopolist when demands are interdependent, Econometrica 53(2) (1985), from p. 345"
    locator: the earlier dominant-strategy version with interdependent demands
  - paper: doi:10.2307/2951601
    title: "R. Preston McAfee and Philip J. Reny, Correlated information and mechanism design, Econometrica 60(2) (1992), from p. 395"
    locator: the extension to continuous type spaces, where the surplus can be extracted approximately
---

The Cremer-McLean theorem says that when the private information of bidders is correlated, an auctioneer can usually extract the whole expected surplus: the item goes to the bidder who values it most, and every bidder type is left with an expected utility of exactly zero. The tool is a side bet on the other bidders' reports, which costs nothing in expectation to a truthful bidder but is costly to a bidder who lies about its type, because its true beliefs about the others differ. With independent types the result fails, and the information rents of [Myerson's optimal auction](/myerson-optimal-auction/) cannot be removed; this is how the theorem differs from the independent private values results of the area.

## Statement

There are $n \ge 2$ bidders and one item. Bidder $i$ has a type $t_i$ from a finite set $T_i$ and the private value $v_i(t_i) \ge 0$. The types are drawn from a joint prior $\pi$ on $T = T_1 \times \cdots \times T_n$ with $\pi(t) > 0$ for every profile. Bidder $i$ of type $t_i$ has the belief $\pi_i(\cdot \mid t_i)$ on $T_{-i}$. Utilities are quasilinear and bidders are risk neutral. Let $\Pi_i$ be the $|T_i| \times |T_{-i}|$ matrix whose row $t_i$ is the belief $\pi_i(\cdot \mid t_i)$.

- **Convex independence** holds for bidder $i$ if no row of $\Pi_i$ is a convex combination of the other rows.
- **Full rank** holds for bidder $i$ if the rows of $\Pi_i$ are linearly independent, that is $\Pi_i$ has rank $|T_i|$. Full rank implies convex independence.

The full surplus is $S = \mathbb{E}_t[\max_i v_i(t_i)]$, the expected welfare of the efficient allocation. No interim IR mechanism can earn more than $S$, because each bidder's expected utility is at least 0.

**Theorem (Cremer and McLean 1988).**

1. If full rank holds for every bidder, there is a DSIC mechanism that is interim IR, allocates efficiently and has expected revenue $S$.
2. If convex independence holds for every bidder, there is a BIC mechanism that is interim IR, allocates efficiently and has expected revenue $S$.

In both cases every type of every bidder has interim expected utility exactly 0. The paper also covers values that depend on all types and shows that, for the dominant-strategy version, the full rank condition cannot be weakened. This page proves the private value case.

### Example

Two bidders have values in $\{1, 2\}$ (types L and H) with $\pi(L, L) = \pi(H, H) = 1/3$ and $\pi(L, H) = \pi(H, L) = 1/6$. A bidder of type L believes the other is L with probability $2/3$, and a bidder of type H believes the other is H with probability $2/3$. The belief matrix of each bidder is $\Pi = \begin{pmatrix} 2/3 & 1/3 \\ 1/3 & 2/3 \end{pmatrix}$, which has full rank.

In the [Vickrey auction](/vickrey-auction/), with a fair coin for ties, a type L bidder gets 0 and a type H bidder gets 1 when the other is L, so its interim utility is $U(H) = 1/3$ and $U(L) = 0$. The revenue is $\frac{1}{3} \cdot 1 + \frac{1}{3} \cdot 2 + \frac{1}{3} \cdot 1 = 4/3$, while $S = \frac{1}{3} \cdot 1 + \frac{2}{3} \cdot 2 = 5/3$.

Add to bidder $i$'s payment a bet $z(t_j)$ that depends only on the other's report and solves $\Pi z = U$:

$$\tfrac{2}{3} z(L) + \tfrac{1}{3} z(H) = 0, \qquad \tfrac{1}{3} z(L) + \tfrac{2}{3} z(H) = \tfrac{1}{3},$$

so $z(L) = -1/3$ and $z(H) = 2/3$: the bidder receives $1/3$ if the other reports L and pays $2/3$ if the other reports H. A type L bidder expects to pay $\frac{2}{3}(-\frac{1}{3}) + \frac{1}{3} \cdot \frac{2}{3} = 0$ and a type H bidder $\frac{1}{3}(-\frac{1}{3}) + \frac{2}{3} \cdot \frac{2}{3} = \frac{1}{3}$, which is exactly its Vickrey rent. The bets bring in $2 \cdot \frac{1}{2} \cdot \frac{1}{3} = 1/3$, so the revenue is $4/3 + 1/3 = 5/3 = S$. The bet does not depend on the bidder's own report, so the mechanism is still DSIC. But ex post a type H bidder who meets another H gets $0 - 2/3 < 0$.

## In plain words

When bidders' private information is linked, a bidder's type tells something about what the others will say. A high type expects others to be high, and a low type expects others to be low. The seller can offer each bidder a side bet on what the others report. The bet is designed so that a truthful bidder of each type expects to pay exactly the profit that it would otherwise keep. A bidder who lies about its type is offered the bet of another type, which it values with the wrong beliefs, and so it loses. In the end the seller gets all the value, and the bidders get nothing on average. The trick needs bidders who do not mind risk and who can pay large amounts.

## Proof

Fix the [Vickrey auction](/vickrey-auction/) $(x^V, p^V)$, with ties broken by a fair coin. It is DSIC and allocates efficiently. Let $U_i(t_i) = \mathbb{E}[v_i(t_i) x_i^V(t) - p_i^V(t) \mid t_i] \ge 0$ be the interim utility of a truthful bidder of type $t_i$, and $U_i$ the vector of these numbers.

**Part 1 (full rank).** Since $\Pi_i$ has rank $|T_i|$, its rows are independent and the system $\Pi_i z_i = U_i$ has a solution $z_i : T_{-i} \to \mathbb{R}$. Define the mechanism: allocate by $x^V$, and charge bidder $i$ the amount $p_i^V(b) + z_i(b_{-i})$. The extra term does not depend on $b_i$, so for any reports of the others the best report of bidder $i$ is the same as in Vickrey: the truth. The mechanism is DSIC and efficient. A truthful bidder of type $t_i$ has interim utility $U_i(t_i) - \sum_{t_{-i}} \pi_i(t_{-i} \mid t_i) z_i(t_{-i}) = U_i(t_i) - (\Pi_i z_i)(t_i) = 0$. So interim IR holds with equality, the bidders' total expected utility is 0, and the revenue equals the expected welfare $S$.

**Part 2 (convex independence).** Fix bidder $i$ and a type $s \in T_i$. The belief $\pi_i(\cdot \mid s)$ is not in the convex hull $C$ of the other rows of $\Pi_i$. The hull of finitely many points is compact and convex, so by the [separating hyperplane theorem](/separating-hyperplane-theorem/) there is a vector $w$ with $\pi_i(\cdot \mid s) \cdot w < \pi_i(\cdot \mid t) \cdot w$ for every $t \ne s$. Every belief sums to 1, so $y = w - (\pi_i(\cdot \mid s) \cdot w)\mathbf{1}$ gives $\pi_i(\cdot \mid s) \cdot y = 0$ and $\pi_i(\cdot \mid t) \cdot y > 0$ for $t \ne s$. Scale $y$ so that $\pi_i(\cdot \mid t) \cdot y \ge 1$ for all $t \ne s$, and call it $y_s$. (The same vector also follows from [Farkas' lemma](/farkas-lemma/).)

Let $M$ bound the Vickrey gain of any lie and the rents: $M = \max_{i, t, s} |U_i(s)| + \max_{i, t_i, b_i, t_{-i}} |v_i(t_i) x_i^V(b_i, t_{-i}) - p_i^V(b_i, t_{-i})|$. Choose $K > M$ and charge bidder $i$ the amount

$$p_i^V(b) + U_i(b_i) + K\, y_{b_i}(b_{-i}).$$

A bidder of type $t$ who reports $s$ while the others tell the truth expects

$$\mathbb{E}\big[v_i(t) x_i^V(s, t_{-i}) - p_i^V(s, t_{-i}) \mid t\big] - U_i(s) - K\, \pi_i(\cdot \mid t) \cdot y_s.$$

For $s = t$ this is $U_i(t) - U_i(t) - 0 = 0$. For $s \ne t$ the first two terms are at most $M$ and the last is at most $-K$, so the total is below 0. Truth is a Bayes-Nash equilibrium, every type gets exactly 0, interim IR holds, and the allocation is the efficient Vickrey one. The expected payments add to the expected welfare, so the revenue is $S$. Note that the beliefs here are conditional on the true type $t$, which is why correlation is essential. $\blacksquare$

## Consequences

- **Information rents can vanish.** With independent types, an optimal auction must leave rents to high types, which is the basis of [Myerson's optimal auction](/myerson-optimal-auction/) and of [revenue equivalence](/revenue-equivalence-theorem/). With generic correlation they disappear. When $|T_{-i}| \ge |T_i|$, full rank holds for an open dense set of priors, so the theorem applies to "most" correlated priors with finite types.
- **Efficiency and budget problems ease.** The same bets can fund or reshape transfers, so correlation also weakens the [Myerson-Satterthwaite](/myerson-satterthwaite-theorem/) impossibility, which needs independence.
- **Revenue ranking of standard auctions is beside the point.** With correlated values, the [linkage principle](/linkage-principle/) ranks the English, second-price and first-price auctions, but none of them is optimal; the optimal mechanism uses lotteries that no standard format has.
- **Continuous types.** McAfee and Reny (1992) extend the idea to continuous type spaces, where the surplus can be extracted up to any epsilon under a corresponding condition on the beliefs.

## Tightness

- **Independent types.** If $\pi = \pi_1 \times \cdots \times \pi_n$, every row of $\Pi_i$ is the same vector, so convex independence fails as soon as $|T_i| \ge 2$. Then a bet $z_i(b_i, t_{-i})$ has an expected value that depends only on the report, not on the true type, and the usual argument applies: if $L < H$ are two values of bidder $i$, interim IC gives $U_i(H) \ge U_i(L) + (H - L) Q_i(L)$, where $Q_i(L)$ is the winning probability of type L. In the example with independent uniform types, $Q(L) = 1/4$ under efficient allocation, so $U(H) \ge 1/4$, and full extraction fails.
- **Full rank in Part 1.** The paper shows that for the dominant-strategy result the rank condition is needed. Convex independence is weaker, and with it alone only the BIC version holds.
- **Ex post IR.** Both mechanisms are only interim IR. In the example a type H bidder that meets another type H loses $2/3$ ex post. With ex post IR, a bidder can refuse the bet after seeing it lose, and full extraction fails in general.
- **Risk neutrality and unlimited liability.** In Part 2 the constant $K$ can be very large when the beliefs of different types are close. Risk-averse bidders would not accept such bets, and bidders with budgets could not pay them.
- **Exact knowledge of the prior.** The bets are tuned to the beliefs. If the seller's model of the beliefs is wrong, or bidders can coordinate their reports, the guarantee is lost. Much later work on robust mechanism design starts from this criticism.

## History

Cremer and McLean had a dominant-strategy version with interdependent demands in 1985, and in 1988 gave the Bayesian version under convex independence together with the dominant-strategy version under full rank. McAfee and Reny (1992) carried the result to continuous types. The theorem is often read as a paradox, because real auctions do not use such bets; the usual answers are the hypotheses listed under Tightness.

## References
