---
title: Without pruning, time-synchronous beam search finds the best path
proves: [correctness]
status: full
---

We use the notation of the page. A *full path* for $n$ frames is a word sequence $W = w_1 \cdots w_K$ with $K \ge 1$ and a segmentation that gives each phone of $w_1, \ldots, w_K$ in order at least one frame, $n$ frames in all. Its score $S$ is the sum of

- the emission score $e_t(\text{phone at } t)$ of every frame $t$;
- $(d - 1)\ell + f$ for each phone that occupies $d$ frames (the last phone of a word pays $f$ for the word exit);
- $\lambda \log p(w_k \mid w_{k-1}) + \log ip$ for each word, with $w_0 = \langle s \rangle$;
- $\lambda \log p(\langle /s \rangle \mid w_K)$.

The search returns the best full path, or nothing if no full path has a finite score. The tree lexicon gives each prefix of a pronunciation one node, so "phone $j$ of word $w$" is a node $q$ of the tree, and $w$ ends at $q$ when $j$ is its last phone.

**Lemma 1 (what a hypothesis means).** With no pruning, after line L1 (for $t = 0$) or line L9 (for $t \ge 1$), the hypothesis $(v, q)$ at frame $t$ has the score

$$H_t(v, q) = \max \text{ of the partial score of a prefix of a full path that has finished the words up to } v \text{ and is in node } q \text{ at frame } t,$$

where the partial score counts everything above that is fixed by frames $0, \ldots, t$: the emissions of these frames, the transitions between them, and the language model and penalty terms of the finished words. A key that no such prefix reaches is absent. Also, after line L5 at frame $t$,

$$E_t(w) = \max \text{ of the partial score of a prefix that ends word } w \text{ at frame } t, \text{ including its exit } f \text{ and its terms } \lambda \log p(w \mid \cdot) + \log ip.$$

*Proof.* Induction on $t$. At $t = 0$ the prefix has read one frame, has finished no word, and sits in a first phone $c$ of some word, a child of the root. Its score is $e_0(c)$, which is line L1.

Line L5 at frame $t$: a prefix that ends $w$ at $t$ is in the last node $q$ of $w$ at $t$, after some previous word $v$, and adds $f + \lambda \log p(w \mid v) + \log ip$. These additions depend only on $(v, q)$ and $w$, so the best such prefix extends the best prefix for $(v, q)$, which is $H_t(v, q)$. Line L5 takes the maximum over all $(v, q)$.

Lines L7 and L8 for frame $t + 1$: a prefix in node $q'$ at $t + 1$ after $v$ got there in one of three ways. It stayed in $q'$ (self loop $\ell$), it moved from the parent of $q'$ in the same word ($f$), or $q'$ is a first phone, and the prefix ended $v$ at frame $t$. In each case the added score, the transition plus $e_{t+1}(q')$, depends only on the key at frame $t$ (or the ended word $v$) and on $q'$. So the best prefix for $(v, q')$ extends the best prefix of one of these three kinds, which are $H_t(v, q')$, $H_t(v, \text{parent})$ and $E_t(v)$. Line L7 covers the first two and line L8 the third, and "relax" keeps the maximum. $\square$

**Theorem (exact without pruning).** With an infinite beam and no histogram limit, the search returns a full path with the best score $S^*$.

*Proof.* A full path ends its last word $w_K$ at frame $n - 1$. Its score is its partial score at the word end plus $\lambda \log p(\langle /s \rangle \mid w_K)$. By Lemma 1, the best partial score of a prefix that ends $w$ at frame $n - 1$ is $E_{n-1}(w)$, so line L10 computes $\max_w E_{n-1}(w) + \lambda \log p(\langle /s \rangle \mid w) = S^*$. The back pointers store, for each hypothesis and word end, the record of the word end it came from, so the traceback reads the words of a path that has this score. $\square$

**Why the key is enough.** The proof uses that the future of a prefix, all terms added after frame $t$, depends only on the key $(v, q)$. This holds for a bigram because the next language model term depends only on $v$. With a trigram the key would need two words, and keeping only $(v, q)$ would merge prefixes with different futures.

**Proposition (pruning).** With any beam or histogram limit, the returned score is the score of a full path, so it is at most $S^*$. It can be smaller.

*Proof.* Pruning removes entries from $H$ and never changes the score of a kept entry, so every score that the search computes is still the partial score of a real prefix, and the returned one is the score of a real full path. For the second claim, take the example of the page: words $AB = (a, b)$ and $CD = (c, d)$, all language model terms 0, $\ell = f = \ln 0.5$, and the emissions $e_0 = (a{:}{-1}, c{:}{-2})$, $e_1 = (b{:}{-5}, d{:}{-1})$, with all other emissions $-9$. The best full path is $CD$ with $-3 + 2 \ln 0.5$. A beam of 0.5 removes $(\langle s \rangle, c)$ at frame 0, since $-2 < -1 - 0.5$, and no other hypothesis can reach the end of $CD$ in two frames. The search returns $AB$ with $-6 + 2 \ln 0.5$. $\square$
