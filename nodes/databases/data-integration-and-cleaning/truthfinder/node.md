---
tag: HNKC9H
kind: algorithm
slug: truthfinder
name: TruthFinder
aliases:
- TruthFinder algorithm
area: databases/data-integration-and-cleaning
level: advanced
summary: "Iterate between the trust of sources and the confidence of the facts they claim, with similar facts supporting each other and conflicting facts counting against each other."
solves: [truth-discovery]
model: real-ram
complexity:
  vars: {n: the number of claims, d: the largest number of different facts on one object, k: the number of iterations}
  time: {worst: "O(k n d)", average: "O(k n d)", best: "O(n d)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: false, external: false, online: false, in_place: false, recursive: false}
history:
  year: 2007
  people: [Xiaoxin Yin, Jiawei Han, Philip S. Yu]
  note: "Presented at KDD 2007 and extended in IEEE TKDE in 2008. It was one of the first methods for truth discovery among conflicting web sources."
prereqs: [truth-discovery]
see_also: [hits-algorithm, pagerank, fixed-point-iteration, cosine-similarity, expectation-maximization, entity-resolution]
sources:
  - paper: doi:10.1145/1281192.1281309
    title: "Xiaoxin Yin, Jiawei Han and Philip S. Yu, Truth discovery with multiple conflicting information providers on the web, Proceedings of the 13th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2007, pages 1048 to 1052"
    locator: "Section 3.1.1 (Equations 1 to 4 and Lemma 1), Section 3.1.2 (the implication between facts, Equation 6), Section 3.1.3 (the dampening factor and the logistic function, Equation 8), Section 3.2 (the iteration and the cosine stop), Section 4 (the parameters and the book data)"
  - paper: "Xiaoxin Yin, Jiawei Han and Philip S. Yu, Truth discovery with multiple conflicting information providers on the web, IEEE Transactions on Knowledge and Data Engineering 20(6), 2008, pages 796 to 808"
    locator: the journal version
---

TruthFinder is an algorithm for [truth discovery](/truth-discovery/): many sources make claims about the same objects, the claims conflict, and the task is to pick the true value of each object without labels. TruthFinder gives each source a *trust* and each fact a *confidence*. The confidence of a fact grows with the trust of the sources that claim it, and the trust of a source is the mean confidence of its facts. It runs the two steps in turn until the trust values stop changing in direction. It also lets a fact gain support from similar facts on the same object and lose support to conflicting ones. The page [truth discovery](/truth-discovery/) states the problem and compares the other methods; this page gives TruthFinder in full. Its equations are heuristics with a probabilistic reading. There is no proof that the iteration converges or that it finds the truth.

## In plain words

Many web sites list the authors of the same books, and they do not agree. You do not know which sites to believe. TruthFinder starts by trusting every site the same. A fact that many trusted sites give gets a high score. A site whose facts have high scores becomes more trusted. Then the scores are computed again with the new trust, and so on, until the trust values settle. Facts that are close to each other, such as two spellings of one author list, help each other. Two different answers to the same question count against each other. At the end, for each book, you take the answer with the highest score.

## The problem

The input is a set of claims $(w, o, v)$: source $w$ says that object $o$ has value $v$. A *fact* is a pair $f = (o, v)$. $W(f)$ is the set of sources that claim $f$, and $F(w)$ is the set of facts of $w$. An optional *implication* $\mathrm{imp}(f' \to f) \in [-1, 1]$, for two facts on the same object, says how much $f'$ supports $f$: positive for similar values, negative for values that exclude each other. The paper uses $\mathrm{imp}(f' \to f) = \mathrm{sim}(f', f) - \mathit{base\_sim}$, with $\mathit{base\_sim} = 0.5$ on its book data. The output is a confidence $s(f)$ for each fact, a trust $t(w)$ for each source, and for each object the fact with the largest confidence.

## The algorithm

```pseudo id=main
TruthFinder(claims, imp, t0, ρ, γ, δ, T)
L1  for each source w do t(w) ← t0                    ▷ t0 = 0.9 in the paper
L2  repeat
L3      for each source w do τ(w) ← -ln(1 - t(w))
L4      for each fact f do σ(f) ← Σ over w in W(f) of τ(w)
L5      for each fact f do σ*(f) ← σ(f) + ρ · Σ over f' ≠ f on the same object of σ(f') · imp(f' → f)
L6      for each fact f do s(f) ← 1 / (1 + e^(-γ · σ*(f)))
L7      t_old ← t;  for each source w do t(w) ← the mean of s(f) over f in F(w)
L8  until 1 - cos(t_old, t) < δ or T iterations are done
L9  return s, t, and for each object the fact with the largest s
```

Lines L3 and L4 are the basic model. If each source is right with probability $t(w)$, independently, then $1 - e^{-\sigma(f)} = 1 - \prod_{w \in W(f)} (1 - t(w))$ is the probability that at least one source of $f$ is right (Lemma 1 of the paper). Working with $\tau = -\ln(1 - t)$ turns the product into a sum. Line L5 adds the support of the other facts on the same object, weighted by $\rho$. Line L6 uses the logistic function instead of $1 - e^{-\sigma^*}$, for two reasons: $\sigma^*$ can be negative, and sources copy each other, so the dampening factor $\gamma < 1$ makes the evidence count less than independence would say. Line L8 compares the direction of the trust vectors with [cosine similarity](/cosine-similarity/). The paper uses $\rho = 0.5$, $\gamma = 0.3$ and $\delta = 0.001\%$. The cap $T$ is not in the paper; the implementation adds it so that the loop always stops.

## Example

Three sources and three books. The implication is $-0.5$ between two different values of the same book, and the parameters are those of the paper.

| source | b1 | b2 | b3 |
|---|---|---|---|
| A | x | x | x |
| B | y | y | |
| C | | x | x |

For b1 the vote is a tie between x and y.

**Iteration 1.** All trusts are 0.9, so $\tau = -\ln 0.1 = 2.303$ for every source. For b1, $\sigma(x) = \sigma(y) = 2.303$, and each loses $0.5 \cdot 0.5 \cdot 2.303$ to the other, so $\sigma^* = 1.727$ and $s = 0.627$ for both. For b2, $\sigma(x) = 4.605$ and $\sigma(y) = 2.303$, so $\sigma^*(x) = 4.030$ and $\sigma^*(y) = 1.151$, which give $s = 0.770$ and $0.585$. For b3, $s(x) = 0.799$. The new trusts are the means: A = 0.732, B = 0.606, C = 0.785.

**Iteration 2.** A is now trusted more than B, so for b1 the confidence of x is 0.581 and that of y is 0.545. The tie is broken in favour of A.

The loop stops after 5 iterations, with trusts A = 0.611, B = 0.529 and C = 0.638 and the answer x for all three books. The trusts fall below 0.9 in every iteration, because the logistic function with $\gamma = 0.3$ keeps the confidences between 0.5 and 0.8 here.

**A larger run.** On generated data with 200 objects, 4 sources that are right 90% of the time and claim half of the objects, and 20 sources that are right 30% of the time, claim 15% of the objects and usually agree on one wrong value (Python seed 42, 1025 claims), the vote is right on 63% of the objects. TruthFinder is right on 72% without implications and 73% with the implication above, after 3 and 5 iterations. These numbers are measurements on that data only.

## Correctness

TruthFinder is a heuristic, so the claims that can be proved are about what it computes. All trust values stay strictly between 0 and 1, so every logarithm in line L3 is defined and every confidence is strictly between 0 and 1. When all trusts are equal and the implication is 0 or a fixed negative constant, the first iteration ranks the facts of each object by their number of sources, as a vote does; later iterations change the answers only through the trusts. The loop stops after at most $T$ iterations. There is no proof that the trusts converge, that the limit is unique, or that the facts with the highest confidence are true. The full statements are in [the proof page](proofs/correctness.md).

## Complexity

- **One iteration.** Lines L3, L4 and L7 take $O(n)$ for $n$ claims. Line L5 takes $O(\sum_o d_o^2) = O(n d)$ calls of imp, where $d_o$ is the number of different facts on object $o$. Without implications, line L5 is free and an iteration takes $O(n)$.
- **The run.** $k$ iterations take $O(k n d)$. On the book data of the paper the trusts settled after a few iterations; this is a measurement, not a bound, so $T$ caps $k$.
- **Space.** $O(n)$ for the claims, trusts and confidences.

## Properties

- **Heuristic.** The trust and confidence equations, $\rho$, $\gamma$ and $t_0$ are choices of the authors, set on their data.
- **Mutual reinforcement.** Like [HITS](/hits-algorithm/) and [PageRank](/pagerank/), it computes two scores from each other, but its update is not linear and has no eigenvector form.
- **Fixed point method.** The update maps trust vectors in $(0, 1)^{|W|}$ to trust vectors, so a limit, if there is one, is a fixed point of that map, as in [fixed-point iteration](/fixed-point-iteration/).
- **Deterministic.** Ties are broken by a fixed order of the values.
- **Independence assumption.** Line L4 treats sources as independent. $\gamma$ only weakens all evidence by the same factor; it does not find which sources copy.

## Variants and improvements

- **Without implications.** Set $\mathrm{imp} = 0$. Then each fact depends only on its own sources, which is a vote weighted by $\tau$.
- **Similarity of values.** For lists of authors the paper defines the similarity from the number of shared authors; numbers and strings need their own similarity.
- **Probabilistic models.** Later methods put the sources and the truths in one probabilistic model and fit it with [expectation maximization](/expectation-maximization/) or sampling. They can model a false positive rate and a false negative rate for each source.
- **Copy detection.** Dong, Berti-Equille and Srivastava model which sources copy from which, instead of one global $\gamma$.
- **Optimization methods.** Methods such as CRH write truth discovery as the minimization of a weighted loss over sources and truths, with an alternating solver.

## When to use it

Use it when many sources claim values for many objects, you have no labels, and you believe that sources that are often right on the objects where others agree with them are also right elsewhere. It helps most when a few sources cover many objects and many weak sources each cover a few. With few sources, or when every source covers only a few objects, the trusts carry little information and a vote does about as well.

## Pitfalls

- **The cosine stop sees only the direction.** If all trusts change by the same factor, the cosine is 1 and the loop stops; with one source it always stops after one iteration. A cap and a check of the absolute change are safer.
- **Narrow trust range.** With $\gamma = 0.3$ the confidences of facts with positive $\sigma^*$ stay above 0.5, so the trusts of good and bad sources can be close, and a large group of weak sources can still outvote one good source.
- **Copying.** Sources that copy one source count as many. The global $\gamma$ does not fix this for one group of copiers.
- **Single truth.** It picks one value for each object. Objects with several true values, such as a list of authors read as separate facts, need a different model.
- **Implication on the wrong scale.** $\rho$ multiplies sums of $\sigma$ that grow with the number of sources, so a strong negative implication on a popular object can drive all its confidences below 0.5.

## Implementations

## History

Yin, Han and Yu introduced TruthFinder at KDD 2007 and gave the full version in IEEE TKDE in 2008. They studied the authors of computer science books listed by online bookstores: 1265 books, 894 bookstores and 34031 listings. With $\rho = 0.5$ and $\gamma = 0.3$ they measured an accuracy of about 95% on that data after three iterations. Later work on truth discovery added copy detection, probabilistic models and optimization models.

## References
