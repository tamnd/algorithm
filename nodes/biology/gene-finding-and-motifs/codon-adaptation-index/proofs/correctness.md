---
title: The two loops compute the codon adaptation index of Sharp and Li
proves: [correctness]
status: full
---

Fix a genetic code. For an amino acid $a$, let $C(a)$ be the set of its codons and $n_a = |C(a)|$. Only amino acids with $n_a \ge 2$ count; in the standard code these are the 18 amino acids other than Met (ATG) and Trp (TGG). Write $a(c)$ for the amino acid of a sense codon $c$.

**Definitions (Sharp and Li 1987).** Let $X_c$ be the number of times codon $c$ occurs in the reference set, with $X_c$ replaced by $1/2$ when it is 0. The relative synonymous codon usage is $\mathrm{RSCU}_c = X_c / \big(\frac{1}{n_{a(c)}} \sum_{d \in C(a(c))} X_d\big)$, and the relative adaptiveness is $w_c = \mathrm{RSCU}_c / \max_{d \in C(a(c))} \mathrm{RSCU}_d$. For a gene whose counted codons are $c_1, \ldots, c_L$ (sense codons of amino acids with $n_a \ge 2$), the index is $\mathrm{CAI} = \mathrm{CAI}_{\mathrm{obs}} / \mathrm{CAI}_{\max}$, where $\mathrm{CAI}_{\mathrm{obs}} = (\prod_k \mathrm{RSCU}_{c_k})^{1/L}$ and $\mathrm{CAI}_{\max} = (\prod_k \max_{d \in C(a(c_k))} \mathrm{RSCU}_d)^{1/L}$.

**Lemma 1.** After lines L1 to L4, $w[c] = w_c$ for every sense codon $c$, and $0 < w_c \le 1$, with $w_c = 1$ for at least one codon of each amino acid.

*Proof.* Line L1 counts each codon, and line L2 sets the zero counts to $1/2$, so after L2 the table holds $X_c > 0$ as defined. Line L3 computes $X_{\max}(a) = \max_{d \in C(a)} X_d$, and line L4 sets $w[c] = X_c / X_{\max}(a(c))$. The denominator $\frac{1}{n_a} \sum_{d} X_d$ of RSCU is the same for all codons of one amino acid, so it cancels: $\mathrm{RSCU}_c / \max_d \mathrm{RSCU}_d = X_c / \max_d X_d = w[c]$. All $X_c$ are positive, so $0 < w_c \le 1$, and the codon where the maximum is reached has $w_c = 1$. $\square$

**Lemma 2.** When line L9 is reached, $L$ is the number of counted codons of the gene and $S = \sum_{k=1}^{L} \ln w_{c_k}$.

*Proof.* Line L5 sets $S = 0$ and $L = 0$. Line L6 visits the codons of the gene in order, and line L7 lets through exactly the counted codons: sense codons of an amino acid with at least two codons. Line L8 adds $\ln w[c]$ to $S$ and 1 to $L$ for each of them, and by Lemma 1 $w[c] = w_c$. By induction on the number of visited codons, $S$ and $L$ are the sum and the count over the counted codons visited so far. $\square$

**Theorem.** If $L \ge 1$, line L9 returns $\mathrm{CAI} = (\prod_{k=1}^{L} w_{c_k})^{1/L}$, and this equals $\mathrm{CAI}_{\mathrm{obs}} / \mathrm{CAI}_{\max}$. Moreover $0 < \mathrm{CAI} \le 1$, with $\mathrm{CAI} = 1$ if and only if every counted codon has $w_{c_k} = 1$.

*Proof.* By Lemma 2, $\exp(S / L) = \exp(\frac{1}{L} \sum_k \ln w_{c_k}) = (\prod_k w_{c_k})^{1/L}$, since $\exp$ and $\ln$ are inverse and the weights are positive. By Lemma 1, $w_{c_k} = \mathrm{RSCU}_{c_k} / \max_{d} \mathrm{RSCU}_d$, so the product of the $w_{c_k}$ is the product of the RSCU values divided by the product of the maxima, and taking the $L$-th root of both gives $\mathrm{CAI}_{\mathrm{obs}} / \mathrm{CAI}_{\max}$. Each factor lies in $(0, 1]$, so the geometric mean lies in $(0, 1]$. It is 1 if and only if $\sum_k \ln w_{c_k} = 0$, and each term is at most 0, so this happens if and only if every term is 0. $\square$

**Corollary (codon usage form).** Let $f_c$ be the number of times the counted codon $c$ occurs in the gene. Then $\mathrm{CAI} = \exp\big(\frac{1}{L} \sum_c f_c \ln w_c\big)$ with $L = \sum_c f_c$, the sum taken over the codons of the 18 amino acids. So the index depends only on the codon counts of the gene, and it does not change when the codons of the gene are put in another order.

*Proof.* Group the terms of $S$ by codon: the codon $c$ contributes $\ln w_c$ once for each of its $f_c$ occurrences. $\square$

**Running time.** Line L1 reads each of the $M$ codons of the reference set once, with one table look-up each, in $\Theta(M)$ time. Lines L2 to L4 handle the 61 sense codons, a constant. Lines L6 to L8 read the $N$ codons of the gene once, with one look-up, one logarithm and one addition each, in $\Theta(N)$ time on the real RAM. The tables have a constant number of entries, so the extra space is $\Theta(1)$.
