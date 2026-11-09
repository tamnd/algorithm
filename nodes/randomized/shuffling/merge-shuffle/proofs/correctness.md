---
title: The MergeShuffle merge keeps a uniform order
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. FLIP() is a fair bit, RANDOM$(a, b)$ is uniform on $\{a, \ldots, b\}$, and all calls are independent. For a finite set $S$ of items, a *uniform order* of $S$ is a random arrangement of $S$ in which each of the $|S|!$ arrangements has probability $1/|S|!$.

## Termination

In the loop of lines L6 to L12, each turn that does not exit increases $i$ by 1, and $i$ can reach $e$ only after both halves are empty, at which point the next flip exits. More precisely, each turn that does not exit takes one item, from the left (line L7 with $i < j$) or the right (line L11 with $j < e$), and there are $n_1 + n_2$ items. So the loop makes at most $n_1 + n_2 + 1$ flips. The loop of lines L13 and L14 runs $e - i$ times. MERGE-SHUFFLE recurses on sizes $\lfloor n/2 \rfloor$ and $\lceil n/2 \rceil$, which are smaller than $n$ for $n \ge 2$. So every call stops.

## Lemma 1: the loop invariant of MERGE

Let $L = (\ell_0, \ldots, \ell_{n_1 - 1})$ be the left half and $R = (r_0, \ldots, r_{n_2 - 1})$ the right half at the start of MERGE. Before each turn of the loop:

1. $T[s \ldots i-1]$ holds the items taken so far, in the order taken;
2. $T[j \ldots e-1] = (r_{b}, \ldots, r_{n_2-1})$, where $b = j - (s + n_1)$ is the number of right items taken;
3. $T[i \ldots j-1]$ holds the left items not yet taken, and the next left item to be taken is $T[i]$.

This holds at the start. A flip 0 with $i < j$ takes $T[i]$ and increases $i$: all three parts stay true. A flip 1 with $j < e$ swaps $T[i]$, a left item, with $T[j] = r_b$. Now $r_b$ is at position $i$ and is taken, and the left item moves to position $j$, the new end of the left block $T[i+1 \ldots j]$. Parts 1 to 3 stay true.

So the sequence of left items that are taken is a function $F_w(L)$ of the bit pattern $w$ and the left order $L$, and for a fixed $w$ this function only moves positions around: the left block acts as a queue, where a 0 takes the front item and a 1 moves the front item to the back.

## Lemma 2: the merged prefix is a uniform order

Assume that $L$ is a uniform order of the left set, $R$ is a uniform order of the right set, and $L$, $R$ and the flips are independent.

Suppose the loop takes $a$ left items and $b$ right items and then exits. Its flips are a word $w \in \{0, 1\}^{a+b}$ with $a$ zeros and $b$ ones, followed by the exit flip, which is 0 with $a = n_1$ or 1 with $b = n_2$. Call this triple $(a, b, \text{exit})$ the *stop state*. Every word with $a$ zeros and $b$ ones can occur before such an exit, because a flip can fail only when its half is empty, and that happens only after all $n_1$ zeros or all $n_2$ ones. Each word has probability $2^{-(a+b+1)}$. So, given the stop state, $w$ is uniform on the $\binom{a+b}{a}$ words, and it is independent of $L$ and $R$.

Given the stop state and $w$:

- The right items taken are $r_0, \ldots, r_{b-1}$, in this order. Since $R$ is uniform, this is a uniform ordered sample of $b$ items from the right set.
- For a fixed $w$, the map $L \mapsto$ (the $a$ items taken, in order, and the order of the rest of the queue) is a bijection, since each step of the queue is a fixed rearrangement. Since $L$ is uniform, the $a$ left items taken form a uniform ordered sample of $a$ items from the left set.

So, given the stop state and the two sets $P_L$ and $P_R$ of taken items, the left items in the prefix are a uniform order of $P_L$, the right items are a uniform order of $P_R$, and the word $w$ that interleaves them is uniform. These three are independent. An order of $P_L \cup P_R$ is the same as a triple (order of $P_L$, order of $P_R$, interleaving word), so there are $a! \, b! \binom{a+b}{a} = (a+b)!$ triples, all equally likely. So the prefix $T[s \ldots i-1]$ is a uniform order of its set $P = P_L \cup P_R$, given the stop state and the set. $\square$

## Lemma 3: the leftover step

**Lemma 3.** Let $T[s \ldots i-1]$ be a uniform order of its set $P$, and let $x = T[i]$, where $P$ and $x$ may be random but RANDOM$(s, i)$ is independent of them and of the order. After line L14, $T[s \ldots i]$ is a uniform order of $P \cup \{x\}$, given $P$ and $x$.

*Proof.* Let $k = i - s$. Line L14 picks $m$ uniform on $\{s, \ldots, i\}$ and swaps $T[i]$ and $T[m]$, which puts $x$ at position $m$ and the old $T[m]$ at position $i$. Each order $\pi$ of $P \cup \{x\}$ comes from exactly one pair (order of $P$, $m$): $m$ is the position of $x$ in $\pi$, and the order of $P$ is $\pi$ with the item at position $i$ moved back to position $m$ (and $\pi$ itself without $x$ if $m = i$). So $\Pr[\pi] = \frac{1}{k!} \cdot \frac{1}{k+1} = \frac{1}{(k+1)!}$. $\square$

## The theorem

**Theorem.** If the left and right halves are independent uniform orders of their sets, then after MERGE the block $T[s \ldots e-1]$ is a uniform order of all $n_1 + n_2$ items. So MERGE-SHUFFLE gives a uniform random permutation.

*Proof.* Given the stop state, Lemma 2 says that the prefix $T[s \ldots i-1]$ is a uniform order of its set. The items in $T[i \ldots e-1]$ are the leftover items. Lines L13 and L14 apply Lemma 3 once for each of them, with fresh calls of RANDOM. By induction on the number of leftover items, the whole block is a uniform order of all items, given the stop state. This holds for each stop state, so it holds without the condition.

For MERGE-SHUFFLE use induction on $n$. For $n \le 1$ there is one order. For $n \ge 2$, line L3 gives two uniform orders, by the induction hypothesis, and they are independent because they use different calls of FLIP and RANDOM. Then MERGE gives a uniform order of the block. $\blacksquare$

## The fair-coin merge without the stop rule

If the loop runs until one half is empty and the rest is appended, the output interleaving word is a word with $n_1$ zeros and $n_2$ ones whose probability is $2^{-k}$, where $k$ is the number of flips, that is, the position of the last flip before one half runs out. Words that end in a long run of one letter need fewer flips and are more likely. For $n_1 = 1$ and $n_2 = 2$ the words $011$ and $101$ have probability $\frac12$ and $\frac14$ and the word $110$ has $\frac14$, not $\frac13$ each. This is why the stop rule and the leftover step are needed.
