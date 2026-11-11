---
title: Re-Pair returns a grammar for its input, with no repeated pair left
proves: [correctness]
status: full
---

We write $s$ for the sequence held in the linked list, and $R$ for the list of rules made so far. For a pair $(x, y)$ define its **frequency** $N_s(x, y)$:

- if $x \ne y$, the number of positions $i$ with $s_i = x$ and $s_{i+1} = y$;
- if $x = y$, the sum of $\lfloor L/2 \rfloor$ over the maximal runs of $x$ in $s$, where $L$ is the length of the run.

**Lemma 1 (non-overlapping count).** $N_s(x, y)$ is the largest number of occurrences of $xy$ in $s$ that pairwise do not overlap, and the scan from left to right that replaces each occurrence it meets replaces exactly that many.

*Proof.* If $x \ne y$, two occurrences of $xy$ cannot share a position, because a shared position would hold both $x$ and $y$. So all occurrences are disjoint, and the scan replaces all of them. If $x = y$, an occurrence of $xx$ lies inside one maximal run of $x$. A run of length $L$ holds at most $\lfloor L/2 \rfloor$ disjoint occurrences, because each one uses 2 of its $L$ positions, and the scan takes positions $(1, 2), (3, 4), \ldots$ of the run, which is $\lfloor L/2 \rfloor$ of them. $\square$

**The invariant (I).** Each time the test of line L5 runs:

1. $\mathrm{expand}(R, s) = w$, where expand replaces each nonterminal by the right-hand side of its rule until only terminals remain.
2. For each pair with $N_s(x, y) \ge 1$, $\mathit{cnt}[x, y] = N_s(x, y)$, and no other pair has an entry in $\mathit{cnt}$.
3. For $x \ne y$, $\mathit{occ}[x, y]$ is the set of nodes $i$ such that node $i$ holds $x$ and the next node holds $y$. For $x = x$, $\mathit{occ}[x, x]$ is the set of first nodes of the maximal runs of $x$ of length at least 2, and the run tables give the last node and the length of each such run.
4. For each pair with $N_s(x, y) \ge 2$, the queue $Q$ holds the entry $(-N_s(x, y), x, y)$. Other entries of $Q$ may exist; we call an entry *stale* if its count is not the current $\mathit{cnt}$ of its pair.

*Initialization.* Line L1 makes $s = w$ and $R$ is empty, so part 1 holds. Line L2 scans $s$ once: it finds each maximal run, records it if its length $L \ge 2$ and adds $\lfloor L/2 \rfloor$ to the count of $(x, x)$, and it records the pair at the end of each run, which joins two different symbols. This is parts 2 and 3. Line L3 puts each pair with count at least 2 in $Q$, which is part 4.

*Line L6 picks the right pair.* Line L6 removes entries from $Q$ until it finds one that is not stale. By part 4, each pair with $N_s \ge 2$ has a current entry in $Q$, so the first current entry removed is the least key $(-N_s(x, y), x, y)$ over all pairs: the pair of largest frequency, and the smallest such pair on a tie. A stale entry is never used. Each entry is removed at most once, so this costs nothing beyond the pushes counted in the cost analysis.

*One replacement keeps (I), case $a \ne b$.* Let $(a, b)$ be the chosen pair and $A$ the new symbol. Its entry in $\mathit{cnt}$ and $\mathit{occ}$ is removed first, since every occurrence will be replaced. The occurrences are disjoint (Lemma 1), and replacing one changes only its own two nodes, so every node in the sorted list of occurrences still starts an occurrence when line L7 reaches it. Consider the occurrence at node $i$, with left neighbour $p$ and right neighbour $q$. The change is $p\,a\,b\,q \to p\,A\,q$. The pairs that change are $(p, a)$ and $(b, q)$, which disappear, and $(p, A)$ and $(A, q)$, which appear; the pair $(a, b)$ is already removed.

- Line L8 removes $(p, a)$. If $p$ holds $a$, then node $i$ is the last node of a maximal run of $a$ (it is followed by $b \ne a$). The run loses its last node, so its contribution falls from $\lfloor L/2 \rfloor$ to $\lfloor (L-1)/2 \rfloor$, and the run is kept only if $L - 1 \ge 2$. This is the procedure run-lose-end. Otherwise $(p, a)$ has two different symbols and loses one position. The same argument, mirrored, holds for $(b, q)$ and run-lose-start.
- Line L9 writes $A$ in node $i$ and unlinks the node of $b$. This is the change $ab \to A$ of $s$.
- Line L10 adds $(p, A)$ and $(A, q)$. The node $q$ is right of $i$ and has not been changed yet, because the occurrences are processed from left to right, so $q$ does not hold $A$, and $(A, q)$ is a pair of two different symbols. The node $p$ holds $A$ exactly when the previous occurrence ended just before $i$. Then node $i$ extends the run of $A$ that ends at $p$ by one node, and the count of $(A, A)$ rises from $\lfloor L/2 \rfloor$ to $\lfloor (L+1)/2 \rfloor$. This is run-grow. Otherwise $(p, A)$ has two different symbols and gains one position.

Each change of a count pushes the new count to $Q$ when it is at least 2, so part 4 holds. After the last occurrence, line L11 adds the rule $A \to ab$. Each $A$ in $s$ now expands to $ab$, so part 1 holds.

*One replacement keeps (I), case $a = b$.* Now $\mathit{occ}[a, a]$ holds the first node of each maximal run of $a$ of length $L \ge 2$. For each run, with left neighbour $p$ and right neighbour $q$, neither holds $a$ because the run is maximal. Line L8 removes the pairs $(p, a)$ and $(a, q)$, each of two different symbols. Lines L9 and L10 turn the run into $A^{\lfloor L/2 \rfloor}$ followed by one $a$ when $L$ is odd, which is the left to right scan of Lemma 1. The new nodes $A$ form one run, recorded by run-grow. The pairs at the borders are $(p, A)$, then $(A, a)$ and $(a, q)$ when $L$ is odd, or $(A, q)$ when $L$ is even. Each has two different symbols, because $A$ is new and $p, q \ne a$. The node $p$ does not hold $A$: two maximal runs of $a$ are separated by at least one other symbol, which line L9 does not change. So the counts are correct, and part 1 holds after line L11 as before.

**Theorem.** RE-PAIR stops. On return, $\mathrm{expand}(R, s) = w$, every rule has the form $A \to xy$, and no pair has frequency 2 or more in $s$. The output is the same as that of the plain method that, while some pair has frequency at least 2, recounts all pairs, takes the most frequent one (the smallest on a tie), and replaces it by a scan from left to right.

*Proof.* Each pass of line L5 either drops a stale entry or replaces a pair of frequency $c \ge 2$, which shortens $s$ by $c \ge 2$. So there are at most $n/2$ replacements. Each count change pushes at most one entry, and there are $O(n)$ count changes (see the cost analysis), so there are $O(n)$ stale entries and the loop ends. By (I), part 1 gives $\mathrm{expand}(R, s) = w$. When $Q$ is empty, part 4 says that no pair has $N_s \ge 2$, and by Lemma 1 no pair has two non-overlapping occurrences. Each step picks the same pair as the plain method (line L6 above) and makes the same replacement (Lemma 1), so by induction on the steps both methods produce the same rules and the same sequence. $\blacksquare$
