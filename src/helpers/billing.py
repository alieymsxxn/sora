import stripe
from typing import Union
from decouple import config


class Billing:
    __STRIPE_SECRET_KEY = config(option='STRIPE_SECRET_KEY', cast=str, default='')
    __DEBUG = config(option='DEBUG', cast=bool, default=True)
    stripe.api_key = __STRIPE_SECRET_KEY

    def __init__(self) -> None:
        if 'sk_test' in self.__STRIPE_SECRET_KEY and not self.__DEBUG:
            raise ValueError('Invalid Stripe key provide')

    @classmethod
    def __search(cls, resource, **kwargs) -> Union[bool, str]:
        query = ''.join([f'{k}: "{v}"' for k, v in kwargs.items()])
        response = resource.search(query=query)
        return response.data[0].id if response.data else None

    @classmethod
    def __create(cls, resource:stripe.APIResource, **kwargs) -> str:
        response = resource.create(**kwargs)
        return response.id

    @classmethod
    def get_or_create_product(cls, name:str, active:bool=True, 
                              description:str=None, metadata:dict={}) -> str:
        product = cls.__search(name=name, resource=stripe.Product)
        if not product:
            product = cls.__create(name=name, active=active, description=description,
                                    metadata=metadata, resource=stripe.Product)
        return product

    @classmethod
    def get_or_create_customer(cls, email: str, name: str = None) -> Union[bool, str]:
        customer = cls.__search(email=email, resource=stripe.Customer)
        if not customer:
            customer = cls.__create(name=name, email=email, resource=stripe.Product)
        return customer

    @classmethod
    def delete(cls):
        pass
