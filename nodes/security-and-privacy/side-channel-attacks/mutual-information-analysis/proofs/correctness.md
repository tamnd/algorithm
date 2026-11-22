---
title: MIA computes the plug-in mutual information, the right key maximizes the population value, and an injective model fails
proves: [correctness]
status: full
---

All logarithms are to base 2. For a finite table of counts $n(a, c)$ with total $m$, write $\hat P(a, c) = n(a, c)/m$ and $\hat P(a)$, $\hat P(c)$ for its row and column sums.

**Lemma 1 (the loop of line L3).** Line L11 returns the first guess with the largest score.

*Proof.* Every score is a finite number at least 0 (Lemma 2), so the first guess passes line L9. After that, line L9 replaces best only when a score is strictly larger. By induction on the guesses, top is the largest score so far and best is the first guess that reaches it. $\square$

**Lemma 2 (line L7).** Line L7 computes the plug-in mutual information

$$\hat I = \sum_{a, c} \hat P(a, c) \log \frac{\hat P(a, c)}{\hat P(a) \hat P(c)},$$

where the sum is over the cells with $n(a, c) > 0$, and $\hat I \ge 0$.

*Proof.* Expand the logarithm of the quotient: $\log \hat P(a, c) - \log \hat P(a) - \log \hat P(c)$. Summing $\hat P(a, c)$ times the first term gives $-H(h, \text{bin})$. Summing over $c$ first, $\sum_c \hat P(a, c) = \hat P(a)$, so the second term gives $H(h)$, and in the same way the third gives $H(\text{bin})$. So $\hat I = H(\text{bin}) + H(h) - H(h, \text{bin})$, which is line L7. It is the Kullback-Leibler divergence of $\hat P(a, c)$ from the product $\hat P(a)\hat P(c)$, and so it is at least 0 by Gibbs' inequality. $\square$

**The model.** The inputs $p$ are uniform on $\{0, \ldots, 15\}$, and $\ell[j^\ast] = f(W_k) + N$ with $W_g = \mathrm{HW}(S(p \oplus g))$ for each guess $g$, any function $f$, and noise $N$ independent of $p$. Let $b$ be any function from the reals to a finite set of bins, and put $Z = b(\ell[j^\ast])$.

**Lemma 3 (the right key has the largest population value).** For every guess $g$, $I(Z; W_g) \le I(Z; W_k)$.

*Proof.* Given $W_k = w$, the value $Z = b(f(w) + N)$ is a function of $N$ alone, and $N$ is independent of $p$, so $Z$ is independent of $W_g$ given $W_k$. That is, $I(Z; W_g \mid W_k) = 0$. Apply the chain rule of mutual information to the pair $(W_g, W_k)$ in two orders:

$$I(Z; W_g, W_k) = I(Z; W_k) + I(Z; W_g \mid W_k) = I(Z; W_k),$$

$$I(Z; W_g, W_k) = I(Z; W_g) + I(Z; W_k \mid W_g) \ge I(Z; W_g).$$

So $I(Z; W_g) \le I(Z; W_k)$. $\square$

This is the data processing inequality for the chain $W_g \to W_k \to Z$. It holds for every $f$, every noise law and every binning, which is the sense in which MIA is generic. It does not say that the inequality is strict.

**Theorem (consistency with fixed bins).** Suppose that the bin edges are fixed in advance, that the other samples are independent of $p$, and that $I(Z; W_k) > I(Z; W_g)$ for every $g \ne k$. Then the probability that MIA returns $k$ tends to 1 as $m \to \infty$.

*Proof.* For each guess and each sample, the table of line L6 has finitely many cells. By the strong [law of large numbers](/law-of-large-numbers/), each cell frequency converges with probability 1 to its probability. The plug-in mutual information is a continuous function of the cell frequencies, because $x \log x$ is continuous on $[0, 1]$. So each estimate converges with probability 1 to the population value. At a sample $j \ne j^\ast$ the bin is independent of $p$, so the limit is 0 for every guess. At $j^\ast$ the limit of guess $g$ is $I(Z; W_g)$. So $\mathrm{score}(k) \to I(Z; W_k)$, and for $g \ne k$, $\mathrm{score}(g) \to \max(I(Z; W_g), 0) = I(Z; W_g)$, which is strictly smaller by assumption. With 16 guesses, with probability 1 the right key has the strictly largest score for all large $m$, and Lemma 1 then returns it. $\blacksquare$

The code takes the bin edges from the smallest and the largest value of each column. Those edges depend on the data, so the theorem applies to the code only in the form above; the tests check the code against exact values on noiseless traces and by measured success rates on noisy ones.

**Proposition (an injective model fails).** If the model value of line L4 is $h_i = M(S(p_i \oplus g))$ for an injective $M$, then all 16 scores are equal, for every set of traces.

*Proof.* The map $p \mapsto M(S(p \oplus g))$ is injective, because XOR with $g$, the S-box and $M$ are all injective. So for every guess the model value is a relabelling of the input $p$, and the table of line L6 for guess $g$ is the table of the pairs $(p_i, \text{bin}_i[j])$ with its rows renamed. Entropies do not depend on the names of the rows, so line L7 gives the same value for every guess at every sample, and line L8 the same score. $\blacksquare$

**The examples.** On the 16 noiseless balanced traces with $f(w) = w$ and 5 bins, each value has its own bin, so the score of $g$ is the exact $I(W_k; W_g)$ for a uniform input. For $g = k$ this is $H(W_k) = -\sum \tfrac{c}{16}\log\tfrac{c}{16}$ over the counts $1, 4, 6, 4, 1$, which is $2.031$ bits. For $f(w) = (w-2)^2$ and 4 bins, the values $0, 1, 4$ fall into 3 different bins, so the score of $k$ is the entropy of the counts $6, 8, 2$, which is $1.406$ bits. The test file computes all other values of both tables by the sum of Lemma 2 and checks the code against them for every key.
