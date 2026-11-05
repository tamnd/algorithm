---
tag: 0SD3QG
kind: theorem
slug: sturmian-characterization
name: Sturmian characterization theorem
aliases:
- Sturmian words as mechanical words
area: strings/string-combinatorics
level: advanced
summary: Sturmian words are exactly the aperiodic balanced words and the mechanical words.
prereqs: [sturmian-word, morse-hedlund-theorem]
see_also: [subword-complexity, fibonacci-word, christoffel-word, continued-fraction, abelian-complexity, palindrome, de-bruijn-graph, euler-totient]
sources:
  - book: isbn:9780521812207
    title: M. Lothaire, Algebraic Combinatorics on Words, Encyclopedia of Mathematics and its Applications 90, Cambridge University Press, 2002
    locator: Chapter 2, Sturmian words (J. Berstel and P. Séébold), Section 2.1, equivalent definitions (balanced aperiodic words, mechanical words of irrational slope, words of complexity n + 1)
  - paper: "Marston Morse and Gustav A. Hedlund, Symbolic dynamics II. Sturmian trajectories, American Journal of Mathematics 62(1), 1940, 1-42"
    locator: Sturmian trajectories as balanced sequences and their representation by rotations of the circle
  - paper: "Ethan M. Coven and Gustav A. Hedlund, Sequences with minimal block growth, Mathematical Systems Theory 7, 1973, 138-153"
    locator: the proof that the aperiodic sequences with n + 1 blocks of length n are the Sturmian sequences
  - book: isbn:9780521823326
    title: Jean-Paul Allouche and Jeffrey Shallit, Automatic Sequences, Cambridge University Press, 2003
    locator: Chapter 10, Subword complexity (the section on Sturmian words), and Chapter 9, Characteristic words
---

The Sturmian characterization theorem says that three classes of infinite binary words coincide: the words with exactly $n + 1$ factors of each length $n$, the balanced words that are not ultimately periodic, and the mechanical words with irrational slope. The first is a counting condition, the second a combinatorial one, and the third a geometric one, the coding of a line or of a rotation of the circle. The theorem goes back to Morse and Hedlund (1940) and Coven and Hedlund (1973), and it is why the three conditions are used interchangeably to define [Sturmian words](/sturmian-word/).

## Statement

Words are over the binary [alphabet](/alphabet/) $\{0, 1\}$, and an infinite word $x = x[0]\,x[1] \cdots$ is indexed from 0. For a finite word $u$, the *height* $h(u) = |u|_1$ is its number of 1s. $F_n$ is the set of factors of $x$ of length $n$ and $p_x(n) = |F_n|$. A word is *balanced* if $|h(u) - h(v)| \le 1$ for all factors $u, v$ with $|u| = |v|$. For $0 \le \alpha \le 1$ and real $\rho$, the lower and upper mechanical words are
$$ s_{\alpha,\rho}[n] = \lfloor (n+1)\alpha + \rho \rfloor - \lfloor n\alpha + \rho \rfloor, \qquad s'_{\alpha,\rho}[n] = \lceil (n+1)\alpha + \rho \rceil - \lceil n\alpha + \rho \rceil . $$

**Theorem.** For an infinite binary word $x$ the following are equivalent.

1. $x$ is Sturmian: $p_x(n) = n + 1$ for every $n \ge 0$.
2. $x$ is balanced and not ultimately periodic.
3. $x = s_{\alpha,\rho}$ or $x = s'_{\alpha,\rho}$ for some irrational $\alpha \in (0, 1)$ and some real $\rho$.

The slope $\alpha$ in (3) is unique: it is the frequency of the letter 1 in $x$, the limit of $h(x[0..n-1])/n$.

## In plain words

Draw a straight line across squared paper and write a 1 each time it climbs past a horizontal grid line during a unit step to the right, and a 0 otherwise. If the slope is not a fraction, the resulting endless word never repeats. The theorem says that three very different descriptions give exactly the same words. The first counts patterns: for each width there is just one more pattern than the width. The second spreads the ones evenly: any two stretches of the same length hold numbers of ones that differ by at most one, and the word never falls into a cycle. The third is the line itself. So a word with the fewest possible patterns for a non-repeating word must come from a line, and a word that spreads its ones as evenly as possible without repeating must too.

## Proof

Write $H(i) = h(x[0..i-1])$ for the height of the prefix of length $i$, so $h(x[i..j-1]) = H(j) - H(i)$. A factor $u$ is *right special* if $u0$ and $u1$ are both factors. Since $x$ is infinite, every factor of length $n$ is followed by at least one letter, so
$$ p_x(n+1) - p_x(n) = \text{the number of right special factors of length } n. \tag{$*$} $$

**(2) ⇒ (1).** Suppose $x$ is balanced and $u \ne v$ are right special factors of length $n$. Let $w$ be their longest common suffix; then $u$ ends with $aw$ and $v$ with $bw$ for letters $a \ne b$. Since $u0, u1, v0, v1$ are factors, so are $aw0, aw1, bw0, bw1$, and in particular $0w0$ and $1w1$, whose heights differ by 2. This contradicts balance, so there is at most one right special factor of each length, and by $(*)$, $p_x(n) \le p_x(0) + n = n + 1$. Since $x$ is not ultimately periodic, $p_x(n) \ge n + 1$ by the [Morse-Hedlund theorem](/morse-hedlund-theorem/). So $p_x(n) = n + 1$.

**(3) ⇒ (2).** For $a, b$ real, $\lfloor a + b \rfloor - \lfloor a \rfloor \in \{\lfloor b \rfloor, \lfloor b \rfloor + 1\}$, and similarly for ceilings. For $x = s_{\alpha,\rho}$ the factor $x[i..i+n-1]$ has height $\lfloor (i+n)\alpha + \rho \rfloor - \lfloor i\alpha + \rho \rfloor$, which takes only the two values $\lfloor n\alpha \rfloor$ and $\lfloor n\alpha \rfloor + 1$; so $x$ is balanced, and the same holds for $s'_{\alpha,\rho}$. The height of every factor of length $n$ also lies within distance 2 of $n\alpha$. If $x[t] = x[t + q]$ for all $t \ge i_0$, then $h(x[i_0..i_0 + jq - 1]) = jg$ with $g = h(x[i_0..i_0 + q - 1])$, so $|jg - jq\alpha| \le 2$ for every $j \ge 1$, which forces $\alpha = g/q$. As $\alpha$ is irrational, $x$ is not ultimately periodic.

**(2) ⇒ (3).** Let $x$ be balanced and not ultimately periodic.

*Step 1: the slope.* Let $a_n$ and $b_n$ be the least and greatest heights of factors of length $n$; by balance $b_n \le a_n + 1$. A factor of length $n + m$ is a factor of length $n$ followed by one of length $m$, so $a_{n+m} \ge a_n + a_m$ and $b_{n+m} \le b_n + b_m$. By Fekete's lemma $a_n/n$ converges to $\sup_n a_n/n$ and $b_n/n$ to $\inf_n b_n/n$; since $|b_n - a_n| \le 1$ the two limits are equal, to some $\alpha \in [0, 1]$, and $a_n \le n\alpha \le b_n$. So every factor $u$ of length $n$ satisfies $n\alpha - 1 \le h(u) \le n\alpha + 1$.

*Step 2: $\alpha$ is irrational.* Suppose $\alpha = r/q$ in lowest terms. If some factor of length $q$ has height $r + 1$, then by balance all have height $r$ or $r + 1$. Fix a residue $c$ modulo $q$ and look at the blocks $x[i..i+q-1]$ with $i \equiv c$. Any $j$ consecutive such blocks form a factor of length $jq$, whose height is at most $jq\alpha + 1 = jr + 1$, so at most one block in each residue class has height $r + 1$. The case of height $r - 1$ is symmetric. Hence beyond some position $N$ every factor of length $q$ has height exactly $r$, and then $x[i + q] - x[i] = h(x[i+1..i+q]) - h(x[i..i+q-1]) = 0$ for $i \ge N$: $x$ is ultimately periodic, a contradiction. So $\alpha$ is irrational, $0 < \alpha < 1$, and $n\alpha$ is never an integer for $n \ge 1$, so the inequalities of Step 1 are strict for $|u| \ge 1$.

*Step 3: the intercept.* Let $D(i) = H(i) - i\alpha$ for $i \ge 0$. For $i < j$, $D(j) - D(i) = h(x[i..j-1]) - (j - i)\alpha$, so $|D(i) - D(j)| < 1$ for all $i, j$. Let $\delta = \sup_i D(i)$ and $\gamma = \inf_i D(i)$; then $\gamma \le D(0) = 0 \le \delta$ and $\delta - \gamma \le 1$, and if $\delta - \gamma = 1$ then $\delta$ and $\gamma$ are not both attained.

- If $\delta - \gamma < 1$, or $\delta - \gamma = 1$ and $\gamma$ is not attained, put $\rho = \delta$. Then $D(i) \le \rho < D(i) + 1$ for every $i$, so $i\alpha + \rho \in [H(i), H(i) + 1)$ and $H(i) = \lfloor i\alpha + \rho \rfloor$. Since $0 \le \rho < 1$, $H(0) = 0 = \lfloor \rho \rfloor$, and $x[n] = H(n+1) - H(n) = s_{\alpha,\rho}[n]$.
- Otherwise $\delta - \gamma = 1$ and $\delta$ is not attained; put $\rho = \gamma$. Then $D(i) - 1 < \rho \le D(i)$, so $H(i) = \lceil i\alpha + \rho \rceil$, with $-1 < \rho \le 0$, and $x = s'_{\alpha,\rho}$.

**(1) ⇒ (2).** Let $x$ be Sturmian. It is not ultimately periodic by the Morse-Hedlund theorem, since $p_x(n) > n$ for all $n$. Three facts are needed.

*Fact A: $x$ is recurrent.* For any $N$, the suffix $x[N..]$ is not ultimately periodic, so it has at least $n + 1$ factors of length $n$; they are factors of $x$, which has only $n + 1$. So every factor of $x$ occurs at some position $\ge N$, for every $N$.

*Fact B: a minimal unbalanced pair.* Suppose $x$ is not balanced, let $m$ be the least length with factors $u, v \in F_m$ and $h(u) - h(v) = 2$, and fix such $u, v$. Removing the first letters leaves factors of length $m - 1$ whose heights differ by at most 1, so $u$ starts with 1 and $v$ with 0; likewise for the last letters. Write $u = 1u'1$ and $v = 0v'0$, so $h(u') = h(v')$. If $u' \ne v'$, let $z$ be their longest common prefix. If $u' = z1s$ and $v' = z0t$, the prefixes $1z1$ of $u$ and $0z0$ of $v$ are shorter than $m$ with heights differing by 2. If $u' = z0s$ and $v' = z1t$, then $h(s) = h(t) + 1$ and the suffixes $s1$ of $u$ and $t0$ of $v$ are shorter than $m$ with heights differing by 2. Both contradict the choice of $m$, so $u' = v' =: w$. Finally $w$ is a [palindrome](/palindrome/): otherwise $w = y\,a\,z\,b\,\tilde y$ with $\tilde y$ the reversal of $y$ and $a \ne b$. If $a = 1$, the prefix $1y1$ of $u$ and the suffix $0\tilde y 0$ of $v$ have heights differing by 2, and if $a = 0$ the prefix $0y0$ of $v$ and the suffix $1\tilde y 1$ of $u$ do; both are shorter than $m$. So $0w0$ and $1w1$ are factors, with $w$ a palindrome of length $k = m - 2$.

*Fact C: the Rauzy graph of order $k$.* Let $G_k$ be the directed graph with vertex set $F_k$ and, for each factor of length $k + 1$, an edge from its prefix of length $k$ to its suffix of length $k$; reading $x$ is a walk in it. It has $k + 1$ vertices and $k + 2$ edges. Every vertex has an outgoing edge because $x$ is infinite and an incoming edge by Fact A. The vertex $w$ has two outgoing edges, $w0$ and $w1$, and two incoming edges, $0w$ and $1w$. Counting edges, every other vertex has exactly one incoming and one outgoing edge. So the walk that leaves $w$ by $wb$ is forced until it returns to $w$, and it cannot repeat another vertex first, because a first repeated vertex would have two incoming edges. These two closed walks, $C_0$ and $C_1$, share no edge, since a shared edge would force, edge by edge backwards through vertices with one incoming edge, the shared first edge $w0 = w1$; so their lengths satisfy $\ell_0 + \ell_1 \le k + 2$. Let $r_b$ be the $\ell_b$ letters read along $C_b$, so $r_b$ starts with $b$, $w\,r_b$ ends with $w$, and the last edge of $C_b$ is $c_b w$, where $c_b$ is the letter just before that final $w$. The last edges of $C_0$ and $C_1$ are the two edges into $w$, so $\{c_0, c_1\} = \{0, 1\}$. A factor of length $k + 2$ is a walk of two edges, determined by its middle vertex and its two edges. A vertex other than $w$ is the middle of exactly one such factor, by Fact A, so
$$ p_x(k+2) = k + \bigl|\{(a, b) : a\,w\,b \in F_{k+2}\}\bigr| . $$

*Case $c_0 = 0$ and $c_1 = 1$.* After its first visit to $w$, the walk of $x$ is a sequence of copies of $C_0$ and $C_1$, and a factor $a\,w\,b$ arises exactly when a copy of $C_a$ is followed by a copy of $C_b$. Both cycles occur infinitely often, otherwise $x$ would be ultimately periodic, so there are switches from $C_0$ to $C_1$ and back, giving $0w1$ and $1w0$. With $0w0$ and $1w1$ this makes four pairs, and $p_x(k+2) = k + 4$, a contradiction.

*Case $c_0 = 1$ and $c_1 = 0$.* If $\ell_0 \ge k + 1$, then $\ell_1 \ge 1$ forces $\ell_0 = k + 1$, and the last edge of $C_0$ is $r_0$ itself; but it starts with $c_0 = 1$, while $r_0$ starts with 0. So $\ell_0 \le k$. Then $w\,r_0 = y\,w$ with $|y| = \ell_0$, so $(w\,r_0)[\ell_0 - 1] = c_0 = 1$ and this letter lies in the first copy of $w$: $w[\ell_0 - 1] = 1$. Also $r_0[0] = (w\,r_0)[k] = w[k - \ell_0]$, since the final copy of $w$ starts at index $\ell_0$; so $w[k - \ell_0] = 0$. Because $w$ is a palindrome, $w[\ell_0 - 1] = w[k - \ell_0]$, a contradiction.

So $x$ is balanced. **Uniqueness of the slope.** In (3), the height of the prefix of length $n$ is within 2 of $n\alpha$, so $\alpha = \lim H(n)/n$, the frequency of 1. $\blacksquare$

**Checks.** By exhaustive search over all binary words of length at most 16: every balanced word has at most one right special factor of each length, and in every unbalanced word each pair of factors of the least unbalanced length with heights differing by 2 has the form $1w1$, $0w0$ with $w$ a palindrome, as in Fact B. For every word $v^\omega$ with $1 \le |v| \le 16$, whenever $p(j) = j + 1$ for all $j \le n$, the factors of length at most $n$ are balanced, which is the finite form of the argument of Fact C. For $n \le 11$, the windows of length $n$ of 30000 random mechanical words, together with $0^n$ and $1^n$, are exactly the balanced words of length $n$.

## Consequences

- **Complexity of a rotation.** For irrational $\alpha$, $s_{\alpha,\rho}[n] = 1$ exactly when the fractional part of $n\alpha + \rho$ lies in $[1 - \alpha, 1)$. The factor of length $n$ at position $i$ is determined by which of the $n + 1$ arcs cut out by the points $-j\alpha \bmod 1$, $0 \le j \le n$, contains $i\alpha + \rho \bmod 1$. The orbit is dense, so every arc is visited and the set of factors depends only on $\alpha$, not on $\rho$.
- **Recurrence and reversal.** Sturmian words are recurrent (Fact A); in fact uniformly recurrent, and their set of factors is closed under reversal, both of which follow from the rotation picture.
- **Finite balanced words.** A finite binary word is balanced if and only if it is a factor of a Sturmian word, and there are $1 + \sum_{i=1}^{n} (n - i + 1)\varphi(i)$ of length $n$, with $\varphi$ the [Euler totient](/euler-totient/). The [Christoffel words](/christoffel-word/) are among them.
- **Abelian complexity.** A Sturmian word has exactly two heights among its factors of each length $n \ge 1$, so its [abelian complexity](/abelian-complexity/) is the constant 2.
- **Characteristic words and continued fractions.** Taking $\rho = \alpha$ gives the characteristic word $c_\alpha$, whose prefixes are built from the [continued fraction](/continued-fraction/) of $\alpha$; the [Fibonacci word](/fibonacci-word/) is $c_\alpha$ for $\alpha = (3 - \sqrt5)/2$.
- **Geometry.** Cutting sequences of lines of irrational slope through the square grid, billiard trajectories in a square, and digital straight lines in image analysis are Sturmian words or their finite factors.

## Tightness

- **Aperiodicity in (2).** The words $(01)^\omega$ and $1\,0^\omega$ are balanced but ultimately periodic, with $p(n) = 2$ for $n \ge 1$.
- **Irrational slope in (3).** A mechanical word of rational slope $r/q$ is periodic with period $q$.
- **Both mechanical forms.** The upper form cannot be dropped: $1\,c_\alpha = s'_{\alpha,0}$ is Sturmian, but it is not $s_{\alpha,\rho}$ for any $\rho$, since that would need $\lfloor i\alpha + \rho \rfloor - \lfloor \rho \rfloor = \lceil i\alpha \rceil$ for all $i \ge 1$, that is, the fractional part of $\rho$ at least $1 - \{i\alpha\}$ for all $i \ge 1$, and these values come arbitrarily close to 1.
- **Recurrence in the local argument.** Fact C uses that every factor occurs again later. Without it the finite implication fails: $110^\omega$ has $p(1) = 2$ and $p(2) = 3$, yet its factors `11` and `00` are unbalanced.
- **Two letters.** Over three or more letters $p(1) \ge 3$, so condition (1) is impossible, and the analogues are the Arnoux-Rauzy and episturmian words, which are not all balanced.

## History

Sequences of this kind appear in Johann Bernoulli's work on continued fractions in astronomy (1772), in Christoffel's arithmetic observation of 1875 and in Markov's work of 1882. Morse and Hedlund (1940) named Sturmian trajectories after Sturm's comparison theorem, studied them as balanced sequences and represented them by rotations of the circle. Coven and Hedlund (1973) proved that the aperiodic sequences of complexity $n + 1$ are exactly these words. The proof given here follows the classical route through balanced words and the slope, with the Rauzy graph argument for the implication from complexity to balance.

## References
