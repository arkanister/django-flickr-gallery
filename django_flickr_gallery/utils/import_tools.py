from django.views.generic.base import View
from django.utils.importlib import import_module


def load_class(class_path):
    """
    Load class by path.
    :param class_path:
        Class path with comma separate.
    :return: Class

    :example:
        >>> from django_flickr_gallery.utils.import_tools import load_class
        >>> load_class("mysiste.MyClass")

    """
    class_path, class_name = class_path.rsplit(".", 1)
    module = import_module(class_path)
    return getattr(module, class_name)


def load_view(path):
    """
    Load view to urls patterns by path.
    :param path:
        Path of view.
    :return: view func
    """
    app_name, view_name = path.split('.')

    absolute_path = '.'.join([app_name, 'views', view_name])
    view = load_class(absolute_path)

    if issubclass(view, View):
        return view.as_view()

    return view
