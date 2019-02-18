from flask_admin import form
from flask_admin._compat import urljoin
from flask import current_app
from flask_admin.model.form import InlineFormAdmin

from blueprints.core.utils import slugify
from wtforms import ValidationError
import os


MEDIA_URL = current_app.config['MEDIA_URL']
MEDIA_PATH = current_app.config['MEDIA_PATH']



class VariantsInlineForm(InlineFormAdmin):
    form_excluded_columns = ('date_create', 'last_sale')

    form_choices = {
        'size':  (('S','S'),
                  ('M','M'),
                  ('L','L'),
                  ('XL','XL'),
                  ('2XL','2XL'),
                  ('3XL','3XL'),
                  ('4XL','4XL'),
                  ('5XL','5XL'))
          }


class MyUploadInput(form.ImageUploadInput):

    def get_url(self, field):
        filename = field.thumbnail_fn(field.data)
        return urljoin(field.url_relative_path, filename)


class MyImageUploadField(form.ImageUploadField):
    thumbnail_size = (800, 600, True)
    widget = MyUploadInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         base_path=MEDIA_PATH,
                         url_relative_path=MEDIA_URL,
                         thumbnail_size=self.thumbnail_size,
                         **kwargs)


    def _save_file(self, data, filename):
        filename = super()._save_file(data, filename)
        return os.path.join(self.url_relative_path, filename)


class MakeSlug:
    def __call__(self, form, field):
        try:
            field.data = slugify(form.name.data)
        except Exception:
            raise ValidationError('Slug: Something wrong')







