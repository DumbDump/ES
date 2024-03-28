# Define the slope of the line segment
slope = 1

# To make it a valid density curve, the area under the curve must equal 1
# Area of a triangle = 0.5 * base * height
# Area = 0.5 * right_endpoint * right_endpoint = 1
# Solve for the right_endpoint
right_endpoint = 2

# Percentage of values below 1
percent_below_1 = (1 / 2) * 100  # Area of the triangle formed by the line segment and x-axis

# Median
median = right_endpoint / 2

# Q1
Q1 = right_endpoint / 4

# Q3
Q3 = 3 * right_endpoint / 4

print("Right-endpoint:", right_endpoint)
print("Percentage of values below 1:", percent_below_1, "%")
print("Median:", median)
print("Q1:", Q1)
print("Q3:", Q3)
