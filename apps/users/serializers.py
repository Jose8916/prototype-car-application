from apps.users.models import *
from rest_framework import serializers

class CardSerializer(serializers.ModelSerializer):
    state_card_name=serializers.SerializerMethodField('is_state')
    username=serializers.SerializerMethodField('is_user')
    def is_state(self,intance):
        return intance.state_card.name
    def is_user(self,intance):
        return intance.user.user.username
    
    class Meta:
        model = Card
        fields = [
            'id',
            'state_card_name',
            'code',
            'username'
        ]
