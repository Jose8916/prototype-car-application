# django
from django.shortcuts import redirect
from django.urls import reverse
import os
class AffiliateStartValidation :
	def __init__(self, get_response):
		self.get_response=get_response

	def __call__(self,request):
		if request.user.groups.filter(name='Affiliate').exists():
			if request.user.extended_user.affiliate.category == None:
				if request.path!=reverse('users:affiliate-registration-step-two'):
					return redirect('users:affiliate-registration-step-two')

		# if not request.user.is_anonymous:
		# 	if es_afiliado: 
		# 		afiliado = request.user.extended_user.affiliate
				# {if not afiliado.category:
								# 	if request.path!=reverse('users:affiliate-registration-step-two'):
								# 		return redirect('users:affiliate-registration-step-two')
								# if afiliado.state_card.id!=1:
								# 	if request.path!=reverse('users:activate-card'):
								# 		return redirect('users:activate-card')}
		response = self.get_response(request)
		return response
