---
tag: KTTQKV
kind: algorithm
slug: gor-method
name: GOR method
aliases:
- Garnier-Osguthorpe-Robson method
- GOR secondary structure prediction
area: biology/structure-prediction
level: intro
summary: Predicts the secondary structure state of each residue by summing, over a window of 17 residues, the information each neighbour carries about the central state.
solves: [protein-secondary-structure-prediction]
model: word-ram
complexity:
  vars: {n: the length of the sequence, h: the half width of the window, k: the number of states, a: the size of the alphabet}
  time: {worst: Θ(n h k), average: Θ(n h k), best: Θ(n h k)}
  space: {extra: Θ(n k + h k a)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1978
  people: [Jean Garnier, David J. Osguthorpe, Barry Robson]
  note: Garnier, Osguthorpe and Robson used information theory to weigh each residue in a window of 17 around the predicted position, in the Journal of Molecular Biology in 1978.
prereqs: [protein-secondary-structure-prediction]
see_also: [chou-fasman-method, psipred, naive-bayes-classifier, shannon-entropy, sliding-window, hidden-markov-model]
sources:
  - paper: doi:10.1016/0022-2836(78)90297-8
    title: Jean Garnier, David J. Osguthorpe and Barry Robson, Analysis of the accuracy and implications of simple methods for predicting the secondary structure of globular proteins, Journal of Molecular Biology 120(1), 1978, pages 97 to 120
    locator: the information values for each residue at offsets from minus 8 to plus 8, their sum over the window, the four states and the decision constants
  - paper: "Jean-François Gibrat, Jean Garnier and Barry Robson, Further developments of protein secondary structure prediction using information theory, new parameters and consideration of residue pairs, Journal of Molecular Biology 198(3), 1987, pages 425 to 443"
    title: Gibrat, Garnier and Robson 1987 (GOR III)
    locator: the extension from single residues to pairs of residues in the window
  - paper: "Jean Garnier, Jean-François Gibrat and Barry Robson, GOR method for predicting protein secondary structure from amino acid sequence, Methods in Enzymology 266, 1996, pages 540 to 553"
    title: Garnier, Gibrat and Robson 1996 (GOR IV)
    locator: the later form of the method with three states and pair information
---

The GOR method predicts the [secondary structure](/protein-secondary-structure/) state of each residue of a protein from its sequence alone. For each state $S$, each offset $m$ from $-8$ to $8$ and each amino acid $a$, a table holds the information $I(S; a, m)$ that "the residue at offset $m$ is $a$" carries about "the central residue is in state $S$"; the score of $S$ at a position is the sum of the 17 table values of its window, and the state with the highest score wins. Unlike the [Chou-Fasman method](/chou-fasman-method/), it uses the neighbours of each residue, not the residue alone, and it is a probabilistic model rather than a set of rules. Under the assumption that the residues of a window are independent given the central state, and with the log prior of each state added to its score, it is a [naive Bayes classifier](/naive-bayes-classifier/) over the window.

## In plain words

Look at one amino acid in a protein and ask whether it is in a helix. The amino acid itself gives a hint. Its neighbours give hints too: an amino acid four places away that likes helices makes a helix here more likely, and one that breaks helices makes it less likely.

The method turns each hint into a number. It learns the numbers by counting, over proteins of known shape, how often each amino acid at each distance goes with each shape at the centre. A positive number means "this makes the shape more likely", and a negative one means "less likely". To predict, it adds up the numbers of all the neighbours within eight places on each side, once for each shape, and picks the shape with the largest total. Each position is decided on its own.

## The problem

The input is a sequence $x = x_0 \cdots x_{n-1}$ over an alphabet of $a$ amino acids (20 for proteins) and a set of $k$ states. The original paper uses four states: helix, extended (strand), turn and coil; later versions use three. Training data are sequences with known states, from the DSSP assignment or an earlier rule. The output is a state for each residue. The model is the [word RAM](/word-ram/) with real arithmetic; the tests use exact integer tables where the decision must be exact.

The information is the log ratio of a conditional probability to a prior,

$$I(S; a, m) = \ln \frac{P(S \text{ at } j \mid a \text{ at } j + m)}{P(S)},$$

in nats on this page. It is positive when residue $a$ at offset $m$ makes $S$ more likely than average. The score of state $S$ at position $j$ is

$$\mathrm{score}(j, S) = d(S) + \sum_{m = -h,\; 0 \le j + m < n}^{h} I(S; x_{j+m}, m),$$

with half width $h = 8$ in the original method and a decision constant $d(S)$, which is 0 unless it is set. The original paper set the constants to shift the predicted fraction of each state toward an estimate of the content, for example from circular dichroism. Near the ends of the sequence, the window loses the offsets that fall outside it. The paper also writes the information as a difference between $S$ and "not $S$"; this page uses the single state form above.

## The algorithm

Training estimates the probabilities from counts with a pseudocount $c$, and prediction scatters the information of each residue to the centres that see it.

```pseudo id=main
GOR-TRAIN(D, h, c)                         ▷ D: sequences with states, c: pseudocount
L1  N(S) ← 0, f(S, m, b) ← 0, f(m, b) ← 0 for all states S, offsets m, residues b
L2  for each (x, t) in D and each position j of x do
L3      N(t_j) ← N(t_j) + 1
L4      for m ← −h to h with 0 ≤ j + m < |x| do
L5          f(t_j, m, x_{j+m}) ← f(t_j, m, x_{j+m}) + 1; f(m, x_{j+m}) ← f(m, x_{j+m}) + 1
L6  for each state S, offset m and residue b do
L7      I(S; b, m) ← ln( ((f(S, m, b) + c) / (f(m, b) + c k)) / ((N(S) + c) / (N + c k)) )
L8  return I

GOR-PREDICT(x, I, h, d)                    ▷ d(S): decision constants
L9  score[j][S] ← d(S) for each position j and state S
L10 for i ← 0 to n − 1 do
L11     for m ← −h to h with 0 ≤ i − m < n do
L12         for each state S do score[i − m][S] ← score[i − m][S] + I(S; x_i, m)
L13 y_j ← the first state S with the largest score[j][S], for each j
L14 return y
```

In line L7, $N = \sum_S N(S)$ is the number of training residues, and $f(m, b)$ counts the positions whose residue at offset $m$ is $b$. Line L12 adds the information of residue $x_i$ to the centre $j = i - m$, for which $x_i$ sits at offset $m$. This scatter order gives the same sums as a gather over each window, with the same cost. A residue that never occurs in the training data gets information 0.

## Example

Train with $h = 1$, two states H and C, pseudocount $c = 1$, on two sequences:

```
x   A A L A G G      G G A L A A
t   H H H H C C      C C H H H H
```

There are $N = 12$ residues, 8 in H and 4 in C, so $P(H) = 9/14$ and $P(C) = 5/14$. At offset 0, the residue A occurs 6 times, always in H, so $P(H \mid A \text{ at } 0) = 7/8$ and $I(H; A, 0) = \ln \frac{7/8}{9/14} = \ln \frac{49}{36} = 0.308$. The residue G occurs 4 times at offset 0, always in C, so $P(C \mid G \text{ at } 0) = 5/6$ and $I(C; G, 0) = \ln \frac{5/6}{5/14} = \ln \frac{7}{3} = 0.847$. The full table, rounded to three places, is

| state | $(-1, A)$ | $(-1, G)$ | $(-1, L)$ | $(0, A)$ | $(0, G)$ | $(0, L)$ |
|---|---|---|---|---|---|---|
| H | 0.105 | -0.474 | 0.154 | 0.308 | -1.350 | 0.154 |
| C | -0.223 | 0.519 | -0.357 | -1.050 | 0.847 | -0.357 |

and offset $+1$ has the same values as offset $-1$ for these data. Predict `GALAG` with $d = 0$:

| $j$ | window | score H | score C | state |
|---|---|---|---|---|
| 0 | (G) A | $-1.350 + 0.105 = -1.245$ | $0.847 - 0.223 = 0.624$ | C |
| 1 | G (A) L | $-0.474 + 0.308 + 0.154 = -0.012$ | $0.519 - 1.050 - 0.357 = -0.888$ | H |
| 2 | A (L) A | $0.105 + 0.154 + 0.105 = 0.365$ | $-0.223 - 0.357 - 0.223 = -0.803$ | H |
| 3 | L (A) G | $-0.012$ | $-0.888$ | H |
| 4 | A (G) | $-1.245$ | $0.624$ | C |

The prediction is `CHHHC`. The values are rounded; the exact sum at $j = 2$ is $2 \ln \frac{10}{9} + \ln \frac{7}{6} = 0.3649$. With the decision constants $d(S) = \ln P(S)$, the scores become log posteriors up to a constant, $-0.077$ for H and $-1.833$ for C at $j = 2$, and the prediction stays `CHHHC`.

## Correctness

There are two claims. First, the scatter loop of lines L10 to L12 computes exactly the window sum: each pair of a residue $i$ and an offset $m$ with $0 \le i - m < n$ matches one pair of a centre $j = i - m$ and an offset $m$ in its window, so each window term is added once. Second, the window sum is a naive Bayes rule: if the residues of a window are independent given the central state, then $\ln P(S \mid \text{window}) = \ln P(S) + \sum_m I(S; x_{j+m}, m) + C_j$ with $C_j$ not depending on $S$, by Bayes' theorem on each factor. So with $d(S) = \ln P(S)$ the method picks a state of largest posterior under that assumption. The assumption is false for real proteins, and the method has no guarantee of accuracy; its quality is measured. The full proof is below.

## Complexity

Let $n$ be the length of the sequence, $h$ the half width, $k$ the number of states and $a$ the alphabet size. Prediction costs $\Theta(n h k)$ time, because each residue adds to at most $2h + 1$ centres and each addition touches $k$ states, and the time is the same in every case. The scores take $\Theta(n k)$ space and the table $\Theta(h k a)$. For the original method the table has $17 \cdot 20 \cdot 4 = 1360$ values. Training on $N$ residues costs $\Theta(N h)$ time for the counts and $\Theta(h k a)$ for the logarithms.

## Properties

- **Linear time, fixed size model.** For fixed $h$ and $k$ the method is linear in $n$, and the model is a small table.
- **Each position is decided alone.** Nothing forces the predicted states to form segments, so isolated one-residue helices can appear. Later methods add a smoothing step or a second model over the outputs.
- **Additive and interpretable.** Each table value says how much one residue at one offset pushes toward one state.
- **Single sequence.** The method uses no relatives of the sequence.
- **Independence assumption.** Neighbouring residues are not independent given the state. Pairs of residues carry information that single residues do not, which is what GOR III adds.

## Variants and improvements

- **Pair information (GOR III and GOR IV).** Add the information of each pair of residues, the one at offset $m$ and the central one, to the single residue terms. The number of parameters grows by a factor of the alphabet size, and much more training data is needed.
- **Multiple alignments (GOR V).** Average the predictions over the aligned homologs of the sequence. This uses evolutionary information, the change that made methods such as [PSIPRED](/psipred/) much more accurate.
- **Decision constants.** Tune $d(S)$ to balance the predicted fraction of each state.
- **A second stage.** Feed the per-position scores to a second model, such as a [hidden Markov model](/hidden-markov-model/) or a window filter, to make the states into segments.

## When to use it

Use GOR to teach information-based prediction, as a fast single sequence baseline, or when no homologs are known and a simple interpretable model is enough. For real predictions on proteins with homologs, profile based methods are much more accurate.

## Pitfalls

- **Zero counts.** Without a pseudocount, a residue that never occurs with a state at some offset gives $\ln 0$. Use a pseudocount, or a prior from the single residue frequencies.
- **Units.** Papers use natural logarithms or other bases. The prediction does not change with the base, but the decision constants must use the same base as the table.
- **Training and test overlap.** A table trained on the test proteins, or on close relatives of them, reports an accuracy that is too high.
- **Window at the ends.** Near the ends, the window has fewer than 17 terms. Treat the missing offsets as absent, not as a residue.
- **Offset sign.** $I(S; a, m)$ is for residue $a$ at $j + m$, so the scatter step adds to centre $i - m$. Swapping the sign mirrors the table and gives wrong scores for asymmetric data.

## Implementations

## History

Garnier, Osguthorpe and Robson published the method in 1978. They predicted four states, used a window from $-8$ to $+8$, and compared the method with other simple methods of the time. Gibrat, Garnier and Robson added pair information in 1987 (GOR III), and later versions (GOR IV in 1996 and GOR V with multiple alignments) kept the information sum as their core.

## References
