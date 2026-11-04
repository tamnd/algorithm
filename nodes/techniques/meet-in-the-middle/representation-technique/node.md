---
tag: 6FT6K8
kind: technique
slug: representation-technique
name: Representation technique
aliases:
- Howgrave-Graham-Joux representations
area: techniques/meet-in-the-middle
level: research
summary: Counts each solution in many ways via redundant representations, so a meet-in-the-middle join finds one of them with far fewer candidates.
prereqs: [horowitz-sahni-algorithm, schroeppel-shamir-algorithm, binomial-coefficient, multinomial-coefficient]
see_also: [howgrave-graham-joux-algorithm, subset-sum-problem, information-set-decoding, syndrome-decoding-problem, meet-in-the-middle-attack, wagners-algorithm, generalized-birthday-problem]
sources:
  - paper: doi:10.1007/978-3-642-13190-5_12
    title: "Nick Howgrave-Graham and Antoine Joux, New generic algorithms for hard knapsacks, EUROCRYPT 2010, LNCS 6110, 235-256"
    locator: the whole paper (representations in {0, 1}^n and the random modular constraint)
  - paper: doi:10.1007/978-3-642-20465-4_21
    title: "Anja Becker, Jean-Sebastien Coron and Antoine Joux, Improved generic algorithms for hard knapsacks, EUROCRYPT 2011, LNCS 6632, 364-385"
    locator: the abstract and the main algorithm (representations in {-1, 0, 1}^n, time 2^(0.291n))
  - paper: doi:10.1007/978-3-642-25385-0_6
    title: "Alexander May, Alexander Meurer and Enrico Thomae, Decoding random linear codes in O~(2^(0.054n)), ASIACRYPT 2011, LNCS 7073, 107-124"
    locator: the application of representations to information set decoding
  - paper: doi:10.1007/978-3-642-29011-4_31
    title: "Anja Becker, Antoine Joux, Alexander May and Alexander Meurer, Decoding random binary linear codes in 2^(n/20): how 1 + 1 = 0 improves information set decoding, EUROCRYPT 2012, LNCS 7237, 520-536"
    locator: the representations with overlapping supports over F_2
  - paper: doi:10.1007/978-3-030-64834-3_22
    title: "Xavier Bonnetain, Remi Bricout, Andre Schrottenloher and Yixin Shen, Improved classical and quantum algorithms for subset-sum, ASIACRYPT 2020, LNCS 12492, 633-666"
    locator: Section 1 (the representation technique and its heuristic) and Section 2.4 (the HGJ merging tree)
---

The representation technique speeds up a [meet-in-the-middle](/meet-in-the-middle-attack/) search by writing each solution as a sum of two smaller parts in many different ways, called representations, and keeping only the parts that pass a random filter. If each solution has $R$ representations and the filter passes a $1/R$ fraction of the candidates, about one representation of each solution survives, while every list shrinks by a factor of $R$. Howgrave-Graham and Joux introduced it in 2010 for hard instances of [subset sum](/subset-sum-problem/), and it has since been used for subset sum and for the decoding of random linear codes. Its running times rest on a heuristic assumption about how the filtered lists are distributed.

## In plain words

In a classic meet-in-the-middle search, you cut the answer into a left part and a right part along a fixed line. Each answer then has exactly one left part and one right part, and you must list every possible left part and every possible right part.

Now drop the fixed line. Let a part be any piece of the answer of half its size. The same answer can now be cut into two pieces in many ways. You do not need all of these ways: one is enough.

So you add a random test that only some candidate pieces pass, for example a condition on the remainder of their sum. Choose the test so strict that, of the many ways to cut the answer, about one passes. Most candidates fail the test, so the lists you must build become much shorter, and the search becomes faster.

## When it applies

- The solution is a vector $e$ in a set with an additive structure, such as $\{0, 1\}^n$, and the condition on it is linear: $\langle a, e \rangle = t$ over the integers, or $H e = s$ over a finite field.
- A plain split of $e$ into fixed left and right halves already gives a meet-in-the-middle algorithm, as in [Horowitz-Sahni](/horowitz-sahni-algorithm/) or [Schroeppel-Shamir](/schroeppel-shamir-algorithm/).
- The solution has many decompositions $e = x + y$ into two vectors of a smaller, fixed shape, for example of half the weight, and the number of decompositions can be counted exactly with [binomial](/binomial-coefficient/) or [multinomial](/multinomial-coefficient/) coefficients.
- The linear condition can be split as a partial condition on $x$ and the matching partial condition on $y$, for example modulo a number $M$ or on a part of the coordinates.
- The instances are random, so that the filtered lists have sizes close to their expected values. The technique gives heuristic bounds for random instances, not worst-case bounds.

## The template

Let $f$ be the linear map of the problem ($f(v) = \langle a, v \rangle$ for subset sum), let $t$ be the target, and let $\mathcal{S}$ be the set of possible solutions (for example, the vectors of weight $w$).

```pseudo id=main
REPRESENTATION-SEARCH(f, t)
L1  choose a shape T of the parts, such that each e in S has R decompositions e = x + y with x, y in T
L2  choose a filter modulus M ≈ R, and a random residue r in [0, M)
L3  L_x ← all x in T with f(x) ≡ r (mod M)          ▷ BUILD: a modular meet in the middle, or this template again
L4  L_y ← all y in T with f(y) ≡ t − r (mod M)
L5  for each x in L_x and each y in L_y with f(x) + f(y) = t do     ▷ a hash join on f
L6      if x + y is in S then return x + y          ▷ VALID: no overlap, entries in the allowed set
L7  go back to L2 with a new r, or stop after enough rounds
```

The holes are the shape $T$ (line L1), the filter (line L2), the method BUILD that makes the filtered lists (lines L3 and L4), and the test VALID (line L6).

**The count.** Let $N = |T|$ be the number of vectors of the shape. Under the heuristic that the values $f(x) \bmod M$ are spread evenly, each filtered list has about $N / M$ entries. A fixed solution $e$ has $R$ decompositions, and each one passes the filter of line L3 with probability $1/M$; when $x$ passes, $y = e - x$ passes line L4 automatically, because $f(y) = t - f(x) \equiv t - r$. So about $R / M$ representations of $e$ survive. With $M \approx R$, about one survives, and

$$|L_x| \approx |L_y| \approx \frac{N}{R}.$$

If the residues of the $R$ representations behave like independent uniform values, the probability that at least one survives is $1 - (1 - 1/R)^R \ge 1 - 1/e \approx 0.632$.

**The consistency rule.** The filter must be applied to the partial values so that the two parts together meet the full condition: $r$ for $x$ and $t - r$ for $y$. In a tree of several levels, the residues at a lower level must sum to the residue of the level above, and each new level adds new bits of constraint that are compatible with the old ones.

**The example count.** Let $e \in \{0, 1\}^n$ have weight $w$, with $w$ even, and let $T$ be the vectors of $\{0, 1\}^n$ of weight $w/2$. A decomposition $e = x + y$ with $x, y \in T$ must have both supports inside the support of $e$ and disjoint, so it is a choice of which $w/2$ of the $w$ ones of $e$ go to $x$:

$$R = \binom{w}{w/2}.$$

Now let $T$ be the vectors of $\{-1, 0, 1\}^n$ with $w/2 + \alpha$ entries equal to 1 and $\alpha$ entries equal to $-1$. At a position where $e_i = 1$, the pair $(x_i, y_i)$ is $(1, 0)$ or $(0, 1)$. At a position where $e_i = 0$, it is $(0, 0)$, $(1, -1)$ or $(-1, 1)$. Let $b_1$ and $b_2$ count the last two kinds, and let $c$ count the positions with $e_i = 1$ and $x_i = 1$. Then $x$ has $c + b_1$ ones and $b_2$ minus ones, and $y$ has $(w - c) + b_2$ ones and $b_1$ minus ones. Both are in $T$ exactly when $b_1 = b_2 = \alpha$ and $c = w/2$. So

$$R_\alpha = \binom{w}{w/2} \cdot \frac{(n - w)!}{\alpha! \, \alpha! \, (n - w - 2\alpha)!}, \qquad N_\alpha = \frac{n!}{(w/2 + \alpha)! \, \alpha! \, (n - w/2 - 2\alpha)!}.$$

For $n = 20$ and $w = 10$:

| $\alpha$ | $R_\alpha$ | $N_\alpha$ | $N_\alpha / R_\alpha$ |
|---|---|---|---|
| 0 | 252 | 15504 | 61.5 |
| 1 | 22680 | 542640 | 23.9 |
| 2 | 317520 | 6046560 | 19.0 |
| 3 | 1058400 | 27713400 | 26.2 |

The $-1$ entries make the set $T$ larger, but they make the number of representations grow faster, up to a point. Here the filtered lists are smallest at $\alpha = 2$. For comparison, a fixed split into left and right halves has $R = 1$, and a single list of all vectors of weight $w/2$ has $N_0 = 15504$ entries.

**A small instance.** Take $a = [31, 17, 45, 8, 26, 53, 12, 39]$ and the solution $\{31, 45, 26, 12\}$ of weight 4 with sum 114. It has $\binom{4}{2} = 6$ representations as two sets of two items. The sums of the first part are $76, 57, 43, 71, 57, 38$, with residues $4, 3, 1, 5, 3, 2$ modulo $M = 6$. So 5 of the 6 residues keep at least one representation, and only $r = 0$ loses the solution. The 28 sets of two items fall into lists of 3, 5, 6, 4, 4 and 6 sets for the residues 0 to 5, instead of one list of 28.

## Classic examples

From simple to hard:

- **Subset sum with $\{0, 1\}$ parts.** The [Howgrave-Graham-Joux algorithm](/howgrave-graham-joux-algorithm/) writes a solution of weight $n/2$ as a sum of two vectors of weight $n/4$, with $\binom{n/2}{n/4}$ representations, and applies the template again to build each list. Becker, Coron and Joux (2011) state its time as $\tilde{O}(2^{0.337n})$ and its memory as $\tilde{O}(2^{0.256n})$, against $\tilde{O}(2^{n/2})$ for [Schroeppel-Shamir](/schroeppel-shamir-algorithm/).
- **Subset sum with $\{-1, 0, 1\}$ parts.** Becker, Coron and Joux (2011) let the parts have $-1$ entries that cancel in the sum, as in the count above. This lowers the time for the [subset sum problem](/subset-sum-problem/) to $\tilde{O}(2^{0.291n})$. Bonnetain, Bricout, Schrottenloher and Shen (2020) also allow entries equal to 2.
- **Information set decoding.** May, Meurer and Thomae (2011) apply representations to the search for a low-weight error vector inside [information set decoding](/information-set-decoding/), with the condition $H e = s$ over $\mathbb{F}_2$ in place of a sum of integers. Their title gives the time $\tilde{O}(2^{0.054n})$ for random binary linear codes in the setting they analyse.
- **Decoding with $1 + 1 = 0$.** Becker, Joux, May and Meurer (2012) let the supports of $x$ and $y$ overlap: over $\mathbb{F}_2$ a position where both have a 1 gives 0 in $x + y$. This is the binary analogue of the $-1$ entries, and it gives more representations for the [syndrome decoding problem](/syndrome-decoding-problem/). Their title gives the time $2^{n/20}$.

## Variations

- **Several levels.** Apply the template inside BUILD: each part is itself a sum of two smaller parts with its own filter. HGJ use a tree with four levels of lists; the sizes of the filters at each level are chosen by numerical optimization.
- **The filter.** Over the integers, the filter is a condition modulo $M$, often a power of two, so that it is a condition on the low bits. Over $\mathbb{F}_2$, it is a condition on some coordinates of $H x$.
- **Richer digit sets.** Parts with entries in $\{-1, 0, 1\}$ or $\{-1, 0, 1, 2\}$ give more representations at the price of larger sets $T$. The best choice is a trade-off, as the table above shows.
- **Las Vegas or Monte Carlo.** A run with a fixed number of rounds can miss the solution. A [Las Vegas](/las-vegas-algorithm/) version adds an exact search at the end, as on the page of the [HGJ algorithm](/howgrave-graham-joux-algorithm/).
- **Related list merges.** [Wagner's algorithm](/wagners-algorithm/) for the [generalized birthday problem](/generalized-birthday-problem/) also merges lists with conditions on partial values, but it looks for any of many solutions, while the representation technique creates many copies of one solution.

## Pitfalls

- **The heuristic is an assumption.** The list sizes $N/M$ and the survival of about one representation assume that the filtered values behave like independent uniform values. This is not proved, and it fails on structured inputs, for example when many items are equal. State the bounds as heuristic.
- **An inconsistent filter.** The filter must be $r$ on one part and $t - r$ on the other, and the residues of the lower levels must add up to those of the upper levels. A filter applied to $x$ alone, or with the wrong residue for $y$, removes the solution.
- **The wrong count.** With $-1$ entries, $R$ and $N$ are multinomial coefficients, as above, not binomial ones. Counting only $\binom{w}{w/2}$ for $R$ while $T$ allows $-1$ entries overestimates the lists by the missing factor, and the chosen $M$ is then too small.
- **Duplicates.** When $M$ is smaller than $R$, several representations of the same solution survive, and the lists hold the same solution many times. The join can then return the same $x + y$ again and again.
- **The validity test.** The sum $x + y$ of two vectors of $T$ can have entries outside the allowed set: a 2 for $\{0, 1\}$ parts, or a $-1$ left over with $\{-1, 0, 1\}$ parts. Line L6 must reject these.
- **The wrong instances.** The technique targets random subset sum instances of density close to 1, where lattice-based low-density attacks, which use [lattice basis reduction](/lattice-basis-reduction/), are not an option. For instances of low density, try those attacks first.

## Exercises

1. Prove that a vector of weight $w$ in $\{0, 1\}^n$, with $w$ even, has exactly $\binom{w}{w/2}$ decompositions $e = x + y$ with $x, y \in \{0, 1\}^n$ of weight $w/2$ each.
2. Show that a fixed split into left and right halves of the positions gives exactly one decomposition, and explain why the filter of line L2 is then useless.
3. For $n = 20$ and $w = 10$, verify the row $\alpha = 1$ of the table, and compute $R_4$, $N_4$ and $N_4 / R_4$.
4. Let a solution have $R$ representations and let $M > R$. Show, with a union bound, that the probability that at least one representation survives a uniform random residue is at most $R / M$.
5. In the small instance above, list the representations that survive for $r = 3$, and give the list $L_y$ for $r = 3$.
6. Over $\mathbb{F}_2$, count the decompositions $e = x + y$ of a vector $e$ of weight $w$ into two vectors of weight $w/2 + \varepsilon$ each, where the supports of $x$ and $y$ overlap in $\varepsilon$ positions outside the support of $e$.

## References
