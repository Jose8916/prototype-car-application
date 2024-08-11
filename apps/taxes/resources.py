from import_export import resources
from import_export.fields import Field

from apps.taxes.models import Rate

class RateExportResource(resources.ModelResource):
	id=Field(attribute='id', column_name='ID')
	unit=Field(attribute='unit', column_name='Unidades')
	value=Field(attribute='value', column_name='Valores')
	discount_increase=Field(attribute='discount_increase', column_name='descuentos e incrementos')
	class Meta:
		model = Rate
		fields = (
			"id",
			"unit",
			"value",
			"discount_increase"
		)
		export_order = (
			"id",
			"unit",
			"value",
			"discount_increase"
		)