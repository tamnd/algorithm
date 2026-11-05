---
title: Hopcroft's algorithm outputs the minimal DFA in O(σ n log n) time
proves: [correctness, termination, complexity]
status: full
---

Let $M = (Q, \Sigma, \delta, q_0, F)$ be a complete DFA, and let $R$ be the set of states reachable from $q_0$, computed by line L1. All sets below are subsets of $R$, and $\delta(q, a) \in R$ for $q \in R$. For $S \subseteq R$ and $a \in \Sigma$ let $\delta_a^{-1}(S) = \{ q \in R : \delta(q, a) \in S \}$; line L7 computes $X = \delta_a^{-1}(S)$ from the lists $\mathrm{pre}_a$ of line L2. States $p, q$ are *equivalent*, $p \sim q$, if $\delta^*(p, z) \in F \Leftrightarrow \delta^*(q, z) \in F$ for all $z \in \Sigma^*$.

The work list $W$ holds pairs (block, symbol). A block is a set that can change when it is split; a pair in $W$ always refers to the current contents of its block, and line L11 keeps this true by putting both halves of a split block into $W$.

## Part 1: no two equivalent states are separated

**Invariant (I1).** Every block of $P$ is a union of classes of $\sim$.

*Proof.* Initially the blocks are $F \cap R$ and $R \setminus F$, and equivalent states agree on $z = \varepsilon$. Suppose (I1) holds, and line L9 splits a block $B$ by $X = \delta_a^{-1}(S)$, where $S$ is a block and so a union of classes. If $p \sim q$, then $\delta(p, a) \sim \delta(q, a)$, because a word $z$ that separated $\delta(p, a)$ from $\delta(q, a)$ would make $az$ separate $p$ from $q$. So $\delta(p, a)$ and $\delta(q, a)$ are both in $S$ or both outside it, and $p, q$ are both in $X$ or both outside it. Hence $B \cap X$ and $B \setminus X$ are unions of classes. $\square$

## Part 2: termination

Each split increases the number of blocks by one, and there are never more than $|R|$ blocks, so there are at most $|R| - 1$ splits. Each split adds at most $\sigma$ pairs to $W$ (line L11 adds one pair for $c$ if $(B, c) \in W$, and line L12 adds one pair otherwise). Line L4 adds at most $\sigma$ pairs. Each pass of the loop removes one pair. So the loop runs at most $\sigma |R|$ times and stops.

## Part 3: the final partition is stable

Say that $P$ is *$a$-stable for* a set $S$ if every block $B$ of $P$ satisfies $B \subseteq \delta_a^{-1}(S)$ or $B \cap \delta_a^{-1}(S) = \emptyset$. Three facts follow from the definition:

- **(F1)** $P$ is $a$-stable for $R$, since $\delta_a^{-1}(R) = R$.
- **(F2)** If $P$ is $a$-stable for $S$, then every refinement of $P$ is $a$-stable for $S$, since each new block lies inside an old one.
- **(F3)** If $P$ is $a$-stable for $S$ and for $T$, then it is $a$-stable for $S \cup T$, $S \cap T$ and $S \setminus T$, since $\delta_a^{-1}$ commutes with union, intersection and difference, and a block that lies inside or outside each of two sets lies inside or outside each of these combinations.

For a symbol $c$, let $\mathcal{S}_c$ be the family of the sets for which the current $P$ is $c$-stable, and $\mathcal{W}_c$ the family of the blocks $C$ with $(C, c) \in W$. Let $\mathcal{B}_c$ be the closure of $\{R\} \cup \mathcal{S}_c \cup \mathcal{W}_c$ under union, intersection and difference.

**Invariant (I2).** Before each test of line L5, for every symbol $c$, every block of $P$ is in $\mathcal{B}_c$.

*Proof.* *Start.* If $P$ has one block, it is $R$. If $P = \{S, R \setminus S\}$ with $S$ the smaller block, line L4 puts $(S, c)$ in $W$ for each $c$, so $S \in \mathcal{W}_c$ and $R \setminus S$ is a difference of $R$ and $S$.

*One pass.* Let $(S, a)$ be removed by line L6, and let $P'$ and $W'$ be the partition and the work list after the pass. We check the three kinds of generators of the old $\mathcal{B}_c$ and show that each of them is in the new family $\mathcal{B}'_c$:

- $R$ is a generator of both.
- A set in $\mathcal{S}_c$ is in $\mathcal{S}'_c$ by (F2), since $P'$ refines $P$.
- A block $C \in \mathcal{W}_c$ with $(C, c) \neq (S, a)$: if $C$ is not split, it is still in $\mathcal{W}'_c$. If $C$ is split into $C_1$ and $C_2$, line L11 puts both halves into $W$ for $c$, so $C = C_1 \cup C_2$ is in $\mathcal{B}'_c$.
- The removed pair $(S, a)$: after the pass, every block $B$ of $P'$ lies inside $X = \delta_a^{-1}(S)$ or outside it. A block that line L8 did not split already did; a split block becomes $B \cap X$ and $B \setminus X$. Here $X$ and $S$ are the sets of the moment line L7 ran, so the set $S$ is in $\mathcal{S}'_a$, even if the block $S$ was split later in the pass.

So the old $\mathcal{B}_c$ is contained in $\mathcal{B}'_c$. Now take a block $B'$ of $P'$. If it is a block of $P$, it is in $\mathcal{B}_c \subseteq \mathcal{B}'_c$. Otherwise it is a half of a block $B$ of $P$ that was split into $B_1$ and $B_2$. If $(B, c)$ was in $W$ when the split happened, line L11 put both halves into $W$, so $B' \in \mathcal{W}'_c$ unless it was split again, which cannot happen in the same pass because each half lies inside or outside $X$. Otherwise line L12 put the smaller half, say $B_1$, into $W$, so $B_1 \in \mathcal{W}'_c$, and $B_2 = B \setminus B_1$ with $B \in \mathcal{B}_c \subseteq \mathcal{B}'_c$. In both cases $B' \in \mathcal{B}'_c$. $\square$

When the loop stops, $W = \emptyset$, so $\mathcal{W}_c = \emptyset$ and every block is in the closure of $\{R\} \cup \mathcal{S}_c$. By (F1) and (F3), $P$ is $c$-stable for every set in this closure. So $P$ is $c$-stable for every block, for every symbol $c$: if $p, q$ are in one block, then $\delta(p, c)$ and $\delta(q, c)$ are in one block.

## Part 4: the output is the minimal DFA

**Lemma.** At the end, states in one block are equivalent.

*Proof.* We show by induction on $|z|$ that for $p, q$ in one block, $\delta^*(p, z)$ and $\delta^*(q, z)$ are in one block. For $z = \varepsilon$ this is the assumption. For $z = c z'$, $\delta(p, c)$ and $\delta(q, c)$ are in one block by Part 3, and the induction hypothesis applies to them and $z'$. Each block lies inside $F$ or inside $R \setminus F$, because the first partition did and blocks only split. So $\delta^*(p, z) \in F \Leftrightarrow \delta^*(q, z) \in F$. $\square$

With (I1), the blocks are exactly the classes of $\sim$ on $R$. Line L13 builds the quotient: its transition $[q] \xrightarrow{a} [\delta(q, a)]$ is well defined by Part 3, a block is accepting when it lies in $F$, and by induction on $|w|$ the quotient reaches the block of $\delta^*(q_0, w)$ on $w$, so it accepts $L(M)$. Its states are all reachable and pairwise inequivalent, so it is the minimal DFA by Part 3 of the [uniqueness of the minimal DFA](/minimal-dfa-uniqueness/).

## Part 5: the running time

Lines L1 and L2 take $O(\sigma n)$ time. Line L13 takes $O(\sigma n)$ time. A pass of the loop that removes $(S, a)$ costs $O(1 + |X| + \sigma \cdot s)$, where $|X| = \sum_{r \in S} |\mathrm{pre}_a(r)|$ and $s$ is the number of splits in the pass. The splits take $O(|X|)$ time in total if each split moves the states of $B \cap X$, which line L7 has already listed, into a new block, and the work-list updates take $O(\sigma)$ per split. Over the whole run there are at most $n - 1$ splits and at most $\sigma n$ passes, so these terms are $O(\sigma n)$. It remains to bound $\sum |X|$ over all passes.

**Claim.** For each state $r$ and symbol $a$, at most $\lfloor \log_2 n \rfloor + 1$ removed pairs $(S, a)$ have $r \in S$.

*Proof.* Let $(S, a)$ and later $(S', a)$ be two consecutive removed pairs with $r$ in the set. We show $|S'| \le |S|/2$, with the sizes at the moments of removal. When $(S, a)$ is removed, the block $S$ of $r$ has no pair with $a$ in $W$. From then on, let $B_t$ be the block of $r$ at time $t$; it only shrinks. Consider the first moment after this when a pair $(C, a)$ with $r \in C$ enters $W$. It cannot come from line L11, which adds a pair for the half of $r$ only when a pair for the block of $r$ and the symbol $a$ is already in $W$. So it comes from line L12, as the smaller half of a split block $B_t$, and $|C| \le |B_t|/2 \le |S|/2$. From then until $(S', a)$ is removed, the set of the pair that contains $r$ can only shrink, by later splits with line L11. So $|S'| \le |S|/2$. Also, line L4 and line L12 never add a pair that is already in $W$, so the pairs in $W$ are distinct. All sets are non-empty and have at most $n$ states, so there are at most $\lfloor \log_2 n \rfloor + 1$ such pairs. $\square$

Hence

$$\sum_{\text{passes}} |X| = \sum_{(S, a) \text{ removed}} \ \sum_{r \in S} |\mathrm{pre}_a(r)| \le (\lfloor \log_2 n \rfloor + 1) \sum_{a \in \Sigma} \sum_{r \in R} |\mathrm{pre}_a(r)| \le (\lfloor \log_2 n \rfloor + 1)\, \sigma n,$$

since $\sum_r |\mathrm{pre}_a(r)| = |R| \le n$ for each $a$. The total time is $O(\sigma n \log n)$, and the space is $O(\sigma n)$ for the lists $\mathrm{pre}_a$, the blocks and the work list. $\blacksquare$
