---
title: "The HMM tagger returns a most probable tag sequence, and its smoothed transitions are distributions"
proves: [correctness]
status: full
---

Fix the order $m \ge 1$, the tag set $Y$ with $k$ tags, a sentence $x_1 \ldots x_n$ with $n \ge 1$, and the two tables of the trained model: $P(t \mid h)$ for a history $h$ of $m$ symbols from $Y \cup \{\langle s \rangle\}$ and a tag $t \in Y \cup \{\langle /s \rangle\}$, and $P(w \mid t)$. Write $y_{1-m} = \cdots = y_0 = \langle s \rangle$ and $y_{n+1} = \langle /s \rangle$, and $h_i = (y_{i-m+1}, \ldots, y_i)$ for the state after position $i$. The model gives

$$\log P(x, y) = \sum_{i=1}^{n} \bigl( \log P(y_i \mid h_{i-1}) + \log P(x_i \mid y_i) \bigr) + \log P(\langle /s \rangle \mid h_n),$$

with $\log 0 = -\infty$ and $-\infty + a = -\infty$.

## Claim 1: Viterbi over states of m tags is exact

For $0 \le i \le n$ and a state $h$, let $\delta_i(h)$ be the largest value of the partial sum $S_i(y_1 \ldots y_i) = \sum_{j=1}^{i} (\log P(y_j \mid h_{j-1}) + \log P(x_j \mid y_j))$ over the tag prefixes $y_1 \ldots y_i$ with $h_i = h$, and $-\infty$ if there is none.

Invariant: after the loop of line L6 has run for position $i$, the table `delta` holds $\delta_i(h)$ for every state $h$ with $\delta_i(h) > -\infty$, and `back[i]` holds for each such $h$ a state $g$ such that a best prefix for $h$ ends with a best prefix for $g$.

Base: line L5 sets $\delta_0(\langle s \rangle^m) = 0$, the empty sum. No other state has a prefix of length 0.

Step: a prefix $y_1 \ldots y_i$ with $h_i = h$ is a prefix $y_1 \ldots y_{i-1}$ with some state $g = h_{i-1}$, followed by the tag $t = y_i$, and $h$ is $g$ with its first symbol dropped and $t$ appended. Its sum is $S_{i-1}(y_1 \ldots y_{i-1}) + \log P(t \mid g) + \log P(x_i \mid t)$. The last two terms depend only on $g$ and $t$, so for a fixed $g$ the sum is largest when the prefix of length $i - 1$ is a best prefix for $g$. Hence $\delta_i(h) = \max_g (\delta_{i-1}(g) + \log P(t \mid g) + \log P(x_i \mid t))$, where $g$ ranges over the states whose last $m - 1$ symbols are the first $m - 1$ symbols of $h$. Line L7 computes this maximum over all states $g$ in `delta` and keeps the maximizer. A state $g$ with $\delta_{i-1}(g) = -\infty$ or a tag with $\log P(x_i \mid t) = -\infty$ is skipped; it can only give $-\infty$, so the maximum does not change.

By the invariant for $i = n$, line L8 finds the maximum over $h$ of $\delta_n(h) + \log P(\langle /s \rangle \mid h)$, which is $\max_y \log P(x, y)$, because every full sequence is a prefix of length $n$ followed by the end transition. Line L9 follows the stored maximizers from the final state back to position 1. Each step goes from a state to a predecessor that is part of a best prefix, so the tags read off form a sequence whose log probability equals the maximum. If no state has a finite score, every sequence has probability 0 and the code raises an error instead.

## Claim 2: the interpolated transitions are distributions

Let $f(g)$ be the number of predicted events with tag $n$-gram $g$ (line L1) and $f_h(c)$ the number of predicted events whose history ends with the context $c$. Each predicted event with history ending in $c$ has exactly one predicted tag, so $\sum_t f(c\,t) = f_h(c)$. Hence for a seen context, the estimate $\hat P(t \mid c) = f(c\,t) / f_h(c)$ is nonnegative and sums to 1 over $t \in Y \cup \{\langle /s \rangle\}$. The same holds for the order 0 estimate $f(t) / N$, since $N$ counts all predicted events.

Line L2 adds the count of each $(m+1)$-gram to exactly one weight, so the weights are nonnegative and their sum before normalization is the number of predicted events, $N > 0$. After normalization they sum to 1. Line L3 forms $P(t \mid h) = \sum_{j=0}^{m} \lambda_j \hat P(t \mid c_j)$, where $c_j$ is the last $j$ symbols of $h$. If every $c_j$ was seen in training, this is a convex combination of distributions on the same set, so it is a distribution. If some $c_j$ was not seen, its estimate is defined as 0 (the rule under Figure 1 of Brants 2000), and the row sums to $1 - \sum_{\text{unseen } j} \lambda_j < 1$ when those weights are positive. Such histories never occur in the training data. The model is then deficient on them, which TnT accepts; the test file checks both cases in exact arithmetic.

The emission $f(w, t) / f(t)$ of a known word sums to 1 over the words of the lexicon for each tag, because each token tagged $t$ has one word. The score of an unknown word is $P(t \mid \text{suffix}) / P(t)$, which is the inverted suffix probability up to a factor $P(\text{suffix})$ that is the same for every tag. A factor common to all tags at one position adds the same constant to every path, so it does not change the argmax of Claim 1.
