import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer, Product, Order
from services.file_services import DataFetcher
from django.http import HttpResponse

class DataFetchAPIView(APIView):
    
    def post(self, request):
        # Perform request validation
        if not request.data.get('customer_fields') and not request.data.get('product_fields') and not request.data.get('order_fields'):
            return Response("At least one field parameter should be provided.", status=400)

        # Fetch data using DataFetcher
        data_fetcher = DataFetcher()
        csv_data = data_fetcher.datafetcher(
            customer_fields=request.data.get('customer_fields'),
            product_fields=request.data.get('product_fields'),
            order_fields=request.data.get('order_fields')
        )

        # Create a combined DataFrame
        combined_df = pd.concat([pd.read_csv(pd.compat.StringIO(csv_data['Customer'])),
                                 pd.read_csv(pd.compat.StringIO(csv_data['Product'])),
                                 pd.read_csv(pd.compat.StringIO(csv_data['Order']))],
                                axis=1)

        # Determine the requested file format
        file_format = request.data.get('format', 'csv').lower()

        if file_format == 'csv':
            # Generate CSV file response
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="data.csv"'
            combined_df.to_csv(path_or_buf=response, index=False, encoding='utf-8')
        elif file_format == 'excel':
            # Generate Excel file response
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
            combined_df.to_excel(response, index=False)
        elif file_format == 'json':
            # Generate JSON file response
            response = HttpResponse(content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="data.json"'
            combined_df.to_json(response, orient='records')
        else:
            return Response("Invalid file format specified.", status=400)

        return response
