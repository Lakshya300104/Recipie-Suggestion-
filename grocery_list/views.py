from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from fpdf import FPDF
import PyPDF2
import requests


def index(request):
    shopping_list = request.session.get('shopping_list',)
    return render(request, 'grocery_list/index.html', {'shopping_list': shopping_list})


def suggest_recipes(request):
    if request.method == 'POST':
        ingredients = request.POST.get('ingredients')
        api_url = "https://api.spoonacular.com/recipes/findByIngredients"
        api_key = "f8bb48b03837434c9285702f58c8064b"  # Replace with your API key
        params = {'ingredients': ingredients, 'number': 5, 'apiKey': api_key}
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            recipe_data = response.json()
            suggested_recipes = [recipe['title'] for recipe in recipe_data]
            return JsonResponse({'recipes': suggested_recipes})
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    return HttpResponse("Invalid request")

def download_pdf(request):
    shopping_list = request.session.get('shopping_list',)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Shopping List", ln=True, align='C')
    pdf.ln(10)
    for item in shopping_list:
        pdf.cell(200, 10, txt=item, ln=True)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shopping_list.pdf"'
    pdf.output(response)
    return response

def upload_pdf(request):
    if request.method == 'POST':
        try:
            pdf_file = request.FILES['pdf_file']
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            items = text.splitlines()
            cleaned_items = [item.strip() for item in items if item.strip()]
            request.session['shopping_list'] = cleaned_items
            return redirect('index')
        except Exception as e:
            return HttpResponse(f"Error uploading PDF: {e}")
    return HttpResponse("Invalid request")