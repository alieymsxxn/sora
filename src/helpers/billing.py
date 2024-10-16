import stripe
import datetime
from typing import Union
from decouple import config

timestamp_to_datetime = lambda ts: datetime.datetime.fromtimestamp(timestamp=ts, tz=datetime.UTC)

class Billing:
    '''
    A class for handling billing operations via Stripe API.

    This class provides methods to interact with Stripe's API to manage billing-related resources,
    including products, customers, and transactions. It allows you to search, create, and retrieve
    Stripe resources in a streamlined way while managing error handling and API key setup.
    '''
    __STRIPE_SECRET_KEY = config(option='STRIPE_SECRET_KEY', cast=str, default='')
    __DEBUG = config(option='DEBUG', cast=bool, default=True)
    stripe.api_key = __STRIPE_SECRET_KEY

    def __init__(self) -> None:
        if 'sk_test' in self.__STRIPE_SECRET_KEY and not self.__DEBUG:
            raise ValueError('Invalid Stripe key provided for non-test environment.')
    
    @classmethod
    def __list(cls, resource: stripe.APIResource, **kwargs):
        listing = resource.list(**kwargs)
        return listing
   
    @classmethod
    def __search(cls, resource: stripe.APIResource, **kwargs) -> Union[bool, str]:
        query = ' AND '.join([f'{k}: "{v}"' for k, v in kwargs.items()])
        response = resource.search(query=query)
        return None if response.is_empty else response.data[0].id

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
    def get_or_create_price(cls, product: str, unit_amount: int, currency: str = 'usd', 
                            recurring: dict = {'interval': 'month'}) -> str:
        lookup_key = f'{product}__{recurring["interval"]}__{unit_amount}'
        price = cls.__search(resource=stripe.Price, lookup_key=lookup_key)
        if not price:
            price = cls.__create(resource=stripe.Price, product=product, unit_amount=unit_amount, 
                                currency=currency, recurring=recurring, lookup_key=lookup_key)
        return price

    @classmethod
    def start_session(cls, customer, success_url, cancel_url, price):
        if not success_url.endswith("?session_id={CHECKOUT_SESSION_ID}"):
            success_url = success_url + "?session_id={CHECKOUT_SESSION_ID}"
        response = stripe.checkout.Session.create(
                        customer=customer,
                        success_url=success_url,
                        cancel_url=cancel_url,
                        line_items=[{"price": price, "quantity": 1}],
                        mode="subscription",
                    )
        return response.url
    
    @classmethod
    def get_session(cls, session_id):
        response = stripe.checkout.Session.retrieve(id=session_id)
        return response
    
    @classmethod
    def get_subscription(cls, subscription_id):
        reponse = stripe.Subscription.retrieve(id=subscription_id)
        return reponse

    @classmethod
    def get_subscription_info(cls, session_id=None, subscription_id=None):
        # session = cls.get_session(session_id=session_id)
        subscription_id = subscription_id if subscription_id else cls.get_session(session_id=session_id).subscription
        subscription = cls.get_subscription(subscription_id=subscription_id)
        info = {
            'mapped_id': subscription.id,
            'price_id': subscription.plan.id,
            'status': subscription.status,
            'start': timestamp_to_datetime(ts=subscription.current_period_start),
            'end': timestamp_to_datetime(ts=subscription.current_period_end),
            'cancelled': subscription.cancel_at_period_end
        }
        return info

    @classmethod
    def list_subscriptions(cls, **kwargs):
        listing = cls.__list(resource=stripe.Subscription, **kwargs)
        return listing

    @classmethod
    def cancel_subscription(cls, subscription_id, cancel_at_period_end=True):
        try:
            if cancel_at_period_end:
                stripe.Subscription.modify(
                    id=subscription_id,
                    cancel_at_period_end=cancel_at_period_end,
                    cancellation_details={
                        "comment": "User opted",
                        "feedback": "other"
                    }
                )
            else:
                stripe.Subscription.cancel(
                    subscription_exposed_id=subscription_id,
                    cancellation_details={
                        "comment": "User opted",
                        "feedback": "other"
                    }
                )
        except Exception as e:
            print(e)
            return False
        return True
    

