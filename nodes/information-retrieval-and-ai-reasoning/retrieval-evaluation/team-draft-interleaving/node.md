---
tag: 8FBQBW
kind: algorithm
slug: team-draft-interleaving
name: Team-draft interleaving
aliases:
- team draft interleave
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: advanced
summary: Lets two rankers pick documents in turns like team captains, with a coin flip for the first pick of each round, and credits each click to the team that picked the document.
model: word-ram
complexity:
  vars: {n: the sum of the lengths of the two rankings}
  time: {worst: O(n)}
  space: {extra: O(n)}
properties: {deterministic: false, recursive: false}
prereqs: [interleaved-evaluation]
see_also: [balanced-interleaving, probabilistic-interleaving, click-model, position-bias, position-based-click-model, implicit-feedback, sign-test]
sources:
  - paper: doi:10.1145/1458082.1458092
    title: Filip Radlinski, Madhu Kurup and Thorsten Joachims, How does clickthrough data reflect retrieval quality?, CIKM 2008, pp. 43-52
    locator: Section 5.2, Algorithm 2 and equations (4) and (5) (team-draft interleaving and its credit rule, and the remark that random clicks give equal preferences in expectation); the user study on arXiv.org
  - paper: doi:10.1145/2063576.2063618
    title: Katja Hofmann, Shimon Whiteson and Maarten de Rijke, A probabilistic method for inferring preferences from clicks, CIKM 2011, pp. 249-258
    locator: Section 3.2 and Figure 2 (team draft fails to detect a ranking difference when the relevant document always lands at the same rank)
  - paper: doi:10.1145/2094072.2094078
    title: Olivier Chapelle, Thorsten Joachims, Filip Radlinski and Yisong Yue, Large-scale validation and analysis of interleaved search evaluation, ACM Transactions on Information Systems 30(1), Article 6, 2012
    locator: the large-scale comparison of team-draft and balanced interleaving on commercial search engines and their agreement with offline judgments
---

Team-draft interleaving is an [interleaved evaluation](/interleaved-evaluation/) method that builds the shown list the way two captains pick players for a team: in each round a fair coin decides which ranking picks first, and then each ranking adds its highest-ranked document that is not yet shown. Each shown document belongs to the team of the ranking that picked it, and a click counts for that team only. Radlinski, Kurup and Joachims introduced it in 2008 to remove the bias of [balanced interleaving](/balanced-interleaving/): when both rankings hold the same documents, each position goes to each team with probability 1/2, so clicks that ignore the documents give a tie in expectation.

## In plain words

Think of two team captains who choose players from a line. In each round a coin decides who chooses first. Each captain takes the best player who is still free, by the captain's own order of preference. The players go into one line in the order they were chosen, and each player wears the shirt of the captain who chose them.

Here the captains are two search engines, the players are results, and the line is the result page the user sees. When the user clicks a result, the engine whose shirt that result wears gets one point. The engine with more points wins this query. If both engines put the same result first, only one of them can take it, and the other takes its next result.

## The problem

The input is two rankings $A$ and $B$ for one query, each with no repeated document, and a source of fair coins. The output is a shown list $I$ with no repeated document and a split of its documents into two teams $T_A$ and $T_B$. After the user clicks the set $C$ of documents of $I$, the output is a preference $o \in \{-1, 0, 1\}$, where 1 means that A is preferred. Over many queries, a [sign test](/sign-test/) on the queries with a preference decides if one ranking wins more often than chance.

## The algorithm

```pseudo id=main
TEAM-DRAFT-INTERLEAVE(A, B)
L1  I ← empty list, TA ← ∅, TB ← ∅
L2  while some A[i] ∉ I and some B[j] ∉ I do
L3      if |TA| < |TB| or (|TA| = |TB| and coin() = 1) then
L4          d ← the first document of A that is not in I
L5          append d to I, TA ← TA ∪ {d}
L6      else
L7          d ← the first document of B that is not in I
L8          append d to I, TB ← TB ∪ {d}
L9  return I, TA, TB

CREDIT(TA, TB, C)                        ▷ C: the clicked documents of I
L10 ha ← |C ∩ TA|, hb ← |C ∩ TB|
L11 return 1 if ha > hb, -1 if ha < hb, else 0
```

The coin in line L3 is drawn only when the teams have equal size, that is, at the start of each round of two picks. The second pick of a round goes to the smaller team. This is Algorithm 2 of Radlinski, Kurup and Joachims, and lines L10 and L11 are their equations (4) and (5). To find the first document not in $I$ in constant amortized time, keep one pointer per ranking and move it past documents that are already shown.

## Example

Take the rankings of the bias example of balanced interleaving: $A = (a, b, c, d)$ and $B = (b, c, d, a)$. Let the coin of round 1 be 1 and the coin of round 2 be 0.

| pick | round | coin | sizes before | team | first document not in I | I |
|---|---|---|---|---|---|---|
| 1 | 1 | 1 | 0, 0 | A | a | a |
| 2 | 1 | | 1, 0 | B | b | a, b |
| 3 | 2 | 0 | 1, 1 | B | c | a, b, c |
| 4 | 2 | | 1, 2 | A | d (a is shown) | a, b, c, d |

Now every document is shown and the loop stops, with $T_A = \{a, d\}$ and $T_B = \{b, c\}$. The four coin results give:

| coins | I | TA | TB | one click on a, b, c, d |
|---|---|---|---|---|
| 1, 1 | a, b, c, d | a, c | b, d | A, B, A, B |
| 1, 0 | a, b, c, d | a, d | b, c | A, B, B, A |
| 0, 1 | b, a, c, d | a, c | b, d | B, A, A, B |
| 0, 0 | b, a, c, d | a, d | b, c | B, A, B, A |

The shown lists are the same two as in balanced interleaving, but in each row the four positions split two and two between the teams. So one click on a random position is a tie in expectation, while balanced interleaving gives B a win with probability $3/4$.

The figure of Radlinski, Kurup and Joachims uses $A = (a, b, c, d, g, h)$ and $B = (b, e, a, f, g, h)$. If A wins every coin, $I = (a, b, c, e, d, f, g, h)$ with $T_A = \{a, c, d, g\}$ and $T_B = \{b, e, f, h\}$. A user who clicks b and e gives $hb = 2$ and $ha = 0$, a preference for B.

## Correctness

The proof is in `proofs/correctness.md`. Before each test of line L2, $I$ has no repeated document, the teams are disjoint and together hold the documents of $I$, the team sizes differ by at most 1, and they are equal after an even number of picks. So positions $2m-1$ and $2m$ always hold one document of each team. When $A$ and $B$ order the same set of documents, the coin of round $m$ gives position $2m-1$ to A with probability $1/2$ and position $2m$ to the other team. Flipping all coins swaps the teams at every position, so for any click model that depends only on positions, the outcomes under a coin vector and under its flip are negatives of each other, and the expected outcome is 0.

## Complexity

- **Time.** Each pick appends one new document, so there are at most $n$ picks. The two pointers only move forward, so all the scans in lines L4 and L7 take $O(n)$ steps in total. With a hash set of shown documents, the whole interleaving costs $O(n)$ time, and CREDIT costs $O(|C|)$.
- **Space.** $I$, the teams and the hash set hold $O(n)$ documents.
- **Coins.** One coin per round, so at most $\lceil |I| / 2 \rceil$ coins.

## Properties

- **Pairs of positions.** Positions $2m-1$ and $2m$ hold one document of each team.
- **Fair under random clicks.** For two orderings of the same documents, each position belongs to each team with probability exactly $1/2$, and clicks that depend only on positions give an expected outcome of 0. This is the property Radlinski, Kurup and Joachims state for the method.
- **Insensitive to some differences.** Let $A = (d_2, d_3, d_1)$ and $B = (d_1, d_2, d_3)$, with only $d_3$ relevant. $A$ ranks $d_3$ higher, but $d_3$ is shown at position 3 for every coin result and goes to each team with probability $1/2$, so the expected outcome is 0. Hofmann, Whiteson and de Rijke give this kind of example with four documents.
- **A dominating ranking does not lose here.** Call A dominant over B if, at every depth, the top of A holds at least as many relevant documents as the top of B, and more at some depth. Let the user click shown position $i$ with probability $1/i$ for a relevant document, and $1/(5i)$ or 0 for a document that is not relevant. For all pairs of rankings of at most 4 documents, the expected outcome is then at least 0 when A dominates B. It can be exactly 0, as in the example above. The sources give no proof of this for longer lists. Under the same click model, [balanced interleaving](/balanced-interleaving/) can prefer the dominated ranking.

## Variants and improvements

- **Balanced interleaving.** The older method, with the same kind of shown list but credit by the top $k$ of each ranking. See [balanced interleaving](/balanced-interleaving/).
- **Probabilistic interleaving.** Replace the deterministic pick by a draw from a softmax over each ranking, which gives credit to rank differences that team draft cannot see. See [probabilistic interleaving](/probabilistic-interleaving/).
- **More than two rankings.** The draft extends to several captains, who pick in a random order in each round. This is the basis of multileaved comparisons.

## When to use it

Team draft is the default choice for online comparison of two rankers that differ by small changes, because random clicks cannot bias it and the code is short. It cannot see a difference when the relevant document lands at the same shown position whichever team picks it, as in the insensitivity example, so for very close rankers, or to reuse logged clicks for a new pair of rankers, use probabilistic interleaving.

## Pitfalls

- **A coin that is not fresh.** Line L3 must draw a new fair coin in each round. If the coin is fixed, for example by a random generator that is seeded again with the same value for every query, A always picks first, its documents sit at positions 1, 3, 5 and so on, and [position bias](/position-bias/) alone makes A win. In the example, coins 1, 1 on every query give A the clicks on positions 1 and 3.
- **Credit by rank in the input ranking.** Line L10 must count clicks by team. Counting a click for both rankings when the document appears in both top parts is the credit of balanced interleaving and brings back its bias.
- **Skipping the shown test.** Lines L4 and L7 must take the first document not yet in $I$. Taking A's next document by rank only puts the same document on the page twice when both rankings share it.
- **Rankings with different documents.** The fairness claim needs both rankings to cover the same documents up to the page length. If one ranking is much shorter, the loop in line L2 stops when it is used up, and the last positions can go to one team.

## Implementations

## History

Radlinski, Kurup and Joachims introduced team-draft interleaving at CIKM 2008, next to balanced interleaving, after showing that the older method is biased when the two rankings are close. In their study on the arXiv.org search engine, both interleaving methods ordered rankings of known quality correctly, while none of eight absolute click metrics did so reliably. Hofmann, Whiteson and de Rijke (CIKM 2011) pointed out that team draft cannot detect some ranking differences, and proposed probabilistic interleaving. Chapelle, Joachims, Radlinski and Yue (2012) ran team draft and balanced interleaving at scale on commercial search engines and measured their agreement with offline judgments and with each other.

## References
