---
title: The two-stack algorithm returns the value of a fully parenthesized expression
proves: [correctness]
status: full
---

**Setting.** The input is a token sequence of an expression $E$ of the grammar $E \to \textit{number} \mid (\, E \;\textit{op}\; E \,)$. The value $\text{val}(E)$ is the number for a number, and $\text{val}(E_1) \textit{ op } \text{val}(E_2)$ for $(E_1 \textit{ op } E_2)$. We write a stack as a sequence from the bottom to the top, and $V \cdot x$ for $V$ with $x$ pushed. One *step* is one pass of the loop of lines L2 to L8 on one token.

**Lemma.** Let $F$ be an expression of the grammar, and suppose the loop is about to read the first token of $F$ with value stack $V$ and operator stack $O$. Then after the loop has read all tokens of $F$, and no others, the value stack is $V \cdot \text{val}(F)$ and the operator stack is $O$. No step on a token of $F$ pops from an empty stack, and no step reads or changes the entries of $V$ and $O$.

*Proof.* By induction on the length of $F$.

*Case $F$ is a number $x$.* $F$ is one token. Line L8 pushes $x$, so the stacks become $V \cdot x$ and $O$, and $x = \text{val}(F)$.

*Case $F = (\, F_1 \textit{ op } F_2 \,)$.* $F_1$ and $F_2$ are shorter than $F$, so the induction hypothesis holds for them. The token `(` is handled by line L3 and changes nothing. By the hypothesis for $F_1$, started on $(V, O)$, the stacks after $F_1$ are $V \cdot v_1$ and $O$, where $v_1 = \text{val}(F_1)$, and the steps on $F_1$ did not touch $V$ and $O$. The token $\textit{op}$ is pushed by line L4: the stacks are $V \cdot v_1$ and $O \cdot \textit{op}$. By the hypothesis for $F_2$, started on these stacks, the stacks after $F_2$ are $V \cdot v_1 \cdot v_2$ and $O \cdot \textit{op}$, with $v_2 = \text{val}(F_2)$. The last token is `)`, handled by lines L6 and L7. Line L6 pops $\textit{op}$ from the operator stack, then $b = v_2$ and $a = v_1$ from the value stack; none of these stacks is empty. Line L7 pushes $a \textit{ op } b = \text{val}(F_1) \textit{ op } \text{val}(F_2) = \text{val}(F)$. The stacks are $V \cdot \text{val}(F)$ and $O$. The pops removed only the entries pushed while reading $F$, so the entries of $V$ and $O$ were not read or changed. $\square$

**Theorem.** On the tokens of an expression $E$, EVALUATE returns $\text{val}(E)$, and when it returns, both stacks are empty.

*Proof.* Line L1 makes both stacks empty. The loop reads exactly the tokens of $E$. By the lemma with $V$ and $O$ empty, after the loop the value stack holds the single entry $\text{val}(E)$ and the operator stack is empty. Line L9 pops and returns $\text{val}(E)$, which leaves the value stack empty. $\square$

**Without left parentheses.** Line L3 does nothing on `(`, so deleting every `(` from the input deletes only steps that do not change the state. The other steps see the same stacks as before, so the algorithm returns the same value on the input with all `(` removed.

**Running time.** Each token causes one step of $O(1)$ work, and each `)` causes three pops and one push. So the time is $\Theta(n)$. By the lemma, the stacks during the steps on $F$ hold at most the entries of the enclosing calls plus those of $F$; by induction on the nesting depth $d$ of $E$, the value stack never holds more than $d + 1$ entries and the operator stack never more than $d$. $\blacksquare$
