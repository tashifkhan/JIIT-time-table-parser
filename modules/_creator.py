import json
from datetime import datetime

def batch_extractor(text):
    start_bracket = text.find('(')
    if start_bracket != -1:
        return text[1:start_bracket].strip()
    return ""

def subject_extractor(text):
    start_bracket = text.find('(')
    if start_bracket != -1:
        end_bracket = text.find(')', start_bracket)
        if end_bracket != -1:
            return text[start_bracket + 1:end_bracket]
    return ""

def location_extractor(text):
    start_dash = text.find('-')
    if start_dash != -1:
        end_slash = text.find('/', start_dash)
        if end_slash != -1:
            return text[start_dash + 1:end_slash]
    return ""

def subject_name_extractor(subjects_dict, code):
    for i in range(len(subjects_dict["Code"])):
        if subjects_dict["Code"][i] == code:
            return subjects_dict["Subject"][i]
    return ""

def time_table_creator(time_table_json_string, subject_json_string, batch, electives_subject_codes):
    time_table = json.loads(time_table_json_string)
    subject = subject_json_string
    your_time_table = []

    for day, it in time_table.items():
        for time, classes in it.items():
            for indi_class in classes:
                subjectCode = indi_class.strip()
                code = subject_extractor(subjectCode)
                if batch in batch_extractor(indi_class.strip()) and "-" not in batch_extractor(indi_class.strip()):
                    if len(indi_class.strip()) > 0:
                        your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                for elective_code in electives_subject_codes:
                    if len(indi_class)>0 and indi_class[0] != "P":
                        if subject_extractor(indi_class) == elective_code:
                            extracted_batch = batch_extractor(indi_class)
                            if ("-" not in extracted_batch) or ("," not in extracted_batch):
                                if len(extracted_batch) in [0,3]:
                                    your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                                elif len(extracted_batch) == 1:
                                    if extracted_batch == batch[0]:
                                        your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                                elif len(extracted_batch) == 2:
                                    for letter in extracted_batch:
                                        your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                            if ("," in extracted_batch):
                                batch_list = extracted_batch.split(",")
                                for index, b in enumerate(batch_list):
                                    if len(batch_list) > 3:
                                        if b.strip()[0].isalpha():
                                            if b.strip()[0] == batch[0]:
                                                batch_list[index] = b[1:]
                                                if batch_list[index] == batch[1:]:
                                                    your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                            else: 
                                                break
                                        else:
                                            if b == batch[1:]:
                                                your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                                    else:
                                        if b.strip()[0] == batch[0]:
                                            if len(b.strip()) == 1:
                                                your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                            else:
                                                batch_nums = ((b.strip())).split("-")
                                                if len(batch) > 1 and all(len(num.strip()) > 1 for num in batch_nums):
                                                    batch_number_str = batch.strip()[1:]

                                                    if batch_number_str:
                                                        batch_number = int(batch_number_str)

                                                        batch_num_0 = int(batch_nums[0].strip()[1:])
                                                        batch_num_1 = int(batch_nums[1].strip()[1:])

                                                        if batch_num_0 <= batch_number <= batch_num_1:
                                                            your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                                    else:
                                                        print("Batch string is empty or incorrectly sliced.")
                                                else:
                                                    print("Batch string or batch_nums are incorrectly formatted.")

    def process_day(day_str):
        day_mapping = {
            'MON': 'Monday',
            'M': 'Monday',
            'MONDAY': 'Monday',
            'TUES': 'Tuesday',
            'TUE': 'Tuesday',
            'T': 'Tuesday',
            'TUESDAY': 'Tuesday',
            'WED': 'Wednesday',
            'W': 'Wednesday',
            'WEDNESDAY': 'Wednesday',
            'THUR': 'Thursday',
            'THURS': 'Thursday',
            'THURSDAY': 'Thursday',
            'THU': 'Thursday',
            'TH': 'Thursday',
            'FRI': 'Friday',
            'FRIDAY': 'Friday',
            'F': 'Friday',
            'SAT': 'Saturday',
            'S': 'Saturday',
            'SA': 'Saturday',
            'SATURDAY': 'Saturday',
            'SATUR': 'Saturday',
            'SUN': 'Sunday',
            'SU': 'Sunday',
            'U': 'Sunday',
            'SUNDAY': 'Sunday'
        }
        
        day_str = day_str.strip().upper()
        return day_mapping.get(day_str, day_str)

    def convert_time_format(time_str):
        # Remove extra spaces
        time_str = time_str.strip().replace(' ', '')
        
        # Ensure the time string contains minutes
        if 'AM' in time_str or 'PM' in time_str:
            if ':' not in time_str:
                time_str = time_str.replace('AM', ':00 AM').replace('PM', ':00 PM')
        
        # Format to ensure no extra spaces
        time_str = time_str.replace('AM', ' AM').replace('PM', ' PM')
        
        try:
            # Convert 12-hour format to 24-hour format
            return datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M')
        except ValueError as e:
            raise ValueError(f"Error parsing time string '{time_str}': {e}")

    def process_timeslot(timeslot):
        # Split the timeslot into start and end times
        start_time, end_time = timeslot.split('-')
        
        # Handle cases with or without AM/PM
        start_time = start_time.strip()
        end_time = end_time.strip().replace('.', ':')
        
        # Assuming AM/PM is consistent and provided
        if not ('AM' in start_time or 'PM' in start_time):
            start_time += " AM"
        if not ('AM' in end_time or 'PM' in end_time):
            end_time += " AM"
        
        # Convert times to 24-hour format
        return convert_time_format(start_time), convert_time_format(end_time)

    formatted_timetable = {}

    for entry in your_time_table:
        day = process_day(entry[0])
        time = entry[1]
        start_time, end_time = process_timeslot(time)
        
        if day not in formatted_timetable:
            formatted_timetable[day] = {}
        
        formatted_timetable[day][f"{start_time}-{end_time}"] = {
            "subject_name": entry[2],
            "type": entry[3],
            "location": entry[4]
        }

if __name__ == "__main__":
    with open("./data/json/time_table.json", 'r') as file:
        time_table = json.load(file)

    with open("./data/json/subject.json", 'r') as file:
        subject = json.load(file)

    your_time_table = []

    batch = input("Enter your Batch: ").upper().strip()
    electives_subject_codes = []
    n = int(input("Number of electives you have: "))
    for i in range(n):
        electives_subject_codes.append(input("Enter the subject code of the elective (shortttened one): ").upper().strip())

    for day, it in time_table.items():
        for time, classes in it.items():
            for indi_class in classes:
                subjectCode = indi_class.strip()
                code = subject_extractor(subjectCode)
                if batch in batch_extractor(indi_class.strip()) and "-" not in batch_extractor(indi_class.strip()):
                    if len(indi_class.strip()) > 0:
                        your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                for elective_code in electives_subject_codes:
                    if len(indi_class)>0 and indi_class[0] != "P":
                        if subject_extractor(indi_class) == elective_code:
                            extracted_batch = batch_extractor(indi_class)
                            if ("-" not in extracted_batch) or ("," not in extracted_batch):
                                if len(extracted_batch) in [0,3]:
                                    your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                                elif len(extracted_batch) == 1:
                                    if extracted_batch == batch[0]:
                                        your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                                elif len(extracted_batch) == 2:
                                    for letter in extracted_batch:
                                        your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                            if ("," in extracted_batch):
                                batch_list = extracted_batch.split(",")
                                for index, b in enumerate(batch_list):
                                    if len(batch_list) > 3:
                                        if b.strip()[0].isalpha():
                                            if b.strip()[0] == batch[0]:
                                                batch_list[index] = b[1:]
                                                if batch_list[index] == batch[1:]:
                                                    your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                            else: 
                                                break
                                        else:
                                            if b == batch[1:]:
                                                your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                                    else:
                                        if b.strip()[0] == batch[0]:
                                            if len(b.strip()) == 1:
                                                your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                            else:
                                                batch_nums = ((b.strip())).split("-")
                                                if len(batch) > 1 and all(len(num.strip()) > 1 for num in batch_nums):
                                                    batch_number_str = batch.strip()[1:]

                                                    if batch_number_str:
                                                        batch_number = int(batch_number_str)

                                                        batch_num_0 = int(batch_nums[0].strip()[1:])
                                                        batch_num_1 = int(batch_nums[1].strip()[1:])

                                                        if batch_num_0 <= batch_number <= batch_num_1:
                                                            your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                                    else:
                                                        print("Batch string is empty or incorrectly sliced.")
                                                else:
                                                    print("Batch string or batch_nums are incorrectly formatted.")

    def process_day(day_str):
        day_mapping = {
            'MON': 'Monday',
            'M': 'Monday',
            'MONDAY': 'Monday',
            'TUES': 'Tuesday',
            'TUE': 'Tuesday',
            'T': 'Tuesday',
            'TUESDAY': 'Tuesday',
            'WED': 'Wednesday',
            'W': 'Wednesday',
            'WEDNESDAY': 'Wednesday',
            'THUR': 'Thursday',
            'THURS': 'Thursday',
            'THURSDAY': 'Thursday',
            'THU': 'Thursday',
            'TH': 'Thursday',
            'FRI': 'Friday',
            'FRIDAY': 'Friday',
            'F': 'Friday',
            'SAT': 'Saturday',
            'S': 'Saturday',
            'SA': 'Saturday',
            'SATURDAY': 'Saturday',
            'SATUR': 'Saturday',
            'SUN': 'Sunday',
            'SU': 'Sunday',
            'U': 'Sunday',
            'SUNDAY': 'Sunday'
        }
        
        day_str = day_str.strip().upper()
        return day_mapping.get(day_str, day_str)

    def convert_time_format(time_str):
        # Remove extra spaces
        time_str = time_str.strip().replace(' ', '')
        
        # Ensure the time string contains minutes
        if 'AM' in time_str or 'PM' in time_str:
            if ':' not in time_str:
                time_str = time_str.replace('AM', ':00 AM').replace('PM', ':00 PM')
        
        # Format to ensure no extra spaces
        time_str = time_str.replace('AM', ' AM').replace('PM', ' PM')
        
        try:
            # Convert 12-hour format to 24-hour format
            return datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M')
        except ValueError as e:
            raise ValueError(f"Error parsing time string '{time_str}': {e}")

    def process_timeslot(timeslot):
        # Split the timeslot into start and end times
        start_time, end_time = timeslot.split('-')
        
        # Handle cases with or without AM/PM
        start_time = start_time.strip()
        end_time = end_time.strip().replace('.', ':')
        
        # Assuming AM/PM is consistent and provided
        if not ('AM' in start_time or 'PM' in start_time):
            start_time += " AM"
        if not ('AM' in end_time or 'PM' in end_time):
            end_time += " AM"
        
        # Convert times to 24-hour format
        return convert_time_format(start_time), convert_time_format(end_time)

    formatted_timetable = {}

    for entry in your_time_table:
        day = process_day(entry[0])
        time = entry[1]
        start_time, end_time = process_timeslot(time)
        
        if day not in formatted_timetable:
            formatted_timetable[day] = {}
        
        formatted_timetable[day][f"{start_time}-{end_time}"] = {
            "subject_name": entry[2],
            "type": entry[3],
            "location": entry[4]
        }
    
    print(json.dumps(formatted_timetable, indent=4))

''' formated timetable
{
"MON":{
    "10 -10.50 AM":{
        "subject_name":"Data Structures and Algorithms",
        "type":"L",
        "location":"G7"
    },
    "3-3.50 PM":{
        "subject_name":"Indian Constitution and Traditional knowledge",
        "type":"L",
        "location":"G8"
    }
},
"TUES":{
    "10 -10.50 AM":{
        "subject_name":"Electromagnetic Field Theory",
        "type":"L",
        "location":"G8"
    },
    "3-3.50 PM":{
        "subject_name":"Data Structures and Algorithms Lab",
        "type":"P",
        "location":"CL04"
    }
},
"WED":{
    "9 -9.50 AM":{
        "subject_name":"Microprocessors and Microcontrollers",
        "type":"P",
        "location":"IOT Lab"
    },
    "1- 1.50 PM":{
        "subject_name":"Data Structures and Algorithms",
        "type":"L",
        "location":"G4"
    },
    "3-3.50 PM":{
        "subject_name":"Indian Constitution and Traditional knowledge",
        "type":"L",
        "location":"G6"
    }
},
"THUR":{
    "9 -9.50 AM":{
        "subject_name":"Indian Constitution and Traditional knowledge",
        "type":"L",
        "location":"G8"
    },
    "10 -10.50 AM":{
        "subject_name":"Electromagnetic Field Theory",
        "type":"L",
        "location":"FF4"
    },
    "3-3.50 PM":{
        "subject_name":"Data Structures and Algorithms",
        "type":"L",
        "location":"G4"
    },
    "4-4.50 PM":{
        "subject_name":"Electromagnetic Field Theory",
        "type":"T",
        "location":"F10"
    }
},
"FRI":{
    "10 -10.50 AM":{
        "subject_name":"Electromagnetic Field Theory",
        "type":"L",
        "location":"G8"
    },
    "3-3.50 PM":{
        "subject_name":"Python for Signal Processing & Communication Lab",
        "type":"P",
        "location":"SPL"
    }
},
"SAT":{
    "9 -9.50 AM":{
        "subject_name":"Electromagnetic Field Theory",
        "type":"P",
        "location":"ACL,JBSPL"
    }
}
}
'''