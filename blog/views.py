from flask import render_template

from . import app
from .database import session, Entry
    
PAGINATE_BY = 10
#paginate_by = int(request.args.get('entries_per', PAGINATE_BY))

@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1, paginate_by=10):
    # Zero-indexed page
    #entries_per = limit
    paginate_by = int(request.args.get('entries_per', PAGINATE_BY))
    if paginate_by > 50 or paginate_by < 1:
        paginate_by = 10
    page_index = page - 1

    count = session.query(Entry).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) // paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

@app.route("/entry/add", methods=["GET"])
def add_entry_get():
    return render_template("add_entry.html")
    
from flask import request, redirect, url_for

@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))
    
@app.route("/entry/<id>")
def entry(id):
    entry = session.query(Entry).get(id)
    
    return render_template("entry.html",
    entry = entry)
    
@app.route("/entry/<id>/edit", methods=["GET"])
def edit_entry_get(id):
    entry =  session.query(Entry).get(id)
    
    return render_template("edit_entry.html",
    entry=entry)
    
@app.route("/entry/<id>/edit", methods=["POST"])
def edit_entry_post(id):
    entry = session.query(Entry).get(id)
    entry.title = request.form["title"]
    entry.content = request.form["content"]
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))
    
@app.route("/entry/<id>/delete", methods=["GET"])
def delete_entry_get(id):
    entry = session.query(Entry).get(id)
    
    return render_template("delete_entry.html",
    entry = entry)
    
@app.route("/entry/<id>/delete", methods=["POST"])
def delete_entry_post(id):
    entry = session.query(Entry).get(id)
    session.delete(entry)
    session.commit()
    return redirect(url_for("entries"))