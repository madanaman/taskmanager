from django.http import HttpResponse
from django.shortcuts import render, redirect
from todolist.models import TaskList
from todolist.form import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).manager = request.user
            form.save()
        messages.success(request, ("New task added sucessfully."))
        return redirect('todolist')

    else:
        all_tasks = TaskList.objects.filter(manager=request.user)
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

def index(request):
    # return HttpResponse("Hi There")
    context = {'index_text':"Index Page"}
    return render(request, 'index.html', context)


@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task.delete()
    else:
        messages.error(request,("User Not Authorized"))
    return redirect('todolist')


@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save(commit=False).manager = request.user
            form.save()
        messages.success(request, ("Task edited sucessfully."))
        return redirect('todolist')

    else:
        task_object = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {"task_object": task_object })

@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = True
    if task.manager == request.user:
        task.save()
    else:
        messages.error(request,("User Not Authorized"))
    return redirect('todolist')


@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    if task.manager == request.user:
        task.save()
    else:
        messages.error(request,("User Not Authorized"))
    return redirect('todolist')