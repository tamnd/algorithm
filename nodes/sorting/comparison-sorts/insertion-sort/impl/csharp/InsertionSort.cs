// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

namespace Algorithm;

/// <summary>Insertion sort.</summary>
public static class InsertionSort
{
    /// <summary>Sorts a in place, in non-decreasing order. The sort is stable.</summary>
    public static void Sort<T>(Span<T> a) where T : IComparable<T>
    {
        for (int i = 1; i < a.Length; i++)                  // @line L1
        {
            T key = a[i];                                   // @line L2
            int j = i - 1;                                  // @line L3
            while (j >= 0 && a[j].CompareTo(key) > 0)       // @line L4
            {
                a[j + 1] = a[j];                            // @line L5
                j--;                                        // @line L6
            }
            a[j + 1] = key;                                 // @line L7
        }
    }
}
