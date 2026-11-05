---
title: Shearsort sorts into snake order
proves: [correctness]
status: full
---

## Reduction to zeros and ones

Each sort on lines L3, L5 and L6 is an odd-even transposition sort on one row or column. So shearsort is a fixed sequence of compare-exchanges $[u : v]$, each of which puts the smaller of the keys at processors $u$ and $v$ on $u$ and the larger on $v$. In a row sorted to the left, $u$ is the right one of the two neighbours. Such a step commutes with every non-decreasing map $f$ on keys: applying $f$ and then the step gives $\min(f(a), f(b)) = f(\min(a, b))$ on $u$ and the same for the maximum on $v$. By induction over the steps, shearsort commutes with $f$. So the argument of the [zero-one principle](/zero-one-principle/) applies: if shearsort leaves some input unsorted in snake order, with keys $a < b$ at snake positions in the wrong order, then the 0-1 input $f(x) = [x \ge b]$ is also left unsorted. It is therefore enough to prove that shearsort sorts every $r \times c$ matrix of zeros and ones.

From now on the keys are zeros and ones. A row is *clean* if all its keys are equal and *dirty* otherwise. Odd-even transposition sorts each line, as shown on its page, so after line L3 each even row is $0 \cdots 0 1 \cdots 1$ and each odd row is $1 \cdots 1 0 \cdots 0$.

## Lemma 1. Two rows in opposite directions

Let row $u$ be sorted increasing to the right, with $a$ zeros, and let row $v$ be sorted increasing to the left, with $b$ zeros, or the other way round. Put the minimum of each column of the two rows in one row and the maximum in the other. Then the row of minima is all zeros or the row of maxima is all ones.

*Proof.* The zeros of one row are in the columns $0, \ldots, a-1$ and the zeros of the other are in the columns $c - b, \ldots, c - 1$. If $a + b \ge c$, these two sets cover all $c$ columns, so each column has a zero and the row of minima is all zeros. If $a + b < c$, each column has a one in at least one of the two rows, and the row of maxima is all ones. $\square$

## Lemma 2. Sorting a column depends only on its number of zeros

*Proof.* A sorted 0-1 column with $z$ zeros has zeros in its top $z$ cells and ones below. A compare-exchange inside the column does not change $z$. $\square$

## Lemma 3. One phase halves the dirty rows

Suppose that before a phase, rows $0, \ldots, A - 1$ are all zeros, rows $r - B, \ldots, r - 1$ are all ones, and the $D = r - A - B$ rows between them are arbitrary. After lines L3 to L5 of the phase, the same holds with some $A' \ge A$, $B' \ge B$ and $D' = r - A' - B' \le \lceil D/2 \rceil$.

*Proof.* Line L3 keeps clean rows clean and sorts every row in its direction. Pair the middle rows as $(A, A+1), (A+2, A+3), \ldots$, which gives $\lfloor D/2 \rfloor$ pairs of neighbouring rows. Neighbouring rows have opposite directions. Apply, in a thought experiment, a compare-exchange to each column of each pair, minimum to the upper row. By Lemma 1, each pair now has a row of zeros or a row of ones. Call the result $M'$. In $M'$ there are at least $A + B + \lfloor D/2 \rfloor$ clean rows, some all zeros and some all ones. Let $Z$ be the number of rows of $M'$ that are all zeros and $O$ the number that are all ones, so $Z + O \ge A + B + \lfloor D/2 \rfloor$, $Z \ge A$ and $O \ge B$.

The thought experiment only exchanges keys inside columns, so by Lemma 2 sorting the columns of $M'$ gives the same matrix as line L5 applied to the matrix after line L3. In $M'$, each column has at least $Z$ zeros and at least $O$ ones. So after the column sort, the top $Z$ rows are all zeros and the bottom $O$ rows are all ones. This gives the claim with $A' = Z$, $B' = O$ and $D' \le D - \lfloor D/2 \rfloor = \lceil D/2 \rceil$. $\square$

## Theorem. Shearsort sorts every r × c matrix into snake order

*Proof.* By the reduction, take a 0-1 matrix. Before the first phase, the hypothesis of Lemma 3 holds with $A = B = 0$ and $D = r$. By Lemma 3 and induction, after $k$ phases it holds with $D \le \lceil r / 2^k \rceil$, so after $\lceil \lg r \rceil$ phases $D \le 1$. Line L6 sorts every row in its direction, keeps the top $A$ rows all zeros and the bottom $B$ rows all ones, and sorts the one middle row, if there is one, in its direction. Read in snake order, the matrix is now a run of zeros followed by a run of ones, which is sorted. $\square$

## Step count

Line L3 and line L6 take $c$ steps each, and line L5 takes $r$ steps, by the bound for odd-even transposition sort. So the step count is $\lceil \lg r \rceil (r + c) + c$. For $r = c = \sqrt{n} = 2^k$, this is $k \cdot 2^{k+1} + 2^k = 2^k (2k + 1) = \sqrt{n}(\lg n + 1)$.
