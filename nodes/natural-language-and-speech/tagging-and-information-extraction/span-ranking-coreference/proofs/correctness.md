---
title: "Span-ranking coreference: the pruning, the marginal likelihood loss and its gradient, and the decoder are correct"
proves: [correctness]
status: full
---

Fix a document of $n$ tokens, a maximum width $L$, a ratio $\lambda > 0$, a number $K \ge 1$ of antecedents, mention scores $s_m(i)$ for every span of width at most $L$, and pair scores $s_a(i, j)$. Spans use fencepost indices: $(a, b)$ covers the tokens $a + 1, \ldots, b$. Logs are natural logs. The line numbers refer to the pseudocode on the page.

## Claim 1: the kept spans are a non-crossing set of at most floor(lambda n) spans

Line L3 adds a span to $M$ only while $|M| < \lfloor \lambda n \rfloor$, so $|M| \le \lfloor \lambda n \rfloor$ at the end. It adds a span only if it crosses no span already in $M$. Crossing is symmetric: $(a, b)$ and $(c, d)$ cross when $a < c < b < d$ or $c < a < d < b$, and the two conditions swap when the spans swap. So when a span $t$ joins $M$, it crosses no earlier member, and every later member was tested against $t$. Hence no two members of $M$ cross. Also, if a span $s$ was skipped while $M$ was not full, then $s$ crosses some member of $M$ that was added before it, so a skipped span with a higher score than a kept span always crosses a kept span. Line L4 only reorders $M$.

## Claim 2: the loss is the negative log of a marginal over full antecedent assignments

Let $m = |M|$ and let $Y(i)$ be the list of line L5: the dummy $\varepsilon$ and at most $K$ earlier spans. Line L6 sets $s(i, \varepsilon) = 0$ and $s(i, j) = s_m(i) + s_m(j) + s_a(i, j)$. Line L7 gives

$$P(y \mid i) = \frac{\exp s(i, y)}{\sum_{y' \in Y(i)} \exp s(i, y')},$$

which is positive and sums to 1 over $Y(i)$. The model of Lee et al. (2017) takes the antecedents of different spans to be independent, so a full assignment $y = (y_1, \ldots, y_m)$ with $y_i \in Y(i)$ has probability $P(y) = \prod_i P(y_i \mid i)$. Let $G(i) \subseteq Y(i)$ be the set of line L8. It is never empty: it holds the gold antecedents of $i$ among $Y(i)$, or $\varepsilon$ alone if there are none. The set of assignments consistent with the gold clusters is the product $G(1) \times \cdots \times G(m)$, so

$$\sum_{y \in G(1) \times \cdots \times G(m)} \prod_i P(y_i \mid i) = \prod_i \sum_{y_i \in G(i)} P(y_i \mid i)$$

by the distributive law. Taking $-\log$ gives the sum of line L9. Each factor is in $(0, 1]$, so the loss is at least 0. It is 0 exactly when every span puts all its probability on $G(i)$, which with finite scores happens only when $G(i) = Y(i)$.

The code computes $\log P(y \mid i)$ with log_softmax and the inner sum with log_sum from the shared helper. Both subtract the largest value before any exp, so no exp of a positive number is taken and the result is finite whenever the scores are finite. The test file checks the identity above against the sum over all assignments, listed one by one, on random documents.

## Claim 3: the gradient

Write $Z_i = \sum_{y' \in Y(i)} \exp s(i, y')$ and $Z_i^G = \sum_{y' \in G(i)} \exp s(i, y')$. The term of span $i$ is $\ell_i = \log Z_i - \log Z_i^G$. For $y \in Y(i)$,

$$\frac{\partial \ell_i}{\partial s(i, y)} = \frac{\exp s(i, y)}{Z_i} - [y \in G(i)] \frac{\exp s(i, y)}{Z_i^G} = P(y \mid i) - Q(y \mid i),$$

where $Q(y \mid i)$ is $P(y \mid i)$ restricted to $G(i)$ and renormalized. The score $s(i, y)$ appears in $\ell_i$ only. By the chain rule, $\partial \ell / \partial s_a(i, j) = P(j \mid i) - Q(j \mid i)$, and $\partial \ell / \partial s_m(k)$ is the sum of $P(y \mid i) - Q(y \mid i)$ over every pair $(i, y)$ with $y \ne \varepsilon$ in which $k$ is either $i$ or $y$. The dummy score is the constant 0 and has no gradient. This is what loss_and_grad returns; the test file checks every component against central finite differences with $h = 10^{-6}$ and tolerance $10^{-5}$.

## Claim 4: the decoder returns a most probable assignment and well-formed clusters

Since $P(y) = \prod_i P(y_i \mid i)$ and the factors depend on different coordinates, $P(y)$ is largest when each factor is largest. $P(y \mid i)$ is increasing in $s(i, y)$ for a fixed $i$, so line L10 picks a maximizer of each factor, and the tuple of the choices maximizes $P(y)$. The test file checks this against all assignments.

Each span $i$ has at most one antecedent $\hat y_i$, and $\hat y_i$ comes before $i$ in the order of line L4. Draw an edge from $i$ to $\hat y_i$. Every edge points to an earlier span, so the edges form no cycle and the graph is a forest; each tree has exactly one span with $\hat y = \varepsilon$, its first span. Line L11 walks the spans in order. When it reaches $i$ with $\hat y_i = j$, the span $j$ has been processed already, so its cluster is known (or $j$ starts a new one), and $i$ joins it. By induction over the order, the cluster of each span is the tree that contains it. The output clusters are the trees with at least two spans, and they are disjoint.
