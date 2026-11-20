---
tag: 6JK03C
kind: theorem
slug: ppad-hardness-of-arrow-debreu
name: PPAD-hardness of market equilibria
aliases:
- Chen-Dai-Du-Teng theorem
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: research
summary: Finding an equilibrium of an Arrow-Debreu market with additively separable piecewise-linear concave utilities is PPAD-complete, even with two segments per good.
prereqs: [arrow-debreu-market, ppad]
see_also: [arrow-debreu-existence-theorem, fisher-market, ppad-completeness-of-nash, nash-equilibrium-computation, end-of-the-line-problem, tfnp, fptas, approximate-ceei]
sources:
  - paper: doi:10.1109/FOCS.2009.29
    title: "Xi Chen, Decheng Dai, Ye Du and Shang-Hua Teng, Settling the complexity of Arrow-Debreu equilibria in markets with additively separable utilities, Proceedings of the 50th IEEE Symposium on Foundations of Computer Science (FOCS 2009), 273-282"
    locator: "the main theorem (Theorem 3 of the arXiv version, arXiv:0904.0644), the price-regulating market of Section 3 and the reduction from sparse two-player games of Sections 4 and 5"
  - paper: doi:10.1145/1970392.1970394
    title: "Vijay V. Vazirani and Mihalis Yannakakis, Market equilibrium under separable, piecewise-linear, concave utilities, Journal of the ACM 58(3), Article 10 (2011)"
    locator: the whole paper (rational equilibria, NP-completeness of deciding existence, membership in PPAD for Fisher and exchange markets, and PPAD-hardness for Fisher markets)
  - paper: "Xi Chen and Shang-Hua Teng, Spending is not easier than trading: on the computational equivalence of Fisher and Arrow-Debreu equilibria, Proceedings of the 20th International Symposium on Algorithms and Computation (ISAAC 2009)"
    locator: the whole paper (PPAD-hardness of Fisher markets with additively separable piecewise-linear concave utilities)
  - paper: "Xi Chen, Xiaotie Deng and Shang-Hua Teng, Sparse games are hard, Proceedings of the 2nd Workshop on Internet and Network Economics (WINE 2006), 262-273"
    locator: the whole paper (the PPAD-completeness of approximate Nash equilibria in sparse two-player games, the starting point of the reduction)
---

This theorem says that computing a [competitive equilibrium](/competitive-equilibrium/) of an [Arrow-Debreu market](/arrow-debreu-market/) is as hard as computing a Nash equilibrium of a two-player game, already for a simple and natural class of utilities. Each agent's utility is a sum over goods of concave piecewise-linear functions, one per good, so each additional unit of a good is worth a bit less. With one linear piece per good the problem is solvable in polynomial time; Chen, Dai, Du and Teng (2009) showed that two pieces per good already make it [PPAD](/ppad/)-complete, and that even an approximate equilibrium with inverse-polynomial error is PPAD-hard. The result answered a question that Vazirani had posed in 2007. Like the [PPAD-completeness of Nash equilibria](/ppad-completeness-of-nash/), it is evidence, not a proof, that no polynomial algorithm exists: it shows that such an algorithm would solve every problem in PPAD.

## Statement

**Notation.** The market has $n$ agents and $m$ divisible goods; agent $i$ has an endowment $w_i \in \mathbb{R}^m_{\ge 0}$ and a utility function $u_i$. Chen, Dai, Du and Teng write $n$ for goods and $m$ for traders; this page swaps the letters to match the rest of the area.

**SPLC utilities.** A function $r : \mathbb{R}_{\ge 0} \to \mathbb{R}_{\ge 0}$ is *$t$-segment piecewise-linear concave* (PLC) if $r(0) = 0$, $r$ is continuous, and $[0, \infty)$ splits into $t$ intervals on which $r$ is linear with slopes $\theta_0 > \theta_1 > \dots > \theta_{t-1} \ge 0$. A utility is *additively separable PLC*, or SPLC, if $u_i(x) = \sum_j r_{ij}(x_j)$ with each $r_{ij}$ PLC. Linear utilities are the case $t = 1$.

**Existence condition.** The *economy graph* has the agents as vertices and an edge from $i$ to $k$ when agent $i$ owns some good $j$ for which $r_{kj}$ is strictly increasing. If the economy graph is strongly connected, an SPLC market has an equilibrium, and when its numbers are rational it has a rational equilibrium whose bit length is polynomial in the input (Theorem 2 of the paper, a corollary of Maxfield 1997). Without some such condition an equilibrium can fail to exist, and Vazirani and Yannakakis (2011) showed that deciding whether one exists is NP-complete.

**Approximate equilibrium.** A price vector $p$ is an *$\varepsilon$-approximate equilibrium* if there is an allocation in which every agent gets an optimal bundle at $p$ and every good clears up to an error of $\varepsilon$ times its total supply. Only the clearing condition is relaxed.

**The problem.** *Sparse Market* takes an SPLC market with rational numbers whose economy graph is strongly connected, in which every $r_{ij}$ has at most 2 segments with slopes between 1 and 27 (or is zero), and every agent owns at most 23 goods and likes at most 23 goods. It asks for an $m^{-13}$-approximate equilibrium.

**Theorem (Chen, Dai, Du and Teng 2009).** Sparse Market is PPAD-complete.

**Corollaries.**
1. Finding an exact equilibrium of a strongly connected SPLC exchange market is PPAD-hard. Vazirani and Yannakakis (2011) proved that finding an exact equilibrium is in PPAD under mild sufficient conditions for existence, so under these conditions it is PPAD-complete.
2. SPLC exchange markets have no [fully polynomial-time approximation scheme](/fptas/), in the sense of an algorithm that finds an $\varepsilon$-approximate equilibrium in time polynomial in the input size and $1/\varepsilon$, unless every problem in PPAD can be solved in polynomial time.
3. The same holds for [Fisher markets](/fisher-market/) with SPLC utilities: finding an equilibrium is PPAD-complete (Chen and Teng 2009; Vazirani and Yannakakis 2011).

The result is about finding *one* equilibrium, a total search problem in [TFNP](/tfnp/). It is not an NP-hardness result, and it says nothing against the existence of an equilibrium, which is guaranteed under the hypotheses.

## In plain words

In a market where people sell what they own and buy what they like best, there are always prices at which everything balances, if trade can reach everyone. This theorem says that finding these prices can be very hard even when tastes are simple: each person values more of a good a bit less once she has a certain amount. The proof builds, for any two-player game, a market whose balanced prices spell out how the two players should play. So a fast method for markets would also give a fast method for games, and none is known. Markets in which each person values every unit of a good the same are much easier.

## Proof

The proof has two parts: membership in PPAD and PPAD-hardness. This is a sketch of the published proof, following the arXiv version of the paper.

*Membership.* Geanakoplos (2003) built a continuous map whose fixed points are exactly the equilibria of a market with quasi-concave utilities. For SPLC utilities this map is Lipschitz, so an approximate equilibrium can be read off an approximate fixed point of a Lipschitz map, and finding such a fixed point is in PPAD (footnote 4 of the paper). For exact equilibria, Vazirani and Yannakakis (2011) gave a separate proof of membership, under mild sufficient conditions for existence.

*Hardness: the source problem.* A two-player game $(A, B)$ with $k$ strategies per player is *normalized* if its payoffs are in $[-1, 1]$, and *sparse* if every row and column of $A$ and $B$ has at most 10 nonzero entries. A pair of mixed strategies is an *$\varepsilon$-well-supported* Nash equilibrium if each player puts weight only on strategies whose payoff is within $\varepsilon$ of her best payoff. Chen, Deng and Teng (2006) proved that finding a $k^{-6}$-well-supported Nash equilibrium of a sparse normalized $k$ by $k$ game is PPAD-complete ("Sparse Bimatrix").

*Step 1: a market that pins the prices to an interval.* The *price-regulating market* $M_m$ has $m$ goods and one agent for every ordered pair $(i, j)$ of distinct goods. Agent $(i, j)$ owns $1/m$ units of good $i$, and her utility is linear: $2$ per unit of good $i$, $1$ per unit of good $j$, $0$ for the others. Normalize prices so that the smallest is $1$. Then $p$ is an $m^{-1}$-approximate equilibrium of $M_m$ exactly when $1 \le p_k \le 2$ for every $k$ (Property 1 of the paper). In one direction, if all prices are in $[1, 2]$, agent $(i, j)$ gets bang per buck $2 / p_i \ge 1 / p_j$ from her own good, so every agent can keep her endowment, which clears the market. In the other direction, suppose that good 1 is the most expensive good and costs more than twice the cheapest good, good 2. Agents $(i, j)$ with $1 \notin \{i, j\}$ give good 1 no value. Agents $(i, 1)$ prefer their own good $i$, because $2 / p_i \ge 2 / p_1 > 1 / p_1$, and agent $(1, 2)$ prefers good 2, because $2 / p_1 < 1 = 1 / p_2$. Only the $m - 2$ agents $(1, j)$ with $j \ne 2$ can buy good 1, and each can pay for at most $1/m$ units of it. So at most $(m - 2)/m$ of the $(m - 1)/m$ units are sold, and the shortfall $1/m$ is more than the allowed error $(1/m) \cdot (m - 1)/m$.

*Step 2: encode a strategy pair in the prices.* Start from $M_{2k+2}$ and read the prices as $x_s = p_s - 1$ and $y_s = p_{k+s} - 1$ for $s = 1, \dots, k$; after normalization, $(x, y)$ is a pair of mixed strategies. The paper shows that the price regulation survives when new agents with small endowments are added (the new agents bring little supply compared with the agents of $M_{2k+2}$).

*Step 3: enforce the Nash conditions.* For each pair of strategies $s \ne s'$ of the row player, add small agents whose utilities are built from the difference of rows $s$ and $s'$ of $A$, and do the same for the column player with $B$. Their utilities have at most two segments per good. The kink of a two-segment utility makes an agent switch from one good to another at a known price ratio. Because the price regulation keeps every price in $[1, 2]$, the designer knows how each new agent behaves at every candidate equilibrium, even before the prices are known. The paper uses these agents so that the market can clear only if every strategy that is worse than another by more than the tolerance gets almost no weight. Sparsity of the game keeps every agent's set of goods small.

*Step 4: correctness.* Theorem 4 of the paper: from every $k^{-13}$-approximate equilibrium of the constructed market, the pair $(x, y)$ of Step 2, after normalization, is a $k^{-6}$-well-supported Nash equilibrium of $(A, B)$. The market has polynomial size and the map from prices to strategies takes polynomial time, so this is a polynomial reduction from Sparse Bimatrix to Sparse Market. $\blacksquare$

**Example (Step 1 with two goods).** In $M_2$, agent $(1, 2)$ owns $1/2$ unit of good 1 and has utility $2 x_1 + x_2$; agent $(2, 1)$ owns $1/2$ unit of good 2 and has utility $x_1 + 2 x_2$. At $p = (1, 2)$, agent $(1, 2)$ gets bang per buck $2$ from good 1 and $1/2$ from good 2, so she keeps her good; agent $(2, 1)$ gets $1$ from each good and is happy to keep hers. The market clears. At $p = (1, 3)$, agent $(2, 1)$ gets $2/3$ from good 2 and $1$ from good 1, so she sells good 2 and wants good 1, and nobody wants good 2 at a positive price. The equilibrium prices are exactly the vectors with $p_2 / p_1 \in [1/2, 2]$.

## Consequences

- **No efficient algorithm is expected.** Unless PPAD is in polynomial time, there is no polynomial algorithm for SPLC exchange or Fisher markets, and no fully polynomial approximation scheme. Convex programs such as the [Eisenberg-Gale program](/eisenberg-gale-program/), which work for linear Fisher markets, cannot capture these markets.
- **Markets and games are equivalent.** Together with membership in PPAD, the theorem shows that SPLC markets and two-player games are polynomially equivalent. An equilibrium of a two-player game can be computed by finding a market equilibrium, and the other way round. Algorithms for one, such as the [Lemke algorithm](/lemke-algorithm/) for games or the [Scarf algorithm](/scarf-algorithm/) for fixed points, therefore have counterparts for the other, with no known polynomial bound.
- **A line between linear and concave.** Linear exchange markets have polynomial and even strongly polynomial algorithms (Jain 2007; Duan and Mehlhorn 2015; Garg and Vegh 2019; see the [Arrow-Debreu market](/arrow-debreu-market/) page). Every concave utility can be approximated by a PLC utility, and two segments per good are enough for hardness.
- **Other classes.** Chen and Deng's PPAD-completeness of two-player Nash, with an earlier reduction of Codenotti, Saberi, Varadarajan and Ye, implies PPAD-hardness for Leontief exchange markets, and Huang and Teng extended it to approximate Leontief equilibria and to CES markets with small elasticity of substitution (as surveyed in Section 1.2.2 of the paper). The [approximate CEEI](/approximate-ceei/) problem of course allocation is also PPAD-complete (Othman, Papadimitriou and Rubinstein 2016).

## Tightness

- **One segment is easy.** With linear utilities ($t = 1$), an exact equilibrium can be computed in polynomial time, so the two segments of the theorem are the least possible.
- **The approximation is inverse-polynomial.** The theorem gives hardness for $\varepsilon = m^{-13}$, which rules out a fully polynomial approximation scheme. It does not rule out polynomial algorithms for a fixed constant $\varepsilon$.
- **The connectivity condition matters.** Strong connectivity of the economy graph guarantees existence and makes the problem total. Without it, the question changes: deciding whether an equilibrium exists is NP-complete (Vazirani and Yannakakis 2011).
- **Evidence, not a lower bound.** PPAD-hardness is conditional. It is not known that PPAD is different from P.

## History

Vazirani (2007, in the book Algorithmic Game Theory) called a polynomial algorithm for additively separable concave utilities a premier open question, and asked about SPLC utilities in particular. Earlier hardness results were for Leontief utilities, through reductions from two-player games. In 2009 Chen, Dai, Du and Teng settled the question for exchange markets with the price-regulating construction. In the same period Chen and Teng (ISAAC 2009) and Vazirani and Yannakakis (ICS 2010, journal version 2011) showed PPAD-hardness for Fisher markets with SPLC utilities; Vazirani and Yannakakis also proved membership in PPAD and the NP-completeness of deciding existence. Chen, Paparas and Yannakakis (2017) later extended such hardness results to other classes of utilities.

## References
