def schedule_meetings(meetings, rooms):
    for r in rooms:
        r["equipment"] = set(r["equipment"])

    for m in meetings:
        m["equipment"] = set(m["equipment"])
        m["feasible_rooms"] = [
            r["id"] for r in rooms
            if r["capacity"] >= m["attendees"] and m["equipment"].issubset(r["equipment"])
        ]

    meetings_sorted = sorted(meetings, key=lambda m: (m["start"], -m["priority"]))

    room_last_end = {r["id"]: 0 for r in rooms}
    schedule = []

    for m in meetings_sorted:
        candidates = [rid for rid in m["feasible_rooms"] if room_last_end[rid] <= m["start"]]
        if not candidates:
            continue

        chosen_room = min(candidates, key=lambda rid: room_last_end[rid])

        schedule.append({
            "meeting_id": m["id"],
            "room_id": chosen_room,
            "time": (m["start"], m["end"])
        })

        room_last_end[chosen_room] = m["end"]

    return schedule


meetings = [
    {"id": 1, "start": 9, "end": 10, "attendees": 8, "equipment": ["projector"], "priority": 3},
    {"id": 2, "start": 9, "end": 11, "attendees": 4, "equipment": [], "priority": 4},
    {"id": 3, "start": 10, "end": 12, "attendees": 12, "equipment": ["projector", "vc"], "priority": 5},
]

rooms = [
    {"id": "A", "capacity": 10, "equipment": ["projector", "whiteboard"]},
    {"id": "B", "capacity": 6, "equipment": ["vc", "projector"]},
    {"id": "C", "capacity": 15, "equipment": ["projector", "vc", "whiteboard"]},
]

result = schedule_meetings(meetings, rooms)
print(result)
