# # class Solution(object):
# #     def isPalindrome(self, x):
# #         """
# #         :type x: int
# #         :rtype: bool
# #         """
# #         if x < 0:
# #             return False

# #         temp = x
# #         res = 0
# #         while temp:
# #             res = int(res * 10 + (temp % 10))
# #             print(res)
# #             temp = int(temp / 10)

# #         print("this is res", res)
# #         return res == x

# # sol = Solution()
# # print(sol.isPalindrome(144))


# class Solution:
#     def twoSum(self, numbers: list[int], target: int) -> list[int]:
#         for index, i_num in enumerate(numbers):
#             for jndex, j_num in enumerate(numbers[1:], 1):
#                 if i_num + j_num == target:
#                     return [index + 1, jndex + 1]




# sol = Solution()
# print(sol.twoSum([1, 2, 3, 4], 3))

import re

text = "[color= green zone  =  normal max_drones = 1"
text = re.sub(r"\s+", " ", text).strip()
text = re.sub(r"\s+=", "=", text).strip()
text = re.sub(r"=\s+", "=", text).strip()
text = re.sub(r"\s+=\s+", "=", text).strip()
print(text)
