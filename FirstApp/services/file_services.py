import pandas as pd
from models import *

class DataFetcher:
    @staticmethod
    def datafetcher(customer_fields=None, product_fields=None, order_fields=None):
        # Fetching data from the Customer table
        customer_queryset = Customer.objects.all()
        if customer_fields:
            customer_queryset = customer_queryset.values(*customer_fields)

        # Fetching data from the Product table
        product_queryset = Product.objects.all()
        if product_fields:
            product_queryset = product_queryset.values(*product_fields)

        # Fetching data from the Order table
        order_queryset = Order.objects.all()
        if order_fields:
            order_queryset = order_queryset.values(*order_fields)

        # Converting data to DataFrames
        customer_df = pd.DataFrame.from_records(customer_queryset)
        product_df = pd.DataFrame.from_records(product_queryset)
        order_df = pd.DataFrame.from_records(order_queryset)

        # Returning data in CSV format
        data = {
            'Customer': customer_df.to_csv(index=False),
            'Product': product_df.to_csv(index=False),
            'Order': order_df.to_csv(index=False)
        }

        return data
