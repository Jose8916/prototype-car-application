from django.db.models import Q
from django.contrib.auth.models import User
from import_export import resources
from import_export.fields import Field
from apps.users.models import *

class CardExport(resources.ModelResource):
	id=Field(attribute='id')
	first_name=Field(attribute='user__user__first_name')
	last_name=Field(attribute='user__user__last_name')
	email=Field(attribute='user__user__username')
	document_type=Field(attribute='user__document_type__name')
	document_number=Field(attribute='user__date_birth')
	date_birth=Field(attribute='user__date_birth')
	gender=Field(attribute='user__gender__name')
	blood_type=Field(attribute='user__blood_type__name')
	category=Field(attribute='user__category__name')
	cell_phone=Field(attribute='user__cell_phone')
	phone_secondary=Field(attribute='user__phone_secondary')
	city=Field(attribute='user__city__name')
	address=Field(attribute='user__address')
	description_address=Field(attribute='user__description_address')
	favorite_station=Field(attribute='user__favorite_station')
	favorite_music=Field(attribute='user__favorite_music')
	contact_person_name=Field(attribute='user__contact_person_name')
	contact_person_phone=Field(attribute='user__contact_person_phone')
	inviting_user=Field(attribute='user__inviting_user')
	authorizing_user=Field(attribute='user__authorizing_user')
	state=Field(attribute='user__state__name')
	call=Field(attribute='user__call')
	code=Field(attribute='code')
	activation_code=Field(attribute='activation_code')
	class Meta:
		model = Card
		fields = (
			'id',
			'first_name',
			'last_name',
			'email',
			'document_type',
			'document_number',
			'date_birth',
			'gender',
			'blood_type',
			'category',
			'cell_phone',
			'phone_secondary',
			'city',
			'address',
			'description_address',
			'favorite_station',
			'favorite_music',
			'contact_person_name',
			'contact_person_phone',
			'inviting_user',
			'authorizing_user',
			'state',
			'call',
			'code',
			'activation_code',
			)
		export_order = (
			'id',
			'first_name',
			'last_name',
			'email',
			'document_type',
			'document_number',
			'date_birth',
			'gender',
			'blood_type',
			'category',
			'cell_phone',
			'phone_secondary',
			'city',
			'address',
			'description_address',
			'favorite_station',
			'favorite_music',
			'contact_person_name',
			'contact_person_phone',
			'inviting_user',
			'authorizing_user',
			'state',
			'call',
			'code',
			'activation_code',
			)
	
class AllyExport(resources.ModelResource):
	id=Field(attribute='id')
	create_date=Field(attribute='create_date')
	name=Field(attribute='name')
	description=Field(attribute='description')
	number_mercantil=Field(attribute='number_mercantil')
	category=Field(attribute='category__name')
	cell_phone=Field(attribute='cell_phone')
	city=Field(attribute='city__name')
	address=Field(attribute='address')
	user_email=Field(attribute='user__user__username')
	city_user=Field(attribute='user__city__name')
	phone_user=Field(attribute='user__cell_phone')
	state=Field(attribute='state__name')
	description_state=Field(attribute='description_state')
	inactive_until=Field(attribute='inactive_until')

	class Meta:
		model = Ally
		fields = ("__all__")
	