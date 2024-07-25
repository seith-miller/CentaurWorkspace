import pytest
import asyncio
from centaur_workspace.tools.code_writing_tool import CodeWritingTool


@pytest.mark.asyncio
@pytest.mark.integration
async def test_factorial_integration():
    tool = CodeWritingTool()

    # Generate factorial code
    code = await tool._arun("write a function to calculate factorial")

    # Execute the generated code
    exec(code, globals())

    # Test the factorial function
    assert "factorial" in globals(), "Factorial function not defined"
    assert factorial(0) == 1  # noqa: F821
    assert factorial(5) == 120  # noqa: F821


@pytest.mark.asyncio
@pytest.mark.integration
async def test_prime_numbers_integration():
    tool = CodeWritingTool()

    # Generate prime numbers code
    code = await tool._arun("write a function to find prime numbers up to n")

    # Execute the generated code
    exec(code, globals())

    # Test the prime numbers function
    assert "find_primes" in globals(), "find_primes function not defined"
    primes = find_primes(20)  # noqa: F821
    assert primes == [2, 3, 5, 7, 11, 13, 17, 19], "Incorrect prime numbers generated"


if __name__ == "__main__":
    asyncio.run(test_factorial_integration())
    asyncio.run(test_prime_numbers_integration())
