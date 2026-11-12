---
tag: Y916HH
kind: algorithm
slug: mccaskill-algorithm
name: McCaskill algorithm
aliases:
- McCaskill partition function
- Base-pair probability algorithm
- RNA partition function algorithm
area: biology/structure-prediction
level: advanced
summary: Dynamic program that computes the partition function over all RNA secondary structures and the probability of each base pair in O(n^3) time and O(n^2) space.
solves: [rna-secondary-structure-prediction]
model: word-ram
complexity:
  vars: {n: the length of the RNA sequence, L: the largest allowed size of a bulge or interior loop}
  time: {worst: Θ(n^3 + n^2 L^2), average: Θ(n^3 + n^2 L^2), best: Θ(n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1990
  people: [John S. McCaskill, Ye Ding, Charles E. Lawrence]
  note: McCaskill gave the partition function and the base pair probabilities in 1990. Ding and Lawrence added sampling of structures by stochastic traceback in 2003.
prereqs: [zuker-algorithm, partition-function]
see_also: [inside-outside-algorithm, ancestral-sampling, nussinov-algorithm, rna-secondary-structure-prediction, rna-folding-kinetics, rna-inverse-folding, rna-pseudoknot-prediction, sankoff-rna-algorithm]
sources:
  - paper: doi:10.1002/bip.360290621
    title: John S. McCaskill, The equilibrium partition function and base pair binding probabilities for RNA secondary structure, Biopolymers 29(6-7), 1990, pages 1105 to 1119
    locator: the recursions for the partition function and for the base pair probabilities
  - paper: doi:10.1093/nar/gkg938
    title: Ye Ding and Charles E. Lawrence, A statistical sampling algorithm for RNA secondary structure prediction, Nucleic Acids Research 31(24), 2003, pages 7280 to 7301
    locator: the stochastic traceback that samples structures from the Boltzmann distribution
  - paper: doi:10.1186/1748-7188-6-26
    title: Ronny Lorenz, Stephan H. Bernhart, Christian Höner zu Siederdissen, Hakim Tafer, Christoph Flamm, Peter F. Stadler and Ivo L. Hofacker, ViennaRNA Package 2.0, Algorithms for Molecular Biology 6, 2011, article 26
    locator: RNAfold -p, the partition function and the pair probabilities with the Turner 2004 parameters
  - paper: doi:10.1093/bioinformatics/btl246
    title: Chuong B. Do, Daniel A. Woods and Serafim Batzoglou, CONTRAfold, RNA secondary structure prediction without physics-based models, Bioinformatics 22(14), 2006
    locator: maximum expected accuracy structures from pair probabilities
---

The McCaskill algorithm computes the [partition function](/partition-function/) $Z = \sum_P e^{-E(P)/RT}$ over all [RNA secondary structures](/rna-secondary-structure/) $P$ of a sequence, and the probability of each base pair in the Boltzmann distribution. It uses the recurrences of the [Zuker algorithm](/zuker-algorithm/) with min replaced by sum and energies replaced by Boltzmann weights, and then an outside pass that gives the pair probabilities. Both passes take $\Theta(n^3 + n^2 L^2)$ time and $\Theta(n^2)$ space. The same tables let you draw structures from the Boltzmann distribution, by the stochastic traceback of Ding and Lawrence.

## In plain words

An RNA string can fold in a huge number of ways. At a fixed temperature, each fold occurs with a probability that falls quickly as its energy rises. A single best fold hides how sure the prediction is. A better answer gives, for each pair of letters, the chance that they pair.

The method uses the tables of the minimum energy method, but each cell adds up the weights of all folds of its part instead of keeping only the best. The total of all weights is the normalizing number. A second pass from the outside in gives, for each pair, the total weight of the folds that contain it. Divide it by the total, and you get the chance of that pair. The same tables let you draw random folds with the right chances.

## The problem

**Input.** A sequence $s = s_1 \cdots s_n$ over $\{A, C, G, U\}$, an energy model, and the temperature as $RT$. On this page the allowed pairs are AU, GC and GU, the hairpin minimum is $m = 3$, and pseudoknots are not allowed.

**Output.** The partition function $Z = \sum_P z^{E(P)}$ over all allowed secondary structures, with $z = e^{-1/RT}$ for energies in units of $RT$, and the probabilities

$$p(i, j) = \frac{1}{Z} \sum_{P \ni (i, j)} z^{E(P)} \quad \text{for all } i < j.$$

The code uses the same toy integer loop model as the [Zuker algorithm](/zuker-algorithm/) page (hairpin $3 + u$, stacks $-(w + w')$ with $w = 3, 2, 1$ for GC, AU and GU, bulge $2 + u$, interior loop $1 + u_1 + u_2 + |u_1 - u_2|$ with $u_1 + u_2 \le L$, multiloop $a + b k + c u$), and $z$ is a rational number, so that the tests can check the results exactly. Real programs use the Turner 2004 parameters of the [nearest-neighbor model](/nearest-neighbor-model/) in kcal/mol at 37 °C.

## The algorithm

The inside tables are the sums over the sets of the Zuker tables: $Q^b(i, j)$ sums over the structures of $[i, j]$ that contain the pair $(i, j)$, $Q^{M1}(i, j)$ over one multiloop branch that starts at $i$, $Q^M(i, j)$ over multiloop parts with at least one branch, and $Q(j)$ over the structures of the prefix $s_1 \cdots s_j$. Each structure has exactly one derivation in these recurrences, so no structure is counted twice.

The outside pass computes, for each inside value $X$, the derivative $\hat X = \partial Z / \partial X$, by reverse-mode propagation through the formulas of the inside pass. A structure that contains the pair $(i, j)$ uses $Q^b(i, j)$ exactly once in its derivation, so $Q^b(i, j) \hat Q^b(i, j)$ is the total weight of these structures.

```pseudo id=main
MCCASKILL(s[1 .. n], z)                    ▷ Q^b, Q^M1, Q^M start at 0
L1  for d ← m + 1 to n − 1 do                   ▷ the span j − i
L2      for i ← 1 to n − d do j ← i + d
L3          if (s_i, s_j) is allowed then Q^b[i, j] ← z^{H(i, j)}       ▷ hairpin
L4              for each inner pair (k, l) with (k − i − 1) + (j − l − 1) ≤ L do Q^b[i, j] += z^{IL(i, j, k, l)} · Q^b[k, l]
L5              for u ← i + 2 to j − 1 do Q^b[i, j] += z^{a + b} · Q^M[i + 1, u − 1] · Q^M1[u, j − 1]
L6          Q^M1[i, j] ← z^b · Q^b[i, j] + z^c · Q^M1[i, j − 1]
L7          Q^M[i, j] ← sum over u in [i, j] of (z^{c (u − i)} + Q^M[i, u − 1]) · Q^M1[u, j]
L8  Q[0] ← 1; for j ← 1 to n do Q[j] ← Q[j − 1] + sum over k ≤ j − m − 1 of Q[k − 1] · Q^b[k, j]; Z ← Q[n]
L9  set every outside value to 0, then Q̂[n] ← 1
L10 for j ← n down to 1 do Q̂[j − 1] += Q̂[j]; for each k do Q̂[k − 1] += Q̂[j] · Q^b[k, j] and Q̂^b[k, j] += Q̂[j] · Q[k − 1]
L11 for d ← n − 1 down to m + 1 do for i ← 1 to n − d do j ← i + d
L12     for each u in [i, j] do Q̂^M1[u, j] += Q̂^M[i, j] · (z^{c (u − i)} + Q^M[i, u − 1]) and Q̂^M[i, u − 1] += Q̂^M[i, j] · Q^M1[u, j]
L13     Q̂^b[i, j] += z^b · Q̂^M1[i, j]; Q̂^M1[i, j − 1] += z^c · Q̂^M1[i, j]
L14     for each inner pair (k, l) do Q̂^b[k, l] += Q̂^b[i, j] · z^{IL(i, j, k, l)}; for each u do Q̂^M[i + 1, u − 1] += Q̂^b[i, j] · z^{a + b} · Q^M1[u, j − 1] and Q̂^M1[u, j − 1] += Q̂^b[i, j] · z^{a + b} · Q^M[i + 1, u − 1]
L15 for each i < j do p[i, j] ← Q^b[i, j] · Q̂^b[i, j] / Z
L16 return Z, p
```

Lines L1 to L8 are the inside pass. Lines L9 to L14 undo the inside formulas in the reverse order: line L12 undoes line L7, line L13 undoes line L6, and line L14 undoes lines L3 to L5. Within one interval, the order $Q^M$, $Q^{M1}$, $Q^b$ is the reverse of the inside order, so each outside value is complete before it is passed on.

**Sampling.** To draw a structure with probability $z^{E(P)} / Z$, start at $Q(n)$ and choose one term of its sum with probability proportional to the term. Then do the same in each cell that the chosen term uses. This is the stochastic traceback of Ding and Lawrence (2003). It is [ancestral sampling](/ancestral-sampling/) in the derivation tree of the recurrences.

## Example

Take $s = $ GGGAAACCC ($n = 9$) in the model of the code, with $z = 1/2$, so a structure of energy $E$ has weight $2^{-E}$. The sequence has 20 secondary structures, including the empty one. The inside values of the pairs of the helix are:

| cell | terms | value |
|---|---|---|
| $Q^b(3, 7)$ | hairpin with $u = 3$: $z^{6}$ | $1/64$ |
| $Q^b(2, 8)$ | hairpin $z^{8}$; stack on $(3, 7)$: $z^{-6} \cdot 1/64$ | $257/256$ |
| $Q^b(1, 9)$ | hairpin $z^{10}$; stack on $(2, 8)$: $z^{-6} \cdot 257/256$; two bulges $z^{3} \cdot z^{7}$; interior loop $z^{3} \cdot z^{6}$ | $65797/1024$ |

The exterior pass gives $Z = Q(9) = 68921/1024 \approx 67.3$. The minimum energy structure (((...))) has energy $-6$ and weight $64$, so its probability is $65536/68921 \approx 0.951$. The pair probabilities are $p(1, 9) = 65797/68921 \approx 0.955$, $p(2, 8) = 66820/68921 \approx 0.970$ and $p(3, 7) = 66582/68921 \approx 0.966$. The inner pairs are more likely than the outer pair, because some structures contain $(2, 8)$ or $(3, 7)$ but not $(1, 9)$. Each other pair has a probability below $0.008$.

## Correctness

The inside recurrences are those of the Zuker algorithm, with min replaced by sum and $+$ by $\times$. The decomposition lemma of the Zuker algorithm shows that each structure of a set falls into exactly one case, with unique parts. So by induction on the span, each inside cell is the sum of the weights $z^{E}$ of its set, and $Q(n) = Z$. The outside pass is reverse-mode differentiation of the polynomial $Z$ in the inside values. In each derivation the cell $Q^b(i, j)$ appears at most once, and it appears exactly when $(i, j)$ is a pair, so $Q^b(i, j) \cdot \partial Z / \partial Q^b(i, j)$ is the weight of the structures with that pair. The full proof is below.

## Complexity

- **Time.** The inside pass has the loops of the Zuker algorithm, so it takes $\Theta(n^3 + n^2 L^2)$ time in the worst case, and $\Theta(n^4)$ without a bound on interior loops. The outside pass visits the same terms once more, and line L15 takes $O(n^2)$. After the inside pass, each sample takes $O(n^2 + n L^2)$ time in the worst case: the traceback visits $O(n)$ cells, and each cell has $O(n + L^2)$ terms.
- **Space.** $\Theta(n^2)$ for the inside and outside tables and for the pair probabilities.
- **Arithmetic.** The bounds count arithmetic operations. With floating point numbers each operation is $O(1)$ on the [word RAM](/word-ram/), but $Z$ grows exponentially with $n$, so real programs scale the weights or work with logarithms. With exact rationals, as in the tests, the numbers grow and each operation costs more.

## Properties

- **Exact.** In exact arithmetic, the algorithm returns the exact $Z$ and the exact pair probabilities of the model.
- **More than one structure.** The pair probabilities show which parts of a prediction are well defined and which are not. A region with many pairs of medium probability has several competing structures.
- **Same structure as inside-outside.** The inside and outside passes match the [inside-outside algorithm](/inside-outside-algorithm/) for a [probabilistic context-free grammar](/probabilistic-context-free-grammar/). The energy model is a grammar whose rule weights are Boltzmann factors.
- **The minimum energy as a limit.** As $RT \to 0$, the Boltzmann distribution puts all its weight on the minimum energy structures, and the sums become the minima of the Zuker algorithm.

## Variants and improvements

- **Maximum expected accuracy.** Choose the structure that maximizes the sum of the pair probabilities of its pairs and of the unpaired probabilities of its other bases, by a Nussinov-like dynamic program over the probability matrix. CONTRAfold (Do, Woods and Batzoglou, 2006) uses this with learned parameters.
- **Centroid structures.** Take the pairs with probability above $1/2$. These pairs never cross and never share a base, so they form a secondary structure.
- **Sampling.** The stochastic traceback of Ding and Lawrence draws structures. Clusters of the samples show the main competing folds.
- **Constraints and accessibility.** Fix some bases as unpaired or paired and compute the partition function again; the ratio of the two partition functions is the probability of the constraint. This gives the accessibility of a site to a binding partner.
- **Pseudoknots.** Dirks and Pierce (2003) gave an $O(n^5)$ partition function algorithm for a class of pseudoknots; see [RNA pseudoknot prediction](/rna-pseudoknot-prediction/).
- **Several sequences.** The [Sankoff algorithm](/sankoff-rna-algorithm/) and [simultaneous alignment and folding](/simultaneous-alignment-and-folding/) extend the partition function to aligned sequences.

## When to use it

Use the McCaskill algorithm when you need more than one structure: to say how sure a prediction is, to find the probability that a site is unpaired, to draw structures, or as the input to a maximum expected accuracy structure. It costs about as much as the Zuker algorithm. Use a tested package with the Turner parameters and scaled arithmetic for real sequences.

## Pitfalls

- **Ambiguous recurrences.** A recurrence that builds a structure in more than one way is harmless for the minimum but counts the structure many times in $Z$. All four tables must be unambiguous.
- **Overflow and underflow.** For long sequences $Z$ does not fit in a floating point number. Use a scale factor per base or log-space arithmetic.
- **The wrong order in the outside pass.** An outside value must collect all its contributions before it is passed on. Process the spans from long to short, and within one interval do $Q^M$, then $Q^{M1}$, then $Q^b$.
- **Units of temperature.** The weight is $e^{-E/RT}$, with $R = 1.987 \times 10^{-3}$ kcal/(mol K) and $T$ in kelvin. Using $kT$ per molecule with energies per mole gives wrong probabilities.
- **The Boltzmann sum is not a structure.** The most probable pairs from different structures can share no base yet give an unlikely combination. Use a decoding rule, such as the centroid or MEA, to get one structure.

## Implementations

## History

John McCaskill published the partition function and the base pair binding probabilities for RNA secondary structure in 1990. It replaced the minimum of the Zuker and Stiegler recursions by a sum, and added the outside recursions for the pair probabilities. The Vienna RNA package of Hofacker and others implemented it as RNAfold -p. Ye Ding and Charles Lawrence (2003) used the same tables for statistical sampling of structures, which became Sfold. Dirks and Pierce (2003) extended the partition function to a class of pseudoknots.

## References
