---
title: Without pruning, token passing finds the best path through the network
proves: [correctness]
status: full
---

We use the notation of the page. A *full path* for $n$ frames is a sequence of word arcs $a_1, \ldots, a_K$ with $K \ge 1$ that starts at the start node, in which each arc starts where the previous one ends and the last one ends at a final node, together with a segmentation that gives each phone of the words of $a_1, \ldots, a_K$ in order at least one frame, $n$ frames in all. Its score $S$ is the sum of the emission scores of the frames, $(d - 1)\ell + f$ for each phone that occupies $d$ frames, $\lambda g(a_k) + \log ip$ for each arc, and $\lambda \cdot \text{final}(q)$ for the last node $q$.

For frame $t$, write $\mathrm{tok}_t(a, j)$ for the token of state $j$ of arc $a$ after lines L3 and L4, and $\mathrm{node}_t(q)$ for the token of node $q$ after line L6. Before frame 0, $\mathrm{node}_{-1}$ holds only the start node with score 0 (line L1).

**Lemma 1 (tokens are best partial scores).** With no pruning, for every $t$:

1. $\mathrm{tok}_t(a, j)$ is the best partial score of a prefix of a full path that is in state $j$ of arc $a$ at frame $t$;
2. $\mathrm{node}_t(q)$ is the best partial score of a prefix that has left a word into node $q$ at the end of frame $t$, exit $f$ included.

A partial score counts the emissions of frames $0, \ldots, t$, the transitions between them, and $\lambda g + \log ip$ of every arc entered so far. A token is absent when no prefix exists.

*Proof.* Induction on $t$. A prefix in state $j$ of arc $a$ at frame $t$ came from one of three places: state $j$ of $a$ at frame $t - 1$ (self loop $\ell$), state $j - 1$ of $a$ at frame $t - 1$ (forward move $f$), or, when $j = 0$, the source node of $a$ at the end of frame $t - 1$, entering $a$ with $\lambda g(a) + \log ip$. In each case the added score, the transition plus $e_t(j)$, depends only on where the prefix was at $t - 1$. So the best prefix extends the best prefix of one of these places, which by induction (or by line L1 at $t = 0$) are $\mathrm{tok}_{t-1}(a, j)$, $\mathrm{tok}_{t-1}(a, j - 1)$ and $\mathrm{node}_{t-1}(\mathrm{src}(a))$. Line L3 takes the best of the three and adds $e_t(j)$, which proves claim 1.

A prefix that leaves a word into $q$ at the end of frame $t$ is in the last state of some arc $a$ into $q$ at frame $t$ and adds $f$. Line L6 takes the best of $\mathrm{tok}_t(a, \text{last}) + f$ over these arcs, which proves claim 2. $\square$

**Theorem (exact without pruning).** With an infinite beam, token passing returns a full path with the best score $S^*$.

*Proof.* A full path leaves its last word into a final node $q$ at the end of frame $n - 1$, and its score is its partial score there plus $\lambda \cdot \text{final}(q)$. By Lemma 1, line L7 computes $\max_q \mathrm{node}_{n-1}(q) + \lambda \cdot \text{final}(q) = S^*$. Each token carries the index of the word link record of the word it left last, and line L6 writes a new record with the previous index, so the traceback reads the words and end frames of a path with this score. $\square$

**Corollary (same best path as time-synchronous beam search).** Build the network of a bigram: one node per word history ($\langle s \rangle$ and each word), an arc $v \to w$ for word $w$ with $g = \log p(w \mid v)$, and final scores $\log p(\langle /s \rangle \mid w)$. Then a full path of the network is a word sequence with a segmentation, and its score $S$ equals the score that time-synchronous beam search gives the same sequence and segmentation: the two add the same terms, token passing adds $\lambda g + \log ip$ when a word starts and beam search when it ends. Both searches return the maximum of the same function over the same set, so with no pruning they return the same best score, and the same path when it is unique.

**Proposition (pruning).** With a finite beam, line L4 removes tokens and never changes the score of a kept one, so the returned score is the score of a real full path and at most $S^*$. The two-word example of the page, with a beam of 0.5, returns a path that is 3 worse than the best.
