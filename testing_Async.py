import asyncio

# Basic async function
async def greet(name):
    # Simulate some async operation (like a database call)
    await asyncio.sleep(1)
    return f"Hello, {name}!"

# Another async function that uses await
async def main():
    # await pauses here until greet() completes
    result = await greet("Alice")
    print(result)
    
    # You can await multiple coroutines
    results = await asyncio.gather(
        greet("Bob"),
        greet("Charlie")
    )
    print(results)

# Run the async program
asyncio.run(main())