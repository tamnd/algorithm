---
tag: SMYWR9
kind: algorithm
slug: smatch
name: "Smatch"
aliases:
- semantic match score
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: Score two AMR graphs by the F1 of matching triples under the best variable mapping, found by hill climbing with restarts.
model: word-ram
complexity:
  vars: {m: the number of variables of the test graph, n: the number of variables of the gold graph, t: the number of triples of both graphs, r: the number of restarts}
  time: {worst: O(r t^2 (m n + m^2))}
  space: {extra: O(t + m + n)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2013
  people: [Shu Cai, Kevin Knight]
  note: "Cai and Knight defined Smatch for the evaluation of AMR parsers, showed that the best mapping can be found with an integer program, and used hill climbing with a concept-matching start and random restarts because it is much faster."
prereqs: [abstract-meaning-representation, hill-climbing]
see_also: [random-restart-hill-climbing, subgraph-isomorphism, quadratic-assignment-problem, maximum-common-subgraph, precision-and-recall, parseval-measures, attachment-score, semantic-parsing]
sources:
  - paper: "Shu Cai and Kevin Knight, Smatch: an Evaluation Metric for Semantic Feature Structures, Proceedings of ACL 2013 (Volume 2: Short Papers), 748-752"
    title: "Shu Cai and Kevin Knight, Smatch: an Evaluation Metric for Semantic Feature Structures"
    locator: "Section 2 (the triples, the example and the score), Section 3 (the integer program, hill climbing, smart initialization and restarts), Table 2 (accuracy and speed of the methods)"
  - paper: "Laura Banarescu, Claire Bonial, Shu Cai, Madalina Georgescu, Kira Griffitt, Ulf Hermjakob, Kevin Knight, Philipp Koehn, Martha Palmer and Nathan Schneider, Abstract Meaning Representation for Sembanking, Proceedings of the 7th Linguistic Annotation Workshop and Interoperability with Discourse, 2013, 178-186"
    title: "Laura Banarescu et al., Abstract Meaning Representation for Sembanking"
    locator: "the PENMAN notation of AMR and the use of Smatch for agreement between annotators"
---

Smatch compares two [abstract meaning representation](/abstract-meaning-representation/) graphs, a test graph from a parser and a gold graph from an annotator, and gives one number between 0 and 1. It writes each graph as a set of triples, maps the variables of the test graph one to one onto the variables of the gold graph, counts the triples that match, and reports the F1 of the best mapping. Finding the best mapping is NP-hard, so the standard tool searches with [hill climbing](/hill-climbing/) from a concept-matching start plus random restarts, and the score it reports can be slightly below the true Smatch score. It is the usual metric for [semantic parsing](/semantic-parsing/) into AMR, in the way that [PARSEVAL](/parseval-measures/) is for constituency trees, but it has no fixed alignment to the words, which is why it needs a search.

## In plain words

Two people draw the meaning of a sentence as a graph. Each graph has boxes such as "want" and "boy" and labeled arrows such as "the wanter is the boy". The box names in the two drawings are arbitrary, so before comparing them we must decide which box in one drawing goes with which box in the other.

For a given pairing, list every fact of the first drawing and count how many also appear in the second. The score is based on the best pairing: it rewards facts that both drawings share and punishes facts that only one of them has.

Trying every pairing is too slow for large graphs. So the program starts from a good guess, pairing boxes with the same name, and makes the change that helps most until no change helps. It repeats this from a few random guesses and keeps the best result.

## The problem

An AMR graph is a set of triples of three kinds: `instance(v, c)` says that the variable $v$ is an instance of the concept $c$, `role(v, w)` is a relation between two variables, and `role(v, k)` gives a variable an attribute with a constant $k$, such as `polarity(v, -)`. The test graph $T$ has $m$ variables, the gold graph $G$ has $n$ variables, and the two graphs have $t$ triples together.

A mapping $\varphi$ sends each test variable to a different gold variable or to nothing. Constants map to themselves. A test triple matches if all its variables are mapped and its image is a triple of $G$. Let $M(\varphi)$ be the number of matched test triples. Then

$$P = \frac{M}{|T|}, \qquad R = \frac{M}{|G|}, \qquad F = \frac{2PR}{P + R} = \frac{2M}{|T| + |G|}.$$

Smatch is $F$ for the mapping with the largest $M$. One mapping maximizes $P$, $R$ and $F$ together, because the denominators do not depend on the mapping. The match count is symmetric: the best $M$ from $T$ to $G$ equals the best $M$ from $G$ to $T$.

For a corpus, Smatch adds up $M$, $|T|$ and $|G|$ over all sentence pairs and then applies the same formulas. This gives more weight to large graphs than the mean of the sentence scores would.

## The algorithm

```pseudo id=main
CLIMB(T, G, φ)
L1  M ← the number of test triples that match under φ
L2  loop
L3      for each test variable a and each gold variable g that is unused, or nothing: gain of sending a to g
L4      for each pair of test variables a, b: gain of swapping their images
L5      if no move has a positive gain then return (M, φ)
L6      apply the move with the largest gain;  M ← M + gain

SMATCH(T, G, r)
L7  (best, φ*) ← CLIMB(T, G, SMART-INIT(T, G))
L8  repeat r times: (M, φ) ← CLIMB(T, G, a random one to one mapping)
L9      if M > best then (best, φ*) ← (M, φ)
L10 return P, R and F for best
```

SMART-INIT sends each test variable to the first unused gold variable with the same concept, and leaves it unmapped if there is none. Lines L3 and L4 are the two kinds of moves of Cai and Knight: change the image of one variable, and swap the images of two variables. Both keep the mapping one to one. Line L6 takes the steepest move, so this is steepest-ascent hill climbing, and lines L7 to L9 make it [random-restart hill climbing](/random-restart-hill-climbing/). The implementation also has an exact search that tries every mapping, which the tests use as the reference.

## Example

The example of Cai and Knight, section 2. The gold graph says "the boy wants to go" and the test graph says "the boy wants the football":

```
gold: (a / want-01 :ARG0 (b / boy) :ARG1 (c / go-01 :ARG0 b))
test: (x / want-01 :ARG0 (y / boy) :ARG1 (z / football))
```

The gold graph has 6 triples: three instance triples, `ARG0(a, b)`, `ARG1(a, c)` and `ARG0(c, b)`. The test graph has 5: three instance triples, `ARG0(x, y)` and `ARG1(x, z)`. The six full mappings of $x, y, z$ onto $a, b, c$ give:

| image of $x, y, z$ | matched triples | $M$ |
|---|---|---|
| $a, b, c$ | `instance(x, want-01)`, `instance(y, boy)`, `ARG0(x, y)`, `ARG1(x, z)` | 4 |
| $a, c, b$ | `instance(x, want-01)` | 1 |
| $b, a, c$ | none | 0 |
| $b, c, a$ | none | 0 |
| $c, a, b$ | none | 0 |
| $c, b, a$ | `instance(y, boy)`, and `ARG0(x, y)`, whose image is `ARG0(c, b)` | 2 |

The best mapping is $x \to a$, $y \to b$, $z \to c$ with $M = 4$, so $P = 4/5$, $R = 4/6 = 2/3$, and $F = 8/11 \approx 0.73$. The smart start finds this mapping directly here, because `want-01` and `boy` occur once in each graph.

Hill climbing can stop too early. Take the test graph `instance(t0, p)`, `instance(t1, q)`, `r(t0, t1)` and the gold graph `instance(g0, q)`, `instance(g1, q)`, `r(g0, g1)`. The smart start leaves $t_0$ unmapped, because no gold variable has the concept $p$, and sends $t_1$ to $g_0$, with $M = 1$. No single move raises $M$, so the climb stops at 1. The best mapping, $t_0 \to g_0$ and $t_1 \to g_1$, has $M = 2$: it gives up nothing and gains the relation, but it takes two moves to reach, and the first of them lowers $M$. A random restart can start near it.

## Correctness

The full proofs are in proofs/correctness.md. The claims:

- **Exact search (theorem).** The search over every one to one partial mapping returns the best $M$, and so the true Smatch score. It is enough to try mappings that map $\min(m, n)$ variables, because mapping one more variable to an unused gold variable never loses a match.
- **Hill climbing (theorem).** Each step raises $M$ by at least 1, and $M \le |T|$, so CLIMB takes at most $|T|$ steps and stops. Every mapping it holds is one to one, so the reported $M$ is at most the best $M$: the reported score is a lower bound on the true score.
- **Not exact (theorem, with the example above).** A climb can stop at a local maximum below the best $M$.
- **NP-hardness (theorem).** Deciding whether some mapping has $M \ge k$ is NP-complete. The proof reduces [subgraph isomorphism](/subgraph-isomorphism/): give every vertex the concept `node` and turn each edge into two `edge` triples, one in each direction. Then a graph $H$ is a subgraph of $K$ exactly when the best $M$ equals the number of triples of $H$, $|V(H)| + 2|E(H)|$. Cai and Knight note that the problem is NP-complete; the reduction on this page is written out for it.

## Complexity

**Exact search.** There are $\sum_{k} \binom{m}{k} \frac{n!}{(n-k)!} \le (n + 1)^m$ one to one partial mappings, and each takes $O(t)$ time to score with a [hash table](/hash-table/) of gold triples. For $m = n = 5$ there are 1546. The exact search is only for tiny graphs.

**Hill climbing.** One step looks at $m(n + 1) + \binom{m}{2}$ moves. Scoring a move from scratch takes $O(t)$, so a step takes $O(t(m n + m^2))$, and a climb has at most $|T| \le t$ steps. With $r$ restarts the worst case is $O(r\,t^2 (m n + m^2))$, expected with hashing. The space is $O(t + m + n)$. The implementation on this page scores moves from scratch for clarity. The standard tool first lists, for each test triple, the pairs of variable images that would make it match, and then computes the gain of a move from the triples that touch the moved variables, which is much faster in practice.

**Measurement.** Cai and Knight compared the integer program, which is exact, with hill climbing from a smart start and four random restarts on AMR data, and found that hill climbing gave nearly the same scores at a small fraction of the time. That setting is the default of the tool.

## Properties

- **Symmetric match count.** The best $M$ from $T$ to $G$ equals the best $M$ from $G$ to $T$, so swapping the graphs swaps $P$ and $R$ and keeps $F$.
- **Identity.** A graph scored against itself, with renamed variables, gets $F = 1$, and hill climbing finds it from the smart start when every concept occurs once.
- **Lower bound.** The reported score never exceeds the true one. More restarts can only raise it.
- **Randomized.** The result depends on the random restarts. With a fixed seed it is reproducible.
- **No word alignment.** The score depends only on the graphs. Two graphs can score high even if a parser got the concepts from the wrong words.

## Variants and improvements

- **Integer program.** Cai and Knight also write the search as a 0-1 integer program, with one variable for each pair of test and gold variables and one for each pair of triples that could match, which gives the exact score with a general solver at a much higher cost. See [binary integer programming](/binary-integer-programming/).
- **Fine-grained scores.** Later tools split the triples by kind and report separate scores for concepts, named entities, negation, reentrancies and semantic roles, to show where a parser fails.
- **Faster or exact metrics.** Later work replaced the search with an exact solver, or with a metric that compares graphs through their paths or through graph kernels, to avoid the randomness of the search.

## When to use it

Use Smatch to evaluate an AMR parser against gold graphs, to measure agreement between two annotators, and in general to compare two small labeled graphs whose node names are arbitrary. Report the corpus score, state the number of restarts or use the default, and use the same tool for every system in a comparison. For graphs that come with an alignment to the words, a metric that uses the alignment is cheaper and exact.

## Pitfalls

- **Averaging sentence scores.** The corpus score sums the counts. The mean of the sentence F values is a different number.
- **Hill climbing noise.** Two runs with different seeds can give slightly different scores. Small differences between systems can be within this noise.
- **Variable names.** Both graphs must use separate variable names, or a reader must rename them first. Otherwise a test variable can be confused with a gold one.
- **Inverse roles.** In PENMAN notation `:ARG0-of` is the inverse of `:ARG0`. The reader must turn `(b :ARG0-of w)` into `ARG0(w, b)`, or equal graphs will not match.
- **Constants and quotes.** `"Ed"` and `Ed` must be read as the same constant.
- **Tool versions.** Tools differ in small details, such as whether the root gets an extra triple. Compare scores only from the same tool.

## Implementations

## History

Cai and Knight introduced Smatch in 2013, the year of the first AMR release by Banarescu and others, who used it to measure agreement between annotators. Cai and Knight wrote the triples, the F1 score and the integer program, and they made hill climbing with a smart start and four random restarts the practical method. Smatch became the standard metric for AMR parsing, and later work added fine-grained scores and exact or faster variants.

## References
