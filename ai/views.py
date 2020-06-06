from django.shortcuts import render
from django.http import JsonResponse


def base(request):
    context = {

    }
    return render(request, 'ai/Base.html', context)


def breast_cancer_detection(request):
    if request.is_ajax():
        if request.method == 'POST':
            print(request.POST)
            results = {
                'result': 'Your Data is here all your info...'
            }
            return JsonResponse(results)

    context = {

    }
    return render(request, 'ai/Breast_Cancer_Detection.html', context)


def female_diabetes_detection(request):
    if request.is_ajax():
        if request.method == 'POST':
            print(request.POST)
            results = {
                'result': 'Your Data is here all your info...'
            }
            return JsonResponse(results)

    context = {

    }
    return render(request, 'ai/Female_Diabetes_Detection.html', context)


def DNA_Classification(request):
    if request.is_ajax():
        if request.method == 'POST':
            print(request.POST)
            # seq = list()
            # for letter in x:
            #     seq.append(letter)
            results = {
                'result': 'Your Data is here all your info...'
            }
            return JsonResponse(results)

    context = {

    }
    return render(request, 'ai/DNA_Classification.html', context)


def heart_disease_prediction(request):
    if request.is_ajax():
        if request.method == 'POST':
            print(request.POST)
            results = {
                'result': 'Your Data is here all your info...'
            }
            return JsonResponse(results)

    context = {

    }
    return render(request, 'ai/Heart_Disease_Prediction.html', context)


def pneumonia_detection(request):
    if request.is_ajax():
        if request.method == 'POST':
            print(request.FILES)
            results = {
                'result': 'Your Data is here all your info...'
            }
            return JsonResponse(results)

    context = {

    }
    return render(request, 'ai/Pneumonia_Detection.html', context)
