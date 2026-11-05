---
tag: GA0RFN
kind: concept
slug: repetition-threshold
name: Repetition threshold
aliases:
- Dejean threshold
- critical exponent
area: strings/string-combinatorics
level: research
summary: The least exponent such that infinite words over k letters avoid repetitions beyond it.
prereqs: [square-free-word, overlap-free-word]
see_also: [dejean-theorem, thue-theorem, thue-morse-word, avoidability, keranen-theorem, fibonacci-word, maximal-repetition, morphic-word]
sources:
  - paper: "Françoise Dejean, Sur un théorème de Thue, Journal of Combinatorial Theory, Series A 13(1), 1972, 90-99"
    locator: the threshold 7/4 for three letters, the longest 7/4-free ternary word, and the conjecture RT(4) = 7/5 and RT(k) = k/(k-1) for k at least 5
  - paper: "Jean-Jacques Pansiot, A propos d'une conjecture de F. Dejean sur les répétitions dans les mots, Discrete Applied Mathematics 7(3), 1984, 297-311"
    locator: the proof that RT(4) = 7/5 and the binary coding of words in which every k - 1 consecutive letters are distinct
  - paper: "James D. Currie and Narad Rampersad, A proof of Dejean's conjecture, Mathematics of Computation 80(274), 2011, 1063-1070"
    locator: the remaining cases of Dejean's conjecture, completing the proof that RT(k) = k/(k-1) for k at least 5
  - paper: "Michaël Rao, Last cases of Dejean's conjecture, Theoretical Computer Science 412(27), 2011, 3010-3018"
    locator: an independent proof of the remaining cases of Dejean's conjecture by computer-checked morphisms
---

The repetition threshold $\mathrm{RT}(k)$ is the least exponent $\alpha$ such that some infinite word over $k$ letters has no factor of exponent greater than $\alpha$. Exponents here are fractional: a word of length $n$ with least period $p$ has exponent $n/p$, so squares have exponent 2 and `abacaba` has exponent $7/4$. Thue's work gives $\mathrm{RT}(2) = 2$, Dejean showed $\mathrm{RT}(3) = 7/4$ and conjectured $\mathrm{RT}(4) = 7/5$ and $\mathrm{RT}(k) = k/(k-1)$ for $k \ge 5$, and this [Dejean's theorem](/dejean-theorem/) was completed in 2011. The threshold measures how little repetition an infinite word can get away with on a given alphabet.

## In plain words

Any long enough string repeats itself somewhere: some stretch is followed by a copy of part of itself. The amount of repetition is measured by a ratio: how long the stretch is compared to the length of the block that repeats. A square, a block followed by a full copy, has ratio two; a block followed by half of a copy has ratio one and a half. With more letters available it is easier to keep this ratio small. The repetition threshold for a given number of letters is the smallest ratio you can promise never to exceed in an endless string. With two letters it is two, with three letters seven quarters, and with many letters it gets close to one.

## The idea

Let $\Sigma$ be an [alphabet](/alphabet/) of $k \ge 2$ letters; only equality of letters is used, and words are indexed from 0.

**Fractional powers.** A nonempty word $w$ of length $n$ with least [period](/string-period/) $p$ has *exponent* $e(w) = n/p$, and $w$ is then an $(n/p)$-power: $w = u^{\lfloor n/p \rfloor} u'$ with $|u| = p$ and $u'$ a prefix of $u$. For example $e(\texttt{abcab}) = 5/3$, $e(\texttt{abacaba}) = 7/4$ and $e(\texttt{alfalfa}) = 7/3$. For a real $\alpha > 1$, a word is *$\alpha$-free* if no factor has exponent $\ge \alpha$, and *$\alpha^+$-free* if no factor has exponent $> \alpha$. [Square-free](/square-free-word/) means 2-free, and [overlap-free](/overlap-free-word/) means $2^+$-free.

**Critical exponent and threshold.** The *critical exponent* of an infinite word $x$ is $E(x) = \sup \{ e(w) : w \text{ a factor of } x \}$, and
$$ \mathrm{RT}(k) = \inf \{ E(x) : x \text{ an infinite word over } k \text{ letters} \}. $$
For every $k \ge 2$ the infimum is attained: there is an infinite $\mathrm{RT}(k)^+$-free word over $k$ letters, while every sufficiently long word over $k$ letters has a factor of exponent at least $\mathrm{RT}(k)$. So $\mathrm{RT}(k)$ is the boundary between avoidable and unavoidable exponents, and the boundary exponent itself is avoidable only in its $^+$ form.

**The values.**

| $k$ | $\mathrm{RT}(k)$ | longest $\mathrm{RT}(k)$-free word | infinite $\mathrm{RT}(k)^+$-free word |
| --- | --- | --- | --- |
| 2 | $2$ | 3 | Thue (1912), the [Thue-Morse word](/thue-morse-word/) |
| 3 | $7/4$ | 38 | Dejean (1972) |
| 4 | $7/5$ | 121 | Pansiot (1984) |
| $k \ge 5$ | $k/(k-1)$ | $k + 1$ | Moulin-Ollagnier, Carpi, Currie and Rampersad, Rao |

The middle column was computed here by exhaustive backtracking: the longest binary 2-free word is `aba`; the longest ternary $7/4$-free words have length 38, for example `abacabcbacbcabacbabcacbacabcbacbcabaca`, whose largest exponent is $12/7$; and the longest quaternary $7/5$-free words have length 121. The same search found $\mathrm{RT}(k)^+$-free words of length 400 for $k = 2, 3, 4$ and of length 300 for $k = 5$, in agreement with the last column.

**The lower bound $k/(k-1)$.** Suppose a word over $k$ letters is $k/(k-1)$-free. A factor $a\,u\,a$ with $|u| = m$ has period at most $m + 1$, so exponent at least $(m+2)/(m+1)$, and $(m+2)/(m+1) < k/(k-1)$ forces $m > k - 2$. So two equal letters are at least $k$ positions apart: every $k$ consecutive letters are distinct, and each letter after the first $k$ must equal the letter $k$ positions back, the only one not among the previous $k - 1$. A word of length $k + 2$ of this form has period $k$ and exponent $(k+2)/k \ge k/(k-1)$. Hence no $k/(k-1)$-free word over $k$ letters is longer than $k + 1$, and $\mathrm{RT}(k) \ge k/(k-1)$. For $k = 3$ and $k = 4$ the threshold is strictly higher, as the finite searches of the table show: every ternary word of length 39 has a factor of exponent at least $7/4 > 3/2$, and every quaternary word of length 122 has one of exponent at least $7/5 > 4/3$.

**Upper bounds by morphisms.** The infinite words in the last column are images of fixed points of [morphisms](/morphic-word/), and freeness is proved by checking that the morphism cannot create a high power out of a short one, plus a finite check on short factors. Dejean used a 19-uniform morphism on three letters. Pansiot recoded a word in which every $k - 1$ consecutive letters are distinct as a binary word recording, at each step, which of the two possible letters comes next; Dejean's bound for large $k$ becomes a property of binary words, and all later proofs use this coding.

**Dejean's conjecture.** Dejean (1972) conjectured $\mathrm{RT}(4) = 7/5$ and $\mathrm{RT}(k) = k/(k-1)$ for $k \ge 5$. Pansiot proved the case $k = 4$ in 1984 and Moulin-Ollagnier the cases $5 \le k \le 11$ in 1992. Mohammad-Noori and Currie settled $12 \le k \le 14$, Carpi all $k \ge 33$, and the last cases were finished by Currie and Rampersad and, independently, by Rao, in papers published in 2011.

## Examples

- **Two letters.** Every binary word of length 4 contains a square, so $\mathrm{RT}(2) \ge 2$. The Thue-Morse word contains the square `0101` but no overlap, so $E = 2$ and $\mathrm{RT}(2) = 2$; the threshold is reached, but only in the $2^+$ form.
- **Three letters.** `abacaba` has period 4 and exponent $7/4$. Every ternary word of length 39 contains a factor of exponent at least $7/4$, yet an infinite ternary word with no factor of exponent above $7/4$ exists. The square-free ternary word of [Thue's theorem](/thue-theorem/) has critical exponent at most 2, which is far from optimal.
- **Five letters.** With $k = 5$ the bound is $5/4$: the word `abcdea` has exponent $6/5 < 5/4$, but `abcdeab` has exponent $7/5$, and the argument above shows that every five-letter word of length 7 contains a factor of exponent at least $5/4$.
- **Critical exponents of famous words.** The [Fibonacci word](/fibonacci-word/) has critical exponent $2 + \varphi \approx 3.618$, with $\varphi$ the golden ratio, by Mignosi and Pirillo (1992); its prefix of length 300 has largest exponent $197/55 \approx 3.58$. The Thue-Morse word has critical exponent 2.

## Where it is used

- **Avoidability.** The threshold is the fractional version of the question of which repetitions can be avoided on a given alphabet, part of [avoidability](/avoidability/) theory, together with abelian powers ([Keränen's theorem](/keranen-theorem/)) and patterns.
- **Counting repetition-free words.** Near the threshold the number of free words changes behavior: on two letters, Karhumäki and Shallit (2004) showed that the number of $\alpha$-free words of length $n$ grows polynomially for $2 < \alpha \le 7/3$ and exponentially for $\alpha > 7/3$.
- **Measuring repetitiveness.** The largest exponent of a finite string is the largest exponent of its [maximal repetitions](/maximal-repetition/), which can be computed in linear time from its runs; the critical exponent is the infinite version.
- **Variants.** Repetition thresholds are studied for restricted classes of words, such as circular words, Sturmian words, rich words and words over $k$ letters with few distinct squares, and for abelian repetitions; each asks for the least exponent that an infinite word of the class must reach.
- **Computer proofs.** The proofs of Dejean's conjecture were among the first large results in combinatorics on words to rely on computer checks of morphisms, and tools for automatic sequences now decide critical exponents of automatic words mechanically.

## References
