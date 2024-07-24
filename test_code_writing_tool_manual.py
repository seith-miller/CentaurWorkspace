from centaur_workspace.tools.code_writing_tool import CodeWritingTool
import asyncio
from dotenv import load_dotenv


async def main():
    load_dotenv()

    tool = CodeWritingTool()

    print("Testing synchronous run (Calculate factorial):")
    result = tool._run("calculate factorial")
    print(result)
    print("\n" + "-" * 50 + "\n")

    print("Testing asynchronous run (Sort a list):")
    result = await tool._arun("sort a list")
    print(result)
    print("\n" + "-" * 50 + "\n")

    print("Testing another case (Find prime numbers):")
    result = await tool._arun("find prime numbers up to n")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
