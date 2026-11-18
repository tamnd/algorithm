---
title: Forward filtering and backward sampling draws a segmentation with probability proportional to P(s) to the power a
proves: [correctness, termination]
status: full
---

Notation. A model gives each piece $w$ a probability $p(w) > 0$. All logs are natural logs. A word $x$ has $n$ characters, and positions are fenceposts $0, \ldots, n$; the piece $x[i{:}j]$ is the edge $i \to j$ of the lattice. A segmentation $s$ is a path $0 \to n$, with $P(s) = \prod_{w \in s} p(w)$. For a smoothing value $a > 0$, the target law is $Q(s) = P(s)^a / Z$ with $Z = \sum_s P(s)^a$, the sum over all segmentations of $x$. Note that $P(s)^a = \prod_{w \in s} p(w)^a$, so $Q$ is the path law of the lattice with edge weights $p(w)^a$.

**Lemma 1 (forward values).** In the LOG semiring, FORWARD gives $\alpha[j] = \ln \sum_{s} P(s)^a$, the sum over the segmentations $s$ of $x[{:}j]$, and $\alpha[0] = 0$.

*Proof.* By induction on $j$: the segmentations of $x[{:}j]$ split, without overlap, by their last piece $x[i{:}j]$, and the weight of each is $p(x[i{:}j])^a$ times the weight of a segmentation of $x[{:}i]$. In log space the product is a sum and the sum over $i$ is log-add. $\square$

**Theorem 1 (the sampler).** If $Z > 0$, SAMPLE-LATTICE stops after at most $n$ steps of line S4 and returns each segmentation $s$ of $x$ with probability exactly $Q(s)$ (up to the rounding of floating point).

*Proof.* Each step of the loop picks a start $i < j$ and sets $j \leftarrow i$, so the loop runs at most $n$ times and ends at $0$. At position $j$ with $\alpha[j] > -\infty$, line S5 gives the start $i$ the weight $\exp(\alpha[i] + a \ln p(x[i{:}j]) - \alpha[j])$. By Lemma 1 these weights are nonnegative and sum to $1$, so line S6 draws $i$ from a probability distribution, and a start with $\alpha[i] = -\infty$ has weight $0$ and is never drawn. Let $s$ have the cut positions $0 = c_0 < c_1 < \cdots < c_r = n$. The sampler returns $s$ when it draws $c_{r-1}$ at $c_r$, then $c_{r-2}$ at $c_{r-1}$, and so on, so

$$\Pr[s] = \prod_{k=1}^{r} \exp\big(\alpha[c_{k-1}] + a \ln p(x[c_{k-1}{:}c_k]) - \alpha[c_k]\big) = \exp\big(\alpha[0] - \alpha[n]\big) \prod_{k=1}^{r} p(x[c_{k-1}{:}c_k])^a = \frac{P(s)^a}{Z},$$

because the $\alpha$ terms telescope, $\alpha[0] = 0$ and $\alpha[n] = \ln Z$. $\square$

**Theorem 2 (the l-best sampler).** NBEST returns the $l$ segmentations of largest $P(s)$ (fewer if $x$ has fewer), and SAMPLE-NBEST returns each of them with probability $P(s)^a / \sum_{t} P(t)^a$, the sum over the returned list.

*Proof.* Let $B_j$ be the $l$ best segmentations of $x[{:}j]$. A segmentation in $B_j$ ends with some piece $x[i{:}j]$, and its prefix is in $B_i$: if the prefix were not among the $l$ best of $x[{:}i]$, then $l$ better prefixes with the same last piece would give $l$ better segmentations of $x[{:}j]$. So the candidates formed from $B_i$ and the edges into $j$ contain $B_j$, and sorting keeps it (ties are broken by the pieces). Lines N2 to N4 normalize the weights $P(s)^a$ in log space and draw one by inversion. $\square$

The sampling frequencies in the tests are checked against the exact law, which is computed by listing all segmentations. That subword regularization improves a translation model is a measurement, reported by Kudo (2018), not a theorem.
