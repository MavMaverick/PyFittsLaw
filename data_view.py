import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('C:/Users/kjpre/OneDrive/Documents/1law/experiment_data.csv')

# Count the total number of unique students
total_unique_students = df['Participant_ID'].nunique()

# Count the number of students who are labeled as 1 or 0
students_count_1 = df[df['Subject Type'] == 1]['Participant_ID'].nunique()
students_count_0 = df[df['Subject Type'] == 0]['Participant_ID'].nunique()

print("Total number of unique students:", total_unique_students)
print("Number of students who are labeled as 1:", students_count_1)
print("Number of students who are labeled as 0:", students_count_0)
