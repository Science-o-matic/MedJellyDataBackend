# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import HiddenInput
from form_utils.forms import BetterModelForm
from sights.models import Sight, Variable


class SightForm(BetterModelForm):
    # water_temperature = forms.FloatField(label="Temperatura del aigua")
    # water_temperature_id = forms.CharField(widget=HiddenInput)
    # metereology_sun = forms.BooleanField(label="Sol")
    # metereology_sun_id = forms.CharField(widget=HiddenInput)
    # metereology_rain = forms.BooleanField(label="Plutja")
    # metereology_rain_id = forms.CharField(widget=HiddenInput)
    # metereology_clouds = forms.BooleanField(label="Núvol")
    # metereology_clouds_id = forms.CharField(widget=HiddenInput)
    # metereology_lrain = forms.BooleanField(label="Xàfecs")
    # metereology_lrain_id = forms.CharField(widget=HiddenInput)
    # # Generate on the fly with ids of variables of this beach
    # sea = forms.ChoiceField(choices=((1,'Plana'), (2, 'Arrissada'), (3, 'Marejol'), (4, 'Maror'), 
    #                                  (5, 'Forta maror')))
    # background_sea = forms.BooleanField(label="Mar de fons")
    # background_sea_id = forms.CharField(widget=HiddenInput)


    def __init__(self, *args, **kwargs):
        BetterModelForm.__init__(self, *args, **kwargs)
        variables = Variable.objects.values_list("type", flat=True)
        print variables
        
    #     self.custom_fields = self._get_custom_fields(model_name, filter_qs)
    #     self.custom_form_fields = self._get_custom_form_fields(
    #         FieldClass, initial)
    #     self.fields.update(self.custom_form_fields)
    #     if self.fieldsets:
    #         self._add_custom_fields_to_fieldset()

    # def _get_custom_form_fields(self, FieldClass=None, initial={}):
    #     custom_fields = {}
    #     for key, cf in self.custom_fields.iteritems():
    #         if not FieldClass:
    #             field_class_name = cf.field_type
    #             FieldClass = getattr(forms, field_class_name)
    #         field = FieldClass(label=cf.verbose_name, required=cf.required,
    #                            initial=initial.get(key, None))
    #         custom_fields[key] = field
    #     return custom_fields

    # def _get_custom_fields(self, model_name=None, filter_qs=None):
    #     if not model_name:
    #         model_name = self._meta.model.__name__
    #     cfields_objects = CustomField.objects.filter(
    #         content_type__model=model_name)
    #     if filter_qs:
    #         cfields_objects = cfields_objects.filter_qs()
    #     custom_fields = {}
    #     for cfield in cfields_objects:
    #         field_name = safe_custom_field_name(cfield.name).lower()
    #         custom_fields[field_name] = cfield
    #     return custom_fields

    # def _add_custom_fields_to_fieldset(self):
    #     for i in range(len(self.fieldsets.fieldsets)):
    #         fs_fields = self.fieldsets.fieldsets[i][1]
    #         add_cfields = fs_fields.get('add_custom_fields',
    #                                     False)
    #         if add_cfields:
    #             fs_fields['fields'].extend(
    #                 self.custom_form_fields.keys())


    class Meta:
        model = Sight
        fieldsets = [('main', {'fields': ['beach', 'timestamp',],
                               'legend': ''}),
                      ]
        #              ('water_temperature', {'fields': ['water_temperature', 'water_temperature_id'],
        #                                     'legend': "Temperatura del aigua"}),
        #              ('metereology', {'fields': ['metereology_sun', 'metereology_sun_id',
        #                                          'metereology_rain', 'metereology_rain_id',
        #                                          'metereology_clouds', 'metereology_clouds_id',
        #                                          'metereology_lrain', 'metereology_lrain_id',
        #                                          ],
        #                               'legend': "Metereologia"}),
        #              ('metereology', {'fields': ['metereology_sun', 'metereology_sun_id',
        #                                          'metereology_rain', 'metereology_rain_id',
        #                                          'metereology_clouds', 'metereology_clouds_id',
        #                                          'metereology_lrain', 'metereology_lrain_id',
        #                                          ],
        #                               'legend': "Metereologia"}),
        #              ('sea', {'fields': ['sea', 'background_sea',],
        #                               'legend': "Estat de la mar"}),

        #              ]

