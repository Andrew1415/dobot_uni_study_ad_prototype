import pandas as pd
import matplotlib.pyplot as plt

input_csv = 'candy_robot_communication_test.csv'
output_csv = 'candy_robot_communication_test_compiled.csv'

df = pd.read_csv(input_csv)

df['x'] = df['x'] + 1
df['y'] = df['y'] + 1

df['duration'] = pd.to_numeric(df['duration'], errors='coerce')

summary_df = df.groupby(['x', 'y']).agg(
    total_duration=('duration', 'sum'),
    average_duration=('duration', 'mean'),
    count=('duration', 'size')
).reset_index()

summary_df.to_csv(output_csv, index=False)

summary_df['x_y'] = summary_df['x'].astype(str) + '_' + summary_df['y'].astype(str)

plt.figure(figsize=(12, 6))
plt.bar(summary_df['x_y'], summary_df['average_duration'], color='lightgreen')
plt.xlabel('Pirmos kategorijos objektų lokacijos (eilutė_stulpelis)\nkiekvienai lokacijai daryta 10 eksperimentų ir išvestas vidurkis')
plt.ylabel('Vidutinis paėmimo ir padėjimo laikas, s')
plt.title('Vidutinis paėmimo ir padėjimo pirmosios kategorijos objektų laikas')
plt.xticks(rotation=90)

min_duration = summary_df['average_duration'].min() - 0.1
max_duration = summary_df['average_duration'].max() + 0.1
plt.ylim(min_duration, max_duration)

plt.tight_layout()

plt.show()

# Plot 1: Average duration grouped by X
avg_duration_x = df.groupby('x')['duration'].mean().reset_index()
plt.figure(figsize=(10, 5))
plt.bar(avg_duration_x['x'].astype(str), avg_duration_x['duration'], color='skyblue')
plt.xlabel('Pirmos kategorijos lokacijų grupavimas eilutėmis')
plt.ylabel('Vidutinis užduoties atlikimo periodas, s')
plt.title('Vidutinis paėmimo ir padėjimo pirmosios kategorijos objektų periodo kitimas nuo trumpiausio iki ilgiausio')
min_duration = summary_df['average_duration'].min() - 0.1
max_duration = summary_df['average_duration'].max() + 0.1
plt.ylim(min_duration, max_duration)
plt.tight_layout()
plt.show()

# Plot 2: Duration from Lowest to Highest
sorted_df = summary_df.sort_values('average_duration')
plt.figure(figsize=(12, 6))
plt.plot(sorted_df['x_y'], sorted_df['average_duration'], marker='o', linestyle='-', color='salmon')
plt.xlabel('Pirmos kategorijos objektų lokacijos (eilutė_stulpelis)\nkiekvienai lokacijai daryta 10 eksperimentų ir išvestas vidurkis')
plt.ylabel('Vidutinis užduoties atlikimo periodas, s')
plt.title('Vidutinis paėmimo ir padėjimo pirmosios kategorijos objektų periodo kitimas nuo trumpiausio iki ilgiausio')
plt.xticks(rotation=90)
min_duration = summary_df['average_duration'].min() - 0.1
max_duration = summary_df['average_duration'].max() + 0.1
plt.ylim(min_duration, max_duration)
plt.grid(which='major', linestyle='-', linewidth=0.75, alpha=0.7)
plt.tight_layout()
plt.show()


print(f"Summary saved to {output_csv}")