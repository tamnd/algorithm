---
tag: JYNM78
kind: definition
slug: uniquely-decodable-code
name: Uniquely decodable code
aliases:
- uniquely decipherable code
area: compression-and-coding/entropy-coding
level: intro
summary: A code whose concatenations of codewords parse in only one way. The Sardinas-Patterson test decides it; every prefix code is one, and McMillan shows they are no shorter.
prereqs: [prefix-code]
see_also: [kraft-inequality, variable-length-code, huffman-coding, unary-coding, trie]
sources:
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 5.1 (nonsingular, uniquely decodable and instantaneous codes, Table 5.1 and Figure 5.1) and Section 5.5 (Theorem 5.5.1, McMillan)
  - paper: doi:10.1109/TIT.1956.1056818
    title: Brockway McMillan, Two inequalities implied by unique decipherability, IRE Transactions on Information Theory 2(4), 1956
    locator: The inequality sum 2^(-l_i) <= 1 for a uniquely decipherable code
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 5, Symbol codes (unique decodability and the prefix property)
---

A code is uniquely decodable if every string of code letters is the concatenation of codewords in at most one way. Then a message can be recovered from its encoding, even though the codewords have different lengths and no separators. Every [prefix code](/prefix-code/) is uniquely decodable, but some uniquely decodable codes are not prefix codes: they can be decoded only with look-ahead, sometimes unbounded. The Sardinas-Patterson test decides unique decodability. McMillan's theorem shows that the larger class gives no shorter codes than prefix codes.

## Definition

Notation. $\Sigma$ is the source alphabet, of size $\sigma$. The code alphabet has $D$ letters, usually $\{0, 1\}$. A code is a map $C : \Sigma \to \{0, 1\}^*$, and its *extension* $C^*$ sends a message $x_1 \cdots x_n$ to $C(x_1) \cdots C(x_n)$. No probability model is needed.

**Definition.** $C$ is *uniquely decodable* if its extension $C^*$ is one-to-one: for any two different finite sequences of source symbols, the concatenations of their codewords are different.

Cover and Thomas (Section 5.1) put codes in four nested classes:

- **Singular** codes send two different symbols to the same codeword.
- **Nonsingular** codes have distinct codewords ($C$ is one-to-one), but $C^*$ may not be.
- **Uniquely decodable** codes have $C^*$ one-to-one.
- **Instantaneous** (prefix) codes have no codeword that is a prefix of another; they are decoded with no look-ahead.

Each class contains the next: instantaneous $\subset$ uniquely decodable $\subset$ nonsingular $\subset$ all codes. The table below, Table 5.1 of Cover and Thomas, shows one code from each class that is not in the next one.

| symbol | singular | nonsingular, not UD | UD, not instantaneous | instantaneous |
|---|---|---|---|---|
| 1 | 0 | 0 | 10 | 0 |
| 2 | 0 | 010 | 00 | 10 |
| 3 | 0 | 01 | 11 | 110 |
| 4 | 0 | 10 | 110 | 111 |

The second code is not uniquely decodable: $010$ is the codeword of 2, and also $C(3) C(1) = 01 \cdot 0$ and $C(1) C(4) = 0 \cdot 10$. The third code is uniquely decodable but needs look-ahead: after $11$, the decoder must count the zeros that follow to decide whether the first codeword is $11$ or $110$.

**Consequence: McMillan.** The codeword lengths $\ell_1, \ldots, \ell_\sigma$ of a uniquely decodable code satisfy $\sum_i D^{-\ell_i} \le 1$. Together with Kraft's construction, this says that every uniquely decodable code can be replaced by a prefix code with the same lengths. The proof, by powers of the Kraft sum, is on the [Kraft inequality](/kraft-inequality/) page.

### The Sardinas-Patterson test

Sardinas and Patterson (1953) gave a finite test. Let $\mathcal{C}$ be the set of codewords, and assume they are distinct and nonempty. For sets of strings $A$ and $B$, let $A^{-1} B = \{ w \ne \varepsilon : a w \in B \text{ for some } a \in A \}$, the nonempty "dangling suffixes" left when a word of $A$ is cut off the front of a word of $B$. Define

$$S_1 = \mathcal{C}^{-1} \mathcal{C}, \qquad S_{i+1} = \mathcal{C}^{-1} S_i \, \cup \, S_i^{-1} \mathcal{C}.$$

**Test.** $C$ is uniquely decodable if and only if no $S_i$ (for $i \ge 1$) contains a codeword.

Each $S_i$ is a set of suffixes of codewords, and there are at most $N = \sum_{c \in \mathcal{C}} |c|$ of these. So the sequence of sets repeats after finitely many steps, and the test stops. The implementation on this page computes the union of all the $S_i$ by breadth-first search over dangling suffixes, so each suffix is handled once. For each suffix it tries every codeword, so the time is $O(N \cdot |\mathcal{C}| \cdot L)$ with $L$ the longest codeword. It also keeps, for each suffix, the two partial parses that reach it, and so it returns an ambiguous string as a witness when the code is not uniquely decodable.

*Why the test works (sketch).* Suppose a string has two different parses. Cut off a common first codeword if there is one, so that the two parses start with different codewords $c \ne c'$, where $c$ is a proper prefix of $c'$. Follow the two parses from left to right. At each point where one parse is ahead of the other, the part by which it is ahead is a dangling suffix, and an induction on the number of codewords read shows that it lies in some $S_i$. At the end the two parses meet. Just before they meet, the parse that is behind reads a codeword equal to the current dangling suffix, so some $S_i$ contains a codeword. Conversely, if a codeword $c$ lies in $S_i$, the chain of cuts that produced it can be unwound into two parses of one string that start with different codewords. Cover and Thomas give the test as a problem in Chapter 5.

## Examples and non-examples

**Dangling suffixes in many rounds.** For $\mathcal{C} = \{0, 0010, 1001\}$, the test finds

$$S_1 = \{010\}, \; S_2 = \{10\}, \; S_3 = \{01\}, \; S_4 = \{1\}, \; S_5 = \{001\}, \; S_6 = \{0, 01\}.$$

$S_6$ contains the codeword 0, so the code is not uniquely decodable. The witness is the 10-bit string $0010010010$, which has the two parses $0010 \cdot 0 \cdot 1001 \cdot 0$ and $0 \cdot 0 \cdot 1001 \cdot 0010$. The code on this page checks by brute force that no shorter string has two parses. So unique decodability cannot be checked by looking only at pairs of codewords.

**Codes that are uniquely decodable but not prefix codes.**

- $\{0, 01\}$: every 1 belongs to the codeword before it. $S_1 = \{1\}$ and $S_2 = \emptyset$.
- $\{0, 01, 11\}$ is a *suffix code*: no codeword is a suffix of another, so it decodes from right to left. From left to right the decoder must wait until a run of ones ends.
- $\{10, 00, 11, 110\}$, the third code of the table: $S_1 = \{0\}$ (from $11$ and $110$), and every later $S_i$ is $\{0\}$ again, which is not a codeword.

**Non-examples.**

- $\{0, 1, 01\}$ is nonsingular but not uniquely decodable: $01 = 0 \cdot 1$. Its Kraft sum is $5/4$, so McMillan's theorem rules it out at once.
- $\{0, 01, 10\}$ has Kraft sum exactly 1 but is not uniquely decodable: $010 = 0 \cdot 10 = 01 \cdot 0$. The Kraft inequality is necessary, not sufficient.
- A code with the empty word as a codeword is never uniquely decodable, since the empty word can be inserted anywhere.
- Unique decodability of the infinite string is a different notion. A code can be uniquely decodable on finite messages but have two parses of one infinite string; the code $\{0, 01, 11\}$ does, on $0111\cdots$.

## Related definitions

- [Prefix codes](/prefix-code/) are the uniquely decodable codes that decode with no look-ahead.
- The [Kraft inequality](/kraft-inequality/) with McMillan's theorem gives the lengths that uniquely decodable codes can have.
- A code with *bounded delay* is one where a decoder always knows a codeword after reading at most $d$ more letters; the third code of the table has unbounded delay, and $\{0, 01\}$ has delay 1.
- A [variable-length code](/variable-length-code/) is any code with codewords of different lengths; unique decodability is the minimum condition for it to be useful.
- In the theory of formal languages, a set $\mathcal{C}$ is called a *code* exactly when it is uniquely decodable, that is, when the monoid generated by $\mathcal{C}$ is free over it.

## References
