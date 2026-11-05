---
tag: HT9BXF
kind: theorem
slug: dejean-theorem
name: Dejean's theorem
aliases:
- Dejean's conjecture
- repetition threshold theorem
area: strings/string-combinatorics
level: research
summary: Gives the exact repetition threshold for every alphabet size.
prereqs: [repetition-threshold, overlap-free-word]
see_also: [thue-theorem, thue-morse-word, square-free-word, avoidability, keranen-theorem, cube, maximal-repetition, string-period]
sources:
  - paper: doi:10.1016/0097-3165(72)90011-8
    title: Françoise Dejean, Sur un théorème de Thue, Journal of Combinatorial Theory, Series A 13(1), 1972, 90-99
    locator: the threshold 7/4 for three letters with a uniform morphism generating a 7/4+-free word, the finiteness of 7/4-free ternary words, and the conjecture for four and more letters
  - paper: doi:10.1016/0166-218x(84)90006-4
    title: Jean-Jacques Pansiot, A propos d'une conjecture de F. Dejean sur les répétitions dans les mots, Discrete Applied Mathematics 7(3), 1984, 297-311
    locator: the threshold 7/5 for four letters and the binary coding of words in which any k - 1 consecutive letters are distinct
  - paper: doi:10.1016/0304-3975(92)90264-g
    title: Jean Moulin Ollagnier, Proof of Dejean's conjecture for alphabets with 5, 6, 7, 8, 9, 10 and 11 letters, Theoretical Computer Science 95(2), 1992, 187-205
    locator: morphisms on Pansiot codes for 5 to 11 letters
  - paper: doi:10.1016/j.tcs.2007.06.001
    title: Arturo Carpi, On Dejean's conjecture over large alphabets, Theoretical Computer Science 385(1-3), 2007, 137-151
    locator: the proof for alphabets of at least 33 letters
  - paper: doi:10.1090/s0025-5718-2010-02407-x
    title: James D. Currie and Narad Rampersad, A proof of Dejean's conjecture, Mathematics of Computation 80(274), 2011, 1063-1070
    locator: the completion of the proof for the remaining alphabet sizes
  - paper: doi:10.1016/j.tcs.2010.06.020
    title: Michaël Rao, Last cases of Dejean's conjecture, Theoretical Computer Science 412(27), 2011, 3010-3018
    locator: an independent completion of the remaining cases with computer-checked morphisms
---

Dejean's theorem gives the [repetition threshold](/repetition-threshold/) $\mathrm{RT}(k)$ for every alphabet size $k$: the least exponent $\alpha$ such that an infinite word over $k$ letters can avoid every repetition of exponent greater than $\alpha$. The values are $2$ for two letters, $7/4$ for three, $7/5$ for four, and $k/(k-1)$ for $k \ge 5$. Dejean found the ternary value and conjectured the rest in 1972; the last cases were proved in 2009 to 2011, by Currie and Rampersad and independently by Rao.

## Statement

Let $\Sigma$ be an [alphabet](/alphabet/) of $k \ge 2$ letters; only equality of letters is used, and indices are 0-based. A nonempty word $w$ with smallest [period](/string-period/) $p$ has exponent $e(w) = |w|/p$. For a real $\alpha > 1$, a word is $\alpha$-free if it has no factor of exponent at least $\alpha$, and $\alpha^+$-free if it has no factor of exponent greater than $\alpha$. The repetition threshold is
$$ \mathrm{RT}(k) = \inf \{ \alpha : \text{some infinite word over } k \text{ letters is } \alpha^+\text{-free} \}. $$

**Theorem (Dejean's conjecture, now a theorem).**
$$ \mathrm{RT}(2) = 2, \quad \mathrm{RT}(3) = \tfrac{7}{4}, \quad \mathrm{RT}(4) = \tfrac{7}{5}, \quad \mathrm{RT}(k) = \tfrac{k}{k-1} \text{ for } k \ge 5. $$
Moreover the threshold is attained on both sides: for each $k$ there is an infinite $\mathrm{RT}(k)^+$-free word over $k$ letters, and every $\mathrm{RT}(k)$-free word over $k$ letters is finite. The longest $\mathrm{RT}(k)$-free words have length $3$ for $k = 2$, $38$ for $k = 3$, $121$ for $k = 4$, and $k + 1$ for $k \ge 5$.

## In plain words

Any long text repeats itself somewhere, and the strength of a repetition is measured by how long the repeating stretch is compared with the block that repeats. Over two letters, some block must be followed by a full copy of itself, but nothing stronger is forced. With more letters, the forced repetitions get weaker. Dejean's theorem says exactly how weak they can be made: over three letters, a stretch about seven quarters of its block; over four letters, seven fifths; and over five or more letters, just one letter more than the block, which is the least possible since some letter must come back eventually. Below these values, every long enough text breaks the rule; at these values, an infinite text that respects them exists.

## Proof

The proof has a lower half, that every long enough word over $k$ letters has a factor of exponent at least the stated value, and an upper half, an infinite word with no factor of larger exponent. The lower half is short for $k \ne 3, 4$ and a finite search for $k = 3, 4$. The upper half is a construction for each $k$, by hand for small $k$ and with computer-checked morphisms for most $k \ge 5$; it is cited here with its method.

**Lemma 1 (the general lower bound).** Every word over $k \ge 2$ letters of length $k + 2$ has a factor of exponent at least $k/(k-1)$. The word $a_1 a_2 \cdots a_k a_1$, with distinct letters $a_i$, of length $k + 1$, is $k/(k-1)$-free.

*Proof.* Let $w$ be $k/(k-1)$-free over $k$ letters. If $w[i] = w[i+d]$ with $d \ge 1$, the factor $w[i..i+d]$ has the period $d$ and length $d + 1$, so its exponent is at least $(d+1)/d$, and $(d+1)/d \ge k/(k-1)$ when $d \le k - 1$. So equal letters of $w$ are at distance at least $k$, and any $k$ consecutive letters of $w$ are distinct, that is, they are all $k$ letters. If $|w| \ge k + 1$, the letter $w[i+k]$ differs from $w[i+1], \ldots, w[i+k-1]$, which are all letters except $w[i]$, so $w[i+k] = w[i]$: $w$ has the period $k$. If $|w| \ge k + 2$, the factor $w[0..k+1]$ has the period $k$ and length $k + 2$, so its exponent is at least $(k+2)/k$, and $(k+2)/k \ge k/(k-1)$ because $(k+2)(k-1) - k^2 = k - 2 \ge 0$. This contradiction proves the first claim. In $a_1 \cdots a_k a_1$, the only factor with a repeated letter is the whole word, of smallest period $k$ and exponent $(k+1)/k < k/(k-1)$. $\square$

So $\mathrm{RT}(k) \ge k/(k-1)$ for every $k$, and every $k/(k-1)$-free word has length at most $k + 1$, the value of the statement for $k = 2$ and $k \ge 5$.

**Lemma 2 (three and four letters).** Every $7/4$-free ternary word has length at most 38, and every $7/5$-free word over four letters has length at most 121; both bounds are attained.

*Proof.* The $\alpha$-free words over $k$ letters form a tree under extension by one letter, closed under prefixes and under renaming the letters. A search of this tree, testing at each step the suffixes of the new word, which are the only new factors, ends: for $k = 3$ and $\alpha = 7/4$ the deepest words have length 38, and there are 18 of them, 3 up to renaming the letters; for $k = 4$ and $\alpha = 7/5$ the deepest have length 121, 2 up to renaming. Dejean and Pansiot carried out these finite checks for their thresholds. $\square$

**Lemma 3 (the Pansiot code).** Let $k \ge 3$ and let $w$ be a word over $k$ letters without factors of exponent at least $(k-1)/(k-2)$, which holds for $\mathrm{RT}(k)^+$-free words. Then any $k - 1$ consecutive letters of $w$ are distinct, and for $i \ge k - 1$ the letter $w[i]$ is either $w[i-k+1]$ or the unique letter missing from $w[i-k+1..i-1]$.

*Proof.* As in Lemma 1, equal letters at distance $d \le k - 2$ give a factor of exponent at least $(d+1)/d \ge (k-1)/(k-2)$. So $w[i]$ differs from the $k - 2$ letters before it, which leaves the two letters named. And $\mathrm{RT}(k) < (k-1)/(k-2)$, since $7/4 < 2$, $7/5 < 3/2$ and $k/(k-1) < (k-1)/(k-2)$. $\square$

So an $\mathrm{RT}(k)^+$-free word is fixed by its first $k - 1$ letters and a binary word that records, at each step, which of the two letters comes next. Pansiot introduced this code, and the constructions for $k \ge 4$ work with it.

**The upper bounds.**

- *$k = 2$.* The [Thue-Morse word](/thue-morse-word/) is [overlap-free](/overlap-free-word/), so it has no factor of exponent greater than 2 (Thue, 1912).
- *$k = 3$.* Dejean gave a 19-uniform morphism on three letters whose fixed point is $7/4^+$-free.
- *$k = 4$.* Pansiot gave a $7/5^+$-free word over four letters, built through its binary code.
- *$5 \le k \le 11$.* Moulin Ollagnier gave morphisms on Pansiot codes and checked by computer that their fixed points decode to $k/(k-1)^+$-free words.
- *$k \ge 33$.* Carpi gave a uniform construction for all large alphabets, again through the code.
- *The remaining sizes.* Mohammad-Noori and Currie treated $12 \le k \le 14$, Currie and Rampersad extended Carpi's method down to $k \ge 27$, and then Currie and Rampersad, and independently Rao, completed all remaining $k$ with morphisms whose correctness is checked by computer.

With Lemmas 1 and 2, each construction gives the exact value of $\mathrm{RT}(k)$, and the lengths of the longest $\mathrm{RT}(k)$-free words show that the threshold exponent itself cannot be avoided. $\blacksquare$

## Consequences

- **Thue's results.** For $k = 2$, every binary word of length 4 has a factor of exponent at least 2, a square, while the Thue-Morse word avoids all exponents above 2. Squares are avoidable on three letters, the [Thue theorem](/thue-theorem/), since $\mathrm{RT}(3) = 7/4 < 2$, and not on two.
- **The threshold tends to 1.** For $k \ge 5$, $k/(k-1)$ is the exponent of a block of $k - 1$ distinct letters followed by its first letter. Lemma 1 shows that such returns are forced, and the theorem shows that nothing longer is: with many letters, repetitions can be made as short as the counting argument allows.
- **Avoidable exponents.** An exponent $\alpha$ is avoidable on $k$ letters, in the sense that an infinite $\alpha$-free word exists, exactly when $\alpha > \mathrm{RT}(k)$. This answers the fractional-power case of [pattern avoidability](/avoidability/).
- **Binary structure.** By Lemma 3, every infinite $\mathrm{RT}(k)^+$-free word over $k \ge 3$ letters is a binary word in disguise. This is why the proofs for large $k$ reduce to building infinite binary words with suitable properties.

## Tightness

The lower and upper bounds meet exactly, and the threshold is sharp on both sides. Below it, the table gives the longest words; at it, infinite words exist.

| $k$ | $\mathrm{RT}(k)$ | longest $\mathrm{RT}(k)$-free word | infinite $\mathrm{RT}(k)^+$-free word |
|---|---|---|---|
| 2 | 2 | 3, e.g. `aba` | Thue-Morse word |
| 3 | 7/4 | 38 | Dejean's morphism |
| 4 | 7/5 | 121 | Pansiot's word |
| $k \ge 5$ | $k/(k-1)$ | $k + 1$, e.g. $a_1 \cdots a_k a_1$ | Moulin Ollagnier, Carpi, Currie and Rampersad, Rao |

The general bound $k/(k-1)$ of Lemma 1 is not the truth for $k = 3, 4$: it gives $3/2$ and $4/3$, while the thresholds are $7/4$ and $7/5$.

## History

Thue showed in 1912 that the binary threshold is 2. Dejean introduced the threshold for every alphabet in 1972, proved $\mathrm{RT}(3) = 7/4$, and conjectured $\mathrm{RT}(4) = 7/5$ and $\mathrm{RT}(k) = k/(k-1)$ for $k \ge 5$. Pansiot proved the case $k = 4$ in 1984 and introduced the binary code. Moulin Ollagnier proved $5 \le k \le 11$ in 1992. After a gap of fifteen years, Mohammad-Noori and Currie did $12 \le k \le 14$ and Carpi did $k \ge 33$ in 2007, and Currie and Rampersad brought the bound down to 27 in 2009. The remaining cases were closed by Currie and Rampersad and, independently, by Rao, both published in 2011.

## References
