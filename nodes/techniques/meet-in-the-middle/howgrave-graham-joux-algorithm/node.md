---
tag: ZVD66Y
kind: algorithm
slug: howgrave-graham-joux-algorithm
name: Howgrave-Graham-Joux algorithm
aliases:
- HGJ algorithm
- Howgrave-Graham-Joux subset sum
area: techniques/meet-in-the-middle
level: research
summary: Subset sum in heuristic time about 2^(0.337n) for dense random instances, using the representation technique; the proved worst case is larger.
solves: [subset-sum-problem]
model: word-ram
complexity:
  vars: {n: the number of items, k: the number of random rounds}
  time: {worst: O(k 4^n + n 2^n), best: O(n 2^(n/2))}
  space: {extra: O(2^n)}
properties: {deterministic: false, comparison: false, recursive: false}
history:
  year: 2010
  people: [Nick Howgrave-Graham, Antoine Joux]
  note: Presented at EUROCRYPT 2010; the first generic algorithm for hard knapsacks with heuristic time below 2^(n/2).
prereqs: [subset-sum-problem, schroeppel-shamir-algorithm, representation-technique, binomial-coefficient]
see_also: [horowitz-sahni-algorithm, schroeppel-shamir-algorithm, representation-technique, information-set-decoding, merkle-hellman-knapsack-cryptosystem, lattice-basis-reduction, las-vegas-algorithm, wagners-algorithm]
sources:
  - paper: doi:10.1007/978-3-642-13190-5_12
    title: "Nick Howgrave-Graham and Antoine Joux, New generic algorithms for hard knapsacks, EUROCRYPT 2010, LNCS 6110, 235-256"
    locator: the whole paper; the long version is IACR ePrint 2010/189, whose abstract claims time 2^(0.3113 n) up to polynomial factors
  - paper: doi:10.1007/978-3-642-20465-4_21
    title: "Anja Becker, Jean-Sebastien Coron and Antoine Joux, Improved generic algorithms for hard knapsacks, EUROCRYPT 2011, LNCS 6632, 364-385"
    locator: the abstract and introduction, which state the HGJ bounds as time 2^(0.337n) and memory 2^(0.256n), and give 2^(0.291n) with representations over {-1, 0, 1}
  - paper: doi:10.1007/978-3-030-64834-3_22
    title: "Xavier Bonnetain, Remi Bricout, Andre Schrottenloher and Yixin Shen, Improved classical and quantum algorithms for subset-sum, ASIACRYPT 2020, LNCS 12492, 633-666"
    locator: Section 2.4, The HGJ algorithm (the four-level merging tree, the list sizes and the corrected time exponent 0.337)
  - paper: doi:10.1137/0210033
    title: "Richard Schroeppel and Adi Shamir, A T = O(2^{n/2}), S = O(2^{n/4}) algorithm for certain NP-complete problems, SIAM Journal on Computing 10(3) (1981), 456-464"
    locator: the four-list algorithm, the previous best method for hard knapsacks
---

The Howgrave-Graham-Joux (HGJ) algorithm solves random instances of the [subset sum problem](/subset-sum-problem/) of density close to 1 faster than $2^{n/2}$. Its key idea is the [representation technique](/representation-technique/): it writes the unknown solution as a sum of two vectors of half its weight in many ways, and it adds a random modular condition that keeps only about one of these ways. The lists that it must build then shrink by the number of representations. The time of the full algorithm is $\tilde{O}(2^{0.337n})$ with memory $\tilde{O}(2^{0.256n})$, under a heuristic assumption about the distribution of the list entries; it is not a proved worst-case bound.

## In plain words

You want half of the numbers to add up to a target. Split the unknown set into two smaller sets, each with a quarter of the numbers. There are many ways to do this split for the same answer.

Now make up a random rule, such as "the sum of the first small set leaves remainder 3 when divided by 4". About one of the many splits obeys the rule, and one is enough. List only the small sets that obey the rule: these lists are much shorter than the list of all small sets. Then look for one small set from each list that add up to the target and do not share a number.

If a round fails, pick a new rule. The short lists give the speed. The speed is only an estimate: it assumes that the remainders of the sums behave like random numbers.

## The problem

The input is a list of integers $a_0, \ldots, a_{n-1}$, a target $t$ and a weight $w$. The output is a vector $e \in \{0, 1\}^n$ with $\sum_i e_i = w$ and $\langle a, e \rangle = \sum_i a_i e_i = t$, or NONE. This is [subset sum](/subset-sum-problem/) with a known number of chosen items. If $w$ is unknown, run the algorithm for each $w$ from 0 to $n$.

HGJ target the *hard* case. The *density* of an instance is $d = n / \log_2 \max_i a_i$. Lattice-based low-density attacks, which use [lattice basis reduction](/lattice-basis-reduction/), solve instances of small density, but not instances of density close to 1. Knapsack cryptosystems, starting with [Merkle-Hellman](/merkle-hellman-knapsack-cryptosystem/), are one reason for the interest in these instances. HGJ analyse random instances of density 1 with $w = n/2$, the weight with the most subsets. Before HGJ, the best generic method for them was the [Schroeppel-Shamir algorithm](/schroeppel-shamir-algorithm/), in $\tilde{O}(2^{n/2})$ time and $\tilde{O}(2^{n/4})$ memory.

## The algorithm

The pseudocode is a simplified HGJ with one level of representations. It is exact: rounds with random choices search for the solution, and an exhaustive search at the end makes sure that the answer is correct even when all rounds fail. It is a [Las Vegas algorithm](/las-vegas-algorithm/) in this sense.

Call a solution $e$ *balanced* for a split of the positions into halves $P$ and $Q$ when it has $p = \lfloor w/2 \rfloor$ ones in $P$ and $q = w - p$ ones in $Q$. A *representation* of $e$ is a pair $(x, y)$ of vectors in $\{0, 1\}^n$ with $x + y = e$, where $x$ has $p_1 = \lfloor p/2 \rfloor$ ones in $P$ and $q_1 = \lfloor q/2 \rfloor$ ones in $Q$. A balanced solution has exactly $\binom{p}{p_1}\binom{q}{q_1}$ representations: choose which ones of $e$ in each half go to $x$.

```pseudo id=main
HGJ(a[0 .. n − 1], t, w, rounds)
L1  p ← ⌊w/2⌋, q ← w − p                  ▷ ones of a balanced solution in each half
L2  p1 ← ⌊p/2⌋, q1 ← ⌊q/2⌋                ▷ ones of x in each half
L3  M ← C(p, p1) · C(q, q1)               ▷ the number of representations
L4  repeat rounds times
L5      split the positions at random into P (⌊n/2⌋ positions) and Q (the rest)
L6      R ← a uniform random residue in [0, M)
L7      L_x ← LIST(P, p1, Q, q1, R)
L8      L_y ← LIST(P, p − p1, Q, q − q1, (t − R) mod M)
L9      H ← a hash map from ⟨a, y⟩ to the vectors y of L_y
L10     for each x in L_x, each y in H[t − ⟨a, x⟩]: if x and y share no one then return x + y
L11 return a w-subset with sum t by exhaustive search, or NONE if there is none

LIST(P, i, Q, j, r)                        ▷ all x with i ones in P, j in Q, ⟨a, x⟩ ≡ r (mod M)
L12 G ← a hash map from ⟨a, z⟩ mod M to the vectors z with j ones, all in Q
L13 out ← an empty list
L14 for each z′ with i ones, all in P, and each z in G[(r − ⟨a, z′⟩) mod M]: append z′ + z to out
L15 return out
```

Lines L1 to L3 fix the shape of $x$ and $y$ and set the modulus $M$ to the number of representations of a balanced solution. A round picks a random split (line L5) and a random residue $R$ (line L6). Line L7 lists the vectors $x$ of the shape of the first part whose sum is $R$ modulo $M$, and line L8 the vectors $y$ of the shape of the second part whose sum is $t - R$ modulo $M$. Each pair $(x, y)$ then has $\langle a, x \rangle + \langle a, y \rangle \equiv t \pmod M$, and line L10 looks for a pair whose sum is exactly $t$ and whose ones do not overlap. LIST is a modular join of a list on $P$ and a list on $Q$, in the style of [Horowitz-Sahni](/horowitz-sahni-algorithm/) with a hash table.

The random rule of line L6 does not lose the solution on average: each representation of $e$ has some residue, and line L6 picks that residue with probability $1/M$. With $M$ representations, about one of them is expected to pass.

**The full algorithm.** HGJ apply the same idea again inside LIST: the vectors $x$ of weight $n/4$ are themselves written in many ways as sums of two vectors of weight $n/8$, with a second modular condition. The lists then form a tree of four levels with eight base lists of vectors of weight $n/16$ on half of the positions. The sizes of the conditions are found by numerical optimization.

## Example

Take $a = [31, 17, 45, 8, 26, 53, 12, 39]$, $t = 114$ and $w = 4$. The only solution is $e = \{31, 45, 26, 12\}$, the positions $\{0, 2, 4, 6\}$. Lines L1 to L3 give $p = q = 2$, $p_1 = q_1 = 1$ and $M = 2 \cdot 2 = 4$. So $x$ and $y$ each have one item from each half.

Take the round with $P = \{31, 17, 45, 8\}$ and $Q = \{26, 53, 12, 39\}$. The solution is balanced: it has $31, 45$ in $P$ and $26, 12$ in $Q$. Its four representations have $x \in \{\{31, 26\}, \{31, 12\}, \{45, 26\}, \{45, 12\}\}$, with sums $57, 43, 71, 57$ and residues $1, 3, 3, 1$ modulo 4. The 16 vectors with one item in each half fall into 4 lists of 4 by their residue. The table shows the round for each value of $R$.

| $R$ | $L_x$ (sums) | residue of $L_y$ | $L_y$ (sums) | pairs with sum 114 | result |
|---|---|---|---|---|---|
| 0 | 20, 56, 84, 84 | 2 | 34, 70, 70, 98 | 0 | fail |
| 1 | 29, 57, 57, 61 | 1 | 29, 57, 57, 61 | 4, of which 2 disjoint | $\{31, 26\} + \{45, 12\}$ |
| 2 | 34, 70, 70, 98 | 0 | 20, 56, 84, 84 | 0 | fail |
| 3 | 43, 43, 47, 71 | 3 | 43, 43, 47, 71 | 4, of which 2 disjoint | $\{31, 12\} + \{45, 26\}$ |

For $R = 1$, the two vectors with sum 57 are $\{31, 26\}$ and $\{45, 12\}$, so the pairs with sum 114 are the four ordered pairs of these two vectors; the two pairs of a vector with itself overlap. So a round with this split succeeds for 2 of the 4 residues. Each list has 4 entries, while the list of all vectors of this shape has 16.

## Correctness

Each returned answer is checked: line L10 returns $x + y$ only when $\langle a, x \rangle + \langle a, y \rangle = t$ and the ones of $x$ and $y$ do not overlap, so $x + y \in \{0, 1\}^n$ has weight $p_1 + q_1 + (p - p_1) + (q - q_1) = w$ and sum $t$. Line L11 is an exhaustive search. So the output is a correct solution, or NONE exactly when there is none.

The key fact for the rounds is this. If, in some round, a solution $e$ is balanced for the split of line L5 and some representation $(x^*, y^*)$ of $e$ has $\langle a, x^* \rangle \equiv R \pmod M$, then the round returns a solution. Indeed $x^* \in L_x$, and $\langle a, y^* \rangle = t - \langle a, x^* \rangle \equiv t - R$, so $y^* \in L_y$, and line L10 finds the pair $(x^*, y^*)$ unless it returns another solution first. The full proof is in the proof file.

## Complexity

**Exact bounds.** In a round, LIST stores at most $2^{\lceil n/2 \rceil}$ vectors in $G$ and returns at most $2^n$ vectors, and line L10 checks at most $|L_x| \cdot |L_y| \le 4^n$ pairs. Line L11 checks at most $\binom{n}{w} \le 2^n$ sets of $w$ items. With $k$ rounds, the worst-case time is $O(k \cdot 4^n + n \cdot 2^n)$ on the [word RAM](/word-ram/), and the space is $O(2^n)$. No better worst-case bound is known for this method. The best case is a hit in the first round, after building $G$ in $O(n \cdot 2^{n/2})$ time.

**Heuristic analysis.** The speed of HGJ rests on an assumption: for random items of about $n$ bits, the sums $\langle a, x \rangle$ of the vectors of each shape behave like independent uniform random numbers modulo $M$ and modulo $2^n$. Under this assumption, with $w = n/2$ and $n$ divisible by 8, write $H(x) = -x \log_2 x - (1 - x) \log_2(1 - x)$ and use $\binom{m}{\alpha m} = 2^{m H(\alpha) + O(\log m)}$:

- $M = \binom{n/4}{n/8}^2 = 2^{n/2 - O(\log n)}$.
- The table $G$ and the loop of line L14 have $\binom{n/2}{n/8} = \tilde{O}(2^{0.406n})$ entries, since $\tfrac{1}{2} H(\tfrac14) \approx 0.4056$.
- The lists $L_x$ and $L_y$ keep about a $1/M$ part of the $\binom{n/2}{n/8}^2$ vectors of their shape: $\tilde{O}(2^{(H(1/4) - 1/2) n}) = \tilde{O}(2^{0.311n})$ entries.
- A pair of $L_x \times L_y$ already agrees with $t$ modulo $M$. It has the exact sum $t$ with probability about $M / 2^n$, so line L10 checks about $2^{(2 \cdot 0.311 - 0.5) n} = 2^{0.123n}$ pairs.
- A random split makes a fixed solution balanced with probability $\binom{n/2}{n/4}^2 / \binom{n}{n/2} = \Theta(1/\sqrt{n})$: 0.514 for $n = 8$, 0.248 for $n = 40$, 0.177 for $n = 80$. Given a balanced solution, about one representation passes the residue test, so a constant fraction of these rounds succeed.

So the one-level version takes about $2^{0.406n}$ time and memory. The full HGJ algorithm, with the second level of representations, shrinks the base lists and reaches time $\tilde{O}(2^{0.337n})$ and memory $\tilde{O}(2^{0.256n})$, as stated by Becker, Coron and Joux (2011). The abstract of the long version of the HGJ paper claims $\tilde{O}(2^{0.3113n})$; Bonnetain, Bricout, Schrottenloher and Shen (2020) recall HGJ "with the corrected time complexity" of Becker, Coron and Joux, which is $0.337n$. These bounds hold for random instances under the heuristic, not for every input.

## Properties

- **Randomized.** The split and the residue are random. The version above is a Las Vegas algorithm: its output is always correct.
- **Heuristic time.** No proof is known that the bound $2^{0.337n}$ holds for all inputs, or for random inputs without the uniformity assumption.
- **Weight-specific.** Each run looks for solutions of one weight $w$.
- **More memory than Schroeppel-Shamir.** Its memory exponent, 0.256, is above the 1/4 of Schroeppel-Shamir.

## Variants and improvements

- **Becker-Coron-Joux (2011).** Let $x$ and $y$ have entries in $\{-1, 0, 1\}$, where the $-1$ entries must cancel in $x + y$. This gives more representations and reaches $\tilde{O}(2^{0.291n})$ time. The same paper gives a constant-memory variant based on cycle finding in $\tilde{O}(2^{0.72n})$ time and a time-memory trade-off.
- **Later work.** Bonnetain, Bricout, Schrottenloher and Shen (2020) allow entries up to 2 in the representations and lower the exponent to about $0.283$, and give quantum versions.
- **Decoding.** The same representations speed up [information set decoding](/information-set-decoding/) for the [syndrome decoding problem](/syndrome-decoding-problem/).

## When to use it

Use HGJ or its successors for random subset sum instances of density close to 1 and $n$ large enough that $2^{n/2}$ is out of reach, where a heuristic running time is acceptable, for example in the cryptanalysis of knapsack-based schemes. For low-density instances, use the lattice-based attacks instead. For an exact method with a proved bound and small memory, use [Schroeppel-Shamir](/schroeppel-shamir-algorithm/). When the items are small, the [dynamic program](/knapsack-dynamic-programming/) in $O(n t)$ time wins. At the small $n$ of the tests on this page, the extra work of the rounds is larger than the gain.

## Pitfalls

- **An inconsistent residue.** Line L8 must use $(t - R) \bmod M$ for $y$. Using $R$ for both lists, as in line L7, keeps only pairs with sum $2R$ modulo $M$, and the solution is found only by chance.
- **Forgetting the overlap test.** Line L10 must check that $x$ and $y$ share no one. Without the check, $x + y$ can have an entry 2, and the returned set has the right sum but is not a subset.
- **The wrong modulus.** If $M$ is much larger than the number of representations, most rounds keep no representation and fail. If it is much smaller, the lists keep many representations of the same solution and grow without benefit. Line L3 sets $M$ to the count of representations.
- **Exhaustive fallback forgotten.** Without line L11, the algorithm is Monte Carlo: it can return NONE when a solution exists, for example when no split makes the solution balanced in the rounds that were run.
- **Trusting the heuristic for structured inputs.** The bound assumes random items. On inputs with many equal sums, such as all items equal, the lists and the number of pairs can be close to the exact worst case.

## Implementations

## History

Howgrave-Graham and Joux presented the algorithm at EUROCRYPT 2010, with a long version on the IACR ePrint archive (2010/189). It was the first generic algorithm for hard knapsacks with a heuristic time below the $2^{n/2}$ of Schroeppel and Shamir (1981). Becker, Coron and Joux (EUROCRYPT 2011) extended the technique to $\{-1, 0, 1\}$ representations.

## References
