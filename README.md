# pyrand
Generates cryptographically secure pseudo random numbers. 

This Python module provides functions for generating random numbers using various entropy sources, such as weather data, time, and built-in Python randomness.

Functions
- randint(min: int, max: int) -> int: Generates a random integer within the specified range.
- uniform(min: int, max: int) -> float: Generates a random float within the specified range.
- random() -> float: Generates a random float between 0 and 1.
- choice(lst): Returns a random element from the input list.
- randintLst(min: int, max: int, length: int) -> list: Generates a list of random integers within the specified range.
- uniformLst(min: int, max: int, length: int) -> list: Generates a list of random floats within the specified range.
- shuffle(lst: list) -> list: Shuffles the input list using a random hash.
- sample(lst, numSamples) -> list: Generates a list of unique elements randomly chosen from the input list.

Dependencies
This module requires the following dependencies:
- requests
- hashlib
- time
- random
