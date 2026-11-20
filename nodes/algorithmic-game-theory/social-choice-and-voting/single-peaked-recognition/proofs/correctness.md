---
title: The outside-in algorithm returns an axis exactly when the profile is single-peaked
proves: [correctness]
status: full
---

The proof follows the structure of Elkind, Lackner and Peters (survey, Theorem 4.2), with the free choices of the code fixed and with the case analysis of the second claim done in full. Let $P = (\succ_1, \ldots, \succ_n)$ be a profile of strict rankings of $A$, $|A| = m$, $n \ge 1$. We use the no-valley form of single-peakedness: a ranking $\succ$ is single-peaked on an axis $\lhd$ if and only if there are no $a \lhd b \lhd c$ with $a \succ b$ and $c \succ b$. Such a triple is a valley at $b$.

**Notation.** In a round, $R$ is the set of unplaced candidates, $B$ is the set of candidates that some voter ranks last in $R$ (line L4), and $N_x$ is the set of voters who do not rank $x$ first in $R$. In the second stage, when the right list is not empty, $\ell$ is the innermost candidate on the left and $r$ the innermost on the right (line L9), and lines L10 and L11 compute

$$L = \{x \in B : \exists i \in N_x,\ r \succ_i x \succ_i \ell\}, \qquad R' = \{x \in B : \exists i \in N_x,\ \ell \succ_i x \succ_i r\}.$$

Elements of $L$ go next to $\ell$ and elements of $R'$ next to $r$. Line L13 puts each free element of $B$ on a side that is still free, the left first.

**Facts about rounds.**

1. Each round puts at most one candidate at the inner end of each list, so the placed candidates are a prefix and a suffix of the final axis and $R$ is the gap between them. Line L16 joins left, gap and right.
2. If $|B| = 1$, its element is a unanimous bottom: every voter ranks it last in $R$.
3. If $|B| = 2$, its two elements go to opposite sides: by line L7 in the first stage, and in the second stage because line L12 rejects $|L| \ge 2$, $|R'| \ge 2$ and $L \cap R' \ne \emptyset$.
4. Every candidate placed in a round is ranked last in that round's $R$ by some voter.

**Lemma 1.** In a round of the second stage, let $x \in R$. Every voter ranks $x$ above $\ell$ or above $r$.

*Proof.* If $\ell$ and $r$ were placed in the same round, then $B$ was $\{\ell, r\}$ in that round and every voter ranked one of them last in a set that contains $x$. If $r$ was placed in a later round than $\ell$, nothing was put on the left in that later round, because $\ell$ is still the innermost left candidate. So that round had $B = \{r\}$, a unanimous bottom, and every voter ranks $x$ above $r$. The case where $\ell$ was placed later is the mirror image. $\square$

## Claim 1: if the code returns an axis, every ranking is single-peaked on it

Suppose voter $i$ has a valley on the output axis. Then it has one on three adjacent candidates: if $a \lhd a' \lhd b$ with $a, b, c$ a valley at $b$, then either $a' \succ_i b$ and $a', b, c$ is a narrower valley, or $b \succ_i a'$ and $a, a', b$ is one. So let $a, b, c$ be adjacent on the axis, in this order, with $a \succ_i b$ and $c \succ_i b$. Look at the first round that places one of them.

- Two of them on the same side in one round is impossible by fact 1. Exactly $a$ and $c$ is impossible: $b$ would be in $R$, voter $i$ ranks it below both, so the voter's bottom in $R$ is a third element of $B$. Exactly $b$ is impossible, because $b$ lies strictly inside the gap.
- So the round places exactly one of $a$ and $c$; by the mirror image we may assume it is $a$. If $|B| = 1$ in that round, $a$ is a unanimous bottom of a set that contains $b$, which contradicts $a \succ_i b$. So $|B| = 2$ and all later rounds are in the second stage.
- Suppose $c$ is placed strictly before $b$. At that round $a$ is placed and $b, c$ are not, the gap is an interval, and $c$ is at its end, so the gap is $\{b, c\}$. Voter $i$ ranks $b$ last in it, so $b \in B$ and $b$ is placed in the same round as $c$, a contradiction.
- So $b$ is placed while $c$ is still in $R$, and it is put next to $a$, so $\ell = a$ in that round. By Lemma 1, voter $i$ ranks $b$ above $\ell = a$ or above $r$; the first is false, so $a \succ_i b \succ_i r$. Voter $i$ ranks $c \in R$ above $b$, so $i \in N_b$ and $b \in R'$. Since line L12 did not stop, $b \notin L$, and line L14 puts $b$ next to $r$, not next to $a$. This is a contradiction. $\square$

## Claim 2: if the code returns NONE, the profile is not single-peaked

**Lemma 2.** (a) If each of three candidates is ranked below the other two by some voter, $P$ is not single-peaked. (b) If there are candidates $a, b, c, d$ and voters $i, j$ with $\{a, d\} \succ_i b \succ_i c$ and $\{c, d\} \succ_j b \succ_j a$, then $P$ is not single-peaked.

*Proof.* (a) On any axis one of the three lies between the other two, and the voter who ranks it last has a valley there. (b) Restrict to $\{a, b, c, d\}$; this keeps single-peakedness. The top two candidates of a single-peaked ranking form an interval, so $\{a, d\}$ and $\{c, d\}$ are intervals, and the last candidates $c$ of $i$ and $a$ of $j$ are the two ends. So the axis is $a, \cdot, \cdot, c$ with $b$ and $d$ in the middle. If $b$ is next to $a$, then $\{a, d\}$ is not an interval; if $d$ is next to $a$, then $\{c, d\}$ is not one. $\square$

The code returns NONE only at line L5 or at line L12.

**Line L5.** Three elements of $B$ are each last in $R$ for some voter, which is Lemma 2(a).

**$|L| \ge 2$ at line L12.** Let $a, b \in L$ with voters $i \in N_a$, $r \succ_i a \succ_i \ell$, and $j \in N_b$, $r \succ_j b \succ_j \ell$. The candidate $r$ was placed in an earlier round, so by fact 4 some voter $t$ ranks $r$ below every candidate of $R$, in particular below $a$ and $b$. By Lemma 2(a) on $\{a, b, r\}$ it suffices to find a voter who ranks $a$ last in this triple and one who ranks $b$ last in it.

Voter $i$ ranks $a$ below $r$. If $b \succ_i a$, voter $i$ ranks $a$ last in the triple; if $a \succ_i b$, it ranks $b$ last. Voter $j$ in the same way ranks $b$ last if $a \succ_j b$ and $a$ last if $b \succ_j a$. If the two voters give different answers, we are done. Otherwise, by the symmetry between $(a, i)$ and $(b, j)$, assume both rank $b$ last, so $r \succ_i a \succ_i b$. Since $i \in N_a$, the top $x$ of voter $i$ in $R$ is not $a$, and it is not $b$, so $\{x, r\} \succ_i a \succ_i b$. Since $a \in B$, some voter $k$ ranks $a$ last in $R$, so $\{x, b\} \succ_k a$. If $r \succ_k a$, voter $k$ ranks $a$ last in the triple and we are done. If $a \succ_k r$, then $\{r, x\} \succ_i a \succ_i b$ and $\{b, x\} \succ_k a \succ_k r$, which is Lemma 2(b) with the candidates $r, a, b, x$ in the roles of $a, b, c, d$.

The case $|R'| \ge 2$ is the mirror image.

**$L \cap R' \ne \emptyset$ at line L12.** Let $a \in L \cap R'$, with voters $i, j \in N_a$, $r \succ_i a \succ_i \ell$ and $\ell \succ_j a \succ_j r$. We find $b \in R \setminus \{a\}$ that both voters rank above $a$. If $|B| = 1$, $a$ is a unanimous bottom, and any other $b \in R$ works ($|R| \ge 2$ in the loop). If $B = \{a, b\}$ and, say, $a \succ_i b$, then $i \in N_b$ and $r \succ_i b$, and by Lemma 1 also $b \succ_i \ell$, so $b \in L$ and $|L| = 2$; that case is done above. The same holds for $j$ with $R'$. So $b \succ_i a$ and $b \succ_j a$, and

$$\{r, b\} \succ_i a \succ_i \ell, \qquad \{\ell, b\} \succ_j a \succ_j r,$$

which is Lemma 2(b) with $r, a, \ell, b$ in the roles of $a, b, c, d$. $\square$

## Running time

Line L1 builds the table of positions in $O(mn)$ time. Each round places one or two candidates, so there are at most $m$ rounds. In a round, line L4 reads one bottom pointer per voter, lines L10 and L11 make at most $2n$ constant-time comparisons, and line L15 moves the pointers past placed candidates. Each pointer moves at most $m$ times in the whole run. The total is $O(mn)$ time and $O(mn)$ space.

The tests in `impl/python/test_single_peaked_recognition.py` compare the answer with a search over all $m!$ axes on every profile of up to 3 voters on 3 candidates and of 2 voters on 4 candidates, and on random profiles with up to 6 candidates, and they check every returned axis.
