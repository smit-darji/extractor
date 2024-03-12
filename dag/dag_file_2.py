def example_function_21():
    try:
        result = int("hello")
        print("Result:", result)
    except ValueError as e:
        print("Error:", e)
    except TypeError as e:
        print("Error:", e)
