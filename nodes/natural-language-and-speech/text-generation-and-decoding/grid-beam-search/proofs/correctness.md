---
title: Grid beam search is sound, exact with an unbounded beam, and makes at most n k (c + 1) calls
proves: [correctness]
status: full
---

We use the notation of the page. The phrases $P_1, \ldots, P_m$ are non-empty, contain no `</s>`, and have $c$ tokens in all. An output $y = y_1 \ldots y_\ell$ ends with its only `</s>`, so its body is $y_1 \ldots y_{\ell - 1}$. A *placement* of the phrases in $y$ is a choice of start positions $s_1, \ldots, s_m$ such that $y_{s_i} \ldots y_{s_i + |P_i| - 1} = P_i$ for each $i$, and the $m$ blocks are disjoint subsets of the body. The output holds the phrases if it has a placement.

A hypothesis $h$ has a prefix $h.y$, a score $h.s$, a set $h.D$ of covered phrases, and, if it is open, a phrase index $h.i$ and a position $h.j$ with $1 \le h.j < |P_{h.i}|$. Write $\mathrm{cnt}(h) = \sum_{i \in h.D} |P_i| + h.j$ for an open $h$, and $\sum_{i \in h.D} |P_i|$ for a closed one.

**Lemma 1 (invariant of a hypothesis).** Every hypothesis $h$ that the search builds satisfies: (a) $h.s = \log p(h.y)$, the sum of the token log probabilities; (b) $h$ lies in the cell $\mathrm{cnt}(h)$; (c) $h.y$ has disjoint blocks that hold each covered phrase in full and, if $h$ is open, the first $h.j$ tokens of $P_{h.i}$ at the end of $h.y$, and these blocks are disjoint.

*Proof.* By induction on the steps. The empty hypothesis of line L1 has score 0, nothing covered, and lies in cell 0. Line L6 appends a free token $w$ to a closed $h$, adds $\log p(w \mid h.y)$ and keeps the cell and the blocks. Line L7 appends the first token of an uncovered phrase $P_i$ to a closed $h$; the new block starts at the new position, after all old blocks, so it is disjoint from them, and the count grows by 1, which is the cell $c' + 1$. If $|P_i| = 1$ the phrase is covered at once. Line L8 appends the next token of the open phrase at the end, so its block stays contiguous, and the count grows by 1; when the last token is placed, the phrase moves to $h.D$ and $h$ becomes closed. Line L9 only removes hypotheses. $\square$

**Theorem 2 (soundness).** If the search returns $(y, s)$, then $y$ holds the phrases and $s = \log p(y)$.

*Proof.* Line L5 finishes only a closed hypothesis $h$ in cell $c$. By Lemma 1(b) and since $h$ is closed, $\sum_{i \in h.D} |P_i| = c$, so $h.D$ holds all $m$ phrases, and by Lemma 1(c) their blocks are disjoint and lie in $h.y$, the body of $y = h.y$ `</s>`. The score is $h.s + \log p(\text{</s>} \mid h.y) = \log p(y)$ by Lemma 1(a). $\square$

**Lemma 3 (safe pruning of cells).** A hypothesis of $t$ tokens with count $c' < c - (n - 1 - t)$ has no extension to an output of at most $n$ tokens that the search can finish.

*Proof.* Each token adds at most 1 to the count, and a finished output of at most $n$ tokens has at most $n - 1 - t$ more tokens before its `</s>`. To finish, the count must reach $c$ (Theorem 2), so $c' + (n - 1 - t) \ge c$ is needed. $\square$

**Theorem 4 (exact with an unbounded beam).** If $k$ is at least the number of hypotheses that are ever put into one cell at one step, the search returns an output $y^*$ that holds the phrases with the largest $\log p(y^*)$ among all outputs of at most $n$ tokens, or none if there is no such output of positive probability.

*Proof.* With such a $k$, line L9 removes only the cells of Lemma 3. Take an output $y$ of positive probability and at most $n$ tokens with a placement $s_1, \ldots, s_m$. Build its hypotheses token by token: at position $u$ of the body, if $u = s_i$ for some $i$, use line L7 with phrase $i$; if $u$ lies inside a block that started earlier, use line L8; otherwise use line L6. Each choice is allowed, since a block starts only when the hypothesis is closed (the blocks are disjoint and contiguous, so the previous block has ended), the phrase is not covered yet, and every token has positive probability. After the body, the hypothesis is closed with count $c$, and line L5 at the next step finishes $y$ with its true score. None of these hypotheses is removed by Lemma 3, since each has a completion. So $y$ is a candidate for best, and line L5 keeps the largest score seen. By Theorem 2 every candidate holds the phrases. $\square$

**Theorem 5 (the call bound).** The search makes at most $n k (c + 1)$ model calls.

*Proof.* Line L4 makes one call per hypothesis in the grid at the start of a step. After line L9 each of the $c + 1$ cells holds at most $k$ hypotheses, and line L1 starts with one. There are $n$ steps. $\square$

**What is not claimed.** With a finite $k$, line L9 can remove the prefix of $y^*$, and the search returns a worse output or none. The page gives a model (seed 0 in the test) where $k = 1$ returns b c `</s>` with log probability $-5.020$, while $y^*$ = a c b c `</s>` has $-2.745$. The test also checks that an unbounded beam returns $y^*$ on that model, as Theorem 4 says.
