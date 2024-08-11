from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.guests.models import balance_wallet, types_movements, wallet

@admin.register(wallet)
class walletAdmin(ImportExportModelAdmin):
    list_display = ('pk','user','balance')
    readonly_fields = ['balance']
    
@admin.register(types_movements)
class types_movementsAdmin(ImportExportModelAdmin):
    list_display = ('pk','name')
    
@admin.register(balance_wallet)
class balance_walletAdmin(ImportExportModelAdmin):
    list_display = ('pk','type_movement','amount','wallet')
    list_filter=('type_movement','wallet','create_date')
    readonly_fields = ['amount']