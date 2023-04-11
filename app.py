from flask import Flask, render_template, request, redirect, url_for
from planer import planer
import json

app = Flask(__name__)

class plan():
    def __init__(self, id, cleaner, date, day, cleaned, person_id, current):
        self.id = id
        self.cleaner = cleaner
        self.date = date
        self.day = day
        self.cleaned = cleaned
        self.person_id = person_id
        self.current = current
        self.color = "uncleaned"
        if current == id:
            self.color = "today"
        if id > current:
            self.color = "future"
        if id-current == 1:
            self.color = "tomorrow"
        if cleaned: 
            self.color = "cleaned"
        

@app.route('/')
def index():
    planer.update_plan()
    ad, ab = planer.make_stats()
    plans = []
    t, id = planer.get_plan()
    for i in t:
        plans.append(plan(i["id"], i["cleaner"], i["date"], i["day"], i["cleaned"], i["person_id"], id))
    return render_template('index.html', plans=plans, ad=ad, ab=ab)

@app.route('/update')
def update():
    try:
        id = int(request.args.get('id'))
        with open("plan.json", "r", encoding="utf-8") as f:
            plan = json.loads(f.read())
            for i in plan:
                if i["id"] == id:
                    if i["cleaned"] == True:
                        i["cleaned"] = False
                    else:
                        i["cleaned"] = True
        with open("plan.json", "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=4, ensure_ascii=False)
        planer.update_plan()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "error": str(e)}
# planer.create_plan()

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)
