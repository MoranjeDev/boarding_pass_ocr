from django.http import HttpResponse
from django.template import loader
import requests
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile


def upload_and_process(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            file_path = uploaded_file.file.path
            
            # Traitement OCR
            ocr_result = process_ocr(file_path)
            
            return render(request, 'results.html', {'ocr_result': ocr_result})
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})

def process_ocr(file_path):
    # Utilisation d'une API OCR en ligne (ex: OCR.Space, Tesseract OCR via un service web, etc.)
    api_url = "https://api.ocr.space/parse/image"
    with open(file_path, 'rb') as file:
        response = requests.post(api_url, files={"file": file}, data={"apikey": "K85136700188957"})
    result = response.json()
    return result.get("ParsedResults")[0].get("ParsedText")