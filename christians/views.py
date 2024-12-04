from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Christian 
import json
from django.http import JsonResponse
from django.db.models import Q

def search_christians(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText', "").strip()
        
        if not search_str:
            return JsonResponse([], safe=False)  
        
      
        query = Q(name__istartswith=search_str, owner=request.user) | \
                Q(age__istartswith=search_str, owner=request.user) | \
                Q(role__icontains=search_str, owner=request.user) | \
                Q(status__icontains=search_str, owner=request.user) | \
                Q(gender__icontains=search_str, owner=request.user)

        christians = Christian.objects.filter(query)
        data = list(christians.values())

        return JsonResponse(data, safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    christians = Christian.objects.filter(owner=request.user)

    # Paginate christians
    paginator = Paginator(christians, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'christians': christians,
        'page_obj': page_obj,
    }

    return render(request, 'christians/index.html', context)


@login_required(login_url='/authentication/login')
def add_christian(request):
    context = {
        'values': request.POST
    }

    if request.method == 'GET':
        return render(request, 'christians/addChristian.html', context)

    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        age = request.POST['age']
        role = request.POST['role']
        status = request.POST['status']

        if not name:
            messages.error(request, 'Name is required')
            return render(request, 'christians/addChristian.html', context)

        if not gender:
            messages.error(request, 'Gender is required')
            return render(request, 'christians/addChristian.html', context)

        Christian.objects.create(
            name=name,
            gender=gender,
            age=age,
            role=role,
            status=status,
            owner=request.user
        )

        messages.success(request, 'Christian added successfully')
        return redirect('christians')


@login_required(login_url='/authentication/login')
def christian_edit(request, id):
    christian = Christian.objects.get(pk=id)
    context = {
        'christian': christian,
        'values': christian
    }

    if request.method == 'GET':
        return render(request, 'christians/editChristian.html', context)

    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['gender']
        age = request.POST['age']
        role = request.POST['role']
        status = request.POST['status']

        if not name:
            messages.error(request, 'Name is required')
            return render(request, 'christians/editChristian.html', context)

        if not gender:
            messages.error(request, 'Gender is required')
            return render(request, 'christians/editChristian.html', context)

        christian.name = name
        christian.age = age
        christian.role = role
        christian.status = status
        christian.gender = gender

        christian.save()

        messages.success(request, 'Christian updated successfully')
        return redirect('christians')


@login_required(login_url='/authentication/login')
def delete_christian(request, id):
    christian = Christian.objects.get(pk=id)
    christian.delete()
    messages.success(request, 'Christian removed')
    return redirect('christians')
