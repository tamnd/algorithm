---
tag: 05H9N7
kind: technique
slug: error-correcting-output-codes
name: Error-correcting output codes
aliases:
- ECOC
- output coding for multiclass classification
area: machine-learning/supervised-learning
level: advanced
summary: "Give each class a codeword, train one binary classifier per code bit, and decode the outputs to the nearest codeword. Row distance d corrects floor((d-1)/2) errors."
prereqs: [multiclass-classification, hamming-distance]
see_also: [multiclass-classification, one-vs-rest, one-vs-one, hamming-distance, minimum-distance, hamming-code, hamming-bound, boosting]
sources:
  - paper: doi:10.1613/jair.105
    title: Thomas G. Dietterich and Ghulam Bakiri, Solving multiclass learning problems via error-correcting output codes, Journal of Artificial Intelligence Research 2, 263-286, 1995
    locator: the code matrix, row and column separation, the exhaustive codes for 3 to 7 classes, and decoding to the nearest codeword in Hamming distance
  - paper: "Erin L. Allwein, Robert E. Schapire and Yoram Singer, Reducing multiclass to binary: a unifying approach for margin classifiers, Journal of Machine Learning Research 1, 113-141, 2000"
    locator: code matrices in {-1, 0, +1}, Hamming decoding (equation 4), loss-based decoding (equation 5), the distance rho (equation 6), and Theorem 1 (training error at most l eps / (rho L(0)))
  - paper: "Venkatesan Guruswami and Amit Sahai, Multiclass learning, boosting, and error-correcting codes, Proceedings of the 12th Annual Conference on Computational Learning Theory, 145-155, 1999"
    locator: output codes combined with boosting, and decoding that uses the confidences of the binary outputs
---

Error-correcting output codes (ECOC) reduce a $k$-class problem to $\ell$ binary problems through a code matrix $M$ with one row (a codeword) per class and one column per binary problem (Dietterich and Bakiri 1995). Column $s$ relabels the training data: class $r$ becomes $M_{rs} \in \{-1, +1\}$, and a binary classifier $f_s$ learns that labeling. A new input gets the output vector $(f_1(x), \ldots, f_\ell(x))$, which is decoded to the nearest row. If any two rows differ in at least $d$ positions, the decoder still finds the right class when up to $\lfloor (d - 1)/2 \rfloor$ of the binary classifiers are wrong. [One-vs-rest](/one-vs-rest/) and [one-vs-one](/one-vs-one/) are special code matrices with little or no error correction; Allwein, Schapire and Singer (2000) unify all three with entries in $\{-1, 0, +1\}$ and replace the Hamming distance by a loss-based distance that uses the confidences.

## In plain words

Give each class a short password made of yes-or-no answers. Each answer is a question about the input that a binary classifier learns to answer, such as "is it one of these classes or one of those?". To classify a new input, ask all the questions, write down the answers, and find the class whose password is closest.

If the passwords are far apart from each other, a few wrong answers do not matter: the nearest password is still the right one. This is the same idea that lets a scratched disk still play. The cost is more questions, and each question must be learnable.

## When it applies

- You have a binary learner and $k \ge 3$ classes, and you want some robustness to the errors of individual binary classifiers.
- The binary problems defined by the columns are learnable. A column that groups classes with nothing in common is hard for the learner, and its errors are many.
- The errors of different columns are not strongly correlated. Error correction assumes that a few independent bits go wrong, not that many go wrong together.

## The template

$M$ is a $k \times \ell$ matrix with entries in $\{-1, 0, +1\}$; a 0 means that column $s$ does not use class $r$. The holes are the code matrix `M`, the binary learner `BINARY`, and the per-entry distance `DIST` of the decoder.

```pseudo id=main
ECOC-TRAIN(S, M, BINARY)                         ▷ S = ((x_1, y_1), ..., (x_n, y_n))
L1  for s ← 1 to ℓ do
L2      S_s ← ((x_i, M[y_i, s]) : M[y_i, s] ≠ 0)
L3      f_s ← BINARY(S_s)                         ▷ a real-valued score
L4  return (f_1, ..., f_ℓ)
ECOC-PREDICT(f, M, x, DIST)
L5  z ← (f_1(x), ..., f_ℓ(x))
L6  D_r ← Σ_s DIST(M[r, s] · z_s) for r = 1, ..., k
L7  return the smallest r with D_r = min_m D_m
```

Two choices of `DIST`, both from Allwein, Schapire and Singer (2000):

- *Hamming decoding* (their equation 4): $\mathrm{DIST}(u) = (1 - \operatorname{sign}(u))/2$ with $\operatorname{sign}(0) = 0$. For $\pm 1$ entries and nonzero outputs this counts the positions where the sign of $z_s$ differs from $M_{rs}$, the [Hamming distance](/hamming-distance/). A zero entry or a zero output counts $\frac12$.
- *Loss-based decoding* (their equation 5): $\mathrm{DIST}(u) = L(u)$, the margin loss that the binary learner minimizes, for example $e^{-u}$, $\log(1 + e^{-2u})$ or $(1 - u)_+$. A confident output far from a codeword costs more than a hesitant one.

**Error correction by the minimum distance.** Let $M \in \{-1, +1\}^{k \times \ell}$ and let $d$ be the [minimum distance](/minimum-distance/) between two rows. Write $t = \lfloor (d - 1)/2 \rfloor$. *Claim:* if the signs of the outputs differ from row $r$ in at most $t$ positions, Hamming decoding returns $r$, and $r$ is the only nearest row. *Proof.* Let $w$ be the sign vector, with $d_H(w, M_r) \le t$. For any other row $s$, the triangle inequality gives $d_H(w, M_s) \ge d_H(M_r, M_s) - d_H(w, M_r) \ge d - t \ge 2t + 1 - t = t + 1 > t$. $\blacksquare$ The bound is tight: take two rows at distance exactly $d$ and flip $t + 1$ of the positions where they differ, starting from row $r$. Then $w$ is at distance $t + 1$ from $M_r$ and $d - t - 1 \le t + 1$ from $M_s$, so $r$ is no longer the unique nearest row. The implementation checks the claim on every error pattern of weight at most $t$ for several codes, and the tightness on a pattern of weight $t + 1$.

**The exhaustive code.** For $3 \le k \le 7$, Dietterich and Bakiri use the code whose columns are all $2^{k-1} - 1$ nonconstant columns with $+1$ in the first row: row 1 is all $+1$, and row $i \ge 2$ alternates runs of $2^{k-i}$ entries $-1$ and $+1$. Any two rows differ in exactly $2^{k-2}$ columns, so $d = 2^{k-2}$. For $k = 4$:

$$M = \begin{pmatrix} + & + & + & + & + & + & + \\ - & - & - & - & + & + & + \\ - & - & + & + & - & - & + \\ - & + & - & + & - & + & - \end{pmatrix}, \qquad \ell = 7,\ d = 4,\ t = 1.$$

*Why every pair is at distance $2^{k-2}$.* The columns are the vectors in $\{-1, +1\}^k$ with first entry $+1$, except the all-$+1$ vector. For rows $r, s \ge 2$, exactly half of the $2^{k-1}$ vectors with first entry $+1$ differ in positions $r$ and $s$, and the excluded all-$+1$ vector does not, so they differ in $2^{k-2}$ columns. For $r = 1$ and $s \ge 2$, they differ where entry $s$ is $-1$, which is again $2^{k-2}$ of the vectors.

**Column separation.** Dietterich and Bakiri also ask that no two columns be equal or complementary. Two such columns define the same binary problem, so their classifiers make the same errors, and the row distance that they add does not correct anything.

**The bound for loss-based decoding.** Let the distance $\Delta(u, v) = \sum_s (1 - u_s v_s)/2$, so a zero entry counts $\frac12$, and let $\rho = \min_{r \ne r'} \Delta(M_r, M_{r'})$. Let $L$ satisfy $\frac12(L(z) + L(-z)) \ge L(0) > 0$, and let $\varepsilon$ be the average binary loss $\frac{1}{n \ell} \sum_i \sum_s L(M_{y_i s}\, f_s(x_i))$. Then the training error of loss-based decoding is at most $\ell \varepsilon / (\rho\, L(0))$ (Allwein, Schapire and Singer 2000, Theorem 1). *Proof sketch.* If example $i$ is decoded to $r \ne y_i$, its loss vector satisfies $D_{y_i} \ge \frac12(D_{y_i} + D_r)$, and each column contributes at least $L(0)$ times its contribution to $\Delta(M_{y_i}, M_r)$, so $D_{y_i} \ge \rho\, L(0)$. Summing over the misclassified examples gives the bound. It holds for any real outputs, and the implementation tests it on random matrices and outputs. For one-vs-rest $\ell / \rho = k/2$; for all-pairs $\rho = (\ell + 1)/2$, so $\ell / \rho < 2$.

**Cost.** Training is $\ell$ runs of the binary learner, each on the examples of the classes with nonzero entries; prediction is $\ell$ score evaluations plus $O(k \ell)$ for decoding.

**Worked example.** With the $k = 4$ code above, let the true class be row 2 and let classifier 1 err. The sign vector $(+, -, -, -, +, +, +)$ is at distances $3, 1, 5, 5$ from the four rows, so Hamming decoding returns row 2. Now let classifiers 1 and 2 both err, with outputs $z = (0.9, 0.1, -0.8, -0.7, 0.6, 0.5, 0.9)$. The signs $(+, +, -, -, +, +, +)$ are at Hamming distances $2, 2, 6, 4$: a tie, which the smallest-index rule breaks wrongly in favor of row 1. Loss-based decoding with $L(u) = e^{-u}$ gives $7.113, 6.073, 11.681, 10.716$ and returns row 2, because the wrong output $0.1$ of classifier 2 is weak. The logistic and hinge losses also return row 2.

## Classic examples

- [One-vs-rest](/one-vs-rest/): the $k \times k$ matrix with $+1$ on the diagonal and $-1$ elsewhere, $d = 2$, so $t = 0$.
- [One-vs-one](/one-vs-one/): the $k \times \binom{k}{2}$ matrix with entries in $\{-1, 0, +1\}$.
- Codes from coding theory as code matrices: the 16 codewords of the [Hamming code](/hamming-code/) $[7, 4]$ give 16 classes, 7 binary problems and $d = 3$; rows of a [Hadamard code](/hadamard-code/) give pairwise distance half the length.
- Dense and sparse random codes (Allwein, Schapire and Singer 2000), and [boosting](/boosting/) combined with output codes (Guruswami and Sahai 1999).

## Variations

- **Code design.** Exhaustive codes for small $k$; for larger $k$, a subset of the exhaustive columns, random codes improved by hill climbing, or algebraic codes such as BCH codes, all aiming at a large row distance and well-separated columns (Dietterich and Bakiri 1995).
- **Ternary codes.** Zeros let a column ignore some classes, which makes the binary problems smaller and easier; Hamming decoding then counts each zero as $\frac12$.
- **Decoding.** Hamming decoding uses signs only; loss-based decoding uses the margins; with probability outputs, decoding can maximize a likelihood.
- **Learned codes.** Choose the columns to match the confusion structure of the data, so that classes that are easy to separate are split first.

## Pitfalls

- **Correlated errors.** The error-correcting guarantee counts wrong bits. If the binary classifiers share a weakness, many bits fail together, and a large $d$ does not help. Column separation reduces this, but cannot remove it.
- **Hard columns.** A column that puts unrelated classes on the same side can be much harder to learn than one-vs-rest columns. With a linear binary learner, many columns of an exhaustive code are not learnable at all, and their error rates swamp the correction.
- **Ties.** With an even $d$, a pattern of $d/2$ errors can sit exactly between two rows. Report the tie rule, or use loss-based decoding.
- **Scaling of the loss.** Loss-based decoding compares sums of losses across rows, so all binary scores must be on the same scale.

## Exercises

1. Use the [Hamming bound](/hamming-bound/) $k \sum_{i = 0}^{t} \binom{\ell}{i} \le 2^{\ell}$ to show that a code for $k = 10$ classes that corrects one error needs $\ell \ge 7$ columns.
2. Show that every row of the exhaustive code for $k$ classes has the same distance $2^{k-2}$ to every other row, and that no two of its columns are equal or complementary.
3. Prove Theorem 1 of Allwein, Schapire and Singer for the hinge loss $(1 - u)_+$, where $L(0) = 1$.
4. Compute $\rho$ for the all-pairs matrix with $k$ classes and show that $\rho = (\ell + 1)/2$ with $\ell = \binom{k}{2}$.
5. For $d$ even, give an error pattern of weight $d/2$ for which Hamming decoding finds two nearest rows, and one of weight $d/2 + 1$ for which it finds a wrong unique nearest row.

## References
