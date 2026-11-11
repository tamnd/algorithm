---
title: The BLAKE3 tree is well defined, the CV stack builds the same tree, and the modes are separated
proves: [correctness]
status: full
---

We use the notation of the page. Let $c = \lceil n / 1024 \rceil$ be the number of chunks ($c = 1$ for the empty input).

**Lemma 1 (the shape depends only on $c$).** Line L4 splits $c \ge 2$ chunks into a left part of $2^{\lfloor \log_2 (c - 1) \rfloor}$ chunks and a right part of the rest. Both parts are not empty, the left part is a complete binary tree, and the recursion ends.

*Proof.* Let $a = 2^{\lfloor \log_2 (c-1) \rfloor}$. Then $a \le c - 1 < 2a$, so $1 \le c - a \le a$. The left part has a power of 2 chunks; by induction its own split gives two halves of equal size, so it is complete. Both parts have fewer than $c$ chunks, so the recursion ends at single chunks. $\square$

**Lemma 2 (the stack builds the same tree).** Let the incremental hasher finish chunk number $j$ (counting from 1) and push its CV after merging once for each trailing zero bit of $j$. Then after chunk $j$ the stack holds, from bottom to top, the CVs of the complete subtrees given by the binary digits of $j$, from the highest to the lowest. When the input ends with chunk $c$, folding the open last chunk with the stack from the top gives the tree of Lemma 1.

*Proof.* By induction on $j$. Write $j = 2^e u$ with $u$ odd. Before chunk $j$ the stack matches the binary digits of $j - 1$, whose lowest $e$ digits are all 1 and whose subtrees have sizes $2^{e-1}, \ldots, 2, 1$ on top. Merging $e$ times joins the new chunk with these, smallest first, into one subtree of size $2^e$, which matches the lowest set digit of $j$. The hasher never closes the last chunk early, because it keeps at least one byte in the buffer, so at the end the stack holds the complete subtrees for the digits of $c - 1$, and the open node is chunk $c - 1$ (counting from 0). Line L4 applied to $c$ chunks puts $a$ chunks on the left, where $a$ is the highest digit of $c - 1$; the bottom of the stack is that subtree. Applying the same argument to the right part, which has $c - a$ chunks and whose $c - a - 1$ has the remaining digits, shows that folding from the top builds the right part first and joins it to the left part last. $\square$

**Theorem 1 (well defined).** By Lemmas 1 and 2, the recursive code and the incremental code compute the same tree, so the same root node and the same output. The tests confirm this for inputs of 0 to 8193 bytes, and confirm both against the official vectors.

**Theorem 2 (the modes are separated).** For any inputs, the compressions of a hash, a keyed hash and a key derivation never share an input $(k, b, t, \ell, d)$ in a way that one mode can use, because $d$ always holds KEYED_HASH, DERIVE_KEY_CONTEXT, DERIVE_KEY_MATERIAL or none of them, and these are distinct bits.

*Proof.* Every compression of one call ORs the same mode flag $d_0$ into $d$, and the other flags (START, END, PARENT, ROOT) never set bits 4, 5 or 6. So two compressions from different modes differ in $d$, and with an ideal $C$ their outputs are independent. $\square$

**Remarks on tightness.** The indifferentiability bound in Section 4.3 of the BLAKE3 paper is of birthday type in the 256-bit chaining values. Generic collision search on CVs matches it, so the bound is tight up to constant factors for that goal. It does not cover attacks that use the structure of the real 7-round compression function; for those there is only cryptanalysis.
