# APPS DJANGO
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,View 
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.paginator import  InvalidPage
# APPS PROPIA
from apps.guests.forms import FormBalance, FormCreateRecharge,FormCreateTransfer
from apps.guests.models import balance_wallet, wallet
from apps.users.models import Card

TEMPLATE_ROOT = "guests/"

class BalanceList(View):
    def get(self,request):
        context = {}
        context["active_balance"] = "text-dark"
        context["form_busqueda"] = FormBalance()
        codigo_invitacion = request.GET.get("codigo_invitacion") or None
        if codigo_invitacion:
            context["codigo_invitacion"] = codigo_invitacion
            formulario = FormBalance(request.GET)
            if formulario.is_valid():
                obj_card = Card.objects.filter(code=codigo_invitacion).first()
                obj_extended_user = obj_card.user
                obj_user = obj_extended_user.user
                obj_user_wallet = wallet.objects.get(user=obj_user)
                movements = obj_user_wallet.wallet_balance.all()
                total_movements = 0
                for movement in movements:
                    total_movements += movement.amount
                context["total_movements"] = total_movements
                page = request.GET.get('page', 1)
                paginator = Paginator(movements,20)
                try:
                    movements = paginator.page(page)
                except PageNotAnInteger:
                    movements = paginator.page(1)
                except EmptyPage:
                    movements = paginator.page(paginator.num_pages)
                context["movements"] = movements
            context["form_busqueda"] = formulario
        return render(request, TEMPLATE_ROOT+'balance.html', context)

class BonusesList(View):
    def get(self,request):
        context = {}
        context["active_bonus"] = "text-dark"
        context["form_busqueda"] = FormBalance()
        codigo_invitacion = request.GET.get("codigo_invitacion") or None
        if codigo_invitacion:
            context["codigo_invitacion"] = codigo_invitacion
            formulario = FormBalance(request.GET)
            if formulario.is_valid():
                obj_card = Card.objects.filter(code=codigo_invitacion).first()
                obj_extended_user = obj_card.user
                obj_user = obj_extended_user.user
                obj_user_wallet = wallet.objects.get(user=obj_user)
                movements = obj_user_wallet.wallet_balance.all().filter(type_movement__id__in = ["4","5"])
                total_movements = 0
                for movement in movements:
                    total_movements += movement.amount
                context["total_movements"] = total_movements
                page = request.GET.get('page', 1)
                paginator = Paginator(movements,20)
                try:
                    movements = paginator.page(page)
                except PageNotAnInteger:
                    movements = paginator.page(1)
                except EmptyPage:
                    movements = paginator.page(paginator.num_pages)
                context["movements"] = movements
            context["form_busqueda"] = formulario
        return render(request, TEMPLATE_ROOT+'balance_bonus.html', context)
    

class RechargeView(CreateView):
    form_class = FormCreateRecharge
    success_url = reverse_lazy("guests:recharge")
    template_name= TEMPLATE_ROOT+'formulario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_recharge"] = "text-dark"
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(errors_form=[form]))
    
    def form_valid(self, form):
        obj_movimiento = form.save(commit=False)
        invitation_code = form.cleaned_data.get("invitation_code")
        if invitation_code:
            obj_card = Card.objects.filter(code=invitation_code).first()
            obj_extended_user = obj_card.user
            obj_user = obj_extended_user.user
            obj_user_wallet = wallet.objects.get(user=obj_user)
        obj_movimiento.type_movement_id = 1
        obj_movimiento.wallet = obj_user_wallet
        obj_movimiento.create_user = self.request.user
        obj_movimiento.save()
        obj_user_wallet.balance += obj_movimiento.amount
        obj_user_wallet.save()
        messages.add_message(self.request, messages.SUCCESS, "Recarga creada correctamente")
        return HttpResponseRedirect(self.success_url)

class TransferView(CreateView):
    form_class = FormCreateTransfer
    success_url = reverse_lazy("guests:transfer")
    template_name= TEMPLATE_ROOT+'formulario_transfer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_transfer"] = "text-dark"
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(errors_form=[form]))
    
    def form_valid(self, form):
        obj_movimiento = form.save(commit=False)
        invitation_code_origin = form.cleaned_data.get("invitation_code_origin")
        invitation_code_destination = form.cleaned_data.get("invitation_code_destination")
        if invitation_code_origin:
            obj_card = Card.objects.filter(code=invitation_code_origin).first()
            obj_extended_user = obj_card.user
            obj_user = obj_extended_user.user
            obj_user_wallet_origin = wallet.objects.get(user=obj_user)
        if invitation_code_destination:
            obj_card = Card.objects.filter(code=invitation_code_destination).first()
            obj_extended_user = obj_card.user
            obj_user = obj_extended_user.user
            obj_user_wallet_destination = wallet.objects.get(user=obj_user)
        obj_movimiento.type_movement_id = 2
        obj_movimiento.wallet = obj_user_wallet_origin
        obj_movimiento.create_user = self.request.user
        obj_movimiento.transfer_user = obj_user_wallet_destination.user
        obj_movimiento.amount = obj_movimiento.amount * -1
        obj_movimiento.save()
        obj_user_wallet_origin.balance += obj_movimiento.amount
        obj_user_wallet_origin.save()
        obj_movimiento_discount = balance_wallet()
        obj_movimiento_discount.type_movement_id = 3
        obj_movimiento_discount.wallet = obj_user_wallet_destination
        obj_movimiento_discount.create_user = self.request.user
        obj_movimiento_discount.origin_user = obj_user_wallet_origin.user
        obj_movimiento_discount.amount = obj_movimiento.amount * -1
        obj_movimiento_discount.save()
        obj_user_wallet_destination.balance += obj_movimiento_discount.amount
        obj_user_wallet_destination.save()
        messages.add_message(self.request, messages.SUCCESS, "Transferencia realizada correctamente")
        return HttpResponseRedirect(self.success_url)

