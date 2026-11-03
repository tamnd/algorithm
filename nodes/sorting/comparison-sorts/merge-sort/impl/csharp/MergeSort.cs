// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

namespace Algorithm;

/// <summary>Merge sort.</summary>
public static class MergeSort
{
    /// <summary>Sorts a in place, in non-decreasing order. The sort is stable.</summary>
    public static void Sort<T>(Span<T> a) where T : IComparable<T>
    {
        var b = new T[(a.Length + 1) / 2];
        Sort(a, b);
    }

    private static void Sort<T>(Span<T> a, T[] b) where T : IComparable<T>
    {
        if (a.Length <= 1) return;                      // @line L1
        int mid = a.Length / 2;                         // @line L2
        Sort(a[..mid], b);                              // @line L3
        Sort(a[mid..], b);                              // @line L4
        Merge(a, mid, b);                               // @line L5
    }

    private static void Merge<T>(Span<T> a, int mid, T[] b) where T : IComparable<T>
    {
        a[..mid].CopyTo(b);                             // @line L6
        int i = 0, j = mid, k = 0;                      // @line L7
        while (i < mid && j < a.Length)                 // @line L8
        {
            if (b[i].CompareTo(a[j]) <= 0)              // @line L9
            {
                a[k] = b[i++];
            }
            else
            {
                a[k] = a[j++];                          // @line L10
            }
            k++;                                        // @line L11
        }
        while (i < mid)                                 // @line L12
        {
            a[k++] = b[i++];                            // @line L13
        }
    }
}
