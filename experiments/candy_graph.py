import pandas as pd
import matplotlib.pyplot as plt

# Replace with your actual file path
input_csv = 'candy_robot_communication_test.csv'
output_csv = 'candy_robot_communication_test_compiled.csv'

# Load the CSV data
df = pd.read_csv(input_csv)

# Ensure duration is numeric
df['duration'] = pd.to_numeric(df['duration'], errors='coerce')

# Group by 'x' then 'y', sum and average 'duration'
summary_df = df.groupby(['x', 'y']).agg(
    total_duration=('duration', 'sum'),
    average_duration=('duration', 'mean'),
    count=('duration', 'size')
).reset_index()

# Save to a new CSV
summary_df.to_csv(output_csv, index=False)

# Create a combined category for plotting
summary_df['x_y'] = summary_df['x'].astype(str) + '_' + summary_df['y'].astype(str)

# Plot the graph
plt.figure(figsize=(12, 6))
plt.bar(summary_df['x_y'], summary_df['average_duration'], color='lightgreen')
plt.xlabel('X_Y Combination')
plt.ylabel('Vidutinis paėmimo ir padėjimo laikas, s')
plt.title('Vidutinis paėmimo ir padėjimo pirmosios kategorijos objektų laikas')
plt.xticks(rotation=90)

# Adjust Y-axis limits
min_duration = summary_df['average_duration'].min() - 0.1
max_duration = summary_df['average_duration'].max() + 0.1
plt.ylim(min_duration, max_duration)

plt.tight_layout()

# Show the graph
plt.show()

print(f"Summary saved to {output_csv}")