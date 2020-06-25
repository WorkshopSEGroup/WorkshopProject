import os
from datetime import datetime

from peewee import *

abs_path = os.path.dirname(os.path.abspath(__file__))
test_rel_path = os.path.join(abs_path, 'testing.db')
project_rel_path = os.path.join(abs_path, 'project.db')

# Use test_rel_path while testing only.
rel_path = test_rel_path
database = SqliteDatabase(rel_path, pragmas={'journal_mode': 'wal', 'foreign_keys': 1})


def create_tables():
    """
    Should happen once, only when the DB is empty.
    """
    tables = [Statistic, User, Store, Product, StoreManagerAppointment, StoreOwnerAppointment,
              ProductsInBasket, Purchase, ProductsInPurchase]
    return database.create_tables(tables)


class BaseModel(Model):
    class Meta:
        database = database


class Statistic(BaseModel):
    """
    table: statistic
    """
    date = DateTimeField(primary_key=True, default=datetime(datetime.now().year, datetime.now().month,
                                                            datetime.now().day))
    guests = IntegerField(null=False, default=0)
    subscribers = IntegerField(null=False, default=0)
    store_managers = IntegerField(null=False, default=0)
    store_owners = IntegerField(null=False, default=0)
    system_managers = IntegerField(null=False, default=0)


class User(BaseModel):
    """
    table: user
    """
    username = CharField(primary_key=True)
    password = CharField(null=False)
    is_system_manager = BooleanField(null=False, default=False)


class Store(BaseModel):
    """
    table: store
    """
    store_name = CharField(unique=True, null=False, primary_key=True)
    founder_username = ForeignKeyField(User, deferrable="INITIALLY DEFERRED", db_column="founder_username",
                                       to_field="username", on_delete="Cascade", on_update="Cascade")


class Product(BaseModel):
    """
    table: product
    """
    product_id = IntegerField(primary_key=True)
    product_name = CharField(null=False)
    store_name = ForeignKeyField(Store, db_column="store_name", on_delete="Cascade", on_update="Cascade")
    price = FloatField(null=False)
    category = CharField(null=False)
    amount = IntegerField(null=False, constraints=[Check('amount >= 0')])
    purchase_type = IntegerField(null=False)

    class Meta:
        indexes = (
            (("product_name", "store_name"), True),
        )


class StoreManagerAppointment(BaseModel):
    """
    table: store manager appointments
    """
    appointee_username = ForeignKeyField(User, db_column="appointee_username", on_delete="Cascade",
                                         on_update="Cascade")
    store_name = ForeignKeyField(Store, db_column="store_name", on_delete="Cascade", on_update="Cascade")
    appointer_username = ForeignKeyField(User, db_column="appointer_username", on_delete="Cascade",
                                         on_update="Cascade")
    can_edit_inventory = BooleanField(null=False, default=False)
    can_edit_policies = BooleanField(null=False, default=False)
    can_appoint_owner = BooleanField(null=False, default=False)
    can_delete_owner = BooleanField(null=False, default=False)
    can_appoint_manager = BooleanField(null=False, default=False)
    can_edit_manager_permissions = BooleanField(null=False, default=False)
    can_delete_manager = BooleanField(null=False, default=False)
    can_close_store = BooleanField(null=False, default=False)
    can_answer_user_questions = BooleanField(null=False, default=False)
    can_watch_purchase_history = BooleanField(null=False, default=False)

    class Meta:
        primary_key = CompositeKey("appointee_username", "store_name")


class StoreOwnerAppointment(BaseModel):
    """
    table: store owner appointment
    """
    appointee_username = ForeignKeyField(User, db_column="appointee_username", on_delete="Cascade",
                                         on_update="Cascade")
    store_name = ForeignKeyField(Store, db_column="store_name", on_delete="Cascade", on_update="Cascade")
    appointer_username = ForeignKeyField(User, db_column="appointer_username", on_delete="Cascade",
                                         on_update="Cascade")

    class Meta:
        primary_key = CompositeKey("appointee_username", "store_name")


class ProductsInBasket(BaseModel):
    """
    table: products in basket
    """
    username = ForeignKeyField(User, db_column="username", on_delete="Cascade",
                               on_update="Cascade")
    product_ref = ForeignKeyField(Product, db_column="product_ref", on_delete="Cascade", on_update="Cascade")
    amount = IntegerField(null=False, constraints=[Check('amount >= 0')])

    class Meta:
        primary_key = CompositeKey("username", "product_ref")


class Purchase(BaseModel):
    """
    table: purchase
    """

    purchase_id = IntegerField(primary_key=True)
    username = ForeignKeyField(User, db_column="username", on_delete="Cascade", on_update="Cascade")
    store_name = ForeignKeyField(Store, db_column="store_name", on_delete="Cascade", on_update="Cascade")
    # product_name = CharField(null=False)
    # product_purchase_price = FloatField(null=False)  # Not the same as the product.price due to policies.
    # amount = IntegerField(null=False)
    total_price = FloatField(null=False)
    date = DateTimeField(null=False, default=datetime.now())


class ProductsInPurchase(BaseModel):
    """
    table: products in purchase
    """
    purchase_id = ForeignKeyField(Purchase, null=False, db_column="purchase_id", on_delete="Cascade",
                                  on_update="Cascade")
    product_name = CharField(null=False)
    # store_name = CharField(null=False)
    product_purchase_price = FloatField(null=False)  # Not the same as the product.price due to policies.
    amount = IntegerField(null=False, constraints=[Check('amount >= 0')])

    class Meta:
        primary_key = CompositeKey("purchase_id", "product_name")


class DiscountPolicy(BaseModel):
    """
    table: discount policy
    """
    discount_policy_id = IntegerField(primary_key=True)
    policy_name = CharField(null=False)
    store_name = ForeignKeyField(Store, db_column="store_name", on_update="Cascade", on_delete="Cascade")
    product_name = CharField(null=False)
    percentage = FloatField(null=False)
    valid_until = DateTimeField(null=False)
    is_active = BooleanField(null=False, default=True)

    class Meta:
        indexes = (
            (("policy_name", "store_name"), True),

        )


class ConditionalDiscountPolicy(BaseModel):
    """
    table: conditional discount policy
    """
    policy_ref = ForeignKeyField(DiscountPolicy, null=False, db_column="policy_ref", on_delete="Cascade",
                                 on_update="Cascade", primary_key=True)
    precondition_product = CharField(null=False)
    precondition_min_amount = CharField(null=True, default=None)
    precondition_min_basket_price = CharField(null=True, default=None)


class CompositeDiscountPolicy(BaseModel):
    """
    table: composite discount policy
    """
    policy_ref = ForeignKeyField(DiscountPolicy, null=False, db_column="policy_ref",
                                 on_update="Cascade", on_delete="Cascade", primary_key=True)
    policy1_ref = ForeignKeyField(DiscountPolicy, null=False, db_column="policy1_ref",
                                  on_update="Cascade", on_delete="Cascade")
    policy2_ref = ForeignKeyField(DiscountPolicy, null=False, db_column="policy2_ref",
                                  on_update="Cascade", on_delete="Cascade")
    flag = IntegerField(null=False)
