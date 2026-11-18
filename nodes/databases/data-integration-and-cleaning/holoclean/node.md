---
tag: DV1WKR
kind: algorithm
slug: holoclean
name: HoloClean probabilistic repair
aliases:
- HoloClean
area: databases/data-integration-and-cleaning
level: research
summary: "Repair data by compiling constraints, value statistics and external data into one probabilistic model, learning its weights on clean cells and inferring the most likely value of each noisy cell."
solves: [database-repair]
model: word-ram
complexity:
  vars: {n: the number of rows, a: the number of attributes, v: the largest number of distinct values in an attribute, q: the number of denial constraints, p: the largest number of predicates in a constraint, e: the number of learning epochs}
  time: {worst: O(n^2 a v q p + e n a v (a + q))}
  space: {extra: O(n a (a + v (a + q)))}
properties: {deterministic: false, exact: false, online: false, in_place: false, recursive: false}
history:
  year: 2017
  people: [Theodoros Rekatsinas, Xu Chu, Ihab F. Ilyas, Christopher Ré]
  note: "Rekatsinas, Chu, Ilyas and Ré presented HoloClean in PVLDB in 2017. It combined the constraint-based repair of Holistic data cleaning with the statistical inference engine of DeepDive."
prereqs: [denial-constraint, factor-graph, gibbs-sampling, database-repair]
see_also: [conditional-functional-dependency, functional-dependency, softmax-regression, markov-random-field, truth-discovery, entity-resolution, consistent-query-answering, functional-dependency-discovery]
sources:
  - url: https://www.vldb.org/pvldb/vol10/p1190-rekatsinas.pdf
    title: "Theodoros Rekatsinas, Xu Chu, Ihab F. Ilyas and Christopher Ré, HoloClean: holistic data repairs with probabilistic inference, PVLDB 10(11), 2017"
    locator: "pages 1190-1201: Section 3 (the signals and the factor graph), Section 4 (compilation to DDlog), Algorithm 2 (domain pruning), Section 5.2 (relaxed denial constraints), Section 6 (experiments)"
  - paper: doi:10.1109/icde.2013.6544847
    title: "Xu Chu, Ihab F. Ilyas and Paolo Papotti, Holistic data cleaning: putting violations into context, ICDE 2013"
    locator: "pages 458-469, detection and repair with denial constraints"
  - paper: doi:10.14778/2536258.2536262
    title: "Xu Chu, Ihab F. Ilyas and Paolo Papotti, Discovering denial constraints, PVLDB 6(13), 2013"
    locator: "pages 1498-1509, the language of denial constraints"
---

HoloClean repairs a dirty table by treating each suspicious cell as a random variable and choosing its most likely value under a model learned from the table itself. It solves the same task as the minimal repairs of [database repair](/database-repair/), but it chooses differently. A minimal repair changes as little as it can to satisfy the constraints. HoloClean weighs the constraints together with how often values occur together and with outside data, so it can make a larger change when the statistics support it, and it may leave a violation in place. It is a heuristic: nothing guarantees that its repairs are the true values, and its quality is known only from measurements. The code on this page is a toy that keeps the main steps, not the HoloClean system.

## In plain words

Some cells of a table break a rule, such as "one zip code has one city". These cells are the suspects. For each suspect, HoloClean lists a few likely values: the value it has now, and the values that often appear next to the other values of its row.

Each candidate value gets a score from a few signals: how often it appears with the rest of the row, how many rule breaks it would cause, and a bonus for being the value that is already there. HoloClean learns how much each signal counts from the cells that broke no rule, since their values are probably right. Then each suspect takes the candidate with the highest score.

## The problem

The input is a table with $n$ rows and $a$ attributes, a set of [denial constraints](/denial-constraint/), and a threshold $\tau$. The table is a list of rows, so equal rows count separately. A *cell* is a pair of a row and an attribute. Each cell has an unknown true value and an observed value, and some observed values are wrong. The output is a value for each cell, together with a probability for each candidate value of each cell that the method changes.

There is no exact objective that the output is proved to optimize. The goal is measured accuracy: the fraction of changed cells that are now right (precision) and the fraction of wrong cells that are now right (recall).

## The algorithm

```pseudo id=main
HOLOCLEAN(D, Sigma, tau)
L1  noisy <- the cells that take part in a violation of a constraint in Sigma
L2  for each cell c of D do
L3      dom(c) <- {v_c} together with each value v with Pr[v | v_c'] >= tau for another cell c' of the row
L4  for each cell c and each d in dom(c) do
L5      f(c, d) <- the co-occurrence statistics Pr[d | v_c'], and the relaxed violation count of each constraint
L6  w <- the weights that maximize the likelihood of the observed values of the clean cells
L7  for each noisy cell c do
L8      P(c, d) <- the softmax over d of w . f(c, d) + prior . [d = v_c]
L9      set c to the value d with the largest P(c, d)
L10 return the repaired table and the probabilities P

GIBBS(D, model, sweeps)
L11 x <- the observed values of the noisy cells
L12 for s <- 1 to sweeps do
L13     for each noisy cell c do
L14         draw x_c with probability proportional to exp(unary(c, x_c) - the weights of the violated pair factors at c)
L15         after the burn-in, count the value of x_c
L16 return the frequency of each value of each cell
```

Line L1 is error detection. A pair of rows that violates a constraint makes every cell of the constraint's attributes in both rows noisy. Line L3 is domain pruning, Algorithm 2 of the paper: a value enters the domain only if it often appears together with some other value of the row. The threshold $\tau$ trades the size of the model against the chance that the true value is missing.

Lines L4 and L5 build the features. In the paper the signals are compiled into a [factor graph](/factor-graph/) by DDlog rules. The co-occurrence features say how likely a value is given each other cell of the row. A denial constraint would give a factor on each pair of rows, which makes the graph huge. The paper's relaxation, Section 5.2, replaces it with a feature of one cell: the number of rows that would conflict with the candidate value if all other cells kept their observed values. After this relaxation the noisy cells are independent given the observed table, and line L8 is exact.

Line L6 is multinomial [softmax regression](/softmax-regression/) with the observed values of the clean cells as labels. The prior term of line L8 is the minimality signal: it prefers the value a cell already has. Lines L11 to L16 are the [Gibbs sampler](/gibbs-sampling/) for the model without the relaxation, in which the pair factors stay. The toy uses it to show the difference between the two models.

## Example

The constraints say that a zip code fixes the city and the state. The table has 8 rows: (z1, Chicago, IL) three times, (z1, Chicgo, IL), (z4, Peoria, IL) twice and (z2, Boston, MA) twice. Row 3, counted from 0, holds the typo. The threshold is $\tau = 0.3$ and the prior is 1.

| step | result |
|---|---|
| L1 | noisy: the zip and city cells of rows 0 to 3, which form violations of "zip fixes city" |
| L3 | dom of the city of row 3: Chicago, Chicgo, Peoria; dom of each zip cell of rows 0 to 5: z1, z4 |
| L5, city of row 3 | Chicago: Pr[Chicago given z1] = 0.75, 0 conflicts; Chicgo: 0.25, 3 conflicts; Peoria: 0, 3 conflicts |
| L5, zip of row 3 | z1: 3 conflicts with the Chicago rows; z4: 2 conflicts with the Peoria rows |
| L6 | 4 clean training cells, the zip and city cells of the Peoria rows; the learned weights are 0.87 for Pr[city given zip] and minus 1.39 per conflict |
| L8 | city of row 3: Chicago 0.965, Chicgo 0.028, Peoria 0.008; zip of row 3: z1 0.432, z4 0.568 |
| L9 | the city of row 3 becomes Chicago, which is right; the zip of row 3 becomes z4, which is wrong |

The wrong change comes from the relaxation. The zip cell is scored with the city fixed at the typo, and with that city every zip in its domain causes conflicts, z4 a little fewer. The joint model would see that fixing the city removes all conflicts of z1. The test file measures the same effect on synthetic data: over 8 random tables with 60 injected errors, the toy fixed all 60 and made 12 wrong changes, all of them zip cells next to a wrong state (a measurement).

## Correctness

HoloClean has no correctness theorem in the sense of returning the true values. The [proof file](proofs/correctness.md) proves what the toy computes.

**Theorem.** Line L1 returns exactly the cells of the violating pairs. Line L8 returns the exact marginal of each noisy cell in the relaxed model, and line L9 its most likely value. Line L6 moves along the gradient of a strictly concave regularized log-likelihood. The sampler of lines L11 to L16 keeps the joint model as its stationary distribution, and with finite weights its frequencies converge with probability 1 to the marginals of that model.

The theorem says nothing about how fast the sampler converges. With large weights it may need far more sweeps than any run can afford, as the Pitfalls show.

## Complexity

The bounds are theorems about the toy, proved in the proof file, in data complexity for a fixed constraint set, with the attributes and the constraints kept as variables.

- **Time.** Detection compares all pairs of rows, $O(n^2 q p)$. Building the features costs $O(n a v (a + q n p))$, since each relaxed count scans the table. Each of the $e$ epochs of learning costs $O(n a v (a + q))$. The total is $O(n^2 a v q p + e\, n a v (a + q))$.
- **Space.** $O(n a (a + v (a + q)))$ for the counts, the domains and the features.
- **Gibbs.** One sweep costs $O(|N| v F p)$ for $|N|$ noisy cells and at most $F$ pair factors per row.

The paper uses hashing and blocking for detection, and DeepDive for learning and inference.

## Properties

- **Heuristic.** The repairs are the most likely values of a learned model, not provably true values.
- **Probabilistic output.** Each repair comes with a marginal probability, which can be used to send uncertain cells to a person.
- **Soft constraints.** A denial constraint is a signal with a learned weight, so the output may still violate it.
- **Weakly supervised.** The labels are the observed values of the clean cells, so no hand-labeled data is needed.
- **Deterministic pipeline.** Lines L1 to L10 make no random choices. Only the sampler is randomized.

## Variants and improvements

- **External data.** The paper adds dictionaries and matching dependencies as further signals, which give a value a feature when it matches a trusted source.
- **Joint inference.** Keeping the pair factors gives the joint model of lines L11 to L16. It is more faithful, but it has a factor for each pair of rows that share a noisy cell, which is why the paper relaxes it.
- **Constraint discovery.** The denial constraints can be [discovered](/functional-dependency-discovery/) from the data, in the style of the work of Chu, Ilyas and Papotti.

## When to use it

Use it when a table has many errors that break known rules, the clean part of the table is large enough to learn from, and a probability per repair is useful. Do not use it when you need a repair with a guarantee, such as the smallest change that satisfies the constraints, or when the queries can be answered without changing the data, by [consistent query answering](/consistent-query-answering/).

## Pitfalls

- **Pruning away the true value.** If $\tau$ in line L3 is too high, the true value never enters the domain. On the table (z1, Chicago, IL) twice, (z1, Chicgo, IL) and (z2, Boston, MA), Pr[Chicago given z1] is 2/3, so $\tau = 0.7$ leaves Chicgo as the only candidate of its cell, and nothing can fix it.
- **No training signal.** If no clean cell has more than one candidate, line L6 learns zero weights and line L8 is decided by the prior alone. On the same table with $\tau = 0.5$, the typo stays, with probability 0.731.
- **Relaxation errors.** Line L5 scores each cell with the other cells at their observed values. Two errors in one row can push each other into wrong repairs, as the zip cell of the example shows.
- **Near-hard factors trap the sampler.** In line L14, a factor weight of 20 makes a move out of a consistent state almost impossible. In the test, two cells that must agree and have no preference have the exact marginal 0.5, but the sampler returns 0 or 1. With weight 1 it returns about 0.5.
- **Clean cells are not all clean.** Line L6 trusts every cell outside a violation. Errors that break no constraint are learned as correct values.

## Implementations

## History

Chu, Ilyas and Papotti introduced holistic data cleaning with denial constraints at ICDE 2013 and studied the discovery of denial constraints in PVLDB the same year. Rekatsinas, Chu, Ilyas and Ré presented HoloClean in PVLDB in 2017. They compiled the signals into DDlog, the language of DeepDive, and ran learning and Gibbs sampling there. On four real data sets, the authors measured an average precision of about 90% and an average recall above 76%, better than the earlier methods they compared with (a measurement).

## References
