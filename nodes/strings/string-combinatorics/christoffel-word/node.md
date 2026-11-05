---
tag: 2WCR5B
kind: definition
slug: christoffel-word
name: Christoffel word
aliases:
- lower Christoffel word
- digital straight segment word
area: strings/string-combinatorics
level: advanced
summary: A balanced word that is a Lyndon word, encoding the lattice path closest to a line.
prereqs: [lyndon-word, word-conjugacy]
see_also: [sturmian-word, fibonacci-word, stern-brocot-tree, fine-and-wilf-theorem, palindrome, bresenham-line-algorithm, abelian-complexity, continued-fraction]
sources:
  - book: isbn:9780821844809
    title: Jean Berstel, Aaron Lauve, Christophe Reutenauer and Franco V. Saliola, Combinatorics on Words, Christoffel Words and Repetitions in Words, CRM Monograph Series 27, American Mathematical Society, 2008
    locator: Part I, Christoffel words (the definition by a discretized line segment, the palindromic and Lyndon properties, the standard factorization, the Christoffel tree and the conjugates)
  - paper: doi:10.1016/s0304-3975(96)00101-6
    title: Jean Berstel and Aldo de Luca, Sturmian words, Lyndon words and trees, Theoretical Computer Science 178(1-2), 1997, 171-203
    locator: the Christoffel words as the balanced Lyndon words, central words and their two coprime periods, and the trees of Christoffel words
  - book: isbn:9780521812207
    title: M. Lothaire, Algebraic Combinatorics on Words, Cambridge University Press, 2002
    locator: Chapter 2, Sturmian words (J. Berstel and P. Séébold), mechanical words, balance, and the standard and Christoffel words
  - paper: "Elwin Bruno Christoffel, Observatio arithmetica, Annali di Matematica Pura ed Applicata, Serie 2, 6, 1875, 148-152"
    title: Elwin Bruno Christoffel, Observatio arithmetica
    locator: the first study of the words now named after Christoffel, through the residues of the multiples of an integer
---

A Christoffel word is the binary word that records how a lattice path follows a line segment from $(0, 0)$ to $(p, q)$, with coprime $p$ and $q$, staying just below it: each letter $a$ is a step to the right and each letter $b$ a step up. For $(p, q) = (4, 3)$ it is `aababab`. Christoffel words are exactly the binary [Lyndon words](/lyndon-word/) that are balanced, each one has the form $aPb$ with $P$ a [palindrome](/palindrome/), and their [conjugates](/word-conjugacy/) are the factors of the periodic Sturmian words. They are the finite building blocks of [Sturmian words](/sturmian-word/) and of digital straight lines.

## Definition

The alphabet is $\{a, b\}$ with $a < b$; the order matters for the Lyndon property and is used nowhere else. Indices are 0-based. Let $p, q \ge 0$ be integers with $\gcd(p, q) = 1$, and $n = p + q \ge 1$.

**Lower Christoffel word.** The lower Christoffel word of slope $q/p$ is the word $w = w[0..n-1]$ with
$$ w[i] = \begin{cases} a & \text{if } \lfloor (i+1)q/n \rfloor = \lfloor iq/n \rfloor, \\ b & \text{otherwise,} \end{cases} \qquad 0 \le i < n. $$
It has $p$ letters $a$ and $q$ letters $b$. Geometrically, it is the path of $n$ unit steps from $(0, 0)$ to $(p, q)$ that stays on or below the segment between them, with no lattice point strictly between the path and the segment.

**Upper Christoffel word.** It is defined the same way with ceilings instead of floors, and gives the path just above the segment.

The two trivial Christoffel words are $a$, for $(p, q) = (1, 0)$, and $b$, for $(0, 1)$; the others have $p, q \ge 1$ and length $n \ge 2$. "Christoffel word" with no qualifier means the lower one.

### Basic facts

1. **Balance.** The factor $w[i..i+m-1]$ has $\lfloor (i + m)q/n \rfloor - \lfloor iq/n \rfloor$ letters $b$, which is $\lfloor mq/n \rfloor$ or $\lfloor mq/n \rfloor + 1$. So any two factors of the same length differ by at most one in their numbers of $b$, and the same holds for the infinite periodic word $w^\infty$, whose factor at index $i$ has the same formula, since $\lfloor (x + n)q/n \rfloor = \lfloor xq/n \rfloor + q$.
2. **Form $aPb$ with $P$ a palindrome.** Let $n \ge 2$. Then $w[0] = a$, since $q < n$, and $w[n-1] = b$, since $\lfloor (n-1)q/n \rfloor = q - 1$. For $1 \le i \le n - 2$, the numbers $iq/n$ and $(i+1)q/n$ are not integers, since $\gcd(q, n) = 1$, and the identity $\lfloor (n - i)q/n \rfloor = q - \lceil iq/n \rceil$ gives
$$ w[n-1-i] = \text{the letter of } \lceil (i+1)q/n \rceil - \lceil iq/n \rceil = \text{the letter of } \lfloor (i+1)q/n \rfloor - \lfloor iq/n \rfloor = w[i]. $$
So $w = aPb$ with $P = w[1..n-2]$ a palindrome, called the central word.
3. **The upper word is the reversal.** The same identity, applied to every $i$, shows that the reversal of the lower Christoffel word is the upper Christoffel word, $bPa$. It is a conjugate of $aPb$.
4. **Lyndon property.** A lower Christoffel word $w$ of length $n \ge 2$ is a Lyndon word. *Proof.* It is primitive: if $w = z^e$, then $e$ divides both $p$ and $q$, so $e = 1$. Its rotation by $r$ is a factor of $w^\infty$, and its prefix of length $m$ has $\lfloor (r + m)q/n \rfloor - \lfloor rq/n \rfloor \ge \lfloor mq/n \rfloor$ letters $b$, the number in the prefix of length $m$ of $w$. At the first index $m$ where $w$ and the rotation differ, their prefixes of length $m + 1$ have different numbers of $b$, so $w$ has the $a$ and the rotation has the $b$. So $w$ is smaller than each of its other rotations, which are all different from $w$. $\square$
5. **Characterizations.** A binary word of length $n \ge 2$ is a lower Christoffel word if and only if it is a balanced Lyndon word (Berstel and de Luca). A binary word is a conjugate of a Christoffel word if and only if it is primitive and circularly balanced, that is, $ww$ is balanced.
6. **Counting.** For each $n \ge 2$ there is one Christoffel word for each $p$ with $1 \le p < n$ and $\gcd(p, n) = 1$, so $\varphi(n)$ of them, with $\varphi$ Euler's function.
7. **Standard factorization.** For $n \ge 2$, $w$ has a unique factorization $w = w_1 w_2$ into two Christoffel words, and $w_2$ is the longest proper suffix of $w$ that is a Lyndon word, as in the standard factorization of Lyndon words. The two factors satisfy $|w_1|_a |w_2|_b - |w_1|_b |w_2|_a = 1$.
8. **The Christoffel tree.** Starting from the pair $(a, b)$, the rule $(u, v) \mapsto (u, uv)$ and $(uv, v)$ produces every pair $(w_1, w_2)$ of fact 7 exactly once, and the products $uv$ are all the Christoffel words of length at least 2. The slopes follow the [Stern-Brocot tree](/stern-brocot-tree/), and the path to a word is given by the [continued fraction](/continued-fraction/) of $q/p$.
9. **Central words and Fine and Wilf.** For $n \ge 3$, the central word $P$ has the two coprime periods $|w_1|$ and $|w_2|$, and $|P| = |w_1| + |w_2| - 2$. So $P$ is an extremal case of the [Fine and Wilf theorem](/fine-and-wilf-theorem/): a word of length $r + s - 2$ with coprime periods $r, s$ that has not the period 1.

## Examples and non-examples

| $(p, q)$ | lower | upper | standard factorization |
|---|---|---|---|
| $(1, 1)$ | `ab` | `ba` | `a` $\cdot$ `b` |
| $(2, 1)$ | `aab` | `baa` | `a` $\cdot$ `ab` |
| $(1, 2)$ | `abb` | `bba` | `ab` $\cdot$ `b` |
| $(3, 2)$ | `aabab` | `babaa` | `aab` $\cdot$ `ab` |
| $(4, 3)$ | `aababab` | `bababaa` | `aabab` $\cdot$ `ab` |
| $(5, 2)$ | `aaabaab` | `baabaaa` | `aaab` $\cdot$ `aab` |
| $(5, 3)$ | `aabaabab` | `babaabaa` | `aab` $\cdot$ `aabab` |
| $(7, 4)$ | `aabaabaabab` | `babaabaabaa` | `aab` $\cdot$ `aabaabab` |

- For $(7, 4)$ the central word is $P = $ `abaabaaba`, a palindrome of length 9 with the coprime periods 3 and 8, and $9 = 3 + 8 - 2$.
- For $(4, 3)$ the letters $b$ are at the indices $i = 2, 4, 6$, where $\lfloor 3(i+1)/7 \rfloor$ steps from 0 to 1, 1 to 2, and 2 to 3.
- The 4 Christoffel words of length 5 are `aaaab`, `aabab`, `ababb`, `abbbb`, for $p = 4, 3, 2, 1$, and $\varphi(5) = 4$.
- The prefixes of length $F_k$ of the [Fibonacci word](/fibonacci-word/) are conjugates of Christoffel words whose slopes are ratios of consecutive Fibonacci numbers.

**Non-examples.**

- `aabb` is a Lyndon word but not balanced: the factors `aa` and `bb` differ by two in their numbers of $b$.
- `abab` is balanced but not primitive, so not a Lyndon word; a pair $(2, 2)$ is not coprime.
- `abaab` is balanced and primitive, but not a Lyndon word; it is a conjugate of the Christoffel word `aabab`.
- `aabbab` is not a conjugate of a Christoffel word: in `aabbabaabbab` the factors `aa` and `bb` differ by two in their numbers of $b$.

## Related definitions

- **[Sturmian words](/sturmian-word/).** The infinite aperiodic balanced words. The factors of a Sturmian word of slope $\alpha$ are limits of factors of Christoffel words whose slopes approach $\alpha$, and the standard words used to build characteristic Sturmian words are conjugates of Christoffel words.
- **Mechanical words.** The words $s[i] = \lfloor (i+1)\alpha + \rho \rfloor - \lfloor i\alpha + \rho \rfloor$; for rational $\alpha = q/n$ and $\rho = 0$ they are the powers of the lower Christoffel word.
- **Digital straight segments.** In image processing, the chain codes of digitized line segments are the factors of the periodic words $w^\infty$, as drawn by the [Bresenham line algorithm](/bresenham-line-algorithm/).
- **Central words and [palindromes](/palindrome/).** The words $P$ of fact 2; they are the palindromes with two coprime periods $r, s$ and length $r + s - 2$, and the prefixes of standard Sturmian words that are palindromes.
- **[Abelian complexity](/abelian-complexity/).** Balanced means Abelian complexity at most 2 at every length, which Christoffel words and their conjugates satisfy.

## References
