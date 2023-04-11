from datetime import datetime
from calendar import monthrange
import json

class planer():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    months = ["Januari", "Februari", "Mars", "April", "Maj", "Juni", "Juli", "Augusti", "September", "Oktober", "November", "December"]
    cleaners = ["Abdurrahman", "Adnan"]
    def create_plan():
        plan = []
        p = 0
        id = 0
        for m in range(datetime.utcnow().month-1, 12):
            mi = monthrange(datetime.utcnow().year, m+1)
            for i in range(1, mi[1]+1):
                id += 1
                data = {
                    "id": id,
                    "cleaner": planer.cleaners[p],
                    "date": f"{i}-{m+1}-{datetime.utcnow().year}",
                    "day": planer.days[datetime(datetime.utcnow().year, m+1, i).weekday()],
                    "cleaned": False,
                    "person_id": p
                }
                plan.append(data)
                if p == 1:
                    p = 0
                    continue
                p += 1
        with open("plan.json", "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=4, ensure_ascii=False)

    def update_plan():
        with open("plan.json", "r",encoding="utf-8") as f:
            plan = json.loads(f.read())
            x = ""
            p = None
            for i in plan:
                if p == None:
                    p = (True, i["person_id"]) if i["cleaned"] == True else (False, i["person_id"])
                    continue
                if p[0] == False:
                    i["cleaner"] = planer.cleaners[p[1]]
                    for t in plan:
                        if t["date"] == f"{datetime.utcnow().day}-{datetime.utcnow().month}-{datetime.utcnow().year}":
                            today = plan.index(t)
                    if plan.index(i) > today:
                        i["cleaner"] = f"({planer.cleaners[p[1]]})"
                    i["person_id"] = p[1]
                elif p[0] == True:
                    if p[1] == len(planer.cleaners)-1:
                        x = planer.cleaners[0]
                    else:
                        x = planer.cleaners[p[1]+1]
                    i["cleaner"] = x
                    i["person_id"] = planer.cleaners.index(x)
                    p = (True, i["person_id"]) if i["cleaned"] == True else (False, i["person_id"])
                if i["cleaned"] == True:
                    p = (True, i["person_id"]) if i["cleaned"] == True else (False, i["person_id"])
        with open("plan.json", "w", encoding="utf-8") as f:
            json.dump(plan,f, indent=4, ensure_ascii=False)

    def get_plan():
        with open("plan.json", "r", encoding="utf-8") as f:
            plan = json.loads(f.read())
            max = len(plan)
            span = (6,5)
            for i in plan:
                if i["date"] == f"{datetime.utcnow().day}-{datetime.utcnow().month}-{datetime.utcnow().year}":
                    w = plan.index(i)
                    id = i["id"]
            print(w, max)
            if w-span[0] >= 0 and w+span[1] < max:
                return plan[w-span[0]:w+span[1]], id
            elif w-span[0] <= 0:
                return plan[0:w+span[1]], id
            elif w+span[1] > max:
                return plan[w-span[0]:max-1],id
    
    def make_stats():
        with open("plan.json", "r", encoding="utf-8") as f:
            plans = json.loads(f.read())
            c = ["Abdurrahman", "Adnan"]
            p = [0, 0]
            u = [0, 0]
            t = [0, 0]
            r = [0, 0]
            for i in c:
                for plan in plans:
                    if plan["cleaner"] == i:
                        if plan["cleaned"]:
                            p[c.index(i)] += 1
                        else:
                            u[c.index(i)] -= 1
                        t[c.index(i)] += 1
                        r[c.index(i)] = (p[c.index(i)]+u[c.index(i)])/t[c.index(i)]
            ab = planer.cleaner(c[0], p[0], u[0], t[0], r[0])
            ad = planer.cleaner(c[1], p[1], u[1], t[1], r[1])
            return ad, ab
    
    class cleaner():
        def __init__(self, name, clean, unclean, total, ratio):
            self.name = name
            self.clean = clean
            self.unclean = unclean
            self.total = total
            self.ratio = ratio