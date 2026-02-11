def sum_numbers(*nums):
    return sum(nums)

def show_user_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print(f"Sum: {sum_numbers(1, 2, 3, 4)})
show_user_info(name="John", age=25)