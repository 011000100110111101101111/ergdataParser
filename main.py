# Combining local directory query output
import glob
# Moving files
import shutil
from calendar import monthrange
from datetime import datetime
from os import listdir, path

# Data manipulation
import pandas as pd

# Global shortcut for reading CSV files
columns = ["Log ID", "Date", "Work Distance", "Work Time (Seconds)", "Total Cal", "Avg Heart Rate", "Drag Factor", "Type"]

def update_data():
  # Reading a new CSV file
  csv_files = glob.glob('*.csv')

  # Quick skip instead of evaluating the rest when running without updated csvs.
  if 'master.csv' in csv_files and len(csv_files) == 1:
    return pd.read_csv('master.csv',usecols=columns)

  if 'master.csv' not in csv_files:
    # lets write master with the first then continue normally
    new_data = pd.read_csv(csv_files[0],usecols=columns)
    new_data.to_csv('master.csv', index=False)
    csv_files.remove(csv_files[0])
    print("Master file created.")
    if len(csv_files) >= 1:
      for csv_file in csv_files:
        new_data = pd.read_csv(csv_file,usecols=columns)
        new_data.to_csv('master.csv', index=False, mode='a', header=False)
  else: # Only update if we already had master file.
    # Reading Existing Master CSV file
    csv_files.remove('master.csv')
    for csv_file in csv_files:
      print("writing file " + csv_file)
      new_data = pd.read_csv(csv_file,usecols=columns)
      master_data = pd.read_csv('master.csv',usecols=columns)
      # Find any Log IDS that are new and dont exist in our master file
      diff = new_data[~new_data['Log ID'].isin(master_data['Log ID'])]
      # Check if diff is empty
      if not diff.empty:
          # Append these "new" Log IDs to our master file
          diff.to_csv('master.csv', mode='a', header=False, index=False)
          return pd.read_csv('master.csv',usecols=columns)
      else:
          print("No new Log IDs found.")
  return pd.read_csv('master.csv',usecols=columns)

########################################################################################
# Calories

def get_todays_calories(data):
  # Calories burned TODAY
  # Sum of all calories
  return data['Total Cal'].sum()

def get_average_calories(data, days):
    # Sum of all calories
    return data['Total Cal'].sum() / days

def get_lifetime_calories(data):
  # Calories burned in lifetime
  return data['Total Cal'].sum()

def get_lifetime_workout_average_calories(data):
  # Average calories burned per day in lifetime
  return data['Total Cal'].mean()


########################################################################################
# Distance

def get_todays_distance(data):
  # Distance row for today
  return data['Work Distance'].sum()

def get_average_distance(data, days):
  # Distance row average for month
  return data['Work Distance'].sum() / days

def get_lifetime_distance(data):
  # Distance row in lifetime
  return data['Work Distance'].sum()

def get_lifetime_workout_average_distance(data):
  # Average distance rowed per workout in lifetime
  return data['Work Distance'].mean()

########################################################################################
# Time

def get_todays_time(data):
  # Time row for today
  return data['Work Time (Seconds)'].sum()

def get_average_time(data, days):
  # Time row average for month
  return data['Work Time (Seconds)'].sum() / days

def get_lifetime_time(data):
  # Time row in lifetime
  return data['Work Time (Seconds)'].sum()

def get_lifetime_workout_average_time(data):
  # Average time rowed per workout in lifetime
  return data['Work Time (Seconds)'].mean()

########################################################################################
# Small Helpers
def get_current_month(data):
    first_day_of_month = pd.Timestamp.now() - pd.offsets.MonthBegin(1)
    # Filter rows based on current month
    this_month_data = data[pd.to_datetime(data['Date']) >= first_day_of_month]
    return this_month_data

def quantify_calories(calories):
  # Customizable aspect, recommend changing to foods you eat daily
  if calories < 100:
    return "A fiber one bar"
  elif calories < 150:
    return "A banana"
  elif calories < 200:
    return "A protein bar"
  elif calories < 250:
    return "An avocado"
  elif calories < 300:
    return "A protein bar and fiber one bar"
  elif calories < 400:
    return "Morning bagel"
  elif calories < 500:
    return "Microwavable rice cup"
  elif calories < 600:
    return "Microwavable rice cup with cheese"
  elif calories < 700:
    return "Microwavable rice cup with cheese and guac"
  else:
    return "Go eat whatever you want, you earned it."


def get_lifetime_usage(data):
  # Lifetime usage
  earliest_date = pd.to_datetime(data['Date']).min()
  current_date = pd.Timestamp.now()
  days_used = (current_date - earliest_date).days
  return days_used

def seconds_to_minutes(seconds):
  minutes = int(seconds // 60)
  leftover_seconds = int(seconds % 60)
  hours = int(minutes // 60)
  leftover_minutes = int(minutes % 60)
  days = int(hours // 24)
  leftover_hours = int(hours % 24)
  years = int(days // 365)
  leftover_days = int(days % 365)
  if years == 0 and leftover_days == 0 and leftover_hours == 0 and leftover_minutes == 0:
    return f"{leftover_seconds} seconds"
  elif years == 0 and leftover_days == 0 and leftover_hours == 0:
    return f"{leftover_minutes} minutes {leftover_seconds} seconds"
  elif years == 0 and leftover_days == 0:
    return f"{leftover_hours} hours {leftover_minutes} minutes {leftover_seconds} seconds"
  elif years == 0:
    return f"{leftover_days} days {leftover_hours} hours {leftover_minutes} minutes {leftover_seconds} seconds"
  else:
    # Holyyyyyyyy god if you got here
    return f"{years} years {leftover_days} days {leftover_hours} hours {leftover_minutes} minutes {leftover_seconds} seconds"

########################################################################################
# Different Use-cases
def daily_stats(data):
  current_date = datetime.now()
  # Filter rows based on current date
  todays_data = data[pd.to_datetime(data['Date']).dt.date == current_date.date()]
  # Average calories this month
  print("-"*40 + "\n")
  print(f"{'Daily Stats for:':<40} {datetime.now().strftime('%B %d %Y')}" + "\n")
  today_cals = get_todays_calories(todays_data)
  if not today_cals == 0:
    print(f"{'Total calories burned:':<40} {today_cals}")
    print(f"{'Calories quantified:':<40} {quantify_calories(today_cals)}")
    print(f"{'Total distance rowed:':<40} {get_todays_distance(todays_data)}")
    print(f"{f'Total time rowed:':<40} {seconds_to_minutes(get_todays_time(todays_data))}")
  else:
    print(f"{'No data for today.':<40} {"Get to it!"}")

  print("\n" + "-"*40)

def monthly_stats(data):
  # We will perform most stats on a monthly basis as to reduce larger datasets.
  working_month = get_current_month(data)
  # Get current date
  current_date = datetime.now()
  # Calculate number of days into the current month
  days_into_month = current_date.day
  # How many days our in OUR month
  _, total_days_in_month = monthrange(current_date.year, current_date.month)
  # Average calories this month
  print("\n\n" + "-"*40 + "\n\n")
  print(f"{'Monthly Stats for:':<40} {current_date.strftime('%B %Y')} ({days_into_month}/{total_days_in_month})")
  print("\n")
  print(f"{'Total calories burned:':<40} {get_average_calories(working_month, 1)} calories")
  print(f"{'Average calories burned per day:':<40} {get_average_calories(working_month, days_into_month)} calories")
  print(f"{'Average distance rowed per day:':<40} {get_average_distance(working_month, days_into_month)} meters")
  print(f"{'Average time rowed per day:':<40} {seconds_to_minutes(get_average_time(working_month, days_into_month))}")

  print("\n\n" + "-"*40 + "\n\n")

def lifetime_stats(data):
  total_days = get_lifetime_usage(data)
  print("\n\n" + "-"*40 + "\n\n")
  print(f"{'Lifetime Stats':<40}" + "\n")
  print(f"{'First workout:':<40} {total_days} days ago")
  print(f"{'Total workouts:':<40} {len(data)} workouts")
  print(f"{'Average workout percentage:':<40} {len(data) / total_days * 100:.2f}%")
  print("\n")
  print(f"{'Total calories burned:':<40} {get_lifetime_calories(data)} calories")
  print(f"{'Average calories burned per workout:':<40} {get_lifetime_workout_average_calories(data):.2f} calories")
  print(f"{'Total distance rowed:':<40} {get_lifetime_distance(data)} meters")
  print(f"{'Average distance rowed per workout:':<40} {get_lifetime_workout_average_distance(data):.2f} meters")
  print(f"{'Total time rowed:':<40} {seconds_to_minutes(get_lifetime_time(data))}")
  print(f"{'Average time rowed per workout:':<40} {seconds_to_minutes(get_lifetime_workout_average_time(data))}")
  print("\n\n" + "-"*40)

########################################################################################
# Main

def main():
  # Full dataset
  all_data = update_data()
  daily_stats(all_data)
  # monthly_stats(all_data)
  # lifetime_stats(all_data)
  # Move all csv files except master.csv to used-reports
  for file_name in listdir('.'):
    if file_name.endswith('.csv') and file_name != 'master.csv':
      new_file_name = file_name.replace('.csv', '_PROCESSED.csv')
      shutil.move(file_name, 'used-reports/' + new_file_name)


main()