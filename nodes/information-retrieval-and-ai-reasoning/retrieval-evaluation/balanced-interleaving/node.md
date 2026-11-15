---
tag: 8GEA8G
kind: algorithm
slug: balanced-interleaving
name: Balanced interleaving
aliases:
- Joachims balanced interleaving
area: information-retrieval-and-ai-reasoning/retrieval-evaluation
level: advanced
summary: Merges two rankings so that every prefix of the shown list holds top prefixes of both of nearly equal length, and compares the clicks inside those prefixes.
model: word-ram
complexity:
  vars: {n: the sum of the lengths of the two rankings}
  time: {worst: O(n)}
  space: {extra: O(n)}
properties: {deterministic: false, recursive: false}
prereqs: [interleaved-evaluation]
see_also: [team-draft-interleaving, probabilistic-interleaving, click-model, position-bias, position-based-click-model, implicit-feedback, sign-test]
sources:
  - paper: "Thorsten Joachims, Evaluating retrieval performance using clickthrough data, in J. Franke, G. Nakhaeizadeh and I. Renz (editors), Text Mining, Physica/Springer Verlag, 2003, pp. 79-96"
    title: Evaluating retrieval performance using clickthrough data
    locator: the method that merges two rankings into one list with balanced prefixes and compares the clicks on the top of each ranking
  - paper: doi:10.1145/1458082.1458092
    title: Filip Radlinski, Madhu Kurup and Thorsten Joachims, How does clickthrough data reflect retrieval quality?, CIKM 2008, pp. 43-52
    locator: Section 5.1, Algorithm 1 and equations (1) to (3) (balanced interleaving and its credit rule); Section 5.2 (the bias example with A = (a, b, c, d) and B = (b, c, d, a)); the user study on arXiv.org
  - paper: doi:10.1145/2063576.2063618
    title: Katja Hofmann, Shimon Whiteson and Maarten de Rijke, A probabilistic method for inferring preferences from clicks, CIKM 2011, pp. 249-258
    locator: Section 3.1 and Figure 1 (the bias of balanced interleave under random clicks)
  - paper: doi:10.1145/2094072.2094078
    title: Olivier Chapelle, Thorsten Joachims, Filip Radlinski and Yisong Yue, Large-scale validation and analysis of interleaved search evaluation, ACM Transactions on Information Systems 30(1), Article 6, 2012
    locator: the comparison of balanced and team-draft interleaving with each other and with offline judgments on commercial search engines
---

Balanced interleaving is the first [interleaved evaluation](/interleaved-evaluation/) method: it merges two rankings A and B of the same query into one shown list, so that every prefix of the shown list is the union of a top part of A and a top part of B whose lengths differ by at most 1. A fair coin decides which ranking gives the first document. The user's clicks then count for a ranking if they fall in the top k of that ranking, where k comes from the lowest click, and the ranking with more such clicks wins the query. The method is due to Joachims, and Radlinski, Kurup and Joachims later showed that it can prefer one ranking under clicks that carry no information.

## In plain words

Two search engines each give a list of results for the same query. We want to show one list to the user and learn which engine is better from the clicks. Balanced interleaving takes results from the two lists in turns: first from one list, then from the other, and so on, and it skips a result that is already shown. A coin decides which list starts. So the top of the shown list always contains the top few results of both engines, in about equal numbers.

After the user clicks, look at the lowest click. Find how deep you must go in either engine's list to reach that result. Count the clicks inside that depth for each engine. The engine with more counted clicks wins this query.

## The problem

The input is two rankings $A = (a_1, a_2, \ldots)$ and $B = (b_1, b_2, \ldots)$ for one query, each with no repeated document, and a fair coin. The output is a shown list $I$ with no repeated document. After the user clicks the set $C$ of documents of $I$, the output is a preference $o \in \{-1, 0, 1\}$, where 1 means that A is preferred.

Over many queries the wins of A and of B are counted, and a [sign test](/sign-test/) on the queries with a preference decides if one ranking wins more often than chance.

## The algorithm

```pseudo id=main
BALANCED-INTERLEAVE(A, B, a_first)       ▷ a_first: the result of one fair coin
L1  I ← empty list, ka ← 1, kb ← 1
L2  while ka ≤ |A| and kb ≤ |B| do
L3      if ka < kb or (ka = kb and a_first) then
L4          if A[ka] ∉ I then append A[ka] to I
L5          ka ← ka + 1
L6      else
L7          if B[kb] ∉ I then append B[kb] to I
L8          kb ← kb + 1
L9  return I

CREDIT(A, B, I, C)                        ▷ C: the clicked documents of I
L10 if C is empty then return 0
L11 c ← the document of C at the lowest position in I
L12 k ← min(rank of c in A, rank of c in B)       ▷ rank ∞ if absent
L13 ha ← |C ∩ {A[1], …, A[k]}|, hb ← |C ∩ {B[1], …, B[k]}|
L14 return 1 if ha > hb, -1 if ha < hb, else 0
```

The pointer $ka$ is the next rank of A to look at, and $kb$ the next rank of B. Line L3 lets the list with the smaller pointer move, and the coin decides when the pointers are equal. So the pointers never differ by more than 1. A document that is already in $I$ is passed over in line L4 or L7, but the pointer still moves. The loop stops as soon as one ranking is used up, so in practice both rankings are cut to the same length first, for example the number of results on a page.

Lines L11 to L13 are equations (1) to (3) of Radlinski, Kurup and Joachims. The rank $k$ is the smallest depth at which the lowest click is in the top of A or of B. The user is assumed to have read about $k$ results of each ranking, and the clicks inside these two tops are compared.

## Example

Take the rankings of the bias example of Radlinski, Kurup and Joachims: $A = (a, b, c, d)$ and $B = (b, c, d, a)$, with $a\_first$ = true.

| step | ka | kb | line | document looked at | I |
|---|---|---|---|---|---|
| 1 | 1 | 1 | L4 | A[1] = a, new | a |
| 2 | 2 | 1 | L7 | B[1] = b, new | a, b |
| 3 | 2 | 2 | L4 | A[2] = b, already in I | a, b |
| 4 | 3 | 2 | L7 | B[2] = c, new | a, b, c |
| 5 | 3 | 3 | L4 | A[3] = c, already in I | a, b, c |
| 6 | 4 | 3 | L7 | B[3] = d, new | a, b, c, d |
| 7 | 4 | 4 | L4 | A[4] = d, already in I | a, b, c, d |

After step 7, $ka = 5 > |A|$ and the loop stops. With $a\_first$ = false the same steps give $I = (b, a, c, d)$.

Now let the user click exactly one document, chosen uniformly at random from the 4 shown. For $I = (a, b, c, d)$:

| click | rank in A | rank in B | k | ha | hb | outcome |
|---|---|---|---|---|---|---|
| a | 1 | 4 | 1 | 1 | 0 | A |
| b | 2 | 1 | 1 | 0 | 1 | B |
| c | 3 | 2 | 2 | 0 | 1 | B |
| d | 4 | 3 | 3 | 0 | 1 | B |

For $I = (b, a, c, d)$ the outcomes are B, A, B, B. So a click that does not depend on the documents at all prefers B with probability $3/4$ and A with probability $1/4$. B is A with its first document moved to the end, and three of its four documents sit one rank higher than in A. This is the bias that Radlinski, Kurup and Joachims point out.

A second example, from the figure of the same paper: $A = (a, b, c, d, g, h)$ and $B = (b, e, a, f, g, h)$. The two shown lists are $(a, b, e, c, d, f, g, h)$ and $(b, a, e, c, f, d, g, h)$. If the user clicks b and e, the lowest click is e, which is at rank 2 of B and not in A, so $k = 2$. Then $ha = 1$ (only b is in the top 2 of A) and $hb = 2$, and B wins with either shown list.

## Correctness

The proof is in `proofs/correctness.md`. The key invariant holds after each step of the loop: the set of documents in $I$ equals $\{A[1], \ldots, A[ka-1]\} \cup \{B[1], \ldots, B[kb-1]\}$, $I$ has no repeated document, and $(ka - 1) - (kb - 1)$ is 0 or 1 when $a\_first$ is true, 0 or $-1$ when it is false. A prefix of $I$ is the value of $I$ after some step, so every prefix of $I$ is the union of a top $ka'$ of A and a top $kb'$ of B with $|ka' - kb'| \le 1$. This is the property that the sources state for the method. CREDIT computes equations (1) to (3) directly; the rank $k$ is finite because $c$ is in $I$, and every document of $I$ comes from A or B.

The invariant does not make the method fair. A prefix holds equal numbers of ranks of A and B, but when the two rankings share documents, one ranking can have more of its documents in the prefix than the other at the depth $k$ that line L12 picks. The example above shows the result.

## Complexity

- **Time.** Each step of the loop moves $ka$ or $kb$ by 1, so there are at most $|A| + |B|$ steps. With a hash set of the shown documents, the test in line L4 or L7 costs $O(1)$, so BALANCED-INTERLEAVE runs in $O(n)$ time with $n = |A| + |B|$. CREDIT finds the positions and ranks in one pass over each list, so it also costs $O(n)$.
- **Space.** $I$ and the hash set hold at most $n$ documents, so the extra space is $O(n)$.
- **Coins.** One fair coin per query, used only in line L3.

## Properties

- **Balanced prefixes.** Every prefix of $I$ holds the top $ka'$ of A and the top $kb'$ of B with $|ka' - kb'| \le 1$. If A and B are the same ranking, $I$ is that ranking.
- **One shown list per coin value.** For fixed A and B there are at most two shown lists, one for each value of the coin. The user sees a normal result list, and nothing marks which ranking gave which document.
- **Biased under random clicks.** A click model that ignores the documents can still prefer one ranking in expectation, as in the example. Hofmann, Whiteson and de Rijke show the same effect with $l_1 = (d_1, d_2, d_3, d_4)$ and $l_2 = (d_2, d_3, d_4, d_1)$.
- **Dominance does not always win.** Call A dominant over B for a set of relevant documents if, at every depth, the top of A holds at least as many relevant documents as the top of B, and more at some depth. Let the user click each shown position $i$ with probability $1/i$ if its document is relevant and 0 if not. For all pairs of rankings of at most 3 documents, a dominant A then never loses in expectation. With 4 documents it can: for $A = (b, c, a, d)$, $B = (c, a, d, b)$ and only a not relevant, the expected outcome is $-1/16$, so B is preferred. The shown lists are $(b, c, a, d)$ and $(c, b, a, d)$, and a click on d counts for B, since d is at rank 3 of B and rank 4 of A. If the user also clicks a not relevant document with probability $1/5$ of the relevant case, the pair $A = (a, b, c)$, $B = (b, c, a)$ with c not relevant gives $-1/60$.

## Variants and improvements

- **Team-draft interleaving.** Give each shown document to the ranking that picked it, and credit clicks by team. Over the coin flips each ranking gets each position with probability 1/2, so clicks that ignore the documents give a tie in expectation. See [team-draft interleaving](/team-draft-interleaving/).
- **Probabilistic interleaving.** Pick documents at random from softmax distributions over both rankings, and compare the clicks in expectation over the possible assignments. See [probabilistic interleaving](/probabilistic-interleaving/).
- **Length cut.** Cut both rankings to the page length before line L1, so that the loop does not stop early on a short ranking.
- **Aggregation.** Count a win per query, or give each user one vote from the majority of the user's queries; Radlinski, Kurup and Joachims report both.

## When to use it

Use balanced interleaving when the two rankings differ a lot near the top, as in its first uses, and when a simple, deterministic credit rule is wanted. When the rankings are close, for example the same ranking with a small shift, the bias in the example can decide the outcome, and team-draft or probabilistic interleaving is the safer choice. All three methods need many queries; the outcome of one query is noisy.

## Pitfalls

- **No membership test.** Lines L4 and L7 must append a document only if it is not already in $I$. Without the test, $A = (a, b)$ and $B = (b, a)$ with $a\_first$ = true give $I = (a, b, b, a)$, and the user sees each result twice.
- **Depth from the shown list.** Line L12 must take the rank of the lowest click in A and in B, not its position in $I$. In the example, a click on c in $I = (a, b, c, d)$ has position 3, and with $k = 3$ both tops contain c, so the outcome is a tie. With the right line, $k = 2$ and B wins.
- **Or in place of and.** Line L2 must stop when either ranking is used up. With "or", line L4 or L7 reads past the end of the shorter ranking. Cut both rankings to the same length instead.
- **Assuming fairness.** Random clicks do not give a tie in expectation. Before reading a small win as a real difference, check how close the two rankings are.

## Implementations

## History

Joachims proposed the method in 2002 and 2003, in work on learning and evaluating rankings from clickthrough data, as a way to get unbiased paired comparisons from clicks. Radlinski, Kurup and Joachims (CIKM 2008) named it balanced interleaving, gave it as Algorithm 1 with the credit rule of equations (1) to (3), and showed its bias on close rankings. In a study on the arXiv.org search engine they made known changes to a ranking and found that none of eight absolute click metrics, such as the clicks per query, reliably showed the order of quality, while balanced and team-draft interleaving did. Hofmann, Whiteson and de Rijke (CIKM 2011) analysed the bias with a random click model, and Chapelle, Joachims, Radlinski and Yue (2012) compared interleaving methods on large commercial search engines and measured how well their outcomes agree with offline judgments.

## References
