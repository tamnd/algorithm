---
title: PPMC with exclusion gives every symbol a positive probability, its decoder follows the encoder step by step, and the code length is within a small term of the sum of the information of the events
proves: [correctness, termination, length]
status: full
---

Notation. The input is $x_1 \ldots x_n$ over the alphabet $\{0, \ldots, m - 1\}$, and $k$ is the maximum order. The *state* before symbol $i$ is the set of context tables, a map from strings of length at most $k$ to counts. While it codes $x_i$, the encoder holds an order $o$ and a set $E$ of excluded symbols. An *event* is one call of the arithmetic coder with a triple $(lo, hi, total)$, and its probability is $(hi - lo)/total$.

**Lemma 1 (the events are well defined).** At each event the probabilities of the possible outcomes are positive and sum to 1, and the symbol $x_i$ is never in $E$.

*Proof.* In a context with candidates $C$ (the seen symbols not in $E$, line L4), line L5 skips the context when $C$ is empty. Otherwise $n_C \ge q \ge 1$, each candidate $t$ has probability $c_t/(n_C + q) > 0$, the escape has $q/(n_C + q) > 0$, and these sum to $(n_C + q)/(n_C + q) = 1$. A symbol enters $E$ only at line L9, after an escape, which happens only when $x_i \notin C$. So $x_i \notin E$ at all times. At order $-1$ (line L10), the symbols not in $E$ include $x_i$, so the uniform distribution over them is defined and gives $x_i$ the probability $1/(m - |E|) > 0$. Halving the counts at line L11 keeps every count at least 1. $\square$

**Lemma 2 (the decoder follows the encoder).** Suppose that before symbol $i$ the decoder has the same state as the encoder and has output $x_1 \ldots x_{i-1}$. Then the decoder visits the same orders with the same sets $E$ and the same triples, outputs $x_i$, and ends with the same state.

*Proof.* Both start symbol $i$ with $E = \emptyset$ and $o = \min(k, i - 1)$ (lines L2 and L13). The context of order $o$ is the last $o$ output symbols, which are the same on both sides, and so are the table and $C$. Whether a context is skipped depends only on $C$. If it is not skipped, the encoder codes an event with total $n_C + q$, and the decoder asks the arithmetic decoder for a target with the same total. By the correctness of the arithmetic coder of Witten, Neal and Cleary (the [arithmetic coding](/arithmetic-coding/) page), a decoder that uses the same sequence of totals gets back the interval of each event, provided it consumes the same triple. A target below $n_C$ falls in the interval of exactly one candidate, and the decoder consumes that triple; this is the symbol the encoder coded. A target of $n_C$ or more means an escape, and both sides add $C$ to $E$ and go down one order. At order $-1$ both use the same list of symbols not in $E$, in increasing order. The update at L11 and L16 depends only on the symbol, the last $k$ symbols and the order where the symbol was found, which are the same on both sides. $\square$

**Theorem 1 (correctness).** DECODE returns $x_1 \ldots x_n$.

*Proof.* Both sides start with empty tables. By Lemma 1 every event is a valid event of the arithmetic coder, and by Lemma 2 and induction on $i$ the decoder outputs $x_i$ at step $i$. $\square$

**Theorem 2 (length).** Let $p_1, \ldots, p_M$ be the probabilities of the $M$ events of the encoding. The output has at most $\sum_j \lg(1/p_j) + M \lg \frac{1}{1 - 2^{-14}} + 2$ bits before the padding to a byte.

*Proof.* The coder keeps $high - low + 1 > 2^{30}$ after each renormalization, and every total is below $2^{16}$, so each event has $r \cdot p_j \ge 2^{14}$, where $r$ is the width before the event. The new width is $\lfloor r \cdot hi / total \rfloor - \lfloor r \cdot lo / total \rfloor \ge r p_j - 1 \ge r p_j (1 - 2^{-14})$. Each renormalization step doubles the width and adds one output bit, written or pending, and the width stays at most $2^{32}$. So the number $s$ of these steps satisfies $2^{32} \prod_j p_j (1 - 2^{-14}) \cdot 2^s \le 2^{32}$, which gives the first two terms. The final step writes the pending bits and 2 more bits. $\square$

The sum $\sum_j \lg(1/p_j)$ is the ideal length that the function `ideal_length` of the implementation computes, and $\lg \frac{1}{1 - 2^{-14}} < 10^{-4}$.

**Termination.** For each symbol, the loop at L3 runs at most $k + 1$ times, since $o$ falls by one at each pass. Each renormalization loop ends, because each pass doubles the width and the width is at least 2. So encoding and decoding end after a number of steps linear in $n$ times the work per context. $\blacksquare$
