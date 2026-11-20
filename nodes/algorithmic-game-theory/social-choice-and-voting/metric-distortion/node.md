---
tag: HN2W5E
kind: definition
slug: metric-distortion
name: Metric distortion of voting rules
aliases:
- distortion of a voting rule
area: algorithmic-game-theory/social-choice-and-voting
level: research
summary: "The worst-case ratio of the social cost of a rule's winner to the optimum when voters and candidates lie in an unknown metric space."
prereqs: [metric-space, triangle-inequality, approximation-ratio]
see_also: [copeland-method, plurality-voting, borda-count, condorcet-winner, preference-profile, k-median-problem, facility-location-problem, smith-set]
sources:
  - paper: doi:10.1016/j.artint.2018.07.006
    title: "Elliot Anshelevich, Onkar Bhardwaj, Edith Elkind, John Postl and Piotr Skowron, Approximating optimal social choice under metric preferences, Artificial Intelligence 264 (2018), 27-51"
    locator: "the definition of metric distortion, the lower bound 3 for every deterministic rule, the bound 5 for Copeland, and the bound 2m - 1 for plurality and for the Borda count"
  - paper: doi:10.1109/FOCS46700.2020.00134
    title: "Vasilis Gkatzelis, Daniel Halpern and Nisarg Shah, Resolving the optimal metric distortion conjecture, Proceedings of the 61st IEEE Symposium on Foundations of Computer Science (FOCS 2020), 1427-1438"
    locator: "the rule PluralityMatching and the proof that its distortion is 3"
  - paper: doi:10.24963/ijcai.2022/50
    title: "Fatih Erdem Kizilkaya and David Kempe, Plurality Veto: a simple voting rule achieving optimal metric distortion, Proceedings of the 31st International Joint Conference on Artificial Intelligence (IJCAI 2022), 349-355"
    locator: "the rule Plurality Veto and the proof that its distortion is 3"
---

Metric distortion measures how much a voting rule loses because it sees only rankings. Voters and candidates are points in a [metric space](/metric-space/) that nobody knows, and each voter ranks the candidates from nearest to farthest. The best candidate is the one with the smallest total distance to the voters. A rule sees only the rankings, so it cannot always find the best candidate. Its distortion is the worst ratio, over all profiles and all metrics that fit them, of the total distance of its winner to the smallest total distance. This is an [approximation ratio](/approximation-ratio/) where the missing input is the metric, not computation time. No deterministic rule has distortion below 3, and rules with distortion exactly 3 are known.

## Definition

Let $V$ be a set of $n$ voters and $C$ a set of $m$ candidates. A metric $d$ on $V \cup C$ is consistent with a profile $P$ when every voter $v$ ranks $a$ above $b$ only if $d(v, a) \le d(v, b)$. The social cost of a candidate is

$$\mathrm{SC}(c, d) = \sum_{v \in V} d(v, c).$$

A deterministic voting rule $f$ maps each profile to a candidate. Its distortion is

$$\mathrm{dist}(f) = \sup_{P} \; \sup_{d \text{ consistent with } P} \; \frac{\mathrm{SC}(f(P), d)}{\min_{c \in C} \mathrm{SC}(c, d)},$$

with the convention $0/0 = 1$. A rule with distortion $\alpha$ always elects a candidate whose social cost is at most $\alpha$ times the optimum, whatever the hidden metric is. For a randomized rule, the numerator is the expected social cost of the winner.

The minimum of $\mathrm{SC}$ over the candidates is the 1-median of the voters among the candidates, as in the [k-median problem](/k-median-problem/) with $k = 1$. The rule must find a good median from ordinal data alone.

## Examples and non-examples

- **The lower bound 3.** Take two candidates $a$ and $b$, and $n$ voters, half of whom rank $a$ first and half $b$ first. By symmetry, a rule may elect $a$. Place the voters who prefer $a$ at the midpoint between $a$ and $b$, at distance 1 from each, and the voters who prefer $b$ at $b$. This metric is consistent with the profile. Then $\mathrm{SC}(a) = (n/2) \cdot 1 + (n/2) \cdot 2 = 3n/2$ and $\mathrm{SC}(b) = n/2$, a ratio of 3. So every deterministic rule has distortion at least 3, already for two candidates.
- **A majority loses little.** If at least half of the voters rank $a$ above $b$, then $\mathrm{SC}(a) \le 3 \, \mathrm{SC}(b)$. Let $M$ be those voters. For $u \in M$, $d(a, b) \le d(u, a) + d(u, b) \le 2 d(u, b)$, so $d(a, b) \le \frac{2}{|M|} \mathrm{SC}(b)$. Voters in $M$ have $d(v, a) \le d(v, b)$, and the others have $d(v, a) \le d(v, b) + d(a, b)$. So $\mathrm{SC}(a) \le \mathrm{SC}(b) + (n - |M|) \frac{2}{|M|} \mathrm{SC}(b) \le 3 \, \mathrm{SC}(b)$. In particular, a [Condorcet winner](/condorcet-winner/) is always within a factor 3 of the optimum.
- **Copeland.** With an odd number of voters, the winner of [Copeland's method](/copeland-method/) beats every other candidate directly or in two steps. Two uses of the lemma above would give 9, and Anshelevich and coauthors proved that its distortion is at most 5.
- **Plurality and Borda.** The distortion of [plurality](/plurality-voting/) and of the [Borda count](/borda-count/) grows with $m$; both are $2m - 1$. Plurality ignores everything but first places, and the Borda count can be pulled away by many voters who are almost indifferent.
- **Rules with distortion 3.** Gkatzelis, Halpern and Shah built PluralityMatching, which elects a candidate for which a certain bipartite graph between voters has a perfect matching, and proved that its distortion is 3. Kizilkaya and Kempe gave Plurality Veto, which starts from plurality scores and lets the voters, one at a time, remove one point from their least preferred remaining candidate, and also proved distortion 3. Before them, Munagala and Wang had reached $2 + \sqrt{5}$.
- **Not utilitarian distortion.** If voters have arbitrary utilities rather than distances, a rule that sees only rankings can have unbounded distortion. The metric assumption, through the [triangle inequality](/triangle-inequality/), is what makes constant bounds possible.

## Related definitions

- **[Approximation ratio](/approximation-ratio/).** Distortion is an approximation ratio against an adversary who picks the metric.
- **Utilitarian distortion.** The same ratio for normalized utilities without a metric. It needs a different model, since the bounds there depend on $m$.
- **Randomized distortion.** The distortion of rules that pick the winner at random, measured in expectation. The lower bound for deterministic rules does not apply to them.
- **[Facility location](/facility-location-problem/) and [k-median](/k-median-problem/).** Distortion with one winner is a 1-median problem with ordinal data. Committee and facility versions ask for several winners.
- **[Smith set](/smith-set/) and the uncovered set.** The lemma on majorities shows that winners close to the top of the majority relation have small distortion. Copeland's method picks from the uncovered set and has distortion at most 5.

## References
