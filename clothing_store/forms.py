from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # ✅ ใช้ CustomUser แทน auth.User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="อีเมล")

    class Meta:
        model = CustomUser  # ✅ ใช้ CustomUser แทน auth.User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("อีเมลนี้ถูกใช้ไปแล้ว กรุณาใช้อีเมลอื่น")
        return email


class AddressForm(forms.Form):
    full_name = forms.CharField(label="ชื่อ-นามสกุล", max_length=100, required=True)
    phone_number = forms.CharField(label="เบอร์โทรศัพท์", max_length=15, required=True)
    address = forms.CharField(label="ที่อยู่", widget=forms.Textarea(attrs={'rows': 3}), required=True)
    city = forms.CharField(label="เมือง", max_length=50, required=True)
    postal_code = forms.CharField(label="รหัสไปรษณีย์", max_length=10, required=True)
    country = forms.CharField(label="ประเทศ", max_length=50, required=True)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit():
            raise forms.ValidationError("เบอร์โทรศัพท์ต้องเป็นตัวเลขเท่านั้น")
        return phone_number

class PaymentForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit_card', '💳 บัตรเครดิต'),
        ('paypal', '🅿️ PayPal'),
        ('bank_transfer', '🏦 โอนเงินผ่านธนาคาร'),
        ('cod', '💰 เก็บเงินปลายทาง')
    ]
    payment_method = forms.ChoiceField(label="วิธีชำระเงิน", choices=PAYMENT_CHOICES, widget=forms.RadioSelect, required=True)
    
    card_number = forms.CharField(label="หมายเลขบัตรเครดิต", max_length=16, required=False, min_length=16)
    expiry_date = forms.CharField(label="วันหมดอายุ (MM/YY)", max_length=5, required=False)
    cvv = forms.CharField(label="CVV", max_length=4, required=False, min_length=3)

    def clean_card_number(self):
        card_number = self.cleaned_data.get("card_number")
        if card_number and (not card_number.isdigit() or len(card_number) != 16):
            raise forms.ValidationError("หมายเลขบัตรเครดิตต้องเป็นตัวเลข 16 หลัก")
        return card_number

    def clean_cvv(self):
        cvv = self.cleaned_data.get("cvv")
        if cvv and (not cvv.isdigit() or len(cvv) not in [3, 4]):
            raise forms.ValidationError("CVV ต้องเป็นตัวเลข 3 หรือ 4 หลัก")
        return cvv

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get("expiry_date")
        if expiry_date:
            import re
            if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', expiry_date):
                raise forms.ValidationError("วันหมดอายุต้องอยู่ในรูปแบบ MM/YY")
        return expiry_date

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get("payment_method")

        if payment_method == "credit_card":
            if not cleaned_data.get("card_number") or not cleaned_data.get("expiry_date") or not cleaned_data.get("cvv"):
                raise forms.ValidationError("กรุณากรอกข้อมูลบัตรเครดิตให้ครบถ้วน")

        return cleaned_data

class CheckoutForm(forms.Form):
    full_name = forms.CharField(label="ชื่อ-นามสกุล", max_length=100, required=True)
    email = forms.EmailField(label="อีเมล", required=True)
    address = forms.CharField(label="ที่อยู่", widget=forms.Textarea(attrs={'rows': 3}), required=True)
    phone_number = forms.CharField(label="เบอร์โทรศัพท์", max_length=15, required=True)
    note = forms.CharField(label="หมายเหตุ (ถ้ามี)", widget=forms.Textarea(attrs={'rows': 2}), required=False)

    payment_method = forms.ChoiceField(
        label="วิธีชำระเงิน",
        choices=[
            ("credit_card", "บัตรเครดิต"),
            ("paypal", "PayPal"),
            ("bank_transfer", "โอนเงินผ่านธนาคาร"),
            ("cod", "เก็บเงินปลายทาง"),
        ],
        widget=forms.RadioSelect,
        required=True,
    )
