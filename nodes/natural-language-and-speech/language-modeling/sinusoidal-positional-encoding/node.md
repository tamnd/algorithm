---
tag: D6ZPH5
kind: technique
slug: sinusoidal-positional-encoding
name: Sinusoidal positional encoding
aliases:
- absolute positional encoding
area: natural-language-and-speech/language-modeling
level: core
summary: "Add to each token vector sines and cosines of its position at geometrically spaced frequencies, so attention can use word order."
prereqs: [scaled-dot-product-attention]
see_also: [transformer, rotary-position-embedding, alibi-attention-bias, multi-head-attention, embedding, givens-rotations, fast-fourier-transform, bert]
sources:
  - paper: "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser and Illia Polosukhin, Attention is all you need, Advances in Neural Information Processing Systems 30 (NIPS 2017)"
    title: Vaswani et al. 2017
    locator: "Section 3.5 (the formula, the geometric wavelengths from 2 pi to 10000 times 2 pi, the linear shift, learned embeddings as the alternative), Table 3 row (E)"
  - paper: "Ofir Press, Noah A. Smith and Mike Lewis, Train short, test long: attention with linear biases enables input length extrapolation, ICLR 2022, arXiv:2108.12409"
    title: Press, Smith and Lewis 2022
    locator: the extrapolation experiments with the sinusoidal, rotary and T5 bias methods
  - book: isbn:9780262048644
    title: Simon J. D. Prince, Understanding Deep Learning, MIT Press 2023
    locator: Chapter 12 (Transformers)
---

The sinusoidal positional encoding gives each position $pos$ of a sequence a fixed vector $\mathrm{PE}(pos)$ of size $d$, made of sines and cosines of $pos$ at $d/2$ frequencies, and adds it to the token embedding at that position. [Scaled dot-product attention](/scaled-dot-product-attention/) does not see the order of its inputs, so without such a signal a [transformer](/transformer/) treats a sentence as a bag of words. The frequencies form a geometric sequence, so the wavelengths run from $2\pi$ to $10000 \cdot 2\pi$. The main property is that a shift by a fixed offset $k$ is a linear map: $\mathrm{PE}(pos + k) = M_k\, \mathrm{PE}(pos)$, with a matrix $M_k$ of 2 by 2 rotations that does not depend on $pos$.

## In plain words

Attention mixes words by how well they match, and it would give the same result if the words were shuffled. So each position needs a mark that tells where it is.

Think of a row of clocks with hands that turn at different speeds. The first hand turns fast, the next one slower, and the last one very slowly. At position one, all hands are turned a little; at position two, twice as much; and so on. The reading of all the hands together is a different pattern for every position, and the pattern is added to the word.

Fast hands tell nearby positions apart. Slow hands tell far positions apart. Because moving forward by a fixed number of steps turns every hand by a fixed amount, the network can learn to look a fixed number of words back.

## When it applies

- The model mixes positions with a mechanism that is blind to order: self-attention in a [transformer](/transformer/) encoder, or a decoder where the causal mask alone gives only weak order information.
- A fixed encoding is wanted: no extra parameters, and values for any position, including positions longer than those seen in training (though the model may not use them well).
- The model takes absolute positions as input. If only distances should matter, a relative method such as [rotary position embedding](/rotary-position-embedding/) or [ALiBi](/alibi-attention-bias/) builds that into the scores.

## The template

Let $d$ be even and let $\omega_i = 10000^{-2i/d}$ for $i = 0, \ldots, d/2 - 1$. Coordinates are numbered from 0, as in the paper.

$$\mathrm{PE}(pos)_{2i} = \sin(pos \cdot \omega_i), \qquad \mathrm{PE}(pos)_{2i+1} = \cos(pos \cdot \omega_i).$$

```pseudo id=main
SINUSOIDAL-PE(pos, d)                ▷ d even
L1  for i ← 0 to d/2 - 1 do
L2      ω_i ← 10000^(-2i/d)
L3      PE[2i] ← sin(pos · ω_i)
L4      PE[2i+1] ← cos(pos · ω_i)
L5  return PE
```

The input of the first layer at position $pos$ is $\sqrt{d}\, E_{x_{pos}} + \mathrm{PE}(pos)$, the scaled token embedding plus the encoding.

**The linear shift (theorem).** For every offset $k$ there is a matrix $M_k$, independent of $pos$, with $\mathrm{PE}(pos + k) = M_k\, \mathrm{PE}(pos)$. By the angle-sum formulas, for each pair,

$$\begin{pmatrix} \sin((pos + k)\omega_i) \\ \cos((pos + k)\omega_i) \end{pmatrix} = \begin{pmatrix} \cos k\omega_i & \sin k\omega_i \\ -\sin k\omega_i & \cos k\omega_i \end{pmatrix} \begin{pmatrix} \sin pos\,\omega_i \\ \cos pos\,\omega_i \end{pmatrix},$$

so $M_k$ is block diagonal with these rotation blocks. The [full proof](proofs/correctness.md) also shows the two corollaries below.

**Distance in the dot product (theorem).** $\mathrm{PE}(p) \cdot \mathrm{PE}(p + k) = \sum_i \cos(k \omega_i)$, which depends only on $k$, and $\lVert \mathrm{PE}(p) \rVert = \sqrt{d/2}$ for every $p$. The linear maps of attention act on the sum of the token embedding and the encoding, so in a trained model the score of two positions depends on both their contents and their absolute positions, not on the offset alone.

**Cost.** $\Theta(d)$ per position, $\Theta(n d)$ for a sequence; in practice the $n \times d$ table is computed once.

## Classic examples

**The original transformer.** Vaswani and colleagues added the encoding to the embeddings in both stacks of the [transformer](/transformer/) for translation. Learned position vectors gave nearly the same BLEU (Table 3, row E, a measurement); they chose the sinusoid because it may extrapolate to longer sequences.

**A small table.** With $d = 4$ the frequencies are $\omega_0 = 1$ and $\omega_1 = 10000^{-1/2} = 0.01$:

| $pos$ | $\sin pos$ | $\cos pos$ | $\sin 0.01 pos$ | $\cos 0.01 pos$ |
|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 1 |
| 1 | 0.841471 | 0.540302 | 0.010000 | 0.999950 |
| 2 | 0.909297 | -0.416147 | 0.019999 | 0.999800 |
| 3 | 0.141120 | -0.989992 | 0.029996 | 0.999550 |

The first pair changes fast and the second slowly. $\mathrm{PE}(1) \cdot \mathrm{PE}(2) = \cos 1 + \cos 0.01 = 1.540252$, and every pair of positions at distance 1 gives the same value. At distance 2 the value is $\cos 2 + \cos 0.02 = 0.583653$.

**The same rotation inside attention.** [Rotary position embedding](/rotary-position-embedding/) uses the same frequencies and the same 2 by 2 rotations, but applies them to the queries and keys instead of adding them to the input, so that the score depends only on the offset.

**Learned positions instead.** [BERT](/bert/) and GPT-2 learn one vector per position up to a maximum length. This is as cheap at run time, but gives nothing for positions beyond that length.

**Relative sinusoids in speech.** The [Conformer](/conformer/) speech encoder uses a relative form of the sinusoidal encoding inside its self-attention modules.

## Variations

- **Halves instead of pairs.** Many code bases put all sines in the first half of the vector and all cosines in the second. This is a fixed permutation of the coordinates and has the same properties.
- **Another base.** The constant 10000 sets the longest wavelength. A larger base suits longer sequences.
- **Concatenation instead of addition.** Appending the encoding keeps it apart from the content at the cost of a wider input.
- **Positions from 1.** The paper numbers positions from 0. Starting from 1 only shifts every vector by $M_1$.
- **Learned absolute positions.** A table of $L \times d$ learned vectors, as in BERT and GPT-2.
- **Relative methods.** [RoPE](/rotary-position-embedding/) and [ALiBi](/alibi-attention-bias/) put the offset into the scores directly.

## Pitfalls

- **Layout mismatch.** Mixing the interleaved layout (sine at $2i$, cosine at $2i + 1$) with the layout in halves, for example when loading weights from another code base, silently gives wrong inputs. Use the layout the model was trained with.
- **Off-by-one positions.** Training with positions from 0 and running with positions from 1 shifts every encoding. Fix one convention.
- **Expecting length extrapolation.** The encoding is defined for any position, but Press and colleagues measured that models trained with it get much worse soon after the training length (a measurement). Do not rely on it for inputs much longer than the training data; use [ALiBi](/alibi-attention-bias/) or train on longer inputs.
- **Odd $d$.** The formula needs pairs; with an odd size, one coordinate has no partner.
- **Scale of the embeddings.** The original multiplies the token embeddings by $\sqrt{d}$ before the sum. Without it, small embeddings can be swamped by the encoding, whose coordinates are of size 1.

## Exercises

1. Prove the angle-sum identity for $M_k$ and show that $M_k$ is orthogonal, $M_k^\top M_k = I$, and that $M_{k} M_{l} = M_{k + l}$.
2. Show that $\mathrm{PE}(p) \cdot \mathrm{PE}(q) = \sum_i \cos((q - p)\omega_i)$ and that it is symmetric in $p$ and $q$. What does this say about telling "before" from "after" with the dot product alone?
3. For $d = 512$, compute the shortest and longest wavelengths $2\pi/\omega_i$. Use the pair with $\omega_0 = 1$ and the fact that $\pi$ is irrational to show that two different integer positions never get the same vector.
4. Show that the layout in halves is $P\, \mathrm{PE}(pos)$ for a permutation matrix $P$, and that the shift property still holds with $P M_k P^\top$.
5. Let $W^Q$ and $W^K$ be the attention maps. Write the score of tokens $x$ at $p$ and $y$ at $q$ as four terms and show which ones depend on $p$ and $q$ separately and not only on $q - p$.

## References
