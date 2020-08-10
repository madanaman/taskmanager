from django.http import HttpResponse
from django.shortcuts import render, redirect
from todolist.models import TaskList
from todolist.form import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save()
        messages.success(request, ("New task added sucessfully."))
        return redirect('todolist')

    else:
        all_tasks = TaskList.objects.all()
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)

        return render(request, 'todolist.html', {"all_tasks": all_tasks})
def helloworld(request):
    return HttpResponse("Hello world")
def contact(request):
    # return HttpResponse("Hi There")
    context = {'contact_text':"Contact Us Page"}
    return render(request, 'contactus.html', context)
def about(request):
    # return HttpResponse("Hi There")
    context = {'about_text':"About us Page"}
    return render(request, 'aboutus.html', context)

def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.delete()
    return redirect('todolist')

def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
        messages.success(request, ("Task edited sucessfully."))
        return redirect('todolist')

    else:
        task_object = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {"task_object": task_object })

def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = True
    task.save()
    return redirect('todolist')


def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()
    return redirect('todolist')