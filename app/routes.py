from flask import Blueprint, render_template, redirect, url_for
from .models import Task
from .forms import TaskForm
from app import create_app, db

main = Blueprint('main', __name__)  

@main.route('/')
def index():
    tasks = Task.query.all()  
    return render_template('index.html', tasks=tasks)  

@main.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)  
    form = TaskForm()

    if form.validate_on_submit(): 
        task.name = form.name.data  
        db.session.commit()  
        return redirect(url_for('main.index')) 

    form.name.data = task.name  
    return render_template('edit_task.html', form=form)  

@main.route('/new', methods=['GET', 'POST'])
def new_task():
    form = TaskForm()
    if form.validate_on_submit():  
        new_task = Task(name=form.name.data)  
        db.session.add(new_task)  
        db.session.commit()  
        return redirect(url_for('main.index'))  

    return render_template('new_task.html', form=form)  

@main.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.index'))  
