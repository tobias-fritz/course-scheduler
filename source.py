from itertools import combinations
from IPython.display import Markdown
import re


def conflict_courses(course_data):
    # return all courses with conflicting schedule 
    
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        slots = {}
        for course, data in course_data.items():
            for slot in data[0]:
                if day not in slot:
                    continue
                start, end = slot.split(" ")[1].split("-")
                for hour in range(int(start), int(end)):
                    if hour in slots:
                        print(f"Overlap found: {course} and {slots[hour]} overlap on {day} at {hour}:00")
                        
                        # make sure every result is only displayed once (earliest point in time)
                        break 
                    else:
                        slots[hour] = course
                                       

def time_table(course_data, course_list):
    # print out a course combination as a markdown table

    filtered_course_data =  {k: v for k, v in course_data.items() if k in course_list}
    
    def parse_time(time_str):
        # Try to match the time string to a pattern with start and end times
        pattern = r"(\w+)\s*(\d+)-(\d+)"
        match = re.match(pattern, time_str)
        if match:
            # Extract the start and end times from the match
            day_str, start_hour_str, end_hour_str = match.groups()
            start_hour = int(start_hour_str)
            end_hour = int(end_hour_str)

            return start_hour, end_hour, day_str

        # If the time string doesn't match the pattern, raise an error
        raise ValueError(f"Invalid time string: {time_str}")


    # initialize the calendar as a 2D list
    calendar = [[" " for _ in range(5)] for _ in range(24)]

    # loop over each course and mark its time slots in the calendar
    for course, data in filtered_course_data.items():
        course_times, _ = data
        for course_time in course_times:
            start_time, end_time, day_str = parse_time(course_time)
            duration = end_time - start_time
            start_day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].index(day_str)
            end_day = start_day + (duration // 24)
            for day in range(start_day, end_day + 1):
                day_offset = day - start_day
                start_hour = start_time if day_offset == 0 else 0
                end_hour = end_time if day_offset == duration // 24 else 24
                for hour in range(start_hour, end_hour):
                    calendar[hour][day] = course
                    #print(hour,day)

    # print the calendar as a markdown table

    md_str = "| Time | Mon | Tue | Wed | Thu | Fri |\n| ---- | --- | --- | --- | --- | --- |"

    for hour in range(8,20):
        row = [f"{hour:02d}:{'00'}-{hour+1:02d}:{'00'}"]
        for day in range(len(calendar[0])):
            #print(calendar[hour][day])
            row.append(calendar[hour][day])
        md_str = md_str+ "\n|"+" | ".join(row)+ " |"

    display(Markdown(md_str))


def schedules(course_data):
    # generate all possible course combinations without overlaps
    
    combinations_list = []
    for i in range(1, len(course_data) + 1):
        for course_combination in combinations(course_data.keys(), i):
            overlap = False
            schedule = {}
            for course in course_combination:
                for slot in course_data[course][0]:
                    day = slot.split()[0]
                    start, end = slot.split()[1].split("-")
                    for hour in range(int(start), int(end)):
                        if day in schedule and hour in schedule[day]:
                            overlap = True
                            break
                        schedule.setdefault(day, set()).add(hour)
                    if overlap:
                        break
                if overlap:
                    break
            if not overlap:
                combinations_list.append(list(course_combination))
    
    # list of course lists
    return combinations_list


def get_credit_sum(combinations_list):
    # calculate the sum of credits for each course combination

    credit_sums = {}
    for combination in combinations_list:
        credit_sum = sum([course_data[course][1] for course in combination])
        credit_sums[tuple(combination)] = credit_sum
    
    return credit_sums


def display_select(combinations_list, credit_sums, lower = 30, higher = 35, required_courses = []):
    # print the course combinations and their credit sums
    
    
    for i, combination in enumerate(combinations_list):
        credit_sum = credit_sums[tuple(combination)]
                
        if lower <= credit_sum < higher and all(course in combination for course in required_courses ):
            print(f"Course combination {i+1} (Credits: {credit_sum}):")
            comb = []
            for course in combination:
                comb.append(course)
                
            time_table(course_data,comb)

