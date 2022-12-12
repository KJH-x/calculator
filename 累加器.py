# encoding=utf-8
'''
Filename : 累加器.py
Datatime : 2022/12/07 
Author :KJH-x
'''


from traceback import print_exc
import math
import sys


def output(result: ...) -> None:
    # 此函数功能目前不佳，在好的替代方案发现之前
    # 新增的输出内容，直接用print
    if type(result) == "<class 'str'>":
        print(f"==> {result}")
    else:
        # print("---Long Result:---start---")
        print(result)
        # print("---Long Result:--- end ---")
    history.append(result)


def isfloat(expression: str) -> bool:
    if expression.count(".") < 2:
        return expression.replace(".", "").isdigit()
    else:
        return False


def isfunction(expression: str) -> bool:
    for br in Lbracket:
        expression = expression.replace(br, "")
    return expression.isalpha()


def assign_class(operator) -> list:
    for i in range(len(level)):
        if operator in level[i]:
            return [operator, i]
    print(f"Unreachable!,with input={operator}")
    raise ValueError


def flash(command='part') -> None:
    global Ans, last, history
    if command in ['part', 'full']:
        Ans = 0
        last = 0
        if command == 'full':
            history = []


def convert(expression: str) -> list:
    cache = []
    left = right = 0
    # 括号优先级计算，左括号加一级，右括号减一级
    # 输入的括号可不在形式上成对，只要左右个数一致即可
    bracketlevel = 0
    # 输入为空，直接下一轮
    if expression == "":
        output("")
        return []
    # 输入查询记录
    elif expression.lower() in ['memory', 'mem']:
        print(memory)
    # 输入分析：
    while left < len(expression):
        function = ""
        # print(f"==interval left={left} right={right}")
        if expression[left].isdigit():
            # 过程量记录
            # 调用isfloat函数，把小数吃掉
            for right in range(left+1, len(expression)+1):

                if isfloat(expression[left:right]):
                    function = float(expression[left:right])
                else:
                    right -= 1
                    break
            cache.append(function)
            last_type = "number"
            left = right
            continue

        elif expression[left] in rightclass:
            if expression[left] == '!':
                # 阶乘立刻计算
                # 后续可能需要改进，这将导致能约分的出现故障
                cache.append(math.factorial(cache.pop()))
            last_type = "number"
            left += 1
            continue

        elif expression[left] in midclass:
            # 记录二元运算符
            # 二元运算符应等待其后的运算结果
            cache.append(assign_class(expression[left]))
            last_type = "operator"
            left += 1
            continue

        elif expression[left].isalpha():
            # 记录函数
            # 调用isfunction来把一串英文和后随括号给吃掉
            for right in range(left+1, len(expression)+1):
                if isfunction(expression[left:right]):
                    function = [expression[left:right], bracketlevel]
                else:
                    right -= 1
                    break
            if function[0][-1] not in Lbracket:
                print(f"[Warn] {function} is not a function, skipped")

            # 记录的时候记录函数名称
            cache.append(function)
            last_type = "function"
            left = right
            bracketlevel += 1
            continue

        elif expression[left] in Lbracket:
            # 遇到左侧等号，处理后加一级
            cache.append([str(expression)[left], bracketlevel])
            left += 1
            bracketlevel += 1
            continue

        elif expression[left] in Rbracket:
            # 遇到右侧等号，处理前减一级
            bracketlevel -= 1
            cache.append([str(expression)[left], bracketlevel])
            left += 1
            continue

        elif expression[left] in [",", "，"]:
            # 分隔符在结构中已经被不同位置的数字等效，故跳过
            left += 1
            continue

        else:
            print(f"[Warn] IN {left+1}, cannot resolve, skipped.")
            left += 1

    if bracketlevel != 0:
        print("\n\t[ERROR] Bracket not closed!\n")
    return cache


def calculate(cache: list) -> float:
    # working
    return 0


def solve(cache: list) -> float:
    # schedule
    return 0


def a_mode(expression: str) -> ...:
    l = sys._getframe().f_code.co_name
    print(l)
    input(l+">")
    return


def special_mode(mode: str, expression: str) -> ...:
    # 此处用来放置需要特殊使用的模式
    # 比如无限求和的近似、矩阵高级运算等等
    if mode == "a_mode":
        print("\n\ta_mode activated:")
        a_mode(expression)
        print("\n\ta_mode exiting...:")
    return


midclass = ['+', '-', '*', '/', '%', '^', 'A', 'P', 'C',]
rightclass = ['!']
# changelog:[]will no longer be used as general brackets
Lbracket = ['(', '{', '（', '【']
Rbracket = [')', '}', '）',  '】']

level = [
    ["nothing"],
    ["+", "-"],
    ["*", "/", "%"],
    ["^"],
    ["A", "P", "C"],
    ['(', ')', '[', ']', '{', '}', '（', '）', '【', '】']
]


Ans = 0
last = 0
history = []


if __name__ == '__main__':

    memory = []
    last_type = ""
    flash()
    while True:
        try:
            # 输入，去除空格和前后空白符
            expression = input("Basic> ").strip().replace(" ", "")
            # Assume that the mode command should act like:
            # MODE:<><mode_name><space|tab><input|none>
            if expression[0:5].lower() == "mode:":
                i = 0
                for i in range(5, len(expression)):
                    if expression[i] in [' ', '\t']:
                        i -= 1
                        break
                mode = expression[5:i+1]
                if i+1 == len(expression):
                    special_mode(mode, "")
                else:
                    special_mode(mode, expression[i:].lower())
            else:
                # 输入主程序，此步获得输入的完整结构信息
                cache = convert(expression)

                print("==>cache:")
                output(cache)
                if expression.count("=") == 0:
                    calculate(cache)
                else:
                    solve(cache)

        except EOFError:
            Ans = history.pop()
            print(f"==Undo==> Ans = {Ans}")
        except KeyboardInterrupt:
            exit()
        except Exception:
            print_exc()
            input()
