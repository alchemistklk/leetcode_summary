'''
1. 模拟法, 直接进行字符串的比较

2. gcd性质法 / 暴力法
(1) 暴力法
(2) 利用gcd性质:
        1. 求一个数字的gcd, 最坏的情况 log n: 即每次 // 2 之后再计算
        2. 因此, 数组中所有数字最坏的 gcd 为 nlogU
        3. 使用集合记录 gcd >= k的集合及对应的区间右端点
        4. 由于求 gcd 过程中存在重复元素, 可以使用原地去重的方法(因为得到的gcd相同的在一起)
        5. 每次更新的时候, 如果 gcd 没有发生变化, 需要更新右端点
        6. 使用 i0 标记不合法的位置, 然后重新计算

3. 中位数法 和 枚举 + 计算变化量
(1) 中位数法
    将costs数组中数字视为 nums[i]的出现次数, 中位数是取 sum(costs)的中位数之和
    ```
    mid = (sum(costs) // 2 + 1) , s = 0
    for i in costs:
        s += c
        if s >= mid:
            mid = s # 此时为计算
    ```
(2) 枚举 + 计算变化量
    1. 以 a[0][0]作为起始点, 计算变化量
    2. 移动之后 其他数字减少的变化量 sum_cost -= nums[i]; 前面部分数字增加变化量 nums[i]
    3. 计算sum_cost
    ```
    ans = total = sum(abs(x - a[0][0]) * c for x, c in zip(nums, costs))
    sum_cost -= 2 * c0
    total -= sum_cost * d
    ```

'''

from itertools import pairwise
from math import gcd
from typing import List

# 2446. 判断两个事件是否存在冲突
# https://leetcode.cn/problems/determine-if-two-events-have-conflict/


class HaveConflictSolution:
    def haveConflict(self, event1: List[str], event2: List[str]) -> bool:
        if event1[0] >= event2[0]:
            event = event1
            event1 = event2
            event2 = event

        return event1[1] >= event2[0]


# 2447. 最大公因数等于 K 的子数组数目
# https://leetcode.cn/problems/number-of-subarrays-with-gcd-equal-to-k/
'''
方法一: 暴力
枚举所有的子数组, 使用gcd()方法计算最大的公因数
剪枝: 0与num的最大公因数为num, 如果最大公因数, 如果 g % k != 0 则结束循环
'''


class SubarraySolution:
    def subarrayGCD(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = 0
        for i in range(n):
            g = 0
            for j in range(i, n):
                g = gcd(nums[j], g)
                if g % k:
                    break
                if g == k:
                    ans += 1

        return ans


'''
方法二: 利用性质计算
1. 将计算gcd的逻辑去重
2. 从左向右计算不同的GCD, o(log nums[i])
   => 所有子数组最多有n(nlogU)个
   => 使用上次结果计算的 gcd 与当前数字合并后得到的 gcd, 之后去重
3. 使用集合 a 存储[gcd, end], 记录上一个不合法的位置 i0, 长度 end - i0
4. 原地去重: 如果相同的数字连在一起, 则使用原地去重, 
   https://leetcode.cn/problems/remove-duplicates-from-sorted-array/

class DistinctSolution:
    def distinct(self, nums: List[int]) -> int:
        j = 0
        for v in nums:
            if v != nums[j]:
                j += 1
                nums[j] = v

        return j + 1

'''


class SubarraySolutionII:
    def subarrayGCD(self, nums: List[int], k: int) -> int:
        a = []  # [gcd, 相同 gcd 的右端点]
        i0 = -1
        ans = 0
        for i, v in enumerate(nums):
            if v % k:
                i0 = i
                a = []  # 此时需要清空数组
                continue
            a.append([v, i])

            # 对gcd去重, 原地去重
            j = 0
            for p in a:
                # 计算当前的gcd
                p[0] = gcd(p[0], v)
                if a[j][0] != p[0]:
                    j += 1
                    a[j] = p
                else:
                    # 合并右端点
                    a[j][1] = p[1]

            if a[0][0] == k:
                ans += a[0][1] - i0  # 计算子数组的个数 right - left + 1

        return ans


# 2448. 使数组相等的最小开销
# https://leetcode.cn/problems/minimum-cost-to-make-array-equal/
'''
方法一: 中位数贪心法
1. 将costs[i]看作每个nums[i]的出现次数, 计算结果等价于求每个数字到特定数字的距离和
2. 求距离之和, 使用中位数求和法
3. 将costs数组看作出现次数后, 我们需要寻找当中的中位数, 寻找costs
4. 中位数的选择是指 在costs中选择

方法二: 枚举 + 变化量
1. 以第一个为初始值计算, total
2. 枚举变化时
    2.1 其他值的变化: (sum_cost - cost[i - 1]) * 变化值(nums[i] - nums[i - 1])
    2.2 之前值的变化: (nums[i] - nums[i - 1]) * cost[i - 1]
    2.3 (sum_cost - c0) * t - c0 * t -> total - 2 * c0 * t
'''


class MinCostSolution:
    def minCost(self, nums: List[int], costs: List[int]) -> int:
        # 方法一: 中位数计算法
        # # 选择costs的中位数, 因为将costs中数字看作出现次数
        # a = sorted(zip(nums, costs))
        # # 需要向上取整
        # s, mid = 0, (sum(costs) + 1) // 2
        # for x, c in a:
        #     s += c
        #     if s >= mid:
        #         return sum(abs(y - x) * c for y, c in a)

        # 方法二: 枚举法
        # 假设选择第一个, 总花费为 total = sum(abs(y - a[0][0]) * c for y, c in a)
        # 如果下一个, 花费减少的花费 (nums[i] - nums[i - 1])
        a = sorted(zip(nums, costs))
        total = ans = sum(abs(y - a[0][0]) * c for y, c in a)
        sum_cost = sum(costs)
        for (x0, c0), (x1, _) in pairwise(a):
            t = x1 - x0
            # 这个变化值需要直接减在 sum_cost上面
            sum_cost -= 2 * c0
            total -= sum_cost * t
            ans = min(ans, total)
        return ans


# 2449. 使数组相似的最少操作次数
# https://leetcode.cn/problems/minimum-number-of-operations-to-make-arrays-similar/
'''
1. 如果要使数组相似操作次数最小则 我们需要将最小值对应最小值, 次小值对应次小值, 排序
2. 注意到 +2, -2 都是奇偶性不会改变, 所以将 nums与target中奇偶性相同一起操作
3. 将奇偶数字操作分开, 将奇数采用相反数, 然后排序后分开
'''


class MakeSimilarSolution:
    def makeSimilar(self, nums: List[int], target: List[int]) -> int:
        def support(a: List[int]):
            for i, x in enumerate(a):
                if x % 2:
                    a[i] = -x  # 由于元素都是正数，把奇数变成相反数，这样排序后奇偶就自动分开了
            # 排序后奇偶自动分开
            a.sort()

        support(nums)
        support(target)

        # return sum(abs(x - y) for x, y in zip(nums, target)) // 4

        ans = 0
        for i, j in zip(nums, target):
            ans += abs(i - j)

        return ans // 4
