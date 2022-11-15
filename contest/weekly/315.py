'''
1. 暴力


2. 暴力
(1) s[::-1] 反转字符串的写法

3. 暴力
(1) 比较逆序字符串是否相等时, 如果是数字类型考虑将字符串解析为数字进行比较
    避免讨论前缀 0 的情况


4. 双指针
(1) 由于题目中要求, 子数组中最小值 == minK 且 子数组中最大值 == maxK -> 考虑使用两个指针分别标记

(2) 如果minI, maxI之间的元素都在 minK 与 maxK 之间
    如果 [left, right] 数据都符合要求个数 right - left + 1
    如果 (left, right] 数据符合要求 right - left

(3) 所以需要记录三个下标 idx:不符合要求的下标, min_i:最小值的下标, max_i:最大值的下标
    因为要包含 minK 与 maxK 所以个数 = min(min_i, max_i) - idx
    由于 idx 可能 大于前面的数字, 所以需要与 0 比较
'''

# 6204. 与对应负数同时存在的最大正整数
# https://leetcode.cn/problems/largest-positive-integer-that-exists-with-its-negative/


from typing import List


class FindMaxSolution:
    def findMax(self,  nums: List[int]) -> int:
        ans = -1
        # 使用map进行记录
        s = set()

        for i in nums:
            if -i in s:
                ans = max(ans, abs(i))
            s.add(i)
        return ans


# 6205. 反转之后不同整数的数目
# https://leetcode.cn/problems/count-number-of-distinct-integers-after-reverse-operations/


class CountDistinctIntegers:
    def countDistinctIntegers(self, nums: List[int]) -> int:
        s = set()
        for i in nums:
            s.add(i)
            o = int(str(i)[::-1])
            s.add(o)
            # 辅助写法, 求数字的相反数
            # tmp = 0
            # while i > 0:
            #     o = i % 10
            #     tmp = tmp * 10 + o
            #     i //= 10

        return len(s)


# 2443. 反转之后的数字和
# https://leetcode.cn/problems/sum-of-number-and-its-reverse/


class SumOfNumber:
    def sumOfNumberAndReverse(self, num: int) -> bool:
        for i in range(num + 1):
            # 错误写法
            # o = str(i)[::-1]
            # if str(i) == o:
            #     return True
            # 涉及到字符串转化为逆序字符串考虑0字符串使用数字进行比较
            o = int(str(num - i)[::-1])
            if i == o:
                return True
        return False


# 6207. 统计定界子数组的数目
# https://leetcode.cn/problems/count-subarrays-with-fixed-bounds/


'''
1. 使用双指针分别记录 minK 与 maxK出现的下标, 统计记录当前不在区间范围的数字下标 idx
2. min(minI, maxI) - idx, 避免存在为 0 的情况, 需要取 max 与 0 进行比较
3. 如果左端点去不到, 起始端点为 -1
'''


class CountSubarrays:
    def countSubarrays(self, nums: List[int], minK: int, maxK: int) -> int:
        # 由于此时 左端点取不到，初始值为 -1
        idx = min_i = max_i = -1
        ans = 0
        for i, v in enumerate(nums):
            if v == minK:
                min_i = i
            if v == maxK:
                max_i = i
            if v > maxK or v < minK:
                idx = i
            ans += max(0, min(min_i, max_i) - idx)

        return ans


# 线段树版本书写
class SegementTree:
    def __init__(self, n: int, nums: List[int]) -> None:
        self.tree = [0] * (4 * n)
        self.build_tree(1, 1, n, nums)

    def build_tree(self, o: int, left: int, right: int,
                   nums: List[int]) -> None:
        if left == right:
            self.tree[o] += nums[left - 1]
            return

        mid = (right + left) // 2

        self.build_tree(2 * o, left, mid, nums)
        self.build_tree(2 * o + 1, mid + 1, right, nums)

        self.tree[o] = self.tree[2 * o] + self.tree[2 * o + 1]

    def update(self, o: int, left: int, right: int,
               idx: int, val: int) -> None:
        if left == right:
            self.tree[o] = val
            return
        mid = (right + left) // 2
        if idx <= mid:
            self.update(2 * o, left, mid, idx, val)
        else:
            self.update(2 * o + 1, mid + 1, right, idx, val)

        self.tree[o] = self.tree[2 * o] + self.tree[2 * o + 1]

    def query(self, o: int, left: int, right: int, ql: int, qr: int) -> int:
        if ql <= left and right <= qr:
            return self.tree[o]

        mid = (right + left) // 2

        ans = 0
        if ql <= mid:
            ans += self.query(2 * o, left, mid, ql, qr)
        if mid < qr:
            ans += self.query(2 * o + 1, mid + 1, right, ql, qr)

        return ans
