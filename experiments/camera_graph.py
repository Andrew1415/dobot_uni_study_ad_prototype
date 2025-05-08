import pandas as pd
import matplotlib.pyplot as plt

# Replace with your actual file path
input_csv = 'candy_location_finding_test.csv'
output_csv = 'candy_location_finding_test_compiled.csv'

# Load the CSV data
df = pd.read_csv(input_csv)

# Ensure duration is numeric
df['duration'] = pd.to_numeric(df['duration'], errors='coerce')

# Group by 'Category', sum and average 'duration'
summary_df = df.groupby('Category').agg(
    total_duration=('duration', 'sum'),
    average_duration=('duration', 'mean'),
    count=('duration', 'size')
).reset_index()

# Save to a new CSV
summary_df.to_csv(output_csv, index=False)

# Define colors based on category name
def get_color(category):
    if 'Red' in category:
        return '#FF4933'
    else:
        return '#D8A900'

# Apply color mapping
colors = summary_df['Category'].apply(get_color)

# Plot the graph with custom colors
plt.figure(figsize=(10,6))
plt.bar(summary_df['Category'], summary_df['average_duration'], color=colors)
plt.xlabel('Pirmos kategorijos objektai')
plt.ylabel('Vidutinis objekto lokacijos radimo laikas, s')
plt.title('Vidutinis pirmos kategorijos \n objektų lokacijos radimo laikas')
plt.xticks(rotation=45)

# Adjust Y-axis limits
min_duration = summary_df['average_duration'].min() - 0.05
max_duration = summary_df['average_duration'].max() + 0.05
plt.ylim(min_duration, max_duration)


plt.tight_layout()

# Show the graph
plt.show()

print(f"Summary saved to {output_csv}")