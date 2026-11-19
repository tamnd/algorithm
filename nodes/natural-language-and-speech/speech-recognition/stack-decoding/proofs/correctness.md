---
title: With an admissible, consistent heuristic, the stack decoder returns the best word sequence
proves: [correctness]
status: full
---

We use the notation of the page. There are $n$ frames. A *full path* is a word sequence $w_1 \cdots w_K$ with $K \ge 1$ and a segmentation of the frames $0, \ldots, n - 1$ into the phones of the words, at least one frame per phone. Its score is

$$S = \sum_{k=1}^{K} \big(\mathrm{seg}_k + \lambda \log p(w_k \mid w_{k-1}) + \log ip\big) + \lambda \log p(\langle /s \rangle \mid w_K),$$

with $w_0 = \langle s \rangle$, where $\mathrm{seg}_k$ is the emission and transition score of word $k$ in its frames, its exit move included. A partial hypothesis $(w_1 \cdots w_k, t)$ covers the frames $0, \ldots, t - 1$, and its score $g$ is the sum of the first $k$ terms. Let $S^*$ be the best score of a full path. We assume $\ell \le 0$, $f \le 0$, $\lambda \ge 0$ and log probabilities $\le 0$, and that there is no stack limit.

**Lemma 1 (the best segment).** For a word $w$ and frames $t \le u$, the value $\mathrm{seg}(w, t, u + 1)$ computed by the word Viterbi pass is the best score of $w$ occupying exactly the frames $t, \ldots, u$.

*Proof.* It is the Viterbi algorithm on the left-to-right chain of the phones of $w$, started in the first phone at frame $t$, read in the last phone at frame $u$, plus the exit $f$. $\square$

So the best full path is found by choosing, for each word, its best segmentation inside its frames: the search over words and end frames, with Lemma 1 for the inside, covers every full path at its best segmentation.

**Lemma 2 (admissible and consistent).** Let $h(t) = \sum_{u \ge t} \max_{\text{phone}} e_u(\text{phone}) + (n - t) \max(0, \log ip)$, and $h(n) = 0$. Then

1. for every extension of a partial hypothesis at $t$ by a word that covers frames $t, \ldots, t' - 1$, its added score $\Delta$ satisfies $\Delta + h(t') \le h(t)$;
2. the final term $\lambda \log p(\langle /s \rangle \mid w_K)$ is $\le 0 = h(n)$;
3. so every partial hypothesis at $t$ has $g + h(t) \ge$ the score of every full path that extends it.

*Proof.* The added score is $\mathrm{seg} + \lambda \log p(w \mid v) + \log ip$. The segment adds one emission per frame, each at most the maximum emission of its frame, and transitions that are $\le 0$. The language model term is $\le 0$, and $\log ip \le (t' - t) \max(0, \log ip)$ since $t' - t \ge 1$. Adding up gives claim 1. Claim 2 holds because log probabilities are $\le 0$. Claim 3 follows by adding claim 1 along the extensions up to $n$ and then claim 2. $\square$

**Lemma 3 (priorities do not grow).** If an entry with priority $P$ is popped, every entry that its expansion pushes has priority at most $P$. A complete entry has priority equal to its score.

*Proof.* A partial child has priority $g + \Delta + h(t') \le g + h(t) = P$ by Lemma 2.1. A complete child has priority $g + \Delta + \lambda \log p(\langle /s \rangle \mid w) \le g + \Delta = g + \Delta + h(n) \le P$ by Lemma 2.1 and 2.2. $\square$

**Lemma 4 (closing is safe).** The future of a partial hypothesis, the set of score sums its extensions can add, depends only on its last word and $t$. When the first entry with key (last word $v$, $t$) is popped, its $g$ is the best score of any partial hypothesis with that key.

*Proof.* The extensions depend on $t$ (which frames remain) and on $v$ (the next language model term), and on nothing else, so the first claim holds. For the second, suppose a hypothesis $x$ with the same key has a larger score $g_x$. Some prefix $y$ of $x$ is on the stack (or is $x$ itself): the root was on the stack, and the expansion of each popped prefix pushes the next one, unless its key was already closed, a case that the same argument handles by induction on the pop order. By Lemma 2.1 along the extensions from $y$ to $x$, the priority of $y$ is at least $g_x + h(t)$, which is larger than the priority $g + h(t)$ of the popped entry. That contradicts the choice of the popped entry as the largest. $\square$

**Theorem (optimality).** With $h$ as in Lemma 2 and no stack limit, the first complete entry that is popped has the score $S^*$.

*Proof.* Let $\pi^*$ be a best full path. Before the pop of a complete entry $c$, some prefix of $\pi^*$, or $\pi^*$ itself as a complete entry, is on the stack, or a prefix with the same key and a score at least as good (Lemma 4), which extends to a full path of score at least $S^*$. By Lemma 2.3 its priority is at least $S^*$. The popped entry has the largest priority, so the score of $c$, which is its priority, is at least $S^*$. It is the score of a full path, so it is at most $S^*$. $\square$

**Termination.** Each key (word, $t$) is expanded at most once, there are at most $V (n + 1) + 1$ keys, and each expansion pushes at most $V n$ entries, so the loop ends.

**Remark (when it fails).** The proof uses two assumptions, and the tests show what happens without them.

- *Stack limit.* Dropping entries can drop every prefix of $\pi^*$. In the example of the page, a stack of size 1 keeps the prefix $x$, whose priority is the largest after the first expansion, and drops the complete $z$; every extension of $x$ scores $-9 + 2 \ln 0.5$, worse than $S^* = -2 + 2 \ln 0.5$.
- *A heuristic below the true rest.* Lemma 2.3 fails, and a complete entry can be popped while a prefix of a better path waits with a lower priority. With $h(t) = -100 (n - t)$, the test returns a one-word sentence about 3.9 worse than the best two-word sentence.
