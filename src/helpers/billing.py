import stripe
from typing import Union
from decouple import config

class Billing:
    __STRIPE_SECRET_KEY = config(option='STRIPE_SECRET_KEY', cast=str, default='')
    __DEBUG = config(option='DEBUG', cast=bool, default=True)
    stripe.api_key = __STRIPE_SECRET_KEY

    def __init__(self) -> None:
        if 'sk_test' in self.__STRIPE_SECRET_KEY and not self.__DEBUG:
            raise ValueError('Invalid Stripe key provided for non-test environment.')

    @classmethod
    def __search(cls, resource: stripe.APIResource, **kwargs) -> Union[bool, str]:
        query = ''.join([f'{k}: "{v}"' for k, v in kwargs.items()])
        response = resource.search(query=query)
        return response.data[0].id if response.data else None

    @classmethod
    def __create(cls, resource: stripe.APIResource, **kwargs) -> str:
        response = resource.create(**kwargs)
        return response.id

    @classmethod
    def get_or_create_product(cls, name: str, active: bool = True, 
                              description: str = None, metadata: dict = None) -> str:
        # metadata = metadata or {}  # Avoid mutable default argument
        product = cls.__search(resource=stripe.Product, name=name)
        if not product:
            product = cls.__create(resource=stripe.Product, name=name, active=active, 
                                   description=description, metadata=metadata)
        return product

    @classmethod
    def get_or_create_customer(cls, email: str, name: str = None) -> Union[bool, str]:
        customer = cls.__search(resource=stripe.Customer, email=email)
        if not customer:
            customer = cls.__create(resource=stripe.Customer, name=name, email=email)
        return customer

    @classmethod
    def delete(cls):
        pass