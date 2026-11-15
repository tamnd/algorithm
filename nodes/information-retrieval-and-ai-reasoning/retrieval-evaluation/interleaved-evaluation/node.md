---
tag: S4177H
kind: technique
slug: interleaved-evaluation
name: Interleaved evaluation
aliases:
- interleaving for online evaluation
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: core
summary: Merges the result lists of two rankers into one shown list and credits the ranker whose documents get more clicks.
prereqs: [test-collection, sign-test]
see_also: [balanced-interleaving, team-draft-interleaving, probabilistic-interleaving, click-model, position-bias, implicit-feedback, position-based-click-model, cranfield-paradigm]
sources:
  - paper: "Thorsten Joachims, Evaluating retrieval performance using clickthrough data, in J. Franke, G. Nakhaeizadeh and I. Renz (editors), Text Mining, Physica/Springer Verlag, 2003, pp. 79-96"
    title: Evaluating retrieval performance using clickthrough data
    locator: the idea of a paired comparison of two rankings from the clicks on one merged result list
  - paper: doi:10.1145/1458082.1458092
    title: Filip Radlinski, Madhu Kurup and Thorsten Joachims, How does clickthrough data reflect retrieval quality?, CIKM 2008, pp. 43-52
    locator: balanced and team-draft interleaving, and the study on the arXiv.org search engine in which interleaving found the known order of quality of rankings and absolute click metrics did not do so reliably
  - paper: doi:10.1145/2063576.2063618
    title: Katja Hofmann, Shimon Whiteson and Maarten de Rijke, A probabilistic method for inferring preferences from clicks, CIKM 2011, pp. 249-258
    locator: the requirements that an interleaving method be fair under random clicks and sensitive to ranking differences, the faults of balanced and team-draft interleaving, and probabilistic interleaving
  - paper: doi:10.1145/2094072.2094078
    title: Olivier Chapelle, Thorsten Joachims, Filip Radlinski and Yisong Yue, Large-scale validation and analysis of interleaved search evaluation, ACM Transactions on Information Systems 30(1), Article 6, 2012
    locator: interleaving experiments on commercial search engines, and the measured agreement of their outcomes with offline judgments and between interleaving methods
---

Interleaved evaluation compares two rankers online. For each query, it runs both rankers, merges their two result lists into one list, and shows that list to the user as if it came from one system. The clicks on the shown list are then credited to the ranker that contributed the clicked documents, and the ranker with more credit wins the query. Over many queries, a paired test such as the [sign test](/sign-test/) on the wins decides whether one ranker is preferred. The design makes each user compare the two rankers side by side, on the same query, at the same time, which removes much of the noise of comparing two groups of users. Joachims proposed the idea in 2002 and 2003. [Balanced](/balanced-interleaving/), [team-draft](/team-draft-interleaving/) and [probabilistic](/probabilistic-interleaving/) interleaving are the classic ways to fill in the merge and the credit.

## In plain words

You have two search engines and want to know which one users like more. Instead of showing engine A to some users and engine B to others, show every user one list that mixes the results of both. Users do not see that the list is mixed. When they click, look at where each clicked result came from. If the results from A get more clicks than those from B on this query, A wins it. Count the wins over many queries and check whether one engine wins more often than chance allows.

The mix must be fair. Users click the top of a list more often whatever it holds, so the mix must give both engines the top places equally often. Otherwise the engine placed higher wins only because of its place.

## When it applies

- Two rankers, or two versions of one ranker, both able to answer the same live query, so that both lists exist at the same time.
- Users who see a ranked list and click on results, so that clicks give [implicit feedback](/implicit-feedback/).
- A question of preference: which ranker is better, not how good each one is on an absolute scale. Interleaving gives a direction and a strength of preference, not a value of nDCG or AP.
- Small differences. Interleaving is used where an A/B test of absolute click metrics, such as clicks per query, needs too much traffic, and where [test collection](/test-collection/) judgments are too costly or too far from what users want.

It does not apply when the result page is not a list, when the two rankers cannot be run on the same query, or when the outcome must be a number that can be compared with past offline experiments.

## The template

```pseudo id=main
INTERLEAVED-COMPARISON(rankerA, rankerB, queries)
L1  wins_A ← 0;  wins_B ← 0;  ties ← 0
L2  for each query q in queries do
L3      A ← rankerA(q);  B ← rankerB(q)
L4      (I, state) ← MERGE(A, B)              ▷ hole: the shown list, with fresh random choices
L5      show I to the user and record the clicked positions C
L6      o ← CREDIT(I, state, A, B, C)         ▷ hole: o > 0 prefers A, o < 0 prefers B, 0 is a tie
L7      if o > 0 then wins_A ← wins_A + 1
L8      else if o < 0 then wins_B ← wins_B + 1
L9      else ties ← ties + 1
L10 return TEST(wins_A, wins_B, ties)          ▷ hole: a paired test over the queries
```

There are three holes. **MERGE** builds the shown list $I$ from $A$ and $B$ and keeps in `state` whatever the credit needs, such as the team of each document or the coin flips. It must use new random choices for each query. **CREDIT** turns the clicks into a preference for this query. **TEST** decides whether the counts show a real preference.

A method fills MERGE and CREDIT so that two properties hold.

- **Fair under random clicks.** If the clicks do not depend on the documents, for example a user who clicks each position with a probability that depends only on the position, the expected outcome of line L6 must be 0. Otherwise [position bias](/position-bias/) alone makes one ranker win.
- **Sensitive.** If $A$ is better than $B$ for a user, in the sense that it puts more relevant documents near the top, the expected outcome under a reasonable [click model](/click-model/) should be positive, and large enough to show with a feasible number of queries.

Line L5 is the only contact with the user. Lines L7 to L9 count a win per query; the outcome of one query is very noisy, and only the counts over many queries carry information. For line L10, the usual choice is a two-sided [sign test](/sign-test/) on wins_A and wins_B, with the ties left out. With 60 wins for A, 40 for B and 100 ties, the sign test gives a two-sided p-value of about 0.057, so the preference is not yet significant at the 5% level. Queries of one user are not independent, so a test can also take one vote per user, the majority of that user's queries.

## Classic examples

- **[Balanced interleaving](/balanced-interleaving/).** MERGE takes documents from $A$ and $B$ in turns, with a coin for the first turn, so every prefix of $I$ holds top parts of both rankings of nearly equal length. CREDIT finds the depth of the lowest click in each ranking and counts the clicks inside the top of each. It is the first method, due to Joachims. It is not fair under random clicks: for $A = (a, b, c, d)$ and $B = (b, c, d, a)$, one click on a random position prefers $B$ with probability $3/4$.
- **[Team-draft interleaving](/team-draft-interleaving/).** MERGE lets the two rankers pick in turns like team captains, with a fresh coin in each round for who picks first, and records the team of each document. CREDIT counts the clicks of each team. Radlinski, Kurup and Joachims introduced it in 2008 to remove the bias of balanced interleaving. It is fair, but it cannot see some differences between rankings.
- **[Probabilistic interleaving](/probabilistic-interleaving/).** MERGE draws each document from a softmax distribution over one of the two rankings, and CREDIT takes the expected outcome over all the ways the shown list could have been assigned to the rankers. Hofmann, Whiteson and de Rijke proposed it in 2011. It is fair and sees rank differences that team draft misses.
- **The arXiv.org study.** Radlinski, Kurup and Joachims made rankings of known order of quality for the arXiv.org search engine, by changing a good ranking in known ways. Balanced and team-draft interleaving found the known order. None of the eight absolute click metrics they tried, such as the clicks per query, did so reliably.

## Variations

- **More than two rankers.** A draft with several captains, who pick in a random order in each round, compares many rankers on one shown list. This is called multileaving.
- **Weighted credit.** CREDIT can count clicks with weights, for example by the time spent on the clicked page, or only the last click of a query.
- **Per-user aggregation.** Count one vote per user instead of one per query, so that heavy users do not dominate the result.
- **Comparison in expectation.** Probabilistic interleaving computes the expected outcome of a query exactly, in place of the outcome of the one assignment that was drawn, which removes the noise of that draw.
- **Learning from interleaving.** An online learner can use interleaved comparisons between the current ranker and a changed one as the feedback for each step, which is the setting of online [learning to rank](/learning-to-rank/).

## Pitfalls

- **Assuming that a merge is fair.** A merge that looks balanced can still be biased, as balanced interleaving shows. Test a method with random clicks on close rankings before trusting a small win.
- **A coin that is not fresh.** If the random choices of line L4 repeat across queries, for example from a generator seeded again with the same value, one ranker always gets position 1 and wins by position bias.
- **Agreement with offline metrics is not given.** An interleaving win says that users clicked more on one ranker's documents. It need not agree with nDCG or AP on a test collection. How often the two agree is a measured result: Chapelle, Joachims, Radlinski and Yue compared interleaving outcomes with offline judgments on commercial search engines and report the agreement they found. Treat it as an empirical fact about those systems, not a theorem.
- **Clicks that are not judgments.** Clicks follow the snippet, not the document, and a click can mean a bad result as well as a good one. Robots and repeated queries also add clicks. Filter them before line L6.
- **Queries with no clicks.** Most methods give a tie when there is no click. Many ties lower the power of the test but do not bias it. Do not drop the queries before the test without saying so.
- **Duplicates and near duplicates.** If $A$ and $B$ hold two copies of the same page under different ids, the shown list holds both, and the credit is split in a way that depends on the ids.

## Exercises

1. Let $A = B$. Show that balanced interleaving shows $A$ itself and that every query is a tie, whatever the clicks. Then show that team-draft interleaving with $A = B$ gives an expected outcome of 0, but that a single query can have a winner.
2. With $A = (a, b, c, d)$ and $B = (b, c, d, a)$, write down the two shown lists of balanced interleaving, one for each coin value. A user clicks one position chosen uniformly at random. Show that $B$ wins with probability $3/4$. (Both shown lists hold the same documents, and the credit of balanced interleaving depends on the clicked document, not on its position. Only a click on $a$ credits $A$.)
3. With $A = (a, b)$ and $B = (b, a)$, list the shown lists and teams of team-draft interleaving for the two coin values, and check that each position belongs to each team with probability $1/2$.
4. An experiment gives 60 wins for $A$, 40 for $B$ and 100 ties. Compute the two-sided p-value of the sign test on the 100 queries with a winner, and find the smallest number of wins for $A$ out of those 100 that is significant at the 5% level. (The p-value is about 0.057, and 61 wins give about 0.035.)

## References
