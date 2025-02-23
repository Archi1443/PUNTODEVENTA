from django import template

register = template.Library()

@register.filter(name='format_estado')
def format_estado(value):
    estados = {
        'en_proceso': 'En proceso',
        'finalizado': 'Finalizado',
        'ingresado': 'Ingresado',
        'entregado': 'Entregado'
    }
    return estados.get(value, value)  # Devuelve el valor formateado o el original si no está en el diccionario
