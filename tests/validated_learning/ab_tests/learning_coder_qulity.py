import pytest
import asyncio
from centaur_workspace.tools.code_writing_tool import CodeWritingTool
from centaur_workspace.llm_providers.openai_provider import OpenAIProvider


# Define the test questions and expected results
TEST_QUESTIONS = [
    {
        "task": "write a function to calculate factorial",
        "function_name": "factorial",
        "tests": [
            {"input": 0, "expected": 1},
            {"input": 5, "expected": 120},
        ],
    },
    {
        "task": "write a function to find prime numbers up to n",
        "function_name": "find_primes",
        "tests": [
            {"input": 20, "expected": [2, 3, 5, 7, 11, 13, 17, 19]},
        ],
    },
    {
        "task": "write a function to calculate Fibonacci sequence up to n",
        "function_name": "fibonacci",
        "tests": [
            {"input": 10, "expected": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]},
        ],
    },
    {
        "task": "write a function to check if a string is a palindrome",
        "function_name": "is_palindrome",
        "tests": [
            {"input": "racecar", "expected": True},
            {"input": "hello", "expected": False},
        ],
    },
    {
        "task": "write a function to sort a list of numbers",
        "function_name": "sort_numbers",
        "tests": [
            {
                "input": [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
                "expected": [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9],
            },
        ],
    },
    {
        "task": "write a function to find the greatest common divisor of two numbers",
        "function_name": "gcd",
        "tests": [
            {"input": (48, 18), "expected": 6},
        ],
    },
    {
        "task": "write a function to implement binary search on a sorted list",
        "function_name": "binary_search",
        "tests": [
            {"input": ([1, 2, 3, 4, 5, 6, 7, 8, 9], 6), "expected": 5},
            {"input": ([1, 2, 3, 4, 5, 6, 7, 8, 9], 10), "expected": -1},
        ],
    },
    {
        "task": "write a function to compute the n-th number "
        "in the Catalan number sequence",
        "function_name": "catalan_number",
        "tests": [
            {"input": 0, "expected": 1},
            {"input": 5, "expected": 42},
        ],
    },
    {
        "task": "write a function to calculate the "
        "Levenshtein distance between two strings",
        "function_name": "levenshtein_distance",
        "tests": [
            {"input": ("kitten", "sitting"), "expected": 3},
            {"input": ("flaw", "lawn"), "expected": 2},
        ],
    },
    {
        "task": "write a function to solve the knapsack problem",
        "function_name": "knapsack",
        "tests": [
            {"input": ([60, 100, 120], [10, 20, 30], 50), "expected": 220},
        ],
    },
]


async def run_test(tool, test_case):
    results = []
    # Generate and test the function code
    code = await tool._arun(test_case["task"])
    exec(code, globals())

    function_name = test_case["function_name"]
    if function_name not in globals():
        results.append(
            {
                "function_name": function_name,
                "task": test_case["task"],
                "status": "Function not defined",
                "details": "",
            }
        )
        return results

    for test in test_case["tests"]:
        function = globals()[function_name]
        try:
            if isinstance(test["input"], tuple):
                result = function(*test["input"])  # noqa: F821
            else:
                result = function(test["input"])  # noqa: F821
            if result == test["expected"]:
                status = "Passed"
                details = ""
            else:
                status = "Failed"
                details = f"Returned {result}, expected {test['expected']}"
        except Exception as e:
            status = "Error"
            details = str(e)

        results.append(
            {
                "function_name": function_name,
                "task": test_case["task"],
                "status": status,
                "details": details,
            }
        )
    return results


class CustomCodeWritingTool(CodeWritingTool):
    pass  # No customization needed for OpenAI


def print_summary(all_results, model_name):
    total_tests = len(all_results)
    passed_tests = sum(1 for res in all_results if res["status"] == "Passed")
    percentage = (passed_tests / total_tests) * 100

    print(f"\nSummary for {model_name}:")
    print(f"Total tests: {total_tests}")
    print(f"Passed tests: {passed_tests}")
    print(f"Failed tests: {total_tests - passed_tests}")
    print(f"Score: {percentage:.2f}%\n")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_coder_quality_gpt35():
    tool = CustomCodeWritingTool(llm_provider=OpenAIProvider(model="gpt-3.5-turbo"))
    all_results = []
    tasks = [run_test(tool, test_case) for test_case in TEST_QUESTIONS]
    results = await asyncio.gather(*tasks)
    for result in results:
        all_results.extend(result)

    print_summary(all_results, "GPT-3.5")


@pytest.mark.asyncio
@pytest.mark.integration
async def test_coder_quality_gpt40():
    tool = CustomCodeWritingTool(llm_provider=OpenAIProvider(model="gpt-4"))
    all_results = []
    tasks = [run_test(tool, test_case) for test_case in TEST_QUESTIONS]
    results = await asyncio.gather(*tasks)
    for result in results:
        all_results.extend(result)

    print_summary(all_results, "GPT-4")


if __name__ == "__main__":
    asyncio.run(test_coder_quality_gpt35())
    asyncio.run(test_coder_quality_gpt40())
