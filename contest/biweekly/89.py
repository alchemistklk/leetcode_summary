'''
1. 枚举
(1) 由于总可能比较小为1440, 比较小, 所以没有枚举所有可能性计算
(2) f"{i:02d}"生成特定的字符串, all(括号的写法)


2. 位运算, 前缀和
(1) 包含 最少 数目的2的幂 -> 求lowbit, 将lowbit代表的数字求乘积则可以通过前缀和计算
(2) python快速求幂公式
    为了提高运算效率, 可以通过打表运算
(3) 对于前缀和的求解, 注意区间的转化 [i, j] -> [j + 1] - [i]

3. 二分答案; 挖掘性质

3.1 二分答案. 最小化的最大值 -> 二分答案
(1) 思路: 在 [0, max]使用二分法猜测结果; 然后进行check; 如果符合题意则记录
    最后返回结果

(2) 解决方法
    确定区间: [0, max(nums)], 从 0 到 数组最大值进行枚举
    确定check方法:
        自定义check方法, 枚举[1, n - 1]的数字, 判断其平衡之后最大值是否 <= max

3.2 模拟


'''

# 2437. 有效时间的数目
# https://leetcode.cn/problems/number-of-valid-clock-times/


from typing import List


class CountTimeSolution:
    def countTime(self, time: str) -> int:
        # ans = 0
        # # 枚举所有的小时
        # for i in range(24):
        #     # 枚举所有的分钟
        #     for j in range(60):
        #         s = f"{i:02d}:{j:02d}"
        #         ok = True
        #         # 同时遍历两个字符串的字符, 如果出现不相等的情况则标记为错
        #         for t, c in zip(time, s):
        #             if t != '?' and t != c:
        #                 ok = False
        #         if ok:
        #             ans += 1
        # return ans

        # 分别枚举
        def count(time: str, limit: int) -> int:
            ans = 0
            for i in range(limit):
                # 生成固定格式的字符串, 带有前导0的两位字符串
                s = f"{i:02d}"
                # 如果都满足括号里面的条件 则 + 1
                if all(t == "?" or t == c for t, c in zip(time, s)):
                    ans += 1

            return ans

        # 切片分别计算 小时 和 分钟
        h = time[:2]
        m = time[3:]

        return count(h, 24) * count(m, 60)


# 2438. 二的幂数组中查询范围内的乘积
# https://leetcode.cn/problems/range-product-queries-of-powers/


class ProductQueriesSolution:
    def productQueries(self, n: int, queries: List[int]) -> List[int]:
        mod = 10 ** 9 + 7
        s = [0]
        while n:
            lowbit = n & -n
            s.append(s[-1] + lowbit.bit_length() - 1)
            n ^= lowbit

        ans = []
        # q[i, j] 代表 [i + 1 ... j + 1] 之间的数字和 s[j + 1] - s[i]
        for le, ri in queries:
            e = s[ri + 1] - s[le]
            mul = pow(2, e, mod)
            ans.append(mul)

        return ans


'''

'''

# 2439. 最小化数组中的最大值
# https://leetcode.cn/problems/minimize-maximum-of-array/


class MinimizeArrayValueSolution:
    def minimizeArrayValue(self, nums: List[int]) -> int:
        '''
        方法一: 二分答案
        '''
        # def check(limit: int) -> bool:
        #     # extra代表累计负载量
        #     extra = 0
        #     # 遍历所有的 具有前缀的元素
        #     for i in range(len(nums) - 1, 0, -1):
        #         # 将当前数组加上 累计负载量 判断与 limit的大小
        #         x = nums[i] + extra
        #         if x > limit:
        #             extra = x - limit
        #         else:
        #             # 清空累积负载
        #             extra = 0

        #     return nums[0] + extra <= limit

        # # 选择刚好符合check的最小值
        # # python 自定义api
        # return bisect_left(range(max(nums)), True, key=check)

        # # left, right = 0, max(nums)
        # # while left < right:
        # #     mid = (left + right) // 2
        # #     # 如果返回true, 此时 limit较大，选择左边区间
        # #     if check(mid):
        # #         right = mid
        # #     else:
        # #         # 此时limit较小，选择右边区间
        # #         right = mid + 1
        # # return left

        '''
        方法二：
        '''


# 2226. 每个小孩最多能分到多少糖果
# https: // leetcode.cn/problems/maximum-candies-allocated-to-k-children/

class MaximumCandiesSolution:
    def maximumCandies(self, candies: List[int], k: int) -> int:
        # 主要在于check方法的书写
        def check(limit: int) -> bool:
            j = 0
            for i, v in enumerate(candies):
                cnt = v // limit
                if cnt > 0:
                    j += cnt

            return j >= k

        left = 0
        right = max(candies)
        while left < right:
            mid = (right + left + 1) // 2
            if check(mid):
                left = mid
            else:
                right = mid - 1

        return left


# 2187. 完成旅途的最少时间
# https://leetcode.cn/problems/minimum-time-to-complete-trips/

class MinimumTimeSolution:
    # 二分答案的check方法
    def minimumTime(self, time: List[int], totalTrips: int) -> int:
        def check(limit: int) -> bool:
            cnt = 0
            for i in time:
                cnt += limit // i

            return cnt >= totalTrips

        left = 0
        right = totalTrips * min(time)

        while left < right:
            mid = (left + right) // 2
            if check(mid):
                right = mid
            else:
                left = mid + 1

        return left



