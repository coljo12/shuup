# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from shuup.core.models import PaymentStatus, ShipmentStatus, ShippingStatus
from shuup.core.order_creator.signals import order_creator_finished
from shuup.core.signals import (
    payment_created, refund_created, shipment_created, shipment_deleted
)
from shuup.notify import Event, Variable
from shuup.notify.typology import Email, Enum, Language, Model, Phone


class OrderReceived(Event):
    identifier = "order_received"

    order = Variable("Order", type=Model("shuup.Order"))
    customer_email = Variable("Customer Email", type=Email)
    customer_phone = Variable("Customer Phone", type=Phone)
    language = Variable("Language", type=Language)


class ShipmentCreated(Event):
    identifier = "shipment_created"

    order = Variable("Order", type=Model("shuup.Order"))
    customer_email = Variable("Customer Email", type=Email)
    customer_phone = Variable("Customer Phone", type=Phone)
    language = Variable("Language", type=Language)

    shipment = Variable("Shipment", type=Model("shuup.Shipment"))
    shipping_status = Variable("Order Shipping Status",
                               type=Enum(ShippingStatus),
                               help_text=_("Possible values: {0}").format(", ".join(
                                    ["{0}".format(choice) for choice in ShippingStatus]))
                               )
    shippment_status = Variable("Shipment Status",
                                type=Enum(ShipmentStatus),
                                help_text=_("Possible values: {0}").format(", ".join(
                                    ["{0}".format(choice) for choice in ShipmentStatus]))
                                )


class ShipmentDeleted(Event):
    identifier = "shipment_deleted"

    order = Variable("Order", type=Model("shuup.Order"))
    customer_email = Variable("Customer Email", type=Email)
    customer_phone = Variable("Customer Phone", type=Phone)
    language = Variable("Language", type=Language)

    shipment = Variable("Shipment", type=Model("shuup.Shipment"))
    shipping_status = Variable("Order Shipping Status",
                               type=Enum(ShippingStatus),
                               help_text=_("Possible values: {0}").format(", ".join(
                                    ["{0}".format(choice) for choice in ShippingStatus]))
                               )


class PaymentCreated(Event):
    identifier = "payment_created"

    order = Variable("Order", type=Model("shuup.Order"))
    customer_email = Variable("Customer Email", type=Email)
    customer_phone = Variable("Customer Phone", type=Phone)
    language = Variable("Language", type=Language)

    payment_status = Variable("Order Payment Status",
                              type=Enum(PaymentStatus),
                              help_text=_("Possible values: {0}").format(", ".join(
                                    ["{0}".format(choice) for choice in PaymentStatus]))
                              )
    payment = Variable("Order", type=Model("shuup.Payment"))


class RefundCreated(Event):
    identifier = "refund_created"

    order = Variable("Order", type=Model("shuup.Order"))
    customer_email = Variable("Customer Email", type=Email)
    customer_phone = Variable("Customer Phone", type=Phone)
    language = Variable("Language", type=Language)

    payment_status = Variable("Order Payment Status",
                              type=Enum(PaymentStatus),
                              help_text=_("Possible values: {0}").format(", ".join(
                                    ["{0}".format(choice) for choice in PaymentStatus]))
                              )


@receiver(order_creator_finished)
def send_order_received_notification(order, **kwargs):
    OrderReceived(
        order=order,
        customer_email=order.email,
        customer_phone=order.phone,
        language=order.language
    ).run()


@receiver(shipment_created)
def send_shipment_created_notification(order, shipment, **kwargs):
    ShipmentCreated(
        order=order,
        customer_email=order.email,
        customer_phone=order.phone,
        language=order.language,
        shipment=shipment,
        shipping_status=order.shipping_status,
        shippment_status=shipment.status
    ).run()


@receiver(shipment_deleted)
def send_shipment_deleted_notification(shipment, **kwargs):
    ShipmentDeleted(
        order=shipment.order,
        customer_email=shipment.order.email,
        customer_phone=shipment.order.phone,
        language=shipment.order.language,
        shipment=shipment,
        shipping_status=shipment.order.shipping_status
    ).run()


@receiver(payment_created)
def send_payment_created_notification(order, payment, **kwargs):
    PaymentCreated(
        order=order,
        customer_email=order.email,
        customer_phone=order.phone,
        language=order.language,
        payment_status=order.payment_status,
        payment=payment
    ).run()


@receiver(refund_created)
def send_refund_created_notification(order, refund_lines, **kwargs):
    RefundCreated(
        order=order,
        customer_email=order.email,
        customer_phone=order.phone,
        language=order.language,
        payment_status=order.payment_status
    ).run()
