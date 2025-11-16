def allocate_equipment(equipment_available, meetings):
    for m in meetings:
        total_equipment_needed = sum(m["equipment_required"].values())
        m["total_equipment_needed"] = total_equipment_needed
        m["value_ratio"] = (m["priority"] * m["duration"]) / total_equipment_needed

    meetings_sorted = sorted(meetings, key=lambda m: -m["value_ratio"])

    schedule = []
    equipment_state = equipment_available.copy()

    for m in meetings_sorted:
        ratios = []
        for eq, qty in m["equipment_required"].items():
            if eq in equipment_state:
                ratios.append(equipment_state[eq] / qty)
            else:
                ratios.append(0)
        equipment_satisfaction = min(1, *ratios)

        if equipment_satisfaction == 0:
            continue

        value = m["priority"] * m["duration"] * equipment_satisfaction

        for eq, qty in m["equipment_required"].items():
            allocated = min(qty * equipment_satisfaction, equipment_state.get(eq, 0))
            equipment_state[eq] -= allocated

        schedule.append({
            "meeting_id": m["id"],
            "value": value,
            "equipment_satisfaction": equipment_satisfaction
        })

    return schedule, equipment_state

equipment_available = {"projector": 3, "vc": 2, "whiteboard": 4}
flexible_meetings = [
    {"id": 1, "priority": 3, "duration": 2, "equipment_required": {"projector": 1, "vc": 1}},
    {"id": 2, "priority": 5, "duration": 1, "equipment_required": {"projector": 1}},
]

schedule, remaining_equipment = allocate_equipment(equipment_available, flexible_meetings)

print("Scheduled Meetings:")
for m in schedule:
    print(m)

print("Remaining Equipment:", remaining_equipment)
