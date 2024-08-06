import json

def batch_extractor(text):
    start_bracket = text.find('(')
    if start_bracket != -1:
        return text[1:start_bracket].strip()
    return ""

def subject_extractor(text):
    start_bracket = text.find('(')
    if start_bracket != -1:
        # Find the position of the closing parenthesis
        end_bracket = text.find(')', start_bracket)
        if end_bracket != -1:
            # Extract the substring inside the brackets
            return text[start_bracket + 1:end_bracket]
    return ""

def location_extractor(text):
    # Find the position of the dash
    start_dash = text.find('-')
    if start_dash != -1:
        # Find the position of the slash after the dash
        end_slash = text.find('/', start_dash)
        if end_slash != -1:
            # Extract the substring after the dash and before the slash
            return text[start_dash + 1:end_slash]
    return ""

def subject_name_extractor(subjects_dict, code):
    for i in range(len(subjects_dict["Code"])):
        if subjects_dict["Code"][i] == code:
            return subjects_dict["Subject"][i]
    return ""


with open("./data/time_table.json", 'r') as file:
    time_table = json.load(file)

with open("./data/subject.json", 'r') as file:
    subject = json.load(file)

your_time_table = []

batch = input("Enter your Batch: ").upper().strip()
# print(batch)
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
                # print(indi_class, batch)
                if len(indi_class.strip()) > 0:
                    your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                    # print([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
            for elective_code in electives_subject_codes:
                # print(elective_code)
                if len(indi_class)>0 and indi_class[0] != "P":
                    if subject_extractor(indi_class) == elective_code:
                        extracted_batch = batch_extractor(indi_class)
                        # print(extracted_batch)
                        if ("-" not in extracted_batch) or ("," not in extracted_batch):
                            if len(extracted_batch) in [0,3]:
                                # print([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                            elif len(extracted_batch) == 1:
                                if extracted_batch == batch[0]:
                                    your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                    # print([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                            elif len(extracted_batch) == 2:
                                for letter in extracted_batch:
                                    your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                    # print([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                        if ("," in extracted_batch):
                            batch_list = extracted_batch.split(",")
                            # print(batch_list, "\n")
                            # check = False
                            for index, b in enumerate(batch_list):
                                # print(b.strip())
                                if len(batch_list) > 3:
                                    # print(b.strip()[0].isalpha())
                                    if b.strip()[0].isalpha():
                                        if b.strip()[0] == batch[0]:
                                            batch_list[index] = b[1:]
                                            # print(batch_list)
                                            if batch_list[index] == batch[1:]:
                                                your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                                # print([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                        else: 
                                            break
                                    else:
                                        if b == batch[1:]:
                                            # print("fuck ya bitch")
                                            your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                            # print([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])

                                else:
                                    if b.strip()[0] == batch[0]:
                                        if len(b.strip()) == 1:
                                            your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                            # print([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                        else:
                                            batch_nums = ((b.strip())).split("-")
                                            # print(batch_nums)
                                            # Ensure the batch string is in expected format
                                            if len(batch) > 1 and all(len(num.strip()) > 1 for num in batch_nums):
                                                batch_number_str = batch.strip()[1:]

                                                if batch_number_str:
                                                    batch_number = int(batch_number_str)

                                                    # Strip and slice batch_nums elements correctly
                                                    batch_num_0 = int(batch_nums[0].strip()[1:])
                                                    batch_num_1 = int(batch_nums[1].strip()[1:])

                                                    if batch_num_0 <= batch_number <= batch_num_1:
                                                        your_time_table.append([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                                        # print([day, time, subject_name_extractor(subject, code), indi_class.strip()[0], location_extractor(subjectCode)])
                                                else:
                                                    print("Batch string is empty or incorrectly sliced.")
                                            else:
                                                print("Batch string or batch_nums are incorrectly formatted.")

# print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
print()
for t in your_time_table:
    print(t)
