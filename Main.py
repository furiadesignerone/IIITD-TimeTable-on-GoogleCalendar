import json
from ics import Calendar, Event
from datetime import datetime, timedelta
import streamlit as st
import streamlit_survey as ss
    
# dictionary to specify whether a particular day is a holiday or not
chutti_h_kya = {}
chutti_h_kya[datetime.strptime("19/1/2024", "%d/%m/%Y")] = "Fest"
chutti_h_kya[datetime.strptime("20/1/2024", "%d/%m/%Y")] = "Fest"
chutti_h_kya[datetime.strptime("26/1/2024", "%d/%m/%Y")] = "Republic Day"
chutti_h_kya[datetime.strptime("24/2/2024", "%d/%m/%Y")] = "Midsems"
chutti_h_kya[datetime.strptime("25/2/2024", "%d/%m/%Y")] = "Midsems"
chutti_h_kya[datetime.strptime("26/2/2024", "%d/%m/%Y")] = "Midsems"
chutti_h_kya[datetime.strptime("27/2/2024", "%d/%m/%Y")] = "Midsems"
chutti_h_kya[datetime.strptime("28/2/2024", "%d/%m/%Y")] = "Midsems"
chutti_h_kya[datetime.strptime("29/2/2024", "%d/%m/%Y")] = "Midsems"
chutti_h_kya[datetime.strptime("1/3/2024", "%d/%m/%Y")] = "Midsems"
chutti_h_kya[datetime.strptime("2/3/2024", "%d/%m/%Y")] = "Midsems"
chutti_h_kya[datetime.strptime("3/3/2024", "%d/%m/%Y")] = "Midsems"
chutti_h_kya[datetime.strptime("4/3/2024", "%d/%m/%Y")] = "Mid Recess"
chutti_h_kya[datetime.strptime("5/3/2024", "%d/%m/%Y")] = "Mid Recess"
chutti_h_kya[datetime.strptime("6/3/2024", "%d/%m/%Y")] = "Mid Recess"
chutti_h_kya[datetime.strptime("7/3/2024", "%d/%m/%Y")] = "Mid Recess"
chutti_h_kya[datetime.strptime("8/3/2024", "%d/%m/%Y")] = "Mid Recess"
chutti_h_kya[datetime.strptime("9/3/2024", "%d/%m/%Y")] = "Mid Recess"
chutti_h_kya[datetime.strptime("10/3/2024", "%d/%m/%Y")] = "Mid Recess"
chutti_h_kya[datetime.strptime("15/3/2024", "%d/%m/%Y")] = "RIISE"
chutti_h_kya[datetime.strptime("16/3/2024", "%d/%m/%Y")] = "RIISE"
chutti_h_kya[datetime.strptime("22/3/2024", "%d/%m/%Y")] = "Astra"
chutti_h_kya[datetime.strptime("23/3/2024", "%d/%m/%Y")] = "Astra"
chutti_h_kya[datetime.strptime("25/3/2024", "%d/%m/%Y")] = "Holi"
chutti_h_kya[datetime.strptime("29/3/2024", "%d/%m/%Y")] = "Good Friday"
chutti_h_kya[datetime.strptime("11/4/2024", "%d/%m/%Y")] = "Eid-ul-Fitr"
chutti_h_kya[datetime.strptime("17/4/2024", "%d/%m/%Y")] = "Ram Navami"

# dictionary to specify whether a particular day has a different timetable or not. if yes, then specify a date of the day of which the timetable is followed.
# (has not yet been integrated in the code)
diff_tt = {}

# date till which you want to add timetable to your google calendar. (keep it in the future and preferably before 29/11/2023(that's when the semester ends ))
tt_till_date = datetime.strptime("30/4/2024", "%d/%m/%Y")

# type of ongoing semester (odd/even)
SEM = "EVEN"

# compare datetime objects
def cmp_date(date1, date2):
    if date1.year != date2.year:
        return date1.year - date2.year
    elif date1.month != date2.month:
        return date1.month - date2.month
    else:
        return date1.day - date2.day

def add_weekly_to_calendar(gc, subject, popup, popup_time):
    arr = subject["start_time"]
    for current_date in arr:
        current_date = datetime.strptime(current_date, "%d/%m/%Y[%H:%M]")
        while cmp_date(current_date, tt_till_date) <= 0 :
            try :
                if chutti_h_kya[datetime.strptime(current_date.strftime("%d/%m/%Y"), "%d/%m/%Y")]:
                    current_date += timedelta(days=7)
            except:
                try :
                    if diff_tt[datetime.strptime(current_date.strftime("%d/%m/%Y"), "%d/%m/%Y")]:
                        current_date += timedelta(days=7)
                except:
                    event = Event()
                    event.name = subject["name"]
                    event.begin =  current_date
                    event.duration = {
                        "hours": subject["duration_hours"],
                        "minutes": subject["duration_minutes"]
                    }
                    event.location = subject["location"]
                    event.description = subject["description"]
                    event.begin = event.begin - timedelta(hours=5, minutes=30)
                    if (popup):
                        event.alarms = [{
                            "action": "DISPLAY",
                            "trigger": f"-PT{popup_time.hour}H{popup_time.minute}M{popup_time.second}S"
                        }]
                    gc.events.add(event)
                    current_date += timedelta(days=7)

def main():
    survey = ss.StreamlitSurvey("Code Flow")
    pages = survey.pages(4, on_submit=lambda: st.success("Now please import 'lectures.ics' file on your Google Calendar. Thank you!"))
    with pages:
        if pages.current == 0 :
            st.write("What year subjects do you want to add to your calendar?")
            st.session_state.years_selected = survey.multiselect("Select your year", options=["First Year", "Second Year", "Third Year", "Fourth Year"])
            st.session_state.data = {}
            if "Third Year" in st.session_state.years_selected or "Fourth Year" in st.session_state.years_selected:
                st.write("Timetable for third and fourth year will be available soon!")
        elif pages.current == 1:
            if "First Year" in st.session_state.years_selected:
                with open(f"Schedules-{SEM}/first_year_lectures.json", "r") as f:
                    st.session_state.data.update(json.load(f))
            if "Second Year" in st.session_state.years_selected:
                with open(f"Schedules-{SEM}/second_year_lectures.json", "r") as f:
                    st.session_state.data.update(json.load(f))

            courseNames = st.session_state.data.keys()
            
            st.session_state.selected_courses = survey.multiselect("Select your courses", options=courseNames)
        elif pages.current == 2:

            st.session_state.popup = survey.checkbox('Do you want a popup before the class?')
            if (st.session_state.popup):
                st.session_state.popup_time_string = survey.text_input('How much time before the class should the popup be? (write in HH:MM format)', value=None)
        
        elif pages.current == 3:
            if not st.session_state.popup:
                st.session_state.popup_time = None
            else:
                st.session_state.popup_time = datetime.strptime(st.session_state.popup_time_string, "%H:%M")

            cal = Calendar()
            
            # st.write("Adding courses to calendar...")
            
            for x in st.session_state.selected_courses:
                add_weekly_to_calendar(cal, st.session_state.data[x], st.session_state.popup, st.session_state.popup_time)
                # st.write(f"Added {x} to calendar")
            st.write("Successfully added all courses to lectures.ics file. Now downlaod and import this file to your Google Calendar.")

            temp_filename = "lectures.ics"
            with open(temp_filename, "w") as f:
                f.write("\n".join(cal))

            with open(temp_filename,"r") as f:
                st.download_button("Download .ics File", f, file_name="lectures.ics")           
            
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.write("Error:", e)
