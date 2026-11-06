---
tag: 938SQX
kind: theorem
slug: valiant-lee-theorem
name: Valiant-Lee theorem
aliases:
- Lee's theorem
area: automata-and-parsing/context-free-parsing
level: research
summary: Computing all constituents of a string under a CFG and Boolean matrix multiplication reduce to each other, so a parser in time O(|G| n^(3-ε)) gives matrix multiplication in time O(m^(3-ε/3)).
prereqs: [valiant-algorithm, boolean-matrix-multiplication, cyk-algorithm]
see_also: [cfg-parsing-problem, context-free-language-recognition, combinatorial-bmm-conjecture, matrix-multiplication-exponent, fine-grained-reduction, conditional-lower-bound, transitive-closure, clique-decision]
sources:
  - paper: doi:10.1016/S0022-0000(75)80046-8
    title: Leslie G. Valiant, General context-free recognition in less than cubic time, Journal of Computer and System Sciences 10(2) (1975)
    locator: pp. 308 to 315
  - paper: doi:10.1145/505241.505242
    title: Lillian Lee, Fast context-free grammar parsing requires fast Boolean matrix multiplication, Journal of the ACM 49(1) (2002)
    locator: pp. 1 to 15 (the definition of c-parsing and the reduction from Boolean matrix multiplication)
  - paper: doi:10.3115/976909.979619
    title: Lillian Lee, Fast context-free parsing requires fast Boolean matrix multiplication, Proceedings of the 35th Annual Meeting of the Association for Computational Linguistics (1997)
    locator: pp. 9 to 15 (the conference version)
  - paper: doi:10.1137/16m1061771
    title: Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, If the current clique algorithms are optimal, so is Valiant's parser, SIAM Journal on Computing 47(6) (2018)
    locator: pp. 2527 to 2555 (conference version in FOCS 2015, doi:10.1109/FOCS.2015.16, pp. 98 to 117)
  - paper: doi:10.1016/j.tcs.2013.09.011
    title: Alexander Okhotin, Parsing by matrix multiplication generalized to Boolean grammars, Theoretical Computer Science 516 (2014)
    locator: pp. 101 to 120 (a simple form of Valiant's recursion with its running time)
---

## Statement

We use the notation of the [context-free grammar](/context-free-grammar/) page: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ for the start symbol, $n$ for the input length and $|G|$ for the grammar size, the sum of $1 + |\alpha|$ over the productions $A \to \alpha$. For a grammar $G$ and a string $w = a_1 \cdots a_n$, the **table** of $G$ on $w$ is the set of triples $(A, i, j)$ with $0 \le i < j \le n$ and $A \Rightarrow^* a_{i+1} \cdots a_j$; it is what the [CYK algorithm](/cyk-algorithm/) computes. Lee calls $(A, i, j)$ a **c-constituent** when, in addition, $S \Rightarrow^* a_1 \cdots a_i\, A\, a_{j+1} \cdots a_n$, so that the span can occur in a parse tree of the whole string; a **c-parser** outputs the c-constituents in a form that answers each query $(A, i, j)$ in $O(1)$ time. Let $M(m)$ be the time to multiply two $m \times m$ Boolean matrices.

**Theorem.**

1. **(Valiant, 1975.)** If $M(m) = O(m^\alpha)$ for some $\alpha > 2$, then the table of any grammar $G$ in [Chomsky normal form](/chomsky-normal-form/) on any string of length $n$ can be computed in $O(|G|\, n^\alpha)$ time. In particular, membership $w \in L(G)$ can be decided in that time.
2. **(Lee, 1997 and 2002.)** Given two $m \times m$ Boolean matrices $A$ and $B$, one can build in $O(m^2)$ time a grammar $G$ in Chomsky normal form with $|G| = O(m^2)$ and a string $w$ of length $n = O(m^{1/3})$ such that every entry of $AB$ can be read in $O(1)$ time from the table of $G$ on $w$, or equally from its c-constituents. Consequently, if some algorithm computes the table, or the c-constituents, in $T(|G|, n)$ time, then $M(m) = O(T(c\, m^2, c\, m^{1/3}) + m^2)$ for a constant $c$. In particular, a parser that takes $O(|G|\, n^{3 - \epsilon})$ time for some $\epsilon > 0$ gives Boolean matrix multiplication in $O(m^{3 - \epsilon/3})$ time.

So general context-free parsing in the sense of the table is subcubic in $n$ (with a linear factor in $|G|$) exactly when Boolean matrix multiplication is subcubic, and both reductions keep combinatorial algorithms combinatorial.

## In plain words

Filling the parse table of a grammar is, at its core, a series of matrix products: to know which symbols cover a stretch of text, we combine what covers its left parts with what covers its right parts, for all cut points at once. Valiant arranged this work into a small number of products of yes and no tables, so any fast method for such products gives a fast parser.

Lee showed that the converse holds too. She built, from two yes and no tables, a grammar and a short string whose parse table contains their product: the row index sits partly in where a stretch starts and partly in the name of a grammar symbol, and the column index the same way at the end of the stretch. A parser much faster than cubic would therefore multiply such tables faster than anyone knows how to do without heavy algebra.

## Proof

**Part 1.** This is the running time of [Valiant's algorithm](/valiant-algorithm/), whose full correctness proof is on that page. In short: COMPUTE$(0, N)$, with $N$ the least power of 2 above $n$, finishes the table by recursion on halves, and the work is $p$ Boolean products of side $t$ for each of the $\frac{N}{t}\left(\frac{N}{2t} - 1\right)$ block products of side $t$, where $p \le |G|$ is the number of pairs $(B, C)$ that are right sides of productions. With $M(t) = O(t^\alpha)$ and $\alpha > 2$, the sum $\sum_t \frac{N^2}{2t^2} M(t)$ is geometric and dominated by $t = N/4$, so it is $O(N^\alpha)$; the cell updates add $O(p N^2)$. The total is $O(|G|\, n^\alpha)$.

**Part 2.** We give a version of Lee's reduction; the encoding of indices follows her idea, and the details of the string and of the helper nonterminals are chosen here to keep the grammar in Chomsky normal form.

*Padding.* Let $\delta = \lceil m^{1/3} \rceil$ and pad $A$ and $B$ with zero rows and columns to size $m' = \delta^3$. Since $\delta \le 2 m^{1/3}$, $m' \le 8m$, and the product of the padded matrices contains $AB$ in its top left corner. From now on $m = \delta^3$. Every index $x \in \{0, \ldots, m - 1\}$ is written as $x = x' \delta^2 + x''$ with a **high part** $x' \in \{0, \ldots, \delta - 1\}$ and a **low part** $x'' \in \{0, \ldots, \delta^2 - 1\}$.

*The string.* Let

$$w = \mathsf{x}\; \mathsf{a}^{\delta}\; \mathsf{b}^{\delta + 1}\; \mathsf{c}^{\delta}\; \mathsf{y},$$

of length $n = 3\delta + 3 = O(m^{1/3})$. The terminals are written in sans serif to keep them apart from the matrices. We index the letters of $w$ from 0: $\mathsf{x}$ is at index 0, the $\mathsf{a}$'s at indices $1, \ldots, \delta$, the $\mathsf{b}$'s at $\delta + 1, \ldots, 2\delta + 1$, the $\mathsf{c}$'s at $2\delta + 2, \ldots, 3\delta + 1$, and $\mathsf{y}$ at $3\delta + 2$. The span $w[s, t)$ is the substring of the letters with indices $s, \ldots, t - 1$; it is $a_{s+1} \cdots a_t$ in the notation of the statement, and the triple $(A, s, t)$ of the table refers to it.

*The grammar.* For $r = 0, \ldots, \delta - 1$, helper nonterminals derive one block of equal letters each:

$$P_r \Rightarrow^* \mathsf{a}^{\delta - r}, \qquad Q_r \Rightarrow^* \mathsf{b}^{r + 1}, \qquad R_r \Rightarrow^* \mathsf{b}^{\delta - r}, \qquad U_r \Rightarrow^* \mathsf{c}^{r + 1}.$$

In Chomsky normal form: $L_a \to \mathsf{a}$, $L_b \to \mathsf{b}$, $L_c \to \mathsf{c}$, $P_{\delta - 1} \to \mathsf{a}$, $P_r \to L_a P_{r+1}$, $Q_0 \to \mathsf{b}$, $Q_r \to L_b Q_{r-1}$, $R_{\delta-1} \to \mathsf{b}$, $R_r \to L_b R_{r+1}$, $U_0 \to \mathsf{c}$, $U_r \to L_c U_{r-1}$. These are $O(\delta)$ productions. The main nonterminals are indexed by pairs of low parts:

- $A_{i'', k''} \to P_{i'} Q_{k'}$ for every pair $(i, k)$ with $A[i, k] = 1$;
- $B_{k'', j''} \to R_{k'} U_{j'}$ for every pair $(k, j)$ with $B[k, j] = 1$;
- $C_{i'', j''} \to A_{i'', k''} B_{k'', j''}$ for all $i'', j'', k''$;
- $S \to X K_{i'', j''}$ and $K_{i'', j''} \to C_{i'', j''} Y$ for all $i'', j''$, with $X \to \mathsf{x} \mid X L_a$ and $Y \to \mathsf{y} \mid L_c Y$, so that $X$ derives exactly $\mathsf{x} \mathsf{a}^*$ and $Y$ exactly $\mathsf{c}^* \mathsf{y}$.

(Productions that use a nonterminal with no production of its own, such as $A_{i'', k''}$ when that part of $A$ is zero, can be deleted without changing any derivation.) There are at most $2m^2$ productions of the first two kinds, $\delta^6 = m^2$ of the third, $2\delta^4$ of the fourth and $O(\delta)$ helpers, each of size at most 3, so $|G| = O(m^2)$, and the grammar is written in $O(m^2)$ time.

*Claim 1.* $A_{i'', k''} \Rightarrow^* w[s, t)$ if and only if $s = 1 + i'$ and $t = \delta + 2 + k'$ for a pair $(i, k)$ with these low parts and $A[i, k] = 1$.

The strings that $A_{i'', k''}$ derives are $\mathsf{a}^{\delta - i'} \mathsf{b}^{k' + 1}$ for the pairs with $A[i, k] = 1$. A substring of $w$ of that form contains both an $\mathsf{a}$ and a $\mathsf{b}$, so it contains the boundary between the letters with indices $\delta$ and $\delta + 1$; with $\delta - i'$ letters $\mathsf{a}$ before the boundary it starts at $s = 1 + i'$, and with $k' + 1$ letters $\mathsf{b}$ after it, it ends at $t = \delta + 1 + k' + 1$. Conversely, that span is such a string.

*Claim 2.* $B_{k'', j''} \Rightarrow^* w[s, t)$ if and only if $s = \delta + 2 + k'$ and $t = 2\delta + 3 + j'$ for a pair $(k, j)$ with these low parts and $B[k, j] = 1$.

The strings are $\mathsf{b}^{\delta - k'} \mathsf{c}^{j' + 1}$; such a substring contains the boundary after the last $\mathsf{b}$, which has index $2\delta + 1$, so it starts at $2\delta + 2 - (\delta - k') = \delta + 2 + k'$ and ends at $2\delta + 1 + j' + 1$.

*Claim 3.* $C_{i'', j''} \Rightarrow^* w[s, t)$ if and only if $s = 1 + i'$ and $t = 2\delta + 3 + j'$ for some $i$ and $j$ with these low parts and $(AB)[i, j] = 1$.

A derivation from $C_{i'', j''}$ starts with some $C_{i'', j''} \to A_{i'', k''} B_{k'', j''}$ and splits the span at a point $r$. By Claim 1, $s = 1 + i'$ and $r = \delta + 2 + k'_1$ with $A[(i', i''), (k'_1, k'')] = 1$; by Claim 2, $r = \delta + 2 + k'_2$ and $t = 2\delta + 3 + j'$ with $B[(k'_2, k''), (j', j'')] = 1$. The two values of $r$ agree, so $k'_1 = k'_2$, and the index $k = k'_1 \delta^2 + k''$ has $A[i, k] = B[k, j] = 1$. Conversely, such a $k$ gives the derivation with the split at $r = \delta + 2 + k'$. The split point carries the high part of $k$, and the nonterminal carries its low part, which is what makes the middle index match.

*Claim 4.* Every such span is a c-constituent: $S \Rightarrow X K_{i'', j''} \Rightarrow X C_{i'', j''} Y$, and $X \Rightarrow^* \mathsf{x} \mathsf{a}^{i'} = w[0, 1 + i')$ while $Y \Rightarrow^* \mathsf{c}^{\delta - 1 - j'} \mathsf{y} = w[2\delta + 3 + j', n)$.

So $(AB)[i, j] = 1$ exactly when $(C_{i'', j''}, 1 + i', 2\delta + 3 + j')$ is in the table, and exactly when it is a c-constituent. Reading the $m^2$ entries takes $O(m^2)$ queries. With $|G| = O(m^2)$ and $n = O(m^{1/3})$, a parser that runs in $O(|G|\, n^{3 - \epsilon})$ time takes $O(m^2 \cdot m^{1 - \epsilon/3}) = O(m^{3 - \epsilon/3})$ time, and the construction and the reading add $O(m^2)$. $\square$

For example, with $\delta = 2$ the matrices are $8 \times 8$, the string is $\mathsf{x\,aa\,bbb\,cc\,y}$ of length 9, and the entry $(AB)[5, 6]$ (high parts $1, 1$, low parts $1, 2$) is the question whether $C_{1, 2}$ derives the span $[2, 8)$, that is $\mathsf{a\,bbb\,cc}$. For $\delta = 2$ and $\delta = 3$ (matrices of side 8 and 27, strings of length 9 and 12, up to 2511 symbols of grammar), the claims were checked by script on random matrices of several densities: the spans derived by each $C_{i'', j''}$, computed with Valiant's algorithm, are exactly the ones Claim 3 predicts, and the spans tested are c-constituents.

## Consequences

- **Subcubic parsing is a matrix problem.** Part 1 gives $O(|G|\, n^{\omega})$ for every exponent $\omega$ above the [matrix multiplication exponent](/matrix-multiplication-exponent/), now below 2.372. Part 2 says that beating cubic time in this form, by any margin, needs subcubic Boolean matrix multiplication.
- **Practical parsers stay cubic.** The algorithms used in practice for general grammars, CYK, the [Earley parser](/earley-parser/) and GLR, all compute the table or more, and all are cubic in the worst case. Lee's reduction maps a combinatorial parser to a combinatorial matrix product, so under the [combinatorial BMM conjecture](/combinatorial-bmm-conjecture/), no combinatorial parser computes the table in $O(|G|\, n^{3 - \epsilon})$ time. A practical fast general parser would be a practical fast matrix product, which has resisted much work.
- **Recognition for one fixed grammar.** Abboud, Backurs and Vassilevska Williams gave a fixed grammar of constant size for which recognition, a single yes or no answer, in $O(n^{\omega - \epsilon})$ time, or in $O(n^{3 - \epsilon})$ time by a combinatorial algorithm, would give faster algorithms for the $k$-clique problem than are known. This strengthens the theorem in the two places where it is weak: the grammar does not grow, and only one bit is output. The same reductions give conditional lower bounds for RNA folding and for the edit distance to the Dyck language.
- **A template for fine-grained reductions.** The proof is an early example of a [fine-grained reduction](/fine-grained-reduction/): it maps instances of size $m$ to instances whose parameters are polynomials in $m$ with carefully chosen exponents, and it keeps track of how a speedup transfers.

## Tightness

- **The exponents do not match.** Part 1 turns an $O(m^\alpha)$ matrix product into an $O(|G|\, n^\alpha)$ parser, but Part 2 turns an $O(|G|\, n^{\alpha})$ parser into only an $O(m^{2 + \alpha/3})$ matrix product, which is worse than $m^\alpha$ for $\alpha < 3$. The two problems are equivalent for being subcubic, not with the same exponent.
- **The grammar is large.** In Part 2, $|G| = \Theta(m^2) = \Theta(n^6)$. A parser whose time grows faster than linearly in $|G|$, or one that is fast only for small grammars, is not covered; for example, an algorithm in $O(|G|^2 + n^{2})$ time would not contradict anything. For one fixed grammar, only the conditional bounds of Abboud et al. are known.
- **The table, not just membership.** The reduction reads $m^2$ entries of the table, so it says nothing about a recognizer that outputs one bit. Whether recognition is as hard as computing the table is open, apart from the clique-based conditional bounds.
- **No unconditional bound.** Both parts compare two problems; the best known lower bound for either, in general models, is the trivial one from reading the input. If $\omega = 2$, Part 1 gives parsing in $O(|G|\, n^{2 + o(1)})$ time.
- **Deterministic grammars are easy.** For LR(1) grammars or other deterministic grammars, parsers take $O(n)$ time, so the hardness lives only in general, nondeterministic grammars.

## History

Valiant's 1975 paper showed that general context-free recognition can be done in the time of Boolean matrix multiplication, $O(n^{2.81})$ with Strassen's algorithm, breaking the cubic bound of Cocke, Kasami and Younger. For more than twenty years it was unclear whether matrix multiplication was really needed. Lillian Lee answered this in 1997, in a paper at ACL, and in the 2002 journal version in the Journal of the ACM: she defined c-parsing to capture what practical parsers compute, and showed that a fast c-parser gives fast Boolean matrix multiplication. Her result explained why no practical general parser beats cubic time. Abboud, Backurs and Vassilevska Williams showed in 2015 (journal version 2018) that, under hypotheses about cliques, even recognition for a fixed grammar cannot be much faster than Valiant's algorithm. The two papers state the two directions separately; this page puts them together.

## References
