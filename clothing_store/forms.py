from django import forms

class AddressForm(forms.Form):
    full_name = forms.CharField(label="ชื่อ-นามสกุล", max_length=100)
    address = forms.CharField(label="ที่อยู่", widget=forms.Textarea)
    city = forms.CharField(label="เมือง", max_length=50)
    postal_code = forms.CharField(label="รหัสไปรษณีย์", max_length=10)
    country = forms.CharField(label="ประเทศ", max_length=50)

class PaymentForm(forms.Form):
    PAYMENT_CHOICES = [
        ('credit_card', '💳 บัตรเครดิต'),
        ('paypal', '🅿️ PayPal'),
        ('bank_transfer', '🏦 โอนเงินผ่านธนาคาร'),
    ]
    payment_method = forms.ChoiceField(label="วิธีชำระเงิน", choices=PAYMENT_CHOICES, widget=forms.RadioSelect)

class CheckoutForm(forms.Form):
    full_name = forms.CharField(label="ชื่อ-นามสกุล", max_length=100, required=True)
    address = forms.CharField(label="ที่อยู่", widget=forms.Textarea, required=True)
    payment_method = forms.ChoiceField(
        label="วิธีชำระเงิน",
        choices=[("credit_card", "บัตรเครดิต"), ("paypal", "PayPal"), ("cod", "เก็บเงินปลายทาง")],
        widget=forms.RadioSelect,
    )