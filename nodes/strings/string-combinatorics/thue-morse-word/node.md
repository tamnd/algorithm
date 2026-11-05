---
tag: 1J9MD5
kind: definition
slug: thue-morse-word
name: Thue-Morse word
aliases:
- Prouhet-Thue-Morse word
area: strings/string-combinatorics
level: core
summary: The fixed point of the morphism a to ab, b to ba; it is overlap-free and cube-free.
prereqs: [overlap, string-morphism]
see_also: [overlap-free-word, thue-theorem, morphic-word, square-free-word, repetition-threshold, subword-complexity, cube, fibonacci-word]
sources:
  - paper: doi:10.1007/978-1-4471-0551-0_1
    title: Jean-Paul Allouche and Jeffrey Shallit, The ubiquitous Prouhet-Thue-Morse sequence, in Sequences and their Applications (SETA '98), Springer, 1999, 1-16
    locator: the whole survey (definitions, the overlap-free property, the Prouhet problem and the history of the sequence)
  - book: isbn:9780521823326
    title: Jean-Paul Allouche and Jeffrey Shallit, Automatic Sequences, Cambridge University Press, 2003
    locator: Chapter 1, Stringology (the Thue-Morse sequence and the proof that it is overlap-free), and Chapter 5, Automatic sequences (the Thue-Morse sequence as a 2-automatic sequence)
  - book: isbn:9780521599245
    title: M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997
    locator: Chapter 2, Square-free words (J. Berstel and C. Reutenauer), the Thue-Morse word, its overlap-freeness and the square-free word derived from it
  - paper: "Axel Thue, Über die gegenseitige Lage gleicher Teile gewisser Zeichenreihen, Norske Vid. Selsk. Skr. I. Mat.-Nat. Kl. Christiania 1, 1912, 1-67; English translation in J. Berstel, Axel Thue's papers on repetitions in words: a translation, Publications du LaCIM 20, Université du Québec à Montréal, 1995"
    locator: the construction of the word by the substitution a to ab, b to ba and the proof that it has no overlap
---

The Thue-Morse word is the infinite binary word $t = 0110100110010110\cdots$ whose letter $t_n$ is the parity of the number of ones in the binary expansion of $n$. It is the fixed point starting with $0$ of the [morphism](/string-morphism/) $\mu$ with $0 \mapsto 01$ and $1 \mapsto 10$ (written $a \mapsto ab$, $b \mapsto ba$ over the letters $a$, $b$). Thue proved in 1912 that it contains no [overlap](/overlap/) $axaxa$, and so no [cube](/cube/), which makes it the standard example of an infinite [overlap-free word](/overlap-free-word/) on two letters.

## Definition

The alphabet is $\{0, 1\}$; the letters $a$ and $b$ of other texts are $0$ and $1$ here. Indices are 0-based, and $\bar{x}$ is the word $x$ with $0$ and $1$ exchanged.

**Thue-Morse word.** $t = t_0 t_1 t_2 \cdots$ with
$$ t_n = s_2(n) \bmod 2, $$
where $s_2(n)$ is the number of ones in the binary expansion of $n$.

**Four equivalent descriptions.**

1. *Recurrence.* $t_0 = 0$, $t_{2n} = t_n$ and $t_{2n+1} = 1 - t_n$.
2. *Doubling.* With $T_0 = 0$ and $T_{k+1} = T_k \overline{T_k}$, the word $T_k$ is the prefix of length $2^k$ of $t$.
3. *Morphism.* $T_k = \mu^k(0)$ for $\mu(0) = 01$, $\mu(1) = 10$, and $\mu(t) = t$: $t$ is the fixed point $\mu^\infty(0)$.
4. *Block form.* Each block $t_{2n} t_{2n+1}$ is $01$ or $10$, and it equals $\mu(t_n)$.

*Proof.* Appending a bit $0$ to the binary expansion of $n$ keeps the number of ones, and appending $1$ adds one, which gives (1). For (2), the numbers $2^k \le m < 2^{k+1}$ have one more leading one than $m - 2^k$, so $t_m = 1 - t_{m - 2^k}$, and the second half of $t_0 \cdots t_{2^{k+1}-1}$ is the complement of the first. For (3) and (4), (1) says $t_{2n} t_{2n+1} = t_n \overline{t_n} = \mu(t_n)$, so $\mu(t_0 \cdots t_{m-1}) = t_0 \cdots t_{2m-1}$ for every $m$, hence $\mu(t) = t$ and $\mu^k(0) = \mu^k(t_0) = t_0 \cdots t_{2^k - 1} = T_k$. $\square$

**The overlap-free property.** $t$ contains no overlap, that is, no factor $cxcxc$ with $c$ a letter.

The proof rests on a lemma: a binary word $w$ is overlap-free if and only if $\mu(w)$ is overlap-free.

*Proof of the lemma.* If $w$ contains an overlap $cxcxc$, then $\mu(w)$ contains $\mu(c x c x c) = (\mu(c)\mu(x))^2 \mu(c)$, which has period $2|cx|$ and length $4|cx| + 2$, so it has exponent more than 2 and contains an overlap (see [overlap](/overlap/), condition 2). Conversely, let $s = \mu(w)$ contain an overlap $s[i..i+2p]$ with period $p$, and recall that $s$ is made of the blocks $s[2j]s[2j+1] = \mu(w[j])$, each $01$ or $10$.

*Case $p$ odd.* For $i \le r \le i + p - 1$, both pairs $(r, r+1)$ and $(r + p, r + p + 1)$ lie in the overlap, and $s[r] = s[r+p]$, $s[r+1] = s[r+p+1]$. Since $p$ is odd, $r$ and $r + p$ have different parities, so one of the two pairs is a block, whose two letters differ. Hence $s[r] \ne s[r+1]$ for $i \le r \le i + p - 1$, and by the period the same holds up to $r = i + 2p - 1$. So the letters of the overlap alternate, and with $p$ odd this gives $s[i+p] \ne s[i]$, a contradiction.

*Case $p = 2q$ even, $i$ even.* Let $j = i/2$. The factor $s[i..i+2p-1]$ is $\mu(w[j..j+2q-1])$, and the period $2q$ says $\mu(w[j..j+q-1]) = \mu(w[j+q..j+2q-1])$, so $w[j..j+q-1] = w[j+q..j+2q-1] = y$, because $\mu$ is injective on letters. The letter $s[i+2p] = s[i]$ is the first letter of the block $\mu(w[j+2q])$, and the first letter of a block determines it, so $w[j+2q] = w[j] = y[0]$. Then $w[j..j+2q] = y\,y\,y[0]$ is an overlap in $w$.

*Case $p = 2q$ even, $i$ odd.* Let $j = (i+1)/2$. As before $s[i+1..i+2p]$ is $\mu(w[j..j+2q-1])$ and gives $w[j..j+q-1] = w[j+q..j+2q-1] = y$. The letter $s[i] = s[i+p]$ is the second letter of the block $\mu(w[j-1])$ and of the block $\mu(w[j+q-1])$, and the second letter also determines the block, so $w[j-1] = y[q-1]$. Writing $y = x c$ with $c = y[q-1]$, the factor $w[j-1..j+2q-1] = c\,x c\,x c$ is an overlap in $w$. $\square$

*Proof of the property.* The word $0$ is overlap-free, so by the lemma and induction every $T_k = \mu^k(0)$ is overlap-free. Each factor of $t$ lies in some prefix $T_k$. $\square$

**Consequences.**

- *Cube-free.* A cube $uuu$ contains the overlap $u u c$, with $c$ the first letter of $u$.
- *Not ultimately periodic.* An ultimately periodic word $v\,u u u \cdots$ contains the cube $uuu$.
- *Uniformly recurrent.* Every factor occurs in every long enough window: a factor $u$ lies in some $T_m$, and $t$ is a concatenation of aligned blocks $T_{m+1} = T_m \overline{T_m}$ and $\overline{T_{m+1}} = \overline{T_m} T_m$, both containing $T_m$, so $u$ occurs in every window of length $2^{m+2}$.

## Examples and non-examples

- **Prefixes.** $T_1 = 01$, $T_2 = 0110$, $T_3 = 01101001$, $T_4 = 0110100110010110$, and the prefix of length 32 is `01101001100101101001011001101001`.
- **Squares occur.** $t$ is not square-free: it contains `00`, `11`, `0101`, `1010`, `010010`, `101101`, `01100110` and `10011001`. Binary words cannot avoid squares at all beyond length 3, so overlaps are the strongest repetitions that a binary word can avoid.
- **Factor counts.** The numbers of distinct factors of lengths $1, 2, \ldots, 16$ are $2, 4, 6, 10, 12, 16, 20, 22, 24, 28, 32, 36, 40, 42, 44, 46$. The growth is linear in the length, as for every fixed point of a uniform morphism; see [subword complexity](/subword-complexity/).
- **The Prouhet partition.** Split $\{0, \ldots, 2^k - 1\}$ by the value of $t_i$. The two parts have equal sums of $j$-th powers for every $j < k$. For $k = 3$ the parts are $\{0, 3, 5, 6\}$ and $\{1, 2, 4, 7\}$: both sum to 14, and the squares sum to 70.
- **Non-example: the Fibonacci word.** The [Fibonacci word](/fibonacci-word/) $f = 0100101001001\cdots$, the fixed point of $0 \mapsto 01$, $1 \mapsto 0$, is not overlap-free: it contains the overlap `01010` at position 3 and the cube $(010)^3 = $ `010010010` at position 5.

## Related definitions

- **Overlap-free word.** A word with no factor $cxcxc$; $t$ is the basic infinite example, and by a lemma of Restivo and Salemi every binary overlap-free word is, up to a few letters at each end, the image under $\mu$ of a shorter overlap-free word. See [overlap-free word](/overlap-free-word/).
- **Square-free ternary word.** Counting the ones between consecutive zeros of $t$ gives the word $2102012\cdots$ over $\{0, 1, 2\}$, which is square-free; see [Thue's theorem](/thue-theorem/).
- **Repetition threshold.** $t$ shows that binary words can avoid every exponent above 2, so the [repetition threshold](/repetition-threshold/) of two letters is 2.
- **Morphic and automatic words.** $t$ is a pure [morphic word](/morphic-word/), the fixed point of a 2-uniform morphism, and so a 2-automatic sequence: a finite automaton reading the binary expansion of $n$ outputs $t_n$.

## References
