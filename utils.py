import base64

#https://mese.webuntis.com/timetable-students-my/2022-08-22/modal/details/1212411/false/13691/5/2022-08-22T11:35:00+02:00/2022-08-22T13:05:00+02:00/details
#https://mese.webuntis.com/timetable-students-my/{yyyy-mm-dd}/modal/details/{lesson_id}/false/{student_id (type=5)}

def b64ToString(b64):
    return base64.b64decode(b64).decode('utf-8')
