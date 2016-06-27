from django.shortcuts import render


def get_featured_photosets(request):
    return render(request, template_name="myapp/show_photos.html")
