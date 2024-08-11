from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from django.http import JsonResponse
from apps.users.serializers import *
@api_view(['GET'])
def api_cod(request,cod):
    queryset = Card.objects.filter(code=cod)
    serializer = CardSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def api_events_wompi(request):
	try:
		reference=request.data['data']['transaction']['reference']
		invoice = Invoice.objects.get(payment_reference=reference)
		#llave de evento que esta en la plataforma de wompi en  mi cuenta
		if request.data['environment'] == "prod":
			event_key="prod_events_PH9pP0cnGytACDxX71thkuqiqO1nHK8G"
		else:
			event_key="test_events_rdO9nDOuBQZnr7FagZ8nF9Dai5VykEtN"
		checksum=request.data['data']['transaction']['id']+request.data['data']['transaction']['status']+str(request.data['data']['transaction']['amount_in_cents'])+str(request.data['timestamp'])+event_key
		checksum=hashlib.sha256(checksum.encode('utf-8')).hexdigest()
		if invoice.exists() and checksum == request.data['signature']['checksum']:
			invoice.id_transaction = request.data['data']['transaction']['id']
			invoice.payment_method= request.data['data']['transaction']['payment_method_type']
			invoice.create_date= request.data['data']['transaction']['created_at']
			if request.data['data']['transaction']['status'] == "APPROVED":
				invoice.state_id= 2
			elif request.data['data']['transaction']['status'] == "DECLINED":
				invoice.state_id= 4
			elif request.data['data']['transaction']['status'] == "VOIDED":
				invoice.state_id= 5
			elif request.data['data']['transaction']['status'] == "ERROR":
				invoice.state_id= 6
			elif request.data['data']['transaction']['status'] == "PENDING":
				invoice.state_id= 3
			invoice.save()
			return Response(status=200)
		else:
			return Response({"error":"No existe una factura relacionada"}, status=400)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		print(e)
		return Response({"error": e}, status=400)