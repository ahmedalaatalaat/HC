# from tensorflow.keras.applications.vgg16 import preprocess_input
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.models import load_model
# from django.http import JsonResponse
from django.shortcuts import render
# import pandas as pd
# import numpy as np
# import pickle
# from PIL import Image
# import os
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
# from main.settings import MEDIA_ROOT


# def base(request):
#     context = {

#     }
#     return render(request, 'ai/Base.html', context)


# def breast_cancer_detection(request):
#     if request.is_ajax():
#         if request.method == 'POST':
#             print(request.POST)

#             # get file path
#             module_dir = os.path.dirname(__file__)  # get current directory
#             knn_file_path = os.path.join(module_dir, 'ai_models/breast_cancer_knn_model')

#             # open the knn model
#             with open(knn_file_path, 'rb') as knn_model_file:
#                 knn_model = pickle.load(knn_model_file)

#             clump_thickness = request.POST.get('clump_thickness')
#             uniform_cell_size = request.POST.get('uniform_cell_size')
#             uniform_cell_shape = request.POST.get('uniform_cell_shape')
#             marginal_adhesion = request.POST.get('marginal_adhesion')
#             single_epithelial_size = request.POST.get('single_epithelial_size')
#             bare_nuclei = request.POST.get('bare_nuclei')
#             bland_chromatin = request.POST.get('bland_chromatin')
#             normal_nucleoli = request.POST.get('normal_nucleoli')
#             mitoses = request.POST.get('mitoses')

#             data = [clump_thickness, uniform_cell_size, uniform_cell_shape, marginal_adhesion, single_epithelial_size, bare_nuclei, bland_chromatin, normal_nucleoli, mitoses]
#             measures = np.array([data])
#             measures = measures.reshape(len(measures), -1)

#             knn_prediction = knn_model.predict(measures)
#             knn_prediction = 'benign' if str(knn_prediction[0]) == '2' else 'malignant'

#             result = knn_prediction

#             results = {
#                 'result': result
#             }
#             return JsonResponse(results)

#     context = {

#     }
#     return render(request, 'ai/Breast_Cancer_Detection.html', context)


# def female_diabetes_detection(request):
#     if request.is_ajax():
#         if request.method == 'POST':

#             print(request.POST)
#             module_dir = os.path.dirname(__file__)  # get current directory
#             file_path = os.path.join(module_dir, 'ai_models/diabetes_onset_detection_model.pkl')
#             with open(file_path, 'rb') as file:
#                 grid = pickle.load(file)

#             n_pregnant = request.POST.get('n_pregnant')
#             glucose_concentration = request.POST.get('glucose_concentration')
#             blood_pressuer = request.POST.get('blood_pressuer')
#             skin_thickness = request.POST.get('skin_thickness')
#             serum_insulin = request.POST.get('serum_insulin')
#             BMI = request.POST.get('BMI')
#             pedigree_function = request.POST.get('pedigree_function')
#             age = request.POST.get('age')

#             data = [n_pregnant, glucose_concentration, blood_pressuer, skin_thickness, serum_insulin, BMI, pedigree_function, age]
#             example_measures = np.array([data])
#             example_measures = example_measures.reshape(len(example_measures), -1)
#             y = grid.predict(example_measures)

#             result = 'You are diabetic' if y[0][0] else 'You are not diabetic'
#             results = {
#                 'result': result,
#             }
#             return JsonResponse(results)

#     context = {

#     }
#     return render(request, 'ai/Female_Diabetes_Detection.html', context)


# def DNA_Classification(request):
#     if request.is_ajax():
#         if request.method == 'POST':
#             print(request.POST)
#             module_dir = os.path.dirname(__file__)  # get current directory
#             file_path = os.path.join(module_dir, 'ai_models/dna_classification_model.pkl')
#             with open(file_path, 'rb') as my_file:
#                 model = pickle.load(my_file)

#             template_data = {'0_a': [], '0_c': [], '0_g': [], '0_t': [], '1_a': [], '1_c': [], '1_g': [], '1_t': [], '2_a': [], '2_c': [], '2_g': [], '2_t': [], '3_a': [], '3_c': [], '3_g': [], '3_t': [], '4_a': [], '4_c': [], '4_g': [], '4_t': [], '5_a': [], '5_c': [], '5_g': [], '5_t': [], '6_a': [], '6_c': [], '6_g': [], '6_t': [], '7_a': [], '7_c': [], '7_g': [], '7_t': [], '8_a': [], '8_c': [], '8_g': [], '8_t': [], '9_a': [], '9_c': [], '9_g': [], '9_t': [], '10_a': [], '10_c': [], '10_g': [], '10_t': [], '11_a': [], '11_c': [], '11_g': [], '11_t': [], '12_a': [], '12_c': [], '12_g': [], '12_t': [], '13_a': [], '13_c': [], '13_g': [], '13_t': [], '14_a': [], '14_c': [], '14_g': [], '14_t': [], '15_a': [], '15_c': [], '15_g': [], '15_t': [], '16_a': [], '16_c': [], '16_g': [], '16_t': [], '17_a': [], '17_c': [], '17_g': [], '17_t': [], '18_a': [], '18_c': [], '18_g': [], '18_t': [], '19_a': [], '19_c': [], '19_g': [], '19_t': [], '20_a': [], '20_c': [], '20_g': [], '20_t': [], '21_a': [], '21_c': [], '21_g': [], '21_t': [], '22_a': [], '22_c': [], '22_g': [], '22_t': [], '23_a': [], '23_c': [], '23_g': [], '23_t': [], '24_a': [], '24_c': [], '24_g': [], '24_t': [], '25_a': [], '25_c': [], '25_g': [], '25_t': [], '26_a': [], '26_c': [], '26_g': [], '26_t': [], '27_a': [], '27_c': [], '27_g': [], '27_t': [], '28_a': [], '28_c': [], '28_g': [], '28_t': [], '29_a': [], '29_c': [], '29_g': [], '29_t': [], '30_a': [], '30_c': [], '30_g': [], '30_t': [], '31_a': [], '31_c': [], '31_g': [], '31_t': [], '32_a': [], '32_c': [], '32_g': [], '32_t': [], '33_a': [], '33_c': [], '33_g': [], '33_t': [], '34_a': [], '34_c': [], '34_g': [], '34_t': [], '35_a': [], '35_c': [], '35_g': [], '35_t': [], '36_a': [], '36_c': [], '36_g': [], '36_t': [], '37_a': [], '37_c': [], '37_g': [], '37_t': [], '38_a': [], '38_c': [], '38_g': [], '38_t': [], '39_a': [], '39_c': [], '39_g': [], '39_t': [], '40_a': [], '40_c': [], '40_g': [], '40_t': [], '41_a': [], '41_c': [], '41_g': [], '41_t': [], '42_a': [], '42_c': [], '42_g': [], '42_t': [], '43_a': [], '43_c': [], '43_g': [], '43_t': [], '44_a': [], '44_c': [], '44_g': [], '44_t': [], '45_a': [], '45_c': [], '45_g': [], '45_t': [], '46_a': [], '46_c': [], '46_g': [], '46_t': [], '47_a': [], '47_c': [], '47_g': [], '47_t': [], '48_a': [], '48_c': [], '48_g': [], '48_t': [], '49_a': [], '49_c': [], '49_g': [], '49_t': [], '50_a': [], '50_c': [], '50_g': [], '50_t': [], '51_a': [], '51_c': [], '51_g': [], '51_t': [], '52_a': [], '52_c': [], '52_g': [], '52_t': [], '53_a': [], '53_c': [], '53_g': [], '53_t': [], '54_a': [], '54_c': [], '54_g': [], '54_t': [], '55_a': [], '55_c': [], '55_g': [], '55_t': [], '56_a': [], '56_c': [], '56_g': [], '56_t': []}

#             dataset = list()
#             for letter in request.POST.get('DNA_sequence'):
#                 dataset.append(letter)

#             for index, item in enumerate(dataset):
#                 if 'a' in item:
#                     template_data[f'{index}_a'].append(1)
#                     template_data[f'{index}_c'].append(0)
#                     template_data[f'{index}_g'].append(0)
#                     template_data[f'{index}_t'].append(0)
#                 elif 'c' in item:
#                     template_data[f'{index}_a'].append(0)
#                     template_data[f'{index}_c'].append(1)
#                     template_data[f'{index}_g'].append(0)
#                     template_data[f'{index}_t'].append(0)
#                 elif 'g' in item:
#                     template_data[f'{index}_a'].append(0)
#                     template_data[f'{index}_c'].append(0)
#                     template_data[f'{index}_g'].append(1)
#                     template_data[f'{index}_t'].append(0)
#                 elif 't' in item:
#                     template_data[f'{index}_a'].append(0)
#                     template_data[f'{index}_c'].append(0)
#                     template_data[f'{index}_g'].append(0)
#                     template_data[f'{index}_t'].append(1)

#             df = pd.DataFrame.from_dict(template_data)
#             measures = np.array(df)
#             measures = measures.reshape(len(measures), -1)
#             predictions = model.predict(measures)

#             result = 'This DNA is a Promoter' if predictions[0] == 1 else 'This DNA is not a Promoter'

#             results = {
#                 'result': result
#             }
#             return JsonResponse(results)

#     context = {

#     }
#     return render(request, 'ai/DNA_Classification.html', context)


# def heart_disease_prediction(request):
#     if request.is_ajax():
#         if request.method == 'POST':
#             print(request.POST)
#             module_dir = os.path.dirname(__file__)  # get current directory
#             file_path = os.path.join(module_dir, 'ai_models/heart_disease_prediction_model.pkl')
#             with open(file_path, 'rb') as my_file:
#                 model = pickle.load(my_file)

#                 age = request.POST.get('age')
#                 sex = request.POST.get('sex')
#                 cp = request.POST.get('cp')
#                 trestbps = request.POST.get('trestbps')
#                 chol = request.POST.get('chol')
#                 fbs = request.POST.get('fbs')
#                 restecg = request.POST.get('restecg')
#                 thalach = request.POST.get('thalach')
#                 exang = request.POST.get('exang')
#                 oldpeak = request.POST.get('oldpeak')
#                 slope = request.POST.get('slope')
#                 ca = request.POST.get('ca')
#                 thal = request.POST.get('thal')

#                 data = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

#                 df = pd.DataFrame(data)
#                 df = df.transpose()

#                 measures = df.to_numpy()
#                 measures = measures.reshape(len(measures), -1)
#                 predictions = np.round(model.predict(measures)).astype(int)
#                 print(predictions)

#                 if predictions[0][0] == 0:
#                     result = 'You are Normal'
#                 elif predictions[0][0] == 1:
#                     result = 'You have ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV)'
#                 elif predictions[0][0] == 2:
#                     result = 'Your report showing probable or definite left ventricular hypertrophy'

#             results = {
#                 'result': result
#             }
#             return JsonResponse(results)

#     context = {

#     }
#     return render(request, 'ai/Heart_Disease_Prediction.html', context)


# def pneumonia_detection(request):
#     if request.is_ajax():
#         if request.method == 'POST':

#             module_dir = os.path.dirname(__file__)  # get current directory
#             file_path = os.path.join(module_dir, 'ai_models/model_vgg16.h5')
#             model = load_model(file_path)

#             file = request.FILES.get('image')
#             img_file = default_storage.save(request.FILES.get('image').name, ContentFile(file.read()))
#             img_path = os.path.join(MEDIA_ROOT, img_file)
#             img = image.load_img(img_path, target_size=(224, 224))

#             x = image.img_to_array(img)
#             x = np.expand_dims(x, axis=0)
#             img_data = preprocess_input(x)
#             classes = model.predict(img_data)
#             print(round(classes[0][0]))

#             os.remove(img_path)

#             result = 'Noraml' if round(classes[0][0]) == 1 else 'Pneumonia'

#             results = {
#                 'result': result
#             }
#             return JsonResponse(results)

#     context = {

#     }
#     return render(request, 'ai/Pneumonia_Detection.html', context)
