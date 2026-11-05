---
tag: B4DZNC
kind: theorem
slug: lcs-optimal-substructure
name: Optimal substructure of LCS
area: sequences/subsequence-problems
level: core
summary: The property that a longest common subsequence of two sequences contains a longest common subsequence of prefixes of those sequences.
prereqs: [longest-common-subsequence, optimal-substructure, cut-and-paste-argument]
see_also: [lcs-dynamic-programming, hirschberg-lcs, tabulation, traceback, overlapping-subproblems, edit-distance]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.4, Theorem 14.1 (Optimal substructure of an LCS)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 15.4, Theorem 15.1 (Optimal substructure of an LCS)
  - paper: "Robert A. Wagner and Michael J. Fischer, The string-to-string correction problem, Journal of the ACM 21(1), 1974, 168-173"
    locator: the recurrence for the cost of an edit sequence of prefixes, and its relation to the longest common subsequence
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11, the recurrence relations for edit distance and their proof
---

The optimal substructure theorem for the [longest common subsequence](/longest-common-subsequence/) says that each LCS of two sequences is made of an LCS of two prefixes, plus at most one item. Which prefixes depends only on the last items of the two sequences. The theorem gives the three-case recurrence on which the [LCS dynamic program](/lcs-dynamic-programming/) and all its faster variants rest. It is Theorem 14.1 of CLRS (fourth edition), and a standard example of the [optimal substructure](/optimal-substructure/) property.

## Statement

For a sequence $X = \langle x_1, \ldots, x_m \rangle$ and $0 \le i \le m$, write $X_i = \langle x_1, \ldots, x_i \rangle$ for its prefix of length $i$, so $X_0 = \varepsilon$.

**Theorem.** Let $X = \langle x_1, \ldots, x_m \rangle$ and $Y = \langle y_1, \ldots, y_n \rangle$ with $m, n \ge 1$, and let $Z = \langle z_1, \ldots, z_k \rangle$ be any LCS of $X$ and $Y$.

1. If $x_m = y_n$, then $k \ge 1$, $z_k = x_m = y_n$, and $Z_{k-1}$ is an LCS of $X_{m-1}$ and $Y_{n-1}$.
2. If $x_m \ne y_n$ and $z_k \ne x_m$ (or $k = 0$), then $Z$ is an LCS of $X_{m-1}$ and $Y$.
3. If $x_m \ne y_n$ and $z_k \ne y_n$ (or $k = 0$), then $Z$ is an LCS of $X$ and $Y_{n-1}$.

**Corollary (the recurrence).** Let $c[i, j] = \mathrm{lcs}(X_i, Y_j)$ for $0 \le i \le m$ and $0 \le j \le n$. Then

$$c[i, j] = \begin{cases} 0 & \text{if } i = 0 \text{ or } j = 0, \\ c[i-1, j-1] + 1 & \text{if } i, j \ge 1 \text{ and } x_i = y_j, \\ \max(c[i-1, j],\ c[i, j-1]) & \text{if } i, j \ge 1 \text{ and } x_i \ne y_j. \end{cases}$$

## In plain words

Look at the last item of each of the two sequences. If the two last items are the same, a best common part can end with them: match them, and solve the problem again for the two sequences without their last items. If the two last items differ, at least one of them is not used in a best common part, so you can drop it. You do not know which one, so you try both and keep the better result.

So the answer for two long sequences comes from the answers for shorter beginnings of them. There are only a few such beginnings, one for each pair of lengths, and this is what makes a table method fast.

## Proof

We use two facts about [subsequences](/subsequence/). (F1) If $W \preceq X_{m-1}$, then $W \preceq X$, and the same for $Y$. (F2) If $W \preceq X_{m-1}$, then $W x_m \preceq X$, where $W x_m$ is $W$ with $x_m$ appended, because the index $m$ is larger than all indices of an embedding of $W$ in $X_{m-1}$.

**Case 1.** Let $x_m = y_n$. First, $z_k = x_m$ and in particular $k \ge 1$. If not, then $Z x_m$ is a common subsequence of $X$ and $Y$: take embeddings of $Z$ in $X$ and in $Y$; if $k = 0$ they are empty, and if $k \ge 1$ the item $z_k \ne x_m$ is not at index $m$ of $X$, so the embedding of $Z$ in $X$ uses only indices below $m$, and likewise the embedding in $Y$ uses only indices below $n$ because $z_k \ne y_n$. Then by (F2), $Z x_m \preceq X$ and $Z y_n \preceq Y$. But $|Z x_m| = k + 1$, which contradicts the maximality of $Z$. So $z_k = x_m = y_n$.

Next, $Z_{k-1}$ is a common subsequence of $X_{m-1}$ and $Y_{n-1}$. Take an embedding $i_1 < \cdots < i_k$ of $Z$ in $X$. If $i_k < m$, change $i_k$ to $m$: the item is the same, since $x_{i_k} = z_k = x_m$, and the indices stay increasing. So we can assume $i_k = m$, and then $i_1, \ldots, i_{k-1} \le m - 1$ embed $Z_{k-1}$ in $X_{m-1}$. The same argument for $Y$ embeds $Z_{k-1}$ in $Y_{n-1}$.

Last, $Z_{k-1}$ is longest. Suppose that $W$ is a common subsequence of $X_{m-1}$ and $Y_{n-1}$ with $|W| > k - 1$. By (F2) for both sequences, $W x_m$ is a common subsequence of $X$ and $Y$ of length $|W| + 1 > k$. This contradicts the maximality of $Z$. This is the [cut-and-paste argument](/cut-and-paste-argument/).

**Case 2.** Let $x_m \ne y_n$ and let $z_k \ne x_m$, or $k = 0$. Take an embedding of $Z$ in $X$. If $k = 0$ it is empty. If $k \ge 1$, its last index is not $m$, because $x_m \ne z_k$. So the embedding uses only indices up to $m - 1$, and $Z \preceq X_{m-1}$. Also $Z \preceq Y$, so $Z$ is a common subsequence of $X_{m-1}$ and $Y$. If $W$ were a longer common subsequence of $X_{m-1}$ and $Y$, then by (F1) it would be a common subsequence of $X$ and $Y$ longer than $Z$, a contradiction. So $Z$ is an LCS of $X_{m-1}$ and $Y$.

**Case 3.** This is case 2 with the roles of $X$ and $Y$ exchanged. $\square$

**Proof of the corollary.** If $i = 0$ or $j = 0$, the only common subsequence is $\varepsilon$, so $c[i, j] = 0$. Let $i, j \ge 1$, and apply the theorem to $X_i$ and $Y_j$ with an LCS $Z$ of length $k = c[i, j]$.

- If $x_i = y_j$, part 1 gives $c[i-1, j-1] = k - 1$, so $c[i, j] = c[i-1, j-1] + 1$.
- If $x_i \ne y_j$, then $z_k$ cannot be equal to both $x_i$ and $y_j$ (or $k = 0$). So part 2 or part 3 applies, and $k = c[i-1, j]$ or $k = c[i, j-1]$. Hence $k \le \max(c[i-1, j], c[i, j-1])$. Conversely, by (F1) an LCS of $X_{i-1}$ and $Y_j$, and an LCS of $X_i$ and $Y_{j-1}$, are common subsequences of $X_i$ and $Y_j$, so $k \ge \max(c[i-1, j], c[i, j-1])$. $\blacksquare$

## Consequences

- **The LCS table.** The corollary defines $c[i, j]$ from three neighbours, $c[i-1, j-1]$, $c[i-1, j]$ and $c[i, j-1]$. So the $(m+1)(n+1)$ values can be filled row by row in $\Theta(mn)$ time. This is the [LCS dynamic programming](/lcs-dynamic-programming/) algorithm, an instance of [tabulation](/tabulation/).
- **Overlapping subproblems.** A plain recursion on the recurrence calls the same pair $(i, j)$ many times, and takes exponential time on inputs with no matches. The table removes the repeats: see [overlapping subproblems](/overlapping-subproblems/).
- **Traceback.** The case that gave each $c[i, j]$ says how to extend an LCS backwards, which is the [traceback](/traceback/) that recovers one LCS.
- **Monotone table.** From the recurrence, $c[i, j]$ is non-decreasing in $i$ and in $j$, and $c[i, j] - c[i-1, j] \in \{0, 1\}$ and $c[i, j] - c[i, j-1] \in \{0, 1\}$. The [bit-parallel LCS](/bit-parallel-lcs/) algorithm stores exactly these 0 and 1 differences in machine words. Hunt-Szymanski uses the same monotonicity.
- **Symmetry and reversal.** The theorem has a mirror form for the first items and suffixes. [Hirschberg's algorithm](/hirschberg-lcs/) runs the recurrence forward on prefixes and backward on suffixes and meets in the middle.
- **Edit distance.** The same proof, with costs, gives the recurrence of [edit distance](/edit-distance/).

## Tightness

- **Case 1 is a "can", case 2 or 3 is an "or".** In case 1 the theorem says each LCS ends with the common last item. In the mismatch case it does not say which item to drop. For $X = \text{AB}$ and $Y = \text{BA}$, both A and B are LCSs. The LCS A is an LCS of $X_1 = \text{A}$ and $Y$ (part 2), and the LCS B is an LCS of $X$ and $Y_1 = \text{B}$ (part 3). Neither single choice is right for both, so the recurrence must take the maximum of two values.
- **A wrong greedy rule.** Matching the first item of $X$ with its first occurrence in $Y$ is not safe. For $X = \text{ABC}$ and $Y = \text{BCA}$, matching A with the A of $Y$ gives length 1, but BC has length 2.
- **The structure needs a prefix order.** For the [longest common substring](/longest-common-substring/), an optimal solution is not made of optimal solutions of smaller prefixes in this way: a longest common substring of $X_{m-1}$ and $Y$ can be in a different place from that of $X$ and $Y$. That problem uses a different table, of the longest common suffixes.

## History

Wagner and Fischer (1974) stated the recurrence, in its form with costs, for the string-to-string correction problem and noted that the longest common subsequence is a special case. CLRS states it in the three-case form above, as Theorem 15.1 in the third edition and Theorem 14.1 in the fourth.

## References
