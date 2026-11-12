---
tag: Q8MXAA
kind: algorithm
slug: chou-fasman-method
name: Chou-Fasman method
aliases:
- Chou-Fasman prediction
area: biology/structure-prediction
level: intro
summary: Predicts helices and strands from a table of per-residue propensities. It finds dense nuclei of high-propensity residues and grows them until a window of four residues breaks them.
solves: [protein-secondary-structure-prediction]
model: word-ram
complexity:
  vars: {n: the length of the protein sequence}
  time: {worst: Θ(n^2), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1974
  people: [Peter Y. Chou, Gerald D. Fasman]
  note: Chou and Fasman computed helix, strand and coil parameters for each amino acid from 15 proteins and then 29 proteins, and gave nucleation rules for prediction, in two papers in Biochemistry in 1974.
prereqs: [protein-secondary-structure-prediction]
see_also: [gor-method, psipred, protein-secondary-structure, ramachandran-plot, sliding-window]
sources:
  - paper: doi:10.1021/bi00699a001
    title: Peter Y. Chou and Gerald D. Fasman, Conformational parameters for amino acids in helical, beta-sheet, and random coil regions calculated from proteins, Biochemistry 13(2), 1974, pages 211 to 222
    locator: the definition of the conformational parameters as frequency ratios, and their values from 15 proteins
  - paper: doi:10.1021/bi00699a002
    title: Peter Y. Chou and Gerald D. Fasman, Prediction of protein conformation, Biochemistry 13(2), 1974, pages 222 to 245
    locator: the parameters from 29 proteins, the former and breaker classes, and the rules for helix and strand nucleation, extension and overlap
  - paper: "Peter Y. Chou and Gerald D. Fasman, Prediction of the secondary structure of proteins from their amino acid sequence, Advances in Enzymology and Related Areas of Molecular Biology 47, 1978, pages 45 to 148"
    title: Chou and Fasman 1978, review of the method
    locator: the full rules, including the prediction of beta turns from bend frequencies
---

The Chou-Fasman method predicts the helices and beta strands of a protein from its sequence alone, with one table of numbers: for each amino acid, its propensity to be in a helix and in a strand. It looks for short windows that are dense in residues of high propensity, called nuclei, grows each nucleus in both directions until four residues of low propensity stop it, and keeps the segments whose mean propensity is high enough. It is a set of rules, not an optimizer, so it has no accuracy guarantee and its measured accuracy is far below modern methods. It is the first widely used method for [protein secondary structure prediction](/protein-secondary-structure-prediction/), and its propensity table is still the standard first view of which amino acids favour which state.

## In plain words

Some amino acids are found in helices more often than you would expect by chance, and some less often. The same holds for strands. Count this once, over proteins of known shape, and give each amino acid two scores: how much it likes helices and how much it likes strands. A score above one means it likes that shape.

To predict, slide a short window along the protein. If most of the amino acids in a window like helices, a helix may start there. Then grow the helix to the left and to the right, one amino acid at a time. Stop when the next four amino acids, on average, do not like helices. Keep the helix if, on the whole, it likes helices more than strands. Do the same for strands. Where a helix and a strand overlap, the shape with the higher total score wins.

## The problem

The input is a protein sequence $x = x_0 x_1 \cdots x_{n-1}$ over the 20 amino acids, and a table that gives each amino acid $a$ two integers $P_\alpha(a)$ and $P_\beta(a)$. The output is one label from $\{H, E, C\}$ for each residue. The model is the [word RAM](/word-ram/) with integer arithmetic. The method uses no relatives of the sequence and no 3D information.

The propensity of $a$ for state $S$ is a ratio of frequencies in a set of proteins of known structure:

$$P_S(a) = \frac{f_S(a)}{\bar{f}_S}, \qquad f_S(a) = \frac{\text{number of residues } a \text{ in state } S}{\text{number of residues } a}, \qquad \bar{f}_S = \frac{\text{number of residues in state } S}{\text{number of residues}}.$$

So $P_S(a) > 1$ means that $a$ is found in state $S$ more often than an average residue. This page stores the values times 100 as integers, so that each test on a mean is an exact test on a sum. The table below lists the values used in the example; they are the ones reprinted in later teaching material from the 29-protein table of Chou and Fasman.

| residue | E (Glu) | A (Ala) | V (Val) | Y (Tyr) | T (Thr) | N (Asn) | S (Ser) |
|---|---|---|---|---|---|---|---|
| $P_\alpha$ | 151 | 142 | 106 | 69 | 83 | 67 | 77 |
| $P_\beta$ | 37 | 83 | 170 | 147 | 119 | 89 | 75 |

## The algorithm

The rules below are the numeric form found in textbooks and teaching material. A helix nucleus is a window of 6 residues with at least 4 of $P_\alpha > 103$; a strand nucleus is a window of 5 residues with at least 3 of $P_\beta > 100$. A segment grows while the four residues at its new end have a sum of at least 400 (mean at least 1.00). A helix is accepted when its mean $P_\alpha$ is above 103 and its sum of $P_\alpha$ is larger than its sum of $P_\beta$; a strand when its mean $P_\beta$ is above 105 and its sum of $P_\beta$ is larger than its sum of $P_\alpha$. The ranges $[s, e)$ are half-open.

```pseudo id=main
SEGMENTS(P, Q, w, k, f, a)                 ▷ P: own state, Q: other state
L1  out ← empty list
L2  for each s0 in 0 .. n − w with |{ r ∈ [s0, s0 + w) : P[r] > f }| ≥ k do
L3      (s, e) ← EXTEND(P, s0, s0 + w)
L4      if Σ P[s .. e − 1] > a · (e − s) and Σ P[s .. e − 1] > Σ Q[s .. e − 1] then append (s, e) to out
L5  return out

EXTEND(P, s, e)
L6  while s > 0 and P[s − 1] + P[s] + P[s + 1] + P[s + 2] ≥ 400 do s ← s − 1
L7  while e < n and P[e − 3] + P[e − 2] + P[e − 1] + P[e] ≥ 400 do e ← e + 1
L8  return (s, e)

CHOU-FASMAN(x)
L9  Pα[r] ← table value of x[r] for helix, Pβ[r] ← table value for strand, for each r
L10 h[0 .. n − 1] ← false, b[0 .. n − 1] ← false
L11 for each (s, e) in SEGMENTS(Pα, Pβ, 6, 4, 103, 103) do h[s .. e − 1] ← true
L12 for each (s, e) in SEGMENTS(Pβ, Pα, 5, 3, 100, 105) do b[s .. e − 1] ← true
L13 y[r] ← H if h[r] and not b[r], E if b[r] and not h[r], C if neither, for each r
L14 r ← 0
L15 while r < n do
L16     if h[r] and b[r] then
L17         t ← r; while t < n and h[t] and b[t] do t ← t + 1
L18         y[r .. t − 1] ← H if Σ Pα[r .. t − 1] > Σ Pβ[r .. t − 1] else E; r ← t
L19     else r ← r + 1
L20 return y
```

Line L2 finds the nuclei. Line L3 grows each one; nuclei that are close together usually grow into overlapping segments, which is harmless because the flags of lines L11 and L12 take the union. Line L4 keeps a segment only if, as a whole, it favours its own state, so a nucleus inside a region that favours the other state is dropped. Lines L14 to L19 settle each run of residues that are in both a helix and a strand by comparing the two sums over the run.

## Example

Predict the 12 residues `ENSESAVNEYVT`, indexed 0 to 11. The rows of propensities are

```
index   0   1   2   3   4   5   6   7   8   9  10  11
res     E   N   S   E   S   A   V   N   E   Y   V   T
Pα    151  67  77 151  77 142 106  67 151  69 106  83
Pβ     37  89  75  37  75  83 170  89  37 147 170 119
```

**Helix.** The windows of 6 that start at 3 (E S A V N E) and at 5 (A V N E Y V) each have 4 residues with $P_\alpha > 103$; every other window has 3. So the helix nuclei start at 3 and 5.

- The nucleus $[3, 9)$ grows to the left because S E S A at 2 to 5 sum to 447. It stops there, because N S E S at 1 to 4 sum to 372. To the right, V N E Y at 6 to 9 sum to 393, so it does not grow. The segment is $[2, 9)$, with $\sum P_\alpha = 771 > 103 \cdot 7 = 721$ and $\sum P_\beta = 566$. It is accepted.
- The nucleus $[5, 11)$ does not grow to the left, because S A V N at 4 to 7 sum to 392. To the right, E Y V T at 8 to 11 sum to 409, so it grows to $[5, 12)$, the end of the sequence. Its $\sum P_\alpha = 724 > 721$, but $\sum P_\beta = 815$ is larger. It is rejected.

**Strand.** The windows of 5 that start at 6 (V N E Y V) and at 7 (N E Y V T) each have 3 residues with $P_\beta > 100$. The nucleus $[6, 11)$ does not grow to the left (A V N E sum to 379) and grows to the right (E Y V T sum to 473) to $[6, 12)$. The nucleus $[7, 12)$ grows to the left once (V N E Y sum to 443) and then stops at the same place. Both give $[6, 12)$, with $\sum P_\beta = 732 > 105 \cdot 6 = 630$ and $\sum P_\alpha = 582$. It is accepted.

**Overlap.** Residues 6, 7 and 8 (V N E) are in both the helix $[2, 9)$ and the strand $[6, 12)$. Over this run $\sum P_\alpha = 324$ and $\sum P_\beta = 296$, so the run goes to H. The result is

```
ENSESAVNEYVT
CCHHHHHHHEEE
```

## Correctness

The method has no notion of a correct answer beyond its own rules, so correctness here means that the procedure computes the labels that the rules define: each nucleus grows to the maximal segment allowed by the four-residue test, accepted segments are exactly those that pass the two sum tests, and each run of overlap gets the label of its sums. The proof uses a loop invariant for each loop of EXTEND and a scan argument for the overlap step. Integer propensities make every decision exact. The full proof is below.

## Complexity

Let $n$ be the length of the sequence, with the window widths fixed. Finding the nuclei costs $O(n)$. There are at most $n$ nuclei, and one call of EXTEND can take up to $n$ steps, so the worst case is $\Theta(n^2)$ time. A run of $n$ alanines reaches it: every window is a nucleus and every nucleus grows to the whole sequence. If no window is a nucleus, the time is $\Theta(n)$. The extra space is $\Theta(n)$ for the two rows of values, the flags and the labels.

The quadratic term is a property of this direct procedure, not of the rules. Precompute, for each position, the nearest window of four with a sum below 400 to its left and to its right, and the prefix sums of $P_\alpha$ and $P_\beta$. Then each segment and its two sums take $O(1)$ time, and the whole method runs in $\Theta(n)$ time.

## Properties

- **Deterministic and local.** The label of a residue depends only on residues within the reach of the windows and the growth, and the same input always gives the same output.
- **Single sequence.** It uses no homologs. This is why it can run on any sequence, and also why its accuracy is low.
- **Exact integer decisions.** With the table stored times 100, no test depends on floating point rounding.
- **No turn states here.** This version labels every residue that is not in a helix or a strand as C.
- **Not an optimizer.** It does not maximize any score. Two rule sets that differ in a threshold can give different segment ends, and there is no objective to decide between them.

## Variants and improvements

- **The original former and breaker classes.** The 1974 paper sorts the amino acids for each state into strong formers, formers, weak formers, indifferent residues, breakers and strong breakers, and states the nucleation and breaking rules with these classes. The numeric thresholds on this page are a later simplification, and published versions differ in the exact thresholds.
- **Beta turns.** The full method also predicts four-residue beta turns. It uses the frequency of each amino acid at each of the four positions of a bend and a turn propensity $P_t$, and it predicts a turn where their product is high and $P_t$ is larger than $P_\alpha$ and $P_\beta$.
- **Linear time.** The precomputation in the complexity section removes the quadratic worst case.
- **Larger tables.** Later work recomputed the propensities from much larger sets of structures with DSSP labels. The rules stay the same with a new table.
- **Window information instead of single residues.** The [GOR method](/gor-method/) replaces the single residue propensity by information values for each neighbour in a window of 17, which uses the context that this method ignores.

## When to use it

Use the method to teach secondary structure prediction, to read the propensity table (glutamate, alanine, leucine and methionine favour helices; valine, isoleucine and tyrosine favour strands; glycine and proline break both), or as a baseline. Do not use it for real predictions: profile based methods such as [PSIPRED](/psipred/) are far more accurate.

## Pitfalls

- **Which table.** Several tables with the name Chou-Fasman are in use, from the 1974 papers, the 1978 review and later reprints, and they differ in some values (lysine has a helix value of 1.14 in some reprints and 1.16 in others). State the table with the predictions.
- **Rounding means.** Testing a mean in floating point can flip a decision at the threshold. Compare integer sums with the threshold times the length.
- **Order of overlap resolution.** Resolve overlaps after all segments are known. Resolving each new segment against the old ones in turn makes the result depend on the order of the nuclei.
- **Off by one at the ends.** The four residues that stop growth to the right end at the new residue, not start at it. Mixing the two moves every segment end by up to three residues.
- **Reading accuracy numbers.** Accuracies reported for small sets of proteins in the 1970s are higher than those of later tests on large sets that exclude the training proteins.

## Implementations

## History

Chou and Fasman published the method in two papers in Biochemistry in 1974. The first defined the conformational parameters and computed them from 15 proteins of known structure. The second recomputed them from 29 proteins and gave the prediction rules, with nucleation, extension and the treatment of overlaps. A long review in 1978 restated the rules and added the prediction of beta turns. The simplicity of the method made it the standard tool of the 1970s and 1980s, until methods with window information and then evolutionary profiles replaced it.

## References
