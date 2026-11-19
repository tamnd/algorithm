---
title: The first group of diverse beam search is a plain beam search
proves: [correctness]
status: full
---

We use the notation of the page. The model gives $\log p(w \mid y)$ for every prefix $y$ and token $w$; the score of a candidate $y w$ built from a beam entry $(y, s)$ is $s + \log p(w \mid y)$. All logs are natural logs. Candidates with score $-\infty$ are never formed (line L5).

Define BEAM-SEARCH$(B')$ as the following procedure, with the same conventions as the code. It starts with the beam {empty prefix, score 0}. At each step $t \le N$ it forms the candidates $y w$ for every entry $(y, s)$ of the beam, in the order of the beam and then of the vocabulary, with score $s + \log p(w \mid y)$. It keeps the $B'$ candidates of largest score, ties broken by the order of generation. The kept candidates that end with "</s>" go to the finished list, and the others form the next beam. It stops after step $N$ or when the beam is empty.

**Theorem 1 (the first group).** For every model, $N$, $G$, $B'$ and $\lambda$, the beams of group 1 of DIVERSE-BEAM-SEARCH at every step, and the outputs it finishes, are those of BEAM-SEARCH$(B')$.

*Proof.* By induction on $t$, we show that $\text{beam}_1$ after step $t$ equals the beam of BEAM-SEARCH$(B')$ after step $t$, in the same order, and that the two procedures finish the same outputs with the same scores at step $t$. Before step 1 both beams hold only the empty prefix with score 0 (line L1).

At step $t$, line L3 sets `used` to the empty count, and group 1 runs first in the loop of line L4. So when group 1 forms its candidates at line L6, `used[w]` $= 0$ for every $w$, and the rank of each candidate equals its score. By the induction hypothesis, the beam entries are the same and in the same order, so lines L5 and L6 generate the same candidates in the same order with the same scores as BEAM-SEARCH$(B')$. Line L7 keeps the $B'$ candidates of largest rank with ties broken by the order of generation, which is the same choice. Line L9 then splits the kept candidates in the same way into finished outputs and the next beam. Line L8 changes only `used`, which group 1 does not read again in this step. $\square$

**Corollary 2.** The list returned by diverse beam search contains every output finished by BEAM-SEARCH$(B')$, with its true score. In particular it contains the best output of BEAM-SEARCH$(B')$.

*Proof.* Line L9 adds every finished output of group 1 to $F$ with its score $s$, which is the sum of the true log probabilities of its tokens, not the rank. Line L10 only sorts $F$. $\square$

**Theorem 3 (no penalty).** If $\lambda = 0$, every group has the same beams at every step as group 1. So every output of $F$ appears $G$ times.

*Proof.* With $\lambda = 0$, the rank of a candidate equals its score whatever `used` holds. All groups start from the same beam (line L1). By induction on $t$, if all groups have the same beam before step $t$, then each group generates the same candidates in the same order with the same ranks, and line L7 keeps the same ones. $\square$

**Lemma 4 (the effect of the penalty).** Fix a step $t$ and a group $g$, and let $u = y w$ and $u' = y' w'$ be two candidates of group $g$ with scores $s_u$ and $s_{u'}$. Suppose that at the time group $g$ ranks them, `used`$[w] = c$ and `used`$[w'] = 0$. If $\lambda c > s_u - s_{u'}$, then $u'$ has the larger rank, so group $g$ cannot keep $u$ and drop $u'$ unless $B'$ other candidates rank above $u'$.

*Proof.* The ranks are $r_u = s_u - \lambda c$ and $r_{u'} = s_{u'}$, and $r_{u'} - r_u = \lambda c - (s_u - s_{u'}) > 0$. Line L7 keeps the $B'$ largest ranks. $\square$

**What is not claimed.** Diverse beam search is not exact. On the model M1 of the page with $G = 2$, $B' = 1$ and $\lambda = 0.2$, both groups return aa</s> (probability 0.2), while the output b</s> has probability 0.36. At the first step group 2 ranks a at $\ln 0.5 - 0.2 = -0.893$ and b at $\ln 0.4 = -0.916$, and keeps a. By Lemma 4 it switches to b exactly when $0.2$ is replaced by a value larger than $\ln 0.5 - \ln 0.4 = 0.2231$. Neither the mode nor any distance between the outputs is guaranteed in general. If $B'$ is at least the number of prefixes of positive probability, then by Theorem 1 the first group keeps every prefix, and its finished list contains every output of at most $N$ tokens, so the best output of the list is the mode. $\square$
