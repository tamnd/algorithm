---
title: "TO-CASEFOLD computes toCasefold, and the canonical caseless match is an equivalence that contains canonical equivalence"
proves: [correctness, termination]
status: full
---

**Setup.** Let $T$ be the set of lines of CaseFolding.txt. For a code point $c$ and a status $s$ in $\{C, F, S, T\}$, write $T_s(c)$ for the mapping of the line of $c$ with status $s$, if there is one. The file has two properties that the proof uses. (P1) For each $c$ and $s$ there is at most one line. (P2) No code point has both a C line and an F line, and no code point has both a C line and an S line. (P2) is how the file is built: the header says that a C line is used by both kinds of folding, and F and S lines are given only where full and simple folding differ.

For the options full and turkic, define the folding of one code point:

- $f(c) = T_T(c)$ if turkic holds and $T_T(c)$ exists;
- otherwise $f(c) = T_F(c)$ if full holds and $T_F(c)$ exists;
- otherwise $f(c) = T_S(c)$ if full does not hold and $T_S(c)$ exists;
- otherwise $f(c) = T_C(c)$ if it exists;
- otherwise $f(c) = c$.

By (P1), each case gives one string, so $f$ is a function. With full = true and turkic = false, $f(c)$ is Case_Folding(c) of the default full folding (statuses C and F), and R4 defines $\mathrm{toCasefold}(X) = f(x_0) f(x_1) \cdots f(x_{n-1})$ for $X = x_0 \cdots x_{n-1}$. With full = false, $f$ is the simple folding (statuses C and S).

**Claim 1.** TO-CASEFOLD$(X, \mathrm{full}, \mathrm{turkic})$ stops and returns $f(x_0) \cdots f(x_{n-1})$.

*Proof.* The loop of line L2 runs once for each of the $n$ code points, and each iteration does a bounded number of steps, so the procedure stops. Invariant: before the iteration for $x_i$, $Y = f(x_0) \cdots f(x_{i-1})$. It holds for $i = 0$ by line L1. In the iteration for $x_i$, lines L3 to L7 test the same conditions in the same order as the definition of $f$ and append the same string, so after it $Y = f(x_0) \cdots f(x_i)$. For $i = n$, line L8 returns $f(x_0) \cdots f(x_{n-1})$. $\square$

**Claim 2.** Simple folding keeps the length in code points.

*Proof.* With full = false and turkic = false, line L4 is never taken, so each code point appends $T_S(c)$, $T_C(c)$ or $c$. Every S and C mapping in the file is one code point (the header defines both as mappings to single characters). So each iteration appends exactly one code point, and by Claim 1 the output has $n$ code points. $\square$

**Claim 3.** Let $K(X) = \mathrm{NFD}(\mathrm{toCasefold}(\mathrm{NFD}(X)))$. The relation "$K(X) = K(Y)$", which line L9 tests, is an equivalence relation. If $X$ and $Y$ are canonically equivalent, then $K(X) = K(Y)$.

*Proof.* The relation compares the values of one function $K$, so it is reflexive, symmetric and transitive. If $X$ and $Y$ are canonically equivalent, then $\mathrm{NFD}(X) = \mathrm{NFD}(Y)$, because NFD is a normal form for canonical equivalence (the uniqueness of the normalization forms, core spec section 3.11). Then the two values of $K$ are computed from the same string and are equal. $\square$

**Claim 4.** The default caseless match D144 does not contain canonical equivalence, so the NFD steps of D145 are needed.

*Proof.* A counterexample is enough. $X$ = U+00C5 and $Y$ = U+0041 U+030A are canonically equivalent. By the C lines `00C5; C; 00E5;` and `0041; C; 0061;`, and since U+030A has no line, $\mathrm{toCasefold}(X)$ = U+00E5 and $\mathrm{toCasefold}(Y)$ = U+0061 U+030A, which differ. The final NFD maps both to U+0061 U+030A. The first NFD is needed too: $X$ = U+03B1 U+0345 U+0301 and $Y$ = U+03B1 U+0301 U+0345 are canonically equivalent ($\mathrm{ccc}$ 240 and 230), and $\mathrm{NFD}(\mathrm{toCasefold}(X))$ = U+03B1 U+03B9 U+0301 differs from $\mathrm{NFD}(\mathrm{toCasefold}(Y))$ = U+03B1 U+0301 U+03B9, because U+03B9 has $\mathrm{ccc} = 0$ and canonical ordering never moves a mark across a starter. $\square$

**Termination of line L9.** NFD and TO-CASEFOLD stop on every finite input, and line L9 calls each a fixed number of times.
