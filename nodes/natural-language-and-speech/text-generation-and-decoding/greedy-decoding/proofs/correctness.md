---
title: Greedy decoding follows the greedy rule and has no constant approximation ratio
proves: [correctness]
status: full
---

We use the notation of the page. The model gives $\ell_y(w) = \log p(w \mid y)$ for every prefix $y$ and every token $w \in V$, where $V$ contains `</s>`. All logs are natural logs. An output is a sequence that ends with `</s>` and has no `</s>` before it. The decoder gets a limit $N \ge 1$.

**Lemma 1 (termination).** GREEDY-DECODE makes at most $N$ calls of the model and returns a sequence of at most $N$ tokens.

*Proof.* The loop of line L2 runs at most $N$ times, and each pass makes one call (line L3) and appends one token (line L5). $\square$

**Lemma 2 (the greedy rule and the score).** Let $(y, s)$ be the result, with $y = y_1 \ldots y_n$. Then for every $t \le n$, $y_t$ is the first token in the order of $V$ among those with the largest value of $\ell_{y_{<t}}$. Only $y_n$ can be `</s>`. If $y_n$ = `</s>`, then $y$ is an output; otherwise $n = N$. In both cases $s = \sum_{t=1}^{n} \log p(y_t \mid y_{<t})$.

*Proof.* By induction on the passes of the loop, the invariant at the start of pass $t$ is: $y = y_1 \ldots y_{t-1}$ holds no `</s>`, each $y_u$ with $u < t$ satisfies the greedy rule, and $s = \sum_{u < t} \log p(y_u \mid y_{<u})$. It holds before the first pass, with the empty prefix and $s = 0$ (line L1). In pass $t$, line L3 gets $\ell_{y_{<t}}$, and the argmax of line L4 returns the first index of a largest value (the helper scans in order and replaces the best only on a strictly larger value), so $y_t$ satisfies the rule. Line L5 adds $\ell_{y_{<t}}(y_t) = \log p(y_t \mid y_{<t})$ to $s$. If $y_t$ = `</s>`, line L6 returns, and $y$ ends with its first `</s>`, so it is an output. Otherwise the invariant holds for pass $t + 1$. If the loop ends without a return, $n = N$ and no token is `</s>`. $\square$

So the returned score is the exact log probability of the returned sequence under the model, apart from rounding of the additions.

**Theorem 3 (no constant ratio).** For every $\varepsilon > 0$ there is a model on 5 tokens whose greedy output $g$ and whose most probable output $y^*$ satisfy $p(g) < \varepsilon \, p(y^*)$.

*Proof.* Take $V = \{a, b, c, d, \text{</s>}\}$, a number $0 < \delta < 1/2$ and an integer $L \ge 1$. At the empty prefix, $p(a) = 1/2 + \delta$, $p(b) = 1/2 - \delta$ and the other tokens have probability 0. After the prefix b, `</s>` has probability 1. After a prefix that starts with a and has at most $L$ tokens, each of a, b, c and d has probability $1/4$ and `</s>` has probability 0. After a longer prefix, `</s>` has probability 1.

At the first step the largest probability is $1/2 + \delta$, so $g_1 = a$. After that, every prefix of length at most $L$ that starts with a has four tied tokens of probability $1/4$, so the greedy output takes $L$ more tokens and then `</s>`, and $p(g) = (1/2 + \delta) \, 4^{-L}$. Every output that starts with a has this same probability, and the output b`</s>` has probability $1/2 - \delta$. So $p(y^*) \ge 1/2 - \delta$ and

$$\frac{p(g)}{p(y^*)} \le \frac{1/2 + \delta}{1/2 - \delta} \, 4^{-L}.$$

Choose $\delta = 1/4$ and $L$ with $3 \cdot 4^{-L} < \varepsilon$. $\square$

With $\delta = 0.01$ and $L = 6$, the bound is $(0.51 / 0.49) \cdot 4^{-6} \approx 0.000254$; the test checks that the ratio is below 0.001. The construction uses the fact that the greedy rule compares the next-token probabilities only. The mass $1/2 + \delta$ of the prefix a is spread over $4^L$ continuations, while the mass of b is on one continuation.

**Corollary 4.** Greedy decoding is not an exact algorithm for the decoding problem and has no constant approximation ratio for it. This follows from Theorem 3. Lemma 2 only says that the output is the one that the greedy rule defines, and the tests compare it with exhaustive search for that reason. $\square$
