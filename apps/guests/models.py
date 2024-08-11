from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from apps.users.models import CardSubscription, Extended_User

class wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet_user', primary_key=True)
    balance = models.BigIntegerField(default=0)
    class Meta:
        db_table = "wallet"
        verbose_name_plural = "Wallet"
        ordering = ["user"]
    
    def __str__(self):
        return str(self.user)
    
class types_movements(models.Model):
    name = models.CharField(max_length=200)
    class Meta:
        db_table = "types_movements"
        verbose_name_plural = "Types movements"
        ordering = ["name"]
    
    def __str__(self):
        return str(self.name)
    
class balance_wallet(models.Model):
    CHOICES_TYPE_BONUS = [
        ("1","Directo"),
        ("2","Indirecto"),
    ]
    type_movement = models.ForeignKey(types_movements,on_delete=models.RESTRICT,related_name='balance_type_movements')
    amount = models.BigIntegerField()
    wallet = models.ForeignKey(wallet,on_delete=models.RESTRICT,related_name='wallet_balance')
    payment_method = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=200, null=True)
    transaction_number = models.CharField(max_length=100, null=True)
    user_bonus_origin = models.ForeignKey(Extended_User,on_delete=models.RESTRICT,related_name='balance_wallet_user_bonus',null=True)
    type_bonus = models.CharField(max_length=1,choices=CHOICES_TYPE_BONUS)
    card_subscription = models.ForeignKey(CardSubscription,on_delete=models.RESTRICT,related_name='balance_wallet_card_suscription',null=True)
    create_date = models.DateTimeField(null=True, default=timezone.now)
    create_user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name='balance_wallet_create_user')    
    transfer_user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name='balance_wallet_transfer_user')    
    origin_user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name='balance_wallet_origin_user')    
    class Meta:
        db_table = "balance_wallet"
        verbose_name_plural = "Balance wallet"
        ordering = ["-create_date"]
        indexes = [
            models.Index(fields=['wallet']),
            models.Index(fields=['type_movement']),
            models.Index(fields=['wallet','user_bonus_origin']),
        ]  
    
    def __str__(self):
        return str(self.create_date)+" | "+str(self.type_movement)+"-"+str(self.amount)
    
    def code_invitation_transfer_user(self):
        code = ""
        if self.transfer_user:
            obj_user = Extended_User.objects.filter(user=self.transfer_user).first() or None
            if obj_user:
                code = obj_user.get_code_invitation()+" | "+obj_user.user.first_name+" "+obj_user.user.last_name
        return code
    
    def code_invitation_origin_user(self):
        code = ""
        if self.origin_user:
            obj_user = Extended_User.objects.filter(user=self.origin_user).first() or None
            if obj_user:
                code = obj_user.get_code_invitation()+" | "+obj_user.user.first_name+" "+obj_user.user.last_name
        return code
    
    def code_invitation_direct(self):
        code = ""
        if self.user_bonus_origin:
            obj_user_invitation = self.user_bonus_origin
            if obj_user_invitation:
                code = str(obj_user_invitation.get_code_invitation())+" | "+obj_user_invitation.user.first_name+" "+obj_user_invitation.user.last_name
        return code