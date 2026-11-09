---
tag: XX0RBH
kind: theorem
slug: zeckendorf-theorem
name: Zeckendorf's theorem
aliases:
- Zeckendorf representation
- Fibonacci number system
- Fibonacci representation of integers
area: combinatorics/counting-algorithms
level: core
summary: Every positive integer can be written uniquely as a sum of non-consecutive Fibonacci numbers.
prereqs: [fibonacci-numbers]
see_also: [fibonacci-numbers, fibonacci-coding, fibonacci-search, greedy-algorithm, binet-formula, counting-integer-compositions, transfer-matrix-method]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 1.2.8, Fibonacci Numbers (the exercise on the Fibonacci number system)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 6.6, Fibonacci Numbers (the Fibonacci number system)
  - paper: "Édouard Zeckendorf, Représentation des nombres naturels par une somme de nombres de Fibonacci ou de nombres de Lucas, Bulletin de la Société Royale des Sciences de Liège 41 (1972), 179-182"
    title: Zeckendorf's own publication of the theorem
    locator: the whole paper
---

Zeckendorf's theorem says that every positive integer is a sum of Fibonacci numbers, no two of them consecutive in the sequence, in exactly one way. For example, $100 = 89 + 8 + 3$. The representation is a number system with binary digits and the single rule "no two adjacent 1s", so it puts the integers $0, \ldots, F_{k+2} - 1$ in one to one correspondence with the binary strings of length $k$ that avoid $11$. The greedy algorithm finds it in $O(\log n)$ steps, and it is the basis of [Fibonacci coding](/fibonacci-coding/).

## Statement

**Notation.** The [Fibonacci numbers](/fibonacci-numbers/) are $F_0 = 0$, $F_1 = 1$ and $F_j = F_{j-1} + F_{j-2}$ for $j \ge 2$. So $F_2, F_3, F_4, \ldots = 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, \ldots$ (OEIS A000045). We use only indices $j \ge 2$, so that the value 1 appears once. A set $J$ of integers is *sparse* if it contains no two consecutive integers.

**Theorem (Zeckendorf).** For every integer $n \ge 1$ there is exactly one finite sparse set $J \subseteq \{2, 3, 4, \ldots\}$ with

$$n = \sum_{j \in J} F_j.$$

With the empty set for $n = 0$, the statement holds for every $n \ge 0$.

**Lemma (the largest sum).** If $J \subseteq \{2, 3, \ldots\}$ is sparse and nonempty with largest element $j$, then $\sum_{i \in J} F_i \le F_{j+1} - 1$, with equality for $J = \{j, j - 2, j - 4, \ldots\}$ down to $2$ or $3$.

**Counting form.** For $k \ge 0$, the map $(b_{k+1}, \ldots, b_2) \mapsto \sum_j b_j F_j$ is a bijection from the binary strings of length $k$ with no two adjacent 1s onto $\{0, 1, \ldots, F_{k+2} - 1\}$. In particular, there are exactly $F_{k+2}$ such strings.

## In plain words

Pick any whole number. Take the largest Fibonacci number that fits, subtract it, and repeat with what is left. You end with a sum of Fibonacci numbers in which no two are neighbours in the sequence, such as 89 plus 8 plus 3 for 100. The theorem says this always works, and that no other choice of non-neighbouring Fibonacci numbers gives the same total. So each number has one Fibonacci "spelling", like its one spelling in binary.

## Proof

*Proof of the lemma.* By induction on $j$. For $j = 2$ the only set is $\{2\}$, with sum $F_2 = 1 = F_3 - 1$. For $j = 3$ the only set is $\{3\}$, because $2$ is adjacent to $3$, and its sum is $F_3 = 2 = F_4 - 1$. For $j \ge 4$, the rest $J \setminus \{j\}$ is sparse with all elements at most $j - 2$. If it is empty, the sum is $F_j \le F_{j+1} - 1$, since $F_{j-1} \ge 1$. Otherwise, by the induction hypothesis its sum is at most $F_{j-1} - 1$, so the total is at most $F_j + F_{j-1} - 1 = F_{j+1} - 1$. The set $\{j, j - 2, \ldots\}$ meets the bound at each step of the induction. $\square$

*Existence.* By strong induction on $n$. For $n = 0$ take the empty set. For $n \ge 1$, let $j \ge 2$ be the largest index with $F_j \le n$. Then $n < F_{j+1} = F_j + F_{j-1}$, so $0 \le n - F_j < F_{j-1}$. By the induction hypothesis, $n - F_j$ has a sparse representation $J'$. Every element of $J'$ is at most $j - 2$, because an element $i \ge j - 1$ would give $n - F_j \ge F_i \ge F_{j-1}$. So $J' \cup \{j\}$ is sparse and represents $n$.

*Uniqueness.* Let $J$ and $K$ be sparse sets in $\{2, 3, \ldots\}$ with the same sum. Remove their common elements: $J' = J \setminus K$ and $K' = K \setminus J$ are still sparse, disjoint and have equal sums. If one of them is empty, its sum is 0, so the other is empty too, and $J = K$. Otherwise let $j = \max J'$ and $k = \max K'$, and say $j > k$ (they differ, since the sets are disjoint). By the lemma, $\sum K' \le F_{k+1} - 1 \le F_j - 1 < F_j \le \sum J'$, which is a contradiction. $\square$

*Counting form.* A string of length $k$ with no two adjacent 1s is the indicator of a sparse set $J \subseteq \{2, \ldots, k+1\}$. By the lemma its sum is at most $F_{k+2} - 1$. By uniqueness, different strings give different sums. By existence and the existence proof, each $n < F_{k+2}$ has a representation whose largest index $j$ satisfies $F_j \le n < F_{k+2}$, so $j \le k + 1$, and the representation is one of these strings. $\blacksquare$

## Consequences

- **The greedy algorithm.** The existence proof is a [greedy algorithm](/greedy-algorithm/): repeatedly subtract the largest Fibonacci number that fits. Since $F_j \ge \varphi^{j-2}$ with $\varphi = (1 + \sqrt 5)/2$, the indices up to $n$ number $O(\log n)$, and the algorithm runs in $O(\log n)$ arithmetic operations. Going down the list of Fibonacci numbers once, from the top, is enough, because each chosen index skips at least one.
- **Counting strings with no $11$.** The counting form proves that the binary strings of length $k$ with no two adjacent 1s number $F_{k+2}$: $1, 2, 3, 5, 8, 13, 21$ for $k = 0, \ldots, 6$. The same count follows from the [transfer-matrix method](/transfer-matrix-method/), and also counts the compositions of $k + 1$ into parts 1 and 2 ([counting integer compositions](/counting-integer-compositions/)).
- **Ranking and unranking.** Compare two strings that avoid $11$ at the first position where they differ. By the lemma, the one with a 1 there has the larger sum, so the bijection preserves the lexicographic order, and the value of a string is its rank. So a program can turn a rank into a string and back in $O(k)$ steps without listing.
- **Fibonacci coding.** Write the Zeckendorf digits from $F_2$ upwards and append a 1. The last digit is always 1 and no other pair of adjacent 1s occurs, so "11" marks the end of each codeword. This is [Fibonacci coding](/fibonacci-coding/), a self-synchronizing code for integers.

## Tightness

- **Sparseness is needed for uniqueness.** Without it, $3 = F_4 = F_3 + F_2$ has two representations, and $8 = F_6 = F_5 + F_4 = F_5 + F_3 + F_2$ has three.
- **The index 1 must be excluded.** $F_1 = F_2 = 1$, so allowing both would give $1 = F_1 = F_2$ two representations.
- **The lemma is tight.** The sum $F_j + F_{j-2} + \cdots$ equals $F_{j+1} - 1$ exactly. For example $8 + 3 + 1 = 12 = 13 - 1$ and $13 + 5 + 2 = 20 = 21 - 1$. So $F_{k+2}$ is exactly the number of integers that the strings of length $k$ reach.
- **Other sequences.** For powers of 2 the same argument gives binary notation, with no sparseness condition. For a general increasing sequence the greedy algorithm still gives a representation when the first term is 1, but uniqueness needs the analogue of the lemma, which depends on the recurrence of the sequence.

## History

The representation was known to Lekkerkerker, who published it in 1952, and to Zeckendorf, who said he had proved it in 1939 and published it in 1972. The theorem is named after Zeckendorf. Apostolico and Fraenkel used Fibonacci representations for robust codes of integers in 1987, and Fraenkel and Klein studied such codes for data compression in the 1990s.

## References
