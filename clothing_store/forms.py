from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import CustomUser  # ✅ Import CustomUser
class CheckoutForm(forms.Form):
    fullname = forms.CharField(
        max_length=255,
        required=True,
        error_messages={'required': 'กรุณากรอกชื่อ-นามสกุล'}
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        required=True,
        error_messages={'required': 'กรุณากรอกที่อยู่'}
    )

    phone_number = forms.RegexField(
        regex=r'^\d{10}$',
        error_messages={
            'invalid': 'เบอร์โทรศัพท์ต้องมี 10 หลักและเป็นตัวเลขเท่านั้น',
            'required': 'กรุณากรอกเบอร์โทรศัพท์'
        }
    )

    postal_code = forms.RegexField(
        regex=r'^\d{5}$',
        error_messages={
            'invalid': 'รหัสไปรษณีย์ต้องมี 5 หลักและเป็นตัวเลขเท่านั้น',
            'required': 'กรุณากรอกรหัสไปรษณีย์'
        }
    )

    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'บัตรเครดิต'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'โอนเงินผ่านธนาคาร'),
        ('cash_on_delivery', 'เก็บเงินปลายทาง')
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        required=True,
        error_messages={'required': 'กรุณาเลือกวิธีการชำระเงิน'}
    )

    # ✅ ตรวจสอบหมายเลขบัตรเครดิตเฉพาะเมื่อเลือก "บัตรเครดิต"
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get("payment_method")
        card_number = cleaned_data.get("credit_card_number")

        if payment_method == "credit_card":
            if not card_number:
                self.add_error("credit_card_number", "กรุณากรอกหมายเลขบัตรเครดิต")
            elif not re.match(r"^\d{16}$", card_number):
                self.add_error("credit_card_number", "หมายเลขบัตรเครดิตต้องเป็นตัวเลข 16 หลัก")

        return cleaned_data
    

    # ✅ ตรวจสอบหมายเลขบัตรเครดิตเฉพาะเมื่อเลือกบัตรเครดิต
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get("payment_method")
        card_number = cleaned_data.get("credit_card_number")

        # ถ้าเลือกบัตรเครดิต ต้องกรอกหมายเลขบัตร
        if payment_method == "credit_card":
            if not card_number:
                self.add_error("credit_card_number", "กรุณากรอกหมายเลขบัตรเครดิต")
            elif not re.match(r"^\d{16}$", card_number):
                self.add_error("credit_card_number", "หมายเลขบัตรเครดิตต้องเป็นตัวเลข 16 หลัก")

        return cleaned_data

# ✅ แก้ไขให้ Import `UserCreationForm` และ `CustomUser`
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="อีเมล")

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
