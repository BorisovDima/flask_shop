from flask import render_template,  jsonify, request
from flask.views import MethodView


class BaseView(MethodView):
    template_name = None
    extra_context = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_template(self, context):
        if self.extra_context: context.update(self.extra_context)
        template = render_template(self.template_name, **context)
        return template


class WrapJsonMixin:

    def dispatch_request(self, *args, **kwargs):
        response = super().dispatch_request(*args, **kwargs)
        if request.is_xhr:
            response = jsonify(self.make_json(response) if getattr(self, 'make_json', False) else response)
        return response


class FilterView(BaseView):
    model = None
    paginate = None
    filter_class = None

    def filter_objs(self, objs):
        if self.filter_class:
            self.filter = self.filter_class(formdata=request.args, csrf_enabled=False)
            objs = self.filter.make_filtering(objs)
        return objs


    def get_objs(self):
        objs = self.filter_objs(self.model.query.filter())
        if self.paginate:
            page = request.args.get('page', '')
            page = int(page) if page.isdigit() else 1
            objs = objs.paginate(page=page, per_page=self.paginate)
        return objs

    def get(self, *args, **kwargs):
        context = {'objects': self.get_objs()}
        if self.filter: context.update({'filter': self.filter})
        return self.get_template(context)


class DetailView(BaseView):
    model = None
    key = None
    from_params = True

    def get_obj(self, kwargs):
        key = kwargs.get(self.key) if not self.from_params else request.args.get(self.key)
        q = self.model.query.filter_by(**{self.key: key})
        return q.first_or_404()

    def get(self, *args, **kwargs):
        obj = self.get_obj(kwargs)
        return self.get_template({'object': obj})

