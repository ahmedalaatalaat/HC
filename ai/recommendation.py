import random
import csv
import math
import operator
from django.shortcuts import render, get_object_or_404
from main.utils import get_object_or_none
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.core import serializers
import operator
from .recommendation import *
import numpy as np
import math
from collections import OrderedDict
import ast


def handle_rating(x, physicianrating_value, physicianrating_values):
    for y in x:
        r = y.rate
        physicianrating_value.append(r)
    physicianratingcount = len(physicianrating_value)
    physicianrating_values_sum = np.sum(physicianrating_value)
    average_rate = physicianrating_values_sum / physicianratingcount
    ceiled_average_rate = math.ceil(average_rate)
    physicianrating_values.append(ceiled_average_rate)
    return physicianrating_values


def Return_Doctor_Details_For_Recommendation(NN):
    array_of_data = []
    doctor = get_object_or_404(Physician, physician_nn=NN)
    physician_nn = doctor.physician_nn
    array_of_data.append(int(physician_nn.national_number))
    physicianSpecialization = PhysicianSpecialization.objects.filter(physician_nn=NN)
    specialization_id = []
    for i in physicianSpecialization:
        specialization_id.append(i.specialization_id)
    array_of_data.append(specialization_id)
    x = PhysicianRating.objects.filter(physician_nn=NN)
    physicianrating_value = []
    physicianrating_values = []
    rate = None
    if PhysicianRating.objects.filter(physician_nn=NN):
        x = PhysicianRating.objects.filter(physician_nn=NN)
        physicianrating_value = []
        rate = handle_rating(x, physicianrating_value, physicianrating_values)
    else:
        # note we should set a default hidden record for rating in database
        x = PhysicianRating.objects.filter(physician_nn=100)
        physicianrating_value = []
        rate = handle_rating(x, physicianrating_value, physicianrating_values)
    array_of_data.append(rate[0])
    physicianclinicworkingtime = []
    fee = []
    physicianclinicworkingtime = PhysicianClinicWorkingTime.objects.filter(physician_nn=NN)
    for x in physicianclinicworkingtime:
        fee.append(x.fee)
    if fee:
        fee = min(fee)
    else:
        fee = 100

    array_of_data.append(fee)
    physicianbooking = []
    physicianbookings = []
    physicianbooking = PhysicianPatientBooking.objects.filter(physician_nn=NN)
    for x in physicianbooking:
        physicianbookings.append(x)
    booking_count = len(physicianbooking)
    array_of_data.append(booking_count)
    return array_of_data


def Save_All_Doctors_In_Recommendation_Data_Base(NN):
    PhysicianRecommendation.objects.all().delete()
    # for saving :
    physician_nn = []
    physicianrating_values = []  # rating
    fee = []
    booking_count = []
    specialization_id = []
    doctors = Physician.objects.all().filter(hide=False)
    doctor = []
    physician_objects = []
    for i in doctors:
        doctor.append(i)
    physicianclinicworkingtime = []
    physicianclinicworkingtimes = []
    for i in doctor:
        physician_object = Physician.objects.filter(physician_nn=i.physician_nn)
        physician_objects.append(physician_object)
        # (******************handle fee******************)
    for x in physician_objects:
        physicianclinicworkingtime = PhysicianClinicWorkingTime.objects.filter(physician_nn=x[0]).filter(hide=False)
        physicianclinicworkingtimes.append(physicianclinicworkingtime)
    array_length = len(physicianclinicworkingtimes)
    feees = []
    pop = []
    for x in range(array_length):
        fees = physicianclinicworkingtimes[x]
        pop.append(fees)
    array_length2 = len(pop)
    for x in range(array_length2):
        feees = pop[x]
        for i in feees:
            fee.append(i)
           # (******************handle rating******************)
    physicianratings = []
    default = None
    for i in physician_objects:
        if PhysicianRating.objects.filter(physician_nn=i[0]):
            x = PhysicianRating.objects.filter(physician_nn=i[0])
            physicianrating_value = []
            handle_rating(x, physicianrating_value, physicianrating_values)
        else:
            # note we should set a default hidden record for rating in database
            x = PhysicianRating.objects.filter(physician_nn=100)
            physicianrating_value = []
            handle_rating(x, physicianrating_value, physicianrating_values)
        physician_nn.append(i[0])
    # ***************************handle     specialization************************
    for i in physician_objects:
        specialization = PhysicianSpecialization.objects.filter(physician_nn=i[0])
        specialization_id.append(specialization)
    # ***************************handle    booking**********************
    physicianbooking = []
    physicianbookings = []
    for i in physician_objects:
        physicianbooking = PhysicianPatientBooking.objects.filter(physician_nn=i[0])
        for x in physicianbooking:
            physicianbookings.append(x)
        booking_count.append(len(physicianbooking))
    keys = []
    values = []

    for i in specialization_id:
        sp = i
        for x in sp:
            nn = x.physician_nn.physician_nn.national_number
            keys.append(nn)
            values.append(x.specialization_id)
    sp_list = [[int(keys[i]), values[i]] for i in range(len(keys))]
    my_dict_sp = {}
    for i in sp_list:
        my_dict_sp[i[0]] = list()
        for item in sp_list:
            if item[0] == i[0]:
                my_dict_sp[i[0]].append(item[1])

    ######################### fee optimization  #############################
    x = []
    y = []
    w = 0
    for i in fee:
        nn = i.physician_nn.physician_nn.national_number
        ff = i.fee
        y.append(ff)
        x.append(nn)
    # feee=[]
    dictlist = [[int(x[i]), y[i]] for i in range(len(y))]
    my_dict_fee = {}

    for i in dictlist:
        my_dict_fee[i[0]] = list()
        for item in dictlist:
            if item[0] == i[0]:
                my_dict_fee[i[0]].append(item[1])
    fee_values = []
    fee_keys = []
    for i in my_dict_fee.keys():
        fee_values.append(min(my_dict_fee[i]))
        fee_keys.append(i)
    fee_ready = dict(zip(fee_keys, fee_values))

    counter = 0
    default_fee = 0
    for i in physician_nn:
        x = int(i.physician_nn.national_number)
        try:
            default_fee = fee_ready[x]
        except KeyError:
            default_fee = 200
        save_to_data_base = PhysicianRecommendation.objects.create(
            physician_nn=physician_nn[counter],
            rating=physicianrating_values[counter],
            specialization_id=my_dict_sp[x],
            booking_count=booking_count[counter],
            fee=default_fee,
        )
        counter = counter + 1
        # ************************************ KNN PART ****************************#


def load_data():
    doctor = []
    doctor = PhysicianRecommendation.objects.all()
    return doctor

# find euclidean distance between 2 data points


def calculate_euclidean_distance(instance1, instance2, length):
    distance_between_points = 0
    rating = instance2.rating
    fee = instance2.fee
    booking_count = instance2.booking_count

    counter = 2
    distance_between_points = pow((float(instance1[counter]) - float(rating)), 2)
    counter = counter + 1
    distance_between_points = pow((float(instance1[counter]) - float(fee)), 2) + distance_between_points
    counter = counter + 1
    distance_between_points = pow((float(instance1[counter]) - float(booking_count)), 2) + distance_between_points

    return math.sqrt(distance_between_points)

# finding the neighbors of the test_instance after sorting them by distance


def fetch_neighbors(training_set, test_instance, k):
    distances = []
    length = len(test_instance) - 2
    counter = 0
    y = 0
    for x in range(len(training_set)):
        z = training_set[counter].specialization_id
        z = ast.literal_eval(z)  # convert list as string to list as int
        # z = [n.strip() for n in z]  or use !!!
        if (np.in1d(test_instance[1], z)).any() == True:
            distance_between_points = calculate_euclidean_distance(test_instance, training_set[counter], length)
            distances.append((training_set[counter], distance_between_points))
        counter = counter + 1

    distances.sort(key=lambda x: x[1])

    neighbors_list = []

    for x in range(k):
        try:
            neighbors_list.append(distances[x + 1][0].physician_nn)
        except IndexError:
            neighbors_list.append(None)
    return neighbors_list


def main(current_doctor_data):
    # preparing data
    training_set = load_data()
    # generating knn_predictions
    k = 6
    test_set = current_doctor_data
    for x in range(len(test_set) - 2):
        neighbors_list = fetch_neighbors(training_set, test_set, k,)
    return neighbors_list
