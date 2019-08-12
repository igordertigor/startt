import os
from shutil import copyfile
from tmpl.analyze import get_template_name


def copy_template(filename, template_folder):
    template_name = os.path.join(template_folder,
                                 get_template_name(filename))
    correct_filename = get_filename(filename)
    if os.path.isfile(template_name):
        copy_file_template(template_name, correct_filename)


def get_filename(filename):
    folder, basename = os.path.split(filename)
    segments = basename.split('.')
    return os.path.join(folder, '.'.join([segments[0], segments[-1]]))


def copy_file_template(template_name, target_name):
    copyfile(template_name, target_name)
