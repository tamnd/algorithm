---
tag: 91A728
kind: concept
slug: approximation-resistance
name: Approximation resistance
aliases:
- approximation-resistant predicate
- approximation resistant CSP
area: approximation/hardness-of-approximation
level: research
summary: A predicate is approximation resistant if no polynomial-time algorithm beats a random assignment on its CSP by any constant, unless P = NP or, in UG-hard versions, the UGC fails.
prereqs: [maximum-csp, approximation-ratio, hastad-3bit-pcp, unique-games-conjecture]
see_also: [raghavendra-theorem, random-assignment-max-3-sat, max-3sat-inapproximability, max-cut-ugc-hardness, boolean-constraint-satisfaction, max-2-sat, approximation-threshold, dictatorship-test]
sources:
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 798 to 859, 2001
    locator: the NP-hardness of Max E3LIN within 1/2 + epsilon and of Max E3SAT within 7/8 + epsilon, and the resistance of 3-bit predicates implied by parity
  - paper: doi:10.1007/s00037-009-0272-6
    title: Per Austrin and Elchanan Mossel, Approximation resistant predicates from pairwise independence, Computational Complexity 18(2), 249 to 271, 2009
    locator: the main theorem, UG-hardness for every predicate whose accepting set supports a balanced pairwise independent distribution
  - paper: doi:10.1145/2873054
    title: Siu On Chan, Approximation resistance from pairwise-independent subgroups, Journal of the ACM 63(3), Article 27, 2016 (STOC 2013)
    locator: NP-hardness, with no conjecture, for predicates whose accepting set contains a pairwise independent subgroup
  - paper: "Uri Zwick, Approximation algorithms for constraint satisfaction problems involving at most three variables per constraint, Proceedings of the 9th ACM-SIAM Symposium on Discrete Algorithms (SODA), 1998"
    locator: SDP algorithms that beat random assignment for every 3-bit predicate not implied by parity
  - paper: "Per Austrin and Johan Håstad, Randomly supported independence and resistance, SIAM Journal on Computing 40(1), 1 to 27, 2011 (STOC 2009)"
    locator: resistance of random predicates with enough accepting inputs, so that almost all predicates of large arity are resistant under the UGC
---

A predicate $P$ is *approximation resistant* if, for every $\varepsilon > 0$, it is hard to approximate Max-CSP($P$) within $\rho(P) + \varepsilon$, where $\rho(P)$ is the fraction of inputs that $P$ accepts, which is exactly what a uniformly random assignment achieves. So for such a predicate the trivial algorithm, which does not even read the constraints, is optimal up to a constant. Håstad proved that 3XOR and 3SAT are approximation resistant unless P = NP. Austrin and Mossel showed that, under the [Unique Games Conjecture](/unique-games-conjecture/), every predicate whose accepting set supports a pairwise independent distribution is resistant. Predicates of arity $2$, such as the cut predicate and 2SAT clauses, are not resistant.

## In plain words

Some problems ask to set many yes or no values so that as many small rules as possible hold, where every rule has the same shape. Setting the values by coin flips already makes a fixed share of the rules hold. For some shapes of rule, careful methods do much better than coin flips. For other shapes, called resistant, no fast method can beat coin flips by any fixed margin, even when almost all rules can hold at once. A rule that says three values must have an odd sum is resistant, and so is a rule that says at least one of three values is true. A rule that says two values must differ is not resistant, because a known method gets about 88 percent of the best answer instead of the half that coin flips get.

## The idea

**The setting.** Fix a predicate $P : \{0,1\}^k \to \{0,1\}$. An instance of Max-CSP($P$) is a weighted list of constraints, each of the form $P(\ell_1, \ldots, \ell_k)$ where the $\ell_i$ are literals on distinct variables, with total weight $1$. The *density* of $P$ is $\rho(P) = |P^{-1}(1)| / 2^k$. On this site a maximization ratio means $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha \le 1$.

**Random assignment, in full.** A uniformly random assignment makes the literals of one constraint uniform on $\{0,1\}^k$, because the variables are distinct and a negation is a bijection. So each constraint holds with probability $\rho(P)$, and by [linearity of expectation](/linearity-of-expectation/) the expected value is $\rho(P)$. The method of conditional expectations turns this into a deterministic algorithm. Since $\mathrm{OPT} \le 1$, this is a $\rho(P)$-approximation for every $P$.

**Definition.** $P$ is *approximation resistant* if for every $\varepsilon > 0$ it is NP-hard to tell instances with $\mathrm{OPT} \ge 1 - \varepsilon$ from instances with $\mathrm{OPT} \le \rho(P) + \varepsilon$. It is *UG-resistant* if this is NP-hard assuming the UGC. It is *resistant on satisfiable instances* if the same holds with $\mathrm{OPT} = 1$ in place of $\mathrm{OPT} \ge 1 - \varepsilon$. Each form implies that approximating Max-CSP($P$) within $\rho(P) + \varepsilon'$ is hard for every $\varepsilon' > 0$.

**Pairwise independence.** A distribution $\mu$ on $\{0,1\}^k$ is *balanced pairwise independent* if each pair of coordinates is uniform on $\{0,1\}^2$. *Theorem (Austrin and Mossel 2009, cited).* If $P^{-1}(1)$ supports a balanced pairwise independent distribution, then $P$ is UG-resistant. The reason is a [dictatorship test](/dictatorship-test/): draw the $k$ queries from $\mu$ coordinatewise, with noise. Dictators pass with probability close to $1$, since $\mu$ lives on accepting inputs. For functions with small influences, the invariance principle says that only the pairwise correlations of $\mu$ matter, and these are the same as for the uniform distribution, so the test accepts with probability close to $\rho(P)$. Chan (2016) proved NP-hardness, without the UGC, when $P^{-1}(1)$ contains a pairwise independent *subgroup* of $\mathbb{F}_2^k$.

**The general picture.** By [Raghavendra's theorem](/raghavendra-theorem/), $P$ is UG-resistant exactly when the basic SDP has instances with SDP value $1 - o(1)$ and optimum $\rho(P) + o(1)$. Pairwise independence is a sufficient condition for this, not a necessary one in general.

## Examples

Densities and status for small predicates, written on bits.

| Predicate | Accepts | Density | Resistant? |
|---|---|---|---|
| 3XOR | $x_1 + x_2 + x_3 = 1$ | $1/2$ | yes, NP-hard (Håstad), not on satisfiable instances |
| 3OR (E3SAT clause) | $x_1 \vee x_2 \vee x_3$ | $7/8$ | yes, NP-hard, also on satisfiable instances (Håstad) |
| NAE3 | not all equal | $3/4$ | no |
| CUT (2XOR) | $x_1 \ne x_2$ | $1/2$ | no, ratio $0.878$ by Goemans-Williamson |
| 2OR (2SAT clause) | $x_1 \vee x_2$ | $3/4$ | no |

**3XOR is resistant.** This is [Håstad's 3-bit PCP](/hastad-3bit-pcp/): telling Max 3LIN instances of value $1 - \varepsilon$ from value $\tfrac12 + \varepsilon$ is NP-hard. Its accepting set, the four strings of odd parity, is a coset of a subspace, and the uniform distribution on it is balanced pairwise independent: fixing two bits leaves exactly one odd completion. Resistance fails on satisfiable instances, because [Gaussian elimination](/gaussian-elimination/) finds a satisfying assignment of a satisfiable system.

**3OR is resistant.** The four odd-parity strings $100, 010, 001, 111$ are all accepted by $x_1 \vee x_2 \vee x_3$, so the pairwise independent distribution of 3XOR is supported inside 3OR as well. The gadget on the Håstad page, four clauses per equation, gives NP-hardness within $\tfrac78 + \varepsilon$, which matches the [random assignment for Max 3SAT](/random-assignment-max-3-sat/). In general, every 3-bit predicate that accepts all strings of one parity is resistant by the same kind of reduction (Håstad 2001), and Zwick (1998) gave SDP algorithms that beat random assignment for every other 3-bit predicate.

**NAE3 is not resistant, in full.** In the $\pm1$ notation, a not-all-equal triple has two values of one sign and one of the other, so $x_1x_2 + x_1x_3 + x_2x_3 = -1$ on every accepted input. Under a balanced pairwise independent distribution each product has mean $0$, so the sum would have mean $0$. So no such distribution exists, and the Austrin-Mossel theorem does not apply. An algorithm confirms that NAE3 is not resistant. A triple of literals is not all equal exactly when $2$ of its $3$ pairs differ, and otherwise $0$ pairs differ. Replace each NAE3 constraint by the three 2XOR constraints "these two literals differ". For every assignment, the fraction of satisfied 2XOR constraints is exactly $\tfrac23$ of the fraction of satisfied NAE3 constraints. The Goemans-Williamson algorithm for Max-2XOR finds an assignment within $\alpha_{\mathrm{GW}} \approx 0.878$ of the 2XOR optimum, so within $0.878$ of the NAE3 optimum. On instances of value $1 - \varepsilon$ this gives at least $0.878(1 - \varepsilon)$, which is above the density $\tfrac34$ for $\varepsilon < 0.14$.

**CUT and 2OR are not resistant.** For CUT the [Goemans-Williamson algorithm](/maximum-cut/) has ratio $0.878 > \tfrac12$. For 2OR, SDP algorithms for [Max 2SAT](/max-2-sat/) reach ratios above $0.94 > \tfrac34$.

## Where it is used

- **Tight hardness results.** Resistance of 3XOR and 3SAT gives the exact [approximation thresholds](/approximation-threshold/) $\tfrac12$ and $\tfrac78$, and these are starting points for gadget reductions to other problems.
- **Max $k$-CSP.** Predicates on $k$ bits whose accepting set is a small pairwise independent subgroup have density close to $k/2^k$. Chan's theorem then shows that Max $k$-CSP is NP-hard to approximate within a ratio of order $k/2^k$.
- **Most predicates are resistant.** Austrin and Håstad (2011) show that a random predicate on $k$ bits with enough accepting inputs supports a pairwise independent distribution with high probability, so under the UGC almost all predicates of large arity are resistant.
- **Classifying CSPs.** Under the UGC, [Raghavendra's theorem](/raghavendra-theorem/) reduces the question for each predicate to the integrality gap of one SDP. For arity $2$, every predicate can be approximated beyond its density, and arity $3$ is settled by the results of Håstad and Zwick above.

## References
