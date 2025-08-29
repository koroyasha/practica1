import re
from collections import Counter
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TextoAnalizadoForm
from .models import TextoAnalizado
from .preprocesamiento import limpiar_texto

def subir_texto(request):
    if request.method == 'POST':
        form = TextoAnalizadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_textos')
    else:
        form = TextoAnalizadoForm()
    return render(request, 'subir.html', {'form': form})

def lista_textos(request):
    textos = TextoAnalizado.objects.all().order_by('-fecha_subida')
    return render(request, 'lista.html', {'textos': textos})

def analizar_texto(request, texto_id):
    texto_obj = get_object_or_404(TextoAnalizado, id=texto_id)
    
    # Leer el contenido del archivo
    try:
        with texto_obj.archivo.open('r') as archivo:
            contenido = archivo.read()
    except Exception as e:
        contenido = ""
        print(f"Error al leer archivo: {e}")
    
    # Inicializar variables para evitar errores
    palabras_comunes_original = []
    palabras_comunes_limpias = []
    total_palabras_original = 0
    total_palabras_limpias = 0
    palabras_limpias_muestra = []
    
    # PROCESAMIENTO ORIGINAL
    try:
        palabras_originales = re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]+\b', contenido.lower())
        contador_original = Counter(palabras_originales)
        palabras_comunes_original = contador_original.most_common(20)
        total_palabras_original = len(palabras_originales)
    except Exception as e:
        print(f"Error en procesamiento original: {e}")
    
    # NUEVO PROCESAMIENTO CON LIMPIEZA
    try:
        palabras_limpias = limpiar_texto(contenido)
        contador_limpio = Counter(palabras_limpias)
        palabras_comunes_limpias = contador_limpio.most_common(20)
        total_palabras_limpias = len(palabras_limpias)
        palabras_limpias_muestra = palabras_limpias[:50]
    except Exception as e:
        print(f"Error en procesamiento limpio: {e}")
    
    return render(request, 'histograma.html', {
        'texto': texto_obj,
        'palabras_comunes_original': palabras_comunes_original,
        'palabras_comunes_limpias': palabras_comunes_limpias,
        'total_palabras_original': total_palabras_original,
        'total_palabras_limpias': total_palabras_limpias,
        'stopwords_eliminadas': total_palabras_original - total_palabras_limpias,
        'palabras_limpias_muestra': palabras_limpias_muestra
    })