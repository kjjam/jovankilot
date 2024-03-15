from django.conf import settings
from django.db import models
from django.utils import timezone
from hashids import Hashids
from ippanel import Client

sms = Client("lE8apDvStCIW2Pq6HpKduMp3fvNLM_SvpqZJKBL_DkY=")


class Customer(models.Model):
    fullname = models.CharField(max_length=30, null=False, blank=False, verbose_name="نام مشتری")
    number = models.CharField(max_length=11, null=False, blank=False, verbose_name="شماره موبایل مشتری")
    address = models.TextField(max_length=200, null=True, blank=True, verbose_name="آدرس مشتری (غیرالزامی)")

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"

    def __str__(self):
        return self.fullname


class Craftsman(models.Model):
    fullname = models.CharField(max_length=30, verbose_name="اسم کامل")
    number = models.CharField(max_length=11, null=False, blank=False, verbose_name="شماره موبایل")

    class Meta:
        verbose_name = "استادکار"
        verbose_name_plural = "استادکارها"

    def __str__(self):
        return self.fullname


class Request(models.Model):
    STATUS = [
        ("NA", "در انتظار تایید"),
        ("AC", "تایید شده"),
        ("CO", "پایان یافته"),
        ("DE", "رد شده")
    ]
    id = models.AutoField(primary_key=True)
    web_id = models.CharField(max_length=200, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name="مشتری")
    installer = models.ForeignKey(Craftsman, on_delete=models.PROTECT, verbose_name="استادکار")
    request = models.TextField(default='', verbose_name="درخواست های مشتری")
    descriptions = models.TextField(default='', verbose_name="توضیحات استادکار", null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS, default="NA", verbose_name="وضعیت درخواست")
    timing = models.DateTimeField(verbose_name="ساعت و تاریخ برای مراجعه")

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    class Meta:
        verbose_name = "درخواست"
        verbose_name_plural = "درخواست ها"

    def save(self, *args, **kwargs):
        if not self.pk:
            # create time
            self.created = timezone.now()
            self.modified = timezone.now()
            # save object
            super().save(*args, **kwargs)
            # obscure id into webid
            salt = settings.WEB_ID_SALT
            hashids = Hashids(salt=salt, min_length=5)
            self.web_id = hashids.encode(self.id)
        else:
            self.modified = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer} -- {self.installer}"


class SMSPanelPattern(models.Model):
    STAGES = [
        ("WE", "خوش آمد گویی"),
        ("WO", "روال کاری")
    ]

    stage = models.CharField(max_length=2,choices=STAGES, unique=True, null=False, blank=False)
    pattern_code = models.CharField(max_length=30, blank=False, null=False)
    panel_number = models.CharField(max_length=30, blank=False, null=False)
