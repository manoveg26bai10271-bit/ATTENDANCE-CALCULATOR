minimum = 75
periods_per_day = 6
subjects = {}

def read_number(prompt, low, high):
while True:
text = input(prompt).strip()
if not text.isdigit():
print("Please enter a whole number.")
continue
value = int(text)
if value < low or value > high:
print(f"Enter a number between {low} and {high}.")
continue
return value

def percentage(attended, held):
if held == 0:
return 0.0
return attended * 100 / held

def get_status(attended, held):
if held == 0:
return "NO DATA"
value = percentage(attended, held)
if value < minimum:
return "DANGER"
if value < minimum + 10:
return "CAUTION"
return "SAFE"

def classes_can_skip(attended, held):
room = attended * 100 // minimum - held
return max(0, room)

def classes_to_attend(attended, held):
need = minimum * held - 100 * attended
if need <= 0:
return 0
return -(-need // (100 - minimum))

def pick_subject():
if not subjects:
print("\nNo subjects added yet.")
return None
names = list(subjects)
print()
for number, name in enumerate(names, start=1):
print(f"{number}. {name}")
choice = read_number("Choose subject: ", 1, len(names))
return names[choice - 1]

def sorted_by_risk():
names = list(subjects)
for i in range(len(names) - 1):
for j in range(len(names) - 1 - i):
a = subjects[names[j]]
b = subjects[names[j + 1]]
if percentage(a[0], a[1]) > percentage(b[0], b[1]):
names[j], names[j + 1] = names[j + 1], names[j]
return names

def totals():
attended_sum = 0
held_sum = 0
for attended, held in subjects.values():
attended_sum += attended
held_sum += held
return attended_sum, held_sum

def add_subject():
name = input("Subject name: ").strip().title()
if name == "":
print("Name cannot be empty.")
return
if name in subjects:
print("That subject already exists. Use the update option instead.")
return
held = read_number("Total classes held so far: ", 0, 500)
attended = read_number("Classes you attended: ", 0, held)
subjects[name] = [attended, held]
print(f"{name} added.")
show_verdict(name)

def show_verdict(name):
attended, held = subjects[name]
status = get_status(attended, held)
value = percentage(attended, held)
print(f"\n{name}: {value:.2f}% -> {status}")
if status == "DANGER":
print(f"!!! Below {minimum}%. Attend the next {classes_to_attend(attended, held)} classes in a row to recover.")
elif held > 0:
print(f"You can skip {classes_can_skip(attended, held)} more class(es) and stay safe.")

def update_attendance():
name = pick_subject()
if name is None:
return
attended_new = read_number("Classes attended since last update: ", 0, 200)
missed_new = read_number("Classes missed since last update: ", 0, 200)
subjects[name][0] += attended_new
subjects[name][1] += attended_new + missed_new
show_verdict(name)

def view_report():
if not subjects:
print("\nNo subjects added yet.")
return

print("\n" + "=" * 78)
print(f"{'Subject':<20}{'Attended':<12}{'Percent':<10}{'Status':<10}{'Can skip':<10}{'Must attend'}")
print("=" * 78)

danger = set()
for name in sorted_by_risk():
attended, held = subjects[name]
status = get_status(attended, held)
if status == "DANGER":
danger.add(name)
print(
f"{name:<20}{str(attended) + '/' + str(held):<12}"
f"{percentage(attended, held):<10.2f}{status:<10}"
f"{classes_can_skip(attended, held):<10}{classes_to_attend(attended, held)}"
)

attended_sum, held_sum = totals()
print("-" * 78)
print(f"Overall attendance: {percentage(attended_sum, held_sum):.2f}% ({attended_sum}/{held_sum})")

if danger:
print("\n!!! DANGER ZONE !!!")
print("Subjects below the limit: " + ", ".join(sorted(danger)))
else:
print("\nAll subjects are above the limit. Keep it up.")

def bunk_calculator():
name = pick_subject()
if name is None:
return
attended, held = subjects[name]
if held == 0:
print("No classes recorded for this subject yet.")
return

can_skip = classes_can_skip(attended, held)
print(f"\n{name}")
print(f"Current attendance : {percentage(attended, held):.2f}%")
print(f"Classes you can skip: {can_skip}")
print(f"That is about {can_skip // periods_per_day} full day(s) with {periods_per_day} periods per day.")

attended_sum, held_sum = totals()
overall_skip = classes_can_skip(attended_sum, held_sum)
print(f"\nOverall you can skip {overall_skip} class(es), roughly {overall_skip // periods_per_day} day(s).")
if get_status(attended, held) == "DANGER":
print(f"But this subject is in danger. Attend {classes_to_attend(attended, held)} classes first.")

def what_if():
name = pick_subject()
if name is None:
return
attended, held = subjects[name]
print("\n1. What if I skip some classes?")
print("2. What if I attend some classes?")
mode = read_number("Choose: ", 1, 2)
count = read_number("How many classes: ", 1, 200)

if mode == 1:
new_attended, new_held = attended, held + count
else:
new_attended, new_held = attended + count, held + count

before = percentage(attended, held)
after = percentage(new_attended, new_held)
print(f"\nBefore: {before:.2f}% ({get_status(attended, held)})")
print(f"After : {after:.2f}% ({get_status(new_attended, new_held)})")
if after < minimum:
print("!!! That plan puts you in the danger zone.")

def semester_planner():
name = pick_subject()
if name is None:
return
attended, held = subjects[name]
remaining = read_number("Classes remaining in the semester: ", 1, 300)

need = minimum * (held + remaining) - 100 * attended
must_attend = 0 if need <= 0 else -(-need // 100)

print(f"\n{name}")
if must_attend > remaining:
best = percentage(attended + remaining, held + remaining)
print(f"Even if you attend every remaining class you will end at {best:.2f}%.")
print(f"The {minimum}% target cannot be reached. Talk to your faculty early.")
else:
print(f"You must attend at least {must_attend} of the {remaining} remaining classes.")
print(f"You can afford to skip {remaining - must_attend} of them.")

def settings():
global minimum, periods_per_day
print(f"\nCurrent minimum: {minimum}%  |  Periods per day: {periods_per_day}")
print("1. Change minimum attendance")
print("2. Change periods per day")
print("3. Back")
choice = read_number("Choose: ", 1, 3)
if choice == 1:
minimum = read_number("New minimum percentage (1-99): ", 1, 99)
elif choice == 2:
periods_per_day = read_number("Periods per day (1-12): ", 1, 12)
else:
pass

def show_menu():
print("\n===== ATTENDANCE RISK CALCULATOR =====")
print("1. Add subject")
print("2. Update attendance")
print("3. View report")
print("4. Bunk calculator")
print("5. What-if simulator")
print("6. Semester planner")
print("7. Settings")
print("8. Exit")

def main():
while True:
show_menu()
choice = input("Enter your choice: ").strip()

if choice == "1":
add_subject()
elif choice == "2":
update_attendance()
elif choice == "3":
view_report()
elif choice == "4":
bunk_calculator()
elif choice == "5":
what_if()
elif choice == "6":
semester_planner()
elif choice == "7":
settings()
elif choice == "8":
print("Stay regular, stay safe. Goodbye!")
break
elif choice == "":
continue
else:
print("Invalid choice. Pick a number from 1 to 8.")

main()
