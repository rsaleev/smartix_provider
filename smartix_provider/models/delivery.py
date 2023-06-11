from .base import SmartixModel
from datetime import datetime
from typing import List

class PostOperation(SmartixModel):
    id:str
    date_create:datetime
    state:str
    final_state:bool
    date_update:datetime
    order_number:str
    ext_id:str
    sum:int
    phone:List[str]
    emails:List[str]
    warning:bool
    type:int
    date_delivery:datetime
    organization_id:int
    organization_name:str
    point_id:int
    point_name:str
    postservice_id:int
    postservice_name:str
    extract_client_invoice_id:int
    location_id:int
    location_name:str

class PostOperationDetailed(SmartixModel):
    id:int 
    date_create:datetime
    state:str
    final_state:bool
    date_update:datetime
    ext_id:str
    sum:int
    phones:List[str]
    emails:List[str]
    warning:bool
    type:int
    date_delivery:datetime
    organization_id:int
    organization_name:str
    point_id:int
    point_name:str
    postservice_id:int
    postservice_name:str
    extract_client_invoice_id:int
    location_id:int
    location_name:str
    marketplace_account_id:int
    marketplace_account_name:str
    organization_seller_id:int
    organization_logist_id:int


class SystemInfo(SmartixModel):
    organization_seller_id:int
    organization_seller_name:str
    organization_logist_id:int
    organization_logist_name:str
    organization_postamat_owner_id:int
    organization_postamat_owner_name:str

class Package(SmartixModel):
    id:str
    barcode:str
    weight:int
    height:int
    width:int
    length:int
    post_operation_id:int

class Item(SmartixModel):
    id:str
    name:str
    count:int
    price:int
    discount_sum:int
    subject_type_id:int
    subject_type_name:str
    payment_method_id:int
    payment_method_name:str
    tax_id:int
    tax_name:str

class CartItem(SmartixModel):
    key:str
    data:Item


class Cart(SmartixModel):
    id:str
    prepayment_sum:int
    postpayment_sum:int
    item_sum:int

class PostOperationDetail(SmartixModel):
    post_operation:PostOperationDetailed
    system_info:SystemInfo
    packagings:List[Package]
    cart_items:List[CartItem]