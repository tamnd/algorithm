---
tag: RQVJG1
kind: algorithm
slug: psipred
name: PSIPRED
aliases:
- PSI-PRED
area: biology/structure-prediction
level: advanced
summary: Two-stage neural network that predicts helix, strand or coil for each residue from a PSI-BLAST profile; Jones reported 76.5 percent Q3 in 1999.
solves: [protein-secondary-structure-prediction]
model: word-ram
complexity:
  vars: {n: the length of the sequence, w: the window width, f: the number of inputs per window position, u: the number of hidden units}
  time: {worst: Θ(n w f u), average: Θ(n w f u), best: Θ(n w f u)}
  space: {extra: Θ(n + u)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1999
  people: [David T. Jones]
  note: Jones fed position-specific scoring matrices from PSI-BLAST to a window network, with a second network over its outputs, in the Journal of Molecular Biology in 1999.
prereqs: [protein-secondary-structure-prediction, position-specific-scoring-matrix, backpropagation]
see_also: [gor-method, chou-fasman-method, activation-function, early-stopping, cross-validation, alphafold]
sources:
  - paper: doi:10.1006/jmbi.1999.3091
    title: David T. Jones, Protein secondary structure prediction based on position-specific scoring matrices, Journal of Molecular Biology 292(2), 1999, pages 195 to 202
    locator: the three PSI-BLAST iterations, the logistic scaling of the profile, the two networks with window 15 and 75 and 60 hidden units, the training with early stopping, the 187 chain test set with three-fold cross-validation, and the Q3 values for two 8 to 3 state reductions
  - paper: doi:10.1093/nar/25.17.3389
    title: Stephen F. Altschul, Thomas L. Madden, Alejandro A. Schäffer, Jinghui Zhang, Zheng Zhang, Webb Miller and David J. Lipman, Gapped BLAST and PSI-BLAST, a new generation of protein database search programs, Nucleic Acids Research 25(17), 1997, pages 3389 to 3402
    locator: the iterated search that builds the position-specific scoring matrix
  - paper: doi:10.1006/jmbi.1993.1413
    title: Burkhard Rost and Chris Sander, Prediction of protein secondary structure at better than 70% accuracy, Journal of Molecular Biology 232(2), 1993, pages 584 to 599
    locator: the two-level network design on alignment profiles that PSIPRED follows, and the 8 to 3 state reduction it uses
---

PSIPRED predicts the [secondary structure](/protein-secondary-structure/) state, helix, strand or coil, of each residue of a protein. It runs PSI-BLAST to build a [position-specific scoring matrix](/position-specific-scoring-matrix/) (PSSM) of the protein's family, feeds a window of 15 rows of that matrix to a neural network, and feeds a window of 15 outputs of the first network to a second network that cleans up the prediction. It is a learned model: its weights come from training on proteins of known structure, it has no accuracy guarantee, and its quality is a measured number. Jones reported a Q3 of 76.5 percent in 1999, which made it the most accurate method of its time.

## In plain words

To guess the shape of one spot of a protein, PSIPRED first looks for its relatives in a large database of proteins. From the relatives it builds a table that says, for each position, which amino acids the family tolerates there. That table says much more about the shape than the single sequence does.

A small neural network then reads the table rows for the position and seven positions on each side. It gives three numbers, one for helix, one for strand and one for coil. A second small network reads those three numbers for the position and its neighbours, and gives three new numbers. This second look fixes predictions that make no sense together, such as a helix only one amino acid long. The largest of the final three numbers is the answer.

## The problem

The input is a protein sequence of length $n$ over the 20 amino acids. The PSI-BLAST search turns it into a PSSM $Q$: $n$ rows of 20 log-odds scores, typically in the range $-7$ to $7$, one row for each position and one score for each amino acid. The output is a label in $\{H, E, C\}$ for each residue, with three output values per residue as confidence. The truth for training and testing is DSSP, cut from 8 states to 3. This is [protein secondary structure prediction](/protein-secondary-structure-prediction/) with evolutionary information.

The model on this page is the forward pass of the two networks in real arithmetic on the [word RAM](/word-ram/). Training is by [backpropagation](/backpropagation/) on labelled data; the weights of the published networks and the training data are not reproduced here, and the implementation uses weights from a seeded generator or by hand.

## The algorithm

Each network has one hidden layer, and every unit applies the logistic function $\sigma(u) = 1/(1 + e^{-u})$, an [activation function](/activation-function/). For a window of $w$ positions centred on residue $j$, each position gives $f$ features and one extra input, the end flag, which is 1 when the position is off the chain (then the $f$ features are 0) and 0 otherwise. So a network reads $w(f + 1)$ inputs. In PSIPRED, $w = 15$ for both networks; network 1 has $f = 20$, so $15 \cdot 21 = 315$ inputs, 75 hidden units and 3 outputs; network 2 has $f = 3$, so $15 \cdot 4 = 60$ inputs, 60 hidden units and 3 outputs.

```pseudo id=main
WINDOW-NET(R, W, b, V, c, w)               ▷ R: n rows of f features; W, b: hidden layer; V, c: output layer
L1  for j ← 0 to n − 1 do
L2      z ← b
L3      for o ← 0 to w − 1 do
L4          p ← j + o − ⌊w/2⌋
L5          if 0 ≤ p < n then z ← z + W_o R[p]                  ▷ W_o: feature columns of block o
L6          else z ← z + (flag column of block o of W)         ▷ only the end flag is 1
L7      g ← σ(z)
L8      out[j] ← σ(V g + c)
L9  return out

PSIPRED(Q, net1, net2)                     ▷ Q: the n × 20 PSSM
L10 R[p][a] ← σ(Q[p][a]) for each position p and amino acid a
L11 S1 ← WINDOW-NET(R, net1)               ▷ w = 15, 75 hidden units
L12 S2 ← WINDOW-NET(S1, net2)              ▷ w = 15, 60 hidden units
L13 y_j ← the state of H, E, C with the largest entry of S2[j], for each j
L14 return y
```

Line L10 maps each PSSM score into $(0, 1)$, which is the scaling of the paper. Lines L5 and L6 add the weights of each window block on the fly: an off-chain block has only its flag input set, so it adds one weight column, and the input vector of length $w(f + 1)$ is never built. Line L12 runs the second network on the outputs of the first, so it sees the predicted states of 15 neighbours and can remove a helix or strand of one residue.

The published method has two more parts that the pseudocode takes as given. PSI-BLAST runs three iterations against a large sequence database, which the paper filters to remove low-complexity, transmembrane and coiled-coil regions, so that unrelated sequences do not drift into the profile. The networks are trained by on-line backpropagation, with 10 percent of the training data held out for [early stopping](/early-stopping/).

## Example

**A hand-sized network.** Take $w = 3$, $f = 1$, one hidden unit with weights $(1, 0, 2, 0, -1, 0.5)$ and bias 0, so that the three blocks are $(1, 0)$, $(2, 0)$ and $(-1, 0.5)$ (feature weight, flag weight). The output layer has weights $1$, $-1$ and $0$ from the hidden unit and biases 0. The input has $n = 2$ rows, $R = [0.5], [1.0]$.

- Centre $j = 0$: block 0 is off the chain and adds its flag weight 0; block 1 adds $2 \cdot 0.5 = 1$; block 2 adds $-1 \cdot 1.0 = -1$. So $z = 0$, $g = \sigma(0) = 0.5$, and the outputs are $\sigma(0.5) = 0.6225$, $\sigma(-0.5) = 0.3775$ and $\sigma(0) = 0.5$.
- Centre $j = 1$: block 0 adds $1 \cdot 0.5 = 0.5$; block 1 adds $2 \cdot 1.0 = 2$; block 2 is off the chain and adds its flag weight 0.5. So $z = 3$, $g = \sigma(3) = 0.9526$, and the outputs are $\sigma(0.9526) = 0.7216$, $\sigma(-0.9526) = 0.2784$ and $0.5$.

The full window vectors are $(0, 1, 0.5, 0, 1.0, 0)$ for $j = 0$ and $(0.5, 0, 1.0, 0, 0, 1)$ for $j = 1$; their dot products with the hidden weights are 0 and 3, the same as the block sums.

**The real sizes.** Network 1 has $315 \cdot 75 + 75 + 75 \cdot 3 + 3 = 23928$ weights and biases. Network 2 has $60 \cdot 60 + 60 + 60 \cdot 3 + 3 = 3843$. One residue costs about $15 \cdot 20 \cdot 75 = 22500$ multiplications in the hidden layer of network 1 and $15 \cdot 3 \cdot 60 = 2700$ in network 2.

## Correctness

For given weights, the forward pass is exact in real arithmetic: the hidden pre-activation $W X_j + b$ of the full window vector $X_j$ splits into one term per block, and each block term is the feature columns times the row on the chain, or the flag column off the chain. The full proof is below. There is no correctness claim for the predictions. PSIPRED is a trained classifier, and its accuracy is a measurement on held-out proteins:

- Jones tested on 187 chains with three-fold cross-validation, after removing from each training set the chains structurally similar to its test chains.
- With the reduction of Rost and Sander (DSSP H and G to helix, E and B to strand, the rest to coil), the Q3 per residue was 76.5 percent; the mean over chains was 76.0 percent with a standard deviation of 7.8, and the segment overlap score was 73.5 percent.
- With the stricter reduction (only H to helix and only E to strand) the same predictions scored 78.3 percent.

## Complexity

Let $n$ be the sequence length, $w$ the window width, $f$ the inputs per position and $u$ the hidden units. One network costs $\Theta(n w f u)$ time for the hidden layer and $\Theta(n u)$ for the output layer, in every case. For PSIPRED the first network dominates, with $w = 15$, $f = 20$ and $u = 75$. The extra space is $\Theta(n)$ for the outputs and $\Theta(u)$ for one hidden layer, besides the weights. The networks are cheap; the PSI-BLAST search that builds the profile takes almost all of the running time, and its cost depends on the size of the database.

## Properties

- **Learned, no guarantee.** The prediction is as good as the training data and the profile. For a protein with few or no homologs, the profile is weak and the accuracy drops toward that of single sequence methods.
- **Local.** Each label depends on 15 profile rows through network 1 and so on 29 profile rows through both networks. Long-range pairing of strands is not seen.
- **Deterministic.** For fixed weights and a fixed profile the output is fixed. The profile depends on the database version, so the same sequence can get slightly different predictions over time.
- **Confidence values.** The three outputs give a confidence for each residue, and the published program reports one.

## Variants and improvements

- **PHD.** The design follows PHD of Rost and Sander (1993), which used profiles from multiple alignments, a sequence-to-structure network and a structure-to-structure network. PSIPRED replaced the alignment profile by the PSI-BLAST PSSM.
- **Deep networks.** Later methods use deep, recurrent and convolutional networks over the whole sequence and more profile features. They report about 82 to 84 percent Q3 without templates.
- **Other targets.** The same two-stage design predicts solvent accessibility, disorder and transmembrane topology.

## When to use it

Use PSIPRED when you need a fast, well-tested secondary structure prediction and the protein has homologs in the sequence databases. Use the confidence values: low-confidence segments are often wrong. For a protein with a close homolog of known structure, the structure of the homolog is better. For the best accuracy today, deep learning methods, or DSSP on a model from [AlphaFold](/alphafold/), do better.

## Pitfalls

- **Profile drift.** Without filtering the database, PSI-BLAST can pull in unrelated sequences through low-complexity or coiled-coil regions, and the profile then misleads the network.
- **Comparing Q3 values.** The two values for two reductions in the correctness section come from the same predictions. Compare methods only on the same test set with the same reduction.
- **Homologs in the test set.** A test protein that is similar to a training protein makes the accuracy look higher. Jones screened by structural similarity, not only by sequence identity.
- **Window edges.** The end flag is a real input. Padding with zeros and no flag makes the start and end of the chain look like a profile of all zeros, which the network never saw in training.
- **Scaling.** The networks were trained on logistic-scaled PSSM values. Feeding raw scores, or a PSSM from a different PSI-BLAST version with a different scale, changes the inputs.

## Implementations

## History

The first neural network predictors of secondary structure read single sequences. Rost and Sander's PHD in 1993 put alignment profiles into the networks and passed 70 percent Q3. Jones published PSIPRED in 1999, replacing the alignment profile by the PSI-BLAST PSSM of Altschul and coworkers (1997), and it became one of the most used prediction servers.

## References
