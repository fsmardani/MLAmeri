from uuid import uuid4

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf
from django.urls import reverse
from tensorflow import keras
from cv2 import cv2
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

from django.http import HttpResponse
from django.shortcuts import render, redirect
import uuid
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .models import Input,Output
# from utils import coutput_path,moutput_path,cmoutput_path


def DETECTING(SourceInputImageDir, M_WindowShape, C_WindowShape):
    M_NetDir = 'app/CNN.h5'
    C_NetDir = 'app/CNN.h5'
    ResultDir_C = 'output'
    TemplatePachDir = 'temp'
    ResultDir_M = 'output'
    ResultDir_M_C = 'output'


    imtest = cv2.imread(SourceInputImageDir, 1)
    model = keras.models.load_model(M_NetDir)
    d = imtest[:, :, 1]
    [a, b] = d.shape
    d = imtest
    ZeroPachesNumber = 0
    NonZeroPachesNumber = 0
    k = 0
    WindowShape = M_WindowShape
    M = np.int(a / WindowShape)
    N = np.int(b / WindowShape)
    M_M = M
    N_M = N
    PatchPosition_M = np.zeros((M, N))
    for i in range(M):
        for j in range(N):
            CNNFeedPic = d[i * WindowShape:i * WindowShape + WindowShape, j * WindowShape:j * WindowShape + WindowShape]
            p = CNNFeedPic.sum()
            if p == 0:
                ZeroPachesNumber = ZeroPachesNumber + 1
            else:
                im = Image.fromarray(CNNFeedPic)
                im.save(TemplatePachDir+'/1.png')
                [img_height, img_width] = [160, 160]
                img = keras.preprocessing.image.load_img(TemplatePachDir+'/1.png', target_size=(img_height, img_width))
                img_array = keras.preprocessing.image.img_to_array(img)
                img_array = tf.expand_dims(img_array, 0)
                predictions = model.predict(img_array)
                Tempimage = plt.imread(TemplatePachDir+"/1.png")
                if predictions[0].sum() > 0:
                    PatchPosition_M[i, j] = 1
                    k = k + 1
                    cv2.rectangle(imtest, (j * WindowShape, i * WindowShape),
                                  (j * WindowShape + WindowShape, i * WindowShape + WindowShape), (0, 0, 255),
                                  thickness=10, lineType=cv2.LINE_8)
                    cv2.putText(imtest, "M", (j * WindowShape, i * WindowShape), cv2.FONT_HERSHEY_SIMPLEX, 2,
                                (0, 0, 255), 5)
    im = Image.fromarray(imtest)
    Out_M_Image = im
    # im.save(ResultDir_M+'/1.png')

    imtest = cv2.imread(SourceInputImageDir, 1)
    CalcIm = imtest
    model = keras.models.load_model(C_NetDir)
    WindowShape = C_WindowShape
    M = np.int(a / WindowShape)
    N = np.int(b / WindowShape)
    M_C = M
    N_C = N
    PatchPosition_C = np.zeros((M, N))
    i = 0
    j = 0
    for i in range(M):
        for j in range(N):
            CNNFeedPic = CalcIm[i * WindowShape:i * WindowShape + WindowShape,
                         j * WindowShape:j * WindowShape + WindowShape]
            p = CNNFeedPic.sum()
            if p == 0:
                ZeroPachesNumber = ZeroPachesNumber + 1
            else:
                im = Image.fromarray(CNNFeedPic)
                im.save(TemplatePachDir+'/2.png')
                [img_height, img_width] = [160, 160]
                img = keras.preprocessing.image.load_img(TemplatePachDir+'/2.png', target_size=(img_height, img_width))
                img_array = keras.preprocessing.image.img_to_array(img)
                img_array = tf.expand_dims(img_array, 0)
                predictions = model.predict(img_array)
                Tempimage = plt.imread(TemplatePachDir+'/2.png')
                if predictions[0].sum() > 0:
                    PatchPosition_C[i, j] = 1
                    k = k + 1
                    cv2.rectangle(CalcIm, (i * WindowShape, j * WindowShape),
                                  (i * WindowShape + WindowShape, j * WindowShape + WindowShape), (0, 255, 0),
                                  thickness=10, lineType=cv2.LINE_8)
                    cv2.putText(CalcIm, "C", (j * WindowShape, i * WindowShape), cv2.FONT_HERSHEY_SIMPLEX, 2,
                                (0, 255, 0), 5)
    im = Image.fromarray(CalcIm)
    Out_C_Image = im
    # im.save(ResultDir_C+'/2.png')

    M_C_Im = imtest
    WindowShape = M_WindowShape
    for i in range(M_M):
        for j in range(N_M):
            if PatchPosition_M[i, j] == 1:
                cv2.rectangle(M_C_Im, (i * WindowShape, j * WindowShape),
                              (i * WindowShape + WindowShape, j * WindowShape + WindowShape), (0, 0, 255), thickness=10,
                              lineType=cv2.LINE_8)
                cv2.putText(M_C_Im, "M", (j * WindowShape, i * WindowShape), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
                            5)
    i = 0
    j = 0
    WindowShape = C_WindowShape
    for i in range(M_C):
        for j in range(N_C):
            if PatchPosition_C[i, j] == 1:
                cv2.rectangle(M_C_Im, (i * WindowShape, j * WindowShape),
                              (i * WindowShape + WindowShape, j * WindowShape + WindowShape), (0, 255, 0), thickness=10,
                              lineType=cv2.LINE_8)
                cv2.putText(M_C_Im, "C", (j * WindowShape, i * WindowShape), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0),
                            5)
    im = Image.fromarray(M_C_Im)
    Out_M_C_Image = im
    # im.save(ResultDir_M_C+'/3.png')
    return Out_M_Image, Out_C_Image, Out_M_C_Image


# @csrf_exempt
def index(request):
    if request.method=='POST':
        if request.FILES:
            if int(request.POST.get("min", None))>=50 and int(request.POST.get("max", None))<=500:
                obj = Input.objects.create(image=request.FILES.get("image"),variable_1=int(request.POST.get("min")),variable_2=int(request.POST.get("max")))
                c_res,m_res,cm_res =DETECTING(f'{obj.image}', int(request.POST.get("min")), int(request.POST.get("max")))
                print(type(c_res))
                Output.objects.create(input_ids=obj,Cimage=c_res,Mimage=m_res,CMimage=cm_res)
                return redirect(reverse('result'))
        else:
            return HttpResponse(request.FILES)
    if request.method=='GET':
        return render(request,'app.html')

def result(request,id):
    obj = Output.objects.filter(input__id=id)[0]
    return render(request,'result.html',{'results':obj})

def get_images(request,pk):
    inputq = Input.objects.filter(pk=pk)[0]
    return render(request,'app.html',{'input':inputq})

