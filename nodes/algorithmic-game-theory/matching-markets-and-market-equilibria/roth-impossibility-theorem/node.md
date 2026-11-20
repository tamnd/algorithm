---
tag: YTB9WN
kind: theorem
slug: roth-impossibility-theorem
name: Roth's impossibility theorem for stable matching
aliases:
- no stable mechanism is strategyproof for both sides
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: No stable matching mechanism makes truthful reporting a dominant strategy for agents on both sides of the market.
prereqs: [stable-matching, gale-shapley, dominant-strategy-incentive-compatibility]
see_also: [deferred-acceptance-strategyproofness, lattice-of-stable-matchings, gibbard-satterthwaite-theorem, school-choice-problem, hospitals-residents-problem, revelation-principle, top-trading-cycles, vcg-mechanism]
sources:
  - paper: doi:10.1287/moor.7.4.617
    title: Alvin E. Roth, The economics of matching, stability and incentives, Mathematics of Operations Research 7(4), 617 to 628 (1982)
    locator: the whole paper (the impossibility theorem, its two-by-two example, and strategyproofness for the proposing side)
  - book: isbn:9780521437882
    title: Alvin E. Roth and Marilda A. Oliveira Sotomayor, Two-Sided Matching, a Study in Game-Theoretic Modeling and Analysis, Cambridge University Press (1990)
    locator: the chapter on strategic questions in the marriage model
  - paper: doi:10.1257/aer.89.4.748
    title: Alvin E. Roth and Elliott Peranson, The redesign of the matching market for American physicians, some engineering aspects of economic design, American Economic Review 89(4), 748 to 780 (1999)
    locator: the computations on how many applicants and programs could gain by misreporting in the medical match
  - paper: doi:10.1257/aer.99.3.608
    title: Fuhito Kojima and Parag A. Pathak, Incentives and stability in large two-sided matching markets, American Economic Review 99(3), 608 to 627 (2009)
    locator: the whole paper (the share of hospitals that can gain by manipulation goes to zero in large markets)
---

Roth's impossibility theorem says that a matching mechanism cannot be both stable and strategyproof for everyone. Whatever rule picks a stable matching from the reported preferences, some agent can sometimes get a better partner by lying. It is the two-sided matching counterpart of the [Gibbard-Satterthwaite theorem](/gibbard-satterthwaite-theorem/), but much easier to prove: one market with two men and two women suffices. The [strategyproofness of deferred acceptance](/deferred-acceptance-strategyproofness/) shows that the bound is tight in one sense: one side can be fully protected, but not both.

## Statement

A marriage market has men and women, each with a strict order over the agents of the other side and the option to stay single. A *mechanism* maps each profile of reported orders to a matching. It is *stable* when its output is stable for the reported profile at every profile. It is *strategyproof* when for every agent and every profile of the others' reports, reporting the true order is a dominant strategy: no false report gives a partner that the agent truly prefers.

**Theorem (Roth 1982).** No stable mechanism is strategyproof. More precisely, for every stable mechanism there is a market with two men and two women, a profile of true orders, and one agent who gains by a false report when all the others report truthfully.

## In plain words

Think of a small market where two good matchings are both stable. In one, the men get their first choices. In the other, the women do. A rule that must always pick a stable matching has to choose one of the two. If it picks the men's favorite, a woman can pretend that she would never accept the man she gets there. Then only the women's favorite is stable, and the rule must give it to her. If the rule picks the women's favorite, a man can do the same trick. So some person always has a reason to lie. The lie is a simple one: claim that a partner you would accept is not acceptable.

## Proof

Take men $m_1, m_2$ and women $w_1, w_2$ with the true orders

$$m_1: w_1, w_2 \qquad m_2: w_2, w_1 \qquad w_1: m_2, m_1 \qquad w_2: m_1, m_2,$$

where every agent of the other side is acceptable. Each man ranks first a woman who ranks him last.

*The stable matchings.* The matching $\mu_M = \{m_1 w_1, m_2 w_2\}$ is stable, because both men have their first choices, so no man is in a blocking pair. The matching $\mu_W = \{m_1 w_2, m_2 w_1\}$ is stable by the same argument for the women. Every other matching leaves at least one man and one woman single, and these two find each other acceptable, so they block. Hence $\mu_M$ and $\mu_W$ are the only stable matchings.

Let $\varphi$ be a stable mechanism. At the true profile it outputs $\mu_M$ or $\mu_W$.

*Case 1: $\varphi$ outputs $\mu_M$.* Let $w_1$ report the order "$m_2$, then single", so that $m_1$ is unacceptable to her, while the others report truthfully. At this profile, $\mu_M$ is not individually rational for $w_1$. The matching $\mu_W$ is still stable: $w_1$ and $w_2$ have their reported first choices. Of the other matchings, those that pair $m_1$ with $w_1$ are not individually rational for $w_1$; the matching $\{m_2 w_2\}$ alone is blocked by $(m_1, w_2)$; and the rest leave $m_2$ and $w_1$, or $m_1$ and $w_2$, both single, and that pair blocks. So $\mu_W$ is the only stable matching for the reports, and $\varphi$ must output it. Then $w_1$ is matched with $m_2$, whom she truly prefers to $m_1$.

*Case 2: $\varphi$ outputs $\mu_W$.* By the symmetry that swaps the roles of men and women, $m_1$ reports "$w_1$, then single", the only stable matching for the reports is $\mu_M$, and $m_1$ gets $w_1$, whom he truly prefers to $w_2$.

In both cases some agent gains by a false report while the others are truthful, so $\varphi$ is not strategyproof. $\blacksquare$

## Consequences

- **The choice of side matters.** A designer must decide which side to protect. Deferred acceptance with one side proposing makes truth dominant for that side only. In the [school choice problem](/school-choice-problem/) this conflict disappears, because schools have priorities and do not report.
- **Manipulation by truncation.** The proof shows the typical manipulation of the receiving side: report a shorter list that drops partners below a threshold. In the example, the woman who truncates her list gets her partner from the woman-optimal stable matching.
- **Small gains in large markets.** In the redesign of the American medical match, Roth and Peranson (1999) computed with the submitted lists how many agents could gain by misreporting, and found very few. Kojima and Pathak (2009) proved that in large many-to-one markets with short lists, the share of hospitals that can gain by manipulation goes to zero. So the impossibility is sharp in small markets but matters little in large ones.
- **Many-to-one markets.** In the [hospitals-residents problem](/hospitals-residents-problem/), the hospitals cannot be protected even by the hospital-proposing mechanism, because a hospital with several seats can gain by a false order (Roth 1985).

## Tightness

- **One side can be protected.** The man-proposing mechanism makes truth dominant for every man, so the theorem fails if only one side reports.
- **Size.** In a market with only one man or only one woman, the mechanism that gives the single agent of that side his first acceptable choice is stable and strategyproof. The proof needs two agents on each side, with two stable matchings.
- **Two stable matchings are needed.** The gain in the proof comes from moving between two stable matchings of the true preferences. Demange, Gale and Sotomayor (1987) showed that no group of agents can misreport so that every member gets a partner better than in every stable matching for the true preferences; so when the stable matching is unique, no single agent gains by lying under any stable mechanism.

## History

Roth (1982) proved the theorem with the example above, in the same paper that showed that the man-proposing mechanism is strategyproof for men. Dubins and Freedman (1981) had studied the incentives of the proposing side, and Roth (1985) extended the analysis to the college admissions model. Roth and Peranson (1999) and Kojima and Pathak (2009) measured and bounded the scope for manipulation in real and large markets.

## References
