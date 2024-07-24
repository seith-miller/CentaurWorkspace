from centaur_workspace.tools.code_writing_tool import CodeWritingTool
import asyncio
from dotenv import load_dotenv


def main():
    load_dotenv()

    tool = CodeWritingTool()

    # Test synchronous run
    print("Testing synchronous run (Calculate factorial):")
    result = tool._run("calculate factorial of a number")
    print(result)
    print("\n" + "-" * 50 + "\n")

    # Test asynchronous run
    print("Testing asynchronous run (Sort a list):")

    async def async_test():
        result = await tool._arun("sort a list of numbers")
        print(result)

    asyncio.run(async_test())

    print("\n" + "-" * 50 + "\n")

    # Test another case
    print("Testing another case (Find prime numbers):")
    result = tool._run("find prime numbers up to n")
    print(result)


if __name__ == "__main__":
    main()
